# R-01 — Category, competitors and existing-tool map (route check)

Status: v1.0, final for acceptance. As of 2026-11-15. Prepared by a Claude session on Cole's instructions of 2026-11-15. Acceptance is the founder's merge of the pull request that carries this file. With R-02 it feeds Gate G1a. No separate review session has attacked it.

Reads with `docs/source/V-000` (section 5 holds the hypotheses), `docs/source/P-000` and `docs/source/INV-000`. Evidence IDs such as E-03 point to rows in [`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md). A sentence marked **Judgment** is my reading of the evidence, not a sourced fact.

**Changed since v0.1** (same day, after Cole's review):

- Read the original `CDM2/azi-hub` code and added it as a third system beside Paperclip and Polsia (sections 2 and 6).
- Corrected the Paperclip teardown: it has an alpha LLM Wiki plugin that v0.1 missed (E-47).
- Added Paperclip's operating model, extension points and commercial signals, and a Polsia teardown.
- Tested six thesis claims Cole raised in review (section 4).
- Added the build options: fold in, fork, plugin, compose or own (section 7).
- Named small local businesses as the first wedge, with price evidence (section 8).
- Changed the recommendation from "Route A, narrowed and staged" to a specific shape of Route A (section 9).

**Changed in v1.0** (after Cole's answers to the questions in v0.2):

- Recorded Cole's four answers, his position on Paperclip and his statement of the mission (section 11).
- Made Cole's own ventures the first pilots, ahead of local businesses (sections 8 and 9).
- Took the reservation agent out of the build's concerns (C-12).
- Added what replicating Paperclip would take and the triggers for moving to an own orchestrator (section 7).

## Bottom line

- **Orchestration is taken. Adopt it.** Paperclip gives away an org-chart orchestrator with more than 2,700 merged pull requests behind it, by its own count (E-01, E-02). Nothing here supports trying to beat it at that.
- **AZI Hub already prototyped the part nobody sells.** Its tiered tenancy, permission-filtered second brain, one-way personal briefing and gated improvement loop exist in working code (E-57, E-58, E-59). Paperclip has none of the first three and half of the fourth (E-03, E-04, E-05, E-47). Polsia has none (E-61 to E-64).
- **Compose, do not fold in.** Keep Paperclip unmodified as the per-organization engine. Build the tiers, the second brain and the sharing broker as a separate service that agents reach over MCP. R-02 should spike this (section 7).
- **Thesis claims.** Permissioned memory for agent fleets exists as components, though not in tiered form. Ten companies for token cost is already available. Self-improvement is valuable and not unique; the gate is the differentiator. "Idea to IPO" has no supporting evidence. The Musk structure was not found.
- **Hypotheses.** H-A1 holds in part. H-A2 now has quoted prices behind it and is still untested on retention. H-A3 is partly falsified. H-A4 survives in a narrower form that now includes the second brain.
- **Customers.** Cole's own ventures come first. The first outside wedge is small local businesses with existing operations, sold as setup plus a monthly plan. Then multi-venture solopreneurs and funded startups. Large organizations are a long-term destination.
- **Recommendation for Gate G1a.** Route A in one shape: the product is the permission layer, orchestration is adopted for now behind a replaceable interface, and Cole's own ventures are the first pilots. Demand stays untested until an outside business pays.
- **Mission.** Cole's stated mission is a management company that takes ventures from idea to IPO on a constantly self-optimizing framework and also runs his personal life. This report records it as the direction to build toward. No evidence shows any system doing this today (T-4).
- **Limits.** Desk research plus code reading. Nobody was interviewed. Nothing was installed or run.

## Method and limits

| Step | What was done |
| --- | --- |
| Web | 39 searches on 2026-11-15 across two passes. Five pages fetched and read in full; every other web source was read as a search excerpt only. The ledger marks which is which. |
| Paperclip | Cloned `paperclipai/paperclip` at commit `da8cfda` (2026-11-15). Read the README, roadmap, product, deployment, installation, operator guides, skill policy, memory, plugin specification, MCP governance, the LLM Wiki plugin and the company schema. Not installed and not run. |
| AZI Hub | Cloned `CDM2/azi-hub` at `95d4feb` (2026-06-23). Read the architecture, state and decision documents, the tenancy map, the visibility policy and its migration, the research workers, the self-improvement schema and the tool list. Not run. |
| Polsia | Two hands-on reviews fetched and read, plus excerpts. Both reviewers sell competing or adjacent products. No account was opened. |
| Control planes | Microsoft Agent 365 and OpenAI Frontier assessed from documentation, press and analyst coverage. |
| Not done | Customer interviews. Hands-on trials of any product. Health-data connectors, authorization engines, durable execution and payment rails, which belong to R-02, R-04 and R-05. A separate review session to attack this report, which P-000 requires before acceptance. |

Many sources are vendors writing about competitors. The ledger grades each row; rows graded Low carry no conclusion on their own.

## 1. The category in November 2026

| Layer | Products | Entry price | Sold to | Evidence |
| --- | --- | --- | --- | --- |
| AI-run company builders | Polsia, NanoCorp, brainer.ceo, Cofounder | $20 to $120 a month; Polsia and NanoCorp also take 3% and 20% of revenue | Solo founders, mostly at the idea stage | E-12, E-14, E-16 |
| AI-employee bundles | Marblism, Lindy | $24 to $50 a month | Small businesses | E-17 |
| AI automation agencies | Thousands of small firms | $1,500 to $5,000 setup, then $500 to $1,500 a month | Small local businesses | E-72 |
| Org-chart orchestrator | Paperclip | Free; vendor cloud in invite-only beta | Technical operators and teams | E-01, E-10 |
| Hosted personal agents | Muse, ChatGPT dots, Claude Duet, Ari | Free to about $100 a month at entry, mostly bundled into plans people already pay for | Individuals, professionals, small-business owners | E-27, E-29, E-30, E-31 |
| Self-hosted personal agents | OpenClaw, Hermes Agent | Free, plus setup effort or a paid installer | Technical individuals; others through installers | E-32, E-33, E-34 |
| Agent memory layers | Cognee, Mem0, Zep, Letta, MintMCP | Not surveyed | Developers | E-67 |
| Enterprise control planes | Microsoft Agent 365, Google Gemini Enterprise, AWS AgentCore, OpenAI Frontier and Presence | $15 to $21 a seat, consumption, or custom contract | Technology leaders of large organizations, often through consultancies | E-18, E-20, E-21, E-22, E-23 |
| Agent runtime | Claude Agent SDK, Claude Managed Agents | Tokens; hosted adds $0.08 per session-hour | Developers | E-25, E-26 |

The 2x2 kept from the Gemini corpus (S-007), filled in:

| | One organization | Several organizations |
| --- | --- | --- |
| **New (greenfield)** | Polsia, brainer.ceo, Cofounder | NanoCorp and Paperclip: many companies, flat and isolated (E-03, E-14) |
| **Existing (brownfield)** | Agent 365, Gemini Enterprise, Frontier, Muse for Small Business, Duet, Marblism, Lindy, the agencies | Nothing found |

The empty cell is existing operations across several organizations. A personal layer above it is also unsold. **Judgment:** an empty cell shows nobody sells it; it does not show anybody wants it.

## 2. Teardowns

### Paperclip (source read)

**How a company runs on it.** It works like a ticket system for agents (E-48):

1. Install it and create a company with a goal.
2. Create a CEO agent: choose its tool (Claude Code, Codex and others), its instructions and a monthly budget.
3. The CEO proposes a strategy, which waits in the human's approval queue.
4. Once approved, it breaks the goal into tasks, assigns them to its reports, and may ask to hire more agents.
5. Agents wake in "heartbeats" on assignment, schedule or mention, take one task at a time, and post work for review.
6. The human watches a dashboard of blocked tasks, stale work and spend. Budgets warn at 80% and pause the agent at 100%.

| V-000 need | Paperclip | Evidence |
| --- | --- | --- |
| Agents in an org chart with roles, delegation, budgets | Yes | E-02, E-48 |
| Human approvals, audit trail | Yes; approval for new agents is off by default | E-02, E-08 |
| Several organizations, isolated | Yes | E-03 |
| Super-organization over sub-organizations | No. Companies are flat; no parent column or grouping table | E-03 |
| Sharing between organizations on purpose | No. Cross-company access stays denied; export and import move whole companies | E-02, E-03 |
| Personal layer | No | E-04 |
| Second brain | Part. An alpha LLM Wiki plugin with sources, linked pages, a maintainer agent and lint routines, scoped to one company. Memory connectors are experimental and off by default. | E-47, E-06 |
| Governed self-improvement | Part. Skills have tests, versions and restore; there is feedback voting and a built-in Learning agent; agents may change skills without approval by default; organizational learning is planned | E-05, E-06, E-49 |
| Model choice per agent | Yes, ten built-in adapters including Claude Code | E-07 |
| Custom UI | Yes. MIT-licensed, and plugins can add pages and sidebar entries | E-01, E-51 |
| Set up by a non-technical person | Not today. Vendor cloud is an invite-only beta; a reviewer notes the technical barrier | E-10, E-11 |

**How it makes money.** It does not yet, in public. Its creator said early in 2026 that it had no revenue (E-54). No paid tier is published and the cloud has a waitlist with no price (E-56, E-10). The code points to the plan: a "Community Edition" beside a "Paperclip EE" that owns the policy editor and policy audit views, a large body of Paperclip Cloud services, and ClipHub, a registry of downloadable company templates (E-53). **Judgment:** this is an open-core company heading for paid hosting and a paid enterprise edition. Governance features are where it intends to charge.

**How far it has got.** Nearly 70,000 GitHub stars by June 2026 (E-09). Named users include security firms, dentists, roofing companies and existing marketing firms (E-54). The public example of a whole company run on it reported revenue of $0, and one review says most teams run three to five agents on specific workflows (E-55, Low). **Judgment:** it has taken off as a tool people adopt. There is no public case of a company scaled on it.

**Risks in its own documents.** Telemetry is on by default, and budget stops act on recorded spend so a run can pass its limit (E-08). Its roadmap lists Self-Organization and Automatic Organizational Learning as planned (E-06). **Judgment:** those two items, a public cloud and the enterprise edition are the moves most likely to close the gap this project is aiming at.

### Polsia (two hands-on reviews read)

Polsia is the opposite design: hosted, and it acts without asking (E-61, E-62).

1. The user types an idea or clicks "surprise me".
2. In about ten minutes it writes a mission and a market research document and puts a site with an inbox on a polsia.app address.
3. A daily cycle reviews the company, checks channels, runs tasks and plans the next cycle.
4. The user gets a morning report and steers by chat. "God Mode" loops on one company for one hour to seven days.

One reviewer's test company posted on X and sent two emails before a card was entered. A user paying $199 a month got a site with fake customer reviews and journalists emailed without his knowledge, and ended with seven signups and no paying customers (E-62).

Its founder said in May 2026 that about 10% of companies had made a dollar, that first-month churn was about 50%, and that the best company earned $3,000 to $4,000. Of 484,592 companies created, 29,132 were active in September (E-63). It is built on the Claude Agent SDK with no model choice found, the code export is mostly a scaffold, and self-hosting is "coming soon" (E-64). Plans start at $20 a month and it takes 3% of customer payments (E-12).

**Judgment:** Polsia could be rebuilt, since it is a scheduled agent loop plus provisioning. Its buyers pay $20 and half leave in a month, so rebuilding it buys a poor market.

### AZI Hub v2.7 (prior code, read)

This is Cole's own repository, last shipped 2026-06-23. It is a single-user prototype, not a product. It matters here because it already contains the parts no vendor sells.

| What it has | How | Evidence |
| --- | --- | --- |
| Tiers: personal, a holding organization, three sub-organizations | A tenancy map with parents and two grants | E-57 |
| A second brain with permissions | One wiki table; each page carries a visibility list and tags; a database policy filters reads. A sub-organization sees global pages and its own, the holding organization sees every sub-organization, siblings see nothing of each other. | E-58 |
| Personal kept apart | Personal data reaches the holding organization only through a one-way briefing tool | E-58 |
| A gated improvement loop | Workers pull new papers, commits on named repositories and blog feeds; findings become proposals that pass through approval, with one allowed to be implementing at a time; A/B runs and prompt variants | E-59 |
| Organization spin-up | A deterministic `create_org` scaffold; short-lived agents whose work is synthesized into the wiki | E-60 |

What it lacks: any user identity, a tenant taken from a trusted source, spend limits, and generality. The sub-organization list is hard-coded (E-58, E-60). P-000 and INV-000 list the rest.

**Judgment:** the code shows one person can build the unsold combination. It does not show anyone else wants it, because it has had one user.

### Microsoft Agent 365 (documentation)

Agent 365 is governance, not a runtime. It gives each agent an identity in Microsoft Entra, lists every agent in the admin center, and applies access policy. Microsoft's own guide calls it metadata and governance only (E-19). It costs $15 per user a month on top of a qualifying Microsoft 365 licence (E-18). **Judgment:** it matters only to large organizations, where it sets the price of governance at $15 a seat.

### OpenAI Frontier (press and analyst coverage)

Frontier is sold, not downloaded. It has no public price and no self-serve signup; OpenAI attaches its own engineers and has multi-year alliances with Accenture, BCG, Capgemini and McKinsey to implement it (E-20, E-21). Its later Presence product is sold the same way (E-22). **Judgment:** this confirms that large organizations need help, and shows who already supplies it.

## 3. Hypothesis tests

### H-A1 — Buyers cannot set up current frameworks without help

**Verdict: holds in part. Not falsified.**

- **For.** A market of paid installers exists for OpenClaw, mostly at $99 to $499 one-time (E-34), and sellers claim owners spend 15 to 40 hours doing it themselves (E-37, Low). Paperclip's hosted version is not open to the public (E-10). Smaller organizations scaling agents stayed flat at 22% year on year while large ones rose to 40% (E-71). At the enterprise end, 17% of organizations have agents deployed, and OpenAI sells Frontier through its own engineers and four consultancies (E-24, E-20, E-21).
- **Against.** Hosted personal agents need no setup at all. Duet, Muse and dots are switched on inside a subscription (E-27, E-29, E-30). Polsia and NanoCorp create a company from a prompt (E-12, E-14). Some non-technical firms, dentists and roofers among them, already use Paperclip (E-54).
- **Falsifier check.** V-000's falsifier is a product that can be set up alone and covers the personal layer, an organization hierarchy and governed self-updating. None was found. Paperclip has the hierarchy half-built and no personal layer (E-03, E-04). Duet and Ari have the personal layer and no organization of agents (E-27, E-31).
- **Judgment.** "Cannot set up" is true of self-hosted frameworks and of enterprises. It is false for the hosted agents a small-business owner is most likely to try first. Help is needed for the combination, not for any single part.

### H-A2 — They will pay for onboarding and keep paying to stay

**Verdict: the price is supported by quotes. Retention is untested.**

- **For.** Agencies that automate small businesses quote $1,500 to $5,000 for setup and $500 to $1,500 a month, consistently across several 2026 guides (E-72). Installers list managed plans at $79 to $299 a month (E-35). Enterprises sign multi-year implementation alliances (E-21). Among US consumers who use agents, 92% pay for AI (E-39).
- **Against.** Quotes and guides are offers, not purchases (E-72, E-35). Bank data from December 2025 has 17.7% of small businesses having paid for any AI tool (E-71). Prices at the bottom are falling: installs from $29, a hosted Paperclip reseller closed, Polsia cut its revenue share from 20% to 3% (E-34, E-10, E-12). The big vendors bundle agents into plans people already hold (E-27, E-30). Polsia loses about half its users in the first month (E-63).
- **Judgment.** What small businesses are quoted for is one or two workflows that produce a visible result, such as answered calls or booked appointments. Nobody is quoted for "becoming an agentic organization". A paid pilot with an outside business would test this hypothesis with money, which is stronger evidence than an interview. Pilots on Cole's own ventures do not test it.

### H-A3 — What they would be onboarded to is not already sold turnkey

**Verdict: partly falsified.**

- **Each main job is already sold turnkey to each buyer.** Solo founders: Polsia, NanoCorp, brainer.ceo (E-12, E-14, E-16). Small businesses: Marblism, Lindy, Muse for Small Business, Duet and the agencies (E-17, E-27, E-30, E-72). Funded startups: Cofounder, or Paperclip run by their own engineers (E-16, E-01). Large organizations: the control planes and their consultancies (E-18 to E-23).
- **The combination is not sold.** Across five company builders, none mentions a personal layer, parent and child companies or sharing between companies (E-16). Paperclip confirms the same in code (E-03, E-04). Polsia has no approvals at all (E-62).
- **Judgment.** The category is taken. What remains is a set of features no vendor has put together: a holding structure with deliberate sharing, a personal space with a one-way boundary, a second brain that respects both, and improvement gated by evidence. Features are a weaker position than a category, and the nearest vendor has two of them on its roadmap and an enterprise edition in its code (E-06, E-53).

### H-A4 — Buyers want a personal layer whose chief of staff coordinates with organization administrators, and vendors do not offer it

**Verdict: falsified as written on the vendor half. A narrower claim stands. The buyer half is untested.**

- **Vendors now offer a personal layer.** Duet is built for professionals and small-business owners (E-27). Muse has a small-business version (E-30). Ari is sold as one chief of staff for work and life, with a privacy line, coordinating with colleagues' agents (E-31).
- **What no vendor offers.** A chief of staff that works with the agents of the owner's own organizations, across a holding organization and its sub-organizations, over a second brain filtered by tier. Hosted agents keep a small memory about one person, held in that person's account, not a governed catalog a business owns (E-65). Duet excludes Team and Enterprise plans at launch (E-28). Dots are one per person (E-29). Ari coordinates between people, not between an owner and their organizations' agents (E-31).
- **The second brain is not dead.** It changed form in 2026, from hand-tagged notes with retrieval to a wiki an agent maintains, with retrieval kept for very large or permissioned collections (E-66). AZI Hub's three-layer memory follows that pattern and adds the permissions (E-58).
- **Buyers.** Demand for personal agents is real: 41% of US AI users have tried one (E-39). Willingness drops for the data F-10 puts in scope: 20% of agent users have connected a financial account and 23% a health app (E-39); 15% in another survey would share financial information (E-41); 22% would allow no financial transactions (E-40).
- **Judgment.** For an owner-operator the person and the company are the same principal, so one system for both is natural. For an employee of a large organization it is a liability. H-A4 can only be true for owner-operators.

### Program-level falsifiers kept from the Gemini corpus (S-008)

| Falsifier | Reading on 2026-11-15 |
| --- | --- |
| Model providers and hyperscalers absorb orchestration and capability composition | Largely met for orchestration, governance and the personal agent (E-18, E-23, E-25, E-27). Not met for multi-organization structure or tiered memory. |
| Implementation cost exceeds the value created | Unknown. Low earnings on company builders are a warning (E-15, E-63). |
| No painful, budgeted customer problem | Untested. Quoted agency prices suggest small businesses budget for single workflows (E-72). |

## 4. Thesis claims raised in review

Six claims Cole made after v0.1, each tested against the evidence.

| ID | Claim | Verdict | Evidence and reasoning |
| --- | --- | --- | --- |
| T-1 | A large fabric of agents, each with memory permissioned by organization or task, is something nobody has built. | Partly true. | Scoped memory for agent fleets is sold as components: per-dataset permissions, user and agent scopes, group-based access, and private, team and organization scopes (E-67). What was not found is the tiered form: a person above a holding organization above sub-organizations, with upward flow by push only. Paperclip scopes everything to one company (E-47, E-50); hosted agents to one person (E-65). AZI Hub has the tiered form in prototype (E-57, E-58). On "large": a controlled study found more agents helped a parallel task by about 81% and hurt a sequential one by 39% to 70% (E-69). Agent count is a cost to justify per task, as N-04 already requires. |
| T-2 | Someone could create ten companies at once and pay only token costs. | Already available. | Paperclip runs any number of companies in one free, self-hosted deployment; its documents estimate $20 to $100 or more a month in model spend per active team (E-03, E-56). NanoCorp sells unlimited businesses for $30 a month (E-14). Polsia sells up to 50 (E-64). This is not a differentiator. |
| T-3 | Self-optimization, including scanning leading repositories and posts for improvements, is highly valuable. | Valuable, not unique. | It is an active research field with reported gains (E-70). Hermes writes and edits its own skills (E-33). Paperclip has skill tests, feedback and a Learning agent (E-05, E-49). AZI Hub's loop already scans papers, repositories and feeds into gated proposals (E-59). The scarce part is the control: one paper warns that a loop able to rewrite its own harness can tamper with its evaluation (E-70). The gate and an evaluation the loop cannot edit are the differentiator. N-05 stands. |
| T-4 | The system can take a company from idea to IPO, deciding whether to build or buy each tool. | No supporting evidence. | The best outcomes found are small: the best Polsia company its founder had seen earned $3,000 to $4,000 (E-63); the public Paperclip company reported $0 (E-55). No product was found that treats build-or-buy as an explicit, gated decision. **Judgment:** hold this as a direction, not a claim. Build-or-buy fits as one decision type in the research-to-decision workflow (C-13). Cole has since set this as the mission (section 11). It is recorded as founder intent, which the manifest treats as authoritative for direction and not as evidence about the market. |
| T-5 | Elon Musk runs about 50 agents as one, a chief of staff delegating to a CEO agent and sub-agents. | Not found. | The documented project is Macrohard: an AI software company in which Grok spawns hundreds of specialized agents, now a division meant to build agents that run businesses, with one report of stalled progress (E-68). It is a competitor signal, not validation. |
| T-6 | All of this could be done with hosted agents such as Muse, orchestrated with Paperclip. | Not as stated. | Duet, dots and Muse cannot be hired as workers in someone else's organization: they are one per person, on personal plans, with no organization features (E-27, E-28, E-29, E-65). Paperclip can hire self-hosted personal agents, Hermes and OpenClaw, through gateway adapters (E-52). The workable version is a self-hosted personal agent plus Paperclip. |

## 5. Capability map

Each capability V-000 asks for, the best existing tool found, and the glue nobody supplies. Coverage: **Full**, **Most**, **Part**, **None**. The last column names the report that settles the choice; R-01 only nominates.

| ID | Capability (V-000 reference) | Best existing tool | Coverage | Missing glue | Evidence | Settled in |
| --- | --- | --- | --- | --- | --- | --- |
| C-01 | Personal chief-of-staff agent that knows the person's life (F-01, section 1) | Claude Agent SDK agent on the VPS, or Hermes Agent joined to Paperclip through its gateway adapter. Claude Duet is the hosted reference. | Part | Duet is a closed preview with no self-hosting and no way to extend it. The SDK supplies the loop, not the knowledge of a life. OpenClaw is passed over on its 2026 security record. | E-26, E-27, E-32, E-33, E-52, E-65 | R-02 |
| C-02 | Personal second brain kept apart from each organization's (section 1, N-02) | Paperclip's LLM Wiki plugin for one organization's brain. Nothing for the personal brain or the boundary. | Part | The tiers and the filtered views. AZI Hub's visibility policy is the pattern. | E-04, E-06, E-25, E-31, E-47, E-58, E-65, E-66, E-67 | R-04 |
| C-03 | Super-organization and sub-organizations (F-02) | Paperclip, one company per organization | Part | A holding layer over flat companies: ownership, roll-up views, budgets under a parent. AZI Hub's tenancy map is the pattern. | E-03, E-50, E-57 | R-03 |
| C-04 | Explicit push from personal to organization; nothing between organizations by default (N-02) | None. Paperclip's isolation supplies "nothing by default". | None | A broker that shares one item on one approval and records it. AZI Hub's one-way briefing is the pattern. | E-03, E-50, E-57, E-58, E-67 | R-03, R-05 |
| C-05 | Agents in roles; single, group and chain conversations (D-05, INV-000) | Paperclip | Most | Group and ordered-chain chat were not found in its documents. AZI Hub has all three. Verify hands-on. | E-02, E-48, E-60 | R-03 |
| C-06 | Human approval for key decisions, production, money and other organizations' state (F-04, N-01) | Paperclip approvals and tool gateway; Agent SDK permissions and hooks beneath | Most | Defaults must be tightened to N-01. Production promotion stays in CI. | E-02, E-08, E-26, E-48, E-62 | R-05 |
| C-07 | Deterministic permissions, policy and state transitions (N-03) | Paperclip's company-scoped checks, approval stages and budget stops | Part | No general policy engine was evaluated. | E-02, E-03, E-08 | R-05 |
| C-08 | Self-improvement gated by verifiable metrics (F-05, N-05) | Paperclip Skill Studio with a company skill policy | Part | Promotion is not tied to a metric. Hermes edits its own skills with no governance; Managed Agents' equivalents are beta or preview. AZI Hub's research workers and proposal gate are the pattern. | E-05, E-06, E-25, E-33, E-49, E-59, E-70 | R-06 |
| C-09 | Agents build new personal sections on request (F-10, F-11, N-07) | Claude Code or the Agent SDK as builder; Paperclip plugins as a surface; read-only Plaid MCP servers for finance data | Part | A section scaffold, a schema per section, sensitivity labels. Health-data connectors not researched. | E-02, E-26, E-46 | R-02, R-04 |
| C-10 | Health and financial data stay in the personal tenant, out of logs and evaluation sets (N-08) | Self-hosted MCP servers that keep tokens on the machine | Part | Log redaction, evaluation-set exclusion, and a test that proves both. | E-39, E-41, E-46 | R-05, R-07 |
| C-11 | Money moves only with approval each time (N-01 applied to F-10) | Paperclip's tool gateway set to "ask first" for the approval. No self-hosted payment rail was researched. Duet's design is the reference: virtual card, approval each time, trades and transfers blocked. | Part | The payment rail and its approval record. AZI Hub's virtual-card tooling is prior art, not re-checked. | E-02, E-27, E-40, E-62 | R-05 |
| C-12 | Morning reservation-booking agent (F-08, F-15) | AZI Hub's own booking tools, left running on the VPS | Part | None for now. Cole states the agent books only on sites that allow agents, not Resy, and is not part of this build (section 11). For reference: no public booking API exists, and Resy has deactivated accounts that ran agents. | E-43, E-44, E-45 | Outside the build; revisit in Phase 5 |
| C-13 | Research-to-decision workflow (F-15) | This repository's own loop of manifest, ledger and gates; Paperclip planning mode with plan approvals as a possible host | Part | The ledger and the gate record as first-class objects. Build-or-buy as a decision type (T-4). | E-02 | R-03 |
| C-14 | Model choice per task, Claude-first (F-16) | Paperclip adapters | Most | Changing the model by asking the system was not found. | E-07, E-33, E-64 | R-02 |
| C-15 | Self-hosted on a VPS (F-17) | Paperclip, Agent SDK and Hermes all self-host | Full | None. | E-01, E-25, E-26, E-33, E-64 | R-02 |
| C-16 | Identity: a person, their personal space, memberships and roles (P-000) | Paperclip authenticated mode | Part | The personal space as a tenant in its own right. | E-02, E-04, E-19, E-60 | R-05 |
| C-17 | Audit and decision log (N-01, INV-000) | Paperclip activity log | Most | A decision log tied to gates. | E-02, E-05 | R-05 |
| C-18 | Spend limits per organization and agent (F-18) | Paperclip budgets | Most | Stops can lag and do not see flat subscriptions; add a second limit at the provider. | E-02, E-08, E-48, E-60 | R-02 |
| C-19 | Onboarding an existing organization (F-03, F-12) | None self-serve. Agencies do it by hand for small businesses; enterprises get vendor engineers and consultancies. | None | The import method. | E-06, E-20, E-21 | R-09 |
| C-20 | Creating a new organization (F-03) | Paperclip onboarding and team templates | Most | A sub-organization scaffold under the holding layer. AZI Hub's `create_org` is the pattern. | E-02, E-48, E-60, E-61 | R-03 |
| C-21 | Multi-agent design measured against a single-agent baseline (N-04) | None found | None | An evaluation harness that runs both designs on the same tasks. | E-05, E-69 | R-03, R-06 |
| C-22 | Multi-person collaboration, later (F-06) | Paperclip multiple human users; Ari for agent-to-agent between people | Part | Deferred by F-06. | E-02, E-31 | Phase 5 |

**What the map says.** Paperclip appears as the best existing tool, or part of it, in 16 of 22 rows. The three rows with no coverage are deliberate sharing, brownfield import and the baseline test. **Judgment:** the custom work is a personal tenant, a holding layer with a sharing broker, a tier-aware second brain, a metric-tied improvement gate and controls for sensitive data. Those are the AZI Hub items INV-000 marks "Pattern". The items it marks "likely replaced" are the ones an adopted control plane and runtime supply.

**One finding for the first slice.**

- **Budget (C-18, F-18).** Since 2026-06-15, Agent SDK use on a Claude subscription draws on a separate monthly credit (E-26). R-02 should confirm how that interacts with the Claude Max plan and the $1,000 cap.

The reservation agent is no longer a first-slice concern (section 11).

## 6. Three systems against the 22 capabilities

Each system rated alone: **Yes**, **Part** or **No**. AZI Hub's ratings describe a single-user prototype (E-57 to E-60, INV-000). Paperclip's rest on E-01 to E-08 and E-47 to E-52. Polsia's rest on E-12 and E-61 to E-64.

| ID | Capability | AZI Hub v2.7 (prototype) | Paperclip | Polsia |
| --- | --- | --- | --- | --- |
| C-01 | Personal chief of staff | Yes. An agent in a personal tier | No | No |
| C-02 | Personal second brain, kept apart | Yes. Personal vault, one-way briefings | No. Company wiki only, alpha | No. Per-company memory |
| C-03 | Super-organization over sub-organizations | Yes. Hard-coded list | Part. Many companies, flat | No. Up to 50, flat |
| C-04 | Sharing only on purpose | Yes. Visibility policy | Part. Isolated; no sharing path | No |
| C-05 | Agents in roles; chat modes | Yes. Single, group, chain | Yes. Org chart, delegation, chat | Part. Fixed agent set |
| C-06 | Human approval | Part. Proposal gates; no user identity | Yes. Strategy, plans, tool calls | No. Acts on its own |
| C-07 | Deterministic policy | Part. Row-level security; tenant from a client header | Part. Access checks, budget stops | No |
| C-08 | Gated self-improvement | Yes. Research workers, proposals, A/B runs; small evaluation sets | Part. Tests and versions; no gate | Part. Saves skills; no gate |
| C-09 | Agents build new sections | Part. Delegates code changes to Claude Code | Part. Plugins plus coding agents | No |
| C-10 | Health and finance data stay personal | No | No | No |
| C-11 | Money only with approval | Part. Role-gated card and wallet tools | Part. "Ask first" on tools | No. Runs ads itself |
| C-12 | Reservation agent | Yes. Still running | No | No |
| C-13 | Research-to-decision | Part. Decision log, research staging | Part. Plan approvals | Part. Research document; no gate |
| C-14 | Model choice | Part. Tier by role; names hard-coded | Yes | No |
| C-15 | Self-hosted | Yes | Yes | No |
| C-16 | Identity | No | Part. Users and roles; no personal space | No |
| C-17 | Audit log | Part. Decision files and traces | Yes | Part. Dashboard and public feed |
| C-18 | Spend limits | No | Yes. Can lag | Part. Task credits |
| C-19 | Onboard an existing organization | No | No | No |
| C-20 | Create a new organization | Yes. `create_org` | Yes | Yes. Its core feature |
| C-21 | Single-agent baseline test | No | No | No |
| C-22 | Multi-person | No | Part. Multiple users | No |
| | **Totals (Yes / Part / No)** | **9 / 7 / 6** | **7 / 9 / 6** | **1 / 5 / 16** |

**Judgment:** AZI Hub and Paperclip are complementary. AZI Hub's "Yes" rows (C-01 to C-04, C-08, C-12) are where Paperclip is weakest, and Paperclip's (C-06, C-14, C-17, C-18) are where AZI Hub is weakest. Neither covers C-10, C-19 or C-21. That pattern argues for combining them, not for replacing one with the other.

## 7. Build on, fork, or own

Cole's concern is that folding Paperclip into this project, or this project into Paperclip, would be hard to do and hard to maintain. The code supports that concern and points to a different arrangement.

| Option | What it means | Assessment |
| --- | --- | --- |
| A. Copy parts of Paperclip into a new codebase | MIT allows it | The useful parts assume company scoping, which runs through 169 of 189 schema files (E-50). Copied code stops receiving upstream fixes. **No**, beyond small utilities. |
| B. Fork Paperclip and add tiers inside it | Change its data model and authorization | The tiers cut through a 3,172-line authorization service that upstream changes constantly (E-50, E-01). A permanent merge burden on the security core. **No.** |
| C. Build everything as a Paperclip plugin | Plugins may own tables, register agent tools and add pages (E-51); the LLM Wiki plugin shows the shape (E-47) | The specification calls the plugin runtime early, says plugin UI is trusted code, and says companies are not plugin trust boundaries (E-51). The project's security boundary would live inside someone else's unfinished runtime. **Use for UI only.** |
| D. Compose: own permission service, unmodified Paperclip, a personal agent | See below | **Recommended to spike first.** |
| E. Own orchestrator | Rebuild AZI Hub's runtime on the new identity model | One system and full control, at the cost of rebuilding everything in E-02 and E-48. INV-000 already marks the agent loop and sandbox "likely replaced". **Fallback if D fails.** |

**Option D in detail.**

- **The permission service** is this project's own code and database. It holds identity, the tier map, the tier-filtered second brain, the sharing broker and the improvement loop. Its boundary is enforced by its own database policy, as AZI Hub's is (E-58).
- **Agents reach it over MCP.** Paperclip already governs connections to a company's own MCP server with policies, approvals and an audit log (E-52). Each organization is a Paperclip company holding a token scoped to that organization's tier.
- **Paperclip stays unmodified** and upgradable. It supplies the org chart, heartbeats, budgets, approvals and adapters (E-02, E-48).
- **The chief of staff** is a Hermes or Agent SDK agent joined through a gateway adapter (E-52, E-33, E-26).
- **A thin plugin** may add a holding view to Paperclip's interface and forward events to the permission service (E-51).

For: the differentiating code is owned outright; the orchestrator can be replaced if Paperclip adds tiers, changes its licence terms or charges for governance (E-53); the same MCP server could later serve other harnesses. Against: two systems to run; Paperclip's own task history stays company-scoped inside Paperclip unless forwarded; none of it is proven until spiked.

**On beating Paperclip.** **Judgment:** not at orchestration, and there is no need. Section 6 shows the two systems cover different rows.

**Proposed pass criteria for the R-02 spike.**

1. A sub-organization's agent, running in Paperclip, queries the permission service and receives its own and global pages only. A sibling's page is never returned.
2. The holding organization's agent reads sub-organization summaries.
3. The only path from personal to an organization is an explicit push.
4. Every call appears in Paperclip's audit log and in the service's own.
5. One real Toveli task runs through this stack, and the same task runs on a single agent as the N-04 baseline.
6. Paperclip is upgraded one release without touching the permission service.

If criteria 1 to 4 cannot be met, fall back to option E.

**What replicating Paperclip would take.** Cole asked whether this project could build the same tool, or a better one, and keep it maintained. By my count Paperclip holds about 1.5 million lines of TypeScript outside its tests, in about 5,600 files, with 486 database migrations and 12 adapter packages (E-73). AZI Hub holds about 29,400 lines (E-74). **Judgment:** the same tool, kept current, is not a realistic project for one person with agents, and rebuilding what is free returns nothing. A lean orchestrator sized to Cole's own ventures is realistic, since AZI Hub's server was about 13,500 lines. That is option E, and option D does not close it off.

**If Paperclip stops being maintained.** Its licence is MIT, so an installed version keeps working and can be pinned (E-01). Because the permission service is separate, the orchestrator beneath it can be replaced by option E without touching the differentiating code. This follows the rule in AZI Hub's own architecture document: keep interfaces stable and let implementations change.

**Triggers for moving to option E.**

1. The spike fails criteria 1 to 4.
2. Paperclip is abandoned or its licence changes.
3. A governance feature this project needs ships only in Paperclip's paid edition (E-53).
4. Upgrades break the integration repeatedly (criterion 6).
5. The product is offered to outside customers and resting on Paperclip weakens the offer. Decide this at Gate G1.

**Governance and hosting.** Cole notes he would add governance features and could offer hosting. For his own ventures under option D, Paperclip's approvals, budgets and audit log cover each organization (E-02, E-48). This project builds governance only for what it owns: approvals on sharing and the improvement gate. Broader governance and a hosted offering are what Paperclip intends to charge for (E-53). They belong to Gate G1, together with trigger 5.

**Founder position, 2026-11-15.** Cole is comfortable adopting Paperclip for now and wants building an own orchestrator kept open (section 11).

## 8. Customer groups, ranked

| | Non-technical owners of existing small businesses (F-13, narrowed) | New, well-funded organizations | Existing large organizations |
| --- | --- | --- | --- |
| Size signal | 32.0M US businesses with no employees in 2024; 24.6% of employer businesses use AI in some function (E-42, E-71) | Not measured | Not measured |
| Do they need help (H-A1)? | Yes. Smaller organizations scaling agents are flat at 22% (E-71) | Least. They have engineers and self-serve tools (E-01, E-16) | Most (E-24) |
| Who already serves them | Agencies, Marblism, Muse for Small Business, Duet (E-72, E-17, E-27, E-30) | Cofounder, Paperclip, the runtimes (E-16, E-01, E-26) | Microsoft, Google, AWS, OpenAI, with the four largest consultancies (E-18 to E-23) |
| Price points seen | $1,500 to $5,000 setup, $500 to $1,500 a month from agencies; free to $50 a month for tools (E-72, E-17, E-30) | About $100 to $125 a seat a month (E-16, E-29) | $15 to $21 a seat for governance; custom contracts above (E-18, E-20, E-23) |
| Does the personal layer fit? | Yes: owner and business are one principal | Weakly: employees, not owners | No: employers and employees want a wall (E-31) |
| Can one founder reach and serve them? | Yes, in person. Cole reports knowing many such businesses in New York. | Yes | No |
| **Rank** | **1** | **2** | **3, as a long-term destination** |

**Before any outside customer.** Cole will pilot on his own ventures first: Toveli and others (section 11). That tests whether the system works across several organizations under one owner. It does not test whether anyone else will pay.

**First outside wedge.** Small local businesses with existing operations, onboarded in person and sold as setup plus a monthly plan. This matches F-12, matches the agency price points (E-72), and uses a channel Cole already has. It resolves the tension in D-10.

**What a first sale looks like.** **Judgment:** one or two workflows with a visible result, because that is what small businesses are quoted for today (E-72). A full conversion into an agentic organization is where an account grows to, not where it starts.

**What would make this more than another agency.** **Judgment:** the same platform run across every client, with each client's knowledge kept in its own tier, and improvements found for one offered to all through the gated loop. Agencies today sell separate workflows on shared tools (E-72).

**Costs of this wedge.** It sells founder hours first. Cole reports 40 to 60 hours a week available (section 11). These buyers cannot self-host, so each needs a managed instance, which F-17 leaves to Gate G1a. Free tools from Meta and Anthropic target the same owners (E-27, E-30).

**Later groups.** Solopreneurs running several ventures are the same product without the in-person sale. Large organizations become reachable when existing systems can be attached through custom MCP connectors; today that market belongs to the control planes and their consultancies (E-18 to E-23).

This ranking is a desk judgment. P-000 leaves the naming of one wedge to R-01 and R-08 together.

## 9. Route recommendation for Gate G1a

Cole decides. R-02 has not run yet and also feeds the gate.

**Recommend: Route A, in this shape.**

1. **The product is the permission layer.** Tiers, the tier-aware second brain, the sharing broker, the personal layer and the gated improvement loop. This is what AZI Hub prototyped and what nobody sells in this form.
2. **Orchestration is adopted.** Paperclip unmodified, composed as in option D, with option E as the fallback.
3. **Cole is the first user.** The first slice becomes the personal layer and his own ventures, with the reservation agent left outside the build. Section 10 proposes the matching amendment to F-15.
4. **Cole's own ventures are the first pilots.** Toveli and others run as sub-organizations under a management company, with the personal layer beside it. This is Cole's decision of 2026-11-15.
5. **Demand is tested with money afterwards.** Two or three local businesses as paid pilots at market rates, on the same stack. Until one pays, H-A2 stays untested and Route A stays a hypothesis.
6. **Held until Gate G1.** Licensing, public self-serve signup, a hosted offering, broader governance, enterprise features and multi-user collaboration.

**What this builds toward.** Cole's mission is a management company that creates and scales his ventures from idea to IPO on a constantly self-optimizing framework, and that also manages his personal life. The shape above maps onto it directly: the management company is the holding organization, each venture is a sub-organization, the personal layer sits beside them, and the improvement loop runs at the holding level so a gain found in one venture can be offered to all. Three things the mission needs are not designed yet: stage gates from idea to scale, build-or-buy as a gated decision, and connections to systems of record. They belong to R-03 and the specification. **Judgment:** this is the right thing to aim at and an unproven thing to claim; section 4 found no system that does it today.

**What moved since v0.1.** The second pass gives more support to Route A than v0.1 did, for two reasons: the differentiating parts already exist in Cole's own code, and small businesses are quoted real prices for onboarding. It gives no support to competing with Paperclip, to "idea to IPO" as a claim, or to agent count as a selling point.

**Fall back to Route B if any of these happens:**

- The spike fails criteria 1 to 4 and option E does not fit the budget.
- When outside pilots are tried, no local business agrees to pay.
- Paperclip ships tiers and a public cloud. The permission layer would then be worth building for Cole's own use only.
- Duet, dots or Muse add several organizations under one owner.

**Main risks.**

- The product's fit rests on one user so far. Pilots on Cole's own ventures can show the system works and still say nothing about demand.
- A service wedge consumes founder hours.
- Paperclip Labs has organizational learning on its roadmap and an enterprise edition in its code (E-06, E-53).
- The largest labs give small-business agents away (E-27, E-30).
- More agents can make results worse (E-69).

## 10. Proposed follow-ups

None of these is made by this report. Each needs Cole's acceptance.

| Where | Proposed change |
| --- | --- |
| V-000 sections 1 and 2 | Add the mission as Cole stated it. Amend F-08 and F-15: the reservation agent stays on the VPS outside the build, and the first slice becomes the personal layer, then Cole's ventures under a management company, then the research-to-decision workflow. Record three decisions: orchestration is adopted for now behind a replaceable interface; Cole's own ventures are the first pilots; 40 to 60 hours a week are available. |
| V-000 section 5 | Restate H-A4 as the narrower claim in section 3, including the second brain. Restate H-A3 as "the combination is not sold turnkey". Replace the counter-signals paragraph with Duet, dots, Muse and Ari. |
| V-000 D-10 | Record the ranking and the first wedge: small local businesses with existing operations. |
| P-000 landscape table | Add rows for hosted personal agents, agent memory layers and automation agencies. |
| R-02 scope | Spike option D against the six pass criteria in section 7, with a Toveli task as the test job and option E as the fallback. Install Paperclip in a throwaway environment, since R-01 did not run it. |
| R-04 | Generalize AZI Hub's visibility model from a hard-coded list to the tier map. Decide wiki, retrieval or both by collection size (E-66). |
| R-06 | Keep the evaluation outside what the improvement loop can edit (E-70). |
| R-08 | After the own-venture pilots, two or three paid local pilots, plus interviews where a pilot is declined. |
| INV-000 | Mark the reservation-booking row as outside the build. Add Paperclip's LLM Wiki plugin to the memory comparison. |

## 11. Founder answers, 2026-11-15

Cole answered the four questions v0.2 asked. These are founder input (S-001): authoritative for intent, not evidence about the market.

| Question in v0.2 | Cole's answer | Effect on this report |
| --- | --- | --- |
| Does the reservation agent compete for tables at release time? | It runs only on sites that allow agents, not Resy. It is not part of this build and only uses the VPS for now. | C-12 is outside the build. The first-slice warning is withdrawn. A proposed amendment to F-08 and F-15 is in section 10. |
| May R-02 spike option D, with option E as the fallback? | Comfortable adopting Paperclip for now if the research supports it. Wants to know whether the same tool, or a better one, could be built and maintained instead. | Section 7 now gives the size of that job, what happens if Paperclip is abandoned, and five triggers for moving to option E. |
| Which local businesses could be first paid pilots? | He will pilot on his own ideas first: Toveli and a few others. | Sections 8 and 9: own ventures are the first pilots. Outside paid pilots follow. H-A2 stays untested until then. |
| How many hours a week can go to pilots? | 40 to 60. | Section 8. |

**Mission, in Cole's words (paraphrased).** Build toward idea to IPO on a constantly self-optimizing framework. The next Alphabet should be creatable with this tool: a management company that scales Toveli and his other ideas, and that also manages his personal life.

**On governance and hosting.** Cole expects to add governance features and could offer hosting. Section 7 places both at Gate G1.

## 12. Open for Gate G1a

1. R-02 has to run the spike. This report nominates option D; it has not shown that it works.
2. Whether a separate review session should attack this report before or after acceptance.

## Sources

All external claims are in [`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md), rows E-01 to E-74, with links, how each source was read and a confidence grade. Findings about AZI Hub also draw on INV-000 and P-000.
