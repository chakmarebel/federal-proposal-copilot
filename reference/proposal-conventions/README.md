# Proposal Conventions

Calibrated structural and stylistic conventions for each major federal proposal type. These complement the section-pattern templates (`reference/section-patterns/`) by capturing the *how-it's-actually-done-in-winning-proposals* details: tone, cadence, heading style, table/figure norms, customer-language adoption, and traceability discipline.

**Where these conventions come from:** structural pattern extraction from author-owned winning examples. **No source-proposal prose appears in these files** — only generalized structural lessons and statistical norms (sentence length distributions, page allocations, etc.). See `scripts/extract-pdf-patterns.py` for the extraction methodology.

## Files

| Convention | Vehicle types it informs | Source calibration |
|---|---|---|
| [far-rfp.md](far-rfp.md) | `far-rfp`, `idiq-to`, `cso-full`, `baa` (full-proposal stage) | Air Force IDIQ technical volume, 2026-04-23 |
| [sbir.md](sbir.md) | `sbir-phase1`, `sbir-phase2`, Direct-to-Phase-II SBIRs, STTR | Direct-to-Phase-II SBIR (AFWERX/BESPIN) — technical volume + pitch deck + milestone-payment workbook, 2026-04-25 |
| [gsa-mas.md](gsa-mas.md) | `gsa-mas-task-order` (MAS-flighted BPA / IDIQ task-order competitions); applicable to direct GSA Schedule offerings (uncalibrated) and BPA task orders | NGA SABER II (GSA MAS-flighted multi-vendor BPA) — Tech + Price (narrative + xlsx) + Security volumes, 2026-04-25 |

## How `proposal-writer` and `red-team-review` use these

`proposal-writer` reads the convention doc that matches the proposal's `section_patterns` value (set in `working/proposal-type.md`) and applies the documented tone/cadence/heading norms. `red-team-review` Pink and Red passes check drafts against these norms (sentence-length distribution, bullet density, heading-numbering compliance, etc.) and flag deviations.

## Calibration discipline

When adding a new convention doc or updating an existing one against a new winning example:

1. Run `scripts/extract-pdf-patterns.py <source.pdf>` to get structural data
2. Identify generalizable patterns (heading numbering, sentence-length distribution, section ordering, bullet/figure density, customer-language usage)
3. Update or write the convention doc with the abstracted patterns
4. **Never quote, paraphrase, or store source-proposal prose** in any framework file. Convention docs describe structure, not content.
5. Cite the calibration source by date + vehicle type only (e.g., "Air Force IDIQ technical volume, 2026-04-23"). No company / customer names.
6. Run the smoke test to verify the framework references resolve.

## Adding a new vehicle's conventions

1. Acquire a winning author-owned example for that vehicle type
2. Pattern-extract using the script (see Calibration discipline above)
3. Write `reference/proposal-conventions/<vehicle-id>.md` matching the structure of [far-rfp.md](far-rfp.md)
4. Update the table above
5. Optionally update the matching `reference/section-patterns/<patterns-id>.md` file with calibrated frontmatter values
