# Agent Orientation

**Read this first if you are an AI agent new to this repository.** It is the fast path to a correct
mental model: what this repo is, how the parts fit, what is enforced mechanically, and where the
traps are. Everything here is verifiable from the tree — no aspirational description.

Written 2026-08-01. If a count or path below disagrees with the tree, trust the tree and fix this
file.

---

## 1. What this is in one paragraph

A **workflow system, not an application.** It operationalizes the Shipley capture and proposal
process for federal defense and intelligence-community pursuits as a set of 30 Claude Code skills
that each read structured inputs and write structured artifacts to disk. There is no server, no
database, and no UI. The "program" is markdown and JSON files in a defined layout, plus ~35 Python
and shell scripts that validate, transform, and gate those files. A human runs skills in a
type-specific order; each skill's output becomes the next skill's input.

The single design goal, stated in `CLAUDE.md` and worth internalizing before you touch anything:
**answer the customer's requirement with a credible solution, rather than describing capabilities
you wish were requirements.** Nearly every constraint in this repo exists to defeat that
solution-first failure mode by making requirement-first sequencing easier to follow than to bypass.

## 2. Which document to read for what

Four docs overlap deliberately. Do not consolidate them; they have different audiences.

| File | Audience | Use it for |
|---|---|---|
| `CLAUDE.md` | Agents, auto-loaded every session | **The operating manual.** Mandatory rules, the skill catalog, the standard workflow, output discipline, activity-trail contract. This is authoritative over anything else, including this file. |
| `OVERVIEW.md` | Humans evaluating the tool | Positioning and the problem it solves. Read for intent, not mechanics. |
| `README.md` | Humans installing and running it | Setup, requirements, the git-boundary guard, operational how-to. |
| `SKILLS.md` | Both | One-page index of all skills by lifecycle phase. **Auto-generated** — never hand-edit. |
| `docs/AGENT-ORIENTATION.md` | Agents | This file: how the pieces relate, invariants, failure modes. |

Design decisions live in dated root-level docs (`PROPOSAL-AGENT-REDESIGN-2026-05-15.md`,
`FPA-VOICE-REDESIGN-2026-07-30.md`, `docs/BD-CTO-DEMAND-SIGNAL-SYNC.md`, and others). When you need
to know *why* something is shaped the way it is, search those before assuming it is accidental.

## 3. The mental model

```
reference/          the rulebook — methodology, rubrics, vocabularies, type registry, schemas
my-company/         who we are — capabilities, past performance, EVIDENCE LEDGER (gitignored)
proposals/<slug>/   one pursuit, one directory (gitignored)
    inputs/         source material, pre-digested to .md
    working/        analysis artifacts — matrices, plans, storyboard, activity log
    drafts/         the authoring layer (markdown)
    reviews/        red / gold / white-glove / compliance findings
    final/          native Office exports for submission
signals/            cross-pursuit demand register (gitignored)
scripts/            validators, extractors, linters, gates
tools/              md→docx, compliance→xlsx, docx polish
```

Four ideas explain most of the design:

**1. Markdown is the authoring layer; Office is the deliverable.** Skills write `.md`. `.docx`,
`.xlsx`, and `.pptx` are produced by `/export-proposal` and `scripts/render-md-to-docx.py`, and are
**derived artifacts** — gitignored, regenerable, never the source of truth. The `.md → .docx → .pdf`
path preserves styling; `.md → .pdf` does not and is not used.

**2. Every artifact is typed and often has a JSON sidecar.** `reference/schemas/` holds 10 schemas.
The pattern: humans read and edit the markdown, skills own the JSON, downstream consumers read the
JSON instead of re-parsing prose.

**3. The proposal type gates the workflow.** `working/proposal-type.md` declares `required_skills`,
`skipped_skills`, `pricing_artifact`, `page_target`, and `submission_mechanism`. There are 15 types
in `reference/proposal-types/`. A skill invoked while listed in `skipped_skills` must exit without
producing output. **Read `working/proposal-type.md` before running anything against a pursuit** —
this is step 0 of the standard workflow and it is not optional.

**4. Claims must be provable.** `my-company/evidence-ledger.json` is the store of approved,
citable evidence with strength ratings. `/evidence-check` audits draft citations against it. A
capability that is real but absent from the ledger is invisible to the pipeline, which means the
proposal cannot get credit for it. Fabricating past performance, certifications, or customer facts
is the cardinal sin here.

## 4. Two workflow tracks

**Main pipeline (structure-first).** quick-look → submission-summary → proposal-manager →
customer-intel → capture-intent → solution-architect → past-performance → pricing → narrative-spine
→ storyboard → graphics → writer → editor → compliance-check → evidence-check → technical-review →
red-team → export. Prose is generated inside a pre-built structural lattice.

**Track B (narrative-first), for `type_id: white-paper`.** Skips `proposal-storyboard` and
`proposal-editor`; substitutes `/proposal-patcher` for the editor. Composition happens first, then
validation. The reasoning: a spine runs lengthwise through an argument, a storyboard runs crosswise
per section, and white papers need the former. Running both the editor and the patcher defeats the
purpose.

`/proposal-writer` runs two passes in both tracks: **draft-loose** (confident in-voice prose, no
template enforcement) then **bind** (attach evidence, verify claims, update the compliance matrix)
without rewriting for style. `drafts/loose/` preserves the pre-bind version.

## 5. What is enforced mechanically, not socially

This is the part most worth knowing, because these gates will block you and the reason will not
always be obvious.

| Gate | Trigger | Blocks on |
|---|---|---|
| `scripts/check-git-boundary.sh` | pre-commit + pre-push hook | Staging anything under `proposals/`, `my-company/`, `signals/`, `scrubs/`, root `drafts/ working/ reviews/`, `corpus/calibration/<slug>/` |
| `scripts/check-canonical-symbols.py` | pre-commit hook | Re-implementing a capability another repo owns (`docs/canonical-symbols.json`) |
| `scripts/prose-lint.py` | `/export-proposal` preflight | HIGH findings: the section-sign glyph, dashes as sentence punctuation, internal process vocabulary in customer-facing prose |
| `scripts/lint-document-structure.py` | `/export-proposal` preflight | Duplicate section numbers, broken figure refs, missing classification marking |
| `scripts/check-strengths.py` | `/export-proposal` preflight | Gold Team Significant Strengths stripped by later edits |
| `scripts/lint-submission-file.py` | Last gate before upload | HIGH rules + `[NEEDS]`/`[TBD]` scan on the **actual outgoing** .docx/.pdf |
| `scripts/build-skills-index.py --check` | CI / pre-commit | Stale `SKILLS.md` |
| `scripts/skill-graph.py --validate-only` | After any skill edit | Bad `phase`, `composes`, or `conflicts_with` reference |

**Hooks are per-clone and not armed by default** — git does not track `.git/hooks/`. Run
`bash scripts/install-hooks.sh` after cloning; `--verify` exits 1 if unarmed. A fresh clone has no
leak protection.

**16 scripts support `--selftest`** — deterministic, offline, no network or API key. Run the
selftest before trusting a script you have just edited, and add cases to it rather than writing a
separate test file. `scripts/smoke-test.sh` runs the suite; note it has known pre-existing failures,
so a non-zero exit there is not necessarily your fault.

## 6. Non-negotiable conventions

- **All outputs go to files.** Never answer a content request only in chat. Analysis → `working/`,
  prose → `drafts/`, findings → `reviews/`.
- **Paste-ready-language sync.** If you give the user proposal language to paste into a Google Doc,
  apply the same change to the corresponding `drafts/*.md` in the same turn. Chat-only language
  silently forks the pipeline and every lint goes stale.
- **Activity trail is mandatory.** Every content-producing skill appends one line to
  `working/activity.md` and one JSON object to `working/ai-runs.jsonl`. Append only, never rewrite.
  Read-only skills (`/status`) do not append.
- **Never hand-edit synced files.** `reference/PROSE-QUALITY-DOCTRINE.md`, `reference/doctrine/*`,
  and the voice anchors are synced from an upstream workbench via `tools/sync-voice-anchors.sh`.
  Change them upstream.
- **Read review artifacts in Word.** The human reads `.docx`. After producing review artifacts, run
  `python scripts/render-md-to-docx.py --proposal <slug>`.
- **Do not invent capabilities, certifications, past performance, or customer facts.** If something
  is missing, state the assumption explicitly.

## 7. The demand signal loop (added 2026-07-31)

The newest subsystem, and the only one that is cross-pursuit rather than per-proposal. Full design in
`docs/BD-CTO-DEMAND-SIGNAL-SYNC.md`.

Customer asks from solicitations *and* from conferences, one-on-ones, trials, and debriefs aggregate
into `signals/demand-signals.jsonl` — append-only, workspace-global — normalized against the 25-theme
controlled vocabulary in `reference/capability-themes.md`. `scripts/build-demand-signal-workbook.py`
produces the weekly `.xlsx` for the CTO shop and `--ingest` reads their dispositions back.
Engineering's answers land in `my-company/evidence-ledger.json` (when a capability becomes provable)
and `my-company/claim-envelope.md` (what BD may state as fact, phrase as intent, or never claim).

Four things to preserve if you work on it:

- **`our_status` is BD's read; `cto_disposition` is engineering's. Never merge them** — the
  disagreements are the meeting agenda.
- **An unknown `capability_theme` is a hard validation failure.** A typo silently splits a theme and
  understates its weight, which is the one error that corrupts the ranking.
- **Reporting is decision-first.** Lead with at most five ranked decisions and what each has cost;
  the full table goes behind them. A leaderboard is an inventory, and nobody prioritizes from an
  inventory.
- **Ledger matching is exact tag match, not prose keywords.** Keyword matching was tried and
  abandoned: generic terms matched 60 of 81 items, every theme read as proven, and the ranking
  collapsed to zero — hiding exactly the themes that could not be substantiated.

`/capture-demand-signals` runs **outside** the per-type `required_skills` workflow. No proposal type
requires or skips it.

## 8. Traps

Things that will cost you time if you do not know them.

- **`.gitignore` does not untrack what is already committed.** Files added before the boundary guard
  existed stay tracked until removed by hand. The `scrubs/` and `my-company/` backlog was cleared
  2026-08-01 and 2026-08-04; as of then only `reviews/framework-audit-2026-05.md` remains. **A
  consequence worth knowing: `my-company/evidence-ledger.json` now has no copy in git at all**, so
  the `~/.claude/backups` routine is the only thing between an accidental delete and rebuilding 86
  evidence items by hand. See the README's boundary section.
- **The boundary guard matches paths, not content.** A tracked file under `scripts/` or `reference/`
  can carry protected material and pass. One reviewed exception exists
  (`scripts/backfill-demand-signals.py`). A passing guard does not mean a file is clean.
- **`my-company/evidence-ledger.json` is not committable and has no other backup.** Back it up to
  `~/.claude/backups` after appending.
- **Once team review moves to Google Docs, the Doc is the source of truth.** Reconcile before any
  export, or the drafts and every gate are testing a document nobody is submitting.
- **Web-form submissions have a second gate.** When `submission_mechanism: web-form`, skills
  downstream of `/capture-portal-structure` must refuse to run without
  `inputs/00_priority/portal-format.md`. This exists because ~40% of tokens on one pursuit went to
  compressing drafts to fit hidden portal limits.
- **Some `reference/` files may still contain `[Your Company]` placeholders.** Audit before using
  them on a new proposal type.
- **44 proposal directories exist**, most inactive. Do not assume a directory under `proposals/` is
  live; check `working/activity.md` for recency.

## 9. Orienting in a new session

```bash
cat CLAUDE.md                                  # the operating manual, authoritative
cat SKILLS.md                                  # what skills exist, by phase
cat proposals/<slug>/working/proposal-type.md   # what this pursuit requires and skips
cat proposals/<slug>/working/activity.md        # what has already been run
/status                                        # read-only pipeline state + next command
bash scripts/install-hooks.sh --verify         # is this clone leak-protected?
```

For a pursuit you have not seen before, read in this order: `proposal-type.md` →
`activity.md` → `quick-look.md` → `requirement-matrix.md` → `narrative-spine.md`. That sequence
gives you the constraints, the history, the judgment, the requirements, and the argument in about
five files.
