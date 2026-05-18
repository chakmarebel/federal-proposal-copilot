---
name: capture-intent
description: Use this skill early in the proposal lifecycle to define the strategic intent behind the bid, including customer belief objectives, discriminator strategy, competitive posture, acceptable risk, and narrative direction.
phase: capture
composes: [proposal-manager, customer-intel, competitor-assessment]
conflicts_with: []  # unique strategic layer; complements competitor-assessment, doesn't duplicate
---

# Capture Intent Skill

## Purpose

Define the strategic intent behind the proposal before drafting begins.

Most proposal systems understand:
- the solicitation
- the requirements
- the company capabilities

Very few understand:
- why the company is actually bidding
- what the customer must believe
- where the company is weak
- what strategic posture the proposal should take
- what the proposal should avoid saying
- what outcome the team actually wants

This skill creates the strategic alignment layer that guides:
- proposal-storyboard
- proposal-writer
- proposal-editor
- competitor-assessment
- red-team-review

Without this layer, proposals drift into generic capability summaries.

## When to Use

Run after opportunity qualification and before solution architecture/storyboarding.

Recommended workflow:

```
/proposal-manager
/customer-intel
/competitor-assessment
/capture-intent
/proposal-solution-architect
/proposal-storyboard
/proposal-writer
```

## Inputs

### Always read
1. `working/proposal-type.md`
2. `working/opportunity-summary.md`
3. `working/capability-matrix.md`
4. `working/requirement-matrix.md`
5. `my-company/company-profile.md`

### Read if relevant
- `working/customer-profile.md` — if `/customer-intel` was run (needed for belief objectives).
- `working/competitor-assessment.md` — if `/competitor-assessment` was run (needed for ghosting + posture).
- `working/teaming-strategy.md` — if teaming work has been done.
- `working/win-themes.md` — if `/proposal-manager` produced a standalone themes file.
- `my-company/evidence-ledger.json` — only when Phase C evidence is enabled.
- Solicitation documents and notes — sample, don't read end-to-end. Use only to clarify ambiguous strategic questions.

## Required Output

Write:

```
working/capture-intent.md
```

Optional:

```
working/capture-risks.md
working/discriminator-map.md
```

## Core Questions

The skill must answer the following questions explicitly.

---

# 1. Why Are We Bidding?

## Goal

Define the actual strategic reason for pursuing the opportunity.

Examples:
- establish beachhead with customer
- transition prototype into production
- expand footprint into adjacent mission space
- demonstrate capability for future larger contract
- strengthen OEM/system-integrator relationship
- gain operational deployment reference
- position for sole-source follow-on
- expand into classified environment
- maintain strategic relevance
- establish credibility in emerging mission area

## Rules

Do not write generic statements like:
> "This opportunity aligns with company growth goals."

Be specific.

---

# 2. What Must the Customer Believe?

## Goal

Define the 3-5 core beliefs the proposal must create.

Examples:

- This team understands operational DDIL realities.
- This architecture can realistically deploy into existing Government infrastructure.
- The company is technically mature despite small size.
- The integration risk is manageable.
- The proposed pilot creates a low-risk path to operational adoption.
- This solution complements, rather than replaces, existing systems.

These become the hidden backbone of the proposal.

---

# 3. What Is Our Strongest Discriminator?

## Goal

Identify the actual differentiators that matter.

Distinguish between:
- real discriminator
- table stakes
- marketing noise

Examples:

| Category | Example |
|---|---|
| Real discriminator | Existing IL6 deployment in similar mission environment |
| Table stakes | Agile development |
| Marketing noise | "Transformative AI platform" |

## Rules

A discriminator only counts if:
- evaluators care
- competitors likely lack it
- evidence exists
- it reduces risk or improves mission outcome

---

# 4. What Is Our Weakest Area?

## Goal

Explicitly identify proposal vulnerabilities.

Examples:
- limited past performance with this customer
- integration experience gap
- no production CDS deployment
- staffing scale concern
- unclear hardware path
- immature commercialization story
- limited operational deployment history

## Rules

Do not hide weaknesses.

The downstream proposal strategy depends on knowing them.

---

# 5. What Should the Proposal Avoid Saying?

## Goal

Define language, positioning, and claims that would damage credibility.

Examples:
- avoid implying enterprise replacement
- avoid overstating autonomy
- avoid claiming automatic ATO reciprocity
- avoid attacking incumbent directly
- avoid overexplaining model architecture
- avoid superiority claims without evidence
- avoid making customer workflow sound obsolete

This is one of the highest-value sections.

---

# 6. What Competitive Posture Should We Take?

## Goal

Define the desired proposal posture.

Examples:

| Posture | Meaning |
|---|---|
| Operationally credible | Calm, technically mature, deployment-focused |
| Disruptive challenger | Faster, lighter, less bureaucratic |
| Trusted integrator | Low-risk execution and interoperability |
| Innovation partner | Experimentation and prototype acceleration |
| Specialized expert | Narrow but deep mission capability |
| Strategic bridge | Enables transition between ecosystems |

## Rules

Choose deliberately.

Do not mix incompatible postures.

---

# 7. What Is the Desired Next Action?

## Goal

Define what the proposal is actually trying to achieve.

Examples:
- invitation to Phase II
- technical interchange meeting
- pilot award
- OTA follow-on
- downselect retention
- integration workshop
- architecture review
- operational demonstration
- production contract

This changes how aggressively the proposal should sell.

---

# 8. Tone and Narrative Direction

## Goal

Define the intended narrative style.

Examples:

| Proposal Type | Preferred Tone |
|---|---|
| FAR technical volume | dense, traceable, evaluator-scored |
| DIU CSO | concise, operational, commercially credible |
| SBIR | technically rigorous with commercialization path |
| White paper | executive-readable and strategically focused |
| RFI | factual and capability-oriented |

## Also Define

- desired technical depth
- acceptable aggressiveness
- acceptable marketing level
- desired executive readability
- desired operational emphasis

---

# 9. Ghosting Strategy

## Goal

Define how the proposal should indirectly contrast competitors.

Examples:
- emphasize disconnected operation because competitors depend on cloud
- emphasize integration openness because competitors are proprietary
- emphasize operational deployment because competitors are lab-focused
- emphasize lightweight deployment because competitors are infrastructure-heavy

## Rules

Never name competitors.

Never sound petty.

Ghosting should feel like natural emphasis, not a direct attack.

---

# Output Format

Write:

```markdown
# Capture Intent — [Opportunity Name]

## Strategic Objective

<why the company is bidding>

---

## Customer Beliefs We Must Create

1. <belief>
2. <belief>
3. <belief>

---

## Primary Discriminators

| Discriminator | Why It Matters | Evidence | Risk |
|---|---|---|---|

---

## Vulnerabilities / Weak Areas

| Weakness | Risk | Mitigation Strategy |
|---|---|---|

---

## Proposal Posture

<desired strategic posture>

---

## Proposal Must Avoid

- <item>
- <item>

---

## Desired Customer Action

<desired next step>

---

## Tone and Narrative Guidance

| Area | Guidance |
|---|---|
| Tone | |
| Technical Depth | |
| Executive Readability | |
| Operational Emphasis | |
| Marketing Aggressiveness | |

---

## Ghosting Strategy

| Competitor Weakness | How We Indirectly Contrast |
|---|---|

---

## Strategic Narrative Summary

<2-4 paragraphs describing how the proposal should feel overall>
```

## Integration Rules

Downstream skills should consume this file as strategic guidance.

### proposal-storyboard
Uses:
- evaluator belief goals
- tone guidance
- prohibited claims
- ghosting direction

### proposal-writer
Uses:
- discriminator emphasis
- proposal posture
- customer-belief priorities

### proposal-editor
Uses:
- tone calibration
- marketing aggressiveness limits
- readability targets

### red-team-review
Uses:
- whether the proposal actually reinforced the intended beliefs
- whether ghosting aligned to strategy
- whether weaknesses were mitigated

## Anti-Patterns to Prevent

The capture-intent layer exists to prevent:

- proposals that sound strategically confused
- generic capability dumps
- contradictory messaging
- overaggressive positioning
- accidental overclaiming
- irrelevant differentiators
- executive summaries with no clear point
- technical detail disconnected from strategy
- weak ghosting
- inconsistent tone between sections

## Final Rule

This document is strategic guidance.

It should not read like proposal prose.

It should read like internal capture leadership alignment.

## Activity Trail

Append to `working/activity.md`:

```
## <timestamp> — capture-intent — defined strategic posture, discriminators, customer beliefs, and proposal guidance → working/capture-intent.md
```

Append to `working/ai-runs.jsonl`:

```json
{"schema_version":"ai-run.v1","timestamp":"<timestamp>","skill":"capture-intent","proposal_id":"<proposal>","job_type":"capture-strategy","provider":"anthropic","model":"claude-opus-4-7","input_tokens_estimate":null,"output_tokens_estimate":null,"cost_estimate_usd":null,"notes":"strategic capture alignment and narrative guidance"}
```
