# R-02 — Runtime and harness, and the spike that closes the route check

Status: v1.0, for acceptance. As of 2026-11-16 (UTC). Prepared by a Claude session on Cole's brief of 2026-11-15. Acceptance is the founder's merge of the pull request that carries this file. With R-01 it feeds Gate G1a. No separate review session has attacked it.

Reads with [`R-01`](R-01_CATEGORY_AND_EXISTING_TOOLS.md) (section 7 holds the options and the spike criteria), `docs/source/V-000` (decisions F-xx, rules N-xx) and `docs/source/P-000`. Evidence IDs such as E-76 point to rows in [`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md). Spike code and raw results are in [`spikes/r-02/`](../../spikes/r-02/). A sentence marked **Judgment** is my reading of the evidence, not a sourced fact.

Terms used throughout. **Option D**: an unmodified Paperclip per organization, with this project's own permission service beside it. **Option E**: a lean orchestrator of our own. **The permission service**: the spike's small service that holds the tier map and the second brain and decides who reads what. **Holding organization**: the management company above the ventures. **Sibling**: another venture under the same holding organization. **The gateway**: the part of Paperclip through which its agents call outside tools.

## Bottom line

- **D holds.** An unmodified Paperclip per organization, with our own permission service beside it, passed criteria 1 to 4 on two Paperclip releases, before and after an upgrade that left the service untouched (section 7).
- **What the pass rests on.** 35 tests written before the service, and 37 checks through Paperclip's gateway, repeated on a fresh machine with the same result. A sibling's page was never returned, and looked the same as a page that does not exist.
- **Trigger 3 for option E is not met.** Approvals, spend caps, the audit log, tool policy, pause and kill all work in Paperclip's free edition. Approval on sharing, the improvement gate and the tiers are ours to build, as option D always assumed (section 6.2).
- **Five things about Paperclip to design around.** A request for a tool that does not exist is not audited. Approving a tool call makes Paperclip run it; the agent does not retry. A tool left out of a connection's enabled list was still callable. A secret an agent prints lands in the run log unmasked. The newer release will not install under a common default file mask.
- **One agent matched the full stack, and a plain agent matched the codebase map.** On the one task run both ways, and on 20 questions about Toveli's code, the simpler setup did as well. The stack and the map earn their place on permission and governance, not on quality (N-04; sections 6.3 and 7).
- **Runtime.** No agent loop needs choosing or building now. Paperclip's adapter is the boundary F-16 asks for (section 1).
- **Budget.** E-26 was wrong: Agent SDK use still draws on a Claude plan's limits. Max and Ultra plans now carry monthly API credit that Cole has not claimed. The spike cost $1.68 (section 5).
- **Not run.** A real Toveli task through the stack. A crash in the middle of a run. Paperclip with real user accounts. A review session.
- **Route A or B is Cole's decision.** The memo is section 10.

## Method and limits

| Step | What was done |
| --- | --- |
| Desk research | 25 ledger rows (E-75 to E-99) on runtimes, durable execution, sandboxing, model choice, plan credits and codebase-map tools, gathered 2026-11-15. Each row says whether the source was read in full or as an excerpt. |
| Paperclip | Source read at tag `v2026.1106.0` (`d69631b01b9c658f80bf8bed389863dce82643e1`) and `v2026.1023.0` (`1b4c803816e82b0265c8422e1a804327a7ed8c54`). Installed from npm at both versions and run, unmodified, on a throwaway machine (below). |
| Permission service | Written for the spike: PostgreSQL row-level security, a session bound inside the database, an append-only audit table, and six tools served over MCP. About 540 lines. The 35 tests for criteria 1 to 3 were committed before the service (commit `5d3ad72`, then `5431d10`). |
| Where third-party code ran | Only on GitHub's hosted runner for the private scratch repository `CDM2/Spike-test`, as a separate unprivileged user with an empty environment, on made-up data. That machine held a token that can write to the scratch repository and, in the two final runs, the throwaway model key. Nothing third-party ran in this session's sandbox. |
| Where Toveli was read | In this session's sandbox, from a clone at `0abafdc`, by our own code only, through git without checking files out. The permission service and its database, which held the map pages, ran inside a jail with no network. Nothing was written to `CDM2/toveli`, and no Toveli source, map page or transcript is in this repository. |
| Model calls | Criteria 5 and 8 only: Sonnet 5.5 through the Messages API. Criteria 1 to 4, 6 and 7 used no model. |
| Not done | Customer interviews. A real Toveli task through the stack (criterion 5 ran on a made-up repository; section 6.4). A crash in the middle of a run. Paperclip's `authenticated` mode with real users. Paperclip's MCP endpoint form of the gateway (the spike used the REST form). Any load or soak test. A separate review session. |

## 1. Runtime: what runs the agent loop

Under option D the word "runtime" covers two layers, and only the second is still open.

- **The organization engine.** Paperclip: the org chart, heartbeats, budgets, approvals and the adapters that start agents (R-01, E-02, E-48). The spike ran it (sections 6 and 7).
- **The agent loop.** The program that calls the model, runs tools and keeps a session. Paperclip starts one per agent through an adapter. Twelve adapter packages ship with it, plus a built-in `process` adapter that runs any command and an `http` adapter (E-91).

The four candidates P-000 named for the agent loop:

| Candidate | What it is | State and isolation | Models | Fit |
| --- | --- | --- | --- | --- |
| Claude Agent SDK | The Claude Code loop as a Python or TypeScript library, with file, shell and web tools, hooks, subagents, MCP and permissions (E-78) | Each session is a subprocess that keeps its transcript on local disk. A `SessionStore` adapter mirrors transcripts so another host can resume. About 1 GiB of RAM and one CPU per agent. The API key can stay outside the container behind a proxy (E-79). | Claude by default. A gateway can put other models behind it (E-81). | Strong for organization agents that write code. Products offered to others need API keys, not a Claude plan login (E-78). |
| Claude Managed Agents | Anthropic hosts the loop and the sandbox (E-82) | Session history and sandbox state sit on Anthropic's side. A session budget pauses at its cap. Vault credentials are swapped in on the way out. | Claude only | Least to operate. Still a beta. It conflicts with F-17 (self-hosted) unless the self-hosted edition is used, and that opened as a private beta on 2026-11-12. $0.08 per session-hour on top of tokens (E-77). |
| Hermes Agent | An open-source personal agent with one gateway per machine across the CLI, desktop and chat bots (E-83) | Six terminal backends. The default is local, with no isolation. Its default approval mode asks a model to judge risk (E-84). | More than 20 providers and local models (E-83) | A candidate for the personal chief of staff, as R-01 said. The default approval mode breaks N-03; `manual` mode does not (E-84). |
| Own loop | AZI Hub's runner: 2,486 lines in the agents directory, a stub Firecracker provider, model IDs written into the source (E-85) | Whatever is built | Whatever is built | INV-000 already marks it "likely replaced". Nothing found here argues for rebuilding it. |

**What the spike adds.** The permission service did not care what the agent loop was. A scripted process with no model reached it through Paperclip's gateway using only the credentials Paperclip injects into every run (E-103). Any loop that can make an HTTP call from inside a Paperclip run can do the same. Paperclip also hands each run an MCP endpoint and a short-lived token for these tools (seen in the run's environment; not exercised, the spike used the REST form).

**Judgment.** Do not pick one agent loop now, and do not build one. Keep Paperclip's adapter as the boundary F-16 asks for. Use the Claude adapter for organization agents first. Choose between the Agent SDK and Hermes for the chief of staff when the first slice is built, by trying both against the same permission service. Leave Managed Agents until its self-hosted edition is generally available. An own loop stays the fallback that option E implies.

## 2. Durable execution

Durable execution means a long job survives a crash or restart and continues without repeating steps that already had an effect.

- **Inside Paperclip.** Recovery is the engine's job: a retry is recorded under an idempotency key before work starts, a sweeper clears stale locks, and waits survive a restart (E-87). In the spike, stopping Paperclip and starting a newer version kept every company, agent, connection and audit event (section 7, criterion 6). Cancelling a run stopped the agent's process in about two seconds (E-106). A crash in the middle of a run was not tested.
- **Dedicated engines.** Temporal, Restate, DBOS and Inngest recur in 2026 guides. Several advise starting with DBOS where Postgres is already in use, because it checkpoints into the application's own database with no extra server (E-86). All agree an engine cannot make an outside side effect happen exactly once; the application still needs idempotency (E-86).

**Judgment.** Add no workflow engine now. Paperclip covers the agents' runs. The permission service's own long jobs (the map sync, later the improvement loop) are short, repeatable and already idempotent in the spike: the map sync rewrites only pages whose content changed (E-108). If a job of ours ever needs checkpoints, a Postgres-backed library is the first thing to try, since the service already runs on Postgres.

## 3. Sandboxing

What the sources say:

- Anthropic documents four levels for Claude Code and the Agent SDK: a sandboxed shell tool, a process-level sandbox runtime, a container, and a virtual machine, with microVMs as the strongest (E-80).
- Hermes skips its command checks inside a container backend, on the ground that the container is the boundary (E-84).
- Paperclip says its gateway is not host-wide enforcement: it governs calls that go through it and nothing else an agent does on the machine (E-89).

What the spike observed:

- A Paperclip agent is an ordinary process running as Paperclip's own operating-system user. It inherits Paperclip's environment plus 28 variables Paperclip adds, among them the run token and an agent private key (E-111). It can read whatever that user can read.
- On the scratch machine Paperclip ran as a separate unprivileged user with an empty environment. The scripted agents saw none of the machine's own credentials (checked on every run, E-111).
- A secret bound to an agent by reference stayed out of API responses. When the agent printed it, the value appeared unmasked in the run log and the run record (E-107).
- A call made straight to the permission service, around Paperclip, appears only in the service's audit log (E-104). The service still decided it; Paperclip never saw it.
- For this session's own code, a jail built from Linux namespaces (no network, a private file system, an unprivileged user, an empty environment) held 15 of 15 escape probes (`spikes/r-02/results/jail-canary.txt`).

**Judgment.** For Cole's own ventures on one VPS: one container per organization holding Paperclip and its agents, with no host credentials inside; the permission service outside it, reachable only on its MCP port; model keys kept outside behind a proxy (E-79). Treat anything an agent can print as logged. Move to a microVM per organization before outside customers share a machine. The permission decision stays in the database either way (N-03), which is why a compromised agent in one organization still cannot read a sibling's pages (section 7, criterion 1).

## 4. Model choice per task (F-16)

F-16 has two halves. "By setting" exists today. "By asking the system" is ours to build.

- **By setting.** In Paperclip each agent has an adapter and its configuration, so the model is chosen per agent (E-91). In the Agent SDK a session takes a model and a subagent can override it; a gateway can put non-Anthropic models behind the same interface (E-81). Hermes sets the main model and each auxiliary task separately (E-84).
- **Prices on 2026-11-15**, per million input and output tokens: Fable 5.2 $8 and $40; Opus 5.5 $4 and $20; Sonnet 5.5 $2 and $10; Haiku 5.5 $0.10 and $0.50 (E-77). Haiku is 20 times cheaper than Sonnet.
- **Measured in the spike.** Sonnet 5.5 answered a code question about Toveli for about one cent, in five to seven seconds, and got all 40 right when it could read the code (E-109). A small coding task with tests cost three to five cents (E-110).

**Judgment.** A starting rule, to be measured and changed: Haiku for extraction, classification and routine heartbeats; Sonnet for coding and research; Opus or Fable for plans and reviews that a human will act on. "By asking the system" is a small routing table the chief of staff can read and propose changes to, with the change itself approved by a human (N-03). It belongs in the first slice's design, not in this spike.

## 5. Budget (F-18) and the correction to E-26

**The correction.** R-01 carried E-26: that from 2026-06-15 Agent SDK use would leave Claude plan limits and draw on a small separate credit. That did not happen. Anthropic paused the change on the day, and its help page, as updated on 2026-10-07, says Agent SDK and `claude -p` use still draws from the plan's limits when signed in with a plan (E-75). The ledger marks E-26 as superseded.

**What is true now.**

- Since 2026-10-07 the Max, Ultra and Team plans include monthly credit for the Claude API: $100 on Max and $200 on Ultra. It covers the API, Managed Agents, the Agent SDK and the Console playground. It is claimed by linking one Console organization, is spent before purchased credit, and expires each billing cycle (E-76).
- Cole says he pays $249 a month for Claude Max and has not claimed any credit. $249 is not a list price; the nearest plan is Ultra at $200 (E-77). **Judgment:** it is probably Ultra bought inside a mobile app store, where prices run higher. **Unverified:** which plan it is, and whether a plan bought that way can claim the credit. The Console will show both.
- A product offered to other people must use API keys. Third-party developers may not offer Claude plan logins or plan rate limits without approval (E-78). Pilots with outside businesses therefore cannot run on Cole's plan.

**Effect on the $1,000 a month in F-18.**

- If the credit can be claimed, up to $200 a month of API use is already paid for. F-18's $1,000 stays "on top of existing subscriptions" as written.
- Cole's own interactive work in Claude Code keeps drawing on the plan, not on the $1,000.
- The whole spike cost $1.68 of API use (section 6.5). At the measured rates, $1,000 buys roughly 100,000 one-cent questions or 25,000 four-cent coding tasks on Sonnet 5.5. Long agentic sessions on Opus cost dollars each, so the budget is a real limit only once agents run unattended all day. Paperclip's per-agent monthly cap stopped an agent in the spike (section 6.2).

**Judgment.** The budget is not a constraint on Phase 1. It becomes one with always-on agents, and Paperclip's caps plus a holding-level total of our own are the controls for that.

## 6. The spike

### 6.1 What was built and where it ran

- **The permission service** (`spikes/r-02/service/`). PostgreSQL with row-level security forced on, an application role that owns nothing, a session that is bound inside the database from the caller's token, and an append-only audit table. Six tools over MCP: who am I, list, search, get, write, publish a briefing. The rules are in `service/CONTRACT.md`. The filter is a database policy; no prompt takes part in it (N-03).
- **Four made-up organizations**: personal, a holding organization, and two ventures named `toveli` and `sibling`, with 12 marker pages. Health and finance pages can exist only in personal; a database constraint refuses them anywhere else.
- **Paperclip**, unmodified, from npm: `paperclipai@2026.1023.0`, then upgraded to `2026.1106.0`. One Paperclip company per organization, each connected to the permission service through Paperclip's gateway with that organization's token. Telemetry off (E-93). Mode `local_trusted`, where local requests act as the board operator.
- **Agents.** For criteria 1 to 4, 6 and 7: a scripted agent with no model, started by Paperclip's built-in `process` adapter, using only the run credentials Paperclip injects. For criterion 5: the same adapter running a small model loop on Sonnet 5.5.
- **Runs.** Six workflow runs on the scratch machine, each on a fresh virtual machine: an environment probe; one that hung because `paperclipai onboard --yes` keeps the server in the foreground; two that exposed harness mistakes and the install problem below; and two on the final harness that gave the same results. Raw output of the last three, and a summary of the one before, is in `spikes/r-02/results/scratch/`. `spikes/r-02/results/README.md` lists every run and every correction. Below, "the two final runs" are `43796944744` and `43798233669`.

### 6.2 Criterion 7: governance coverage

The brief asks for each control to be sorted into one of three classes: verified working in Paperclip's free edition, present but paid-edition only, or ours to build. Each "verified working" row was exercised through Paperclip's own API in the free npm package, on both versions, in both final runs, with the same result. No control on the list fell into the middle class. Sizes are rough: S is days, M is a week or two, L is more.

| Control | Asked for by | Paperclip, free edition | Verdict | If ours, size |
| --- | --- | --- | --- | --- |
| Approval before a tool call acts | N-01, N-03 | Works. 409, approval card, then Paperclip runs the approved call once. Needs a task-scoped session (E-102). | Verified working | |
| Approval before a new agent exists | The brief | Works. Direct creation is refused, the hire waits as pending, a human approves (E-106). | Verified working | |
| Approval for what an agent does with its own shell | N-01 | Not covered. The gateway governs tool calls that go through it and nothing else on the machine (E-89). | Ours | S to M: keep credentials out of agent environments and route pushes and payments through gated tools |
| Spend cap per agent | F-18, the brief | Works. A $1.00 monthly cap with $1.50 of reported cost paused the agent with reason "budget" and refused its next run. The made-up cost carried no price source, which set a second block that raising the cap did not clear (E-106). | Verified working | |
| Spend cap across organizations | F-18 | Not present. Budgets are per company and per agent. | Ours | S: a total in the permission service |
| Audit log | N-01, the brief | Works per company: an activity log (about 30 kinds of event seen) and the gateway's call log. Two limits under criterion 4 (E-104, E-106). | Verified working | |
| Audit across organizations | N-02, N-03 | Not present. An agent's token is refused another company's log (E-106). | Ours | S: the service's own log already spans organizations |
| Secrets | The brief; N-08 for keeping sensitive values out of logs | Partly. A secret is stored, bound by reference, and never returned by the API. When the agent printed it, the value sat unmasked in the run log and run record (E-107). | Verified working for storage and delivery. Masking in logs: ours | S to M: a key-injecting proxy, so agents never hold long-lived keys (E-79) |
| Tool and MCP policy | N-03, the brief | Works with block rules: the tool disappears from the agent's list and a call by its known name is refused with the rule's ID. One trap: a tool left out of a connection's enabled list was still listed and callable while the connection was granted to all agents (E-105). | Verified working, with the trap noted | |
| Pause or kill | The brief | Works. A paused agent's run is refused. Cancelling a run stopped the process in 2.2 seconds. A terminated agent cannot run (E-106). | Verified working | |
| Organization to organization is zero by default | N-02 | Works inside Paperclip: an agent's token gets 403 on another company (E-106). Across the second brain it is the permission service's job, and criterion 1 passed. | Verified working | |
| Approval on sharing | N-02, F-25 | Not a Paperclip concept. | Ours. Built in the spike for the personal briefing. | M for a production version with a review screen |
| Gate on the improvement loop | N-05, F-05 | Not present as a gate tied to measured results. | Ours. Not built in the spike. | M to L |
| Tiers: holding reads below, siblings apart, personal one-way | F-02, F-25 to F-27 | Not present. Companies are the only boundary (E-03, E-50). | Ours. Built in the spike. | M to harden |

**Paid edition.** One feature outside this list is visibly gated in the product at `v2026.1106.0`: the trust settings' editor for more than one containment boundary says "Get Paperclip EE" (E-113). Nothing in N-01 to N-08 needed it. Paperclip's own specification has a table headed "V1 vs Pro/Enterprise Controls (recommended target split)". Its paid column lists tool allowlists with centralized policy evaluation, scoped approver roles and policy overlays across companies (E-92). Tool policy works in the free package today. The table is a stated intention, so it is a risk and not a present fact.

**Trigger 3 for option E is not met.** Every control this project needs from Paperclip worked in the free edition at both pinned releases. The controls Paperclip lacks are the ones option D always meant to own. If block rules or approvals moved to the paid edition, trigger 3 would be met for that control. By F-28 the cost would then be passed on as a paid feature, or the control rebuilt.

### 6.3 Criterion 8: the codebase map

**Existing tools, surveyed first.**

- Aider's repository map ranks definitions by a reference graph and fits them into a token budget; it has been ported to standalone tools and MCP servers (E-94).
- DeepWiki and Google Code Wiki generate wikis on the vendor's servers. Private repositories need a paid Devin account or sit behind a waitlist (E-95). Sending a venture's private code to a vendor's servers is a decision this project has not taken; F-17 is self-hosted.
- Self-hosted: deepwiki-open has a model write the wiki; a group of code-graph servers index with tree-sitter, without a model, and serve the graph over MCP. Each indexes for one machine or one repository. An organization-wide graph is sold as an enterprise or hosted feature (E-96).
- Evidence on whether maps help: an ETH Zurich study found repository context files did not improve task success and raised cost by more than 20% (E-97). A paper comparing a code-graph agent with an exploring agent scored 0.83 against 0.92, with about ten times fewer tokens (E-98). Claude Code and Codex ship with no index and search at run time (E-99).

None of these puts the map inside a store with tiers. Extraction is a commodity; where the pages live and who may read them is this project's part.

**The smallest mapper** (`spikes/r-02/mapper/map_repo.py`, 411 lines, no model, no dependencies beyond git and Python). It reads a repository at one commit and writes one overview page, one page per package and one page per file: role, purpose in the file's own words, imports, importers, exports, tests, entry points, scripts, build and deploy steps. Pages go to Toveli's organization in the second brain, tagged as codebase.

| Check | Result |
| --- | --- |
| Toveli at `0abafdc` | 233 files became 241 pages in half a second. 33 of 126 code files say nothing about their own purpose, and the page says so. |
| A new commit updates the map without a full rebuild | From `525054d` to `0abafdc` the mapper re-read 53 of 233 files and rewrote 61 of 241 pages. The result equals a full rebuild, page by page, by content hash (E-108). |
| A sibling organization cannot read Toveli's code pages | The sibling's agent listed, fetched by path and searched: no Toveli code page came back. Toveli's agent listed all 241. The holding agent could read them, which is the current rule and R-04's to settle (E-108). |

**The comparison.** Twenty questions about Toveli, written and answered from the code before the mapper existed (`spikes/r-02/qa/questions.json`, commit `5d3ad72`). Three agents, the same loop, Sonnet 5.5, two runs each, graded by a script.

| Agent | Correct | Input tokens per question | Seconds | Tool calls | Cost per question |
| --- | --- | --- | --- | --- | --- |
| (a) Map only | 32 of 40 (16 and 16) | 11,740 | 7.1 | 3.6 | $0.0110 |
| (b) Map first, then code | 40 of 40 | 9,875 | 4.7 | 2.9 | $0.0098 |
| (c) Plain agent, no map (N-04 baseline) | 40 of 40 | 6,718 | 6.7 | 4.1 | $0.0093 |

**The plain agent matched the map.** With the code in reach, the map added no accuracy: both scored 40 of 40. The map made answers about two seconds faster and saved about one tool call a question. It cost 47% more input tokens and 5% more money. The map-only agent got every build, dependency and entry-point question right (26 of 26) and 6 of 14 on what a file does, where a value lives and code detail. It said what it could not determine instead of guessing.

Limits of this test: one repository of 233 files, 20 questions that I wrote, one model, two runs, and a ceiling, since two agents scored 100% and the test cannot separate them. It agrees in direction with E-97 and E-98.

**Judgment.** For an agent that can open the code, do not build more map than this. The map's use is the reader who may not open the code: the holding organization's agent or the chief of staff asking how a venture builds and what depends on what. For that reader the map answered the structural questions correctly at one cent each, under the tier filter, with no repository access. Keep the small deterministic mapper for that purpose and revisit when a venture's repository is ten times larger.

### 6.4 Where the spike departs from the brief

- **Criterion 5 ran on a made-up repository.** Cole made Toveli read-only for this project after the brief. No Toveli task ran through Paperclip.
- **The scratch machine was a GitHub-hosted runner**, not a Codespace: the runner's results come back through git, with nothing to paste. Cole approved a scratch repository; the repository is `CDM2/Spike-test`, private.
- **The model key.** A throwaway key with a $100 cap, which Cole made for the spike, was used in this session's sandbox. Cole also set it as a repository secret on the scratch repository, and the two final runs used it for criterion 5 only. During those few minutes the key sat in a file the Paperclip user could read, so third-party code could have read it. It should be revoked now.
- **Test count.** One commit message says 40 tests; the count is 35.
- **Two harness checks were corrected after first contact with Paperclip**, both recorded in `spikes/r-02/results/README.md`: a check for leaked credentials matched three variable names that Paperclip itself sets, and the "same answer as a missing page" check compared Paperclip's wrapper, which carries a fresh request ID each time, instead of the answer inside it. Neither is one of the 35 tests written before the service.

### 6.5 Spend

$1.68 of API use against the $100 cap. The figure is computed from the token counts the API returned, at list prices (E-77); it is not an invoice.

- Criterion 8: $1.34 for 129 answers (the 120 scored ones and a nine-answer trial of the runner).
- Criterion 5: $0.34 for nine task runs (one in this session's sandbox, eight on the scratch machine).
- Criteria 1 to 4, 6 and 7 made no model calls.
- The scratch machine used about 55 minutes of GitHub-hosted runner time from the account's included allowance.

### 6.6 Decisions and open items for Cole

1. **Gate G1a:** Route A or Route B.
2. **Option D:** confirm F-20 now that the spike is in, or hold it for the review session.
3. **Criterion 4:** accept "pass, with two limits", or call the unlogged request a fail.
4. **Criterion 5:** accept the made-up task, or run a real Toveli task later, when Toveli's own build is ready to be touched.
5. **The codebase map (C-23, F-24):** keep it small and aimed at readers without code access, as section 6.3 suggests, or drop it from the first slice.
6. **What the holding organization reads of a venture's code map:** everything today. R-04 settles it.
7. **P-000:** it is "the plan in use" with no acceptance record. Accept it or say it needs none.
8. **API credit:** check in the Console whether the plan's monthly credit can be claimed (E-76).
9. **Toveli access:** this session's GitHub credential can write to `CDM2/toveli`. Nothing was written. Removing the app's access to that repository is the only hard lock.
10. **Clean up:** revoke the throwaway key; delete `CDM2/Spike-test` once this pull request is merged.
11. **Review session:** recommended before the gate, for the reason below.

**Should a separate session attack R-01 and R-02 before Gate G1a? Yes.** P-000 requires it and neither report has had it. For R-02 the reason is specific: I wrote the permission service and its tests, so nobody independent has tried to break it. The reviewer should try to read a sibling's page by any route, challenge the reading of criterion 4, check the 20 questions for bias toward either side, re-derive the E-26 correction from the sources, and argue the case for E. One session.

## 7. Pass, fail or not run

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | A sub-organization's agent, running in Paperclip, gets its own and global pages only. A sibling's page is never returned. | **Pass** | Through the gateway, on both Paperclip versions, in both final runs: the Toveli agent read its three pages and the global page. No sibling, holding-only or personal marker appeared in anything it received across 17 requests. Asking for a sibling's page by ID or by path gave the same answer as asking for a page that does not exist. Passing another organization's name as an argument changed nothing. The sibling's agent saw none of Toveli's pages. Directly against the service: 35 of 35 tests, including the database refusing the application role when no session is bound. Two deliberate breaks show the tests bite: with the read rule made to return true, 18 tests fail; with the application role allowed to bypass row-level security, 23 fail (E-100, E-101). |
| 2 | The holding organization's agent reads sub-organization summaries. | **Pass** | Through the gateway the holding agent read both ventures' pages and no personal page. The stricter setting, summaries only, passes in the direct tests; it was not run through Paperclip (E-100, E-101). |
| 3 | The only path from personal to an organization is an explicit push. | **Pass** | The personal agent's briefing went in as pending. The holding agent could not see it. After a human approved it, the holding agent could, and Toveli's agent still could not. A venture's agent that tried to publish a briefing was refused. A health page written by a venture's agent was refused by the database even after a human approved that call in Paperclip. The briefing switch off, the personal space off, and a single-company setup pass in the direct tests (F-25 to F-27; E-100 to E-102). |
| 4 | Every call appears in Paperclip's audit log and in the service's own. | **Pass, with two limits** | Of 28 requests in a run, 27 were calls to tools that exist. All 27 are in Paperclip's audit log (22 matched by invocation ID, 5 by the request ID in the logged arguments) and all 27 are in the service's log under the same request ID, allowed and refused alike. Limit one: the 28th request named a tool that does not exist; Paperclip answered 404 and logged nothing. Limit two: a call made straight to the service, around Paperclip, is in the service's log only, as Paperclip's own documentation says it would be (E-89, E-104). I count this a pass because the unlogged request never became a call. Read as "every request", it fails on that one case. |
| 5 | One real Toveli task runs through this stack, and the same task runs on a single agent (N-04). | **Run on a made-up repository. Not run on Toveli.** | Toveli is read-only for this project on Cole's instruction, so the task was a small feature in a made-up repository whose rules live in the organization's second brain. Stack arm: a model-driven agent inside Paperclip `2026.1106.0` read the conventions from the permission service through the gateway. Plain arm: one agent with the same conventions as a file. Four runs of each on the scratch machine (one in the first final run, three in the second). All eight passed the nine hidden tests. Means over the three repeats: stack $0.038, 19.6 seconds, 5 turns, 11,927 input tokens; plain $0.035, 20.9 seconds, 4 turns, 7,934 input tokens. Each stack run's calls to the second brain are in both audit logs. The task ran through the stack. The stack did not beat the single agent: same outcome, about 10% more cost. A real Toveli task: **not run** (E-110). |
| 6 | Paperclip is upgraded one release without touching the permission service. | **Pass, after one install setting** | `2026.1023.0` to `2026.1106.0` with `npm install` over the old install. Paperclip applied 41 database migrations on start and kept every company, agent, connection and audit event. The same 37 checks passed before and after. The service's files and its running process were the same before and after. One obstacle: under a file-creation mask of 0002, which the newly created user had on the Ubuntu runner, the newer version's installer stops with "Copilot executable has unsafe permissions". With 022 it installs. That is a setting on the machine, not a change to Paperclip (E-112). |
| 7 | Governance coverage, and whether trigger 3 is met. | **Done. Trigger 3 is not met.** | Section 6.2. |
| 8 | Codebase map of Toveli against a plain agent. | **Done. The plain agent matched the map.** | Section 6.3. |

How the approval step behaves, since criteria 3 and 7 lean on it. A tool marked ask-first stops with HTTP 409 and an approval card on the task. The agent's session must be tied to a task, or Paperclip refuses outright. When the human approves, Paperclip itself runs the exact call that was approved, once. The agent's own retry is then refused as already used (E-102). The permission service still decides: the approved health write reached it and was refused.

## 8. D or E

**D.** Build on an unmodified Paperclip per organization with our own permission service beside it.

- Criteria 1 to 4 pass through an unmodified Paperclip on two releases. R-01 made those four the test for falling back to E.
- The upgrade changed 41 database migrations' worth of Paperclip and nothing of ours.
- Every governance control needed from Paperclip works in the free edition. The ones it lacks are small or are the product.
- The cost of D seen in the spike: two systems to run, an approval flow with its own rules, an install that fails under a common default, and audit and policy that stop at the gateway.

**Judgment.** This answers "can D work", and it can. It does not answer "is D better than one agent" for any real task: on the one task run both ways, a single plain agent did as well for less (section 7, criterion 5). D's reason to exist is permission, approval and audit across organizations. No customer has yet said they want that (R-01, H-A2).

## 9. What would change the answer

| If this happens | Then |
| --- | --- |
| A sibling page is ever returned through the stack, or the review session breaks criteria 1 to 3 | Stop. Fix the service first. This is a fault in our part, so it argues for neither D nor E. |
| Block rules, approvals or the audit log move to Paperclip's paid edition (trigger 3) | Price it in under F-28, or move that control into the permission service. If several move, E. |
| Two upgrades in a row break the connection or the checks (trigger 4) | E. One install obstacle in one upgrade is not that. |
| Paperclip is abandoned or relicensed (trigger 2) | Pin the last MIT release, then E on our own schedule. |
| A real multi-step venture task does no better through the stack than on one agent, after a fair trial | Keep the permission service and drop orchestration to the minimum, which is most of the way to E. |
| Outside customers will not accept a product resting on Paperclip (trigger 5) | E, decided at Gate G1. |
| Approvals need to cover what agents do in a shell, and gated tools prove too narrow | Sandbox per organization first; E only if Paperclip's adapters cannot run inside it. |

## 10. Gate G1a memo

**To:** Cole. **Decision:** Route A (a product) or Route B (a personal system on existing frameworks). **Date:** 2026-11-16.

**What the route check found.**

1. Orchestration is free and maintained by others. Paperclip ran four organizations, approvals, budgets, an audit log and an upgrade in this spike without a line changed (sections 6 and 7).
2. The part nobody sells still looks unsold: tiers above companies, a second brain filtered by tier, a one-way personal layer, approval on sharing (R-01 section 6). The spike built a working version in about 540 lines and it passed.
3. That part is small. Small means quick to build and quick for someone else to copy. Paperclip's own specification puts policy across companies in its paid tier (E-92).
4. Nothing here tested demand. No one outside has been asked or has paid (R-01, H-A2).
5. Cost is not the limit. The spike cost $1.68. Cole's plan may already include $200 a month of API credit (E-76).
6. A single agent matched the full stack on the one task tried both ways, and a plain agent matched the codebase map. Under N-04 neither multi-part design has earned its place on quality. Their case rests on permission and governance.

**What each route means next.**

| | Route A | Route B |
| --- | --- | --- |
| Build | The permission service as the product; Paperclip adopted behind an interface; Cole's ventures as first pilots | The same service, built only as far as Cole's own use needs |
| Next reports | R-04 (permissions and what the holding tier reads), R-05, then R-08 (pricing, with F-28) | R-04 only, lighter |
| First proof needed | An outside business pays | Cole uses it weekly for his own ventures |
| Main risk | Building for a buyer who has not been found | Building a private tool and calling it a product later |
| Cost of being wrong | Months | Weeks; B can become A later because the code is the same |

**What I would look at before deciding.** Whether the first three months of work differ between the routes. On this evidence they barely do: both start with the permission service, the personal layer and Cole's own ventures (F-15a, F-21). The routes part at the first outside pilot. That makes this decision cheap to take now and cheap to revisit at Gate G1.

**Open before the gate.** No review session has attacked R-01 or R-02; one is recommended first. Criterion 5 has not run on a real Toveli task. P-000 has no acceptance record of its own. Section 6.6 lists every decision asked of Cole.

The choice of route is Cole's.

## Sources

Evidence rows E-75 to E-113 in [`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md). Rows E-100 to E-112 are runs of this spike; their raw output is under [`spikes/r-02/results/`](../../spikes/r-02/results/). Paperclip source: `paperclipai/paperclip` at tags `v2026.1023.0` (`1b4c803816e82b0265c8422e1a804327a7ed8c54`) and `v2026.1106.0` (`d69631b01b9c658f80bf8bed389863dce82643e1`). npm packages as installed: `paperclipai@2026.1023.0`, integrity `sha512-PA2gLYoJKcmen1YaNr7jtyyZK2xNyW92XEedgZ82S1MMeMEB2kdmk1okRMD4aFUV4OZPFBwk76pV0jCM2Fuy0g==`; `paperclipai@2026.1106.0`, integrity `sha512-jcZrSB5DItxeDJGO7TccI0WcYca2IbBJxpbaKZN6kZp+isNIbVF2AgmfFQq394mjXD+TTHwS5P3AT6jjpqXbng==`. Scratch repository: `CDM2/Spike-test`, harness commits `54bf31e` and `7928416` for the two final runs. Toveli: `CDM2/toveli` at `0abafdc`, read only.
