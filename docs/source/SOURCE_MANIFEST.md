# Source manifest — azi-hub-v2

Manifest v1.1, 2026-11-15. This file says what each source is and how much authority it has. It is metadata, not evidence.

v1.1 amends v1 of the same day, on the founder's instruction in the R-02 brief: the status cells of the canonical artifacts are brought up to date with the two merges, and S-015 is added.

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

## Canonical artifacts

| ID | File | Version | Status |
| --- | --- | --- | --- |
| P-000 | `P-000_RESTART_FINDINGS_AND_PLAN.md` | 2026-11-15, amended the same day | The plan in use. Merged with pull request #1 (2baba1b). Gate G0 accepted V-000; P-000 has no acceptance record of its own. The amendments of 2026-11-15 are proposed in the pull request that carries V-000 v0.3. |
| V-000 | `V-000_VISION_BASELINE_AND_DRIFT_AUDIT.md` | 0.3 | v0.2 accepted at Gate G0: pull request #1 merged on 2026-11-15 (2baba1b). v0.3 proposed; accepted when its pull request is merged. |
| INV-000 | `INV-000_CAPABILITY_INVENTORY.md` | 0.3 | Draft. v0.3 appends two amendments from R-01 section 10 and three rows for capability C-23. |
| R-01 | `../research/R-01_CATEGORY_AND_EXISTING_TOOLS.md` | 1.0, 2026-11-15 | Accepted: pull request #2 squash-merged on 2026-11-15 (546715c). Not attacked in a separate review session. v0.2 added a second research pass and a reading of S-004; v1.0 folds in the founder's answers of 2026-11-15. |
| LEDGER | `../research/EVIDENCE_LEDGER.md` | v1.2, 2026-11-15 | Open, 74 rows; the next row is E-75. Rows are added by each research report. |

Gate G0 note: pull request #1, which carried V-000 v0.2, was merged on 2026-11-15 (commit 2baba1b). The status cells above for P-000 and V-000, and V-000's own acceptance record, were written before that merge and are left for the founder to update.

Update, 2026-11-15: the founder asked for those records to be brought up to date. The status cells above, V-000's acceptance record and the README status now reflect pull request #1 (2baba1b) and pull request #2 (546715c). The note above is kept as written.

## Rules

1. Keep founder input, model synthesis and external evidence distinguishable.
2. A superseded artifact stays in the repository, marked with what superseded it.
3. Authorization to prepare a document, acceptance of it, ticket readiness and verification are four separate records.
4. Research reports carry an as-of date and claim-level citations.
5. No employer or third-party proprietary data in this repository.
