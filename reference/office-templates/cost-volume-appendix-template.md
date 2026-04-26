# Cost Volume Appendix xlsx Spec

Specification for the Excel companion to a FAR cost volume (`pricing_artifact: far-cost-volume`). The Word document contains the narrative and BOE; this workbook contains the numeric tables that are impractical in Word (rate buildups, WBS × LCAT × period hours, CLIN matrices).

## Workbook structure

### Sheet 1: Cost Summary

The CLIN × Period matrix from `drafts/cost-volume.md`:

| CLIN | Description | Base | Opt 1 | Opt 2 | Opt 3 | Opt 4 | Total |
|---|---|---:|---:|---:|---:|---:|---:|
| 0001 | | | | | | | `=SUM(C:G)` |
| 0002 | | | | | | | |
| **Total** | | `=SUM(C:C)` | `=SUM(D:D)` | | | | `=SUM(C:G) row total` |

### Sheet 2: Cost Element Breakdown

By period, by cost element:

| Element | Base | Opt 1 | Opt 2 | ... | Total |
|---|---:|---:|---:|---:|---:|
| Direct Labor | | | | | |
| Fringe | `=<Direct Labor>*<fringe_rate>` | | | | |
| Overhead | | | | | |
| G&A | | | | | |
| ODC — Travel | | | | | |
| ODC — Materials | | | | | |
| Subcontracts | | | | | |
| Subtotal Cost | `=SUM(above)` | | | | |
| Fee | | | | | |
| **Total Evaluated Price** | | | | | |

### Sheet 3: WBS × LCAT Hours (base period)

The engineering build-up table. One row per (WBS, LCAT) combination:

| WBS | LCAT | Hours | Rate | Cost |
|---|---|---:|---:|---:|
| 1.0 | Senior ML Engineer | | | `=C2*D2` |
| 1.0 | Program Manager | | | |
| 2.0 | Senior ML Engineer | | | |
| ... | | | | |

Repeat per-option-period on additional sheets (Sheet 3b, 3c, ...) or use a "Period" column on a single flat table.

### Sheet 4: Indirect Rate Pools

| Pool | Rate | Base | Source |
|---|---:|---|---|
| Fringe | | Total direct labor | [NICRA 2025-001] |
| Overhead | | Direct labor + fringe | [FY25 audit] |
| G&A | | Total cost input | [NICRA 2025-001] |

### Sheet 5: Labor Rate Table

| LCAT | Clearance | Base Year Rate | Esc % | Yr 2 | Yr 3 | Yr 4 | Yr 5 |
|---|---|---:|---:|---:|---:|---:|---:|
| Senior ML Engineer | Secret | | 3% | `=C2*(1+D2)` | `=E2*(1+D2)` | ... | ... |

### Sheet 6: ODC Detail

Travel, materials, equipment itemized:

**Travel:**
| Trip | Destination | Purpose | # Trips | Per-Trip Cost | Total |
|---|---|---|---:|---:|---:|

**Materials / Equipment:**
| Item | Vendor | Quote Ref | Qty | Unit | Total |
|---|---|---|---:|---:|---:|

### Sheet 7: Subcontract Summary

| Sub | Work | $ Base | Per Option | Total | % of Prime |
|---|---|---:|---:|---:|---:|

### Sheet 8: Unbalanced Pricing Check (internal)

Not submitted. Internal check for evaluators looking at CLIN-to-CLIN and period-to-period cost distribution. Flag:
- Any CLIN with Base period cost >60% of its total (possible front-loading)
- Any CLIN with Option period cost <20% of its Base (possible buy-in)
- Direct labor % of total by period (should be roughly consistent)

### Sheet 9: Weighted Guidelines (DoD cost-reimbursement only)

Per DFARS 215.404-71. Applies only when contract type is CPFF, CPIF, or CPAF.

## Formatting

- All currency: `$#,##0`
- Period column widths: 14 each
- Conditional formatting on subtotals: bold, top border
- Print setup: Fit-to-page (width), landscape, repeat header row

## Data integrity

Every number in the Word cost volume must trace to this workbook. If the narrative cites a figure not in the workbook, something is wrong — fix the narrative or add the supporting data.
