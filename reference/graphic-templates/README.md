# Graphic Templates (Parametric)

Phase D of v1.5. Pre-built, tested HTML layouts for common proposal graphic patterns. AI fills placeholders; layout is deterministic. See [docs/v1.5-plan.md](../../docs/v1.5-plan.md).

## Why parametric

Today's `proposal-graphics` skill writes fresh HTML/CSS from scratch for every graphic. Output varies run-to-run, token cost is ~5-10k per graphic, render bugs are common (overlapping text, misaligned boundaries), and brand consistency drifts across proposals.

Parametric templates change that. The AI only generates structured data (JSON); the layout comes from a pre-tested HTML template. Result: identical visual quality every time, ~200-500 tokens per graphic, zero layout bugs, brand palette baked in.

## Precedence (same pattern as `reference/office-templates/`)

When `/proposal-graphics` renders a graphic, it looks for a template in this order:

1. **`my-company/graphic-templates/<pattern>/`** — your branded override (gitignored; local to your machine)
2. **`reference/graphic-templates/<pattern>/`** — framework default (in this directory)
3. **Fall back** to the existing "AI writes HTML from scratch" flow if no template matches

This is additive — nothing breaks. Untouched patterns keep their current behavior.

## Template file structure

Every pattern under `reference/graphic-templates/<pattern>/` must contain:

```
<pattern>/
├── template.html       ← the parameterized layout
├── schema.json         ← JSON Schema for what the data JSON must supply
├── example-data.json   ← a real data file that fills the template
├── example.html        ← rendered output from example-data.json (open in browser to preview)
└── README.md           ← when to use, anti-patterns, required fields summary
```

## Placeholder syntax

Minimal — no templating engine. Claude (or a ~10-line Python helper) can evaluate these via regex:

| Syntax | Meaning |
|---|---|
| `{{field}}` | Substitute with `data["field"]` |
| `{{a.b.c}}` | Dotted path: `data["a"]["b"]["c"]` |
| `{{array.0.name}}` | Array index: `data["array"][0]["name"]` |
| `<!-- REPEAT:items -->` ... `<!-- END:REPEAT -->` | Render the inner block once per item in `data["items"]`; use `{{item.field}}` inside |

When positions are SVG-coordinate-dependent (each item must go at a different x/y), use indexed flat placeholders (`{{tiers.0.name}}`) instead of REPEAT blocks. REPEAT blocks are for table-row / list patterns where items flow naturally.

## How `/proposal-graphics` uses this

1. Read `working/proposal-type.md` and `working/graphics-brief.md`
2. Identify the requested pattern (user specifies by name or by description — e.g., "three-tier architecture")
3. Resolve to a template: check `my-company/graphic-templates/<pattern>/` first, then `reference/graphic-templates/<pattern>/`
4. Read the template's `schema.json` to know what data fields are needed
5. Assemble data from the graphics-brief, proposal-plan (win themes, discriminators), and inline user input
6. Validate data against the schema
7. Fill the template (string substitution) → write to `graphics/fig<N>-<pattern>.html`
8. Render to PNG via headless Chrome → `graphics/rendered/fig<N>-<pattern>.png`

## Templates shipped in Phase D.1

| Pattern | Status | Typical use |
|---|---|---|
| [three-tier-architecture/](three-tier-architecture/) | ✅ shipped | Enterprise / GCC / Tactical Edge diagrams; three-band architectures with boundaries between bands |
| [capability-matrix/](capability-matrix/) | ✅ shipped | Products × services / capabilities × customer-needs comparisons; two-column accented header layout |

## Templates deferred to on-demand

Built next time a real proposal needs that pattern:

| Pattern | Trigger |
|---|---|
| `swim-lane-timeline` | Execution timeline with parallel workstreams + go/no-go gates |
| `lifecycle-loop` | Four-node diamond with circular arrows and a center concept label |
| `objectives-split` | Technical vs. operational objectives side-by-side with numbered items |
| `differentiator-comparison` | Us vs. generic competitor pattern (ghosted — never name competitors) |

Deferred ≠ unimportant. The framework supports them; they just aren't built yet. When a real proposal calls for one, build it, use it, ship it. Each takes ~3-4 hours once the framework pattern is familiar.

## Adding a new template

1. Create `reference/graphic-templates/<pattern>/` with all 5 files
2. Add a row to the table above
3. Open `template.html` in a browser to verify the example data renders cleanly
4. Run the smoke test — it validates every template dir has the required 5 files

## Design conventions (for new templates)

- **Half-page print is the target.** Word embed at ~5" wide. Minimum font sizes: titles 28px, headings 22px, body 17-19px, captions 14px.
- **Dark canvas is the framework default** — works well for technical proposal graphics and prints with strong contrast. User overrides in `my-company/graphic-templates/` may use light canvas or any palette that matches your brand.
- **Action captions live OUTSIDE the graphic** — in the Word doc text, not inside the HTML. See `reference/proposal-writing-patterns.md` Pattern 3.
- **SVG for any vector content** (arrows, boundaries, flow lines). Inline CSS in `<style>` blocks. No external dependencies.
- **Self-contained file** — no external images, no CDN fonts, no network requests. Renders identically on every machine.
