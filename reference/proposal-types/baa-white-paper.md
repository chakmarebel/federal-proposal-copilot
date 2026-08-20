---
type_id: baa-white-paper
display_name: BAA White Paper (step 1 of a two-step BAA)
solicitation_vehicle: BAA
page_target: 3-5
pricing_artifact: rom
pp_required: false
required_skills: [opportunity-quick-look, submission-summary, customer-intel, capture-intent, proposal-solution-architect, narrative-spine, proposal-graphics, pricing-analyst, proposal-writer, evidence-check, red-team-review, proposal-patcher, adversarial-review]
skipped_skills: [proposal-manager, competitor-assessment, capture-scorecard, past-performance, proposal-storyboard, proposal-editor, compliance-check, technical-review]
section_patterns: white-paper
compliance_sources: [TechnicalTopics, ResearchObjectives]
evaluator_framing: Lab technical POC deciding whether to invite a full proposal and whether this is worth a share of a research budget they control — scientific merit and topic fit, not commercial polish
typical_duration: 1-2 weeks
submission_mechanism: email
notes: |
  Step 1 of an open two-step BAA (AFRL AFAR FA8750-23-S-7008, ARL W911NF-23-S-0001, and
  most lab BAAs). The white paper is the initial submission; formal proposals are accepted
  BY INVITATION ONLY. Winning the white paper stage buys an invitation, not an award.

  Distinct from the other white-paper types in this catalog:
    - `white-paper`      — unsolicited thought piece, no ROM, no named topic. Wrong here:
                           a BAA white paper is scored against a published research topic.
    - `ota-white-paper`  — gate to a 10 USC 4022 prototype OTA. Wrong here: the award
                           instrument under a BAA is usually a FAR contract or assistance
                           agreement, and non-traditional-contributor status is irrelevant.
    - `baa`              — the FULL proposal, 15-30 pages with a FAR cost volume. That is
                           step 2, and only after an invitation.

  Compliance is light but real: BAAs prescribe required white-paper content (title,
  submitter, topic name AND topic/focus-area ID, TPOC name, objective and approach,
  innovation and advancement over the state of the art, ROM cost estimate, biographical
  qualifications) and required markings for proprietary and restricted technical data.
  `compliance-check` is skipped because there is no Section L/M to matrix, but the
  required-content list belongs in `working/submission-summary.md` and must be verified
  by hand before send.

  Two structural facts drive strategy on an OPEN BAA:
    1. Open BAAs have annual funding windows, not a single deadline. Missing a window
       does not close the door — the paper sits in the bin against the next tranche.
       An awardable-but-unfunded paper on file when money lands is the mechanism.
    2. Multiple awards per focus area across multiple funding years are normal. An
       incumbent holding the focus area is a teaming target as often as a blocker.

  A white paper with no advocate inside the lab is a filing, not a pursuit. Name the
  internal champion in `working/capture-intent.md` or do not submit.

  ROM is a rough-order-of-magnitude range with the cost drivers named, not a priced
  BOE. Pricing detail belongs in step 2.
---

# BAA White Paper

## Evaluator mindset
A lab technical POC with a research budget and more ideas than money. They are asking:
"Does this fit my published topic? Is it actually new? Can these people do it? Roughly
what does it cost, and does that fit what I might have?" They will decide in one sitting
whether to spend a full-proposal review cycle on it.

They are not a contracting officer and not a source-selection board. Scientific merit and
topic fit decide it.

## Required artifacts
- Header block: title, submitting organization, research topic name, topic / focus-area ID,
  TPOC name (the BAA usually mandates all five and papers get bounced without them)
- Objective — the research question, stated as a question
- Technical approach with phases and go/no-go decision points
- Innovation: what is new, and what state of the art it advances past. Name the prior work
  it beats and say by how much
- Prior results that make the claim credible — publications, prototypes, measured benchmarks
- Biographical qualifications for the PI and key technical staff
- ROM cost estimate with a period of performance, and the cost drivers named
- One graphic, if it carries an argument the prose cannot
- Proprietary / restricted-data markings per the BAA's marking instructions

## Common pitfalls
- Pitching a product instead of a research question. This is 6.1/6.2 money; the reader
  buys hypotheses, not licenses
- Omitting the topic / focus-area ID, which is the single most common bounce reason
- Exceeding the page limit. 3-5 pages usually means 5, and a sixth page is a rejection
- Over-claiming TRL. Labs fund the gap between what works and what is proven; claiming
  it already works argues yourself out of the money
- No named PI. Merit review is personality-driven and an unnamed team reads as unstaffed
- Pricing like a proposal. A ROM range with drivers is what was asked for
- Treating a missed window as a closed door on an open BAA

## Acquisition guidance

Apply `reference/doctrine/acquisition-guidance-catalog.md`:

**Tier 1 (cost):** ROM realism per GAO-20-195G — a range with named drivers and a stated
basis beats a single number with no derivation.
**Tier 2 (pathway):** if the work transitions to a program, name the receiving program
office and the follow-on instrument. BAA awards die at the end of the period of
performance unless a transition path was designed in.
**Tier 3 (ATO):** keep IL/ATO claims evidence-cited. A 6.2 research effort does not need
an ATO, and claiming accreditation the research does not require reads as padding.
