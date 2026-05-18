---
name: compliance-check
description: Diff requirements against draft coverage and update the compliance matrix. Run after proposal-writer, before red-team-review. Reads working/compliance-matrix.md + drafts/; writes reviews/compliance-gaps.md.
phase: review
composes: [proposal-manager, proposal-writer]
conflicts_with: [red-team-review]  # don't score proposal quality; that's red-team-review's job
---

# /compliance-check

## Purpose

Ensure every "shall" from the solicitation has a home in the draft. Closes the loop between `proposal-manager` (which seeds the matrix) and `proposal-writer` (which should be filling it). Produces a **gap list** that red-team treats as P0 findings.

## When to run

- After each `proposal-writer` pass (checks whether new drafts closed open reqs)
- Before every `red-team-review` invocation (Pink is mostly this, but formal)
- Before final submission (as a gate — zero `Gap` rows, all rationales in place)

## What it reads

- `working/proposal-type.md` — for `compliance_sources` and the skipped check
- `working/compliance-matrix.md` — the seeded + updated matrix
- `drafts/*.md` — to verify actual coverage
- `working/proposal-plan.md` — for cross-check of eval criteria

## What it writes

- **Updates** `working/compliance-matrix.md`:
  - Recomputes the Status column for every row by scanning `drafts/`
  - Regenerates the Summary counters block at the bottom
  - Updates the `Last updated` field
- **Updates** `working/compliance-matrix.json` — structured sidecar conforming to [`reference/schemas/compliance-matrix.schema.json`](../../../reference/schemas/compliance-matrix.schema.json). Written atomically on every run, fully regenerated from the current `.md` state plus the draft scan. Required fields:
  - `schema_version: "compliance-matrix.v1"`
  - `generated_by: "compliance-check"`
  - `generated_at`: ISO-8601 timestamp
  - `proposal_name`, `type_id`, `compliance_sources` (from `working/proposal-type.md`)
  - `rows` — every matrix row with `req_id`, `source`, `requirement`, `section`, `page`, `status`, `evidence`, and (Phase C) `evidence_refs`
  - `summary` — counters derived from the rows
- **Creates/overwrites** `reviews/compliance-gaps.md` with:
  - Total + counters
  - Gap list (requirements with Status = `Gap`)
  - Planned-but-undrafted list (Status = `Planned` AND at least one draft exists)
  - Partials (Status = `Partial`)
  - Exception log (Status = `Exception` — verify rationale present)
  - Recommendations per finding
- **Creates/overwrites** `working/compliance-matrix.xlsx` — sortable/filterable Excel version for sharing with teammates. Delegate to `anthropic-skills:xlsx` using the spec at `reference/office-templates/compliance-matrix-template.md`. The xlsx reads from the JSON sidecar (not re-parses markdown) for consistency. This runs on every `/compliance-check` invocation, not just on export, so teammates always have a current spreadsheet. (The final submission-package copy at `final/xlsx/compliance-matrix.xlsx` is produced by `/export-proposal` and may be styled differently per branded template.)

### `.md`, `.json`, `.xlsx` all stay in sync

Every `/compliance-check` run produces all three forms from the same in-memory representation. Humans can hand-edit the `.md` between runs (to flip a row to Exception, add Evidence, etc.); on the next run, those hand edits are preserved in the regenerated `.md` and propagated to `.json` + `.xlsx`. Do not hand-edit the `.json` or `.xlsx` — they're derived.

## Algorithm

1. Read `working/proposal-type.md`. If `compliance_sources` is empty list, exit with:
   > Skipped: proposal type `<type_id>` has no compliance sources. No matrix expected.

2. Read `working/compliance-matrix.md`. If it doesn't exist, exit with:
   > No compliance matrix found. Run `/proposal-manager` first to seed it.

3. For each row in the matrix:
   - If Section is blank and no draft references the Req ID → **Gap**
   - If Section is assigned but no draft file exists for that section → **Planned**
   - If a draft file exists and contains the Req ID (or its verbatim phrase, case-insensitive, first 50 chars) → search for substantive treatment (heading, paragraph ≥50 words that mentions key terms) → **Drafted** or **Covered** based on completeness heuristic
   - If Section is assigned but draft mentions the req only in passing → **Partial**
   - If user previously flipped to **Exception**, preserve it but require non-empty Evidence column (otherwise flag)
4. Recompute counters. Update the matrix file.
5. Write `reviews/compliance-gaps.md` with gap/partial/exception lists and recommended owner for each (proposal-writer for Gaps, humans for Exceptions).

## Coverage heuristic (substantive treatment)

A requirement is **Covered** (not merely Drafted) when the draft:
- Contains a heading or sub-heading that addresses it, AND
- Has ≥50 words of substantive discussion mentioning the requirement's key nouns/verbs, AND
- If the req uses "shall describe/provide/demonstrate," the draft has a matching descriptive/demonstrative passage

If uncertain, mark **Drafted** (not Covered) and flag for human review.

## Output discipline

- Do not invent coverage. If unsure, mark `Partial` or `Drafted`, not `Covered`.
- Do not silently drop rows. If the matrix has rows from a prior proposal-manager pass that don't appear in current drafts, they stay as `Planned` or `Gap`.
- Never rewrite the Requirement verbatim column — that's the source text.

## On completion

Append to `working/activity.md`:

```
## <timestamp> — compliance-check — <N total>: <covered>C / <drafted>D / <planned>P / <gap>G → reviews/compliance-gaps.md
```

Then tell the user the headline counts and the #1 gap to close first.
