# REV-01 brief: attack R-01 and R-02

Written 2026-11-17 for a fresh session. You did not write these reports. Your job is to break them, not to improve their wording.

Cole decided Gate G1a on 2026-11-16: Route B, with three rules that keep Route A open (V-000 F-29, F-30). This review decides whether option D can be confirmed and whether anything found should reopen the route decision.

## Where things are

- Repository: `CDM2/azi-hub-v2`.
- Pull request #4, branch `research/r-02-runtime-and-harness`: the R-02 report, ledger rows E-75 to E-113, spike code and raw results under `spikes/r-02/`.
- Pull request #5, branch `docs/gate-g1a-route-b`, stacked on #4: V-000 v0.4 (Gate G1a), P-000's notes of 2026-11-17, and this brief.
- **Which branch to work from.** Check the state of #4 and #5 first. If both are merged, work from `main`. If either is still open, work from `docs/gate-g1a-route-b`, which contains both. Open your own branch from that point and target your pull request at the same place.

## Read first, in this order

1. `docs/source/SOURCE_MANIFEST.md`
2. `docs/source/V-000_VISION_BASELINE_AND_DRIFT_AUDIT.md` (decisions F-xx, rules N-01 to N-08)
3. `docs/source/P-000_RESTART_FINDINGS_AND_PLAN.md` (phases, gates, Route A and B, the notes of 2026-11-17)
4. `docs/research/R-01_CATEGORY_AND_EXISTING_TOOLS.md`
5. `docs/research/R-02_RUNTIME_AND_HARNESS.md`
6. `docs/research/EVIDENCE_LEDGER.md`
7. `spikes/r-02/service/CONTRACT.md`, `schema.sql`, `server.mjs`, `tests/`, and `results/README.md`

## What to attack, in this order

1. **The permission service (R-02 criteria 1 to 3).** Try to read a sibling organization's page, a personal page, or a health or finance page by any route: the six MCP tools, crafted arguments, search snippets, error and timing differences, the admin routes, the session binding in the database, the definer functions and their search path, token handling. Write new tests under `spikes/r-02/review/` and run them against the service with a local PostgreSQL. Report every leak with the exact call that produced it. Also say what the 35 existing tests do not cover.
2. **Criterion 4.** R-02 calls it "pass, with two limits". Argue whether the request that Paperclip did not log makes it a fail. Check the matching logic in `spikes/r-02/paperclip/harness.py` against the raw result files.
3. **Criterion 7 and trigger 3.** Check each row of the governance table against `results/scratch/*/governance-*/governance.json`. Flag anything stated more strongly than the evidence.
4. **Criterion 8.** Check the 20 questions in `spikes/r-02/qa/questions.json` and the grader for bias toward either the map or the plain agent. Say whether a larger repository or harder questions would plausibly change the result. Do not re-run the model.
5. **The E-26 correction and the budget section.** Re-derive from the sources behind E-75 and E-76.
6. **Alternatives R-01 did not compare head to head.** Desk research only, and light: the deep comparison waits until the tool runs (P-000, notes of 2026-11-17). Put three code-first orchestration frameworks (LangGraph, CrewAI, Microsoft Agent Framework) and the products sold as an "agentic mesh" or "agent fabric" against R-01's capability map (section 5) and R-02's criteria. State whether any of them obviously beats option D, and argue the best case for option E. At most 15 new ledger rows.
7. **R-01.** Attack its hypothesis verdicts and its customer ranking. Re-check ten ledger rows of your choosing against their sources.
8. **The Gate G1a memo (R-02 section 10) and the decision.** Is the framing of Route A and Route B fair? Does anything argue against Route B with the three rules in V-000 F-29?
9. **A second person (V-000 F-31).** Cole wants to run one sub-organization with another person who must never reach his personal space, his other sub-organizations or the holding organization's pages. The spike was built for one person. Known so far: the service has no person with memberships, only a token bound to one organization (`schema.sql` lines 40 to 44); any personal-kind organization reads every organization (line 154); human approval is one admin token; Paperclip ran in its owner-only mode with no logins; all agents share one operating-system user (E-111). Using the service only, show what a human token of one sub-organization can and cannot read, and what breaks when a second personal space exists. Do not run Paperclip. Then attack the seven pass criteria of the shared-venture spike in P-000's note on R-03: what do they miss?

## Constraints

- Do not modify: `R-01`, `R-02`, V-000, P-000, INV-000, existing ledger rows, this brief, anything under `spikes/r-02/` except a new `spikes/r-02/review/` directory, `CDM2/azi-hub`, `CDM2/toveli`, or Paperclip's source.
- Append only. New ledger rows start at E-114 and carry their date. Findings go in one new file: `docs/reviews/REV-01_R-01_AND_R-02.md`. Add a row for it to the manifest's table of canonical artifacts.
- Do not run Paperclip or any other third-party code in your sandbox. Running this project's own service and tests is fine. Synthetic data only.
- `CDM2/toveli` is read-only and you should not need it.
- No secrets in the repository. Model spend cap: $0. Ask Cole before any model call.
- Permissions are enforced by deterministic code in the database or service, never by a prompt (N-03). A fix that relies on a prompt is not a fix.
- Manifest rules apply, including N-06.
- A check you could not run is "not checked", not a pass.
- GitHub: if `gh pr` commands fail, use `gh api` (REST).

## Output: `docs/reviews/REV-01_R-01_AND_R-02.md`

1. Verdict in five lines: does option D stand, does each criterion stand, does anything reopen the Route B decision.
2. Findings, most severe first. Each one: blocker, should fix, or note; the evidence; the exact reproduction; the smallest fix.
3. Per criterion 1 to 8: stands, stands with changes, or does not stand.
4. The alternatives table from item 6.
5. The second-person findings from item 9.
6. What you could not check, and why.

Open a pull request with that file, any tests and any ledger rows.

## When you finish, send Cole

- The pull request link.
- The five most important findings.
- Whether option D can be confirmed, and what must be fixed first if not.
- Whether anything reopens Route B.
- Decisions you need from him.

Keep chat replies short and answer-first. He is on mobile.
