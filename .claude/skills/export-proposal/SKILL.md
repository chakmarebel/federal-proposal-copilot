---
name: export-proposal
description: Package proposal deliverables into native Microsoft Office formats (Word, Excel, PowerPoint) for review cycles and final submission. Reads working/proposal-type.md to determine which formats this type needs, converts .md drafts to .docx, pricing/compliance data to .xlsx, and optional briefings to .pptx. Uses the anthropic-skills docx/xlsx/pptx skills for conversion. Writes to the final/ directory. Use after drafting is stable and Gold Team has been run — export is the submission-prep step, not the authoring step.
---

# /export-proposal

## Purpose

Federal proposal work reviews in Word, prices in Excel, and briefs in PowerPoint. The authoring layer is markdown (humans + Claude collaborate best there), but the *delivered* artifacts must be native Office formats. This skill is the bridge.

**When to run:** After drafting is stable, compliance-check is clean (or has only documented Exceptions), and at least Pink + Red team passes have run. Export is the last step before submission, not a mid-draft step.

**Workflow:** `.md` → `.docx`/`.xlsx`/`.pptx` → (user-initiated) `.pdf` via Word's Save as PDF. The skill does not produce PDF directly — Word's native PDF export preserves formatting and styling in a way markdown-to-PDF converters do not.

## Inputs

1. `working/proposal-type.md` — declares what artifacts this type produces. Drives format dispatch.
2. `drafts/*.md` — narrative sections to convert to Word
3. `working/compliance-matrix.md` — converts to Excel (sortable, filterable, shareable with teammates)
4. `working/pricing-inputs.md` — raw numbers for any Excel pricing artifact
5. `graphics/*.html` — rendered graphics (convert to PNG for Word embed)
6. `reviews/gold-team-scorecard.md` — optional export for internal review
7. `my-company/templates/*.{docx,xlsx,pptx}` — optional branded base templates (see Branded Templates below)

## Format Dispatch by Proposal Type

Different types need different export bundles. Read `working/proposal-type.md` and apply this dispatch:

| Type | Primary .docx | .xlsx artifacts | .pptx artifacts |
|---|---|---|---|
| `far-rfp` | Tech Vol + Mgmt Vol + PP Vol (separate docs) | Cost Volume, Compliance Matrix, Rate tables | Optional kickoff brief |
| `idiq-to` | Task Order Response | Cost Volume, Compliance Matrix | Optional |
| `cso-brief` | Solution Brief (single doc) | ROM workbook (simple), Compliance Matrix | — |
| `cso-full` | Full Proposal (single doc) | Commercial pricing table, Compliance Matrix | — |
| `baa` | Technical Volume + Cost Volume | Cost Volume detail, Compliance Matrix | — |
| `ota-white-paper` | White Paper (single doc) | ROM | — |
| `ota-proposal` | Full Proposal | Milestone Payment Schedule, Compliance Matrix | Often required: milestone brief deck |
| `sbir-phase1` | Technical Volume | **SBIR Budget (xlsx is the primary pricing artifact)**, Compliance Matrix | — |
| `sbir-phase2` | Technical Volume + Commercialization Plan | SBIR Budget xlsx, Compliance Matrix | Optional transition brief |
| `white-paper` | White Paper (single doc) | — | Optional |
| `rfi` | RFI Response | — | — |
| `sources-sought` | Sources Sought Response | Relevant Experience table (optional) | — |
| `rom` | ROM Document | ROM workbook (optional, if ranges are numerous) | — |

## Process

### Step 1: Preflight

1. Read `working/proposal-type.md`.
2. Check that drafts exist in `drafts/`. If empty, exit with: "No drafts to export. Run `/proposal-writer` first."
3. Check Gold Team status. If `reviews/gold-team-scorecard.md` doesn't exist, warn but proceed: "Gold Team has not been run. Recommend `/red-team-review --mode=gold` before final export."
4. Check compliance. If `reviews/compliance-gaps.md` shows `Gap` rows, warn: "N unresolved compliance gaps. Confirm Exceptions are documented before submission."
5. Check for branded templates at `my-company/templates/`. If present, use them as base. If not, use professional defaults (documented below).

### Step 2: Scaffold `final/`

Create (if not exists):

```
final/
├── docx/             ← Word documents
├── xlsx/             ← Excel workbooks
├── pptx/             ← PowerPoint decks (if any)
├── pdf/              ← User-produced PDFs via Word (placeholder dir)
├── graphics-png/     ← Rendered graphics for Word embed
└── PACKAGE.md        ← Manifest of every deliverable, its source, and its format
```

### Step 3: Render graphics to PNG

For each `graphics/*.html`:
- Use headless Chrome (or equivalent) to render to PNG at 2x DPI for print quality
- Write to `final/graphics-png/<name>.png`
- Preserve the action caption separately (it goes in the Word doc text, not the image)

### Step 4: Convert drafts to Word (.docx)

For each Word document in the Format Dispatch table:

1. Determine which `drafts/*.md` files belong to this document (per type's section_patterns and the proposal-plan's recommended structure)
2. Concatenate in order, applying section heading hierarchy
3. Insert graphics: where the draft says `See Figure N` or references `graphics/figN-*.html`, replace with embedded `final/graphics-png/figN-*.png` + the action caption from `working/graphics-brief.md` as Word caption-styled text below the image
4. Delegate to `anthropic-skills:docx` for the actual conversion, passing:
   - The concatenated markdown
   - The base template path (from `my-company/templates/` or default)
   - Figure→PNG mapping
   - Style overrides for proposal-specific needs (CAGE/UEI in header, page numbering, etc.)
5. Write to `final/docx/<document-name>.docx`

**Do NOT auto-convert to PDF.** Instruct the user: "Open `final/docx/<name>.docx` in Word and use File → Save As → PDF. Word's native PDF export preserves styling, fonts, and embedded graphics in a way markdown-to-PDF converters do not."

### Step 5: Produce Excel artifacts (.xlsx)

**5a. Compliance Matrix → xlsx (always, when matrix exists)**

Delegate to `anthropic-skills:xlsx`. Convert the 7-column table in `working/compliance-matrix.md` to a workbook with:
- Sheet 1: "Matrix" — all rows, with filter dropdowns on Source, Status, Section
- Sheet 2: "Summary" — the counter block as a small dashboard
- Sheet 3: "Gaps" — filtered view of any Gap/Partial/Exception rows
- Conditional formatting: Covered = green, Drafted = blue, Planned = yellow, Partial = orange, Gap = red
- Write to `final/xlsx/compliance-matrix.xlsx`

**5b. Pricing artifact → xlsx (when `pricing_artifact` in proposal-type is `sbir-budget` or `far-cost-volume`)**

For `sbir-budget`:
- Use `reference/office-templates/sbir-budget-template.md` as the spec (or `my-company/templates/sbir-budget-template.xlsx` if present)
- Populate with values from `working/pricing-inputs.md`
- Agencies often provide their own required spreadsheet — if `inputs/00_priority/` contains an agency budget template (any `.xlsx`), use that as the base instead
- Write to `final/xlsx/sbir-budget.xlsx`

For `far-cost-volume`:
- Use `reference/office-templates/cost-volume-appendix-template.md` as the spec
- Populate the CLIN × Period × Cost Element cube from `working/pricing-inputs.md`
- Include BOE hour tables as additional sheets
- Write to `final/xlsx/cost-volume-appendix.xlsx`

For `ota-milestones`:
- Milestone schedule renders fine in Word (it's small), but also produce an xlsx companion for PMO tracking
- Write to `final/xlsx/milestone-schedule.xlsx`

For `rom`, `cso-commercial`, `none`: skip xlsx pricing export.

### Step 6: PowerPoint briefing (optional)

Only if the type or user explicitly requests it (e.g., `ota-proposal` often has a kickoff brief requirement):

1. Use the graphics PNGs + win themes from `working/proposal-plan.md` to build a 5-10 slide deck
2. Delegate to `anthropic-skills:pptx`
3. Write to `final/pptx/<name>-brief.pptx`

### Step 7: Package manifest

Write `final/PACKAGE.md`:

```markdown
# Submission Package — [Proposal Name]

**Type:** [type_id]
**Exported:** [timestamp]
**Gold Team pWin:** [from scorecard, if present]
**Compliance status:** [N Covered / M Drafted / K Planned / J Gap]

## Deliverables

| File | Source | Format | Purpose |
|---|---|---|---|
| `docx/technical-volume.docx` | drafts/technical-approach.md + drafts/management-approach.md + graphics PNGs | Word | Primary narrative, reviews in Word, submits as PDF |
| `xlsx/compliance-matrix.xlsx` | working/compliance-matrix.md | Excel | Team coordination + submission appendix |
| `xlsx/sbir-budget.xlsx` | working/pricing-inputs.md | Excel | Primary pricing artifact (SBIR) |
| `graphics-png/fig1-architecture.png` | graphics/fig1-architecture.html | PNG (2x) | Embedded in Word |
| ... | | | |

## Submission Checklist

- [ ] Open each `docx/` file in Word; review formatting; Save As PDF to `pdf/`
- [ ] Verify xlsx files open without errors
- [ ] Verify graphics PNGs are legible at target print size
- [ ] Confirm compliance matrix shows zero `Gap` rows
- [ ] Confirm Gold Team rewrites have been applied
- [ ] Confirm proposal-type.md `page_target` is met (spot-check page count in Word)
- [ ] Cover page + CAGE/UEI/NAICS populated
- [ ] File naming matches agency submission requirements
```

### Step 8: Activity trail

Append to `working/activity.md`:

```
## <timestamp> — export-proposal — <N docx>, <M xlsx>, <K pptx>, <J PNG> → final/PACKAGE.md
```

## Branded Templates (optional, recommended)

If you drop your own branded Office templates at `my-company/templates/`, export-proposal uses them as the base:

| File | Used for |
|---|---|
| `my-company/templates/proposal-template.docx` | Word base — cover page style, heading hierarchy, fonts, colors, footer (CAGE/UEI) |
| `my-company/templates/pricing-template.xlsx` | Excel base — company-branded budget/cost templates |
| `my-company/templates/briefing-template.pptx` | PowerPoint base — slide master with logo, colors, layouts |

If any file is missing, a professional default is used (see `reference/office-templates/` for the defaults).

## Rules

- **Do not produce PDF automatically.** Word → PDF is a user step. The skill produces docx; the user opens Word and saves as PDF.
- **Do not embed HTML graphics in Word.** Always convert HTML → PNG first.
- **Do not regenerate content.** Export reads what's in `drafts/` — it does not re-write, re-summarize, or improve. If content is wrong, fix it in `.md` and re-export.
- **Never overwrite `my-company/templates/`.** Those are user-provided.
- **Always emit `final/PACKAGE.md`** — it's the artifact index for the submission.
- **Never remove or modify `drafts/`.** The markdown is the source of truth; exports are derived.
- **Single run = complete package.** Don't do partial exports that leave `final/` in a half-updated state. If a step fails, fail cleanly and leave `final/` empty.

## After Running

Tell the user:
1. What was produced (counts by format)
2. What to do next (open Word, review, save as PDF)
3. Any warnings (missing Gold Team, unresolved gaps, missing branded templates)
4. Path to `final/PACKAGE.md` as the index
