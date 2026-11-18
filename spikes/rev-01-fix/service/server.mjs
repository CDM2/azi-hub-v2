// REV-01 fix pass: the permission service. One dependency (pg). See CONTRACT.md.
//
// The service holds no permission logic. For every call it opens a transaction as the
// unprivileged database role, presents the caller's token to brain.begin_session(), and calls
// one database function. That function decides what comes back and writes the log row for an
// allowed call in the same transaction. The role cannot read or write any table directly.
// MCP is spoken by hand as JSON-RPC over HTTP.
import http from "node:http";
import crypto from "node:crypto";
import fs from "node:fs";
import pg from "pg";

const PORT = Number(process.env.PORT || 8900);
const HOST = process.env.HOST || "127.0.0.1";
const SOCKET = process.env.LISTEN_SOCKET || "";
const ADMIN_TOKEN = process.env.BRAIN_ADMIN_TOKEN || "";
if (!ADMIN_TOKEN || !process.env.BRAIN_APP_DSN || !process.env.BRAIN_OWNER_DSN) {
  console.error("BRAIN_ADMIN_TOKEN, BRAIN_APP_DSN and BRAIN_OWNER_DSN are required");
  process.exit(2);
}
const app = new pg.Pool({ connectionString: process.env.BRAIN_APP_DSN, max: 8 });
const owner = new pg.Pool({ connectionString: process.env.BRAIN_OWNER_DSN, max: 4 });

const sha = (s) => crypto.createHash("sha256").update(s).digest("hex");
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const CONTROL = /[\u0000-\u001f\u007f]/;
const printable = (v, max) => String(v).replace(/[\u0000-\u001f\u007f]/g, "?").slice(0, max);
class ToolError extends Error { constructor(code) { super(code); this.code = code; } }
class AdminError extends Error { constructor(status, code, detail) { super(code); this.status = status; this.code = code; this.detail = detail; } }
const clean = (v, max) => {
  if (typeof v !== "string" || v.includes("\u0000")) throw new ToolError("invalid_arguments");
  if (v.length > max) throw new ToolError("invalid_arguments");
  return v;
};
const optional = (v, max) => (v == null ? null : clean(v, max));
const uuidOr = (v, code) => { const s = clean(v, 10000); if (!UUID.test(s)) throw new ToolError(code); return s; };
const limitOf = (v) => (Number.isInteger(v) ? Math.max(1, Math.min(200, v)) : null);
const decisionOf = (v) => { const d = v == null ? "approve" : clean(v, 20); if (d !== "approve" && d !== "reject") throw new ToolError("invalid_arguments"); return d; };

// One transaction bound to the token's organization. Everything a caller does goes through here.
async function withSession(token, fn) {
  const c = await app.connect();
  try {
    await c.query("begin");
    await c.query("select brain.begin_session($1)", [token]);
    const out = await fn(c);
    await c.query("commit");
    return out;
  } catch (e) {
    await c.query("rollback").catch(() => {});
    throw e;
  } finally {
    c.release();
  }
}
const one = async (c, sql, args) => (await c.query(`select ${sql} as r`, args)).rows[0].r;

// Each tool is one database function. `rid` is the caller's request id and `h` the hash of its arguments; both go into the log row.
const TOOLS = Object.assign(Object.create(null), {
  brain_whoami: {
    description: "Say which organization, and which person if any, this caller acts for.",
    readOnly: true, props: {}, required: [],
    run: (c, a, rid, h) => one(c, "brain.t_whoami($1, $2)", [rid, h]),
  },
  brain_list: {
    description: "List the pages this caller may read. Optional filters: source_type (human, agent, codebase), kind.",
    readOnly: true,
    props: { source_type: { type: "string" }, kind: { type: "string" }, limit: { type: "integer" } }, required: [],
    run: (c, a, rid, h) => one(c, "brain.t_list($1, $2, $3, $4, $5)", [rid, h, optional(a.source_type, 20), optional(a.kind, 20), limitOf(a.limit)]),
  },
  brain_search: {
    description: "Search the title, body and path of the pages this caller may read.",
    readOnly: true,
    props: { query: { type: "string" }, source_type: { type: "string" }, limit: { type: "integer" } }, required: ["query"],
    run: (c, a, rid, h) => one(c, "brain.t_search($1, $2, $3, $4, $5)", [rid, h, clean(a.query, 10000), optional(a.source_type, 20), limitOf(a.limit)]),
  },
  brain_get: {
    description: "Fetch one page by id or by path. `org` narrows the lookup to one organization this caller may already read.",
    readOnly: true,
    props: { id: { type: "string" }, path: { type: "string" }, org: { type: "string" } }, required: [],
    run: (c, a, rid, h) => {
      const org = typeof a.org === "string" && !a.org.includes("\u0000") && a.org.length <= 200 ? a.org : null;
      if (a.id != null) return one(c, "brain.t_get($1, $2, $3, null, $4)", [rid, h, uuidOr(a.id, "not_found"), org]);
      if (a.path != null) return one(c, "brain.t_get($1, $2, null, $3, $4)", [rid, h, clean(a.path, 10000), org]);
      throw new ToolError("invalid_arguments");
    },
  },
  brain_write: {
    description: "Add a note or a summary to this caller's own organization. A global page waits for a person's approval unless a person who controls the organization wrote it.",
    readOnly: false,
    props: { title: { type: "string" }, body: { type: "string" }, kind: { type: "string", enum: ["note", "summary"] },
             sensitivity: { type: "string", enum: ["normal", "health", "finance"] }, visibility: { type: "string", enum: ["org", "global"] } },
    required: ["title", "body"],
    run: (c, a, rid, h) => one(c, "brain.t_write($1, $2, $3, $4, $5, $6, $7)",
      [rid, h, clean(a.title, 300), clean(a.body, 200000), optional(a.kind, 20), optional(a.sensitivity, 20), optional(a.visibility, 20)]),
  },
  publish_briefing: {
    description: "Personal space only: offer a short briefing (2,000 characters at most) to an organization the person belongs to. `to` names it; without `to` it goes to the one top-level organization the person owns. The person must approve it before anyone there can read it.",
    readOnly: false,
    props: { content: { type: "string" }, to: { type: "string" } }, required: ["content"],
    run: (c, a, rid, h) => one(c, "brain.t_publish_briefing($1, $2, $3, $4)", [rid, h, clean(a.content, 2000), optional(a.to, 200)]),
  },
  push_to_parent: {
    description: "Sub-organization only: offer a short report (2,000 characters at most) to the organization above. A person who controls this organization must approve it first.",
    readOnly: false,
    props: { content: { type: "string" } }, required: ["content"],
    run: (c, a, rid, h) => one(c, "brain.t_push_to_parent($1, $2, $3)", [rid, h, clean(a.content, 2000)]),
  },
  pending_approvals: {
    description: "A person's token only: the pushes and global pages waiting for this person's decision, with their text.",
    readOnly: true, props: {}, required: [],
    run: (c, a, rid, h) => one(c, "brain.t_pending_approvals($1, $2)", [rid, h]),
  },
  approve_push: {
    description: "A person's token only: approve or reject a pending push. `decision` is approve (default) or reject.",
    readOnly: false,
    props: { push_id: { type: "string" }, decision: { type: "string", enum: ["approve", "reject"] } }, required: ["push_id"],
    run: (c, a, rid, h) => one(c, "brain.t_decide_push($1, $2, $3, $4)", [rid, h, uuidOr(a.push_id, "not_found"), decisionOf(a.decision)]),
  },
  approve_page: {
    description: "A person's token only: approve or reject a pending global page. `decision` is approve (default) or reject.",
    readOnly: false,
    props: { page_id: { type: "string" }, decision: { type: "string", enum: ["approve", "reject"] } }, required: ["page_id"],
    run: (c, a, rid, h) => one(c, "brain.t_decide_page($1, $2, $3, $4)", [rid, h, uuidOr(a.page_id, "not_found"), decisionOf(a.decision)]),
  },
});

function toolList() {
  return Object.keys(TOOLS).map((name) => ({
    name, description: TOOLS[name].description,
    inputSchema: { type: "object", properties: { ...TOOLS[name].props, request_id: { type: "string" } }, required: TOOLS[name].required },
    annotations: { readOnlyHint: TOOLS[name].readOnly, destructiveHint: false, idempotentHint: TOOLS[name].readOnly, openWorldHint: false },
  }));
}

const DB_ERRORS = { BR400: "invalid_arguments", BR403: "forbidden", BR404: "not_found", BR409: "disabled",
                    "42501": "forbidden", "23514": "forbidden", "23503": "forbidden", "23505": "forbidden",
                    "22P02": "invalid_arguments", "22001": "invalid_arguments", "22021": "invalid_arguments" };

// A refusal is logged in its own transaction. If the row cannot be written this throws, and the request fails:
// nothing is answered that is not in the log.
async function logDenied(token, tool, requestId, reason, argsSha, target) {
  await withSession(token, (c) => c.query("select brain.audit_denied($1, $2, $3, $4, $5)", [tool, requestId, reason, argsSha, target]));
}
async function logAuthFailure() {
  const c = await app.connect();
  try { await c.query("select brain.audit_auth_failure()"); } finally { c.release(); }
}

async function callTool(token, name, args) {
  const a = args && typeof args === "object" && !Array.isArray(args) ? args : {};
  const argsSha = sha(JSON.stringify(a));
  const rid = a.request_id;
  const ridOk = rid === undefined || (typeof rid === "string" && rid.length <= 100 && !CONTROL.test(rid));
  const requestId = rid === undefined ? null : typeof rid === "string" ? printable(rid, 100) : null;
  const raw = typeof a.id === "string" ? a.id : typeof a.path === "string" ? a.path : typeof a.push_id === "string" ? a.push_id : typeof a.page_id === "string" ? a.page_id : null;
  const target = raw == null ? null : printable(raw, 200);
  const deny = async (tool, reason, error) => { await logDenied(token, tool, requestId, reason, argsSha, target); return { isError: true, payload: { error } }; };

  // The name must be a string that names one of the tools above. An array, a number or a name from Object.prototype is an unknown tool.
  if (typeof name !== "string" || !Object.hasOwn(TOOLS, name)) {
    return deny(printable(typeof name === "string" ? name : JSON.stringify(name) ?? "undefined", 60), "unknown_tool", "invalid_arguments");
  }
  // The request id joins this log to the caller's own. One that cannot be stored as written is refused, not repaired.
  if (!ridOk) return deny(name, "invalid_request_id", "invalid_arguments");
  try {
    return { isError: false, payload: await withSession(token, (c) => TOOLS[name].run(c, a, requestId, argsSha)) };
  } catch (e) {
    if (e.code === "28000") throw e;
    const code = e instanceof ToolError ? e.code : DB_ERRORS[e.code];
    if (!code) console.error("tool failure", name, e.code, e.message);
    return deny(name, code || "internal_error", code || "internal_error");
  }
}

async function rpc(token, msg) {
  const { id, method, params } = msg && typeof msg === "object" ? msg : {};
  const ok = (result) => ({ jsonrpc: "2.0", id, result });
  if (method === "tools/call") {
    const r = await callTool(token, params && params.name, params && params.arguments);
    return ok({ content: [{ type: "text", text: JSON.stringify(r.payload) }], isError: r.isError });
  }
  // Every other message is logged too, under its method name; one the service does not know is logged as refused.
  const known = await withSession(token, (c) => one(c, "brain.audit_rpc($1)", [typeof method === "string" ? printable(method, 100) : null]));
  if (!known) return { jsonrpc: "2.0", id: id ?? null, error: { code: -32601, message: "method not found" } };
  if (method === "initialize") {
    return ok({ protocolVersion: (params && params.protocolVersion) || "2025-06-18", capabilities: { tools: { listChanged: false } },
                serverInfo: { name: "azi-permission-service-rev01-fix", version: "0.1.0" } });
  }
  if (method.startsWith("notifications/")) return null;
  if (method === "ping") return ok({});
  return ok({ tools: toolList() });
}

// Admin: the operator's console in the spike ----------------------------------------------------------------
// Every route that changes or shows data writes a log row (actor "operator"). Reading the log itself does not.

const BOOL = (v, key) => { if (typeof v !== "boolean") throw new AdminError(400, "invalid_setting", key); return v; };
const READS = ["all", "summaries", "none", "default"];

async function applySettings(c, body) {
  const known = ["org", "personal_enabled", "briefing_enabled", "push_enabled", "holding_reads", "parent_reads"];
  for (const k of Object.keys(body)) if (!known.includes(k)) throw new AdminError(400, "unknown_setting", k);
  const changed = {};
  const setChildReads = async (org, value) => {
    if (typeof org !== "string" || !READS.includes(value)) throw new AdminError(400, "invalid_setting", "holding_reads");
    const r = await c.query("update brain.orgs set parent_reads = $2 where id = $1 and kind = 'sub'", [org, value === "default" ? null : value]);
    if (r.rowCount !== 1) throw new AdminError(400, "invalid_setting", "not a sub-organization: " + printable(org, 60));
    changed["parent_reads:" + org] = value;
  };
  if (body.org !== undefined) {
    // Settings of one organization, or of the person whose personal space it is.
    if (typeof body.org !== "string") throw new AdminError(400, "invalid_setting", "org");
    const o = (await c.query("select kind from brain.orgs where id = $1", [body.org])).rows[0];
    if (!o) throw new AdminError(400, "invalid_setting", "unknown organization");
    for (const k of ["holding_reads", "parent_reads"]) if (k in body) await setChildReads(body.org, body[k]);
    for (const [k, col] of [["personal_enabled", "personal_enabled"], ["briefing_enabled", "push_enabled"], ["push_enabled", "push_enabled"]]) {
      if (!(k in body)) continue;
      if (o.kind !== "personal") throw new AdminError(400, "invalid_setting", k + " is a person's switch; name a personal space");
      await c.query(`update brain.people set ${col} = $2 where personal_org = $1`, [body.org, BOOL(body[k], k)]);
      changed[col + ":" + body.org] = body[k];
    }
  } else {
    for (const k of ["personal_enabled", "briefing_enabled"]) {
      if (k in body) { await c.query(`update brain.settings set ${k} = $1`, [BOOL(body[k], k)]); changed[k] = body[k]; }
    }
    if ("push_enabled" in body || "parent_reads" in body) throw new AdminError(400, "invalid_setting", "name an organization");
    if ("holding_reads" in body) {
      const v = body.holding_reads;
      if (v && typeof v === "object" && !Array.isArray(v)) {
        for (const [org, value] of Object.entries(v)) await setChildReads(org, value);     // {"holding_reads": {"<org>": "none"}}
      } else if (v === "all" || v === "summaries") {
        await c.query("update brain.settings set holding_reads = $1", [v]); changed.holding_reads = v;
      } else throw new AdminError(400, "invalid_setting", "holding_reads is all or summaries for the deployment; none is set per organization");
    }
  }
  await c.query("select brain.audit_operator('admin:settings', 'allow', null, $1, null, null, null, $2)", [typeof body.org === "string" ? body.org : null, JSON.stringify(changed)]);
  const out = (await c.query("select personal_enabled, briefing_enabled, holding_reads from brain.settings")).rows[0];
  out.organizations = Object.fromEntries((await c.query("select id, parent_reads, brain.child_mode_(id) as effective from brain.orgs where kind = 'sub' order by id")).rows
    .map((r) => [r.id, { parent_reads: r.parent_reads ?? "default", effective: r.effective }]));
  out.people = Object.fromEntries((await c.query("select id, personal_org, personal_enabled, push_enabled from brain.people order by id")).rows
    .map((r) => [r.id, { personal_org: r.personal_org, personal_enabled: r.personal_enabled, briefing_enabled: r.push_enabled }]));
  return out;
}

async function loadFixture(c, body) {
  await c.query("truncate brain.pages, brain.pushes, brain.principals, brain.sessions, brain.memberships, brain.people, brain.orgs cascade");
  const s = body.settings || {};
  await c.query("update brain.settings set personal_enabled = $1, briefing_enabled = $2, holding_reads = $3",
    [s.personal_enabled !== false, s.briefing_enabled !== false, s.holding_reads || "all"]);
  const orgs = [...(body.orgs || [])].sort((x, y) => (x.parent ? 1 : 0) - (y.parent ? 1 : 0));
  for (const o of orgs) await c.query("insert into brain.orgs (id, kind, parent_id, parent_reads) values ($1, $2, $3, $4)", [o.id, o.kind, o.parent || null, o.parent_reads || null]);
  const kinds = Object.fromEntries(orgs.map((o) => [o.id, o.kind]));
  for (const p of body.people || []) await c.query("insert into brain.people (id, personal_org) values ($1, $2)", [p.id, p.personal_org || null]);
  const personOf = Object.fromEntries((body.people || []).filter((p) => p.personal_org).map((p) => [p.personal_org, p.id]));
  // A personal space with nobody behind it cannot be used, so a fixture that has one is refused outright.
  for (const o of orgs) if (o.kind === "personal" && !personOf[o.id]) throw new AdminError(400, "invalid_fixture", "personal space without a person: " + printable(o.id, 60));
  for (const m of body.memberships || []) await c.query("insert into brain.memberships (person_id, org_id, org_kind, role) values ($1, $2, $3, $4)", [m.person, m.org, kinds[m.org], m.role || "member"]);
  for (const p of body.principals || []) {
    await c.query("insert into brain.principals (token_sha256, org_id, actor, person_id) values ($1, $2, $3, $4)", [sha(p.token), p.org, p.actor, p.person || personOf[p.org] || null]);
  }
  for (const p of body.pages || []) {
    const global = p.visibility === "global" && p.pending !== true;       // a fixture's global page is loaded as approved, by "fixture"
    await c.query(`insert into brain.pages (org_id, org_kind, title, body, kind, source_type, sensitivity, visibility, path, pushed_from, global_approved_by, global_approved_at)
                   values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)`,
      [p.org, kinds[p.org], p.title, p.body || "", p.kind || "note", p.source_type || "human", p.sensitivity || "normal", p.visibility || "org", p.path || null,
       p.pushed_from || null, global ? "fixture" : null, global ? new Date() : null]);
  }
  const out = { orgs: orgs.length, people: (body.people || []).length, pages: (body.pages || []).length };
  await c.query("select brain.audit_operator('admin:reset', 'allow', null, null, null, null, null, $1)", [JSON.stringify(out)]);
  return out;
}

async function adminRoute(c, path, query, body) {
  if (path === "/admin/reset") return loadFixture(c, body);
  if (path === "/admin/settings") return applySettings(c, body);
  if (path === "/admin/approve_briefing" || path === "/admin/approve_page") {
    const page = path.endsWith("page");
    const id = page ? body.page_id : body.briefing_id ?? body.push_id;
    if (typeof id !== "string" || !UUID.test(id)) throw new AdminError(404, "not_found");
    if (typeof body.approver !== "string" || !body.approver.trim()) throw new AdminError(400, "approver_required");
    if (body.decision != null && body.decision !== "approve" && body.decision !== "reject") throw new AdminError(400, "invalid_decision");
    const fn = page ? "brain.operator_decide_page" : "brain.operator_decide_push";
    const out = (await c.query(`select ${fn}($1, $2, $3) as id`, [id, body.approver, body.decision ?? "approve"])).rows[0].id;
    return { page_id: out, status: body.decision === "reject" ? "rejected" : "approved" };
  }
  if (path === "/admin/pushes") {
    // The operator sees the text of pending pushes here, so this read is logged.
    const rows = (await c.query(`select id, from_org, to_org, content, status, created_at, created_by_actor, decided_by, decided_via, page_id from brain.pushes
                                  where ($1::text is null or status = $1) order by created_at, id`, [query.get("status")])).rows;
    await c.query("select brain.audit_operator('admin:pushes', 'allow', null, null, null, null, null, $1)", [JSON.stringify({ status: query.get("status"), rows: rows.length })]);
    return { rows };
  }
  if (path === "/admin/codebase_sync") {
    const kind = (await c.query("select kind from brain.orgs where id = $1", [body.org])).rows[0]?.kind;
    if (!kind) throw new AdminError(400, "unknown_organization");
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
    await c.query("select brain.audit_operator('admin:codebase_sync', 'allow', null, $1, null, null, null, $2)", [body.org, JSON.stringify({ written, deleted })]);
    return { written, deleted };
  }
  if (path === "/admin/pages_digest") {
    const rows = (await c.query("select path, content_sha, updated_at from brain.pages where org_id = $1 and source_type = $2 order by path", [query.get("org"), query.get("source_type") || "codebase"])).rows;
    await c.query("select brain.audit_operator('admin:pages_digest', 'allow', null, $1, null, null, null, $2)", [query.get("org"), JSON.stringify({ rows: rows.length })]);
    return { rows };
  }
  if (path === "/admin/audit") {
    const page = query.get("page_id");
    if (page != null && !UUID.test(page)) throw new AdminError(400, "invalid_page_id");
    return { rows: (await c.query(`select id::int as id, ts, via, org, actor, person, tool, request_id, decision, reason, target, result_count, page_ids, detail
                                     from brain.audit where id > $1 and ($2::uuid is null or $2::uuid = any (page_ids)) order by id`, [Number(query.get("since_id") || 0), page])).rows };
  }
  if (path === "/admin/audit_verify") {
    const r = (await c.query("select rows_checked::int as rows_checked, first_bad_id::int as first_bad_id from brain.audit_verify()")).rows[0];
    return { ok: r.first_bad_id == null, ...r };
  }
  return null;
}

async function admin(path, query, body) {
  const c = await owner.connect();
  try {
    await c.query("begin");
    const out = await adminRoute(c, path, query, body && typeof body === "object" && !Array.isArray(body) ? body : {});
    await c.query(out == null ? "rollback" : "commit");
    return out;
  } catch (e) {
    await c.query("rollback").catch(() => {});
    const refused = e instanceof AdminError ? e : DB_ERRORS[e.code] ? new AdminError(e.code === "BR404" ? 404 : 409, DB_ERRORS[e.code]) : null;
    if (!refused) throw e;
    // The refusal is logged too, in a transaction of its own.
    await c.query("select brain.audit_operator($1, 'deny', $2, null, null, null, null, null)", ["admin:" + printable(path.slice(7), 50), refused.code]);
    throw refused;
  } finally { c.release(); }
}

function send(res, status, obj, headers = {}) {
  const text = obj == null ? "" : JSON.stringify(obj);
  res.writeHead(status, { "content-type": "application/json", "cache-control": "no-store", ...headers });
  res.end(text);
}
// One documented form and no other: "Authorization: Bearer <token>".
const bearer = (req) => {
  const h = req.headers.authorization;
  const m = typeof h === "string" ? /^Bearer +(.+)$/.exec(h) : null;
  return m ? m[1].trim() : null;
};
// Compared as hashes, so the comparison takes the same path whatever the length or bytes of what was sent.
const ADMIN_SHA = Buffer.from(sha(ADMIN_TOKEN), "hex");
const isAdmin = (token) => token != null && crypto.timingSafeEqual(Buffer.from(sha(token), "hex"), ADMIN_SHA);

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  try {
    if (req.method === "GET" && url.pathname === "/healthz") return send(res, 200, { ok: true });
    let raw = "";
    for await (const chunk of req) { raw += chunk; if (raw.length > 30_000_000) return send(res, 413, { error: "too_large" }); }
    const token = bearer(req);

    if (url.pathname.startsWith("/admin/")) {
      if (!isAdmin(token)) {
        await owner.query("select brain.audit_operator('admin:auth', 'deny', 'invalid_token', null, null, null, null, null)");
        return send(res, 401, { error: "unauthorized" });
      }
      let body = {};
      if (raw) { try { body = JSON.parse(raw); } catch { return send(res, 400, { error: "invalid_json" }); } }
      try {
        const out = await admin(url.pathname, url.searchParams, body);
        return out == null ? send(res, 404, { error: "not_found" }) : send(res, 200, out);
      } catch (e) {
        if (e instanceof AdminError) return send(res, e.status, { error: e.code, detail: e.detail });
        throw e;
      }
    }

    if (url.pathname === "/mcp") {
      if (req.method !== "POST") return send(res, 405, { error: "method_not_allowed" }, { allow: "POST" });
      // Every MCP request needs a valid token, including initialize and tools/list.
      try {
        if (token == null || token.includes("\u0000")) throw Object.assign(new Error("invalid_token"), { code: "28000" });
        await withSession(token, async () => {});
      } catch (e) {
        if (e.code !== "28000") throw e;
        await logAuthFailure();
        return send(res, 401, { error: "unauthorized" }, { "www-authenticate": "Bearer" });
      }
      let body;
      try { body = raw ? JSON.parse(raw) : {}; } catch {
        await logDenied(token, "mcp:invalid_json", null, "invalid_json", null, null);
        return send(res, 400, { error: "invalid_json" });
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
