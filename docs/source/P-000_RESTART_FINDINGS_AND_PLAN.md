# P-000 — Agentic OS restart: findings and build plan

Status: proposed, not accepted. As of 2026-11-15. Markdown copy of the Claude doc of the same name.

Amended 2026-11-15, after R-01 was accepted. Two additions are appended below and dated: rows for the landscape table and notes on the research program. No earlier text is changed. This file was merged with pull request #1 (commit 2baba1b). Gate G0 accepted V-000; P-000 has no acceptance record of its own and is the plan in use.

## Bottom line

Start a new repository, keep AZI Hub running as prior art and as the first migration test, and build the first slice for yourself rather than for an unvalidated buyer.

- **Two earlier questions are settled.** v2.8 is lost, so main at v2.7 is the baseline. The colleague's repository is yours to use, by your account.
- **A route check comes before the rest of the research.** The generic platform layer is sold by Microsoft, OpenAI, Google and AWS and given away by Paperclip. If that leaves no room for a product, the plan re-routes to a personal, self-updating system assembled from existing frameworks.
- **Gemini's output is a question list, not research.** Five artifacts and a taxonomy of more than 50 topics contain no external evidence. Keep its discipline and drop its neutrality about things you have already decided.
- **AZI Hub is the stronger codebase.** About 29,500 lines of working TypeScript with real tenant isolation in Postgres. It has no user identity, almost no CI, and a hand-built runtime that current SDKs largely replace.
- **autonomous-startup-engine is mostly ideas.** Its engine is in-memory Python with no model or database client, and more than a quarter of the Python is a duplicated folder.
- **Toveli's document set is the right template, but its loop is too human-heavy for your goal.** Three tickets merged in 16 days with you reviewing every pull request. This plan keeps its controls and replaces blanket human review with risk tiers.
- **Sequence.** Reset and vision baseline, route check, the research the chosen route needs, specification, engineering handoff, a human-reviewed foundation, then a tiered autonomous loop.

## What I read

| Source | Coverage |
| --- | --- |
| Attached files | All read, including the CAT research-to-product plan and the AZI Hub project brief added later. The .docx and PDF taxonomies duplicate the Markdown files. |
| CDM2/azi-hub, main at 95d4feb (2026-06-23) | State and decision records, CI, migrations, tenancy, authentication, agent runner, compose and Dockerfile read; code measured by area. Not every file read line by line. |
| CDM2/autonomous-startup-engine at 159c1b1 | README, architecture document, engine samples, layout and duplication checked. Tests counted, not run. |
| CDM2/toveli at 525054d | All 43 Markdown files outlined. Process files read in full or in the sections that carry process. Product research files read by heading only. |
| Web | Eight searches on the current landscape. A first pass, not the landscape report. |

## The Gemini corpus

Five layers of planning with no evidence gathered.

**Keep**

- The three-way provenance split: implemented (AZI Hub), adjacent concept (Conducting AI), research program (CAT).
- The five contradictions, especially the personal layer against tenant isolation.
- The 2x2 of greenfield or brownfield against single or multiple organizations.
- The CAT operating rules: label every claim, deterministic software for permissions and money, benchmark multi-agent designs against a single-agent baseline.
- The falsification criteria, the skill-learning lifecycle and the authority spectrum.
- Slice 0, the governed research-to-decision workflow, as a candidate first slice.

**Drop or fix**

- **Neutrality about your decisions.** The CAT plan excludes the personal layer from the product boundary. You have said it stays.
- **The taxonomy as a work plan.** More than 50 subcategories with 14 fields each cannot be researched one by one.
- **A stale competitive view.** No file mentions Paperclip, Polsia, Microsoft Agent 365, Claude Managed Agents or AWS AgentCore.
- **The dossier as a source.** Its hypothesis list differs from the research-problem document it summarizes, and it repeats an implementation claim the code contradicts.
- **Numbering drift** across the research-problem file, the taxonomy and the manifest.

## AZI Hub

A working single-operator system, not yet a multi-user product. Main is at v2.7, merged 2026-06-23. About 29,500 lines of TypeScript (13,500 server, 8,900 client, 7,100 across 64 tools), 18 Postgres migrations, 23 test files.

**Worth carrying forward as patterns**

- Row-level security forced on tenant tables, a non-superuser application database user, and a 535-line isolation test.
- The framework and instance mount boundary, and the hardened container.
- North Star injection with a kill list, `log_decision`, and the weekly drift audit.
- The proposal, evaluation and gate schema, including the index that allows only one proposal to be implementing at a time.
- `create_org` as a deterministic scaffold with no model calls.
- Scrubbed-environment delegation to Claude Code, and the ephemeral agent lifecycle.

**Gaps found in the code**

1. **v2.8 is lost.** No v2.8 branch exists and the working copy was wiped. The v2.8 scope survives only as a list in notes.
2. **No user identity.** Authentication is one optional shared API key; without it the server runs open. The tenant comes from an `X-Org-Id` header the client sets. Isolation guards against bugs, not against a second user.
3. **CI runs two of 23 test files.** The only workflow triggers on push to main, runs those two, then deploys to the VPS over SSH as root. Nothing runs on pull requests.
4. **Stale dependencies.** Kuzu was archived in October 2025; the pinned 0.11.3 is its last release. Model IDs a generation old are hard-coded in 41 places.
5. **A hand-built runtime.** The agent loop, session compaction and sandbox providers duplicate what the Claude Agent SDK now supplies. The Firecracker provider is a stub.
6. **Instance code inside the framework.** Restaurant booking, crypto wallet, virtual card, CAPTCHA-solving, call and SMS tools sit in core beside an unrelated dashboard app and hard-coded agent names.
7. **Thin evaluation data.** The four golden sets hold 20, 10, 7 and 20 rows. The North Star's own expiry date passed on 2026-09-11.

## autonomous-startup-engine

A single commit that assembles pieces of several of your colleague's projects. It holds less working code than AZI Hub.

| Part | What is there |
| --- | --- |
| Coordination engine | 5,072 lines of standard-library Python with no model or database client. `coordination/` is a byte-identical copy of `engine/`. |
| Threat rules | One 5,161-line file of pattern rules mapped to OWASP and MITRE identifiers. |
| Agents | About 1,100 lines of Streamlit agents; the only place a model is called. |
| Web apps | 17,430 lines of TypeScript, of which 9,506 are UI-kit components. |
| Dashboard | 3,736 lines plus an Express API over Drizzle. No code links the Python engine to this database. |
| Tests | 103 Python test functions and one JavaScript test file. Counted, not run. |
| Missing | CI, containers, authentication, tenancy. |

**Ideas worth testing:** splitting deterministic workflows from model-driven work; verifying outcomes with probes; several trials on ambiguous work with small-sample correction; measuring each agent's contribution; activating agents only above a workload threshold.

**Ownership.** You confirmed the colleague handed this over for you to use as you wish. The repository's own documents still label nine components proprietary and patent-sensitive, so a one-line written confirmation is worth having if this ever ships commercially.

## Toveli as a template

**Copy:** the source manifest and its four separate records (authorization, acceptance, readiness, verification); the vision baseline and drift audit; the evidence ledger; the ENG-001 playbook and its six prompts; A-001 and A-002 with self-contained ticket cards; repository controls (protected main, required checks named after their first real run, read-only workflow token, pinned actions, frozen lockfile, CODEOWNERS, a pull-request template with checks actually run); fail-closed configuration and kill switches; the rule that "not run" is a valid answer.

**Change:** the review model (risk tiers instead of you on every pull request); document weight (one file per ticket, a machine-readable status file, a short rolling state file); acceptance cases written as failing tests before the build session; no assumption that you can review at Toveli's rate.

## What changed in the landscape

First pass from search results; report R-01 does it properly.

| Area | State in November 2026 |
| --- | --- |
| "AI company" tools | [Paperclip](https://paperclip.ing/product/): MIT-licensed, org charts, budgets, heartbeats, governance, multiple companies. [Polsia](https://noqta.tn/en/news/polsia-ai-autonomous-company-30m-funding-2026) raised $30M in May 2026. |
| Enterprise control planes | [Microsoft Agent 365](https://futurumgroup.com/insights/microsoft-agent-365-turns-shadow-ai-into-a-governed-asset-class/) GA on 2026-05-01. [OpenAI Frontier](https://openai.com/index/introducing-openai-frontier/) launched February 2026. Google, AWS, Salesforce and ServiceNow [compete for the same position](https://futurumgroup.com/insights/who-will-control-the-enterprise-agentic-workforce-cios-face-a-new-platform-war/). |
| Agent runtime | [Claude Managed Agents](https://www.helpnetsecurity.com/2026/04/09/claude-managed-agents-bring-execution-and-control-to-ai-agent-workflows/) public beta April 2026: hosted sandboxes, sessions, credentials. |
| Protocols | MCP and A2A both under the Linux Foundation's [Agentic AI Foundation](https://axios.com/2026/08/17/a2a-agentic-ai-foundation-open-ai-standards) since August 2026. |
| Graph store | [Kuzu archived](https://www.theregister.com/2025/10/14/kuzudb_abandoned/) October 2025. |

Rows added 2026-11-15 from R-01 (its sections 1 and 10). Evidence IDs point to `../research/EVIDENCE_LEDGER.md`.

| Area | State in November 2026 |
| --- | --- |
| Hosted personal agents | Claude Duet (research preview since 2026-10-21, individual plans), ChatGPT dots (since 2026-09-29, from $100 a month), Meta's Muse and Muse for Small Business (September 2026, free to $100 a month) and Ariso's Ari. Each is one agent per person with a small memory. None was found with several organizations under one owner (E-27 to E-31, E-65). |
| Agent memory layers | Cognee, Mem0, Zep, Letta and MintMCP sell scoped memory for fleets of agents as components: permissions per dataset, user and agent scopes, group access. None was found in the tiered form of a person, a holding organization and sub-organizations (E-67). |
| AI automation agencies | Many small firms quote $1,500 to $5,000 to set up one or two workflows for a small business and $500 to $1,500 a month to maintain them. These are quoted prices, not purchase data (E-72). |

Candidates for what vendors do not cover, to test: a person-owned layer that connects to organizations; a holding layer with brokered sharing between sub-organizations; self-improvement gated by evidence; verification of outcomes.

## Restart shape

**Fixed by you** (full list in V-000 section 2): the personal layer is in the product and optional for a customer, with scope the user chooses, including financial and health areas; super-organization and sub-organization structure stays; new and existing enterprises both in scope; humans hold creative direction and key decisions; governed self-improvement; you are the first user; setup consulting is allowed as onboarding, with no custom framework per customer; Claude-first with easy model choice; self-hosted for your own use; a build budget of up to $1,000 a month.

**Open, for the research:** first external customer and wedge; role agents, composed capabilities or one agent with workflows; build or adopt for runtime, orchestration, memory and policy; Claude-first or model-agnostic; hosting; business model.

**New repository.** Identity has to become the root of the data model: a person, their personal space, their memberships in organizations, their roles. That touches every table and route in AZI Hub.

**Route check first.**

- **Route A, product.** The plan as written, with you as first user and a commercial thesis tested in parallel.
- **Route B, personal system.** A self-updating system for your projects and personal life on existing runtimes and tools, with custom code only for the glue nobody supplies.

Route B removes the customer and pricing report, licensing and blank-tenant packaging, most of the service-management layer and the larger document set. It keeps identity, secrets handling, backups, CI, the vision baseline, ADRs, ticket files and the tiered loop.

**Your Route A hypothesis.** Off-the-shelf frameworks may exist but not in a form that non-technical people, or organizations with existing operations, can set up alone. The product is onboarding plus an ecosystem that keeps them, with a personal layer vendors do not offer. Candidate customers are existing large organizations, new well-funded organizations and non-technical solopreneurs. R-01 tests the claims (V-000 section 5) and, with R-08, names one first wedge among the three groups.

## Phases and gates

1. **Phase 0, Reset.** Repository and manifest. V-000, the vision baseline and drift audit. Capability inventory for AZI Hub and autonomous-startup-engine. *Gate G0: you accept V-000.*
2. **Phase 1a, Route check.** R-01 maps the category and, for each capability you want, the best existing tool and the missing glue. R-02 tests the leading runtime in a spike. *Gate G1a: you choose Route A or Route B.*
3. **Phase 1b, Research.** The remaining reports the route needs, each attacked in a separate review session. *Gate G1: thesis, first slice and non-goals accepted.*
4. **Phase 2, Specification.** Route A: V-001 product and business plan, V-002 build specification. Route B: one short specification. *Gate G2.*
5. **Phase 3, Engineering handoff.** ENG-001 playbook, A-001 architecture, ticket files, ADRs, threat model, starter CLAUDE.md. *Gate G3: foundation tickets authorized.*
6. **Phase 4, Foundation.** Five to eight tickets, all reviewed by you: repository and CI, identity, data boundaries with isolation tests, approvals, audit log, runtime adapter, evaluation harness, loop orchestrator. *Gate G4: the review agent's findings are compared with yours before any auto-merge.*
7. **Phase 5, Autonomous build-out.** Personal layer, organization and sub-organizations, governed self-improvement, AZI Hub data migration. Route A adds multi-user collaboration. *Gate at each milestone: you run the demo.*
8. **Phase 6, Operations.** Runbooks, restore drill, release records. Route A adds packaging and licensing. *Gate G6.*

## Research program

| Report | What it decides |
| --- | --- |
| R-01 Category and competitors | Whether a product has room, and which existing tools already cover each capability. Hands-on teardowns of Paperclip and two control planes. |
| R-02 Runtime and harness | Agent SDK, Managed Agents or an own loop; durable execution; sandboxing. Ends in a spike. |
| R-03 Organization model | Role agents, composed capabilities or a single agent; brokerage between organizations. |
| R-04 Memory and knowledge | Compiled wiki, platform memory or graph; the personal and organizational boundary. |
| R-05 Identity and governance | People, agents and delegated authority; policy engine; approvals; audit. |
| R-06 Self-improvement | Skill lifecycle, evaluation set sizing, what may promote automatically. |
| R-07 Security and operations | Agent threat model, secrets, supply chain, scoped standards, lean service management. |
| R-08 Customers and economics | Segments, pricing, unit costs, open core or license. Route A only. |
| R-09 Brownfield onboarding | Import of an existing organization, with AZI Hub as the case. |

R-01 and R-02 run first as the route check. R-05 follows on either route. Desk research never counts as customer validation.

Notes added 2026-11-15. R-01 section 10 proposed scope notes for four reports. R-02's are in effect on Cole's instruction of 2026-11-15. The others apply when those reports are scoped.

- **R-02.** Besides the desk research in the table above, spike R-01 option D against the six pass criteria in R-01 section 7, in a throwaway environment, with a Toveli task as the test job and option E as the fallback. Cole added two criteria: (7) a governance coverage table that sorts each required control into free in Paperclip, paid edition only, or ours to build; (8) a codebase map of Toveli, scored against a plain coding agent as the N-04 baseline.
- **R-04.** Generalize AZI Hub's visibility model from a hard-coded list to the tier map. Decide wiki, retrieval or both by collection size. Include Paperclip's LLM Wiki plugin in the comparison. Decide what the holding tier reads of a sub-organization's codebase map.
- **R-06.** Keep the evaluation outside what the improvement loop can edit.
- **R-08.** After the pilots on Cole's own ventures, two or three paid local pilots, plus interviews where a pilot is declined.

## Build, review, integrate loop

1. **Planner** picks the next ready ticket and confirms its dependencies are merged.
2. **Test author** turns the card's acceptance and failure cases into failing tests.
3. **Builder** implements on a branch until tests and CI pass, then writes the evidence table.
4. **Reviewer**, read-only, checks the diff against the card, the ADRs and the threat model.
5. **Fixer** resolves findings on the same branch; the reviewer re-reviews only the changed code.
6. **Integrator** merges or escalates by tier, updates status and records the commit.

| Tier | Covers | Merge rule |
| --- | --- | --- |
| 0 | Docs, tests, UI, non-sensitive modules | Auto-merge on green CI and a clean review |
| 1 | Domain logic | Auto-merge, plus your weekly sample audit |
| 2 | Identity, tenancy, policy, secrets, migrations, CI, money | Your approval required |

Stops that always reach you: a ticket that fails review twice, any change to CI or branch rules, a test weakened to pass, a budget cap reached, every production promotion. Auto-merge is realistic for tiers 0 and 1 after Gate G4, not for the security boundary or product judgment.

## Engineering, security and operations baseline

| Area | Baseline |
| --- | --- |
| Source control | Protected main, squash merges, no bypass actors, required checks, CODEOWNERS on tier-2 paths |
| CI | Frozen-lockfile install, typecheck, lint, unit and database tests on every pull request; secret and dependency scans; pinned actions; read-only token |
| Releases | Build once; record commit, CI run, image digest, SBOM and schema version; migrations by a separate authorized job; human-only promotion |
| Secure development | NIST SSDF as the practice list; OWASP ASVS scoped per feature; no conformance claim without evidence |
| Agent security | Threat model before the first sensitive ticket; permissions before retrieval; model output never authorizes spending, publishing or access; secrets out of context windows |
| Service management | Service register, change records through pull requests, incident and problem records, restore drills |
| Kill switches | Capability approvals per environment, admission stops, fail-closed production boot |

## Sources

Repository findings come from the three private repositories at the commits listed above. Web facts come from search-result excerpts of the linked pages, accessed 2026-11-15; pages were not opened in full.
