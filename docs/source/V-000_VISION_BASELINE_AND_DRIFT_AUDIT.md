# V-000 — Vision baseline and drift audit

Status: v0.5, proposed, 2026-11-18. v0.3 was accepted when the founder merged pull request #3 (commit 4a31bf2, 2026-11-17 04:59 UTC). v0.4 is proposed in pull request #5, which was open when this was written. v0.5 records the decisions Cole gave on 2026-11-17 after reading the review REV-01, in section 2a (F-32 to F-40), with new open items and acceptance rows. Every addition carries its date. No accepted text is rewritten or removed. Acceptance of v0.5 is the founder's merge of the pull request that carries it.

Status line as written for v0.4, kept for the record: "v0.4, proposed, 2026-11-17. v0.3 was accepted when the founder merged pull request #3 (commit 4a31bf2, 2026-11-17 04:59 UTC). v0.4 records Gate G1a (Route B) and two decisions made around it, in section 2a, with new open items and acceptance rows. Every addition carries its date. No accepted text is rewritten or removed. Acceptance of v0.4 is the founder's merge of the pull request that carries it."

Status line as written for v0.3, kept for the record: "v0.3, proposed, 2026-11-15. v0.2 was accepted at Gate G0 when the founder merged pull request #1 on 2026-11-15 (commit 2baba1b). v0.3 appends the changes R-01 section 10 proposed and the founder's inputs of 2026-11-15. Every addition carries its date. No v0.2 text is rewritten or removed; where a v0.2 statement is amended, the amendment sits beside it and governs. Acceptance of v0.3 is the founder's merge of the pull request that carries it."

Status line as written for v0.2, kept for the record: "v0.2, proposed. The founder's answers of 2026-11-15 are folded in. Acceptance is the founder's merge of the pull request that carries this file (Gate G0)."

Inputs: founder note and chat replies of 2026-11-15; `AZI-HUB-PROJECT-BRIEF.md`; `CAT_Research_to_Product_Plan` (2026-08-18); the Gemini artifacts; the code of `azi-hub` and `autonomous-startup-engine`.

Inputs added for v0.3: `docs/research/R-01_CATEGORY_AND_EXISTING_TOOLS.md` v1.0, accepted with pull request #2 (commit 546715c), sections 7 to 11; the founder's inputs after that merge (manifest S-015).

Inputs added for v0.4: `docs/research/R-02_RUNTIME_AND_HARNESS.md` v1.0 (proposed in pull request #4) and the founder's replies to it in chat on 2026-11-16 and 2026-11-17 (manifest S-021).

## 1. Founder intent, restated

One person directs their personal life and a set of organizations through a single self-improving system. Agents do the execution. The human keeps creative direction and the key decisions.

A chief-of-staff agent knows the person's own life well enough to work with the administrators of their organizations. The personal second brain is kept apart from each organization's second brain and shared only on purpose.

It works for a new organization and for an existing one. Cole uses it first. If a product has room, other people get it, with onboarding help for those who already have operations.

**Added 2026-11-15 (v0.3). The mission, as Cole stated it** (R-01 section 11). Build toward idea to IPO on a constantly self-optimizing framework. The next Alphabet should be creatable with this tool: a management company that creates and scales Toveli and Cole's other ventures, and that also manages his personal life. This is the direction to build toward, recorded as F-19. It is not a claim about what any system does today; R-01 found no evidence of one (T-4).

## 2. Fixed decisions (Cole, 2026-11-15)

| ID | Decision |
| --- | --- |
| F-01 | The personal layer is part of the product. A customer may leave it off. |
| F-02 | Super-organization and sub-organization structure stays. |
| F-03 | New and existing enterprises are both in scope. |
| F-04 | Humans hold creative direction and key decisions. |
| F-05 | The system improves itself under control. |
| F-06 | Cole is the first user. Multi-person collaboration (the "social" layer) comes later. |
| F-07 | The route check is the first research step. Route A (product) is preferred. Route B (personal system on existing frameworks) is the fallback if a product has no room. |
| F-08 | New repository `CDM2/azi-hub-v2`. AZI Hub stays up about one more week for the morning reservation-booking agent, which then moves to the personal layer. |
| F-09 | `autonomous-startup-engine` is Cole's to use as he wishes. |
| F-10 | Personal-layer scope is chosen by the user and can grow, including financial and health areas. A user can ask for a new section, for example investing, subscriptions or diet. Users will not all want the same sections. |
| F-11 | Agents have the access they need to build those sections. |
| F-12 | Setup consulting is allowed as onboarding, aimed at people with existing operations. No custom framework is built per customer. |
| F-13 | Candidate customers: existing large organizations; new, well-funded organizations; non-technical solopreneurs running or starting small businesses. |
| F-14 | Organizations modelled first: AZI Hub with AltZ Capital, Sandbox and Media, plus Toveli as a sub-organization. Once the product is trusted these are expected to be wiped, with Toveli as the main organization. |
| F-15 | First slice: the personal layer plus the reservation-agent migration, then the research-to-decision workflow from the CAT plan. |
| F-16 | Claude-first behind an adapter boundary. Choosing a model per task must be easy, by setting or by asking the system. |
| F-17 | Self-hosted on Cole's VPS for his own use. A hosted offering is decided at Gate G1a. |
| F-18 | Build budget: up to $1,000 a month for agent and API runs, on top of existing Claude Max, ChatGPT and GitHub Pro subscriptions. Cole can raise it. |

### 2a. Amendments and additions (v0.3, 2026-11-15)

Rows F-01 to F-18 above stand as accepted in v0.2. Two are amended and six are added. Sources: Cole's answers recorded in R-01 section 11, and his inputs after the R-01 merge (manifest S-015).

| ID | Decision | Relation to v0.2 |
| --- | --- | --- |
| F-08a | The reservation-booking agent stays on the old VPS and is outside this build. It runs only on sites that allow agents. It does not move to the personal layer as part of the first slice. | Amends F-08. The new repository stands. "About one more week" and the move to the personal layer no longer apply. |
| F-15a | First slice: the personal layer, then Cole's own ventures as sub-organizations under a management company, then the research-to-decision workflow. | Amends F-15. The reservation-agent migration is removed and the ventures step is added. |
| F-19 | Mission: build toward idea to IPO on a constantly self-optimizing framework. A management company creates and scales Toveli and Cole's other ventures and also manages his personal life. | New. Direction, not a claim (section 1). |
| F-20 | Orchestration is adopted for now: unmodified Paperclip for each organization, behind a replaceable interface, with this project's own permission layer beside it (R-01 option D). This holds subject to the R-02 spike. A lean orchestrator of our own (option E) stays open. | New. |
| F-21 | Cole's own ventures are the first pilots: Toveli and a few others. Paid pilots with outside businesses follow. | New. Own ventures come before any F-13 customer group. |
| F-22 | Cole has 40 to 60 hours a week for this work. | New. |
| F-23 | Governance: this version builds in as much governance as is practical. Replacing Paperclip with a layer of our own, with our own governance and cloud, is a later option if the product takes off. | New. Changes where R-01 section 7 placed broader governance; see D-13. |
| F-24 | Codebases go in each company's second brain. Agents get a map: what each file and script does, its dependencies, and how it builds and deploys. Pages are tagged so that codebase, agent-written and human-written context can be told apart. Goal: upload the existing Toveli codebase, run a mapping pass, and have little onboarding work left. | New. Capability C-23 (section 2b). |

**Added later on 2026-11-15, still v0.3: Cole's answers to the R-02 spike plan** (manifest S-016). Four more decisions. They refine N-02 and N-08 below and change no accepted row.

| ID | Decision | Relation to v0.2 |
| --- | --- | --- |
| F-25 | Personal information is never sent to an organization, with one exception: a curated briefing that a human approves before it goes out. The briefing goes to the holding organization only. It has an off switch, because some users will not want it, most of all where several people work in the same organizations. Information flows back from the organizations to the personal space under the current permission rules. Health and finance pages exist only in the personal space. | New. Narrows "explicit push" in N-02 to this one path. Agrees with N-08. |
| F-26 | The product can ship with the personal space switched on or off. Some businesses will not want a personal space, and offering it to them would confuse what the product is. | New. F-01 stands; the personal space becomes optional per deployment. |
| F-27 | The holding organization can read the organizations below it. A page lives once, in the organization that owns it; the holding organization reads it there and no copy is made. A user who runs one company has only the holding organization, with no management layer above it. | New. Detail for F-02. How much the holding organization reads (everything or summaries) stays with R-04. |
| F-28 | Pricing of governance: a control that needs Paperclip's paid edition is passed on as a paid feature and is not subsidized. Governance this project builds itself is free for now. | New. An input to R-08. |

R-02 tests F-25 to F-27 in its spike (criteria 1 to 3) with the briefing switch on and off, the personal space on and off, and a single-company setup.

**Added 2026-11-17, v0.4: Gate G1a and two decisions made around it** (manifest S-021). Cole gave these in chat on 2026-11-16 and 2026-11-17 after reading the results of R-02. They change no accepted row.

| ID | Decision | Relation to earlier decisions |
| --- | --- | --- |
| F-29 | Gate G1a: Route B. The system is built first for Cole's own use: his personal space, the holding organization and his ventures. Three rules keep Route A open. One: tiers and organizations stay data and are never hard-coded. Two: a test that sets up a brand-new, empty organization from nothing runs on every change. Three: before Gate G1 there are five conversations with outside business owners, and if one of them wants a pilot, Route A is taken up. | Answers the question P-000 put to Gate G1a. F-15a and F-21 stand. Rule two keeps a small part of the blank-tenant work that Route B otherwise drops. |
| F-30 | Route A is not dropped. It comes later as a side track once Route B is running, possibly as a sub-organization of its own under the holding organization. The Route B build must be able to reach it without a large rebuild. Cole's reasons: he wants to use the tool as soon as possible, and if it works for him, customers will follow and will not wait months. | New. The Route A hypotheses in section 5 stay open. R-08 is Route A only and waits. |
| F-31 | A second person. Cole may run a sub-organization with another person. That person may reach that sub-organization's code and agents. They must never reach his personal space, his other sub-organizations or the holding organization's pages. On 2026-11-17 Cole agreed to the shared-venture spike that tests this (P-000, note of 2026-11-17 on R-03). The session recommends that no second person is added to any organization before it passes. | New. Extends N-02 from organizations to people. R-02 was built and tested for one person (ledger E-100, E-111). |

Where option D stands after R-02. The spike supports F-20: criteria 1 to 4 and 6 passed on an unmodified Paperclip (R-02 section 7). On 2026-11-16 Cole said he thinks he agrees with option D and raised the second-person question. He has not confirmed option D. The session recommends confirming it after the separate review of R-01 and R-02. For a second person, option D is unproven (F-31).

**Added 2026-11-18, v0.5: Cole's decisions after the review REV-01** (manifest S-023). Cole gave these in chat in two messages on the evening of 2026-11-17, after reading the review's summary. They change no accepted row. F-34 amends F-25 in one respect and says so.

| ID | Decision | Relation to earlier decisions |
| --- | --- | --- |
| F-32 | Option D is confirmed, on two conditions. Both must be met before real data goes in. One: an isolation test passes with one Paperclip per organization, the personal space included, in Paperclip's authenticated mode (REV-01 RV-01). Two: the permission service is fixed for REV-01 RV-02, RV-05, RV-06 and RV-07. One Paperclip per organization is the layout. Cole left that to the session ("If you think it makes the most sense to do one paperclip per organization let's do it"); the session does, because in Paperclip's local trusted mode every request is the board and all agents of one install run as one operating-system user (ledger E-114, E-111). | Confirms F-20 with conditions. Settles the v0.4 open item about a separate Paperclip for a shared venture: every organization gets its own. Condition two is reported in `docs/reviews/REV-01_FIX_PASS.md`. Condition one is open. |
| F-33 | First slice: the personal space, the holding organization and one venture, built together, so that the way the tiers work with each other is right from the start. Not a venture on its own with no layer above it. | Refines F-15a, which listed them in sequence. Replaces the review's suggestion of ventures first (REV-01 section 9). |
| F-34 | The personal rule, restated. Nothing reads a personal page unless Cole directly supplies the information. His example: "chief of staff, share my calendar for today with venture y so they can book a meeting". In his words, "the personal page should have access to everything". The chief of staff in the personal space is to know what is going on everywhere and, once the system is proven, relay to the holding organization and to the ventures what he needs done. | Amends F-25 in one respect: an approved push from the personal space may go to any organization its person belongs to, not to the holding organization only. This is the session's reading of his example; Cole to correct it if wrong. The rest of F-25 stands: the person approves before anything leaves, the off switch, health and finance pages only in the personal space. With a second person in the system, "everything" is everything he belongs to (F-31). |
| F-35 | A fourth rule for Route B: people and memberships are data from the first ticket, and a test with two people and two holding organizations runs on every change. | Adds to the three rules of F-29. Proposed by REV-01 (RV-03, RV-14). Makes F-31 testable. |
| F-36 | R-05 goes back on Route B's list. | Reverses its omission from the Gate G1a memo (REV-01 RV-14). |
| F-37 | Route A stays an eventual venture. Cole adds that it is also the way off Paperclip onto an orchestrator of this project's own, and that he already senses Paperclip's agent graph and harness are not great. | F-30 stands. This is not a decision to leave Paperclip; option E stays open as in F-20. |
| F-38 | Every action by an agent or by a person goes into one append-only log, so that what happened can be understood and steps can be rolled back. On R-02 criterion 4 Cole questioned keeping logs in two places and left the choice to the session. The session's choice: the permission service's log is the record. Paperclip keeps its own log whether or not this project wants it, and that log is used only as a cross-check. | New. Makes the audit part of C-07 a requirement on people's actions as well as agents'. Rollback is a requirement on record; it is not designed or built (section 6). |
| F-39 | The order of customer groups for going to market stays as R-01 has it: small-business owners and individuals starting a business first, then well-capitalized startups, then larger existing businesses. | Keeps R-01 section 8. REV-01 RV-13 argued that the first group gains least from tiers; Cole read that and kept the order. |
| F-40 | F-29 rule three stays as written. The review's proposal to sharpen "wants a pilot" to "pays for a pilot" is put off until there is something to pilot. Cole expects to bear the early costs himself to win first customers and a proof of concept. | REV-01 section 9, item 6: deferred, not rejected. |

Cole also said the failing tests of the review must be resolved, and on reading the notes of an outside conversation told the session to start the fix pass. That is an instruction, not a vision decision; it is in the acceptance record below.

Where option D stands after the review and the fix pass (2026-11-18). Confirmed on two conditions (F-32). Condition two: `docs/reviews/REV-01_FIX_PASS.md` reports that the 23 review tests that failed against the R-02 service are resolved in a fixed copy of the service under `spikes/rev-01-fix/`, and says exactly which assertions changed. Condition one is open: it needs Paperclip installed on a scratch machine, which the session's sandbox does not allow. For a second person, the permission service now passes the review's second-person tests; nothing about a second person has been tested with Paperclip running.

### 2b. Capability added after R-01 (2026-11-15)

R-01 section 5 lists capabilities C-01 to C-22. This one continues that numbering. R-01 itself is not edited.

| ID | Capability (V-000 reference) | Best existing tool | Coverage | Missing glue | Evidence | Settled in |
| --- | --- | --- | --- | --- | --- | --- |
| C-23 | A codebase map in each organization's second brain: for each file its purpose, imports and entry points, plus the build and deploy steps; tagged as codebase; readable only inside that organization's tier (F-24, N-02) | Not assessed yet. R-02 criterion 8 surveys existing tools (repository maps, code graphs, generated repository wikis) before anything is built. | Not assessed | Not assessed. Prior art: AZI Hub's `seedCodebaseIndex` writes one page per directory with a file list and export names, tagged `source_type: codebase` (INV-000). | None yet. R-02 adds the ledger rows. | R-02 (spike criterion 8), R-04 |

## 3. Non-negotiables proposed to carry over

| ID | Rule | Origin |
| --- | --- | --- |
| N-01 | No agent pushes to production, moves money, or changes another organization's state without human approval. | AZI Hub kill list |
| N-02 | No tenant mixing. Personal to organization is explicit push only. Organization to organization is zero by default. | AZI Hub tier model |
| N-03 | Deterministic software decides permissions, policy, money, state transitions and approvals. | CAT rule 5 |
| N-04 | A multi-agent design must beat a single agent with workflows to be kept. | CAT rule 7 |
| N-05 | Self-improvement acts only on verifiable metrics. Strategy stays human-gated. | AZI Hub brief 6.6 |
| N-06 | No employer or third-party proprietary data enters this project. | CAT plan, step 4 |
| N-07 | Agents extend a user's own instance. Changes to the shared core go through the build loop and its review tiers. | AZI Hub framework and instance boundary; applies F-11 |
| N-08 | Health and financial data are the highest sensitivity class: they stay in the personal tenant, are never pushed to an organization by default, and stay out of logs and evaluation sets. | Follows from F-10 and N-02 |

How N-01 applies to F-10: a finance section may read, analyze and propose. A trade, payment or transfer needs the user's approval each time, unless a later decision record sets a pre-approved limit.

Added 2026-11-15 (v0.3). How N-02, N-03 and N-06 apply to F-24: a codebase map is that organization's data. A sibling organization never reads it. The database or the service applies that filter, never a prompt. What the holding tier may read of a sub-organization's map is settled in R-04. Source code that belongs to an employer or a third party does not go in.

## 4. Drift audit

| # | Earlier position | Current intent | Disposition |
| --- | --- | --- | --- |
| D-01 | CAT plan: personal second brain stays outside the product boundary and outside tenancy. | F-01. | Resolved by F-01. The old rule's safety content is kept as N-02: explicit push only. |
| D-02 | CAT charter non-goal: personal health or financial automation. | F-10. | Resolved by F-10. In scope as sections the user chooses; N-01 and N-08 apply. |
| D-03 | AZI Hub kill list: no one-off consulting or services work. | F-12. | Resolved by F-12. The kill-list item narrows to "no bespoke one-off builds". |
| D-04 | AZI Hub: infrastructure first. CAT checklist: build a full vertical outcome. | Landscape shows the horizontal layer is crowded. | The first slice is a vertical outcome for Cole (F-15). The route check decides the rest. |
| D-05 | AZI Hub: named executive-role agents. CAT and Gemini: a hypothesis. | The chief-of-staff role is stated intent; other roles are undecided. | Chief of staff is a requirement. Other role agents stay a hypothesis for R-03. |
| D-06 | Gemini artifacts: every quadrant and the personal layer left open. | Section 2. | Superseded by section 2. |
| D-07 | Brief and dossier: the tenant is resolved from request context, never accepted as a parameter. | Code takes it from a header the client sets. | Implementation claims in summaries are unverified until checked in code. The new build ties the organization to the signed-in person. |
| D-08 | CAT plan Slice 0: governed research-to-decision. | F-15. | Resolved by F-15: it is the second step of the first slice. |
| D-09 | CAT plan: integrate with systems of record, do not replace them. | Unchanged. | Default stays "integrate"; R-09 can challenge it. |
| D-10 | Plan requires one first wedge. | F-13 names three customer groups with different buyers, sales cycles and competitors. | All three stay candidates. R-01 and R-08 rank them and name one first wedge. Cole as first user is closest to the solopreneur group; the onboarding thesis (F-12) is closest to existing organizations. |
| D-11 | CAT charter non-goals: production self-modification; high-impact autonomous financial actions. | F-10 and F-11: agents build personal sections, including financial ones. | Allowed inside the instance boundary (N-07) with N-01. R-05, R-06 and R-07 define the controls. |

Rows added 2026-11-15 (v0.3). D-10 above is kept as written; D-10a records what R-01 settled.

| # | Earlier position | Current intent | Disposition |
| --- | --- | --- | --- |
| D-10a | D-10 left the three F-13 customer groups as candidates for R-01 and R-08 to rank. | R-01 section 8, accepted with pull request #2, ranks them: 1, non-technical owners of existing small businesses; 2, new, well-funded organizations; 3, existing large organizations, as a long-term destination. Cole's own ventures come before all three (F-21). | Ranking recorded. First outside wedge: small local businesses with existing operations, onboarded in person and sold as setup plus a monthly plan. This is a desk judgment until an outside business pays; R-08 tests it. |
| D-12 | F-08 and F-15: the reservation agent moves to the personal layer as part of the first slice. | The agent runs only on sites that allow agents and is outside the build. | Resolved by F-08a and F-15a. |
| D-13 | R-01 section 7: this project builds governance only for what it owns (approvals on sharing, the improvement gate). Broader governance and hosting wait for Gate G1. | F-23: as much governance in this version as is practical. | Resolved by F-23 for governance. R-02 criterion 7 sorts every required control into free in Paperclip, paid edition only, or ours to build, and says whether R-01's trigger 3 for option E is met. A hosted offering still waits for Gate G1 (F-17). |
| D-14 | AZI Hub: a codebase index of one page per directory, covering its own code only. A fuller "cartographer" pass was planned and not built. | F-24: a file-level map of each company's codebase in that company's brain. | Carried as C-23. R-02 criterion 8 checks existing tools first, then tests the smallest version on Toveli against a plain coding agent (N-04). |

## 5. Route A hypothesis, to be tested in R-01

| ID | Claim | What would falsify it |
| --- | --- | --- |
| H-A1 | People and organizations with existing operations cannot set up current frameworks without help. | A product they can set up alone already covers the personal layer, an organization hierarchy and governed self-updating. |
| H-A2 | They will pay for onboarding and keep paying to stay in the ecosystem. | Interviews or pricing evidence show they will not, or that onboarding is a one-time job with no reason to stay. |
| H-A3 | What they would be onboarded to is not already sold turnkey. | Polsia, NanoCorp, Paperclip or a control-plane vendor already sells it to the same buyer. |
| H-A4 | Buyers want a personal layer whose chief-of-staff agent coordinates with organization administrators, and vendors do not offer it. | A vendor offers it, or buyers do not want personal and company context in one system. |

Early counter-signals, from search results only: NanoCorp and Polsia already sell no-code creation of AI-run companies, and OpenAI pairs forward-deployed engineers with enterprise customers for onboarding. Neither covers the personal layer as far as the first pass shows.

### 5a. The hypotheses after R-01 (added 2026-11-15, v0.3)

R-01 section 3 tested the four claims. The table above is kept as accepted in v0.2. H-A3 and H-A4 are restated as R-01 section 10 proposed. The IDs do not change, so ledger rows that cite them still apply. Evidence IDs point to `../research/EVIDENCE_LEDGER.md`.

| ID | Claim, as it stands now | What would falsify it | R-01 verdict on the v0.2 wording |
| --- | --- | --- | --- |
| H-A1 | Unchanged. | Unchanged. | Holds in part. True of self-hosted frameworks and of enterprises; false for the hosted personal agents a small-business owner is likely to try first. |
| H-A2 | Unchanged. | Unchanged. | The price is supported by quotes. Retention is untested, and no outside business has paid. |
| H-A3 | Restated: the combination is not sold turnkey. That is a holding structure with deliberate sharing, a personal space with a one-way boundary, a second brain that respects both, and improvement gated by evidence. | A vendor sells that combination to the same buyer. | Partly falsified as first written: each main job is already sold turnkey to each buyer group. |
| H-A4 | Restated: owner-operators want a chief of staff that works with the agents of their own organizations, across a holding organization and its sub-organizations, over a second brain filtered by tier, and no vendor offers that. | A vendor offers it, or owner-operators do not want personal and company context in one system. | Falsified as first written on the vendor half: personal layers are now sold. The buyer half is untested. |

**Counter-signals as of 2026-11-15.** This replaces the paragraph above, which is kept as written. Hosted personal agents now exist and need no setup: Claude Duet, ChatGPT dots, Meta's Muse and Muse for Small Business, and Ariso's Ari, which is sold as one chief of staff across work and life (E-27, E-29, E-30, E-31). None was found to cover several organizations under one owner or a second brain filtered by tier (E-28, E-29, E-31, E-65). NanoCorp and Polsia still sell no-code creation of AI-run companies (E-12, E-14). OpenAI still sells enterprise onboarding through its own engineers and four consultancies (E-20, E-21).

## 6. Open items

Nothing blocks Phase 1a. Left for later gates:

- The first wedge among the F-13 groups: Gate G1a and Gate G1.
- Pre-approved limits for money movement, if any: R-05.
- How far agents may change shared core code: R-06 and R-07.

Added 2026-11-15 (v0.3):

- Gate G1a waits on R-02, which runs the option D spike. F-20 holds only if the spike supports it.
- The first wedge now has a desk answer (D-10a). It stays open until an outside business pays.
- What the holding tier may read of a sub-organization's codebase map: R-04.
- Whether a separate review session attacks R-01 and R-02 before Gate G1a: Cole.

Added 2026-11-17 (v0.4):

- Gate G1a is decided: Route B (F-29). On the review item above: Cole decided the route first and asked for the review's prompt on 2026-11-17, so the review runs next. Its brief is `docs/reviews/REV-01_BRIEF.md`.
- Confirmation of option D (F-20): Cole. The session recommends waiting for the review.
- Whether a venture shared with a second person runs on its own Paperclip instance. The session recommends it; Cole has not decided. The shared-venture spike tests both ways.
- What the holding organization reads of a venture's code map. Cole left this to the session to investigate and decide. The session's proposed default: structure pages only (the overview and the package pages), file pages opt-in for each venture, and nothing from a venture shared with a second person except by an approved push. R-04 confirms or changes it.
- R-02 criterion 5 has not run on a real Toveli task. It stays open until Toveli may be touched by this project.

Added 2026-11-18 (v0.5):

- Option D is confirmed on two conditions (F-32), which closes the v0.4 item on confirmation. A separate Paperclip for a shared venture is settled too: every organization gets its own.
- Condition one of F-32, the isolation test, is open. It needs Paperclip on a scratch machine.
- Health and finance pages stay out of the system until condition one passes and REV-01 RV-04 (Paperclip keeps the arguments of every call as text) is answered for the personal install.
- Whether one owner's approval is enough for a report that leaves a venture two people own, or both must approve: Cole. The fix pass built "one owner".
- The operator's approval routes in the permission service: keep as an override, restrict, or remove. Cole. The fix pass kept them, logs them, and makes them name a person who has the authority.
- Rollback (F-38). The fix pass built the append-only log and nothing that blocks rollback. It built no rollback, and the code mapper still updates pages in place. The design belongs in a later report.
- Who the five conversations of F-29 rule three are with. The outside conversation of 2026-11-17 (ledger E-128) was with a builder, not a buyer; the session does not count it unless Cole says so.
- REV-01 findings that the fix pass did not touch because they are about Paperclip or about the reports: RV-01, RV-04, RV-08 (the cross-check half), RV-09 to RV-14, RV-20, RV-21. Each still waits for Cole's ruling.

## 7. Acceptance record

| Record | Person | Date | Scope |
| --- | --- | --- | --- |
| Draft v0.1 prepared | Claude session | 2026-11-15 | Not accepted |
| Answers and direction to revise and push | Cole | 2026-11-15 (chat) | Authorizes v0.2 and the Phase 0 seed push; not acceptance |
| Founder acceptance (Gate G0) | Cole | 2026-11-15 | Merge of the pull request carrying v0.2: pull request #1, squash-merged at 2baba1b |
| R-01 v1.0 accepted | Cole | 2026-11-15 | Pull request #2, squash-merged at 546715c (2026-11-16 01:00 UTC). An input to v0.3; not an acceptance of V-000 |
| Inputs and instruction to prepare v0.3 | Cole | 2026-11-15 (chat, R-02 brief) | Authorizes v0.3; not acceptance |
| Draft v0.3 prepared | Claude session | 2026-11-15 | Not accepted |
| Answers to the R-02 spike plan | Cole | 2026-11-15 (chat) | Adds F-25 to F-28 to the v0.3 draft; not acceptance |
| Founder acceptance of v0.3 | Cole | 2026-11-17 UTC | Merge of the pull request carrying v0.3: pull request #3, squash-merged at 4a31bf2 (2026-11-17 04:59 UTC) |
| Gate G1a and the decisions around it | Cole | 2026-11-16 and 2026-11-17 (chat) | Route B with three rules, Route A later, the second-person rule. Authorizes v0.4 (F-29 to F-31); not acceptance |
| Draft v0.4 prepared | Claude session | 2026-11-17 | Not accepted |
| Founder acceptance of v0.4 (Gate G1a on record) | pending | | Merge of the pull request carrying v0.4 |
| Review REV-01 v1.0 prepared | Claude session | 2026-11-17 | Pull request #6. Not accepted |
| Decisions after the review, and the instruction to run the fix pass | Cole | 2026-11-17 (chat, two messages) | Option D confirmed on two conditions; one Paperclip per organization; the first slice; the personal rule; the fourth rule; R-05; Route A; one append-only log; the customer order; rule three unchanged. Authorizes v0.5 (F-32 to F-40) and the fix pass; not acceptance |
| Draft v0.5 prepared | Claude session | 2026-11-18 | Not accepted |
| Founder acceptance of v0.5 | pending | | Merge of the pull request carrying v0.5 |
