# R-02 spike plan

Status: revision 2, 2026-11-15, after Cole's reply to revision 1. Waiting for his final OK. Nothing below has run except the jail canary and a check that the API key authenticates (a model list, which costs nothing).

The spike tests R-01 option D: unmodified Paperclip for each organization, our own permission service reached over MCP, and a chief-of-staff agent. Criteria 1 to 6 are in R-01 section 7. Cole added 7 (governance coverage) and 8 (codebase map).

Changed since revision 1:

- Paperclip runs on a throwaway scratch repository, not in this session's sandbox.
- Toveli is read-only throughout. No Toveli ticket is worked on. Criterion 5 uses a made-up repository.
- Criterion 3 tests that nothing goes from personal to an organization, pending Cole's answer on the one exception that exists today.
- Criterion 2 follows the current AZI Hub rule.

## Words used

- **Page.** One entry in a second brain: a note, a summary, a description of a code file.
- **Holding organization.** The organization at the top that owns the others. AZI Hub in the old system; "the management company" in the mission.
- **Sub-organization.** A venture under it: Toveli, AltZ Capital.
- **Sibling.** Another sub-organization under the same holding organization. AltZ Capital is Toveli's sibling.
- **Personal.** Cole's own space, beside the holding organization.

## 1. Where things run

| What | Where | Why |
| --- | --- | --- |
| Paperclip, the permission service, criteria 1 to 7 | A throwaway private repository that Cole creates. A GitHub Actions run on it, or one command in a Codespace on it. Results are committed back to that repository, so nothing is pasted. | A separate machine with a token that reaches only the scratch repository. No Toveli, no real data, no real secret. |
| The Toveli codebase map and its three question-answering agents (criterion 8) | This session's sandbox, inside the jail | It needs the Toveli source, which stays here. No Paperclip runs here. |

The jail (`jail/jail.sh`) has no network, an empty environment, an unprivileged user, and empty filesystems mounted over the session's home. `jail/canary.sh` tries 15 ways out; all 15 failed on 2026-11-15 (`results/jail-canary.txt`). It shares a kernel with the session, so it is not a guarantee, which is why Paperclip does not run in it.

Pinned versions of Paperclip: `v2026.1023.0` (`1b4c803816e82b0265c8422e1a804327a7ed8c54`) to start, upgraded to `v2026.1106.0` (`d69631b01b9c658f80bf8bed389863dce82643e1`) for criterion 6. Its source is not edited; a criterion that needs a patch is a fail for option D. Its telemetry is switched off by its documented setting.

## 2. Toveli is read-only

- Nothing in `CDM2/toveli` has been edited, committed or pushed by this session. The local clone is at `0abafdc` with no changes.
- The session's GitHub credential could write to that repository; the GitHub API reports full permissions. Read-only is therefore a rule this plan follows, not something GitHub enforces for it. Two seatbelts are in place: pushing from the local clone is disabled, and the copy the agents read sits in the jail, which has no network and no credentials.
- Cole can make it enforced: remove the Claude GitHub app's access to `CDM2/toveli`. The clone already here is all the spike needs.
- The agents only read. They answer questions about the code. They do not draft ticket deliverables, and no ticket in A-002 is touched.
- The copy in the jail is deleted when the spike ends. The map and any Toveli source stay out of every repository.

## 3. Model calls and spend

| Criteria | Model calls | How |
| --- | --- | --- |
| 1, 2, 3, 4, 6 | None | A scripted agent runs in Paperclip through its built-in `process` adapter and calls the permission service through Paperclip's MCP gateway. |
| 7 | None expected | Controls are exercised through Paperclip's API. If the spend-cap test needs a real model call to record spend, it joins the criterion 5 run and the report says so. |
| 5 | Yes, small | One Claude agent inside Paperclip does a small job on a made-up repository, using the brain through the gateway. One plain agent does the same job outside Paperclip. |
| 8 | Yes | Three question-answering agents over 20 questions, two runs each, on Sonnet 5.5. The mapping pass is deterministic and calls no model. |

Expected spend: $30 to $60. Cap: $100; every model call goes through a bridge that prices each response at list rates and refuses further requests at $95.

The key is held in a root-only file outside the jail and is in no repository. For criterion 8 it never enters the jail. For the one Paperclip run in criterion 5 it has to be on the scratch machine, as a repository secret; that is the only place it sits near Paperclip, and the exposure is the remaining balance. If Cole prefers, that run is skipped and recorded as not run.

## 4. Needed from Cole

1. Create an empty private repository for the spike and say its name. Delete it when the spike is done.
2. Personal to organization: nothing ever, or keep the one curated briefing that exists today (test 3).
3. Whether the throwaway key may be set as a secret on the scratch repository for the criterion 5 run.

## 5. Test sets

Tests for criteria 1 to 3 and the 20 questions are committed before the code they test. The commit order is the proof.

Made-up organizations: a personal space, a holding organization, and two sub-organizations. All page content is made up. No real personal, health or financial data is used anywhere in the spike.

| # | Criterion | Passes when |
| --- | --- | --- |
| 1 | A sub-organization's agent gets its own and global pages only | Through Paperclip's gateway the agent lists, searches and fetches. It never receives a sibling's page: not by ID, not by search text, not by passing the sibling's name as an argument, not with the sibling's token, not through a count or an error message. The same holds when the database is queried directly as the service's own role. |
| 2 | The holding organization reads its sub-organizations | As in AZI Hub today: the holding organization's agent reads global pages, its own and every sub-organization's. It reads nothing personal. A stricter mode, summaries only, is also run and reported, because AZI Hub's configuration file says "summaries" where its code allows everything. |
| 3 | Nothing goes from personal to an organization | No organization's token reads a personal page by any tool. The personal space can read organization pages. No tool copies a personal page into an organization's brain. Health and finance pages can exist only in personal; the database refuses to store one anywhere else. If Cole keeps the curated briefing, the test instead allows that one path and requires his approval on each briefing. |
| 4 | Every call is in both audit logs | Each allowed and each denied call appears in Paperclip's call event log and in the service's own log, matched one to one by an ID. A call that goes around Paperclip appears only in ours; the report records that as a known limit (ledger E-89), not a pass. |
| 5 | A model-driven agent works through the stack | The Paperclip agent completes the job using brain pages it fetched through the gateway, and the calls are in both logs. A plain agent does the same job; tokens and time are recorded for both. The report states that no real Toveli task was run through Paperclip. |
| 6 | Paperclip is upgraded one release | After the upgrade from `v2026.1023.0` to `v2026.1106.0`, tests 1 to 4 pass again with no change to the permission service or its configuration. |
| 7 | Governance coverage | Not pass or fail, and nothing is bought. A table of every control N-01 to N-08 and R-01 require: approvals, spend caps, audit log, secrets, tool and MCP policy, pause or kill, approval on sharing, the gate on the improvement loop. Each is marked as working in free Paperclip, present only in Paperclip's paid edition, or ours to build with a rough size, with the evidence. It ends by saying whether R-01's trigger 3 is met. |
| 8 | Codebase map | First a survey of existing tools. Then the smallest mapper on a read-only copy of `CDM2/toveli`: a deterministic manifest written to Toveli's brain as pages tagged as codebase. Scored on 20 questions whose answers were checked against the code: (a) map only, (b) map first, then raw code, (c) one coding agent with plain read access and no map. Accuracy, tokens and time for each. Also: the sibling organization cannot read a Toveli code page, and a new commit updates only the pages for changed files and matches a full rebuild. If (c) matches the map, the report says so. |

Any criterion that cannot be run is recorded as not run.

## 6. Founder input recorded here, 2026-11-15

- No edits to the Toveli codebase from this project. Cole works through Toveli's tickets in order in another session.
- Personal information is never sent to an organization. Health and finance pages exist only in personal. Whether the existing curated briefing stays is open (item 2 above).
- Governance pricing: a feature that needs Paperclip's paid edition is charged to the customer; features this project builds can be free for now. This is a pricing position for R-08 and Gate G1, not a spike input.
- Cole has a Claude Max plan and has not claimed its monthly API credits (ledger E-76).

## 7. What goes in the repositories

`CDM2/azi-hub-v2`: spike code, tests, the 20 questions with their answer keys, scores and raw logs, under `spikes/r-02/`. The scratch repository: a copy of the spike code and the raw results of each run. Toveli source, the map itself and the API key go in neither.
