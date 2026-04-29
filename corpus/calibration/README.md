# Calibration Corpus

A growing record of `(auto-generated draft, final submitted version, edit notes)` tuples — one per submitted proposal. The corpus is the data that lets the framework **learn from real edits** and close the gap between AI output (~80% complete) and submission-ready (~100%).

## Why this exists

Every time you take an auto-generated draft and edit it for 1-3 hours before submission, you're producing the highest-value training signal in the entire system. Capturing it systematically is what turns a 80%-complete tool into a 95%-complete tool over time.

Without the corpus, every proposal starts from the same baseline and the same gaps repeat. With the corpus, gaps surface as patterns and the framework evolves to close them.

## Structure

```
corpus/calibration/
├── README.md                       # this file
├── _template/                      # templates for new entries
│   ├── README.md
│   ├── manifest.json.example
│   └── edit-notes.md.template
└── <proposal-slug>/                # one directory per submission (gitignored content)
    ├── manifest.json               # metadata: slug, type, dates, status
    ├── auto-draft/                 # snapshot of drafts/ BEFORE your edits
    │   ├── executive-summary.md
    │   ├── technical-approach.md
    │   └── ...
    ├── final-submitted/            # what you actually sent
    │   ├── executive-summary.md
    │   └── ...
    └── edit-notes.md               # 5-min reflection on what you changed and why
```

The structure (this README + `_template/`) is committed. Per-proposal content (`<proposal-slug>/`) is gitignored — it contains your real proposal text, customer details, evidence, and so on.

## Lifecycle

The `/capture-submission` skill manages the corpus lifecycle in two phases:

### Phase 1 — Snapshot the auto-draft (pre-edit)

After running `/proposal-writer` and before you start editing for submission:

```
/capture-submission
```

This snapshots the current `drafts/` state to `corpus/calibration/<slug>/auto-draft/`. Do this **before** you start your manual cleanup — once you start editing, you've lost the AI's actual output as a comparison baseline.

### Phase 2 — Capture the final + notes (post-submit)

After you've submitted the proposal:

```
/capture-submission
```

The skill detects that `auto-draft/` already exists, copies your `final/` directory to `corpus/calibration/<slug>/final-submitted/`, and opens `edit-notes.md` for you to fill out (5 minutes — see template).

## What to put in `edit-notes.md`

Five minutes of reflection. Don't over-engineer it. The categories are designed to surface systemic patterns:

1. **Total time spent on post-AI editing** (rough hours)
2. **% of time per edit category** (tone, customer-language, tightening, evidence, restructure, redundancy, factual fixes, formatting)
3. **Top 3 systemic patterns** — what did you fix more than once?
4. **Framework gaps** — what was missing that you had to add manually?
5. **What worked** — what did the AI get right that you want to preserve?
6. **Recommended framework changes** — specific suggestions for SKILL files / patterns

The most valuable item is #3. Patterns that repeat within one proposal almost certainly repeat across proposals — those are the fixes that pay off most when applied to the framework.

## Reading the corpus

Two ways to use the accumulated corpus:

### Per-proposal review
After completing one entry:
```
/red-team-review --mode=lessons-learned
```
Reads the diff between auto-draft and final, plus your edit-notes, and produces structured findings about what the framework should change.

### Cross-proposal pattern analysis
After ~5+ entries:
```
/recalibrate-framework  (future skill — not yet built)
```
Reads every corpus entry and surfaces patterns visible only across multiple proposals (e.g., "the writer always over-uses 'leverage' — appears as an edit in 6/7 entries"). These cross-proposal patterns are the highest-leverage framework improvements because they're systemic, not one-off.

For now (with 0-1 entries), the per-proposal review is enough.

## Discipline rules

1. **Snapshot before editing.** Once you start hand-editing for submission, the auto-draft is gone. Run `/capture-submission` immediately after the writer skill completes, before you touch anything.
2. **Capture even rejected proposals.** If you decided not to submit, the edit notes still teach the framework — note "decided not to submit, reason: X" and what you would have changed.
3. **Don't over-categorize edit notes.** The 8 categories are guides, not a rubric. If your edits don't fit, write what fits.
4. **Five minutes per entry, max.** The corpus is only useful if it gets populated. A perfect entry that takes an hour to write is worse than a rough entry that takes five minutes — because you'll skip the hour version.
5. **Privacy.** Per-proposal content is gitignored. Customer names, evidence, pricing, and IP all stay local. Only the structure ships in the public framework.
6. **No retention limit.** Keep entries indefinitely. The corpus is more valuable at scale than empty.

## What this is *not*

- **Not a fine-tuning dataset.** No model retraining is happening. This is calibration data for the framework's prompts, patterns, and style guide.
- **Not a full proposal archive.** Your submitted proposals live in `proposals/<slug>/final/`. The corpus is a thin slice for calibration purposes.
- **Not a substitute for `/red-team-review`.** Pre-submit review still catches gaps before submission. The corpus catches gaps that survived submission.

## Cross-reference

- **Methodology grounding:** [reference/methodology/shipley-alignment.md](../../reference/methodology/shipley-alignment.md) §"Lessons Learned" — Shipley's institutional discipline of evolving the methodology from edited proposals over decades.
- **Skill that operates on the corpus:** [.claude/skills/capture-submission/SKILL.md](../../.claude/skills/capture-submission/SKILL.md)
- **Existing review mode:** `red-team-review --mode=lessons-learned` reads corpus entries.
