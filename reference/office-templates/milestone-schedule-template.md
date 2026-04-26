# OTA Milestone Schedule xlsx Spec

Specification for the Excel companion to `drafts/milestone-schedule.md` (OTA proposals, `pricing_artifact: ota-milestones`). Useful for PMO tracking after award and for Agreements Officer review during evaluation.

## Workbook structure

### Sheet 1: Milestone Schedule

Direct export of the milestone table from `drafts/milestone-schedule.md`:

| # | Title | Deliverable | Acceptance Criterion | Start | Duration (months) | End | Payment | % of Total |
|---|---|---|---|---|---:|---|---:|---:|
| M1 | | | | | | `=Start+Duration` | | `=Payment/Total` |
| M2 | | | | | | | | |
| **Total** | | | | | | | `=SUM()` | 100% |

**Formatting:**
- Acceptance Criterion column: word wrap, width 40
- Payment: `$#,##0`
- % of Total: `0.0%`
- Conditional: if any single milestone >40% of total → yellow fill + note: "review payment pacing — may appear front-loaded to AO"

### Sheet 2: Gantt View

Visual Gantt chart generated from Sheet 1's Start + Duration columns. Each milestone is a horizontal bar. Use Excel's built-in stacked bar chart or conditional formatting approach.

### Sheet 3: Internal Cost Buildup (NOT FOR SUBMISSION)

The cost decomposition that *informed* each milestone payment but is not submitted externally:

| Milestone | Direct Labor | ODCs | Subs | Indirect | Fee Equiv | Total |
|---|---:|---:|---:|---:|---:|---:|
| M1 | | | | | | `=SUM()` |

Add header: "⚠ INTERNAL ONLY — Milestone payments are the external artifact. This sheet exists for PMO tracking and defensibility."

### Sheet 4: Data Rights Assertions

| Data / Software Item | Category | Basis | Marking |
|---|---|---|---|
| [item] | [Restricted / Government Purpose Rights / Unlimited] | [Exclusively private expense / Mixed funding / Delivered under this agreement] | [10 USC 4022 marking] |

### Sheet 5: Follow-on Production (10 USC 4022(f))

| Question | Answer |
|---|---|
| Prototype completion criteria | |
| Expected Phase III vehicle | |
| Non-traditional contributor status | |
| Cost share (if applicable) | |

## Formatting & file properties

- Author: [Company]
- Title: "Milestone Payment Schedule — [Prototype Project]"
- Keywords: "OTA, milestone, 10 USC 4022"
