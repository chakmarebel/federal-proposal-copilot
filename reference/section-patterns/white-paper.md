---
patterns_id: white-paper
display_name: White Paper / Directed Brief / Unsolicited
typical_length: 3-10 pages
target_word_count: 1200
max_word_count: 2000
section_order:
  - cover-page
  - executive-summary
  - problem-statement
  - proposed-approach
  - outcomes-and-value
  - team-and-credibility
  - rom-or-next-steps
required_sections: [executive-summary, problem-statement, proposed-approach, outcomes-and-value]
optional_sections: [cover-page, team-and-credibility, rom-or-next-steps]
---

# White Paper Section Patterns

White papers must earn their time in the first 60 seconds. The executive summary carries the proposal — if the reader stops there, the recommendation must still land.

**Length budget (hard cap: 2,000 words total).** The writer MUST check word count before declaring the draft complete. If the draft exceeds 2,000 words, compress before handing off — do not ship the long draft and let the reviewer cut. Target is 1,200 words.

**`required_sections` semantics.** The listed sections are the *maximum eligible set* — not a minimum floor to which more can be added without budget pressure. Every section costs word budget. Add optional sections only when the source material clearly justifies them AND the total stays under 2,000 words.

**Per-section word budgets (at 1,200-word target):**

| Section | Target | Hard Max |
|---|---|---|
| executive-summary | 200 words | 250 words |
| problem-statement | 150 words | 200 words |
| proposed-approach | 300 words | 400 words |
| outcomes-and-value | 150 words | 200 words |
| team-and-credibility | 100 words | 150 words |
| rom-or-next-steps | 100 words | 150 words |
| custom policy/considerations list | 300 words | 400 words |

**Heading depth.** Title is paragraph-styled (not Heading 1). Section headings at H3 (`### 1. Title`) in markdown source, which exports as Heading 3 in Word. No subsection headings (H4+) in a brief under 10 pages.

## cover-page
**Purpose:** Brand + context in 10 seconds. Often omitted for short (<5pp) directed briefs.
**Template:**
```
# [Solution Name]
## A White Paper from [Company] to [Customer]
### [One-line positioning — what this is about]

Prepared by: [Company], [Date]
Point of Contact: [Name, email, phone]
Distribution: [Statement from reference/distribution-statements.md if applicable]
```

## executive-summary (required)
**Purpose:** The paper in one page. If evaluator only reads this page, what must land?
**Structure:** Plain thesis sentence or theme statement (Pattern 1, only if it sounds natural) → 3-4 bullets naming AoIs / mission pains addressed with proof points (Pattern 2) → commitment (timeline + what's next).
**Template:**
```
**[Theme statement: what we do, why it matters, proof hook].**

[Customer] operates in [environment]. [State the operational constraint in customer language; do not ghost competitors in general white papers.]
We offer:

1. **[Discriminator 1].** [Proof point]. Addresses [AoI or customer need].
2. **[Discriminator 2].** [Proof point]. Addresses [AoI/need].
3. **[Discriminator 3].** [Proof point]. Addresses [AoI/need].

See Figure 1 for the architecture. [Action caption reference — Pattern 3.]

We commit to [specific outcome] within [timeframe].
```
**Patterns:** 1 where natural, 2, 3. Do not force ghosting in general white papers.

## problem-statement (required)
**Purpose:** Demonstrate we understand the customer's world, in their language.
**Structure:** 1-2 paragraphs. Framing sentence → 2-3 concrete pains → pivot to "addressing these requires..."
**Pitfalls:** Don't describe OUR capability here. That comes next.

## proposed-approach (required)
**Purpose:** Describe what we'd do, grounded in the architecture.
**Structure:** Overview paragraph → 3-4 numbered capabilities, each with: what we do, how it works, proof it's deployable.
**Reference graphic:** Typically a single architecture diagram (Figure 1). Must have an action caption (Pattern 3) in the text, not embedded in image.
**Patterns:** 1, 2, 3 per subsection

## outcomes-and-value (required)
**Purpose:** What the customer gets. Quantify.
**Structure:** 2-3 sentences per outcome, with numbers where possible. Tie each outcome back to the customer's stated mission pain.

## team-and-credibility (optional)
**Purpose:** Why us vs. anyone else claiming the same thing.
**Include if:** Page budget allows AND the team is a meaningful differentiator (named PIs, prior contract performance, specific credentials).
**Structure:** 1 paragraph per key team member + 1 paragraph per proof contract (customer, scope, outcome).

## rom-or-next-steps (optional)
**Purpose:** Give the reader a clear next action.
**Include if:** The customer asked for a ROM OR the paper is a pitch-for-engagement.
**Structure:** If ROM, follow `reference/pricing-artifacts/rom.md` (very short version — range, assumptions, validity). If next-steps, 2-3 bullets with timeline.

## rom-or-next-steps — considerations / recommendations template

When this section contains a numbered list of policy considerations or recommendations (e.g., Senate staff asks, customer asks), use **imperative voice, one sentence each**:

```
1. [Imperative verb phrase — the action the reader should take.]
2. [Next action.]
```

Do NOT add rationale paragraphs under each consideration. If rationale is needed, append a single em-dash clause: `1. [Action] — [brief one-clause rationale].`

The wrong pattern (too long):
> 1. Mandate provenance disclosure. Congress should require any AI vendor seeking federal contracts to disclose the national origin of all training data. This is important because...

The right pattern:
> 1. Mandate provenance disclosure for any AI vendor seeking federal contracts.

## Global rules
- **No filler.** Every sentence earns its place.
- **No FAR-style boilerplate** (reps & certs, CLINs, etc. — wrong format).
- **Max 2 graphics.** White papers with 5+ figures read like sales collateral.
- **Opening discipline.** Every section needs a clear first sentence, but not every section needs a formal Shipley-style theme statement. If the formal pattern makes the section sound robotic, use a plain topic sentence that advances the narrative spine.
- **Cut criterion.** Before declaring the draft complete, apply this test: would deleting this section change a reader's takeaway from the executive summary? If no, cut it.
- **Length check.** Run a word count before marking the draft complete. Exceed 2,000 words? Compress, don't hand off.
