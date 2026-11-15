Prepared for Cole Masterson \| 18 August 2026

| **FINAL RECOMMENDATION** Use the first playbook as the structural backbone, import the second playbook’s stronger canonical-file discipline and first vertical slice, and correct both by separating desk research from real customer validation, reducing context duplication, and generating final artifacts one at a time rather than in one oversized synthesis response. |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

This document is the operating manual. Do not upload both prior playbooks into the new Project. They contain overlapping instructions and would create avoidable context competition. Instead, use the compact instruction set and artifact package below.

# 1. Executive decision

Both drafts are strong and more similar than different. The optimal plan is a controlled research program, not a better single mega-prompt. The first document is more complete and implementation-oriented; the second is more disciplined about canonical replacements, assurance, and the initial proving workflow.

| **Area**               | **Playbook 1**                                           | **Playbook 3**                                                               | **Final choice**                                    |
|------------------------|----------------------------------------------------------|------------------------------------------------------------------------------|-----------------------------------------------------|
| Research decomposition | Best: eight explicit phases and strong build artifacts   | Good: seven broader phases                                                   | Use eight phases, but add a customer-evidence gate  |
| Canonical state        | Good file structure and source ledger                    | Best: replacement files, four audits, stable IDs                             | Use Playbook 3 discipline                           |
| Architecture rigor     | Best: explicit contracts, events, ADRs, failure/recovery | Strong but slightly more consolidated                                        | Use Playbook 1                                      |
| Final synthesis        | Too many files requested in one response                 | One master report then handoff                                               | Generate an index, then one artifact per fresh chat |
| First slice            | Generic trusted intent-to-action loop                    | Specific research-to-decision slice aligned with your diligence/QC strengths | Use research-to-decision as Slice 0                 |
| Customer proof         | Mostly desk research and hypotheses                      | Better buyer challenge, still not real interviews                            | Add external validation before architecture lock    |

| **The key distinction** Claude can research, structure hypotheses, and produce a high-quality plan. It cannot create genuine customer evidence from desk research. Interview findings, design-partner commitments, workflow baselines, and willingness-to-pay must remain labeled as unvalidated until you supply real evidence. |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## What changes versus both drafts

- Keep the Project Instructions short enough to remain stable. Put operating detail in phase prompts and canonical files.

- Do not upload the two source playbooks after setup. Upload only the final starter pack and approved artifacts.

- Use Phase 2A for desk-based customer hypotheses, then Phase 2B for founder-provided interview evidence. Do not “approve” the wedge before this gate.

- Do not ask one final chat to emit nine large artifacts. Have one integration chat produce a conflict-resolution memo and artifact index, then use separate chats to generate each final file.

- Freeze architecture only after product-wedge approval. Prototype architecture choices with spikes before selecting irreversible infrastructure.

- Keep the personal second brain outside the initial product boundary and outside company tenancy. Treat it as a later, separately authorized integration.

- Use a low-risk research-to-decision workflow as the first proving slice, then graduate to bounded actions only after evaluation and control gates pass.

# 2. Exact operating sequence

| **Step** | **Action**                        | **Completion evidence**                                                                                                                                               |
|----------|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1        | Prepare locally                   | Create the starter files in Section 4. Keep the prior Word documents outside Project Knowledge as reference only.                                                     |
| 2        | Create one fresh private Project  | Name it “CAT \| Company Automation Tool”. Select the strongest research-capable model available in your account and enable web research during evidence-heavy phases. |
| 3        | Install stable instructions       | Paste the Project Instructions from Section 3 once. Do not paste phase prompts into Project Instructions.                                                             |
| 4        | Load minimal knowledge            | Upload only the starter canonical files. Add the founder brief and constraints. Do not load unrelated notes or employer/proprietary materials.                        |
| 5        | Run Phase 0                       | Use a fresh chat. Claude returns the program plan and replacement canonical files, not market conclusions.                                                            |
| 6        | Run each phase in a new chat      | At the start, tell Claude which artifact versions are Approved. At the end, download outputs and replace changed canonical files.                                     |
| 7        | Apply the gate yourself           | Mark each output Approved, Approved with Conditions, or Rejected. Claude recommends; you decide.                                                                      |
| 8        | Introduce real customer evidence  | After desk hypotheses, run interviews or design-partner conversations. Upload anonymized notes and ask Claude to update the evidence ledger.                          |
| 9        | Red-team at decision points       | Run adversarial chats after product thesis, architecture, and integrated blueprint. Resolve defects before continuing.                                                |
| 10       | Synthesize in two passes          | First resolve conflicts and freeze vocabulary. Then generate final artifacts one per chat from the approved index.                                                    |
| 11       | Move approved files to Git        | The repository, not Claude Project, becomes the implementation system of record.                                                                                      |
| 12       | Start Claude Code in plan mode    | Require a vertical-slice plan, ADRs, tests, and verification commands before code.                                                                                    |
| 13       | Implement one slice per branch/PR | Update requirements, tests, evals, telemetry, and traceability with every behavioral change.                                                                          |

# 3. Project Instructions to paste once

### Paste into Project Instructions

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>You are the principal research partner, product strategist, enterprise architect, venture designer, and rigorous skeptic for CAT, a proposed Company Automation Tool and governed company execution system.</p>
<p>Your objective is to discover the strongest evidence-supported product, business, and technical design. Do not validate the founder's initial hierarchy by default. Treat executive agents, swarms, graphs, ontologies, an Alphabet layer, and a personal second brain as hypotheses to compare against simpler alternatives.</p>
<p>OPERATING RULES</p>
<p>1. Separate verified fact, sourced claim, inference, estimate, assumption, founder choice, design judgment, and unresolved question. Label them.</p>
<p>2. For current products, standards, versions, pricing, capabilities, incidents, market data, and legal or regulatory claims, use current sources. Prefer primary sources and record publisher, title, date, URL, access date, source class, and exact proposition supported.</p>
<p>3. Never fabricate facts, citations, customers, interviews, benchmarks, market sizes, vendor capabilities, or precision. Desk research is not customer validation.</p>
<p>4. Optimize for a small founding team and a narrow, valuable wedge. Distinguish first slice, MVP, platform foundation, expansion, and long-term north star.</p>
<p>5. Prefer deterministic software for permissions, policy, accounting, state transitions, approvals, budgets, record updates, and irreversible actions. Use models only where ambiguity or adaptive reasoning creates testable value.</p>
<p>6. Every consequential action must have identity, authorization, least privilege, policy, budget, provenance, durable state, idempotency where applicable, observability, approval or escalation, and recovery.</p>
<p>7. Compare the minimum single-agent plus deterministic-workflow baseline against every multi-agent design. Justify each agent, service, state store, memory write, and autonomous loop.</p>
<p>8. Keep personal, parent/portfolio, and operating-company data and authority separated. No implicit cross-boundary memory or action.</p>
<p>9. Treat memory as typed systems: authoritative records, documents, retrieval indexes, working state, episodic traces, preferences, decisions, and evaluated policies. Define ownership, provenance, retention, deletion, review, and rollback.</p>
<p>10. Do not recommend uncontrolled self-modification. Improvement follows observe, propose, simulate, evaluate, approve, canary, monitor, rollback, and record.</p>
<p>11. Maintain stable IDs and canonical artifacts: HYP, EVD, DEC, RSK, FR, NFR, ADR, API, EVT, EVAL, and KPI.</p>
<p>12. Do not silently overwrite decisions. Supersede them with new evidence, rationale, and reversal triggers.</p>
<p>13. Begin each phase with objective, decision enabled, scope, exclusions, plan, required evidence, and exit criteria. End with evidence, contradiction, completeness, and buildability audits plus PASS, PASS WITH CONDITIONS, or FAIL.</p>
<p>14. Ask only questions that materially change the phase. Otherwise make the smallest labeled assumption and continue.</p>
<p>15. Return complete, version-controlled Markdown artifacts. Keep important reasoning out of chat-only prose.</p>
<p>OUTPUT STYLE</p>
<p>Lead with the decision and implications. Use direct board-quality prose, implementation-grade detail, stable vocabulary, compact tables, and Mermaid diagrams where useful. Avoid marketing language and false certainty.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 4. Starter knowledge pack

Create these as separate Markdown or CSV files. The Word playbook itself is not the knowledge base. The canonical files are.

| **File**                        | **Purpose**                                             | **Initial content**                                                   |
|---------------------------------|---------------------------------------------------------|-----------------------------------------------------------------------|
| 00_PROJECT_CHARTER.md           | Founder thesis, boundaries, non-goals, success criteria | Use template below                                                    |
| 01_FOUNDER_CONTEXT.md           | Skills, resources, cloud constraints, risk tolerance    | Personal project context only; exclude employer data                  |
| 02_RESEARCH_PROTOCOL.md         | Source hierarchy, evidence labels, freshness rules      | Primary-first; exact proposition support                              |
| 03_ARTIFACT_REGISTRY.md         | Version, status, dependencies, supersedes               | Empty registry with schema                                            |
| 04_ASSUMPTION_REGISTER.md       | Assumption, impact, confidence, test, owner             | Seed with first-slice and buyer assumptions                           |
| 05_EVIDENCE_LEDGER.csv          | Claim-to-source traceability                            | EVD ID, claim, source, date, class, proposition, confidence, artifact |
| 06_DECISION_LOG.md              | Decision history and reversal triggers                  | Founder approval is explicit                                          |
| 07_OPEN_QUESTIONS.md            | Prioritized unknowns and validation path                | Rank by decision impact                                               |
| 08_RISK_REGISTER.md             | Product, technical, security, legal, market, financial  | Likelihood/impact are labeled judgments                               |
| 09_GLOSSARY.md                  | Canonical terms and rejected synonyms                   | Separate agent, workflow, tool, policy, memory                        |
| 10_REQUIREMENTS_TRACEABILITY.md | Need to requirement to design to test to KPI            | Begin after wedge approval                                            |
| 11_CONSTRAINTS.md               | Budget, deployment, data, security, team, providers     | State Azure/GCP preferences if applicable                             |

### 00_PROJECT_CHARTER.md starter content

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p># CAT Project Charter</p>
<p>Status: Draft</p>
<p>Owner: Founder</p>
<p>## One-sentence thesis</p>
<p>CAT is a governed company execution system that turns authorized intent into observable, auditable, and continuously improving workflows across people, agents, software, and data.</p>
<p>## Enduring ambition</p>
<p>Create a control plane for operating one or many companies while preserving accountable human authority over consequential decisions.</p>
<p>## Initial product boundary</p>
<p>Research will determine the first customer and wedge. Initial implementation will integrate with systems of record rather than rebuild ERP, CRM, accounting, identity, email, or document management.</p>
<p>## Required properties</p>
<p>Persistent and resumable; explicit identity and authorization; durable state; typed contracts; tenant isolation; provenance; approvals; budgets; evaluation; observability; reversibility; model and cloud portability where economically justified.</p>
<p>## Hypotheses, not requirements</p>
<p>Executive-role agents; unlimited swarms; a central ontology; a universal second brain; replacing systems of record; fully autonomous company operation; CAT as a new category; the CAT name itself.</p>
<p>## Initial non-goals</p>
<p>Personal health or financial automation; cross-company universal memory; high-impact autonomous financial, legal, employment, security, or customer actions; rebuilding horizontal enterprise systems; production self-modification.</p>
<p>## First proof objective</p>
<p>Demonstrate one trusted research-to-decision loop: authorized objective, typed plan, approved tools and sources, durable execution, evidence traceability, human review, recorded decision, evaluation, cost attribution, replay, and audit.</p>
<p>## Success criterion for research</p>
<p>A specific buyer, user, urgent job, measurable value, feasible wedge, defensible expansion path, and implementation package that survives evidence and red-team gates.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 5. Phase plan and gates

| **Phase**                    | **Decision enabled**                                      | **Primary artifact**         | **Founder gate**                             |
|------------------------------|-----------------------------------------------------------|------------------------------|----------------------------------------------|
| 0 Program design             | Is the research program unbiased and complete?            | 20_PROGRAM_PLAN_v1.md        | Approve questions, scope, evidence rules     |
| 1 Landscape                  | Is CAT distinct, and what should be bought or integrated? | 21_LANDSCAPE_v1.md           | Approve taxonomy and credible comparison set |
| 2A Customer hypotheses       | Which beachheads merit direct validation?                 | 22_CUSTOMER_HYPOTHESES_v1.md | Select interview targets, not final ICP      |
| 2B Customer evidence         | What did actual evidence support or falsify?              | 23_CUSTOMER_EVIDENCE_v1.md   | Approve ICP/wedge or repeat validation       |
| 3 Product thesis             | What exactly is the product and first slice?              | 24_PRODUCT_THESIS_v1.md      | Freeze MVP boundary and non-goals            |
| 4 Competitive/build-buy      | Which components deserve prototypes?                      | 25_BUILD_BUY_v1.md           | Approve spike shortlist                      |
| 5 Architecture               | Which architecture meets approved requirements?           | 26_ARCHITECTURE_v1.md        | Approve architecture with open ADRs          |
| 6 Trust/operations/economics | Can it operate safely and economically?                   | 27_TRUST_OPERATIONS_v1.md    | Approve autonomy ladder and controls         |
| 7 Business plan              | Can this become a durable business?                       | 28_BUSINESS_PLAN_v1.md       | Approve business case and validation roadmap |
| 8 Integration                | What coherent plan survives all reviews?                  | 29_INTEGRATION_MEMO_v1.md    | Freeze vocabulary, conflicts, artifact index |
| 9 Build handoff              | Can Claude Code implement Slice 0?                        | 30_BUILD_HANDOFF_INDEX_v1.md | Approve repo package before code             |

### Phase 0 kickoff

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>COMMON PHASE CONTRACT</p>
<p>Read all Approved canonical artifacts. Restate the decision this phase enables. List evidence required and exclusions. Separate facts, assumptions, judgments, and recommendations. Update the evidence ledger and changed canonical files. Show contradictions and reversal triggers. End with four audits and a Gate Review. Return the named artifact in full plus complete replacement content for each changed canonical file.</p>
<p>Produce 20_PROGRAM_PLAN_v1.md only. Deliver: founder-thesis restatement without endorsement; testable hypothesis tree; scope and authority map; 25 highest-leverage unknowns; source hierarchy and dated research cutoff; artifact manifest; initial assumptions, contradictions, risks, and glossary; weighted recommendation rubric; premortem; execution order and exit criteria. Do not perform substantive landscape research.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Phase 1: landscape

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>COMMON PHASE CONTRACT</p>
<p>Read all Approved canonical artifacts. Restate the decision this phase enables. List evidence required and exclusions. Separate facts, assumptions, judgments, and recommendations. Update the evidence ledger and changed canonical files. Show contradictions and reversal triggers. End with four audits and a Gate Review. Return the named artifact in full plus complete replacement content for each changed canonical file.</p>
<p>Produce 21_LANDSCAPE_v1.md. Research the evolution and current state of ERP, CRM, BPM, workflow, RPA, iPaaS, process mining, enterprise search, knowledge graphs, digital twins, copilots, coding agents, agent runtimes, orchestration frameworks, durable workflow engines, agent interoperability, identity/policy, observability/evaluation, and personal-agent systems. Separate systems of record, control plane, workflow engine, agent runtime, knowledge, policy, assurance, and experience. Include a do-nothing/use-existing-products baseline, direct and adjacent competitors, substitutes, enabling infrastructure, build/buy/partner/defer implications, and what evidence would show CAT is not a distinct category. Do not select final architecture.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Phase 2A: customer hypotheses

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>COMMON PHASE CONTRACT</p>
<p>Read all Approved canonical artifacts. Restate the decision this phase enables. List evidence required and exclusions. Separate facts, assumptions, judgments, and recommendations. Update the evidence ledger and changed canonical files. Show contradictions and reversal triggers. End with four audits and a Gate Review. Return the named artifact in full plus complete replacement content for each changed canonical file.</p>
<p>Produce 22_CUSTOMER_HYPOTHESES_v1.md. Rank plausible beachheads, including founder/venture studio, regulated knowledge-work team, SMB or mid-market operations, enterprise function, service provider, and any stronger segment found in research. For each: buyer, user, triggering event, job, current workflow, baseline, urgency, budget logic, trust barrier, integrations, adoption friction, measurable proof event, sales motion, expansion, and falsification test. Deliver interview guide, screening criteria, evidence-capture template, 15 demand hypotheses, and a recommendation for who to interview first. Do not label willingness-to-pay or demand as validated.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Phase 2B: customer evidence

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>COMMON PHASE CONTRACT</p>
<p>Read all Approved canonical artifacts. Restate the decision this phase enables. List evidence required and exclusions. Separate facts, assumptions, judgments, and recommendations. Update the evidence ledger and changed canonical files. Show contradictions and reversal triggers. End with four audits and a Gate Review. Return the named artifact in full plus complete replacement content for each changed canonical file.</p>
<p>Produce 23_CUSTOMER_EVIDENCE_v1.md using only the interview notes, workflow samples, design-partner feedback, or other founder-supplied evidence now in Project Knowledge. Distinguish observation, quotation, interpretation, and hypothesis. Summarize recurrent pain, current spend or effort where actually provided, objections, trust requirements, workflow baselines, proof-of-value criteria, and counterevidence. Score candidate wedges, but preserve sample limitations. Recommend APPROVE WEDGE, CONTINUE VALIDATION, PIVOT, or STOP. If no real evidence is supplied, return FAIL rather than simulating customers.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Phase 3: product thesis and Slice 0

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>COMMON PHASE CONTRACT</p>
<p>Read all Approved canonical artifacts. Restate the decision this phase enables. List evidence required and exclusions. Separate facts, assumptions, judgments, and recommendations. Update the evidence ledger and changed canonical files. Show contradictions and reversal triggers. End with four audits and a Gate Review. Return the named artifact in full plus complete replacement content for each changed canonical file.</p>
<p>Produce 24_PRODUCT_THESIS_v1.md. Define CAT in one sentence, category, buyer, user, wedge, promise, product boundary, non-goals, and kill criteria. Distinguish Slice 0, MVP, platform foundation, expansion, and long-term vision. Decide whether CAT replaces, wraps, or coordinates systems of record. Define the complete research-to-decision journey and measurable success. Compare against a simpler workflow product and a single-agent baseline. Keep the personal second brain out of the initial boundary unless evidence compels otherwise.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Phase 4: competitive teardown and architecture spikes

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>COMMON PHASE CONTRACT</p>
<p>Read all Approved canonical artifacts. Restate the decision this phase enables. List evidence required and exclusions. Separate facts, assumptions, judgments, and recommendations. Update the evidence ledger and changed canonical files. Show contradictions and reversal triggers. End with four audits and a Gate Review. Return the named artifact in full plus complete replacement content for each changed canonical file.</p>
<p>Produce 25_BUILD_BUY_v1.md. Deeply compare the short-listed products, frameworks, services, and protocols using current primary sources. Evaluate durable state, workflow semantics, permissions, tenancy, tool execution, memory, evaluation, observability, deployment, portability, maturity, pricing where public, lock-in, and failure modes. Create build/buy/partner/integrate/defer decisions by capability. Recommend small architecture spikes with hypotheses, setup, pass/fail criteria, cost limits, and decision enabled. Do not freeze the stack from feature matrices alone.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Phase 5: architecture

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>COMMON PHASE CONTRACT</p>
<p>Read all Approved canonical artifacts. Restate the decision this phase enables. List evidence required and exclusions. Separate facts, assumptions, judgments, and recommendations. Update the evidence ledger and changed canonical files. Show contradictions and reversal triggers. End with four audits and a Gate Review. Return the named artifact in full plus complete replacement content for each changed canonical file.</p>
<p>Produce 26_ARCHITECTURE_v1.md. Start from approved FRs, NFRs, threat assumptions, and spike evidence. Compare at least three options, including a minimal deterministic-workflow plus bounded-agent design. Define tenancy and authority, control and work planes, durable workflow state, agent/tool gateway, policy, event model, business versus run state, knowledge and memory, systems-of-record integration, approvals, observability, evaluation, cost attribution, recovery, deployment, and migration. Provide C4-style Mermaid views, trust boundaries, five sequence diagrams, domain model, API/event concepts, failure analysis, thin-slice deployment, ADR candidates, and measurable NFRs. Explain why every service exists and what happens when it fails.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Phase 6: trust, governance, operations, and economics

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>COMMON PHASE CONTRACT</p>
<p>Read all Approved canonical artifacts. Restate the decision this phase enables. List evidence required and exclusions. Separate facts, assumptions, judgments, and recommendations. Update the evidence ledger and changed canonical files. Show contradictions and reversal triggers. End with four audits and a Gate Review. Return the named artifact in full plus complete replacement content for each changed canonical file.</p>
<p>Produce 27_TRUST_OPERATIONS_v1.md. Define autonomy tiers by action class; identity, least privilege, policy-as-code, approvals, monetary/action budgets, sandboxing, secrets, provenance, tenant isolation, prompt-injection and memory-poisoning controls, secure SDLC, supply-chain controls, incident response, kill switches, SRE, FinOps, support, model risk, and regulatory research questions. Define controlled improvement with offline evaluation, signed changes, staged rollout, canaries, and rollback. Include operating cost drivers and attribution by tenant, company, user, workflow, run, model, tool, and project/deal.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Phase 7: business plan

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>COMMON PHASE CONTRACT</p>
<p>Read all Approved canonical artifacts. Restate the decision this phase enables. List evidence required and exclusions. Separate facts, assumptions, judgments, and recommendations. Update the evidence ledger and changed canonical files. Show contradictions and reversal triggers. End with four audits and a Gate Review. Return the named artifact in full plus complete replacement content for each changed canonical file.</p>
<p>Produce 28_BUSINESS_PLAN_v1.md. Build a board-quality plan grounded in approved evidence: category narrative, ICP, wedge, positioning, moat hypotheses, GTM, design partners, implementation motion, pricing/value metric, partnerships, scenario unit economics with formulas and labeled assumptions, roadmap, hiring, funding options, KPIs, risks, and validation milestones. Do not invent TAM, pricing acceptance, margins, or customer pipeline. Map platform expansion to validated pull and control maturity, not technical possibility.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Phase 8: integration and conflict resolution

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>COMMON PHASE CONTRACT</p>
<p>Read all Approved canonical artifacts. Restate the decision this phase enables. List evidence required and exclusions. Separate facts, assumptions, judgments, and recommendations. Update the evidence ledger and changed canonical files. Show contradictions and reversal triggers. End with four audits and a Gate Review. Return the named artifact in full plus complete replacement content for each changed canonical file.</p>
<p>Produce 29_INTEGRATION_MEMO_v1.md first, not the full final package. Act as an editorial board. Identify every material conflict across vocabulary, customer, product scope, systems of record, tenancy, authority, data flows, architecture, autonomy, economics, and roadmap. Decide each conflict or preserve it as an explicit open decision. Produce: final vocabulary; decision freeze list; unresolved blockers; traceability gaps; one-page now/not-now; premortem; and an ordered artifact index with exact filenames and dependencies. Do not generate all final artifacts in this chat.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 6. Final artifact generation

After the integration memo is Approved, open a fresh chat for each artifact below. This avoids truncation, makes review easier, and lets Claude retrieve only the relevant context.

| **Order** | **Artifact**                      | **Purpose**                                                    |
|-----------|-----------------------------------|----------------------------------------------------------------|
| 1         | 31_EXECUTIVE_MEMO_v1.md           | Board-ready decision summary                                   |
| 2         | 32_MASTER_BLUEPRINT_v1.md         | Integrated product, business, architecture, and operating plan |
| 3         | 33_PRD_v1.md                      | Users, journeys, scope, FRs, NFRs, acceptance                  |
| 4         | 34_ARCHITECTURE_v1.md             | Views, boundaries, deployment, ADR map                         |
| 5         | 35_DOMAIN_DATA_CONTRACTS_v1.md    | Entities, lifecycle, authority, privacy, retention             |
| 6         | 36_API_EVENT_TOOL_CONTRACTS_v1.md | Commands, events, idempotency, auth context, versioning        |
| 7         | 37_SECURITY_THREAT_MODEL_v1.md    | Threats, controls, residual risk, recovery                     |
| 8         | 38_EVALUATION_PLAN_v1.md          | Golden tasks, safety tests, thresholds, regression             |
| 9         | 39_DECISIONS_RISKS_v1.md          | Final decisions, alternatives, reversal triggers, risks        |
| 10        | 40_VERTICAL_SLICE_BACKLOG_v1.md   | Sequenced slices, dependencies, definition of done             |
| 11        | 41_CLAUDE_CODE_HANDOFF_v1.md      | Repository mapping and implementation instructions             |

### Reusable final-artifact prompt

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Read 29_INTEGRATION_MEMO_v1.md and all Approved artifacts relevant to [ARTIFACT]. Produce [FILENAME] in full.</p>
<p>Rules:</p>
<p>- Follow the frozen vocabulary and decisions. Do not reopen settled choices without new contradictory evidence.</p>
<p>- Trace every material recommendation to EVD, DEC, FR/NFR, ADR, RSK, or a labeled founder choice.</p>
<p>- Resolve any artifact-local inconsistency before writing.</p>
<p>- Include status, version, owner, dependencies, supersedes, and approval criteria at the top.</p>
<p>- Run evidence, contradiction, completeness, and buildability audits.</p>
<p>- Return only the complete artifact and a short Gate Review. Do not summarize omitted sections.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 7. How you should review each phase

| **Check**    | **Question**                                                                                | **Reject if**                                                                   |
|--------------|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Evidence     | Does each consequential current claim map to a source that supports that exact proposition? | Citations are decorative, circular, stale, or vendor claims are treated as fact |
| Customer     | Is there a specific buyer, user, trigger, workflow baseline, and measurable outcome?        | “All companies” or hypothetical demand is presented as validation               |
| Scope        | Does the first slice prove a complete job with explicit non-goals?                          | It recreates an agent org chart or horizontal platform                          |
| Architecture | Do requirements precede components, with explicit state, trust and failure semantics?       | It is a technology list without authority and recovery                          |
| Agency       | Does each action have identity, permission, policy, budget, audit, approval, and rollback?  | An LLM can act because it reasoned that it should                               |
| Memory       | Are writes typed, scoped, versioned, attributable, reviewable, and reversible?              | Universal vector memory or cross-tenant leakage                                 |
| Economics    | Are assumptions visible and sensitivities tied to cost/value drivers?                       | Precise forecasts rest on invented data                                         |
| Buildability | Do requirements map to contracts, tests, evals, telemetry, and acceptance?                  | Narrative plan cannot become executable work                                    |
| Consistency  | Do terms, diagrams, permissions, roadmap, and business model agree?                         | Contradictory tenancy or product boundary                                       |

| **Approval syntax** Add a short founder decision to 06_DECISION_LOG.md: status, conditions, rejected alternatives, rationale, evidence relied upon, and trigger to revisit. Never rely on “looks good” in chat as the approval record. |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

# 8. Recommended first product slice

| **SLICE 0: Governed research-to-decision** An operator submits an objective. CAT creates a typed plan, routes bounded research through approved tools and sources, records provenance and cost, presents a recommendation for human review, stores the approved decision, and supports replay and audit without production write authority. |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Why this is the right proving ground for you

It aligns with your existing strengths in evidence-heavy diligence, workflow control, audit trails, cost attribution, and quality control. More importantly, it tests the core CAT control plane without beginning with high-impact financial, legal, employment, security, or customer actions.

| **Capability proven** | **Minimum acceptance evidence**                                                       |
|-----------------------|---------------------------------------------------------------------------------------|
| Identity and tenancy  | Authenticated user, company/workspace scope, no cross-tenant access                   |
| Typed orchestration   | Versioned workflow with durable, resumable state                                      |
| Bounded agency        | One research agent with allow-listed tools and structured outputs                     |
| Policy and approval   | Policy decision plus human approval before decision finalization                      |
| Evidence provenance   | Claim-source links, access date, model/prompt/tool versions                           |
| Evaluation            | Golden tasks, citation-support checks, completeness and contradiction tests           |
| Economics             | Token/tool/infrastructure attribution by user, company, workflow, and run             |
| Audit and replay      | Append-only events, explainable reconstruction, replay without duplicate side effects |
| Recovery              | Timeout, retry, cancellation, manual takeover, and rollback procedure                 |

# 9. Repository and Claude Code handoff

### Recommended repository structure

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>cat/</p>
<p>CLAUDE.md</p>
<p>README.md</p>
<p>docs/</p>
<p>executive/</p>
<p>product/</p>
<p>architecture/adrs/</p>
<p>domain/</p>
<p>contracts/</p>
<p>security/</p>
<p>evals/</p>
<p>operations/</p>
<p>business/</p>
<p>decisions/</p>
<p>roadmap/</p>
<p>traceability/</p>
<p>apps/</p>
<p>services/</p>
<p>packages/</p>
<p>infra/</p>
<p>tests/</p>
<p>evals/</p>
<p>scripts/</p>
<p>.github/workflows/</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Do not create every application and service folder merely because it appears above. The approved architecture and first vertical slice determine which folders actually exist. Documentation is committed before implementation code.

### First Claude Code prompt: inspect and plan only

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Read CLAUDE.md and the complete approved /docs package. Do not modify code yet.</p>
<p>For Slice 0:</p>
<p>1. Restate the user outcome, scope, non-goals, requirements, threats, decisions, and acceptance criteria using stable IDs.</p>
<p>2. Inspect the repository and identify contradictions, missing prerequisites, unsafe assumptions, and specifications that are not testable.</p>
<p>3. Map each requirement to component, interface, state, event, policy, test/evaluation, telemetry, and rollback.</p>
<p>4. Propose the smallest end-to-end implementation plan, including schema, migrations, typed contracts, feature flag, test fixtures, evaluation data, and verification commands.</p>
<p>5. Identify every place deterministic code should be used instead of an LLM.</p>
<p>6. Draft or complete only the ADRs required before this slice.</p>
<p>7. List expected files and the exact evidence that will prove completion.</p>
<p>Stop after the plan and ADR proposals. Do not implement.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

### Second Claude Code prompt: implement one approved milestone

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Implement the approved milestone for Slice 0 only.</p>
<p>Follow CLAUDE.md, approved ADRs, security requirements, contracts, and repository conventions. Treat model output as untrusted. Validate structured outputs and tool arguments. Preserve human approval and audit behavior. Add or update unit, integration, contract, security, and evaluation tests as applicable. Add structured telemetry and cost attribution. Make migrations reversible where feasible. Update documentation, decision records, and the RTM for any behavioral change.</p>
<p>Run formatting, linting, type checking, tests, security checks, migrations, and relevant evals. Diagnose failures rather than bypassing checks. At completion return changed files, commands and results, acceptance-criteria evidence, security considerations, residual limitations, rollback procedure, and the next smallest milestone. Do not expand to additional agents, departments, or self-improvement features.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 10. Practical do / do not checklist

| **Do**                                                 | **Do not**                                                    |
|--------------------------------------------------------|---------------------------------------------------------------|
| Use one Project and separate chats by phase            | Use one huge chat for research, synthesis, and implementation |
| Replace canonical files after each approved phase      | Rely on chat history as memory                                |
| Keep citations at claim level and verify exact support | Assume a citation means the claim is true                     |
| Use interview evidence before finalizing the wedge     | Let Claude simulate customer validation                       |
| Generate final artifacts one at a time                 | Request nine full artifacts in one response                   |
| Prototype high-impact architecture decisions           | Choose infrastructure from a static feature matrix            |
| Build a full vertical outcome                          | Build horizontal infrastructure with no user outcome          |
| Use systems of record through integrations first       | Rebuild ERP, CRM, identity, billing, and email in the MVP     |
| Keep personal and company contexts separate            | Create universal memory or automatic context transfer         |
| Use evaluations and executable checks                  | Treat linting as security, product validation, or correctness |
| Record every scope or decision change                  | Let implementation silently redefine the product              |

# 11. Sources and provenance

This plan synthesizes and critiques the two supplied playbooks. The first provides the strongest detailed phase architecture and build contracts; the second provides the strongest canonical-file discipline, assurance framing, and proposed first product slice. Current Anthropic guidance also emphasizes deliberate context management and giving Claude Code executable verification signals such as tests, builds, linters, and visual checks. Product UI and model availability should be checked in your account at execution time.

- CAT_Claude_Project_Research_and_Build_Playbook.docx, supplied by Cole Masterson, 18 August 2026.

- CAT_Claude_Project_Research_and_Build_Playbook 3.docx, supplied by Cole Masterson, 18 August 2026.

- Anthropic, “Best practices for Claude Code,” https://code.claude.com/docs/en/best-practices, accessed 18 August 2026.

- Anthropic, “Prompt library,” https://code.claude.com/docs/en/prompt-library, accessed 18 August 2026.

# 12. One-page launch checklist

☐ Create a fresh private CAT Project.

☐ Paste Section 3 into Project Instructions.

☐ Create and upload the 12 starter canonical files.

☐ Do not upload the two prior playbooks.

☐ Complete founder context and constraints without proprietary employer data.

☐ Run Phase 0 in a fresh chat.

☐ Apply the founder gate and replace canonical files.

☐ Run Phase 1, then 2A.

☐ Conduct real interviews or collect workflow evidence before Phase 2B.

☐ Do not approve the wedge without Phase 2B evidence or an explicit founder override.

☐ Run the product red team after Phase 3.

☐ Run architecture spikes before freezing Phase 5.

☐ Run security and simplification red teams after Phase 5.

☐ Run business/customer red team after Phase 7.

☐ Approve the integration memo before final artifacts.

☐ Generate each final artifact in its own chat.

☐ Commit approved handoff files to Git.

☐ Start Claude Code with the planning prompt.

☐ Implement only Slice 0, one milestone per branch/PR.

☐ Require tests, evals, telemetry, security checks, and RTM updates before merge.
