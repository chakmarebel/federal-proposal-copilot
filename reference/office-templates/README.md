# Office Template Specs

Specs for the native Office templates used by `/export-proposal`. These describe the *expected structure* of the output files so `anthropic-skills:docx` / `anthropic-skills:xlsx` / `anthropic-skills:pptx` can produce consistent deliverables across proposals.

## Why specs, not binaries

This directory contains markdown specs, not .docx/.xlsx/.pptx files. Binary templates belong in `my-company/templates/` — that's where users drop their branded versions. The specs here document what the export skill should produce when no branded template exists.

## Files

| Spec | Used by | Output |
|---|---|---|
| [compliance-matrix-template.md](compliance-matrix-template.md) | `/export-proposal` + `/compliance-check` | `final/xlsx/compliance-matrix.xlsx` |
| [sbir-budget-template.md](sbir-budget-template.md) | `/export-proposal` when `pricing_artifact: sbir-budget` | `final/xlsx/sbir-budget.xlsx` |
| [cost-volume-appendix-template.md](cost-volume-appendix-template.md) | `/export-proposal` when `pricing_artifact: far-cost-volume` | `final/xlsx/cost-volume-appendix.xlsx` |
| [milestone-schedule-template.md](milestone-schedule-template.md) | `/export-proposal` when `pricing_artifact: ota-milestones` | `final/xlsx/milestone-schedule.xlsx` |
| [proposal-docx-spec.md](proposal-docx-spec.md) | `/export-proposal` for all Word documents | `final/docx/*.docx` |

## Precedence

When `/export-proposal` builds a deliverable:

1. **If `my-company/templates/<name>.{docx,xlsx,pptx}` exists** — use it as the base. Populate with proposal data.
2. **Else if `inputs/00_priority/*.xlsx`** contains an agency-provided template (common for SBIR) — use it as the base.
3. **Else** — use the spec in this directory to generate from scratch with professional defaults.

## Contributing a branded template

Drop your own branded `.docx`, `.xlsx`, or `.pptx` at `my-company/templates/`. Match the filename to the spec name (without the `-template.md` suffix). Example:

- `my-company/templates/proposal.docx` ← used by `proposal-docx-spec.md`
- `my-company/templates/sbir-budget.xlsx` ← used by `sbir-budget-template.md`

See [my-company/templates/README.md](../../my-company/templates/README.md) (if it exists) for your organization's template conventions.
