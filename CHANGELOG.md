# Changelog

All notable changes to Federal Proposal Copilot are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versions are pre-1.0 while the framework's skill surface stabilizes.

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
