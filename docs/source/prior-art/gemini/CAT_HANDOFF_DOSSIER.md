# CAT / Agentic OS — Complete Research, Technical & Architectural Handoff Dossier

**Document Status:** Master Consolidation & Handoff Dossier  
**Scope:** End-to-End Intellectual Lineage, Technical Architecture, Code-Level Mechanics, Database Schemas, Governance Protocols, Research Problem Definition, and 16-Domain Pre-Research Ontology  
**Intended Consumer:** Downstream LLMs (Claude Projects, Claude Code, Cursor) & Principal Architects ingesting this dossier alongside your source documents and the 4 Instagram Reels screen recording videos.

---

## Table of Contents
1. [Executive Orientation & How to Read This Dossier](#1-executive-orientation--how-to-read-this-dossier)
2. [Chronological Intellectual Lineage & Structural Tensions](#2-chronological-intellectual-lineage--structural-tensions)
3. [Part I — AZI Hub: The Implemented Engineering & Architectural Baseline](#3-part-i--azi-hub-the-implemented-engineering--architectural-baseline)
   - [3.1 Production Stack & Repository Topology](#31-production-stack--repository-topology)
   - [3.2 Multi-Tenant "Alphabet Layer" & Channel-Owned Auth](#32-multi-tenant-alphabet-layer--channel-owned-auth)
   - [3.3 Three-Layer Hybrid Memory & Cross-Tenant Query Broker](#33-three-layer-hybrid-memory--cross-tenant-query-broker)
   - [3.4 North Star Goal Governance & Anti-Drift Mechanics](#34-north-star-goal-governance--anti-drift-mechanics)
   - [3.5 Organization Lifecycle (`create_org` Interview → Scaffold → Fill)](#35-organization-lifecycle-create_org-interview--scaffold--fill)
   - [3.6 Tool-Space Governance (`ToolSearchService` & 4-Pass Skill Auditor)](#36-tool-space-governance-toolsearchservice--4-pass-skill-auditor)
   - [3.7 Automated Self-Improvement Cadence, Eval Substrate & SCOPE Loop](#37-automated-self-improvement-cadence-eval-substrate--scope-loop)
   - [3.8 Autonomous Dev Pipeline (`delegate_to_claude_code` & `ralph_loop`) & Ephemeral Agents](#38-autonomous-dev-pipeline-delegate_to_claude_code--ralph_loop--ephemeral-agents)
   - [3.9 Honest Implementation Status & Known Weaknesses](#39-honest-implementation-status--known-weaknesses)
4. [Part II — Conducting AI: The Enterprise Change-Management Conceptual Branch](#4-part-ii--conducting-ai-the-enterprise-change-management-conceptual-branch)
   - [4.1 Breakdown of the 4 Screen Recording Videos](#41-breakdown-of-the-4-screen-recording-videos)
   - [4.2 Core Product Thesis & McKinsey *Rewired* Alignment](#42-core-product-thesis--mckinsey-rewired-alignment)
   - [4.3 Technical Architecture, Relational/Graph DDL & Conductor Pseudocode](#43-technical-architecture-relationalgraph-ddl--conductor-pseudocode)
   - [4.4 Hybrid GraphRAG & Cryptographic Node-Level Governance](#44-hybrid-graphrag--cryptographic-node-level-governance)
5. [Part III — The CAT Skeptical Reset & Governing Research Methodology](#5-part-iii--the-cat-skeptical-reset--governing-research-methodology)
   - [5.1 Project Charter, Operating Rules & Slice 0 Proving Ground](#51-project-charter-operating-rules--slice-0-proving-ground)
   - [5.2 Governing Research Problem & Central Research Question](#52-governing-research-problem--central-research-question)
   - [5.3 The 2×2 Strategic Matrix & Hypothesis Space](#53-the-22-strategic-matrix--hypothesis-space)
   - [5.4 Falsification Criteria & Top 30 Research Questions](#54-falsification-criteria--top-30-research-questions)
6. [Part IV — Complete Chronological Log of All Six Project Chats](#6-part-iv--complete-chronological-log-of-all-six-project-chats)
7. [Part V — Canonical 16-Domain Pre-Research Taxonomy (`v3` Specification)](#7-part-v--canonical-16-domain-pre-research-taxonomy-v3-specification)

---

## 1. Executive Orientation & How to Read This Dossier

This dossier captures the complete body of engineering, product strategy, adversarial auditing, and research design conducted across the **Agentic OS / CAT (Company Automation Tool)** program.

To prevent downstream LLMs from conflating **implemented prototypes**, **adjacent conceptual branches**, and **unvalidated hypotheses**, every concept in this document is strictly categorized under three provenance regimes:

| Regime | Source Artifacts | Authority & Epistemic Status |
| :--- | :--- | :--- |
| **1. Implemented Baseline (`AZI Hub`)** | `AZI-HUB-PROJECT-BRIEF.md` | **Prior Art / Implemented Experience.** Actual running TypeScript/Node/Postgres/pgvector monorepo deployed on Hetzner VPS. Treated as empirical engineering evidence and architectural hypotheses—*not* as the mandatory CAT specification. |
| **2. Adjacent Conceptual Branch (`Conducting AI`)** | Chat 1 (`HISTORICAL REFERENCE SOURCE ONLY`) + 4 Instagram Reels screen recordings | **External Inspiration / Theorized Blueprint.** Enterprise AI change-management OS (50–1,000+ employees) modeled on McKinsey's *Rewired*, Neo4j Enterprise Brain, and Conductor routing. Treated strictly as prior conceptual art. |
| **3. Governing Research Program (`CAT`)** | `CAT_Research_to_Product_Plan.docx`, `00_FOUNDER_CORPUS_MAP_v1.md`, `01_CORPUS_BLIND_SPOT_AUDIT_v1.md`, `02_RESEARCH_PROBLEM_v2.md`, `03_AI_NATIVE_ORGANIZATION_RESEARCH_TAXONOMY_v3.md`, `SOURCE_MANIFEST_v2.md` | **Authoritative Research & Design Framework.** Enforces a skeptical reset: tests all multi-agent, OS, graph, and Alphabet-layer claims against single-agent deterministic baselines and non-agent alternatives before writing production code. |

---

## 2. Chronological Intellectual Lineage & Structural Tensions

### 2.1 Three-Phase Evolution
1. **Origin Phase — AZI Hub (Implemented Baseline):** Built first as a self-hosted, single-monorepo, multi-tenant agent operating system designed to run the founder's own holding company ("Alphabet layer" → renamed in `v2.2` to `AZI Hub` / `AltZ Capital` / `AltZ Sandbox` / `AltZ Media`) and eventually be licensed externally via a strict framework/instance filesystem boundary.
2. **Conceptual Branch — Conducting AI (External Influence):** Introduced via four Instagram Reels screen recordings demonstrating an interactive concentric-ring "Organisation Brain," an "Omni-Chat" routing interface, cryptographic node-level RBAC solving "The Obsidian Trap," and McKinsey *Rewired* vertical playbooks with 4-role human governance (*SOP Owner, AI Lead, AI Champion, System Owner*).
3. **Current Phase — CAT Research-to-Product Program (Skeptical Reset):** Deliberately suspends architectural assumptions. Mandates an evidence-first, 10-phase research-to-product pipeline (`Phase -1A` through `Phase 9`) anchored on a low-risk proving wedge (**Slice 0: Governed Research-to-Decision**), strict separation of personal vs. corporate memory, and symmetric evaluation of non-agent baselines (BPM, RPA, iPaaS, ERP-native automation) and single-agent deterministic workflows.

### 2.2 Five Core Structural Contradictions Exposed Across the Corpus
Downstream models must preserve—not silently paper over—these five unresolved tensions:
1. **Personal Brain Boundary:** `AZI Hub` integrates the personal tier (`cmo-memory-personal`, `coo-orchestration-personal`) as a peer to the meta-org (`Alt Z`) on one shared runtime. `CAT` explicitly excludes the personal second brain from the initial product boundary and prohibits implicit cross-boundary memory or action.
2. **Universal Enterprise Graph vs. Strict Tenant Isolation:** `Conducting AI` centers on a unified "Enterprise Brain" topological graph mapping every employee, tool, SOP, and chat log. `AZI Hub` enforces zero default org-to-org visibility (`Org ↔ Org = Zero by default`, routed exclusively through `AZI Hub`), and `CAT` designates "cross-company universal memory" as an explicit non-goal.
3. **Architectural Presumption vs. Baseline Skepticism:** `AZI Hub` implements executive-role agents (`ceo-<org>`, CTO `Ralph`), multi-agent swarms, North Star prompt injection, and holding-company hierarchies. `CAT` treats every one of these as unvalidated hypotheses that must outperform a single-agent + deterministic-workflow baseline to justify their complexity.
4. **Autonomous Self-Improvement vs. Deterministic State Control:** `AZI Hub` runs cron-driven researcher agents (`memory-researcher`, `orchestration-researcher`) with SCOPE recursive self-critique and auto-approved prompt variants (while gating code changes behind human approval). `CAT` prohibits uncontrolled self-modification and mandates deterministic software for permissions, policy, accounting, state transitions, approvals, budgets, record updates, and irreversible actions.
5. **Internal Holding-Company OS vs. External Commercial Wedge:** `AZI Hub` was built to operate a founder's multi-venture portfolio; `Conducting AI` targets 50–1,000+ employee traditional corporations; `CAT` requires customer validation to identify a single urgent buyer, user, and commercial wedge before committing to a platform topology.

---

## 3. Part I — AZI Hub: The Implemented Engineering & Architectural Baseline

*Synthesized from `AZI-HUB-PROJECT-BRIEF.md` (covering `ARCHITECTURE.md`, `IMPLEMENTATION.md`, `CLAUDE.md`, `DECISIONS.md`, `CURRENT_STATE.md`, `v2.2-RESTRUCTURE.md`, `v2.3-AUTOPILOT.md`, `refactor/PROGRESS.md`).*

### 3.1 Production Stack & Repository Topology
* **Runtime & Language:** TypeScript monorepo running on Node 22 and Fastify.
* **Frontend:** React + Vite, including a 3D knowledge graph visualizer and per-org Agent Cards sidebar.
* **Database & Vector Store:** PostgreSQL 16 with `pgvector` extension; Redis for queues/caching.
* **Model & Embedding Layer:** Direct Anthropic SDK integration (explicit Architectural Decision Record rejecting LangGraph: *"steal the patterns without the dependency"*); local embeddings generated via **Ollama**.
* **Deployment:** Containerized via Docker Compose on a Hetzner VPS behind Cloudflare, with GitHub Actions CI/CD auto-deploying every commit pushed to main.
* **Framework / Instance Hard Boundary (Licensing Prerequisite):**
  * Root-level framework files (`ARCHITECTURE.md`, `IMPLEMENTATION.md`, sprint specs, `docker-compose.yml`, `Dockerfile`, `.github/`, `scripts/`, `pg-migrations/`) are **never mounted into the agent container**.
  * Agents operate exclusively within `/workspace` (core runtime), `/orgs`, `/personal`, and `/shared`. A licensed tenant cannot modify core platform code via agents; only the repository operator can push commits.

### 3.2 Multi-Tenant "Alphabet Layer" & Channel-Owned Auth
* **Core Tenet:** Tenancy is enforced at runtime in the database and auth layers—not via separate git repos or separate container deployments.
* **Canonical Registry (`config/tenants.json`):** Defines `id`, `tier`, `display_name`, `parent`, and `permission_grants` across Tier 0 (Personal), Tier 1 (`azi-hub` meta-org), and Tier 2 subsidiary operating companies (`altz-capital`, `altz-sandbox`, `altz-media`). *(Note: legacy docs `IMPLEMENTATION.md` and `refactor/PROGRESS.md` still reference `orgs/alphabet/`—this is stale naming from pre-`v2.2`, not a separate codebase.)*
* **Database Isolation:**
  * PostgreSQL Row-Level Security (RLS) enforced on every tenant-scoped table via `org_id = current_setting('app.current_org_id')`.
  * `org_id` is the leading index column on all tenant tables.
  * Tenant ID is resolved exclusively from authenticated request context and is never accepted as an untrusted tool/API parameter.
  * `SecretProvider` abstraction isolates credentials using tenant-prefixed keys.
* **Channel-Owned Authorization Matrix:**
  * Permissions attach to the organization rather than individual human accounts; any worker or ephemeral agent spawned inside `AltZ Media` automatically inherits `AltZ Media`'s exact permission set.
  * **Officer Instancing:** Two reusable officer codebases are instantiated per tier—`cmo-memory-{personal,azi-hub}` and `coo-orchestration-{personal,azi-hub}`. Personal Chief of Staff and `Alt Z` operate as **peers** (Chief of Staff represents the founder while asleep; it does not subordinate `AZI Hub`).

| Boundary Edge | Enforced Permission Rule |
| :--- | :--- |
| `Personal → AZI Hub` | **Explicit push only.** Human publishes briefings/goals upward; `AZI Hub` never reads `personal/` by default. |
| `AZI Hub → Orgs` | Reads all subsidiary state; can issue directives; cannot silently mutate internal org files. |
| `Orgs → AZI Hub` | Each org publishes a periodic structured *state* summary. `AZI Hub` reads state summaries rather than raw org vaults to control token cost and noise. |
| `Org ↔ Org` | **Zero visibility by default.** Cross-org coordination must be explicitly brokered through `AZI Hub`. |
| `Human → Any Tier` | Superadmin authority across all tiers. |

### 3.3 Three-Layer Hybrid Memory & Cross-Tenant Query Broker
1. **Layer 1 — RAW (`vault/raw/`):** Immutable capture of raw events, transcripts, and external inputs. Never edited by agents; serves as the ground-truth audit log.
2. **Layer 2 — COMPILED WIKI (`vault/wiki/`):** LLM-maintained Markdown knowledge base using bidirectional `[[wikilinks]]`, structured one page per entity. This is the primary surface agents read, accumulating synthesized understanding rather than raw text dumps. Obsidian acts purely as a human read/inspection interface over plain-text files.
3. **Layer 3 — INDEXES & RETRIEVAL:** Hybrid search combining BM25 lexical full-text search, `pgvector` semantic embeddings, and entity graph traversal, followed by an LLM re-ranking step.
4. **Unified Cross-Tenant Broker (`v2.6`):** Cross-org queries route exclusively through `CMO-M` (permission-scoped query broker). Backed by a unified `wiki_pages` PostgreSQL table with `visibility[]` array filtering enforced at the SQL layer via RLS policy (`SET LOCAL app.visibility_filter`).
5. **Documentation-as-Anti-Drift:** Every organization maintains five mandatory operational files rotated/updated at session close: `CLAUDE.md` (briefing), `ARCHITECTURE.md` (system reality), `DECISIONS.md` (append-only decision log), `CURRENT_STATE.md` (rotated every session), and `SECOND_BRAIN_TAXONOMY.md`.

### 3.4 North Star Goal Governance & Anti-Drift Mechanics
Based on the engineering premise that **long-horizon goal drift—not missing capability—is the #1 production failure mode** of multi-agent systems:
1. **Turn-Level North Star Injection (`AgentRunner.injectNorthStar()`):**
   * Prepends `## NORTH STAR — Your primary directive` + the verbatim contents of `orgs/<org>/vault/north-star.md` (or `personal/vault/north-star.md`) to the **very top of every system prompt on every single turn** (zero extra API calls; silent pass-through if absent).
   * **Layered Prompt Assembly:**
     * `orgadmin` / `superadmin` agents receive: `[North Star] + [Org CLAUDE.md] + [Org ARCHITECTURE.md] + [Ephemeral Protocol (if spawn-capable)] + [Role Prompt]`.
     * Worker agents receive: `[North Star] + [Role Prompt]`.
     * Reference documents in `vault/ethos/` (`business-context.md`, `security-model.md`, `operating-model.md`) are **queryable via retrieval tools only—never auto-injected**.
2. **Mandatory Pre-Commitment Audit (`log_decision` tool):**
   * CEOs and CTOs must invoke `log_decision` *before* committing capital, resources, or external actions.
   * Writes `orgs/<org>/vault/decisions/YYYY-MM-DD-<id>.md` with required fields: `summary`, `reasoning`, `north_star_alignment`, and `alternatives_considered`.
3. **Weekly Goal-Drift Auditor:**
   * Executed every **Monday at 06:00 UTC** by `CMO-M` (deliberately assigned to the existing memory officer rather than spawning a dedicated auditor agent).
   * Reads the prior 7 days of `vault/decisions/` across all orgs, evaluates alignment against each org's current North Star, and writes flagged drift reports to `orgs/azi-hub/vault/proposals/goal-drift/<date>.md` for human review. **Never mutates state autonomously.**

### 3.5 Organization Lifecycle (`create_org` Interview → Scaffold → Fill)
1. **Step 1 — Interview (Conversational):** Superadmin agent interviews the founder on purpose, 12-month definition of success, explicit non-goals, decision authority boundaries, and brand voice (optionally running web research first).
2. **Step 2 — Deterministic Scaffold (`create_org` tool):** Superadmin-only, idempotent TypeScript tool containing **zero LLM generation**. Given `org_id` (kebab-case), `display_name`, `description`, and `parent` (default `azi-hub`):
   * Appends tenant entry to `config/tenants.json` at Tier 2.
   * Creates directory tree: `orgs/<org>/{config,vault,vault/ethos,vault/decisions,memory,skills}`.
   * Generates `agents.config.json` with `ceo-<org>`, `skill-auditor-<org>` (cron `0 8 * * 1`), and `cross_org_refs` linking read-only sidebar entries for the personal Chief of Staff and `Alt Z`.
   * Writes `ui.config.json` and `<!-- FILL: ... -->` template stubs for `north-star.md`, `vault/ethos/{business-context,security-model}.md`, and the five operational files.
3. **Step 3 — Fill (Conversational, Tenant-Scoped):** Interview transcript is routed to the **owning org's CTO** (`Ralph` for `azi-hub`, or the sub-org's own CTO; `Ralph` never writes cross-org), which populates the `<!-- FILL: ... -->` stubs via `web_browse` and `create_file`. `vault/decisions/` and `vault/okrs.md` are deliberately left uncreated until real operations begin (OKRs written by `ceo-<org>` after an initial two-week operating window).

### 3.6 Tool-Space Governance (`ToolSearchService` & 4-Pass Skill Auditor)
* **Empirical Premise (`v2.2-RESTRUCTURE.md`):** Tool-selection accuracy peaks in the **3–15 tools per turn** band and degrades sharply beyond 15 due to semantic overlap and name collisions (e.g., `search` vs. `web_search` vs. `bing_search`).
* **Dynamic Tool RAG (`ToolSearchService`):** Embeds all tool schemas (~64 total tools in registry) and retrieves only the top **~8–12 semantically relevant tools** per turn. If the embedding service fails, gracefully degrades to the first 12 tools alphabetically (hard ceiling of 15 tools). Tracks `tools_available`, `tools_loaded`, and `tools_used` on every turn trace.
* **Weekly 4-Pass Skill Auditor (`skill-auditor-<org>`, Mondays 08:00 UTC):**
  1. *Pass 1 — Health:* Lints tool schemas and runs connectivity health checks on all MCP servers.
  2. *Pass 2 — Interference:* Flags pairs with embedding cosine similarity `> 0.85`, naming collisions, and any agent configured with `> 15` static tools.
  3. *Pass 3 — Description Quality:* Rewrites ambiguous tool descriptions to improve vector retrieval precision.
  4. *Pass 4 — Replacement Research:* Web-searches for superior alternatives to the top-5 most frequently invoked tools, requiring concrete benchmark/feature comparisons.
  * Outputs proposals exclusively to the local org's CEO (`ceo-<org>`), never mutating tools directly.

### 3.7 Automated Self-Improvement Cadence, Eval Substrate & SCOPE Loop
* **PostgreSQL Measurement & Evolution Schema (Migration `006`):**
  * Turn telemetry logs: `tenant`, `agent`, `model`, `tokens_in`, `tokens_out`, `latency`, `tools_called`, `tools_available`, `tools_loaded`, `tools_used`, `outcome_label`, `parent_turn_id`.
  * Grader suite: `tool_success_rate`, `agent_response_quality` (LLM-as-judge), `tokens_per_turn_by_model`, `memory_query_precision`.
  * Golden `.jsonl` eval datasets covering memory retrieval (known-correct page IDs), agent routing (labeled recipients), code quality (reference implementations), and cost per turn.
  * Tables: `researcher_staging`, `proposals` (lifecycle `draft → recommended → approved → implementing → merged | rejected`, protected by a partial unique index guaranteeing **at most one proposal in `implementing` state at any time**), `ab_eval_runs`, and `prompt_variants` (enforcing exactly one active prompt variant per agent).
* **Cron Schedule (`CronService` / `scheduled_tasks`):**
  * **Hourly:** Staging workers scrape arXiv (`cs.SE`, `cs.DC`, `cs.MA`), GitHub, MCP registries, SDK releases, and personal inbox into `researcher_staging` (hash-deduplicated).
  * **Sun 03:00 UTC:** `CMO-M` memory synthesis pass.
  * **Sun 04:00 UTC:** `memory-researcher` clusters staged items and emits **at most one** structured proposal (`Problem / Proposed Change / Expected Eval Impact / Implementation Sketch at file-path granularity / Cost-Risk / Sources`) to `vault/proposals/memory/`.
  * **Sun 05:00 UTC:** `orchestration-researcher` emits **at most one** proposal to `vault/proposals/orchestration/`.
  * **Mon 06:00 UTC:** `CMO-M` goal-drift audit.
  * **Mon 08:00 UTC:** Per-org `skill-auditor-<org>` 4-pass review.
  * **1st of Month 09:00 UTC:** `orchestration-researcher` performs full **Architecture Self-Audit**.
  * **Continuous (5-min poll, 30-min idle):** `SessionCloseWorker` compiles idle conversations into a `vault/wiki/` page + `raw_event`.
  * **Weekly:** Hard-deletes soft-deleted ephemeral agents older than 30 days.
* **Evolution Gate & SCOPE Recursive Self-Critique (ICLR 2026):**
  * Low-blast-radius prompt variants may auto-promote if A/B eval deltas clear threshold; **all code modifications require human approval**.
  * To prevent researchers from generating shallow incremental proposals, the SCOPE loop scores each researcher's historical proposals (approval rate, A/B pass rate, merge cycle time) and feeds those signals back to refine the *researcher agent's own system prompt*.

### 3.8 Autonomous Dev Pipeline (`delegate_to_claude_code` & `ralph_loop`) & Ephemeral Agents
* **Headless Coding Subprocess (`delegate_to_claude_code`):** Allows authorized agents to invoke Claude Code headlessly on the VPS under a **strict environment variable allowlist** (explicitly stripping `DATABASE_URL`, `GITHUB_TOKEN`, and deployment secrets).
* **Iterative Multi-File Execution (`ralph_loop`):** Gives the CTO agent (`Ralph`) a structured loop backed by `prd.json` (per-story pass/fail flags) and `progress.txt` (persistent cross-iteration memory).
* **Ephemeral Agent Lifecycle (`v2.6`):** Requires `is_ephemeral: true` at spawn; hides ephemeral workers from UI/API agent rosters; enforces batch cleanup via `terminate_ephemeral_agents`, which synthesizes an entire swarm batch (e.g., 500 spawned workers) into **one single org-scoped wiki page**. Failing to terminate ephemeral batches is logged as a protocol violation.

### 3.9 Honest Implementation Status & Known Weaknesses
* **Shipped & Verified:** Tiered RLS tenancy, runtime, 3-layer hybrid memory, North Star injection + `log_decision` + weekly drift auditor, `ToolSearchService`, end-to-end proposal/eval/gate chain against live Postgres, `create_org`, operational 5-file docs, 4-pass skill auditors, `SessionCloseWorker`, 3D knowledge graph, ephemeral lifecycle, and CI/CD auto-deploy.
* **In Flight:** Brain write-pipeline tagging, human-gated memory curator agent for destructive deletions, worker backoff + dead-letter queue (DLQ) resilience, org-structure enforcement, and graph/routing UX.
* **Known Weaknesses to Pressure-Test:**
  1. Naming drift in older docs (`orgs/alphabet/` vs. `orgs/azi-hub/`).
  2. Self-improvement loop only optimizes verifiable local metrics; strategic shifts remain human-gated.
  3. Golden `.jsonl` eval datasets were seeded small (10–20 items vs. 30–100 target), risking noisy grader signal.
  4. Tool catalog reached ~64 tools; Tool RAG mitigates but does not eliminate semantic tool interference.
  5. Full framework self-modification (DGM-Hyperagents style) remains speculative and blocked by the container mount boundary.

---

## 4. Part II — Conducting AI: The Enterprise Change-Management Conceptual Branch

*Synthesized from Chat 1 (`HISTORICAL REFERENCE SOURCE ONLY — Conducting AI / McKinsey-derived adjacent concept`) and the 4 Instagram Reels screen recording videos.*

### 4.1 Breakdown of the 4 Screen Recording Videos
*(Match your 4 local video files to the visual sequences below when loading into another LLM):*
* **Video 1 & Video 2/4 — Personal AI Brain ("The Obsidian Trap") vs. Custom Organisation Brain:**
  * Opens with a chaotic personal knowledge graph (Obsidian-style markdown cluster) representing individual employees building fragmented, unshared AI setups.
  * Transitions to a custom-built **Organisation Brain** rendered as an interactive concentric-ring topological network:
    * **Center Core:** Company Identity, Infrastructure & Strategic North Star.
    * **Inner Ring:** Business Divisions (Growth, Operations, Finance, Legal/Compliance).
    * **Outer Rings (Color-Coded Nodes):** **Blue nodes** = Human Employees; **Orange/Yellow nodes** = Autonomous Sub-Agents; **Green nodes** = SOPs & Knowledge Documents; **Red/Purple nodes** = SaaS Integrations (Slack, HubSpot, Google Drive, Notion).
  * Demonstrates clicking an employee node (**"Brandon Liu, Head of Growth"**) to dynamically filter the graph and open a deep profile drawer with tabs for *Overview*, *Work*, *AI Access*, *Activity*, *IT Consent*, and *Compliance*, alongside a Sprint Kanban board assigning 4 human roles per agent (**SOP Owner**, **AI Lead**, **AI Champion**, **System Owner**).
  * Demonstrates the **Omni-Chat Interface** with a left-hand roster of specialized sub-agents (*Customer Service Agent*, *Inventory Demand Forecasting Model*) enforcing RBAC so a junior Sales rep cannot query HR payroll context.
* **Video 3 — McKinsey *Rewired* Blueprint & Industry Playbooks:**
  * Presenter walks through physical pages of *Rewired: The McKinsey Playbook on How Leading Companies Win with Technology and AI* (highlighting *Building Your Talent Bench*, *An Operating Model That Outruns the Competition*, and *Technology for Speed and Distributed Innovation*).
  * Transitions to **"Conducting AI for: Real Estate"**—a pre-packaged vertical industry playbook mapping domain workflows, underwriting SOPs, and compliance rules directly into the Enterprise Brain graph.

### 4.2 Core Product Thesis & McKinsey *Rewired* Alignment
* **Target Market:** Mid-to-large traditional enterprises (50–1,000+ employees) attempting AI transformation.
* **Four Core Problems Addressed:** (1) *The Obsidian Trap* (siloed personal AI tools, zero institutional memory); (2) *The Context Gap* (generic LLMs blind to org charts, reporting lines, and SOPs); (3) *Compliance & RBAC Exposure* (cross-departmental data leakage); (4) *Execution Chasm* (lack of McKinsey-style stakeholder ownership per deployed agent).
* **4-Phase Rollout:** Phase 1 Blueprint Mapping (Weeks 1–4) → Phase 2 Core Infrastructure Build (Weeks 5–8) → Phase 3 Functional Pilot Deployment (Weeks 9–12) → Phase 4 Global Enterprise Scale (Weeks 13+).

### 4.3 Technical Architecture, Relational/Graph DDL & Conductor Pseudocode
* **Proposed Stack:** Next.js 15 (RSC) + Tailwind + Three.js / React Three Fiber (WebGL 60 FPS concentric graph up to 50k nodes), Python 3.11 FastAPI orchestration backend, Neo4j Enterprise causal cluster, Pinecone / `pgvector` (1536-dim embeddings), and LangGraph / custom state graph engine.
* **Core Relational Identity DDL (PostgreSQL):**
  * `corporate_tenants` (`tenant_id`, `company_name`, `domain_verification`, `is_active`)
  * `enterprise_users` (`user_id`, `tenant_id`, `email`, `full_name`, `clearance_level` enum `Tier_1_Public` through `Tier_4_Highly_Confidential`, `metadata_payload` JSONB)
  * `cryptographic_edge_tokens` (`token_id`, `user_id`, `graph_node_target`, `scoped_permissions` array `{'READ','WRITE','EXECUTE'}`, `expiration_horizon`, `cryptographic_signature`)
  * `operational_governance_ledger` (`entry_id`, `timestamp`, `tenant_id`, `user_id`, `assigned_agent_id`, `raw_user_intent`, `executed_graph_path` JSONB, `tool_calls_executed` JSONB, `response_hash` SHA-256, `compliance_validation_code`)
* **Topological Graph Model (Neo4j Cypher):**
  * Nodes: `:Tenant`, `:Employee`, `:Agent`, `:SOP`, `:Tool` with unique UUID constraints and `clearance` properties.
  * Directional Edges: `(:Employee)-[:MANAGES {assigned_sprint}]->(:Agent)`, `(:Agent)-[:REFERENCES {strict_mode: true}]->(:SOP)`, `(:Agent)-[:INTEGRATES_WITH {encryption: "TLS_1_3"}]->(:Tool)`, `(:Employee|Agent)-[:BELONGS_TO]->(:Tenant)`.
* **Conductor Engine Execution Pipeline:**
  1. `_verify_cryptographic_signature(context)` via HMAC-SHA256 over `user_id:tenant_id:user_clearance`.
  2. `_extract_query_intent_and_entities(raw_query)` in strict JSON mode.
  3. `_fetch_authorized_graph_subnetwork()` executing Cypher bounded traversal (`*1..3`) filtered by `target.clearance IN $accessible_tiers`.
  4. `vector.fetch_context_chunks(sop_node_ids, raw_query)` retrieving authorized SOP chunks.
  5. `llm.stream_generate()` streaming SSE tokens back to Omni-Chat.

### 4.4 Hybrid GraphRAG & Cryptographic Node-Level Governance
Combines dense vector cosine similarity ($\cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|}$) over SOP text chunks with Cypher structural path traversals, gated at every hop by a KMS-signed JWT envelope specifying `max_traversal_depth`, `allowed_labels`, `clearance_restriction`, and `edge_whitelist_actions`, mapped to **ISO 42001**, **SOC 2 Type II** (AES-256-GCM at rest, TLS 1.3 in transit), and **GDPR/CCPA** data residency controls.

---

## 5. Part III — The CAT Skeptical Reset & Governing Research Methodology

*Synthesized from `CAT_Research_to_Product_Plan.docx` and `02_RESEARCH_PROBLEM_v2.md`.*

### 5.1 Project Charter, Operating Rules & Slice 0 Proving Ground
* **One-Sentence Thesis:** *"CAT is a governed company execution system that turns authorized intent into observable, auditable, and continuously improving workflows across people, agents, software, and data."*
* **15 Mandatory Operating Rules:**
  1. Label every claim (`verified fact`, `sourced claim`, `inference`, `estimate`, `assumption`, `founder choice`, `design judgment`, `unresolved question`).
  2. Use primary sources with publisher, title, date, URL, access date, and exact proposition supported.
  3. Never fabricate citations, customers, interviews, benchmarks, or market sizes; desk research is never customer validation.
  4. Optimize for a small founding team and a narrow wedge (`Slice 0 → MVP → Platform Foundation → Expansion → North Star`).
  5. Prefer deterministic software for permissions, policy, accounting, state transitions, approvals, budgets, record updates, and irreversible actions.
  6. Every consequential action requires identity, authorization, least privilege, policy, budget, provenance, durable state, idempotency, observability, approval/escalation, and recovery.
  7. Benchmark every multi-agent design against a minimum single-agent + deterministic-workflow baseline.
  8. Enforce strict isolation between personal, parent/portfolio, and operating-company data and authority.
  9. Treat memory as typed systems (authoritative records, documents, retrieval indexes, working state, episodic traces, preferences, decisions, evaluated policies) with explicit retention, deletion, and rollback.
  10. Improvement follows `observe → propose → simulate → evaluate → approve → canary → monitor → rollback → record`.
  11. Maintain stable artifact IDs (`HYP`, `EVD`, `DEC`, `RSK`, `FR`, `NFR`, `ADR`, `API`, `EVT`, `EVAL`, `KPI`).
  12. Never silently overwrite decisions; supersede via `06_DECISION_LOG.md` with rationale and reversal triggers.
  13. Begin every phase with objective, decision enabled, scope, exclusions, plan, required evidence, exit criteria; end with four audits (evidence, contradiction, completeness, buildability) + Gate Review (`PASS`, `PASS WITH CONDITIONS`, `FAIL`).
  14. Ask only questions that materially alter phase direction.
  15. Return complete version-controlled Markdown artifacts.
* **10-Phase Program Plan:** `Phase 0` Program Design (`20_PROGRAM_PLAN_v1.md`) → `Phase 1` Landscape (`21_LANDSCAPE_v1.md`) → `Phase 2A` Customer Hypotheses (`22_CUSTOMER_HYPOTHESES_v1.md`) → `Phase 2B` Customer Evidence (`23_CUSTOMER_EVIDENCE_v1.md`) → `Phase 3` Product Thesis (`24_PRODUCT_THESIS_v1.md`) → `Phase 4` Build/Buy & Spikes (`25_BUILD_BUY_v1.md`) → `Phase 5` Architecture (`26_ARCHITECTURE_v1.md`) → `Phase 6` Trust/Operations/Economics (`27_TRUST_OPERATIONS_v1.md`) → `Phase 7` Business Plan (`28_BUSINESS_PLAN_v1.md`) → `Phase 8` Integration Memo (`29_INTEGRATION_MEMO_v1.md`) → `Phase 9` Build Handoff (`30_BUILD_HANDOFF_INDEX_v1.md`).
* **Slice 0 Proving Ground — Governed Research-to-Decision:**
  * Operator submits an objective → CAT generates a typed plan → routes bounded research through allow-listed tools/sources → records provenance & cost attribution → presents recommendation for human approval → logs approved decision → supports deterministic replay and audit **without production write authority**.
  * Proves 9 capabilities: Identity/Tenancy, Typed Orchestration, Bounded Agency, Policy/Approval, Evidence Provenance, Evaluation, Economics/Cost Attribution, Audit/Replay, and Recovery.

### 5.2 Governing Research Problem & Central Research Question
> *"Where, if anywhere, is the highest-leverage and most defensible control point in the emerging AI software and organizational stack for enabling organizations to become increasingly AI-native, and what customer problem would justify owning that control point?"*

### 5.3 The 2×2 Strategic Matrix & Hypothesis Space
* **Transformation Mode × Deployment Boundary Matrix:**
  * **Greenfield × Single-Org:** Create and run one new AI-native organization from zero.
  * **Greenfield × Multi-Org:** Create and run a portfolio of new AI-native ventures (venture studio / holding company).
  * **Brownfield × Single-Org:** Incrementally transform one existing enterprise into an AI-native operating model.
  * **Brownfield × Multi-Org:** Transform and coordinate a portfolio of existing companies (PE/VC/conglomerate).
* **Three Distinct Hypothesis Classes (Section 3 of `02_RESEARCH_PROBLEM_v2.md`):**
  * **3a. Product / Control-Point Hypotheses:** (1) Governed Execution & Approval Control Plane; (2) Organizational Capability / Composition Layer (dynamically composing capabilities from humans, agents, software, workflows, and external services without assuming static C-suite agents); (3) Enterprise Context & Memory Fabric; (4) Legacy Discovery & Integration Switchboard; (5) Vertical AI-Native Operating Template.
  * **3b. Architectural Hypotheses:** Agent Infrastructure/Runtime; Orchestration/Control Plane; Optimization/Self-Improvement Layer; Hybrid Deterministic State Machine + Bounded Agent Loop.
  * **3c. Business-Model / Delivery-Model Hypotheses:** Pure Multi-Tenant SaaS; Private VPC / Enterprise License; Hybrid Software + Implementation/Transformation Services Platform; Venture-Studio / Equity-Plus-Platform Model.

### 5.4 Falsification Criteria & Top 30 Research Questions
* **Two-Tier Falsification Framework:**
  * *Program-Level Falsification:* Evidence that no independent CAT control point survives foundation-model/hyperscaler absorption and incumbent ERP/CRM/iPaaS expansion, or that deterministic non-agent software solves the target jobs at superior economics.
  * *Hypothesis-Level Falsification:* Evidence invalidating a specific architectural or wedge claim (e.g., multi-agent swarms failing single-agent baselines, graph maintenance costs exceeding value, HITL approval fatigue) without invalidating the broader program.
* **Top 30 Research Questions (from `00_FOUNDER_CORPUS_MAP_v1.md` & `01_CORPUS_BLIND_SPOT_AUDIT_v1.md`):**
  * *Customer & Wedge (Q1–Q10):* Exact economic buyer, daily end-user, urgent JTBD, minimum proof-of-value event, willingness-to-pay without replacing Systems of Record, venture studio budget viability, SMB trust barriers, manual drift-management workarounds, willingness-to-pay to solve "The Obsidian Trap," mandatory Slice 0 integrations.
  * *Architecture vs. Baseline (Q11–Q17):* Single-agent deterministic baseline vs. multi-agent Alphabet layer, residual value if swarms/executive agents are removed, North Star turn-injection overhead vs. state machines, resolving parent-org vs. human supervisor conflicts, cross-tenant boundary actions, Omni-Chat UX vs. deterministic approval dashboards, Tool RAG accuracy at 100+ tools.
  * *Data, Governance & Memory (Q18–Q24):* Context-window RBAC enforcement, graph continuous-update compute economics, HITL approval fatigue threshold, idempotency over non-idempotent legacy APIs, deterministic rollback after hallucinated actions, resolving Layer 1 Raw vs. Layer 2 Wiki contradictions, customer acceptance of cordoned framework boundaries.
  * *Self-Optimization, Brownfield & Moat (Q25–Q30):* Plateauing of self-optimization loops, statistical power of 10–20 item eval sets, preventing SCOPE grader overfitting, customer-valued improvement metrics, brownfield legacy discovery/VPC/SOC 2 requirements and consulting vs. software economics, and whether frontier context/reasoning gains erase the Conductor layer.

---

## 6. Part IV — Complete Chronological Log of All Six Project Chats

1. **Chat 1 — `HISTORICAL REFERENCE SOURCE ONLY — Conducting AI / McKinsey-derived adjacent concept`**
   * *Inputs:* 4 Instagram Reels screen recording videos of Conducting AI's Enterprise Brain platform.
   * *Outputs:* Unified timestamped transcript, UI/diagram breakdown, initial PRD, and a comprehensive 10-section Investor-Ready Business & Technical Build Guide (PostgreSQL DDL, Neo4j Cypher schema, Python `ConductorEngine` pseudocode, GraphRAG pipeline, JWT governance envelope, 24-month roadmap, financial model).
2. **Chat 2 — `PHASE -1A — Corpus Reconstruction — COMPLETE` (Aug 25–27, 2026)**
   * *Inputs:* `AZI-HUB-PROJECT-BRIEF.md`, Chat 1, `CAT_Research_to_Product_Plan.docx`.
   * *Outputs:* `00_FOUNDER_CORPUS_MAP_v1.md` — established the 3-stage lineage (AZI Hub → Conducting AI → CAT), separated implemented facts from theorized concepts, mapped 5 structural contradictions, and compiled the initial 30 research questions.
3. **Chat 3 — `PHASE -1B — Corpus Blind Spot Audit — COMPLETE` (Aug 28, 2026)**
   * *Inputs:* `00_FOUNDER_CORPUS_MAP_v1.md` + foundational corpus.
   * *Outputs:* `01_CORPUS_BLIND_SPOT_AUDIT_v1.md` — audited 18 blind-spot dimensions, elevated **Greenfield vs. Brownfield** and **Single-Org vs. Multi-Org** into first-class research axes, exposed 4 cognitive biases (*Founder-Build Bias*, *Top-Down McKinsey Bias*, *Skeptical Reset Bias*, *Systems of Record Bias*), and pruned premature AZI-specific implementation minutiae.
4. **Chat 4 — `PHASE -1C — Research Problem Definition` (Aug 28, 2026)**
   * *Inputs:* `00_FOUNDER_CORPUS_MAP_v1.md` + `01_CORPUS_BLIND_SPOT_AUDIT_v1.md`.
   * *Outputs:* Draft `01_RESEARCH_PROBLEM_v1.md` → refined in Turn 2 into **`02_RESEARCH_PROBLEM_v2.md`** — neutralized brownfield bias, separated Product/Control-Point vs. Architectural vs. Business-Model hypotheses, introduced the **Organizational Capability / Composition Layer**, removed false binary dichotomies in technical questions, and split Program-Level vs. Hypothesis-Level falsification criteria.
5. **Chat 5 — `PHASE -1D — Research Taxonomy — ITERATION HISTORY` (Aug 28, 2026)**
   * *Inputs:* `02_RESEARCH_PROBLEM_v2.md` + prior canonical artifacts.
   * *Outputs:* Draft `v1` (rejected for over-compressing 100 topics into 3 buckets) → expanded into **`02_AI_NATIVE_ORGANIZATION_RESEARCH_TAXONOMY_v2.md`** containing **16 granular domains**, 46+ subcategories with 14-field specifications, and 6 cross-cutting evaluation matrices.
6. **Chat 6 — `PHASE -1D FINAL — Canonical Taxonomy Editorial Pass` (Aug 29–30, 2026)**
   * *Inputs:* Attached `02_AI_NATIVE_ORGANIZATION_RESEARCH_TAXONOMY_v2.md`.
   * *Outputs:* **`03_AI_NATIVE_ORGANIZATION_RESEARCH_TAXONOMY_v3.md`** — surgical sentence-level editorial pass converting all residual declarative statements into empirical questions, removing historical architecture leakage, separating `TECHNICAL AUTHORIZATION ≠ ORGANIZATIONAL AUTHORITY`, expanding AI/agent security attack surfaces, separating operational state/memory from learning/evaluation substrates, generalizing Domain 9 to *Enterprise Discovery, Integration & System Interaction*, broadening Domain 12/13.1 beyond labor arbitrage to net economic surplus, and passing all 13 preflight neutrality checks.

---

## 7. Part V — Canonical 16-Domain Pre-Research Taxonomy (`v3` Specification)

Every category in `03_AI_NATIVE_ORGANIZATION_RESEARCH_TAXONOMY_v3.md` is evaluated across **14 standardized fields** (*Definition, Relevance to CAT, Key Research Questions, Primitives, Systems to Investigate, Academic Traditions, Evidence Required, Maturity Dimensions, Commoditization Questions, Potential Moat Questions, Greenfield/Brownfield Implications, Single/Multi-Org Implications, Dependencies*) and governed by an **Emergent Categories Register** so out-of-taxonomy discoveries amend the ontology rather than being forced into legacy buckets.

### Complete 16-Domain & Subcategory Hierarchy
* **Domain 1 — Model / Intelligence & Reasoning**
  * `1.1` Foundation Models & Inference Routing (cost-latency curves, semantic routers, fallback resilience, provider absorption)
  * `1.2` Reasoning, Planning & Decomposition (ToT/GoT, reflection loops, plan verification checkpoints, horizon degradation)
* **Domain 2 — Agent Execution & Harnesses**
  * `2.1` Agent Runtimes & Execution Environments (Docker, Firecracker microVMs, E2B, Modal, Wasm, cold-start & escape isolation)
  * `2.2` Agent Harnesses & Control Loops (ReAct vs. Plan-and-Execute, infinite-loop/context-saturation guards)
  * `2.3` Single-Agent Architectures (monolithic single-agent baseline benchmarked against multi-agent swarms)
* **Domain 3 — Multi-Agent Coordination & Workflow**
  * `3.1` Multi-Agent Systems & Topologies (hierarchical, mesh, pipeline, blackboard; error amplification across hops)
  * `3.2` Workflow Engines & State Machines (Temporal, Prefect, Airflow, DAGs, finite state machines, deterministic transition guards)
  * `3.3` Durable Execution & Fault Tolerance (event sourcing, CQRS, checkpointing, replay, RTO/RPO)
  * `3.4` Event-Driven & Actor-Model Systems (Ray, Akka, Kafka, Elixir/Erlang mailboxes, async pub-sub)
* **Domain 4 — Tools, Skills & Interoperability**
  * `4.1` Tool Discovery, Selection & Invocation (Tool RAG, schema validation, tool-space interference from 10 to 500+ tools)
  * `4.2` Skills & Capability Registries (versioning, capability manifests, self-improving skill lifecycles & safety gates)
  * `4.3` Interoperability Protocols (MCP, A2A, JSON-RPC transport, interoperability-server trust & supply-chain risk)
* **Domain 5 — State, Memory & Knowledge**
  * `5.1` Memory Systems & Learning/Evaluation Substrates (separating runtime operational state from execution traces, human corrections, counterexamples, and skill performance histories; temporal freshness, semantic drift, contradiction resolution, and forgetting)
  * `5.2` Long-Context Architecture & Optimization (KV-caching, prompt caching, distractor sensitivity, instruction interference, multi-hop synthesis vs. retrieval)
  * `5.3` Knowledge Graphs & Ontologies (Neo4j, Neptune, RDF, entity resolution, continuous graph update cost)
  * `5.4` Retrieval Systems & Context Engineering (BM25 + vector + graph hybrid retrieval, cross-encoder re-ranking, token budgeting)
* **Domain 6 — Identity, Security & Governance**
  * `6.1` Identity, Authentication & Granular Authorization (human vs. agent vs. workload identity; RBAC/ABAC/ReBAC/capability-based auth; strict separation of `TECHNICAL AUTHORIZATION ≠ ORGANIZATIONAL AUTHORITY` along `IDENTITY → AUTHENTICATION → DELEGATED CREDENTIALS → TECHNICAL AUTHORIZATION → ORGANIZATIONAL AUTHORITY → ACTION → PROVENANCE`)
  * `6.2` Policy, Guardrails & Governance Frameworks (OPA, deterministic Policy Decision/Enforcement Points vs. prompt guardrails)
  * `6.3` Human Approvals, Intervention & Escalation (async approval gates, risk-scored diff UIs, notification fatigue & rubber-stamping thresholds)
  * `6.4` Sandboxing, Execution Security & Secrets Management (prompt injection, indirect injection, tool poisoning, confused-deputy, secrets leakage, agent-generated-code risk, cross-tenant contamination)
* **Domain 7 — Evaluation, Observability & Improvement**
  * `7.1` Observability, Tracing & Telemetry (OpenTelemetry, step-by-step trace replay, token/latency/cost attribution)
  * `7.2` Evaluation & Benchmarking Frameworks (golden datasets, statistical sample sizing, LLM-as-judge calibration)
  * `7.3` Agent Self-Evaluation & Optimization Loops (DSPy, SCOPE critique, governed authority spectrum: `OBSERVE → DIAGNOSE → RECOMMEND → SIMULATE → EVALUATE → PROPOSE → HUMAN-APPROVED → CANARY → ROLLBACK → BOUNDED AUTONOMOUS → STRUCTURAL MODIFICATION`)
  * `7.4` Automated System Evolution & Code Generation (headless coding loops, static analysis, CI/CD gates, formal verification)
* **Domain 8 — Infrastructure, Reliability & Deployment**
  * `8.1` Deployment Infrastructure & VPC/On-Premise Topologies (multi-tenant SaaS vs. dedicated VPC vs. air-gapped Kubernetes/vLLM)
  * `8.2` Reliability, Recovery & Idempotency (idempotency keys, Saga compensating transactions over non-idempotent legacy APIs, DLQs)
  * `8.3` Compute, Cost & Resource Optimization (model cascading, prompt caching, FinOps unit cost attribution)
* **Domain 9 — Enterprise Discovery, Integration & System Interaction**
  * `9.1` System Interaction & Legacy Integration (structured APIs, event streams, direct DBs, UI/browser automation, legacy protocol bridges)
  * `9.2` Process & Workflow Discovery (structured event-log process mining + unstructured communication/tacit workflow discovery)
  * `9.3` Data Ingestion, Discovery & Harmonization (parsers, semantic chunking, deduplication, tenant-tagged ingestion)
* **Domain 10 — Organizational Design & Capability Composition**
  * `10.1` Objective Formation, Capability Decomposition & Dynamic Composition (translating strategic goals into dynamic human-agent-software-workflow capability graphs)
  * `10.2` Organizational Topology & Team Formation (ephemeral task pods vs. static hierarchies vs. matrix structures)
  * `10.3` Authority, Delegation & Decision Rights (spending caps, delegation trees, agency theory, cryptographic sign-off rules)
  * `10.4` Workflow & Process Redesign (AI-native BPR avoiding "paving the cow path")
* **Domain 11 — Human-AI Organization & Adoption**
  * `11.1` Institutional Knowledge & Organizational Memory (capturing tacit knowledge without human documentation fatigue)
  * `11.2` Human-AI Teaming & Algorithmic Management (mixed-initiative UX, psychological response to algorithmic task allocation)
  * `11.3` Change Management & Trust Building (stakeholder alignment, trust calibration, adoption velocity)
  * `11.4` Complex Adaptive Systems & Organizational Behavior (emergent feedback loops, unintended incentive gaming)
* **Domain 12 — Customer Jobs-to-Be-Done & Adoption**
  * `12.1` Multi-Stakeholder Segmentation (8 distinct roles: *economic buyer, executive sponsor, technical buyer, compliance approver, implementation owner, daily user, beneficiary, displaced stakeholder*)
  * `12.2` Customer Jobs-to-Be-Done (spanning cost reduction, revenue generation, decision quality, experimentation velocity, compliance/risk, and new capabilities)
  * `12.3` Implementation, Onboarding & Delivery Motion (time-to-value, self-serve vs. forward-deployed engineering/consulting)
* **Domain 13 — Economics & Business Models**
  * `13.1` AI-Native Organizational Economics & Value Creation (net economic surplus, compute-to-value ratios, surplus capture)
  * `13.2` Pricing, Value Metrics & Unit Economics (seat vs. consumption vs. workflow/outcome pricing, gross margin durability)
  * `13.3` SaaS vs. Services vs. Hybrid Business Models (services margin dilution vs. productized onboarding moats)
* **Domain 14 — Strategy, Control Points & Moats**
  * `14.1` Platform Control Points & Ecosystem Leverage (where sustainable pricing power sits in the stack)
  * `14.2` Moat Mechanisms & Data Network Effects (switching costs, compliance certifications, cross-run learning loops without privacy leakage)
  * `14.3` Competitive Dynamics & Incumbent/Hyperscaler Response (AWS/Azure/GCP, OpenAI/Anthropic/Google, Salesforce/ServiceNow/Microsoft)
* **Domain 15 — Lifecycle, Deployment Modes & Scaling**
  * `15.1` Greenfield Creation vs. Brownfield Transformation (evaluated neutrally without stereotyping either mode)
  * `15.2` Single-Organization vs. Multi-Organization / Portfolio Systems (single-enterprise vs. holding company / venture studio / PE portfolio)
* **Domain 16 — Non-Agent Alternatives & Baselines**
  * `16.1` Deterministic Software, BPM & Workflow Automation (Camunda, Appian, Pegasystems, custom code)
  * `16.2` RPA, iPaaS & ERP/CRM-Native Automation (UiPath, Workato, Zapier, MuleSoft, Power Automate, Salesforce Flow)
  * `16.3` Enterprise Search, Knowledge Management & Data Platforms (SharePoint, Confluence, Elasticsearch, data warehouses)
  * `16.4` Human-Operated Processes & Managed Services / BPO Baselines (human outsourcing & SOP-driven teams)

### Six Cross-Cutting Evaluation Matrices Required in Phase 1
1. **Evaluation Dimensions Matrix:** Task success, reliability, latency, cost, security, maintainability, recovery/fault tolerance, scalability, interoperability, organizational fit, portability, and regulatory exposure.
2. **2×2 Coverage Matrix:** Mapping every candidate control point and architecture across `Greenfield/Brownfield × Single-Org/Multi-Org`.
3. **Control-Point Map:** Comparing value capture across orchestration, memory/graph, integration switchboard, governance/approval gate, and vertical templates.
4. **Non-Agent Baseline Map:** Head-to-head comparison against deterministic BPM, RPA/iPaaS, Enterprise Search, and human BPO.
5. **Academic Traditions Map:** Distributed systems/actor model, MAS/classical planning, organizational economics/agency theory/CAS, and HCI/algorithmic management.
6. **Build / Buy / Adopt OSS / Partner / Defer Decision Matrix:** Evaluated across 13 criteria (*strategic differentiation, maturity, reliability, security, portability, vendor lock-in, cost, implementation burden, ecosystem adoption, compliance readiness, customizability, switching costs, roadmap dependence*).