---
patterns_id: ota
display_name: OTA Full Proposal (Prototype Project)
typical_length: 20-40 pages
section_order:
  - cover-page
  - executive-summary
  - statement-of-objectives-response
  - prototype-project-scope
  - technical-approach
  - milestone-schedule
  - team-composition
  - data-rights-assertions
  - follow-on-production
  - relevant-experience
required_sections: [executive-summary, statement-of-objectives-response, prototype-project-scope, technical-approach, milestone-schedule, team-composition, follow-on-production]
optional_sections: [cover-page, data-rights-assertions, relevant-experience]
---

# OTA Section Patterns

OTAs are prototype agreements under 10 USC 4022. The Agreements Officer + Program Manager care about prototype value, milestone execution, non-traditional status, and follow-on production path — NOT FAR Part 15 cost realism.

## executive-summary (required)
**Purpose:** Prototype concept + team credibility + follow-on production commitment.
**Structure:** What we'll prototype → why the current approach fails → what we deliver → follow-on transition path.

## statement-of-objectives-response (required)
**Purpose:** Map every SOO objective to a section in this proposal. The AO uses this as the crosswalk.
**Structure:** Table: SOO objective → addressed in section § → success criterion.
**Must be complete.** Every SOO item maps somewhere.

## prototype-project-scope (required)
**Purpose:** Clear boundaries of what's a prototype vs. what's production.
**Structure:** In-scope list → out-of-scope list → success definition.

## technical-approach (required)
**Purpose:** How we build the prototype.
**Structure:** Architecture → build approach → integration plan → test plan.
**Reference graphic:** Architecture diagram + integration context.
**Patterns:** 1, 2, 3

## milestone-schedule (required)
**Purpose:** Milestone-payment schedule. The external pricing artifact for an OTA.
**Reference:** `reference/pricing-artifacts/ota-milestones.md`
**Structure:** Milestone table with deliverable, acceptance criterion, duration, payment.
**Export:** Renders to `final/docx/` embedded AND `final/xlsx/milestone-schedule.xlsx` companion.

## team-composition (required)
**Purpose:** Prove non-traditional contributor status (or document cost share justifying traditional prime).
**Structure:** Per-organization: role, non-traditional determination, specific contributions.
**Pitfalls:** Don't gloss over non-traditional status. Either assert it with evidence or show cost share ≥1/3 for traditional primes.

## data-rights-assertions (optional but usually required)
**Purpose:** What rights the government gets in deliverables.
**Authority:** 10 USC 4022 (NOT DFARS 252.227).
**Structure:** Per-deliverable: data category (Restricted / Government Purpose / Unlimited), basis, marking.

## follow-on-production (required)
**Purpose:** Establish eligibility for 10 USC 4022(f) follow-on production.
**Structure:** 2-3 paragraphs. Successful prototype → expected Phase III vehicle → terms negotiable at production time.
**Critical:** If omitted, cannot be added after award. Always include.

## relevant-experience (optional)
**Purpose:** Prior OTA or prototype execution credibility.
**Structure:** 2-3 references. Agreement #, customer, scope, outcome. NOT PPQ format — this is lighter.

## Global rules
- **No FAR cost volume.** Milestone payments only (cost buildup stays internal in `working/pricing-inputs.md`).
- **Non-traditional or cost share.** One or the other must be established.
- **10 USC 4022 data rights.** Using DFARS citations is a red flag that we don't understand OTAs.
- **Follow-on production language is not optional.**
