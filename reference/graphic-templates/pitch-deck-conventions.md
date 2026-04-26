# Pitch Deck Conventions for SBIR & Federal Proposal Briefings

Calibrated structural conventions for SBIR pitch decks (Volume 5), federal-proposal kickoff briefings, and quad-chart-equivalent slide deliverables. Companion to [`reference/proposal-conventions/sbir.md`](../proposal-conventions/sbir.md) and [`reference/graphic-templates/illustrator-conventions.md`](illustrator-conventions.md).

**Calibration source:** Direct-to-Phase-II SBIR pitch deck (15 slides, 16:9 widescreen), 2026-04-25. Same author-owned source as the technical-volume + pricing calibration. No source content reproduced.

---

## 1. Slide-master and dimensions

### Aspect ratio: 16:9 widescreen

- **14.0 × 8.0 inches** is the calibrated source size (effectively 16:9)
- **NOT** PowerPoint default 13.33 × 7.5 (also 16:9 but slightly different ratio)
- **NOT** legacy 4:3 (10 × 7.5)
- The 14×8 ratio matches modern projector / VTC native aspect; safer for any presentation environment

When configuring `export-proposal` to render pitch decks, use `slide_width=14, slide_height=8` (in inches) unless the agency specifies otherwise.

### Layout strategy: "Title Only" everywhere

**Calibration shows 100% of slides used the "Title Only" layout** — every slide built as a custom canvas rather than using PowerPoint's pre-built layouts (Title and Content, Two Content, etc.).

**Why this works:**
- Pitch-deck slides are visual products — each slide solves a specific communication problem
- Pre-built layouts force content into placeholder shapes; custom canvas allows the illustrator to compose freely
- Brand consistency comes from the slide-master colors/fonts/footer, not from layout enforcement

**For your decks:** start every slide with "Title Only" layout. Place title, body, graphics, and brand elements as individual shapes on the canvas. Use slide-master to control colors, fonts, and footer/page-number positioning.

### Slide count: 15 slides for a Phase II pitch

Calibration: 15 slides total. Distribution by purpose (per the source):
- 1 cover slide
- 2 slides addressing each evaluation criterion (Criteria B + Criteria C explicitly titled)
- 12 content slides supporting the criteria

**For Phase II pitch decks, target 15-18 slides.** More signals padding; fewer leaves criteria under-defended.

---

## 2. Density cadence

Calibration shows **alternating slide density** — not every slide is dense. The density profile from the source:

| Slide | Shape count | Type |
|---|---|---|
| 1 | 2 | Cover (light) |
| 2 | 22 (with 11 images) | Team / company overview (very dense) |
| 3 | 3 | Criteria B intro (light) |
| 4 | 2 | Criteria C intro (light) |
| 5 | 25 | Detail framework (very dense) |
| 6 | 3 + 1 table | Compliance/criteria summary (light) |
| 7 | 7 | Mid-density |
| 8 | 16 | Dense content |
| 9 | 16 | Dense content |
| 10 | 22 | Very dense |
| 11 | 7 + 2 images | Mid-density with figures |
| 12 | 5 + 1 table | Light + table |
| 13 | 4 + 1 table | Light + table |
| 14 | 3 | Light |
| 15 | 3 + 1 table | Light + table (closing) |

**Pattern:** the deck alternates between **anchor slides** (16-25 shapes — the "look at this comprehensive view" moments) and **breath slides** (2-7 shapes — section openers, bullet summaries, single-graphic slides). Cognitive pacing.

**Anti-pattern:** every slide dense. Reviewer fatigue sets in by slide 5; the rest doesn't get attention.

---

## 3. Slide structure (canonical 15-slide SBIR pitch)

Calibrated against winning Direct-to-Phase-II pitch deck. Adapt section count for traditional Phase II or shorter formats.

### Slide 1 — Cover

- Company name + program/topic name + topic number
- Brand logo prominent
- Single hero image OR a brand pattern (subtle)
- Visual weight ~2 shapes — keep clean

### Slide 2 — Team / Company at a Glance (anchor slide)

- Company logo or wordmark
- 6-12 customer logos arrayed in a grid (with permission to display)
- Founding date, employee count, headquarters
- Optional: small map showing customer locations
- Optional: 2-3 key metrics (years in business, $ funded, customer count)
- ~20 shapes, 8-12 images

This is the **"who we are at a glance"** slide. High visual density is appropriate — evaluators want to absorb company context fast.

### Slide 3 — Criteria B Intro

- Title: "Criteria B: Ability to Accomplish work and Commercialize the Results"
- Sub-title or framing sentence
- Visual cue (icon or band) signaling section transition
- Light density (2-3 shapes)

### Slides 4-7 — Criteria B Content

- Team capability matrix (rows = capability, cols = evidence)
- Past performance summary (3-5 projects with logos + brief outcomes)
- Methodology / framework infographic
- Compliance/risk-management approach

### Slide 4 — Criteria C Intro

- Title: "Criteria C: Commercialization Potential"
- Sub-title or framing sentence
- Light density

### Slides 5-10 — Criteria C Content

- Market sizing (TAM / SAM / SOM funnel or equivalent)
- Customer-segment breakdown
- Sales channels / go-to-market
- Phase III transition path (named customers, named programs)
- Existing commercial revenue (with traction metrics)
- Pricing model summary

### Slides 11-13 — Schedule + Budget Summary

- Phase II schedule (Gantt or milestone diagram)
- Budget summary table (high-level — full pricing in Volume 1 workbook)
- Milestone payment schedule (links to MOU / cost volume)

### Slide 14 — Risks + Mitigations

- Top 3-5 risks
- Each with mitigation
- Light density (3-4 shapes)

### Slide 15 — Summary + Call to Action

- 3-5 reinforcement bullets
- Closing statement
- Contact info
- Light density

### Pattern: Criterion-mapped slide titles

A high-yield evaluator-friendly pattern: **explicitly title slides with the evaluation criterion they address**. Calibration source uses:

- "Criteria B: Ability to Accomplish work and Commercialize the Results"
- "Criteria C: Commercialization Potential"

This signals to evaluators reading the deck: "Here is exactly where we address criterion B; here is exactly where we address criterion C." Eliminates the search cost of mapping content to criteria.

For non-SBIR briefings (kickoff decks, OTA briefings), substitute the relevant evaluation factor: "Factor 1: Technical Approach", "Subfactor 2.1: Management", etc.

---

## 4. Typography hierarchy

Calibrated against the source deck. Theme-font-driven (the deck uses `+mn-lt` minor latin, the slide-master's body font, in 80%+ of text), with brand fonts (Verdana, Helvetica) for accents.

| Element | Estimated size | Style | Notes |
|---|---|---|---|
| Slide title | 32-44pt | bold | Theme heading font |
| Slide subtitle | 18-22pt | regular or italic | Theme heading font |
| Section/criterion intro title | 36-48pt | bold | Larger than content-slide titles for emphasis |
| Body text | 14-18pt | regular | Theme body font (Verdana acceptable for accent text) |
| Bullet points | 14-16pt | regular | Smaller than body where bullets are dense |
| Table cells | 11-13pt | regular | Smaller for density |
| Captions / footnotes | 10-12pt | italic | Brand color often applied |
| Footer / page number | 10pt | regular | Slide-master-driven |

**Font discipline:**
- 90%+ of text uses theme fonts (slide-master configured)
- Brand fonts (Verdana, Helvetica) reserved for distinctive elements: section headers, callouts, captions
- Avoid mixing 3+ font families on a single slide

---

## 5. Color and brand application

Pitch decks use the **same 5-role brand palette** as proposal documents (see [`reference/graphic-templates/illustrator-conventions.md`](illustrator-conventions.md) §6). Specific to pitch decks:

- **Slide-master sets the primary brand color and footer styling** — every slide inherits
- **Single accent color** used for slide-title underlines, section dividers, section-title backgrounds
- **Tile palette** (4-6 distinct colors) reserved for capability-tile slides or matrix slides
- **Light fill** for callout boxes, "key insight" panels, and table alternating rows

**Brand element placement:**
- Logo: typically top-right or footer-right (calibrated source uses footer placement)
- Page number: bottom-right, ~10pt
- Footer text: company name + slide title or topic # + date

---

## 6. Imagery norms

### Image-as-evidence pattern

Calibration shows images concentrated on **two slide types**:

1. **Team/Company overview slide** — 8-12 customer logos in a grid (proves reach + credibility)
2. **Architecture/system diagram slide** — 1-2 hero images (the actual product or system)

**Anti-pattern:** decorative stock photos (people in hard hats, abstract digital cityscapes, etc.). Federal evaluators are not impressed by stock imagery.

### Customer logo grid

Used on the team overview slide:
- 6-12 logos in a grid
- Equal-size cells
- Greyscale OR full-color (consistent — don't mix)
- Each logo is **factual evidence** ("we work with these customers"), not decoration

**Permission discipline:** Only display customer logos with that customer's permission. If you don't have permission, use a category tile ("DoD Service Branch") with no logo.

### System / architecture images

- 1 hero image per architectural concept slide
- Clean, vector-based, brand-aligned
- Should ideally be the **same style** as the architecture diagrams in the technical volume (parametric three-tier-architecture or capability-matrix from [`reference/graphic-templates/`](.))

---

## 7. Tables in pitch decks

Calibration shows 4 tables across 15 slides (slides 6, 12, 13, 15):

- **Slide 6** — Compliance/criteria summary table (often a 2-column "Criteria → Evidence" mapping)
- **Slide 12** — Schedule milestone table
- **Slide 13** — Budget rollup table
- **Slide 15** — Closing summary table

**Pitch-deck table conventions:**
- Smaller text than proposal-document tables (11-13pt vs. 9-10pt — pitch decks are projected, not printed)
- Header row in primary brand color, white bold text
- Alternating row shading subtle (5-10% grey)
- Bullet markers within cells: chevron `▶` or simple bullet `•`
- Maximum 8 rows visible without scrolling — denser tables go in the technical volume, not the pitch

---

## 8. Anti-patterns

- **Pre-built layout slides** (Title and Content, Two Content) — pitch decks should be Title Only with custom shapes
- **Stock photos** as decoration
- **>5 bullets per slide** of plain text — split into 2 slides, or convert to a graphic
- **Inconsistent slide-density** without rhythm — calibration shows alternating dense/light pacing; random density disorients
- **Tiny fonts** (<10pt) — projected text becomes unreadable below this
- **Too many tables** — pitch decks are visual; if you need >4 tables, you're in document territory
- **Generic slide titles** ("Approach", "Capabilities") — replace with criterion-mapped titles ("Criteria A: Technical Merit") or claim-style titles ("On-Device Inference Eliminates Cloud Risk")
- **Missing footer continuity** — every slide needs the same footer (logo, page #, optional date/topic)

---

## 9. Pink-team checklist (pitch-deck-specific)

- [ ] 16:9 widescreen aspect ratio (14×8 inches recommended)
- [ ] 100% Title Only layout (no pre-built content layouts)
- [ ] Slide count appropriate for format (15-18 for SBIR Phase II pitch; 8-12 for shorter briefings)
- [ ] Cover slide identifies company + program + topic # explicitly
- [ ] At least one team-overview slide with customer logos (with permission)
- [ ] Criterion-mapped slide titles for evaluation-criterion sections
- [ ] Density cadence — alternating dense/light slides, not uniform high density
- [ ] Theme fonts dominant; brand fonts only for accents
- [ ] Footer/page-number identical on every slide (slide-master-driven)
- [ ] No stock decorative photos
- [ ] Tables ≤4 per deck; ≤8 rows per table
- [ ] Architecture diagrams aligned visually with proposal-document graphics

---

## 10. Recommended Phase D template additions

Beyond the existing graphic templates, pitch decks would benefit from:

1. **`pitch-deck-cover-slide`** — single-slide template, 16:9, with placeholders for company/topic/date
2. **`team-overview-slide`** — multi-image grid layout with customer logos placeholders
3. **`criterion-intro-slide`** — large-title section divider for evaluation criterion mapping
4. **`milestone-schedule-slide`** — Gantt/timeline layout for Phase II schedule
5. **`compliance-criteria-table-slide`** — 2-column "Criterion → Evidence" mapping table

These would form a **pitch-deck-template-pack** consumable by `export-proposal --format pptx` to produce branded slide decks from structured data.

---

## 11. Calibration changelog

| Date | Source | Slides | Notes |
|---|---|---|---|
| 2026-04-25 | Direct-to-Phase-II SBIR pitch deck | 15 | Established 16:9 widescreen norm, "Title Only everywhere" layout strategy, density-cadence pattern, criterion-mapped slide titles, customer-logo-grid pattern, image-as-evidence discipline, theme-font-with-brand-accent typography |
