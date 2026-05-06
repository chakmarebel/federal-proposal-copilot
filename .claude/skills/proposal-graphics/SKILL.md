---
name: proposal-graphics
description: Use this skill to create proposal-ready architecture graphics, anchor graphics, and figure concepts with PowerPoint/Figma-ready structure. Reads from working/ files and writes graphic specs to working/graphics-brief.md.
---

# Proposal Graphics Skill

## Purpose
Translate the solution into clear visuals that strengthen evaluator understanding.

## Inputs
Read from:
- `working/storyboard.md` (if it exists) — **primary driver.** Each section storyboard names a "Graphic Argument" stating what the figure must prove. Build graphics from those arguments, not from architecture alone.
- `working/solution-strategy.md`
- `working/architecture-concept.md`
- `drafts/technical-approach.md` (if drafting has begun)
- Any existing visual standards, brand templates, or reference graphics in `inputs/05_graphic_standards/`

**Workflow position:** runs after `/proposal-storyboard`, not before. If `working/storyboard.md` is absent, warn and recommend running storyboard first — graphics built without knowing the section arguments tend to decorate rather than prove.

## Output
Write to `working/graphics-brief.md` with one section per graphic containing:
1. Graphic objective
2. Figure title
3. One-paragraph explanation
4. ASCII wireframe
5. Component list
6. Layout instructions for PowerPoint/Figma
7. Color/grouping logic
8. **Action caption** (see below — mandatory, not description)
9. **What this graphic proves** (one sentence — this is what `proposal-writer` cites and what Gold Team verifies)

### Action Caption Standard (mandatory)

Per `reference/proposal-writing-patterns.md` Pattern 3, every graphic gets an **action caption** — text placed under (not inside) the graphic stating what the graphic *proves*, not what it shows.

Structure:
- **Figure number + short title** (document reference)
- **What the graphic proves** (one sentence asserting the evaluative point)
- **Where it's substantiated** (section or source reference)

**Write action captions in `working/graphics-brief.md`. Do NOT embed captions inside the HTML graphic.** Captions live in the Word doc text so the writer can control numbering, cross-references, and formatting.

**Example:**

Bad (description):
> *Figure 3. System architecture.*

Good (action):
> *Figure 3. Three-tier architecture eliminates cloud dependency.* Edge-only inference paths carry all mission-critical operations; enterprise connectivity is used only for model updates, shown to be optional in §4.2. Source: deployed configuration at [customer].

If you can't write an action caption for a graphic, the graphic has no evaluative point — reconsider whether it should exist.

## Design Rules
- One graphic = one core idea
- Use left-to-right or top-down flow
- Avoid crossing lines
- Reduce text inside boxes
- Group related elements clearly
- Distinguish:
  - Your company's components
  - Partner-provided components
  - Government-provided components
  - External systems/data

## Default Color Logic — Brand Palette
Use your company's brand palette unless the customer specifies otherwise. Update these values to match your brand:
- **Background:** `#191c20` (near-black)
- **Primary accent:** `#ee2929` (brand red) — titles, accent bars, pills, hero elements, glow effects
- **Dark grey:** `#393939` — borders, dividers, secondary structure
- **Medium grey:** `#9f9f9f` — secondary text, subtitles, captions
- **Light grey:** `#c8c8c8` — body text, descriptions
- **White:** `#ffffff` — headings, primary labels
- **Red tint backgrounds:** `rgba(238,41,41,.08)` to `rgba(238,41,41,.15)` — hero tier fills, callout backgrounds
- **Red accent borders:** `rgba(238,41,41,.4)` — commitment callouts, emphasis boxes

### Tier Treatment (for architecture graphics)
- **Enterprise tier:** `#2a2d31` fill, `#393939` stroke
- **GCC tier:** `#2a2d31` fill, `#393939` stroke
- **Edge/Tactical tier (hero):** `rgba(238,41,41,.08)` fill, `#ee2929` stroke — visually emphasized

### Element Patterns
- Title bars: white text, `border-bottom: 2px solid #ee2929`
- Registry/badge pills: `#ee2929` fill, dark text
- Commitment callouts: `rgba(238,41,41,.08)` fill, `#ee2929` border
- Glow filters: `flood-color: #ee2929`
- Row accent bars: 4px wide, `#ee2929`

## Template Dispatch (v1.5 Phase D — mandatory first step)

Before generating HTML from scratch, **check whether the requested pattern has a parametric template**. Templates produce identical visual quality in seconds at ~200-500 tokens vs. free-form HTML generation at ~5-10k tokens with variable quality.

### Lookup order

Given a graphic request (typically from `working/graphics-brief.md`), identify the pattern name. Resolve in this order:

1. **`my-company/graphic-templates/<pattern>/`** — user's branded override (gitignored)
2. **`reference/graphic-templates/<pattern>/`** — framework default (in-repo)
3. **Fall back to free-form HTML generation** if no template matches

### Pattern matching

Match the request to a template by name (e.g., "three-tier architecture" → `three-tier-architecture`) or by description keywords:

| Request keywords | Likely template |
|---|---|
| "three tier", "enterprise / gcc / edge", "three-band architecture", "DDIL boundary" | `three-tier-architecture` |
| "capability matrix", "capability to proof", "capability table", "requirement-to-capability" | `capability-matrix` |
| "timeline with gates", "swim lane", "phased execution", "milestone timeline" | `swim-lane-timeline` *(not yet shipped — falls back)* |
| "lifecycle loop", "continuous cycle", "four-node diamond" | `lifecycle-loop` *(not yet shipped — falls back)* |
| "technical vs operational", "objectives split", "numbered objectives side-by-side" | `objectives-split` *(not yet shipped — falls back)* |
| "us vs them", "differentiator comparison" (ghosted, never named) | `differentiator-comparison` *(not yet shipped — falls back)* |

Currently shipped templates (v1.5 Phase D.1):
- [`three-tier-architecture`](../../../reference/graphic-templates/three-tier-architecture/) — three horizontal tiers with boundaries and registry pills
- [`capability-matrix`](../../../reference/graphic-templates/capability-matrix/) — 2- or 3-column capability-to-evidence table

If no template exists for the requested pattern, fall through to free-form HTML generation (the pre-v1.5 flow) and note in `working/graphics-brief.md` that a parametric template should be built for this pattern in Phase D's next iteration.

### Template-mode workflow

When a template matches:

1. Read `<template_root>/schema.json` for the data contract
2. Read `<template_root>/example-data.json` for a known-good starting point
3. Assemble data for this specific graphic — pulling from:
   - `working/graphics-brief.md` (user intent / figure description)
   - `working/proposal-plan.json` (win themes, discriminators for capability-matrix rows)
   - `my-company/evidence-ledger.json` (evidence entries for proof-point columns)
   - `my-company/brand-palette.md` (theme color overrides)
   - Inline user prompts for anything not derivable
4. Validate data against `schema.json` (all required fields present, array lengths match min/maxItems)
5. Write data to `graphics/fig<N>-<pattern>.data.json` for reproducibility / iteration
6. Render via `python scripts/render-graphic.py <template> <data> <output.html> --strict`
7. Render PNG at 2× DPI via headless Chrome → `graphics/rendered/fig<N>-<pattern>.png`
8. Write the graphic's brief entry in `working/graphics-brief.md` including the action caption

### When to override in `my-company/graphic-templates/`

If your brand palette differs materially from the framework default (dark canvas with red accent), or you want a different visual treatment for a pattern, copy the framework template to `my-company/graphic-templates/<pattern>/` and modify freely. The skill picks up your override automatically. Framework updates to the reference version won't touch your override.

## Output Formats

Three stages — graphics move from spec → HTML → PNG:

1. **Spec in `working/graphics-brief.md`** — ASCII wireframe, component list, layout instructions, color mapping, action caption, "what this graphic proves"
2. **Rendered HTML in `graphics/`** — browser-viewable HTML files that produce the actual graphic. HTML is the editable master; if a revision is needed, edit the HTML, not the PNG.
3. **PNG rendering in `graphics/rendered/<name>.png`** — produced at 2x DPI via headless Chrome, for Word embed. The final submission artifact for Word insertion.

The `graphics/` directory is top-level (peer to `drafts/`, `working/`, `reviews/`), NOT inside `inputs/`, because rendered graphics are outputs, not inputs.

### HTML → PNG rendering

Use headless Chrome to render each `graphics/*.html` to `graphics/rendered/<name>.png`. Windows command:

```bash
chrome --headless --disable-gpu --screenshot="graphics/rendered/fig1-architecture.png" \
       --window-size=2400,1600 --device-scale-factor=2 \
       "file:///absolute/path/to/graphics/fig1-architecture.html"
```

Target sizing:
- **Logical size:** 1200 × 800 (landscape) or 1000 × 1200 (portrait)
- **Device scale factor:** 2 (for print-quality Retina output)
- **Final PNG size:** 2400 × 1600 (landscape) — embeds at **6.5" wide** (full column on 8.5×11 page with 1" margins) by default. See "Legibility for 8.5×11 proposal embedding" below for the canvas/embed sizing rule that drives all minimum font sizes.

Run this step at the end of graphic creation. `/export-proposal` will verify each PNG exists and regenerate any missing ones before building the Word doc.

### Optional PowerPoint briefing

When the proposal type or user requests a briefing deck (e.g., OTA kickoff briefing, executive summary slides), `/export-proposal` can wrap the PNGs into a PowerPoint deck. The graphics skill does not produce PPTX directly — it produces the reusable PNG components, and the export step orchestrates the deck assembly via `anthropic-skills:pptx`.

## Critical Rules
- **Write specs to `working/graphics-brief.md`**
- **Write rendered HTML graphics to `graphics/`** (top-level, not inside `inputs/`)
- **Render each HTML to PNG in `graphics/rendered/`** at 2x DPI before calling graphics done
- **Never embed action captions inside the graphic** — captions live in the Word doc text so the writer can control numbering and cross-references
- **Every graphic must be legible when embedded in an 8.5×11 proposal at full-column width** — see "Legibility for 8.5×11 proposal embedding" below for the binding rule. Non-negotiable.

## Legibility for 8.5×11 proposal embedding (mandatory)

**Target: ≥10pt rendered body text** for any graphic embedded in an 8.5×11 federal proposal. Headings ≥12pt, titles ≥18pt, captions ≥9pt. Below these thresholds the graphic fails the print-legibility test and gets flagged by White Glove review.

### The pixel-to-point math

For a canvas of `W` logical pixels embedded at `E` inches wide, each logical pixel renders at `(E × 72) ÷ W` points.

Solve for the logical pixel size needed: `logical_px = target_pt × W ÷ (E × 72)`.

> ⚠ **Why this matters:** the framework's earlier default — 1200-logical-px canvas embedded at 5" wide — produced **0.30 pt per logical pixel**, so an 18px label rendered as a 5.4pt sliver. That is illegible on paper. Always pick a canvas + embed combination from the table below.

### Recommended canvas + embed combinations

| Canvas (logical px) | Embed width | px/pt ratio | Min body (10pt) | Min heading (12pt) | Min title (18pt) |
|---|---|---|---|---|---|
| **1200 × 800** | **6.5" (full column)** ← default for hero figures | 0.39 pt/px | **26px** | **31px** | **46px** |
| 1000 × 700 | 5.0" (half column / two-up) | 0.36 pt/px | 28px | 33px | 50px |
| 800 × 500 | 3.25" (inline / quarter column) | 0.29 pt/px | 34px | 41px | 62px |

**Default for hero architecture figures:** 1200 × 800 canvas embedded at 6.5" wide (full column on a standard 8.5×11 page with 1" margins). Use this unless space dictates a smaller embed.

### Minimum font sizes (1200×800 canvas at 6.5" embed — the default)

- **Title:** 46–54px (≥18pt)
- **Section heading:** 31–38px (≥12pt)
- **Body / label text:** 26–30px (≥10pt)
- **Caption / secondary:** 24–28px (≥9–10pt) — never below 24px
- **Footer / brand strip:** 22px minimum

These minimums are non-negotiable for federal proposal embedding. Anything below 24px in body/label position fails White Glove review.

### Verifying after rendering

After PNG render, open the PNG at 100% in an image viewer sized so the image fills ~6.5 inches of screen width (or print a test page). If body text isn't readable from arm's length, the graphic fails — increase font sizes in the HTML and re-render before declaring graphics done.

## Lessons Learned (Calibration Session — White Paper Graphics)

### Sizing & Legibility
- **8.5×11 print is the target.** See the "Legibility for 8.5×11 proposal embedding" section above for the binding rule. Body text below ~10pt rendered (24px logical at the default canvas/embed) is unreadable on paper.
- **Earlier guidance was undersized.** Prior versions of this skill recommended 17–19px body text on a 1200-canvas at 5" embed, which renders as ~5.4pt. That guidance is superseded — use the canvas + embed table above.
- **Minimize whitespace aggressively.** Compact layouts read better at small sizes. Remove spacer elements, reduce padding, tighten gaps.
- **Test text overflow.** Long labels ("Automated LoRA & Fine-Tuning Platform") will overflow small SVG boxes. Always check that text fits within its container.

### Design Patterns That Worked
- **Three-tier architecture:** Horizontal bands stacked vertically, registry pills between tiers, dashed boundary lines with centered labels, flow arrows with tight text labels. Keep it to one scannable page.
- **Lifecycle loop:** Four nodes in a diamond with circular arc arrows. Flow label boxes sit beside the arcs, not on them. Center element holds the key concept.
- **Two-column layout:** Products vs. Services, Technical vs. Operational — column header carries the category, no per-item badges needed. Cleaner and more space-efficient.
- **Capability rows:** Left label column with red accent bar + right description. No emoji icons — accent bars are cleaner and more professional.
- **Swim lane timeline:** Three horizontal rows (Deploy/Adapt/Measure) with phase columns. Gate markers as diamonds below. Commitment callouts highlighted with brand red.

### Anti-Patterns to Avoid
- **Emoji icons in professional graphics.** Replace with accent bars, numbered circles, or simple geometric markers.
- **Text overlapping arrows or boundary lines.** Move labels above/below or into separate callout boxes beside the arrows.
- **IL-level badges (IL-5, IL-6) and DDIL zone badges inside boxes.** These clutter the graphic — mention in the caption text instead.
- **Figure numbers in the graphic title.** Captions with figure numbers belong in the document text, not the graphic itself.
- **Off-brand accent colors.** Stick to your brand palette. Avoid adding colors that aren't in your brand guide.
- **Key metric taglines at bottom of graphics.** These belong in the body text, not the graphic.

### Workflow
1. Write the spec to graphics-brief.md first (wireframe + layout instructions)
2. Build the HTML rendering immediately after — don't wait for approval of the spec alone
3. Show the HTML to the user for feedback
4. Iterate on the HTML directly — specs are reference, HTML is the deliverable
5. Captions are written separately for inclusion in the Word document
