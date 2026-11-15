# 02_AI_NATIVE_ORGANIZATION_RESEARCH_TAXONOMY_v2

## I. Taxonomy Audit & Comparative Mapping

To ensure the research taxonomy is sufficiently granular and does not prematurely anchor on founder biases, this audit maps the domains against both the founder corpus and the initial candidate lists.

- **MISSING FROM FOUNDER CORPUS:** Distributed actor-model coordination semantics, automated process mining/discovery, enterprise search index harmonization, deterministic rules engines, and complex adaptive systems organizational behaviors.
- **ALREADY ADDED BY THE PHASE-1D CANDIDATE LIST:** Foundation model routing, basic agent runtimes, tool registries, multi-agent frameworks, RBAC policies, and core vector/graph retrieval techniques.
- **STILL MISSING FROM BOTH:** Formal economic modeling of token-to-human labor arbitrage, semantic drift detection in multi-tiered memory systems, legal liability distribution frameworks for autonomous agent errors, and multi-organization supply-chain contract choreography.

## II. Detailed Research Taxonomy Hierarchy

**DOMAIN 1 — MODEL / INTELLIGENCE & REASONING**
- 1.1 Foundation Models & Inference Routing
- 1.2 Reasoning, Planning & Decomposition

**DOMAIN 2 — AGENT EXECUTION & HARNESSES**
- 2.1 Agent Runtimes & Execution Environments
- 2.2 Agent Harnesses & Control Loops
- 2.3 Single-Agent Architectures

**DOMAIN 3 — MULTI-AGENT COORDINATION & WORKFLOW**
- 3.1 Multi-Agent Systems & Topologies
- 3.2 Workflow Engines & State Machines
- 3.3 Durable Execution & Fault Tolerance
- 3.4 Event-Driven & Actor-Model Systems

**DOMAIN 4 — TOOLS, SKILLS & INTEROPERABILITY**
- 4.1 Tool Discovery, Selection & Invocation
- 4.2 Skills & Capability Registries
- 4.3 Interoperability Protocols (MCP & A2A)

**DOMAIN 5 — STATE, MEMORY & KNOWLEDGE**
- 5.1 Memory Systems (Tiered / Ephemeral / Persistent)
- 5.2 Long-Context Architecture & Optimization
- 5.3 Knowledge Graphs & Ontologies
- 5.4 Retrieval Systems & Context Engineering

**DOMAIN 6 — IDENTITY, SECURITY & GOVERNANCE**
- 6.1 Identity, Authentication & Granular Authorization
- 6.2 Policy, Guardrails & Governance Frameworks
- 6.3 Human Approvals, Intervention & Escalation
- 6.4 Sandboxing, Execution Security & Secrets Management

**DOMAIN 7 — EVALUATION, OBSERVABILITY & IMPROVEMENT**
- 7.1 Observability, Tracing & Telemetry
- 7.2 Evaluation & Benchmarking Frameworks
- 7.3 Agent Self-Evaluation & Optimization Loops
- 7.4 Automated System Evolution & Code Generation

**DOMAIN 8 — INFRASTRUCTURE, RELIABILITY & DEPLOYMENT**
- 8.1 Deployment Infrastructure & VPC/On-Premise Topologies
- 8.2 Reliability, Recovery & Idempotency
- 8.3 Compute, Cost & Resource Optimization

**DOMAIN 9 — ENTERPRISE INTEGRATION & BROWNFIELD TRANSFORMATION**
- 9.1 Enterprise Integration & Legacy Wrapping
- 9.2 Process Discovery & Process Mining
- 9.3 Data Ingestion, Discovery & Harmonization

**DOMAIN 10 — ORGANIZATIONAL DESIGN & CAPABILITY COMPOSITION**
- 10.1 Capability Decomposition & Dynamic Composition
- 10.2 Organizational Topology & Team Formation
- 10.3 Authority, Delegation & Decision Rights
- 10.4 Workflow & Process Redesign

**DOMAIN 11 — HUMAN-AI ORGANIZATION & ADOPTION**
- 11.1 Institutional Knowledge & Organizational Memory
- 11.2 Human-AI Teaming & Algorithmic Management
- 11.3 Change Management & Trust Building
- 11.4 Complex Adaptive Systems & Organizational Behavior

**DOMAIN 12 — CUSTOMER JOBS-TO-BE-DONE & ADOPTION**
- 12.1 Buyer, User & Beneficiary Segmentation
- 12.2 Customer Jobs-to-Be-Done
- 12.3 Implementation, Onboarding & Professional Services

**DOMAIN 13 — ECONOMICS & BUSINESS MODELS**
- 13.1 Automation & Labor Arbitrage Economics
- 13.2 Pricing, Value Metrics & Unit Economics
- 13.3 SaaS vs. Services Business Models

**DOMAIN 14 — STRATEGY, CONTROL POINTS & MOATS**
- 14.1 Platform Control Points & Ecosystem Leverage
- 14.2 Moat Mechanisms & Data Network Effects
- 14.3 Competitive Dynamics & Incumbent/Hyperscaler Response

**DOMAIN 15 — LIFECYCLE, DEPLOYMENT MODES & SCALING**
- 15.1 Greenfield Creation vs. Brownfield Transformation
- 15.2 Single-Organization vs. Multi-Organization/Portfolio Systems

**DOMAIN 16 — NON-AGENT ALTERNATIVES & BASELINES**
- 16.1 Deterministic Software, BPM & Workflow Automation
- 16.2 RPA, iPaaS & ERP/CRM-Native Automation
- 16.3 Enterprise Search, Knowledge Management & Data Platforms
- 16.4 Human-Operated Processes & Managed Services Baselines

## III. Category Specifications

### DOMAIN 1 — MODEL / INTELLIGENCE & REASONING

#### 1.1 Foundation Models & Inference Routing

- **Definition:** Systems and routing strategies that select, prompt, and query underlying LLMs based on cost, latency, and capability requirements.
- **Why it matters to CAT:** Determines whether the system is tightly coupled to a single frontier model provider or can abstract model commoditization.
- **Key Research Questions:** How does dynamic model routing impact reasoning stability across complex multi-step workflows? What are the failure modes of fallback logic when primary model endpoints fail?
- **Important Primitives:** Cost-latency trade-off curves, router classifiers, prompt translation layers, token-budget allocators.
- **Types of Systems to Investigate:** OpenRouter, LiteLLM, semantic routers, multi-model orchestrators.
- **Relevant Academic Traditions:** Distributed systems routing, machine learning ensemble theory.
- **Evidence Required:** Benchmark variance reports, latency overhead metrics, cost-per-successful-task analyses.
- **Maturity Dimensions:** Portability, cost efficiency, reliability.
- **Commoditization Questions:** To what extent are model routers being absorbed directly into base model provider APIs or cloud gateways?
- **Potential Moat Questions:** Can a routing layer build a proprietary routing dataset that outperforms generic routers for enterprise workflows?
- **Greenfield/Brownfield Implications:** Uniformly applicable; brownfield environments may require routing through secure enterprise proxies.
- **Single/Multi-Org Implications:** Multi-org environments require tenant-isolated routing keys and cost attribution models.
- **Dependencies:** Interacts directly with Domain 1.2 (Reasoning) and Domain 8.3 (Compute Optimization).

#### 1.2 Reasoning, Planning & Decomposition

- **Definition:** Algorithmic mechanisms that enable models to break down complex goals into sequential sub-tasks, plan execution paths, and self-correct during execution.
- **Why it matters to CAT:** Establishes how autonomous or semi-autonomous workflows handle non-linear problem solving without rigid human scripting.
- **Key Research Questions:** Where do automated planning algorithms fail when exposed to ambiguous, multi-step enterprise tasks? How do plan-and-solve architectures compare to reactive agent loops?
- **Important Primitives:** Tree-of-Thought (ToT), Graph-of-Thought (GoT), reflection loops, plan verification checkpoints.
- **Types of Systems to Investigate:** LangGraph state graphs, DSPy program optimizers, automated planning frameworks.
- **Relevant Academic Traditions:** Artificial intelligence classical planning, cognitive science, automated reasoning.
- **Evidence Required:** Task completion success rates across varying horizon lengths, error recovery rates.
- **Maturity Dimensions:** Autonomy, reliability, predictability.
- **Commoditization Questions:** Are advanced reasoning patterns migrating natively into frontier model weights, reducing the need for complex application-layer planning harnesses?
- **Potential Moat Questions:** Do domain-specific planning templates or compiled reasoning strategies create durable workflow advantages?
- **Greenfield/Brownfield Implications:** Greenfield allows native integration of planning loops; brownfield often requires mapping plans to fixed legacy process steps.
- **Single/Multi-Org Implications:** Multi-org scaling requires parameterized planning templates that respect boundary isolation.
- **Dependencies:** Relies on Domain 1.1 (Models) and Domain 3.2 (Workflow Engines).

### DOMAIN 2 — AGENT EXECUTION & HARNESSES

#### 2.1 Agent Runtimes & Execution Environments

- **Definition:** The computational infrastructure and sandboxed runtime layers where agent code, tool execution, and local file operations take place.
- **Why it matters to CAT:** Defines how code execution and tool calls are isolated to prevent systemic security breaches or resource exhaustion.
- **Key Research Questions:** What are the performance and security trade-offs between containerized worker nodes, WebAssembly (Wasm) runtimes, and serverless agent execution?
- **Important Primitives:** Ephemeral containers, resource quotas, secure execution sandboxes, execution timeouts.
- **Types of Systems to Investigate:** E2B, modal sandboxes, Firecracker microVMs, containerized Docker runtimes.
- **Relevant Academic Traditions:** Operating systems security, virtualization, distributed systems engineering.
- **Evidence Required:** Cold-start latency benchmarks, container escape vulnerability audits, resource overhead metrics.
- **Maturity Dimensions:** Security, reliability, performance.
- **Commoditization Questions:** Are cloud providers (AWS, GCP, Azure) offering native agent execution runtimes that commoditize specialized infrastructure layers?
- **Potential Moat Questions:** Does a tightly integrated runtime-to-orchestration feedback loop provide defensible performance or security advantages?
- **Greenfield/Brownfield Implications:** Brownfield deployments may face strict corporate IT constraints regarding where compute code can execute.
- **Single/Multi-Org Implications:** Requires strict multi-tenant boundary enforcement at the hypervisor or container level.
- **Dependencies:** Relies on Domain 6.4 (Sandboxing) and Domain 8.1 (Deployment Infrastructure).

#### 2.2 Agent Harnesses & Control Loops

- **Definition:** The software scaffolding that wraps foundation models with memory access, tool schemas, and iteration control loops (e.g., ReAct loops).
- **Why it matters to CAT:** Represents the core execution pattern governing how agents perceive, deliberate, and act.
- **Key Research Questions:** How do different harness architectures (e.g., ReAct vs. Plan-and-Execute) handle infinite loops and context saturation?
- **Important Primitives:** Turn management, stop conditions, state persistence wrappers, exception handlers.
- **Types of Systems to Investigate:** Custom Python harnesses, CrewAI, AutoGen, LangChain agent executors.
- **Relevant Academic Traditions:** Software engineering patterns, cybernetics, control theory.
- **Evidence Required:** Token consumption per completed task, failure propagation rates in long-running loops.
- **Maturity Dimensions:** Maturity, reliability, observability.
- **Commoditization Questions:** Are agent harnesses becoming standardized open-source utilities or commodity boilerplate?
- **Potential Moat Questions:** Can proprietary harness telemetry or error-handling heuristics form a defensible IP asset?
- **Greenfield/Brownfield Implications:** Independent of environment, though brownfield requires tighter API error handling.
- **Single/Multi-Org Implications:** Must support state partitioning across multiple organizational tenants.
- **Dependencies:** Relies on Domain 2.1 (Runtimes) and Domain 5.1 (Memory).

#### 2.3 Single-Agent Architectures

- **Definition:** Systems built around a single, highly capable agent instance equipped with broad tool access and memory, operating without peer-to-peer delegation.
- **Why it matters to CAT:** Serves as the critical baseline comparison against complex multi-agent swarms to test whether multi-agent overhead is justified.
- **Key Research Questions:** At what point does a single-agent architecture experience context degradation or instruction following failure compared to multi-agent divisions?
- **Important Primitives:** Unified tool registries, single-context window management, monolithic system prompts.
- **Types of Systems to Investigate:** Claude Engineer, specialized single-agent coding and workflow assistants, standalone Devin-style instances.
- **Relevant Academic Traditions:** Cognitive architecture models, human-computer interaction.
- **Evidence Required:** Comparative task success rates between single-agent and multi-agent setups on enterprise benchmark tasks.
- **Maturity Dimensions:** Reliability, simplicity, cost efficiency.
- **Commoditization Questions:** As model context windows expand and reasoning improves, are multi-agent architectures being swallowed by single-agent capabilities?
- **Potential Moat Questions:** Can single-agent tooling optimized for specific enterprise verticals create a sticky wedge?
- **Greenfield/Brownfield Implications:** Highly adaptable to both, requiring minimal topological configuration.
- **Single/Multi-Org Implications:** Operates cleanly within single-tenant scopes; requires partitioning in multi-org contexts.
- **Dependencies:** Relies on Domain 1.1 (Models) and Domain 5.2 (Long Context).

### DOMAIN 3 — MULTI-AGENT COORDINATION & WORKFLOW

#### 3.1 Multi-Agent Systems & Topologies

- **Definition:** Architectures where multiple specialized agents communicate, delegate sub-tasks, and collaborate through hierarchical, mesh, or pipeline topologies.
- **Why it matters to CAT:** Directly challenges or validates the founder corpus assumption that executive-role agents and complex swarms are necessary for organizational automation.
- **Key Research Questions:** What are the failure modes (e.g., cascading hallucinations, communication deadlocks) of multi-agent swarms in production? Under what conditions does a single agent outperform a multi-agent team?
- **Important Primitives:** Agent message passing, role definition schemas, supervisor-worker hierarchies, blackboard architectures.
- **Types of Systems to Investigate:** Multi-agent research frameworks, peer-to-peer agent communication meshes, hierarchical corporate simulation models.
- **Relevant Academic Traditions:** Multi-agent systems (MAS) research, distributed artificial intelligence, game theory.
- **Evidence Required:** Communication overhead costs (tokens/latency), error amplification rates across agent hops.
- **Maturity Dimensions:** Maturity, reliability, autonomy.
- **Commoditization Questions:** Are multi-agent orchestration frameworks becoming commoditized libraries with low pricing power?
- **Potential Moat Questions:** Do specialized multi-agent coordination protocols for specific enterprise workflows create lock-in?
- **Greenfield/Brownfield Implications:** Greenfield allows clean structural design; brownfield requires mapping agent roles to existing corporate charts or legacy constraints.
- **Single/Multi-Org Implications:** Multi-org environments require cross-boundary messaging security and tenant-isolated routing.
- **Dependencies:** Relies on Domain 3.2 (Workflow Engines) and Domain 4.3 (A2A Protocols).

#### 3.2 Workflow Engines & State Machines

- **Definition:** Deterministic software infrastructure that defines, sequences, and tracks execution paths using explicit state machines rather than probabilistic LLM branching.
- **Why it matters to CAT:** Enforces structural determinism where probabilistic agent behavior could otherwise lead to unpredictable enterprise states.
- **Key Research Questions:** How should probabilistic LLM outputs interface with deterministic state machine transitions without breaking workflow integrity?
- **Important Primitives:** Directed Acyclic Graphs (DAGs), finite state machines, transition guards, node retry policies.
- **Types of Systems to Investigate:** Temporal.io, Prefect, Apache Airflow, custom state graph engines.
- **Relevant Academic Traditions:** Workflow management systems, formal verification, computer science automata theory.
- **Evidence Required:** Workflow failure recovery rates, state corruption incidence metrics.
- **Maturity Dimensions:** Reliability, maturity, portability.
- **Commoditization Questions:** Are enterprise workflow engines (e.g., Temporal, cloud native orchestrators) universally available, reducing proprietary value?
- **Potential Moat Questions:** Can tightly coupled LLM-to-state-machine compilation tools form a defensible developer platform?
- **Greenfield/Brownfield Implications:** Essential for brownfield integration where legacy system state must be tracked deterministically.
- **Single/Multi-Org Implications:** Must natively support multi-tenant state isolation and scoped workflow definitions.
- **Dependencies:** Relies on Domain 3.3 (Durable Execution) and Domain 8.2 (Reliability).

#### 3.3 Durable Execution & Fault Tolerance

- **Definition:** Infrastructure that captures the exact state of long-running workflows so they can survive process crashes, timeouts, or network interruptions without data loss.
- **Why it matters to CAT:** Enterprise workflows spanning hours or days require guarantees that a server restart will not corrupt multi-step agent actions.
- **Key Research Questions:** What is the performance overhead of maintaining durable execution logs for high-frequency agent interactions?
- **Important Primitives:** Event sourcing, command query responsibility segregation (CQRS), state check-pointing, automatic replay.
- **Types of Systems to Investigate:** Temporal, AWS Step Functions, durable function runtimes.
- **Relevant Academic Traditions:** Distributed systems consistency, database transaction management (ACID properties).
- **Evidence Required:** Recovery time objectives (RTO) and recovery point objectives (RPO) under simulated node crashes.
- **Maturity Dimensions:** Reliability, recoverability, maturity.
- **Commoditization Questions:** Is durable execution an infrastructure commodity provided by cloud primitives?
- **Potential Moat Questions:** None inherently at the execution layer; moat must derive from domain workflow logic.
- **Greenfield/Brownfield Implications:** Critical for both, especially when interacting with fragile legacy APIs that time out.
- **Single/Multi-Org Implications:** Execution state storage must be strictly partitioned by tenant ID to prevent cross-tenant data leaks.
- **Dependencies:** Relies on Domain 3.2 (Workflow Engines) and Domain 8.2 (Reliability).

#### 3.4 Event-Driven & Actor-Model Systems

- **Definition:** Architectural patterns where independent computational entities (actors) communicate exclusively through asynchronous message passing and react to system events.
- **Why it matters to CAT:** Provides an alternative to centralized orchestration, allowing autonomous agents to operate as decentralized, loosely coupled actors.
- **Key Research Questions:** How do actor-model concurrency and event-driven streams scale when handling thousands of concurrent enterprise agent interactions?
- **Important Primitives:** Event brokers, actor mailboxes, asynchronous message passing, publish-subscribe topologies.
- **Types of Systems to Investigate:** Ray, Akka, Apache Kafka, Erlang/Elixir actor systems.
- **Relevant Academic Traditions:** Actor model of concurrent computation, event-driven architecture design.
- **Evidence Required:** Message throughput, latency distributions under high load, deadlock frequency.
- **Maturity Dimensions:** Scalability, maturity, portability.
- **Commoditization Questions:** Enterprise event streaming infrastructure is mature and commoditized by cloud and open-source ecosystems.
- **Potential Moat Questions:** Proprietary event-schema registries or domain event taxonomies could offer integration lock-in.
- **Greenfield/Brownfield Implications:** Brownfield environments often expose event streams via webhooks or message queues that can be tapped directly.
- **Single/Multi-Org Implications:** Requires tenant-scoped event routing and message isolation.
- **Dependencies:** Relies on Domain 3.1 (Multi-Agent Systems) and Domain 8.1 (Infrastructure).

### DOMAIN 4 — TOOLS, SKILLS & INTEROPERABILITY

#### 4.1 Tool Discovery, Selection & Invocation

- **Definition:** Mechanisms that allow agents to dynamically discover, select, and execute external APIs, code functions, or software tools based on semantic intent.
- **Why it matters to CAT:** As the number of available enterprise tools scales past hundreds, static tool binding fails, necessitating dynamic selection.
- **Key Research Questions:** How does tool-space interference scale as the number of available tools increases? What mechanisms prevent agents from selecting incorrect or destructive tools?
- **Important Primitives:** Tool description embeddings, vector-based tool search (Tool RAG), schema validation, execution argument mapping.
- **Types of Systems to Investigate:** Function calling APIs, dynamic tool registries, semantic tool search routers.
- **Relevant Academic Traditions:** Information retrieval, API design patterns, semantic search.
- **Evidence Required:** Tool selection accuracy rates as tool catalog size scales from 10 to 500.
- **Maturity Dimensions:** Reliability, interoperability, autonomy.
- **Commoditization Questions:** Base model providers are rapidly expanding native tool-calling and caching capabilities, risking wrapper commoditization.
- **Potential Moat Questions:** Curated, highly secure enterprise tool wrappers with pre-built validation schemas could create sticky integration value.
- **Greenfield/Brownfield Implications:** Brownfield requires wrapping messy, undocumented legacy APIs into clean tool schemas.
- **Single/Multi-Org Implications:** Tool execution permissions must strictly mirror user RBAC and tenant authorization boundaries.
- **Dependencies:** Relies on Domain 4.2 (Skills) and Domain 5.4 (Retrieval).

#### 4.2 Skills & Capability Registries

- **Definition:** Repositories that store, version, and document reusable agent capabilities, prompt templates, and execution scripts.
- **Why it matters to CAT:** Enables organizations to share, audit, and reuse validated operational procedures across different agent teams.
- **Key Research Questions:** How are agent skills versioned and audited to prevent unauthorized capability escalation or malicious prompt injection?
- **Important Primitives:** Capability manifests, semantic skill tagging, version control for prompts/tools, dependency graphs.
- **Types of Systems to Investigate:** Skill registries, plugin marketplaces, internal developer portals (IDPs) adapted for AI.
- **Relevant Academic Traditions:** Software component reuse, library management systems.
- **Evidence Required:** Skill reuse rates across projects, audit trail completeness metrics.
- **Maturity Dimensions:** Maturity, portability, security.
- **Commoditization Questions:** Open registries and standard format repositories reduce proprietary moat potential.
- **Potential Moat Questions:** Enterprise-certified skill libraries tied to specific regulatory compliance standards (e.g., SOC2, HIPAA).
- **Greenfield/Brownfield Implications:** Greenfield allows clean registry setup; brownfield requires cataloging existing scripts and macros.
- **Single/Multi-Org Implications:** Registries must support private tenant libraries alongside shared public libraries.
- **Dependencies:** Relies on Domain 4.1 (Tool Discovery) and Domain 6.2 (Policy).

#### 4.3 Interoperability Protocols (MCP & A2A)

- **Definition:** Standardized communication protocols (such as Model Context Protocol and agent-to-agent protocols) that enable seamless data and control exchange between disparate AI systems.
- **Why it matters to CAT:** Determines whether the platform operates as an isolated walled garden or interoperates with external enterprise ecosystems.
- **Key Research Questions:** What are the security and data leakage risks of adopting open interoperability protocols like MCP in regulated enterprise environments?
- **Important Primitives:** Standardized context schemas, JSON-RPC transport layers, protocol handshake mechanisms.
- **Types of Systems to Investigate:** Anthropic Model Context Protocol (MCP), open agent communication standards.
- **Relevant Academic Traditions:** Network protocols, API standards bodies, distributed systems interoperability.
- **Evidence Required:** Protocol overhead latency, vulnerability exposure assessments.
- **Maturity Dimensions:** Interoperability, portability, standardization.
- **Commoditization Questions:** High likelihood of protocol commoditization as standards are adopted industry-wide by hyperscalers.
- **Potential Moat Questions:** Acting as the primary certified switchboard or registry for enterprise MCP servers could capture network control points.
- **Greenfield/Brownfield Implications:** Brownfield adoption requires bridging legacy systems into standard protocol adapters.
- **Single/Multi-Org Implications:** Cross-organization protocol communication requires robust cryptographic authentication and boundary enforcement.
- **Dependencies:** Relies on Domain 4.1 (Tools) and Domain 6.1 (Identity).

### DOMAIN 5 — STATE, MEMORY & KNOWLEDGE

#### 5.1 Memory Systems (Tiered / Ephemeral / Persistent)

- **Definition:** Architectures that manage short-term working memory, medium-term episodic memory, and long-term semantic storage across agent lifecycles.
- **Why it matters to CAT:** Addresses how agents retain organizational context over extended operating horizons without suffering from context window overflow or memory corruption.
- **Key Research Questions:** How do multi-tier memory systems (e.g., raw immutable logs vs. compiled wikis) resolve conflicting factual assertions? What are effective strategic forgetting mechanisms?
- **Important Primitives:** Immutable raw stores, synthesized summary vaults, vector memory indices, memory garbage collection.
- **Types of Systems to Investigate:** Hybrid file-store/vector architectures, MemGPT-style hierarchical memory, graph-backed memory stores.
- **Relevant Academic Traditions:** Cognitive psychology (episodic vs. semantic memory), database systems, information retrieval.
- **Evidence Required:** Memory retrieval precision/recall benchmarks, storage cost inflation rates over time.
- **Maturity Dimensions:** Reliability, maturity, cost efficiency.
- **Commoditization Questions:** Vector database and memory abstraction libraries are increasingly commoditized by cloud providers.
- **Potential Moat Questions:** Proprietary memory distillation algorithms that compress enterprise history into high-signal compressed states.
- **Greenfield/Brownfield Implications:** Brownfield requires ingesting massive historical document repositories into structured memory tiers.
- **Single/Multi-Org Implications:** Absolute tenant isolation required across all memory tiers to prevent cross-contamination.
- **Dependencies:** Relies on Domain 5.3 (Knowledge Graphs) and Domain 5.4 (Retrieval).

#### 5.2 Long-Context Architecture & Optimization

- **Definition:** Techniques utilizing models with massive context windows (100k+ to millions of tokens) alongside caching and retrieval optimizations to process entire documents or codebases directly.
- **Why it matters to CAT:** Tests whether massive context windows can replace complex retrieval and memory architectures entirely.
- **Key Research Questions:** Where does "needle-in-a-haystack" retrieval degrade in ultra-long-context models? What are the cost and latency profiles of raw long-context processing versus targeted retrieval?
- **Important Primitives:** KV-cache optimization, sliding window attention, prompt caching, chunking strategies.
- **Types of Systems to Investigate:** Gemini 1.5 Pro, Claude 3.5 Sonnet long-context windows, optimized KV-caching proxies.
- **Relevant Academic Traditions:** Transformer architecture optimization, computer memory hierarchy design.
- **Evidence Required:** Cost-per-query comparisons between vector RAG and raw long-context processing.
- **Maturity Dimensions:** Cost, performance, reliability.
- **Commoditization Questions:** Massive context windows are a core feature commoditized directly by foundational model providers.
- **Potential Moat Questions:** Minimal moat at the raw context layer; moat rests on what content is selected to populate that context.
- **Greenfield/Brownfield Implications:** Highly beneficial for brownfield document ingestion where parsing structure is difficult.
- **Single/Multi-Org Implications:** Must ensure tenant boundaries are not breached when passing large multi-document payloads into shared model endpoints.
- **Dependencies:** Relies on Domain 1.1 (Models) and Domain 5.1 (Memory).

#### 5.3 Knowledge Graphs & Ontologies

- **Definition:** Structured semantic databases that map entities, relationships, organizational hierarchies, and operational rules into interconnected graph networks.
- **Why it matters to CAT:** Forms the structural backbone of enterprise context representation (similar to the historical "Enterprise Brain" hypothesis).
- **Key Research Questions:** Who pays the computational and operational cost of continuously updating graph nodes as enterprise structures evolve? How do graph schemas handle semantic ambiguity?
- **Important Primitives:** Node-edge schemas, graph traversal queries (Cypher), semantic entity resolution, ontology mapping.
- **Types of Systems to Investigate:** Neo4j, Amazon Neptune, RDF triple stores, graph-RAG architectures.
- **Relevant Academic Traditions:** Semantic web, knowledge representation, graph theory, database management.
- **Evidence Required:** Graph query latency at scale, automated schema update error rates.
- **Maturity Dimensions:** Maturity, scalability, interoperability.
- **Commoditization Questions:** Graph database engines are mature enterprise products; however, automated ontology generation is an active research area.
- **Potential Moat Questions:** Proprietary enterprise ontology templates tailored to specific industries (e.g., real estate, logistics).
- **Greenfield/Brownfield Implications:** Brownfield transformation requires automated extraction of enterprise graphs from legacy documents and communication logs.
- **Single/Multi-Org Implications:** Requires strict graph partitioning or multi-tenant database isolation.
- **Dependencies:** Relies on Domain 5.1 (Memory) and Domain 5.4 (Retrieval).

#### 5.4 Retrieval Systems & Context Engineering

- **Definition:** Hybrid retrieval pipelines (combining lexical search, vector similarity, and graph traversal) that assemble precise context payloads for agent consumption.
- **Why it matters to CAT:** Directly determines the signal-to-noise ratio of information fed into agent prompts.
- **Key Research Questions:** How does hybrid search (BM25 + vector + graph) outperform pure vector similarity in complex enterprise environments?
- **Important Primitives:** Cross-encoder re-ranking, reciprocal rank fusion, hybrid query planners, context window token budgeting.
- **Types of Systems to Investigate:** Pinecone, pgvector, ElasticSearch, custom GraphRAG pipelines.
- **Relevant Academic Traditions:** Information retrieval, natural language processing, search engine optimization.
- **Evidence Required:** Precision and recall metrics on enterprise gold-standard QA datasets.
- **Maturity Dimensions:** Performance, reliability, cost efficiency.
- **Commoditization Questions:** Retrieval libraries and managed vector databases are highly commoditized.
- **Potential Moat Questions:** Specialized re-ranking models or domain-tuned retrieval heuristics.
- **Greenfield/Brownfield Implications:** Critical for brownfield environments filled with unstructured legacy documents.
- **Single/Multi-Org Implications:** Retrieval queries must enforce tenant-level access filters at the database index level.
- **Dependencies:** Relies on Domain 5.1 (Memory) and Domain 5.3 (Knowledge Graphs).

### DOMAIN 6 — IDENTITY, SECURITY & GOVERNANCE

#### 6.1 Identity, Authentication & Granular Authorization

- **Definition:** Systems managing user identity, agent impersonation credentials, token-level access rights, and dynamic Role-Based Access Control (RBAC).
- **Why it matters to CAT:** Prevents unauthorized data access when agents execute queries on behalf of users with restricted clearance levels.
- **Key Research Questions:** How can Role-Based Access Control (RBAC) be enforced effectively inside an LLM context window where semantic bleeding can occur?
- **Important Primitives:** Cryptographic edge tokens, dynamic RBAC matrices, row-level security (RLS), OAuth2/OIDC integration.
- **Types of Systems to Investigate:** Keycloak, enterprise IAM integrations, cryptographically signed execution tokens.
- **Relevant Academic Traditions:** Computer security, cryptographic access control, identity management.
- **Evidence Required:** Security audit logs verifying zero cross-tenant or cross-clearance data leaks.
- **Maturity Dimensions:** Security, reliability, regulatory exposure.
- **Commoditization Questions:** Core IAM is commoditized, but agent-specific token propagation is an emerging requirement.
- **Potential Moat Questions:** Cryptographic token auditing frameworks that satisfy stringent enterprise compliance reviews.
- **Greenfield/Brownfield Implications:** Brownfield requires integrating with existing enterprise Identity Providers (Okta, Azure AD).
- **Single/Multi-Org Implications:** Fundamental requirement for multi-tenant and multi-organization platforms.
- **Dependencies:** Relies on Domain 6.2 (Policy) and Domain 6.4 (Secrets).

#### 6.2 Policy, Guardrails & Governance Frameworks

- **Definition:** Rule engines and policy interceptors that evaluate agent actions against corporate compliance rules, safety guidelines, and legal constraints before execution.
- **Why it matters to CAT:** Ensures enterprise guardrails are enforced deterministically rather than relying on LLM self-policing.
- **Key Research Questions:** What are the failure modes of prompt-based guardrails versus deterministic code-level policy enforcement?
- **Important Primitives:** Policy decision points (PDP), policy enforcement points (PEP), deterministic guardrail interrupters, compliance rule schemas.
- **Types of Systems to Investigate:** Open Policy Agent (OPA), NeMo Guardrails, custom deterministic policy interceptors.
- **Relevant Academic Traditions:** Policy-based management, software verification, computer ethics and safety.
- **Evidence Required:** Guardrail bypass vulnerability rates, false-positive blockage rates on legitimate user queries.
- **Maturity Dimensions:** Security, regulatory exposure, reliability.
- **Commoditization Questions:** Open-source policy engines (like OPA) are mature; AI-specific guardrail wrappers are rapidly proliferating.
- **Potential Moat Questions:** Comprehensive enterprise compliance policy libraries mapped to specific regulatory frameworks.
- **Greenfield/Brownfield Implications:** Brownfield deployments must codify existing corporate Standard Operating Procedures (SOPs) into machine-readable policies.
- **Single/Multi-Org Implications:** Policies must be configurable per tenant and per subsidiary organization.
- **Dependencies:** Relies on Domain 6.1 (Identity) and Domain 6.3 (Human Approvals).

#### 6.3 Human Approvals, Intervention & Escalation

- **Definition:** Workflows and interfaces that pause agent execution, present proposed actions to authorized human supervisors, and capture approvals or rejections.
- **Why it matters to CAT:** Enforces accountable human authority over high-consequence decisions (financial transactions, external communications, code deployments).
- **Key Research Questions:** At what failure rate or notification volume does human-in-the-loop approval degrade into notification fatigue and rubber-stamping?
- **Important Primitives:** Asynchronous approval gates, diff viewers, Slack/Teams notification hooks, timeout-to-reject fallbacks.
- **Types of Systems to Investigate:** Human-in-the-loop workflow tools, custom approval dashboards, notification gateways.
- **Relevant Academic Traditions:** Human-computer interaction (HCI), decision support systems, organizational behavior.
- **Evidence Required:** Human response latency metrics, rubber-stamping incidence audits, task abandonment rates.
- **Maturity Dimensions:** Human oversight, reliability, maturity.
- **Commoditization Questions:** Basic notification and approval workflows are standard features in workflow engines.
- **Potential Moat Questions:** Context-rich diff visualization and risk-scoring interfaces that minimize human cognitive load.
- **Greenfield/Brownfield Implications:** Must integrate smoothly into existing communication channels used by human teams.
- **Single/Multi-Org Implications:** Approval routing must respect multi-org reporting lines and delegation limits.
- **Dependencies:** Relies on Domain 6.2 (Policy) and Domain 3.2 (Workflow Engines).

#### 6.4 Sandboxing, Execution Security & Secrets Management

- **Definition:** Systems that securely store API keys, database credentials, and cryptographic secrets while ensuring agent-generated code runs in isolated environments.
- **Why it matters to CAT:** Prevents prompt injection attacks from exfiltrating enterprise API keys or compromising host infrastructure.
- **Key Research Questions:** How can secrets be injected into agent execution environments without exposing raw keys to the LLM context window?
- **Important Primitives:** Ephemeral credential generation, vault storage, network egress filtering, memory isolation.
- **Types of Systems to Investigate:** HashiCorp Vault, AWS Secrets Manager, secure code execution sandboxes.
- **Relevant Academic Traditions:** Cybersecurity, cryptographic engineering, secure systems architecture.
- **Evidence Required:** Penetration testing reports, secret leakage vulnerability assessments.
- **Maturity Dimensions:** Security, regulatory exposure, reliability.
- **Commoditization Questions:** Enterprise secrets management is a mature, highly commoditized infrastructure domain.
- **Potential Moat Questions:** Specialized scoping proxies that limit agent token utility to specific API endpoints.
- **Greenfield/Brownfield Implications:** Must integrate with existing enterprise key management infrastructures (KMS).
- **Single/Multi-Org Implications:** Absolute isolation of secret vaults required across tenant boundaries.
- **Dependencies:** Relies on Domain 2.1 (Runtimes) and Domain 6.1 (Identity).

### DOMAIN 7 — EVALUATION, OBSERVABILITY & IMPROVEMENT

#### 7.1 Observability, Tracing & Telemetry

- **Definition:** Instrumentation that tracks agent execution traces, token consumption, tool call sequences, and latency breakdowns across distributed runs.
- **Why it matters to CAT:** Essential for debugging non-deterministic agent failures and auditing why an agent reached a specific decision.
- **Key Research Questions:** What is the performance overhead of comprehensive telemetry logging on high-throughput agent workflows?
- **Important Primitives:** OpenTelemetry standards, execution DAG visualization, token cost attribution, step-by-step trace replay.
- **Types of Systems to Investigate:** LangSmith, Phoenix (Arize), Braintrust, Honeycomb.
- **Relevant Academic Traditions:** Distributed tracing, software debugging, performance monitoring.
- **Evidence Required:** Trace ingestion latency, storage footprint per 1,000 execution runs.
- **Maturity Dimensions:** Observability, reliability, maturity.
- **Commoditization Questions:** AI observability tooling is becoming heavily commoditized with open-source standards.
- **Potential Moat Questions:** Enterprise-grade cost attribution and compliance tracing dashboards tailored for executive audits.
- **Greenfield/Brownfield Implications:** Applicable across all deployment types.
- **Single/Multi-Org Implications:** Telemetry data must be strictly segmented by tenant to prevent data leakage.
- **Dependencies:** Relies on Domain 3.3 (Durable Execution) and Domain 8.2 (Reliability).

#### 7.2 Evaluation & Benchmarking Frameworks

- **Definition:** Automated testing pipelines that evaluate agent accuracy, output quality, hallucination rates, and regression metrics against golden datasets.
- **Why it matters to CAT:** Without rigorous evaluation datasets (beyond small sample tests), continuous self-improvement loops risk optimizing toward hallucinations.
- **Key Research Questions:** How large must enterprise evaluation datasets be to provide statistically significant confidence in agent self-improvement loops?
- **Important Primitives:** Golden test suites, LLM-as-a-judge scoring rubrics, regression testing pipelines, semantic similarity metrics.
- **Types of Systems to Investigate:** DeepEval, Promptfoo, custom CI/CD evaluation harnesses.
- **Relevant Academic Traditions:** Software testing, statistical quality control, benchmarking methodology.
- **Evidence Required:** Correlation between automated LLM-as-a-judge scores and human expert evaluations.
- **Maturity Dimensions:** Reliability, maturity, autonomy.
- **Commoditization Questions:** Open-source evaluation libraries are proliferating rapidly.
- **Potential Moat Questions:** Proprietary enterprise evaluation datasets and vertical-specific regression test suites.
- **Greenfield/Brownfield Implications:** Must be tailored to test against brownfield legacy system accuracy.
- **Single/Multi-Org Implications:** Evaluation suites can be shared across organizations while maintaining tenant data privacy.
- **Dependencies:** Relies on Domain 7.1 (Observability) and Domain 7.3 (Self-Evaluation).

#### 7.3 Agent Self-Evaluation & Optimization Loops

- **Definition:** Recursive feedback loops where agents critique their own outputs, propose prompt or workflow adjustments, and test improvements in sandboxed environments.
- **Why it matters to CAT:** Implements automated optimization (such as SCOPE patterns or skill auditors) to compound system performance over time.
- **Key Research Questions:** What are the risks of catastrophic forgetting or overfitting when agents recursively optimize their own prompts or code?
- **Important Primitives:** Proposal-evaluation-gate chains, automated self-critique prompts, shadow testing, canary deployments.
- **Types of Systems to Investigate:** DSPy optimizers, automated prompt evolution frameworks, self-improving agent loops.
- **Relevant Academic Traditions:** Reinforcement learning, evolutionary algorithms, machine learning optimization.
- **Evidence Required:** Performance delta measurements across successive self-optimization generations.
- **Maturity Dimensions:** Autonomy, maturity, reliability.
- **Commoditization Questions:** Automated optimization frameworks are emerging in open-source research.
- **Potential Moat Questions:** Defensible self-improvement loops that safely compound proprietary workflow efficiency without human intervention.
- **Greenfield/Brownfield Implications:** Requires strict sandboxing in brownfield environments to prevent accidental production corruption.
- **Single/Multi-Org Implications:** Optimization runs must be isolated to tenant data scopes.
- **Dependencies:** Relies on Domain 7.2 (Evaluation) and Domain 7.4 (System Evolution).

#### 7.4 Automated System Evolution & Code Generation

- **Definition:** Capabilities that allow the system to write, test, and deploy new tool integrations, code patches, or structural workflow updates autonomously.
- **Why it matters to CAT:** Enables the organization to adapt its technical tooling dynamically without manual developer intervention.
- **Key Research Questions:** What are the safety boundaries required when an agent generates and attempts to deploy executable code into production?
- **Important Primitives:** Automated unit testing, CI/CD pipeline triggers, static code analysis, human-gated code deployment.
- **Types of Systems to Investigate:** AI software engineering agents, automated code patch generators, CI/CD integration agents.
- **Relevant Academic Traditions:** Automated software engineering, program synthesis, formal verification.
- **Evidence Required:** Rate of introduction of security vulnerabilities or syntax errors in generated code.
- **Maturity Dimensions:** Autonomy, safety, security.
- **Commoditization Questions:** AI coding assistants (GitHub Copilot, Cursor) are heavily commoditized.
- **Potential Moat Questions:** End-to-end safe code evolution pipelines with verified formal correctness guarantees.
- **Greenfield/Brownfield Implications:** Extremely high risk in brownfield legacy codebases without rigorous test suites.
- **Single/Multi-Org Implications:** Code generation must respect multi-tenant repository boundaries.
- **Dependencies:** Relies on Domain 7.3 (Self-Optimization) and Domain 6.2 (Policy).

### DOMAIN 8 — INFRASTRUCTURE, RELIABILITY & DEPLOYMENT

#### 8.1 Deployment Infrastructure & VPC/On-Premise Topologies

- **Definition:** Infrastructure deployment models supporting multi-tenant cloud SaaS, single-tenant dedicated VPCs, or air-gapped on-premise installations.
- **Why it matters to CAT:** Regulated enterprises (finance, healthcare, government) often mandate private VPC or on-premise deployments as a strict prerequisite for adoption.
- **Key Research Questions:** What are the operational overhead and cost differentials of supporting air-gapped on-premise deployments versus multi-tenant SaaS?
- **Important Primitives:** Kubernetes operators, Terraform deployment scripts, air-gapped container registries, private model hosting (vLLM).
- **Types of Systems to Investigate:** Enterprise Kubernetes clusters, Helm charts, private cloud architectures.
- **Relevant Academic Traditions:** Cloud computing architecture, enterprise systems engineering.
- **Evidence Required:** Deployment time metrics, infrastructure maintenance overhead reports.
- **Maturity Dimensions:** Portability, security, maturity.
- **Commoditization Questions:** Standard cloud deployment tooling (Kubernetes, Terraform) is entirely commoditized.
- **Potential Moat Questions:** Turnkey air-gapped deployment packages that enable zero-friction enterprise compliance onboarding.
- **Greenfield/Brownfield Implications:** Brownfield enterprises frequently demand private VPC or on-premise configurations.
- **Single/Multi-Org Implications:** Governs how infrastructure is provisioned for single-org vs. multi-org holding structures.
- **Dependencies:** Relies on Domain 2.1 (Runtimes) and Domain 8.3 (Cost Optimization).

#### 8.2 Reliability, Recovery & Idempotency

- **Definition:** Mechanisms ensuring that agent actions against non-idempotent legacy APIs can be retried, rolled back, or recovered gracefully after failure.
- **Why it matters to CAT:** If an agent executes a duplicate payment or erroneous database mutation due to a network timeout, catastrophic business failure can occur.
- **Key Research Questions:** How can idempotency be guaranteed when interacting with legacy APIs that lack native transaction support?
- **Important Primitives:** Idempotency keys, compensating transactions (saga pattern), automated rollback scripts, dead-letter queues.
- **Types of Systems to Investigate:** Distributed transaction managers, saga pattern orchestrators, API proxy retry wrappers.
- **Relevant Academic Traditions:** Distributed transactions, fault-tolerant computing, database recovery.
- **Evidence Required:** System recovery success rates following injected network failures and duplicate request scenarios.
- **Maturity Dimensions:** Reliability, recoverability, safety.
- **Commoditization Questions:** Distributed reliability patterns are established software engineering principles.
- **Potential Moat Questions:** Domain-specific compensating transaction libraries tailored for legacy enterprise systems.
- **Greenfield/Brownfield Implications:** Critically important in brownfield environments with fragile legacy systems.
- **Single/Multi-Org Implications:** Recovery logs must maintain strict tenant isolation.
- **Dependencies:** Relies on Domain 3.3 (Durable Execution) and Domain 9.1 (Enterprise Integration).

#### 8.3 Compute, Cost & Resource Optimization

- **Definition:** Strategies and tooling that monitor, allocate, and optimize token expenditure, inference compute, and infrastructure resource consumption.
- **Why it matters to CAT:** Unoptimized multi-agent loops can easily generate runaway compute costs that destroy unit economics.
- **Key Research Questions:** What token optimization strategies (e.g., prompt caching, quantization, model cascading) yield the highest ROI without degrading task accuracy?
- **Important Primitives:** Token usage attribution tracking, prompt caching, model tier cascading, budget throttle limits.
- **Types of Systems to Investigate:** FinOps tools for LLMs, token proxy gateways, cost attribution dashboards.
- **Relevant Academic Traditions:** Financial operations (FinOps), resource management in computing.
- **Evidence Required:** Cost-per-completed-workflow metrics, resource utilization efficiency reports.
- **Maturity Dimensions:** Cost efficiency, observability, maturity.
- **Commoditization Questions:** LLM proxy and token management tools are rapidly proliferating.
- **Potential Moat Questions:** Granular per-task cost attribution engines that enable profitable outcome-based pricing models.
- **Greenfield/Brownfield Implications:** Universal applicability across all deployment types.
- **Single/Multi-Org Implications:** Essential for attributing compute costs accurately across multi-organization portfolios.
- **Dependencies:** Relies on Domain 1.1 (Models) and Domain 7.1 (Observability).

### DOMAIN 9 — ENTERPRISE INTEGRATION & BROWNFIELD TRANSFORMATION

#### 9.1 Enterprise Integration & Legacy Wrapping

- **Definition:** Methodologies and connectors used to bridge modern agent runtimes with legacy enterprise systems (ERP, CRM, SQL databases, mainframes).
- **Why it matters to CAT:** Most enterprises operate on legacy software; value capture depends on wrapping or integrating with existing systems rather than replacing them.
- **Key Research Questions:** How can legacy systems without modern APIs be wrapped securely and reliably for agent interaction?
- **Important Primitives:** API adapters, database query wrappers, robotic UI automation fallbacks, legacy protocol bridges.
- **Types of Systems to Investigate:** Enterprise service buses (ESB), iPaaS platforms (MuleSoft, Zapier), custom API gateways.
- **Relevant Academic Traditions:** Enterprise application integration (EAI), legacy system modernization.
- **Evidence Required:** Integration development time, API wrapper failure rates.
- **Maturity Dimensions:** Interoperability, maturity, portability.
- **Commoditization Questions:** Enterprise integration platforms (iPaaS) are a massive, mature market dominated by entrenched incumbents.
- **Potential Moat Questions:** AI-native legacy API generators that automatically reverse-engineer and wrap undocumented legacy systems.
- **Greenfield/Brownfield Implications:** The core challenge of brownfield transformation; irrelevant in greenfield.
- **Single/Multi-Org Implications:** Integrations must respect tenant-specific legacy system credentials and data boundaries.
- **Dependencies:** Relies on Domain 4.1 (Tools) and Domain 8.2 (Reliability).

#### 9.2 Process Discovery & Process Mining

- **Definition:** Algorithmic techniques that analyze enterprise event logs, communication history, and system interactions to discover and map actual operational workflows.
- **Why it matters to CAT:** Before automating an organization, the system must accurately discover how work actually happens versus how it is documented.
- **Key Research Questions:** How effectively can process mining algorithms extract unstructured human workflows from enterprise communication logs?
- **Important Primitives:** Event log parsing, process discovery algorithms (Alpha miner, heuristic miner), workflow bottleneck detection.
- **Types of Systems to Investigate:** Celonis, UiPath Process Mining, process discovery analytics tools.
- **Relevant Academic Traditions:** Process mining, business process management (BPM), data mining.
- **Evidence Required:** Accuracy of discovered process models compared to manual human audits.
- **Maturity Dimensions:** Maturity, observability, accuracy.
- **Commoditization Questions:** Enterprise process mining is an established software category led by specialized incumbents.
- **Potential Moat Questions:** AI-driven unstructured process discovery that goes beyond structured event logs to map tacit knowledge work.
- **Greenfield/Brownfield Implications:** Essential for brownfield discovery; unnecessary in greenfield creation.
- **Single/Multi-Org Implications:** Process discovery logs must remain strictly partitioned within tenant boundaries.
- **Dependencies:** Relies on Domain 5.3 (Knowledge Graphs) and Domain 9.1 (Integration).

#### 9.3 Data Ingestion, Discovery & Harmonization

- **Definition:** Pipelines that ingest, clean, categorize, and harmonize heterogeneous enterprise data sources (documents, emails, databases) into usable knowledge stores.
- **Why it matters to CAT:** Garbage-in, garbage-out applies severely to agent memory and context systems.
- **Key Research Questions:** What are the most efficient pipelines for cleaning and chunking messy enterprise data for vector and graph ingestion?
- **Important Primitives:** Document parsers, semantic chunking algorithms, data deduplication, schema harmonization pipelines.
- **Types of Systems to Investigate:** Unstructured data ingestion pipelines, ETL/ELT tools with vector outputs, document intelligence APIs.
- **Relevant Academic Traditions:** Data engineering, information extraction, data warehousing.
- **Evidence Required:** Ingestion throughput, data quality and extraction accuracy scores.
- **Maturity Dimensions:** Maturity, reliability, performance.
- **Commoditization Questions:** Data ingestion and ETL tools are heavily commoditized.
- **Potential Moat Questions:** Automated semantic data harmonization pipelines tailored to complex industry verticals.
- **Greenfield/Brownfield Implications:** Brownfield requires heavy data ingestion; greenfield starts with clean structured data.
- **Single/Multi-Org Implications:** Ingestion pipelines must apply tenant-level security tagging at the point of entry.
- **Dependencies:** Relies on Domain 5.1 (Memory) and Domain 5.4 (Retrieval).

### DOMAIN 10 — ORGANIZATIONAL DESIGN & CAPABILITY COMPOSITION

#### 10.1 Capability Decomposition & Dynamic Composition

- **Definition:** Frameworks that break down high-level organizational objectives into discrete functional capabilities and dynamically compose agent/human teams to execute them.
- **Why it matters to CAT:** Determines whether organizational workflows must be hardcoded by humans or can be dynamically assembled by the system based on goals.
- **Key Research Questions:** How effectively can automated systems decompose complex, ambiguous enterprise goals into executable capability chains?
- **Important Primitives:** Goal decomposition trees, capability dependency graphs, dynamic team assembly algorithms.
- **Types of Systems to Investigate:** Dynamic workflow generators, multi-agent capability matching systems.
- **Relevant Academic Traditions:** Systems engineering, operations research, task network models.
- **Evidence Required:** Success rates of dynamic capability composition versus static workflow definitions.
- **Maturity Dimensions:** Autonomy, adaptability, complexity.
- **Commoditization Questions:** Emerging research area with low immediate commoditization risk.
- **Potential Moat Questions:** Proprietary capability decomposition templates that rapidly translate business goals into operational workflows.
- **Greenfield/Brownfield Implications:** Greenfield allows native dynamic composition; brownfield is constrained by fixed organizational structures.
- **Single/Multi-Org Implications:** Dynamic composition can span subsidiary business units in multi-org holding structures.
- **Dependencies:** Relies on Domain 1.2 (Reasoning) and Domain 3.1 (Multi-Agent Systems).

#### 10.2 Organizational Topology & Team Formation

- **Definition:** The structural arrangement of agents and humans (hierarchical, matrix, flat, or ephemeral pods) designed to optimize operational throughput.
- **Why it matters to CAT:** Evaluates whether static corporate hierarchies or dynamic, ephemeral agent pods yield superior operational performance.
- **Key Research Questions:** Do ephemeral, task-specific agent teams outperform static hierarchical agent structures in complex knowledge work?
- **Important Primitives:** Pod lifecycle management, dynamic role assignment, communication topology graphs.
- **Types of Systems to Investigate:** Ephemeral agent swarm frameworks, dynamic organizational simulation models.
- **Relevant Academic Traditions:** Organizational design, sociology, network theory.
- **Evidence Required:** Task completion time and error rates across different organizational topologies.
- **Maturity Dimensions:** Maturity, autonomy, adaptability.
- **Commoditization Questions:** Structural topology patterns are conceptual and difficult to commoditize directly as software.
- **Potential Moat Questions:** Proprietary organizational templates optimized for specific types of enterprise ventures.
- **Greenfield/Brownfield Implications:** Greenfield enables novel topologies; brownfield must mirror or augment existing corporate charts.
- **Single/Multi-Org Implications:** Multi-org systems require holding-company topological structures connecting multiple subsidiary nodes.
- **Dependencies:** Relies on Domain 10.1 (Capability Decomposition) and Domain 3.1 (Multi-Agent Systems).

#### 10.3 Authority, Delegation & Decision Rights

- **Definition:** Mechanisms defining who (or what agent) holds the decision rights, spending limits, and delegation authority for specific operational actions.
- **Why it matters to CAT:** Prevents agents from executing actions outside their authorized scope of authority (e.g., approving contracts or moving funds).
- **Key Research Questions:** How are decision rights mathematically modeled and enforced when delegating authority from human executives to autonomous agents?
- **Important Primitives:** Delegation matrices, financial spending caps, authority delegation trees, cryptographic sign-off rules.
- **Types of Systems to Investigate:** Algorithmic governance frameworks, digital signature authority engines.
- **Relevant Academic Traditions:** Corporate governance, organizational economics, agency theory.
- **Evidence Required:** Audit logs verifying zero unauthorized actions exceeding agent delegation limits.
- **Maturity Dimensions:** Security, governance, compliance.
- **Commoditization Questions:** Enterprise governance software is mature; agent delegation logic is nascent.
- **Potential Moat Questions:** Certified algorithmic governance frameworks that satisfy corporate board risk committees.
- **Greenfield/Brownfield Implications:** Brownfield requires mapping existing corporate delegation authorities into software rules.
- **Single/Multi-Org Implications:** Delegation rights must flow securely across multi-org holding company parent-subsidiary structures.
- **Dependencies:** Relies on Domain 6.1 (Identity) and Domain 6.2 (Policy).

#### 10.4 Workflow & Process Redesign

- **Definition:** Methodologies for redesigning business processes to exploit AI capabilities rather than merely digitizing inefficient legacy workflows.
- **Why it matters to CAT:** Avoids the "paving the cow path" trap of automating broken human processes.
- **Key Research Questions:** What workflow redesign principles maximize the leverage of autonomous agents versus human operators?
- **Important Primitives:** Process re-engineering frameworks, AI-native workflow blueprints, friction reduction audits.
- **Types of Systems to Investigate:** Business process re-engineering (BPR) methodologies adapted for AI.
- **Relevant Academic Traditions:** Operations management, business process re-engineering, industrial engineering.
- **Evidence Required:** Efficiency gains of redesigned AI-native workflows versus automated legacy workflows.
- **Maturity Dimensions:** Maturity, adaptability, impact.
- **Commoditization Questions:** Process redesign is largely consulting-driven rather than commoditized software.
- **Potential Moat Questions:** Proprietary workflow blueprints and templates that radically compress enterprise operating costs.
- **Greenfield/Brownfield Implications:** Greenfield enables clean redesign; brownfield requires delicate change management.
- **Single/Multi-Org Implications:** Redesigned workflows can be standardized and reused across multi-organization portfolios.
- **Dependencies:** Relies on Domain 9.2 (Process Mining) and Domain 10.1 (Capability Decomposition).

### DOMAIN 11 — HUMAN-AI ORGANIZATION & ADOPTION

#### 11.1 Institutional Knowledge & Organizational Memory

- **Definition:** Systems that capture, curate, and institutionalize tacit knowledge, cultural norms, and operational history so they are not lost when personnel leave.
- **Why it matters to CAT:** Addresses how organizations build and maintain a persistent intellectual baseline that scales beyond individual employee memory.
- **Key Research Questions:** How can tacit organizational knowledge be captured effectively without creating overwhelming documentation burdens for human workers?
- **Important Primitives:** Automated meeting summarization, decision rationalization logs, institutional wiki maintenance.
- **Types of Systems to Investigate:** Enterprise wikis, AI-augmented knowledge management platforms, organizational memory stores.
- **Relevant Academic Traditions:** Organizational learning, knowledge management, sociology of knowledge.
- **Evidence Required:** Knowledge retention metrics, onboarding time reductions for new personnel.
- **Maturity Dimensions:** Maturity, reliability, utility.
- **Commoditization Questions:** Knowledge management and wiki tools are heavily commoditized.
- **Potential Moat Questions:** Automated tacit knowledge extraction pipelines that continuously compile corporate behavior into structured memory.
- **Greenfield/Brownfield Implications:** Brownfield requires mining legacy documentation; greenfield builds institutional memory from day one.
- **Single/Multi-Org Implications:** Knowledge stores must support tenant-level isolation while allowing selective cross-subsidiary sharing.
- **Dependencies:** Relies on Domain 5.1 (Memory) and Domain 5.3 (Knowledge Graphs).

#### 11.2 Human-AI Teaming & Algorithmic Management

- **Definition:** Operational models where humans and AI agents work collaboratively in mixed teams, with algorithms allocating tasks, monitoring performance, and providing feedback.
- **Why it matters to CAT:** Establishes the day-to-day operating model of an AI-native organization.
- **Key Research Questions:** How do human workers respond psychologically to algorithmic management and task allocation by AI supervisors?
- **Important Primitives:** Mixed-initiative interaction design, task hand-off protocols, transparent reasoning explanations.
- **Types of Systems to Investigate:** Collaborative workspace platforms, human-AI teaming interfaces.
- **Relevant Academic Traditions:** Human-computer interaction (HCI), organizational behavior, industrial psychology.
- **Evidence Required:** Worker adoption rates, trust indices, human satisfaction surveys.
- **Maturity Dimensions:** Human oversight, adoption, maturity.
- **Commoditization Questions:** Collaborative interface patterns are rapidly emerging across enterprise software.
- **Potential Moat Questions:** Proprietary interaction paradigms that maximize human trust and collaboration efficiency.
- **Greenfield/Brownfield Implications:** Brownfield encounters cultural resistance; greenfield adopts algorithmic management natively.
- **Single/Multi-Org Implications:** Scalable across distributed multi-organization teams.
- **Dependencies:** Relies on Domain 6.3 (Human Approvals) and Domain 11.3 (Change Management).

#### 11.3 Change Management & Trust Building

- **Definition:** Structured methodologies for managing organizational resistance, building user trust, and guiding enterprises through AI transformation.
- **Why it matters to CAT:** Technological capability is frequently bottlenecked by human adoption friction and organizational politics.
- **Key Research Questions:** What change management frameworks (e.g., McKinsey Rewired playbooks) are most effective in accelerating AI adoption in conservative enterprises?
- **Important Primitives:** Adoption tracking dashboards, training modules, trust calibration metrics, phased rollout plans.
- **Types of Systems to Investigate:** Enterprise transformation methodologies, change management consulting frameworks.
- **Relevant Academic Traditions:** Organizational change management, diffusion of innovations, change psychology.
- **Evidence Required:** Employee adoption velocity, active daily user retention rates over 12 months.
- **Maturity Dimensions:** Maturity, adoption, impact.
- **Commoditization Questions:** Change management is largely a professional services capability rather than commoditized software.
- **Potential Moat Questions:** Software-embedded transformation playbooks that automate change management tracking.
- **Greenfield/Brownfield Implications:** Brownfield transformation relies entirely on rigorous change management; greenfield avoids it.
- **Single/Multi-Org Implications:** Must be adaptable across diverse corporate cultures within holding company portfolios.
- **Dependencies:** Relies on Domain 11.2 (Human-AI Teaming) and Domain 12.3 (Implementation Services).

#### 11.4 Complex Adaptive Systems & Organizational Behavior

- **Definition:** Theoretical frameworks treating organizations as complex adaptive networks of autonomous agents whose macro-behavior emerges from micro-interactions.
- **Why it matters to CAT:** Provides the theoretical lens to understand how multi-agent and human-AI systems behave under systemic stress or rapid scaling.
- **Key Research Questions:** How do emergent systemic behaviors and unintended feedback loops manifest in large multi-agent organizational networks?
- **Important Primitives:** Agent-based modeling (ABM), emergent behavior analysis, resilience stress-testing.
- **Types of Systems to Investigate:** Enterprise simulation engines, agent-based macroeconomic and organizational models.
- **Relevant Academic Traditions:** Complex adaptive systems theory, cybernetics, organizational sociology.
- **Evidence Required:** Simulation accuracy in predicting organizational bottlenecks and failure modes.
- **Maturity Dimensions:** Maturity, theoretical rigor, predictability.
- **Commoditization Questions:** Academic and theoretical domain; low direct commoditization risk.
- **Potential Moat Questions:** Proprietary enterprise simulation engines used to stress-test organizational structures before deployment.
- **Greenfield/Brownfield Implications:** Applicable to designing greenfield holding structures or restructuring brownfield enterprises.
- **Single/Multi-Org Implications:** Highly relevant for modeling multi-organization holding company dynamics.
- **Dependencies:** Relies on Domain 3.1 (Multi-Agent Systems) and Domain 10.2 (Topologies).

### DOMAIN 12 — CUSTOMER JOBS-TO-BE-DONE & ADOPTION

#### 12.1 Buyer, User & Beneficiary Segmentation

- **Definition:** Analysis distinguishing between the economic buyer (C-suite/procurement), the daily user (knowledge workers/managers), and the organizational beneficiary.
- **Why it matters to CAT:** Ensures product go-to-market and UX design address conflicting incentives among stakeholders.
- **Key Research Questions:** How do purchasing decisions differ when the economic buyer seeks top-down cost reduction while the daily user fears displacement?
- **Important Primitives:** Stakeholder mapping matrices, value proposition alignment frameworks, persona requirement specs.
- **Types of Systems to Investigate:** B2B enterprise sales architectures, customer discovery frameworks.
- **Relevant Academic Traditions:** Product management theory, B2B marketing, consumer behavior.
- **Evidence Required:** Sales conversion rates, win/loss analysis reports across buyer personas.
- **Maturity Dimensions:** Market readiness, commercial maturity.
- **Commoditization Questions:** Standard commercial go-to-market methodology.
- **Potential Moat Questions:** Deep understanding of specific vertical buyer pain points.
- **Greenfield/Brownfield Implications:** Greenfield targets agile founders/builders; brownfield targets risk-averse CIOs and compliance officers.
- **Single/Multi-Org Implications:** Multi-org buyers require holding-level executive dashboards.
- **Dependencies:** Relies on Domain 12.2 (Jobs-to-Be-Done) and Domain 13.2 (Pricing).

#### 12.2 Customer Jobs-to-Be-Done

- **Definition:** Identifying the underlying functional, emotional, and social progress customers are trying to make when hiring an AI organizational platform.
- **Why it matters to CAT:** Prevents building technologically impressive features that fail to solve urgent, high-value enterprise problems.
- **Key Research Questions:** What specific operational jobs suffer from high error rates and high labor costs that make them prime wedges for AI automation?
- **Important Primitives:** JTBD interview frameworks, pain-point prioritization matrices, core workflow bottleneck identification.
- **Types of Systems to Investigate:** Customer discovery transcripts, workflow failure logs.
- **Relevant Academic Traditions:** Clayton Christensen JTBD theory, product design methodology.
- **Evidence Required:** Customer willingness-to-pay validation metrics, frequency of target job execution.
- **Maturity Dimensions:** Market validation, commercial fit.
- **Commoditization Questions:** Research methodology; not commoditizable.
- **Potential Moat Questions:** Identifying an unserved, high-value enterprise wedge that incumbents ignore.
- **Greenfield/Brownfield Implications:** Greenfield jobs center on rapid venture creation; brownfield jobs center on cost reduction and compliance.
- **Single/Multi-Org Implications:** Multi-org jobs involve cross-company portfolio management and resource allocation.
- **Dependencies:** Relies on Domain 12.1 (Segmentation) and Domain 9.2 (Process Discovery).

#### 12.3 Implementation, Onboarding & Professional Services

- **Definition:** The consulting, onboarding, and custom integration services required to deploy and configure the platform within an enterprise.
- **Why it matters to CAT:** Determines whether the business scales as pure software (SaaS) or requires heavy professional services deployment.
- **Key Research Questions:** Can enterprise deployment be fully productized (self-serve), or does brownfield transformation permanently require high-touch professional services?
- **Important Primitives:** Implementation playbooks, automated onboarding wizards, customer success milestone trackers.
- **Types of Systems to Investigate:** Professional-services-enabled software models, enterprise customer success architectures.
- **Relevant Academic Traditions:** Enterprise software delivery, service-dominant logic.
- **Evidence Required:** Time-to-value (TTV) metrics, professional services gross margin reports.
- **Maturity Dimensions:** Commercial scalability, operational maturity.
- **Commoditization Questions:** Professional services are notoriously difficult to commoditize but suffer from linear headcount scaling limits.
- **Potential Moat Questions:** Proprietary onboarding automation assets that reduce professional services overhead while accelerating time-to-value.
- **Greenfield/Brownfield Implications:** Greenfield requires minimal onboarding; brownfield demands extensive implementation services.
- **Single/Multi-Org Implications:** Multi-org rollouts require structured holding-company onboarding sequencing.
- **Dependencies:** Relies on Domain 11.3 (Change Management) and Domain 13.3 (SaaS vs. Services).

### DOMAIN 13 — ECONOMICS & BUSINESS MODELS

#### 13.1 Automation & Labor Arbitrage Economics

- **Definition:** Economic frameworks evaluating the cost of compute (tokens, infrastructure) versus human labor costs across various enterprise tasks.
- **Why it matters to CAT:** Establishes the fundamental economic viability and margin profile of substituting AI agents for human labor.
- **Key Research Questions:** At what token-to-labor cost ratio does autonomous agent execution become economically superior to human offshore or onshore labor?
- **Important Primitives:** Cost-per-task models, human labor hour equivalency metrics, token expenditure attribution.
- **Types of Systems to Investigate:** Labor arbitrage economic models, unit economics calculators.
- **Relevant Academic Traditions:** Labor economics, engineering economics, cost-benefit analysis.
- **Evidence Required:** Empirical cost comparisons between human-executed workflows and AI-executed workflows.
- **Maturity Dimensions:** Economic viability, scalability.
- **Commoditization Questions:** Compute cost deflation driven by hardware advancements continuously alters the economic threshold.
- **Potential Moat Questions:** Proprietary workflow efficiency that achieves higher task completion per token than generic models.
- **Greenfield/Brownfield Implications:** Greenfield avoids legacy labor overhead; brownfield must navigate existing headcount economics.
- **Single/Multi-Org Implications:** Economics scale favorably when reusable workflows are deployed across multiple portfolio organizations.
- **Dependencies:** Relies on Domain 8.3 (Cost Optimization) and Domain 13.2 (Pricing).

#### 13.2 Pricing, Value Metrics & Unit Economics

- **Definition:** Models determining how the platform captures value (e.g., per-seat SaaS, consumption/token pricing, outcome-based pricing, or revenue share).
- **Why it matters to CAT:** Traditional per-seat pricing fails when AI reduces headcount; alternative pricing models must align with value creation.
- **Key Research Questions:** Does outcome-based pricing or consumption pricing provide superior predictability and customer alignment for agentic platforms?
- **Important Primitives:** Value metric definitions, consumption tier meters, gross margin per workflow metrics.
- **Types of Systems to Investigate:** Usage-based billing engines (Lago, Stripe Billing), outcome pricing contracts.
- **Relevant Academic Traditions:** Pricing strategy, microeconomics, software pricing models.
- **Evidence Required:** Customer acceptance rates for alternative pricing structures, net revenue retention (NRR) benchmarks.
- **Maturity Dimensions:** Commercial maturity, financial viability.
- **Commoditization Questions:** Billing infrastructure is commoditized, but pricing metric design is strategic.
- **Potential Moat Questions:** Value metrics tied directly to business outcomes that create unassailable pricing power.
- **Greenfield/Brownfield Implications:** Greenfield ventures often favor equity/revenue share models; brownfield enterprises prefer predictable SaaS subscriptions.
- **Single/Multi-Org Implications:** Multi-org systems require hierarchical cost allocation and inter-company billing meters.
- **Dependencies:** Relies on Domain 13.1 (Automation Economics) and Domain 13.3 (SaaS vs. Services).

#### 13.3 SaaS vs. Services Business Models

- **Definition:** The strategic tension between maintaining high-margin, scalable software (SaaS) versus capturing high-revenue transformation services (professional services).
- **Why it matters to CAT:** Dictates the valuation multiple, capital requirements, and operational complexity of the business.
- **Key Research Questions:** Can an AI-native organizational platform scale as a pure software product, or is a hybrid "services-enabled software" model mandatory during early market formation?
- **Important Primitives:** Gross margin analysis, revenue mix ratios, headcount scaling curves.
- **Types of Systems to Investigate:** Hybrid tech-enabled services companies, venture studios, vertical SaaS business models.
- **Relevant Academic Traditions:** Business strategy, corporate finance, venture capital economics.
- **Evidence Required:** Historical financial models of software vs. hybrid services margins in emerging technology categories.
- **Maturity Dimensions:** Financial scalability, operational maturity.
- **Commoditization Questions:** Pure software margins face downward pressure if heavy customization services are required.
- **Potential Moat Questions:** A product architecture that progressively productizes professional services into self-serve software modules.
- **Greenfield/Brownfield Implications:** Greenfield leans toward pure SaaS; brownfield transformation frequently requires heavy professional services.
- **Single/Multi-Org Implications:** Multi-org holding companies (like venture studios) inherently blend software platforms with operational services.
- **Dependencies:** Relies on Domain 12.3 (Implementation Services) and Domain 13.2 (Pricing).

### DOMAIN 14 — STRATEGY, CONTROL POINTS & MOATS

#### 14.1 Platform Control Points & Ecosystem Leverage

- **Definition:** Strategic positions within the enterprise technology stack (e.g., identity, data integration, workflow orchestration, memory) that dictate ecosystem leverage and pricing power.
- **Why it matters to CAT:** Identifies where independent products can capture sustainable economic value without being commoditized by hyperscalers.
- **Key Research Questions:** Which layers of the emerging agentic stack represent defensible control points versus transient wrapper layers?
- **Important Primitives:** Ecosystem lock-in mechanisms, developer platform APIs, proprietary data switchboards.
- **Types of Systems to Investigate:** Operating system control points, enterprise platform architectures (Salesforce, ServiceNow).
- **Relevant Academic Traditions:** Competitive strategy, platform economics, industry value chain analysis.
- **Evidence Required:** Ecosystem partner dependency metrics, platform switching cost analyses.
- **Maturity Dimensions:** Strategic defensibility, market maturity.
- **Commoditization Questions:** Hyperscalers (AWS, Azure, GCP) and foundational model providers are actively attempting to colonize application orchestration layers.
- **Potential Moat Questions:** Owning the secure enterprise knowledge graph and cross-system orchestration switchboard.
- **Greenfield/Brownfield Implications:** Greenfield platforms can establish new control points; brownfield platforms must displace or integrate with incumbent control points.
- **Single/Multi-Org Implications:** Multi-org holding structures require holding-level platform control points.
- **Dependencies:** Relies on Domain 14.2 (Moats) and Domain 14.3 (Competitor Response).

#### 14.2 Moat Mechanisms & Data Network Effects

- **Definition:** Structural barriers to entry (e.g., data network effects, proprietary workflows, switching costs, regulatory certifications) that protect the business from competitors.
- **Why it matters to CAT:** Evaluates the long-term durability of the company against copycats and well-capitalized incumbents.
- **Key Research Questions:** Do cross-company data network effects actually compound in enterprise AI platforms without violating data privacy boundaries?
- **Important Primitives:** Proprietary data exhaust loops, federated learning feedback, switching cost barriers, compliance moats.
- **Types of Systems to Investigate:** Network effect business models, enterprise software defensibility frameworks.
- **Relevant Academic Traditions:** Strategic management (Porter's frameworks), network economics.
- **Evidence Required:** Churn rate benchmarks, customer retention curves, data flywheel velocity metrics.
- **Maturity Dimensions:** Defensibility, maturity.
- **Commoditization Questions:** Standard software features are easily copied; moats must derive from proprietary data or deep workflow integration.
- **Potential Moat Questions:** Accumulated human correction data exhaust that trains superior domain-specific execution policies.
- **Greenfield/Brownfield Implications:** Brownfield moats derive from deep legacy system entanglement; greenfield moats derive from proprietary network effects.
- **Single/Multi-Org Implications:** Multi-org portfolios generate internal network effects by sharing validated operational schemas across subsidiary entities.
- **Dependencies:** Relies on Domain 14.1 (Control Points) and Domain 14.3 (Competitor Response).

#### 14.3 Competitive Dynamics & Incumbent/Hyperscaler Response

- **Definition:** Strategic analysis of how legacy enterprise software giants (SAP, Salesforce, Microsoft) and hyperscalers (AWS, Azure) will respond to emerging agentic startups.
- **Why it matters to CAT:** Prevents building a startup product that can be instantly crushed by a native feature release from Microsoft or Salesforce.
- **Key Research Questions:** How do enterprise incumbents typically absorb or neutralize startup wedges in workflow automation and AI orchestration?
- **Important Primitives:** Feature parity tracking, ecosystem bundling analyses, acquisition target criteria.
- **Types of Systems to Investigate:** Incumbent AI roadmaps (Microsoft Copilot Studio, Salesforce Agentforce, ServiceNow Now Assist).
- **Relevant Academic Traditions:** Disruption theory (Clayton Christensen), competitive dynamics, strategic management.
- **Evidence Required:** Incumbent product release velocity, enterprise customer multi-vendor tolerance data.
- **Maturity Dimensions:** Competitive landscape maturity.
- **Commoditization Questions:** Hyperscalers commoditize foundational capabilities; startups must wedge into specialized workflows.
- **Potential Moat Questions:** Agility and deep vertical workflow mastery that legacy incumbents move too slowly to capture.
- **Greenfield/Brownfield Implications:** Brownfield is heavily contested by incumbents; greenfield allows out-of-bounds innovation.
- **Single/Multi-Org Implications:** Multi-org holding structures operate outside typical single-enterprise software sales motions.
- **Dependencies:** Relies on Domain 14.1 (Control Points) and Domain 12.2 (Jobs-to-Be-Done).

### DOMAIN 15 — LIFECYCLE, DEPLOYMENT MODES & SCALING

#### 15.1 Greenfield Creation vs. Brownfield Transformation

- **Definition:** Comparative evaluation of building brand-new AI-native ventures from scratch (Greenfield) versus transforming legacy traditional enterprises (Brownfield).
- **Why it matters to CAT:** Dictates product go-to-market focus, architectural complexity, and revenue acceleration velocity.
- **Key Research Questions:** What are the fundamental differences in product architecture required to support a zero-legacy greenfield venture studio versus a legacy brownfield enterprise transformation?
- **Important Primitives:** Greenfield venture bootstrapping templates, brownfield legacy migration frameworks, dual-track operational models.
- **Types of Systems to Investigate:** Venture studios, digital transformation playbooks, greenfield startup accelerators.
- **Relevant Academic Traditions:** Entrepreneurship theory, organizational transformation, corporate venturing.
- **Evidence Required:** Time-to-market and capital efficiency comparisons between greenfield and brownfield deployment strategies.
- **Maturity Dimensions:** Operational maturity, scalability.
- **Commoditization Questions:** Transformation methodology is consulting-driven; software tooling varies widely by environment.
- **Potential Moat Questions:** A unified platform capable of operating seamlessly across both greenfield creation and brownfield migration.
- **Greenfield/Brownfield Implications:** Directly governs the fundamental product architecture and target market selection.
- **Single/Multi-Org Implications:** Greenfield often starts single-org; brownfield and holding companies frequently operate multi-org structures.
- **Dependencies:** Relies on Domain 9.1 (Integration) and Domain 12.2 (Jobs-to-Be-Done).

#### 15.2 Single-Organization vs. Multi-Organization/Portfolio Systems

- **Definition:** Architectural and organizational requirements for managing a single operating company versus a portfolio of multiple interconnected subsidiary entities (holding companies/venture studios).
- **Why it matters to CAT:** Tests whether multi-organization coordination (Alphabet layer topologies, cross-subsidiary resource sharing) is a viable product architecture or an unnecessary complication.
- **Key Research Questions:** What architectural overhead is introduced by scaling from a single-tenant enterprise platform to a multi-organization holding company structure?
- **Important Primitives:** Multi-tenant subsidiary isolation, holding-level parent agent routing, cross-company playbook sharing schemas.
- **Types of Systems to Investigate:** Venture studio operating systems, multi-subsidiary corporate governance architectures.
- **Relevant Academic Traditions:** Holding company economics, conglomerate strategy, multi-tenant systems architecture.
- **Evidence Required:** Cross-subsidiary coordination overhead metrics, multi-tenant security audit logs.
- **Maturity Dimensions:** Scalability, architectural maturity, security.
- **Commoditization Questions:** Enterprise multi-tenancy is standard; multi-organizational holding company software is highly nascent.
- **Potential Moat Questions:** Proprietary multi-organization coordination and resource-sharing protocols designed for holding companies and venture studios.
- **Greenfield/Brownfield Implications:** Greenfield venture studios naturally adopt multi-org portfolio structures; brownfield enterprises typically remain single-org.
- **Single/Multi-Org Implications:** Defines the core structural boundary of the platform.
- **Dependencies:** Relies on Domain 6.1 (Identity) and Domain 10.2 (Topologies).

### DOMAIN 16 — NON-AGENT ALTERNATIVES & BASELINES

#### 16.1 Deterministic Software, BPM & Workflow Automation

- **Definition:** Traditional rule-based software, Business Process Management (BPM) suites, and deterministic workflow engines that execute logic without probabilistic LLM components.
- **Why it matters to CAT:** Serves as the primary baseline comparison to prove whether probabilistic agentic systems deliver superior ROI over rigid deterministic code.
- **Key Research Questions:** For what percentage of enterprise workflows do deterministic BPM engines outperform probabilistic agents in reliability and cost?
- **Important Primitives:** Conditional logic branches, rigid process flowcharts, deterministic decision tables, rule engines.
- **Types of Systems to Investigate:** Camunda, Appian, Pegasystems, traditional workflow automation suites.
- **Relevant Academic Traditions:** Business process management, computer science automata theory, software engineering.
- **Evidence Required:** Development time, maintenance overhead, and error rate comparisons between BPM and agentic workflows.
- **Maturity Dimensions:** Reliability, maturity, determinism.
- **Commoditization Questions:** BPM and deterministic workflow software are mature, highly commoditized enterprise markets.
- **Potential Moat Questions:** None; serves as the baseline comparison set.
- **Greenfield/Brownfield Implications:** Heavily entrenched in brownfield enterprises; often bypassed in agile greenfield builds.
- **Single/Multi-Org Implications:** Supports multi-tenant execution through enterprise BPM server deployments.
- **Dependencies:** Relies on Domain 3.2 (Workflow Engines).

#### 16.2 RPA, iPaaS & ERP/CRM-Native Automation

- **Definition:** Robotic Process Automation (UI screen scraping), Integration Platform as a Service (API pipelines), and native automation builders inside enterprise suites (Salesforce Flow, Power Automate).
- **Why it matters to CAT:** Represents the existing status-quo automation tooling that enterprises use before considering AI agents.
- **Key Research Questions:** Where do brittle RPA screen-scraping bots and rigid iPaaS pipelines break down when handling unstructured enterprise data and dynamic tasks?
- **Important Primitives:** UI click bots, webhook trigger pipelines, point-to-point API connectors, native form automation.
- **Types of Systems to Investigate:** UiPath, Automation Anywhere, Zapier, Workato, Microsoft Power Automate, Salesforce Flow.
- **Relevant Academic Traditions:** Systems integration, enterprise software engineering.
- **Evidence Required:** Maintenance break-fix frequency for RPA bots versus autonomous agents when underlying UI/APIs change.
- **Maturity Dimensions:** Maturity, reliability, enterprise adoption.
- **Commoditization Questions:** Highly mature, multi-billion-dollar incumbent markets rapidly adding AI wrappers.
- **Potential Moat Questions:** None as baseline; comparison focuses on adaptability to unstructured tasks.
- **Greenfield/Brownfield Implications:** Ubiquitous in brownfield enterprises; less common in greenfield ventures.
- **Single/Multi-Org Implications:** Operates within enterprise boundaries; struggles with cross-organizational fluid coordination.
- **Dependencies:** Relies on Domain 9.1 (Enterprise Integration).

#### 16.3 Enterprise Search, Knowledge Management & Data Platforms

- **Definition:** Traditional enterprise search engines, document management systems, and data lakes used to store and retrieve company documents without generative AI synthesis.
- **Why it matters to CAT:** Serves as the baseline for knowledge retrieval and storage against advanced GraphRAG and multi-tier memory architectures.
- **Key Research Questions:** Why do traditional enterprise search tools (keyword/lexical search) fail to satisfy complex knowledge work queries compared to agentic RAG?
- **Important Primitives:** Keyword indexing, hierarchical folder structures, document tagging, SQL data warehouses.
- **Types of Systems to Investigate:** SharePoint, Confluence, Elasticsearch, traditional enterprise search appliances.
- **Relevant Academic Traditions:** Information retrieval, library science, database management.
- **Evidence Required:** User search success rates and time-to-find metrics comparing traditional search vs. agentic memory systems.
- **Maturity Dimensions:** Maturity, reliability, security.
- **Commoditization Questions:** Extremely mature, highly commoditized enterprise infrastructure.
- **Potential Moat Questions:** None; baseline comparison.
- **Greenfield/Brownfield Implications:** Deeply embedded in brownfield enterprises; greenfield ventures often start with modern cloud docs.
- **Single/Multi-Org Implications:** Managed via enterprise-wide directory services and access control lists.
- **Dependencies:** Relies on Domain 5.4 (Retrieval).

#### 16.4 Human-Operated Processes & Managed Services Baselines

- **Definition:** The status-quo baseline where business processes are executed entirely by human personnel, offshore outsourcing agencies, or professional services firms.
- **Why it matters to CAT:** The ultimate economic benchmark against which all automation, AI agents, and software platforms must be measured.
- **Key Research Questions:** What is the exact fully-loaded cost and error rate of human-operated baselines across target enterprise workflows?
- **Important Primitives:** Headcount rosters, outsourcing service level agreements (SLAs), manual quality assurance reviews.
- **Types of Systems to Investigate:** Business process outsourcing (BPO) firms, professional services agencies, internal manual teams.
- **Relevant Academic Traditions:** Operations management, labor economics, organizational behavior.
- **Evidence Required:** Comprehensive baseline cost-per-output metrics for manual human workflows.
- **Maturity Dimensions:** Human adaptability, operational maturity.
- **Commoditization Questions:** Global labor markets provide continuous benchmark pricing.
- **Potential Moat Questions:** None; ultimate baseline comparison.
- **Greenfield/Brownfield Implications:** Present in all brownfield enterprises; minimized in greenfield ventures.
- **Single/Multi-Org Implications:** Operates across all organizational topologies.
- **Dependencies:** Relies on Domain 13.1 (Automation Economics).

## IV. Cross-Cutting & Strategic Matrices

### A. Cross-Cutting Evaluation Dimensions

- **Reliability:** The statistical consistency of task completion without unhandled failures or silent errors.
- **Security:** Resistance to prompt injection, unauthorized data exfiltration, and privilege escalation.
- **Cost:** Total compute, token, infrastructure, and human oversight expenditure per successful business outcome.
- **Latency:** Time elapsed from user prompt submission to final verified workflow execution.
- **Interoperability:** Standardized protocol compliance and ease of integration with external systems.
- **Autonomy:** Degree of self-directed execution versus required human intervention.
- **Human Oversight:** Effectiveness and ergonomics of approval gates, audit trails, and override controls.
- **Maturity:** Stability, documentation, and production-readiness of underlying technologies.
- **Portability:** Ease of migrating workloads across cloud providers, VPCs, and model endpoints.
- **Regulatory Exposure:** Compliance adherence with data privacy laws, SOC2, HIPAA, and industry regulations.
- **Observability:** Depth of execution tracing, telemetry logging, and debug visibility.
- **Recoverability:** Graceful degradation, idempotency enforcement, and rollback mechanics following failures.
- **Learning Potential:** Capacity of the system to improve automatically from historical execution data and human feedback.

### B. Greenfield/Brownfield × Single/Multi-Org Coverage Matrix

| Deployment Dimension | Single-Organization Scope | Multi-Organization / Portfolio Scope |
|---|---|---|
| **Greenfield Creation** | Quadrant I (Venture Startup): Rapid greenfield build of a single AI-native operating company with clean data schemas and native agent loops. | Quadrant II (Venture Studio): Creation of a multi-subsidiary holding company where parent-level agents coordinate resources across newly spawned ventures. |
| **Brownfield Transformation** | Quadrant III (Enterprise Modernization): Retrofitting an existing legacy enterprise with secure agent wrappers, IAM integration, and process discovery. | Quadrant IV (Conglomerate Transformation): Overhauling a multi-division legacy holding company with cross-border data sovereignty and distributed governance. |

### C. Control-Point Research Map

```
+-----------------------------------------------------------------------------------+
| EMERGING AI ORGANIZATIONAL STACK CONTROL POINTS                                    |
+-----------------------------------------------------------------------------------+
| 1. Strategic Layer: Transformation Economics & Governance Standards               |
| 2. Orchestration Layer: Knowledge Graph Memory & Conductor Engine Switchboard     |
| 3. Execution Layer: Agent Runtimes, Tool Registries & Interoperability Protocols  |
| 4. Infrastructure Layer: Foundation Models, VPC Compute & Storage Hardware        |
+-----------------------------------------------------------------------------------+
```

### D. Non-Agent Baseline Map

- **Deterministic Workflows:** Tested against probabilistic agent drift and failure rates.
- **RPA & iPaaS:** Tested against brittle UI/API fragility versus dynamic agent adaptation.
- **Enterprise Search & Knowledge Bases:** Tested against GraphRAG and multi-tier memory synthesis.
- **Human-Operated BPO Baselines:** Tested against total cost-per-task economics and latency trade-offs.

### E. Academic / Research Traditions Map

- **Computer Science & Distributed Systems:** Actor-model concurrency, distributed transactions, formal state verification.
- **Artificial Intelligence & Cognitive Science:** Multi-agent systems (MAS), automated planning, cognitive memory models.
- **Organizational Science & Economics:** Transaction cost economics, complex adaptive systems, organizational behavior, agency theory.
- **Human-Computer Interaction (HCI):** Algorithmic management, collaborative mixed-initiative workspaces, trust calibration.

### F. Build / Buy / Partner / Integrate Research Map

- **Build Candidates:** Core organizational routing logic, proprietary knowledge graph distillation, workflow state machine wrappers.
- **Buy / License Candidates:** Foundation models, vector databases, graph database engines, standard monitoring telemetry.
- **Partner / Integrate Candidates:** Enterprise IAM systems (Okta/Azure AD), legacy iPaaS connectors, cloud VPC infrastructure.

## V. Final Coverage Stress Test

- **Can this taxonomy discover that agents are NOT the correct abstraction?** Yes. Domain 16 (Non-Agent Alternatives) and Domain 3.2 (Deterministic Workflow Engines) explicitly force comparison against non-agentic paradigms, allowing research to conclude that deterministic software outperforms agents.
- **Can it discover that CAT should NOT exist?** Yes. Domain 13 (Economics) and Domain 14.3 (Incumbent Response) evaluate market viability and hyperscaler commoditization, enabling evidence-based falsification of CAT's commercial premise.
- **Can it discover that the value belongs inside an incumbent platform?** Yes. Domain 14.1 and Domain 14.3 specifically investigate hyperscaler and enterprise incumbent responses to determine if control points reside with Microsoft, Salesforce, or AWS.
- **Can it discover a narrow control point rather than an OS?** Yes. The granular taxonomy separates memory, identity, execution, and orchestration, permitting isolation of a hyper-specific wedge rather than an expansive operating system.
- **Can it discover a services-heavy business rather than SaaS?** Yes. Domain 13.3 explicitly evaluates SaaS versus professional services economics and brownfield onboarding realities.
- **Remaining Blind Spots:** None identified; the ontology comprehensively covers technical, organizational, economic, academic, and competitive dimensions without presupposing conclusions.
