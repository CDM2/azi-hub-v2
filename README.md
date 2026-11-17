# azi-hub-v2

Restart of the AZI Hub agentic operating system. This repository starts with documents, not code.

Start here:

1. `docs/source/SOURCE_MANIFEST.md` — what each source is and how much authority it has.
2. `docs/source/P-000_RESTART_FINDINGS_AND_PLAN.md` — findings on the prior code and research, and the phased plan.
3. `docs/source/V-000_VISION_BASELINE_AND_DRIFT_AUDIT.md` — founder decisions, drift audit and open questions (v0.2 accepted at Gate G0; v0.3 proposed).
4. `docs/source/INV-000_CAPABILITY_INVENTORY.md` — what carries over from `azi-hub` and `autonomous-startup-engine`.
5. `docs/research/R-01_CATEGORY_AND_EXISTING_TOOLS.md` — route check: hypothesis tests, existing-tool map and customer ranking (v1.0, accepted), with its sources in `docs/research/EVIDENCE_LEDGER.md`.
6. `docs/research/R-02_RUNTIME_AND_HARNESS.md` — runtime, durable execution, sandboxing, model choice and budget; the spike of R-01 option D with a pass, fail or not run table; and the Gate G1a memo (v1.0, proposed). Spike code and raw results are in `spikes/r-02/`.
7. `docs/reviews/REV-01_BRIEF.md` — the brief for a separate session that attacks R-01 and R-02.

Status, 2026-11-15: Phase 1a, the route check.

- Gate G0 passed on 2026-11-15: pull request #1 was merged at 2baba1b, which accepted V-000 v0.2.
- R-01 v1.0 was accepted the same day: pull request #2 was merged at 546715c.
- V-000 v0.3 is proposed. It is accepted when its pull request is merged.
- R-02, the runtime report and spike, is in progress. Gate G1a, the choice between Route A and Route B, follows R-02 and is the founder's decision.
- Update, 2026-11-16: R-02 v1.0 is proposed in its pull request, stacked on the one that carries V-000 v0.3. Neither R-01 nor R-02 has been attacked in a separate review session. Gate G1a is open.
- Update, 2026-11-17: V-000 v0.3 was accepted when pull request #3 was merged at 4a31bf2. Gate G1a is decided: Route B, with three rules that keep Route A open (V-000 F-29 and F-30, proposed as v0.4 in a pull request stacked on the one that carries R-02). Next: the review in `docs/reviews/REV-01_BRIEF.md`, then Phase 1b.

Earlier status line, kept for the record: "Phase 0. Nothing here is accepted until the founder accepts V-000 (Gate G0)."
