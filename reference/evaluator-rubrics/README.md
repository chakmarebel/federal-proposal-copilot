# Evaluator Rubrics

Reference library of federal source-selection rating definitions, strength/weakness/deficiency taxonomies, and scoring guidance. Used by the Gold Team pass in `red-team-review` to score drafts the way a real source selection board would.

## Why externalize this

Source-selection language is standardized across DoD (DoDI 5000.74, DFARS 215.304-.306) and civilian FAR Part 15.305. Encoding it in reusable reference files — rather than re-explaining it inside each skill — means:

- Scoring is consistent across proposals
- Rating definitions can be updated in one place when policy changes
- Rubrics are auditable (you can point to "this is why you got Acceptable instead of Good")

## Files

| File | Purpose |
|---|---|
| [adjectival-ratings.md](adjectival-ratings.md) | Standard 5-level ratings (Outstanding / Good / Acceptable / Marginal / Unacceptable) with what each means for Technical, Management, and Past Performance factors |
| [strengths-weaknesses-deficiencies.md](strengths-weaknesses-deficiencies.md) | FAR 15.305 definitions of Strength, Significant Strength, Weakness, Significant Weakness, Deficiency, Uncertainty — plus how evaluators write them up |
| [past-performance-ratings.md](past-performance-ratings.md) | CPARS-aligned confidence levels (Substantial Confidence / Satisfactory Confidence / Neutral Confidence / Limited Confidence / No Confidence) |
| [price-evaluation.md](price-evaluation.md) | How price is evaluated (best value tradeoff, LPTA, cost realism) and how Gold Team should assess pricing volume |

## How Gold Team uses these

Given `working/proposal-plan.md` (which contains the eval criteria extracted from Section M) and the drafts in `drafts/`, Gold Team:

1. For each evaluation factor / subfactor, consult [adjectival-ratings.md](adjectival-ratings.md) for the rating thresholds applicable to that factor type (technical vs. management vs. past performance vs. price).
2. Read the relevant draft section(s).
3. Identify Strengths / Significant Strengths / Weaknesses / Significant Weaknesses / Deficiencies per [strengths-weaknesses-deficiencies.md](strengths-weaknesses-deficiencies.md).
4. Assign a rating that would be defensible if the proposal were debriefed.
5. State exactly what would move the rating up one level.

Ratings are opinions, but they must be **evidence-based** — every rating cites specific paragraphs, graphics, or missing content. "It feels like an Acceptable" is not a valid rationale.

## When rubrics don't apply

- **White papers, RFIs, ROMs, Sources Sought:** no formal eval criteria. Gold Team either skips (if `compliance_sources: []` in proposal-type.md) or applies a lightweight "reader response" pass instead. See the Gold Team section of `red-team-review/SKILL.md`.
- **BAAs:** merit-based review, not Section M. Rubric adapts — emphasis on scientific merit, feasibility, and PI credentials rather than the standard Technical/Management/PP structure.
- **OTAs:** no FAR Part 15 scoring. Gold Team applies prototype-value analysis (demonstrable milestone → expected outcome → transition path) instead of adjectival ratings.

## Adding a new rubric

Create a new `.md` file here with the rating definitions, cite the authority (FAR/DFARS/agency source selection guide), and add it to the table above.
