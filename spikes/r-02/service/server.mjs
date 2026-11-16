// R-02 spike: the permission service. One dependency (pg). See CONTRACT.md.
//
// The service holds no permission logic of its own. For every agent call it opens a
// transaction as the unprivileged database role, presents the caller's token to
// brain.begin_session(), and runs plain queries; row-level security decides what comes
// back and what may be written. MCP is spoken by hand as JSON-RPC over HTTP.
import http from "node:http";
import crypto from "node:crypto";
import fs from "node:fs";
import pg from "pg";

const PORT = Number(process.env.PORT || 8900);
const HOST = process.env.HOST || "127.0.0.1";
const SOCKET = process.env.LISTEN_SOCKET || "";
const ADMIN_TOKEN = process.env.BRAIN_ADMIN_TOKEN || "";
const app = new pg.Pool({ connectionString: process.env.BRAIN_APP_DSN, max: 8 });
const owner = new pg.Pool({ connectionString: process.env.BRAIN_OWNER_DSN, max: 4 });
if (!ADMIN_TOKEN || !process.env.BRAIN_APP_DSN || !process.env.BRAIN_OWNER_DSN) {
  console.error("BRAIN_ADMIN_TOKEN, BRAIN_APP_DSN and BRAIN_OWNER_DSN are required");
  process.exit(2);
}

const sha = (s) => crypto.createHash("sha256").update(s).digest("hex");
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
class ToolError extends Error { constructor(code) { super(code); this.code = code; } }
const clean = (v, max) => {
  if (typeof v !== "string" || v.includes("\u0000")) throw new ToolError("invalid_arguments");
  if (v.length > max) throw new ToolError("invalid_arguments");
  return v;
};
const likePattern = (q) => "%" + q.replace(/[\\%_]/g, (c) => "\\" + c) + "%";
const limitOf = (v) => Math.max(1, Math.min(200, Number.isInteger(v) ? v : 50));

// One transaction bound to the token's organization. Everything an agent does goes through here.
async function withSession(token, fn) {
  const c = await app.connect();
  try {
    await c.query("begin");
    const who = (await c.query("select * from brain.begin_session($1)", [token])).rows[0];
    const out = await fn(c, who);
    await c.query("commit");
    return out;
  } catch (e) {
    await c.query("rollback").catch(() => {});
    throw e;
  } finally {
    c.release();
  }
}

const LIST_COLS = "id, org_id as org, title, kind, source_type, path";
const TOOLS = {
  brain_whoami: {
    description: "Say which organization this caller acts for.",
    readOnly: true, props: {}, required: [],
    run: async (c, who) => ({ org: who.org, kind: who.kind, actor: who.actor }),
  },
  brain_list: {
    description: "List the pages this caller may read. Optional filters: source_type (human, agent, codebase), kind.",
    readOnly: true,
    props: { source_type: { type: "string" }, kind: { type: "string" }, limit: { type: "integer" } }, required: [],
    run: async (c, who, a) => {
      const st = a.source_type == null ? null : clean(a.source_type, 20), kind = a.kind == null ? null : clean(a.kind, 20);
      const where = "($1::text is null or source_type = $1) and ($2::text is null or kind = $2)";
      const count = (await c.query(`select count(*)::int as n from brain.pages where ${where}`, [st, kind])).rows[0].n;
      const pages = (await c.query(`select ${LIST_COLS} from brain.pages where ${where} order by org_id, coalesce(path, title) limit $3`, [st, kind, limitOf(a.limit)])).rows;
      return { count, pages };
    },
  },
  brain_search: {
    description: "Search the title, body and path of the pages this caller may read.",
    readOnly: true,
    props: { query: { type: "string" }, source_type: { type: "string" }, limit: { type: "integer" } }, required: ["query"],
    run: async (c, who, a) => {
      const q = clean(a.query, 10000);
      if (!q.trim()) throw new ToolError("invalid_arguments");
      const st = a.source_type == null ? null : clean(a.source_type, 20);
      const where = "(title ilike $1 escape '\\' or body ilike $1 escape '\\' or path ilike $1 escape '\\') and ($2::text is null or source_type = $2)";
      const args = [likePattern(q.slice(0, 500)), st];
      const count = (await c.query(`select count(*)::int as n from brain.pages where ${where}`, args)).rows[0].n;
      const pages = (await c.query(`select ${LIST_COLS}, left(body, 300) as snippet from brain.pages where ${where} order by org_id, coalesce(path, title) limit $3`, [...args, limitOf(a.limit)])).rows;
      return { count, pages };
    },
  },
  brain_get: {
    description: "Fetch one page by id or by path.",
    readOnly: true,
    props: { id: { type: "string" }, path: { type: "string" } }, required: [],
    run: async (c, who, a) => {
      let row;
      if (a.id != null) {
        const id = clean(a.id, 10000);
        if (!UUID.test(id)) throw new ToolError("not_found");
        row = (await c.query("select id, org_id as org, title, body, kind, source_type, sensitivity, visibility, path, meta, updated_at from brain.pages where id = $1", [id])).rows[0];
      } else if (a.path != null) {
        const p = clean(a.path, 10000);
        row = (await c.query("select id, org_id as org, title, body, kind, source_type, sensitivity, visibility, path, meta, updated_at from brain.pages where path = $1 order by org_id limit 1", [p.slice(0, 1000)])).rows[0];
      } else throw new ToolError("invalid_arguments");
      if (!row) throw new ToolError("not_found"); // a page the caller may not read looks exactly like no page
      return { page: row };
    },
  },
  brain_write: {
    description: "Add a note or a summary to this caller's own organization.",
    readOnly: false,
    props: { title: { type: "string" }, body: { type: "string" }, kind: { type: "string", enum: ["note", "summary"] },
             sensitivity: { type: "string", enum: ["normal", "health", "finance"] }, visibility: { type: "string", enum: ["org", "global"] } },
    required: ["title", "body"],
    run: async (c, who, a) => {
      const row = await c.query(
        `insert into brain.pages (org_id, org_kind, title, body, kind, sensitivity, visibility, source_type)
         values ($1, $2, $3, $4, $5, $6, $7, $8) returning id`,
        [who.org, who.kind, clean(a.title, 300), clean(a.body, 200000), a.kind == null ? "note" : clean(a.kind, 20),
         a.sensitivity == null ? "normal" : clean(a.sensitivity, 20), a.visibility == null ? "org" : clean(a.visibility, 20),
         who.actor === "human" ? "human" : "agent"]);
      return { id: row.rows[0].id };
    },
  },
  publish_briefing: {
    description: "Personal space only: offer a short curated briefing to the holding organization. A human must approve it before anyone there can read it.",
    readOnly: false,
    props: { content: { type: "string" } }, required: ["content"],
    run: async (c, who, a) => {
      const content = clean(a.content, 2000);
      if (!content.trim()) throw new ToolError("invalid_arguments");
      if (who.kind !== "personal") throw new ToolError("forbidden");
      if (!(await c.query("select brain.feature('briefing') as on")).rows[0].on) throw new ToolError("disabled");
      const row = await c.query("insert into brain.briefings (from_org, to_org, content) values ($1, brain.holding_org(), $2) returning id", [who.org, content]);
      return { briefing_id: row.rows[0].id, status: "pending" };
    },
  },
};

function toolList() {
  return Object.entries(TOOLS).map(([name, t]) => ({
    name, description: t.description,
    inputSchema: { type: "object", properties: { ...t.props, request_id: { type: "string" } }, required: t.required },
    annotations: { readOnlyHint: t.readOnly, destructiveHint: false, idempotentHint: t.readOnly, openWorldHint: false },
  }));
}

const DB_DENIALS = { "42501": "forbidden", "23514": "forbidden", "23503": "forbidden", "23505": "forbidden", "22P02": "invalid_arguments", "22001": "invalid_arguments", "22021": "invalid_arguments" };

async function audit(token, tool, requestId, decision, reason, args) {
  const argsSha = sha(JSON.stringify(args ?? {}));
  const c = await app.connect();
  try {
    await c.query("begin");
    if (token != null) await c.query("select brain.begin_session($1)", [token]).catch(async () => { await c.query("rollback"); await c.query("begin"); });
    await c.query("select brain.audit_log($1, $2, $3, $4, $5)", [tool, requestId, decision, reason, argsSha]);
    await c.query("commit");
  } catch (e) {
    await c.query("rollback").catch(() => {});
    console.error("AUDIT WRITE FAILED", e.message); // a real build must fail the call here
  } finally { c.release(); }
}

async function callTool(token, name, args) {
  const tool = TOOLS[name];
  const a = args && typeof args === "object" && !Array.isArray(args) ? args : {};
  const requestId = typeof a.request_id === "string" ? a.request_id.slice(0, 100) : null;
  if (!tool) { await audit(token, String(name).slice(0, 60), requestId, "deny", "unknown_tool", a); return { isError: true, payload: { error: "invalid_arguments" } }; }
  try {
    const payload = await withSession(token, async (c, who) => {
      const out = await tool.run(c, who, a);
      await c.query("select brain.audit_log($1, $2, 'allow', null, $3)", [name, requestId, sha(JSON.stringify(a))]);
      return out; // the action and its audit row commit together
    });
    return { isError: false, payload };
  } catch (e) {
    if (e.code === "28000") throw e;
    const code = e instanceof ToolError ? e.code : DB_DENIALS[e.code];
    if (!code) { console.error("tool failure", name, e.code, e.message); }
    await audit(token, name, requestId, "deny", code || "internal_error", a);
    return { isError: true, payload: { error: code || "internal_error" } };
  }
}

async function rpc(token, msg) {
  const { id, method, params } = msg || {};
  const ok = (result) => ({ jsonrpc: "2.0", id, result });
  if (method === "initialize") {
    return ok({ protocolVersion: (params && params.protocolVersion) || "2025-06-18", capabilities: { tools: { listChanged: false } },
                serverInfo: { name: "azi-permission-service-spike", version: "0.0.1" } });
  }
  if (typeof method === "string" && method.startsWith("notifications/")) return null;
  if (method === "ping") return ok({});
  if (method === "tools/list") return ok({ tools: toolList() });
  if (method === "tools/call") {
    const r = await callTool(token, params && params.name, params && params.arguments);
    return ok({ content: [{ type: "text", text: JSON.stringify(r.payload) }], isError: r.isError });
  }
  return { jsonrpc: "2.0", id: id ?? null, error: { code: -32601, message: "method not found" } };
}

// Admin: the human's console in the spike -------------------------------------------------------

async function adminRoute(path, query, body) {
  const c = await owner.connect();
  try {
    await c.query("begin");
    let out = {};
    if (path === "/admin/reset") {
      await c.query("truncate brain.pages, brain.briefings, brain.principals, brain.sessions, brain.orgs cascade");
      const s = body.settings || {};
      await c.query("update brain.settings set personal_enabled = $1, briefing_enabled = $2, holding_reads = $3",
        [s.personal_enabled !== false, s.briefing_enabled !== false, s.holding_reads || "all"]);
      const orgs = [...(body.orgs || [])].sort((x, y) => (x.parent ? 1 : 0) - (y.parent ? 1 : 0));
      for (const o of orgs) await c.query("insert into brain.orgs (id, kind, parent_id) values ($1, $2, $3)", [o.id, o.kind, o.parent || null]);
      for (const p of body.principals || []) await c.query("insert into brain.principals (token_sha256, org_id, actor) values ($1, $2, $3)", [sha(p.token), p.org, p.actor]);
      const kinds = Object.fromEntries(orgs.map((o) => [o.id, o.kind]));
      for (const p of body.pages || []) {
        await c.query(`insert into brain.pages (org_id, org_kind, title, body, kind, source_type, sensitivity, visibility, path)
                       values ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
          [p.org, kinds[p.org], p.title, p.body || "", p.kind || "note", p.source_type || "human", p.sensitivity || "normal", p.visibility || "org", p.path || null]);
      }
      out = { orgs: orgs.length, pages: (body.pages || []).length };
    } else if (path === "/admin/settings") {
      for (const k of ["personal_enabled", "briefing_enabled", "holding_reads"]) {
        if (k in body) await c.query(`update brain.settings set ${k} = $1`, [body[k]]);
      }
      out = (await c.query("select personal_enabled, briefing_enabled, holding_reads from brain.settings")).rows[0];
    } else if (path === "/admin/approve_briefing") {
      out = { page_id: (await c.query("select brain.approve_briefing($1, $2) as id", [body.briefing_id, String(body.approver || "")])).rows[0].id };
    } else if (path === "/admin/codebase_sync") {
      const kind = (await c.query("select kind from brain.orgs where id = $1", [body.org])).rows[0]?.kind;
      if (!kind) throw new Error("unknown organization");
      let written = 0, deleted = 0;
      for (const p of body.upserts || []) {
        const r = await c.query(
          `insert into brain.pages (org_id, org_kind, title, body, kind, source_type, path, content_sha, meta)
           values ($1, $2, $3, $4, $5, 'codebase', $6, $7, $8)
           on conflict (org_id, path) where path is not null
           do update set title = excluded.title, body = excluded.body, kind = excluded.kind, content_sha = excluded.content_sha,
                         meta = excluded.meta, updated_at = now()
           where brain.pages.content_sha is distinct from excluded.content_sha`,
          [body.org, kind, p.title, p.body, p.kind || "code_file", p.path, p.content_sha, JSON.stringify(p.meta || {})]);
        written += r.rowCount;
      }
      for (const path_ of body.deletes || []) {
        deleted += (await c.query("delete from brain.pages where org_id = $1 and path = $2 and source_type = 'codebase'", [body.org, path_])).rowCount;
      }
      out = { written, deleted };
    } else if (path === "/admin/audit") {
      out = { rows: (await c.query("select id::int as id, ts, org, actor, tool, request_id, decision, reason from brain.audit where id > $1 order by id", [Number(query.get("since_id") || 0)])).rows };
    } else if (path === "/admin/pages_digest") {
      out = { rows: (await c.query("select path, content_sha, updated_at from brain.pages where org_id = $1 and source_type = $2 order by path", [query.get("org"), query.get("source_type") || "codebase"])).rows };
    } else {
      await c.query("rollback");
      return null;
    }
    await c.query("commit");
    return out;
  } catch (e) {
    await c.query("rollback").catch(() => {});
    throw e;
  } finally { c.release(); }
}

function send(res, status, obj, headers = {}) {
  const text = obj == null ? "" : JSON.stringify(obj);
  res.writeHead(status, { "content-type": "application/json", "cache-control": "no-store", ...headers });
  res.end(text);
}
const bearer = (req) => {
  const h = req.headers.authorization || req.headers["x-brain-token"] || "";
  const m = /^Bearer\s+(.+)$/i.exec(Array.isArray(h) ? h[0] : h);
  return m ? m[1].trim() : (typeof h === "string" && h.trim() ? h.trim() : null);
};
const sameToken = (a, b) => a != null && a.length === b.length && crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  try {
    if (req.method === "GET" && url.pathname === "/healthz") return send(res, 200, { ok: true });
    let raw = "";
    for await (const chunk of req) { raw += chunk; if (raw.length > 30_000_000) return send(res, 413, { error: "too_large" }); }
    let body = {};
    if (raw) { try { body = JSON.parse(raw); } catch { return send(res, 400, { error: "invalid_json" }); } }
    const token = bearer(req);

    if (url.pathname.startsWith("/admin/")) {
      if (!sameToken(token, ADMIN_TOKEN)) return send(res, 401, { error: "unauthorized" });
      const out = await adminRoute(url.pathname, url.searchParams, body);
      return out == null ? send(res, 404, { error: "not_found" }) : send(res, 200, out);
    }

    if (url.pathname === "/mcp") {
      if (req.method !== "POST") return send(res, 405, { error: "method_not_allowed" }, { allow: "POST" });
      // Every MCP request needs a valid token, including initialize and tools/list.
      try {
        if (token == null || token.includes("\u0000")) throw Object.assign(new Error("invalid_token"), { code: "28000" });
        await withSession(token, async () => {});
      } catch (e) {
        if (e.code !== "28000") throw e;
        await audit(null, "auth", null, "deny", "invalid_token", {});
        return send(res, 401, { error: "unauthorized" }, { "www-authenticate": "Bearer" });
      }
      const batch = Array.isArray(body) ? body : [body];
      const replies = [];
      for (const msg of batch) { const r = await rpc(token, msg); if (r) replies.push(r); }
      if (replies.length === 0) { res.writeHead(202); return res.end(); }
      return send(res, 200, Array.isArray(body) ? replies : replies[0]);
    }
    return send(res, 404, { error: "not_found" });
  } catch (e) {
    console.error("request failed", req.method, url.pathname, e.code || "", e.message);
    return send(res, 500, { error: "internal_error" });
  }
});

server.listen(PORT, HOST, () => console.error(`listening on http://${HOST}:${PORT}`));
if (SOCKET) {
  // A second listener on a Unix socket, so a harness outside a no-network jail can reach the service inside it.
  try { fs.unlinkSync(SOCKET); } catch {}
  const viaSocket = http.createServer((req, res) => server.emit("request", req, res));
  viaSocket.listen(SOCKET, () => { fs.chmodSync(SOCKET, 0o777); console.error("listening on socket", SOCKET); });
}
