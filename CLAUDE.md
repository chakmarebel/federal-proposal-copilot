# Federal Proposal Workspace

## Mission
This workspace operationalizes the Shipley capture and proposal process for federal defense / IC proposals and white papers. Guide the user through each step's required artifact. **Enforce requirement-first sequencing.** Defeat the solution-first failure mode by making the requirement-breakdown step harder to skip than to do. Every artifact must improve probability of winning — by answering the customer's requirement with a credible solution, not by describing capabilities the user wishes were requirements.

## Company Context

This is a company-neutral framework. Your company's identity, capabilities, past
performance, contract vehicles, evidence ledger, and brand palette live in
`my-company/` — which is git-ignored and never published.

**First-run setup (required).** Before running any drafting skill, run
`/setup-company` to scaffold `my-company/` and supply:
- Company name; CAGE / UEI / NAICS; location; founding year
- Core product / capability summary and key differentiators
- Past performance and customer references
- Contract vehicles and teaming agreements
- A brand palette and logo for proposal graphics (`my-company/branding/`)

Skills read company facts from `my-company/` — they never assume a specific company.

## Priorities
1. Compliance first â€” every output maps to requirements
2. Evaluator clarity â€” write as if scoring against criteria
3. Credible architecture â€” design before writing
4. Precise differentiation â€” no unsupported claims
5. Reuse repository material aggressively, but tailor precisely
6. Concise, scorable writing â€” no filler

## Core Rules
- Do not produce generic marketing language
- Do not invent capabilities, certifications, past performance, or customer facts
- If something is missing, state the assumption explicitly
- Design the solution before drafting narrative
- Keep sections non-redundant
- Prefer tables and structured outputs over long prose during analysis
- When drafting graphics, optimize for PowerPoint/Figma recreation
- **All outputs go to local files in this workspace** â€” never just display in chat

## Skill Index

[`SKILLS.md`](SKILLS.md) is the one-page directory of every skill in `.claude/skills/`, grouped by lifecycle phase. Read it at session start to orient before reaching into any individual `SKILL.md`. **The index is auto-generated** by `scripts/build-skills-index.py` from each SKILL.md's YAML frontmatter — do not hand-edit it.

**Frontmatter contract.** Every `SKILL.md` declares: `name`, `description`, `phase`, `composes`, `conflicts_with`. Valid `phase` values: `setup`, `capture`, `planning`, `drafting`, `review`, `submission`, `inspection`. `composes` is the list of upstream skills this one consumes; `conflicts_with` is the list of peer skills this one must NOT duplicate (with an inline `#` rationale).

**Maintenance when adding or modifying a skill:**

```bash
python scripts/skill-graph.py --validate-only       # catch bad phase / composes / conflicts_with refs
python scripts/build-skills-index.py                # regenerate SKILLS.md
python scripts/build-skills-index.py --check        # CI / pre-commit gate (exit 1 if stale)
python scripts/skill-graph.py --format mermaid      # render the dependency DAG
```

**Activity tracking.** Each proposal's `working/activity.md` is the single source of truth for what skills ran when. There is no separate skill log. Aggregate across proposals with `python scripts/skill-stats.py` (supports `--since` and `--per-skill`).

**Pre-submit gate (mandatory after team revisions).** Two scripts catch the failure modes that survive Red Team / Gold Team / White Glove when they're introduced *after* those reviews (team revisions, last-minute insertions, compression edits). Run both before `/export-proposal` produces the final submission package; either exits 1 on a blocking finding.

```bash
# Structural lint — duplicate section numbers, broken figure refs, missing classification marking
python scripts/lint-document-structure.py --proposal <slug>

# Gold Team Significant Strength preservation — flags MOS-slate-style stripping
python scripts/check-strengths.py --proposal <slug> --target docx
```

`check-strengths.py` writes `reviews/strength-preservation.md` with the specific phrases preserved vs. missing for each Significant Strength. Use `--target docx` after `/export-proposal` to verify the rendered Word doc still carries the load-bearing claims; use `--target drafts` (default) for a pre-export sanity check.

**Read review artifacts in Word, not markdown.** The framework authors review / lessons-learned / proposal-plan / team-review-brief artifacts in `.md` because it's the format the skills write. Bill reads them in `.docx`. After any session that produces review artifacts, run:

```bash
# Single file
python scripts/render-md-to-docx.py path/to/file.md

# All reviews + working/ artifacts for one proposal
python scripts/render-md-to-docx.py --proposal <slug>

# Every review/reference artifact across the workspace (idempotent — only re-renders changed .md)
python scripts/render-md-to-docx.py --all
```

`.docx` lands beside the `.md` (e.g., `reviews/gold-team-scorecard.md` → `reviews/gold-team-scorecard.docx`). The `.md` is the source of truth; the `.docx` is a derived artifact (gitignored). `scripts/build-team-review-brief.py` auto-emits `.docx` alongside `.md` because that artifact is meant for human reading from day one.

## Standard Workflow

**Step 0 â€” Read the proposal type (mandatory).** Before running any skill against an active proposal, read `working/proposal-type.md`. It declares:
- `required_skills` â€” the ordered workflow for this proposal type
- `skipped_skills` â€” skills that do NOT apply (do not run them)
- `pricing_artifact`, `pp_required`, `page_target`, `evaluator_framing`
- `compliance_sources` â€” which parts of the solicitation drive the compliance matrix
- `submission_mechanism` â€” `email`, `document-upload`, or `web-form` (see `reference/proposal-types/README.md`)

If a skill is invoked that appears in `skipped_skills`, exit with "Skipped for type <type_id>" and do not produce output. If `working/proposal-type.md` is missing, instruct the user to run `/new-proposal` (or copy a file from `reference/proposal-types/` manually).

**Step 0b â€” Portal format gate (mandatory for web-form submissions).** When `submission_mechanism: web-form`, every skill downstream of `/capture-portal-structure` (i.e., `/proposal-manager`, `/proposal-solution-architect`, `/proposal-writer`, `/compliance-check`, `/export-proposal`) must check for `inputs/00_priority/portal-format.md`. If absent, exit with "Portal format not captured. Run `/capture-portal-structure` first." This prevents the expensive failure mode of drafting against an assumed structure â€” learned from the NATO DIANA submission where ~40% of tokens went to compressing drafts to fit hidden portal limits.

The full skill catalog below is the superset. Each proposal type uses only the subset listed in its `required_skills`:

1. `/opportunity-quick-look` — Rapid triage across 8 factors: mission fit, customer, funding, scope, schedule, competitive position, barriers, **and submission mechanism** → `working/quick-look.md`. **Stop here if PASS or HOLD.**
1b. `/capture-portal-structure` — **Only when `submission_mechanism: web-form`** (DIANA, DIU CSO Phase 1, Challenge.gov, AFWERX Open Topic, Valid Evaluation, etc.). Register for the portal first, then run this skill to capture section structure, hard character limits, metadata fields, and submission mechanics. Inherits from `reference/portal-formats/<portal-id>.md` if known. Writes `inputs/00_priority/portal-format.md` + `working/section-budgets.md`. `/proposal-manager` refuses to run without it when the type requires a web-form submission.
1c. `/submission-summary` — Deliverable spec: a one-page, factual summary of exactly what the customer requires us to submit — response format, volume/section structure, page or word limits, pricing artifact, due date, submission mechanics → `working/submission-summary.md`. **Stops for human confirmation of the deliverable shape before planning begins.** Runs after `/opportunity-quick-look` (and `/capture-portal-structure` if web-form), before `/proposal-manager`. `/proposal-manager` consumes it as the authoritative response-requirements source.
2. `/proposal-manager` — Decompose requirements, extract evaluation criteria, define win themes, bid/no-bid, seed compliance matrix → `working/proposal-plan.md` + `working/compliance-matrix.md`. When `submission_mechanism: web-form`, pulls section structure from the captured portal format, not the solicitation PDF. Consumes `working/submission-summary.md` for the deliverable structure.
3. `/customer-intel` — Profile decision makers, buying history, hot buttons → `working/customer-profile.md`
4. `/competitor-assessment` — Identify competitors, build comparison chart, teaming gaps → `working/competitor-assessment.md`
5. `/capture-scorecard` — Assess readiness across 9 dimensions, go/no-go → `working/capture-scorecard.md`
6. `/capture-intent` — Strategic intent layer: why we're bidding, customer beliefs to create, prohibited claims, posture, ghosting strategy, desired customer action → `working/capture-intent.md`. Consumed by storyboard, writer, editor, and red-team to keep the proposal strategically coherent.
7. `/proposal-solution-architect` — Map requirements to capabilities, design architecture → `working/` (5 files)
8. `/past-performance` — Map PP to eval criteria, draft narratives → `drafts/past-performance.md`. **Runs before storyboard** so the storyboard can plan around real proof points, not aspirational ones.
9. `/pricing-analyst` — Dispatches on `pricing_artifact` in `working/proposal-type.md` to the matching template in `reference/pricing-artifacts/`. Produces exactly one artifact type: ROM range, SBIR line-item budget, OTA milestone-payment schedule, CSO commercial pricing, or FAR cost volume with BOEs. Output path varies by artifact; companion file is always `working/pricing-inputs.md`. **Runs before storyboard** so cost constraints (LOE caps, milestone shape) inform the storyboard's claim envelope.
9b. `/narrative-spine` — Pre-prose argument layer: writes the proposal's narrative spine — a one-page, plain-prose statement of what the proposal claims and why it is compelling against the customer's actual problem — then **stops for human sign-off** → `working/narrative-spine.md`. Reads the solicitation directly (not just the matrices). The storyboard decomposes it; the writer drafts it. Runs after architecture/capture-intent (and past-performance/pricing if the type uses them), before storyboard. For white papers (no storyboard), it feeds `/proposal-writer` directly.
10. `/proposal-storyboard` — Decomposes the approved narrative spine into a section-by-section writing plan: evaluator question, required answer, claims allowed/prohibited, proof points, graphic argument, target length → `working/storyboard.md` + `working/storyboard-coverage-map.md`. Every downstream drafting skill keys off this file.
11. `/technical-review --phase=approach` — Pre-write feasibility gate. Validates architecture/storyboard for hidden assumptions, integration realism, ATO plausibility, schedule realism *before tokens are spent on graphics or prose for a flawed approach* → `reviews/technical-review-approach.md`
12. `/proposal-graphics` — Draft graphics brief and figure concepts driven by storyboard's "Graphic Argument" fields, after the approach has cleared technical review → `working/graphics-brief.md`
13. `/proposal-writer` — Two passes. **draft-loose** writes each section as a confident, in-voice argument from the narrative spine, in the selected narrative operating mode, with the section template / pattern enforcement / evidence markers / matrix updates suspended → `drafts/loose/`. **bind** attaches evidence citations, verifies every claim, runs the winning-pattern completeness check, and updates the compliance matrix — without rewriting for style → `drafts/`. `/proposal-writer` with no mode runs both (`full`); `--mode=draft-loose` / `--mode=bind` run a single pass.
14. `/proposal-editor` — Editorial pass: tightens prose, removes marketing language, removes AI smell, preserves compliance/evidence/proof. Edits the bound drafts **in place** at `drafts/` (the pre-edit version is preserved at `drafts/loose/`). → `drafts/` + `reviews/editorial-changes.md`
15. `/compliance-check` — Diff required vs. covered requirements → `reviews/compliance-gaps.md`. Also emits `working/compliance-matrix.json` sidecar.
16. `/evidence-check` — (Phase C) Audit evidence citations in drafts against `my-company/evidence-ledger.json`: flag `CLAIM-UNSUPPORTED` markers, typo'd IDs, retired/restricted evidence, and surface unused approved evidence. Run after `/proposal-editor`, before `/red-team-review --mode=gold`. Writes `reviews/evidence-check.md` and updates `working/compliance-matrix.json` evidence_coverage metric.
17. `/technical-review --phase=drafts` — Post-write claim-truthfulness review. Validates draft prose against architecture for hand-waving, hidden contradictions, magical integrations, ATO/cyber realism, claim truthfulness → `reviews/technical-review-drafts.md`. Cites the approach-phase report.
18. `/red-team-review` — Red (narrative quality + customer focus) → **Gold (rubric-driven mock evaluation using `reference/evaluator-rubrics/`: adjectival ratings, Strengths/Weaknesses/Deficiencies with paragraph-cited evidence, win-theme visibility, discriminator proof-point check, Phase C unsupported-claim scan, pWin estimate)** → White Glove → `reviews/`. Compliance coverage is validated separately by `/compliance-check`.
19. `/export-proposal` — After drafting + Gold Team, convert markdown drafts to native Office: .docx (Word narratives), .xlsx (compliance matrix, pricing), .pptx (optional briefings), + graphics PNGs. Writes to `final/`. User then opens Word and saves as PDF for submission.
20. `/status` — Read-only: show pipeline state, compliance coverage, next recommended command. Use any time.

## Directory Structure
```
proposals/
â”œâ”€â”€ inputs/           # Source materials (pre-digested .md files)
â”‚   â”œâ”€â”€ 00_priority/  # Solicitation, eval criteria, must-read
â”‚   â”œâ”€â”€ 01_customer/  # Mission context, problem, constraints
â”‚   â”œâ”€â”€ 02_yourCompany/ # Our capabilities, past performance
â”‚   â”œâ”€â”€ 03_teammates/ # Partner capabilities
â”‚   â”œâ”€â”€ 04_patterns/  # Reference architectures, win themes
â”‚   â”œâ”€â”€ 05_graphic_standards/  # Visual standards, brand templates (INPUTS only)
â”‚   â””â”€â”€ 06_notes/     # Raw notes, meeting inputs
â”œâ”€â”€ working/          # Analysis artifacts (matrices, strategies, activity log)
â”œâ”€â”€ drafts/           # Proposal section drafts (markdown authoring layer)
â”œâ”€â”€ graphics/         # Rendered HTML graphics (intermediate output)
â”œâ”€â”€ reviews/          # Red team, compliance, gap logs
â””â”€â”€ final/            # Native Office exports produced by /export-proposal
    â”œâ”€â”€ docx/         # Word documents (primary submission format)
    â”œâ”€â”€ xlsx/         # Excel (compliance matrix, pricing artifacts)
    â”œâ”€â”€ pptx/         # PowerPoint (optional briefings)
    â”œâ”€â”€ html/         # Self-contained HTML drafts (crisp vector figures, screen review)
    â”œâ”€â”€ pdf/          # User-produced via Word's Save As PDF
    â””â”€â”€ graphics-png/ # Graphics rendered to PNG for Word embed
```

**Output format discipline.** Authoring happens in markdown. Submission deliverables are native Microsoft Office formats (.docx/.xlsx/.pptx), produced by `/export-proposal` from the markdown sources. The `.md â†’ .docx â†’ .pdf` path (via Word's Save As PDF) preserves styling; the `.md â†’ .pdf` direct path does not and should not be used for federal submissions.

## File Output Rules
- Always write analysis to `working/` files
- Always write draft content to `drafts/` files
- Always write review findings to `reviews/` files
- Update files incrementally â€” don't overwrite without reason
- Use descriptive filenames that match the content

## Activity Trail (mandatory)

Every content-producing skill (submission-summary, proposal-manager, customer-intel, competitor-assessment, capture-scorecard, proposal-solution-architect, narrative-spine, proposal-graphics, past-performance, pricing-analyst, proposal-writer, red-team-review, compliance-check, import-from-capture, new-proposal) **MUST** update two files on successful completion:

### 1. `working/activity.md` â€” human-readable narrative

Append one line in this format:

```
## YYYY-MM-DD HH:MM â€” <skill-name> [<mode if any>] â€” <one-line summary> â†’ <primary output path>
```

- Append only â€” never rewrite the file
- One line per invocation, human-readable, factual
- Read-only skills (`/status`) do NOT append
- If `working/activity.md` does not exist, create it from `templates/working/activity.md`

### 2. `working/ai-runs.jsonl` â€” machine-readable AI run ledger (v1.5 Phase A)

Append one JSON Lines entry per AI model invocation conforming to [`reference/schemas/ai-run.schema.json`](reference/schemas/ai-run.schema.json):

```json
{"schema_version":"ai-run.v1","timestamp":"2026-04-22T15:30:00Z","skill":"proposal-manager","proposal_id":"cso-brief-acme","job_type":"planning","provider":"anthropic","model":"claude-opus-4-7","input_tokens_estimate":null,"output_tokens_estimate":null,"cost_estimate_usd":null,"notes":"eval factors + win themes extraction"}
```

- Append only (JSON Lines â€” one object per line, no surrounding array)
- One entry per model invocation (a skill that makes 3 AI calls produces 3 entries)
- `input_tokens_estimate` / `output_tokens_estimate` / `cost_estimate_usd` may be `null` in Phase A â€” real counts come from Anthropic SDK / Console in later phases
- `proposal_id` matches the proposals/<slug>/ directory name
- If `working/ai-runs.jsonl` does not exist, create it empty and append the first entry
- Read-only skills (`/status`) do NOT append

Both files are consumed by `/status`, the Phase B dashboard, and the smoke test.

## Writing Standards
- Direct, concise, technically grounded
- No filler or buzzwords
- No unsupported adjectives ("robust", "innovative", "scalable" without proof)
- Prefer concrete descriptions of components, functions, interfaces, workflows, outcomes
- Write like an evaluator has 15 minutes and a red pen
- **Apply the four winning patterns** (theme statements, discriminator proof points, action captions, ghosting) per `reference/proposal-writing-patterns.md`, gated by proposal type. These are enforced by `proposal-writer` and scored by `red-team-review` Gold Team.
- **Voice doctrine.** See `reference/PROSE-QUALITY-DOCTRINE.md` (canonical, synced from `chakmarebel/proposal-workbench` via `tools/sync-voice-anchors.sh`).

## Default Positioning
Positioning emphasis comes from `my-company/` (capabilities, differentiators,
positioning notes). Unless source material says otherwise, lead with the
differentiators and proof points declared there — never with generic claims the
company cannot substantiate.

## Review Standard
Before declaring anything "final," check for:
- Compliance gaps
- Unaddressed evaluator concerns
- Empty claims
- Repetition across sections
- Architecture/narrative mismatch
- Missing differentiation
