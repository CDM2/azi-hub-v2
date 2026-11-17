# R-02 spike: raw results

Everything here is output of the spike described in `docs/research/R-02_RUNTIME_AND_HARNESS.md`. All data is made up, apart from facts about `CDM2/toveli` at `0abafdc` in the two criterion 8 files (short answers and counts; no source, no map pages, no transcripts).

## From this session's sandbox

| File | What it is |
| --- | --- |
| `jail-canary.txt` | 15 probes that the no-network jail holds. 15 held. |
| `criteria-1-3-direct-jail.txt` | The 35 tests for criteria 1 to 3, run straight against the permission service in the jail, plus two deliberate breaks that make them fail. |
| `criterion-8-map-update-and-sibling.json` | The mapper on Toveli: full build, incremental update from `525054d` to `0abafdc`, and the sibling-organization checks. 9 of 9 pass. |
| `criterion-8-qa.json` | 20 questions, three agents, two runs each, on Sonnet 5.5: per-answer score, tokens, time and cost. |

## From the scratch machine (`scratch/`)

A GitHub-hosted runner for the private repository `CDM2/Spike-test`, a fresh virtual machine per run. Paperclip ran there as its own unprivileged user with an empty environment.

| Run | Harness commit | What happened |
| --- | --- | --- |
| `43791010227-1` | `900b199` | Environment probe only. Not kept here. |
| (cancelled) | `4aacfc0` | Hung: `paperclipai onboard --yes` sets up and then keeps running the server in the foreground. No results. |
| `43794423882-1` | `bd719c5` | First full pass. Criteria 1 and 2 passed apart from one wrong check. Found: ask-first calls need a task-scoped session (`approval_path_missing`); two harness checks were wrong (below); the upgrade's install failed. Summaries kept. |
| `43795703101-1` | `474d0c9` | Found: approving an action makes Paperclip run it; the agent's retry is refused. Records the install failure of `2026.1106.0` under umask 0002, in place and into a fresh directory (`install-2026.1106.0-pc.log`, `install-2026.1106.0-pc-new.log`, `upgrade-diagnostics.txt`). |
| `43796944744-1` | `54bf31e` | Final harness, umask 022. 37 of 37 checks on `2026.1023.0`; in-place upgrade; 37 of 37 on `2026.1106.0`; governance probes on both; criterion 5 once per arm. |
| `43798233669-1` | `7928416` | The same again on a fresh machine, with criterion 5 three times per arm. Same results. Kept in full. |

In each run directory: `stages.log` (the timeline), `direct-tests.txt` (the 35 tests on that machine), `old/` and `new/` (`checks.json` for criteria 1 to 4 on each Paperclip version), `governance-old/` and `governance-new/` (criterion 7 probes), `upgrade.txt` and `upgrade-migrations.txt` (the upgrade), `version-*.txt` (npm integrity of what was installed), `task/task.json` (criterion 5), and tails of the service and Paperclip logs.

## Corrections made to the harness after first contact with Paperclip

None of these is one of the 35 tests written before the service.

1. **Leaked-credential check.** It matched any variable name containing `GH_` or `GITHUB_`. Paperclip sets `GH_CONFIG_DIR`, `PAPERCLIP_GITHUB_AUTH_MODE` and `PAPERCLIP_GITHUB_HOST_HOME` itself. The check now looks for the runner's own credential names.
2. **"A sibling's page looks like a missing page."** It compared Paperclip's whole response, which carries a new request ID and timing each call. It now compares the status, the service's answer and the reason code.
3. **Approvals.** The harness first assumed the agent retries after approval, as Paperclip's guide says. In both releases the approval itself runs the call. The checks now read the outcome from the approval.
4. **Observations are kept apart from criterion checks.** Two lines print as `NOTE`: a tool left out of a connection's enabled list was still callable, and a request for a tool that does not exist is not in Paperclip's audit log.

## What was removed before committing

Colour codes; signed or base64-encoded blobs from Paperclip's responses (replaced with a marker); long repeated payloads in the two older runs; request traces except the final run's. The bearer tokens that appear are the fixture's made-up ones.
