---
name: narrative-spine
description: Use this skill after solution architecture and capture intent to write the proposal's narrative spine — a one-page, plain-prose argument of what the proposal claims and why it is compelling against the customer's actual problem — for human sign-off before storyboarding or drafting begins.
phase: planning
composes: [proposal-solution-architect, capture-intent]
conflicts_with: []  # complements proposal-storyboard — the spine is the lengthwise argument; the storyboard is the crosswise per-section plan
---

# Narrative Spine Skill

## Purpose

Write the proposal's **narrative spine** — the single, coherent argument the whole proposal makes — in plain prose, before any section structure or draft text exists.

The pipeline already produces requirement matrices, capability matrices, a proposal plan, a capture-intent document, and an architecture concept. What it has never produced is the thing a senior capture lead writes in their head before drafting: *the story of why this proposal wins against the customer's actual problem.* Win themes get reduced to a three-column table; the architecture gets recorded as a fielded concept; the strategic intent gets written as internal alignment notes. None of those is an argument. They are inputs to an argument.

Without a spine, the proposal-writer fills connective tissue between pre-validated atoms — and that is the structural cause of stilted, capability-tour prose. The spine is the missing artifact. It is what the storyboard decomposes and what the writer drafts from. It is also the cheapest possible place to put a human in the loop: one page, three minutes to read, easy to redirect.

## When to Use

Run **after** `/proposal-solution-architect` and `/capture-intent` (and after `/past-performance` and `/pricing-analyst` if the proposal type runs them — real proof points and the cost envelope should inform the argument). Run **before** `/proposal-storyboard`.

For white papers (which skip the storyboard), run it after `/proposal-solution-architect` and before `/proposal-writer`.

Recommended workflow:

```
/proposal-solution-architect
/past-performance        (if the type runs it)
/pricing-analyst         (if the type runs it)
/narrative-spine         <<< here — human signs off before continuing
/proposal-storyboard
/proposal-writer
```

## Inputs

### Always read

1. `working/proposal-type.md` — **read first.** If this skill is in `skipped_skills`, exit with "Skipped for type <type_id>." Note `page_target` and `evaluator_framing` — they control how ambitious the spine can be (see Discipline Rules).
2. **The solicitation and customer source material, directly** — every file in `inputs/00_priority/` and `inputs/01_customer/`. This is deliberate and non-negotiable. The narrative-spine skill is the one pre-prose stage that reads the customer's own words instead of a digested matrix. The argument has to answer the problem the customer actually stated, in language traceable to how they stated it.
3. `working/capture-intent.md` — strategic intent: why we are bidding, customer beliefs to create, posture, prohibited claims, ghosting direction. The spine operationalizes this into a single argument.
4. `working/proposal-plan.md` — evaluation criteria and win themes.
5. `working/architecture-concept.md` and `working/solution-strategy.md` — what is actually being proposed.
6. `reference/narrative-operating-modes.md` — use it to scale the argument to the response length and evaluator frame before writing the spine.
7. **`reference/voice-anchors/*.md`** — voice cadence exemplars. Read these before drafting the spine. Imitate their rhythm and clinical confidence; do NOT reuse their content. The spine is the first place voice matters, and getting its cadence right carries forward through the writer. (Canonical source: `reference/PROSE-QUALITY-DOCTRINE.md`.)

If a required input is missing, state it explicitly and proceed only if the argument can still be formed. If `capture-intent.md` is missing, recommend running `/capture-intent` first — without it the spine has no strategic posture to express.

### Read if relevant

- `working/customer-profile.md` — if `/customer-intel` was run (decision-maker hot buttons sharpen the argument).
- `working/competitor-assessment.md` — if `/competitor-assessment` was run (the argument should beat a real alternative, not a strawman).
- `drafts/past-performance.md` or `working/pp-relevance-matrix.md` — so the spine argues with real proof points.
- `working/pricing-inputs.md` — so the argument respects the cost/LOE envelope.
- `working/capability-matrix.md`, `working/requirement-matrix.md` — for grounding, not as the primary source.

## Output

Write **one file**:

```
working/narrative-spine.md
```

It is **prose**. It has no section numbers, no field tables, no per-section breakdown. If it looks like a storyboard, it is wrong — see Discipline Rules.

After writing it, **stop and hand it to the human** (see Human Sign-Off Gate).

## The Spine Standard

`working/narrative-spine.md` contains exactly five parts, in this order:

```markdown
# Narrative Spine — [Proposal Name]

## Positioning

<One sentence. What this proposal IS, framed against what it is not.
This is the line a reader should be able to repeat after a single read.
Example shape: "This is disconnected adaptive autonomy infrastructure for
tactical UxS operations — not another AI platform.">

## Narrative Mode

<One line naming the selected mode from `reference/narrative-operating-modes.md`
and the reason. Example: "Mode: solution-brief — 7-page CSO screener, so
the argument must establish fit, feasibility, proof, and next action without
teaching the whole market.">

## The Argument

<The case, in movements. One short paragraph per movement. A movement is
one beat of the argument — a claim the reader must accept before the next
one lands. Plain prose. No bullets. No section numbers. Write it the way
you would explain to a sharp colleague why this proposal wins. Typically
3-6 movements. Each movement should be traceable to a customer-stated
problem and to real evidence or architecture — not to what we wish were
true.>

## Through-Line

<One or two sentences naming the single idea the reader should still feel
at the end of the last section. If the argument has a heartbeat, this is
it.>

## What This Proposal Must Not Become

<2-4 bullets naming the drift the spine exists to prevent — e.g. "a tour
of company capabilities," "a brochure exec summary," "a restatement of
the SOO." Pulled from capture-intent's prohibited claims plus the failure
modes specific to this opportunity.>
```

## Discipline Rules

- **Prose, not structure.** The spine runs *lengthwise* through the whole proposal — it is the argument start to finish. The storyboard runs *crosswise* — a per-section table of fields. If `narrative-spine.md` has section numbers or a field table, it has become a storyboard. Delete and rewrite as prose.
- **Read the customer's own words.** Quote one or two short phrases from the solicitation that the argument must answer. The spine earns its keep by being demonstrably *about this customer's problem*, not a generic case.
- **Length-aware.** Match the spine's ambition to `page_target`. A 2-3 page white paper has no room to teach abstract concepts — its spine is ~150 words and compresses the argument into the tightest possible form. A 20-40 page proposal can afford to teach — its spine is up to one page and may name what each movement will explain. Do not write a 30-page-proposal spine for a white paper.
- **Mode-aware.** The selected narrative mode changes the spine's job. A `compressed-brief` spine should make the recommendation feel inevitable quickly. A `scored-volume` spine should keep compliance sections connected by one evaluator-facing case. A `technical-merit` spine should make the technical hypothesis, proof plan, and transition logic coherent.
- **One argument, not a list.** The spine asserts a single coherent case. If you cannot state it in one positioning sentence, the capture strategy is not resolved — say so plainly and recommend the user revisit `/capture-intent` rather than papering over it.
- **Honest.** The spine argues with the real evidence and the real weaknesses from `capture-intent.md`. It does not wish. A spine built on an unsupported claim produces a proposal built on an unsupported claim.
- **Do not draft proposal prose.** The spine is the plan for the argument. The storyboard decomposes it; the writer drafts it. Writing section text here defeats the purpose and collides with `/proposal-writer`.

## Human Sign-Off Gate

After writing `working/narrative-spine.md`, **stop.** Do not chain into `/proposal-storyboard` or `/proposal-writer`.

Emit a **decision card** (per [`reference/schemas/decision-card.schema.json`](../../../reference/schemas/decision-card.schema.json)) — present it to the user in chat, and append it as one JSON line to `working/decision-cards.jsonl`. The card makes the gate fast to act on without hiding the artifact:

```json
{"schema_version":"decision-card.v1","gate_id":"narrative-spine-approval","proposal_id":"<slug>","generated_by":"narrative-spine","generated_at":"<timestamp>","decision":"Approve the proposal's central argument before storyboarding/drafting begins.","artifact":"working/narrative-spine.md","recommendation":"<approve as written | approve with the noted change | revisit /capture-intent first>","confidence":"<High|Medium|Low>","rationale":"<one or two sentences>","risk_if_wrong":"<what the whole proposal gets wrong if this argument is off>","on_approval":"the storyboard decomposes this spine and the writer drafts it","human_time_estimate":"3 minutes","approve_action":"/proposal-storyboard","review_required":true}
```

`review_required` is **always `true`** for this gate. The card does not replace reading the one-pager — it frames it. Tell the user, explicitly:

> The narrative spine is written to `working/narrative-spine.md` — read the one page. This is the highest-leverage three minutes in the whole proposal: it decides the argument every section will carry, and it is the cheapest point to correct course. Edit it or approve it. When it reads right, run `/proposal-storyboard` (or `/proposal-writer` for a white paper).

The spine is the one stage designed for human judgment. Surface it and wait.

## Integration With Downstream Skills

- **`/proposal-storyboard`** decomposes the *approved* spine into sections. Each section storyboard should advance one movement of the argument; a section that advances no movement is a candidate for cutting.
- **`/proposal-writer`** reads `working/narrative-spine.md` first, as primary orientation. Every drafted section should be traceable to a movement of the spine. The writer drafts the argument; it does not invent a new one.
- **`/red-team-review`** checks whether the drafted proposal still carries the spine's through-line — a proposal that lost its spine in drafting is a red-team finding.

## Anti-Patterns to Prevent

The narrative-spine stage exists to prevent:

- capability-tour proposals (a list of what we do, with no argument)
- executive summaries that read like a company brochure
- sections that restate the solicitation instead of answering it
- proposals where every section is competent but the whole makes no case
- a "spine" that is secretly a storyboard (field tables, section numbers)
- an argument built on aspirational rather than real proof points

## Activity Trail

On completion, append one line to `working/activity.md`:

```
## <timestamp> — narrative-spine — wrote <N>-movement argument, positioning line set, handed to human for sign-off → working/narrative-spine.md
```

Append one JSON line to `working/ai-runs.jsonl` per [`reference/schemas/ai-run.schema.json`](../../../reference/schemas/ai-run.schema.json):

```json
{"schema_version":"ai-run.v1","timestamp":"<timestamp>","skill":"narrative-spine","proposal_id":"<proposal>","job_type":"planning","provider":"anthropic","model":"claude-opus-4-7","input_tokens_estimate":null,"output_tokens_estimate":null,"cost_estimate_usd":null,"notes":"narrative spine — pre-prose argument"}
```

## Final Rule

This skill plans the argument. It does not write the proposal. One page, prose, handed to a human. That is the whole job.
