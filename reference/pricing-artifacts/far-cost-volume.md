---
artifact_id: far-cost-volume
output_file: drafts/cost-volume.md
companion_file: working/pricing-inputs.md
mental_model: DCAA-auditable cost volume with CLIN structure, BOE per element, and certified or verifiable rate support
must_not_produce:
  - ROM ranges without supporting buildup
  - Commercial-item pricing language
  - Milestone-payment schedule (that's OTA)
  - Unsupported assumptions on rates, hours, or ODCs
---

# FAR Cost Volume

## Mental model
The cost/price analyst is reading for **cost realism** (is the price high enough to actually execute?) and **reasonableness** (is it too high?). Every number must trace to a verifiable source: labor rates to payroll or prevailing wage, indirect rates to NICRA or DCAA audit, ODCs to quotes or history.

This is the most rigorous pricing artifact. It is also the most common — use this template for any FAR Part 15 competitive procurement, IDIQ task order, or BAA that requires a full cost volume.

## Required inputs (ask the user)

### Contract structure
- Contract type: FFP, CPFF, CPIF, T&M, LH, FP-LOE, FPIF
- CLIN structure: what CLINs exist, what's priced under each (base + options)
- Period of performance: base + option periods, durations

### Labor
- Labor categories (title, clearance level if applicable)
- For each category: billing / wrap rate OR direct rate + indirect rate disclosure
- Rate source: GSA Schedule / NICRA / prevailing wage / commercial / DCAA-approved
- Named key personnel (required if solicitation calls for them): name, role, rate, hours
- Hours per LCAT per CLIN per period

### Indirect rates (if not using wrap rates)
- Fringe rate + base
- Overhead rate + base (may have multiple pools — engineering, on-site, off-site)
- G&A rate + base
- Source: NICRA / provisional / DCAA-approved / forward-priced rate agreement

### ODCs
- Travel: trips per period, destinations, per-diem method (GSA rates or actual)
- Materials / supplies
- Equipment (prior-approval thresholds under FAR 45)
- Software licenses
- Subcontracts: company, work, $ with pass-through handling fee
- Consultants

### Fee / profit
- Rate (typical: 7-10% services, 6-8% R&D, lower for LPTA)
- Weighted Guidelines analysis if required (DoD DFARS 215.404)

### Strategy
- LPTA or best value?
- Known or suspected budget / should-cost?
- Price-to-win target?
- Identified cost risks (scope uncertainty, travel, subs)?

## Calculation approach

**Engineering build-up** is the preferred method for anything above ~$1M:
1. Decompose scope to WBS elements (usually parallels the technical volume sections)
2. For each WBS element, estimate hours per LCAT
3. Apply rates (wrap or buildup) to get direct cost
4. Apply indirects per the rate structure
5. Sum with ODCs, subs, fee → Total Evaluated Price (TEP)

**Analogous** estimates (by comparison to prior projects) are acceptable for sub-elements but not for the full cost volume.

## Output structure (`drafts/cost-volume.md`)

```markdown
# Cost Volume — [Proposal Name]

**Solicitation:** [Number]
**Offeror:** [Company] — CAGE [X], UEI [X]
**Contract Type:** [FFP / CPFF / etc.]
**Period of Performance:** [Base + Options]
**Total Evaluated Price:** $[Total]

## 1. Cost Summary

### 1.1 Price by CLIN and Period

| CLIN | Description | Base | Opt 1 | Opt 2 | Total |
|---|---|---:|---:|---:|---:|
| 0001 | [Description] | $[X] | $[X] | $[X] | $[X] |
| 0002 | [Description] | $[X] | $[X] | $[X] | $[X] |
| **Total** | | $[X] | $[X] | $[X] | **$[X]** |

### 1.2 Price by Cost Element

| Cost Element | Base | Opt 1 | Opt 2 | Total |
|---|---:|---:|---:|---:|
| Direct Labor | $[X] | $[X] | $[X] | $[X] |
| Fringe ([rate]%) | $[X] | $[X] | $[X] | $[X] |
| Overhead ([rate]%) | $[X] | $[X] | $[X] | $[X] |
| G&A ([rate]%) | $[X] | $[X] | $[X] | $[X] |
| ODC — Travel | $[X] | $[X] | $[X] | $[X] |
| ODC — Materials | $[X] | $[X] | $[X] | $[X] |
| Subcontracts | $[X] | $[X] | $[X] | $[X] |
| Subtotal Cost | $[X] | $[X] | $[X] | $[X] |
| Fee ([rate]%) | $[X] | $[X] | $[X] | $[X] |
| **Total Evaluated Price** | **$[X]** | **$[X]** | **$[X]** | **$[X]** |

## 2. Basis of Estimate (by WBS)

### 2.1 WBS 1.0 — [Title]
**Scope.** [Paragraph on what work this covers, traceable to the technical volume section.]
**Hours.** [Labor category × hours table]
**Method.** [Engineering build-up / analogous / parametric — state it]
**Assumptions.** [List]

### 2.2 WBS 2.0 — [Title]
[Same structure]

[Repeat per WBS element]

## 3. Labor Rate Justification

### 3.1 Rate Source
[Paragraph. GSA Schedule / NICRA / prevailing wage / commercial comparables / DCAA-audited actuals.]

### 3.2 Labor Category Rates

| LCAT | Clearance | Rate ($/hr) | Source |
|---|---|---:|---|
| [Senior ML Engineer] | [Secret] | $[X] | [GSA Schedule / Payroll avg + [X]% escalation] |
| ... | | | |

### 3.3 Key Personnel (if required)
[Named resumes + rates. Cross-reference technical volume key personnel section.]

### 3.4 Escalation
Out-year rates escalated at [X]% per year based on [BLS ECI / company history].

## 4. Indirect Rate Support

### 4.1 Rate Structure
| Pool | Rate | Base | Source |
|---|---:|---|---|
| Fringe | [X]% | Total direct labor | [NICRA / Provisional / FY-audit] |
| Overhead | [X]% | Direct labor + fringe | [NICRA / Provisional] |
| G&A | [X]% | Total cost input | [NICRA / Provisional] |

### 4.2 Supporting Documentation
[NICRA letter, most recent DCAA audit, or provisional billing rate agreement — attach or reference.]

## 5. Other Direct Costs

### 5.1 Travel
[Table: trip, destination, purpose, per-diem basis, cost]
Per-diem method: GSA rates (default) or [alternate with justification].

### 5.2 Materials and Supplies
[Itemized with vendor quotes or catalog reference.]

### 5.3 Equipment
[Itemized. Note FAR 45 prior-approval thresholds if any item exceeds $5K.]

### 5.4 Software Licenses
[List. Vendor, licensing model, cost.]

## 6. Subcontracts

| Sub | Work Description | $ | Prime Work Share Impact |
|---|---|---:|---|
| [Name] | [Scope] | $[X] | [% of total]  |

Pass-through handling: [X]% on subcontract total.

Subcontractor cost proposals are attached for subs exceeding [$X] or [%] of prime price per FAR 15.404-3.

## 7. Fee / Profit

Fee rate: [X]% applied to [Total Cost Input or CPFF-defined base].

Rationale:
[Paragraph. Risk profile, contract type (FFP vs. CPFF), Weighted Guidelines result if applicable, competitor benchmarking.]

## 8. Assumptions and Exclusions

### 8.1 Assumptions
[Numbered list. Each with cost-swing implication.]

### 8.2 Exclusions
[Numbered list. What is NOT included in price — GFE, facilities, etc.]

## 9. Price Reasonableness

This price is reasonable based on:
- Independent Government Cost Estimate (IGCE) alignment (if known)
- Prior contract history at comparable rates
- Market comparables for labor categories
- Competitive pressure from [N] expected offerors

## 10. Cost Realism

This price is realistic based on:
- Labor hours derived from engineering decomposition of the technical volume
- Indirect rates supported by NICRA / recent DCAA audit
- ODCs quoted or based on history
- No unbalanced pricing between CLINs or periods

[Appendices: Subcontractor cost proposals, NICRA letter, any required certifications]
```

## `working/pricing-inputs.md` (companion)

```markdown
# FAR Cost Volume Inputs

## WBS
[Full WBS tree — parallels technical volume sections]

## Hours by LCAT by WBS by CLIN by period
[Spreadsheet-style table — this is the source for every BOE]

## Rate buildup
- Wrap rate derivation (if used)
- Indirect rate pool definitions
- Escalation factors

## ODC sourcing
- Travel quotes or GSA per-diem lookups
- Materials vendor quotes
- Equipment quotes

## Subcontract received cost proposals
[Reference attachments]

## Price-to-win analysis (internal)
- IGCE estimate if known
- Competitor price estimates
- Margin analysis (fee as % of cost)

## Risks to the estimate
[List — scope assumptions, rate risk, escalation, etc.]
```

## Pitfalls
- **Unbalanced pricing** — CLINs that shift cost from one period to another to game evaluation. Modern source selection explicitly checks for this.
- **Indirect rate mismatch** — using a lower rate than your DCAA-audited provisional without forward-pricing agreement. Audit finding after award.
- **Missing Weighted Guidelines** — for DoD cost-reimbursement, DFARS 215.404-71 is mandatory.
- **Subcontract markup > 10%** — typical handling fee is 5-8%. Anything higher invites scrutiny.
- **Travel undersped** — most common overrun source. Build in realistic trip counts.
- **Out-year escalation errors** — escalate EVERY rate, not just labor. Missing ODC escalation on 5-year TOs adds up.
- **Mixing wrap rates and rate buildups** — pick one approach per labor category and be consistent.
