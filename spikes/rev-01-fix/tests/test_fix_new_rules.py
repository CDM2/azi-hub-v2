"""REV-01 fix pass: tests for the rules the fix added. None of these existed before.

The copied tests (test_criteria_1_3, test_rev01_attacks, test_rev01_second_person) show that what the review found is
closed. These show that what was built to close it does what ../service/CONTRACT.md says, and nothing more:
approval by a person, pushes, per-venture and per-person switches, and the log.

Made-up data only. Standard library only. Paperclip is not involved and was not run.
Run:  BRAIN_URL=... BRAIN_ADMIN_TOKEN=... BRAIN_APP_DSN=... [SUPER_DSN=...] python3 -m unittest -v test_fix_new_rules
The tests that tamper with the log as a database superuser need SUPER_DSN and say NOT RUN without it.
"""
import contextlib
import hashlib
import json
import os
import statistics
import time
import unittest
import uuid

from common import ADMIN, APP_DSN, SUPER_DSN, admin, audit_rows, call, http_call, last_audit_id, page_id, psql, raw_request, rpc
from test_rev01_second_person import TOK, fixture, markers

COLE, FRIEND = TOK("personal", "human"), TOK("friend-personal", "human")     # each person, as a person, in their own personal space
FRIEND_IN_SHARED = TOK("shared", "human")                                   # the friend, as a person, in the shared venture
NOT_FOUND, FORBIDDEN = {"error": "not_found"}, {"error": "forbidden"}


def sees(token, marker):
    ok, _, raw = call(token, "brain_search", {"query": marker})
    return ok and marker in raw


def who_sees(marker, orgs):
    return [o for o in orgs if sees(TOK(o), marker)]


T_LIST, T_SEARCH = "brain.t_list(text, text, text, text, int)", "brain.t_search(text, text, text, text, int)"


@contextlib.contextmanager
def worst_case(*functions, allow_scans=False):
    """As a database superuser, put the named read functions into the conditions under which a missing protection shows, then put
    them back as they were. PostgreSQL plans a statement afresh the first five times a connection runs it and may then keep one plan
    made without looking at the caller's actual organizations. That kept plan is the unfavourable one for both protections, so it is
    forced here. `allow_scans` also takes the scan setting off, which is what leaves the fence standing alone."""
    had = {fn: "enable_seqscan=off" in psql(f"select coalesce(array_to_string(proconfig, ','), '') from pg_proc where oid = '{fn}'::regprocedure", SUPER_DSN)[1]
           for fn in functions}
    try:
        for fn in functions:
            psql(f"alter function {fn} set plan_cache_mode = force_generic_plan" + (f"; alter function {fn} reset enable_seqscan" if allow_scans else ""), SUPER_DSN)
        yield
    finally:
        for fn in functions:
            psql(f"alter function {fn} reset plan_cache_mode" + (f"; alter function {fn} set enable_seqscan = off" if allow_scans and had[fn] else ""), SUPER_DSN)


def load(**extra):
    """Step C of the second-person data (both people, both personal spaces, the friend's own company), plus anything extra."""
    fx = fixture("C")
    for key, rows in extra.items():
        fx[key] = fx[key] + rows
    admin("/admin/reset", fx)
    return fx


class Base(unittest.TestCase):
    def setUp(self):
        load()


class GlobalPagesNeedAPerson(Base):
    """REV-01 RV-02. An agent's global page is not readable below until a person who controls the organization releases it."""

    def test_an_agents_global_page_waits_for_a_person_who_controls_the_organization(self):
        ok, w, raw = call(TOK("mgmt"), "brain_write", {"title": "for every venture", "body": "CANARY-NEWGLOBAL-1", "visibility": "global"})
        self.assertEqual((ok, w.get("status")), (True, "pending_approval"), raw)
        self.assertEqual(who_sees("CANARY-NEWGLOBAL-1", ["mgmt", "personal", "toveli", "sibling", "shared", "friend-personal", "acme", "acme-sub"]), ["mgmt", "personal"])
        ok, got, _ = call(TOK("mgmt"), "brain_get", {"id": w["id"]})
        self.assertEqual(got["page"]["status"], "pending_approval")
        # Nobody but a person who controls the organization can release it, and anyone else learns nothing from trying.
        for token, expected in [(TOK("mgmt"), FORBIDDEN), (TOK("personal"), FORBIDDEN), (TOK("toveli"), FORBIDDEN),
                                (FRIEND_IN_SHARED, NOT_FOUND), (FRIEND, NOT_FOUND)]:
            ok, payload, _ = call(token, "approve_page", {"page_id": w["id"]})
            self.assertEqual((ok, payload), (False, expected))
        for approver, status in [("", 400), ("friend", 404), ("nobody", 404), ("mgmt", 404)]:
            code, _ = http_call("POST", "/admin/approve_page", ADMIN, {"page_id": w["id"], "approver": approver})
            self.assertEqual(code, status, approver)
        self.assertEqual(who_sees("CANARY-NEWGLOBAL-1", ["toveli", "sibling", "shared"]), [])
        # The person sees the whole text before deciding. The other person is shown nothing.
        ok, mine, _ = call(COLE, "pending_approvals")
        self.assertEqual([(p["page_id"], p["org"], p["body"]) for p in mine["pages"]], [(w["id"], "mgmt", "CANARY-NEWGLOBAL-1")])
        ok, theirs, _ = call(FRIEND, "pending_approvals")
        self.assertEqual(theirs, {"pushes": [], "pages": []})
        ok, done, raw = call(COLE, "approve_page", {"page_id": w["id"]})
        self.assertEqual((ok, done["status"]), (True, "approved"), raw)
        self.assertEqual(who_sees("CANARY-NEWGLOBAL-1", ["toveli", "sibling", "shared", "friend-personal", "acme", "acme-sub"]),
                         ["toveli", "sibling", "shared", "friend-personal"], "released to this holding organization's ventures, and to nobody outside it")
        ok, again, _ = call(COLE, "approve_page", {"page_id": w["id"]})
        self.assertEqual(again, NOT_FOUND, "a page is released once")

    def test_a_rejected_global_page_stays_an_ordinary_page_of_its_organization(self):
        ok, w, _ = call(TOK("mgmt"), "brain_write", {"title": "for every venture", "body": "CANARY-NEWGLOBAL-2", "visibility": "global"})
        ok, done, raw = call(COLE, "approve_page", {"page_id": w["id"], "decision": "reject"})
        self.assertEqual((ok, done["status"]), (True, "rejected"), raw)
        self.assertEqual(who_sees("CANARY-NEWGLOBAL-2", ["mgmt", "toveli", "sibling", "shared"]), ["mgmt"])
        ok, got, _ = call(TOK("mgmt"), "brain_get", {"id": w["id"]})
        self.assertEqual((got["page"]["visibility"], got["page"].get("status")), ("org", None))
        self.assertEqual(call(COLE, "pending_approvals")[1]["pages"], [])
        self.assertEqual(call(COLE, "approve_page", {"page_id": w["id"]})[1], NOT_FOUND, "a rejected page cannot be released later")

    def test_only_a_person_who_controls_the_organization_publishes_at_once(self):
        """Cole, as a person in the holding organization, publishes directly. An employee who is a member but not an owner does not."""
        load(orgs=[{"id": "employee-personal", "kind": "personal", "parent": None}],
             people=[{"id": "employee", "personal_org": "employee-personal"}], memberships=[{"person": "employee", "org": "mgmt", "role": "member"}],
             principals=[{"org": "mgmt", "actor": "human", "token": "fix-mgmt-cole", "person": "cole"},
                         {"org": "mgmt", "actor": "human", "token": "fix-mgmt-employee", "person": "employee"},
                         {"org": "employee-personal", "actor": "agent", "token": "fix-employee-personal-agent"}])
        # Being a member of the holding organization opens that organization to the employee's personal space, and none of the ventures below it.
        self.assertEqual(markers("fix-employee-personal-agent"), {"MGMT", "GLOBAL"})
        ok, w, raw = call("fix-mgmt-cole", "brain_write", {"title": "from the owner", "body": "CANARY-NEWGLOBAL-3", "visibility": "global"})
        self.assertEqual((ok, w.get("status")), (True, None), raw)
        self.assertTrue(sees(TOK("toveli"), "CANARY-NEWGLOBAL-3"))
        ok, w, raw = call("fix-mgmt-employee", "brain_write", {"title": "from an employee", "body": "CANARY-NEWGLOBAL-4", "visibility": "global"})
        self.assertEqual((ok, w.get("status")), (True, "pending_approval"), raw)
        self.assertFalse(sees(TOK("toveli"), "CANARY-NEWGLOBAL-4"))
        self.assertEqual(call("fix-mgmt-employee", "approve_page", {"page_id": w["id"]})[1], NOT_FOUND, "a member who is not an owner cannot release a page")
        self.assertEqual(call("fix-mgmt-employee", "brain_whoami")[1]["person"], "employee")


class Pushes(Base):
    """REV-01 RV-15 and Cole's rule of 2026-11-17: nothing leaves a personal space unless its person supplies it, and says so as a person."""

    def test_a_push_shows_its_text_to_the_person_who_decides_and_to_nobody_else(self):
        ok, b, raw = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-1 what I need the holding company to do this week"})
        self.assertEqual((ok, b.get("status"), b.get("to")), (True, "pending", "mgmt"), raw)
        self.assertEqual(who_sees("CANARY-PUSH-1", ["mgmt", "toveli", "sibling", "shared", "personal", "friend-personal", "acme"]), [])
        ok, mine, _ = call(COLE, "pending_approvals")
        self.assertEqual([(p["push_id"], p["from"], p["to"], p["content"]) for p in mine["pushes"]],
                         [(b["briefing_id"], "personal", "mgmt", "CANARY-PUSH-1 what I need the holding company to do this week")])
        for token in [FRIEND, FRIEND_IN_SHARED]:
            self.assertEqual(call(token, "pending_approvals")[1], {"pushes": [], "pages": []})
        for token in [TOK("personal"), TOK("mgmt"), TOK("toveli")]:                       # an agent is never shown the queue
            self.assertEqual(call(token, "pending_approvals")[1], FORBIDDEN)
        # An agent cannot approve, not even the agent of the same personal space. Another person cannot either.
        for token, expected in [(TOK("personal"), FORBIDDEN), (TOK("mgmt"), FORBIDDEN), (FRIEND, NOT_FOUND), (FRIEND_IN_SHARED, NOT_FOUND)]:
            ok, payload, _ = call(token, "approve_push", {"push_id": b["briefing_id"]})
            self.assertEqual((ok, payload), (False, expected))
        for approver, status in [("", 400), ("friend", 404), ("nobody", 404)]:
            code, _ = http_call("POST", "/admin/approve_briefing", ADMIN, {"briefing_id": b["briefing_id"], "approver": approver})
            self.assertEqual(code, status, approver)
        self.assertFalse(sees(TOK("mgmt"), "CANARY-PUSH-1"))
        ok, done, raw = call(COLE, "approve_push", {"push_id": b["briefing_id"]})
        self.assertEqual((ok, done["status"]), (True, "approved"), raw)
        self.assertEqual(who_sees("CANARY-PUSH-1", ["mgmt", "toveli", "sibling", "shared", "friend-personal", "acme"]), ["mgmt"])
        ok, got, _ = call(TOK("mgmt"), "brain_get", {"id": done["page_id"]})
        self.assertEqual((got["page"]["kind"], got["page"]["pushed_from"], got["page"]["written_by"]), ("briefing", "personal", "cole"))
        self.assertEqual(call(COLE, "approve_push", {"push_id": b["briefing_id"]})[1], NOT_FOUND, "a push is decided once")

    def test_a_push_can_go_straight_to_one_venture(self):
        """Cole, 2026-11-17: "chief of staff, share my calendar for today with venture y so they can book a meeting"."""
        ok, b, raw = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-2 free on Thursday after 14:00", "to": "toveli"})
        self.assertEqual((ok, b.get("to")), (True, "toveli"), raw)
        call(COLE, "approve_push", {"push_id": b["briefing_id"]})
        # The venture reads it. So does the holding organization, because it reads that venture in full. Nobody else.
        self.assertEqual(who_sees("CANARY-PUSH-2", ["toveli", "mgmt", "sibling", "shared", "acme", "friend-personal"]), ["toveli", "mgmt"])

    def test_a_push_cannot_go_where_its_person_does_not_belong(self):
        for to in ["acme", "acme-sub", "friend-personal", "personal", "no-such-organization"]:
            ok, payload, _ = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-3", "to": to})
            self.assertEqual((ok, payload), (False, FORBIDDEN), to)
        ok, payload, _ = call(TOK("friend-personal"), "publish_briefing", {"content": "CANARY-PUSH-3", "to": "mgmt"})
        self.assertEqual((ok, payload), (False, FORBIDDEN), "the friend belongs to the shared venture, not to the holding organization above it")
        self.assertEqual(call(COLE, "pending_approvals")[1]["pushes"], [])
        self.assertEqual(call(FRIEND, "pending_approvals")[1]["pushes"], [])

    def test_a_rejected_push_is_never_delivered(self):
        ok, b, _ = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-4"})
        ok, done, raw = call(COLE, "approve_push", {"push_id": b["briefing_id"], "decision": "reject"})
        self.assertEqual((ok, done["status"], done["page_id"]), (True, "rejected", None), raw)
        self.assertEqual(call(COLE, "approve_push", {"push_id": b["briefing_id"]})[1], NOT_FOUND)
        code, _ = http_call("POST", "/admin/approve_briefing", ADMIN, {"briefing_id": b["briefing_id"], "approver": "cole"})
        self.assertEqual(code, 404)
        self.assertFalse(sees(TOK("mgmt"), "CANARY-PUSH-4"))

    def test_each_person_decides_their_own_pushes_and_they_go_to_their_own_company(self):
        ok, mine, _ = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-5 from Cole"})
        ok, theirs, _ = call(TOK("friend-personal"), "publish_briefing", {"content": "CANARY-PUSH-6 from the friend"})
        self.assertEqual((mine["to"], theirs["to"]), ("mgmt", "acme"))
        self.assertEqual([p["content"] for p in call(COLE, "pending_approvals")[1]["pushes"]], ["CANARY-PUSH-5 from Cole"])
        self.assertEqual([p["content"] for p in call(FRIEND, "pending_approvals")[1]["pushes"]], ["CANARY-PUSH-6 from the friend"])
        self.assertEqual(call(COLE, "approve_push", {"push_id": theirs["briefing_id"]})[1], NOT_FOUND)
        self.assertEqual(call(FRIEND, "approve_push", {"push_id": mine["briefing_id"]})[1], NOT_FOUND)
        call(COLE, "approve_push", {"push_id": mine["briefing_id"]})
        call(FRIEND, "approve_push", {"push_id": theirs["briefing_id"]})
        self.assertEqual(who_sees("CANARY-PUSH-5", ["mgmt", "acme", "shared"]), ["mgmt"])
        self.assertEqual(who_sees("CANARY-PUSH-6", ["mgmt", "acme", "shared"]), ["acme"])

    def test_with_two_companies_of_their_own_a_person_must_say_where_a_push_goes(self):
        load(orgs=[{"id": "labs", "kind": "holding", "parent": None}], memberships=[{"person": "cole", "org": "labs", "role": "owner"}],
             principals=[{"org": "labs", "actor": "agent", "token": "fix-labs-agent"}])
        ok, payload, _ = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-7"})
        self.assertEqual((ok, payload), (False, {"error": "invalid_arguments"}), "with two top-level organizations there is no default, and the service must not pick one")
        ok, b, raw = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-7", "to": "labs"})
        self.assertEqual((ok, b.get("to")), (True, "labs"), raw)
        call(COLE, "approve_push", {"push_id": b["briefing_id"]})
        self.assertEqual([o for o, t in [("labs", "fix-labs-agent"), ("mgmt", TOK("mgmt"))] if sees(t, "CANARY-PUSH-7")], ["labs"])

    @unittest.skipUnless(APP_DSN, "BRAIN_APP_DSN not set: NOT RUN")
    def test_the_database_login_cannot_decide_a_push_or_a_page_through_any_function(self):
        """A real pending push and a real pending global page, and every function that could decide them, called as the service's own
        login with and without a bound session. (The first run of the mutation sweep showed that nothing tested this with a real push.)"""
        ok, b, _ = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-15"})
        ok, w, _ = call(TOK("mgmt"), "brain_write", {"title": "g", "body": "CANARY-NEWGLOBAL-5", "visibility": "global"})
        push, page = b["briefing_id"], w["id"]
        internal = [f"select brain.operator_decide_push('{push}', 'cole', 'approve')", f"select brain.decide_push_('{push}', 'cole', 'approve', 'operator')",
                    f"select brain.decide_push_('{push}', 'cole', 'approve', 'human_token')", f"select brain.operator_decide_page('{page}', 'cole', 'approve')",
                    f"select brain.decide_page_('{page}', 'cole', 'approve')"]
        granted = [f"select brain.t_decide_push(null, null, '{push}', 'approve')", f"select brain.t_decide_page(null, null, '{page}', 'approve')"]
        for bind in ["", f"select brain.begin_session('{TOK('personal')}'); ", f"select brain.begin_session('{TOK('mgmt')}'); "]:
            for sql in internal + granted:
                code, out = psql("begin; " + bind + sql + "; commit;")
                self.assertNotEqual(code, 0, f"{sql!r} ran for the database login ({bind[:40] or 'no session'}): {out[:200]}")
        self.assertFalse(sees(TOK("mgmt"), "CANARY-PUSH-15") or sees(TOK("toveli"), "CANARY-NEWGLOBAL-5"))
        waiting = call(COLE, "pending_approvals")[1]
        self.assertEqual(([p["push_id"] for p in waiting["pushes"]], [p["page_id"] for p in waiting["pages"]]), ([push], [page]))

    @unittest.skipUnless(SUPER_DSN, "SUPER_DSN not set: NOT RUN")
    def test_the_text_and_the_route_of_a_push_cannot_be_changed_once_written(self):
        """Even the role that owns the tables cannot swap the text of a push between the moment a person reads it and the moment they approve."""
        ok, b, _ = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-8"})
        pid = b["briefing_id"]
        for sql in [f"update brain.pushes set content = 'something else' where id = '{pid}'", f"update brain.pushes set to_org = 'toveli' where id = '{pid}'",
                    f"update brain.pushes set from_org = 'friend-personal' where id = '{pid}'", f"delete from brain.pushes where id = '{pid}'"]:
            code, out = psql("set role brain_owner; " + sql, SUPER_DSN)
            self.assertNotEqual(code, 0, f"{sql!r} was accepted: {out[:200]}")
        call(COLE, "approve_push", {"push_id": pid})
        code, out = psql(f"set role brain_owner; update brain.pushes set status = 'pending', decided_by = null, decided_at = null, page_id = null where id = '{pid}'", SUPER_DSN)
        self.assertNotEqual(code, 0, "a decided push was reopened")
        self.assertTrue(sees(TOK("mgmt"), "CANARY-PUSH-8"))


class ReportsUpward(Base):
    """V-000 section 6: nothing leaves a venture shared with a second person except by an approved push."""

    def test_a_shared_venture_reports_upward_only_by_a_push_one_of_its_owners_approves(self):
        self.assertNotIn("SHARED", markers(TOK("mgmt")))
        ok, p, raw = call(TOK("shared"), "push_to_parent", {"content": "CANARY-REPORT-1 revenue this month, as the two of us agreed to report it"})
        self.assertEqual((ok, p.get("status"), p.get("to")), (True, "pending", "mgmt"), raw)
        self.assertFalse(sees(TOK("mgmt"), "CANARY-REPORT-1"))
        for token, expected in [(TOK("mgmt"), FORBIDDEN), (TOK("shared"), FORBIDDEN), (TOK("toveli"), FORBIDDEN)]:
            self.assertEqual(call(token, "approve_push", {"push_id": p["push_id"]})[1], expected)
        # Either owner sees it waiting, with the text. The friend approves, as a person, from inside the venture.
        for token in [COLE, FRIEND, FRIEND_IN_SHARED]:
            self.assertEqual([x["content"][:15] for x in call(token, "pending_approvals")[1]["pushes"]], ["CANARY-REPORT-1"])
        ok, done, raw = call(FRIEND_IN_SHARED, "approve_push", {"push_id": p["push_id"]})
        self.assertEqual((ok, done["status"]), (True, "approved"), raw)
        self.assertEqual(who_sees("CANARY-REPORT-1", ["mgmt", "toveli", "sibling", "acme", "friend-personal"]), ["mgmt"])
        ok, got, _ = call(TOK("mgmt"), "brain_get", {"id": done["page_id"]})
        self.assertEqual((got["page"]["kind"], got["page"]["pushed_from"], got["page"]["written_by"]), ("report", "shared", "friend"))
        # The holding organization still reads nothing else of the venture, and the friend gained nothing above it.
        self.assertNotIn("SHARED", markers(TOK("mgmt")))
        self.assertEqual(markers(FRIEND_IN_SHARED), {"SHARED", "GLOBAL"})
        # A report is not personal text: the briefing switch does not hide it.
        admin("/admin/settings", {"briefing_enabled": False})
        self.assertTrue(sees(TOK("mgmt"), "CANARY-REPORT-1"))

    def test_only_a_sub_organization_reports_upward(self):
        for token in [TOK("mgmt"), TOK("personal"), TOK("acme"), TOK("friend-personal")]:
            ok, payload, _ = call(token, "push_to_parent", {"content": "CANARY-REPORT-2"})
            self.assertEqual((ok, payload), (False, FORBIDDEN))
        ok, p, _ = call(TOK("toveli"), "push_to_parent", {"content": "CANARY-REPORT-3"})          # Cole's own venture: Cole decides
        self.assertEqual(call(FRIEND, "approve_push", {"push_id": p["push_id"]})[1], NOT_FOUND)
        self.assertEqual(call(COLE, "approve_push", {"push_id": p["push_id"]})[1]["status"], "approved")


class Switches(Base):
    """REV-01 RV-03: what the layer above reads is set per venture, and each person has their own two switches."""

    def test_what_the_layer_above_reads_is_set_per_venture(self):
        reads = lambda: {m for m in ["CANARY-TOVELI-1", "CANARY-SIBLING-1", "CANARY-SHARED-1", "CANARY-SHARED-2"] if sees(TOK("mgmt"), m)}
        self.assertEqual(reads(), {"CANARY-TOVELI-1", "CANARY-SIBLING-1"}, "by default the holding organization reads nothing of a venture that has a second person")
        out = admin("/admin/settings", {"org": "toveli", "holding_reads": "none"})
        self.assertEqual(out["organizations"]["toveli"], {"parent_reads": "none", "effective": "none"})
        self.assertEqual(reads(), {"CANARY-SIBLING-1"})
        self.assertTrue(sees(TOK("personal"), "CANARY-TOVELI-1"), "the person still reads their own venture from their personal space")
        admin("/admin/settings", {"org": "toveli", "holding_reads": "default"})
        admin("/admin/settings", {"org": "shared", "holding_reads": "summaries"})
        self.assertEqual(reads(), {"CANARY-TOVELI-1", "CANARY-SIBLING-1", "CANARY-SHARED-2"})
        admin("/admin/settings", {"holding_reads": {"shared": "all"}})
        self.assertEqual(reads(), {"CANARY-TOVELI-1", "CANARY-SIBLING-1", "CANARY-SHARED-1", "CANARY-SHARED-2"})
        admin("/admin/settings", {"org": "shared", "parent_reads": "default"})
        admin("/admin/settings", {"holding_reads": "summaries"})                      # the deployment's default moves the ordinary ventures only
        self.assertEqual(reads(), set())
        self.assertEqual(markers(TOK("mgmt")) & {"TOVELI", "SIBLING", "SHARED"}, set())

    def test_a_venture_with_its_own_member_list_is_closed_to_the_owner_above_unless_they_are_on_it(self):
        """A venture under Cole's holding organization that the friend runs alone. Owning the organization above does not open it."""
        load(orgs=[{"id": "partnerco", "kind": "sub", "parent": "mgmt"}], memberships=[{"person": "friend", "org": "partnerco", "role": "owner"}],
             principals=[{"org": "partnerco", "actor": "agent", "token": "fix-partnerco-agent"}],
             pages=[{"org": "partnerco", "title": "Partner notes", "body": "CANARY-PARTNERCO-1", "kind": "note", "source_type": "human"}])
        self.assertTrue(sees("fix-partnerco-agent", "CANARY-PARTNERCO-1") and sees(TOK("friend-personal"), "CANARY-PARTNERCO-1"))
        self.assertEqual(who_sees("CANARY-PARTNERCO-1", ["personal", "mgmt", "toveli", "shared"]), [])
        self.assertEqual(call(TOK("personal"), "publish_briefing", {"content": "x", "to": "partnerco"})[1], FORBIDDEN)
        ok, p, _ = call("fix-partnerco-agent", "push_to_parent", {"content": "CANARY-REPORT-4"})
        self.assertEqual(call(COLE, "approve_push", {"push_id": p["push_id"]})[1], NOT_FOUND, "Cole owns the organization above but is not on this venture's list")
        self.assertEqual(call(FRIEND, "approve_push", {"push_id": p["push_id"]})[1]["status"], "approved")
        self.assertTrue(sees(TOK("mgmt"), "CANARY-REPORT-4"))

    def test_a_setting_the_service_does_not_understand_is_refused_and_changes_nothing(self):
        before = admin("/admin/settings", {})
        for body in [{"holding_reads": "none"}, {"holding_reads": "everything"}, {"holding_reads_shared": "none"}, {"org": "mgmt", "holding_reads": "none"},
                     {"org": "shared", "holding_reads": "everything"}, {"org": "no-such-organization", "holding_reads": "none"}, {"personal_enabled": "no"},
                     {"org": "toveli", "personal_enabled": False}, {"briefing_enabled": 0}, {"holding_reads": {"shared": "none", "mgmt": "none"}}, {"push_enabled": False}]:
            code, raw = http_call("POST", "/admin/settings", ADMIN, body)
            self.assertEqual(code, 400, f"{body}: {raw[:120]}")
        self.assertEqual(admin("/admin/settings", {}), before, "a refused request must leave every setting as it was, including the valid half of a mixed one")

    def test_each_person_has_their_own_two_switches(self):
        ok, theirs, _ = call(TOK("friend-personal"), "publish_briefing", {"content": "CANARY-PUSH-9 from the friend"})
        call(FRIEND, "approve_push", {"push_id": theirs["briefing_id"]})
        ok, mine, _ = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-10 from Cole"})
        call(COLE, "approve_push", {"push_id": mine["briefing_id"]})
        self.assertTrue(sees(TOK("acme"), "CANARY-PUSH-9") and sees(TOK("mgmt"), "CANARY-PUSH-10"))
        # The friend's briefing switch: the friend's earlier briefings are hidden and no new one can be offered. Cole's are untouched.
        out = admin("/admin/settings", {"org": "friend-personal", "briefing_enabled": False})
        self.assertEqual((out["people"]["friend"]["briefing_enabled"], out["people"]["cole"]["briefing_enabled"]), (False, True))
        self.assertFalse(sees(TOK("acme"), "CANARY-PUSH-9"))
        self.assertTrue(sees(TOK("mgmt"), "CANARY-PUSH-10"))
        self.assertEqual(call(TOK("friend-personal"), "publish_briefing", {"content": "x"})[1], {"error": "disabled"})
        self.assertTrue(call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-11"})[0])
        admin("/admin/settings", {"org": "friend-personal", "briefing_enabled": True})
        self.assertTrue(sees(TOK("acme"), "CANARY-PUSH-9"))
        # The friend's personal space: both of its tokens stop, a push it left pending cannot be approved, and nothing else changes.
        ok, left, _ = call(TOK("friend-personal"), "publish_briefing", {"content": "CANARY-PUSH-12 left pending"})
        admin("/admin/settings", {"org": "friend-personal", "personal_enabled": False})
        for token in [TOK("friend-personal"), FRIEND]:
            self.assertEqual(rpc(token, "brain_whoami", {})[0], 401)
        code, _ = http_call("POST", "/admin/approve_briefing", ADMIN, {"briefing_id": left["briefing_id"], "approver": "friend"})
        self.assertEqual(code, 409)
        self.assertFalse(sees(TOK("acme"), "CANARY-PUSH-12"))
        for token in [TOK("personal"), COLE, FRIEND_IN_SHARED, TOK("acme")]:
            self.assertEqual(rpc(token, "brain_whoami", {})[0], 200)

    def test_a_token_that_stands_for_a_person_works_only_where_that_person_belongs(self):
        load(principals=[{"org": "toveli", "actor": "human", "token": "fix-toveli-friend", "person": "friend"},
                         {"org": "toveli", "actor": "human", "token": "fix-toveli-cole", "person": "cole"},
                         {"org": "personal", "actor": "human", "token": "fix-personal-friend", "person": "friend"}])
        self.assertEqual(rpc("fix-toveli-friend", "brain_whoami", {})[0], 401, "the friend does not belong to Cole's other venture")
        self.assertEqual(rpc("fix-personal-friend", "brain_whoami", {})[0], 401, "nobody but its own person can hold a token for a personal space")
        self.assertEqual(rpc("fix-toveli-cole", "brain_whoami", {})[0], 200)

    def test_a_personal_space_with_nobody_behind_it_is_refused_when_data_is_loaded(self):
        fx = fixture("C")
        fx["people"] = [p for p in fx["people"] if p["id"] != "friend"]
        fx["memberships"] = [m for m in fx["memberships"] if m["person"] != "friend"]
        fx["principals"] = [dict(p, person=None) for p in fx["principals"]]
        code, raw = http_call("POST", "/admin/reset", ADMIN, fx)
        self.assertEqual(code, 400, raw[:200])
        self.assertEqual(rpc(TOK("personal"), "brain_whoami", {})[0], 200, "a refused load must leave the data that was there")


class PathLookup(Base):
    """REV-01 RV-18. `org` narrows a lookup to an organization the caller may already read. It never widens it."""

    def test_org_narrows_and_never_widens(self):
        admin("/admin/codebase_sync", {"org": "shared", "upserts": [{"path": "apps/api/main.ts", "title": "Code: apps/api/main.ts", "body": "CANARY-SHARED-CODE", "content_sha": "x"}]})
        ok, got, _ = call(TOK("personal"), "brain_get", {"path": "apps/api/main.ts"})
        self.assertEqual((got["page"]["org"], got["other_orgs"]), ("shared", ["toveli"]), "without `org` the reader is told that another organization holds the same path")
        ok, got, _ = call(TOK("personal"), "brain_get", {"path": "apps/api/main.ts", "org": "toveli"})
        self.assertEqual((got["page"]["org"], "other_orgs" in got), ("toveli", False))
        for token, args in [(FRIEND_IN_SHARED, {"path": "apps/api/main.ts", "org": "toveli"}), (TOK("sibling"), {"path": "apps/api/main.ts", "org": "toveli"}),
                            (TOK("sibling"), {"path": "apps/api/main.ts", "org": "shared"}), (TOK("mgmt"), {"path": "apps/api/main.ts", "org": "shared"}),
                            (TOK("acme"), {"path": "apps/api/main.ts", "org": "toveli"}), (TOK("toveli"), {"path": "apps/api/main.ts", "org": "no-such-organization"})]:
            self.assertEqual(call(token, "brain_get", args)[1], NOT_FOUND, args)
        ok, got, _ = call(FRIEND_IN_SHARED, "brain_get", {"path": "apps/api/main.ts"})
        self.assertEqual((got["page"]["org"], "other_orgs" in got), ("shared", False), "the friend is not told that Cole's other venture has the same path")


class TheLog(Base):
    """REV-01 RV-07, RV-08 and RV-19, and Cole's requirement of 2026-11-17: every action by an agent or a person is in one append-only log."""

    def test_every_message_leaves_exactly_one_row(self):
        before = last_audit_id()
        tool = lambda name, args: {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": args}}
        batch = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}, {"jsonrpc": "2.0", "method": "notifications/initialized"},
                 {"jsonrpc": "2.0", "id": 2, "method": "ping"}, {"jsonrpc": "2.0", "id": 3, "method": "tools/list"},
                 {"jsonrpc": "2.0", "id": 4, "method": "resources/list"}, None, 7, {"jsonrpc": "2.0", "id": 5},
                 tool("brain_whoami", {}), tool("brain_get", {"path": "no/such/file"}), tool("no_such_tool", {}), tool("brain_list", {"request_id": 5}),
                 tool("brain_list", {"request_id": "x" * 101}), tool("brain_search", {"query": ""})]
        status, raw = http_call("POST", "/mcp", TOK("toveli"), batch)
        self.assertEqual(status, 200, raw[:200])
        rows = audit_rows(before)
        self.assertEqual([(r["tool"], r["decision"], r["reason"]) for r in rows],
                         [("mcp:initialize", "allow", None), ("mcp:notification", "allow", None), ("mcp:ping", "allow", None), ("mcp:tools/list", "allow", None),
                          ("mcp:unknown_method", "deny", "unknown_method"), ("mcp:unknown_method", "deny", "unknown_method"),
                          ("mcp:unknown_method", "deny", "unknown_method"), ("mcp:unknown_method", "deny", "unknown_method"),
                          ("brain_whoami", "allow", None), ("brain_get", "deny", "not_found"), ("no_such_tool", "deny", "unknown_tool"),
                          ("brain_list", "deny", "invalid_request_id"), ("brain_list", "deny", "invalid_request_id"), ("brain_search", "deny", "invalid_arguments")])
        self.assertEqual({(r["org"], r["actor"], r["via"]) for r in rows}, {("toveli", "agent", "mcp")})
        # A body that is not JSON, and a token that is refused, are rows as well.
        before = last_audit_id()
        status, _ = raw_request("POST", "/mcp", [("Authorization", "Bearer " + TOK("toveli")), ("Content-Type", "application/json")], b"{not json")
        self.assertEqual(status, 400)
        status, _ = http_call("POST", "/mcp", "wrong-token", tool("brain_list", {}))
        self.assertEqual(status, 401)
        self.assertEqual([(r["org"], r["tool"], r["decision"], r["reason"]) for r in audit_rows(before)],
                         [("toveli", "mcp:invalid_json", "deny", "invalid_json"), (None, "auth", "deny", "invalid_token")])

    def test_an_allowed_read_records_which_pages_it_returned_and_never_their_text(self):
        before = last_audit_id()
        ok, found, _ = call(TOK("toveli"), "brain_search", {"query": "CANARY"})
        ok, got, _ = call(TOK("toveli"), "brain_get", {"path": "apps/api/main.ts"})
        ok, w, _ = call(TOK("toveli"), "brain_write", {"title": "t", "body": "CANARY-TOVELI-LOGGED"})
        rows = audit_rows(before)
        self.assertEqual([(r["tool"], r["result_count"], sorted(r["page_ids"])) for r in rows],
                         [("brain_search", found["count"], sorted(p["id"] for p in found["pages"])), ("brain_get", 1, [got["page"]["id"]]), ("brain_write", 1, [w["id"]])])
        self.assertEqual(rows[1]["target"], "apps/api/main.ts")
        self.assertNotIn("CANARY", json.dumps(rows), "the log holds which pages, never what they say")
        # So "who was handed this page" is one question to the log.
        asked = admin(f"/admin/audit?since_id={before}&page_id={got['page']['id']}", method="GET")["rows"]
        self.assertEqual([(r["org"], r["tool"]) for r in asked], [("toveli", "brain_search"), ("toveli", "brain_get")])

    def test_what_the_operator_does_is_in_the_same_log(self):
        ok, b, _ = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-13"})
        before = last_audit_id()
        admin("/admin/settings", {"org": "shared", "holding_reads": "summaries"})
        admin("/admin/pushes?status=pending", method="GET")
        page = admin("/admin/approve_briefing", {"briefing_id": b["briefing_id"], "approver": "cole"})["page_id"]
        admin("/admin/codebase_sync", {"org": "toveli", "upserts": [{"path": "a.py", "title": "Code: a.py", "body": "x", "content_sha": "1"}]})
        admin("/admin/pages_digest?org=toveli", method="GET")
        http_call("POST", "/admin/approve_briefing", ADMIN, {"briefing_id": b["briefing_id"], "approver": "cole"})        # already decided: refused
        http_call("POST", "/admin/settings", ADMIN, {"holding_reads": "none"})                                           # refused
        http_call("POST", "/admin/settings", ADMIN + "x", {"personal_enabled": False})                                   # wrong token
        rows = audit_rows(before)
        self.assertEqual([(r["tool"], r["decision"], r["reason"]) for r in rows],
                         [("admin:settings", "allow", None), ("admin:pushes", "allow", None), ("admin:approve_briefing", "allow", None),
                          ("admin:codebase_sync", "allow", None), ("admin:pages_digest", "allow", None), ("admin:approve_briefing", "deny", "not_found"),
                          ("admin:settings", "deny", "invalid_setting"), ("admin:auth", "deny", "invalid_token")])
        self.assertEqual({(r["actor"], r["via"]) for r in rows}, {("operator", "admin")})
        self.assertEqual(rows[0]["detail"], {"parent_reads:shared": "summaries"})
        self.assertEqual((rows[2]["person"], rows[2]["target"], rows[2]["page_ids"], rows[2]["detail"]),
                         ("cole", b["briefing_id"], [page], {"decision": "approve", "on_behalf_of": "cole"}))
        self.assertNotIn("CANARY", json.dumps(rows))
        # A person's own decision, made with their own token, reads differently from the operator recording it for them.
        ok, b2, _ = call(TOK("personal"), "publish_briefing", {"content": "CANARY-PUSH-14"})
        before = last_audit_id()
        call(COLE, "approve_push", {"push_id": b2["briefing_id"]})
        row = audit_rows(before)[-1]
        self.assertEqual((row["tool"], row["actor"], row["person"], row["via"], row["target"]), ("approve_push", "human", "cole", "mcp", b2["briefing_id"]))

    @unittest.skipUnless(APP_DSN, "BRAIN_APP_DSN not set: NOT RUN")
    def test_the_database_login_cannot_read_without_leaving_a_row(self):
        """The function that returns the pages writes the row, in the same transaction. There is no other way to the pages."""
        before = last_audit_id()
        code, out = psql(f"begin; select brain.begin_session('{TOK('toveli')}'); select brain.t_search('fix-direct', null, 'CANARY', null, 10); commit;")
        self.assertIn("CANARY-TOVELI-1", out)
        self.assertEqual([(r["org"], r["tool"], r["decision"], r["request_id"]) for r in audit_rows(before)], [("toveli", "brain_search", "allow", "fix-direct")])

    @unittest.skipUnless(SUPER_DSN, "SUPER_DSN not set: NOT RUN")
    def test_the_log_refuses_change_and_a_change_forced_past_the_triggers_is_detected(self):
        call(TOK("toveli"), "brain_whoami")
        call(TOK("toveli"), "brain_get", {"path": "no/such/file"})
        call(TOK("toveli"), "brain_whoami")
        target = last_audit_id() - 1                                                    # the refused brain_get
        for sql in [f"update brain.audit set decision = 'allow' where id = {target}", f"delete from brain.audit where id = {target}", "truncate brain.audit"]:
            code, out = psql("set role brain_owner; " + sql, SUPER_DSN)
            self.assertNotEqual(code, 0, f"the owner of the table ran {sql!r}")
            self.assertIn("append-only", out)
        self.assertEqual(admin("/admin/audit_verify", method="GET")["first_bad_id"], None)
        saved = psql(f"select row_to_json(a) from brain.audit a where id = {target}", SUPER_DSN)[1]
        try:
            # A superuser switches the triggers off and rewrites a refusal as an allowed call. The chain names the row.
            psql(f"alter table brain.audit disable trigger user; update brain.audit set decision = 'allow' where id = {target}", SUPER_DSN)
            self.assertEqual(admin("/admin/audit_verify", method="GET")["first_bad_id"], target)
            # The same superuser removes the row instead. The chain names the row after the gap.
            psql(f"delete from brain.audit where id = {target}", SUPER_DSN)
            self.assertEqual(admin("/admin/audit_verify", method="GET")["first_bad_id"], target + 1)
        finally:
            psql(f"delete from brain.audit where id = {target}; insert into brain.audit select * from json_populate_record(null::brain.audit, $j${saved}$j$); "
                 "alter table brain.audit enable trigger user", SUPER_DSN)
        self.assertEqual(admin("/admin/audit_verify", method="GET")["first_bad_id"], None, "the test must leave the log as it found it")


class OtherOrganizationsPagesCostNothing(Base):
    """Two risks the fix itself could have introduced, and what closes each in schema.sql: the "offset 0" fence, and sequential scans
    switched off in the read functions. The mutation sweep removes each in turn and these tests are what notice."""

    def test_list_and_search_time_do_not_grow_with_other_organizations_pages_even_before_statistics_catch_up(self):
        """REV-01 RV-05, harder than the review's own test: 20,000 pages instead of 1,500, measured at once, before PostgreSQL has had
        the minute it needs to notice that the table grew. Against R-02 the review measured 4.9 ms growing to 2,853 ms at 10,000 pages.
        Measured twice: as deployed, and with the unfavourable kind of plan forced (needs SUPER_DSN), which is the only kind under
        which a missing scan setting shows. The mutation sweep's third run showed that the first measurement alone can miss it."""
        def median_ms(tool, args, n=9):
            ts = []
            for _ in range(n):
                t0 = time.perf_counter()
                ok, payload, _ = call(TOK("toveli"), tool, args)
                ts.append((time.perf_counter() - t0) * 1000)
                assert ok and payload["count"] in (1, 3), payload
            return statistics.median(ts)
        both = lambda: (median_ms("brain_list", {}), median_ms("brain_search", {"query": "launch checklist"}))
        before = both()
        for batch in range(4):
            ups = [{"path": f"gen/{batch}-{i:05d}.py", "title": f"Code: gen/{batch}-{i:05d}.py", "body": f"made-up page {i}", "content_sha": str(i)} for i in range(5000)]
            admin("/admin/codebase_sync", {"org": "sibling", "upserts": ups})
        after = both()
        print(f"\n    scale: toveli brain_list {before[0]:.1f} -> {after[0]:.1f} ms, brain_search {before[1]:.1f} -> {after[1]:.1f} ms, after the sibling gained 20,000 pages")
        for b, a, tool in zip(before, after, ["brain_list", "brain_search"]):
            self.assertLess(a, b + 5, f"toveli's {tool} went from {b:.1f} ms to {a:.1f} ms when the sibling gained 20,000 pages")
        if not SUPER_DSN:
            print("    scale with the unfavourable plan forced: NOT RUN (SUPER_DSN not set)")
            return
        with worst_case(T_LIST, T_SEARCH):
            forced = both()
        print(f"    scale with the unfavourable plan forced: brain_list {forced[0]:.1f} ms, brain_search {forced[1]:.1f} ms")
        for b, a, tool in zip(before, forced, ["brain_list", "brain_search"]):
            self.assertLess(a, b + 5, f"with the unfavourable plan, toveli's {tool} took {a:.1f} ms against {b:.1f} ms before the sibling gained 20,000 pages")

    def test_search_time_does_not_depend_on_what_other_organizations_pages_say(self):
        """Measured twice. First as deployed. Then in the conditions under which a missing fence does its damage (needs SUPER_DSN): the
        unfavourable kind of plan forced and the scan setting taken off the search function, so that the fence stands alone. Without the
        fence PostgreSQL then tries the search text on every row first. The mutation sweep's second run showed that the first
        measurement alone does not notice a missing fence."""
        def median_ms(n=9):
            ts = []
            for _ in range(n):
                t0 = time.perf_counter()
                ok, payload, _ = call(TOK("toveli"), "brain_search", {"query": "launch checklist"})
                ts.append((time.perf_counter() - t0) * 1000)
                assert ok and payload["count"] == 1
            return statistics.median(ts)
        before = median_ms()
        for batch in range(4):                                                         # 240 made-up pages of 100,000 characters each, in the SIBLING
            ups = [{"path": f"big/{batch}-{i:03d}.txt", "title": f"Code: big/{batch}-{i:03d}.txt", "body": os.urandom(50000).hex(),
                    "content_sha": hashlib.sha1(f"{batch}-{i}".encode()).hexdigest()} for i in range(60)]
            admin("/admin/codebase_sync", {"org": "sibling", "upserts": ups})
        after = median_ms()
        print(f"\n    content timing: toveli brain_search {before:.1f} ms before, {after:.1f} ms after the sibling gained 24 million characters")
        self.assertLess(after, before + 15, f"toveli's search went from {before:.1f} ms to {after:.1f} ms: the search text is being tried against the sibling's pages")
        if not SUPER_DSN:
            print("    content timing with the fence standing alone: NOT RUN (SUPER_DSN not set)")
            return
        with worst_case(T_SEARCH, allow_scans=True):
            alone = median_ms()
        print(f"    content timing with the fence standing alone: {alone:.1f} ms")
        self.assertLess(alone, before + 15, f"with only the fence, toveli's search took {alone:.1f} ms against {before:.1f} ms before: the fence is not holding")


@unittest.skipUnless(APP_DSN, "BRAIN_APP_DSN not set: NOT RUN")
class KnownLimits(Base):
    """What this pass does not close. Each test asserts the rule one would want and is marked as an expected failure,
    so the gap shows in every run instead of living only in a document."""

    @unittest.expectedFailure
    def test_the_database_login_cannot_learn_how_much_the_whole_database_holds(self):
        """PostgreSQL lets any login ask how large a table is. One database for every organization means the service's own login can
        watch the pages table grow. A token cannot; this needs the database password. One database per customer removes it."""
        size = lambda: psql("select pg_relation_size('brain.pages')")[1]
        before = size()
        ups = [{"path": f"gen/{i:05d}.py", "title": f"Code: gen/{i:05d}.py", "body": f"made-up page {i}", "content_sha": str(i)} for i in range(1500)]
        admin("/admin/codebase_sync", {"org": "sibling", "upserts": ups})
        self.assertEqual(before, size())

    @unittest.expectedFailure
    def test_a_read_that_the_database_login_rolls_back_still_leaves_a_row(self):
        """The row for an allowed read is written in the same transaction as the read. The service always commits before it answers, so a
        token cannot read without a row. Someone holding the database password and a valid token can: read, then roll back. Closing it
        means writing the row first in a transaction of its own, at the price of one more transaction per call."""
        before = last_audit_id()
        code, out = psql(f"begin; select brain.begin_session('{TOK('toveli')}'); select brain.t_search('fix-direct-2', null, 'CANARY', null, 10); rollback;")
        self.assertIn("CANARY-TOVELI-1", out)
        self.assertEqual([r["request_id"] for r in audit_rows(before)], ["fix-direct-2"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
