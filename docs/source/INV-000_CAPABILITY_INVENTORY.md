# INV-000 — Capability inventory of prior code

Status: draft v0.3, 2026-11-15. v0.3 appends the section "Amendments, 2026-11-15 (v0.3)" at the end: two amendments R-01 section 10 proposed, and three rows for the codebase map (capability C-23). The v0.2 rows are unchanged.

Status line as written for v0.2: draft v0.2 (adds conversation modes and the organization graph as their own rows). As of 2026-11-15. Sources: `CDM2/azi-hub` main at 95d4feb, `CDM2/autonomous-startup-engine` at 159c1b1.

Dispositions: **Pattern** = carry the idea, rebuild the code. **Port** = move the code with changes. **Decide** = a research report settles it. **Drop** = do not carry.

## AZI Hub

| Capability | Where | Disposition | Settled in |
| --- | --- | --- | --- |
| Tier model: personal, super-organization, sub-organizations; push-only upward, zero between organizations | `config/tenants.json`, brief section 2 | Pattern (requirement) | V-000 |
| Row-level security with FORCE, non-superuser app role, isolation tests | `pg-migrations/002`, `core/tests/tenant-isolation.test.ts` | Pattern | R-05 |
| Tenant from `X-Org-Id` header; optional shared API key | `core/src/server/tenancy/TenantContext.ts`, `index.ts` | Drop | R-05 |
| Hard-coded user and agent names | prompts, configs | Drop; replace with an identity model | R-05 |
| North Star injection, kill list, staleness banner | `AgentRunner.ts` | Pattern | R-03 |
| `log_decision` and weekly drift audit | `core/tools/logDecision.tool.ts` | Pattern | R-03, R-06 |
| `create_org` deterministic scaffold | `core/tools/createOrg.tool.ts` | Pattern | R-03 |
| Three-layer memory: raw, compiled wiki, indexes; session-close synthesis | `core/src/server/memory/` | Decide against platform memory | R-04 |
| Wiki visibility broker with row-level security | `pg-migrations/017`, `Database.ts` | Pattern | R-04, R-05 |
| Kuzu graph index | `core/package.json` | Drop or replace (archived upstream) | R-04 |
| Agent loop, compaction, MCP client | `AgentRunner.ts`, `AgentManager.ts` | Decide; likely replaced by an adopted runtime | R-02 |
| Tool Search (retrieval over tool schemas) | `ToolSearchService.ts` | Decide against native tool handling | R-02 |
| Sandbox providers; Firecracker stub | `core/src/server/sandbox/` | Decide; likely replaced | R-02 |
| Ephemeral agent lifecycle | migration 017, tools | Decide (depends on runtime) | R-02, R-03 |
| Proposal, evaluation and gate schema; prompt variants | `pg-migrations/006` | Pattern | R-06 |
| Four-pass skill auditor | cron, prompts | Pattern | R-06 |
| Golden evaluation sets (57 rows in total) | `eval/*.jsonl` | Rebuild larger | R-06 |
| Headless Claude Code delegation and `ralph_loop` | `core/tools/` | Superseded by the build loop | ENG-001 |
| Container hardening and mount boundary | `docker-compose.yml` | Pattern | R-07 |
| Deploy workflow: push to main, two test files, SSH as root | `.github/workflows/deploy.yml` | Drop | ENG-001 |
| Conversation modes: single agent, group, and ordered chain (agents run in a set 1-2-3 order) | `core/src/client/hooks/useChat.ts`, `useGroupChat.ts`, `components/OrgChatPanel.tsx` | Pattern (requirement to keep all three); mechanism depends on the orchestration model | R-03 |
| React client: agent roster, 3D knowledge graph | `core/src/client/` | Port selectively, later | Phase 5 |
| Reservation booking (Resy, OpenTable) | `core/tools/` | Port to the personal layer first | Phase 5, milestone 1 |
| Crypto wallet, virtual cards, balance monitors, SMS, call bots | `core/tools/`, `callbot/`, `sms/` | Instance-level; port only on need | Phase 5 |
| CAPTCHA solver | `core/tools/captchaSolve.tool.ts` | Drop | — |
| `originatoriq` app inside core | `core/src/originatoriq/` | Remove; separate project | — |
| Legacy SQLite migrations and dependency | `migrations/`, `node-sqlite3-wasm` | Drop | — |

## autonomous-startup-engine

| Capability | Where | Disposition | Settled in |
| --- | --- | --- | --- |
| Deterministic workflow registry | `workflows/deterministic.py` | Pattern | R-03 |
| Queue coordinator and recovery router | `engine/engine/` | Decide against a single-agent baseline | R-03 |
| Tournament with small-sample shrinkage | `engine/engine/tournament.py` | Decide | R-06 |
| Contribution attribution (Shapley) and context router | `engine/engine/context_router.py` | Decide | R-03, R-06 |
| Threshold-gated activation ("clutch") | `engine/engine/clutch.py` | Decide | R-03 |
| Meta-learner and agent proposal engine | `engine/intelligence/` | Decide | R-06 |
| Knowledge wiki: ingest, propose, lint, evolve | `intelligence/wiki.py` | Compare with AZI Hub wiki | R-04 |
| Execution observer and SKILL.md export | `intelligence/*.js` | Decide | R-06 |
| Threat rule library mapped to OWASP and MITRE | `security/threat_engine_v2.py` | Input to the threat model | R-07 |
| A2A gateway and interceptor | `engine/protocols/`, `security/` | Compare with the A2A standard | R-02, R-07 |
| Sales and meetings apps, Streamlit agents | `deployments/` | Drop (venture-specific demos) | — |
| Dashboard and Drizzle schemas | `dashboard/`, `shared/db/` | Reference only | — |
| Duplicate `coordination/` folder | `coordination/` | Ignore (copy of `engine/`) | — |

## Concepts not in code

| Capability | Where | Disposition | Settled in |
| --- | --- | --- | --- |
| Organization graph ("enterprise brain"): people, agents, procedures and tools as nodes, with ownership and access as edges, and named human roles per agent | Conducting AI concept, `prior-art/gemini/CAT_HANDOFF_DOSSIER.md` part II. Never built. AZI Hub's nearest piece is the wiki knowledge graph and agent cards. | Decide | R-04 for the graph, R-05 for roles and access |

## Amendments, 2026-11-15 (v0.3)

The rows above are kept as written in v0.2. Where a row is amended here, this section governs.

### Rows amended (R-01 section 10)

| Row | Change | Source |
| --- | --- | --- |
| Reservation booking (Resy, OpenTable) | Disposition becomes **outside the build**. The agent stays on the old VPS and runs only on sites that allow agents. "Port to the personal layer first" and "Phase 5, milestone 1" no longer apply. | V-000 F-08a and F-15a; R-01 section 11 |
| Three-layer memory: raw, compiled wiki, indexes | Disposition stays Decide. The comparison R-04 makes now includes Paperclip's alpha LLM Wiki plugin, which keeps one company's wiki with sources, backlinks, revisions and a maintainer agent, beside platform memory. | R-01 section 2; ledger E-47 |

### Rows added: the codebase in the second brain (capability C-23, V-000 F-24)

Read in `CDM2/azi-hub` at 95d4feb on 2026-11-15.

| Capability | Where | Disposition | Settled in |
| --- | --- | --- | --- |
| Codebase index in the second brain: one wiki page per directory of the server and client source, holding the file list and the exported names found by a regular expression. No model calls. Written once, at first boot, behind a seed flag. | `core/src/server/memory/BrainSeedWriter.ts` (`seedCodebaseIndex`) | Pattern. It covers AZI Hub's own code only, stops at directory level, and is not refreshed after the first seed. | R-02 (spike criterion 8), R-04 |
| Provenance tags on brain pages: `source_type` has `codebase` and `agent_output` as explicit values. Human-written context is spread over `document`, `daily_note` and `voice_memo`, not one tag. Codebase pages also carry `readers` and `writers` lists of agent ids. | `orgs/azi-hub/vault/SECOND_BRAIN_TAXONOMY.md`; `BrainSeedWriter.ts` | Pattern. Supplies most of the codebase, agent-written and human-written distinction F-24 asks for; a single human-written marker is missing. | R-04 |
| "Cartographer": deterministic extraction into a manifest, then a question-answering agent that reads the manifest first and raw code second | Not in the repository at 95d4feb; a search for the term found nothing. Recorded from Cole's earlier project notes: founder input, not code. | Decide, against a plain coding agent (N-04) | R-02 (spike criterion 8) |
