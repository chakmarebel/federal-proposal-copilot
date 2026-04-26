# Pricing Artifact Templates

One file per `pricing_artifact` value declared in `reference/proposal-types/*.md`. The `pricing-analyst` skill reads `working/proposal-type.md`, looks up the `pricing_artifact` field, and follows the matching template here.

## Artifacts

| Artifact ID | Format | Output file | Used by |
|---|---|---|---|
| `none` | no pricing | (none) | `white-paper`, `rfi`, `sources-sought` |
| [`rom.md`](rom.md) | Rough Order of Magnitude range | `drafts/rom.md` | `rom`, `cso-brief`, `ota-white-paper` |
| [`sbir-budget.md`](sbir-budget.md) | SBIR line-item budget | `drafts/sbir-budget.md` | `sbir-phase1`, `sbir-phase2` |
| [`ota-milestones.md`](ota-milestones.md) | Milestone-payment schedule | `drafts/milestone-schedule.md` | `ota-proposal` |
| [`cso-commercial.md`](cso-commercial.md) | Commercial-item pricing | `drafts/cso-pricing.md` | `cso-full` |
| [`far-cost-volume.md`](far-cost-volume.md) | FAR/DCAA cost volume with CLINs + BOEs | `drafts/cost-volume.md` | `far-rfp`, `idiq-to`, `baa` |
| [`gsa-mas-pricing.md`](gsa-mas-pricing.md) | LCAT-mapping narrative + single-sheet pricing workbook (Schedule rates pre-approved, no DCAA buildup) | `drafts/price-narrative.md` + `final/xlsx/pricing-workbook.xlsx` | `gsa-mas-task-order` |

## Template structure (every artifact file)

Each artifact template declares:

```yaml
---
artifact_id: <id>
output_file: drafts/<filename>.md
companion_file: working/pricing-inputs.md
mental_model: <one-line evaluator/reader framing>
must_not_produce: [list of what this artifact is NOT — prevents drift]
---
```

Body sections:

1. **Mental model** — how the reader thinks about this pricing artifact
2. **Required inputs** — what to ask the user for (and what NOT to ask)
3. **Calculation approach** — the method (analogous, parametric, engineering buildup, market comparables, milestone-based)
4. **Output structure** — the section template for the deliverable
5. **Pitfalls** — what goes wrong if this artifact drifts toward a different pricing type

## Adding a new artifact

1. Add a file here following the structure above
2. Add the artifact ID to the `pricing_artifact` enum in `reference/proposal-types/README.md`
3. Use it in one or more proposal-type files
