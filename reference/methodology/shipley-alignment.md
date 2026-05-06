# Shipley Alignment

Cross-walk between the Shipley Proposal Guide (industry-standard reference) and this framework. Documents alignments, divergences, and gaps. Updated when new Shipley material is reviewed or when framework files are refined based on Shipley calibration.

**Source basis:** Shipley Proposal Guide §various chapters (2001/2006 ed.), reviewed 2026-04-25. Source content is **not** reproduced in any framework file; this doc captures methodology and discipline patterns abstracted into the framework's own language.

---

## Summary

| Area | Alignment | Notes |
|---|---|---|
| Capture planning methodology | 🟡 Partial | Shipley methodology documented in `methodology/capture-planning.md`; framework skills cover fragments but no consolidated `/capture-plan` skill yet |
| Color team review model | 🔴 Refined | Framework's historical Pink/Red/Gold/White Glove diverged from Shipley's 6-team model. Resolved: framework now supports Shipley-canonical naming with backward-compat aliases. See `methodology/color-teams.md` |
| Theme statements (Pattern 1) | 🟢 Strong | Framework Pattern 1 aligns with Shipley's theme-statement discipline. Refined with Shipley's "section-theme vs. section-summary" distinction |
| Discriminators (Pattern 2) | 🟢 Strong | Framework Pattern 2 aligns; refined by adding Shipley's Features→Advantages→Benefits (FAB) hierarchy as a deeper structure |
| Action captions (Pattern 3) | 🟢 Strong | Framework Pattern 3 directly matches Shipley's 8-point action-caption discipline |
| Ghosting (Pattern 4) | 🟢 Strong | Framework Pattern 4 aligns; informed by Shipley's customer-language adoption discipline |
| Compliance and Responsiveness | 🟡 Partial | Framework's `compliance-check` covers compliance; "responsiveness" (does the proposal speak to customer issues?) is implicit in Pink Team but not explicit |
| Customer Focus | 🟢 Strong | Framework's `evaluator_framing` field on each proposal type captures this; reinforced by Shipley discipline |
| BD process model | 🟡 New | Shipley's 6-phase + 5-decision-point process documented in `methodology/bd-process.md`; framework skills cover most of the lifecycle but with gaps (no `/capture-plan`, no `/post-submit`) |
| Bid decisions | 🟡 Partial | Framework's `opportunity-quick-look` + `capture-scorecard` cover Interest + Pursuit decisions; Preliminary Bid + Final Bid + Submit decisions don't have explicit framework artifacts |
| Storyboards and mock-ups | 🔴 Gap | Framework has no storyboard skill or pattern. Pink Team in Shipley reviews storyboards before drafting — framework currently runs Pink on completed drafts. Resolved partially: new `--mode=storyboard-pink` added; full storyboard methodology documented but not skill-supported |
| Price to Win | 🔴 Gap | Framework's `pricing-analyst` covers vehicle-specific pricing artifacts; "price to win" analysis (predicting competitor pricing + setting price posture) is not currently covered |
| BD-CMM (BD Capability Maturity Model) | ⚪ Out of scope | The 5-level CMM-style maturity model for BD organizations. Useful as reference; not a framework feature |

Legend: 🟢 strong alignment · 🟡 partial / refined · 🔴 divergence resolved or gap · ⚪ deliberately out of scope

---

## Detailed alignments

### Theme Statements (Pattern 1)

**Shipley discipline (9 points):**
1. Use a logical process to brainstorm theme statements
2. Use theme statements consistently
3. Link benefits to features, trying to state benefits first
4. Quantify benefits if possible
5. Draft concise theme statements, preferably in a single complete sentence
6. Differentiate section theme statements and section summaries
7. Ensure benefits go beyond advantages
8. Tailor theme structure and approach to the evaluation process
9. Use the **Theme Litmus Test** to enhance theme impact

**Framework alignment:**
- `proposal-writing-patterns.md` Pattern 1 (Theme Statements) covers points 1-5 directly
- Point 6 (section-theme vs. section-summary) — refined: framework now distinguishes between an opening **theme statement** (1 sentence asserting the section's main point) and an optional closing **section summary** (recapitulates the section's key takeaways for the evaluator)
- Point 7 (benefits beyond advantages) — addressed via the FAB hierarchy (see Discriminators below)
- Point 8 (tailor to evaluation process) — already in framework via `evaluator_framing` field
- Point 9 (Theme Litmus Test) — adopted; see new section below

#### Theme Litmus Test (added to framework)

A theme statement passes the litmus test if it satisfies **all** of:

1. **Single sentence** — if it requires two sentences, it isn't a theme; it's a paragraph
2. **Specific** — names a particular capability, benefit, or proof point
3. **Quantified** — includes a number, scale, or measurable outcome where possible
4. **Tied to a customer issue** — addresses something the customer cares about, not something we want to talk about
5. **Discriminator-bearing** — implies (or states) something only we offer, not a generic strength
6. **Evaluator-actionable** — gives the evaluator a reason to score the section higher

Theme statements that fail any of these are weak. Strengthen or replace.

This is now part of `proposal-writing-patterns.md` Pattern 1.

---

### Discriminators + Features-Advantages-Benefits (Pattern 2)

**Shipley FAB hierarchy:**
- **Features** — separate aspects of the seller's product/service (speed, schedule, capacity, certification, weight, color, etc.)
- **Advantages** — how, in the seller's opinion, the feature helps the prospect
- **Benefits** — how the feature/advantage actually solves a problem the prospect has acknowledged

Example progression (Shipley-canonical):
- Feature: "The controller has 400MB of memory."
- Advantage: "The controller's 400MB of memory allows you to store more instructions than your current model."
- Benefit: "With 400MB of memory you can run the entire <customer's specific workflow> without interruption, eliminating the rebooting delays your operators reported in the prior system."

**Why this matters for our Pattern 2:**

Framework Pattern 2 (Discriminator Proof Points) currently emphasizes:
- Claim
- Evidence
- Relevance
- Scope

This works but is **shallower than Shipley's FAB hierarchy.** Strong proof points should escalate from feature → advantage → benefit. The benefit is what wins; features and advantages alone don't.

**Refinement applied to `proposal-writing-patterns.md` Pattern 2:** added FAB hierarchy as the structure for proof-point statements. The discriminator's evidence should naturally articulate as feature → advantage → benefit, not just as a flat claim.

---

### Action Captions (Pattern 3)

**Shipley discipline (8 points):**
1. Use interpretive action captions with every graphic
2. Three parts: figure number, title, caption
3. Informative titles, not "horse" titles (ambiguous labels)
4. Connect customer benefit to feature depicted
5. Quantify benefit if possible
6. Place captions BELOW the graphic
7. Reference all graphics by figure number in preceding text
8. Different typeface/style for figure title, caption, and body text

**Framework alignment:** all 8 points already covered in `proposal-writing-patterns.md` Pattern 3 + `graphic-templates/illustrator-conventions.md` §"Action Captions". Strong direct alignment.

**Minor refinement:** point 8 (typographic differentiation between title, caption, and body) was implicit in framework conventions but is now explicit in `illustrator-conventions.md` §5 (Caption convention).

---

### Customer Focus

**Shipley emphasis:** every page should be evaluated from the customer's perspective. Common failure: bidder-focused proposals that read as marketing-of-self rather than addressing customer issues.

**Framework alignment:** the `evaluator_framing` field in every proposal-type registry file captures this idea explicitly. Each type carries a one-line mental model the writer adopts (e.g., FAR RFP: "GS-13/14 evaluator with a Section M score sheet — every requirement must be findable in <30 seconds"; SBIR: "feasibility-study review — technical merit and commercialization potential, not a full research program").

**Strong alignment, no refinement needed.**

---

### Compliance and Responsiveness

**Shipley distinction:**
- **Compliance** = does the proposal address every requirement?
- **Responsiveness** = does the proposal address requirements **as the customer wants them addressed**?

A proposal can be 100% compliant but unresponsive. Example: customer wants "innovative approach to data integration" → bidder writes a perfectly-organized response that lists every data-integration tool but doesn't articulate innovation. Compliant. Unresponsive.

**Framework alignment:**
- Compliance is fully handled by `/compliance-check` skill + `working/compliance-matrix.json`
- Responsiveness is **implicit** in Pink Team review but not explicitly named
- **Refinement:** added an explicit "responsiveness check" to the Pink Team checklist in `red-team-review/SKILL.md`. For each requirement, ask: "is this addressed in the way the customer would want it addressed, not just in the way we wanted to write it?"

---

## Documented divergences (now resolved)

### Divergence 1: Color team naming and timing

**See `methodology/color-teams.md` §"Framework alignment with Shipley naming"** for the full divergence analysis.

**Resolution applied to `red-team-review/SKILL.md`:** added new modes (`--mode=blue`, `--mode=black-hat`, `--mode=storyboard-pink`, `--mode=mock-eval`, `--mode=lessons-learned`); restructured the Gold mode to be Shipley-canonical (executive profit/risk sign-off); preserved backward compatibility via aliases.

### Divergence 2: Pink Team timing

Framework's historical Pink ran on drafts; Shipley's Pink runs on storyboards/mock-ups before drafting. Resolved by adding `--mode=storyboard-pink` for the Shipley-canonical timing and retiring the draft-Pink mode in May 2026 — compliance coverage on completed drafts is now solely owned by `/compliance-check`.

### Divergence 3: Gold Team scope

Framework's historical Gold = rubric mock evaluation. Shipley's Gold = executive profit/risk sign-off. Resolved by:
- `--mode=red` now includes mock evaluation (Shipley-canonical)
- `--mode=mock-eval` preserves the historical rubric-only behavior as an alias
- `--mode=gold` is repositioned as executive risk/profit review (Shipley-canonical)

---

## Identified gaps (not yet resolved)

These are items where Shipley emphasizes something the framework doesn't currently cover. Each is a candidate for future enhancement.

### Gap 1: Storyboarding methodology

**Shipley discipline:** storyboards are produced and Pink-Team-reviewed BEFORE prose drafting begins. Each major section gets a single storyboard; mock-ups have a 1:1 page-level relationship.

**Framework status:** no storyboard skill or template. Pink Team historically runs on drafts.

**Recommended future enhancement:** new `/storyboard` skill that produces section-level storyboard briefs from `working/proposal-plan.md` + `working/compliance-matrix.md`. Storyboards become the input to a Shipley-canonical Pink Team review (`--mode=storyboard-pink`).

For now: methodology documented in `methodology/color-teams.md`; manual storyboarding using the Shipley pattern is supported.

### Gap 2: Price to Win

**Shipley discipline:** structured analysis of likely competitor pricing + customer budget constraints + win-rate-vs-margin tradeoff. Produces a "price to win" target the offeror prices against.

**Framework status:** `/pricing-analyst` produces vehicle-specific pricing artifacts (ROM, SBIR budget, FAR cost volume, etc.) but does NOT include price-to-win analysis. The framework's pricing focus is "what to deliver" not "what number wins."

**Recommended future enhancement:** new `/price-to-win` skill that produces a competitive pricing analysis output. Inputs: `working/competitor-assessment.md`, customer budget intelligence, prior-similar-procurement data. Output: a recommended pricing posture (price floor, target, ceiling) with rationale.

### Gap 3: Capture plan consolidation

**Shipley discipline:** capture planning culminates in a consolidated **capture plan document** with Integrated Solution Worksheet, Bidder Comparison Matrix, win strategy, action list, and decision artifacts.

**Framework status:** capture artifacts are fragmented across `/customer-intel` (customer profile), `/competitor-assessment` (competitor analysis), `/capture-scorecard` (9-dimension stoplight), `/opportunity-quick-look` (initial qualification). No consolidated capture plan.

**Recommended future enhancement:** new `/capture-plan` skill that consolidates the above into a single `working/capture-plan.md` artifact following the structure in `methodology/capture-planning.md`. Becomes the input to Blue Team and Black Hat Team reviews.

### Gap 4: Post-submit lifecycle

**Shipley discipline:** post-submit is its own phase with structured activities (customer Q&A, oral presentations, BAFO, debrief request, lessons learned integration).

**Framework status:** no post-submit skill or coverage. `/red-team-review --mode=lessons-learned` provides a hook but the broader post-submit activities aren't supported.

**Recommended future enhancement:** new `/post-submit` skill that manages the post-submission lifecycle through award (or non-award).

---

## Methodology that is deliberately out of scope

Shipley covers some material this framework deliberately does not address:

- **BD-CMM** (Business Development Capability Maturity Model) — useful as a reference for organizational BD maturity assessment, but not a proposal-writing tool. Could become a reference doc but not a skill.
- **Daily Team Management** — proposal-team operational logistics. Useful for proposal managers but not what AI-augmented drafting is for.
- **International Proposals** — out of scope; framework focuses on US federal.
- **Grant Writing** — different rules and conventions; would warrant its own framework branch.
- **Cliches / Gobbledygook / Jargon / Redundant Words** — generic English-writing guidance; covered implicitly by the `proposal-writer` skill's tone discipline + style-guide.md.

---

## Calibration changelog

| Date | Source | Chapters reviewed | Framework changes |
|---|---|---|---|
| 2026-04-25 | Shipley Proposal Guide (2001/2006 ed.) | BD-CMM, Capture Planning, Process, Reviews, Theme Statements, Action Captions, Storyboards and Mock-ups, FAB | Created `methodology/` library (4 docs); refined `red-team-review/SKILL.md` with Shipley-canonical color-team modes; refined `proposal-writing-patterns.md` Pattern 1 (Theme Litmus Test) and Pattern 2 (FAB hierarchy); added compliance + responsiveness distinction to red-team Pink Team checklist; identified 4 framework gaps for future enhancement |
