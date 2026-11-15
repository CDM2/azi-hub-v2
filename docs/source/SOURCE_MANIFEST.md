# Source manifest — azi-hub-v2

Manifest v1, 2026-11-15. This file says what each source is and how much authority it has. It is metadata, not evidence.

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

## Canonical artifacts

| ID | File | Version | Status |
| --- | --- | --- | --- |
| P-000 | `P-000_RESTART_FINDINGS_AND_PLAN.md` | 2026-11-15 | Proposed |
| V-000 | `V-000_VISION_BASELINE_AND_DRIFT_AUDIT.md` | 0.2 | Proposed; founder answers folded in; accepted when its pull request is merged (Gate G0) |
| INV-000 | `INV-000_CAPABILITY_INVENTORY.md` | 0.2 | Draft |

## Rules

1. Keep founder input, model synthesis and external evidence distinguishable.
2. A superseded artifact stays in the repository, marked with what superseded it.
3. Authorization to prepare a document, acceptance of it, ticket readiness and verification are four separate records.
4. Research reports carry an as-of date and claim-level citations.
5. No employer or third-party proprietary data in this repository.
