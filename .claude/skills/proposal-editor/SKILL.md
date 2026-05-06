---
name: proposal-editor
description: Use this skill after proposal-writer to transform compliant draft content into natural, evaluator-friendly, submission-quality prose without breaking compliance or evidence traceability.
---

# Proposal Editor Skill

## Purpose

The proposal-writer creates compliant, technically grounded draft content. The proposal-editor transforms that draft into writing that sounds credible, natural, concise, and submission-ready.

This is an editorial pass — not a rewrite from scratch.

The editor's mission is to:
- preserve compliance
- preserve technical meaning
- preserve evidence
- reduce proposal-template voice
- reduce marketing language
- improve evaluator readability
- tighten narrative flow
- reduce redundancy
- sharpen scoreable takeaways

The editor is intentionally optimized for prose quality, not process generation.

## When to Use

Run after `/proposal-writer` and before `/red-team-review`.

Recommended workflow:

```
/proposal-writer
/proposal-editor
/compliance-check
/red-team-review --mode=red
/red-team-review --mode=gold
```

## Inputs

Read in this order:

1. `working/proposal-type.md`
2. `reference/editorial-voice-guide.md` (mandatory)
3. `working/proposal-plan.md`
4. `working/compliance-matrix.md` (if exists)
5. `working/competitor-assessment.md` (if exists)
6. All files in `drafts/`
7. Relevant proposal conventions file:
   - `reference/proposal-conventions/far-rfp.md`
   - `reference/proposal-conventions/sbir.md`
   - `reference/proposal-conventions/gsa-mas.md`
   - etc.

## Editorial Philosophy

The proposal-editor is not trying to make the proposal sound impressive.

It is trying to:
- make evaluators trust the proposal
- make the proposal easier to score
- make the offeror sound competent and credible
- make the technical narrative easier to follow
- remove AI-generated stiffness and proposal boilerplate

The editor should behave like a senior proposal lead with technical literacy and strong editorial instincts.

## Critical Rules

### Preserve Compliance

Do NOT:
- remove solicitation references
- remove required section coverage
- remove requirement traceability
- remove compliance language required by the solicitation
- remove required headings
- remove evidence markers
- remove proof points unless duplicated or unsupported

If an edit risks reducing compliance coverage, preserve the original structure and tighten locally.

### Preserve Evidence Markers

Evidence comments must survive editing.

Example:

```markdown
Our platform operated in disconnected mode for 14 months. <!-- evidence: EV-022 -->
```

Do not delete or alter evidence IDs.

If prose surrounding an unsupported claim is softened, preserve the unsupported marker:

```markdown
<!-- evidence: CLAIM-UNSUPPORTED -->
```

## Rewrite Priorities

Apply these in order:

1. Preserve compliance
2. Preserve technical accuracy
3. Preserve evidence
4. Improve naturalness
5. Remove marketing language
6. Reduce redundancy
7. Improve evaluator readability
8. Tighten for page count

## What to Edit Aggressively

### 1. Marketing Language

Replace empty adjectives with observable facts.

Bad:
> robust, innovative, transformative, cutting-edge

Good:
> describe what the system does, where it runs, what risk it reduces, or what proof exists

### 2. Proposal Template Voice

Rewrite sections that sound generated from process guidance.

Bad:
> This section describes our technical approach for enabling mission success.

Better:
> The proposed architecture allows users to continue core workflows even when enterprise connectivity is unavailable.

### 3. Overbuilt Sentences

Break long sentences into shorter declarative statements.

### 4. Repetitive Themes

If the same point appears in multiple sections:
- keep the strongest version
- trim the duplicates
- cross-reference if necessary

### 5. Empty Transition Language

Cut phrases like:
- in order to
- the fact that
- at this point in time
- it is important to note
- as previously mentioned

### 6. Unsupported Claims

If a superiority claim lacks evidence:
- soften it
- localize it
- qualify it
- or preserve the unsupported marker

Do not silently convert speculation into confident prose.

## Editing Modes

### Mode 1 — Light Polish

Use when drafts are already structurally strong.

Focus:
- tone
- readability
- redundancy
- sentence flow
- word choice

### Mode 2 — Structural Rewrite

Use when drafts are technically correct but poorly organized.

Allowed actions:
- reorder paragraphs
- move proof points
- merge repetitive sections
- rewrite openings/closings
- rebuild transitions

Do NOT change section numbering or required headings.

### Mode 3 — Executive Compression

Use when page pressure exists.

Focus:
- remove filler
- compress repetitive explanations
- reduce background detail
- preserve discriminators and proof

Goal:
- reduce length without losing scoreable content

## Section-Level Guidance

### Executive Summary

The executive summary should answer:
- what problem exists
- why it matters now
- what the offeror proposes
- why this team is credible
- what the Government should do next

Remove:
- company brochure language
- architecture over-explanation
- generic capability lists

### Technical Approach

Technical sections should:
- lead with operational purpose
- explain architecture in plain terms first
- move into technical depth only where needed
- make evaluator benefits obvious

### Management Approach

Remove generic agile boilerplate unless required.

Focus on:
- execution control
- schedule control
- Government visibility
- escalation
- integration risk reduction

### Past Performance

Every reference should answer:
- what was delivered
- for whom
- under what conditions
- why it is relevant to this evaluation

## Output Rules

Edited files are written to:

```
drafts/edited/
```

Preserve original drafts.

Example:

```
drafts/technical-approach.md
drafts/edited/technical-approach.md
```

## Required Deliverables

### 1. Edited Draft Files

Create edited versions of every modified section.

### 2. Editorial Change Log

Write:

```
reviews/editorial-changes.md
```

Include:

| Section | Major Changes | Why |
|---|---|---|
| technical-approach.md | Reduced marketing language, simplified architecture explanation, merged duplicate DDIL explanation | Improved evaluator readability and reduced redundancy |

### 3. Editorial Findings Summary

At the top of `reviews/editorial-changes.md`, summarize:

- biggest narrative weaknesses found
- most repetitive themes
- most common AI-writing patterns observed
- unsupported claims identified
- sections still requiring human SME review

## Editorial Standards

A successful edit should:

- sound like a competent human wrote it
- remain technically grounded
- remain compliant
- remain evidence-backed
- read faster
- feel calmer and more confident
- reduce "AI smell"

## Anti-Patterns the Editor Must Catch

- every section opening with the same formula
- repetitive theme statements
- excessive use of "will"
- architecture paragraphs with no operational meaning
- paragraphs that only restate the solicitation
- ghosting that feels forced or obvious
- proof points disconnected from evaluation criteria
- proposal-speak replacing technical specificity

## Human Escalation Rules

Flag for human review if:

- a claim appears strategically risky
- a claim may violate truthfulness standards
- architecture detail appears inconsistent
- the solicitation language is ambiguous
- a proof point materially changes meaning after rewrite

Do NOT guess.

## Final Pass

Before saving:

1. Read the edited section aloud internally.
2. Ask: "Does this sound like an experienced capture/proposal lead wrote it?"
3. Ask: "Would a Government evaluator trust this more after the rewrite?"
4. Ask: "Did the rewrite preserve scoreable content?"

If the answer is no, revise again.

## Activity Trail

Append to `working/activity.md`:

```
## <timestamp> — proposal-editor — edited <N sections>, reduced redundancy, tightened narrative flow → drafts/edited/
```

Append to `working/ai-runs.jsonl`:

```json
{"schema_version":"ai-run.v1","timestamp":"<timestamp>","skill":"proposal-editor","proposal_id":"<proposal>","job_type":"editorial-rewrite","provider":"anthropic","model":"claude-opus-4-7","input_tokens_estimate":null,"output_tokens_estimate":null,"cost_estimate_usd":null,"notes":"editorial rewrite pass"}
```
