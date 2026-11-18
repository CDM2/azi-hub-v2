# Source manifest — azi-hub-v2

Manifest v1.5, 2026-11-18. This file says what each source is and how much authority it has. It is metadata, not evidence.

v1.1 amends v1 of the same day, on the founder's instruction in the R-02 brief: the status cells of the canonical artifacts are brought up to date with the two merges, and S-015 is added. S-016 was added later the same day.

v1.2 (2026-11-16) is proposed in the pull request that carries R-02: sources S-017 to S-020, an R-02 row, and the ledger's new version and row count.

v1.3 (2026-11-17) is proposed in the pull request that records Gate G1a: source S-021, the status cells for V-000, P-000 and INV-000 brought up to date with the merge of pull request #3, and a row for the review brief.

v1.4 (2026-11-17) is proposed in the pull request that carries the review REV-01: source S-022, a row for the review, and the ledger's new version and row count. No other cell is changed. The cells for R-01 and R-02 still say neither has been attacked in a separate review session; the REV-01 row below supersedes that wording, and the cells are left for Cole to update when he rules on the review.

v1.5 (2026-11-18) is proposed in the pull request that carries the fix pass: source S-023, the V-000 cell brought to v0.5, a row for the fix-pass report, and the ledger's new version and row count. No other cell is changed.

## Source classes

- **Founder input.** Stated by Cole. Authoritative for intent; not evidence about the market.
- **Prior implementation.** Code that ran. Evidence of what was built, not a specification.
- **Model-synthesized artifact.** Written by an AI from other inputs. Useful structure; every claim in it is unverified until checked.
- **Research evidence.** Externally sourced facts with a claim-level citation and an as-of date.
- **Process template.** Shows how to run the work; says nothing about this product.
- **Canonical project artifact.** The current accepted synthesis. Not proof that its claims are true.

## Inputs

| ID | Source | Class | Treatment |
| --- | --- | --- | --- |
| S-001 | Founder note and chat replies, 2026-11-15 | Founder input | Highest authority for intent. Recorded in V-000 section 2. |
| S-002 | `prior-art/AZI-HUB-PROJECT-BRIEF.md` | Model-synthesized artifact | Describes AZI Hub from its docs. Check implementation claims against code. |
| S-003 | `prior-art/CAT_Research_to_Product_Plan.md` (2026-08-18) | Model-synthesized artifact | Methodology. Its exclusion of the personal layer is overridden by F-01. |
| S-004 | `CDM2/azi-hub`, main at 95d4feb | Prior implementation | Reference only. Not copied into this repository. |
| S-005 | `CDM2/autonomous-startup-engine` at 159c1b1 | Prior implementation | Reference only. Cole's to use (F-09). |
| S-006 | `prior-art/gemini/00_FOUNDER_CORPUS_MAP_v1.md` | Model-synthesized artifact | Keep the lineage and contradictions. |
| S-007 | `prior-art/gemini/01_CORPUS_BLIND_SPOT_AUDIT_v1.md` | Model-synthesized artifact | Source of the 2x2. Its competitor list is stale. |
| S-008 | `prior-art/gemini/02_RESEARCH_PROBLEM_v2.md` | Model-synthesized artifact | Keep the falsification criteria. |
| S-009 | `prior-art/gemini/03_RESEARCH_TAXONOMY_v2.md` and `_v3.md` | Model-synthesized artifact | Checklist only. Superseded as a work plan by R-01 to R-09. |
| S-010 | `prior-art/gemini/SOURCE_MANIFEST_v1.md`, `_v2.md` | Model-synthesized artifact | History. |
| S-011 | `prior-art/gemini/CAT_HANDOFF_DOSSIER.md` | Model-synthesized artifact | Not a faithful summary. Use S-006 to S-009 where they differ. |
| S-012 | `CDM2/toveli` ENG-001, A-001, A-002, repository controls | Process template | Structure borrowed. No product content carried over. |
| S-013 | `paperclipai/paperclip` at da8cfda (2026-11-15), MIT | Research evidence | Read as source for R-01. Not installed, not run, not copied into this repository. |
| S-014 | External web sources gathered 2026-11-15 for R-01 | Research evidence | Recorded claim by claim in `../research/EVIDENCE_LEDGER.md`, each row with how it was read and a confidence grade. Rows E-01 to E-08, E-47 to E-53 and E-73 are S-013; rows E-57 to E-60 and E-74 are S-004. |
| S-015 | Founder inputs after the R-01 merge and the brief for R-02, 2026-11-15 (chat) | Founder input | Same authority as S-001. Governance in this version and the codebase map. Recorded in V-000 section 2a as F-23 and F-24. |
| S-016 | Founder answers to the R-02 spike plan, 2026-11-15 (chat, two messages) | Founder input | Same authority as S-001. The personal-to-organization rule and its off switch, the optional personal space, what the holding organization reads, and how governance is priced. Recorded in V-000 section 2a as F-25 to F-28. Also: the Toveli repository is read-only for this project, and the spike's third-party code runs on a scratch repository. |
| S-017 | `paperclipai/paperclip` at release tags `v2026.1023.0` (`1b4c803816e82b0265c8422e1a804327a7ed8c54`) and `v2026.1106.0` (`d69631b01b9c658f80bf8bed389863dce82643e1`), MIT; and the npm package `paperclipai` at `2026.1023.0` and `2026.1106.0` | Research evidence | Source read for R-02. The npm package was installed and run unmodified, only on the scratch machine (S-019), on made-up data. Not copied into this repository and not patched. Ledger rows E-87 to E-93 and E-100 to E-113. |
| S-018 | `CDM2/toveli` at `0abafdc` (and `525054d` for the update test), as an input to the R-02 spike | Prior implementation | Read only, in the session's sandbox, by this project's own code. Nothing was written to it. No Toveli source, map page or transcript is in this repository; `spikes/r-02/qa/questions.json` and two result files hold short facts about it (counts, names of packages and scripts, one-line answers). This is separate from S-012, which borrowed Toveli's process documents. |
| S-019 | `CDM2/Spike-test`, a private scratch repository, and its GitHub-hosted runner, 2026-11-16 | Process template | The throwaway machine for third-party code. Holds a copy of the spike's own code and the raw results on a `results` branch. To be deleted after the pull request carrying R-02 is merged; the results that matter are copied to `spikes/r-02/results/`. |
| S-020 | External web sources gathered 2026-11-15 for R-02 | Research evidence | Ledger rows E-75 to E-86 and E-94 to E-99, each with how it was read and a confidence grade. Row E-85 is S-004. |
| S-021 | Founder replies to R-02, 2026-11-16 and 2026-11-17 (chat) | Founder input | Same authority as S-001. Gate G1a (Route B with three rules), Route A later, the second-person rule, acceptance of P-000, the ruling on R-02 criterion 4, the wider R-04, and agreement to the shared-venture spike. Recorded in V-000 section 2a as F-29 to F-31 and in P-000's notes of 2026-11-17. |
| S-022 | Sources gathered on 2026-11-17 for the review REV-01: `paperclipai/paperclip` read at tag `v2026.1106.0` and at `da8cfda`, not installed or run; external web sources; the R-02 spike's saved results, read again; and the review's own tests against the unmodified permission service | Research evidence | Ledger rows E-114 to E-127, each with how it was read and a confidence grade. The tests and their raw output are under `spikes/r-02/review/`. Made-up data only. |
| S-023 | Founder replies to the review REV-01, 2026-11-17 (chat, two messages). With them, an outside conversation of the same day as Cole relayed it, and the session's own tests of the fixed permission service on 2026-11-18 | Founder input; the conversation and the tests are research evidence | The replies have the same authority as S-001 and are recorded in V-000 section 2a as F-32 to F-40. The conversation is ledger row E-128, graded low; Cole's notes and a transcript of it were read by the session and are not in the repository, because they hold a third party's and his employer's information (N-06). The tests are ledger rows E-129 to E-132, with raw output under `spikes/rev-01-fix/results/`. Made-up data only. |

## Canonical artifacts

| ID | File | Version | Status |
| --- | --- | --- | --- |
| P-000 | `P-000_RESTART_FINDINGS_AND_PLAN.md` | 2026-11-15, amended 2026-11-15 and 2026-11-17 | The plan in use. Merged with pull request #1 (2baba1b); the amendments of 2026-11-15 merged with pull request #3 (4a31bf2). Accepted by Cole in chat on 2026-11-16; that acceptance and the notes of 2026-11-17 are proposed in the pull request that records Gate G1a. |
| V-000 | `V-000_VISION_BASELINE_AND_DRIFT_AUDIT.md` | 0.5 | v0.2 accepted at Gate G0: pull request #1 merged on 2026-11-15 (2baba1b). v0.3 accepted: pull request #3 merged on 2026-11-17 (4a31bf2). v0.4 proposed, recording Gate G1a (Route B); accepted when its pull request is merged. v0.5 proposed, recording Cole's decisions after the review REV-01 (F-32 to F-40); accepted when its pull request is merged. |
| INV-000 | `INV-000_CAPABILITY_INVENTORY.md` | 0.3 | Draft. v0.3 appends two amendments from R-01 section 10 and three rows for capability C-23; merged with pull request #3 (4a31bf2). |
| R-01 | `../research/R-01_CATEGORY_AND_EXISTING_TOOLS.md` | 1.0, 2026-11-15 | Accepted: pull request #2 squash-merged on 2026-11-15 (546715c). Not attacked in a separate review session. v0.2 added a second research pass and a reading of S-004; v1.0 folds in the founder's answers of 2026-11-15. |
| R-02 | `../research/R-02_RUNTIME_AND_HARNESS.md` | 1.0, 2026-11-16 | Proposed; accepted when its pull request is merged. Not attacked in a separate review session. Carries the spike under `spikes/r-02/` and feeds Gate G1a with R-01. |
| REV-01 brief | `../reviews/REV-01_BRIEF.md` | 2026-11-17 | Instructions for a separate session to attack R-01 and R-02. A brief, not a finding; the review itself will be `../reviews/REV-01_R-01_AND_R-02.md`. |
| REV-01 | `../reviews/REV-01_R-01_AND_R-02.md` | 1.0, 2026-11-17 | Proposed; accepted when its pull request is merged. The separate review of R-01 and R-02 that P-000 requires, by a session that wrote neither. A review states findings and proposes fixes; it changes no report, decision or service file. Its tests are under `spikes/r-02/review/`. Each finding takes effect only when Cole rules on it. |
| REV-01 fix pass | `../reviews/REV-01_FIX_PASS.md` | 1.0, 2026-11-18 | Proposed; accepted when its pull request is merged. What was done in the permission service about the review's findings, by the session that wrote the review. The fixed service, its tests and raw results are under `spikes/rev-01-fix/`; `spikes/r-02/` is unchanged. Not attacked in a separate review session. |
| LEDGER | `../research/EVIDENCE_LEDGER.md` | v1.6, 2026-11-18 | Open, 132 rows (E-01 to E-132). Rows E-75 to E-113 are proposed with R-02 (E-100 to E-112 are runs of the spike). Rows E-114 to E-127 are proposed with REV-01. Rows E-128 to E-132 are proposed with the REV-01 fix pass. Rows are added by each research report and review. |

Gate G0 note: pull request #1, which carried V-000 v0.2, was merged on 2026-11-15 (commit 2baba1b). The status cells above for P-000 and V-000, and V-000's own acceptance record, were written before that merge and are left for the founder to update.

Update, 2026-11-15: the founder asked for those records to be brought up to date. The status cells above, V-000's acceptance record and the README status now reflect pull request #1 (2baba1b) and pull request #2 (546715c). The note above is kept as written.

## Rules

1. Keep founder input, model synthesis and external evidence distinguishable.
2. A superseded artifact stays in the repository, marked with what superseded it.
3. Authorization to prepare a document, acceptance of it, ticket readiness and verification are four separate records.
4. Research reports carry an as-of date and claim-level citations.
5. No employer or third-party proprietary data in this repository.
