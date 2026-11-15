# INV-000 — Capability inventory of prior code

Status: draft v0.1. As of 2026-11-15. Sources: `CDM2/azi-hub` main at 95d4feb, `CDM2/autonomous-startup-engine` at 159c1b1.

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
| React client: chat modes, agent roster, 3D graph | `core/src/client/` | Port selectively, later | Phase 5 |
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
