---
name: status
description: Show the current state of the active proposal — proposal type, stages completed, open compliance gaps, and the next recommended command. Reads working/proposal-type.md, working/activity.md, working/compliance-matrix.md, and working/proposal-plan.md. Writes nothing. Use when returning to a proposal after time away, deciding what to do next, or checking progress before a review.
phase: inspection
composes: [proposal-manager, compliance-check]
conflicts_with: [dashboard]  # per-proposal CLI summary; use dashboard for portfolio-wide view
---

# /status — Proposal state at a glance

## Purpose

Federal proposals are multi-week efforts. Coming back to one on day 12 is expensive if you can't see what's done, what's open, and what's next. `/status` answers that in one shot without writing any new files.

## What it reads

- `working/proposal-type.md` — proposal type, required skills, skipped skills, pricing artifact
- `working/activity.md` — chronological log of skill invocations
- `working/compliance-matrix.md` — requirement coverage (if present)
- `working/proposal-plan.md` — eval criteria, win themes, bid/no-bid (if present)
- `drafts/` — which sections have been drafted
- `reviews/` — which review passes have run

## What it outputs

Prints a terminal-friendly summary. Does **not** write files. Structure:

```
═══════════════════════════════════════════════════════════
 PROPOSAL STATUS — <proposal name>
═══════════════════════════════════════════════════════════

Type:       <display_name>  (<type_id>)
Customer:   <from proposal-brief or customer-profile>
Due:        <from proposal-plan if available>
Mode:       <Full Capture | Responsive>

─── Pipeline ──────────────────────────────────────────────
[✓] opportunity-quick-look      2026-04-18 — PASS
[✓] proposal-manager            2026-04-19 — 37 reqs extracted
[✓] customer-intel              2026-04-19
[✓] competitor-assessment       2026-04-20 — 3 competitors profiled
[✓] capture-scorecard           2026-04-20 — 6G 2Y 1R — GO
[✓] proposal-solution-architect 2026-04-21
[ ] proposal-graphics           — not started
[ ] past-performance            — SKIPPED for this type
[ ] pricing-analyst             — not started (ROM required)
[ ] proposal-writer             — not started
[ ] red-team-review             — not started

─── Compliance coverage ───────────────────────────────────
37 requirements total
  ✓ Covered in drafts:    0
  ⚠ Planned, not drafted: 37
  ✗ Gaps (no owner):      0

─── Drafts ───────────────────────────────────────────────
(no draft files yet)

─── Reviews ──────────────────────────────────────────────
(no review files yet)

─── Next recommended action ──────────────────────────────
→ /proposal-graphics       (next required skill for this type)

  Other available:
  → /pricing-analyst       (required for rom pricing artifact)
  → /proposal-writer       (blocked until architecture + graphics complete)
```

## How to run

1. Confirm a proposal is active. Current proposal is the working directory, or the one matching `$ARGUMENTS` if provided (e.g., `/status mystic-depot`).
2. Read the files listed above. Any missing file → mark that stage as not started; do not fail.
3. Build the pipeline table by matching `required_skills` from `working/proposal-type.md` against entries in `working/activity.md`. Skills in `skipped_skills` render as `SKIPPED for this type`.
4. Count compliance rows by status column (`Covered` / `Drafted` / empty).
5. Compute next action: the first skill in `required_skills` that does not have a completed entry in `activity.md` and whose dependencies are met (see dependency rules below).
6. Print the summary. Do not write any file.

## Dependency rules (for "next action")

- `proposal-manager` has no dependency (after `opportunity-quick-look`).
- `competitor-assessment`, `customer-intel`, `capture-scorecard` can run in any order after `proposal-manager`.
- `proposal-solution-architect` requires `proposal-manager` and (if not skipped) `competitor-assessment`.
- `proposal-graphics` requires `proposal-solution-architect`.
- `past-performance` requires `proposal-manager` (uses eval criteria).
- `pricing-analyst` requires `proposal-solution-architect` (needs architecture to price).
- `proposal-writer` requires `proposal-solution-architect`, `proposal-graphics`, and (if not skipped) `past-performance` + `pricing-analyst`.
- `red-team-review` requires at least one file in `drafts/`.
- `compliance-check` can run any time after `proposal-manager`; recommended after each writer pass.

## Output discipline

- Do not invent status. If a file is missing, say "not started" — never guess.
- Do not speculate about quality. Report counts and file presence only.
- Do not modify any file. This skill is read-only.

## On completion

Append to `working/activity.md`:

```
## <timestamp> — status — <pipeline complete / N stages remaining>
```

(Exception: only append if run explicitly by the user as a milestone check — do not spam the log with every `/status` call. Rule of thumb: skip the append for `/status`.)
