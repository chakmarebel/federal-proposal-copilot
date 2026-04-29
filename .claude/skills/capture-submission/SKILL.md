---
name: capture-submission
description: Use this skill to snapshot a proposal's auto-generated draft and final submitted version into the calibration corpus, with edit notes. Run twice per proposal — once before manual editing (snapshot the AI's output) and once after submission (capture the final + notes). Builds the data the framework needs to learn from real edits and close the gap between auto-generation and submission-ready.
---

# Capture Submission Skill

## Purpose

Snapshot the (auto-generated draft, final submitted version, edit notes) tuple for a submitted proposal into `corpus/calibration/`. This is the data layer that lets the framework learn from your edits and improve over time.

## When to use

Run this skill **twice per proposal**:

1. **After `/proposal-writer` completes, before you start editing for submission.** This snapshots the AI's actual output as a baseline. If you skip this step and start editing first, the auto-draft is gone — you can't reconstruct it.
2. **After you submit the proposal.** This captures the final version + opens the edit-notes template for you to fill out.

The skill detects which phase you're in based on what already exists in `corpus/calibration/<slug>/`.

## Inputs

Read in this order:

1. `working/proposal-type.md` — for proposal_type and to confirm a proposal is active
2. `corpus/calibration/<slug>/manifest.json` (if exists) — to determine current phase
3. `drafts/` — source for auto-draft snapshot (Phase 1)
4. `final/` — source for final-submitted snapshot (Phase 2). Look in `final/docx/` first (most reliable post-export source), fall back to `drafts/` if user submitted markdown directly
5. `corpus/calibration/_template/` — template files for new entries

## Phase detection

The skill chooses behavior based on existing state:

| State | Detection | Phase | Action |
|---|---|---|---|
| `corpus/calibration/<slug>/` does not exist | First run | **Phase 1: pre-edit snapshot** | Snapshot `drafts/` → `auto-draft/`, init `manifest.json`, copy `edit-notes.md.template` |
| `corpus/calibration/<slug>/auto-draft/` exists, `final-submitted/` does not | Second run | **Phase 2: post-submit capture** | Snapshot `final/` (or `drafts/` if user names the source) → `final-submitted/`, update `manifest.json`, prompt user to fill `edit-notes.md` |
| Both `auto-draft/` and `final-submitted/` exist, `edit-notes.md` is filled out (more than the template defaults) | Third run | **Phase 3: complete** | Update `manifest.json` to status=complete, suggest running `/red-team-review --mode=lessons-learned` |
| Both exist, `edit-notes.md` is still template defaults | Reminder | **Reminder** | Print "edit-notes.md still has template placeholders — please fill it out for the entry to be useful" |

## Phase 1: Pre-edit snapshot

When `corpus/calibration/<slug>/` does not exist:

1. Read `working/proposal-type.md` — confirm a proposal is active. Extract `type_id` and customer (from working/customer-profile.md if available).
2. Create directory: `corpus/calibration/<slug>/`
3. Copy `drafts/*.md` → `corpus/calibration/<slug>/auto-draft/` (preserve filenames). Skip empty drafts and drafts/.gitkeep.
4. If `working/compliance-matrix.md` exists, copy it to `corpus/calibration/<slug>/auto-draft/_compliance-matrix.md` for context.
5. If `working/graphics-brief.md` exists, copy it to `corpus/calibration/<slug>/auto-draft/_graphics-brief.md`.
6. Create `corpus/calibration/<slug>/manifest.json` from `_template/manifest.json.example` with these fields filled in:
   ```json
   {
     "schema_version": "calibration-manifest.v1",
     "slug": "<slug>",
     "proposal_type": "<type_id>",
     "customer": "<customer name or null>",
     "captured_pre": "<ISO 8601 timestamp now>",
     "captured_post": null,
     "submitted_date": null,
     "status": "pre-edit",
     "outcome": null,
     "edit_hours_estimate": null,
     "notes": ""
   }
   ```
7. Copy `_template/edit-notes.md.template` → `corpus/calibration/<slug>/edit-notes.md` and substitute `[Proposal Slug]` with the actual slug.
8. Append to `working/activity.md`:
   ```
   ## YYYY-MM-DD HH:MM — capture-submission [phase=pre] — auto-draft snapshot → corpus/calibration/<slug>/auto-draft/
   ```
9. Print to user:
   ```
   Auto-draft snapshot captured to corpus/calibration/<slug>/auto-draft/.

   Continue editing in drafts/ (or final/ after running /export-proposal).
   When you submit, re-run /capture-submission to capture the final version
   and fill out edit-notes.md.
   ```

## Phase 2: Post-submit capture

When `corpus/calibration/<slug>/auto-draft/` exists but `final-submitted/` does not:

1. Locate the final submitted source. Priority order:
   a. `final/docx/` — if exists and contains files, this is the most reliable post-export source. Note: these are .docx files. Use the `anthropic-skills:docx` skill to extract markdown text from each, OR if the user has run `/export-proposal` and kept the markdown source intact, use the source markdown. Prefer markdown for diffability.
   b. `final/<format>/` for any format that has files
   c. `drafts/` — fallback if user submitted markdown directly without exporting
   d. **If none of the above**, prompt the user: "I can't find the final submitted version. Where is it? (path or 'paste here')"
2. Copy the located files → `corpus/calibration/<slug>/final-submitted/` (preserve section filenames; if from .docx, write extracted markdown).
3. Update `manifest.json`:
   - `captured_post`: ISO 8601 timestamp now
   - `submitted_date`: prompt user "What date did you submit? (YYYY-MM-DD, or press Enter for today)"
   - `status`: "post-submit"
4. Prompt user: "Open `corpus/calibration/<slug>/edit-notes.md` and fill it out. Five minutes. The most valuable section is #3 (top 3 systemic patterns)."
5. Append to `working/activity.md`:
   ```
   ## YYYY-MM-DD HH:MM — capture-submission [phase=post] — final captured + edit-notes ready → corpus/calibration/<slug>/
   ```
6. Print to user:
   ```
   Final version captured to corpus/calibration/<slug>/final-submitted/.

   Next step: open corpus/calibration/<slug>/edit-notes.md and fill it out
   (5 min). Then re-run /capture-submission one more time to mark the entry
   complete and unlock /red-team-review --mode=lessons-learned for this entry.
   ```

## Phase 3: Mark complete + suggest review

When `auto-draft/`, `final-submitted/`, and `edit-notes.md` (filled out) all exist:

1. Detect "filled out" by checking that `edit-notes.md` has more than just the template placeholders. Heuristic: at least one of sections 1, 3, or 4 has non-placeholder content.
2. If still has placeholders → print reminder, do NOT mark complete.
3. If filled out:
   - Update `manifest.json`:
     - `status`: "complete"
     - `edit_hours_estimate`: extract from edit-notes.md section 1 if user filled it in
     - `outcome`: prompt "Outcome (awarded/not-awarded/pending/withdrawn, or press Enter for pending)"
   - Append to `working/activity.md`:
     ```
     ## YYYY-MM-DD HH:MM — capture-submission [phase=complete] — entry finalized → corpus/calibration/<slug>/
     ```
   - Print to user:
     ```
     Calibration entry complete: corpus/calibration/<slug>/
       auto-draft/         (N files)
       final-submitted/    (N files)
       edit-notes.md       (filled)
       manifest.json       (status=complete)

     Recommended next step:
       /red-team-review --mode=lessons-learned

     This will diff auto-draft vs final-submitted, ingest your edit notes,
     and produce framework improvement proposals in
     reviews/lessons-learned-<slug>.md.
     ```

## Output paths

- `corpus/calibration/<slug>/auto-draft/<section>.md` (Phase 1)
- `corpus/calibration/<slug>/auto-draft/_compliance-matrix.md` (Phase 1, if exists)
- `corpus/calibration/<slug>/auto-draft/_graphics-brief.md` (Phase 1, if exists)
- `corpus/calibration/<slug>/manifest.json` (Phase 1, updated each phase)
- `corpus/calibration/<slug>/edit-notes.md` (Phase 1, populated by user, finalized in Phase 3)
- `corpus/calibration/<slug>/final-submitted/<section>.md` (Phase 2)

## Critical Rules

- **Never overwrite an existing auto-draft.** If `auto-draft/` already exists, you're past Phase 1. Detect the phase and act accordingly. Re-snapshotting the auto-draft after edits would destroy the calibration signal.
- **Never overwrite an existing final-submitted.** Same logic.
- **Never edit `edit-notes.md` content yourself** — that's the user's reflection. The skill only creates the file from template; the user fills it.
- **No PII in `manifest.json`.** Customer name and outcome are OK; specific evaluator names, contact info, or pricing data are not. The manifest is gitignored along with the per-proposal directory, but defense-in-depth.
- **Read-only on the corpus once a phase is complete.** Each phase appends or fills in fields; no phase rewrites prior phases.

## Cross-reference

- Discipline + structure: [`corpus/calibration/README.md`](../../../corpus/calibration/README.md)
- Templates: [`corpus/calibration/_template/`](../../../corpus/calibration/_template/)
- Downstream consumer: `red-team-review --mode=lessons-learned` reads completed corpus entries and produces framework improvement proposals
- Future cross-proposal analysis: a `/recalibrate-framework` skill (not yet built) will read multiple corpus entries to surface patterns visible only across proposals

## Activity Trail

On completion, append to `working/activity.md` in the proposal workspace (NOT the corpus directory):

```
## YYYY-MM-DD HH:MM — capture-submission [phase=<pre|post|complete>] — <one-line summary> → corpus/calibration/<slug>/
```

This makes the calibration capture visible in `/status` output and the dashboard.
