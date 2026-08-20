---
type_id: unsolicited-proposal
display_name: Unsolicited Proposal (FAR Subpart 15.6)
solicitation_vehicle: unsolicited
page_target: 15-30 excl. cover, appendices, and cost volume
pricing_artifact: far-cost-volume
pp_required: true
submission_mechanism: email
required_skills: [customer-intel, capture-scorecard, capture-intent, proposal-manager, proposal-solution-architect, past-performance, pricing-analyst, narrative-spine, proposal-storyboard, technical-review, proposal-graphics, proposal-writer, proposal-editor, compliance-check, evidence-check, red-team-review, export-proposal]
skipped_skills: [opportunity-quick-look, capture-portal-structure, submission-summary, competitor-assessment, adversarial-review, proposal-patcher]
section_patterns: unsolicited-proposal
compliance_sources: [FAR-15.603c, FAR-15.605, FAR-15.609, AgencySupplement]
evaluator_framing: An acquisition coordinator screening for validity in fifteen minutes, then a technical evaluator asking whether this is worth spending money on outside of competition
typical_duration: 2-4 weeks
notes: |
  A FAR Subpart 15.6 unsolicited proposal. This is NOT the same as the `white-paper` type, which
  covers unsolicited *thought pieces*. An unsolicited proposal offers to perform work for a price and
  asks the Government to obligate money outside of competition. It has a fixed, fully enumerable
  content requirement set even though there is no solicitation.

  **Why compliance-check is required here and skipped for white-paper.** There is no Section L, but
  FAR 15.603(c) (six validity criteria), 15.605 (a/b/c content), and 15.609 (legends) are a closed
  requirement list, and the agency supplement adds more. `proposal-manager` seeds the compliance
  matrix from the enumerated citation set in `reference/section-patterns/unsolicited-proposal.md`
  rather than from a solicitation PDF. A worked example of the finished matrix is
  `reviews/2026-08-20-hsi-unsolicited-compliance-matrix.md`.

  **The screening gate is validity, not quality.** At FAR 15.606-1 a coordinator screens for the six
  15.603(c) criteria and the 15.605 content list. Failing any one is a return without technical
  evaluation, however good the technical approach is. Build the validity table and the compliance
  matrix FIRST, not last.

  **Route to acquisition, not to the program office.** Send formally to the agency's unsolicited
  proposal coordinator or contracting activity, with the cognizant program office copied for
  technical validation. State explicitly that only the Contracting Officer can bind the Government
  (FAR 15.604(b)). A proposal mailed only to a program manager usually dies unreviewed.

  **The two claims that kill these.** (1) Commercial availability: most agency supplements bar an
  unsolicited proposal that offers a commercially available item. Scope the submission to the work
  that genuinely is not on a catalog, and point the Government at our vehicles for anything that is.
  (2) Prior contacts: 15.605(c)(7) requires naming every agency person already contacted. This is a
  signed representation. Reconcile it against the addressee list before anything ships.
---

# Unsolicited Proposal (FAR Subpart 15.6)

## Reader mindset

Two readers in sequence, and they want different things.

**Reader one, the unsolicited proposal coordinator.** Fifteen minutes, screening at FAR 15.606-1 for
validity and completeness. They are not evaluating the idea. They are checking whether this is a valid
unsolicited proposal that they are obliged to route, or something they can return. They read the title
page, the validity table, and the content checklist. Make their job mechanical and they will route it.

**Reader two, the technical evaluator at 15.606-2.** They are being asked to justify spending money
outside of competition, which is a harder thing to defend than picking a winner in a competition.
Their unspoken question is "why can nobody else do this, and why should we not just compete it?" The
answer has to be in the document and it has to be specific.

## Required artifacts

- Title page with the FAR 15.609(a) restrictive legend and control number
- Letter of transmittal, signed by an official authorized to obligate the offeror
- Statement of validity, all six FAR 15.603(c) criteria, separately affirmed
- Basic information block, FAR 15.605(a)(1) through (a)(6)
- Technical content, FAR 15.605(b)(1) through (b)(4), including key personnel **and alternates**
- Supporting content, FAR 15.605(c)(1) through (c)(7)
- Cost detail sufficient for meaningful cost realism analysis. This is a lower bar than a Section L
  cost volume but a much higher one than a ROM
- Compliance matrix mapping every citation above to its location, as an appendix
- FAR 15.609(b) sheet markings on every restricted page

## Common pitfalls

Each of these was observed live in the HSI proposal review of 20 August 2026
(`reviews/2026-08-20-hsi-unsolicited-proposal-review.md`). They are the reason this type exists.

- **Naming a program sponsor while representing that no contact has occurred.** The single most
  common return reason, and an integrity problem rather than a drafting one.
- **Self-labelling a commercially available element inside the price.** Honest, and it hands the
  Contracting Officer the disposition. Scope it out and point at the vehicle instead.
- **Placeholder key personnel.** 15.605(b)(3) names alternates explicitly. Brackets here read as an
  unstaffed effort.
- **Past performance written from memory.** In a 15.6 submission past performance is a
  representation. Write it from `my-company/past-performance.md` and the evidence ledger, never from
  recall, and never fuse two separate relationships into one stronger-sounding sentence.
- **An accreditation schedule with no Government review time in it.** ATO and agency software-approval
  gates are Government-controlled. On firm-fixed-price, an optimistic assumption is our money.
- **Negative claims about the customer's own portfolio.** "No fielded capability does this" is
  unverifiable by us and falsifiable by them. Claim what we do and let them draw the conclusion.
- **Publishing scale-up pricing nobody asked for.** A not-to-exceed for a future option year exposes a
  per-seat delta and invites a cost-realism question about the base.
- **Success metrics the offeror does not control.** Split contract performance measures from mission
  outcome indicators. Only the first belong in a fixed-price commitment.

## Acquisition guidance

Apply `reference/doctrine/acquisition-guidance-catalog.md` (Applicability Matrix row for this type):

**Tier 1 (cost):** 15.605(c)(1) requires enough detail for a meaningful determination. Every cost
element needs a stated basis. Apply the GAO-20-195G four characteristics to the breakdown.
**Tier 2 (pathway):** name the acquisition path you believe fits, and offer an alternate. Unsolicited
proposals often convert better through an other-transaction or an S&T innovation program than through
a FAR 6.302 justification, and offering both reads as acquisition literacy.
**Tier 3 (ATO):** accreditation is usually the schedule driver. Name the gates, name who controls
them, and price the accreditation period as a standalone milestone. Keep every IL and ATO claim
evidence-cited and inside `my-company/claim-envelope.md`.
**Tier 4 (AI):** for AI capability, answer in the customer's own AI governance vocabulary, and state
the human-decision gate as an architectural property rather than a policy promise.

## Sole-source reality check

Run this before drafting, in `capture-scorecard`. An unsolicited proposal is pure internal spend with
no guaranteed reader, so the go decision has to survive four questions.

1. Can the Government articulate why only we can do this, in one sentence, using our words? If not,
   the likely outcome is a competed requirement that we have just written for someone else.
2. Is there a plausible funding line that does not require a new start? Name it.
3. Is there a sponsor with both the mission need and the acquisition latitude to act, and is that the
   office we are sending it to?
4. What does the customer's own forecast say? Document the SAM.gov and agency forecast search with
   dates and terms, and keep the record. 15.603(c)(5) is an assertion we may be asked to support.
