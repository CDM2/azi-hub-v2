"""REV-01 review, item 9: a second person (V-000 F-31), on the permission service only.

Scenario. Cole runs the sub-organization "shared" with a friend. The friend must never reach Cole's personal
space, his other sub-organizations ("toveli", "sibling") or the holding organization's pages ("mgmt").
The service has no person: a token is bound to one organization. So the friend is modelled the only way the
service allows today, in three steps:

  A. The friend holds a human token of "shared" and nothing else.
  B. The friend also has a personal space of their own ("friend-personal"), as P-000's shared-venture
     criterion 3 requires ("two people each have a personal space").
  C. The friend also runs a company of their own in the same service ("acme" with "acme-sub").

Every test asserts what F-31 and P-000's note on R-03 require. A PASS is a rule the service holds today.
A FAIL is a rule it does not hold; the docstring names the finding in docs/reviews/REV-01_R-01_AND_R-02.md.
Paperclip is not involved and was not run. Made-up data only. Standard library only.
"""
import json
import re
import unittest

from common import admin, call, http_call, page_id

ORGS = [("personal", "personal", None), ("mgmt", "holding", None), ("toveli", "sub", "mgmt"), ("sibling", "sub", "mgmt"), ("shared", "sub", "mgmt")]
STEP_B = [("friend-personal", "personal", None)]
STEP_C = [("acme", "holding", None), ("acme-sub", "sub", "acme")]
PRINCIPALS = [("personal", "agent"), ("mgmt", "agent"), ("toveli", "agent"), ("sibling", "agent"), ("shared", "agent"), ("shared", "human"),
              ("friend-personal", "agent"), ("acme", "agent"), ("acme-sub", "agent")]
PAGES = [
    ("mgmt", "Shared style guide", "CANARY-GLOBAL-1 everyone under this holding organization may read this.", {"visibility": "global"}),
    ("mgmt", "Holding plan", "CANARY-MGMT-1 allocation across ventures.", {}),
    ("toveli", "Toveli launch notes", "CANARY-TOVELI-1 launch checklist.", {}),
    ("toveli", "Code: apps/api/main.ts", "CANARY-TOVELI-2 code page.", {"kind": "code_file", "source_type": "codebase", "path": "apps/api/main.ts"}),
    ("sibling", "Sibling roadmap", "CANARY-SIBLING-1 confidential roadmap.", {}),
    ("shared", "Shared venture notes", "CANARY-SHARED-1 notes both people may read.", {}),
    ("shared", "Shared venture summary", "CANARY-SHARED-2 weekly summary.", {"kind": "summary", "source_type": "agent"}),
    ("shared", "Code: app/main.py", "CANARY-SHARED-3 code page.", {"kind": "code_file", "source_type": "codebase", "path": "app/main.py"}),
    ("personal", "Cole goals", "CANARY-PERSONAL-1 goals for the year.", {}),
    ("personal", "Cole health log", "CANARY-PERSONAL-2 made-up health entry.", {"sensitivity": "health"}),
    ("personal", "Cole brokerage note", "CANARY-PERSONAL-3 made-up finance entry.", {"sensitivity": "finance"}),
    ("friend-personal", "Friend goals", "CANARY-FRIENDP-1 the friend's own goals.", {}),
    ("friend-personal", "Friend health log", "CANARY-FRIENDP-2 made-up health entry.", {"sensitivity": "health"}),
    ("acme", "Acme plan", "CANARY-ACME-1 the friend's own company plan.", {}),
    ("acme", "Acme handbook", "CANARY-ACMEGLOBAL-1 global page of the friend's company.", {"visibility": "global"}),
    ("acme-sub", "Acme sub notes", "CANARY-ACMESUB-1", {}),
]
TOK = lambda org, actor="agent": f"rev01-{org}-{actor}"
FRIEND = TOK("shared", "human")


def fixture(steps="A"):
    orgs = ORGS + (STEP_B if steps in ("B", "C") else []) + (STEP_C if steps == "C" else [])
    ids = {o[0] for o in orgs}
    return {"settings": {"personal_enabled": True, "briefing_enabled": True, "holding_reads": "all"},
            "orgs": [{"id": i, "kind": k, "parent": p} for i, k, p in orgs],
            "principals": [{"org": o, "actor": a, "token": TOK(o, a)} for o, a in PRINCIPALS if o in ids],
            "pages": [dict({"org": o, "title": t, "body": b, "kind": "note", "source_type": "human"}, **extra) for o, t, b, extra in PAGES if o in ids]}


def markers(token):
    """The set of made-up organizations whose page text this token can get by search."""
    ok, payload, raw = call(token, "brain_search", {"query": "CANARY", "limit": 200})
    assert ok, raw[:200]
    return set(re.findall(r"CANARY-([A-Z]+)-\d", raw))


class StepA_FriendHoldsOneHumanToken(unittest.TestCase):
    def setUp(self):
        admin("/admin/reset", fixture("A"))

    def test_the_friend_reads_the_shared_venture_and_global_pages_only(self):
        """P-000 shared-venture criterion 2. Holds."""
        self.assertEqual(markers(FRIEND), {"SHARED", "GLOBAL"})
        ok, payload, raw = call(FRIEND, "brain_list", {"limit": 200})
        self.assertEqual({p["org"] for p in payload["pages"]}, {"shared", "mgmt"})
        self.assertEqual(payload["count"], 4)

    def test_the_friend_cannot_fetch_any_other_page_by_id_path_or_words(self):
        """P-000 shared-venture criterion 2, by every read tool. Holds."""
        targets = {"toveli": page_id(TOK("toveli"), "CANARY-TOVELI-1"), "sibling": page_id(TOK("sibling"), "CANARY-SIBLING-1"),
                   "mgmt": page_id(TOK("mgmt"), "CANARY-MGMT-1"), "personal": page_id(TOK("personal"), "CANARY-PERSONAL-2")}
        for org, pid in targets.items():
            ok, payload, raw = call(FRIEND, "brain_get", {"id": pid})
            self.assertEqual((ok, payload), (False, {"error": "not_found"}), org)
        for args in [{"path": "apps/api/main.ts"}, {"path": "/"}]:
            ok, payload, raw = call(FRIEND, "brain_get", args)
            self.assertFalse(ok)
        for query in ["launch checklist", "confidential roadmap", "allocation", "goals for the year", "health", "brokerage", "apps/api"]:
            ok, payload, raw = call(FRIEND, "brain_search", {"query": query})
            self.assertEqual(payload["count"], 0, query)

    def test_the_friend_cannot_use_the_admin_routes_publish_a_briefing_or_write_a_global_page(self):
        """Holds."""
        for method, path in [("GET", "/admin/audit?since_id=0"), ("GET", "/admin/pages_digest?org=mgmt"), ("POST", "/admin/settings")]:
            status, _ = http_call(method, path, FRIEND, {} if method == "POST" else None)
            self.assertEqual(status, 401)
        ok, payload, _ = call(FRIEND, "publish_briefing", {"content": "x"})
        self.assertEqual(payload, {"error": "forbidden"})
        ok, payload, _ = call(FRIEND, "brain_write", {"title": "g", "body": "x", "visibility": "global"})
        self.assertEqual(payload, {"error": "forbidden"})

    def test_a_holding_agent_cannot_hand_the_friend_another_ventures_page(self):
        """RV-02. F-31: the friend must never reach Cole's other sub-organizations or the holding organization's pages.
        Calls: mgmt agent brain_write {visibility: global} with text it read from toveli and from its own plan; friend brain_search."""
        for marker in ["CANARY-TOVELI-1", "CANARY-MGMT-1"]:
            _, found, _ = call(TOK("mgmt"), "brain_search", {"query": marker})
            call(TOK("mgmt"), "brain_write", {"title": "for all ventures", "body": "copied: " + found["pages"][0]["snippet"], "visibility": "global"})
        got = markers(FRIEND)
        self.assertEqual(got, {"SHARED", "GLOBAL"}, f"the friend's token now reads {sorted(got)}: an AGENT in the holding organization published the text "
                                                    "as a global page and no human approved it")

    def test_the_holding_organizations_standing_read_can_be_switched_off_for_the_shared_venture_alone(self):
        """RV-03. P-000 shared-venture criterion 6, and V-000 section 6 ("nothing from a venture shared with a second person except by an approved push")."""
        tried = []
        for body in [{"holding_reads": {"shared": "none"}}, {"holding_reads_shared": "none"}, {"org": "shared", "holding_reads": "none"}, {"holding_reads": "none"}]:
            status, raw = http_call("POST", "/admin/settings", __import__("common").ADMIN, body)
            tried.append(status)
        got = markers(TOK("mgmt"))
        self.assertTrue("SHARED" not in got and "TOVELI" in got,
                        f"no setting exists for one venture (statuses {tried}); the holding agent reads {sorted(got)}. "
                        "holding_reads is one switch for every venture")

    def test_what_the_friend_writes_does_not_reach_coles_agents_without_a_decision(self):
        """RV-03. The other direction of the same rule: text the friend writes is read by the holding agent and by Cole's personal agent at once."""
        ok, w, _ = call(FRIEND, "brain_write", {"title": "note from the friend", "body": "CANARY-SHARED-9 text addressed to whichever agent reads this"})
        readers = [org for org in ["mgmt", "personal"] if "CANARY-SHARED-9" in call(TOK(org), "brain_search", {"query": "CANARY-SHARED-9"})[2]]
        self.assertEqual(readers, [], f"read without any approval by the agents of: {readers}")


class StepB_TwoPersonalSpaces(unittest.TestCase):
    def setUp(self):
        admin("/admin/reset", fixture("B"))

    def test_neither_personal_space_reads_the_other(self):
        """P-000 shared-venture criterion 3, first half. Holds."""
        self.assertNotIn("FRIENDP", markers(TOK("personal")))
        self.assertNotIn("PERSONAL", markers(TOK("friend-personal")))
        for token, marker_owner, marker in [(TOK("personal"), TOK("friend-personal"), "CANARY-FRIENDP-2"), (TOK("friend-personal"), TOK("personal"), "CANARY-PERSONAL-2")]:
            ok, payload, _ = call(token, "brain_get", {"id": page_id(marker_owner, marker)})
            self.assertEqual(payload, {"error": "not_found"})

    def test_the_friends_personal_space_reads_only_the_organizations_the_friend_belongs_to(self):
        """RV-03. P-000 shared-venture criterion 3, second half. schema.sql line 154: any personal-kind organization reads every organization."""
        got = markers(TOK("friend-personal"))
        self.assertEqual(got, {"FRIENDP", "SHARED", "GLOBAL"},
                         f"the friend's personal space reads {sorted(got)}: Cole's holding organization and both of his other ventures")

    def test_switching_one_personal_space_off_leaves_the_other_working(self):
        """RV-03. F-26 makes the personal space optional per deployment; with two people it has to be per person."""
        status_friend, _ = http_call("POST", "/admin/settings", __import__("common").ADMIN, {"personal_enabled": False, "org": "friend-personal"})
        ok, payload, raw = call(TOK("personal"), "brain_whoami")
        self.assertTrue(ok, "the only personal switch is global: switching the friend's personal space off switched Cole's off too "
                            f"(Cole's token now gets {payload})")


class StepC_FriendAlsoRunsACompany(unittest.TestCase):
    def setUp(self):
        admin("/admin/reset", fixture("C"))

    def test_coles_personal_space_does_not_read_the_friends_company(self):
        """RV-03, the same rule from the other side."""
        got = markers(TOK("personal"))
        self.assertFalse(got & {"ACME", "ACMESUB"}, f"Cole's personal space reads {sorted(got)}, including a company he does not belong to")

    def test_a_global_page_stays_inside_its_own_holding_organization(self):
        """RV-03. Global means "every organization under this holding organization", not every organization in the service."""
        self.assertNotIn("ACMEGLOBAL", markers(TOK("toveli")), "Cole's venture reads the other company's global page")
        self.assertNotIn("GLOBAL", markers(TOK("acme-sub")) - {"ACMEGLOBAL"}, "the friend's company reads Cole's holding organization's global page")

    def test_a_briefing_goes_to_its_own_persons_holding_organization(self):
        """RV-03. schema.sql brain.holding_org(): "order by id limit 1". With two holding organizations, every briefing goes to the first by name."""
        ok, b, _ = call(TOK("personal"), "publish_briefing", {"content": "CANARY-COLEBRIEF-1 Cole's personal priorities"})
        admin("/admin/approve_briefing", {"briefing_id": b["briefing_id"], "approver": "cole"})
        seen_by = [org for org in ["mgmt", "acme"] if "CANARY-COLEBRIEF-1" in call(TOK(org), "brain_search", {"query": "CANARY-COLEBRIEF-1"})[2]]
        self.assertEqual(seen_by, ["mgmt"], f"Cole's approved personal briefing is readable in {seen_by}: it was addressed to the other person's company")

    def test_a_holding_organization_reads_only_its_own_sub_organizations(self):
        """Holds: the parent check in the read rule is by parent_id."""
        self.assertFalse(markers(TOK("acme")) & {"TOVELI", "SIBLING", "SHARED", "MGMT"})
        self.assertFalse(markers(TOK("mgmt")) & {"ACME", "ACMESUB"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
