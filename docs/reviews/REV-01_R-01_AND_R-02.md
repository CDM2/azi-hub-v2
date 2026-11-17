# REV-01 — Review of R-01 and R-02

Status: v1.0, for Cole's ruling. As of 2026-11-17. Prepared by a separate Claude session on the brief in [`REV-01_BRIEF.md`](REV-01_BRIEF.md). This session did not write R-01, R-02 or the spike. Its job was to break them.

Reads with [`R-01`](../research/R-01_CATEGORY_AND_EXISTING_TOOLS.md), [`R-02`](../research/R-02_RUNTIME_AND_HARNESS.md), `docs/source/V-000` (decisions F-xx, rules N-xx) and `docs/source/P-000`. Evidence IDs such as E-116 point to rows in [`EVIDENCE_LEDGER.md`](../research/EVIDENCE_LEDGER.md); this review adds E-114 to E-127. Finding IDs are RV-01 to RV-21. Tests, measurements and raw output are in [`spikes/r-02/review/`](../../spikes/r-02/review/). A sentence marked **Judgment** is my reading, not a sourced fact.

Terms. **Option D**: an unmodified Paperclip per organization with our own permission service beside it. **Option E**: a lean orchestrator of our own. **The service**: the spike's permission service. **Holding organization**: the management company above the ventures. **Sibling**: another venture under the same holding organization. **The gateway**: the part of Paperclip through which its agents call outside tools. **The board**: Paperclip's name for the human operator with full rights. **C1 to C8**: R-02's eight pass criteria.

## 1. Verdict in five lines

1. **Option D stands as the working choice, not as "D holds".** The spike showed that an unmodified Paperclip can sit in front of our service. It did not test the layout R-02 itself recommends, it never let an agent leave the gateway, and nothing in it compared D with E.
2. **Criteria.** C2 and C6 stand. C1, C3, C4 and C7 stand with changes. C5 was not run, and its stand-in does not test N-04. C8 stands for its main result and not for its claim about the map-only reader.
3. **Our service.** With the spike's own four organizations, no call returned a sibling's, personal, health or finance page to a caller that may not read it. But 15 of 24 new tests fail: an agent can relay pages across tiers with no human step, timing reveals that a page exists and how much other organizations hold, and a crafted request leaves no audit row.
4. **A second person is not safe today.** A second personal space reads every organization. With a second holding organization, Cole's approved briefing lands in the other person's company. 8 of 13 second-person tests fail.
5. **Nothing reopens Route B.** Two additions to its three rules are needed: people and memberships as data from the first ticket, and "pays for a pilot" in place of "wants a pilot".

**Can option D be confirmed?** Yes, on two conditions, both before any real personal or venture data goes in. One: the isolation test runs with one Paperclip per organization, the personal space included, in authenticated mode, with an agent told to try (RV-01). Two: the service is fixed for RV-02, RV-05, RV-06 and RV-07. If the first condition fails or proves too heavy to run, that is the case for E, and the permission service carries over unchanged.

## 2. Method and limits

| Step | What was done |
| --- | --- |
| Branch | Pull requests #4 and #5 were both open, so the work started from `docs/gate-g1a-route-b` (`ae9e034`), as the brief says. |
| Service | The unmodified `server.mjs` and `schema.sql` on a local PostgreSQL 16.15 with Node 22.23.4. The 35 existing tests pass there. R-02 used PostgreSQL 17; that difference was not tested. |
| New tests | 24 attack tests, 13 second-person tests, three measurements and a sweep of 19 deliberate breaks, in `spikes/r-02/review/`. Each test asserts what the contract or V-000 requires, so a failing test is a defect. |
| Raw results | R-02's result files were re-read with scripts, not re-run. |
| Paperclip | Not run. Its source was read at `v2026.1106.0` (documents and the gateway service) and at `da8cfda` (to re-check three ledger rows). |
| Desk research | 15 searches and one page fetch on 2026-11-17. Every web source except one was read as a search excerpt. |
| Third-party code run | PostgreSQL and the service's one dependency, the `pg` driver 8.23.1. Nothing else. |
| Model calls | None. |

Section 7 lists what could not be checked.

## 3. Findings, most severe first

**Blocker**: fix or decide before any real personal or venture data goes in, or, where it says so, before a second person is added. **Should fix**: fix before Phase 2 writes a specification from this spike. **Note**: record now, fix when the service is built for real.

### RV-01 — Blocker. The pass was measured on a layout R-02 says not to use, against an agent that never left the gateway

**Evidence.**

- R-02 defines option D as a Paperclip per organization, and its section 3 recommends one container per organization. The spike ran one Paperclip holding all four organizations as companies, in `local_trusted` mode, with every agent a child process of that one server under one operating-system user (`scratch/stages/all.sh`; `paperclip/harness.py`, `ensure_company`; E-111).
- Paperclip's own documentation for that mode: no authentication is required, and every request is treated as the board (E-114). The harness's approvals show it. `approve_action()` posts to Paperclip with no credential at all, and the result records `decidedByUserId: local-board`.
- Paperclip encrypts stored secrets with a master key kept in a file that only its own operating-system user can read (E-115). Its agents run as that user.
- The scripted agent always sent its run token and only ever called the gateway. `agent_probe.py` checks the names of environment variables. It never calls Paperclip without its token, never asks for another company's connection, and never opens Paperclip's files.
- These boundaries have failed in Paperclip before, in 2026 (RV-10).

**What follows.** C1 and C3 passed for calls through the gateway. Whether an agent with a shell can act as the board by leaving its token off, or read another company's stored token for the service, was not tested. Paperclip's documentation says the first is open in the mode the spike used. Read with E-111, it implies the second. The rows of C7 marked "verified working" for approvals, pause, kill, spend cap and the company boundary are true of an agent that keeps using its token.

**Reproduce.** Not run; this review may not run Paperclip. From any agent process in the spike's setup: the harness's own approval request (`POST /api/tool-gateway/action-requests/<id>/approve` with `{"companyId": ...}` and no `Authorization` header), and a read of the master key file under Paperclip's data directory.

**Smallest fix.** No code. Decide that option D means one Paperclip per organization, the personal space included, each under its own operating-system user or container, in authenticated mode with sign-up closed. Pull criterion 4 of the shared-venture spike forward, widen it to the personal space, and run it before real data goes in.

### RV-02 — Blocker. An agent in the holding organization can move any page it reads to every venture, with no human step

**Evidence.** A holding organization's agent may write a page with `visibility: global`, and every organization reads global pages. Nothing checks what the page contains or asks a human. The existing tests treat this as a feature (`test_holding_can_publish_a_global_page`). So the only thing that keeps a sibling's roadmap, or the approved personal briefing, away from the other ventures is the holding agent's prompt. N-03 says a prompt may not be that thing. Three tests fail (`RelayThroughTheHoldingAgent`), and a fourth with a friend's token.

**Reproduce**, with the fixture's tokens, each a `tools/call` on `POST /mcp`:

1. `test-token-mgmt-agent`: `brain_search {"query": "CANARY-SIBLING-1"}` returns the sibling's page.
2. `test-token-mgmt-agent`: `brain_write {"title": "relay", "body": "relayed: CANARY-SIBLING-1 confidential roadmap of the other venture.", "visibility": "global"}` returns an ID.
3. `test-token-toveli-agent`: `brain_search {"query": "confidential roadmap"}` returns one page, in organization `mgmt`, holding the sibling's text.

The same three calls move an approved briefing to a sub-organization. Switching briefings off afterwards hides the briefing page and not the copy.

**Smallest fix.** In the `pages_add` policy, require `visibility = 'org'` for agent and human tokens. Make a page global only through a pending request that the human approves, the same way `approve_briefing` works. A copy an agent writes inside its own organization cannot be prevented once agents may write; narrow contract rule 6 to say so.

### RV-03 — Blocker for a second person. The service has no person, and three rules assume there is only one

**Evidence.** Section 6 has the table. In short: a second personal space reads every organization (`schema.sql` line 154); `brain.holding_org()` picks the first holding organization by name, so with two of them every briefing goes to that one; a global page is global to the whole service; the personal switch, the briefing switch and `holding_reads` are one setting each for everybody. 8 of 13 tests fail.

**Reproduce.** `spikes/r-02/review/test_rev01_second_person.py`. The worst case, with a second holding organization named `acme`: Cole's personal agent calls `publish_briefing {"content": "CANARY-COLEBRIEF-1 ..."}`, the admin approves it, and `brain_search {"query": "CANARY-COLEBRIEF-1"}` finds it with `acme`'s token and not with `mgmt`'s.

**Smallest fix.** A `people` table and a `memberships` table. A personal space reads an organization only where a membership exists. A briefing names its target, which must be an organization its person belongs to. A global page is read only under the holding organization that published it. Each switch moves to the person or the organization it concerns. This is the identity work P-000 called the reason for a new repository.

### RV-04 — Blocker for health and finance pages. Paperclip stores the arguments of every call in clear

**Evidence.** R-02 matched five calls "by the request ID in the logged arguments". That works because Paperclip's audit events carry the call's arguments as text (`argumentsSummary.summary`), and its approval records do too (`canonicalArgumentsSummary.summary`). In `results/scratch/43798233669-1/new/checks-trace.json` the approval record for the write tagged `health` holds the page body, `CANARY-SENSITIVE-GW`, in clear. The service refused that write. Paperclip had already stored it. Search queries are stored the same way (E-118).

**What follows.** N-08 says health and finance data stay out of logs. Under option D a chief of staff that runs inside Paperclip sends every write and every search through a log that keeps the text. R-02 found the same for a printed secret (E-107) and did not draw the conclusion for N-08.

**Reproduce.** Read the file above and search for `CANARY-SENSITIVE-GW`. Whether Paperclip shortens long arguments was not checked.

**Smallest fix.** A design decision, not code: pages tagged health or finance are not written or searched through Paperclip's gateway. Either the personal agent reaches the service by a path Paperclip does not log, or those sections wait until R-05 and R-07 settle it. The build item "only Paperclip may reach the service" has to allow for this.

### RV-05 — Should fix. Every read slows down with the pages other organizations hold

**Evidence.** The policy calls `brain.can_read()` for every row a query touches, and that function runs three more queries. Measured for the Toveli agent listing its own four pages (`results/scale.txt`):

| Pages added to the sibling | Toveli's list | Holding organization's list |
| --- | --- | --- |
| 0 | 4.9 ms | 5.2 ms |
| 250 | 77 ms | 91 ms |
| 1,000 | 322 ms | 397 ms |
| 5,000 | 1,418 ms | 1,710 ms |
| 10,000 | 2,853 ms | 3,281 ms |

Toveli's map alone is 241 pages, which by this table costs every caller about 75 ms a call. Three consequences. The service is unusable at a few ventures with code maps. Any caller can measure how much every other organization holds, the personal space included, from its own latency. And any writer can slow the service for everyone.

**Reproduce.** `python3 measure.py scale`, or the test `test_a_callers_latency_does_not_depend_on_other_organizations_pages`.

**Smallest fix.** State the rule as column comparisons against values worked out once per statement. `spikes/r-02/review/fix-sketch-read-rule.sql` does this in about 40 lines: 8 ms at 10,000 pages, and the 35 existing tests still pass. It is a sketch for the build session, not a reviewed design.

### RV-06 — Should fix. A page that exists in another organization answers slower than a page that does not exist

**Evidence.** Contract rule 3 says a sibling's pages are not returned "and their existence is not revealed". The answer text is identical. The time is not: 513 microseconds slower by ID and 521 by path, over 1,000 interleaved samples each (95% intervals 434 to 576 and 442 to 594). Earlier runs gave between 0.4 and 0.57 ms. With 15 samples of each, a guess names the existing path correctly 97% of the time (`results/timing.txt`). IDs are random and cannot be guessed. Paths can: a venture's agent can learn which files exist in another venture's code map.

**Cause.** PostgreSQL runs the session lookup only when a row first needs it. A row of another organization triggers the lookup, about 0.7 ms in the database. No row, no lookup. The sketch for RV-05 does not close this (`results/fix-sketch.txt`).

**Reproduce.** With `test-token-toveli-agent`: time `brain_get {"path": "services/quant/run.py"}` against `brain_get {"path": "services/quant/rux.py"}`. Both return `{"error":"not_found"}`. Or `python3 measure.py timing`.

**Smallest fix.** Make the lookup run on every call whether or not a row matches. Two ways: `begin_session` stores the caller's readable organizations where the policy can compare them without a function call; or reads go through one database function that looks up the session first and the page second. Neither was built or tested here. This is measured with the caller on the same machine; through Paperclip it needs more samples, and a direct call needs few.

### RV-07 — Should fix. A crafted request leaves no row in the service's audit log

**Evidence.** Contract rule 10: every call, allowed or denied, is written. `request_id` is copied to the audit row without the check every other argument gets. A zero byte in it makes the audit insert fail. For a denied call the service logs "AUDIT WRITE FAILED" to its own output and answers as usual. Six such calls left zero audit rows, among them a refused read of a sibling's path, a refused briefing and a request for a tool that does not exist. Combined with RV-06, an agent can probe without a trace. An allowed call is different: its audit row commits with the action, so no read was returned without a row.

Two smaller faults in the same place. A tool name sent as a JSON array, `["brain_list"]`, runs `brain_list` and is logged as `{"brain_list"}`. The names `constructor`, `__proto__` and `toString` answer `internal_error` where any other unknown tool answers `invalid_arguments`.

Separately, a row records a hash of the arguments and nothing else. After an incident the log cannot say which page a call fetched.

**Reproduce.** With `test-token-toveli-agent`: `brain_get {"path": "services/quant/run.py", "request_id": "rev01\u0000nul"}`, then `GET /admin/audit`. No row. Tests: `AuditCompleteness`.

**Smallest fix.** Pass `request_id` through the same `clean()` as the other arguments. Refuse a tool name that is not a string, and look tools up with an own-property check. When the audit write of a denial fails, fail the call. Record the page ID or path a call asked for.

### RV-08 — Should fix. Criterion 4's count and its limits are understated

**Evidence**, from R-02's own result files (E-118):

- **31 requests, not 28.** The agents sent 28 planned tool calls and three retries of approved actions per pass. R-02 counts 28.
- **Four requests left no event in Paperclip's gateway audit, not one.** The unknown tool name, as R-02 says, and the three retries, each refused with `action_not_approved`. Those three named a tool that exists. The harness never put them through its matcher. In Paperclip's source at the pinned release, the code that raises that refusal writes no event at that point (E-117); its callers were not traced.
- **A call refused by a block rule is not in that log either.** In all five governance passes where a block rule refused a call with HTTP 403, the gateway audit for that company held 8 events with outcomes `allowed` and `unknown` only. Paperclip's other log, the company activity log, lists a `tool_gateway.call_denied` action. C4 was scored against the first log.
- **One check cannot fail.** "Every call that reached the service is in the service's audit log" is computed as `in_brain + pc_only == made`, and the code counts every call that is not in the service's log as "stopped by Paperclip". The numbers happen to be right (27 rows for 27 calls). The check proves nothing.
- **The join between the two logs is written by the agent.** The shared request ID is an argument the harness added. A real agent can leave it out or repeat another call's.

**Smallest fix.** Restate C4 as what was shown: every call that reached a tool is in both logs. Then test Paperclip's refusals against its activity log. In the service, record the request ID Paperclip itself puts on the outgoing request; whether Paperclip sends one was not checked.

### RV-09 — Should fix. Five rows of the governance table are stated more strongly than the evidence

Checked against all six `governance.json` files (E-118).

| Row in R-02 section 6.2 | What the files show |
| --- | --- |
| Spend cap per agent: "Verified working" | The agent was paused with reason `budget`. But the refusal of its next run reads "recorded usage has no reliable price", a different block, in every pass. After the cap was raised the agent still did not run (`ran_after_raise: false`). The cost was a made-up event posted through the API, not metered model spend. Shown: the cap trips. Not shown: that the cap is what refuses a run, that raising it releases the agent, or that real spend is counted. |
| Approval before a tool call acts | The flow works. The approval was given by a request with no credential (RV-01). Shown as a workflow, not as a control an agent cannot operate itself. |
| Approval before a new agent exists | Works when the company setting is on. It is off by default (E-08), and the harness switched it on and off with requests that carried no credential. |
| Pause or kill; organization to organization is zero by default | True for an agent that sends its run token. In the mode tested, a local request with no token is the board. |
| Audit log | The gateway's log misses three kinds of refused request (RV-08). |

The conclusion on trigger 3 stands: nothing this project needs sat behind the paid edition at either release. E-92 remains a stated intention to move policy controls there.

### RV-10 — Should fix. Neither report mentions Paperclip's 2026 security record

**Evidence** (E-116). Four advisories from 2026. All are reported fixed at or by `v2026.416.0` in April, though the public record is less clear for two of them. The releases the spike used are later.

- CVE-2026-41679, scored 10.0: on a network-reachable instance in authenticated mode with default settings, someone with no account could register, obtain a board key, import a company and run commands on the host. Open sign-up is the default and remained available after the fix.
- GHSA-x8hx-rhr2-9rf7, scored 9.6: in the default `local_trusted` mode, a web page the operator opened could reach the local service and do the same. The cause, as reported: the service took a request's network location for its identity.
- GHSA-xfqj-r5qw-8g4j, scored 8.3: data read across companies in authenticated mode.
- CVE-2026-41208: an agent could change its own configuration to run a command on the host.

**What follows.** R-01 passed over OpenClaw "on its 2026 security record" and did not look at Paperclip's. R-02 lists five things about Paperclip to design around and none is this. **Judgment:** these do not argue for E by themselves; a smaller system of our own would have its own faults and fewer people looking. They do settle three things. Paperclip's company boundary is not what separates organizations; our service is. Anything that must stay apart does not share a Paperclip instance. And a second person means authenticated mode on a reachable instance, which is the setting of the worst of the four.

**Smallest fix.** Add to R-02's section 9 a sixth trigger: an unfixed flaw in Paperclip's tenant or host boundary. Track its advisories. Close sign-up on any authenticated instance.

### RV-11 — Should fix. The 35 tests miss 10 of 19 deliberate breaks

R-02 reports two deliberate breaks, both noticed. `mutation_sweep.py` runs 19 (`results/mutation-sweep.txt`). The tests notice 9.

| Survived | What was weakened | Why the tests cannot see it |
| --- | --- | --- |
| M01 | The line that keeps personal pages from other callers | One personal space in the fixture. With two, this line is all that separates them. |
| M02 | A holding organization reads only its own children | One holding organization in the fixture. |
| M06, M07, M08 | An agent may add any kind of page, set a path, choose its provenance | The service sets these itself; no test tries the database rule behind it. |
| M11, M12, M13 | Who may publish a briefing, in what state, with the switch off | The service checks first. Contract rule 2 says the database also applies every filter. For briefings that is untested. |
| M16 | The audit log's append-only triggers | The tests try as a role with no rights on the table, so the triggers are never reached. |
| M18 | The application role may update and delete pages | No test tries. |

Also not covered: timing and latency; hostile input to the audit path; batches; more than one person, personal space or holding organization; the admin routes other than approval; token forms; what the database role learns with no session; anything on the host.

**Smallest fix.** Add the review's tests to the suite. Make the two-person, two-holding fixture the default one. Run the sweep whenever the schema changes.

### RV-12 — Should fix. Criterion 8: the map was built to the questions, and the reader it is kept for was never given a baseline

**Evidence.**

- The 20 questions were committed at 21:21 on 2026-11-15 and the mapper 28 minutes later, by the same session (`5d3ad72`, `5269900`). At least four extractions in `map_repo.py` mirror a question's wording: the package-manager pin and its file (Q01), the `.nvmrc` pin beside the `engines` range (Q02), `registerRootComponent` (Q13), the number of `CREATE TABLE` statements per migration (Q16).
- 13 of the 20 questions fall in the three categories the overview page was written to hold. The map-only agent's 26 of 26 on those measures that fit.
- No question asks what only a map knows cheaply: which files import a file, which tests cover it.
- All 20 are lookups with one or two source files, and 12 name a path or an identifier. In 233 files a search finds those at once.
- The grader gives full marks to an answer that lists several candidates. No saved answer used that.

**What stands.** The main result. The bias runs toward the map, and the plain agent still matched it. **Judgment:** a larger repository would plausibly change cost and time in the map's favour, since searching grows with the repository and a lookup does not. It would not plausibly change accuracy while the code is in reach (E-97, E-98).

**What does not stand.** "For that reader the map answered the structural questions correctly" should read "the questions it was built to answer". And the reader the map is kept for, the holding agent with no code access, has no baseline. The fair comparison is the holding agent asking the venture's agent, which can read the code. That was not run.

**Smallest fix.** Before more is built on the map: ten new questions written by someone who has not seen the mapper, half of them about importers and tests, and the delegation baseline.

### RV-13 — Should fix. R-01: the ranking picks the buyers its own product does least for

**Hypothesis verdicts.**

- **H-A1, "holds in part".** Its falsifier is a single product that covers the personal layer, a hierarchy and governed self-updating. No evidence about whether buyers need help can meet that, so "not falsified" says only that nobody sells the bundle. For the buyers ranked first, the evidence is low adoption (E-71), which fits "do not want it" as well as "cannot set it up". One of the E-71 figures, smaller organizations "flat at 22%", is from a consultancy survey whose definition of a smaller organization was not checked against a local business. Fairer verdict: true of self-hosting in general, untested for the ranked buyer.
- **H-A2, "the price is supported by quotes".** The sources are pricing guides, most of them written for people who run or want to start an agency (E-72, E-127). They are sellers' advice on what to charge. They are not quotes a buyer received. Other guides from the same search give wider ranges. And what is priced is one or two workflows, which R-01 itself says is not this product. R-01 names "small businesses are quoted real prices" as one of two reasons it moved toward Route A. It is a weak one.
- **H-A3, "partly falsified".** Fair. One gap: the search for "a second brain that respects permissions" covered company builders and memory components. It did not cover enterprise search and workspace products, where permission-aware retrieval across an organization is the core of what is sold. I did not research them either. R-04 should.
- **H-A4.** The first wording was falsified, and the restated one describes exactly what AZI Hub built. A claim narrowed until it survives is a description, not a test. Its reasoning, "owner and business are one principal", has its first counter-example in F-31: with two owners the personal layer becomes the liability R-01 says it is for employees.

**"AZI Hub already prototyped the part nobody sells."** R-01 rates AZI Hub "Yes" on tiers, the personal second brain and sharing on purpose. P-000 found that the tenant came from a header the client sets and that there was no user identity. The data model existed. The enforcement did not. This review shows the rebuilt version still assumes one person (RV-03). That was R-01's other reason for moving toward Route A.

**Customer ranking.** Rank 1 is non-technical owners of one existing small business. The table's criteria are size, need for help, who serves them, price points, fit of the personal layer and reach. It has no row for whether the buyer has the problem the product solves. A dentist has one business and no holding structure. Tiers, the thing this project owns, do nothing for them. What they buy is the agency's product, where this project has no advantage. The buyers who need tiers are owners of several ventures, which is the one empty cell in R-01's own 2x2 and is Cole's own profile. R-01 lists them under "later". Three further gaps: the size signal (32.0 million businesses with no employees) counts every business with no paid employee, and is then paired with a rate for employer businesses; the example users include dentists, who handle health records, and nothing covers what that requires; and the second column's price evidence is a personal agent's subscription (E-29).

**Judgment.** Re-rank owners of several ventures first. This matters now, not later: rule three of F-29 turns on five conversations, and with whom decides what a "yes" pulls the project toward.

**Ten ledger rows re-checked**: section 8.

### RV-14 — Should fix. The Gate G1a memo: one claim is wrong, one report went missing, one rule is too soft

- **"B can become A later because the code is the same."** Not as spiked. The service hard-codes one holding organization, one personal space, three kinds of organization, and one setting row for everyone (RV-03). That already breaks rule one of F-29 on tiers. Rule one says nothing about people, and rule two, the empty-organization test, would not catch a personal space that reads everything. P-000 gave identity as the reason for a new repository. Route B, built "only as far as Cole's own use needs", is where that gets skipped.
- **R-05 dropped out.** The memo's table lists R-05 under Route A only. P-000 says R-05 follows on either route. P-000's note of 2026-11-17 then folds its question of a person with memberships into the shared-venture spike. Nothing on Route B now owns approvals, the audit log or who the approver is. This review found faults in all three.
- **Rule three.** "Wants a pilot" is a conversation. P-000 says desk research never counts as validation, and R-01 says paying is the test.
- **The order of the first slice.** F-15a puts the personal layer first. That is the most sensitive data on the least tested part.
- **"D holds."** R-02's section 8 says in a Judgment that the spike answers "can D work". Its bottom line says "D holds" without that. C1 to C3 test our own service and would pass in front of any orchestrator. No E arm was run.

**Does anything argue against Route B?** No. Every finding here says the system is not ready for other people. The strongest argument against B is the project's own history, a platform built with one user and then left for months. Rule three exists to answer that, which is why it should be about money.

**Smallest fix.** A fourth rule in F-29: a person with memberships is in the schema from the first ticket, and a two-person, two-holding fixture runs on every change. Rule three becomes "pays for a pilot". R-05 goes back on Route B's list, in a light form.

### Notes

| ID | Note | Evidence and reproduction | Smallest fix |
| --- | --- | --- | --- |
| RV-15 | A briefing is approved blind and by nobody in particular. No route shows a pending briefing's text. The approver is free text and may be empty. A pending briefing can be approved while the personal space is switched off. A personal agent can put text from a health page into a briefing; only the human's approval stands in the way. | `BriefingApproval` (2 tests fail). `POST /admin/approve_briefing {"briefing_id": ..., "approver": ""}` returns 200. | Show the text before approval. Tie the approver to a signed-in person. Refuse approval while the personal space is off. |
| RV-16 | The admin token's length can be read without knowing the token. A wrong token of the right length that holds a byte above 0x7f gets HTTP 500; every other wrong token gets 401. | `GET /admin/audit` with `Authorization: Bearer ` followed by as many `0xE9` bytes as the token has characters (34 in the review's run) returns 500. Test `test_a_wrong_admin_token_is_always_answered_401`. | Compare hashes of the two tokens, which are always the same length. |
| RV-17 | Two undocumented token forms are accepted: an `X-Brain-Token` header, and `Authorization` with no `Bearer`. | `test_only_the_documented_header_form_carries_a_token`. | Accept `Authorization: Bearer` only. |
| RV-18 | `brain_get` by path returns the first organization by name. A reader of several organizations cannot ask for the other one's page at the same path, and whoever sorts first answers for all. | `PathLookupAcrossOrganizations`. Two ventures each with `README.md`; the holding agent can only ever get `alpha`'s. | Return every match with its organization, or take an organization the caller may read as an argument. |
| RV-19 | With the service's database password and no token, the role learns more than "nothing". `EXPLAIN ANALYZE` reports rows removed by the policy, which reveals the total page count and, through the path index, every path of every organization. The role can also write any audit row with no session. | `explain (analyze) select 1 from brain.pages where org_id = 'sibling' and path = 'services/quant/run.py'` shows `Rows Removed by Filter: 1`; a path that does not exist shows none. Two tests fail. | Treat the database password as a secret agents never hold. Refuse `audit_log` without a bound session. R-02's phrase "the database refusing the application role" should read "returns no rows". |
| RV-20 | R-02 lists as unverified whether a plan bought in an app store can claim the API credit. The page R-02 cites for E-76 says it can, claimed on claude.ai in a browser (E-121). The rest of the E-26 correction and the budget arithmetic re-derive correctly. | Section 8. | Cole claims the credit. |
| RV-21 | The mapper copies each file's leading comment, package scripts and workflow commands into pages that the holding agent and the personal agent read. Nothing scans that text for secrets, and anyone who can commit to a venture's repository writes into those pages. | `mapper/map_repo.py`, `purpose_of` and the workflow parser. Not exercised. | A secret scan before pages are written. Treat map pages from a shared venture as untrusted text. |

**What held.** Nine attack tests pass. The session binding held against temporary tables that shadow the service's own, a changed search path, savepoints, `COPY`, `RETURNING` and views. 800 interleaved calls from four organizations never crossed. An agent cannot forge a page's kind, path, owner or provenance. Every admin route refuses every agent and human token. The holding organization in summaries mode cannot reach a note by ID or path. A briefing cannot be approved twice.

## 4. Per criterion

| # | Criterion | R-02 | This review | Why |
| --- | --- | --- | --- | --- |
| 1 | A sub-organization's agent gets its own and global pages only | Pass | **Stands with changes** | Holds for every direct call tried. Change the statement to "through the gateway" (RV-01). "Global" has to mean approved by a human (RV-02). Existence and volume leak by timing (RV-05, RV-06). |
| 2 | The holding organization reads its sub-organizations | Pass | **Stands** | Summaries mode also held by ID and path. Not run through Paperclip, as R-02 says. |
| 3 | The only path from personal to an organization is an explicit push | Pass | **Stands with changes** | The push works as built. An agent can then carry the briefing on to every venture, and the off switch does not reach the copy (RV-02). Health text reached Paperclip's records (RV-04). Approval is blind (RV-15). |
| 4 | Every call is in both audit logs | Pass, with two limits | **Stands with changes** | True as "every call that reached a tool". Not true of every request: four of 31 are missing from the log that was scored, in two kinds, and a third kind is in a different log (RV-08). The service's own log can be evaded (RV-07). Cole's ruling of 2026-11-16 accepted two limits; there are more. |
| 5 | One real Toveli task through the stack, and on one agent | Not run on Toveli | **Not run. The stand-in does not test N-04** | Both arms were one agent writing one function. The only difference was where five lines of conventions came from. "One agent matched the full stack" compares one agent with one agent. It says nothing for or against orchestration. |
| 6 | Paperclip upgraded one release without touching the service | Pass | **Stands** | The files agree. Not covered: going back after 41 migrations, an upgrade with a run in flight, several instances. |
| 7 | Governance coverage; trigger 3 | Done; not met | **Stands with changes** | Trigger 3: agreed. Five rows overstated (RV-09). |
| 8 | Codebase map against a plain agent | Plain agent matched | **Stands with changes** | Main result stands and is stronger than stated. The map-only claim does not generalize, and its reader has no baseline (RV-12). |

## 5. Alternatives R-01 did not compare

Desk research only, from search excerpts, as the brief asks. Nothing was installed. The deep comparison waits until the tool runs.

| Alternative | What it is | Against R-01's capability map | Against R-02's criteria | Obviously beats D? |
| --- | --- | --- | --- | --- |
| **LangGraph** (E-122) | A library, MIT. Agents as graphs, with checkpoints in SQLite or Postgres, pauses for human review, and a memory store. Hosted deployment is LangSmith: $39 a seat a month, cloud only; self-hosting it needs the Enterprise plan. | Covers approval pauses (C-06), model choice (C-14), self-hosting of the library (C-15). A memory primitive, no tiers (C-02). No org chart, budgets, interface or company boundary (C-03, C-05, C-18). | C1 to C3 depend on our service, not on the orchestrator. C4 would be met in full, since we would write the log line. C7: approvals free; an audit interface and access control are the paid part or ours. | **No.** Less to trust and more to build. |
| **CrewAI** (E-123) | A library, MIT, built around agents in roles. The hosted platform has a free tier of 50 runs a month and a custom-priced Enterprise tier with self-hosting, single sign-on and access control. | Roles and crews (C-05). Human review for flows (C-06, part). No audit log or access control in the free library (C-07, C-17). No tiers, personal layer or budgets. | As LangGraph. More of governance sits in the paid tier than with Paperclip today. | **No.** |
| **Microsoft Agent Framework** (E-124) | A library, MIT, version 1.0 since 2026-04-03, successor to AutoGen and Semantic Kernel. Workflows with checkpoints, approval before a tool runs, MCP and A2A, connectors for Claude and others. Identity and governance come from Microsoft's cloud. | Orchestration patterns (C-05), approvals (C-06), model choice (C-14), library self-hosting (C-15). Identity only through Entra (C-16). No tiers, budgets or interface. | As LangGraph. Its governance story assumes Azure, which F-17 does not. | **No.** |
| **Agent fabric and agent mesh products** (E-125) | MuleSoft Agent Fabric: a control plane that registers, routes, governs and cost-caps agents built elsewhere, from $2,000 a month. Solace Agent Mesh: an Apache-2.0 framework in which agents talk over Solace's event broker. Agent 365 is in R-01. | Governance over agents that already exist (C-06, C-07, C-17, C-18), sold to integration teams of large organizations. Nothing on a personal layer, a holding structure or a second brain. Not self-hosted for one owner. | Not comparable: they govern, they do not run an organization of agents on a VPS. | **No.** A later connection point for the large-organization group, not a base. |

**None obviously beats option D** for what Route B wants: something usable soon with little of our own to maintain. Only Paperclip ships the org chart, heartbeats, an approvals inbox, budgets and an interface for free.

**The best case for E**, argued as its advocate:

1. **The question changed and was not asked again.** R-01 chose D for a product, where Paperclip's breadth and interface help a sale. Route B has one user. Section 8 of R-02 was written before the gate.
2. **D as it must be run is not D as tested.** One Paperclip per organization means several installs, several upgrades (the two releases the spike used are 14 days apart), several interfaces and no single view across them (RV-01). The single view was a large part of the appeal.
3. **Orchestration has not shown value.** The one task run both ways had one agent on each side (C5). The org chart, delegation and heartbeats were never exercised on real work.
4. **The security surface.** About 1.5 million lines of someone else's code with four serious advisories this year (RV-10), against a few thousand lines of our own on top of a library. AZI Hub's whole server was 13,500.
5. **E got cheaper.** R-01 sized E as rebuilding AZI Hub's runtime. Durable runs, approval pauses and checkpoints are now library features under MIT licences (E-122, E-124), and the Agent SDK supplies the loop.
6. **Audit.** Under E the audit log is ours and C4 can be met as written.

**Against that.** The interface is the expensive part, and E starts with none. Cole wants to use the tool soon (F-30). The service is the same under both, so choosing D now costs little if it is wrong.

**Judgment.** D stays the working choice. E is closer than R-02 makes it look, and two facts will decide it: what one Paperclip per organization costs to run, and which parts of Paperclip Cole actually uses after two weeks. If that list is short, E on a library is a small system.

## 6. A second person (V-000 F-31)

The service only. Paperclip was not run. The friend is modelled the only way the service allows today, in three steps: A, a human token of the shared venture; B, the friend also has a personal space; C, the friend also runs a company in the same service.

**Who reads whose pages** (`results/second-person-matrix.txt`). Columns are whose made-up pages.

| Token | Shared venture | Cole's global page | Toveli | Sibling | Holding | Cole personal | Friend personal | Friend's company | Friend's global page |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Friend, human, shared venture | reads | reads | no | no | no | no | no | no | **reads** |
| Shared venture's agent | reads | reads | no | no | no | no | no | no | **reads** |
| Friend's personal space | reads | reads | **reads** | **reads** | **reads** | no | reads | reads | reads |
| Cole's personal space | reads | reads | reads | reads | reads | reads | no | **reads** | **reads** |
| Cole's holding agent | reads | reads | reads | reads | reads | no | no | no | **reads** |
| Toveli's agent | no | reads | reads | no | no | no | no | no | **reads** |
| Friend's company agent | no | **reads** | no | no | no | no | no | reads | reads |

Bold marks a read F-31 forbids, or a page that crosses from one person's holding organization to the other's.

**Step A. What a human token of one sub-organization can and cannot do.**

- It reads the shared venture's pages and global pages. It cannot read Toveli, the sibling, a holding-only page or anything personal: not by list, search, ID or path. Holds.
- It writes notes and summaries in the shared venture, labelled as written by a human. It cannot publish a briefing or a global page, approve anything, or read any audit row, its own venture's included. Holds.
- A human token is an agent token with a different label. Nothing ties it to a person. One person in two ventures is two unrelated tokens. Removing a person means finding every token.
- The holding agent can hand the friend any page it reads (RV-02). Fails.
- Everything the friend writes is read at once by Cole's holding agent and personal agent. There is no switch for one venture: `holding_reads` is one setting for all (criterion 6 of the shared-venture spike). Fails.

**Step B. What breaks when a second personal space exists.**

- The two personal spaces cannot read each other. Holds, by one line that no existing test covers (RV-11, M01).
- The friend's personal space reads Cole's holding organization and every one of his ventures. Fails.
- Switching the friend's personal space off switches Cole's off. Fails.

**Step C. What breaks when a second holding organization exists.**

- Each holding organization reads only its own ventures. Holds.
- Cole's personal space reads the friend's company. Fails.
- A global page crosses to the other company in both directions. Fails.
- Cole's approved personal briefing is delivered to the friend's company, because it sorts first by name. The admin who approves sees neither the text nor the destination. Fails.

**The seven pass criteria of the shared-venture spike: what they miss.**

1. **The relay.** Criterion 2 allows "global pages". As built, that is whatever an agent in the holding organization chooses to publish. Add: no page becomes readable by the shared venture without a human decision recorded in the service.
2. **The other direction.** Nothing covers what Cole's agents read from the shared venture. The friend's notes and the code map built from the friend's commits reach the holding and personal agents as instructions they might follow. Add a test: a page in the shared venture tells the holding agent to publish a holding page, and nothing leaks.
3. **Briefing routing.** Criterion 3 covers reads. Add: a person's briefing can go only to an organization that person belongs to and names.
4. **Who approves.** Approval is one admin token. Add: approvals are per person and per organization, the approver is the signed-in person, and neither an agent nor the other person can approve in their place.
5. **The friend is not protected from Cole.** All seven criteria guard Cole. Cole operates the database, holds the admin token and administers Paperclip, so he can read the friend's personal space. Criterion 3 puts two personal spaces in a service one of the two people runs. Either the friend's personal space lives in the friend's own deployment, or the friend accepts that in writing.
6. **Audit for both.** "Logged on both sides" covers pushes only. Add: each person can read the audit rows of the organizations they belong to, including each time the holding organization read the venture.
7. **Leaving.** Nothing tests removal: every token, login and repository right of the friend stops working, and it is settled who keeps the venture's pages.
8. **Side channels and load.** Timing and volume (RV-05, RV-06). The friend can also slow Cole's service by writing pages. Add a quota and a latency check.
9. **Paperclip's mode.** Criterion 1 needs logins, which means authenticated mode on a reachable instance. Add: sign-up is closed, a request with no credential is refused, and an agent cannot approve its own request by leaving its token off (RV-01, RV-10).
10. **Keys and spend.** Whose model key the shared venture's agents use. Cole's plan cannot be shared (E-78). Add: its own API key and its own cap.
11. **Tests that bite.** Require that each criterion's test fails when its rule is removed (RV-11).

**Where this leaves the spike's own rule.** P-000 says: if criterion 2 or 3 fails, no second person is added until the service is fixed. Criterion 3 fails today, at the service, without Paperclip. So that half of the spike is already answered.

**Judgment.** No second person until RV-02 and RV-03 are fixed. A shared venture gets its own Paperclip instance by default, without waiting for a test to fail in a shared one.

## 7. What I could not check, and why

| Not checked | Why |
| --- | --- |
| Anything about Paperclip at run time: whether an agent can act as the board, read another company's stored token or approve its own request; whether refused retries and unknown tools are in the activity log; whether argument text is shortened; whether Paperclip sends its own request ID to the service | The brief forbids running Paperclip. RV-01, RV-04 and RV-08 rest on its documentation, its source and R-02's result files. |
| The service on PostgreSQL 17 | Only 16.15 was available. |
| Timing through Paperclip or over a network | Measured on one machine, caller and service together. |
| Any fix beyond the read-rule sketch | The brief forbids changing the service. The other fixes are proposals. |
| A re-run of criterion 8 or criterion 5 | No model calls; spend cap $0. |
| The six runs on the scratch machine | They cannot be repeated from here. Their saved output was re-read. |
| R-02's jail and its 15 probes | Not re-run. |
| Anthropic's API list prices (E-77) | The pricing page did not come back from search and could not be fetched. Plan prices and credits were confirmed from other pages. |
| The consultancy and bank figures in E-71, and E-42 | Not reached in the time. The ledger rows not listed in section 8 were not re-checked. |
| Enterprise search and workspace products as sellers of a permission-aware second brain | Named in RV-13 from general knowledge. Not researched. |
| Whether the tests run on every change | The repository has no CI yet. |

## 8. The E-26 correction, the budget, and ten ledger rows

**E-26 and the budget.** Re-derived from the help article behind E-75 and the documentation page behind E-76.

- The article still carries both notices: the change to Agent SDK billing was paused on 15 June, and since 7 October use while signed in with a plan still draws on the plan's limits. E-75 is right, and so is striking E-26.
- The credit amounts, what they cover and how they are claimed match E-76.
- One line was missed. The same page says plans bought through the iOS or Android app are eligible, with the claim made on claude.ai in a browser (E-121). R-02 lists this as unverified.
- The Max plan's help page says its $100 is the web price and that mobile prices vary. That fits R-02's reading that $249 is an app-store price. Which plan Cole holds is still his to check.
- Arithmetic: $1.34 and $0.34 make $1.68. The per-question costs follow from the token counts at the stated prices. $1,000 buys 100,000 one-cent questions.

**Ledger rows re-checked.**

| Row | Claim | Result |
| --- | --- | --- |
| E-03 | Paperclip's companies are flat | **Holds.** `companies.ts` at `da8cfda` has no parent, group or holding column. |
| E-50 | 169 of 189 schema files reference a company; the authorization service is 3,172 lines | **Holds exactly.** |
| E-73 | About 1.5 million lines in about 5,600 files; 486 migrations; 12 adapters | **Holds.** My count: 1,533,101 lines in 5,698 files. The interface is 424,000 lines by my filter against 404,000 in the row (E-126). |
| E-27, E-28 | Duet: research preview from 2026-10-21 by waitlist; no Team or Enterprise plans | **Holds.** Several sources agree. |
| E-39 | Survey of 5,067 US adults: agent users gave access to health apps (23%) and financial accounts (20%) | **Holds** for the figures found. The 41% and 92% figures were not in the excerpts. |
| E-63 | Polsia: about 10% of companies made a dollar; about 50% left in month one | **Holds.** The founder also put the second month at about 50%, which R-01 does not carry. |
| E-69 | 180 configurations; plus 81% on a parallel task; minus 39% to 70% on a sequential one | **Holds.** |
| E-71 | 24.6% of employer businesses used AI in the period to 2026-10-18; 19.8% in May | **Holds** for the Census figures. The question was widened in November 2025; both figures are after that. The other two figures in the row were not checked. |
| E-72 | Agencies quote $1,500 to $5,000 setup and $500 to $1,500 a month | **Holds as a range found in guides.** They are sellers' pricing guides, and other guides give wider ranges (E-127). See RV-13. |
| E-75, E-76 | The correction to E-26 and the API credits | **Hold.** One line missed (E-121). |
| E-88 | Tag `v2026.1106.0` is `d69631b` | **Holds.** |

## 9. Decisions for Cole

1. **Option D.** Confirm it on the two conditions in section 1, or hold it until the isolation test has run.
2. **What "per organization" means.** One Paperclip per organization, each under its own operating-system user or container? I recommend yes for the personal space and for any shared venture at the least. The cost is several installs, several upgrades and no single view.
3. **Criterion 4.** Accept it as "every call that reached a tool is in both logs", knowing Paperclip does not log every refusal, or call it a fail.
4. **Order of the first slice.** Ventures before the personal layer, so health and finance pages arrive after the fixes and the isolation test? F-15a says personal first.
5. **Health and finance pages and Paperclip's logs** (RV-04). Keep those sections out of Paperclip until R-05 and R-07 say how.
6. **F-29.** Add the fourth rule on people. Change rule three to "pays for a pilot". Decide who the five conversations are with; I suggest at least three owners of more than one venture.
7. **R-05.** Put it back on Route B's list in a light form.
8. **The customer ranking** (V-000 D-10a). Keep it, or put owners of several ventures first.
9. **Housekeeping.** Claim the API credit: app-store plans are eligible. R-02's items on the throwaway key and the scratch repository still stand.

## Sources

Ledger rows E-114 to E-127, added with this review. Tests, measurements and raw output: `spikes/r-02/review/`. R-02's result files: `spikes/r-02/results/`. Paperclip source: `paperclipai/paperclip` at tag `v2026.1106.0` (`d69631b01b9c658f80bf8bed389863dce82643e1`) and at `da8cfda42e499e0c3a5206ef44b7d67407022585`. Web sources were gathered on 2026-11-17; all but one were read as search excerpts.
