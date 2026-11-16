# R-02 spike plan

Status: proposed, 2026-11-15. Waiting for Cole's OK. Nothing below has run except the jail canary.

The spike tests R-01 option D: unmodified Paperclip for each organization, our own permission service reached over MCP, and a chief-of-staff agent. Criteria 1 to 6 are in R-01 section 7. Cole added 7 (governance coverage) and 8 (codebase map).

## 1. Where Paperclip runs

In this session's sandbox, inside a jail. The alternative is a script for a throwaway Codespace on a scratch repository, with Cole pasting the output back.

The jail (`jail/jail.sh`):

- Its own network namespace with loopback only. The session's credential proxy and the internet are unreachable.
- Its own process and mount namespaces. Empty filesystems are mounted over the session's home, root's home and `/tmp`, so the three private clones and the signing key are not there to read.
- An empty environment and an unprivileged user that cannot regain privileges.

`jail/canary.sh` tries 15 ways out: read each clone, read the environment, reach the proxy, reach GitHub and Anthropic, resolve a name, see other processes, write outside its home. All 15 failed on 2026-11-15 (`results/jail-canary.txt`). The same resources are reachable outside the jail, so the probes are meaningful. The canary runs again before each stage and its output is kept.

What the jail is not: a separate virtual machine. It shares a kernel with the session. Getting out would take a kernel or container escape. A Codespace on a scratch repository is a separate machine and is the stronger boundary.

Installing: packages are downloaded outside the jail with install scripts switched off, so nothing third-party executes there. Install scripts and Paperclip itself run only inside the jail.

Pinned versions: Paperclip `v2026.1023.0` (`1b4c803816e82b0265c8422e1a804327a7ed8c54`) to start, upgraded to `v2026.1106.0` (`d69631b01b9c658f80bf8bed389863dce82643e1`) for criterion 6. Both are published release tags. Paperclip's source is not edited; a criterion that needs a patch is a fail for option D. Telemetry is switched off by its documented environment variable.

## 2. Model calls and spend

| Criteria | Model calls | How |
| --- | --- | --- |
| 1, 2, 3, 4, 6 | None | A scripted agent runs in Paperclip through its built-in `process` adapter and calls the permission service through Paperclip's MCP gateway. |
| 7 | None expected | Controls are exercised through Paperclip's interface and API. If the spend-cap test needs a real model call to record spend, it moves to the stage below and is said so. |
| 5 | Yes | A Claude agent inside Paperclip, and one single agent outside it as the N-04 baseline. |
| 8 | Yes | Three question-answering agents over 20 questions. The mapping pass itself is deterministic and calls no model. |

Expected spend: $35 to $65, on Sonnet 5.5 for every agent so the comparison is like for like. Cap: $100.

The API key never enters the jail. A small bridge outside the jail injects it into requests that the jail sends over a local socket, the pattern Anthropic documents for hosted agents (ledger E-79). The bridge prices every response at list rates and refuses further requests at $95.

Without a key: criteria 1 to 4, 6 and 7 still run. Criterion 8 can run on this session's own subagents with no API spend, with token counts as the harness reports them. Criterion 5 would be recorded as not run.

## 3. Needed from Cole

1. Jail here, or a Codespace script.
2. A throwaway Anthropic API key with a $100 workspace spend limit, revoked after the spike. Or "no key".
3. The Toveli task for criterion 5. Proposed: the data inventory from TOV-022 (its acceptance case 3). It is a ready ticket, documentation only, and a script can check it against A-001. The draft is handed over as a file and is not pushed to Toveli.
4. Sonnet 5.5 for all agents, two runs per arm in criterion 8: yes or change.

## 4. Test sets

Tests for criteria 1 to 3 and the 20 questions are committed before the code they test. The commit order is the proof.

Synthetic organizations: a personal space, a holding organization, and two sub-organizations (`toveli` and a synthetic sibling). All page content is synthetic except the Toveli codebase map.

| # | Criterion | Passes when |
| --- | --- | --- |
| 1 | A sub-organization's agent gets its own and global pages only | Through Paperclip's gateway the agent lists, searches and fetches. It never receives a sibling page: not by ID, not by search text, not by passing another organization's name as an argument, not with another organization's token, not through a count or an error message. The same holds when the database is queried directly as the service's own role. |
| 2 | The holding organization reads sub-organization summaries | The holding agent reads pages marked as summaries from both sub-organizations. It does not read their other pages or anything personal. |
| 3 | Personal reaches an organization only by explicit push | No organization token reads a personal page by any tool. The only write path is a push tool called by the personal principal, which copies one page, records who approved it, and is refused for the health and finance class (N-08). |
| 4 | Every call is in both audit logs | Each allowed and each denied call appears in Paperclip's call event log and in the service's own log, matched one to one by an ID. A call that goes around Paperclip appears only in ours; the plan records that as a known limit (E-89), not a pass. |
| 5 | A real Toveli task runs through the stack and on one agent | Both runs produce the deliverable. A script checks each against the ticket's acceptance case. Tokens, time and the number of human interventions are recorded. |
| 6 | Paperclip is upgraded one release | After the upgrade, tests 1 to 4 pass again with no change to the permission service or its configuration. |
| 7 | Governance coverage | Not pass or fail. A table of every control N-01 to N-08 and R-01 require: approvals, spend caps, audit log, secrets, tool and MCP policy, pause or kill, approval on sharing, the gate on the improvement loop. Each is marked verified in the free edition, present but paid edition only, or ours to build with a rough size, with the evidence. It ends by saying whether R-01's trigger 3 is met. |
| 8 | Codebase map | First a survey of existing tools. Then the smallest mapper on `CDM2/toveli`: a deterministic manifest written to Toveli's brain as pages tagged as codebase. Scored on 20 questions whose answers were checked against the code: (a) map only, (b) map first, then raw code, (c) one coding agent with plain repository access. Accuracy, tokens and time for each. Also: the sibling organization cannot read a Toveli code page, and a new commit updates only the pages for changed files and matches a full rebuild. If (c) matches the map, the report says so. |

Any criterion that cannot be run is recorded as not run.

## 5. What goes in the repository

Spike code, tests, the 20 questions with their answer keys, scores and raw logs go under `spikes/r-02/`. Toveli source, the map itself and the criterion 5 deliverable stay out.
