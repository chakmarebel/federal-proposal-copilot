# Graphics (Rendered Output)

Rendered HTML/SVG graphics live here. This is a **first-class output directory** alongside `drafts/`, `working/`, and `reviews/`.

## What goes here

- Rendered HTML files produced by `/proposal-graphics` (e.g., `fig1-architecture.html`, `fig2-timeline.html`)
- `rendered/` subdirectory — PNG screenshots of the HTML at 2x DPI, produced by headless Chrome. Used for Word embed via `/export-proposal`.

## What does NOT go here

- **Input visual standards / brand templates** — put those in `inputs/05_graphic_standards/`
- **Graphic specs / wireframes / briefs** — put those in `working/graphics-brief.md` (they're analysis, not rendered output)
- **Draft narrative text** — put that in `drafts/`

## File naming

Use descriptive, ordered filenames so graphics match their figure numbers in the written proposal:

```
fig1-architecture.html
fig2-deployment-timeline.html
fig3-capability-matrix.html
```

## Captions

**Do not embed captions inside the graphic HTML.** Captions live in the Word doc text so the writer can control numbering, cross-references, and formatting. Action captions are written in `working/graphics-brief.md` and pulled into `drafts/` by `/proposal-writer`.

See `reference/proposal-writing-patterns.md` Pattern 3 for the action-caption standard.
