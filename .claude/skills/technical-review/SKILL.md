---
name: technical-review
description: Use this skill in two phases — `--phase=approach` BEFORE writing (validates architecture/storyboard feasibility) and `--phase=drafts` AFTER writing (validates claim truthfulness, integration realism, ATO/cyber realism). Catches technical risk where it's cheapest to fix.
---

# Technical Review Skill

## Two-Phase Operation (mandatory dispatch)

This skill runs at two distinct points in the workflow. **The phase determines inputs, scope, and output filename.** If no phase is given, ask the user before proceeding.

| Mode | Position in workflow | Scope | Output |
|---|---|---|---|
| `--phase=approach` | After `/proposal-storyboard`, BEFORE `/proposal-writer` | Validate architectural feasibility, integration realism, schedule/staffing realism, ATO plausibility, hidden assumptions — *before tokens are spent on prose for a flawed approach* | `reviews/technical-review-approach.md` |
| `--phase=drafts` | After `/proposal-writer` and `/proposal-editor`, before `/red-team-review` | Validate claim truthfulness, technical-depth calibration, prose-level architecture consistency, hidden contradictions introduced during drafting | `reviews/technical-review-drafts.md` |

**Critical rule:** `--phase=approach` does NOT read `drafts/`. Drafts don't exist yet at that workflow position. Reading them invalidates the gate's purpose (the gate exists to prevent flawed approaches from becoming flawed prose).

`--phase=drafts` re-reads architecture and storyboard inputs because draft prose can introduce inconsistencies with the approved architecture (over-specified components, undefined interfaces, magical integrations) that need cross-checking.

## Purpose

Perform an engineering and solution-integrity review of the proposal.

This skill is intentionally separate from:
- compliance review
- editorial review
- proposal scoring
- Shipley color-team review

The technical-review skill behaves like a skeptical chief engineer, solution architect, integrator, or program CTO reviewing the proposal for:

- technical accuracy
- architectural consistency
- feasibility
- integration realism
- deployment realism
- operational credibility
- ATO/security plausibility
- truthfulness of technical claims
- hidden execution risk

The goal is not to make the proposal prettier.

The goal is to ensure the proposal would survive contact with:
- customer engineers
- technical evaluators
- operational users
- program offices
- integration teams
- cybersecurity reviewers
- test events
- real deployment conditions

## When to Use

Run twice:
1. **Approach phase** — after `/proposal-storyboard`, before `/proposal-writer`. Catches feasibility issues at the cheapest possible point.
2. **Drafts phase** — after `/proposal-editor`, before `/red-team-review`. Catches claim-truthfulness issues introduced during prose generation.

Recommended workflow:

```
/proposal-solution-architect
/past-performance
/proposal-storyboard
/technical-review --phase=approach     ← gate before writing
/proposal-graphics
/proposal-writer
/proposal-editor
/technical-review --phase=drafts       ← gate before red team
/compliance-check
/red-team-review --mode=red
/red-team-review --mode=gold
```

## Inputs

### `--phase=approach` (pre-write feasibility gate)

Read in this order:

1. `working/proposal-type.md`
2. `working/proposal-plan.md`
3. `working/requirement-matrix.md`
4. `working/capability-matrix.md`
5. `working/solution-strategy.md`
6. `working/architecture-concept.md`
7. `working/assumptions-and-risks.md`
8. `working/storyboard.md` (mandatory at this phase — if absent, exit and recommend running `/proposal-storyboard` first)
9. `working/capture-intent.md` if present
10. `working/competitor-assessment.md` if present
11. `working/compliance-matrix.md` if present
12. `my-company/evidence-ledger.json` if present

Do NOT read `drafts/` at this phase. They don't exist yet.

### `--phase=drafts` (post-write claim-truthfulness review)

Read in this order:

1. All approach-phase inputs (1-12 above)
2. `working/graphics-brief.md` if present
3. All files in `drafts/`
4. All files in `drafts/edited/` if present
5. `reviews/editorial-changes.md` if present
6. `reviews/technical-review-approach.md` (the prior approach-phase report — flag any approach-phase findings that should have been addressed but weren't)

## Review Philosophy

Assume the evaluator is technically competent and skeptical.

The technical-review skill should actively search for:
- hidden assumptions
- architecture inconsistencies
- hand-waving
- impossible timelines
- magical integrations
- unsupported scaling claims
- unrealistic staffing assumptions
- ambiguous deployment paths
- vague cybersecurity language
- claims that sound plausible but fail under scrutiny

This skill should behave like someone trying to break the proposal before the Government does.

## Output Files

**Phase-specific output filename:**

| Phase | Output |
|---|---|
| `--phase=approach` | `reviews/technical-review-approach.md` |
| `--phase=drafts` | `reviews/technical-review-drafts.md` |

Optional supplementary output for either phase:

```
reviews/technical-risks.md
reviews/architecture-conflicts.md
```

The drafts-phase review should explicitly cite the approach-phase report and flag any pre-write findings that became prose-level issues. Approach-phase issues that the writer ignored are higher severity than first-time-found drafts-phase issues.

## Core Review Areas

---

# 1. Architecture Integrity

## Goal

Determine whether the proposed architecture is internally consistent and technically plausible.

## Review Questions

- Does the architecture actually support the operational claims?
- Are components/interfaces clearly defined?
- Does data flow make sense?
- Are dependencies acknowledged?
- Are disconnected/DDIL claims technically plausible?
- Are latency assumptions believable?
- Is edge compute capacity realistic?
- Are cloud/local responsibilities clearly separated?
- Are synchronization assumptions realistic?
- Are external dependencies hidden?
- Is the runtime model deployment path believable?

## Flag Examples

| Issue | Why It Matters |
|---|---|
| "Local inference" but architecture still depends on enterprise APIs | Contradiction |
| Claimed disconnected operation with hidden cloud dependencies | Operational failure risk |
| Unrealistic GPU/memory assumptions | Deployment infeasible |
| Ambiguous data authority model | Integration and governance risk |
| Undefined interface boundaries | Integration ambiguity |

---

# 2. Integration Realism

## Goal

Determine whether the proposed integration approach is operationally believable.

## Review Questions

- Does the proposal assume unrealistic customer access?
- Are existing systems actually reachable?
- Are interfaces known or speculative?
- Is cross-domain movement realistic?
- Does the proposal underestimate integration effort?
- Are external vendor dependencies acknowledged?
- Is data normalization/governance ignored?
- Does the proposal assume API access that may not exist?
- Is deployment inside customer infrastructure plausible?

## Flag Examples

| Issue | Why It Matters |
|---|---|
| "Integrates with existing systems" without naming mechanism | Hand-waving |
| Assumes enterprise connectivity in tactical context | Mission mismatch |
| Assumes direct access to classified systems | Unrealistic deployment assumption |
| CDS integration described vaguely | High execution risk |

---

# 3. Operational Credibility

## Goal

Determine whether the proposal sounds like it understands real operational conditions.

## Review Questions

- Does the proposal acknowledge operational constraints?
- Does it account for degraded connectivity?
- Does it acknowledge user burden/training burden?
- Does it assume perfect data availability?
- Does it understand deployment realities?
- Does it acknowledge sustainment burden?
- Does the workflow fit operational tempo?
- Is the operator experience realistic?
- Does the proposal overestimate automation reliability?

## Flag Examples

| Issue | Why It Matters |
|---|---|
| Assumes analysts will manually curate large datasets | Unrealistic workflow |
| Assumes continuous synchronization | Operational mismatch |
| Overstates autonomous behavior | Trust and control risk |
| Ignores sustainment/training burden | Lifecycle credibility issue |

---

# 4. Security / ATO / Cyber Realism

## Goal

Ensure cybersecurity and accreditation language is technically believable.

## Review Questions

- Are IL classifications used correctly?
- Are ATO claims specific and truthful?
- Is reciprocity described accurately?
- Are cross-domain assumptions realistic?
- Is zero-trust/security language concrete?
- Are data-handling boundaries clear?
- Are identity/access assumptions believable?
- Is model update/distribution security addressed?
- Are software supply-chain risks ignored?

## Flag Examples

| Issue | Why It Matters |
|---|---|
| "ATO ready" without explanation | Buzzword compliance theater |
| Implies reciprocity is automatic | Factually incorrect |
| Uses IL5/IL6 terminology loosely | Evaluator credibility hit |
| Cross-domain described vaguely | High-risk architecture gap |

---

# 5. Timeline / Staffing / Execution Realism

## Goal

Determine whether the delivery plan is believable.

## Review Questions

- Is the schedule realistic?
- Are dependencies acknowledged?
- Are staffing assumptions believable?
- Is onboarding time ignored?
- Is Government participation underestimated?
- Are hardware lead times ignored?
- Are test/integration cycles missing?
- Is RMF/ATO time ignored?
- Is transition/sustainment underdeveloped?

## Flag Examples

| Issue | Why It Matters |
|---|---|
| Full deployment in 30 days with no integration assumptions | Unrealistic |
| No Government coordination assumptions | Delivery risk |
| Staffing ramps too aggressively | Resource credibility issue |
| Ignores test event scheduling realities | Program realism gap |

---

# 6. Technical Claim Truthfulness

## Goal

Prevent technical exaggeration and accidental hallucination.

## Review Questions

- Is every major claim supportable?
- Are superiority claims qualified?
- Are benchmarks contextualized?
- Are deployment claims specific?
- Are prototype claims presented as operational deployments?
- Is experimental functionality overstated?
- Is future roadmap described as current capability?
- Are assumptions disguised as facts?

## Claim Categories

Classify major technical claims as:

| Category | Meaning |
|---|---|
| Verified | Supported directly by evidence |
| Reasonable Inference | Likely true but partially inferred |
| Assumption | Depends on external conditions |
| Unsupported | No evidence found |
| High Risk | Likely to trigger evaluator skepticism |
| Prohibited | Should not appear in proposal |

## Required Output Table

| Claim | Classification | Risk | Recommended Action |
|---|---|---|---|

---

# 7. Technical Depth Calibration

## Goal

Ensure technical detail matches the proposal type and audience.

## Review Questions

- Is the proposal too shallow?
- Is the proposal too academic?
- Is implementation detail excessive?
- Is architecture detail insufficient?
- Is the customer likely to understand the terminology used?
- Is the proposal explaining mechanisms the evaluator does not care about?
- Is the proposal hiding important implementation realities?

## Examples

| Problem | Fix |
|---|---|
| Executive summary contains GPU/container detail | Move to technical approach |
| Technical approach reads like marketing copy | Add architecture/process detail |
| White paper reads like FAR boilerplate | Compress and simplify |
| SBIR reads like a product brochure | Add technical hypothesis and feasibility detail |

---

# Technical Review Output Format

Write:

```markdown
# Technical Review — [Proposal Name]

## Overall Technical Credibility Assessment

<2-4 paragraph assessment>

## Technical Risk Summary

| Severity | Count |
|---|---|
| High | X |
| Medium | X |
| Low | X |

---

## Findings

| ID | Severity | Category | Location | Issue | Why It Matters | Recommended Fix |
|---|---|---|---|---|---|---|

---

## Claim Truthfulness Review

| Claim | Classification | Evidence | Risk | Recommended Rewrite |
|---|---|---|---|---|

---

## Architecture Integrity Assessment

<assessment>

---

## Integration Realism Assessment

<assessment>

---

## Operational Credibility Assessment

<assessment>

---

## Security / ATO Assessment

<assessment>

---

## Timeline / Staffing Realism Assessment

<assessment>

---

## Highest-Risk Proposal Areas

1. <risk>
2. <risk>
3. <risk>

---

## Recommended Immediate Rewrites

<copy-paste-ready rewrites>
```

## Severity Standards

| Severity | Meaning |
|---|---|
| High | Likely evaluator concern or technical credibility hit |
| Medium | Real weakness or ambiguity that should be tightened |
| Low | Improvement opportunity or clarity issue |

## Rules

- Be skeptical.
- Be technically grounded.
- Do not assume claims are true simply because they sound plausible.
- Prefer operational realism over marketing optimism.
- Flag hidden assumptions.
- Flag integration hand-waving.
- Flag architecture contradictions.
- Flag vague cybersecurity language.
- Flag magical AI claims.
- Do not rewrite for tone; rewrite for technical truthfulness.

## Anti-Patterns to Catch

- "AI-enabled decision advantage" with no workflow explanation
- disconnected claims with hidden cloud dependency
- undefined data authority model
- unexplained synchronization behavior
- ATO implications stated casually
- CDS language without architecture detail
- "edge AI" with no hardware/runtime explanation
- unrealistic integration timelines
- vague references to autonomous agents
- undefined human-in-the-loop controls
- performance claims without constraints/context
- confusing prototype/demo with operational deployment

## Final Test

Before finalizing, ask:

1. Would a skeptical chief engineer believe this?
2. Would a Government integrator see hidden work?
3. Would the proposed deployment survive real operational conditions?
4. Did the proposal accidentally promise magic?
5. Would this survive a technical interchange meeting?

If not, flag it.

## Activity Trail

Append to `working/activity.md`:

```
## <timestamp> — technical-review [<phase>] — identified <N findings>, <H high-risk>, reviewed architecture/integration/ATO realism → reviews/technical-review-<phase>.md
```

Append to `working/ai-runs.jsonl` (note `phase` in `notes`):

```json
{"schema_version":"ai-run.v1","timestamp":"<timestamp>","skill":"technical-review","proposal_id":"<proposal>","job_type":"technical-review","provider":"anthropic","model":"claude-opus-4-7","input_tokens_estimate":null,"output_tokens_estimate":null,"cost_estimate_usd":null,"notes":"phase=<approach|drafts> — architecture and execution realism review"}
```
