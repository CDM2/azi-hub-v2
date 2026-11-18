"""REV-01 fix pass: which deliberate breaks of the fixed service do its tests notice?

The review ran 19 breaks of R-02's schema against R-02's 35 tests and 10 went unnoticed (RV-11). This does the same
to the fixed service, and to the server as well as the schema, because three of the review's findings were in the server.

Each mutant is a copy of service/schema.sql or service/server.mjs with one rule weakened. The copy is loaded (or started),
all four test files are run, and the result is one of:

  killed     at least one test failed: the tests notice that the rule is gone
  SURVIVED   every test passed although a rule was gone: a gap in the tests
  same       every test passed, and that was expected: the mutant removes one of two locks on the same rule,
             and its entry names the mutant that removes both
  UNEXPECTED a "same" mutant that was killed, which would mean the two locks are not equivalent

A run that fails only in the two tests that time whole HTTP calls is repeated once; those two carry about 100 microseconds
of disk noise and fail by chance now and then. If the repeat passes, the first failure is reported as noise, not as a kill.

Run through run.sh, or:  python3 mutation_sweep.py   with SUPER_DSN, OWNER_PW, APP_PW, BRAIN_ADMIN_TOKEN, BRAIN_APP_DSN,
BRAIN_OWNER_DSN and SERVICE_DIR (a directory holding node_modules with `pg`) set. It starts its own copy of the
service on SWEEP_PORT (default 8911) and leaves the original schema loaded. Standard library only.
"""
import os, pathlib, re, shutil, subprocess, sys, tempfile, time, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
SCHEMA = (HERE / "service" / "schema.sql").read_text()
SERVER = (HERE / "service" / "server.mjs").read_text()
TESTS = HERE / "tests"
FILES = ["test_criteria_1_3", "test_rev01_attacks", "test_rev01_second_person", "test_fix_new_rules"]
NOISY = {"test_a_forbidden_page_takes_as_long_as_a_missing_page", "test_a_forbidden_page_id_takes_as_long_as_a_missing_page_id"}
SUPER_DSN = os.environ["SUPER_DSN"]
PORT = os.environ.get("SWEEP_PORT", "8911")
ONLY = set(sys.argv[1:])

HUMAN_ONLY = "  if s.actor <> 'human' or s.person_id is null then raise exception 'forbidden' using errcode = 'BR403'; end if;\n"

# (name, expectation, what is weakened, [(file, text to find, replacement), ...]). Each "find" must occur exactly once.
S, J = "schema", "server"
MUTANTS = [
    # --- who reads what
    ("N01", "same", "read rule: the second lock on personal spaces is removed (the first lock is that no session's scope ever holds another personal space; N03 removes both)",
     [(S, "     and (p.org_kind <> 'personal' or p.org_id = (s).org_id)                                              -- second lock: nobody else reads a personal space\n", "")]),
    ("N02", "killed", "session: a personal space's scope takes in every other personal space (the second lock still stops reads; pushes are what notice)",
     [(S, "from brain.orgs o where o.kind <> 'personal' and brain.belongs_(v_person, o.id);", "from brain.orgs o where o.id <> v.org_id and (o.kind = 'personal' or brain.belongs_(v_person, o.id));")]),
    ("N03", "killed", "N01 and N02 together: both locks on personal spaces are gone",
     [(S, "     and (p.org_kind <> 'personal' or p.org_id = (s).org_id)                                              -- second lock: nobody else reads a personal space\n", ""),
      (S, "from brain.orgs o where o.kind <> 'personal' and brain.belongs_(v_person, o.id);", "from brain.orgs o where o.id <> v.org_id and (o.kind = 'personal' or brain.belongs_(v_person, o.id));")]),
    ("N04", "killed", "session: a personal space reads every organization, whoever it belongs to (R-02's rule)",
     [(S, "from brain.orgs o where o.kind <> 'personal' and brain.belongs_(v_person, o.id);", "from brain.orgs o where o.kind <> 'personal';")]),
    ("N05", "killed", "membership: a plain member of an organization counts as belonging to everything below it",
     [(S, "return found and (v_role = 'owner' or (v_first and not p_need_owner));", "return found and (v_role = 'owner' or not p_need_owner);")]),
    ("N06", "killed", "membership: a plain member counts as controlling the organization",
     [(S, "return found and (v_role = 'owner' or (v_first and not p_need_owner));", "return found and (v_role = 'owner' or v_first);")]),
    ("N07", "killed", "membership: a venture's own member list no longer closes it to an owner of the organization above",
     [(S, "      return found and (v_role = 'owner' or (v_first and not p_need_owner));\n", "      if found and (v_role = 'owner' or (v_first and not p_need_owner)) then return true; end if;\n")]),
    ("N08", "killed", "parent reads: a venture with a second person is read by the layer above by default",
     [(S, "                       then 'none' else (select s.holding_reads from brain.settings s) end)", "                       then (select s.holding_reads from brain.settings s) else (select s.holding_reads from brain.settings s) end)")]),
    ("N09", "killed", "parent reads: a venture's own setting is ignored",
     [(S, "  select coalesce(c.parent_reads,\n", "  select coalesce(null,\n")]),
    ("N10", "killed", "session: summaries mode reads everything",
     [(S, "filter (where brain.child_mode_(c.id) = 'all'), '{}'),", "filter (where brain.child_mode_(c.id) in ('all', 'summaries')), '{}'),")]),
    ("N11", "killed", "session: an organization reads every sub-organization, not only its own children",
     [(S, "      from brain.orgs c where c.parent_id = v.org_id;", "      from brain.orgs c where c.parent_id is not null and c.id <> v.org_id;")]),
    ("N12", "killed", "session: global pages are read across holding organizations",
     [(S, "    if v.kind = 'sub' then v_glob := array[brain.root_of_(v.org_id)]; end if;", "    select coalesce(array_agg(o.id), '{}') into v_glob from brain.orgs o where o.kind = 'holding' and o.id <> v.org_id;")]),
    ("N13", "killed", "read rule: a global page is readable below before a person approves it (RV-02)",
     [(S, " and p.visibility = 'global' and p.global_approved_at is not null))  -- approved global pages", " and p.visibility = 'global'))")]),
    ("N14", "killed", "read rule: summaries-only organizations are read in full",
     [(S, "          or (p.org_id = any ((s).sum_orgs) and p.kind = 'summary')                                       -- summaries only\n", "          or (p.org_id = any ((s).sum_orgs))\n")]),
    ("N15", "killed", "read rule: the briefing switches no longer hide earlier briefings",
     [(S, "     and (p.kind <> 'briefing' or ((s).briefings_on and p.pushed_from <> all ((s).muted_orgs)))           -- a briefing switch that is off hides earlier briefings\n", "")]),
    ("N16", "killed", "read rule: one person's briefing switch no longer hides that person's earlier briefings",
     [(S, "((s).briefings_on and p.pushed_from <> all ((s).muted_orgs))", "((s).briefings_on)")]),
    ("N17", "killed", "session: a bound session outlives its transaction",
     [(S, "  select * into s from brain.sessions where pid = pg_backend_pid() and txid = txid_current_if_assigned();", "  select * into s from brain.sessions where pid = pg_backend_pid();")]),
    ("N18", "killed", "session: the tool functions run without a bound session",
     [(S, "  if not found then raise exception 'no_session' using errcode = '28000'; end if;\n  return s;", "  return s;")]),
    ("N19", "killed", "session: the deployment's personal-space switch is not checked",
     [(S, "p.personal_enabled and st.personal_enabled and", "p.personal_enabled and")]),
    ("N20", "killed", "session: a person's own personal-space switch is not checked",
     [(S, "p.personal_enabled and st.personal_enabled and", "st.personal_enabled and")]),
    ("N21", "killed", "session: a personal-space token that stands for somebody else is accepted",
     [(S, " and (v.person_id is null or v.person_id = p.id);", ";")]),
    ("N22", "killed", "session: a person's token works in an organization the person does not belong to",
     [(S, "    if v.person_id is not null and not brain.belongs_(v.person_id, v.org_id) then", "    if false then")]),
    ("N23", "killed", "lookup: `org` is ignored instead of narrowing (RV-18)",
     [(S, "from unnest(s.all_orgs || s.sum_orgs || s.glob_orgs) o where p_org is null or o = p_org;", "from unnest(s.all_orgs || s.sum_orgs || s.glob_orgs) o;")]),
    ("N24", "killed", "search and list: the fence is removed, so the search text is tried against other organizations' rows",
     [(S, None, None)]),                                                              # filled in below: four replacements
    ("N25", "killed", "search and list: sequential scans are allowed again, so latency grows with other organizations' pages (RV-05)",
     [(S, None, None)]),                                                              # filled in below: three replacements
    # --- writing
    ("N26", "killed", "write: an agent may add a page of any kind",
     [(S, "  if v_kind not in ('note', 'summary') then raise exception 'forbidden' using errcode = 'BR403'; end if;\n", "")]),
    ("N27", "killed", "write: provenance is not taken from the caller",
     [(S, "          case s.actor when 'human' then 'human' else 'agent' end, s.person_id,", "          'human', s.person_id,")]),
    ("N28", "killed", "constraint removed: any organization may write a global page",
     [(S, "  constraint only_holding_publishes_global check (visibility = 'org' or org_kind = 'holding'),\n", "")]),
    ("N29", "killed", "constraint removed: health and finance pages may be stored outside a personal space",
     [(S, "  constraint health_and_finance_stay_personal check (sensitivity = 'normal' or org_kind = 'personal'),\n", "")]),
    ("N30", "killed", "write: any person's global page is published at once, whether or not they control the organization",
     [(S, "  v_approved := v_vis = 'global' and s.actor = 'human' and brain.controls_(s.person_id, s.org_id);", "  v_approved := v_vis = 'global' and s.actor = 'human' and s.person_id is not null;")]),
    # --- pushes and approval
    ("N31", "killed", "briefing: an organization may offer one, not only a personal space",
     [(S, "  if s.kind <> 'personal' then raise exception 'forbidden' using errcode = 'BR403'; end if;\n", "")]),
    ("N32", "killed", "briefing: it may be addressed to an organization its person does not belong to",
     [(S, "  if v_to = s.org_id or v_to <> all (s.all_orgs) then raise exception 'forbidden' using errcode = 'BR403'; end if;", "  if v_to = s.org_id then raise exception 'forbidden' using errcode = 'BR403'; end if;")]),
    ("N33", "killed", "briefing: the switches are not checked when one is offered",
     [(S, "  if not s.briefings_on or s.org_id = any (s.muted_orgs) then raise exception 'disabled' using errcode = 'BR409'; end if;\n", "")]),
    ("N34", "killed", "briefing: with several top-level organizations the service picks one instead of refusing",
     [(S, "    if v_roots is null or cardinality(v_roots) <> 1 then raise exception 'invalid_arguments' using errcode = 'BR400'; end if;", "    if v_roots is null then raise exception 'invalid_arguments' using errcode = 'BR400'; end if;")]),
    ("N35", "killed", "approval: anyone who is a person may decide any push (RV-15)",
     [(S, "  if not found or not coalesce(brain.may_decide_(p_person, b.from_org), false) then raise exception 'not_found' using errcode = 'BR404'; end if;", "  if not found then raise exception 'not_found' using errcode = 'BR404'; end if;")]),
    ("N36", "killed", "approval: an agent may decide a push",
     [(S, HUMAN_ONLY + "  v_page := brain.decide_push_(", "  v_page := brain.decide_push_(")]),
    ("N37", "killed", "approval: the switches are not checked when a briefing is approved (RV-15)",
     [(S, "    if not (st.briefing_enabled and pp.push_enabled and st.personal_enabled and pp.personal_enabled) then", "    if false then")]),
    ("N38", "killed", "approval: anyone who is a person may release any global page",
     [(S, "  if not found or not brain.controls_(p_person, r.org_id) then raise exception 'not_found' using errcode = 'BR404'; end if;", "  if not found then raise exception 'not_found' using errcode = 'BR404'; end if;")]),
    ("N39", "killed", "approval: an agent may release a global page",
     [(S, HUMAN_ONLY + "  v_page := brain.decide_page_(", "  v_page := brain.decide_page_(")]),
    ("N40", "killed", "approval: the queue shows every pending push to every person",
     [(S, "from brain.pushes b where b.status = 'pending' and brain.may_decide_(s.person_id, b.from_org);", "from brain.pushes b where b.status = 'pending';")]),
    ("N41", "killed", "approval: an agent may read the queue",
     [(S, HUMAN_ONLY + "  select coalesce(jsonb_agg(jsonb_build_object('push_id'", "  select coalesce(jsonb_agg(jsonb_build_object('push_id'")]),
    ("N42", "killed", "pushes: the trigger that freezes a push's text and route is not created",
     [(S, "create trigger pushes_no_rewrite before update or delete on brain.pushes\n  for each row execute function brain.pushes_are_decided_once();\n", "")]),
    ("N43", "killed", "reports: any organization may send one upward, to nowhere in particular",
     [(S, "  select o.parent_id into v_to from brain.orgs o where o.id = s.org_id and o.kind = 'sub';\n  if v_to is null then raise exception 'forbidden' using errcode = 'BR403'; end if;",
       "  select coalesce(o.parent_id, (select h.id from brain.orgs h where h.kind = 'holding' and h.id <> s.org_id order by h.id limit 1)) into v_to from brain.orgs o where o.id = s.org_id;\n  if v_to is null then raise exception 'forbidden' using errcode = 'BR403'; end if;")]),
    # --- the log
    ("N44", "killed", "log: an allowed call writes no row",
     [(S, "  select brain.audit_write_('mcp', (s).org_id, (s).actor, (s).person_id, p_tool, p_request_id, 'allow', null, p_args_sha, p_target, p_count, p_page_ids, null)", "  select null::bigint")]),
    ("N45", "killed", "log: the row for an allowed read does not say which pages were returned",
     [(S, "p_tool, p_request_id, 'allow', null, p_args_sha, p_target, p_count, p_page_ids, null)", "p_tool, p_request_id, 'allow', null, p_args_sha, p_target, p_count, null, null)")]),
    ("N46", "killed", "log: the append-only triggers are not created",
     [(S, "create trigger audit_no_change before update or delete on brain.audit\n  for each row execute function brain.audit_is_append_only();\n"
          "create trigger audit_no_truncate before truncate on brain.audit\n  for each statement execute function brain.audit_is_append_only();\n", "")]),
    ("N47", "killed", "log: the chain's hash leaves out the decision, so a refusal can be rewritten as an allowed call unnoticed",
     [(S, "p_person, p_tool, p_request_id, p_decision, p_reason, p_args_sha, p_target, p_count, p_page_ids::text, p_detail)::text", "p_person, p_tool, p_request_id, null, p_reason, p_args_sha, p_target, p_count, p_page_ids::text, p_detail)::text")]),
    ("N48", "killed", "log: the chain does not link a row to the one before it, so a removed row goes unnoticed",
     [(S, "    if r.prev_hash is distinct from v_prev\n       or r.row_hash", "    if r.row_hash")]),
    ("N49", "killed", "log: the role may record a refusal without a session, for no organization (RV-19)",
     [(S, "declare s brain.sessions := brain.scope_();\nbegin\n  perform brain.audit_write_('mcp', s.org_id, s.actor, s.person_id, p_tool, p_request_id, 'deny',",
          "declare s brain.sessions;\nbegin\n  select * into s from brain.sessions where pid = pg_backend_pid() and txid = txid_current_if_assigned();\n"
          "  perform brain.audit_write_('mcp', s.org_id, s.actor, s.person_id, p_tool, p_request_id, 'deny',")]),
    ("N50", "same", "log: the role may call the internal log writer (it runs with the caller's rights, and the caller has none on the log; N57 makes it run with the owner's rights as well)",
     [(S, "  brain.audit_auth_failure()\nto brain_app;", "  brain.audit_auth_failure(),\n  brain.audit_write_(text, text, text, text, text, text, text, text, text, text, int, uuid[], jsonb)\nto brain_app;")]),
    ("N57", "killed", "N50, and the log writer runs with the owner's rights: the role may write any row it likes, allowed or denied (RV-19)",
     [(S, "  brain.audit_auth_failure()\nto brain_app;", "  brain.audit_auth_failure(),\n  brain.audit_write_(text, text, text, text, text, text, text, text, text, text, int, uuid[], jsonb)\nto brain_app;"),
      (S, "language plpgsql set search_path = brain, pg_temp as $$\ndeclare\n  v_prev text; v_id bigint; v_ts timestamptz;", "language plpgsql security definer set search_path = brain, pg_temp as $$\ndeclare\n  v_prev text; v_id bigint; v_ts timestamptz;")]),
    ("N51", "killed", "log: a message the service does not know is logged as allowed",
     [(S, "null, case when v_known then 'allow' else 'deny' end, case when v_known then null else 'unknown_method' end,", "null, 'allow', null,")]),
    # --- privileges
    ("N52", "killed", "privileges: the role is granted select on the pages table (row-level security, with no policy for it, still returns nothing)",
     [(S, "insert into brain.settings default values;", "grant select on brain.pages to brain_app;\ninsert into brain.settings default values;")]),
    ("N53", "killed", "privileges: the role may read the token table, the people and the log",
     [(S, "insert into brain.settings default values;", "grant select on brain.principals, brain.people, brain.audit to brain_app;\ninsert into brain.settings default values;")]),
    ("N54", "same", "privileges: the role may call the operator's approval function (it runs with the caller's rights, and the caller has none on any table; N58 makes it run with the owner's rights as well)",
     [(S, "  brain.audit_auth_failure()\nto brain_app;", "  brain.audit_auth_failure(),\n  brain.operator_decide_push(uuid, text, text)\nto brain_app;")]),
    ("N58", "killed", "N54, and the operator's approval function runs with the owner's rights: the role may approve any push in any person's name",
     [(S, "  brain.audit_auth_failure()\nto brain_app;", "  brain.audit_auth_failure(),\n  brain.operator_decide_push(uuid, text, text)\nto brain_app;"),
      (S, "create function brain.operator_decide_push(p_push uuid, p_approver text, p_decision text) returns uuid\nlanguage plpgsql set search_path = brain, pg_temp as $$",
          "create function brain.operator_decide_push(p_push uuid, p_approver text, p_decision text) returns uuid\nlanguage plpgsql security definer set search_path = brain, pg_temp as $$")]),
    ("N55", "same", "privileges: the role may call the internal read rule directly (it runs with the caller's rights, and the caller has none on the table; N56 gives it those too)",
     [(S, "  brain.audit_auth_failure()\nto brain_app;", "  brain.audit_auth_failure(),\n  brain.visible_pages_(brain.sessions)\nto brain_app;")]),
    ("N56", "killed", "N55, and row-level security is switched off on the pages table, and the role is granted select on it",
     [(S, "  brain.audit_auth_failure()\nto brain_app;", "  brain.audit_auth_failure(),\n  brain.visible_pages_(brain.sessions)\nto brain_app;"),
      (S, "alter table brain.pages enable row level security;\nalter table brain.pages force row level security;\n", ""),
      (S, "insert into brain.settings default values;", "grant select on brain.pages to brain_app;\ninsert into brain.settings default values;")]),
    # --- the server
    ("J01", "killed", "server: a tool name is looked up without checking that it is one of the tools (RV-07: \"constructor\", an array)",
     [(J, 'if (typeof name !== "string" || !Object.hasOwn(TOOLS, name)) {', "if (!TOOLS[name]) {"),
      (J, "const TOOLS = Object.assign(Object.create(null), {", "const TOOLS = Object.assign({}, {")]),
    ("J02", "killed", "server: a request id that cannot be stored as written is passed on instead of refused (RV-07)",
     [(J, 'if (!ridOk) return deny(name, "invalid_request_id", "invalid_arguments");', "")]),
    ("J03", "killed", "server: a refusal is not logged",
     [(J, "const deny = async (tool, reason, error) => { await logDenied(token, tool, requestId, reason, argsSha, target); return", "const deny = async (tool, reason, error) => { return")]),
    ("J04", "killed", "server: a refused token is not logged",
     [(J, "        await logAuthFailure();\n", "")]),
    ("J05", "killed", "server: the token may come in other headers and forms (RV-17)",
     [(J, '  const h = req.headers.authorization;\n  const m = typeof h === "string" ? /^Bearer +(.+)$/.exec(h) : null;\n  return m ? m[1].trim() : null;',
          '  const h = req.headers.authorization || req.headers["x-brain-token"] || "";\n  const m = /^Bearer\\s+(.+)$/i.exec(h);\n  return m ? m[1].trim() : (h.trim() ? h.trim() : null);')]),
    ("J06", "killed", "server: the admin token is compared byte for byte after a length check (RV-16)",
     [(J, 'const isAdmin = (token) => token != null && crypto.timingSafeEqual(Buffer.from(sha(token), "hex"), ADMIN_SHA);',
          "const isAdmin = (token) => token != null && token.length === ADMIN_TOKEN.length && crypto.timingSafeEqual(Buffer.from(token), Buffer.from(ADMIN_TOKEN));")]),
    ("J07", "killed", "server: an approval with no approver named is passed to the database (RV-15)",
     [(J, '    if (typeof body.approver !== "string" || !body.approver.trim()) throw new AdminError(400, "approver_required");\n', "")]),
    ("J08", "killed", "server: a setting it does not know is ignored instead of refused",
     [(J, '  for (const k of Object.keys(body)) if (!known.includes(k)) throw new AdminError(400, "unknown_setting", k);\n', "")]),
    ("J09", "killed", "server: what the operator does is not logged",
     [(J, """  await c.query("select brain.audit_operator('admin:settings', 'allow', null, $1, null, null, null, $2)", [typeof body.org === "string" ? body.org : null, JSON.stringify(changed)]);\n""", "")]),
    ("J10", "killed", "server: a wrong admin token is not logged",
     [(J, """        await owner.query("select brain.audit_operator('admin:auth', 'deny', 'invalid_token', null, null, null, null, null)");\n""", "")]),
    ("J11", "killed", "server: a message that is not a tool call is not logged",
     [(J, """  const known = await withSession(token, (c) => one(c, "brain.audit_rpc($1)", [typeof method === "string" ? printable(method, 100) : null]));""",
          """  const known = typeof method === "string" && (["initialize", "ping", "tools/list"].includes(method) || method.startsWith("notifications/"));""")]),
    ("J12", "killed", "server: a fixture with a personal space and nobody behind it is loaded",
     [(J, """  for (const o of orgs) if (o.kind === "personal" && !personOf[o.id]) throw new AdminError(400, "invalid_fixture", "personal space without a person: " + printable(o.id, 60));\n""", "")]),
]


def apply(text, find, repl, name):
    assert text.count(find) == 1, f"{name}: the text to replace occurs {text.count(find)} times: {find[:70]!r}"
    return text.replace(find, repl)


def build(name, edits):
    schema, server = SCHEMA, SERVER
    if name == "N24":
        assert schema.count("(select * from brain.visible_pages_(s) offset 0) p") == 4
        return schema.replace("(select * from brain.visible_pages_(s) offset 0) p", "brain.visible_pages_(s) p"), server
    if name == "N25":
        assert schema.count(" set enable_seqscan = off as $$") == 2
        return schema.replace(" set enable_seqscan = off as $$", " as $$"), server
    for which, find, repl in edits:
        if which == S: schema = apply(schema, find, repl, name)
        else: server = apply(server, find, repl, name)
    return schema, server


def load(sql_text):
    with tempfile.NamedTemporaryFile("w", suffix=".sql", delete=False) as f:
        f.write(sql_text)
    out = subprocess.run(["psql", SUPER_DSN, "-X", "-q", "-v", "ON_ERROR_STOP=1", "-v", "owner_pw=" + os.environ["OWNER_PW"],
                          "-v", "app_pw=" + os.environ["APP_PW"], "-f", f.name], capture_output=True, text=True)
    os.unlink(f.name)
    return out.returncode, out.stderr.strip()[-300:]


class Service:
    """This sweep's own copy of the service, restarted for every mutant."""
    def __init__(self):
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="sweep-"))
        os.symlink(pathlib.Path(os.environ["SERVICE_DIR"]) / "node_modules", self.dir / "node_modules")
        shutil.copy(HERE / "service" / "package.json", self.dir / "package.json")
        self.proc = None

    def start(self, server_text):
        self.stop()
        (self.dir / "server.mjs").write_text(server_text)
        self.proc = subprocess.Popen(["node", "server.mjs"], cwd=self.dir, env=dict(os.environ, PORT=PORT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/healthz", timeout=1).read(); return True
            except Exception:
                if self.proc.poll() is not None: return False
                time.sleep(0.1)
        return False

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate(); self.proc.wait(timeout=10)
        self.proc = None


def run_tests(only=None):
    args = [sys.executable, "-m", "unittest"] + (sorted(only) if only else FILES)
    out = subprocess.run(args, cwd=TESTS, capture_output=True, text=True, env=dict(os.environ, BRAIN_URL=f"http://127.0.0.1:{PORT}", PYTHONDONTWRITEBYTECODE="1"))
    text = out.stdout + out.stderr
    ran = re.search(r"Ran (\d+) tests", text)
    failed = re.findall(r"^(?:FAIL|ERROR): (\S+) \((\S+)\)", text, re.M)
    unexpected = re.search(r"unexpected successes=(\d+)", text)
    return int(ran.group(1)) if ran else 0, failed, int(unexpected.group(1)) if unexpected else 0


def verdict_of(svc_ok):
    """Run the tests; repeat once if the only failures are the two noisy timing tests. Returns (ran, failed tests, note)."""
    ran, failed, unexpected = run_tests()
    note = ""
    if failed and not unexpected and {f[0] for f in failed} <= NOISY:
        ran2, failed2, _ = run_tests(only={f"{f[1]}" for f in failed})
        if not failed2:
            note = f"  [noise: {', '.join(f[0] for f in failed)} failed once and passed when repeated]"
            failed = []
    names = [f[0] for f in failed] + (["an expected failure passed"] * unexpected)
    return ran, names, note


def main():
    svc = Service()
    try:
        rc, err = load(SCHEMA); assert rc == 0, err
        assert svc.start(SERVER), "the unmodified service did not start"
        ran, failed, note = verdict_of(True)
        print(f"baseline: ran {ran}, failed {len(failed)}{note}", flush=True)
        assert ran and not failed, f"the unmodified service must pass every test before any mutant is tried: {failed}"
        counts = {"killed": [], "SURVIVED": [], "same": [], "UNEXPECTED": [], "NOT LOADED": []}
        for name, expect, what, edits in MUTANTS:
            if ONLY and name not in ONLY: continue
            schema, server = build(name, edits)
            rc, err = load(schema)
            if rc != 0 or not svc.start(server):
                counts["NOT LOADED"].append(name); print(f"{name}  NOT LOADED  {what}  ({err})", flush=True); continue
            ran, failed, note = verdict_of(True)
            if failed: verdict = "killed" if expect == "killed" else "UNEXPECTED"
            else: verdict = "same" if expect == "same" else "SURVIVED"
            counts[verdict].append(name)
            print(f"{name}  {verdict:<10}  ran {ran}, failed {len(failed):2d}  {what}" + (f"  [first: {failed[0]}]" if failed else "") + note, flush=True)
        rc, err = load(SCHEMA); assert rc == 0, err
        assert svc.start(SERVER)
        ran, failed, note = verdict_of(True)
        print(f"restored: ran {ran}, failed {len(failed)}{note}")
        total = sum(len(v) for v in counts.values())
        print(f"mutants: {total}; killed {len(counts['killed'])}; survived {len(counts['SURVIVED'])}: {', '.join(counts['SURVIVED']) or 'none'}; "
              f"same as expected {len(counts['same'])}: {', '.join(counts['same']) or 'none'}; unexpected {len(counts['UNEXPECTED'])}: {', '.join(counts['UNEXPECTED']) or 'none'}; "
              f"not loaded {len(counts['NOT LOADED'])}: {', '.join(counts['NOT LOADED']) or 'none'}")
    finally:
        svc.stop(); shutil.rmtree(svc.dir, ignore_errors=True)


if __name__ == "__main__":
    main()
