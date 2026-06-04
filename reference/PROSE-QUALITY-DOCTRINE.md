# Federal Proposal Prose-Quality Doctrine

Universal across proposal-workbench, federal-proposal-assistant, and federal-proposal-copilot.

## What this doctrine governs

This doctrine governs how AI produces prose for federal proposals.

It covers:

- the reframe -> polish sequence;
- ventriloquism as a failure mode;
- voice anchors as imitation, not rules;
- rubric inversion;
- loose/bind separation;
- narrative-spine sign-off discipline.

It does not cover any specific application's product strategy, architecture, UX, or operator workflow. Those live in each app's own doctrine.

## Canonical sources (read these in order)

1. `PROPOSAL-AGENT-DIAGNOSIS-2026-05-15.md` in `federal-proposal-assistant` -- why this doctrine exists. It documents the empirical 70% prose ceiling, the validation-first generation pattern, and the missing narrative-spine failure.
2. `PROPOSAL-AGENT-REDESIGN-2026-05-15.md` in `federal-proposal-assistant` -- what to do about it. Track A items A1-A6 define the incremental prose-quality architecture.
3. This file -- the operationalized doctrine. It is what every app building federal proposal AI must implement or consciously defer.

## Reframe, then polish — in that order

The "polish ≠ reframe" anti-pattern above does NOT mean polish is bad. It means polish-AS-A-REPLACEMENT-FOR-reframing is bad. Done in order, both are required. The failure mode polish is meant to catch has a name: *ventriloquism* — declarative statements that position the author as speaking FOR the customer's internal state.

Compelling prose is produced in two stages:

1. **Reframe (perspective).** Adopt the customer's perspective when describing problems. Customer's frame, our voice. Lead with the customer's problem as we understand it; describe their challenge with empathy and demonstrated judgment. Solution comes AFTER problem framing, never instead of it.

2. **Polish (tone-drift gate).** Scan the reframed prose for ventriloquism and downgrade declarative statements about the customer's unstated internal state to bounded epistemic phrasing:
   - "The Navy's top challenge is X" → "Based on our analysis, the Navy's challenges include X"
   - "The customer needs Y" → "Our review of the solicitation indicates the customer requires Y"
   - "AFRL's strategic priority is Z" → "AFRL's published priorities suggest Z is central to this opportunity"

   Preserve declarative voice when the underlying fact is genuinely objective: statute, published policy, public solicitation language, EdgeRunner's own verified capabilities. Require bounded epistemic voice when the subject is the customer's *unstated* priorities, challenges, decisions, or internal posture.

   Polish is not decoration. It is a guard against author overreach. Skipping it because the reframe "sounds customer-centric" produces ventriloquism in nicer wrapping, and evaluators read that as the vendor presuming to speak for them.

## Self-narration and performative honesty -- a second tone-drift failure

Ventriloquism is overreach about the *customer's* internal state. Its mirror is overreach about
*our own* virtue: prose that narrates the proposal's own honesty, candor, restraint, or insight
instead of simply being precise. It shows up as self-congratulatory meta-commentary:

> "The honest boundary is the network layer, and saying so is itself a signal that we understand the
> actual problem rather than overselling a capability we do not hold."

A busy, skeptical evaluator reads this as marketing and as filler. It spends word count praising the
author instead of answering the requirement, and it frequently smuggles in the very overclaim it
claims to disavow. The polish pass must delete it. State the capability and its boundary plainly and
let the precision carry the credibility:

> "EdgeRunner's agents run disconnected at the edge. Cross-domain networking is provided by the
> integrating program, not by EdgeRunner."

Rule: never describe the proposal's own honesty, restraint, or understanding. Assert the bounded
fact; the boundary itself is the signal. Enforced deterministically by the prose-lint
self-referential-commentary check.

## Typography -- no dashes as sentence punctuation

Do not use em-dashes, en-dashes, or double-hyphens as sentence punctuation in customer-facing
proposal prose. Models reach for them constantly; federal proposal house style does not use them.
Rewrite with a period, comma, colon, or parentheses. Enforced by the prose-lint em-dash check.

## Voice anchors -- imitation, not rules

Voice anchors are exemplars of cadence and confidence, not rules to be checked against. Models match cadence far better from examples than from prohibitions.

The canonical voice anchors live in `proposal-workbench/reference/voice-anchors/`:

- `vulcan-jatf-opening.md` -- post-edit Exhibit C from the redesign section 2.3.
- `socpac-section-3-4.md` -- Exhibit D from section 2.6.
- `bill-passage.md` -- placeholder until a confirmed Bill-written passage is added; consumers skip empty/comment-only files.

Each anchor is a short prose excerpt. Anchors are read as exemplars; never paraphrased into a rule. Anchors precede instructions in the rendered prompt so the model orients on cadence first.

Models should imitate:

- cadence;
- paragraph economy;
- transition style;
- argument posture;
- confidence level.

Models must not reuse:

- facts from the anchor;
- names from the anchor;
- mission context from the anchor;
- claims from the anchor.

When a generic banned-word or style heuristic conflicts with the cadence demonstrated by the voice anchor, the anchor wins.

## Rubric inversion -- write the argument, audit afterward

Use this instruction verbatim where a writer is tempted to optimize for a downstream evaluator:

> Write the most compelling honest argument for this section, grounded in the customer's actual problem. The rubric and compliance check run AFTERWARD as audits; they will return a patch list; patch only the gaps. Do not pre-emptively optimize for the rubric.

Telling the writer the test produces formulaic monotony. Rubric inversion stops that. The rubric still matters, but it audits real prose after composition instead of shaping every sentence before the argument exists.

## Loose/bind separation -- composition then verification

Drafting is two structurally separated passes:

- **Pass 1 (loose):** compose in voice. Evidence markers, compliance enforcement, completeness checklist, and pattern enforcement are suspended. The pass is allowed to over-claim because it is not a submission artifact.
- **Pass 2 (bind):** verify on real prose. Attach evidence markers, mark unsupported claims, update the compliance matrix, and repair factual overreach. This pass is forbidden to restyle.

Pass 1 must not receive evidence/compliance bindings. This is not a prompt-only instruction to "ignore" evidence; the inputs are structurally withheld.

Pass 2 reads Pass 1's output as input. Single-pass writing produces slot-filling. The separation is what makes composition possible.

## Narrative spine -- one-page argument, human sign-off

Before any drafting begins, the system produces a one-page prose argument of what the proposal claims and why it is compelling against the customer's actual problem.

A human signs off on this spine before downstream drafting proceeds. The spine is the lengthwise through-line of the document; the storyboard is the crosswise per-section plan. They are not substitutes.

Per Redesign A1, this is the highest-leverage move in the prose-quality stack. It promotes the "what are we arguing and why should the evaluator care?" decision to an early, reviewable artifact instead of burying it inside section drafting.

## Cross-app references

Per-app implementations of this doctrine:

- `proposal-workbench/PRODUCT-DOCTRINE.md` -- workbench product north star. It links here for prose-quality doctrine.
- `federal-proposal-assistant/CLAUDE.md` -- FPA runtime contract. Track B remains documented there; A3 voice anchors are imported from the canonical workbench paths in WP-N2.
- `federal-proposal-copilot/CLAUDE.md` -- copilot runtime contract. Copilot syncs up to the shared prose-quality scope in WP-N3.

The earlier `PRODUCT-DOCTRINE.md` section "Where the prose-quality work actually lives" is superseded by this canonical-source model. The diagnosis and redesign docs remain canonical in FPA; this file operationalizes them for every app.

## How to consume this doctrine

Each downstream app drops the consumer sync script template from this repo into its own `tools/` directory and runs it on demand:

- source template: `proposal-workbench/tools/consumer-sync-template.sh`;
- default destination doctrine: `reference/PROSE-QUALITY-DOCTRINE.md`;
- default destination anchors: `reference/voice-anchors/`.

The script fetches `PROSE-QUALITY-DOCTRINE.md` and the canonical voice anchors from the proposal-workbench repo. See `tools/consumer-sync-template.sh` for usage and override variables.

## Revision discipline

When this doctrine is refined in proposal-workbench, the PR description must note the cross-app implication.

Consumers re-run their sync script when they choose to absorb the update. There is no automated cross-repo CI in this model; consumers own when they pull the shared doctrine and anchors into their own repository.
