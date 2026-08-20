---
type_id: white-paper
display_name: White Paper (directed or unsolicited)
solicitation_vehicle: unsolicited
page_target: 3-10
pricing_artifact: none
pp_required: false
required_skills: [submission-summary, customer-intel, proposal-solution-architect, narrative-spine, proposal-graphics, proposal-writer, evidence-check, red-team-review, proposal-patcher, adversarial-review]
skipped_skills: [opportunity-quick-look, proposal-manager, competitor-assessment, capture-scorecard, past-performance, pricing-analyst, compliance-check, proposal-editor, proposal-storyboard]
section_patterns: white-paper
compliance_sources: []
evaluator_framing: Busy stakeholder reading on a phone — lead with the mission pain and the "so what"; everything else is optional
typical_duration: 3-10 days
notes: |
  Unsolicited or directed white paper. No solicitation = no compliance matrix. Purpose is to
  influence thinking, generate a follow-up meeting, or shape a future solicitation. Pricing is
  optional (include a ROM only if the reader asked for one).

  Track B workflow — narrative-first, not structure-first:
    1. narrative-spine    → human sign-off on the argument before any prose
    2. proposal-writer    → draft-loose (voice draft) then bind (evidence + verification)
    3. evidence-check     → CLAIM-UNSUPPORTED audit
    4. red-team-review    → Gold Team W/D findings
    5. proposal-patcher   → surgical fixes from audit, no global rewrite
    6. export-proposal    → final .docx

  proposal-storyboard and proposal-editor are SKIPPED for this type. The storyboard
  is replaced by the narrative spine + writer's loose pass. The editor is replaced by
  the patcher's surgical audit-driven fixes.

  If this is in response to a Request for White Papers (RWP) with evaluation criteria,
  use ota-white-paper or cso-brief instead — those include compliance and ROM.

  If this offers to perform work for a price and asks the Government to obligate money outside
  of competition, it is an unsolicited PROPOSAL, not an unsolicited white paper. Use
  unsolicited-proposal instead. That type carries the FAR 15.603(c) / 15.605 / 15.609 requirement
  set and requires compliance-check; this one has no compliance source and skips it.
---

# White Paper

## Reader mindset
The reader has 5 minutes. They skim the executive summary and the figures. If they don't get the "so what" in the first page, the rest doesn't get read.

## Required artifacts
- Executive summary (1 page — problem, insight, recommendation)
- Operational / mission problem framing
- Proposed approach or capability
- Outcome / impact (quantified if possible)
- One or two graphics (architecture or concept)
- Optional: ROM, schedule, team

## Common pitfalls
- Writing a proposal instead of a thought piece
- Burying the recommendation at the end
- No clear call-to-action (what should the reader do next?)
- Pricing where none was asked for — signals you don't understand the format


## Acquisition guidance

Apply `reference/doctrine/acquisition-guidance-catalog.md` (Applicability Matrix row for this type):

**Tier 2 (pathway):** if a software/AI capability, frame to **DoDI 5000.87 (SWP)** — MVP/MVCR and a ≤12-month-to-operational story; name the AAF pathway the reader actually buys on.
**Tier 3 (ATO):** for Navy readers, **RAISE 2.0** — container/security-gate posture and **edge ConMon via stage-sync** turn DDIL deployment into a designed-for behavior. Keep IL/ATO claims evidence-cited.
**Tier 4 (AI):** answer in the DoD AI Ethical Principles vocabulary, not as an adjective.
