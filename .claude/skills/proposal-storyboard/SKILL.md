---
name: proposal-storyboard
description: Use this skill after proposal-solution-architect and before proposal-writer to create section-by-section storyboards that define evaluator questions, required answers, proof points, graphics, target length, and prohibited claims before prose drafting begins.
phase: drafting
composes: [proposal-solution-architect, capture-intent, competitor-assessment]
conflicts_with: []  # unique pre-prose planning role
---

# Proposal Storyboard Skill

## Purpose

Decompose the approved narrative spine into a section-by-section writing plan before drafting prose.

The narrative spine (`working/narrative-spine.md`, produced by `/narrative-spine`) is the *lengthwise* argument — the case the whole proposal makes. The storyboard is the *crosswise* plan — what each section must do to advance that argument. It translates the approved spine, capture strategy, compliance matrix, solution architecture, and section pattern into a section-by-section writing plan, and prevents the proposal-writer from rambling, over-marketing, diving too deep technically, or forcing Shipley patterns where they do not improve the response.

The storyboard answers one question for every section:

> What must the evaluator understand, believe, and score after reading this section?

## When to Use

Run after `/proposal-solution-architect` and before `/proposal-writer`.

Recommended workflow:

```
/proposal-manager
/customer-intel
/competitor-assessment
/proposal-solution-architect
/proposal-storyboard
/proposal-writer
/proposal-editor
/compliance-check
/red-team-review --mode=red
```

## Inputs

### Always read
1. `working/proposal-type.md` — proposal type, page target, evaluator framing, section pattern.
2. `working/narrative-spine.md` — **the approved one-page argument (produced by `/narrative-spine`).** This is the primary input. The storyboard *decomposes* the spine: each section storyboard should advance one movement of the argument, and a section that advances no movement is a candidate for cutting. If `working/narrative-spine.md` does not exist, recommend the user run `/narrative-spine` first.
3. `working/compliance-matrix.md` — requirement traceability and coverage targets.
4. `working/proposal-plan.md` — evaluation criteria, win themes, bid strategy, discriminator candidates.
5. `working/solution-strategy.md`
6. `working/architecture-concept.md`
7. `reference/section-patterns/<section_patterns>.md` — derived from `working/proposal-type.md`.
8. `reference/narrative-operating-modes.md` — select the prose mode that matches `page_target`, `submission_mechanism`, and `evaluator_framing`. Record that mode in the storyboard header and apply it to section length, depth, and transition planning.

### Read if relevant
- `working/requirement-matrix.md` — for traceability columns in coverage map.
- `working/capability-matrix.md` — when storyboarding capability-mapped sections.
- `working/assumptions-and-risks.md` — when storyboarding risk/management sections.
- `working/customer-profile.md` — if `/customer-intel` was run.
- `working/competitor-assessment.md` — if `/competitor-assessment` was run (required for ghosting angles).
- `working/capture-intent.md` — if `/capture-intent` was run (drives belief objectives + prohibited claims).
- `working/graphics-brief.md` — if `/proposal-graphics` was run.
- `reference/proposal-conventions/<vehicle-id>.md` — if convention file exists for this type.
- `reference/editorial-voice-guide.md` — for tone-section calibration.
- `my-company/evidence-ledger.json` — only if Phase C evidence is enabled.

## Outputs

Write:

```
working/storyboard.md
working/storyboard-coverage-map.md
```

Optional, when useful:

```
working/storyboard-open-questions.md
```

## Storyboard Standard

Each section storyboard must be specific enough that a proposal writer can draft from it without inventing strategy.

For each required section, produce:

```markdown
## <section-id>: <Section Title>

**Purpose:** <why this section exists>

**Evaluator Question:** <the question the evaluator is trying to answer>

**Required Answer:** <the plain-English answer the section must provide>

**Primary Takeaway:** <one sentence the evaluator should remember>

**Reader Movement:** <what the reader believes before this section -> what they should believe after it>

**Narrative Mode:** <compressed-brief | solution-brief | scored-volume | technical-merit | market-research | pricing-artifact>

**Transition Job:** <consequence | selection | proof | decision | none/formal response>

**Requirements Covered:** <Req IDs from compliance matrix, or "None/formal compliance not applicable">

**Evaluation Factor / Scoring Tie:** <Section M factor, AOI, CSO criterion, SBIR merit factor, or reader concern>

**Customer Language to Reuse:**
- <exact term or phrase from solicitation/customer docs>
- <exact term or phrase>

**Claims Allowed:**
- <claim that may be made, with evidence or source>

**Claims Prohibited or Must Be Qualified:**
- <claim that should not be made or must be softened>

**Proof Points / Evidence:**
- <evidence item, past performance, benchmark, deployment, named artifact, or CLAIM-UNSUPPORTED marker>

**Solution Content to Include:**
- <specific architecture/process/capability content>

**Competitor / Ghosting Angle:**
- <positive contrast only, or "None">

**Graphic Needed:** <Yes/No>

**Graphic Argument:** <what the graphic must prove, not merely show>

**Recommended Figure Caption:**
> *Figure X. <Title>.* <action caption asserting what the figure proves>.

**Target Length:** <word count or page fraction>

**Compression Rule:** <what to cut first if the section runs long, and what must survive>

**Do Not Say:**
- <phrase, claim, or rabbit hole to avoid>

**Drafting Notes:**
- <specific instructions to proposal-writer>
```

## Storyboard Quality Rules

### Be Specific

Bad:
> Discuss technical approach.

Good:
> Explain how local inference continues analyst workflows when SIPR/cloud connectivity is unavailable, then tie that architecture to the solicitation's DDIL requirement and the prior Navy/Army deployment evidence.

### Answer Evaluator Questions

Every section must map to the question the evaluator is actually asking.

Examples:

| Section | Evaluator Question |
|---|---|
| Executive Summary | Why should I care, and why this team? |
| Technical Approach | Does this solution actually meet the requirement with manageable risk? |
| Management Approach | Can this team execute without creating schedule, staffing, or integration risk? |
| Past Performance | Has this team done similar work under similar conditions? |
| White Paper Approach | Is this credible enough to justify a meeting, pilot, CSO award, or follow-on ask? |
| RFI Response | Is this company relevant to the requirement and worth shaping around? |

### Control Claims

The storyboard must distinguish between:

- verified claims
- reasonable inferences
- assumptions
- unsupported claims
- prohibited claims

If a claim is not supported, do not let the writer discover that during drafting. Flag it upfront.

### Control Depth

Specify where technical detail belongs and where it does not.

Examples:

- Executive summary: operational outcome only; no container/runtime implementation detail
- Technical approach: architecture and interfaces; enough detail to establish feasibility
- Management approach: execution controls; no generic agile sermon
- White paper: pilot logic and transition path; avoid FAR-style boilerplate

### Control Tone

The storyboard should state the intended tone for each section.

Examples:

- concise and executive-readable
- dense and evaluator-scored
- plainspoken and pilot-oriented
- technical but not academic
- factual and non-salesy

### Plan Reader Movement

Every section must move the evaluator somewhere. Do not merely list the artifacts the writer should include.

For each section, answer:

- What does the reader believe before this section?
- What should the reader believe after this section?
- What proof, mechanism, or commitment creates that shift?
- What transition connects this section to the prior movement of the narrative spine?

If the answer is "the reader learns more about our capability," the section is not planned tightly enough. Reframe it as a decision, scoring, risk, or mission-value movement.

### Select the Narrative Operating Mode

Use `reference/narrative-operating-modes.md` to choose one mode for the whole response and, if needed, a section-specific override:

- `compressed-brief` for 1-5 page white papers, short directed briefs, and tight web-form fields.
- `solution-brief` for 5-10 page CSO/OTA/white-paper responses.
- `scored-volume` for FAR, IDIQ, OTA full, and CSO full proposals.
- `technical-merit` for SBIR and BAA technical merit responses.
- `market-research` for RFI and sources-sought.
- `pricing-artifact` for ROM and price narratives.

The mode controls depth. A compressed brief should not spend paragraphs teaching the market. A scored volume should not hide compliance structure in elegant prose. A technical-merit response should not replace mechanism with sales language.

## Coverage Map

Create `working/storyboard-coverage-map.md` with a table:

| Req ID / Eval Criterion | Storyboard Section | Planned Proof | Graphic | Risk / Gap |
|---|---|---|---|---|

Use this to ensure the storyboard covers every known requirement before prose begins.

If a requirement has no planned section home, mark it as a gap. Do not bury it.

## Open Questions

Create `working/storyboard-open-questions.md` if any of the following are true:

- a required claim lacks evidence
- a requirement has no clear section home
- a graphic is needed but the argument is unclear
- a technical commitment may exceed known capability
- the solicitation language is ambiguous
- page budget appears insufficient
- competitor ghosting would require unsupported assumptions

Format:

| Question | Why It Matters | Proposed Default if Unanswered |
|---|---|---|

## Integration with Proposal Writer

After `working/storyboard.md` exists, `/proposal-writer` should treat it as the primary drafting plan.

The proposal writer should not invent:
- new win themes
- new discriminators
- new ghosting angles
- new major claims
- new graphics
- new section structure

If the writer believes the storyboard is insufficient, it should flag the gap rather than writing around it.

## Anti-Patterns to Prevent

The storyboard must prevent:

- generic capability summaries
- executive summaries that read like company brochures
- technical sections that bury the answer under implementation detail
- sections that are individually compliant but do not advance the narrative spine
- transitions that announce structure instead of carrying the argument
- management sections filled with agile boilerplate
- repeated DDIL/cloud/edge explanations across every section
- proof points appearing after the evaluator needs them
- ghosting that sounds obvious or petty
- graphics that decorate instead of prove
- unsupported "leading provider" or "best-in-class" claims

## Activity Trail

Append to `working/activity.md`:

```
## <timestamp> — proposal-storyboard — planned <N sections>, mapped <M requirements>, flagged <K open questions> → working/storyboard.md
```

Append to `working/ai-runs.jsonl`:

```json
{"schema_version":"ai-run.v1","timestamp":"<timestamp>","skill":"proposal-storyboard","proposal_id":"<proposal>","job_type":"storyboarding","provider":"anthropic","model":"claude-opus-4-7","input_tokens_estimate":null,"output_tokens_estimate":null,"cost_estimate_usd":null,"notes":"section-level storyboard and coverage map"}
```

## Final Rule

Do not draft proposal prose in this skill.

This skill plans the answer. The writer drafts the answer. The editor makes it sound human.
