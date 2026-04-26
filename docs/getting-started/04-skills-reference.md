# 04 — Skill Reference

Quick reference for every skill the framework ships. For a workflow walkthrough, see [03-first-proposal.md](03-first-proposal.md).

## Setup skills

| Skill | Purpose | When |
|---|---|---|
| `/setup-company` | Populates `my-company/` with your identity, capabilities, past performance, vehicles, brand | One-time setup |
| `/new-proposal` | Scaffolds a new proposal workspace; selects proposal type from registry | Once per proposal |
| `/import-from-capture` | Imports an opportunity payload from a BD pipeline tool (optional) | If you use a capture tool |

## Triage and planning

| Skill | Purpose | Output |
|---|---|---|
| `/opportunity-quick-look` | Rapid 7-criterion triage; PASS / HOLD / NO-BID | `working/quick-look.md` |
| `/proposal-manager` | Decompose requirements, build compliance matrix, win themes, bid/no-bid | `working/proposal-plan.md` + `working/compliance-matrix.md` |
| `/customer-intel` | Profile decision makers, buying history, hot buttons | `working/customer-profile.md` |
| `/competitor-assessment` | Identify competitors, comparison chart, teaming gaps | `working/competitor-assessment.md` |
| `/capture-scorecard` | 9-dimension go/no-go readiness check | `working/capture-scorecard.md` |
| `/capture-portal-structure` *(when applicable)* | Capture web-form portal field requirements | `working/portal-format.md` |

## Solution development

| Skill | Purpose | Output |
|---|---|---|
| `/proposal-solution-architect` | Map requirements to capabilities, design architecture, identify assumptions and risks | `working/` (5 files) |
| `/proposal-graphics` | Graphics brief + rendered HTML/SVG figures | `working/graphics-brief.md` + `graphics/` |
| `/past-performance` | Map PP to eval criteria, draft narratives, Past Performance Coverage Matrix | `drafts/past-performance.md` |
| `/pricing-analyst` | Cost model, BOE narratives — dispatches by `pricing_artifact` in proposal type | `working/pricing-inputs.md` + vehicle-specific artifact |

## Drafting and review

| Skill | Purpose | Output |
|---|---|---|
| `/proposal-writer` | Draft every required section; update compliance matrix with coverage | `drafts/<section>.md` |
| `/compliance-check` | Diff required vs. covered requirements | `reviews/compliance-gaps.md` |
| `/evidence-check` | Audit evidence citations against `my-company/evidence-ledger.json` | `reviews/evidence-check.md` |
| `/red-team-review` | Pink (compliance) → Red (narrative) → Gold (mock eval) → White Glove (final QA) | `reviews/<mode>-review.md` |
| `/export-proposal` | Convert markdown drafts to native .docx / .xlsx / .pptx | `final/` |

## Read-only / utility

| Skill | Purpose |
|---|---|
| `/status` | Pipeline state, compliance coverage, next recommended command |

## Skill gating by proposal type

Each proposal type declares `required_skills` and `skipped_skills` in its registry entry. For example:

- **`far-rfp`** uses the full chain (most competitive workflow)
- **`white-paper`** skips `competitor-assessment`, `capture-scorecard`, `pricing-analyst` (no formal pricing for white papers)
- **`rom`** skips most skills — only runs `proposal-manager`, `pricing-analyst`, `proposal-writer`
- **`rfi`** skips `pricing-analyst`, `competitor-assessment`, `red-team-review` modes Red and Gold

If you invoke a skill that the proposal type lists as `skipped_skills`, the skill exits with `Skipped for type <type_id>` and produces no output. This is intentional — it prevents wasted effort.

To see which skills apply to your proposal type, check `working/proposal-type.md` after `/new-proposal` runs, or browse [reference/proposal-types/](../../reference/proposal-types/).

## Red Team modes

The `/red-team-review` skill supports nine modes mapped to the Shipley color-team model:

| Mode | When | Purpose |
|---|---|---|
| `--mode=blue` | Capture phase | Review the capture plan and win strategy |
| `--mode=black-hat` | Capture phase | Competitive simulation — what would competitor X bid? |
| `--mode=storyboard-pink` | Pre-draft | Compliance check on storyboards before drafting |
| `--mode=pink` | After first draft | Compliance review on the actual draft |
| `--mode=red` | After complete draft | Narrative review — writes to score? |
| `--mode=mock-eval` | Backward-compat alias for older Gold behavior | Rubric-driven mock evaluation |
| `--mode=gold` | Pre-submit | Executive profit/risk sign-off |
| `--mode=white-glove` | Final QA | Typos, formatting, page-limit check |
| `--mode=lessons-learned` | Post-submit | Capture what worked, what didn't |

Default (no mode flag) runs the most common chain: Pink → Red → Gold → White Glove.

## More info

- [Methodology library](../../reference/methodology/) — Shipley alignment, color teams, capture planning, BD process
- [Section patterns](../../reference/section-patterns/) — per-vehicle section orders and templates
- [Proposal conventions](../../reference/proposal-conventions/) — calibrated structural conventions per vehicle
- [Evaluator rubrics](../../reference/evaluator-rubrics/) — scoring rubrics applied by Gold Team
