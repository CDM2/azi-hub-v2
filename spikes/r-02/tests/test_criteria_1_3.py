"""R-02 spike, criteria 1 to 3, tested against the permission service directly.

Written before the service (see ../service/CONTRACT.md). Standard library only.
Run:  BRAIN_URL=http://127.0.0.1:8900 BRAIN_ADMIN_TOKEN=... BRAIN_APP_DSN=postgres://brain_app:...@127.0.0.1:5432/brain \
      python3 -m unittest -v test_criteria_1_3

Every made-up page carries a marker such as CANARY-SIBLING-1. A test fails if a marker
the caller must not see appears anywhere in a raw response: in a result, a count, or an error.
"""
import json
import os
import pathlib
import re
import subprocess
import unittest
import urllib.error
import urllib.request
import uuid

URL = os.environ.get("BRAIN_URL", "http://127.0.0.1:8900")
ADMIN = os.environ.get("BRAIN_ADMIN_TOKEN", "")
APP_DSN = os.environ.get("BRAIN_APP_DSN", "")
FIXTURE = json.loads((pathlib.Path(__file__).parent / "fixture.json").read_text())
TOKENS = {(p["org"], p["actor"]): p["token"] for p in FIXTURE["principals"]}
T_PERSONAL, T_MGMT = TOKENS[("personal", "agent")], TOKENS[("mgmt", "agent")]
T_TOVELI, T_TOVELI_HUMAN, T_SIBLING = TOKENS[("toveli", "agent")], TOKENS[("toveli", "human")], TOKENS[("sibling", "agent")]


def http(method, path, token=None, body=None):
    req = urllib.request.Request(URL + path, method=method, data=None if body is None else json.dumps(body).encode())
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def call(token, tool, args=None):
    """One MCP tools/call. Returns (ok, payload, raw_text)."""
    rpc = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "tools/call",
           "params": {"name": tool, "arguments": dict(args or {}, request_id=str(uuid.uuid4()))}}
    status, raw = http("POST", "/mcp", token, rpc)
    if status != 200:
        return False, {"http": status}, raw
    msg = json.loads(raw)
    if "error" in msg:
        return False, msg["error"], raw
    res = msg["result"]
    text = res["content"][0]["text"] if res.get("content") else "{}"
    try:
        payload = json.loads(text)
    except ValueError:
        payload = {"text": text}
    return (not res.get("isError", False)), payload, raw


def admin(path, body=None, method="POST"):
    status, raw = http(method, path, ADMIN, body)
    assert status == 200, f"admin {path} -> {status} {raw[:300]}"
    return json.loads(raw) if raw else {}


def reset(**settings):
    fx = json.loads(json.dumps(FIXTURE))
    fx["settings"].update(settings)
    return admin("/admin/reset", fx)


def psql(sql, dsn=None):
    out = subprocess.run(["psql", dsn or APP_DSN, "-X", "-A", "-t", "-v", "ON_ERROR_STOP=1", "-c", sql],
                         capture_output=True, text=True, timeout=60)
    return out.returncode, (out.stdout + out.stderr).strip()


def page_id(token, marker):
    ok, payload, _ = call(token, "brain_search", {"query": marker})
    assert ok and payload["pages"], f"owner cannot find its own page {marker}"
    return payload["pages"][0]["id"]


class Base(unittest.TestCase):
    settings = {}

    def setUp(self):
        reset(**self.settings)

    def assertNoMarker(self, raw, *orgs):
        for org in orgs:
            self.assertNotRegex(raw, re.compile(r"CANARY-%s" % org, re.I), f"leak: a {org} page reached this caller")

    def assertSees(self, raw, *markers):
        for m in markers:
            self.assertIn(m, raw)


class Criterion1SubOrganization(Base):
    """A sub-organization's agent gets its own and global pages only."""

    def test_list_returns_own_and_global_only(self):
        ok, payload, raw = call(T_TOVELI, "brain_list", {"limit": 100})
        self.assertTrue(ok, raw)
        self.assertEqual({p["org"] for p in payload["pages"]}, {"toveli", "mgmt"})
        self.assertEqual(payload["count"], 4)  # three Toveli pages and the one global page
        self.assertEqual(len(payload["pages"]), 4)
        ok, payload, raw = call(T_TOVELI, "brain_search", {"query": "CANARY"})
        self.assertSees(raw, "CANARY-TOVELI-1", "CANARY-TOVELI-2", "CANARY-TOVELI-3", "CANARY-GLOBAL-1")
        self.assertNoMarker(raw, "SIBLING", "PERSONAL", "MGMT")

    def test_search_for_sibling_text_finds_nothing(self):
        for query in ["CANARY-SIBLING-1", "confidential roadmap", "Sibling", "services/quant", "%", "_"]:
            ok, payload, raw = call(T_TOVELI, "brain_search", {"query": query})
            self.assertTrue(ok, raw)
            self.assertNoMarker(raw, "SIBLING", "PERSONAL", "MGMT")
        ok, payload, raw = call(T_TOVELI, "brain_search", {"query": "CANARY-SIBLING-1"})
        self.assertEqual(payload["count"], 0)
        self.assertEqual(payload["pages"], [])

    def test_get_by_id_does_not_reveal_a_sibling_page(self):
        sibling_page = page_id(T_SIBLING, "CANARY-SIBLING-1")
        ok1, p1, raw1 = call(T_TOVELI, "brain_get", {"id": sibling_page})
        ok2, p2, raw2 = call(T_TOVELI, "brain_get", {"id": str(uuid.uuid4())})
        self.assertFalse(ok1)
        self.assertFalse(ok2)
        self.assertEqual(p1, p2, "a forbidden page must look exactly like a missing page")
        self.assertNoMarker(raw1, "SIBLING")
        ok, _, raw = call(T_TOVELI, "brain_get", {"path": "services/quant/run.py"})
        self.assertFalse(ok)
        self.assertNoMarker(raw, "SIBLING")

    def test_naming_another_organization_in_the_arguments_changes_nothing(self):
        for extra in [{"org": "sibling"}, {"org_id": "sibling"}, {"organization": "sibling"}, {"visibility": ["sibling"]},
                      {"as": "mgmt"}, {"source_org": "personal"}]:
            for tool, args in [("brain_list", {}), ("brain_search", {"query": "CANARY"})]:
                _, _, raw = call(T_TOVELI, tool, dict(args, **extra))
                self.assertNoMarker(raw, "SIBLING", "PERSONAL", "MGMT")

    def test_token_decides_the_organization(self):
        ok, who, _ = call(T_TOVELI, "brain_whoami")
        self.assertEqual((who["org"], who["kind"]), ("toveli", "sub"))
        ok, who, _ = call(T_SIBLING, "brain_whoami")
        self.assertEqual(who["org"], "sibling")
        _, _, raw = call(T_SIBLING, "brain_search", {"query": "CANARY"})
        self.assertSees(raw, "CANARY-SIBLING-1", "CANARY-GLOBAL-1")
        self.assertNoMarker(raw, "TOVELI", "PERSONAL", "MGMT")

    def test_missing_or_wrong_token_gets_nothing(self):
        for token in [None, "", "nope", T_TOVELI + "x", "test-token-", "' OR 1=1 --"]:
            rpc = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "brain_list", "arguments": {}}}
            status, raw = http("POST", "/mcp", token, rpc)
            self.assertIn(status, (401, 403), raw[:200])
            self.assertNotIn("CANARY", raw)

    def test_hostile_input_does_not_leak(self):
        hostile = ["' OR '1'='1", "'; SELECT body FROM brain.pages --", "\\", "%' UNION SELECT * FROM brain.pages --",
                   "CANARY-SIBLING-1' OR org_id='sibling", "\x00", "a" * 5000]
        for q in hostile:
            _, _, raw = call(T_TOVELI, "brain_search", {"query": q})
            self.assertNoMarker(raw, "SIBLING", "PERSONAL", "MGMT")
            _, _, raw = call(T_TOVELI, "brain_get", {"id": q})
            self.assertNoMarker(raw, "SIBLING", "PERSONAL", "MGMT")
            _, _, raw = call(T_TOVELI, "brain_get", {"path": q})
            self.assertNoMarker(raw, "SIBLING", "PERSONAL", "MGMT")

    def test_writes_stay_in_the_callers_organization(self):
        ok, payload, raw = call(T_TOVELI, "brain_write", {"title": "t", "body": "CANARY-TOVELI-NEW", "org": "sibling"})
        _, _, raw_sibling = call(T_SIBLING, "brain_search", {"query": "CANARY-TOVELI-NEW"})
        self.assertNotIn("CANARY-TOVELI-NEW", raw_sibling)
        ok, payload, raw = call(T_TOVELI, "brain_write", {"title": "t2", "body": "CANARY-TOVELI-NEW2"})
        self.assertTrue(ok, raw)
        _, _, raw_own = call(T_TOVELI, "brain_search", {"query": "CANARY-TOVELI-NEW2"})
        self.assertIn("CANARY-TOVELI-NEW2", raw_own)
        _, _, raw_sibling = call(T_SIBLING, "brain_search", {"query": "CANARY-TOVELI-NEW2"})
        self.assertNotIn("CANARY-TOVELI-NEW2", raw_sibling)

    def test_a_sub_organization_cannot_publish_a_global_page(self):
        ok, _, raw = call(T_TOVELI, "brain_write", {"title": "g", "body": "CANARY-TOVELI-GLOBAL", "visibility": "global"})
        _, _, raw_sibling = call(T_SIBLING, "brain_search", {"query": "CANARY-TOVELI-GLOBAL"})
        self.assertNotIn("CANARY-TOVELI-GLOBAL", raw_sibling)

    def test_provenance_is_set_by_the_service(self):
        ok, payload, raw = call(T_TOVELI, "brain_write", {"title": "p", "body": "CANARY-TOVELI-PROV", "source_type": "human"})
        self.assertTrue(ok, raw)
        _, got, _ = call(T_TOVELI, "brain_get", {"id": payload["id"]})
        self.assertEqual(got["page"]["source_type"], "agent", "an agent cannot label its page as human-written")
        ok, payload, raw = call(T_TOVELI, "brain_write", {"title": "p2", "body": "x", "source_type": "codebase"})
        _, got, _ = call(T_TOVELI, "brain_get", {"id": payload["id"]})
        self.assertEqual(got["page"]["source_type"], "agent")
        ok, payload, raw = call(T_TOVELI_HUMAN, "brain_write", {"title": "p3", "body": "x"})
        _, got, _ = call(T_TOVELI, "brain_get", {"id": payload["id"]})
        self.assertEqual(got["page"]["source_type"], "human")
        ok, listed, _ = call(T_TOVELI, "brain_list", {"source_type": "codebase"})
        self.assertEqual([p["path"] for p in listed["pages"]], ["apps/example/main.ts"])

    def test_sibling_cannot_read_a_codebase_page(self):
        for args in [{"source_type": "codebase"}, {}]:
            _, _, raw = call(T_SIBLING, "brain_list", args)
            self.assertNoMarker(raw, "TOVELI")
        ok, _, raw = call(T_SIBLING, "brain_get", {"path": "apps/example/main.ts"})
        self.assertFalse(ok)
        self.assertNoMarker(raw, "TOVELI")
        _, _, raw = call(T_SIBLING, "brain_search", {"query": "apps/example", "source_type": "codebase"})
        self.assertNoMarker(raw, "TOVELI")


@unittest.skipUnless(APP_DSN, "BRAIN_APP_DSN not set: the direct database checks were NOT RUN")
class Criterion1DatabaseItself(Base):
    """The same rules hold when the database is queried directly as the service's own role."""

    def test_no_session_means_no_rows(self):
        code, out = psql("select count(*) from brain.pages")
        self.assertEqual((code, out), (0, "0"), "without a bound session the role must see nothing")

    def test_bound_session_sees_only_its_organization(self):
        code, out = psql(f"begin; select brain.begin_session('{T_TOVELI}'); "
                         "select string_agg(distinct org_id, ',' order by org_id) from brain.pages; commit;")
        self.assertEqual(code, 0, out)
        self.assertIn("mgmt,toveli", out)
        self.assertNotIn("sibling", out)
        self.assertNotIn("personal", out)
        code, out = psql(f"begin; select brain.begin_session('{T_TOVELI}'); "
                         "select count(*) from brain.pages where body like '%CANARY-SIBLING%' or body like '%CANARY-PERSONAL%'; commit;")
        self.assertTrue(out.strip().endswith("0"), out)

    def test_session_does_not_outlive_its_transaction(self):
        code, out = psql(f"begin; select brain.begin_session('{T_TOVELI}'); commit; select count(*) from brain.pages;")
        self.assertTrue(out.strip().endswith("0"), out)

    def test_role_cannot_pick_an_organization_or_switch_off_the_policy(self):
        attempts = [
            "set app.org_id = 'sibling'; select count(*) from brain.pages",
            "select set_config('app.org_id','sibling',false); select count(*) from brain.pages",
            "set row_security = off; select count(*) from brain.pages",
            "alter table brain.pages disable row level security",
            "alter table brain.pages no force row level security",
            "set role postgres",
            "set session authorization postgres",
            "insert into brain.sessions values (pg_backend_pid(), txid_current(), 'sibling')",
            "select * from brain.principals",
            "update brain.settings set holding_reads = 'all'",
            "delete from brain.audit",
            "update brain.audit set decision = 'allow'",
            "create policy leak on brain.pages for select using (true)",
            "select brain.begin_session('wrong-token')",
        ]
        for sql in attempts:
            code, out = psql(sql)
            leaked = re.search(r"CANARY-(SIBLING|PERSONAL|MGMT)", out)
            self.assertIsNone(leaked, f"{sql!r} leaked: {out[:200]}")
            if "count(*)" in sql and code == 0:
                self.assertTrue(out.strip().endswith("0"), f"{sql!r} returned rows: {out[:200]}")
            elif "count(*)" not in sql:
                self.assertNotEqual(code, 0, f"{sql!r} should be refused, got: {out[:200]}")

    def test_role_cannot_write_into_another_organization(self):
        code, out = psql(f"begin; select brain.begin_session('{T_TOVELI}'); "
                         "insert into brain.pages (org_id, org_kind, title, body) values ('sibling','sub','x','CANARY-TOVELI-FORGED'); commit;")
        self.assertNotEqual(code, 0, out)

    def test_table_forces_row_security_and_role_is_plain(self):
        code, out = psql("select relrowsecurity::text || relforcerowsecurity::text from pg_class where oid = 'brain.pages'::regclass")
        self.assertEqual(out, "truetrue")
        code, out = psql("select rolsuper::text || rolbypassrls::text || rolcreaterole::text from pg_roles where rolname = current_user")
        self.assertEqual(out, "falsefalsefalse")


class Criterion2Holding(Base):
    """The holding organization reads its sub-organizations; never anything personal."""

    def test_holding_reads_all_pages_of_its_sub_organizations(self):
        ok, payload, raw = call(T_MGMT, "brain_search", {"query": "CANARY"})
        self.assertTrue(ok, raw)
        self.assertSees(raw, "CANARY-GLOBAL-1", "CANARY-MGMT-1", "CANARY-TOVELI-1", "CANARY-TOVELI-3", "CANARY-SIBLING-1", "CANARY-SIBLING-2")
        self.assertNoMarker(raw, "PERSONAL")

    def test_holding_cannot_write_into_a_sub_organization(self):
        ok, payload, raw = call(T_MGMT, "brain_write", {"title": "h", "body": "CANARY-MGMT-NEW", "org": "toveli"})
        _, got, _ = call(T_MGMT, "brain_search", {"query": "CANARY-MGMT-NEW"})
        self.assertTrue(all(p["org"] == "mgmt" for p in got["pages"]))

    def test_holding_can_publish_a_global_page(self):
        ok, payload, raw = call(T_MGMT, "brain_write", {"title": "g", "body": "CANARY-GLOBAL-NEW", "visibility": "global"})
        self.assertTrue(ok, raw)
        _, _, raw = call(T_SIBLING, "brain_search", {"query": "CANARY-GLOBAL-NEW"})
        self.assertIn("CANARY-GLOBAL-NEW", raw)


class Criterion2HoldingSummariesOnly(Base):
    """The stricter mode: the holding organization reads only summaries from below."""
    settings = {"holding_reads": "summaries"}

    def test_holding_reads_only_summaries(self):
        ok, payload, raw = call(T_MGMT, "brain_search", {"query": "CANARY"})
        self.assertSees(raw, "CANARY-GLOBAL-1", "CANARY-MGMT-1", "CANARY-TOVELI-2", "CANARY-SIBLING-2")
        for hidden in ["CANARY-TOVELI-1", "CANARY-TOVELI-3", "CANARY-SIBLING-1", "CANARY-SIBLING-3"]:
            self.assertNotIn(hidden, raw)
        self.assertNoMarker(raw, "PERSONAL")


class Criterion3Personal(Base):
    """Nothing goes from personal to an organization except an approved, curated briefing."""

    def test_no_organization_reads_a_personal_page(self):
        personal_page = page_id(T_PERSONAL, "CANARY-PERSONAL-1")
        for token in [T_MGMT, T_TOVELI, T_SIBLING, T_TOVELI_HUMAN]:
            for tool, args in [("brain_list", {"limit": 100}), ("brain_search", {"query": "CANARY"}),
                               ("brain_search", {"query": "goals"}), ("brain_get", {"id": personal_page})]:
                _, _, raw = call(token, tool, args)
                self.assertNoMarker(raw, "PERSONAL")

    def test_personal_reads_its_organizations(self):
        ok, payload, raw = call(T_PERSONAL, "brain_search", {"query": "CANARY", "limit": 100})
        self.assertTrue(ok, raw)
        self.assertSees(raw, "CANARY-PERSONAL-1", "CANARY-PERSONAL-2", "CANARY-MGMT-1", "CANARY-TOVELI-1", "CANARY-SIBLING-1", "CANARY-GLOBAL-1")

    def test_personal_cannot_write_into_an_organization(self):
        ok, payload, raw = call(T_PERSONAL, "brain_write", {"title": "x", "body": "CANARY-PERSONAL-COPY", "org": "mgmt"})
        for token in [T_MGMT, T_TOVELI, T_SIBLING]:
            _, _, raw = call(token, "brain_search", {"query": "CANARY-PERSONAL-COPY"})
            self.assertNotIn("CANARY-PERSONAL-COPY", raw)
        ok, payload, raw = call(T_PERSONAL, "brain_write", {"title": "x", "body": "CANARY-PERSONAL-GLOBAL", "visibility": "global"})
        for token in [T_MGMT, T_TOVELI, T_SIBLING]:
            _, _, raw = call(token, "brain_search", {"query": "CANARY-PERSONAL-GLOBAL"})
            self.assertNotIn("CANARY-PERSONAL-GLOBAL", raw)

    def test_health_and_finance_pages_only_exist_in_personal(self):
        for sensitivity in ["health", "finance"]:
            for token in [T_TOVELI, T_MGMT, T_TOVELI_HUMAN]:
                ok, payload, raw = call(token, "brain_write", {"title": "s", "body": "CANARY-SENSITIVE", "sensitivity": sensitivity})
                self.assertFalse(ok, f"{sensitivity} page accepted outside personal: {raw[:200]}")
            ok, payload, raw = call(T_PERSONAL, "brain_write", {"title": "s", "body": "CANARY-PERSONAL-S", "sensitivity": sensitivity})
            self.assertTrue(ok, raw)
        _, _, raw = call(T_MGMT, "brain_search", {"query": "CANARY-SENSITIVE"})
        self.assertNotIn("CANARY-SENSITIVE", raw)

    def test_only_personal_can_publish_a_briefing(self):
        for token in [T_MGMT, T_TOVELI, T_SIBLING]:
            ok, payload, raw = call(token, "publish_briefing", {"content": "CANARY-BRIEFING-FORGED"})
            self.assertFalse(ok, raw)

    def test_briefing_reaches_the_holding_organization_only_after_approval(self):
        ok, payload, raw = call(T_PERSONAL, "publish_briefing", {"content": "CANARY-BRIEFING-1 priorities for this week."})
        self.assertTrue(ok, raw)
        self.assertEqual(payload["status"], "pending")
        _, _, raw = call(T_MGMT, "brain_search", {"query": "CANARY-BRIEFING-1"})
        self.assertNotIn("CANARY-BRIEFING-1", raw, "a briefing must not be visible before the human approves it")
        admin("/admin/approve_briefing", {"briefing_id": payload["briefing_id"], "approver": "cole"})
        _, got, raw = call(T_MGMT, "brain_search", {"query": "CANARY-BRIEFING-1"})
        self.assertIn("CANARY-BRIEFING-1", raw)
        self.assertEqual(got["pages"][0]["kind"], "briefing")
        for token in [T_TOVELI, T_SIBLING]:
            _, _, raw = call(token, "brain_search", {"query": "CANARY-BRIEFING-1"})
            self.assertNotIn("CANARY-BRIEFING-1", raw, "a briefing goes to the holding organization only")
        _, _, raw = call(T_MGMT, "brain_search", {"query": "CANARY"})
        self.assertNoMarker(raw, "PERSONAL")

    def test_briefing_is_short_and_curated(self):
        ok, payload, raw = call(T_PERSONAL, "publish_briefing", {"content": "x" * 2001})
        self.assertFalse(ok, "a briefing over 2,000 characters must be refused")
        ok, payload, raw = call(T_PERSONAL, "publish_briefing", {"content": ""})
        self.assertFalse(ok)

    def test_an_agent_cannot_approve_its_own_briefing(self):
        ok, payload, _ = call(T_PERSONAL, "publish_briefing", {"content": "CANARY-BRIEFING-2"})
        for token in [T_PERSONAL, T_MGMT, None]:
            status, raw = http("POST", "/admin/approve_briefing", token, {"briefing_id": payload["briefing_id"], "approver": "agent"})
            self.assertIn(status, (401, 403))
        _, _, raw = call(T_MGMT, "brain_search", {"query": "CANARY-BRIEFING-2"})
        self.assertNotIn("CANARY-BRIEFING-2", raw)


class Criterion3BriefingSwitchedOff(Base):
    settings = {"briefing_enabled": False}

    def test_nothing_goes_from_personal_to_any_organization(self):
        ok, payload, raw = call(T_PERSONAL, "publish_briefing", {"content": "CANARY-BRIEFING-OFF"})
        self.assertFalse(ok, raw)
        for token in [T_MGMT, T_TOVELI, T_SIBLING]:
            _, _, raw = call(token, "brain_search", {"query": "CANARY"})
            self.assertNoMarker(raw, "PERSONAL", "BRIEFING")

    def test_switching_off_hides_earlier_briefings(self):
        admin("/admin/settings", {"briefing_enabled": True})
        ok, payload, _ = call(T_PERSONAL, "publish_briefing", {"content": "CANARY-BRIEFING-3"})
        admin("/admin/approve_briefing", {"briefing_id": payload["briefing_id"], "approver": "cole"})
        _, _, raw = call(T_MGMT, "brain_search", {"query": "CANARY-BRIEFING-3"})
        self.assertIn("CANARY-BRIEFING-3", raw)
        admin("/admin/settings", {"briefing_enabled": False})
        _, _, raw = call(T_MGMT, "brain_search", {"query": "CANARY-BRIEFING-3"})
        self.assertNotIn("CANARY-BRIEFING-3", raw)


class PersonalSpaceSwitchedOff(Base):
    """The product also has to run as organizations only."""
    settings = {"personal_enabled": False}

    def test_personal_token_stops_working(self):
        rpc = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "brain_list", "arguments": {}}}
        status, raw = http("POST", "/mcp", T_PERSONAL, rpc)
        self.assertIn(status, (401, 403))
        self.assertNotIn("CANARY", raw)

    def test_organizations_work_as_before(self):
        _, _, raw = call(T_TOVELI, "brain_search", {"query": "CANARY"})
        self.assertSees(raw, "CANARY-TOVELI-1", "CANARY-GLOBAL-1")
        self.assertNoMarker(raw, "SIBLING", "PERSONAL", "MGMT")
        _, _, raw = call(T_MGMT, "brain_search", {"query": "CANARY"})
        self.assertSees(raw, "CANARY-TOVELI-1", "CANARY-SIBLING-1")
        self.assertNoMarker(raw, "PERSONAL")


class SingleCompany(unittest.TestCase):
    """One company, no layer above it, no personal space."""

    def test_one_organization_alone(self):
        fx = {"settings": {"personal_enabled": False, "briefing_enabled": False, "holding_reads": "all"},
              "orgs": [{"id": "solo", "kind": "holding", "parent": None}],
              "principals": [{"org": "solo", "actor": "agent", "token": "test-token-solo-agent"}],
              "pages": [{"org": "solo", "title": "Only page", "body": "CANARY-SOLO-1", "kind": "note", "source_type": "human"}]}
        admin("/admin/reset", fx)
        ok, payload, raw = call("test-token-solo-agent", "brain_list", {})
        self.assertTrue(ok, raw)
        self.assertEqual(payload["count"], 1)
        ok, payload, raw = call("test-token-solo-agent", "brain_write", {"title": "n", "body": "CANARY-SOLO-2"})
        self.assertTrue(ok, raw)
        ok, payload, raw = call(T_TOVELI, "brain_list", {})
        self.assertFalse(ok)


class Criterion4OwnAuditLog(Base):
    """The service's half of criterion 4: every call, allowed or denied, is logged."""

    def test_every_call_is_logged_with_its_decision(self):
        before = admin("/admin/audit?since_id=0", method="GET")
        last = max([r["id"] for r in before["rows"]] or [0])
        sibling_page = page_id(T_SIBLING, "CANARY-SIBLING-1")
        last = max(r["id"] for r in admin("/admin/audit?since_id=0", method="GET")["rows"])
        rid = {name: str(uuid.uuid4()) for name in ["list", "get_denied", "write_denied", "briefing_denied"]}
        rpc = lambda tool, args: http("POST", "/mcp", T_TOVELI, {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                                                  "params": {"name": tool, "arguments": args}})
        rpc("brain_list", {"request_id": rid["list"]})
        rpc("brain_get", {"id": sibling_page, "request_id": rid["get_denied"]})
        rpc("brain_write", {"title": "s", "body": "b", "sensitivity": "health", "request_id": rid["write_denied"]})
        rpc("publish_briefing", {"content": "x", "request_id": rid["briefing_denied"]})
        http("POST", "/mcp", "wrong-token", {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "brain_list", "arguments": {}}})
        rows = admin(f"/admin/audit?since_id={last}", method="GET")["rows"]
        by_rid = {r["request_id"]: r for r in rows if r.get("request_id")}
        self.assertEqual((by_rid[rid["list"]]["decision"], by_rid[rid["list"]]["org"], by_rid[rid["list"]]["tool"]), ("allow", "toveli", "brain_list"))
        for name in ["get_denied", "write_denied", "briefing_denied"]:
            self.assertEqual(by_rid[rid[name]]["decision"], "deny", name)
        self.assertTrue(any(r["decision"] == "deny" and r["reason"] == "invalid_token" for r in rows), "a rejected token must be logged too")
        self.assertEqual(len([r for r in rows if r["org"] == "toveli"]), 4)
        self.assertNotIn("CANARY", json.dumps(rows), "the audit log holds decisions, not page content")


if __name__ == "__main__":
    unittest.main(verbosity=2)
