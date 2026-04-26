# capability-matrix

Parametric graphic template for two- or three-column capability-to-evidence tables. Second most-used proposal pattern after three-tier-architecture — answers "what can you do and how do you prove it?" in a single scannable graphic.

## Visual

- **Dark canvas**, ~1200px wide, variable height (scales with row count).
- **Accent header row** — first column header has the red fill (draws eye to the capability column).
- **Alternating row backgrounds** for readability (panel / panel_alt).
- **Highlight row** option — one row per matrix can be flagged as the strongest proof point and gets accent tint treatment.
- **Footer strip** with brand / tagline / optional website, same style as three-tier.

Preview: open [example.html](example.html) in a browser. Renders without external resources.

## When to use

- **Capability → Evidence** mapping (most common): "We do X → here's the deployment / research / contract that proves it"
- **Capability → Requirement → Evidence** (3-column variant): map each requirement from Section M / PWS to a capability and its proof
- **Feature comparison** that's not head-to-head competitive (for competitive ghosting, use `differentiator-comparison` when shipped)

## When NOT to use

- **More than ~12 rows** — the table gets dense and unreadable. Split into two graphics or pick a different pattern.
- **Complex cells with multiple sub-items** — cells are single-paragraph. Nested lists or multi-paragraph prose don't render cleanly.
- **Time-based or sequential information** — use a timeline template (coming in `swim-lane-timeline`).
- **Hierarchical / tree-structured data** — use a different pattern; tables don't show hierarchy.

## Required data fields

See `schema.json` for the full contract.

- `title` (string) — top title
- `subtitle` (string, optional) — positioning sentence
- `columns` (array of 2-3) — header definitions, first typically accent
- `rows` (array of 3-12) — each with `cells` (must match column count), `row_class` (`""` or `"alt"` for striping), `highlight` (bool)
- `footer` — `brand`, `tagline`, optional `website`
- `theme` (optional) — color overrides

## Row styling notes

- Set `row_class: ""` for even-index rows, `row_class: "alt"` for odd-index rows. Produces subtle alternating stripe.
- Set `highlight: true` on **at most one row** — typically the most important proof point. Gets red tint + accent border. Using highlight on multiple rows dilutes the effect.
- For 3-column layouts, the first column (capability) is still the widest at 34% — that's fixed in template CSS.

## How `/proposal-graphics` uses this

Same flow as three-tier — resolve template (`my-company/` override > `reference/` default), assemble data against schema, validate, fill via `scripts/render-graphic.py`, write HTML + PNG.

For capability matrices specifically, the writer often pulls data from:
- `working/proposal-plan.json` → `discriminators` (each discriminator becomes a row)
- `my-company/evidence-ledger.json` → evidence entries matching each discriminator's `evidence_refs`

If Phase C evidence ledger is populated, the skill can auto-build a capability-matrix graphic from the discriminators without asking for row-by-row input.

## Anti-patterns

- **Don't exceed ~220 chars per cell.** Cells are single-line-wrapping; long prose overflows. For richer proof narratives, keep them in the draft text and cite the graphic briefly.
- **Don't use highlight for more than one row.** Accent treatment loses meaning.
- **Don't repeat information.** If every row says "deployed at USASOC," that's a message for the narrative, not a column value.
- **Don't title the graphic "Capability Matrix."** That's the template name, not a title. Use a title that makes an assertion: "Every Commitment Backed by Deployed Evidence" > "Capability Matrix."

## Rendering

```bash
python scripts/render-graphic.py \
  reference/graphic-templates/capability-matrix/template.html \
  reference/graphic-templates/capability-matrix/example-data.json \
  reference/graphic-templates/capability-matrix/example.html \
  --strict
```

## File inventory

| File | Purpose |
|---|---|
| [template.html](template.html) | Parameterized table with `{{placeholder}}` + `<!-- REPEAT -->` for columns and rows |
| [schema.json](schema.json) | JSON Schema defining required data fields |
| [example-data.json](example-data.json) | 6-row example data showing 2-column layout + one highlight row |
| [example.html](example.html) | Rendered output (open in browser to preview) |
| README.md | This file |
