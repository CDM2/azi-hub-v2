"""REV-01 review of R-02, criteria 1 to 4: attacks on the permission service, called directly.

Every test states what ../service/CONTRACT.md or V-000 requires and asserts it. So:
  - a test that PASSES is an attack that the service held;
  - a test that FAILS is a defect, and its docstring names the finding in docs/reviews/REV-01_R-01_AND_R-02.md.
The failing tests are meant to go green when the fixes land. Nothing here changes the service.

Run:  BRAIN_URL=... BRAIN_ADMIN_TOKEN=... BRAIN_APP_DSN=... python3 -m unittest -v test_rev01_attacks
Standard library only. Made-up data only.
"""
import concurrent.futures as cf
import hashlib
import json
import random
import re
import statistics
import time
import unittest
import uuid

from common import (ADMIN, APP_DSN, T_MGMT, T_PERSONAL, T_SIBLING, T_TOVELI, T_TOVELI_HUMAN, admin, audit_rows, call, http_call,
                    last_audit_id, page_id, psql, raw_request, reset, rpc)

OTHERS = re.compile(r"CANARY-(SIBLING|PERSONAL|MGMT)", re.I)


class Base(unittest.TestCase):
    settings = {}

    def setUp(self):
        reset(**self.settings)


# ------------------------------------------------------------------------------------------------ held

class Held(Base):
    """Attacks that the service held. These pass."""

    def test_agent_cannot_forge_page_kind_path_meta_or_owner(self):
        """brain_write accepts only notes and summaries in the caller's own organization (contract rules 1, 9)."""
        for kind in ["briefing", "code_file", "code_overview", "code_package"]:
            ok, payload, raw = call(T_MGMT, "brain_write", {"title": "forged", "body": "CANARY-FORGED-KIND", "kind": kind})
            self.assertFalse(ok, f"an agent created a page of kind {kind}: {raw[:200]}")
        ok, payload, raw = call(T_TOVELI, "brain_write", {"title": "t", "body": "CANARY-TOVELI-EXTRA", "path": "services/quant/run.py",
                                                         "org_id": "sibling", "org_kind": "holding", "meta": {"x": 1}, "id": str(uuid.uuid4()),
                                                         "source_type": "codebase", "content_sha": "x"})
        self.assertTrue(ok, raw)
        _, got, _ = call(T_TOVELI, "brain_get", {"id": payload["id"]})
        self.assertEqual((got["page"]["org"], got["page"]["path"], got["page"]["source_type"], got["page"]["meta"]), ("toveli", None, "agent", {}))
        _, _, raw = call(T_SIBLING, "brain_search", {"query": "CANARY-TOVELI-EXTRA"})
        self.assertNotIn("CANARY-TOVELI-EXTRA", raw)

    def test_every_admin_route_refuses_agent_and_human_tokens(self):
        routes = [("POST", "/admin/reset"), ("POST", "/admin/settings"), ("POST", "/admin/approve_briefing"), ("POST", "/admin/codebase_sync"),
                  ("GET", "/admin/audit?since_id=0"), ("GET", "/admin/pages_digest?org=sibling"), ("GET", "/admin/"), ("POST", "/admin/nope")]
        for method, path in routes:
            for token in [T_TOVELI, T_TOVELI_HUMAN, T_MGMT, T_PERSONAL, None, "", ADMIN + "x", ADMIN[:-1]]:
                status, raw = http_call(method, path, token, {} if method == "POST" else None)
                self.assertEqual(status, 401, f"{method} {path} with {str(token)[:12]!r}: {status} {raw[:120]}")
                self.assertNotIn("CANARY", raw)

    def test_batch_requests_and_odd_json_do_not_leak(self):
        sibling_page = page_id(T_SIBLING, "CANARY-SIBLING-1")
        batch = [{"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": name, "arguments": args}} for i, (name, args) in enumerate([
            ("brain_get", {"id": sibling_page}), ("brain_list", {"limit": 10 ** 9}), ("brain_list", {"limit": -5, "kind": "briefing"}),
            ("brain_search", {"query": "CANARY", "source_type": ["codebase"]}), ("brain_search", {"query": {"$ne": None}}),
            ("brain_get", {"id": sibling_page, "path": "services/quant/run.py"}), ("brain_get", {"id": [sibling_page]}),
            ("brain_get", {"path": "services/quant/run.py\n"}), ("brain_get", {"path": "SERVICES/QUANT/RUN.PY"}),
            ("brain_list", {"source_type": "codebase' or '1'='1"})])]
        status, raw = http_call("POST", "/mcp", T_TOVELI, batch)
        self.assertEqual(status, 200)
        self.assertIsNone(OTHERS.search(raw), raw[:300])
        for body in ["null", "[]", "[null, 1, \"x\"]", "{\"method\": \"tools/call\"}", "{\"method\": \"tools/call\", \"params\": \"brain_list\"}"]:
            status, raw = raw_request("POST", "/mcp", [("Authorization", "Bearer " + T_TOVELI), ("Content-Type", "application/json")], body.encode())
            self.assertIsNone(OTHERS.search(raw), raw[:300])

    def test_concurrent_callers_never_see_each_others_pages(self):
        """The session is bound per transaction on pooled connections. 400 interleaved calls from three organizations."""
        plan = [(T_TOVELI, "TOVELI", ("SIBLING", "PERSONAL", "MGMT")), (T_SIBLING, "SIBLING", ("TOVELI", "PERSONAL", "MGMT")),
                (T_MGMT, "MGMT", ("PERSONAL",)), (T_PERSONAL, "PERSONAL", ())] * 100
        random.shuffle(plan)

        def one(item):
            token, own, forbidden = item
            ok, payload, raw = call(token, "brain_search", {"query": "CANARY", "limit": 100})
            _, listed, raw_list = call(token, "brain_list", {"limit": 100})
            orgs = {p["org"] for p in listed.get("pages", [])}
            allowed = {"TOVELI": {"toveli", "mgmt"}, "SIBLING": {"sibling", "mgmt"}, "MGMT": {"mgmt", "toveli", "sibling"},
                       "PERSONAL": {"personal", "mgmt", "toveli", "sibling"}}[own]
            leaked = [f for f in forbidden if f"CANARY-{f}" in raw] + sorted(orgs - allowed)
            return leaked, (ok and f"CANARY-{own}" in raw and own.lower() in orgs)

        with cf.ThreadPoolExecutor(max_workers=24) as ex:
            results = list(ex.map(one, plan))
        self.assertEqual([r[0] for r in results if r[0]], [], "a caller received another organization's marker under load")
        self.assertTrue(all(r[1] for r in results), "a caller did not receive its own pages under load")

    def test_holding_in_summaries_mode_cannot_reach_a_note_by_id_or_path(self):
        note, code = page_id(T_TOVELI, "CANARY-TOVELI-1"), page_id(T_TOVELI, "CANARY-TOVELI-3")
        admin("/admin/settings", {"holding_reads": "summaries"})
        for args in [{"id": note}, {"id": code}, {"path": "apps/example/main.ts"}]:
            ok, _, raw = call(T_MGMT, "brain_get", args)
            self.assertFalse(ok, raw[:200])
        _, payload, raw = call(T_MGMT, "brain_list", {"source_type": "codebase"})
        self.assertEqual(payload["count"], 0)

    def test_a_briefing_cannot_be_approved_twice_or_by_a_human_token(self):
        ok, payload, _ = call(T_PERSONAL, "publish_briefing", {"content": "CANARY-BRIEFING-R0"})
        for token in [T_TOVELI_HUMAN, T_PERSONAL, T_MGMT]:
            status, _ = http_call("POST", "/admin/approve_briefing", token, {"briefing_id": payload["briefing_id"], "approver": "x"})
            self.assertEqual(status, 401)
        admin("/admin/approve_briefing", {"briefing_id": payload["briefing_id"], "approver": "cole"})
        status, _ = http_call("POST", "/admin/approve_briefing", ADMIN, {"briefing_id": payload["briefing_id"], "approver": "cole"})
        self.assertNotEqual(status, 200, "the same briefing was approved a second time")
        _, got, _ = call(T_MGMT, "brain_search", {"query": "CANARY-BRIEFING-R0"})
        self.assertEqual(got["count"], 1)


@unittest.skipUnless(APP_DSN, "BRAIN_APP_DSN not set: the direct database checks were NOT RUN")
class HeldInTheDatabase(Base):
    """Attacks on the session binding and the definer functions, as the service's own database role. These pass."""

    def test_temp_objects_and_search_path_do_not_change_the_bound_organization(self):
        bind = f"begin; select brain.begin_session('{T_TOVELI}'); "
        attempts = [
            "create temp table sessions (pid int, txid bigint, org_id text, actor text); insert into sessions values (pg_backend_pid(), txid_current(), 'sibling', 'agent');",
            "create temp table orgs (id text, kind text, parent_id text); insert into orgs values ('toveli', 'personal', null);",
            "create temp table settings (personal_enabled boolean, briefing_enabled boolean, holding_reads text); insert into settings values (true, true, 'all');",
            "set local search_path = pg_temp, brain; create function pg_temp.current_org() returns text language sql as $$ select 'sibling' $$; "
            "create function pg_temp.can_read(text, text, text, text) returns boolean language sql as $$ select true $$;",
            "savepoint s; select brain.begin_session('wrong-token');",
            "create temp view v as select * from brain.pages; select count(*) from v where org_id = 'sibling';",
        ]
        for extra in attempts:
            code, out = psql(bind + extra + " select 'ORGS=' || coalesce(string_agg(distinct org_id, ',' order by org_id), '') from brain.pages; commit;")
            m = re.search(r"ORGS=(\S*)", out)
            if m:
                self.assertEqual(m.group(1), "mgmt,toveli", f"{extra[:60]!r}: {out[-200:]}")
            self.assertIsNone(OTHERS.search(out), out[-300:])

    def test_a_savepoint_rollback_unbinds_the_session(self):
        code, out = psql(f"begin; savepoint s; select brain.begin_session('{T_TOVELI}'); rollback to s; select count(*) from brain.pages; commit;")
        self.assertTrue(out.strip().endswith("0"), out)

    def test_copy_returning_and_other_statement_forms_respect_the_policy(self):
        bind = f"begin; select brain.begin_session('{T_TOVELI}'); "
        for sql in ["copy brain.pages to stdout;", "copy (select body from brain.pages where org_id in ('sibling', 'personal')) to stdout;",
                    "select body from brain.pages tablesample bernoulli (100);",
                    "insert into brain.pages (org_id, org_kind, title, body) values ('toveli', 'sub', 'x', 'y') "
                    "returning (select string_agg(body, '|') from brain.pages where org_id <> 'toveli' and visibility = 'org');",
                    "select body from brain.pages where org_id = 'sibling' for share;",
                    "with x as materialized (select body from brain.pages) select * from x;"]:
            code, out = psql(bind + sql + " rollback;")
            self.assertIsNone(OTHERS.search(out), f"{sql!r} leaked: {out[:200]}")


# ---------------------------------------------------------------------------------------------- defects

class RelayThroughTheHoldingAgent(Base):
    """REV-01 finding RV-02. An agent, with no human step, moves pages across tiers by writing a global page."""

    def test_a_siblings_page_cannot_reach_another_venture_without_a_human_decision(self):
        """N-02: organization to organization is zero by default. N-03: code decides, not a prompt.
        Calls: mgmt agent brain_search -> mgmt agent brain_write visibility=global -> toveli agent brain_search."""
        _, found, _ = call(T_MGMT, "brain_search", {"query": "CANARY-SIBLING-1"})
        text = found["pages"][0]["snippet"]
        ok, written, raw = call(T_MGMT, "brain_write", {"title": "relay", "body": "relayed: " + text, "visibility": "global"})
        _, _, raw_toveli = call(T_TOVELI, "brain_search", {"query": "confidential roadmap"})
        self.assertNotIn("CANARY-SIBLING-1", raw_toveli,
                         "the sibling's text reached the toveli agent through a global page that the holding AGENT wrote; no human approved it")

    def test_a_personal_briefing_stays_in_the_holding_organization(self):
        """F-25 and contract rule 6: the briefing goes to the holding organization only, and the switch hides earlier briefings."""
        ok, b, _ = call(T_PERSONAL, "publish_briefing", {"content": "CANARY-BRIEFING-R1 personal priorities"})
        admin("/admin/approve_briefing", {"briefing_id": b["briefing_id"], "approver": "cole"})
        _, found, _ = call(T_MGMT, "brain_search", {"query": "CANARY-BRIEFING-R1"})
        call(T_MGMT, "brain_write", {"title": "relay", "body": "relay: " + found["pages"][0]["snippet"], "visibility": "global"})
        _, _, raw = call(T_SIBLING, "brain_search", {"query": "CANARY-BRIEFING-R1"})
        self.assertNotIn("CANARY-BRIEFING-R1", raw, "the approved briefing's text reached a sub-organization through an agent-written global page")

    def test_switching_briefings_off_removes_personal_text_from_every_organization(self):
        ok, b, _ = call(T_PERSONAL, "publish_briefing", {"content": "CANARY-BRIEFING-R2 personal priorities"})
        admin("/admin/approve_briefing", {"briefing_id": b["briefing_id"], "approver": "cole"})
        _, found, _ = call(T_MGMT, "brain_search", {"query": "CANARY-BRIEFING-R2"})
        call(T_MGMT, "brain_write", {"title": "copy", "body": "copy: " + found["pages"][0]["snippet"]})
        admin("/admin/settings", {"briefing_enabled": False})
        _, _, raw = call(T_MGMT, "brain_search", {"query": "CANARY-BRIEFING-R2"})
        self.assertNotIn("CANARY-BRIEFING-R2", raw, "after the switch is off the holding organization still reads the briefing's text, in a copy an agent made")


class TimingAndScale(Base):
    """REV-01 findings RV-05 and RV-06. Contract rule 3: a sibling's pages are never returned and their existence is not revealed."""

    @staticmethod
    def _time_get(token, args, n):
        out = []
        for _ in range(n):
            t0 = time.perf_counter_ns()
            status, raw = rpc(token, "brain_get", args() if callable(args) else args)
            out.append((time.perf_counter_ns() - t0) / 1000.0)
            assert "not_found" in raw, raw[:200]
        return out

    def test_a_forbidden_page_takes_as_long_as_a_missing_page(self):
        """RV-06. brain_get for a path that exists in another organization, against a path that exists nowhere.
        Both answers are {"error":"not_found"}. 400 interleaved pairs; the median difference must be under 100 microseconds."""
        self._time_get(T_TOVELI, {"path": "services/quant/run.py"}, 40)                     # warm-up
        a, b = [], []
        for _ in range(400):
            pair = [("a", {"path": "services/quant/run.py"}), ("b", {"path": "services/quant/rux.py"})]
            random.shuffle(pair)
            for which, args in pair:
                (a if which == "a" else b).extend(self._time_get(T_TOVELI, args, 1))
        diff = statistics.median(a) - statistics.median(b)
        boots = sorted(statistics.median(random.choices(a, k=len(a))) - statistics.median(random.choices(b, k=len(b))) for _ in range(300))
        low, high = boots[7], boots[292]
        print(f"\n    RV-06 timing: forbidden {statistics.median(a):.0f} us, missing {statistics.median(b):.0f} us, "
              f"difference {diff:.0f} us (95% interval {low:.0f} to {high:.0f})")
        self.assertLess(abs(diff), 100, f"a page that exists in another organization answers {diff:.0f} microseconds slower than a missing page "
                                        f"(95% interval {low:.0f} to {high:.0f}); the same error text hides nothing")

    def test_a_callers_latency_does_not_depend_on_other_organizations_pages(self):
        """RV-05. 1,500 made-up pages are added to the SIBLING. The toveli agent's own list (4 pages) must not get slower."""
        def median_ms(n=7):
            ts = []
            for _ in range(n):
                t0 = time.perf_counter()
                ok, payload, _ = call(T_TOVELI, "brain_list", {"limit": 50})
                ts.append((time.perf_counter() - t0) * 1000)
                assert ok and payload["count"] == 4
            return statistics.median(ts)
        before = median_ms()
        ups = [{"path": f"gen/{i:05d}.py", "title": f"Code: gen/{i:05d}.py", "body": f"made-up page {i}", "kind": "code_file",
                "content_sha": hashlib.sha1(str(i).encode()).hexdigest()} for i in range(1500)]
        admin("/admin/codebase_sync", {"org": "sibling", "upserts": ups})
        after = median_ms()
        print(f"\n    RV-05 scale: toveli brain_list {before:.1f} ms before, {after:.1f} ms after 1,500 pages were added to the sibling")
        self.assertLess(after, before * 3 + 5, f"toveli's list went from {before:.1f} ms to {after:.1f} ms when the sibling gained 1,500 pages: "
                                               "the caller can measure how much other organizations hold, and reads slow down for everyone")


class AuditCompleteness(Base):
    """REV-01 finding RV-07 (and RV-19 for the last test). Contract rule 10: every call, allowed or denied, is written to the audit log."""

    def test_a_nul_byte_in_request_id_does_not_remove_the_call_from_the_audit_log(self):
        """RV-07. Six calls with request_id "rev01\\u0000nul": a denied get by a sibling's path, a denied briefing, an unknown tool, and three others."""
        before = last_audit_id()
        calls = [("brain_get", {"path": "services/quant/run.py"}), ("brain_get", {"id": str(uuid.uuid4())}), ("publish_briefing", {"content": "x"}),
                 ("brain_admin_dump", {}), ("brain_list", {}), ("brain_write", {"title": "t", "body": "CANARY-TOVELI-NUL"})]
        for tool, args in calls:
            status, raw = rpc(T_TOVELI, tool, dict(args, request_id="rev01\u0000nul"))
            self.assertEqual(status, 200)
        rows = [r for r in audit_rows(before) if r["org"] == "toveli"]
        self.assertEqual(len(rows), len(calls), f"{len(calls)} calls were made and {len(rows)} audit rows exist: {[(r['tool'], r['decision']) for r in rows]}")

    def test_the_audit_row_names_the_tool_that_ran(self):
        """RV-07. tools/call with name ["brain_list"] (a JSON array) runs brain_list."""
        before = last_audit_id()
        status, raw = rpc(T_TOVELI, ["brain_list"], {"request_id": "rev01-array-name"})
        ran = '\\"pages\\"' in raw
        rows = [r for r in audit_rows(before) if r["request_id"] == "rev01-array-name"]
        self.assertTrue(rows, "no audit row at all")
        if ran:
            self.assertEqual(rows[0]["tool"], "brain_list", f"brain_list ran and the audit log calls it {rows[0]['tool']!r}")
        else:
            self.assertEqual(rows[0]["decision"], "deny")

    def test_a_tool_name_from_the_object_prototype_is_an_unknown_tool(self):
        """RV-07. "constructor", "__proto__" and "toString" must be answered and logged like any tool that does not exist."""
        before = last_audit_id()
        _, expected = rpc(T_TOVELI, "no_such_tool", {"request_id": "rev01-unknown"})
        for name in ["constructor", "__proto__", "toString", "hasOwnProperty"]:
            _, raw = rpc(T_TOVELI, name, {"request_id": "rev01-" + name})
            self.assertEqual(json.loads(raw)["result"], json.loads(expected)["result"], f"{name}: {raw[:160]}")
        reasons = {r["request_id"]: r["reason"] for r in audit_rows(before) if (r["request_id"] or "").startswith("rev01-")}
        self.assertEqual(set(reasons.values()), {"unknown_tool"}, reasons)

    @unittest.skipUnless(APP_DSN, "BRAIN_APP_DSN not set: NOT RUN")
    def test_the_database_role_cannot_write_an_audit_row_without_a_bound_session(self):
        """RV-19. schema.sql says the audit row "is stamped from the bound session". With no session the role can still write any row it likes."""
        before = last_audit_id()
        code, out = psql("select brain.audit_log('admin_reset', 'rev01-forged', 'allow', null, 'x')")
        forged = [r for r in audit_rows(before) if r["request_id"] == "rev01-forged"]
        self.assertFalse(forged, f"a row with no organization and an invented tool name was accepted: {forged}")


class AdminAndTokenHandling(Base):
    """REV-01 findings RV-16 and RV-17."""

    def test_a_wrong_admin_token_is_always_answered_401(self):
        """RV-16. A wrong token whose length in characters equals the real one, but which holds a byte above 0x7f, must get 401 like any other."""
        seen = {}
        for n in sorted({8, 16, 24, 32, 40, 48, 64, len(ADMIN) - 1, len(ADMIN), len(ADMIN) + 1}):
            status, _ = raw_request("GET", "/admin/audit?since_id=999999999", [("Authorization", b"Bearer " + b"\xe9" * n)])
            seen[n] = status
        self.assertEqual(set(seen.values()), {401}, f"status by token length: {seen}. The length that answers 500 is the admin token's length.")

    def test_only_the_documented_header_form_carries_a_token(self):
        """RV-17. The contract documents one form: Authorization: Bearer <token>."""
        accepted = []
        for headers in [{"X-Brain-Token": T_TOVELI}, {"X-Brain-Token": "Bearer " + T_TOVELI}, {"Authorization": T_TOVELI}]:
            status, raw = rpc(None, "brain_whoami", {}, headers)
            if status == 200:
                accepted.append(list(headers.items())[0][0] + ": " + list(headers.values())[0][:11] + "...")
        self.assertEqual(accepted, [], f"undocumented forms were accepted: {accepted}")


class BriefingApproval(Base):
    """REV-01 finding RV-15."""

    def test_an_approval_names_its_approver(self):
        """RV-15. Contract rule 6: approved by the human. The approver is free text and may be empty."""
        ok, b, _ = call(T_PERSONAL, "publish_briefing", {"content": "CANARY-BRIEFING-R3"})
        status, raw = http_call("POST", "/admin/approve_briefing", ADMIN, {"briefing_id": b["briefing_id"], "approver": ""})
        self.assertNotEqual(status, 200, "a briefing was approved with an empty approver")

    def test_nothing_new_leaves_the_personal_space_while_it_is_switched_off(self):
        """RV-15. Contract rule 7: with the personal space off the product runs as organizations only."""
        ok, b, _ = call(T_PERSONAL, "publish_briefing", {"content": "CANARY-BRIEFING-R4 pending when the space was switched off"})
        admin("/admin/settings", {"personal_enabled": False})
        status, raw = http_call("POST", "/admin/approve_briefing", ADMIN, {"briefing_id": b["briefing_id"], "approver": "cole"})
        _, _, found = call(T_MGMT, "brain_search", {"query": "CANARY-BRIEFING-R4"})
        self.assertNotIn("CANARY-BRIEFING-R4", found, "a briefing was approved into the holding organization while the personal space was off")


class PathLookupAcrossOrganizations(unittest.TestCase):
    """REV-01 finding RV-18. brain_get by path returns the first organization by name; the reader cannot say which one it means."""

    def test_a_reader_of_several_organizations_can_fetch_each_ones_page_at_the_same_path(self):
        fx = {"settings": {}, "orgs": [{"id": "mgmt", "kind": "holding", "parent": None}, {"id": "alpha", "kind": "sub", "parent": "mgmt"},
                                       {"id": "toveli", "kind": "sub", "parent": "mgmt"}],
              "principals": [{"org": "mgmt", "actor": "agent", "token": "rev01-mgmt"}],
              "pages": [{"org": o, "title": "Code: README.md", "body": f"CANARY-{o.upper()}-README", "kind": "code_file", "source_type": "codebase",
                         "path": "README.md"} for o in ["alpha", "toveli"]]}
        admin("/admin/reset", fx)
        got = set()
        for args in [{"path": "README.md"}, {"path": "README.md", "org": "toveli"}, {"path": "toveli/README.md"}, {"path": "toveli:README.md"}]:
            ok, payload, raw = call("rev01-mgmt", "brain_get", args)
            if ok:
                got.add(payload["page"]["org"])
        self.assertEqual(got, {"alpha", "toveli"}, f"by path the holding agent can only ever get the page of {sorted(got)}; "
                                                   "whichever organization sorts first answers for every other one")


@unittest.skipUnless(APP_DSN, "BRAIN_APP_DSN not set: NOT RUN")
class WhatTheDatabaseRoleLearnsWithoutASession(Base):
    """REV-01 finding RV-19. R-02 section 7: "the database refusing the application role when no session is bound"."""

    def test_explain_analyze_does_not_reveal_another_organizations_paths(self):
        plan = "explain (analyze, costs off, timing off, summary off) select 1 from brain.pages where org_id = 'sibling' and path = '%s'"
        code, exists = psql(plan % "services/quant/run.py")
        code, missing = psql(plan % "services/quant/nope.py")
        removed = lambda text: (re.search(r"Rows Removed by Filter: (\d+)", text) or [None, "0"])[1]
        self.assertEqual(removed(exists), removed(missing),
                         f"with no token at all the role can tell a sibling path that exists (rows removed {removed(exists)}) from one that does not "
                         f"({removed(missing)}), and can walk every path by range")


if __name__ == "__main__":
    unittest.main(verbosity=2)
