# 03_AI_NATIVE_ORGANIZATION_RESEARCH_TAXONOMY_v3

## I. Taxonomy Audit & Comparative Mapping

To ensure the research taxonomy is sufficiently granular and does not prematurely anchor on historical biases, this audit maps the domains against both prior assumptions and emerging candidate architectures.

- **AREAS REQUIRING EMPIRICAL VALIDATION:** Distributed actor-model coordination semantics, automated process mining/discovery, enterprise search index harmonization, deterministic rules engines, and complex adaptive systems organizational behaviors.
- **CANDIDATE ARCHITECTURES FOR INVESTIGATION:** Foundation model routing, basic agent runtimes, tool registries, multi-agent frameworks, RBAC policies, and core vector/graph retrieval techniques.
- **EXPANDED RESEARCH REQUIREMENTS:** Formal economic modeling of net value creation, semantic drift detection in state systems, objective alignment, legal liability distribution frameworks for autonomous agent errors, and multi-organization supply-chain contract choreography.

## II. Detailed Research Taxonomy Hierarchy

**DOMAIN 1 --- MODEL / INTELLIGENCE & REASONING**
- 1.1 Foundation Models & Inference Routing
- 1.2 Reasoning, Planning & Decomposition

**DOMAIN 2 --- AGENT EXECUTION & HARNESSES**
- 2.1 Agent Runtimes & Execution Environments
- 2.2 Agent Harnesses & Control Loops
- 2.3 Single-Agent Architectures

**DOMAIN 3 --- MULTI-AGENT COORDINATION & WORKFLOW**
- 3.1 Multi-Agent Systems & Topologies
- 3.2 Workflow Engines & State Machines
- 3.3 Durable Execution & Fault Tolerance
- 3.4 Event-Driven & Actor-Model Systems

**DOMAIN 4 --- TOOLS, SKILLS & INTEROPERABILITY**
- 4.1 Tool Discovery, Selection & Invocation
- 4.2 Skills & Capability Registries (Including Learning Lifecycles)
- 4.3 Interoperability Protocols (MCP & A2A)

**DOMAIN 5 --- STATE, MEMORY & KNOWLEDGE**
- 5.1 Organizational State & Memory Systems
- 5.2 Long-Context Architecture & Optimization
- 5.3 Knowledge Graphs & Ontologies
- 5.4 Retrieval Systems & Context Engineering

**DOMAIN 6 --- IDENTITY, SECURITY & GOVERNANCE**
- 6.1 Identity, Authentication & Granular Authorization
- 6.2 Policy, Guardrails & Governance Frameworks
- 6.3 Human Approvals, Intervention & Escalation
- 6.4 Sandboxing, Execution Security & Secrets Management

**DOMAIN 7 --- EVALUATION, OBSERVABILITY & IMPROVEMENT**
- 7.1 Observability, Tracing & Telemetry
- 7.2 Evaluation & Benchmarking Frameworks
- 7.3 System Self-Evaluation & Authority Optimization Spectrums
- 7.4 Automated System Evolution & Code Generation

**DOMAIN 8 --- INFRASTRUCTURE, RELIABILITY & DEPLOYMENT**
- 8.1 Deployment Infrastructure & VPC/On-Premise Topologies
- 8.2 Reliability, Recovery & Idempotency
- 8.3 Compute, Cost & Resource Optimization

**DOMAIN 9 --- ENTERPRISE DISCOVERY, INTEGRATION & SYSTEM INTERACTION**
- 9.1 Enterprise Integration & System Interaction
- 9.2 Process Discovery & Process Mining
- 9.3 Data Ingestion, Discovery & Harmonization

**DOMAIN 10 --- ORGANIZATIONAL DESIGN & CAPABILITY COMPOSITION**
- 10.1 Objective Formation, Decomposition & Dynamic Composition
- 10.2 Organizational Topology & Team Formation
- 10.3 Organizational Authority, Delegation & Decision Rights
- 10.4 Workflow & Process Redesign
- 10.5 Resource Allocation & Decision Science
- 10.6 Legal, Liability & Accountability Coverage

**DOMAIN 11 --- HUMAN-AI ORGANIZATION & ADOPTION**
- 11.1 Institutional Knowledge & Organizational Memory
- 11.2 Human-AI Teaming & Algorithmic Management
- 11.3 Change Management & Trust Building
- 11.4 Complex Adaptive Systems & Organizational Behavior

**DOMAIN 12 --- CUSTOMER JOBS-TO-BE-DONE & ADOPTION**
- 12.1 Stakeholder & Beneficiary Segmentation
- 12.2 Customer Jobs-to-Be-Done (Value Discovery)
- 12.3 Implementation, Onboarding & Deployment Methodologies

**DOMAIN 13 --- ECONOMICS & BUSINESS MODELS**
- 13.1 AI-Native Organizational Economics & Value Creation
- 13.2 Pricing, Value Metrics & Unit Economics
- 13.3 SaaS vs. Services Business Models

**DOMAIN 14 --- STRATEGY, CONTROL POINTS & MOATS**
- 14.1 Platform Control Points & Ecosystem Leverage
- 14.2 Moat Mechanisms & Data Network Effects
- 14.3 Competitive Dynamics & Incumbent/Hyperscaler Response

**DOMAIN 15 --- LIFECYCLE, DEPLOYMENT MODES & SCALING**
- 15.1 Greenfield Creation vs. Brownfield Transformation Contexts
- 15.2 Single-Organization vs. Multi-Organization/Portfolio Systems

**DOMAIN 16 --- NON-AGENT ALTERNATIVES & BASELINES**
- 16.1 Deterministic Software, BPM & Workflow Automation
- 16.2 RPA, iPaaS & ERP/CRM-Native Automation
- 16.3 Enterprise Search, Knowledge Management & Data Platforms
- 16.4 Human-Operated Processes & Managed Services Baselines

---

## III. Category Specifications

### DOMAIN 1 --- MODEL / INTELLIGENCE & REASONING

#### 1.1 Foundation Models & Inference Routing
- **Definition:** Systems and routing strategies that select, prompt, and query underlying LLMs based on cost, latency, and capability requirements.
- **Why it matters to CAT:** Determines whether the system is tightly coupled to a single frontier model provider or can abstract model reliance.
- **Key Research Questions:** How does dynamic model routing impact reasoning stability across complex multi-step workflows? What are the failure modes of fallback logic when primary model endpoints fail?
- **Important Primitives:** Cost-latency trade-off curves, router classifiers, prompt translation layers, token-budget allocators.
- **Types of Systems to Investigate:** Semantic routers, multi-model orchestrators, API gateways.
- **Relevant Academic Traditions:** Distributed systems routing, machine learning ensemble theory.
- **Evidence Required:** Benchmark variance reports, latency overhead metrics, cost-per-successful-task analyses.
- **Maturity Dimensions to Assess:** Portability, cost efficiency, reliability.
- **Commoditization Questions:** Are model routers being absorbed directly into base model provider APIs or cloud gateways?
- **Potential Moat Questions:** Can a routing layer build a proprietary routing dataset that reliably outperforms generic enterprise routers?
- **Greenfield/Brownfield Implications:** How do routing requirements differ between open cloud architectures and environments mandating secure enterprise proxies?
- **Single/Multi-Org Implications:** How are tenant-isolated routing keys and cost attribution models enforced across multi-org boundaries?
- **Dependencies:** Interacts directly with Domain 1.2 (Reasoning) and Domain 8.3 (Compute Optimization).

#### 1.2 Reasoning, Planning & Decomposition
- **Definition:** Algorithmic mechanisms that enable models to break down complex goals into sequential sub-tasks, plan execution paths, and self-correct during execution.
- **Why it matters to CAT:** Establishes how autonomous or semi-autonomous workflows handle non-linear problem solving without rigid human scripting.
- **Key Research Questions:** Where do automated planning algorithms fail when exposed to ambiguous, multi-step enterprise tasks? How do plan-and-solve architectures compare empirically to reactive agent loops?
- **Important Primitives:** Tree-of-Thought (ToT), Graph-of-Thought (GoT), reflection loops, plan verification checkpoints.
- **Types of Systems to Investigate:** State graph frameworks, program optimizers, automated planning frameworks.
- **Relevant Academic Traditions:** Artificial intelligence classical planning, cognitive science, automated reasoning.
- **Evidence Required:** Task completion success rates across varying horizon lengths, error recovery rates.
- **Maturity Dimensions to Assess:** Autonomy, reliability, predictability.
- **Commoditization Questions:** Are advanced reasoning patterns migrating natively into frontier model weights, reducing the need for application-layer planning harnesses?
- **Potential Moat Questions:** Do domain-specific planning templates or compiled reasoning strategies create durable workflow advantages?
- **Greenfield/Brownfield Implications:** Does legacy process adherence severely constrain automated reasoning loops compared to unconstrained environments?
- **Single/Multi-Org Implications:** Can multi-org scaling leverage parameterized planning templates that respect boundary isolation?
- **Dependencies:** Relies on Domain 1.1 (Models) and Domain 3.2 (Workflow Engines).

### DOMAIN 2 --- AGENT EXECUTION & HARNESSES

#### 2.1 Agent Runtimes & Execution Environments
- **Definition:** The computational infrastructure and sandboxed runtime layers where system code, tool execution, and local operations take place.
- **Why it matters to CAT:** Defines how code execution and tool calls are isolated to prevent systemic security breaches or resource exhaustion.
- **Key Research Questions:** What are the performance and security trade-offs between containerized worker nodes, WebAssembly (Wasm) runtimes, and serverless execution?
- **Important Primitives:** Ephemeral containers, resource quotas, secure execution sandboxes, execution timeouts.
- **Types of Systems to Investigate:** Ephemeral execution services, microVM frameworks, containerized runtimes.
- **Relevant Academic Traditions:** Operating systems security, virtualization, distributed systems engineering.
- **Evidence Required:** Cold-start latency benchmarks, container escape vulnerability audits, resource overhead metrics.
- **Maturity Dimensions to Assess:** Security, reliability, performance.
- **Commoditization Questions:** Will cloud providers commoditize specialized agent execution layers natively?
- **Potential Moat Questions:** Does a tightly integrated runtime-to-orchestration feedback loop provide defensible performance or security advantages?
- **Greenfield/Brownfield Implications:** What constraints do existing corporate IT policies place on where dynamic code can execute?
- **Single/Multi-Org Implications:** How is strict multi-tenant boundary enforcement achieved at the hypervisor or container level?
- **Dependencies:** Relies on Domain 6.4 (Sandboxing) and Domain 8.1 (Deployment Infrastructure).

#### 2.2 Agent Harnesses & Control Loops
- **Definition:** The software scaffolding that wraps foundation models with memory access, tool schemas, and iteration control loops.
- **Why it matters to CAT:** Represents the core execution pattern governing how systems perceive, deliberate, and act.
- **Key Research Questions:** How do different harness architectures handle infinite loops and context saturation?
- **Important Primitives:** Turn management, stop conditions, state persistence wrappers, exception handlers.
- **Types of Systems to Investigate:** Custom control loops, generalized execution frameworks, state machine harnesses.
- **Relevant Academic Traditions:** Software engineering patterns, cybernetics, control theory.
- **Evidence Required:** Token consumption per completed task, failure propagation rates in long-running loops.
- **Maturity Dimensions to Assess:** Maturity, reliability, observability.
- **Commoditization Questions:** Are harness architectures standardizing into open-source boilerplate utilities?
- **Potential Moat Questions:** Can proprietary harness telemetry or error-handling heuristics form a defensible IP asset?
- **Greenfield/Brownfield Implications:** Does reliance on fragile external APIs require specialized harness error-handling loops?
- **Single/Multi-Org Implications:** How does the harness partition state across organizational tenants?
- **Dependencies:** Relies on Domain 2.1 (Runtimes) and Domain 5.1 (Memory).

#### 2.3 Single-Agent Architectures
- **Definition:** Systems built around a single, highly capable agent instance equipped with broad tool access and memory, operating without peer-to-peer delegation.
- **Why it matters to CAT:** Serves as the critical baseline comparison against complex multi-agent swarms to test whether multi-agent overhead is actually justified.
- **Key Research Questions:** At what point does a single-agent architecture experience context degradation or instruction following failure compared to multi-agent divisions?
- **Important Primitives:** Unified tool registries, single-context window management, monolithic system prompts.
- **Types of Systems to Investigate:** Specialized coding and workflow assistants, standalone unified instances.
- **Relevant Academic Traditions:** Cognitive architecture models, human-computer interaction.
- **Evidence Required:** Comparative task success rates between single-agent and multi-agent setups on enterprise benchmark tasks.
- **Maturity Dimensions to Assess:** Reliability, simplicity, cost efficiency.
- **Commoditization Questions:** As model context windows expand and reasoning improves, are multi-agent architectures being swallowed by single-agent capabilities?
- **Potential Moat Questions:** Can single-agent tooling optimized for specific enterprise verticals create a sticky wedge?
- **Greenfield/Brownfield Implications:** Is single-agent architecture inherently more adaptable across varying deployment environments?
- **Single/Multi-Org Implications:** What are the boundaries for a single agent traversing multi-org data?
- **Dependencies:** Relies on Domain 1.1 (Models) and Domain 5.2 (Long Context).

### DOMAIN 3 --- MULTI-AGENT COORDINATION & WORKFLOW

#### 3.1 Multi-Agent Systems & Topologies
- **Definition:** Architectures where multiple specialized agents communicate, delegate sub-tasks, and collaborate through hierarchical, mesh, or pipeline topologies.
- **Why it matters to CAT:** Tests prior historical hypotheses regarding hierarchical executive-agent necessity against the empirical reality of swarm coordination overhead.
- **Key Research Questions:** What are the failure modes (e.g., cascading hallucinations, communication deadlocks) of multi-agent swarms in production? Under what conditions does a single agent consistently outperform a multi-agent team?
- **Important Primitives:** Agent message passing, role definition schemas, supervisor-worker hierarchies, blackboard architectures.
- **Types of Systems to Investigate:** Multi-agent research frameworks, peer-to-peer communication meshes, complex topology architectures.
- **Relevant Academic Traditions:** Multi-agent systems (MAS) research, distributed artificial intelligence, game theory.
- **Evidence Required:** Communication overhead costs (tokens/latency), error amplification rates across agent hops.
- **Maturity Dimensions to Assess:** Maturity, reliability, autonomy.
- **Commoditization Questions:** Are multi-agent orchestration frameworks becoming commoditized libraries with low pricing power?
- **Potential Moat Questions:** Do specialized multi-agent coordination protocols for specific enterprise workflows create lock-in?
- **Greenfield/Brownfield Implications:** Does mapping multi-agent topologies to existing organizational charts create friction?
- **Single/Multi-Org Implications:** How is cross-boundary messaging security enforced in multi-org environments?
- **Dependencies:** Relies on Domain 3.2 (Workflow Engines) and Domain 4.3 (Interoperability).

#### 3.2 Workflow Engines & State Machines
- **Definition:** Deterministic software infrastructure that defines, sequences, and tracks execution paths using explicit state machines rather than probabilistic LLM branching.
- **Why it matters to CAT:** Enforces structural determinism where probabilistic behavior could otherwise lead to unpredictable enterprise states.
- **Key Research Questions:** How should probabilistic outputs interface with deterministic state machine transitions without breaking workflow integrity?
- **Important Primitives:** Directed Acyclic Graphs (DAGs), finite state machines, transition guards, node retry policies.
- **Types of Systems to Investigate:** Distributed state graph engines, legacy workflow orchestrators, custom directed graphs.
- **Relevant Academic Traditions:** Workflow management systems, formal verification, computer science automata theory.
- **Evidence Required:** Workflow failure recovery rates, state corruption incidence metrics.
- **Maturity Dimensions to Assess:** Reliability, maturity, portability.
- **Commoditization Questions:** Are enterprise workflow engines universally available primitives that offer no proprietary value?
- **Potential Moat Questions:** Can tightly coupled LLM-to-state-machine compilation tools form a defensible developer platform?
- **Greenfield/Brownfield Implications:** Is state machine enforcement strictly necessary for interacting with non-idempotent legacy APIs?
- **Single/Multi-Org Implications:** Do multi-tenant state definitions require unique scoping logic?
- **Dependencies:** Relies on Domain 3.3 (Durable Execution) and Domain 8.2 (Reliability).

#### 3.3 Durable Execution & Fault Tolerance
- **Definition:** Infrastructure that captures the exact state of long-running workflows so they can survive process crashes, timeouts, or network interruptions without data loss.
- **Why it matters to CAT:** Enterprise workflows spanning hours or days require guarantees that a server restart will not corrupt multi-step actions.
- **Key Research Questions:** What is the performance overhead of maintaining durable execution logs for high-frequency probabilistic interactions?
- **Important Primitives:** Event sourcing, command query responsibility segregation (CQRS), state check-pointing, automatic replay.
- **Types of Systems to Investigate:** Durable function runtimes, cloud-native orchestrators.
- **Relevant Academic Traditions:** Distributed systems consistency, database transaction management (ACID properties).
- **Evidence Required:** Recovery time objectives (RTO) and recovery point objectives (RPO) under simulated node crashes.
- **Maturity Dimensions to Assess:** Reliability, recoverability, maturity.
- **Commoditization Questions:** Is durable execution purely an infrastructure commodity provided by cloud primitives?
- **Potential Moat Questions:** Can specialized durable state management optimized for non-deterministic AI tasks provide an edge over generic workflow systems?
- **Greenfield/Brownfield Implications:** How does interacting with fragile external APIs increase dependency on durable execution?
- **Single/Multi-Org Implications:** How must execution state storage be partitioned by tenant ID to prevent data leaks?
- **Dependencies:** Relies on Domain 3.2 (Workflow Engines) and Domain 8.2 (Reliability).

#### 3.4 Event-Driven & Actor-Model Systems
- **Definition:** Architectural patterns where independent computational entities communicate exclusively through asynchronous message passing and react to system events.
- **Why it matters to CAT:** Provides an alternative to centralized orchestration, allowing autonomous entities to operate as decentralized, loosely coupled actors.
- **Key Research Questions:** How do actor-model concurrency and event-driven streams scale when handling thousands of concurrent enterprise interactions?
- **Important Primitives:** Event brokers, actor mailboxes, asynchronous message passing, publish-subscribe topologies.
- **Types of Systems to Investigate:** Actor systems, enterprise event stream platforms.
- **Relevant Academic Traditions:** Actor model of concurrent computation, event-driven architecture design.
- **Evidence Required:** Message throughput, latency distributions under high load, deadlock frequency.
- **Maturity Dimensions to Assess:** Scalability, maturity, portability.
- **Commoditization Questions:** Does commoditized event streaming infrastructure capture the majority of the value?
- **Potential Moat Questions:** Could proprietary event-schema registries or domain event taxonomies offer integration lock-in?
- **Greenfield/Brownfield Implications:** Can systems tap directly into existing corporate webhooks and legacy message queues?
- **Single/Multi-Org Implications:** What mechanisms guarantee tenant-scoped event routing?
- **Dependencies:** Relies on Domain 3.1 (Multi-Agent Systems) and Domain 8.1 (Infrastructure).

### DOMAIN 4 --- TOOLS, SKILLS & INTEROPERABILITY

#### 4.1 Tool Discovery, Selection & Invocation
- **Definition:** Mechanisms that allow systems to dynamically discover, select, and execute external APIs, code functions, or software tools based on semantic intent.
- **Why it matters to CAT:** As the number of available enterprise tools scales past hundreds, static tool binding fails, necessitating dynamic selection.
- **Key Research Questions:** How does tool-space interference scale as the number of available tools increases? What mechanisms prevent the selection of incorrect or destructive tools?
- **Important Primitives:** Tool description embeddings, vector-based tool search (Tool RAG), schema validation, execution argument mapping.
- **Types of Systems to Investigate:** Function calling APIs, dynamic tool registries, semantic tool search routers.
- **Relevant Academic Traditions:** Information retrieval, API design patterns, semantic search.
- **Evidence Required:** Tool selection accuracy rates as tool catalog size scales from 10 to 500.
- **Maturity Dimensions to Assess:** Reliability, interoperability, autonomy.
- **Commoditization Questions:** Are base model providers expanding native tool-calling rapidly enough to risk wrapper commoditization?
- **Potential Moat Questions:** Can highly secure, curated tool wrappers with pre-built validation schemas create sticky integration value?
- **Greenfield/Brownfield Implications:** Does integration heavily require wrapping poorly documented legacy APIs into clean schemas?
- **Single/Multi-Org Implications:** Must tool execution permissions strictly mirror user RBAC and tenant authorization boundaries?
- **Dependencies:** Relies on Domain 4.2 (Skills) and Domain 5.4 (Retrieval).

#### 4.2 Skills & Capability Registries (Including Learning Lifecycles)
- **Definition:** Repositories and lifecycle engines that store, version, execute, and continually improve reusable capabilities, prompts, and operational scripts.
- **Why it matters to CAT:** Explores whether reusable skills can become persistent, empirically improving organizational assets through repeated execution, rather than remaining static scripts.
- **Key Research Questions:** What constitutes a "skill" or reusable capability in modern systems? How are skills represented, stored, discovered, invoked, composed, versioned, and deprecated? What execution data must be retained each time a skill is used? What outcome data is required to determine whether a skill performed well? How can performance changes be attributed to the skill itself rather than the model, context, or task difficulty? Can repeated execution traces produce reliable skill improvements? What prevents regression, reward hacking, or semantic drift during skill updates? Does accumulated skill execution data create a genuine learning effect or moat, or is it easily replicated by foundation models? Could foundation models internalize capabilities that currently require explicit skills, making elaborate registries unnecessary?
- **Important Primitives:**
- STATIC SKILLS (manually authored/versioned capabilities)
- ADAPTIVE SKILLS (capabilities whose parameters change based on evidence)
- SELF-PROPOSED SKILLS (systems proposing new capabilities)
- SELF-EVALUATED SKILLS (systems testing candidate changes)
- HUMAN-GATED EVOLUTION (validated changes requiring authorized promotion)
- BOUNDED AUTONOMOUS EVOLUTION (changes promoted automatically within constraints).
- **Types of Systems to Investigate:** Skill registries, internal developer portals (IDPs) adapted for AI, adaptive capability execution systems.
- **Relevant Academic Traditions:** Software component reuse, reinforcement learning, evolutionary algorithms, knowledge management.
- **Evidence Required:** Skill reuse rates, audit trail completeness, performance delta measurements across successive self-optimization generations.
- **REQUIREMENT FOR FUTURE PHASE 1 RESEARCH:** Investigate commercial systems, open-source projects, academic research, and emerging architectures implementing any portion of this capability-learning lifecycle: SKILL DEFINITION → EXECUTION → TELEMETRY → OUTCOME OBSERVATION → FEEDBACK → ATTRIBUTION → FAILURE ANALYSIS → CANDIDATE IMPROVEMENT → OFFLINE EVALUATION → VERSIONING → CANARY TESTING → APPROVAL GATE → PROMOTION → CONTINUED MONITORING.
- **Maturity Dimensions to Assess:** Maturity, portability, security, adaptability.
- **Commoditization Questions:** Do open registries and standard format repositories reduce proprietary moat potential?
- **Potential Moat Questions:** Does a dedicated experience/evaluation store containing historical execution traces, outcomes, and counterexamples form an unassailable data moat?
- **Greenfield/Brownfield Implications:** Does legacy integration demand static skills, whereas modern environments permit adaptive skills?
- **Single/Multi-Org Implications:** Can skills improve locally for one organization while contributing privacy-preserving learning to general capabilities across portfolios?
- **Dependencies:** Relies on Domain 7.1 (Observability), Domain 7.2 (Evaluation), Domain 7.3 (Self-Evaluation), and Domain 7.4 (Automated Evolution). Distinctly separate from standard Domain 5.1 (Operational Memory).

#### 4.3 Interoperability Protocols (MCP & A2A)
- **Definition:** Standardized communication protocols that enable seamless data and control exchange between disparate AI systems.
- **Why it matters to CAT:** Determines whether a platform operates as an isolated walled garden or interoperates with external enterprise ecosystems.
- **Key Research Questions:** What are the security and data leakage risks of adopting open interoperability protocols in regulated environments?
- **Important Primitives:** Standardized context schemas, JSON-RPC transport layers, protocol handshake mechanisms.
- **Types of Systems to Investigate:** Open context protocols, agent-to-agent communication standards.
- **Relevant Academic Traditions:** Network protocols, API standards bodies, distributed systems interoperability.
- **Evidence Required:** Protocol overhead latency, vulnerability exposure assessments.
- **Maturity Dimensions to Assess:** Interoperability, portability, standardization.
- **Commoditization Questions:** Are protocols rapidly becoming standardized and adopted industry-wide by hyperscalers?
- **Potential Moat Questions:** Can acting as the primary certified switchboard or registry for enterprise protocol servers capture network control points?
- **Greenfield/Brownfield Implications:** Does adoption require bridging legacy systems into standard protocol adapters?
- **Single/Multi-Org Implications:** How does cross-organization protocol communication maintain cryptographic authentication and boundary enforcement?
- **Dependencies:** Relies on Domain 4.1 (Tools) and Domain 6.1 (Identity).

### DOMAIN 5 --- STATE, MEMORY & KNOWLEDGE

#### 5.1 Organizational State & Memory Systems
- **Definition:** Architectures that manage persistent organizational state, temporal records, and contextual truth.
- **Why it matters to CAT:** Addresses how organizations represent and retain truth over extended operating horizons without assuming that "agent memory" is the correct or sole abstraction for state management.
- **Key Research Questions:** Does persistent organizational state belong primarily in systems of record, event logs, workflow state, databases, document/knowledge systems, retrieval systems, graphs, model context, specialized agent memory, or an undiscovered combination? How are contradiction resolution, temporal state, and semantic drift handled across state boundaries? How is reconciliation managed between system representation and organizational reality?
- **Important Primitives:** Systems of record, state synchronization loops, schema evolution mechanisms, conflict resolution protocols, state freshness metrics, forgetting mechanics, provenance tracking.
- **Types of Systems to Investigate:** Hybrid database architectures, log-backed memory stores, state reconciliation layers.
- **Relevant Academic Traditions:** Database systems, distributed state management, cognitive psychology, information retrieval.
- **Evidence Required:** Retrieval precision/recall benchmarks, state conflict resolution error rates, storage cost inflation rates.
- **Maturity Dimensions to Assess:** Reliability, maturity, cost efficiency.
- **Commoditization Questions:** Are memory abstraction libraries and state sync tools increasingly commoditized by cloud providers?
- **Potential Moat Questions:** Can proprietary distillation algorithms that compress organizational history into high-signal states form a durable moat?
- **Greenfield/Brownfield Implications:** Does ingestion of unstructured legacy states require fundamentally different architectures than natively structured systems?
- **Single/Multi-Org Implications:** How is absolute tenant isolation enforced across varying state storage layers?
- **Dependencies:** Relies on Domain 5.3 (Knowledge Graphs) and Domain 5.4 (Retrieval).

#### 5.2 Long-Context Architecture & Optimization
- **Definition:** Techniques utilizing models with massive context windows alongside caching and retrieval optimizations to process large payloads directly.
- **Why it matters to CAT:** Tests whether massive context windows reduce, change, or entirely eliminate the need for separate retrieval, memory, or context-engineering layers.
- **Key Research Questions:** How does distractor sensitivity, instruction interference, and conflicting evidence impact reasoning in ultra-long context? What are the limitations of multi-hop synthesis and temporal reasoning over massive documents? How are access-control and provenance preserved when injecting raw context?
- **Important Primitives:** KV-cache optimization, sliding window attention, prompt caching, chunking strategies.
- **Types of Systems to Investigate:** Ultra-long-context frontier models, optimized KV-caching proxies.
- **Relevant Academic Traditions:** Transformer architecture optimization, computer memory hierarchy design.
- **Evidence Required:** Cost-per-query comparisons between targeted retrieval and raw long-context processing, distractor sensitivity benchmarks.
- **Maturity Dimensions to Assess:** Cost, performance, reliability.
- **Commoditization Questions:** Is massive context management commoditized directly by foundational model providers?
- **Potential Moat Questions:** Does any moat rest purely on what content is selected to populate the context window rather than the processing layer itself?
- **Greenfield/Brownfield Implications:** Is long-context particularly beneficial when structural parsing of legacy documents fails?
- **Single/Multi-Org Implications:** How are tenant boundaries protected from cross-contamination when passing large multi-document payloads into shared endpoints?
- **Dependencies:** Relies on Domain 1.1 (Models) and Domain 5.1 (State).

#### 5.3 Knowledge Graphs & Ontologies
- **Definition:** Structured semantic databases that map entities, relationships, organizational hierarchies, and operational rules into interconnected graph networks.
- **Why it matters to CAT:** Forms the structural backbone of enterprise context representation (evaluating historical prior hypotheses).
- **Key Research Questions:** Who pays the computational and operational cost of continuously updating graph nodes as structures evolve? How do graph schemas handle semantic ambiguity?
- **Important Primitives:** Node-edge schemas, graph traversal queries, semantic entity resolution, ontology mapping.
- **Types of Systems to Investigate:** RDF triple stores, modern graph databases, graph-RAG architectures.
- **Relevant Academic Traditions:** Semantic web, knowledge representation, graph theory, database management.
- **Evidence Required:** Graph query latency at scale, automated schema update error rates.
- **Maturity Dimensions to Assess:** Maturity, scalability, interoperability.
- **Commoditization Questions:** While graph databases are mature, is automated ontology generation remaining a defensible capability?
- **Potential Moat Questions:** Do proprietary enterprise ontology templates tailored to specific industries offer structural advantages?
- **Greenfield/Brownfield Implications:** Does legacy transformation require automated extraction of enterprise graphs from unstructured histories?
- **Single/Multi-Org Implications:** What partitions are required to isolate multi-tenant graph traversals?
- **Dependencies:** Relies on Domain 5.1 (State) and Domain 5.4 (Retrieval).

#### 5.4 Retrieval Systems & Context Engineering
- **Definition:** Hybrid retrieval pipelines that assemble precise context payloads for system consumption.
- **Why it matters to CAT:** Directly determines the signal-to-noise ratio of information fed into execution prompts.
- **Key Research Questions:** How does hybrid search outperform pure vector similarity in complex environments? How is access-control and data provenance reliably preserved through the retrieval layer?
- **Important Primitives:** Cross-encoder re-ranking, reciprocal rank fusion, hybrid query planners, context window token budgeting.
- **Types of Systems to Investigate:** Vector databases, enterprise search indices, custom GraphRAG pipelines.
- **Relevant Academic Traditions:** Information retrieval, natural language processing, search engine optimization.
- **Evidence Required:** Precision and recall metrics on enterprise gold-standard QA datasets.
- **Maturity Dimensions to Assess:** Performance, reliability, cost efficiency.
- **Commoditization Questions:** Are managed vector databases and retrieval libraries fully commoditized infrastructure?
- **Potential Moat Questions:** Can specialized re-ranking models or domain-tuned retrieval heuristics provide competitive advantage?
- **Greenfield/Brownfield Implications:** Are highly advanced retrieval pipelines uniquely critical for navigating unstructured legacy repositories?
- **Single/Multi-Org Implications:** How are tenant-level access filters enforced strictly at the database index level?
- **Dependencies:** Relies on Domain 5.1 (State) and Domain 5.3 (Knowledge Graphs).

### DOMAIN 6 --- IDENTITY, SECURITY & GOVERNANCE

#### 6.1 Identity, Authentication & Granular Authorization
- **Definition:** Systems separating human identity, agent identity, workload/service identity, and managing authentication alongside delegated identity and authorization (RBAC, ABAC, ReBAC).
- **Why it matters to CAT:** Explicitly establishes that TECHNICAL AUTHORIZATION ≠ ORGANIZATIONAL AUTHORITY, preventing unauthorized data access or workload execution.
- **Key Research Questions:** How does the system investigate the relationship between Identity → Authentication → Delegated Credentials → Technical Authorization → Organizational Authority → Action → Provenance? How can capability-based or policy-based authorization be enforced inside a context window? What are the limitations of prior hypotheses like cryptographic edge tokens?
- **Important Primitives:** Human/Agent/Workload identities, credential delegation, non-repudiation, OAuth2/OIDC integration, dynamic RBAC/ABAC matrices, row-level security (RLS).
- **Types of Systems to Investigate:** Enterprise IAM integrations, specialized agent identity management platforms, delegated credential authorities.
- **Relevant Academic Traditions:** Computer security, cryptographic access control, identity management.
- **Evidence Required:** Security audit logs verifying zero cross-tenant or cross-clearance data leaks, non-repudiation verification rates.
- **Maturity Dimensions to Assess:** Security, reliability, regulatory exposure.
- **Commoditization Questions:** While core IAM is commoditized, is agent-specific workload identity propagation an emerging proprietary layer?
- **Potential Moat Questions:** Can identity auditing frameworks that cleanly satisfy stringent enterprise compliance reviews form a structural moat?
- **Greenfield/Brownfield Implications:** Does integration with existing Identity Providers present unique friction compared to native identity schemas?
- **Single/Multi-Org Implications:** How are federated identities managed across multiple holding company subsidiaries?
- **Dependencies:** Relies on Domain 6.2 (Policy) and Domain 10.3 (Organizational Authority).

#### 6.2 Policy, Guardrails & Governance Frameworks
- **Definition:** Rule engines and policy interceptors that evaluate actions against corporate compliance rules, safety guidelines, and legal constraints before execution.
- **Why it matters to CAT:** Ensures enterprise guardrails are enforced deterministically and securely rather than relying on probabilistic self-policing.
- **Key Research Questions:** How do systems prevent direct/indirect prompt injection, tool poisoning, malicious tool descriptions, and memory/retrieval poisoning? What are the failure modes of prompt-based guardrails versus deterministic code-level interceptors?
- **Important Primitives:** Policy decision points (PDP), policy enforcement points (PEP), deterministic guardrail interrupters, compliance rule schemas, preventive/detective controls, containment protocols.
- **Types of Systems to Investigate:** Deterministic policy interceptors, specialized AI application firewalls.
- **Relevant Academic Traditions:** Policy-based management, software verification, computer ethics and safety.
- **Evidence Required:** Guardrail bypass vulnerability rates, false-positive blockage rates on legitimate queries.
- **Maturity Dimensions to Assess:** Security, regulatory exposure, reliability.
- **Commoditization Questions:** Are AI-specific guardrail wrappers being absorbed into foundational models or open-source policy engines?
- **Potential Moat Questions:** Does maintaining comprehensive enterprise compliance policy libraries mapped to specific regulations provide a defensible wedge?
- **Greenfield/Brownfield Implications:** How easily can existing corporate Standard Operating Procedures be codified into machine-readable policies?
- **Single/Multi-Org Implications:** Must policies be hierarchically configurable per tenant and subsidiary organization?
- **Dependencies:** Relies on Domain 6.1 (Identity) and Domain 6.3 (Human Approvals).

#### 6.3 Human Approvals, Intervention & Escalation
- **Definition:** Workflows and interfaces that pause execution, present proposed actions to authorized supervisors, and capture approvals or rejections.
- **Why it matters to CAT:** Enforces accountable authority over high-consequence decisions (financial transactions, external communications, code deployments).
- **Key Research Questions:** At what failure rate or notification volume does human-in-the-loop approval degrade into notification fatigue and rubber-stamping?
- **Important Primitives:** Asynchronous approval gates, diff viewers, notification hooks, timeout-to-reject fallbacks.
- **Types of Systems to Investigate:** Human-in-the-loop workflow tools, custom approval dashboards, notification gateways.
- **Relevant Academic Traditions:** Human-computer interaction (HCI), decision support systems, organizational behavior.
- **Evidence Required:** Human response latency metrics, rubber-stamping incidence audits, task abandonment rates.
- **Maturity Dimensions to Assess:** Human oversight, reliability, maturity.
- **Commoditization Questions:** Are basic notification and approval workflows standard features in generalized automation engines?
- **Potential Moat Questions:** Do context-rich diff visualizations and risk-scoring interfaces that minimize human cognitive load create product stickiness?
- **Greenfield/Brownfield Implications:** Must intervention pipelines integrate cleanly into existing communication channels?
- **Single/Multi-Org Implications:** Does approval routing respect multi-org reporting lines and cross-boundary delegation limits?
- **Dependencies:** Relies on Domain 6.2 (Policy) and Domain 3.2 (Workflow Engines).

#### 6.4 Sandboxing, Execution Security & Secrets Management
- **Definition:** Systems managing secure execution, secrets, and supply-chain integrity to prevent exploitation.
- **Why it matters to CAT:** Defends against data exfiltration, confused-deputy problems, privilege escalation, secrets leakage, software/tool supply-chain vulnerabilities, and cross-tenant contamination.
- **Key Research Questions:** How can secrets be securely injected into execution environments without exposing raw keys to context windows? How are interoperability-server trust boundaries enforced? How is agent-generated code risk contained safely?
- **Important Primitives:** Ephemeral credential generation, vault storage, network egress filtering, memory isolation, data lineage tracking, provenance auditing.
- **Types of Systems to Investigate:** Secure credential vaults, execution sandboxes, AI supply chain security monitors.
- **Relevant Academic Traditions:** Cybersecurity, cryptographic engineering, secure systems architecture.
- **Evidence Required:** Penetration testing reports, secret leakage vulnerability assessments, cross-tenant data isolation proofs.
- **Maturity Dimensions to Assess:** Security, regulatory exposure, reliability.
- **Commoditization Questions:** Is enterprise secrets management highly commoditized, leaving only AI-specific scoping mechanisms as differentiated?
- **Potential Moat Questions:** Can specialized scoping proxies that cryptographically limit execution token utility to precise API endpoints provide a moat?
- **Greenfield/Brownfield Implications:** Does integration with legacy Key Management Systems present specific vulnerabilities?
- **Single/Multi-Org Implications:** How is absolute isolation of secret vaults guaranteed across holding company boundaries?
- **Dependencies:** Relies on Domain 2.1 (Runtimes) and Domain 6.1 (Identity).

### DOMAIN 7 --- EVALUATION, OBSERVABILITY & IMPROVEMENT

#### 7.1 Observability, Tracing & Telemetry
- **Definition:** Instrumentation tracking execution traces, token consumption, tool call sequences, and latency breakdowns.
- **Why it matters to CAT:** Essential for debugging non-deterministic failures and supplying execution trace telemetry back to skill-learning lifecycles.
- **Key Research Questions:** What is the performance overhead of comprehensive telemetry logging on high-throughput workflows? How does operational tracing interface with persistent skill evaluation data?
- **Important Primitives:** Execution DAG visualization, token cost attribution, trace replay, performance attribution logging.
- **Types of Systems to Investigate:** AI observability platforms, specialized tracing standards.
- **Relevant Academic Traditions:** Distributed tracing, software debugging, performance monitoring.
- **Evidence Required:** Trace ingestion latency, storage footprint per execution runs.
- **Maturity Dimensions to Assess:** Observability, reliability, maturity.
- **Commoditization Questions:** Is observability tooling becoming heavily commoditized via open-source telemetry standards?
- **Potential Moat Questions:** Can enterprise-grade cost attribution and compliance dashboards tailored for executive audits serve as a defensible layer?
- **Greenfield/Brownfield Implications:** Are observability requirements uniform across deployment types?
- **Single/Multi-Org Implications:** How is telemetry data rigidly segmented by tenant to prevent leakage?
- **Dependencies:** Relies on Domain 3.3 (Durable Execution) and Domain 4.2 (Skills).

#### 7.2 Evaluation & Benchmarking Frameworks
- **Definition:** Automated testing pipelines that evaluate accuracy, output quality, and regression metrics against golden datasets.
- **Why it matters to CAT:** Prevents optimization loops from degrading system performance and provides the evidence layer for evaluating candidate skill improvements.
- **Key Research Questions:** How large must evaluation datasets be to provide statistically significant confidence in automated improvements? How should successful and failed executions become training/evaluation data separately from operational state?
- **Important Primitives:** Golden test suites, LLM-as-a-judge scoring rubrics, regression pipelines, semantic similarity metrics, offline skill evaluation pipelines.
- **Types of Systems to Investigate:** Benchmarking harnesses, specialized evaluation CI/CD tools.
- **Relevant Academic Traditions:** Software testing, statistical quality control, benchmarking methodology.
- **Evidence Required:** Correlation between automated LLM-as-a-judge scores and human expert evaluations.
- **Maturity Dimensions to Assess:** Reliability, maturity, autonomy.
- **Commoditization Questions:** Are open-source evaluation libraries proliferating rapidly enough to erode commercial value?
- **Potential Moat Questions:** Do proprietary evaluation datasets and vertical-specific regression test suites constitute a durable moat?
- **Greenfield/Brownfield Implications:** Must evaluation suites be extensively customized to measure against brownfield legacy system accuracy?
- **Single/Multi-Org Implications:** Can evaluation suites securely share validation structures across organizations without violating privacy?
- **Dependencies:** Relies on Domain 7.1 (Observability) and Domain 7.3 (Self-Evaluation).

#### 7.3 System Self-Evaluation & Authority Optimization Spectrums
- **Definition:** Frameworks governing how systems analyze performance and implement changes across an escalating spectrum of autonomy.
- **Why it matters to CAT:** Replaces assumed monolithic self-improvement loops with a rigorous assessment of technical feasibility and safety across varied workflows.
- **Key Research Questions:** Which levels of autonomy are economically valuable, safe, and acceptable? How does optimization differ when performed on prompts, routing, context, tools, policies, or organizational processes? What prevents overfitting to recent executions?
- **Important Primitives:** Authority Spectrum: OBSERVE → DIAGNOSE → RECOMMEND → SIMULATE → EVALUATE → PROPOSE CHANGE → HUMAN-APPROVED CHANGE → CANARY/STAGED DEPLOYMENT → AUTOMATED ROLLBACK → BOUNDED AUTONOMOUS OPTIMIZATION → STRUCTURAL/SYSTEM MODIFICATION.
- **Types of Systems to Investigate:** Optimization engines, shadow-testing harnesses, automated feedback loop orchestrators.
- **Relevant Academic Traditions:** Reinforcement learning, evolutionary algorithms, machine learning optimization.
- **Evidence Required:** Performance delta measurements, catastrophic forgetting rates across successive generations.
- **Maturity Dimensions to Assess:** Autonomy, maturity, safety.
- **Commoditization Questions:** Are bounded optimization frameworks emerging as open-source primitives?
- **Potential Moat Questions:** Can a defensible feedback loop safely compound workflow efficiency without human intervention over time?
- **Greenfield/Brownfield Implications:** Does unconstrained autonomous optimization pose prohibitive risk in fragile legacy environments?
- **Single/Multi-Org Implications:** How are optimization modifications constrained to single-tenant data scopes?
- **Dependencies:** Relies on Domain 7.2 (Evaluation) and Domain 4.2 (Skills).

#### 7.4 Automated System Evolution & Code Generation
- **Definition:** Capabilities allowing systems to write, test, and deploy code patches, tool integrations, or structural workflow updates.
- **Why it matters to CAT:** Investigates whether organizations can dynamically adapt technical tooling without manual developer intervention.
- **Key Research Questions:** What safety boundaries are required when generating executable code? Does automated evolution transfer successfully across different organizational workflows?
- **Important Primitives:** Automated unit testing, CI/CD pipeline triggers, static code analysis, human-gated deployment.
- **Types of Systems to Investigate:** Automated software engineering agents, code patch generators.
- **Relevant Academic Traditions:** Automated software engineering, program synthesis, formal verification.
- **Evidence Required:** Introduction rate of security vulnerabilities or syntax errors in generated code.
- **Maturity Dimensions to Assess:** Autonomy, safety, security.
- **Commoditization Questions:** As AI coding assistants commoditize, is end-to-end structural evolution retaining proprietary value?
- **Potential Moat Questions:** Can verified formal correctness guarantees over generated workflows create a defensible platform?
- **Greenfield/Brownfield Implications:** Is code generation prohibitively risky in brownfield codebases lacking robust test suites?
- **Single/Multi-Org Implications:** Must generated code evolution respect isolated tenant repository boundaries?
- **Dependencies:** Relies on Domain 7.3 (Self-Evaluation) and Domain 6.2 (Policy).

### DOMAIN 8 --- INFRASTRUCTURE, RELIABILITY & DEPLOYMENT

#### 8.1 Deployment Infrastructure & VPC/On-Premise Topologies
- **Definition:** Infrastructure deployment models supporting multi-tenant cloud SaaS, single-tenant dedicated VPCs, or air-gapped installations.
- **Why it matters to CAT:** Regulated enterprises often mandate specific infrastructure postures as a strict prerequisite for adoption.
- **Key Research Questions:** What are the operational overhead and cost differentials of supporting air-gapped on-premise deployments versus multi-tenant SaaS?
- **Important Primitives:** Kubernetes operators, deployment scripts, air-gapped container registries, private model hosting.
- **Types of Systems to Investigate:** Enterprise clusters, private cloud architectures, infrastructure-as-code deployments.
- **Relevant Academic Traditions:** Cloud computing architecture, enterprise systems engineering.
- **Evidence Required:** Deployment time metrics, infrastructure maintenance overhead reports.
- **Maturity Dimensions to Assess:** Portability, security, maturity.
- **Commoditization Questions:** Are standard cloud deployment tools entirely commoditized?
- **Potential Moat Questions:** Can turnkey air-gapped deployment packages enable zero-friction enterprise compliance onboarding?
- **Greenfield/Brownfield Implications:** What deployment architectures are predominantly demanded by legacy environments versus emerging ventures?
- **Single/Multi-Org Implications:** How is infrastructure provisioned to support multi-tenant holding structures securely?
- **Dependencies:** Relies on Domain 2.1 (Runtimes) and Domain 8.3 (Cost Optimization).

#### 8.2 Reliability, Recovery & Idempotency
- **Definition:** Mechanisms ensuring actions against non-idempotent endpoints can be retried, rolled back, or recovered gracefully after failure.
- **Why it matters to CAT:** Prevents catastrophic business failure caused by erroneous duplicate execution or partial transaction timeouts.
- **Key Research Questions:** How can idempotency be guaranteed when interacting with APIs lacking native transaction support?
- **Important Primitives:** Idempotency keys, compensating transactions, automated rollback scripts, dead-letter queues.
- **Types of Systems to Investigate:** Distributed transaction managers, saga pattern orchestrators, retry wrappers.
- **Relevant Academic Traditions:** Distributed transactions, fault-tolerant computing, database recovery.
- **Evidence Required:** System recovery success rates following injected network failures.
- **Maturity Dimensions to Assess:** Reliability, recoverability, safety.
- **Commoditization Questions:** Are distributed reliability patterns established and accessible enough to negate proprietary value?
- **Potential Moat Questions:** Can domain-specific compensating transaction libraries tailored for legacy interactions provide lock-in?
- **Greenfield/Brownfield Implications:** Is complex reliability orchestration predominantly a symptom of brittle legacy environments?
- **Single/Multi-Org Implications:** Do recovery logs maintain strict tenant isolation during rollback procedures?
- **Dependencies:** Relies on Domain 3.3 (Durable Execution) and Domain 9.1 (Integration).

#### 8.3 Compute, Cost & Resource Optimization
- **Definition:** Strategies and tooling that monitor, allocate, and optimize token expenditure, compute usage, and infrastructure consumption.
- **Why it matters to CAT:** Unoptimized workflows can quickly generate runaway compute costs that destroy overall unit economics.
- **Key Research Questions:** What optimization strategies (e.g., caching, model cascading) yield the highest ROI without degrading task accuracy?
- **Important Primitives:** Usage attribution tracking, prompt caching, model tier cascading, budget throttle limits.
- **Types of Systems to Investigate:** FinOps tools, token proxy gateways, cost attribution dashboards.
- **Relevant Academic Traditions:** Financial operations (FinOps), resource management in computing.
- **Evidence Required:** Cost-per-completed-workflow metrics, resource utilization efficiency reports.
- **Maturity Dimensions to Assess:** Cost efficiency, observability, maturity.
- **Commoditization Questions:** Are token management tools proliferating rapidly enough to commoditize this layer?
- **Potential Moat Questions:** Can granular per-task cost attribution engines enable highly profitable, outcome-based pricing models?
- **Greenfield/Brownfield Implications:** Is cost optimization equally critical across all deployment environments?
- **Single/Multi-Org Implications:** How is cost accurately attributed across multi-organization portfolios?
- **Dependencies:** Relies on Domain 1.1 (Models) and Domain 7.1 (Observability).

### DOMAIN 9 --- ENTERPRISE DISCOVERY, INTEGRATION & SYSTEM INTERACTION

#### 9.1 Enterprise Integration & System Interaction
- **Definition:** Methodologies bridging computational runtimes with structural elements including APIs, event streams, databases, UI/browser interactions, legacy protocols, systems of record, and systems of control.
- **Why it matters to CAT:** Defines how a system connects to and safely interacts with an organization's existing digital environment without assuming a particular transformation strategy.
- **Key Research Questions:** How does a system robustly integrate with un-instrumented UIs, non-standard APIs, and mission-critical systems of record? Does wrapping legacy systems provide durable value?
- **Important Primitives:** API adapters, UI browser automation, database query wrappers, legacy protocol bridges, integration middleware.
- **Types of Systems to Investigate:** iPaaS platforms, enterprise service buses, browser automation agents, system discovery crawlers.
- **Relevant Academic Traditions:** Enterprise application integration (EAI), legacy system modernization.
- **Evidence Required:** Integration development time, interaction failure rates, API wrapper resilience metrics.
- **Maturity Dimensions to Assess:** Interoperability, maturity, portability.
- **Commoditization Questions:** Are specialized AI-to-legacy bridges being outpaced by the deep moats of established iPaaS incumbents?
- **Potential Moat Questions:** Can automated integration mechanisms that reverse-engineer system schemas dynamically provide a defensible wedge?
- **Greenfield/Brownfield Implications:** Does legacy interaction remain exclusively a brownfield challenge?
- **Single/Multi-Org Implications:** Must integrations strictly respect tenant-specific system credentials and data boundaries?
- **Dependencies:** Relies on Domain 4.1 (Tools) and Domain 8.2 (Reliability).

#### 9.2 Process Discovery & Process Mining
- **Definition:** Algorithmic techniques analyzing event logs, communications, and interactions to map actual operational workflows.
- **Why it matters to CAT:** Necessary to accurately map how work actually happens rather than how it is documented.
- **Key Research Questions:** How effectively can discovery algorithms extract unstructured human workflows compared to structured event logs?
- **Important Primitives:** Event log parsing, discovery algorithms, workflow bottleneck detection.
- **Types of Systems to Investigate:** Process mining engines, unstructured workflow analytics.
- **Relevant Academic Traditions:** Process mining, business process management (BPM), data mining.
- **Evidence Required:** Accuracy of discovered models compared to manual human audits.
- **Maturity Dimensions to Assess:** Maturity, observability, accuracy.
- **Commoditization Questions:** Is process discovery entirely dominated by entrenched software incumbents?
- **Potential Moat Questions:** Can AI-driven discovery that accurately maps tacit knowledge work create a new enterprise wedge?
- **Greenfield/Brownfield Implications:** Is process mining strictly utilized for legacy environments, or does it hold value for optimizing new ventures?
- **Single/Multi-Org Implications:** Must discovered process logs remain rigorously partitioned by tenant?
- **Dependencies:** Relies on Domain 5.3 (Knowledge Graphs) and Domain 9.1 (Integration).

#### 9.3 Data Ingestion, Discovery & Harmonization
- **Definition:** Pipelines that ingest, clean, categorize, and harmonize heterogeneous data sources (documents, databases) into usable semantic stores.
- **Why it matters to CAT:** Critical dependency for memory and context architectures, preventing garbage-in/garbage-out cascades.
- **Key Research Questions:** What pipelines are most efficient for cleaning and mapping heterogeneous data for ingestion?
- **Important Primitives:** Document parsers, semantic chunking algorithms, data deduplication, schema harmonization pipelines.
- **Types of Systems to Investigate:** ETL/ELT tools, document intelligence APIs, data discovery crawlers.
- **Relevant Academic Traditions:** Data engineering, information extraction, data warehousing.
- **Evidence Required:** Ingestion throughput, data quality and extraction accuracy scores.
- **Maturity Dimensions to Assess:** Maturity, reliability, performance.
- **Commoditization Questions:** Are standard data ingestion and ETL tools heavily commoditized?
- **Potential Moat Questions:** Do automated semantic harmonization pipelines tailored to complex industry verticals offer defensibility?
- **Greenfield/Brownfield Implications:** Are greenfield environments genuinely free of the data harmonization burdens that plague legacy systems?
- **Single/Multi-Org Implications:** How is tenant-level security tagging applied dynamically at the point of ingestion?
- **Dependencies:** Relies on Domain 5.1 (State) and Domain 5.4 (Retrieval).

### DOMAIN 10 --- ORGANIZATIONAL DESIGN & CAPABILITY COMPOSITION

#### 10.1 Objective Formation, Decomposition & Dynamic Composition
- **Definition:** Frameworks governing how organizational objectives are formed, KPIs selected, and goals dynamically decomposed into executable capabilities.
- **Why it matters to CAT:** Prevents optimization loops from degrading the underlying organizational purpose through reward hacking, and explores whether workflows can be dynamically assembled.
- **Key Research Questions:** What exactly is a self-optimizing organization optimizing? Who holds authority to define that objective? How do systems reconcile stakeholder preference aggregation and conflicting objectives? Can capabilities be dynamically composed to satisfy ad-hoc objectives?
- **Important Primitives:** Objective formation loops, constraints, KPIs, metric validity checks, goal decomposition trees, capability dependency graphs.
- **Types of Systems to Investigate:** Dynamic workflow generators, goal-alignment frameworks, multi-agent composition systems.
- **Relevant Academic Traditions:** Systems engineering, operations research, task network models.
- **Evidence Required:** Measurement validity scores, dynamic composition success rates versus static definitions.
- **Maturity Dimensions to Assess:** Autonomy, adaptability, complexity.
- **Commoditization Questions:** Is dynamic composition an emerging research capability safe from near-term commoditization?
- **Potential Moat Questions:** Could proprietary decomposition templates that rapidly translate business goals into operations provide competitive advantage?
- **Greenfield/Brownfield Implications:** Does legacy organizational structure severely limit dynamic composition capabilities?
- **Single/Multi-Org Implications:** Can capabilities be dynamically composed across subsidiary boundaries?
- **Dependencies:** Relies on Domain 1.2 (Reasoning) and Domain 3.1 (Multi-Agent Systems).

#### 10.2 Organizational Topology & Team Formation
- **Definition:** The structural arrangement of actors (hierarchical, matrix, flat, or ephemeral pods) designed to optimize operational throughput.
- **Why it matters to CAT:** Investigates whether static corporate hierarchies or dynamic ephemeral structures yield superior empirical performance.
- **Key Research Questions:** Do ephemeral, task-specific pods outperform static structures in complex knowledge work?
- **Important Primitives:** Pod lifecycle management, dynamic role assignment, communication topology graphs.
- **Types of Systems to Investigate:** Ephemeral organizational frameworks, simulation models.
- **Relevant Academic Traditions:** Organizational design, sociology, network theory.
- **Evidence Required:** Task completion time and error rates across varied topologies.
- **Maturity Dimensions to Assess:** Maturity, autonomy, adaptability.
- **Commoditization Questions:** Are topological structures strictly conceptual or implementable as commoditized software platforms?
- **Potential Moat Questions:** Do proprietary organizational templates optimized for specific venture types create lock-in?
- **Greenfield/Brownfield Implications:** Are novel topologies primarily restricted to new ventures lacking legacy chart constraints?
- **Single/Multi-Org Implications:** How do holding company topological structures connect subsidiary nodes efficiently?
- **Dependencies:** Relies on Domain 10.1 (Composition) and Domain 3.1 (Multi-Agent Systems).

#### 10.3 Organizational Authority, Delegation & Decision Rights
- **Definition:** Mechanisms defining who or what entity holds the decision rights, spending limits, and organizational delegation authority (distinct from technical system authorization).
- **Why it matters to CAT:** Bridges human governance to system action, enforcing explicit scope of authority.
- **Key Research Questions:** How are decision rights mathematically modeled when delegating authority from humans to autonomous systems?
- **Important Primitives:** Delegation matrices, financial spending caps, authority delegation trees, cryptographic sign-off rules.
- **Types of Systems to Investigate:** Algorithmic governance frameworks, digital signature authority engines.
- **Relevant Academic Traditions:** Corporate governance, organizational economics, agency theory.
- **Evidence Required:** Audit logs verifying strict adherence to delegation limits.
- **Maturity Dimensions to Assess:** Security, governance, compliance.
- **Commoditization Questions:** Will traditional enterprise governance software absorb dynamic delegation logic?
- **Potential Moat Questions:** Can certified algorithmic governance frameworks that satisfy corporate board risk committees form a moat?
- **Greenfield/Brownfield Implications:** Does mapping complex historical delegation rules pose unique integration challenges?
- **Single/Multi-Org Implications:** How do delegation rights flow securely across parent-subsidiary structures?
- **Dependencies:** Relies on Domain 6.1 (Identity) and Domain 6.2 (Policy).

#### 10.4 Workflow & Process Redesign
- **Definition:** Methodologies for redesigning business processes to exploit capabilities rather than digitizing inefficient legacy workflows.
- **Why it matters to CAT:** Addresses the risk of "paving the cow path" by simply automating broken processes.
- **Key Research Questions:** What redesign principles empirically maximize the leverage of AI-native platforms?
- **Important Primitives:** Process re-engineering frameworks, native workflow blueprints, friction reduction audits.
- **Types of Systems to Investigate:** AI-adapted business process re-engineering (BPR) methodologies.
- **Relevant Academic Traditions:** Operations management, business process re-engineering, industrial engineering.
- **Evidence Required:** Efficiency gains of redesigned native workflows versus automated legacy workflows.
- **Maturity Dimensions to Assess:** Maturity, adaptability, impact.
- **Commoditization Questions:** Is process redesign intrinsically a consulting-driven effort rather than a software-driven feature?
- **Potential Moat Questions:** Can proprietary workflow blueprints that radically compress operating costs serve as a durable IP advantage?
- **Greenfield/Brownfield Implications:** To what extent does redesign rely on rigorous change management in legacy environments?
- **Single/Multi-Org Implications:** Can optimized workflows be standardized across broad multi-organization portfolios?
- **Dependencies:** Relies on Domain 9.2 (Process Mining) and Domain 10.1 (Composition).

#### 10.5 Resource Allocation & Decision Science
- **Definition:** Mechanisms determining the allocation of capital, compute, human time, attention, agent capacity, budgets, and risk capacity across the organization.
- **Why it matters to CAT:** Moving beyond basic task orchestration to sophisticated resource distribution based on changing constraints.
- **Key Research Questions:** How does an organization efficiently route, schedule, and allocate scarce resources automatically? Does algorithmic capital allocation yield measurably superior ROI?
- **Important Primitives:** Optimization algorithms, scheduling engines, budgeting matrices, risk allocation limits, task routing protocols.
- **Types of Systems to Investigate:** Enterprise optimization software, algorithmic capital allocation models.
- **Relevant Academic Traditions:** Operations research, decision science, mechanism design, transaction-cost economics, information economics.
- **Evidence Required:** Resource utilization rates, reduction in idle capacity, scheduling conflict resolution accuracy.
- **Maturity Dimensions to Assess:** Complexity, efficiency, maturity.
- **Commoditization Questions:** Do existing operations research engines commoditize general resource allocation capabilities?
- **Potential Moat Questions:** Can domain-specific algorithmic allocation routines (e.g., highly optimized venture resource sharing) provide unique defensibility?
- **Greenfield/Brownfield Implications:** Does optimal resource allocation require greenfield operational freedom?
- **Single/Multi-Org Implications:** How are multi-portfolio risk budgets algorithmically balanced across separate organizations?
- **Dependencies:** Relies on Domain 10.1 (Objectives) and Domain 13.1 (Economics).

#### 10.6 Legal, Liability & Accountability Coverage
- **Definition:** Frameworks for addressing liability allocation, contractual responsibility, and regulated decision-making for system actions.
- **Why it matters to CAT:** Explores accountability distribution when autonomous or semi-autonomous workflows trigger legally significant outcomes.
- **Key Research Questions:** How is legal liability allocated for automated errors? What audit evidence is required to satisfy explainability and insurance requirements in varied jurisdictions?
- **Important Primitives:** Legally significant delegation tracking, liability transfer contracts, compliance recordkeeping, audit evidence ledgers.
- **Types of Systems to Investigate:** Regulated decision-support systems, cryptographic audit ledgers.
- **Relevant Academic Traditions:** Technology law, jurisprudence, corporate compliance theory.
- **Evidence Required:** Jurisdictional acceptance of audit logs, liability insurance underwriting criteria for automated workflows.
- **Maturity Dimensions to Assess:** Regulatory maturity, accountability, legal risk.
- **Commoditization Questions:** Will standard enterprise compliance modules expand to cover AI-specific liability attribution?
- **Potential Moat Questions:** Do specialized compliance architectures that legally shield human operators through certified auditability offer an insurmountable wedge?
- **Greenfield/Brownfield Implications:** Are legacy regulatory compliance burdens significantly heavier than emerging frameworks?
- **Single/Multi-Org Implications:** How is liability ring-fenced within subsidiary organizations to protect the parent structure?
- **Dependencies:** Relies on Domain 10.3 (Organizational Authority) and Domain 6.1 (Identity).

### DOMAIN 11 --- HUMAN-AI ORGANIZATION & ADOPTION

#### 11.1 Institutional Knowledge & Organizational Memory
- **Definition:** Systems capturing, curating, and institutionalizing tacit knowledge and operational history so they persist independently of personnel.
- **Why it matters to CAT:** Investigates how organizations maintain a persistent intellectual baseline at scale.
- **Key Research Questions:** How can tacit knowledge be captured effectively without creating overwhelming documentation burdens for human workers?
- **Important Primitives:** Automated meeting summarization, decision rationalization logs, institutional knowledge curation.
- **Types of Systems to Investigate:** AI-augmented knowledge management platforms, organizational memory stores.
- **Relevant Academic Traditions:** Organizational learning, knowledge management, sociology of knowledge.
- **Evidence Required:** Knowledge retention metrics, onboarding time reductions for new personnel.
- **Maturity Dimensions to Assess:** Maturity, reliability, utility.
- **Commoditization Questions:** Are core knowledge management tools entirely commoditized by incumbent suites?
- **Potential Moat Questions:** Can automated tacit knowledge extraction pipelines continuously compile behavior into structured, proprietary memory?
- **Greenfield/Brownfield Implications:** Does capturing institutional knowledge differ profoundly when mining legacy documentation versus capturing new operations?
- **Single/Multi-Org Implications:** How do knowledge stores support isolation while allowing selective cross-subsidiary sharing?
- **Dependencies:** Relies on Domain 5.1 (State) and Domain 5.3 (Knowledge Graphs).

#### 11.2 Human-AI Teaming & Algorithmic Management
- **Definition:** Operational models where humans and systems work collaboratively, with algorithms allocating tasks, monitoring performance, and providing feedback.
- **Why it matters to CAT:** Establishes the day-to-day empirical operating model of the organization.
- **Key Research Questions:** How do human workers respond psychologically and effectively to algorithmic management and task allocation?
- **Important Primitives:** Mixed-initiative interaction design, task hand-off protocols, transparent reasoning explanations.
- **Types of Systems to Investigate:** Collaborative workspace platforms, teaming interfaces.
- **Relevant Academic Traditions:** Human-computer interaction (HCI), organizational behavior, industrial psychology.
- **Evidence Required:** Worker adoption rates, trust indices, human satisfaction surveys.
- **Maturity Dimensions to Assess:** Human oversight, adoption, maturity.
- **Commoditization Questions:** Are collaborative interface patterns standardizing rapidly across enterprise software?
- **Potential Moat Questions:** Do proprietary interaction paradigms that demonstrably maximize trust and collaboration offer competitive leverage?
- **Greenfield/Brownfield Implications:** Does algorithmic management encounter significantly steeper cultural resistance in legacy environments?
- **Single/Multi-Org Implications:** Are interaction paradigms scalable across distributed, diverse organizational portfolios?
- **Dependencies:** Relies on Domain 6.3 (Human Approvals) and Domain 11.3 (Change Management).

#### 11.3 Change Management & Trust Building
- **Definition:** Structured methodologies for managing resistance, building trust, and guiding adoption.
- **Why it matters to CAT:** Technological capabilities are frequently bottlenecked by human friction and organizational politics.
- **Key Research Questions:** What change management frameworks are empirically effective in accelerating adoption in conservative environments?
- **Important Primitives:** Adoption tracking dashboards, trust calibration metrics, phased rollout plans.
- **Types of Systems to Investigate:** Transformation methodologies, automated adoption trackers.
- **Relevant Academic Traditions:** Organizational change management, diffusion of innovations, change psychology.
- **Evidence Required:** Employee adoption velocity, active user retention rates.
- **Maturity Dimensions to Assess:** Maturity, adoption, impact.
- **Commoditization Questions:** Is change management fundamentally a professional service resistant to software commoditization?
- **Potential Moat Questions:** Can software-embedded transformation playbooks automate and scale change management effectively?
- **Greenfield/Brownfield Implications:** What magnitude of change management is required depending on the deployment environment?
- **Single/Multi-Org Implications:** How are transformation methodologies adapted across diverse corporate cultures within a portfolio?
- **Dependencies:** Relies on Domain 11.2 (Teaming) and Domain 12.3 (Implementation).

#### 11.4 Complex Adaptive Systems & Organizational Behavior
- **Definition:** Theoretical frameworks treating organizations as networks of autonomous entities whose macro-behavior emerges from micro-interactions.
- **Why it matters to CAT:** Provides the theoretical lens to predict how organizations behave under systemic stress or rapid scaling.
- **Key Research Questions:** How do emergent systemic behaviors and unintended feedback loops manifest in highly automated environments?
- **Important Primitives:** Agent-based modeling (ABM), emergent behavior analysis, resilience stress-testing.
- **Types of Systems to Investigate:** Enterprise simulation engines, macro-organizational models.
- **Relevant Academic Traditions:** Complex adaptive systems theory, cybernetics, organizational sociology.
- **Evidence Required:** Simulation accuracy in predicting bottlenecks and failure modes.
- **Maturity Dimensions to Assess:** Maturity, theoretical rigor, predictability.
- **Commoditization Questions:** Does theoretical rigor provide any direct software commoditization risk?
- **Potential Moat Questions:** Could proprietary simulation engines used to stress-test structures before deployment create a novel service moat?
- **Greenfield/Brownfield Implications:** Can adaptive frameworks accurately model both legacy refactoring and new venture dynamics?
- **Single/Multi-Org Implications:** Are emergent behaviors uniquely volatile within interconnected holding company portfolios?
- **Dependencies:** Relies on Domain 3.1 (Multi-Agent Systems) and Domain 10.2 (Topology).

### DOMAIN 12 --- CUSTOMER JOBS-TO-BE-DONE & ADOPTION

#### 12.1 Stakeholder & Beneficiary Segmentation
- **Definition:** Analysis distinguishing among the economic buyer, executive sponsor, technical buyer, compliance approver, daily user, potentially displaced stakeholder, and beneficiary.
- **Why it matters to CAT:** Ensures product go-to-market strategies do not incorrectly preselect buyer personas or misalign incentives.
- **Key Research Questions:** How do purchasing and adoption dynamics shift across differing stakeholder combinations and incentive structures?
- **Important Primitives:** Stakeholder mapping matrices, value proposition alignment frameworks, persona requirement specs.
- **Types of Systems to Investigate:** B2B enterprise sales architectures, customer discovery frameworks.
- **Relevant Academic Traditions:** Product management theory, B2B marketing, consumer behavior.
- **Evidence Required:** Sales conversion rates, win/loss analysis reports across varying personas.
- **Maturity Dimensions to Assess:** Market readiness, commercial maturity.
- **Commoditization Questions:** Are standard go-to-market methodologies sufficient, or are new frameworks required?
- **Potential Moat Questions:** Does a deep mastery of specific, unaddressed stakeholder pain points provide a defensible wedge?
- **Greenfield/Brownfield Implications:** Does target stakeholder profile fundamentally dictate greenfield versus brownfield strategy?
- **Single/Multi-Org Implications:** How do executive dashboards serve holding-level buyers across multiple organizations?
- **Dependencies:** Relies on Domain 12.2 (Jobs-to-Be-Done) and Domain 13.2 (Pricing).

#### 12.2 Customer Jobs-to-Be-Done (Value Discovery)
- **Definition:** Identifying the functional, emotional, and social progress customers seek, including cost reduction, labor substitution/augmentation, revenue generation, quality improvement, speed, compliance, and time-to-market.
- **Why it matters to CAT:** Prevents building technologically impressive features that fail to solve urgent, validated problems.
- **Key Research Questions:** Which specific jobs yield the highest net economic surplus when optimized? What value propositions trigger the fastest adoption cycles?
- **Important Primitives:** JTBD interview frameworks, pain-point prioritization matrices, bottleneck identification.
- **Types of Systems to Investigate:** Customer discovery transcripts, workflow failure logs.
- **Relevant Academic Traditions:** JTBD theory, product design methodology.
- **Evidence Required:** Willingness-to-pay validation metrics, frequency of target job execution.
- **Maturity Dimensions to Assess:** Market validation, commercial fit.
- **Commoditization Questions:** Can deep JTBD research offer competitive advantage beyond commoditized features?
- **Potential Moat Questions:** Can identifying an unserved, high-value enterprise wedge ignored by incumbents anchor a lasting moat?
- **Greenfield/Brownfield Implications:** Do target jobs pivot dramatically based on the legacy state of the customer?
- **Single/Multi-Org Implications:** Do multi-org jobs uniquely prioritize portfolio coordination and capital allocation?
- **Dependencies:** Relies on Domain 12.1 (Segmentation) and Domain 9.2 (Process Discovery).

#### 12.3 Implementation, Onboarding & Deployment Methodologies
- **Definition:** The methodologies, services, and playbooks required to deploy and configure platforms successfully.
- **Why it matters to CAT:** Investigates whether commercial scaling relies on software mechanics or high-touch professional services.
- **Key Research Questions:** Can enterprise deployment be fully productized, or do complex integrations permanently mandate high-touch professional services?
- **Important Primitives:** Implementation playbooks, automated onboarding wizards, milestone trackers.
- **Types of Systems to Investigate:** Professional-services-enabled software models, customer success architectures.
- **Relevant Academic Traditions:** Enterprise software delivery, service-dominant logic.
- **Evidence Required:** Time-to-value (TTV) metrics, professional services gross margin reports.
- **Maturity Dimensions to Assess:** Commercial scalability, operational maturity.
- **Commoditization Questions:** Are deployment frameworks distinct enough to avoid commoditization?
- **Potential Moat Questions:** Do proprietary onboarding automation assets that radically compress time-to-value form a barrier to entry?
- **Greenfield/Brownfield Implications:** Does legacy transformation inherently necessitate more extensive implementation services?
- **Single/Multi-Org Implications:** Must multi-org rollouts follow structured, sequential holding-company sequencing?
- **Dependencies:** Relies on Domain 11.3 (Change Management) and Domain 13.3 (SaaS vs. Services).

### DOMAIN 13 --- ECONOMICS & BUSINESS MODELS

#### 13.1 AI-Native Organizational Economics & Value Creation
- **Definition:** Economic frameworks evaluating net economic surplus relative to available alternatives across dimensions including throughput, quality, revenue uplift, error reduction, coordination costs, transaction costs, and working-capital effects.
- **Why it matters to CAT:** Establishes the governing framework for assessing fundamental economic viability and value capture potential.
- **Key Research Questions:** Under what specific conditions does an AI-enabled organizational system create net economic surplus relative to available alternatives, and who captures that surplus? How does token-to-human labor economics factor into overall net surplus?
- **Important Primitives:** Cost-per-task models, human equivalency metrics, transaction cost models, fixed/variable cost structures.
- **Types of Systems to Investigate:** Economic valuation models, automation unit economics calculators.
- **Relevant Academic Traditions:** Labor economics, engineering economics, cost-benefit analysis.
- **Evidence Required:** Empirical surplus comparisons between human baselines, deterministic software, and advanced systems.
- **Maturity Dimensions to Assess:** Economic viability, scalability.
- **Commoditization Questions:** Does continuously deflating compute cost fundamentally alter margin capture over time?
- **Potential Moat Questions:** Can structurally superior workflow efficiencies protect margins against underlying hardware deflation?
- **Greenfield/Brownfield Implications:** How do legacy headcount and software costs influence the baseline calculations of economic surplus?
- **Single/Multi-Org Implications:** Do economics compound favorably when optimized routines are applied across broad portfolios?
- **Dependencies:** Relies on Domain 8.3 (Cost Optimization) and Domain 13.2 (Pricing).

#### 13.2 Pricing, Value Metrics & Unit Economics
- **Definition:** Models determining how a platform captures value (e.g., consumption, outcome-based, SaaS, revenue share).
- **Why it matters to CAT:** Evaluates whether traditional pricing paradigms remain viable or require structural innovation.
- **Key Research Questions:** Do outcome-based or consumption-based pricing models provide superior alignment and predictability compared to traditional SaaS seats?
- **Important Primitives:** Value metric definitions, consumption tier meters, margin-per-workflow metrics.
- **Types of Systems to Investigate:** Usage-based billing engines, outcome pricing frameworks.
- **Relevant Academic Traditions:** Pricing strategy, microeconomics, software pricing models.
- **Evidence Required:** Customer acceptance rates for novel pricing structures, net revenue retention benchmarks.
- **Maturity Dimensions to Assess:** Commercial maturity, financial viability.
- **Commoditization Questions:** Does standard billing infrastructure commoditize, shifting differentiation entirely to metric design?
- **Potential Moat Questions:** Can value metrics tied directly to validated business outcomes generate unassailable pricing power?
- **Greenfield/Brownfield Implications:** Are certain customer profiles or deployment environments fundamentally averse to specific pricing models?
- **Single/Multi-Org Implications:** What billing infrastructure is required for hierarchical cost allocation across holding entities?
- **Dependencies:** Relies on Domain 13.1 (Economics) and Domain 13.3 (SaaS vs. Services).

#### 13.3 SaaS vs. Services Business Models
- **Definition:** The strategic tension between maintaining scalable software versus capturing transformation revenue via professional services.
- **Why it matters to CAT:** Dictates operational complexity, capital requirements, and eventual valuation profiles.
- **Key Research Questions:** Is a hybrid "services-enabled software" model empirically mandatory during early market formation, or can products scale purely as SaaS?
- **Important Primitives:** Gross margin analysis, revenue mix ratios, headcount scaling curves.
- **Types of Systems to Investigate:** Tech-enabled services companies, vertical SaaS models.
- **Relevant Academic Traditions:** Business strategy, corporate finance, venture capital economics.
- **Evidence Required:** Historical financial models of software vs. services margins in emerging technology categories.
- **Maturity Dimensions to Assess:** Financial scalability, operational maturity.
- **Commoditization Questions:** Do heavy customization requirements permanently suppress software margin potential?
- **Potential Moat Questions:** Can architectures that progressively productize professional services into self-serve modules form a structural advantage?
- **Greenfield/Brownfield Implications:** Does complex environment integration permanently tie product viability to services capability?
- **Single/Multi-Org Implications:** Do multi-org models inherently blend platform software with operational holding-company services?
- **Dependencies:** Relies on Domain 12.3 (Implementation) and Domain 13.2 (Pricing).

### DOMAIN 14 --- STRATEGY, CONTROL POINTS & MOATS

#### 14.1 Platform Control Points & Ecosystem Leverage
- **Definition:** Strategic positions within the technology stack that dictate ecosystem leverage and pricing power.
- **Why it matters to CAT:** Identifies where independent products can capture sustainable economic value without being absorbed.
- **Key Research Questions:** Which emerging layers represent highly defensible, durable control points versus transient wrappers? Does an independent control point exist at all?
- **Important Primitives:** Ecosystem lock-in mechanisms, developer platform APIs, proprietary integrations.
- **Types of Systems to Investigate:** Ecosystem architectures, historical enterprise platform control points.
- **Relevant Academic Traditions:** Competitive strategy, platform economics, value chain analysis.
- **Evidence Required:** Partner dependency metrics, platform switching cost analyses.
- **Maturity Dimensions to Assess:** Strategic defensibility, market maturity.
- **Commoditization Questions:** Are hyperscalers and model providers successfully colonizing upper orchestration layers?
- **Potential Moat Questions:** Does establishing the primary enterprise cross-system integration hub create a definitive control point?
- **Greenfield/Brownfield Implications:** Must platforms displace entrenched legacy control points to gain leverage?
- **Single/Multi-Org Implications:** Are there unique control points available exclusively at the multi-organization holding layer?
- **Dependencies:** Relies on Domain 14.2 (Moats) and Domain 14.3 (Competitor Response).

#### 14.2 Moat Mechanisms & Data Network Effects
- **Definition:** Structural barriers to entry (e.g., learning effects, workflows, switching costs) that protect the business.
- **Why it matters to CAT:** Evaluates long-term durability against copycats and capitalized incumbents.
- **Key Research Questions:** Do cross-company data network effects genuinely compound without violating privacy boundaries?
- **Important Primitives:** Data exhaust loops, federated learning feedback, switching cost barriers.
- **Types of Systems to Investigate:** Network effect business models, software defensibility frameworks.
- **Relevant Academic Traditions:** Strategic management, network economics.
- **Evidence Required:** Churn rate benchmarks, customer retention curves, data flywheel velocity.
- **Maturity Dimensions to Assess:** Defensibility, maturity.
- **Commoditization Questions:** Are standard features easily replicated, requiring deep integration or proprietary data for defensibility?
- **Potential Moat Questions:** Does accumulated evaluation/learning data that empirically improves capabilities offer the strongest defensible moat?
- **Greenfield/Brownfield Implications:** Do defensibility strategies differ profoundly between entrenched legacy entanglements and new ecosystem network effects?
- **Single/Multi-Org Implications:** Can portfolios generate internal network effects by sharing validated capabilities across subsidiaries?
- **Dependencies:** Relies on Domain 14.1 (Control Points) and Domain 14.3 (Competitor Response).

#### 14.3 Competitive Dynamics & Incumbent/Hyperscaler Response
- **Definition:** Strategic analysis of how legacy software giants and hyperscalers will respond to emerging architectures.
- **Why it matters to CAT:** Prevents building wedges that are easily neutralized by native incumbent feature releases.
- **Key Research Questions:** How do incumbents typically absorb or neutralize startup wedges in enterprise automation?
- **Important Primitives:** Feature parity tracking, ecosystem bundling analyses, acquisition target criteria.
- **Types of Systems to Investigate:** Incumbent AI roadmaps, hyperscaler feature architectures.
- **Relevant Academic Traditions:** Disruption theory, competitive dynamics, strategic management.
- **Evidence Required:** Incumbent release velocity, enterprise customer multi-vendor tolerance data.
- **Maturity Dimensions to Assess:** Competitive landscape maturity.
- **Commoditization Questions:** If hyperscalers commoditize core foundations, where do independent platforms wedge successfully?
- **Potential Moat Questions:** Can superior agility and deep vertical mastery preempt incumbent absorption?
- **Greenfield/Brownfield Implications:** Is the brownfield space fundamentally more contested by incumbents than greenfield creation?
- **Single/Multi-Org Implications:** Do complex holding structures operate outside typical single-enterprise competitive vectors?
- **Dependencies:** Relies on Domain 14.1 (Control Points) and Domain 12.2 (Jobs-to-Be-Done).

### DOMAIN 15 --- LIFECYCLE, DEPLOYMENT MODES & SCALING

#### 15.1 Greenfield Creation vs. Brownfield Transformation Contexts
- **Definition:** Comparative evaluation of deploying architectures for brand-new operations versus transforming existing operations.
- **Why it matters to CAT:** Evaluates environment-specific architectural complexity, go-to-market strategies, and acceleration velocity.
- **Key Research Questions:** What are the fundamental differences in product architecture required to support zero-legacy setups versus complex legacy transformations? Are certain architectures strictly limited to one environment?
- **Important Primitives:** Venture bootstrapping templates, legacy migration frameworks, dual-track operational models.
- **Types of Systems to Investigate:** Venture studios, transformation playbooks, startup accelerators.
- **Relevant Academic Traditions:** Entrepreneurship theory, organizational transformation, corporate venturing.
- **Evidence Required:** Time-to-market and capital efficiency comparisons across varying environmental deployments.
- **Maturity Dimensions to Assess:** Operational maturity, scalability.
- **Commoditization Questions:** Does transformation methodology remain a highly variable, un-commoditized consulting capability?
- **Potential Moat Questions:** Could a unified platform capable of seamless operation across both environments offer unique scale advantages?
- **Greenfield/Brownfield Implications:** Treats environment as an empirical dimension to test rather than assuming specific methodologies or customer profiles.
- **Single/Multi-Org Implications:** Are greenfield or brownfield ventures inherently predisposed toward specific organizational topologies?
- **Dependencies:** Relies on Domain 9.1 (Integration) and Domain 12.2 (Jobs-to-Be-Done).

#### 15.2 Single-Organization vs. Multi-Organization/Portfolio Systems
- **Definition:** Architectural requirements for managing a single operating entity versus a portfolio of multiple interconnected subsidiaries.
- **Why it matters to CAT:** Tests whether complex multi-organization coordination represents a viable architecture or an unnecessary, burdensome complication.
- **Key Research Questions:** What exact architectural overhead is introduced by scaling from single-tenant systems to multi-tenant, interconnected portfolios?
- **Important Primitives:** Multi-tenant isolation, parent-level routing frameworks, cross-company sharing schemas.
- **Types of Systems to Investigate:** Venture studio operating software, multi-subsidiary governance architectures.
- **Relevant Academic Traditions:** Holding company economics, conglomerate strategy, multi-tenant architecture.
- **Evidence Required:** Cross-subsidiary coordination overhead metrics, multi-tenant security audit proofs.
- **Maturity Dimensions to Assess:** Scalability, architectural maturity, security.
- **Commoditization Questions:** While standard multi-tenancy is commoditized, are holding-company management layers remaining nascent?
- **Potential Moat Questions:** Do proprietary coordination and resource-sharing protocols designed for interconnected portfolios create sticky network effects?
- **Greenfield/Brownfield Implications:** Does portfolio coordination architecture differ depending on the legacy status of the subsidiaries?
- **Single/Multi-Org Implications:** Defines the structural boundary requirements for investigation.
- **Dependencies:** Relies on Domain 6.1 (Identity) and Domain 10.2 (Topology).

### DOMAIN 16 --- NON-AGENT ALTERNATIVES & BASELINES

#### 16.1 Deterministic Software, BPM & Workflow Automation
- **Definition:** Traditional rule-based software, Business Process Management (BPM) suites, and deterministic workflow engines.
- **Why it matters to CAT:** Serves as the primary baseline to prove whether probabilistic systems deliver genuinely superior ROI, or if determinism dominates.
- **Key Research Questions:** For what percentage of workflows do deterministic engines consistently outperform probabilistic systems in reliability, cost, and efficiency?
- **Important Primitives:** Conditional logic branches, rigid process flowcharts, rule engines.
- **Types of Systems to Investigate:** Traditional workflow automation suites, enterprise BPM software.
- **Relevant Academic Traditions:** Business process management, automata theory, software engineering.
- **Evidence Required:** Maintenance overhead, cost, latency, and error rate comparisons.
- **Maturity Dimensions to Assess:** Reliability, maturity, determinism, portability.
- **Commoditization Questions:** Are deterministic platforms overly commoditized, or do they still capture significant value?
- **Potential Moat Questions:** Under what conditions does a deeply embedded deterministic engine provide a more defensible moat than a modern probabilistic system?
- **Greenfield/Brownfield Implications:** Is deterministic software predominantly favored in entrenched legacy environments over agile ventures?
- **Single/Multi-Org Implications:** How does deterministic software scale across multi-tenant architectures?
- **Dependencies:** Relies on Domain 3.2 (Workflow Engines).

#### 16.2 RPA, iPaaS & ERP/CRM-Native Automation
- **Definition:** Robotic Process Automation, Integration Platform as a Service, and native enterprise suite automation.
- **Why it matters to CAT:** Represents the status-quo automation tooling organizations utilize before exploring advanced paradigms.
- **Key Research Questions:** Under what exact conditions do RPA bots and iPaaS pipelines fail when handling unstructured data or dynamic tasks compared to adaptive systems?
- **Important Primitives:** UI click bots, webhook pipelines, point-to-point connectors, native forms.
- **Types of Systems to Investigate:** Incumbent RPA vendors, iPaaS suites, native CRM/ERP automations.
- **Relevant Academic Traditions:** Systems integration, enterprise software engineering.
- **Evidence Required:** Maintenance break-fix frequency comparisons when underlying UIs/APIs change.
- **Maturity Dimensions to Assess:** Maturity, reliability, enterprise adoption, interoperability.
- **Commoditization Questions:** How rapidly are incumbent platforms absorbing AI capabilities to prevent commoditization of their pipelines?
- **Potential Moat Questions:** Does deep integration into proprietary UI ecosystems offer incumbents unassailable defensibility?
- **Greenfield/Brownfield Implications:** Do modern environments bypass these tools entirely in favor of API-first architectures?
- **Single/Multi-Org Implications:** How do point-to-point connectors scale across holding company networks?
- **Dependencies:** Relies on Domain 9.1 (Integration).

#### 16.3 Enterprise Search, Knowledge Management & Data Platforms
- **Definition:** Search engines, document systems, and data lakes managing information without generative synthesis.
- **Why it matters to CAT:** Provides the fundamental comparative baseline for evaluating advanced memory and retrieval architectures.
- **Key Research Questions:** For which specific queries do traditional retrieval systems outperform or match the cost-efficiency of advanced GraphRAG or semantic pipelines?
- **Important Primitives:** Keyword indexing, hierarchical folder structures, document tagging, SQL data warehouses.
- **Types of Systems to Investigate:** Traditional enterprise search appliances, document management suites.
- **Relevant Academic Traditions:** Information retrieval, library science, database management.
- **Evidence Required:** User search success rates and time-to-find metrics across varied systems.
- **Maturity Dimensions to Assess:** Maturity, reliability, security, cost.
- **Commoditization Questions:** Is traditional enterprise search too commoditized to present meaningful competition?
- **Potential Moat Questions:** Does owning the underlying data lake provide a stronger moat than the generative synthesis layer applied above it?
- **Greenfield/Brownfield Implications:** Are traditional structured indices more reliable in highly regulated legacy environments?
- **Single/Multi-Org Implications:** How are traditional indices segmented effectively across portfolio companies?
- **Dependencies:** Relies on Domain 5.4 (Retrieval).

#### 16.4 Human-Operated Processes & Managed Services Baselines
- **Definition:** The status-quo baseline where tasks are executed entirely by human personnel or outsourced professional services.
- **Why it matters to CAT:** The ultimate economic benchmark required to prove systemic capability and value creation.
- **Key Research Questions:** What is the exact fully-loaded cost, throughput, and error rate of human-operated baselines across target enterprise workflows compared to automated equivalents?
- **Important Primitives:** Headcount rosters, SLAs, manual quality assurance reviews.
- **Types of Systems to Investigate:** Business process outsourcing (BPO) firms, professional services, internal teams.
- **Relevant Academic Traditions:** Operations management, labor economics, organizational behavior.
- **Evidence Required:** Comprehensive baseline cost-per-output metrics and latency figures.
- **Maturity Dimensions to Assess:** Human adaptability, operational maturity, scalability.
- **Commoditization Questions:** Is offshore human labor sufficiently commoditized to set a rigid price ceiling on software alternatives?
- **Potential Moat Questions:** Under what conditions do premium managed human services maintain a moat against automated solutions?
- **Greenfield/Brownfield Implications:** Are legacy organizations fundamentally more dependent on human baseline operations?
- **Single/Multi-Org Implications:** How do human labor pools scale dynamically across varied organizational subsidiaries?
- **Dependencies:** Relies on Domain 13.1 (Economics).

---

## IV. Cross-Cutting & Strategic Matrices

### A. Cross-Cutting Evaluation Dimensions
- **Reliability:** The statistical consistency of task completion without unhandled failures or silent errors.
- **Security:** Resistance to prompt injection, unauthorized data exfiltration, privilege escalation, and supply-chain vulnerabilities.
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
| **Greenfield Creation** | **Quadrant I:** What architectures effectively support the creation and operation of a single new organization? | **Quadrant II:** What architectures efficiently support the creation and operation of multiple new interconnected organizations? |
| **Brownfield Transformation** | **Quadrant III:** What technical and integration mechanisms are required to transform or augment one existing legacy organization? | **Quadrant IV:** What frameworks are required to transform and coordinate multiple existing legacy organizations simultaneously? |

### C. Candidate Control-Point Research Map

```text
+-----------------------------------------------------------------------------------+
| EMERGING AI ORGANIZATIONAL STACK CANDIDATE CONTROL POINTS |
| (Note: None is presumed to be a durable control point prior to research discovery) |
+-----------------------------------------------------------------------------------+
| Candidate Locations to Investigate: |
| - Model/Inference Layer |
| - Agent Runtime / Durable Execution |
| - Tool / Capability Registry |
| - Interoperability / Enterprise Integration Gateway |
| - Identity / Authorization / Governance Policy |
| - Organizational State / Context / Knowledge Representation |
| - Evaluation / Optimization / Capability Composition |
| - Organizational Authority / Resource Allocation |
| - Business Outcome / Economic Value Layer |
+-----------------------------------------------------------------------------------+
| Evidence Required for Assessment: |
| Customer dependence, technical indispensability, switching costs, ecosystem leverage, |
| proprietary data/learning effects, trust boundaries, portability, provider risk. |
+-----------------------------------------------------------------------------------+

### D. Non-Agent Baseline Map

-   **Deterministic Workflows:** Tested against probabilistic adaptation and failure rates.

-   **RPA & iPaaS:** Tested against brittle UI/API fragility versus dynamic adaptation.

-   **Enterprise Search & Knowledge Bases:** Tested against context synthesis and multi-tier memory.

-   **Human-Operated BPO Baselines:** Tested against total cost-per-task economics and latency.

### E. Academic / Research Traditions Map

-   **Computer Science & Distributed Systems:** Actor-model concurrency, formal state verification, cryptography.

-   **Artificial Intelligence & Cognitive Science:** Multi-agent systems, automated planning, reinforcement learning.

-   **Organizational Science & Economics:** Transaction cost economics, complex adaptive systems, decision science, agency theory.

-   **Human-Computer Interaction (HCI):** Algorithmic management, collaborative mixed-initiative workspaces, trust calibration.

### F. Build / Buy / Partner / Integrate Decision-Object Map

For major capabilities across all 16 Domains, Phase 1 research must gather evidence to determine if a platform should:

-   **Build:** Construct proprietary capability.

-   **Buy / License:** Procure commercial vendor solutions.

-   **Adopt Open Source:** Utilize community-maintained primitives.

-   **Partner / Integrate:** Establish ecosystem alliances.

-   **Defer / Omit:** Deprioritize capability entirely.

*Dimensions to Assess for Decision Routing:* Strategic differentiation, maturity, reliability, security, portability, vendor lock-in, cost, implementation burden, ecosystem adoption, compliance readiness, ability to customize, switching costs, and roadmap dependence.

## V. Final Coverage Stress Test

**KNOWN INCOMPLETENESS PRINCIPLE:** This taxonomy is a starting ontology, not a closed universe. Phase 1 research must maintain an **EMERGENT CATEGORIES REGISTER** containing newly discovered technical paradigms, primitives, academic traditions, customer problems, economic mechanisms, competitors, control points, or failure modes that do not fit the existing structure. Important out-of-taxonomy discoveries must trigger the amendment of this taxonomy rather than being forced improperly into an existing category.

-   **Can this taxonomy discover that agents are NOT the correct abstraction?** Yes. Domain 16 explicitly evaluates non-agent alternatives symmetrically, allowing the discovery that deterministic or services-heavy models dominate.

-   **Can it discover that CAT should NOT exist?** Yes. Domain 13 and Domain 14 objectively investigate economic surplus and moat defensibility without assuming viability.

-   **Does it preserve neutrality?** Yes. Assumptions regarding architectures, historical artifacts, control points, business models, and environments have been uniformly converted into empirical research questions.
