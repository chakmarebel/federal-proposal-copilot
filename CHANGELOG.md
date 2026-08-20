# Changelog

All notable changes to Federal Proposal Copilot are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versions are pre-1.0 while the framework's skill surface stabilizes.

## [0.3.0] — 2026-08-20

Two months of upstream work, and the sync mechanism rebuilt so it stops going stale.

### Added

- **Final-file lint — the gate that sees what you actually upload.**
  `scripts/lint-submission-file.py` extracts text from the outgoing `.docx` / `.pdf` and
  applies the prose-lint HIGH rules plus a `[NEEDS]` / `[TBD]` bracket scan. It exists
  because team review forks to Google Docs or Word, where a drafts-only lint never sees
  the submitted file — the markdown can be clean while the shipped document is not. Run
  it last, on every submission artifact. `--selftest` included.
- **Matrices render to Excel, not Word.** `scripts/render-matrix-to-xlsx.py` turns any
  matrix-style markdown artifact into a working `.xlsx` — one worksheet per heading,
  prose preserved on a `Notes` sheet, verdict columns colour-coded, header rows frozen
  and filterable. A matrix is a table reviewers sort, filter, and hand back; Word cannot
  do any of that. Narrative artifacts still render to `.docx`.
  The renderer **never overwrites a workbook it did not write**: generated files are
  stamped in their document properties, and an unstamped file at a target path is
  reported `[KEEP]` and left alone even under `--force`. That guard is there because a
  `--force` sweep destroyed hand-curated workbooks whose extra sheets existed only in
  the `.xlsx`.
- **White-glove `.docx` rendering on every render.** `scripts/render-md-to-docx.py` now
  calls `tools/polish_docx.py::whiteglove()` on each document: content-proportional
  table column widths, header rows repeating across page breaks, rows that never split
  mid-cell, tightened cell spacing, 1" margins. `polish_docx.py --tables-only` applies
  just that pass to arbitrary files; the full polish adds the running header/footer.
- **Four proposal types**, each with its section pattern: `baa-white-paper`,
  `unsolicited-proposal` (FAR 15.6), `pitch-demo` (with
  `reference/pitch-demo-readiness-gate.md`), and `marketplace-video-pitch`. Plus the
  `colosseum` portal format.
- **`/capture-demand-signals` and the demand-signal loop.** An append-only, workspace-global
  register of what customers actually asked for, so the engineering shop sees demand by
  frequency and customer breadth instead of as anecdotes — and answers back in writing.
  Ships the schema, the controlled capability vocabulary, the extractor, the CRM-candidate
  ingest/promote pair, the exposure-ranked prose brief, and the five-sheet `.xlsx` workbook
  whose `Gap Queue` sheet is the write-back surface. Design in
  `docs/BD-CTO-DEMAND-SIGNAL-SYNC.md`. The framework ships the machinery; the register is
  yours and is gitignored.
- **Repo hygiene tooling.** `scripts/check-git-boundary.sh` refuses to publish
  company-private paths, `scripts/install-hooks.sh` wires it to pre-commit, and
  `scripts/backup-company-assets.py` snapshots the gitignored `my-company/` outside the
  repo — content-hashed, and refusing to snapshot a file that is empty, unparseable, or
  a ledger whose `items[]` has collapsed to zero. `my-company/` has no copy in git, so an
  ordinary git operation can destroy it with no undo.
- **Voice doctrine corpus.** `reference/voice-profiles/proposal.md` and the
  `reference/voice-pairs/proposal` paired before/after examples — six named
  AI-proposalese failure modes (explainer tail, abstract subject, narrated reasoning,
  overloaded benefit tail, pseudo-cleft, solicitation echo), each with the rewrite.
- **`docs/AGENT-ORIENTATION.md`** — the fast path for an agent new to the repo: the
  mental model, what is enforced mechanically, and the traps, in one pass.
- **`reference/preventable-gold-team-findings.md`** — findings that should have been
  caught before Gold Team, so they are.
- **Calibration tooling** — `scripts/calibration-status.py` and
  `scripts/new-calibration-entry.sh` support the existing `/capture-submission` skill.

### Changed

- **The sync mechanism is now transform-based rather than freeze-based.**
  Company neutralization moved out of hand-edits and into
  `tools/neutralize-company.sed`, shared by `tools/sync-from-fpa.sh` and
  `tools/sync-voice-anchors.sh`. This matters because a hand-neutralized file has to be
  frozen off the sync surface forever, and frozen content goes stale — which is exactly
  what had happened. Files whose only divergence is mechanical now stay on the surface
  and keep receiving upstream improvements.
- **`tools/sync-from-fpa.sh` gained `FPA_LOCAL`**, to sync from a local upstream checkout
  rather than a clone, and reports the HEAD it read.
- Refreshed from upstream: `proposal-writer`, `proposal-manager`, `proposal-storyboard`,
  `red-team-review`, `adversarial-review`, `proposal-patcher`, the prose-lint rule set,
  the evaluator-upstream toolchain, `check-strengths.py`, `md_to_docx.py`, and the
  shared doctrine.

### Fixed

- **Company identity that had been published.** `reference/voice-anchors/` carried two
  full upstream proposal passages naming a real company and two real products, and
  `.claude/skills/export-proposal/SKILL.md` carried an operator's local Windows path in
  two usage examples — despite the sync model documenting the latter as already
  neutralized. All are now neutralized by transform, so they cannot silently return.
- Two neutralization rules that were correct token-by-token but wrong sentence-by-sentence:
  rewriting the bare upstream repo name produced "copilot, and copilot" in doctrine that
  names all three sibling repos, and collapsing two distinct product names to one
  placeholder turned a voice anchor into "[Your Product] and [Your Product] form a
  two-layer stack." Both are documented in `docs/fpa-sync-model.md` as standing lessons.

### Added — safeguards

- **`tools/leak-scan.sh`** greps the whole distributable tree for company-identity markers
  and exits non-zero on any survivor. Both sync scripts run it as their closing step, so a
  sync that would publish an identifier fails loudly instead of committing quietly. The
  neutralize table is only ever as complete as the last thing someone noticed; this is the
  part that notices.

### Known issues

- `scripts/promote-crm-candidates.py --selftest` fails: it asserts an alias mapping that
  `reference/customer-aliases.tsv` no longer contains. This is an upstream defect mirrored
  faithfully, not sync damage. Fixing it requires deciding whether the alias rows were lost
  or the assertion is stale — a data question, not a code question. Tracked in
  `docs/fpa-sync-model.md`.

## [0.2.0] — 2026-07-06

Evaluator-first drafting and a native external-review loop.

### Added

- **`/adversarial-review` — context-blind review loop (optional, every proposal type).**
  Fresh-context reviewer agents read *only* what an outside evaluator would see — the
  finished document, nothing from your workspace or the conversation — and return
  cost-cited findings that feed a converging critique → triage → patch cycle until a
  round comes back clean. It replaces the manual "paste the draft into an external AI"
  habit with a repeatable, in-pipeline step. Four personas ship in
  `reference/adversarial-personas.md`: Skeptical Evaluator, Cold Reader, Competitor's
  Capture Manager, and Compliance Hawk. Runs after `/red-team-review`, before
  `/export-proposal`. `--mode=export-prompt` / `--mode=ingest` keep the external-model
  path available in the same findings format for A/B comparison.
- **Evaluator-upstream drafting — the rubric drives the draft, not just the review.**
  The evaluator's lens now runs *before* the draft, so Gold Team confirms the score
  instead of triggering a structural rewrite:
  - **Typed evaluation model** (`/proposal-manager` Step 4b) — this solicitation's
    factors, weighting, pass/fail gates, and constraints captured as a curatable,
    provenance-tracked rubric (`working/evaluation-model.md` + `.json`). Re-extraction
    never destroys rows you've confirmed, edited, or added by hand; AI-inferred
    criteria are always labeled as such.
  - **Factor-keyed storyboard** — `/proposal-storyboard` keys each section to the
    evaluation factors it must win and the strength it must earn, and flags any section
    that maps to no factor.
  - **Draft-prompt injection** — `/proposal-writer` writes each section toward the
    specific factors and discriminators it must earn (only when those artifacts exist;
    no change to behavior otherwise).
  - **Lift metric** — every scored `/red-team-review` run appends a snapshot to
    `reviews/gold-team-history.jsonl`; `scripts/compute-lift.py` reports the
    baseline→current pWin trajectory and unsupported-claim density over time.
- **Track B (white-paper) workflow** documented in `CLAUDE.md` — the narrative-first
  order of operations (narrative spine → writer → patcher) that white papers use
  instead of the storyboard-driven main pipeline.
- New JSON schemas: `evaluation-model`, `gold-team-snapshot`, and `adversarial-round`
  (append-only round history).

### Changed

- `/proposal-manager`, `/proposal-storyboard`, `/proposal-writer`, and
  `/red-team-review` now produce and consume the evaluation model; `/proposal-patcher`
  can apply accepted `/adversarial-review` findings.

### Maintenance

- The upstream sync tooling (`tools/sync-from-fpa.sh`) now carries feature scripts and
  JSON schemas alongside skills, normalizes schema namespaces, and regenerates the
  skills index automatically — so a framework feature and its supporting files flow
  across in one step instead of arriving half-complete.

## [0.1.0] — 2026-06-10

Initial public baseline of Federal Proposal Copilot — the company-neutral,
Claude Code–native distribution of the Shipley-aligned proposal framework.

### Added

- **29 skills** spanning the full lifecycle — capture (`/opportunity-quick-look`,
  `/customer-intel`, `/competitor-assessment`, `/capture-scorecard`, `/capture-intent`),
  planning (`/proposal-manager`, `/proposal-solution-architect`, `/narrative-spine`,
  `/proposal-storyboard`), drafting (`/proposal-writer`, `/proposal-editor`,
  `/proposal-graphics`, `/past-performance`, `/pricing-analyst`), review
  (`/technical-review`, `/compliance-check`, `/evidence-check`, `/red-team-review`,
  `/proposal-patcher`), and submission (`/export-proposal`, `/status`).
- **14 proposal types** with per-type required-skill workflows, plus parametric
  proposal graphics and Red/Gold/White-Glove color-team reviews.
- **`/setup-company`** first-run scaffolding for the git-ignored `my-company/`
  substrate (identity, capabilities, past performance, evidence ledger, brand palette).
- Read-only portfolio **dashboard** over the JSON sidecars produced by the pipeline.
- **Prose-quality doctrine and voice anchors**, plus pre-submit lint gates
  (prose lint, structural lint, and Gold Team strength preservation) enforced at export.
- **FPA → copilot sync mechanism** (`tools/sync-from-fpa.sh`) keeping shared, canonical
  content aligned with the upstream working repository.

[0.2.0]: https://github.com/chakmarebel/federal-proposal-copilot/releases/tag/v0.2.0
[0.1.0]: https://github.com/chakmarebel/federal-proposal-copilot/releases/tag/v0.1.0
