# V-000 — Vision baseline and drift audit

Status: v0.2, proposed. The founder's answers of 2026-11-15 are folded in. Acceptance is the founder's merge of the pull request that carries this file (Gate G0).

Inputs: founder note and chat replies of 2026-11-15; `AZI-HUB-PROJECT-BRIEF.md`; `CAT_Research_to_Product_Plan` (2026-08-18); the Gemini artifacts; the code of `azi-hub` and `autonomous-startup-engine`.

## 1. Founder intent, restated

One person directs their personal life and a set of organizations through a single self-improving system. Agents do the execution. The human keeps creative direction and the key decisions.

A chief-of-staff agent knows the person's own life well enough to work with the administrators of their organizations. The personal second brain is kept apart from each organization's second brain and shared only on purpose.

It works for a new organization and for an existing one. Cole uses it first. If a product has room, other people get it, with onboarding help for those who already have operations.

## 2. Fixed decisions (Cole, 2026-11-15)

| ID | Decision |
| --- | --- |
| F-01 | The personal layer is part of the product. A customer may leave it off. |
| F-02 | Super-organization and sub-organization structure stays. |
| F-03 | New and existing enterprises are both in scope. |
| F-04 | Humans hold creative direction and key decisions. |
| F-05 | The system improves itself under control. |
| F-06 | Cole is the first user. Multi-person collaboration (the "social" layer) comes later. |
| F-07 | The route check is the first research step. Route A (product) is preferred. Route B (personal system on existing frameworks) is the fallback if a product has no room. |
| F-08 | New repository `CDM2/azi-hub-v2`. AZI Hub stays up about one more week for the morning reservation-booking agent, which then moves to the personal layer. |
| F-09 | `autonomous-startup-engine` is Cole's to use as he wishes. |
| F-10 | Personal-layer scope is chosen by the user and can grow, including financial and health areas. A user can ask for a new section, for example investing, subscriptions or diet. Users will not all want the same sections. |
| F-11 | Agents have the access they need to build those sections. |
| F-12 | Setup consulting is allowed as onboarding, aimed at people with existing operations. No custom framework is built per customer. |
| F-13 | Candidate customers: existing large organizations; new, well-funded organizations; non-technical solopreneurs running or starting small businesses. |
| F-14 | Organizations modelled first: AZI Hub with AltZ Capital, Sandbox and Media, plus Toveli as a sub-organization. Once the product is trusted these are expected to be wiped, with Toveli as the main organization. |
| F-15 | First slice: the personal layer plus the reservation-agent migration, then the research-to-decision workflow from the CAT plan. |
| F-16 | Claude-first behind an adapter boundary. Choosing a model per task must be easy, by setting or by asking the system. |
| F-17 | Self-hosted on Cole's VPS for his own use. A hosted offering is decided at Gate G1a. |
| F-18 | Build budget: up to $1,000 a month for agent and API runs, on top of existing Claude Max, ChatGPT and GitHub Pro subscriptions. Cole can raise it. |

## 3. Non-negotiables proposed to carry over

| ID | Rule | Origin |
| --- | --- | --- |
| N-01 | No agent pushes to production, moves money, or changes another organization's state without human approval. | AZI Hub kill list |
| N-02 | No tenant mixing. Personal to organization is explicit push only. Organization to organization is zero by default. | AZI Hub tier model |
| N-03 | Deterministic software decides permissions, policy, money, state transitions and approvals. | CAT rule 5 |
| N-04 | A multi-agent design must beat a single agent with workflows to be kept. | CAT rule 7 |
| N-05 | Self-improvement acts only on verifiable metrics. Strategy stays human-gated. | AZI Hub brief 6.6 |
| N-06 | No employer or third-party proprietary data enters this project. | CAT plan, step 4 |
| N-07 | Agents extend a user's own instance. Changes to the shared core go through the build loop and its review tiers. | AZI Hub framework and instance boundary; applies F-11 |
| N-08 | Health and financial data are the highest sensitivity class: they stay in the personal tenant, are never pushed to an organization by default, and stay out of logs and evaluation sets. | Follows from F-10 and N-02 |

How N-01 applies to F-10: a finance section may read, analyze and propose. A trade, payment or transfer needs the user's approval each time, unless a later decision record sets a pre-approved limit.

## 4. Drift audit

| # | Earlier position | Current intent | Disposition |
| --- | --- | --- | --- |
| D-01 | CAT plan: personal second brain stays outside the product boundary and outside tenancy. | F-01. | Resolved by F-01. The old rule's safety content is kept as N-02: explicit push only. |
| D-02 | CAT charter non-goal: personal health or financial automation. | F-10. | Resolved by F-10. In scope as sections the user chooses; N-01 and N-08 apply. |
| D-03 | AZI Hub kill list: no one-off consulting or services work. | F-12. | Resolved by F-12. The kill-list item narrows to "no bespoke one-off builds". |
| D-04 | AZI Hub: infrastructure first. CAT checklist: build a full vertical outcome. | Landscape shows the horizontal layer is crowded. | The first slice is a vertical outcome for Cole (F-15). The route check decides the rest. |
| D-05 | AZI Hub: named executive-role agents. CAT and Gemini: a hypothesis. | The chief-of-staff role is stated intent; other roles are undecided. | Chief of staff is a requirement. Other role agents stay a hypothesis for R-03. |
| D-06 | Gemini artifacts: every quadrant and the personal layer left open. | Section 2. | Superseded by section 2. |
| D-07 | Brief and dossier: the tenant is resolved from request context, never accepted as a parameter. | Code takes it from a header the client sets. | Implementation claims in summaries are unverified until checked in code. The new build ties the organization to the signed-in person. |
| D-08 | CAT plan Slice 0: governed research-to-decision. | F-15. | Resolved by F-15: it is the second step of the first slice. |
| D-09 | CAT plan: integrate with systems of record, do not replace them. | Unchanged. | Default stays "integrate"; R-09 can challenge it. |
| D-10 | Plan requires one first wedge. | F-13 names three customer groups with different buyers, sales cycles and competitors. | All three stay candidates. R-01 and R-08 rank them and name one first wedge. Cole as first user is closest to the solopreneur group; the onboarding thesis (F-12) is closest to existing organizations. |
| D-11 | CAT charter non-goals: production self-modification; high-impact autonomous financial actions. | F-10 and F-11: agents build personal sections, including financial ones. | Allowed inside the instance boundary (N-07) with N-01. R-05, R-06 and R-07 define the controls. |

## 5. Route A hypothesis, to be tested in R-01

| ID | Claim | What would falsify it |
| --- | --- | --- |
| H-A1 | People and organizations with existing operations cannot set up current frameworks without help. | A product they can set up alone already covers the personal layer, an organization hierarchy and governed self-updating. |
| H-A2 | They will pay for onboarding and keep paying to stay in the ecosystem. | Interviews or pricing evidence show they will not, or that onboarding is a one-time job with no reason to stay. |
| H-A3 | What they would be onboarded to is not already sold turnkey. | Polsia, NanoCorp, Paperclip or a control-plane vendor already sells it to the same buyer. |
| H-A4 | Buyers want a personal layer whose chief-of-staff agent coordinates with organization administrators, and vendors do not offer it. | A vendor offers it, or buyers do not want personal and company context in one system. |

Early counter-signals, from search results only: NanoCorp and Polsia already sell no-code creation of AI-run companies, and OpenAI pairs forward-deployed engineers with enterprise customers for onboarding. Neither covers the personal layer as far as the first pass shows.

## 6. Open items

Nothing blocks Phase 1a. Left for later gates:

- The first wedge among the F-13 groups: Gate G1a and Gate G1.
- Pre-approved limits for money movement, if any: R-05.
- How far agents may change shared core code: R-06 and R-07.

## 7. Acceptance record

| Record | Person | Date | Scope |
| --- | --- | --- | --- |
| Draft v0.1 prepared | Claude session | 2026-11-15 | Not accepted |
| Answers and direction to revise and push | Cole | 2026-11-15 (chat) | Authorizes v0.2 and the Phase 0 seed push; not acceptance |
| Founder acceptance (Gate G0) | pending | | Merge of the pull request carrying v0.2 |
