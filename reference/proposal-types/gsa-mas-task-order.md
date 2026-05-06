---
type_id: gsa-mas-task-order
display_name: GSA MAS-Flighted Task Order / BPA Competition
solicitation_vehicle: GSA-MAS-BPA
page_target: 13-25 pp Technical + 2-3 pp Price + 5-8 pp Security + xlsx pricing workbook
pricing_artifact: gsa-mas-pricing
pp_required: true
required_skills: [opportunity-quick-look, proposal-manager, customer-intel, competitor-assessment, capture-intent, proposal-solution-architect, past-performance, proposal-storyboard, proposal-graphics, technical-review, pricing-analyst, proposal-writer, proposal-editor, compliance-check, evidence-check, red-team-review]
skipped_skills: [capture-scorecard]
section_patterns: gsa-mas-task-order
compliance_sources: [EvaluationFactors, EvaluationSubFactors, SOW]
evaluator_framing: Multi-vendor BPA / IDIQ competition under an existing GSA MAS Schedule. Evaluators score Sub-Factors (typically 1.1 Corporate Experience, 1.2 Staffing Key Personnel, 1.3 Approach). Past Performance Coverage Matrix is the highest-leverage compliance artifact. Resumes embed in technical body, not appendix. Multi-volume submission: Tech + Price (narrative + xlsx workbook) + Security (when cleared).
typical_duration: 2-4 weeks
notes: |
  GSA MAS-flighted task-order or BPA competitions issued by an agency that limits eligibility to
  vendors holding a specific GSA MAS Schedule. Vendor responds with a multi-volume submission
  using existing Schedule-approved labor categories and ceiling rates.

  Distinct from:
  - Direct GSA MAS Schedule offering (different patterns, uncalibrated)
  - FAR Part 15 RFP (uses 'far-rfp' type with 'full-proposal' patterns)
  - Standalone IDIQ TO under non-MAS contract (uses 'idiq-to' type)

  See:
  - reference/section-patterns/gsa-mas-task-order.md
  - reference/proposal-conventions/gsa-mas.md
  - reference/pricing-artifacts/gsa-mas-pricing.md
  - reference/section-patterns/security-volume.md (used when solicitation requires cleared work)
---

# Proposal Type: GSA MAS-Flighted Task Order / BPA Competition

Multi-vendor task-order or BPA competitions issued by an agency under an existing GSA MAS Schedule. Vendor must hold the relevant Schedule (typically GSA MAS Information Technology Category) to bid.

## When to use this type

- Solicitation explicitly limits offerors to current Schedule contract holders
- Solicitation references a specific GSA MAS BPA or IDIQ contract number
- Multi-volume submission requested (Technical + Price + Security)
- Evaluation organized around Sub-Factors (1.1, 1.2, 1.3 typical)
- Pricing requested as labor-category × period table referencing Schedule rates

## When NOT to use this type

- Direct Schedule offering submission to GSA itself (different patterns)
- Standalone task order under non-MAS IDIQ (use `idiq-to`)
- FAR Part 15 RFP with full Section L/M (use `far-rfp`)
- Single-volume technical-only response (use `idiq-to`)

## Multi-volume artifact set

| Volume | File | Pattern source |
|---|---|---|
| Vol 1 — Technical | `Vol 1 Technical.pdf` | `section-patterns/gsa-mas-task-order.md` |
| Vol 2 — Price (narrative) | `Vol 2 Price.pdf` | `pricing-artifacts/gsa-mas-pricing.md` |
| Vol 3 — Security (if cleared) | `Vol 3 Security.pdf` | `section-patterns/security-volume.md` |
| Vol IV — Price (workbook) | `Vol IV Price-Attach.xlsx` | `pricing-artifacts/gsa-mas-pricing.md` |
| Attachments | DD 254, FCL Template, PCL Template (FOUO) | `section-patterns/security-volume.md` §"Required attachments" |

## High-leverage discriminators for this type

- **Past Performance Coverage Matrix** as the Sub-Factor 1.1 anchor — single most important graphic
- **Embedded resumes** in technical body (NOT appendix) — different from FAR / SBIR conventions
- **Letter-spaced acronym header strip** — program name expanded across the top of every body page
- **Single-sheet pricing workbook** with simple `"$"#,##0.00` currency format
- **Volume numbering with Roman IV** for the pricing workbook attachment
