---
name: pricing-analyst
description: Develop the pricing artifact appropriate to the proposal type (ROM, SBIR budget, OTA milestones, CSO commercial pricing, or FAR cost volume). Reads working/proposal-type.md first and dispatches to the matching template in reference/pricing-artifacts/. Do NOT produce a generic cost volume for every type.
phase: drafting
composes: [proposal-solution-architect, proposal-manager]
conflicts_with: []  # dispatch on pricing_artifact yields one artifact per type; no peer
---

# Pricing Analyst Skill

## Dispatch on Proposal Type

**Read `working/proposal-type.md` before anything else.** The `pricing_artifact` field determines which template to follow. Do not guess — look it up.

| `pricing_artifact` | Template | Markdown output | Native Office output (via `/export-proposal`) |
|---|---|---|---|
| `none` | (skip) | none | none |
| `rom` | `reference/pricing-artifacts/rom.md` | `drafts/rom.md` | `.docx` only |
| `sbir-budget` | `reference/pricing-artifacts/sbir-budget.md` | `drafts/sbir-budget.md` | `.docx` narrative + **`.xlsx` is the primary artifact** (budget lives in Excel) |
| `ota-milestones` | `reference/pricing-artifacts/ota-milestones.md` | `drafts/milestone-schedule.md` | `.docx` + `.xlsx` (milestone schedule for PMO tracking) |
| `cso-commercial` | `reference/pricing-artifacts/cso-commercial.md` | `drafts/cso-pricing.md` | `.docx` only (commercial-item pricing is short) |
| `far-cost-volume` | `reference/pricing-artifacts/far-cost-volume.md` | `drafts/cost-volume.md` | `.docx` narrative + **`.xlsx` appendix** (CLIN tables, rate buildups, WBS × LCAT hours) |
| `gsa-mas-pricing` | `reference/pricing-artifacts/gsa-mas-pricing.md` | `drafts/price-narrative.md` | `.docx` narrative (2-3 pp, LCAT mapping table) + **single-sheet `.xlsx`** with Schedule-rate × period × LCAT computation (`"$"#,##0.00` format, `=ROUND(CELL*N,N)` and `=SUM(CELL:CELL)` patterns) |

**Process:**
1. Read `working/proposal-type.md`.
2. If `pricing_artifact: none` → exit with: "No pricing artifact required for type `<type_id>`. Skipped."
3. Otherwise, read the matching template file in `reference/pricing-artifacts/`.
4. Follow that template's Required Inputs, Calculation Approach, Output Structure, and Pitfalls sections. Each template has its own input-collection prompts and `must_not_produce` list — honor both.
5. Write to the template's declared `output_file` (in `drafts/`) and `companion_file` (`working/pricing-inputs.md`).

**Do not mix artifacts.** If the type says `rom`, do not produce a FAR cost volume "just to be thorough." Producing the wrong artifact for the vehicle signals misunderstanding of the procurement and hurts scoring.

If `working/proposal-type.md` is missing, instruct the user to run `/new-proposal` or copy a file from `reference/proposal-types/`. Do not fall back to a default.

## Purpose
Translate the approved solution architecture (or scope summary, for lightweight types) into the pricing artifact required by the vehicle. Pricing is not just numbers — it is an argument for value and a commitment to execution at a stated cost, in the format the reader expects.

## When to Use
- A pricing artifact is required by the proposal type (see dispatch table above)
- For heavier artifacts (`far-cost-volume`, `ota-milestones`, `sbir-budget`, `cso-commercial`): solution architecture should exist first (`working/solution-strategy.md`, `working/architecture-concept.md`)
- For `rom`: a scope summary is sufficient; architecture is optional
- Run after `/proposal-solution-architect` (or directly after `/new-proposal` for `rom`), before or parallel to `/proposal-writer`

## Inputs (shared across all artifacts)

Read before prompting for any information:
- `working/proposal-type.md` — **first.** Determines the dispatch.
- `working/proposal-plan.md` — pricing format requirements, evaluation weight for price, contract type (if this skill is applicable per the type)
- `working/solution-strategy.md` — scope of work, deliverables, key activities (optional for `rom`)
- `working/architecture-concept.md` — components, interfaces, deployment model (optional for `rom`)
- `working/requirement-matrix.md` — scope and performance requirements (if exists)
- `inputs/00_priority/` — solicitation for any stated pricing format requirements
- **The matching artifact template** (`reference/pricing-artifacts/<artifact>.md`) — for Required Inputs, Calculation Approach, Output Structure, and Pitfalls specific to this vehicle

## Interactive Input Collection

The artifact template drives the inputs. Each template has its own "Required inputs (ask the user)" section tailored to that vehicle — e.g., ROM wants scope + duration + range method; FAR cost volume wants LCATs, indirect rates, CLINs, ODCs, fee.

**Do not ask for inputs that aren't in the template's required list.** If the user volunteers DCAA-level detail for a ROM, note it in `working/pricing-inputs.md` but don't bloat the deliverable with it.

## Workflow

1. Read `working/proposal-type.md` and identify `pricing_artifact`.
2. If `none`, exit with note.
3. Read the matching `reference/pricing-artifacts/<artifact>.md`.
4. Honor its `must_not_produce` list — this prevents drift (e.g., producing a FAR cost volume when the type calls for a ROM).
5. Collect inputs per that template's input list.
6. Run the template's Calculation Approach.
7. Write the output file per the template's Output Structure.
8. Write the companion `working/pricing-inputs.md` per the template's companion-file structure.
9. On completion, append to `working/activity.md`:
   ```
   ## <timestamp> — pricing-analyst [<artifact_id>] — <total $ or range> → <output_file>
   ```

## Output Files
**Always write to disk — never just display in chat.**

Output path depends on `pricing_artifact` — see dispatch table at the top. Companion file is always `working/pricing-inputs.md`.

## Pricing Strategy Rules (apply to every artifact)

- Never price below your cost to execute — a win you can't deliver is worse than a loss.
- Acknowledge assumptions explicitly. Every assumption that inflates cost should be callable out so the customer can provide GFE or change scope. Every assumption that deflates cost is a risk you absorb.
- Match format to vehicle. Producing FAR-style BOEs for a CSO, or ROM ranges for a FAR RFP, signals unfamiliarity.
- Price every commitment. If the technical volume says "we will provide X," the pricing artifact must fund it.
- For LPTA: sharpen the pencil on ODCs and overhead; margin compression is expected.
- For best value: price to win on merit, not lowest cost; defend the fee as risk-appropriate.

## After Running This Skill
Tell the user:
1. Which artifact was produced (type + file path)
2. Headline number (range for ROM, total for everything else)
3. Top 3 pricing risks or assumptions
4. Any price-to-win or must-not-produce flags triggered
5. Confirm the output file + `working/pricing-inputs.md` were written
6. Activity trail entry appended

---

## Lessons Learned

### On BOE Narratives
- Evaluators read BOE narratives to assess whether the team understands the work. A vague BOE ("we will provide X senior engineers as needed") signals that the team hasn't thought through execution.
- Engineering build-up estimates (hours derived from task analysis) are more credible than analogy estimates ("we did something similar for $Y").

### On Fee
- Fee is not just profit — it is a signal of confidence and risk tolerance. Too low (below 8%) looks desperate. Too high (above 12% on a competitive bid) draws scrutiny. Match fee to competition type and risk profile.

### On Teaming / Subcontracts
- Price subcontractor work as pass-through with a small handling fee (typically 5-8%). Excessive markup on subcontracts is a red flag for evaluators.
- If a subcontractor's work is core to the solution, justify why it's not being done by the prime.

### On Assumptions
- Every assumption that inflates cost should be called out so the customer can choose to provide GFE or change scope to reduce price.
- Every assumption that deflates cost is a risk — if the assumption is wrong, you absorb the overrun.
