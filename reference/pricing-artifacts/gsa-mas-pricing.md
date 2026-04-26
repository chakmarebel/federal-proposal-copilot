---
artifact_id: gsa-mas-pricing
output_files:
  - drafts/price-narrative.md → final/docx/price-narrative.docx
  - working/pricing-inputs.md
  - final/xlsx/pricing-workbook.xlsx
companion_file: working/pricing-inputs.md
mental_model: Map solicitation labor categories to your already-approved GSA Schedule rates. Don't build new rates — show the crosswalk and let the workbook compute the totals.
must_not_produce:
  - DCAA-auditable rate buildups (rates are pre-approved by GSA)
  - Indirect rate certifications
  - SBIR-style phase budget structure
  - DFARS data rights assertions (use FAR Part 12 commercial-item terms instead)
---

# GSA MAS Pricing Artifact

## Mental model

GSA MAS pricing is **fundamentally different from SBIR or FAR cost volumes** because the rates already exist on your approved Schedule. Your job in a Schedule-flighted task-order or BPA competition is:

1. **Map the solicitation's labor categories** to your already-approved Schedule labor categories
2. **Apply your approved Schedule ceiling rates** (or any agency-specific discount you've agreed to)
3. **Compute total prices** by labor category × hours × period

The price narrative is **2-3 pages of formal contracting language**. The numerical work happens in a single-sheet xlsx attachment. Together they form the price submission.

This is **not** the same as a direct Schedule offering (where you establish rates with GSA in the first place). For Schedule offerings, calibrate against an actual Schedule submission first; this template covers task-order/BPA-flighted competitions only.

## Two-artifact split: narrative + workbook

| Artifact | Purpose | Format |
|---|---|---|
| Price narrative (Vol 2) | Formal contracting declarations + LC mapping table | PDF (typically 2-3 pages) |
| Pricing workbook (Vol IV) | Numerical rates and totals per LC × period | xlsx (single sheet typical) |

Both are required. The narrative establishes the contracting context; the workbook delivers the numbers.

---

## Required inputs

### Company / contracting identifiers
- Company legal name + DBA name (if any)
- GSA Contract Number (format: `47QTCA[YEAR]D[serial]`, e.g., `47QTCA19D00FF`)
- CAGE Code
- DUNS Code
- Tax ID
- Size of Business (Small / Other Than Small + applicable categories like SDVOSB, WOSB, HUBZone)
- Validity Period of Quote (typically 90 days from submission)
- Company Point of Contact (Name, Title, Phone, Email)
- Payment Terms (Net 30 standard for GSA)

### Labor category mapping
- Solicitation's labor category names (e.g., "Software Engineer - Principal", "Software Engineer - Senior", "Software Engineer - Mid")
- Your approved GSA Schedule labor category names (e.g., "Software Engineer 4", "Software Engineer 3", "Software Engineer 2")
- The mapping rationale (1:1 by skill level, by years-of-experience equivalence, etc.)

### Pricing data
- Approved GSA Schedule ceiling rates per labor category (hourly, fully loaded)
- Estimated hours per LC × period (period typically year-by-year over the BPA/IDIQ ceiling)
- Any agency-specific discount applied (typical 0-15% off ceiling)
- Any Other Direct Costs (ODCs) — usually minimal in GSA MAS competitions

### Solicitation amendments
- List of all RFQ amendments received (Amendment 1, 2, ...) — required for "Acknowledgement of Amendments" section

---

## Price narrative structure (Vol 2)

Calibrated against winning examples — typically 2 pages.

### Section 1 — Company Information

Bulleted list of contracting identifiers (see "Required inputs" above). One bullet per item.

### Section 2 — Price Narrative

Lead-in paragraph: brief description of the GSA MAS basis for the pricing.

```
[Company] is providing pricing for the [Solicitation Reference, e.g., "Attachment 2 — Price Quote
Template"] under our existing [GSA Schedule reference, e.g., "GSA MAS IT Category"] contract
[GSA Contract Number]. The [N] labor categories defined in the [Solicitation Reference]
correspond to GSA Schedule labor categories as described in this section.
```

**Table 1: Labor Category Mapping** — 2-column table:

| Solicitation Labor Category | Offeror's GSA Schedule Labor Category |
|---|---|
| [Sol LC 1] | [Schedule LC 1] |
| [Sol LC 2] | [Schedule LC 2] |
| [Sol LC 3] | [Schedule LC 3] |

Closing paragraph (2-3 sentences): describe how rates were derived (Schedule ceiling, applicable discount, period escalation if any), and note that the actual numerical pricing is provided in the attached workbook.

### Section 3 — Acknowledgement of Amendments

Brief, formal:

```
[Company] acknowledges receipt of the following amendments to [Solicitation Reference]:
- Amendment 1, dated [Date]
- Amendment 2, dated [Date]
- ...
```

Or if none:

```
[Company] acknowledges no amendments have been issued to [Solicitation Reference] as of
[Date of Submission].
```

---

## Pricing workbook structure (Vol IV)

Calibrated against winning examples — typically a single-sheet xlsx workbook.

### Single-sheet layout

| Element | Pattern |
|---|---|
| Top-of-sheet | Workbook header marking — typically "unclassified" in row 1 |
| Header rows (rows 2-5) | RFQ#, Company name, GSA Contract #, Period of Performance |
| Body — Labor by LC × Period | Rows for labor categories; columns for periods (years 1-5 or task-order base + options) |
| Subtotal rows | `=SUM(<column range>)` to total each period |
| Grand total row | `=SUM(<period subtotals>)` for total ceiling |
| ODC section (if applicable) | Typically below labor; same period-column structure |
| Final total | Labor + ODC = Total Quote |

### Calibrated formula patterns

| Pattern | Frequency | Use |
|---|---|---|
| `=SUM(CELL:CELL)` | Most common | Column / row rollups |
| `=ROUND(CELL*N,N)` | Second most | Rate × hours rounded to currency precision |
| `=CELL` | Pass-through | Reference between worksheets or sections |
| `=CELL*CELL` | Direct | Rate × base computation |
| `=SUM(CELL,CELL,CELL,CELL)` | Discrete | Non-contiguous cell summation (e.g., total across non-adjacent CLINs) |

**Use `=ROUND(CELL*N,N)` rather than plain `=CELL*N` for rate × hours calculations.** ROUND prevents floating-point drift in cost summaries — the difference between `$1,234,567.89` and `$1,234,567.890000004` matters when a CO is comparing against a budget cap.

### Number format conventions

| Format | Calibrated frequency | Use |
|---|---|---|
| `"$"#,##0.00` | Primary currency | Dollar amounts (simple format, no parens for negatives) |
| `0.00%` | Percentage | Discount percentages, escalation rates |
| `0.00` | Plain decimal | Hours, quantities |
| `0000` | Padded integer | CLIN numbers (e.g., 0001, 0002) |
| `d-mmm-yy` | Date | Period-of-performance date references |
| `General` | Default | Untyped cells |

**Note: GSA MAS pricing uses simple `"$"#,##0.00` currency format** — different from SBIR pricing's accounting format `_("$"* #,##0.00_);_("$"* \(#,##0.00\)...`. The reasoning: GSA MAS rates are pre-approved and don't include negative amounts; simple currency is sufficient.

### Workbook-level conventions

- **Single sheet** typical (not 4 like SBIR's milestone-payment workbook)
- **No frozen panes, no auto-filter** — print/export-ready
- **9-15 merged cell ranges** acceptable for section headers
- **`unclassified` marking** in row 1 — required for any unclassified pricing artifact (other classification levels would mark differently)
- **No external sheet references** — all data in one sheet (different from SBIR where Pricing references Indirects sheet)

---

## Output discipline

When `/export-proposal` runs against a `gsa-mas-pricing` artifact:

1. Generate `final/docx/price-narrative.docx` from the price-narrative draft
2. Generate or copy through `final/xlsx/pricing-workbook.xlsx` — populated from `working/pricing-inputs.md` if no agency template was provided in `inputs/00_priority/`
3. Both deliverables must be present in the final/ submission package
4. The xlsx workbook should match the formula and format conventions documented above

**Do NOT produce:**
- DCAA-auditable rate buildups (rates are pre-approved by GSA — don't re-justify them)
- SBIR-style phase budget structure (this isn't a phased prototype)
- Indirect rate certifications (covered by your Schedule submission)
- DFARS Data Rights assertions (FAR Part 12 commercial-item terms apply by default)

If the user asks for any of those, push back: "GSA MAS pricing is a Schedule-rate-mapping exercise, not a cost buildup. Do you actually need a different vehicle (FAR Part 15) for this work?"

---

## Pitfalls

- **Building rates from scratch** — your Schedule rates are already approved. Don't re-derive them; map and apply.
- **Discount inconsistency** — if you offer the agency a discount off Schedule, apply it consistently across all LCs in the workbook. Discount-by-LC is acceptable but should be explained in the narrative.
- **LC mapping ambiguity** — every solicitation LC must map to exactly one Schedule LC. If your Schedule doesn't have a matching LC, you cannot offer that solicitation LC (or you must add it via Schedule modification first).
- **Wrong currency format** — using SBIR's accounting format `_("$"* #,##0.00_);_("$"* \(#,##0.00\)...` in a GSA pricing workbook signals SBIR conditioning. Use simple `"$"#,##0.00`.
- **Forgetting amendment acknowledgement** — all RFQ amendments must be explicitly acknowledged in the price narrative. Missing amendments = noncompliant.
- **Period escalation drift** — if you're offering year-1 / year-2 / year-3 / etc., escalation between years should match what your Schedule allows (typically 0% or a small annual %). Verify against your Schedule terms.

---

## Calibration source

NGA SABER II Price Volume + Pricing Workbook (Vol 2 + Vol IV), 2026-04-25. Single-sheet workbook (107 rows × 11 cols), 254 formulas dominated by SUM/ROUND/multiplication patterns, simple `"$"#,##0.00` currency format throughout.
