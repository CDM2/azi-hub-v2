# REV-01 fix pass: the permission service after the review

Version 1.0, 2026-11-18. Proposed; accepted when its pull request is merged. Written by the session that wrote the review `REV-01_R-01_AND_R-02.md`, on Cole's instruction of 2026-11-17 ("start the fix pass"; "the amount of new tests and second person tests that are failing is something we need to resolve"). A fix written and tested by one session has not been attacked by another. Section 8 says what was not checked.

The fixed service is under `spikes/rev-01-fix/`. Nothing under `spikes/r-02/` was changed. Paperclip was not installed or run. Made-up data only. No model was called.

## 1. Result

1. **The 23 failing review tests are resolved.** 21 pass with their original assertions intact. 1 passes after its assertion was corrected, because the review had Cole's rule wrong. 1 is kept failing on purpose, because no code can make it pass; a narrower test of what code can enforce was added and passes.
2. **All 104 tests run: 101 pass and 3 are known limits kept failing on purpose** (section 7). The 104 are R-02's 35, the review's 37, 3 added beside them and 29 new ones for the rules this pass added.
3. **Of 70 deliberate breaks of the fixed service, the tests notice 66. The other 4 each remove one of two locks on the same rule, and the tests notice when both are removed.** The review ran 19 breaks against R-02's tests and 10 went unnoticed (RV-11).
4. **This meets condition two of F-32, as far as the session that built it can say.** Condition one, the isolation test with one Paperclip per organization, is untouched and still open. No real data should go in on the strength of this pass alone.
5. **Building the fix introduced two new problems, both found and closed before this report** (section 6), and the first three runs of the sweep each found a gap in the tests (section 5). They are stated because a fix that needed fixing is a reason for the separate review in section 9.

## 2. What happened to each finding

Finding numbers are the review's. "Fixed" means a test that failed now passes, or a measurement that showed the problem no longer does.

| Finding | Status | What shows it |
| --- | --- | --- |
| RV-01 the tested layout is not the recommended one | **Not in this pass.** Needs Paperclip running. | Open item, V-000 section 6 |
| RV-02 an agent relays pages through a global page | **Fixed.** An agent's global page is read only inside its own organization until a person who controls that organization approves it. | 3 review tests pass, and a fourth is known limit 1 in section 7; `GlobalPagesNeedAPerson` (3 tests) |
| RV-03 the service has no person | **Fixed.** People and memberships are data. A personal space reads what its person belongs to. Each venture sets what the layer above reads; the default for a venture with a second person is nothing. Each person has their own switches. A push names its target. | 7 review tests; `Switches` (6), `Pushes` (8), `ReportsUpward` (2) |
| RV-04 Paperclip keeps call arguments as text | **Not in this pass.** It is about what Paperclip stores. | Open item, V-000 section 6 |
| RV-05 reads slow down as other organizations grow | **Fixed.** One venture's list: 3.1 ms with no other pages, 2.9 ms after another venture gained 10,000. Against R-02: 4.9 ms and 2,853 ms. | `results/scale.txt`; 2 tests |
| RV-06 a forbidden page answers slower than a missing one | **Fixed.** Inside the database the difference is under 0.3 microseconds in six runs of 20,000 lookups each way. On R-02's schema the same measurement gives about 240. Over HTTP the difference is inside the noise (11 and -13 microseconds, intervals spanning zero) and a guess from the timing is right 46 to 48% of the time, where a coin toss is 50%. | `results/timing-in-database.txt`, `results/timing.txt`; 3 tests |
| RV-07 calls that leave no log row | **Fixed.** A request id that cannot be stored as sent is refused and logged. A tool name must be a string naming a tool. A refusal that cannot be logged fails the call. | 3 review tests; `TheLog` (5) |
| RV-08 criterion 4 undercounted | **Half fixed.** This service's half: every message is one row, including messages that are not tool calls; the row for a read lists the pages returned; operator actions are rows. The other half compares against Paperclip's log and needs Paperclip. | `TheLog.test_every_message_leaves_exactly_one_row` |
| RV-09 to RV-14 | **Not in this pass.** Findings about the reports and the gate memo. Cole ruled on parts of RV-13 and RV-14 (F-35, F-36, F-39, F-40). | V-000 section 2a |
| RV-15 approval was blind, unnamed, and possible with the personal space off | **Fixed.** The person sees the text first. Only that person can approve, with their own token; an agent cannot. The operator route must name a person who has the authority. Nothing is approved while a switch is off. A push's text cannot change after it is written. | 2 review tests; `Pushes` (8) |
| RV-16 the admin token's length could be learned | **Fixed.** Compared as hashes; a wrong token is always answered 401. | 1 review test |
| RV-17 undocumented ways to send a token | **Fixed.** One form only. | 1 review test |
| RV-18 a path lookup could not say which organization | **Fixed.** `org` narrows a lookup, and the answer says which other readable organizations hold the same path. | 1 review test; `PathLookup` |
| RV-19 what the database login learns without a token | **Fixed, with two limits left** (section 7). The login cannot query a table, read a plan, or write a log row without a session. | 2 review tests; `test_criteria_1_3` database class |
| RV-20, RV-21 | **Not in this pass.** Not about this service. | |

## 3. What changed in the design

The contract is `spikes/rev-01-fix/service/CONTRACT.md`. Each changed rule is marked there with the finding that caused it. The five changes that matter:

1. **The database login cannot touch a table.** In R-02 it could select from the pages table and row-level security filtered the rows. Now it can call fourteen functions and nothing else. This is still N-03: deterministic code in the database decides. It is a different mechanism from the one R-01 and R-02 describe, and both reports say "row-level security" where this service now says "functions". Row-level security stays switched on with no policy for the login, so a grant made by mistake returns nothing.
2. **People are data.** A person, a personal space, memberships with a role of owner or member. Who reads what and who may approve what follow from them. This is the fourth Route B rule (F-35).
3. **A person approves, as a person.** An agent's token cannot approve anything, including the agent of the same personal space. A person's token can. The push is frozen once written, shown in full to the person, and decided once.
4. **One log, written by the database.** The function that returns pages writes the row in the same transaction. Operator actions are rows in the same log. Each row carries a hash of the row before it, so a row changed or removed by someone who can switch the triggers off is still detected.
5. **Text can leave in two more ways, both by approval.** A personal space can push to any organization its person belongs to, not only the holding organization (F-34). A venture can send a report to the organization above, which is the only way anything leaves a venture whose parent reads nothing.

## 4. The tests, and every assertion that changed

`spikes/rev-01-fix/CHANGED_ASSERTIONS.md` lists each one with the reason. In short:

| File | Tests | Against R-02 | Against the fixed service |
| --- | --- | --- | --- |
| R-02's own (`test_criteria_1_3.py`) | 35 | 35 pass | 35 pass. 29 unchanged, 6 changed. |
| The review's attacks | 24, now 27 | 9 pass, 15 fail | 26 pass, 1 known limit. 18 unchanged, 6 changed, 3 added. |
| The review's second-person tests | 13 | 5 pass, 8 fail | 13 pass. 12 unchanged, 1 changed. |
| New rules | 29 | did not exist | 27 pass, 2 known limits. |

On 2026-11-17 the session told Cole that done meant all 72 existing tests passing. That was too strong, and he was told so before the work started. Four things had to change:

- **One review test had the rule wrong.** It required that Cole's personal agent not read a venture he co-owns. His rule is that the personal space reads everything he belongs to. The assertion was corrected.
- **One review test demands what no code can do.** It requires that switching briefings off removes the text from a copy an agent already wrote down. It is kept as written and marked as an expected failure.
- **One R-02 test asserted the hole.** It required an agent's global page to be readable by every venture at once. That is RV-02. It now requires the opposite until a person approves.
- **Five R-02 tests and three review tests selected from the table directly.** The login can no longer do that, so they ask the same questions through the functions, and now also require the direct select to be refused. Two more review tests kept their assertions and gained one each.

## 5. Deliberate breaks

`spikes/rev-01-fix/mutation_sweep.py`; raw output in `results/mutation-sweep.txt`. 58 breaks of the schema and 12 of the server, one at a time, each run against all 104 tests.

**Final run: 70 breaks, 66 noticed, 4 with no effect as expected, none unnoticed.** No run had to be repeated for timing noise.

The 4 with no effect (N01, N50, N54, N55) are breaks where a second lock holds. N01 removes the read rule's own line about personal spaces; the session's scope never contains another personal space anyway. N50, N54 and N55 grant the database login a function it should not have; each runs with the caller's rights, and the caller has none on any table. For each of the four there is a break that removes both locks (N03, N57, N58, N56), and the tests notice all of those.

The sweep was run four times, and each of the first three changed the tests:

- **Run 1** (68 breaks; `results/mutation-sweep-run-1.txt`): 64 noticed, 2 with no effect as expected, 2 unnoticed (N50, N54). Both unnoticed breaks were harmless for the reason above. Checking them showed a real gap all the same: no test called the operator's approval function on a real pending push. Had that function been written to run with the owner's rights, the database login could have approved any push in any person's name and every test would have passed. A test was added (`Pushes.test_the_database_login_cannot_decide_a_push_or_a_page_through_any_function`), with two harder breaks, N57 and N58. N58 fails that test and no other.
- **Run 2** (70 breaks; `results/mutation-sweep-run-2.txt`): 65 noticed, 4 with no effect as expected, 1 unnoticed (N24, the fence). The test for the fence passed without the fence. The test was changed to measure under the conditions in which a missing fence does its damage; without the fence it then reads 446 ms against 4 ms.
- **Run 3** (stopped after 30 breaks; `results/mutation-sweep-run-3-stopped.txt`): N24 was noticed, and N25, the scan setting, was not, although runs 1 and 2 had noticed it. Whether the test caught it depended on which kind of plan PostgreSQL happened to be using (section 6). The test was changed to force the unfavourable kind. The scan setting was also taken off the page lookup, where no test showed a need for it: that lookup uses the index in both kinds of plan.
- **Run 4** is the final run above, from a clean checkout, with the service and tests as committed. Before it, the two breaks whose result had varied (N24, N25) were run three more times each and were noticed every time.

What the sweep does not show: that the 70 breaks are the ones that matter. They were chosen by the session that wrote the rules.

## 6. Two problems the fix introduced, and how they were closed

Moving the read rule from row-level security into functions removed a protection that PostgreSQL gave for free: with row-level security, the database applies the rule before it lets a query's own conditions look at a row. In a function, the planner is free to reorder.

1. **Search text was tried against other organizations' pages.** In the first version of the search function PostgreSQL evaluated the text match before the read rule, because the match looked cheaper. No page leaked, but one venture's search took 3.5 ms before and 216 ms after another venture stored 24 million characters, and how long it took depended on what those pages said. Closed with a fence (`offset 0`) that forces the rule to run first.
2. **Lists and searches still slowed down as other organizations grew.** PostgreSQL scanned the whole table: one venture's list went from 3.9 ms to 18.9 ms when another gained 20,000 pages. Far better than R-02's 2,853 ms and still the same finding. Closed by switching sequential scans off inside the list and search functions, so that they walk the index from the caller's own organizations.

The figures in these two items were measured while building and are not in `results/`. The sweep's mutants N24 and N25 put the service back into each state, and the two tests in `OtherOrganizationsPagesCostNothing` then fail.

Both closures are settings a later edit could remove without noticing. Each has a comment in `schema.sql`, a test, and a mutant in the sweep.

One more thing came out of this. PostgreSQL plans a statement afresh the first five times a connection runs it, looking at the caller's actual values, and may then keep one plan made without looking at them. Both problems show only under the kept plan. So each of the two tests passed without its protection until it was made to force that kind of plan (section 5). `run.sh` also runs all 104 tests with each kind forced: both runs pass (`results/tests-all-force_generic_plan.txt`, `results/tests-all-force_custom_plan.txt`).

## 7. What this pass does not close

Three are tests kept failing on purpose, so they show in every run:

1. **A copy an agent made of a briefing stays.** Switching briefings off hides the page the service delivered, for every caller. It cannot find text an agent wrote down while the briefing was readable. The log names every caller that was handed the page.
2. **The database login can ask how large the pages table is.** PostgreSQL allows that to any login. It needs the database password, not a token. One database per customer removes it.
3. **Someone with the database password and a valid token can read and then roll back, leaving no log row.** A token alone cannot: the service commits before it answers. Closing it means writing the row first in a transaction of its own, one more transaction per call.

Others:

4. **A parent reading only summaries can tell by timing, between 0.8 and 1.6 microseconds, whether an id belongs to some page of its own venture.** It learns nothing about an organization it does not read. Measured in `results/timing-in-database.txt`.
5. **The log is tamper-evident, not tamper-proof.** A database superuser can still remove the whole log.
6. **Text a second person writes in a shared venture reaches the other owner's personal agent**, which is the agent that can read that owner's health and finance pages. The page says who wrote it, and nothing leaves the personal space without the person's approval. Nothing stops the agent from being influenced by what it reads. This follows from Cole's rule that the personal space reads everything, and he should know it does.
7. **No rollback.** F-38 asks for steps to be rolled back. This pass built the append-only log and nothing that blocks rollback; pages are still updated in place by the code mapper.
8. **No task is created in the receiving organization's Paperclip when a push is approved.** The push lands as a page. Whether and how it becomes work for that organization's agents needs Paperclip.
9. **A caller with no valid token can fill the log.** Every refused token is a row, and there is no rate limit. This was true of R-02 as well. A limit belongs in front of the service.

## 8. Not checked

- Anything with Paperclip running: the isolation test (RV-01), what Paperclip stores of a push or a page (RV-04), the cross-check of the two logs (RV-08), R-02's criteria 4 to 8 against the fixed service. R-02's harness under `spikes/r-02/paperclip/` was not run against it.
- The fixed service by a session that did not write it.
- PostgreSQL other than 16.15. The fence and the scan setting depend on planner behaviour, which can differ between versions.
- The planner's own statistics as a side channel. When PostgreSQL plans with a caller's actual values it consults statistics gathered over every organization's rows. No effect was seen; none was looked for beyond the timing tests.
- Timing over a real network. The measurements are on one machine.
- Load: the log takes one lock per row, so writes queue. Throughput was not measured.
- A venture nested more than one level below a holding organization. The rules are written for any depth; the tests use one level.
- The mapper (`spikes/r-02/mapper/`) against the fixed service. Its write path, `/admin/codebase_sync`, is unchanged apart from a log row.

## 9. Decisions for Cole

1. **Have a separate session attack this fix**, as REV-01 attacked R-02, before condition two of F-32 is called met. The session recommends it. This pass changed the mechanism the whole permission claim rests on. Section 6 shows the builder missed two things on the first try, and section 5 that the builder's tests missed three more.
2. **One owner or both?** A report leaving a venture two people own is approved by either owner. Requiring both is a small change. Built: either.
3. **The operator's approval routes.** They let whoever holds the admin token record an approval in a named person's name. Kept so R-02's tests still run; logged as the operator's action. In a product they should go or need their own rule.
4. **A second person's text reaches your personal agent** (section 7, item 6). Accept, or have the personal agent read shared ventures only on request.
5. **Amend R-01 and R-02 where they say "row-level security"?** They are accepted or proposed as written. The session recommends a note in each when the fix is accepted, not a rewrite.
6. **The isolation test** needs Paperclip on a scratch machine, outside this sandbox. It is the remaining condition of F-32.
