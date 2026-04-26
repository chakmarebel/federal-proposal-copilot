# Graphic & Illustration Conventions for Federal Full Proposals

Calibrated structural and styling conventions distilled from author-owned winning examples produced by professional proposal-design illustrators. Companion to `reference/section-patterns/full-proposal.md` and `reference/proposal-conventions/far-rfp.md`.

**Scope:** Layout patterns, typography hierarchy, color-palette structure, callout-box conventions, icon usage, complexity norms, and Pink-team checklist additions for graphics in FAR full proposals (FAR Part 15 RFPs, IDIQ task orders, CSO full proposals, BAA full proposals).

**Calibration source:** Air Force IDIQ technical volume, 52 pages, 2026-04-23. No source-proposal imagery stored in the repo; this doc captures only generalized structural patterns.

---

## 1. Page-level layout taxonomy

Federal full-proposal volumes use a small, repeatable set of page-level layouts. Identify which layout each page is, design accordingly.

### 1.1 Cover page

Single column, vertical hierarchy, generous whitespace.

```
┌──────────────────────────────────────────────────┐
│  [Logo]                          [decorative]    │
│  ────────                          [pattern]     │
│                                                  │
│           [Customer org / decision maker]        │
│           [Program / contract title]             │
│                                                  │
│              [Volume / step name]   ← accent     │
│                                                  │
│                [Solicitation #]                  │
│                  [Date]                          │
│                                                  │
│                                                  │
│  [POC LABEL]            [PREPARED FOR LABEL]     │
│  ─────────              ──────────────────       │
│  Name                   Name                     │
│  Phone                  Address                  │
│  Email                  Other                    │
│  Address                                         │
│                                                  │
│  CAGE / DUNS / UEI                               │
│                                                  │
│  ────────────────────────────────────────────    │
│  [Distribution restriction — small italic]       │
└──────────────────────────────────────────────────┘
```

**Element count:** ~6-8 distinct text blocks. Low complexity by design — the cover should feel composed, not crowded.
**Decorative elements:** at most one — usually a subtle abstract geometric motif in the upper corner that aligns with brand identity.
**Color discipline:** brand background + white text + ONE accent color used for ONE element only (typically the volume designator). Resist using accents in 2+ places.
**Typography:** company name largest, then customer block, then volume designator, then solicitation #/date. Ratio roughly 4:3:2:1.

### 1.2 TOC + List-of-Figures + List-of-Tables pages

```
┌──────────────────────────────────────────────────┐
│  [Header strip — see §2.1]                       │
│                                                  │
│        Table of Contents                         │
│                                                  │
│  1. Section ........................... 1       │
│  2. Section ........................... 2       │
│   2.1 Subsection ..................... 3        │
│     2.1.1 Sub-subsection ............ 4         │
│  ...                                             │
│                                                  │
│  List of Figures                                 │
│  Figure 1: [...]   ...................1         │
│  ...                                             │
│                                                  │
│  List of Tables                                  │
│  Table 1: [...]    ...................2         │
│  ...                                             │
│                                                  │
│  [Footer strip — see §2.2]                       │
└──────────────────────────────────────────────────┘
```

**Dot-leader convention:** Use `..............` between entry text and right-aligned page number. Word's TOC field handles this automatically when configured.
**Pagination:** Front-matter uses lowercase Roman (i, ii, iii, ...). Body switches to Arabic (1, 2, 3, ...). Distinct headers are common (the body's page-1 is the executive summary, not the TOC).
**Indent depth matches heading depth:** 4-level headings → 4-level TOC indents.
**Heading text matches exactly:** TOC entries include the bracketed solicitation references that appear in the body headings.

### 1.3 Body section page (single-column with optional callout)

The most common page type. ~70-80% of body pages.

```
┌──────────────────────────────────────────────────┐
│  [Header strip]                                  │
│                                                  │
│  X.Y.Z Section Title [PWS X.Y.Z]                 │
│                                                  │
│  Body paragraph 1 ...                ┌────────┐  │
│  ... lorem ipsum dolor sit amet,     │ Header │  │
│  consectetur adipiscing elit ...     ├────────┤  │
│                                      │ Side-  │  │
│  Body paragraph 2 ...                │ bar    │  │
│                                      │ body   │  │
│  Service Enablement: lead-in text +  │        │  │
│  body content ...                    └────────┘  │
│                                                  │
│  Issue Management: lead-in + body ...            │
│                                                  │
│  [Body paragraph 3 — full-width again]           │
│                                                  │
│  [Footer strip]                                  │
└──────────────────────────────────────────────────┘
```

**Sidebar / callout box:** see §3.2.
**"Lead-in label:" pattern:** bold red label followed by colon, inline with body, used to introduce a sub-theme without a numbered heading. Higher visual rhythm than pure prose.

### 1.4 Body section page with full-width figure

```
┌──────────────────────────────────────────────────┐
│  [Header strip]                                  │
│                                                  │
│  X.Y.Z Section Title [PWS X.Y.Z]                 │
│                                                  │
│  Body paragraph ...                              │
│  Body paragraph ... see Figure N below.          │
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │                                            │  │
│  │             [Figure N]                     │  │
│  │                                            │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Figure N: [Title]. [Action assertion sentence]  │
│                                                  │
│  Body paragraph continues ...                    │
│                                                  │
│  [Footer strip]                                  │
└──────────────────────────────────────────────────┘
```

**Figure placement:** Below the first text reference to it ("see Figure N"). Never floats orphaned at the top.
**Figure span:** Usually full text-column width. Half-page figures are acceptable when paired with adjacent narrative; quarter-page is rare.
**Caption directly below figure:** italic, two-part — see §5.

### 1.5 Compliance / matrix table page

Used for PWS-response tables, KPI summaries, and similar structured rollups.

```
┌──────────────────────────────────────────────────┐
│  [Header strip]                                  │
│                                                  │
│  Body lead-in paragraph (1-3 sentences)          │
│                                                  │
│  Table N: Title                                  │
│  ┌──────┬─────────────┬───────────────────────┐  │
│  │ Col1 │ Column Two  │ Column Three          │  │
│  ╞══════╪═════════════╪═══════════════════════╡  │
│  │ ...  │ ...         │ • bullet              │  │
│  │      │             │ • bullet              │  │
│  │      │             │ • bullet              │  │
│  ├──────┼─────────────┼───────────────────────┤  │
│  │ ...  │ ...         │ • bullet              │  │
│  └──────┴─────────────┴───────────────────────┘  │
│                                                  │
│  Body continues ...                              │
│                                                  │
│  [Footer strip]                                  │
└──────────────────────────────────────────────────┘
```

**Header row:** dark fill (navy/teal/brand), white bold text, no borders between cells — clean horizontal band.
**Alternating row shading:** light grey on every other row (very subtle, e.g., `#F4F6F9`).
**Cell padding:** generous (8-12 px equivalent).
**Bullets within cells:** small triangular / arrow / chevron marker, not standard round bullets. Indented ~6 px from cell-left.
**Column widths:** narrow ID columns (e.g., `PWS #` at ~8% width), wide content columns. Width ratio often 1:3:5 for a 3-column compliance table.

---

## 2. Header and footer strips (mandatory on every body page)

### 2.1 Header strip

Layout: left-anchor logo, center-anchor program identification, right-anchor solicitation #, thin divider rule below.

```
┌──────────────────────────────────────────────────┐
│ [logo] | Customer/Program Identification | Sol# │
│ ─────────────────────────────────────────── ───  │
└──────────────────────────────────────────────────┘
```

- **Logo (left):** Small mark only (~24-32 px height). Not the full wordmark. The brand element is identifying, not loud.
- **Program identification (center):** Customer abbreviation + program name in italic ~9-10pt. Carries the framework terminology of the customer (e.g., the customer's data principles spelled out: "Visible Accessible Understandable Linked Trusted (VAULT)").
- **Solicitation # (right):** Bold ~9-10pt with `Solicitation:` or `Sol:` lead-in label. Often in the brand accent color.
- **Divider rule:** Thin ~1pt rule in brand accent color (orange/red/teal). Sits just below the header text, separating it from the body.

### 2.2 Footer strip

```
┌──────────────────────────────────────────────────┐
│ Volume Designator           Date | Page N        │
│ Distribution restriction line — italic, smallest │
└──────────────────────────────────────────────────┘
```

- **Left:** Volume designator with bold step/section reference (e.g., "**Step 2**: Technical Approach").
- **Right:** Date + page number, separated by a small vertical bar `|`.
- **Bottom line:** Distribution restriction sentence in italic, smallest font (~7-8pt). Wraps to one line.
- **Separator:** Thin rule above the bottom line.

### 2.3 Continuity rule

The header and footer appear **identically on every body page** — same text, same position, only the page number changes. This builds reader trust ("I'm in the right document, on the right page") and supports skim navigation.

---

## 3. Graphic patterns (taxonomy)

The professional illustrator deploys a **small library of 6-8 patterns**, repeating them across the proposal. Each pattern carries a specific narrative job. Identify the pattern that fits the message; do not invent a new pattern unless the message genuinely requires it.

### 3.1 Three-tier band (already in framework)

See `reference/graphic-templates/three-tier-architecture/`. Used for: Enterprise → Theater → Tactical Edge architectures, hierarchical data flows, classification-boundary diagrams.

### 3.2 Right-floating callout box (sidebar)

Width: ~30-40% of text column. Floats right. Body text wraps around it on the left.

```
┌─────────────────┐
│ Title (bold,    │   ← navy/teal header bar with white bold italic title
│ italic, white)  │
├─────────────────┤
│ Body text in    │   ← light blue/grey background fill
│ light fill      │
│ (~10pt)         │
└─────────────────┘
```

**Used for:**
- Mini case studies (one paragraph, names a customer, names a result)
- Pull-quote-style highlights of a proof point
- "How we did this elsewhere" sidebar
- Reusable success stories

**Pink-team check:** every callout box should answer the question "would the evaluator be worse off if this were absent?" If yes, keep. If no (decoration only), cut.

### 3.3 N-column capability tiles

Horizontal row of 4-6 colored tiles, each identifying a category/capability/customer. Used for: program-portfolio summaries, capability heat maps, deployed-customer maps.

```
┌───────┬───────┬───────┬───────┬───────┬───────┐
│ Cat 1 │ Cat 2 │ Cat 3 │ Cat 4 │ Cat 5 │ Cat 6 │  ← color-coded
│ ─────  │ ───── │ ───── │ ───── │ ───── │ ───── │  header bars,
│ body  │ body  │ body  │ body  │ body  │ body  │  each tile a
│ text  │ text  │ text  │ text  │ text  │ text  │  different brand
│ [icon]│ [icon]│ [icon]│ [icon]│ [icon]│ [icon]│  color
└───────┴───────┴───────┴───────┴───────┴───────┘
```

**Each tile contains:**
- Header bar with category name (white bold, on colored fill)
- 2-4 sentences of body text
- One small icon (line or filled, geometric, unique per tile) bottom-right

**Color discipline:** each tile gets a distinct color from the brand palette. 4-6 tiles = 4-6 distinct accent colors. The colors aren't arbitrary — they correspond to a category meaning (e.g., one color for SOF, another for IC, another for Acquisitions).

**Icon discipline:** icons relate to category content (e.g., a chip for compute, a satellite for ISR, a pattern for data). Not decorative animals or abstract shapes.

**Used as the executive-summary anchor graphic** in the calibration source. Powerful as a "look at our breadth" opener.

### 3.4 Hub-and-spoke / orbital

Central concept (donut or circle), inner ring partitioned into 4 quadrants, outer spokes radiating to 6-10 sub-elements.

```
            ─[Subcat1]
           /
   [Subcat6] ─┐
              │       ┌──────────┐
              ├──────►│ Center   │◄──────┤[Subcat2]
              │       │ Concept  │
              │       │ (donut)  │
   [Subcat5] ─┘       └──────────┘ ─[Subcat3]
                          │
                       [Subcat4]
```

**Each spoke contains:**
- Small icon
- Bold short label (1-2 words)
- 3-4 short bullets (3-6 words each)

**Center concept:** Often a 4-quadrant inner ring (Plan / Execute / Monitor / Control or similar process model). Quadrants in different shades of the same brand color.

**Used for:** "all the things wrapped around a central concept" — typically a Program Management Office capability rollup, an integrated process model, or an enterprise-services overview.

### 3.5 Progression curve (maturity / state model)

Curved arrow showing progression from low-state to high-state, with named stages along the curve.

```
                                    [Stage N]
                                 ↗
                              [Stage N-1]
                           ↗
                        [Stage 4]
                     ↗
                  [Stage 3]
               ↗
            [Stage 2]
         ↗
   [Stage 1]
   ────────────────────────────────────────────►
   Maturity Axis
```

**Variants:**
- Add a "Chasm!" or "Inflection" annotation at the inflection point of the curve (e.g., where reactive analytics → predictive analytics)
- Add 3-4 question-style callout boxes positioned along the curve to label what each stage answers ("What happened?" → "Why?" → "What will happen?" → "What should we do?")
- Y-axis labeled (productivity, capability, value)
- X-axis labeled (time, maturity, investment)

**Used for:** narrative arcs ("here's where the customer is, here's where we'll take them"), educational framing ("here's the industry-standard maturity model and how we accelerate movement up it").

### 3.6 PWS-response compliance table

Used for FAR-style PWS-by-PWS commitment tracking. Three columns: PWS#, Requirement, Plan-to-meet.

See §1.5 for the layout. This is a TABLE, but its specific structure is a graphic pattern in its own right. Always include a `Table N: Title` line above with action-caption-style assertion.

### 3.7 Service / process model diagrams

Process flows with discrete stages, often with a feedback loop. Boxes connected by arrows; stages may be colored by phase.

```
[Stage 1] ──► [Stage 2] ──► [Stage 3] ──► [Stage 4]
   ▲                                          │
   └──────────────────────────────────────────┘
                  Feedback / Iterate
```

Used for: agile development cycles, data-pipeline stages, service-management lifecycle.

---

## 4. Typography hierarchy

Calibrated ratios from the source. Use these as starting points; brand specifications may override.

| Element | Estimated size | Style | Notes |
|---|---|---|---|
| Cover company name | 36-44pt | bold sans | Largest element on the cover |
| Cover customer / program | 20-26pt | semibold serif | ~60% of company name size |
| Cover volume designator | 14-16pt | bold | In the brand accent color |
| Cover sol# / date | 11-13pt | regular | Smallest cover text, label/value |
| H1 (e.g., "1. Executive Summary") | 14-16pt | bold | Below the header strip |
| H2 (e.g., "2.1 ... [PWS 1.0]") | 13-14pt | bold | Bracketed sol-ref carries here |
| H3 (e.g., "2.2.1 ... [PWS 2.1]") | 12-13pt | bold | |
| H4 (e.g., "2.2.1.1 ... [PWS 2.1.1]") | 11-12pt | bold | Often inline with first line |
| Body | 10-11pt | regular | Single-spaced |
| In-body lead-in label | 10-11pt | bold + accent color | "Service Enablement:" pattern |
| Bold inline emphasis | 10-11pt | bold | Customer-language terms, key phrases |
| Numbered list numbers (commitments) | 10-11pt | bold + accent color | Red bold for the "1.", "2.", etc. |
| Tables (cell text) | 9-10pt | regular | Slightly smaller than body |
| Tables (header row) | 9-10pt | bold + white | On dark fill |
| Captions | 9-10pt | italic | Two-sentence pattern, see §5 |
| Header strip program ID | 9-10pt | italic | |
| Header strip sol# | 9-10pt | bold + accent | |
| Footer strip page # | 9-10pt | regular | Right-aligned |
| Distribution line | 7-8pt | italic | Smallest text in the doc |

**Ratio summary:** title (4) : H1 (1.5) : H2 (1.4) : body (1.0) : caption (0.95) : distribution (0.75).

---

## 5. Caption convention (action-caption format)

Every figure and table caption follows a **two-part structure**:

```
Figure N: [Title — descriptive label, ends with period.] [Assertion sentence — what the graphic proves, italicized or roman, declarative voice.]
```

**Examples (generic):**
- `Figure 1: Octo's Current Support across the Air Force Data Enterprise. *Octo brings relevant mission experience to our technical approach and project execution.*`
- `Figure 11: Gartner Maturity Curve. *Team Octo's experience and expertise allow our customers to mature their analytics capabilities and increase productivity while avoiding the proactivity chasm that many organizations suffer during this transition.*`

**Pattern rules:**
- Caption begins with `Figure N:` or `Table N:` (bold).
- First sentence: descriptive title, ends with period.
- Second sentence: assertion of what the graphic *proves*, not what it shows. Italic optional but common.
- Caption directly below the figure/table, full text-column width, NOT inside the graphic.
- Caption always references a customer-relevant outcome or evaluation factor — never decorative.

This matches `reference/proposal-writing-patterns.md` Pattern 3 (Action Captions).

---

## 6. Color palette structure

Calibration source uses a 5-role brand palette. Federal-proposal palettes generally follow this structure:

| Role | Use cases | Calibration sample (approximate) |
|---|---|---|
| Primary brand | Cover background, header bars, table header rows, callout box headers | Deep navy / teal |
| Accent (single, dominant) | Volume designator, numbered-commitment digits, key emphasis, header divider, page number, sol# label | Red / coral (one specific shade) |
| Secondary brand | Decorative geometric patterns, section dividers | Lighter teal / steel-blue |
| Tile category palette | The 4-6 colors used in N-column capability tiles (one per category) | Distinct hues — orange, red, teal, green, blue, purple — matching brand family |
| Light fill | Callout box bodies, table alternating rows, sidebar backgrounds | Light blue-grey, very subtle |
| Body text | Body text, headings | Black / very dark navy |
| Background | Page background | White |

**Palette discipline:**
- **One accent color, used everywhere accents go.** Resist using two reds, an orange, and a coral. Pick one.
- **Tile palette is reserved for N-column capability tiles.** Don't use those colors elsewhere; it dilutes the cue.
- **Light fill is for backgrounds only**, never for text.
- **Body text is never colored** except for the inline lead-in labels (in accent color) — and even those should be used sparingly (~3-5 per page max).

Your `my-company/brand-palette.md` should declare these 5 roles and their hex values. The graphic templates read those role names, not specific hex values.

---

## 7. Icon usage discipline

- **Each icon represents a category, not decoration.** If you can't say "this icon means X," don't include it.
- **One style throughout the proposal.** Don't mix line icons + filled icons + 3D illustrations. Pick line OR filled, stay consistent.
- **Geometric / abstract preferred over photo-realistic.** Federal-proposal aesthetic is graphic, not photographic.
- **Size:** small (16-32px equivalent at 100% page scale). Icons are markers, not focal points.
- **Position:** within the tile they label (bottom-right corner), or to the left of a category label (acting as a bullet substitute), never floating in body text.
- **Provenance:** use brand-licensed icon sets (Font Awesome, Material Icons, Heroicons, custom). Never use random web-sourced icons; copyright concerns and visual inconsistency.

---

## 8. Element complexity norms

Calibrated density per page-type:

| Page type | Distinct elements | Notes |
|---|---|---|
| Cover | 6-8 | Generous whitespace; resist adding |
| TOC | 30-50 (entries) | Density acceptable; readability via dot leaders |
| Body section (text-only) | 1-3 paragraphs + lead-in labels | Most common page |
| Body section + sidebar | 1-3 paragraphs + 1 callout | Callout is one cognitive unit |
| Body section + figure | 1-2 paragraphs + 1 figure + caption | Figure span: full or 2/3 width |
| Capability-tile page | 4-6 tiles + 1-2 paragraphs body | High visual density; works as anchor |
| Hub-and-spoke graphic page | 1 graphic (8-10 spokes) + 1-2 paragraphs body | Graphic dominates; minimal body |
| Compliance table | 1 table (8-15 rows) + 1-3 paragraphs body | Table dominates |

**Anti-pattern: the everything-page.** Pages combining 3+ elements (callout + figure + table + multiple paragraphs of new content) are cognitive overload. Split.

---

## 9. Pink-team checklist additions (graphics)

Augments the existing Pink/Red/Gold checks in `red-team-review`. Validate every body page against:

- [ ] Header strip is present and identical to other body pages (logo, program ID, sol#)
- [ ] Footer strip is present (volume designator, date, page #, distribution restriction)
- [ ] Page number increments correctly (Roman in front matter, Arabic in body)
- [ ] Each figure has a Figure N: caption with action-caption second sentence
- [ ] Each table has a Table N: caption with descriptive title (assertion optional but recommended)
- [ ] Caption appears DIRECTLY BELOW the figure/table (not floating elsewhere)
- [ ] First in-text reference to the figure precedes the figure on the same page (or the page immediately prior)
- [ ] Callout boxes (sidebars) carry a distinct title and proof-point body, not decoration
- [ ] No graphic uses 3+ colors outside the brand palette
- [ ] Icons (if present) are from a single style family and represent categories, not decoration
- [ ] No "everything-page" — pages with 3+ heavy elements are split or simplified
- [ ] Graphics span full text-column width or are paired with adjacent narrative (no orphan half-page floats)

---

## 10. Recommended Phase D template additions

Calibration suggests these new parametric templates would have high reuse value. Listed in priority order based on observed frequency in winning proposals:

1. **`capability-tiles/`** (`section_patterns: capability-tiles`)
   - 4-6 horizontal colored tiles with header bar, body text, and icon
   - Schema: array of tiles (each with name, color_role, body, icon_id), title, caption
   - Highest reuse: works as Executive Summary anchor graphic

2. **`callout-sidebar/`** (a snippet rather than a full graphic — for inline embedding)
   - Title + body, navy/teal header with light-fill body
   - Schema: title, body, optional reference link
   - Inline embed within drafts/*.md → renders to floating sidebar in docx export

3. **`hub-and-spoke/`** (`section_patterns: hub-and-spoke`)
   - Center concept + inner-ring quadrants + 6-10 outer spokes
   - Schema: center (title, optional 4-quadrant labels), spokes (each: icon, label, 3-4 bullets)

4. **`maturity-curve/`** (`section_patterns: maturity-curve`)
   - Curved progression with N stages, optional inflection annotation, optional callout questions
   - Schema: stages (array of 4-8), axes (x/y labels), inflection (label, position), callouts (optional array)

5. **`pws-response-table/`** (a docx-friendly table, not a graphic)
   - 3-column compliance table (PWS#, Requirement, Plan)
   - Built into export-proposal docx output, sourced from compliance-matrix.json

These would extend the existing `three-tier-architecture/` and `capability-matrix/` templates from Phase D.1.

---

## 11. Calibration changelog

| Date | Source | Pages reviewed | New observations |
|---|---|---|---|
| 2026-04-25 | Air Force IDIQ technical volume | 1, 3, 8, 12, 19, 22, 27, 32 | Established this convention library: 7 graphic patterns (3 already templated, 4 proposed for future Phase D), header/footer strip pattern, 5-role color palette structure, two-part caption convention, "lead-in label" in-body pattern, anti-everything-page rule |
