# Editorial Voice Guide

This guide calibrates proposal prose after the drafting pass. It is intentionally different from the Shipley/process guidance. The drafting workflow creates compliant raw material; the editorial pass turns that material into writing that sounds credible, natural, and submission-ready.

## Editorial Objective

Write like a senior capture lead and solution architect who understands the customer's mission, the solicitation, and the offeror's actual delivery capacity. The prose should be clear, technically grounded, and evaluator-friendly without sounding like a brochure or a template.

The editor's job is not to make the proposal more exciting. The editor's job is to make it more believable, easier to score, and harder to dismiss.

## Core Voice

- Direct, calm, and operationally credible
- Plain language with enough technical specificity to prove substance
- Confident where evidence exists; restrained where evidence is limited
- Customer-first, not company-first
- Written for a busy Government evaluator, not a marketing audience

## Narrative Mode Calibration

Before editing, read `reference/narrative-operating-modes.md` and identify the draft's mode from `working/proposal-type.md`.

- `compressed-brief`: cut setup, concept teaching, and secondary proof. The recommendation or offer must be clear on the first page.
- `solution-brief`: keep problem -> approach -> proof -> next action visible. Preserve only the technical detail that proves feasibility or transition value.
- `scored-volume`: preserve traceability and evaluator signposts, but make section openings and closings carry the narrative spine.
- `technical-merit`: preserve mechanism, hypothesis, work plan, and risk controls. Remove product brochure voice.
- `market-research`: answer directly and avoid proposal theatrics.
- `pricing-artifact`: keep assumptions, ranges, and exclusions visible; remove sales prose.

If the prose sounds polished but mismatched to its mode, it is not done.

## What Good Sounds Like

Good proposal prose usually does four things in order:

1. Names the customer's problem or evaluation concern.
2. States the offeror's answer in plain terms.
3. Explains how it works at the level needed for credibility.
4. Ties the point to proof, risk reduction, or mission value.

### Good Pattern

> The Government needs an approach that works when enterprise connectivity is unavailable, degraded, or intentionally restricted. [Company] addresses this by running mission-tailored inference locally on approved hardware, allowing users to continue core workflows without waiting on reach-back services. This reduces operational risk in DDIL environments while preserving a path for enterprise synchronization when connectivity returns.

### Bad Pattern

> [Company] delivers a cutting-edge, scalable, next-generation AI capability that leverages innovative architectures to transform mission outcomes across the enterprise and tactical edge.

The bad version is empty. It could describe any company. It creates no evaluator confidence.

## Rewrite Priorities

Apply these in order:

1. **Preserve compliance.** Do not remove required content, requirement references, or solicitation terminology.
2. **Preserve evidence.** Do not delete proof points, evidence markers, or past-performance facts unless they are unsupported or redundant.
3. **Improve naturalness.** Make the prose sound like a human expert wrote it.
4. **Reduce hype.** Replace marketing adjectives with observable facts.
5. **Reduce cognitive load.** Shorten overbuilt sentences, split dense paragraphs, and move lists into bullets where useful.
6. **Sharpen evaluator takeaways.** Make the scoreable point obvious.
7. **Flag, do not hide, uncertainty.** If a claim is unsupported, soften it or mark it rather than laundering it into confident prose.

## Anti-Patterns to Remove

| Anti-pattern | Why it hurts | Editorial fix |
|---|---|---|
| Marketing stack | Sounds like a brochure | Replace adjectives with functions, constraints, and evidence |
| Process theater | Talks about methodology instead of answer | Lead with the customer's outcome, then describe the process only if needed |
| Template voice | Reads like Shipley guidance pasted into prose | Convert pattern language into normal sentences |
| Artifact stitching | Moves from matrix to matrix instead of idea to idea | Restore the narrative spine and use transitions that show consequence, proof, selection, or decision |
| Over-technical dive | Loses evaluator before the point lands | State the conclusion first, then technical details |
| Unsupported superiority | Creates weakness in evaluation | Add proof, soften, or remove |
| Passive delivery commitments | Hides accountability | Use active voice for what the offeror will deliver |
| Repetition across sections | Wastes page budget | Assign each idea to one section and cross-reference if needed |
| Customer-blind language | Talks about company capability without mission tie | Start from the customer's stated need or evaluation factor |

## Banned or Suspect Phrases

Avoid or replace unless the solicitation uses the term or the phrase is technically necessary:

- cutting-edge
- innovative
- robust
- seamless
- transformative
- best-in-class
- world-class
- next-generation
- game-changing
- mission-critical, unless the customer uses it
- leverage, as a verb
- utilize
- holistic
- comprehensive, unless describing actual scope
- scalable, unless describing scale mechanism
- end-to-end, unless defining the actual endpoints
- integrated solution, unless explaining what is integrated and how
- proven, unless immediately backed by evidence

## Preferred Word Choices

| Instead of | Prefer |
|---|---|
| utilize | use |
| leverage | use, apply, extend |
| robust | describe the failure mode it withstands |
| innovative | describe what is new or different |
| §3.2 / §§3–4 (section-sign glyph) | Section 3.2 / Sections 3–4 — spell it out; refer to the section by name where possible. The § glyph never appears in proposal prose. |
| seamless | describe the interface or workflow |
| scalable | describe the scale path |
| solution | system, approach, architecture, workflow, capability — whichever is precise |
| enables enhanced | enables, improves, reduces, supports |
| designed to provide | provides, delivers, supports |

## Sentence Discipline

- Use short opening sentences for important points.
- Use longer technical sentences only when they carry real content.
- Keep most paragraphs to 3-5 sentences.
- Split paragraphs when they mix problem, approach, proof, and management details.
- Do not open every section with the same formula.
- Do not force a theme statement when a plain topic sentence is stronger.
- Vary section openings; repeated "Our approach..." or "This section..." rhythms create AI smell.
- Make transitions explain why the next idea follows, not merely that another section has begun.
- **Open concern-first, never cinematic.** Lead with the customer's mission problem or the evaluator's question — the concern itself. Do not stage a dramatized scene ("Picture the demonstration room...", "In August, four personas will..."). Cinematic openings read as cheesy and undercut the impression that the offeror truly understands the mission. The human element belongs in visible command of the problem and plain, engaged language — not in theatrics.

## Section-Level Editing Rules

### Executive Summary

The executive summary should not sound like a company overview. It should answer: why this, why now, why this team, and what the Government can do next.

- Lead with the customer problem or operational opportunity.
- Introduce the company only after the need is clear.
- Keep proof points selective and concrete.
- Avoid architecture detail unless it is the main discriminator.
- Close with a clear path forward.

### Technical Approach

The technical approach must be scorable. It should explain what will be delivered, how it works, how risk is reduced, and where proof exists.

- Use the customer's terminology from the solicitation.
- Explain architecture in operational terms before implementation detail.
- Make commitments explicit: "[Company] will..."
- Avoid deep implementation detail unless it answers an evaluation criterion.
- Use graphics as evidence, not decoration.

### Management Approach

The management approach should reduce execution risk, not recite generic agile/process language.

- Tie governance to risk control, schedule control, quality, and customer visibility.
- Avoid generic Scrum/SAFe boilerplate unless required.
- State decision rights, cadence, escalation paths, and deliverables.

### Past Performance / Team Credibility

This section must prove relevance, not merely list experience.

- State customer, scope, similarity, outcome, and relevance.
- Avoid "experience in" without saying what was delivered.
- Connect each reference to the evaluation criteria.

### White Papers / CSO / OTA Responses

These should read more like a crisp technical business case than a FAR volume.

- Fewer formal pattern markers.
- More direct problem-solution-value flow.
- Stronger emphasis on pilot path, transition, and decision ask.
- Avoid dense compliance language unless the instructions require it.

## Before / After Examples

### Example 1 — Marketing to Credible

Before:
> Our innovative platform leverages next-generation AI to deliver robust operational capabilities across the tactical edge.

After:
> The platform runs mission-tailored AI models locally on approved edge hardware, allowing users to continue core workflows when cloud access is unavailable or unreliable.

### Example 2 — Overbuilt to Natural

Before:
> Through a comprehensive and scalable architecture, [Company] will enable the Government to operationalize AI-enabled decision advantage across distributed mission environments.

After:
> [Company] will give distributed mission teams a local AI capability that supports decision-making without depending on continuous enterprise connectivity.

### Example 3 — Process Theater to Evaluator Value

Before:
> Our team will apply agile best practices, DevSecOps principles, and mature governance processes to ensure successful execution.

After:
> [Company] will manage delivery through two-week increments, Government-visible backlog reviews, and acceptance criteria tied to each required capability. This gives the Government early visibility into progress and a clear mechanism to redirect work before schedule risk accumulates.

### Example 4 — Unsupported Claim to Defensible Claim

Before:
> [Company] is the leading provider of disconnected AI for the Department of Defense.

After:
> [Company] has deployed disconnected AI capabilities in multiple DoD environments and will apply those operational lessons to reduce integration and fielding risk for this effort. <!-- evidence: CLAIM-UNSUPPORTED if no ledger item supports the deployment claim -->

## Editorial Tests

Before saving edited prose, ask:

1. Would a skeptical evaluator know what we are actually proposing?
2. Is the customer problem visible before the company capability?
3. Are claims backed by evidence or softened appropriately?
4. Could this sentence appear in a competitor proposal unchanged? If yes, make it more specific or cut it.
5. Is the prose easier to score after the edit?
6. Did the edit preserve requirement coverage and evidence markers?

## Final Standard

The edited draft should feel like it was written by a competent human who knows the mission and wants to win without sounding desperate. The prose should be plain enough to skim, technical enough to trust, and disciplined enough to survive red team review.
