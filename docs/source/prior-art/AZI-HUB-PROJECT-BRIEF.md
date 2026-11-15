# AZI Hub — Project Brief for External Research Review

*Synthesized from the repository's markdown corpus (ARCHITECTURE.md, IMPLEMENTATION.md, CLAUDE.md, DECISIONS.md, CURRENT_STATE.md, v2.2-RESTRUCTURE.md, v2.3-AUTOPILOT.md, refactor/PROGRESS.md, per-org north-star.md and vault docs). Written to be attached to a research prompt evaluating whether this design is still valuable in the current agentic-OS landscape.*

---

## 0. One-paragraph summary

AZI Hub is a self-hosted, single-monorepo, multi-tenant agent operating system. It models a holding company — a personal tier, a meta-org tier, and N subsidiary orgs — where every tier is a *tenant* with its own agents, memory vault, tool allowlist, and credentials, all running on **one shared runtime**. The three load-bearing ideas are: (1) tenancy is a runtime property enforced in the auth and query layers, not a filesystem or git property; (2) long-horizon goal drift is the primary failure mode of multi-agent systems, countered by a short "North Star" document injected at the top of every agent turn; (3) the framework improves itself on a fixed cron cadence through researcher agents that write proposals, an eval harness that A/B tests them, and a human gate that must approve anything with real blast radius.

---

## 1. Project goals

### Stated purpose
Dual-purpose from the start:
1. **Operate the founder's own companies** via agent organizations.
2. **Eventually license the platform** to external customers — which is why there is a hard framework/instance separation (see §6).

### The meta-org's own North Star (verbatim intent, `orgs/azi-hub/vault/north-star.md`)
> AZI Hub is an AI-native holding company that builds, capitalizes, and operates a portfolio of autonomous ventures — each run by its own agent organization, all compounding into one self-improving system.

**12-month success criteria as written:**
- Three operating subsidiaries each running autonomously with their own North Star, CEO agent, and skill governance.
- A working org lifecycle: idea → scaffolded, staffed, governed org in a single guided session via `create_org`.
- A measurable self-improvement loop: tool-selection accuracy, memory-query precision, and tokens-per-turn all trending favorably month-over-month, evidenced in COO traces.
- Zero cross-tenant data leakage and zero unreviewed agent-initiated changes to production.

**Explicit kill list (the anti-goals — the most important governance artifact in the system):**
- No agent pushes to production, moves money, or changes another org's state without explicit human approval.
- No one-off consulting/services work — only durable, compounding ventures.
- No spinning up an org or agent for a task that fits in a few tool calls; spawning must earn its cost.
- No tenant mixing: each subsidiary's data, memory, and decisions stay inside its own boundary.
- No auto-promotion of officer-agent prompts or strategic decisions; those stay human-gated.

---

## 2. The tier model ("Alphabet layer" topology)

The architecture was originally specced under Alphabet/Google/YouTube/Waymo codenames and renamed in v2.2 to AZI Hub / AltZ Capital / AltZ Sandbox / AltZ Media. **Note: `IMPLEMENTATION.md` and `refactor/PROGRESS.md` still use the old `orgs/alphabet/` paths — this is stale naming, not a second system.**

```
TIER 0 — PERSONAL (layer zero, "second brain")
  Human's own support team. Life vault in Obsidian-compatible markdown.
  Agents: Chief of Staff, cmo-memory-personal, coo-orchestration-personal.
  Sees: everything the human lets it see.
        │  delegates strategic goals downward
        ▼
TIER 1 — AZI HUB (meta-org / the "Alphabet layer")
  Alt Z (superadmin/CEO), Chief Memory Officer (CMO-M / Reed),
  Chief Orchestration Officer (COO / Oliver), Ralph (CTO), Marcus (CFO),
  Clara (Chief of Staff), Scout (Skill Auditor), researchers (Finn/Arlo).
  Shared "company brain" vault. Sees: all orgs + what personal publishes up.
        │
   ┌────┴────┬─────────────┐
   ▼         ▼             ▼
TIER 2 — SUB-ORGS: AltZ Capital (quant fund) │ AltZ Sandbox (experiments) │ AltZ Media (content)
  Each: own CEO, own CTO, own skill-auditor, own vault, own memory,
        own skills, own MCP bindings, own ui.config.json.
```

Canonical registry: `config/tenants.json` (id, tier, display_name, parent, plus `permission_grants`).

### Permission flows (the core tenets)
| Edge | Rule |
|---|---|
| Personal → AZI Hub | **Push only, explicit.** The human publishes briefings/goals. AZI Hub never reads personal by default. |
| AZI Hub → Orgs | Reads all. Can write directives; cannot silently modify org internals. |
| Orgs → AZI Hub | Each org publishes a structured periodic *state* document. AZI Hub reads those, not the raw org vault (cost + noise). |
| Org ↔ Org | **Zero by default.** Must route through AZI Hub. Two orgs coordinating is a decision the meta-org makes, never an emergent behavior. |
| Human → any tier | Superadmin. Always. |

This is the "channel-owned auth" pattern: permissions attach to the org, and an agent's access is a function of which org it belongs to. A worker spawned inside AltZ Media inherits AltZ Media's permission set automatically — zero config, zero drift.

### Officer instancing
Rather than three distinct officer agents, there are **two officer patterns instantiated once per tier**: `cmo-memory-{personal,azi-hub}` and `coo-orchestration-{personal,azi-hub}`. One codebase, N instances, different permission scopes. The personal Chief of Staff and Alt Z are **peers, not superior/subordinate** — the Chief of Staff represents the human when asleep; it does not own AZI Hub.

### Why one repo
Explicit ADR (`DECISIONS.md`, 2026-04-23): monorepo over polyrepo, because the framework's own self-improvement agent needs to push a cross-cutting change to all orgs in one commit; because the mount-security audit runs once; and because *isolation lives in the auth and query layers, not in git topology*.

---

## 3. Repository outline

```
azi-hub/
├── core/                       # THE RUNTIME — one copy, all tiers
│   ├── src/server/             # Fastify, AgentRunner, ToolRegistry, MemoryManager,
│   │                           #   ToolSearchService, CronService, eval/, research/, storage/
│   ├── src/client/             # React SPA (react-router, tenant switcher)
│   ├── tools/                  # *.tool.ts — ~64 tools, default-export ToolDefinition
│   ├── tests/
│   └── ralph/                  # CTO agent's iterative-loop working memory (prd.json, progress.txt)
│
├── personal/                   # TIER 0
│   ├── config/agents.config.json + config/prompts/*.md
│   ├── vault/{raw,wiki}/       # raw = immutable capture; wiki = LLM-compiled
│   └── memory/
│
├── orgs/
│   ├── azi-hub/                # TIER 1 meta-org
│   │   ├── config/agents.config.json + config/agents/<id>.card.json
│   │   ├── vault/              # north-star.md, okrs.md, strategy.md,
│   │   │                       #   decisions/, playbooks/, proposals/{memory,orchestration,
│   │   │                       #   architecture,skills,goal-drift}/, ethos/, audit/
│   │   ├── CLAUDE.md ARCHITECTURE.md IMPLEMENTATION.md DECISIONS.md CURRENT_STATE.md
│   │   ├── memory/  skills/    # cross-org skills inherited by children
│   ├── altz-capital/ altz-sandbox/ altz-media/   # TIER 2, same shape + mcp-connectors.json
│
├── shared/                     # skills/ (vendored submodules + custom), tools/, ui-widgets/
├── config/tenants.json         # master tenancy map
├── pg-migrations/              # 018+ SQL migrations — HUMAN-ONLY, agents never write here
├── eval/                       # *.jsonl eval datasets + phase8-e2e.md runbook
├── docs/sprints/               # per-sprint specs (e.g. v2.8-stabilization.md)
├── refactor/                   # PROGRESS.md, GAP_PROGRESS.md, LEGACY_AUDIT.md
├── scripts/                    # audit-mounts.sh, deploy, smoke harnesses
└── ARCHITECTURE.md IMPLEMENTATION.md CLAUDE.md DECISIONS.md CURRENT_STATE.md
    V2.2-RESTRUCTURE.md V2.3-AUTOPILOT.md   # root-level, NOT mounted into the agent container
```

### Markdown inventory — what each root doc is for
| File | Role |
|---|---|
| `ARCHITECTURE.md` | The design bible. Parts 1–9: monorepo rationale, tier topology, repo layout, officer roles, three-layer memory model, DB choice, phase roadmap, and the v2.2/v2.5 "current ground truth" sections. **Closest thing to a single-file answer.** |
| `IMPLEMENTATION.md` | Phases 1–8 with work items and hard exit criteria per phase, plus Parts D/E/F (UI contract, self-improvement scaffolding, ops). Uses stale `alphabet` naming. |
| `CLAUDE.md` | Operator briefing for Claude Code sessions. Stack, critical paths, conventions, what-not-to-touch. Explicitly the *only* CLAUDE.md at root level; per-org CLAUDE.md files are separate and serve agents. |
| `DECISIONS.md` | Append-only ADR log. One dated entry per architectural decision, with the rejected alternative recorded. |
| `CURRENT_STATE.md` | Rotating snapshot — working / in-progress / broken / next. Reflects NOW, not history. |
| `V2.2-RESTRUCTURE.md` | The most research-dense doc. Contains the North Star pattern derivation, tool-overload research, Tool Search spec, and the hardened self-improvement loop (SCOPE pattern). |
| `V2.3-AUTOPILOT.md` | The autonomous dev pipeline: agents orchestrating Claude Code headlessly, CI/CD auto-deploy, and the framework/instance security boundary. |
| `SECOND_BRAIN_TAXONOMY.md` | Memory-agent-owned taxonomy for wiki page types and vault subfolders. |
| `refactor/PROGRESS.md` | Per-phase build log with commit SHAs and exit-criterion proof. |
| `eval/phase8-e2e.md` | Manual operator runbook proving the self-improvement chain end-to-end. |

### Documentation-as-anti-drift
A five-file discipline is treated as a first-class architectural mechanism, not overhead: `CLAUDE.md` (briefing), `ARCHITECTURE.md` (what exists), `DECISIONS.md` (append-only, never edited), `CURRENT_STATE.md` (rotated every session), `SECOND_BRAIN_TAXONOMY.md`. Every org gets its own copy of the operational five. Session-closing updates are named the highest-leverage habit in the project.

---

## 4. North Star architecture — goal governance

The design premise: **goal drift, not missing capability, is the #1 production failure mode of long-running multi-agent systems.** Three mechanisms counter it.

### 4.1 North Star injection
Each org has `orgs/<org>/vault/north-star.md` (personal uses `personal/vault/north-star.md`). `AgentRunner.injectNorthStar()` prepends `## NORTH STAR — Your primary directive` plus the file contents to the **top of every system prompt, every turn**. It costs no extra API call, re-grounds automatically, and passes through silently when the file is absent.

Constraints that make it work:
- **≤ ~600 words.** Longer and agents stop reliably reading all of it.
- **Frontmatter versioned** (`version`, `last_updated`, `last_reviewed`, `expires`, `approved_by`). Staleness produces an injected banner when past `expires` (90-day default).
- **Fixed five sections:** one-sentence purpose / 12-month success / **kill list** / decision authority / brand voice. The kill list is called out as the single most important section for preventing drift.
- Authoritative — overrides any conflicting instruction.

Layered briefing: orgadmin/superadmin agents additionally get the org's `CLAUDE.md` + `ARCHITECTURE.md` prepended below the North Star; workers get the North Star only; spawn-capable agents additionally get the ephemeral-agent protocol.

Reference documents (business context, security model, operating model) live in `vault/ethos/` and are **queryable but never injected** — injection is reserved for the one canonical file.

### 4.2 `log_decision` trail
CEOs/CTOs must call `log_decision` *before* committing resources. It writes a dated record to `orgs/<org>/vault/decisions/YYYY-MM-DD-<id>.md` capturing summary, reasoning, **`north_star_alignment`** (a required field), and alternatives considered. This creates the audit substrate the drift auditor consumes.

### 4.3 Weekly goal-auditor
A scheduled responsibility on the existing memory officer (deliberately *not* a new agent): every Monday 06:00 UTC, read the last 7 days of decisions across all orgs, check each against that org's current North Star version, and write anything inconsistent to `orgs/azi-hub/vault/proposals/goal-drift/<date>.md` for human review. **It changes nothing autonomously.**

---

## 5. Org lifecycle — how a new organization is created

Three-step **interview → scaffold → fill**, deliberately split so the deterministic part is auditable and the judgment-heavy part stays where full context lives.

**1. Interview (conversation layer).** The superadmin agent interviews the human: purpose, 12-month success, what it will *not* do, decision authority, brand voice. Optionally web-researches the space first.

**2. Scaffold (`create_org` tool — superadmin only, deterministic, idempotent, no LLM generation inside it).** Given `org_id` (kebab-case), `display_name`, `description`, optional `parent` (default `azi-hub`), it:
- appends the tenant to `config/tenants.json` at tier 2 under the parent;
- creates `orgs/<org>/{config,vault,vault/ethos,vault/decisions,memory,skills}`;
- writes `agents.config.json` containing a `ceo-<org>`, a `skill-auditor-<org>` (pre-scheduled `0 8 * * 1`), and `cross_org_refs` to the personal Chief of Staff and to Alt Z so those appear as read-only external agents in the new org's sidebar;
- writes a default `ui.config.json`;
- lays down `<!-- FILL: … -->` template stubs for `vault/north-star.md`, `vault/ethos/{business-context,security-model}.md`, and the five operational docs.

**3. Fill (conversation layer).** The interview answers are routed to the **owning org's CTO** — Ralph for azi-hub, the sub-org's own CTO otherwise. Ralph never writes cross-org. Stubs get replaced via `web_browse` + `create_file`.

Deliberately *not* generated at creation time: `vault/decisions/` (populated by `log_decision` as the org operates) and `vault/okrs.md` (written by the org CEO after a first two-week operating period, not upfront).

---

## 6. Self-optimization — how the framework improves itself, automatically

### 6.1 The evolution gate (nothing self-modifies without passing through this)
```
[Researcher agent] → writes proposal.md → [COO] reads, runs A/B eval
        ↓                                        ↓
  proposals/*.md                          ab_eval_runs (delta per grader)
                                                 ↓
                                    [Alt Z] reviews, recommends
                                                 ↓
                                    [Human] approves / rejects   ← HMAC token, single-use, expiring
                                                 ↓
                                    [Ralph] implements in a PR
                                                 ↓
                                    [Evals run on the PR branch]
                                                 ↓
                                    merge iff evals green
```
Prompt changes (low blast radius, fully reversible) may auto-approve when the eval delta clears a threshold. **Code changes always pass through the human.**

### 6.2 The measurement substrate (built before any evolution)
- Every agent turn emits a trace: tenant, agent, model, tokens in/out, latency, tools called, `tools_available` / `tools_loaded` / `tools_used`, outcome label, parent turn id.
- Grader suite: `tool_success_rate`, `agent_response_quality` (LLM-as-judge), `tokens_per_turn_by_model`, `memory_query_precision`.
- Eval datasets as `.jsonl`: memory retrieval with known-correct page IDs, agent routing with labeled recipients, code quality with reference implementations, cost per turn. The docs state flatly: *without these, self-improvement is theater.*
- Schema (migration 006): `researcher_staging`, `proposals` (status lifecycle draft→recommended→approved→implementing→merged|rejected, with a partial unique index enforcing **at most one proposal in `implementing` at a time**), `ab_eval_runs`, `prompt_variants` (exactly one active variant per agent).

### 6.3 The recurring cadence (all seeded idempotently into `scheduled_tasks`, run by `CronService`)
| Cadence | Agent | Job |
|---|---|---|
| Hourly | staging workers | Fetch arxiv (cs.SE/cs.DC/cs.MA), GitHub, MCP registries, SDK commits, personal inbox → `researcher_staging`, deduped by hash |
| Sun 03:00 | CMO-M | Memory synthesis pass |
| Sun 04:00 | memory-researcher | Cluster staged inputs → **one** proposal to `vault/proposals/memory/` |
| Sun 05:00 | orchestration-researcher | Cluster staged inputs → **one** proposal to `vault/proposals/orchestration/` |
| Mon 06:00 | CMO-M | Goal-drift audit against North Stars (§4.3) |
| Mon 08:00 | `skill-auditor-<org>` (one per org) | 4-pass skill review (§6.4) |
| 1st of month 09:00 | orchestration-researcher | **Architecture self-audit** (§6.5) |
| Continuous | SessionCloseWorker | 5-min poll, 30-min idle → compile session into a wiki page + raw_event |
| Weekly | ephemeral cleanup cron | Hard-delete soft-deleted ephemeral agents past 30 days |

Proposal discipline is enforced in the system prompts: **one proposal per run**, five fixed sections (Problem / Proposed Change / Expected Eval Impact / Implementation Sketch / Cost-Risk / Sources), never propose code you can't outline at file-path granularity, and never propose changes to ARCHITECTURE.md or IMPLEMENTATION.md.

### 6.4 Skill governance (the tool-overload response)
Premise from research cited in `V2.2-RESTRUCTURE.md`: accuracy is concentrated in the **3–15 tools per turn** band and degrades sharply beyond it; name collisions and semantic overlap ("search" vs "web_search" vs "bing_search") directly confuse tool selection. Two responses:

- **Tool Search (`ToolSearchService`)** — RAG over tool schemas. Only the most relevant ~8–12 tools are sent to the model per turn, out of allowlists of 30+. Graceful degradation: if the embedding service is unavailable, fall back to the first 12 alphabetically; never exceed 15 without dynamic selection. Efficiency is tracked via the `tools_available`/`tools_loaded`/`tools_used` trace columns.
- **Weekly skill auditor, one per org, 4 passes in order:** (1) health — lint every tool, health-check every MCP; (2) interference — flag cosine > 0.85 description overlap, name collisions, and any agent over 15 tools; (3) description quality — rewrite weak descriptions for retrieval; (4) replacement research — web-search for better alternatives to the top-5 most-called tools, never proposing without a specific comparison. **Writes proposals only; never mutates skills autonomously.** Proposals go to the org's own CEO, not up to AZI Hub.

### 6.5 Recursive self-critique (the "hardened loop")
The identified gap: researchers research their own domain but never critique their own design, producing incremental proposals ("add the Linear MCP connector") rather than architectural ones. Two fixes:

**Trace-to-improvement on the researchers themselves** (SCOPE pattern, ICLR 2026): after each researcher run, score the proposals it generated — was it approved? did it pass A/B? how long from proposal to merge? — and feed those signals back as prompt refinement for the *researcher's own system prompt*. Consistently rejected proposals mean its sources or format need updating.

**Monthly architecture self-audit** answering five fixed questions, written to `vault/proposals/architecture/YYYY-MM-monthly-audit.md`:
1. Tool counts — query `agent_traces.tools_loaded` vs `tools_available`; is any agent still overloaded?
2. Prompt staleness — which officer prompts haven't changed in 90+ days?
3. Memory precision trend — is the `memory_query` zero-result rate rising?
4. Framework gaps — any agent framework repo created in the last 30 days with >500 stars that solves something unaddressed?
5. Self-critique — which of my own proposals were rejected last month, and what pattern am I missing?

### 6.6 The stated ceiling on self-improvement
The docs are explicit and self-limiting here, which is worth carrying into any redesign:

> Self-improvement works in code, math, and optimization because outcomes are verifiable. The loop works well for tool selection (measurable via traces), memory retrieval (precision@5), token usage, and prompt quality on well-defined tasks (LLM-as-judge). It works **less well** for strategic direction, org-level decisions, and whether a business idea is good. The human-in-the-loop gate is the correct boundary for now. Don't try to automate that gate away — that's where the research warns about reward hacking.

---

## 7. Supporting subsystems (context for evaluation)

**Memory — three layers.** Layer 1 RAW (`vault/raw/`, immutable after capture, never edited by agents, source of truth) → Layer 2 COMPILED WIKI (`vault/wiki/`, LLM-maintained markdown with `[[wikilinks]]`, one page per entity; this is what agents *read*; it accumulates synthesis, not just text) → Layer 3 INDEXES (BM25 full-text + pgvector embeddings + entity graph). Queries are hybrid search + LLM re-rank. Obsidian is the human read interface, not the storage engine — plain text in, plain text out, agents maintain the structure.

**Cross-tenant memory** goes through a permission-scoped query broker (CMO-M) — the only path by which any agent reads another org's memory. It sees compiled wiki pages that orgs publish upward, never raw credentials or tool outputs from orgs it lacks a read grant for. As of v2.6 this unified into a single `wiki_pages` table with `visibility[]` filtering enforced by an RLS policy via `SET LOCAL app.visibility_filter`.

**Isolation.** Postgres 16 + pgvector, RLS on every tenant-scoped table (`org_id = current_setting('app.current_org_id')`), `org_id` as leading index column everywhere, tenant resolved from request context and never accepted as a plain parameter, and a `SecretProvider` abstraction with tenant-prefixed keys.

**Framework/instance boundary (the licensing prerequisite).** Root-level files — ARCHITECTURE.md, IMPLEMENTATION.md, the sprint specs, docker-compose.yml, Dockerfile, `.github/`, `scripts/`, `pg-migrations/` — are **not mounted into the agent container**. Agents operate only within `/workspace` (core), `/orgs`, `/personal`, `/shared`. Stated as intentional and permanent: a licensed user must not be able to modify the core product through agents; only the operator can, by pushing commits.

**Autonomous dev pipeline (v2.3).** Agents orchestrate Claude Code headlessly on the VPS via `delegate_to_claude_code` (strict env allowlist — never passes `DATABASE_URL`, `GITHUB_TOKEN`, or deploy tokens to the subprocess), with GitHub Actions auto-deploying every commit. The CTO agent has a `ralph_loop` tool for iterative multi-file work, backed by `prd.json` (per-story pass flags) and `progress.txt` (accumulated cross-iteration memory).

**Ephemeral agents (v2.6).** `is_ephemeral` is required at spawn; ephemeral agents are invisible to all UI/API listings; `terminate_ephemeral_agents` synthesizes an entire batch into **one** org-scoped wiki page (500 spawned agents → one terminate call, one summary); 30-day soft delete then weekly hard delete. Failure to terminate is defined as a protocol violation, and the protocol is injected into every spawn-capable agent's prompt.

**Stack.** TypeScript monorepo · Node 22 · Fastify · React/Vite · Postgres 16 + pgvector · Redis · Docker Compose · Anthropic SDK direct (explicit ADR rejecting LangGraph: "steal the patterns without the dependency") · local embeddings via Ollama · deployed on a Hetzner VPS behind Cloudflare.

---

## 8. Honest current state

**Shipped and running:** tiered tenancy with RLS, the agent runtime, hybrid memory, North Star injection + `log_decision` + goal-auditor, Tool Search, the full proposal/eval/gate chain (demonstrated end-to-end against a live DB), `create_org`, per-org operational docs and Agent Cards, skill auditors on cron, session-close synthesis, the 3D knowledge graph, ephemeral agent lifecycle, and CI/CD auto-deploy.

**In flight:** a hardening sprint covering brain write-pipeline tagging, a human-gated curator agent for destructive memory actions, worker resilience (backoff + dead-letter queue), org-structure enforcement, and graph/routing UX.

**Known weak points worth pressure-testing in the research project:**
- Naming drift in the older docs (`orgs/alphabet/` vs `orgs/azi-hub/`) — the docs are not fully self-consistent.
- The self-improvement loop's own admission that it only optimizes verifiable metrics; everything strategic remains human-gated, which caps how "autonomous" the system can actually become.
- Eval datasets were seeded small (10–20 items per file against a target of 30–100), so grader signal may be thin.
- Tool count has grown to ~64; Tool Search mitigates but does not solve the underlying tool-space interference problem.
- Framework self-modification (the DGM-Hyperagents-style layer) is specified but deliberately left as the most ambitious, least-realized piece.
