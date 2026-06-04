---
name: export-proposal
description: Package proposal deliverables into native Microsoft Office formats (Word, Excel, PowerPoint) for review cycles and final submission. Reads working/proposal-type.md to determine which formats this type needs, converts .md drafts to .docx, pricing/compliance data to .xlsx, and optional briefings to .pptx. Uses the workspace's shared Python converters (tools/md_to_docx.py, tools/compliance_to_xlsx.py) for .docx/.xlsx and anthropic-skills:pptx for briefings. Writes to the final/ directory. Use after drafting is stable and Gold Team has been run — export is the submission-prep step, not the authoring step.
phase: submission
composes: [proposal-editor, red-team-review, proposal-graphics]
conflicts_with: []  # unique submission-packaging role
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
5. **Pre-submit gate (blocking).** Run the prose and structural lints against the drafts before producing any Office output:

   ```bash
   python scripts/prose-lint.py --proposal <slug>
   python scripts/lint-document-structure.py --proposal <slug>
   ```

   `prose-lint.py` exits 1 on a HIGH finding — the section-sign glyph, an em-/en-dash or `--` used as sentence punctuation, or internal process vocabulary (e.g. "storyboard", "gold team", "narrative spine") leaking into customer-facing prose. `lint-document-structure.py` exits 1 on duplicate section numbers, broken figure references, or a missing classification/distribution marking. **If either exits 1, stop and report the findings — do not render `final/` output.** Surface advisory prose-lint findings (marketing words, self-narration / performative-honesty commentary, prohibited-claim diction without a ledger cite, forbidden absolutes) to the user but do not block on them. After the Word docs are rendered (Step 4), re-run the structural lint and `check-strengths.py --target docx` against `final/docx/` per CLAUDE.md's pre-submit gate.

6. Check for branded templates at `my-company/templates/`. If present, use them as base. If not, use professional defaults (documented below).

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

**Use the shared Python conversion script — do NOT delegate to anthropic-skills:docx.**

The workspace ships a tested, proposal-agnostic converter at `tools/md_to_docx.py` (uses `python-docx`). Invoke it via Bash:

```bash
cd "C:/Users/wbal9/Claude Code Projects/federal-proposal-assistant"
python tools/md_to_docx.py --proposal <slug>
```

This produces:
- `final/docx/<stem>.docx` for every `.md` file in `drafts/` (individual files)
- `final/docx/full-proposal-combined.docx` — all sections in alphabetical order, page-break separated

**Common overrides:**

```bash
# Explicit file order (when alpha sort is wrong):
python tools/md_to_docx.py --proposal <slug> \
  --files sec1-technical-approach.md sec2-management.md sec3-past-performance.md

# Combined only, custom name:
python tools/md_to_docx.py --proposal <slug> \
  --mode combined --combined-name "technical-volume"

# Individual files only (skip combined):
python tools/md_to_docx.py --proposal <slug> --mode individual
```

**White paper heading normalization.** When `proposal_type: white-paper`, the converter applies a heading demotion pass before the standard mapping:
- `# H1` (title) → Word Body Text (paragraph style, not Heading 1)
- `## H2` → Word Heading 3
- `### H3` → Word Heading 4
- `#### H4` → Word Heading 4 (same level — white papers rarely go deeper)

This matches the expected white-paper docx output without requiring manual heading demotion in Word.

**Standard markdown → Word mapping (all other types):**
- `# H1` through `###### H6` → Word heading styles 1–6
- `**bold**`, `*italic*`, `***bold-italic***`, `` `code` `` → inline runs
- `- bullet` / `1. numbered` with leading spaces for nesting → List Bullet / List Number
- `| table |` pipe tables → Table Grid style, bold first row, auto column widths
- ` ``` ` fenced code blocks → verbatim monospace, auto-sized to fit the column
- `> blockquote` → indented italic (used for action captions)
- `<!-- figure: NAME -->` → embeds `graphics/rendered/NAME.png`, centered, fit to column
- other `<!-- comments -->` stripped; `---` separators and `*Note:` lines skipped

**After the script runs:** Tell the user to open the `.docx` in Word, review formatting, then use **File → Save As → PDF**. Do NOT produce PDF directly — Word's PDF export preserves styling; markdown-to-PDF tools do not.

**Optional HTML preview.** `python scripts/render-md-to-html.py --proposal <slug>` renders the narrative drafts to self-contained HTML in `final/html/` — a screen-review format that keeps graphics as crisp vector (HTML/SVG) rather than rasterized PNG. It is a review aid, not a submission format; the submission deliverable remains the `.docx`.

### Step 5: Produce Excel artifacts (.xlsx)

**5a. Compliance Matrix → xlsx (always, when matrix exists)**

**Use the shared Python script — do NOT delegate to anthropic-skills:xlsx.**

```bash
cd "C:/Users/wbal9/Claude Code Projects/federal-proposal-assistant"
python tools/compliance_to_xlsx.py --proposal <slug>
```

This reads `working/compliance-matrix.md` and produces `final/xlsx/compliance-matrix.xlsx` with:
- Sheet 1 "Matrix" — all rows, auto-filter dropdowns, color-coded Status column
  (Covered = green, Drafted = blue, Planned = yellow, Partial = orange, Gap = red)
- Sheet 2 "Summary" — counts by status
- Sheet 3 "Gaps" — filtered view of Gap / Partial / Exception rows

**5b. Pricing artifact → xlsx (when `pricing_artifact` in proposal-type is `sbir-budget` or `far-cost-volume`)**

For `sbir-budget`:
- Check if an agency-provided budget template exists in `inputs/00_priority/` (any `.xlsx`). If yes, populate that template with values from `working/pricing-inputs.md` using openpyxl.
- If no agency template, build from scratch using the line items in `working/pricing-inputs.md`.
- Write to `final/xlsx/sbir-budget.xlsx`.

For `far-cost-volume`:
- Build a CLIN × Period × Cost Element workbook from `working/pricing-inputs.md`.
- Include BOE hour tables as additional sheets.
- Write to `final/xlsx/cost-volume-appendix.xlsx`.

For `ota-milestones`:
- Produce an xlsx milestone schedule companion for PMO tracking.
- Write to `final/xlsx/milestone-schedule.xlsx`.

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

### Step 7b: Edit-readiness flag file (white paper only)

When `proposal_type: white-paper`, write `final/edit-readiness.md` after the package manifest. This gives the user a single checklist of items that require human confirmation before submission:

```markdown
# Edit Readiness — [Proposal Name]

The following items require human confirmation before submitting. Export is complete; these are the things the tool cannot verify.

- [ ] **POC** — Is the point-of-contact name and email correct? (Current: [name from draft])
- [ ] **Distribution statement** — Is the classification / distribution statement appropriate for this audience?
- [ ] **Version of record** — Is this the version you intend to submit? (Exported: [timestamp])
- [ ] **Headline numbers** — Are the key statistics (cost figures, benchmark percentages) verified against primary sources?
- [ ] **Recipient** — Is the submission address / recipient confirmed?
```

Populate the bracketed fields from the draft content where available.

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
