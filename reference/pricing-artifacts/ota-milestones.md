---
artifact_id: ota-milestones
output_file: drafts/milestone-schedule.md
companion_file: working/pricing-inputs.md
mental_model: Payment-on-completion schedule tied to demonstrable deliverables — not a cost volume
must_not_produce:
  - FAR Part 15 cost volume
  - CLIN structure
  - DCAA-audit-ready labor hour tables
  - DFARS 252.227 data rights assertions (assert under 10 USC 4022)
  - Time-and-materials or cost-plus structure (OTAs are typically milestone-payment)
---

# OTA Milestone Payment Schedule

## Mental model
The Agreements Officer is structuring a prototype agreement under 10 USC 4022. They care about: what gets demonstrated at each milestone, what's the acceptance criterion, what's the payment, and is the total reasonable for the prototype scope.

The evaluator is NOT doing FAR Part 15 cost realism analysis. They are doing **prototype-value analysis**: is the milestone worth the payment?

## Required inputs (ask the user)

### Basics
- Consortium or direct award (and vehicle if consortium, e.g., TReX, DIU CSO, S2MARTS)
- Statement of Objectives (SOO) — provides the anchor deliverables
- Prototype project scope summary
- Target period of performance (months)
- Target total price (ceiling)

### Team
- Prime + teammates
- Non-traditional contributor status (required for some OTA authorities — verify)
- Cost-share commitment (if any — often required when prime is traditional)

### Milestones
- Number of milestones (typically 3-6 for a 12-24 month prototype)
- For each milestone: title, one-sentence deliverable description, acceptance criterion, duration from prior milestone, payment amount
- Cost buildup **not required** in the deliverable — keep internal in `working/pricing-inputs.md`

### Follow-on production
- Will you assert follow-on production eligibility under 10 USC 4022(f)?
- If yes: name the expected Phase III / production vehicle

### Data rights
- What technical data / software will be developed?
- Assertions under 10 USC 4022 (not DFARS 252.227)

## Calculation approach

Milestone pricing is typically derived from an **internal cost estimate** (which does look like a FAR buildup — labor hours, ODCs, etc.) but is **expressed externally as milestone payments**.

Keep the internal buildup in `working/pricing-inputs.md`. The customer-facing artifact shows only milestones, deliverables, and payment amounts.

Milestones should be:
- **Discrete** — independently demonstrable
- **Verifiable** — acceptance criterion is unambiguous
- **Paced** — roughly equal difficulty (avoid one tiny milestone and one huge one)
- **Value-proportional** — each payment matches the value of what was demonstrated

## Output structure (`drafts/milestone-schedule.md`)

```markdown
# Milestone Payment Schedule — [Prototype Project Name]

**Prime:** [Company] ([traditional / non-traditional])
**Teammates:** [list, with status]
**Vehicle:** [Direct OTA / Consortium name]
**SOO Reference:** [section of the SOO this addresses]
**Period of Performance:** [N] months
**Total Prototype Cost:** $[Total]
**Cost Share:** [amount or N/A]
**Follow-on Production:** Asserted under 10 USC 4022(f) — [describe expected Phase III vehicle]

## Statement of Objectives Crosswalk

| SOO Objective | Addressed in Milestone(s) |
|---|---|
| [SOO 1] | M1, M3 |
| [SOO 2] | M2, M4 |
| ... | ... |

## Milestone Schedule

| # | Title | Deliverable | Acceptance Criterion | Duration | Payment |
|---|---|---|---|---:|---:|
| M1 | [title] | [what gets delivered — document, prototype, demo] | [how the government confirms it's done] | Month [N] | $[X] |
| M2 | [title] | ... | ... | Month [N] | $[X] |
| M3 | [title] | ... | ... | Month [N] | $[X] |
| M4 | [title] | ... | ... | Month [N] | $[X] |
| **Total** | | | | [N] months | **$[Total]** |

## Milestone Narratives

### M1 — [title]
**Scope.** [2-3 sentences on what is performed to produce the deliverable.]
**Deliverable.** [Specific artifact: report, code drop, live demo, prototype hardware, etc.]
**Acceptance criterion.** [How the government verifies completion. Must be unambiguous.]
**Payment.** $[X] upon acceptance.

### M2 — [title]
[Same structure]

[Repeat for each milestone]

## Cost Share (if applicable)
[1 paragraph. How much, what it covers, how it's tracked.]

## Data Rights
Data rights will be asserted under 10 USC 4022 for this prototype agreement. Specific assertions:

| Data / Software Item | Category | Basis |
|---|---|---|
| [e.g., inference engine source code] | Restricted | Developed exclusively at private expense prior to award |
| [e.g., prototype integration scripts] | Government Purpose Rights | Developed partly with government funding under this agreement |

## Follow-on Production

This prototype agreement is structured to support a follow-on production agreement under 10 USC 4022(f). Upon successful completion of the prototype (all milestones accepted), the Government may award a follow-on production agreement without further competition, subject to:
- Successful prototype completion as defined by milestone acceptance criteria
- Government requirement continuing to exist
- Negotiated terms with the awardee
```

## `working/pricing-inputs.md` (companion — internal)

This is where the cost buildup lives. Do not share externally.

```markdown
# OTA Pricing Inputs (Internal)

## Milestone cost buildup

### M1 — [title] — $[X]
- Direct labor: [hours × blended rate] = $[X]
- ODCs: $[X]
- Subs: $[X]
- Indirect (loaded into blended rate OR shown separately): $[X]
- Fee equivalent: $[X]
- **Total: $[X]**

[Repeat per milestone]

## Rate basis
[Blended rates or full buildup — document the source]

## Cost share rationale (if applicable)
[What you're contributing, why, how tracked]

## Non-traditional contributor analysis
[If prime is traditional, show ≥1/3 of total cost from non-traditional teammates OR identify the "significant participation" rationale]
```

## Pitfalls
- **Producing a FAR cost volume** — tells the AO you don't understand OTAs. Biggest red flag.
- **Milestone payments that front-load** — e.g., 60% at M1. AO will push back. Pace payments to demonstrated value.
- **Vague acceptance criteria** — "Government reviews and approves" is not an acceptance criterion. Specify what makes it pass.
- **Forgetting follow-on production language** — you cannot add 10 USC 4022(f) assertions after award. Include them now.
- **DFARS data rights** — wrong authority. Use 10 USC 4022.
- **Missing non-traditional analysis** — if prime is traditional, OTA eligibility hinges on teammate mix or cost share. Document it.
