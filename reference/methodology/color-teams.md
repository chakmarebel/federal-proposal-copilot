# Color Team Review Model

The canonical proposal review model used across the federal contracting industry. Each color team has a specific scope, timing, and audience. This framework names and structures its review skill (`red-team-review`) around this model.

**Source:** Shipley Proposal Guide §Reviews (2001/2006 ed.). The 6-team model is industry standard; specific implementations vary by organization.

---

## The six teams (canonical sequence)

Reviews follow the proposal lifecycle. Earlier teams catch strategic issues; later teams catch tactical and quality issues. Skipping early teams costs more later — most rework results from win-strategy errors that should have been caught at Blue Team.

| Team | Phase | Scope | Audience | Output |
|---|---|---|---|---|
| **Blue Team** | Pre-bid (during capture) | Validates the **capture plan and win strategy** before the bid decision | Independent senior reviewers (NOT the proposal team) | Strategy refinements, positioning actions, gap-fill priorities |
| **Black Hat Team** | Pre-bid (during capture) | Reviews **competitors' likely strategies and solutions**; updates own win strategy in response | Independent reviewers role-playing top competitors | Competitor profile updates; ghosting opportunities; differentiation gaps |
| **Pink Team** | Mid-draft (storyboards / mock-ups, BEFORE writing prose) | Validates **strategy deployment and compliance** at the storyboard / outline stage | Independent reviewers familiar with the bid request | Storyboard corrections; compliance-matrix gaps; theme alignment |
| **Red Team** | Post-draft (full proposal complete) | Evaluates the proposal for **customer focus, completeness, and clarity of strategy** | Independent reviewers, often role-playing evaluators | Specific rewrite recommendations; mock evaluator scoring |
| **Gold Team** | Pre-submit (final approval) | Confirms the offer entails **acceptable profit and risk** | Senior management responsible for offer execution | Authorization to submit (or withhold) |
| **Lessons Learned Review** | Post-submit (after debrief) | Determines how processes, strategies, and people can be improved | Capture + proposal teams + customer debrief if available | Process improvements; capability gaps to address |

---

## Detailed scope per team

### Blue Team

**When:** During capture, before the proposal is drafted. After the capture plan is substantially complete.

**Scope:**
- Capture plan completeness and credibility
- Win strategy validation: does the strategy actually win against expected competitors?
- Customer relationship status: are we positioned where we think we are?
- Solution-vs-requirements fit
- Pricing approach and price-to-win posture

**Composition:** Senior reviewers independent of the proposal team — typically business development leadership, technical experts not on the bid team, sales seniors.

**Output:** Strategy refinements, positioning-action priorities, gap-fill recommendations. Often results in capture-plan updates.

### Black Hat Team

**When:** During capture, often paired with or following Blue Team.

**Scope:**
- Competitive analysis: who are the likely bidders, what are their strategies?
- Competitor strengths and weaknesses
- Likely competitor pricing and discount postures
- Ghosting opportunities (where can we frame our solution to highlight a competitor's weakness without naming them?)

**Composition:** Reviewers who role-play each top competitor. Each Black Hat member is responsible for one competitor's perspective and argues from inside that competitor's mindset.

**Output:** Competitor profile updates; ghosting strategy; differentiation gaps to close; strategic adjustments to win strategy.

### Pink Team

**When:** Mid-draft — after storyboards and mock-ups are complete but BEFORE prose drafting begins. This is critical: **Pink Team reviews structure, not text**.

**Scope:**
- Compliance: does the planned structure address every requirement from Section L/M (or equivalent)?
- Strategy deployment: are win themes and discriminators present at the right places in the planned structure?
- Theme integration: are storyboard concepts coherent across sections?
- Section-level outline quality: is each section's planned content complete?

**Composition:** Independent reviewers (or team members reviewing portions they did not author). Must understand the bid request thoroughly, the win strategy, and how to read storyboards/outlines.

**Output:** Storyboard corrections; outline restructuring; compliance-matrix gaps to close; theme placement adjustments.

**Key discipline:** prose drafting does NOT begin until Pink Team findings are dispositioned. Drafting against an unverified outline is the most common source of rework.

### Red Team

**When:** Post-draft — after the proposal is substantively complete (all sections drafted, graphics in place, compliance matrix populated).

**Scope:**
- Customer focus: does the proposal read from the customer's perspective?
- Completeness: every requirement addressed?
- Strategy and discriminator clarity: do win themes land?
- Solution clarity: can an evaluator extract the offered approach in 30 seconds per section?
- Mock evaluation: scored against the published evaluation criteria as if Red Team were the source-selection board

**Composition:** Independent reviewers role-playing evaluators. Should include domain experts and writing experts.

**Output:** Specific rewrite recommendations per section; mock evaluator scoring against the actual evaluation rubric; assessment of likely competitive position.

### Gold Team

**When:** Pre-submit — after Red Team findings have been incorporated. Last review before submission.

**Scope:**
- Profitability and risk: does the proposed offer entail acceptable profit margin and execution risk?
- Liability exposure: are commitments made in the proposal within the company's ability to deliver?
- Strategic fit: does winning this contract advance corporate strategy?
- Pricing posture: final price-to-win check

**Composition:** Senior management responsible for offer execution — typically C-suite, business unit leadership, finance, contracts.

**Output:** Authorization to submit. Or: a no-bid decision at the last minute (rare but real — if the offer terms have drifted into unacceptable risk territory during proposal development, Gold Team can withdraw).

**Critical clarification:** Gold Team is NOT a proposal-quality review. That is Red Team's job. Gold Team is an **executive risk/profit sign-off** on the offer the proposal makes.

### Lessons Learned Review

**When:** Post-submit, ideally after the customer debrief (whether win or loss).

**Scope:**
- Strategic accuracy: was the win strategy correct?
- Market intelligence quality: did our competitor and customer intelligence prove accurate?
- Process effectiveness: did the proposal process work?
- Team effectiveness: how did the team work together?
- Capture-to-proposal handoff quality
- Specific gaps to close before the next bid

**Composition:** Capture team + proposal team. If possible, integrate the customer's debrief findings.

**Output:** Process improvements; capability gaps to address; updates to standing capture and proposal templates; personnel development recommendations.

---

## Framework alignment with Shipley naming

This framework's `red-team-review` skill historically used a 4-mode model (Pink → Red → Gold → White Glove) that diverged from Shipley's canonical 6-team model in three ways:

### Divergence 1: Pink Team timing

**Shipley:** Pink reviews storyboards/mock-ups BEFORE drafting begins. Catches structural issues before prose is written.

**Framework (historical):** Pink reviews drafts AFTER drafting is complete. Compliance-focused.

**Resolution:** The framework's draft-Pink mode (`--mode=pink`) was retired in May 2026. Compliance coverage on completed drafts is now solely the responsibility of `/compliance-check`, which already does the same matrix-vs-drafts diff. The Shipley-canonical pre-draft Pink remains available as `--mode=storyboard-pink`.

### Divergence 2: Gold Team scope

**Shipley:** Gold = executive profit/risk sign-off. NOT a proposal-quality review.

**Framework (historical):** Gold = rubric-driven mock evaluation. A proposal-quality review.

**Resolution:** The framework's `red-team-review --mode=gold` is more accurately described as **"Mock Evaluation"** — what Shipley calls part of Red Team. We've split this:
- `--mode=red` now includes mock evaluation against the rubric (Shipley-canonical Red)
- A new `--mode=gold` provides the executive profit/risk sign-off (Shipley-canonical Gold)

For backward compatibility, the historical Gold-mode behavior is preserved under `--mode=mock-eval` (callable explicitly) and remains the default behavior of `--mode=red` enhanced.

### Divergence 3: Missing teams

**Shipley:** Blue Team and Black Hat Team run during capture, before bid decision.

**Framework (historical):** No equivalent. The `capture-scorecard` skill captures some of the bid-decision content but doesn't structure the Blue/Black Hat reviews.

**Resolution:** Two new `red-team-review` modes added:
- `--mode=blue` — capture plan + win strategy review
- `--mode=black-hat` — competitor strategy review (consumes `working/competitor-assessment.md`)

These run in the capture phase, before the bid decision. They are independent of the proposal-drafting modes.

---

## Updated `red-team-review` mode catalog

| Mode | Phase | What it does | Inputs |
|---|---|---|---|
| `--mode=blue` | Capture | Validates capture plan + win strategy | `working/capture-scorecard.md`, `working/competitor-assessment.md`, `working/customer-profile.md` |
| `--mode=black-hat` | Capture | Reviews competitor strategies; identifies ghosting + differentiation gaps | `working/competitor-assessment.md` |
| `--mode=storyboard-pink` | Pre-draft | Reviews storyboards/outlines for compliance + strategy deployment | `working/storyboards/`, `working/compliance-matrix.md`, `working/proposal-plan.md` |
| `/compliance-check` (separate skill) | Mid-draft | Compliance coverage on completed drafts (replaces retired `--mode=pink`) | `drafts/`, `working/compliance-matrix.md` |
| `--mode=red` | Post-draft | Customer focus + completeness + mock evaluation | `drafts/`, `working/proposal-plan.md`, `reference/evaluator-rubrics/` |
| `--mode=mock-eval` | Post-draft (alias) | Rubric-driven mock evaluation only (backward-compat alias) | Same as red |
| `--mode=gold` | Pre-submit | Executive profit/risk sign-off | `drafts/`, `working/pricing-inputs.md`, `working/risk-register.md` |
| `--mode=white-glove` | Pre-submit | Final QA, formatting, package readiness | `final/` package |
| `--mode=lessons-learned` | Post-submit | Process improvement review | All workspace + customer debrief if available |

Default `--mode=full` runs the relevant teams in sequence based on workspace state.

---

## When to skip teams

Not every proposal warrants every team:

| Proposal type | Recommended teams |
|---|---|
| FAR full proposal (high-stakes, $50M+) | All 6 |
| GSA MAS task-order BPA | Blue + Pink + Red + White Glove (Black Hat optional, Gold optional) |
| SBIR Phase II | Pink + Red + White Glove (Blue/Black Hat usually skipped — merit review) |
| White paper | Pink + White Glove (light) |
| RFI | White Glove only |
| ROM | White Glove only |

Use the proposal-type registry's `required_skills` list as the starting point; add color-team modes as appropriate to the bid stakes.
