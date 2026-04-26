---
name: red-team-review
description: Use this skill to review proposal drafts like a government evaluator and identify weaknesses, gaps, ambiguity, and redundancy. Reads from drafts/ and writes findings to reviews/.
---

# Red Team Review Skill

## Review Gate Mode

This skill supports the **Shipley-canonical 6-team color review model** (see [`reference/methodology/color-teams.md`](../../../reference/methodology/color-teams.md) for the full methodology). Each mode corresponds to a specific phase in the proposal lifecycle.

At the start of the skill, ask the user which review gate they want to run — or infer from context based on which review files already exist in `reviews/`.

### Color-team modes (Shipley-canonical, full lifecycle)

| Mode | Phase | Focus |
|------|-------|-------|
| `--mode=blue` | Capture (pre-bid) | Validates capture plan + win strategy. Independent senior reviewers (NOT proposal team). Output: strategy refinements, positioning actions |
| `--mode=black-hat` | Capture (pre-bid) | Reviews competitors' likely strategies and solutions; updates own win strategy in response. Reviewers role-play top competitors |
| `--mode=storyboard-pink` | Pre-draft | Reviews storyboards/outlines for compliance + strategy deployment BEFORE prose drafting begins. Catches structural issues before text is written |
| `--mode=pink` (or `--mode=compliance`) | Mid-draft | **Compliance check on completed drafts** — framework's historical Pink. Different timing from Shipley-canonical Pink |
| `--mode=red` | Post-draft | Customer focus + completeness + clarity of strategy + mock evaluation against rubric |
| `--mode=mock-eval` | Post-draft (alias) | Rubric-driven mock evaluation only (backward-compat alias for the framework's historical Gold mode) |
| `--mode=gold` | Pre-submit | **Executive profit/risk sign-off** (Shipley-canonical Gold). NOT a proposal-quality review — that's Red's job |
| `--mode=white-glove` | Pre-submit | Editorial QA, formatting, submission checklist, package readiness |
| `--mode=lessons-learned` | Post-submit | Process and strategy improvement review using customer debrief if available |
| `--mode=full` | Default | Runs the relevant teams in sequence based on workspace state |

### Backward compatibility

The framework's historical mode names continue to work:
- Old "Pink Team" = new `--mode=pink` (compliance check on drafts)
- Old "Gold Team" (mock evaluation) = new `--mode=mock-eval` OR included in `--mode=red`
- Old "White Glove" = new `--mode=white-glove`

The Shipley-canonical names (`blue`, `black-hat`, `storyboard-pink`, `gold` as profit/risk) are the **preferred** names going forward. Historical aliases will continue to work indefinitely.

### When to skip teams

Not every proposal warrants every team:

| Proposal type | Recommended modes |
|---|---|
| FAR full proposal (high-stakes, $50M+) | blue, black-hat, storyboard-pink, pink, red, gold, white-glove, lessons-learned |
| GSA MAS task-order BPA | blue, pink, red, white-glove (black-hat optional; gold optional) |
| SBIR Phase II | pink, red, white-glove (blue/black-hat skipped — merit review) |
| White paper | pink (compliance), white-glove (light) |
| RFI | white-glove only |
| ROM | white-glove only |

If no mode is specified, ask before proceeding.

---

## Pink Team — Compliance Review

**Purpose:** Find every hole before writing quality is assessed. A non-compliant proposal is disqualified before it's evaluated.

**Inputs:** `working/proposal-type.md`, `working/compliance-matrix.md`, `working/proposal-plan.md`, all files in `drafts/`

**Type check:** If `working/proposal-type.md` declares `compliance_sources: []` (white-paper, rfi, rom, sources-sought), skip formal compliance analysis and run only the attachment/formatting checks below.

**Process:**
1. **Run `/compliance-check` first.** It re-reads the matrix and drafts, recomputes the Status column, and writes `reviews/compliance-gaps.md`. Pink Team *starts from that output* — don't duplicate the diffing work here.
2. Read `reviews/compliance-gaps.md` and treat every `Gap` row as a P0 finding.
3. Treat `Partial` and `Planned (with drafts present)` rows as P1 findings.
4. For `Exception` rows, verify the Evidence column contains a rationale; if empty, flag as P1.

**Also check (not in the matrix):**
- Required page limits not exceeded (vs. `page_target` in `proposal-type.md`)
- **Convention compliance** — if `reference/proposal-conventions/<vehicle-id>.md` exists for this proposal type, validate the draft against its calibrated norms. For `full-proposal` (FAR RFP / IDIQ TO / CSO full / BAA), the conventions to check against are in [`reference/proposal-conventions/far-rfp.md`](../../../reference/proposal-conventions/far-rfp.md):
  - Every body-section heading carries a bracketed solicitation reference
  - Heading hierarchy mirrors PWS/SOW where applicable
  - Mean sentence length in body sections is 22-28 words (run `python scripts/extract-pdf-patterns.py` post-export to verify)
  - Customer's framework terminology is used verbatim, consistently
  - Every figure has at least one in-text reference
  - Front-matter ≤ 15% of total page count
  - Five-Commitment opener present at the start of Technical Approach (or equivalent)
  - Section H / General Information present if solicitation requires
- **Graphics convention compliance** — for every body page with figures, validate against [`reference/graphic-templates/illustrator-conventions.md`](../../../reference/graphic-templates/illustrator-conventions.md):
  - Header strip and footer strip identical to other body pages (logo, program ID, sol#, page #, distribution restriction)
  - Each figure carries a two-part action caption (`Figure N: [Title]. [Assertion of what it proves.]`)
  - First in-text reference to figure precedes the figure (no orphan floats)
  - Every graphic matches one of the 7 documented patterns (3-tier band, callout sidebar, N-column tiles, hub-and-spoke, maturity curve, compliance table, process flow) — flag invented patterns
  - No "everything-page" — pages with 3+ heavy elements (callout + figure + table + multi-paragraph new content) are split or simplified
  - Brand palette discipline: one accent color used across all accents; tile-palette colors reserved for N-column tile graphics only
- Required attachments present (resumes, past performance forms, reps & certs as applicable to the type)
- Required formatting (fonts, margins, page numbers, headers/footers)
- Required section titles match solicitation language exactly
- For OTA: milestone-payment schedule present; follow-on production language present
- For SBIR: commercialization plan present; data rights assertions correct
- For CSO: commercial-item justification present
- For FAR RFP: reps & certs addressed

**Write to:** `reviews/pink-team.md` — consolidated Pink findings (referencing, not duplicating, `reviews/compliance-gaps.md`).

**Pink Team is complete when:** Zero P0 findings. All P1 items are either resolved or accepted risks with documented rationale.

**Activity trail:** Append to `working/activity.md`:
```
## <timestamp> — red-team-review [pink] — <P0 count> P0, <P1 count> P1 findings → reviews/pink-team.md
```

---

## Red Team — Narrative Quality Review

**Purpose:** Read like a GS-14 evaluator with 15 minutes and a scoring rubric. Find everything that will cost points.

**Inputs:** All files in `drafts/`, `working/proposal-plan.md` (win themes, evaluation criteria), `working/competitor-assessment.md`

**Review categories:**
1. **Technical credibility** — is the architecture real and defensible?
2. **Differentiation** — why this team over competitors? Is it explicit?
3. **Evaluator clarity** — can every answer be found in under 30 seconds?
4. **Evidence** — every claim backed by proof (past performance, benchmarks, deployed systems)?
5. **Risk reduction** — are risks acknowledged and mitigated explicitly?
6. **Redundancy** — same content in multiple sections?
7. **Win themes** — are the 3-5 win themes woven through every section?
8. **Graphics alignment** — do visuals reinforce the narrative, or just decorate it?

**Output table:**
| Issue | Severity | Section | Why It Hurts Score | Recommended Fix |
|-------|----------|---------|-------------------|-----------------|

**Recommended rewrites:** For the top 3–5 issues, provide the specific rewritten text — copy-paste ready.

**Write to:** `reviews/red-team-notes.md`

---

## Gold Team — Rubric-Based Mock Evaluation

**Purpose:** Simulate the source selection board. Score the proposal against each evaluation factor using federal source-selection rubrics, citing specific Strengths/Weaknesses/Deficiencies with paragraph-level evidence. This is "write to the score sheet" in practice.

**Type check:** If `working/proposal-type.md` declares `compliance_sources: []` (white-paper, rfi, rom, sources-sought), skip formal rubric scoring and run the [Lightweight Reader Response](#lightweight-reader-response) pass below instead.

**Inputs:**
- `working/proposal-type.md` — determines whether formal scoring or lightweight pass applies
- `working/proposal-plan.md` — evaluation factors, subfactors, and weights extracted by `proposal-manager`
- `working/compliance-matrix.md` — current coverage status (informs Technical/Management ratings)
- All files in `drafts/`
- **Reference rubrics (mandatory):**
  - `reference/evaluator-rubrics/adjectival-ratings.md` — Outstanding/Good/Acceptable/Marginal/Unacceptable definitions
  - `reference/evaluator-rubrics/strengths-weaknesses-deficiencies.md` — S/SS/W/SW/D definitions and writing conventions
  - `reference/evaluator-rubrics/past-performance-ratings.md` — if there's a PP factor
  - `reference/evaluator-rubrics/price-evaluation.md` — for the Price/Cost factor

### Process

1. **Load the rubric.** Read the four rubric files above before scoring anything. Gold Team ratings must come from the rubric, not from impression.

2. **For each evaluation factor/subfactor:**
   - Read the factor definition from `working/proposal-plan.md`
   - Determine factor type (Technical / Management / Past Performance / Price) and use the right rubric
   - Read the corresponding draft section(s)
   - Enumerate findings as Strengths, Significant Strengths, Weaknesses, Significant Weaknesses, or Deficiencies per `strengths-weaknesses-deficiencies.md`
   - **Every finding must cite a specific paragraph, table, figure, or the absence thereof.** "Seems weak in X" is not a valid finding — it must be "Section §3.2.1, paragraph 2, states X but does not quantify Y, creating a Weakness."
   - Assign the rating that emerges from the S/W/D pattern (do NOT pre-assign a rating and back-fill)
   - Write the rationale in the voice of a source-selection decision document

3. **Check win theme visibility.** From `working/proposal-plan.md`, pull the win themes defined by `proposal-manager`. For each theme, verify it is:
   - Stated in the executive summary
   - Reinforced in at least 2 major technical sections
   - Supported by at least 1 concrete proof point per section where it appears
   - Not just stated as a claim but connected to a differentiator
   
   Gold Team reports each theme's visibility as: **Strong** (all four) / **Present** (stated and reinforced) / **Weak** (stated but not reinforced) / **Absent**.

4. **Check discriminator proof points.** For each discriminator in `working/proposal-plan.md`, verify there is a concrete proof point in the draft (past contract, demo, technical benchmark, named personnel, certification). Discriminators without proof points are Weaknesses.

5. **Check ghosting.** From `working/competitor-assessment.md`, pull the top competitor's weaknesses. For each, verify the draft subtly frames the solution in a way that highlights that competitor weakness without naming the competitor. Missing ghosting opportunities are noted but not Weaknesses.

5b. **Check evidence citations (Phase C).** If `my-company/evidence-ledger.json` exists, run `/evidence-check` first (or read its most recent output at `reviews/evidence-check.md`). For each finding:
   - **Every `<!-- evidence: CLAIM-UNSUPPORTED -->` marker is an automatic Weakness.** Rationale: the writer explicitly flagged that a claim in the draft has no backing evidence. Severity depends on where the claim appears — in the executive summary or a Section M subfactor response, it's a Significant Weakness; in a minor capability paragraph, an ordinary Weakness.
   - **Every retired or unknown evidence ID is a Weakness** — cited evidence that doesn't exist in the ledger is structurally unsupportable.
   - **Every restricted-context violation is a Significant Weakness** — citing an item the ledger says is not cleared for this proposal type is a compliance / integrity issue.
   - **Unused approved evidence relevant to the proposal** is an *opportunity note* (not a Weakness) — "consider adding EV-031 as a proof point for subfactor X."

   Do NOT re-do the deterministic scan here — consume `/evidence-check`'s output. If `reviews/evidence-check.md` is older than any `drafts/*.md` file, warn the user and recommend re-running `/evidence-check` first.

   If `my-company/evidence-ledger.json` does not exist, skip this step with a note: "Phase C evidence ledger not populated — evidence citation scoring not applied."

6. **Compute overall rating pattern.** Tabulate factor ratings weighted per Section M's statement of importance. Do not invent percentages.

7. **Estimate pWin (rough, not definitive).**
   - All factors Outstanding or Good + competitive price → pWin High
   - Mostly Acceptable with 1-2 Good → pWin Moderate
   - Any Marginal or Unacceptable factor → pWin Low until fixed
   - Any Deficiency → pWin Very Low (unawardable)

### Output: `reviews/gold-team-scorecard.md`

```markdown
# Gold Team Mock Evaluation — [Proposal Name]

**Type:** [type_id from proposal-type.md]
**Date:** [timestamp]
**Evaluator profile:** Mock GS-13/14 source-selection evaluator applying `reference/evaluator-rubrics/`

## Scorecard Summary

| Factor | Importance | Rating | Rationale (1-line) |
|---|---|---|---|
| [Factor 1 name] | [Most Important / etc.] | [Outstanding/Good/Acceptable/Marginal/Unacceptable] | [one line] |
| [Factor 2] | | | |
| [Factor N — Past Performance] | | [Substantial/Satisfactory/Neutral/Limited/No Confidence] | |
| Price | | [assessment, not rating] | |

## pWin Estimate: [High / Moderate / Low / Very Low]

[1-2 paragraphs explaining the estimate based on factor pattern + competitor assessment + price posture]

---

## Factor 1 — [Name]

**Rating:** [Adjectival]
**Source (Section M):** [quote or paraphrase the eval standard]

### Strengths

#### Strength 1: [short label]
- **Basis:** [cite: drafts/technical-approach.md §3.2, paragraph 2]
- **Benefit to Government:** [what the government gets]

#### Significant Strength: [short label]
- **Basis:** [cite]
- **Benefit to Government:** [why this is decisive, not just good]

### Weaknesses

#### Weakness 1: [short label]
- **Basis:** [cite paragraph or its absence]
- **Risk to Government:** [what could go wrong]
- **Fix to resolve:** [specific rewrite or addition]

#### Significant Weakness: [short label]
- **Basis:** [cite]
- **Risk to Government:** [material execution risk]
- **Fix to resolve:** [specific]

### Deficiencies
(None / list with fix-to-resolve for each)

### Rating Rationale
[Paragraph written in the voice of a source-selection decision document. Pattern of S/W/D → rating. Cite the rubric threshold that was met.]

### What Would Move This to [Next Higher Rating]
[Specific, actionable. "Add a Significant Strength in subfactor X by citing the [prior customer] deployment as a proof point."]

---

[Repeat for each factor]

---

## Win Theme Visibility

| Theme | Status | Notes |
|---|---|---|
| [Theme 1 from proposal-plan.md] | Strong/Present/Weak/Absent | [where it's strong, where it's missing] |
| [Theme 2] | | |

## Discriminator Proof-Point Check

| Discriminator | Proof Point Present? | Cite |
|---|---|---|
| [Discriminator 1] | Yes/No | [draft location or "absent"] |

## Ghosting Check (vs. top competitor)

| Competitor Weakness | Ghosted? | Notes |
|---|---|---|
| [Weakness from competitor-assessment.md] | Yes/No/Partial | [where in draft] |

## Prioritized Rewrite List

1. **[Highest impact fix]** — resolves [factor rating → next level or compliance Gap]
2. [Next]
3. [Next]
[List in order of scoring impact, not author convenience]

## Overall Assessment

[2-3 paragraphs. Honest view of whether this wins as drafted. If No, what must change. If Yes, what preserves the win.]
```

### Activity trail

Append to `working/activity.md`:

```
## <timestamp> — red-team-review [gold] — <N factors scored>: <OutstandingCount>O/<GoodCount>G/<AcceptableCount>A/<MarginalCount>M/<UnacceptableCount>U, pWin: <level> → reviews/gold-team-scorecard.md
```

### Lightweight Reader Response

For white papers, RFIs, ROMs, and sources-sought responses — no Section M exists, so formal adjectival scoring doesn't apply. Run this lightweight pass instead:

1. Read the draft.
2. Imagine the intended reader (program officer, market researcher, CO). What's their first reaction?
3. Assess:
   - **Clarity of the "so what"** — is it findable in the first page?
   - **Credibility** — does it read as someone who understands the mission?
   - **Call to action** — is it clear what the reader should do next?
   - **Length discipline** — is it within `page_target` from `proposal-type.md`?
4. Output: `reviews/gold-team-scorecard.md` with the four dimensions, 1-line assessments each, and a prioritized rewrite list. Skip the S/W/D structure — it's not applicable.

### Gold Team discipline

- **Never assign a rating without Strength/Weakness analysis first.** The rating must *emerge* from the findings.
- **Every finding cites a specific location or absence.** No "feels weak" — show me where.
- **Use the rubric language verbatim.** "Appreciably increases" is an FAR term of art; use it, don't paraphrase.
- **Don't stack trivial strengths to imply a Significant Strength.** Evaluators see through this.
- **Don't over-claim.** Gold Team is supposed to be honest, not motivational. If pWin is Low, say so and say why.

---

## White Glove — Final QA

**Purpose:** Catch everything that could embarrass the team or trigger a non-compliance finding on submission day.

**Checklist — run every item:**

**Editorial:**
- [ ] No double spaces after periods
- [ ] Consistent section numbering throughout (e.g., "5." not "5.0")
- [ ] No informal language (check: "Govt", "ours", "we've", contractions in formal sections)
- [ ] All acronyms defined on first use in each major section
- [ ] No run-on sentences; no sentence fragments
- [ ] Consistent verb tense throughout each section

**Formatting:**
- [ ] Page count within limits (by volume if applicable)
- [ ] Font, size, and margin compliance
- [ ] Heading styles applied correctly (not manual bold on Normal paragraphs)
- [ ] Figure captions present and numbered sequentially
- [ ] No floating/anchored images that may shift across systems
- [ ] Header and footer match requirements (document title, company, page numbers)
- [ ] Classification and distribution marking present (if required)
- [ ] Cover page complete with all required elements

**Content completeness:**
- [ ] All required attachments included (resumes, PPQs, certifications, representations and certifications)
- [ ] All cross-references resolve correctly
- [ ] No placeholder text remaining ([TBD], [TO BE PROVIDED], [INSERT])
- [ ] Pricing volume matches technical volume commitments (no orphaned commitments)

**Submission:**
- [ ] File naming convention matches solicitation requirements
- [ ] File format matches solicitation requirements (PDF, DOCX, etc.)
- [ ] Submission portal/method confirmed
- [ ] Submission deadline confirmed with timezone

**Write to:** `reviews/white-glove-checklist.md`

---

## Full Review (Default)
Runs all four passes in sequence. Write findings to all four output files. Present a consolidated summary at the end: total issues by severity, recommendation on whether the proposal is ready to submit.

---

## Output Files (by mode)
- Pink Team → `reviews/pink-team.md` (references `reviews/compliance-gaps.md` from `/compliance-check`)
- Red Team → `reviews/red-team-notes.md`
- Gold Team → `reviews/gold-team-scorecard.md`
- White Glove → `reviews/white-glove-checklist.md`
- Full Review → all four files

**Critical Rule: Always write to files — never just display in chat.**

## Lessons Learned (Calibration Session — White Paper Review)

### Structural Issues to Catch
- **Section duplication is the #1 problem.** Overview sections (e.g., "What is [Your Company]") and detail sections (e.g., "Addressing the Execution Gap") almost always repeat the same capabilities. Flag every instance and recommend which section should own which content.
- **Closing paragraphs that restate the section.** Section 2 closing ("These challenges are interconnected...") should pivot to the solution, not summarize the section. Flag circular closings.
- **Tables already in graphics.** If a capabilities table appears as both a graphic and inline text, flag the duplication and recommend removing one.

### Editorial Issues to Catch
- Double spaces after periods
- Inconsistent section numbering ("5.0" vs "5.")
- Informal language in formal documents ("Govt" → "Government", "ours" → "[Your Company]")
- Run-on sentences — especially when incorporating reviewer feedback (e.g., eval sentence with missing punctuation)
- Grammar breaks when mixing verb forms ("tasks integrating tools, reference local data" — inconsistent tense)
- Manual bold on Normal paragraphs instead of proper Heading styles

### Formatting Issues to Catch
- Missing figure captions/numbering
- Font mismatch between body (Times New Roman) and headers/footers (default Aptos)
- Floating images (anchored positioning) that may shift when document is opened on different systems
- Missing UNCLASSIFIED/distribution marking
- Missing header/footer document identification
- Blank spacer paragraphs instead of proper paragraph spacing

### Tone Issues to Catch
- Data capture framed as mandatory when it should be optional
- Commitments that imply customer obligations
- Hardware-specific claims (e.g., "16GB VRAM") when model selection isn't finalized
- Overpromising on timelines without qualifying assumptions

### Review Delivery Format
Present findings in two parts:
1. **Priority fixes table** — numbered, with severity (High/Medium/Low), location, and effort estimate
2. **Recommended rewrites** — for the top 3-5 issues, provide the specific rewritten text, not just a description of what to fix. The author should be able to copy-paste the fix.
