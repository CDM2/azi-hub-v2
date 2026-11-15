# R-01 — Category, competitors and existing-tool map (route check)

Status: draft for review, not accepted. As of 2026-11-15. Prepared by a Claude session on Cole's instruction of 2026-11-15. With R-02 it feeds Gate G1a.

Reads with `docs/source/V-000` (section 5 holds the hypotheses), `docs/source/P-000` and `docs/source/INV-000`. Evidence IDs such as E-03 point to rows in [`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md). A sentence marked **Judgment** is my reading of the evidence, not a sourced fact.

## Bottom line

- **The generic platform has no room.** Org-chart orchestration is free and MIT-licensed in Paperclip (E-01, E-02). Enterprise agent governance costs $15 to $21 a seat from Microsoft and Google (E-18, E-23). An AI-run company costs $20 to $30 a month from Polsia and NanoCorp (E-12, E-14).
- **The personal layer stopped being a gap this autumn.** Meta, OpenAI and Anthropic each launched a proactive personal agent between 2026-09-08 and 2026-10-21, and two of the three are aimed at small-business owners (E-27, E-29, E-30). Ariso already sells one chief of staff across a person's work and life (E-31).
- **One combination is still unsold.** No product found gives one owner a personal space, several organizations under a holding structure, sharing between them only on purpose, and self-improvement gated by evidence. Paperclip covers most of the organization half, part of self-improvement and no personal layer (E-03, E-04, E-05).
- **Hypotheses.** H-A1 holds in part. H-A2 is untested. H-A3 is partly falsified. H-A4 is falsified as written and survives in a narrower form.
- **Customer ranking.** First, non-technical owner-operators who already run a small business. Second, new well-funded organizations. Third, existing large organizations, which I recommend dropping as a first wedge.
- **Recommendation for Gate G1a.** Keep Route A, narrowed and staged. Build the first slice the Route B way: adopt existing tools and write only the missing glue. Hold all Route A-only spending until about ten owner-operator interviews have tested H-A2 and H-A4.
- **Limits.** This is desk research. Nobody was interviewed. Paperclip was read as source, not run. The two control planes were assessed from documentation and press.

## Method and limits

| Step | What was done |
| --- | --- |
| Web | 26 searches on 2026-11-15. Three pages fetched and read in full; every other web source was read as a search excerpt only. The ledger marks which is which. |
| Paperclip | Cloned `paperclipai/paperclip` at commit `da8cfda` (2026-11-15). Read the README, roadmap, product, deployment, installation, skill-policy and memory documents and the company schema. Not installed and not run: running third-party code belongs in the R-02 spike, in a throwaway environment. |
| Control planes | Microsoft Agent 365 and OpenAI Frontier assessed from Microsoft's documentation and from press and analyst coverage. No tenant or account was available. |
| Not done | Customer interviews. Hands-on trials of any product. Health-data connectors, authorization engines, durable execution and payment rails, which belong to R-02, R-04 and R-05. A separate review session to attack this report, which P-000 requires before acceptance. |

Many sources are vendors writing about competitors. The ledger grades each row; rows graded Low carry no conclusion on their own.

## 1. The category in November 2026

| Layer | Products | Entry price | Sold to | Evidence |
| --- | --- | --- | --- | --- |
| AI-run company builders | Polsia, NanoCorp, brainer.ceo, Cofounder | $20 to $120 a month; Polsia and NanoCorp also take 3% and 20% of revenue | Solo founders, mostly at the idea stage | E-12, E-14, E-16 |
| AI-employee bundles | Marblism, Lindy | $24 to $50 a month | Small businesses | E-17 |
| Org-chart orchestrator | Paperclip | Free; vendor cloud in invite-only beta | Technical operators and teams | E-01, E-10 |
| Hosted personal agents | Muse, ChatGPT dots, Claude Duet, Ari | Free to about $100 a month at entry, mostly bundled into plans people already pay for | Individuals, professionals, small-business owners | E-27, E-29, E-30, E-31 |
| Self-hosted personal agents | OpenClaw, Hermes Agent | Free, plus setup effort or a paid installer | Technical individuals; others through installers | E-32, E-33, E-34 |
| Enterprise control planes | Microsoft Agent 365, Google Gemini Enterprise, AWS AgentCore, OpenAI Frontier and Presence | $15 to $21 a seat, consumption, or custom contract | Technology leaders of large organizations, often through consultancies | E-18, E-20, E-21, E-22, E-23 |
| Agent runtime | Claude Agent SDK, Claude Managed Agents | Tokens; hosted adds $0.08 per session-hour | Developers | E-25, E-26 |

The 2x2 kept from the Gemini corpus (S-007), filled in:

| | One organization | Several organizations |
| --- | --- | --- |
| **New (greenfield)** | Polsia, brainer.ceo, Cofounder | NanoCorp and Paperclip: many companies, flat and isolated (E-03, E-14) |
| **Existing (brownfield)** | Agent 365, Gemini Enterprise, Frontier, Muse for Small Business, Duet, Marblism, Lindy | Nothing found |

The empty cell is existing operations across several organizations. A personal layer above it is also unsold. **Judgment:** an empty cell shows nobody sells it; it does not show anybody wants it.

## 2. Teardowns

### Paperclip (source read)

Paperclip is the closest existing thing to AZI Hub's organization layer. It is MIT-licensed, self-hosted, and starts from one command on a machine with Node.js 24.11 (E-01).

| V-000 need | Paperclip | Evidence |
| --- | --- | --- |
| Agents in an org chart with roles, delegation, budgets | Yes | E-02 |
| Human approvals, audit trail | Yes; approval for new agents is off by default | E-02, E-08 |
| Several organizations, isolated | Yes | E-03 |
| Super-organization over sub-organizations | No. Companies are flat; no parent column or grouping table | E-03 |
| Sharing between organizations on purpose | No. Cross-company access stays denied; export and import move whole companies | E-02, E-03 |
| Personal layer | No | E-04 |
| Second brain | Experimental, off by default, company-scoped connectors | E-06 |
| Governed self-improvement | Part. Skills have tests, versions and restore; agents may change skills without approval by default; organizational learning is planned | E-05, E-06 |
| Model choice per agent | Yes, ten built-in adapters including Claude Code | E-07 |
| Set up by a non-technical person | Not today. Vendor cloud is an invite-only beta; a reviewer notes the technical barrier | E-10, E-11 |

Risks seen in its own documents: telemetry is on by default, and budget stops act on recorded spend so a run can pass its limit (E-08). The project moves fast: its README claims over 2,700 merged pull requests (E-01). Its roadmap lists Self-Organization and Automatic Organizational Learning as planned (E-06). **Judgment:** those two items, plus a public cloud launch, are the moves most likely to close the gap this project is aiming at.

### Microsoft Agent 365 (documentation)

Agent 365 is governance, not a runtime. It gives each agent an identity in Microsoft Entra, lists every agent in the admin center, and applies access policy. Microsoft's own guide calls it metadata and governance only (E-19). It costs $15 per user a month on top of a qualifying Microsoft 365 licence (E-18). It has no personal layer, no organization modelling and no self-improvement. **Judgment:** it matters only to the large-organization group, where it sets the price of governance at $15 a seat.

### OpenAI Frontier (press and analyst coverage)

Frontier is sold, not downloaded. It has no public price and no self-serve signup; OpenAI attaches its own engineers and has multi-year alliances with Accenture, BCG, Capgemini and McKinsey to implement it (E-20, E-21). Its later Presence product is sold the same way (E-22). **Judgment:** this confirms that large organizations need help, and shows who already supplies it.

## 3. Hypothesis tests

### H-A1 — Buyers cannot set up current frameworks without help

**Verdict: holds in part. Not falsified.**

- **For.** A market of paid installers exists for OpenClaw, mostly at $99 to $499 one-time (E-34), and sellers claim owners spend 15 to 40 hours doing it themselves (E-37, Low). Paperclip's hosted version is not open to the public (E-10). At the enterprise end, 17% of organizations have agents deployed, and OpenAI sells Frontier through its own engineers and four consultancies (E-24, E-20, E-21).
- **Against.** Hosted personal agents need no setup at all. Duet, Muse and dots are switched on inside a subscription (E-27, E-29, E-30). Polsia and NanoCorp create a company from a prompt (E-12, E-14).
- **Falsifier check.** V-000's falsifier is a product that can be set up alone and covers the personal layer, an organization hierarchy and governed self-updating. None was found. Paperclip has the hierarchy half-built and no personal layer (E-03, E-04). Duet and Ari have the personal layer and no organization of agents (E-27, E-31).
- **Judgment.** "Cannot set up" is true of self-hosted frameworks and of enterprises. It is false for the hosted agents a solopreneur is most likely to try first. Help is needed for the combination, not for any single part.

### H-A2 — They will pay for onboarding and keep paying to stay

**Verdict: untested. Desk evidence supports a small one-time fee and says nothing reliable about staying.**

- **For.** Installers list managed plans at $79 to $299 a month (E-35). One competitor sells setup plus a monthly retainer (E-38, Low). Enterprises sign multi-year implementation alliances (E-21). Among US consumers who use agents, 92% pay for AI (E-39).
- **Against.** Listed prices are offers, not purchases; no page reports uptake (E-35). The only revenue anecdote contradicts itself (E-36, Low). Prices are falling: installs from $29, a hosted Paperclip reseller at 10 euros a month closed in October, and Polsia cut its revenue share from 20% to 3% (E-34, E-10, E-12). The big vendors bundle agents into plans people already hold (E-27, E-30). Few NanoCorp businesses earn anything, which caps what their owners will keep paying (E-15, Low).
- **Judgment.** What people demonstrably pay monthly for today is hosting and upkeep, which is a commodity. "Staying in the ecosystem" needs a reason that survives a free Muse and a bundled Duet. Only interviews can test that. P-000 already says desk research never counts as customer validation.

### H-A3 — What they would be onboarded to is not already sold turnkey

**Verdict: partly falsified.**

- **Each main job is already sold turnkey to each buyer.** Solo founders: Polsia, NanoCorp, brainer.ceo (E-12, E-14, E-16). Small businesses: Marblism, Lindy, Muse for Small Business, Duet (E-17, E-27, E-30). Funded startups: Cofounder, or Paperclip run by their own engineers (E-16, E-01). Large organizations: the control planes and their consultancies (E-18 to E-23).
- **The combination is not sold.** Across five company builders, none mentions a personal layer, parent and child companies or sharing between companies (E-16). Paperclip confirms the same in code (E-03, E-04).
- **Judgment.** The category is taken. What remains is three features no vendor has put together: a holding structure with deliberate sharing, a personal space with a one-way boundary, and improvement gated by evidence. Features are a weaker position than a category, and the nearest vendor has two of them on its roadmap (E-06).

### H-A4 — Buyers want a personal layer whose chief of staff coordinates with organization administrators, and vendors do not offer it

**Verdict: falsified as written on the vendor half. A narrower claim stands. The buyer half is untested.**

- **Vendors now offer a personal layer.** Duet is built for professionals and small-business owners (E-27). Muse has a small-business version (E-30). Ari is sold as one chief of staff for work and life, with a privacy line, coordinating with colleagues' agents (E-31).
- **What no vendor offers.** A chief of staff that works with the agent administrators of the owner's own organizations, across a super-organization and its sub-organizations, with the personal second brain filtered from each organization's. Duet's announcement mentions no organizations or separation of contexts, and Team and Enterprise plans are excluded at launch (E-27, E-28). Dots are one per person, with teams of dots planned (E-29). Ari coordinates between people, not between an owner and their organizations' agents (E-31).
- **Buyers.** Demand for personal agents is real: 41% of US AI users have tried one (E-39). Willingness drops for the data F-10 puts in scope: 20% of agent users have connected a financial account and 23% a health app (E-39); 15% in another survey would share financial information (E-41); 22% would allow no financial transactions (E-40). Ari markets the wall between person and employer as a feature (E-31).
- **Judgment.** For an owner-operator the person and the company are the same principal, so one system for both is natural. For an employee of a large organization it is a liability. H-A4 can only be true for owner-operators, which narrows the buyer before any interview is held.

### Program-level falsifiers kept from the Gemini corpus (S-008)

| Falsifier | Reading on 2026-11-15 |
| --- | --- |
| Model providers and hyperscalers absorb orchestration and capability composition | Largely met for orchestration, governance and the personal agent (E-18, E-23, E-25, E-27). Not met for multi-organization structure. |
| Implementation cost exceeds the value created | Unknown. Low earnings on company builders are a warning (E-15, Low). |
| No painful, budgeted customer problem | Untested. Needs interviews. |

## 4. Capability map

Each capability V-000 asks for, the best existing tool found, and the glue nobody supplies. Coverage: **Full**, **Most**, **Part**, **None**. The last column names the report that settles the choice; R-01 only nominates.

| ID | Capability (V-000 reference) | Best existing tool | Coverage | Missing glue | Evidence | Settled in |
| --- | --- | --- | --- | --- | --- | --- |
| C-01 | Personal chief-of-staff agent that knows the person's life (F-01, section 1) | Claude Agent SDK agent on the VPS; Hermes Agent as the alternative to test. Claude Duet is the hosted reference. | Part | Duet is a closed preview with no self-hosting and no way to extend it. The SDK supplies the loop, not the knowledge of a life. OpenClaw is passed over on its 2026 security record. | E-26, E-27, E-32, E-33 | R-02 |
| C-02 | Personal second brain kept apart from each organization's (section 1, N-02) | None as a product. AZI Hub's wiki with row-level visibility is the pattern (INV-000). | None | The boundary itself and filtered views. Every memory product found is scoped to a company or an agent. | E-04, E-06, E-25, E-31 | R-04 |
| C-03 | Super-organization and sub-organizations (F-02) | Paperclip, one company per organization | Part | A holding layer over flat companies: ownership, roll-up views, budgets under a parent. | E-03 | R-03 |
| C-04 | Explicit push from personal to organization; nothing between organizations by default (N-02) | None. Paperclip's isolation supplies "nothing by default". | None | A broker that shares one item on one approval and records it. | E-03 | R-03, R-05 |
| C-05 | Agents in roles; single, group and chain conversations (D-05, INV-000) | Paperclip | Most | Group and ordered-chain chat were not found in its documents. Verify hands-on. | E-02 | R-03 |
| C-06 | Human approval for key decisions, production, money and other organizations' state (F-04, N-01) | Paperclip approvals and tool gateway; Agent SDK permissions and hooks beneath | Most | Defaults must be tightened to N-01. Production promotion stays in CI. | E-02, E-08, E-26 | R-05 |
| C-07 | Deterministic permissions, policy and state transitions (N-03) | Paperclip's company-scoped checks, approval stages and budget stops | Part | No general policy engine was evaluated. | E-02, E-03, E-08 | R-05 |
| C-08 | Self-improvement gated by verifiable metrics (F-05, N-05) | Paperclip Skill Studio with a company skill policy | Part | Promotion is not tied to a metric. Hermes edits its own skills with no governance; Managed Agents' equivalents are beta or preview. AZI Hub's proposal, evaluation and gate record is the pattern (INV-000). | E-05, E-06, E-25, E-33 | R-06 |
| C-09 | Agents build new personal sections on request (F-10, F-11, N-07) | Claude Code or the Agent SDK as builder; Paperclip plugins as a surface; read-only Plaid MCP servers for finance data | Part | A section scaffold, a schema per section, sensitivity labels. Health-data connectors not researched. | E-02, E-26, E-46 | R-02, R-04 |
| C-10 | Health and financial data stay in the personal tenant, out of logs and evaluation sets (N-08) | Self-hosted MCP servers that keep tokens on the machine | Part | Log redaction, evaluation-set exclusion, and a test that proves both. | E-39, E-41, E-46 | R-05, R-07 |
| C-11 | Money moves only with approval each time (N-01 applied to F-10) | Paperclip's tool gateway set to "ask first" for the approval. No self-hosted payment rail was researched. Duet's design is the reference: virtual card, approval each time, trades and transfers blocked. | Part | The payment rail and its approval record. AZI Hub's virtual-card tooling is prior art, not re-checked. | E-02, E-27, E-40 | R-05 |
| C-12 | Morning reservation-booking agent (F-08, F-15) | AZI Hub's own Resy and OpenTable tools, ported (INV-000) | Part | No public booking API exists, and Resy has deactivated accounts that ran agents. The port carries that risk. The sanctioned route is booking inside ChatGPT; a scheduled, sanctioned route was not found. | E-43, E-44, E-45 | R-02 spike; Phase 5 milestone 1 |
| C-13 | Research-to-decision workflow (F-15) | This repository's own loop of manifest, ledger and gates; Paperclip planning mode with plan approvals as a possible host | Part | The ledger and the gate record as first-class objects. | E-02 | R-03 |
| C-14 | Model choice per task, Claude-first (F-16) | Paperclip adapters | Most | Changing the model by asking the system was not found. | E-07, E-33 | R-02 |
| C-15 | Self-hosted on a VPS (F-17) | Paperclip, Agent SDK and Hermes all self-host | Full | None. | E-01, E-25, E-26, E-33 | R-02 |
| C-16 | Identity: a person, their personal space, memberships and roles (P-000) | Paperclip authenticated mode | Part | The personal space as a tenant in its own right. | E-02, E-04, E-19 | R-05 |
| C-17 | Audit and decision log (N-01, INV-000) | Paperclip activity log | Most | A decision log tied to gates. | E-02, E-05 | R-05 |
| C-18 | Spend limits per organization and agent (F-18) | Paperclip budgets | Most | Stops can lag and do not see flat subscriptions; add a second limit at the provider. | E-02, E-08 | R-02 |
| C-19 | Onboarding an existing organization (F-03, F-12) | None self-serve. Enterprises get vendor engineers and consultancies. | None | The import method. | E-06, E-20, E-21 | R-09 |
| C-20 | Creating a new organization (F-03) | Paperclip onboarding and team templates | Most | A sub-organization scaffold under the holding layer. | E-02 | R-03 |
| C-21 | Multi-agent design measured against a single-agent baseline (N-04) | None found | None | An evaluation harness that runs both designs on the same tasks. | E-05 | R-03, R-06 |
| C-22 | Multi-person collaboration, later (F-06) | Paperclip multiple human users; Ari for agent-to-agent between people | Part | Deferred by F-06. | E-02, E-31 | Phase 5 |

**What the map says.** Paperclip appears as the best existing tool, or part of it, in 15 of 22 rows. The four rows with no coverage are the personal second brain, deliberate sharing, brownfield import and the baseline test. **Judgment:** the custom work is a personal tenant, a holding layer with a sharing broker, a metric-tied improvement gate and controls for sensitive data. That matches the AZI Hub items INV-000 already marks "Pattern", and the items it marks "likely replaced" are the ones an adopted control plane and runtime supply.

**Two findings for the first slice.**

- **Reservation agent (C-12).** Resy has deactivated accounts that ran booking agents (E-44). Moving the agent as it is carries that risk whichever route is chosen.
- **Budget (C-18, F-18).** Since 2026-06-15, Agent SDK use on a Claude subscription draws on a separate monthly credit (E-26). R-02 should confirm how that interacts with the Claude Max plan and the $1,000 cap.

## 5. Customer groups, ranked

| | Non-technical solopreneurs (F-13) | New, well-funded organizations | Existing large organizations |
| --- | --- | --- | --- |
| Size signal | 32.0M US businesses with no employees in 2024 (E-42) | Not measured | Not measured |
| Do they need help (H-A1)? | Yes for self-hosted tools; no for hosted agents (E-34, E-27) | Least. They have engineers and self-serve tools (E-01, E-16) | Most (E-24) |
| Who already serves them | Polsia, NanoCorp, Marblism, Muse, Duet (E-12, E-14, E-17, E-27, E-30) | Cofounder, Paperclip, the runtimes (E-16, E-01, E-26) | Microsoft, Google, AWS, OpenAI, with the four largest consultancies (E-18 to E-23) |
| Price points seen | Free to $50 a month; installs at $99 to $499 (E-12, E-17, E-34) | About $100 to $125 a seat a month (E-16, E-29) | $15 to $21 a seat for governance; custom contracts above (E-18, E-20, E-23) |
| Does the personal layer fit? | Yes: owner and business are one principal | Weakly: employees, not owners | No: employers and employees want a wall (E-31) |
| Can one founder reach and serve them? | Yes, but support load is high | Yes | No |
| **Rank** | **1** | **2** | **3** |

**Why this order.** The large-organization group has the clearest need and the worst position: the vendors own the product, the consultancies own the onboarding, and the personal layer is unwelcome. The well-funded group can buy but needs the least help, so F-12's onboarding thesis is weakest there. The solopreneur group is where the personal layer fits and where Cole is himself a user, at the cost of low prices and strong free competitors.

**Narrowing rank 1.** F-13 says "running or starting". Those starting are served for $20 to $30 a month with poor reported results (E-12, E-14, E-15). F-12 aims onboarding at people with existing operations. **Judgment:** the first wedge to test is non-technical owner-operators who already run one or more small businesses. This resolves the tension recorded in D-10.

**A consequence for F-17.** These buyers cannot self-host; they pay installers or use hosted agents (E-34, E-27). A product for them means a managed instance per customer. That decision belongs to Gate G1a.

This ranking is a desk judgment. P-000 leaves the naming of one wedge to R-01 and R-08 together.

## 6. Route recommendation for Gate G1a

Cole decides. R-02 has not run yet and also feeds the gate.

**Recommend: Route A, narrowed and staged.**

1. **Close two doors.** The generic platform, and large organizations as a first customer.
2. **Keep one open.** A managed instance for owner-operators with existing operations, offering what nobody combines: a personal layer, several organizations with deliberate sharing, and gated self-improvement.
3. **Build by adoption.** The first slice in F-15 is identical under both routes. Assemble it from existing tools and write only the glue in section 4.
4. **Hold Route A-only spending.** No licensing, blank-tenant packaging or multi-user work until H-A2 and H-A4 have been put to about ten owner-operators. Interviews cost no build budget.
5. **Decide again at Gate G1** with interview notes in the ledger.

**Fall back to Route B if any of these happens:**

- Paperclip opens its cloud to the public with a personal workspace or a company hierarchy.
- Duet, dots or Muse add several organizations under one owner.
- Fewer than three of ten interviewed owner-operators would pay for setup and a monthly plan.

**The main risk in this recommendation.** The narrowed wedge describes Cole. A sample of one is the weakest evidence in this report, and the recommendation depends on interviews that have not happened.

## 7. Proposed follow-ups

None of these is made by this report. Each needs Cole's acceptance.

| Where | Proposed change |
| --- | --- |
| V-000 section 5 | Restate H-A4 as the narrower claim in section 3. Restate H-A3 as "the combination is not sold turnkey". Replace the counter-signals paragraph with Duet, dots, Muse and Ari. |
| V-000 D-10 | Record the provisional ranking and the narrowed first wedge. |
| P-000 landscape table | Add a row for hosted personal agents. |
| R-02 scope | Spike Paperclip as the control plane with the Claude Agent SDK or Claude Code beneath it, on the VPS, with the reservation agent as the test job. Run the same job on a single agent as the N-04 baseline. Install Paperclip there, since R-01 did not run it. |
| R-08 | Bring interviews forward: ten owner-operators, testing H-A2 and H-A4, before Gate G1. |
| INV-000 | Add the account risk to the reservation-booking row. |

## 8. Questions for Cole

1. Does the morning reservation agent compete for tables at release time, or book ordinary availability? The first has no sanctioned route (C-12).
2. Do you accept dropping large organizations as a first-wedge candidate?
3. May R-02 treat adopting Paperclip as the leading option for the organization layer?
4. Can you reach ten owner-operators for interviews before Gate G1?

## Sources

All external claims are in [`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md), rows E-01 to E-46, with links, how each source was read and a confidence grade. Findings about AZI Hub and autonomous-startup-engine come from INV-000 and P-000.
