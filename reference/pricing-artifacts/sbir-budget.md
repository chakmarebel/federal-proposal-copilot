---
artifact_id: sbir-budget
output_file: drafts/sbir-budget.md
companion_file: working/pricing-inputs.md
mental_model: Line-item budget conforming to the SBIR Policy Directive — not a FAR cost volume
must_not_produce:
  - FAR Part 15 cost volume structure
  - DCAA-audit-ready rate certifications
  - DFARS 252.227 data rights assertions (use SBIR Policy Directive markings)
  - Pricing that exceeds the topic's budget cap
---

# SBIR Budget

## Mental model
Reviewer is checking: does the budget fit the topic cap, does the direct labor make sense for the proposed work, and is the cost/hour reasonable for a small business performing R&D?

Phase I is a feasibility study (small, short). Phase II is prototype development (larger, longer, Phase I results required).

## Required inputs (ask the user)

### Basics
- Phase (I or II)
- Agency (DoD, NASA, DOE, NIH, NSF — caps and rules vary)
- Topic number and title
- Topic budget cap (read from solicitation — do not assume)
- Period of performance (Phase I: typically 6 months DoD / 6-12 months civilian; Phase II: typically 24 months)

### Labor
- Principal Investigator: name, hourly rate, estimated hours
  - **SBIR rule:** PI must commit ≥51% employment during performance (Phase I) — verify
- Other key personnel: name, role, hourly rate, hours
- Fringe rate (if applicable — otherwise load is inside the hourly rate)

### Indirect rates (if on a provisional or negotiated rate agreement)
- Fringe rate
- Overhead rate
- G&A rate
- Whether the firm has a NICRA (negotiated indirect cost rate agreement) or is using de minimis (10%)

### Other direct costs
- Materials / supplies
- Equipment (SBIR: equipment ≥$5K typically restricted in Phase I — verify topic)
- Travel (destination, purpose, rough estimate)
- Subcontracts (name, work description, $ — Phase I: prime must perform ≥67%; Phase II: ≥50%)
- Consultants (if any — distinguish from subcontracts)

### Fee
- Fee rate (SBIR typically 7% — verify against agency policy; some allow up to 10%)

## Calculation approach

Line-item buildup using standard SBIR budget format. Every agency has its own spreadsheet template — this markdown is the narrative + table view that mirrors it. If the agency provides a required spreadsheet (DoD DD Form 250, NIH Detailed Budget, etc.), the user must also fill that; this artifact supplements it with narrative.

## Output structure (`drafts/sbir-budget.md`)

```markdown
# SBIR [Phase I | Phase II] Budget — [Topic Number]

**Firm:** [Company Name]
**Topic:** [Topic Number and Title]
**Agency:** [Agency]
**Period of Performance:** [Months]
**Total Requested:** $[Total] (topic cap: $[Cap])

## Budget Summary

| Cost Element | Amount |
|---|---:|
| Direct Labor | $[X] |
| Fringe Benefits ([rate]%) | $[X] |
| **Total Direct Labor with Fringe** | $[X] |
| Materials / Supplies | $[X] |
| Equipment | $[X] |
| Travel | $[X] |
| Subcontracts / Consultants | $[X] |
| Other Direct Costs | $[X] |
| **Total Direct Costs** | **$[X]** |
| Overhead ([rate]%) | $[X] |
| G&A ([rate]%) | $[X] |
| **Total Costs** | **$[X]** |
| Fee ([rate]%) | $[X] |
| **Total Requested Price** | **$[Total]** |

## Direct Labor Detail

| Name | Role | Rate ($/hr) | Hours | Cost |
|---|---|---:|---:|---:|
| [PI name] | Principal Investigator | $[rate] | [hrs] | $[X] |
| [name] | [role] | $[rate] | [hrs] | $[X] |
| **Total** | | | [hrs] | **$[X]** |

**PI commitment:** The Principal Investigator will commit ≥51% of employment during the performance period in accordance with SBIR Policy Directive.

## Budget Narrative

### Direct Labor
[1 paragraph explaining the team, each role's contribution, and how hours were estimated.]

### Materials and Equipment
[Paragraph. If equipment purchases are proposed, explain necessity and why not rentable. Phase I equipment typically limited to <$5K per item.]

### Travel
[Paragraph. Destination, purpose, number of trips, per-person cost estimate. Typical Phase I travel: kickoff meeting + one review.]

### Subcontracts / Consultants
[Paragraph per subcontractor. Prime work share: Phase I ≥67%, Phase II ≥50%.]

### Indirect Rates
[Paragraph. State whether rates are NICRA, provisional, or de minimis. Reference the most recent DCAA audit if applicable.]

### Fee
[1-2 sentences. Fee rate and rationale. Note: SBIR typically 7%.]

## Compliance Statement

This budget complies with:
- Topic budget cap: $[cap]
- Prime work share: [%] (requirement: ≥67% Phase I / ≥50% Phase II)
- PI employment commitment: ≥51% during performance period
- [Any agency-specific requirements]

## Data Rights
Data developed under this award will be marked in accordance with the SBIR/STTR Policy Directive, not DFARS 252.227. Specific data rights assertions are included in the technical volume.
```

## `working/pricing-inputs.md` (companion)

Capture the raw rate buildups and any assumptions that drove the numbers:

```markdown
# SBIR Pricing Inputs

## Rate sources
- Fringe: [source — prior NICRA, industry avg, etc.]
- Overhead: [source]
- G&A: [source]
- Labor rates: [source — payroll records, prevailing wage]

## Budget checks (internal)
- Topic cap: $[cap]
- Proposed total: $[total]
- Margin to cap: $[delta]
- Prime work share calc: [prime direct labor $ / total direct labor $] = [%]
- PI hours / total period hours: [%]

## Key assumptions
[List anything that could move the budget]
```

## Calibrated milestone-payment-profile workbook structure

When the agency requires a milestone-payment-profile workbook (common for AFWERX/BESPIN-flighted SBIRs and some other agency variants), use this 4-sheet structure calibrated against winning examples:

### Sheet 1: Summary / MOU Terms
- Compact (typical 25 rows × 3 cols): MOU header info, milestone terms, payment summary
- Mostly value cells with a few `=CELL+CELL` rollup formulas

### Sheet 2: Internal Staffing
- **Half-month-period grid:** Name | LC (Labor Category) | 0.5 | 1 | 1.5 | 2 | ... | 14.5 | 15 | TOTAL | Hours
- 30 half-month columns spans a 15-month Phase II
- One row per named or category staff member
- Values in cells = hours allocated to that person in that half-month
- TOTAL column: `=SUM(<row range>)` per row
- Hours column: derived from total × hours/month convention
- Adjust column count for shorter/longer Phase II durations (e.g., 24 months = 48 half-month columns)

**Why half-month and not monthly:** captures ramp/de-ramp slope more accurately for cost-realism review. Onboarding doesn't happen on month-1; production effort doesn't go to zero on month-15. Half-month granularity matches reality.

### Sheet 3: Pricing
- Top-of-sheet header references pull from Indirects sheet:
  - `=ROUND(Indirects!$P$12,4)` for fringe rate (or whatever cell holds the calculated rate)
  - `=ROUND(Indirects!$P$20,4)` for overhead
  - `0.08` literal for fee/profit (8% typical SBIR ceiling, agency-specific)
- Body: rate × base calculations (`=CELL*CELL`) + additive rollups (`=CELL+CELL`)
- Currency formatting: `_("$"* #,##0.00_);_("$"* \(#,##0.00\);_("$"* "-"??_);_(@_)` — full accounting format with parens for negatives, dash for zero
- Percentage formatting: `0.00%` and `0%`
- 50+ formulas in a 79-cell sheet — heavily computed, not hand-entered

### Sheet 4: Indirects
- Largest sheet (typical 60+ rows × 17+ cols)
- Header: date range header (e.g., `Jan - Dec 18` for fiscal-year rate buildup)
- Multi-month rate calculation worksheet with ROUND() wrappers throughout to prevent floating-point drift in cost summaries
- Mix of accounting formats (`_(* #,##0_)...`) and percentage formats
- One source of truth for fringe / overhead / G&A rates that the Pricing sheet references

### Workbook conventions

- **No frozen panes, no auto-filter** — workbook is print/export-oriented, not for browsing in a UI. The CO/AO consumes it as a delivered artifact.
- **Single source of truth for rates** — Indirects sheet calculates, Pricing sheet references via `=ROUND(Indirects!$X$N,4)`. Never duplicate rates.
- **ROUND() wrappers everywhere** — prevents floating-point drift between Internal Staffing total → Pricing rollup → milestone payment summary.
- **Accounting number format is non-negotiable** for currency cells. Plain `$#,##0` is acceptable for summary tables; `_("$"* #,##0.00_)...` is required where the workbook will be inspected by a contracting officer.
- **Half-month staffing granularity** for Phase II durations of 12+ months. Monthly is acceptable for Phase I.
- **No merged cells in data ranges** — only in section header rows. Merged data cells break formulas and sorting.

When the framework's `export-proposal` skill produces an `xlsx` for an SBIR Phase II workspace, this 4-sheet structure should be the default scaffold (when no agency-provided template is in `inputs/00_priority/*.xlsx`).

## Pitfalls
- **Exceeding the topic cap** — instant disqualification. Compute margin before submission.
- **Prime work share miscalc** — below 67% (Phase I) / 50% (Phase II) is fatal.
- **PI commitment** — if PI is on multiple SBIRs, aggregate commitment cannot exceed 100%. Check.
- **Applying DFARS data rights** — use SBIR Policy Directive markings instead.
- **Fee > 7%** — only allowable if agency policy explicitly permits. Verify.
- **Equipment purchases** — Phase I often limits equipment; Phase II more flexible. Read the topic carefully.
