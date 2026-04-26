# SBIR Budget xlsx Spec

Specification for the SBIR budget workbook exported at `final/xlsx/sbir-budget.xlsx` when `pricing_artifact: sbir-budget`. Some agencies provide their own required Excel template — if one exists in `inputs/00_priority/*.xlsx`, prefer that over this spec.

## Workbook structure

### Sheet 1: Budget Summary

The single-page cost element summary that matches the markdown in `drafts/sbir-budget.md`. Values populated from `working/pricing-inputs.md`.

| Cost Element | Amount |
|---|---:|
| Direct Labor | `=SUM(...)` |
| Fringe Benefits ([rate]%) | `=D2*<fringe_rate>` |
| **Total Direct Labor with Fringe** | `=D2+D3` |
| Materials / Supplies | |
| Equipment | |
| Travel | |
| Subcontracts / Consultants | |
| Other Direct Costs | |
| **Total Direct Costs** | `=SUM(...)` |
| Overhead ([rate]%) | `=<base>*<oh_rate>` |
| G&A ([rate]%) | `=<base>*<ga_rate>` |
| **Total Costs** | `=SUM(...)` |
| Fee ([rate]%) | `=<base>*<fee_rate>` |
| **Total Requested Price** | `=SUM(...)` |

**Formulas, not hardcoded values.** If the user adjusts a rate, totals recalc. Highlight input cells in light yellow; calculated cells in white.

### Sheet 2: Direct Labor Detail

| Name | Role | Rate ($/hr) | Hours | Cost |
|---|---|---:|---:|---:|
| [PI name] | Principal Investigator | | | `=C2*D2` |
| [name] | [role] | | | `=C3*D3` |
| | | | | |
| **Total** | | | `=SUM(D2:D5)` | `=SUM(E2:E5)` |

Below the table, add a compliance callout:
- "PI Commitment: ≥51% (SBIR requirement) — Actual: `=<PI_hours>/<total_hours>`%"
- Conditional: if <51%, cell turns red and adds: "⚠ VIOLATES SBIR PI commitment requirement"

### Sheet 3: Indirect Rates

| Rate | Value | Source |
|---|---:|---|
| Fringe | | [NICRA / Provisional / de minimis] |
| Overhead | | |
| G&A | | |

### Sheet 4: Prime Work Share Check

Computes prime vs. sub work share from Sheet 1:

- Prime direct labor ($): `=<Sheet1 direct labor>`
- Sub direct labor ($): `=<Sheet1 subs>`
- Prime share: `=Prime/(Prime+Sub)`
- Requirement: Phase I ≥67%, Phase II ≥50% (pull Phase from `working/proposal-type.md`)
- Conditional: if below requirement, cell turns red with warning

### Sheet 5: Topic Cap Check

- Topic cap: (manual entry from solicitation)
- Proposed total: `=<Sheet1 total>`
- Margin: `=Cap-Proposed`
- Conditional: if negative, cell turns red and displays "⚠ EXCEEDS TOPIC CAP — DISQUALIFYING"

## Formatting

- Currency: `$#,##0` for all cost cells
- Percentage: `0.0%` for rate cells
- Header rows: bold, white on dark blue
- Totals: bold, top border
- Print setup: Fit-to-page-width, landscape where needed

## Agency-specific templates

**DoD SBIR:** DoD typically provides `DoD SBIR Proposal Cost Volume Template.xlsx`. If present in `inputs/00_priority/`, populate that instead.

**NIH:** NIH uses PHS 398/424 forms. If an NIH budget form is in inputs, route to that workflow instead.

**NSF, DOE, NASA:** Agency-specific templates vary. Always check `inputs/00_priority/` first.
