# Portal Format Library

Web-form submission portals (DIANA, DIU CSO Phase 1, some SBIR topic portals, Challenge.gov, AFWERX Open Topics, xTech, NSIN prizes) impose their own section structure and hard character limits — often invisible until after registration. This library captures those portal formats so the next proposal against the same portal inherits the structure instead of rediscovering it.

## When a portal format belongs here

Add a file to this directory when **all three** conditions are true:

1. Submission is via a **web form**, not a document upload (i.e., you paste into fields rather than attaching a PDF).
2. The portal imposes **its own section labels and character/word limits** that differ from the solicitation PDF.
3. The format is **stable across proposals** — a one-off custom form for a single opportunity doesn't warrant a reference entry.

If the portal just accepts PDF uploads following Section L of the solicitation, it's not a portal format — it's a document-upload mechanism, and the section structure is in the solicitation itself.

## File naming

One file per portal or portal family. Use the portal's short name:

- `diana.md` — NATO DIANA challenge platform
- `diu-cso-brief.md` — DIU CSO Phase 1 solution brief portal
- `challenge-gov.md` — generic Challenge.gov template (varies per prize, flag variances)
- `afwerx-open-topic.md` — AFWERX Open Topic portal
- `valid-evaluation.md` — Valid Evaluation third-party platform

## Structure of a portal format file

Copy `_template.md` and fill in. Every file declares:

- Source provenance (where the info came from, when captured)
- Portal metadata fields (title limits, TRL selectors, system type enums)
- Section list with **hard character limits** (or word limits, or page limits)
- Image/attachment allowances
- Required agreements / declarations at submission
- Optional opt-outs that need a human decision
- Any formatting quirks (markdown support, line-break handling, Unicode, etc.)

## How skills consume portal formats

1. `/opportunity-quick-look` asks the "where does this go" question and flags web-form submissions.
2. If a portal format matching the opportunity already lives here, `/new-proposal` copies it into `inputs/00_priority/portal-format.md` automatically.
3. If no matching format is on file, `/capture-portal-structure` runs — guided capture after the user registers for the portal — and produces both the proposal-local `portal-format.md` **and** a draft entry for this library (for the next run).
4. `/proposal-manager` gates on the presence of `inputs/00_priority/portal-format.md` when `submission_mechanism: web-form` is declared on the proposal type. It refuses to plan a proposal without knowing the section limits.
5. `/proposal-writer` reads per-section character budgets from `portal-format.md` and writes to budget.

## Adding a new portal format

1. Copy `_template.md` to `<portal-id>.md`.
2. Fill in every section — don't leave placeholders.
3. Test once against a real draft to confirm character limits match what the portal enforces (client-side vs. server-side, with/without markdown).
4. Commit. The next proposal against this portal inherits the captured format.

## Portals on file

| File | Portal | Submitting body | Last verified |
|---|---|---|---|
| [diana.md](diana.md) | NATO DIANA | DIANA (Defence Innovation Accelerator for the North Atlantic) | 2026-04-23 |
| _template.md | (blank template) | — | — |
