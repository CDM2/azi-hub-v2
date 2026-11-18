# Every assertion that changed in the fix pass

The fix pass copied 72 existing tests into `tests/` and ran them against the fixed service. This file lists every test whose assertions are not exactly what they were, with the reason. A test not listed here asserts exactly what it asserted before. The originals are untouched under `spikes/r-02/tests/` and `spikes/r-02/review/`; `diff` shows the same thing this file says.

## Summary

| File | Tests | Against the R-02 service | Against the fixed service |
| --- | --- | --- | --- |
| `test_criteria_1_3.py` (R-02's own) | 35 | 35 pass | 35 pass. 29 unchanged, 6 changed. |
| `test_rev01_attacks.py` (the review's) | 24, now 27 | 9 pass, 15 fail | 26 pass, 1 kept failing on purpose. 18 unchanged, 6 changed, 3 added. |
| `test_rev01_second_person.py` (the review's) | 13 | 5 pass, 8 fail | 13 pass. 12 unchanged, 1 changed. |
| `test_fix_new_rules.py` (new) | 29 | did not exist | 27 pass, 2 kept failing on purpose. |

Of the 23 review tests that failed against R-02:

- 21 now pass with their original assertions intact. Two of those also gained an assertion.
- 1 passes after its assertion was corrected, because the review had the rule wrong (second-person, below).
- 1 is kept exactly as written and marked as an expected failure, because no code can make it pass (attacks, item 4 below).

"Kept failing on purpose" means the test is marked `expectedFailure`. It asserts a rule one would want, the service does not keep it, and the run shows it as `expected failures=N` every time. If such a test ever passes, the run fails with "unexpected success".

## Setup that changed (not assertions)

- `tests/fixture.json` is R-02's fixture plus three things the fixed service needs: one person (`cole`, whose personal space is `personal`), one membership (`cole` owns `mgmt`), and one more token (`cole` as a person in his personal space). Pages, organizations and the five original tokens are the same.
- `fixture()` in `test_rev01_second_person.py` now says who the two people are and what each belongs to, and adds a token for each as a person. Organizations and pages are the same.
- The service under test is `../service`, not `spikes/r-02/service`.

## `test_criteria_1_3.py`: 6 of 35 changed

The first five are the tests that query the database directly as the service's own login. That login could select from `brain.pages` under row-level security. It now has no privilege on any table (REV-01 RV-05, RV-06, RV-19), so a test that selected from the table has to ask the same question another way.

1. **`Criterion1DatabaseItself.test_no_session_means_no_rows`.** Was: `select count(*) from brain.pages` returns `0`. Now: the same statement is refused with "permission denied", and four tool functions called with no session are each refused with `no_session`. Stricter than before.
2. **`Criterion1DatabaseItself.test_bound_session_sees_only_its_organization`.** Was: with the toveli token bound, a select on the table shows organizations `mgmt,toveli` and no sibling or personal marker. Now: the same two checks through `brain.t_list` and `brain.t_search`, plus a third: a bound session still cannot select from the table.
3. **`Criterion1DatabaseItself.test_session_does_not_outlive_its_transaction`.** Was: after commit the table shows 0 rows. Now: after commit `brain.t_list` is refused with `no_session`.
4. **`Criterion1DatabaseItself.test_role_cannot_pick_an_organization_or_switch_off_the_policy`.** The 14 original attempts and the assertions are unchanged. 22 attempts are added: the new tables, every function that is not a granted tool, creating a function in the schema, and loading `auto_explain`.
5. **`Criterion1DatabaseItself.test_table_forces_row_security_and_role_is_plain`.** The two original assertions are unchanged. One is added: the login holds no privilege on any table or sequence of the schema.
6. **`Criterion2Holding.test_holding_can_publish_a_global_page`, renamed `test_holding_global_page_reaches_the_sub_organizations_only_after_a_person_approves`.** Was: the holding organization's agent writes a global page and the sibling reads it at once. That behaviour is finding RV-02: it lets an agent relay any page to every venture. Now: the write succeeds with `status: pending_approval`, the sibling does not read it, and it reads it after Cole approves as a person. This is the one R-02 test whose expected behaviour was reversed.

## `test_rev01_attacks.py`: 6 of 24 changed, 3 added

1. **`HeldInTheDatabase.test_temp_objects_and_search_path_do_not_change_the_bound_organization`** (passed before). The six original attempts are kept and four added for the new tables and functions. The assertion is the same (`mgmt,toveli`); the answer is read through `brain.t_list` because the login cannot select from the table.
2. **`HeldInTheDatabase.test_a_savepoint_rollback_unbinds_the_session`** (passed before). Was: after the rollback the table shows 0 rows. Now: `brain.t_list` is refused with `no_session`.
3. **`HeldInTheDatabase.test_copy_returning_and_other_statement_forms_respect_the_policy`** (passed before). The six original statements are kept. Was: none of them leaks a marker. Now: none leaks and each is refused. Four statements are added that go through the functions.
4. **`RelayThroughTheHoldingAgent.test_switching_briefings_off_removes_personal_text_from_every_organization`** (failed before). Kept exactly as written and marked as an expected failure. It requires that once briefings are switched off, the holding organization can no longer read the briefing's text in a copy its own agent wrote down. The service cannot tell that copy from any other page, so no code removes it. The review said as much in its own text and then wrote a test that demanded it. The rule code can keep is the first added test below.
5. **`AuditCompleteness.test_the_database_role_cannot_write_an_audit_row_without_a_bound_session`** (failed before). The original statement and assertion are kept. `brain.audit_log` no longer exists, so four statements against the functions that replaced it are added, and one assertion: with a session, the login can record a refusal for its own organization and never an allowed call.
6. **`WhatTheDatabaseRoleLearnsWithoutASession.test_explain_analyze_does_not_reveal_another_organizations_paths`** (failed before). The original assertion is kept. One is added: the statement is refused in both cases.

Added:

- **`RelayThroughTheHoldingAgent.test_switching_briefings_off_hides_the_delivered_page_everywhere_and_the_log_names_who_read_it`.** The enforceable half of item 4.
- **`TimingAndScale.test_a_forbidden_page_id_takes_as_long_as_a_missing_page_id`.** The review measured the timing difference by page id and asserted it only by path.
- **`TimingAndScale.test_inside_the_database_a_forbidden_lookup_costs_what_a_missing_one_costs`.** The two HTTP timing tests carry about 100 microseconds of noise from the commit to disk, against a threshold of 100. This one measures the lookup inside one database session, 20,000 times each way, and requires the median difference to be under 1 microsecond.

## `test_rev01_second_person.py`: 1 of 13 changed

1. **`StepA_FriendHoldsOneHumanToken.test_what_the_friend_writes_does_not_reach_coles_agents_without_a_decision`** (failed before). Was: a note the friend writes in the shared venture is read by neither the holding organization's agent nor Cole's personal agent (`readers == []`). The half about the personal agent was the review's mistake. Cole's rule of 2026-11-17 is that his personal space reads everything he belongs to, and he co-owns that venture. Now: `readers == ["personal"]`. The holding organization's agent still reads nothing. One assertion is added: the page Cole's personal agent gets says the friend wrote it (`written_by`).

The consequence is worth stating plainly: text a second person writes in a shared venture is read by the personal agent of the other owner, which is the agent that can also read that owner's health and finance pages. The service labels who wrote it and lets nothing leave the personal space without the person's approval. It does not stop that agent from being influenced by what it reads.
