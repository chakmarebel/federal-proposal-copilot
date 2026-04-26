---
patterns_id: rom
display_name: Standalone ROM
typical_length: 1-3 pages
section_order:
  - header-block
  - scope
  - estimated-investment
  - basis-of-estimate
  - key-cost-drivers
  - key-assumptions
  - risks-to-estimate
  - next-steps
required_sections: [header-block, scope, estimated-investment, basis-of-estimate, key-assumptions]
optional_sections: [key-cost-drivers, risks-to-estimate, next-steps]
---

# ROM Section Patterns

Short, directional, defensible. Not a cost volume. Not a proposal. A ballpark the customer uses to decide whether to fund a formal RFP.

See `reference/pricing-artifacts/rom.md` for the full pricing artifact spec. This file is the **narrative section structure** that `/proposal-writer` produces for ROM-type proposals. Both files align; pricing-analyst produces `drafts/rom.md` using this structure.

## header-block (required)
**Purpose:** Who, who-for, when, validity window.
**Template:**
```
**To:** [Customer / POC]
**From:** [Your Company]
**Date:** [YYYY-MM-DD]
**Validity:** Valid for [30-60] days from the date above.
```

## scope (required)
**Purpose:** What's in, what's out. One paragraph.
**Structure:** 3-5 sentences. Deliverables, boundaries, explicit exclusions.

## estimated-investment (required)
**Purpose:** The number. As a range.
**Structure:**
```
**$[Low] – $[High]** over **[N] months**
*(range ±[X]% based on [method])*
```

## basis-of-estimate (required)
**Purpose:** How the range was derived.
**Structure:** Name the method (Analogous / Parametric / Expert judgment). 1 paragraph explaining the derivation.

## key-cost-drivers (optional)
**Purpose:** The 3-5 things that dominate the number.
**Structure:** Bulleted list. Each bullet: driver → rough cost-swing implication.

## key-assumptions (required)
**Purpose:** The 3-5 assumptions that, if false, change the range.
**Structure:** Bulleted list. Each bullet: assumption → what changes if false.

## risks-to-estimate (optional)
**Purpose:** What could move the range upward.
**Structure:** 2-4 bullets. Scope creep, schedule compression, dependencies, etc.

## next-steps (optional, recommended)
**Purpose:** What the customer needs to do to turn a ROM into a firm proposal.
**Structure:** 2-4 bullets on what decisions/information would firm the estimate.

## Global rules
- **Range, not point.** Never "$1.25M" — always "$1.0M-$1.5M" or "$1.2M ±25%".
- **Validity window.** Without one, ROMs rot and become de facto commitments.
- **No CLINs. No BOE narratives. No indirect rate disclosures.** If your ROM looks like a cost volume, you've failed.
- **Significant figures match the uncertainty.** `$1,487,293.22` is as wrong as `$1.5M` under a ±30% range — just in the opposite direction.
