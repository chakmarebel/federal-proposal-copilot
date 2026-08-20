---
type_id: pitch-demo
display_name: Pitch + Demo (CSO/OTA Phase 2 Down-Select)
solicitation_vehicle: CSO
page_target: "≤20 slides + ≤20-min video demo + short admin/technical-abstract volume"
pricing_artifact: rom
pp_required: relevant-experience
submission_mechanism: document-upload
required_skills: [submission-summary, proposal-manager, customer-intel, capture-intent, proposal-solution-architect, past-performance, pricing-analyst, narrative-spine, proposal-storyboard, technical-review, proposal-graphics, proposal-writer, proposal-editor, compliance-check, evidence-check, red-team-review, export-proposal]
skipped_skills: [opportunity-quick-look, capture-scorecard]
section_patterns: pitch-demo
compliance_sources: [EvaluationCriteria, AreasOfInterest, InvitationLetter, DemonstrationRequirements]
evaluator_framing: Technical advisors watching a LIVE test of your *testing/prototype capability* against a published rubric, then probing it for ~40 minutes of Q&A. Points come from criteria satisfied and capability shown running — not from product polish or a compelling story.
typical_duration: 2-3 weeks
readiness_gate: reference/pitch-demo-readiness-gate.md
notes: |
  The Phase-2 down-select in a DIU/CSO or OTA pitch event: you passed the Phase-1
  brief and are now invited to present + demonstrate live. Deliverables are a slide
  deck, a pre-recorded video demo, a short administrative/technical-abstract volume,
  a ROM, and (often) a company survey — uploaded to a portal (Box) ahead of a live
  60-min session (≤20 min present/demo + ≥40 min Q&A with technical advisors).

  THIS TYPE EXISTS BECAUSE THE DEMO IS THE PROPOSAL. It is structurally different
  from a written volume: the scored evidence is a live/recorded demonstration and the
  answers given under 40 minutes of hostile technical Q&A — not prose an evaluator
  reads alone. The single biggest failure mode (see the MYSTIC DEPOT Phase II loss,
  2026-07) is bringing a differentiated *concept* whose decisive moments are captured
  or roadmap rather than built-and-live, and treating the pitch as a product-demo
  opportunity instead of a scored answer to the customer's published requirement.
  The readiness gate below is mandatory precisely to defeat that failure mode.
---

# Pitch + Demo (CSO/OTA Phase 2 Down-Select)

## Evaluator mindset
You already cleared Phase 1 — the panel is interested. Now technical advisors (often MITRE or an FFRDC) watch you *demonstrate* the capability and then spend most of the hour probing it. They are scoring **the rigor of the thing the solicitation said it would grade**, defending an adjectival rating against a rubric. They discount anything they cannot see run. In a resource-limited down-select, clearing every published rubric row is necessary — out-flashing a rival is not the game.

**Read the grading sentence out of the Invitation Letter and make it the spine.** In MYSTIC DEPOT it was verbatim: *"we will be grading the rigor and reliability of your testing capabilities rather than the performance of an AI-enabled system itself."* We quoted it on one slide and then built a demo that showed the AI performing. Do not repeat that.

## Required artifacts
- **Demo storyboard** keyed to the rubric — every beat maps to a scored criterion, with an explicit `live | captured-reproducible | roadmap` maturity label per beat (`/proposal-storyboard`).
- **Pitch deck** (slides PDF) — cover with any required restricted-data legend; maturity vocabulary on every capability callout.
- **Video demonstration** (≤ the stated length) — the recorded evidence; script via `/proposal-writer`.
- **Administrative / technical-abstract volume** — company viability, ROM, schedule, data rights, classified-work approach, OCI/foreign-national disclosures.
- **ROM pricing** (`reference/pricing-artifacts/rom.md`) — a scored field. Fill it early; a blank caps the rating.
- **Requirements-to-solution crosswalk** — maps every Letter requirement to where it is demonstrated.
- Company survey / attendee roster / RSVP — operational, tracked but not scored content.

## Readiness gate (MANDATORY — this is why the type exists)
Apply [`reference/pitch-demo-readiness-gate.md`](../pitch-demo-readiness-gate.md) at three points:
1. `/technical-review --phase=approach` — run gate rows **G1–G5** as a pre-build feasibility check on the storyboard, *before* graphics or video production. A P0 fail here means the concept or the claim changes, not the label.
2. `/red-team-review` (Gold) — re-run the **full gate** on the finished package; a scored capability may not be labeled `integrated`/`live` unless a reproducible artifact backs it. Score optimism drift explicitly (final self-assessment must be at least as harsh as the first honest one).
3. `/export-proposal` — **any open P0 gate row is export-blocking**, same posture as the pre-submit prose/structure lint. Do not package a deck that claims live capability it cannot re-run under Q&A, or carries a blank on a scored field.

## Common pitfalls (all observed in MYSTIC DEPOT Phase II)
- **Demoing the product instead of answering the requirement.** The camera must be on the capability the Letter grades, not on the AI doing tricks.
- **Captured/roadmap money-moments presented as live.** The two beats that prove the graded capability must run on the machine, staged to re-run under questioning.
- **Demoing a stand-in for the claimed thing** (auditing an abstract agent while claiming to audit a *fielded* system). What runs must make the evaluator's read-back sentence literally true.
- **Scored capability parked on an un-integrated or unconfirmed partner.** Roadmap doesn't score at a down-select; teaming/OCI confirmations are submission-blocking.
- **Blanks on scored admin fields** (ROM, licenses) carried into review. A blank is a rating cap.
- **Answering one line of effort and skipping the other.** Multi-LOE solicitations score every line; a demo that covers only the favorite one (Mystic Depot: LOE1 harness shown, LOE2 methodology barely) leaves scored points on the table. (Gate G10.)
- **Running out of time and dropping the last slides.** A 20-min plan with no buffer sheds its back-end content when the live demo runs long — and the back end is often where required disclosures (OCI §VI) and scored follow-on (§VIII) live. Rehearse to time; front-load scored content. (Gate G11.)
- **Under-rehearsed 40-minute Q&A.** Most of the risk lives here; run an adversarial murder-board, not a doc review.

## Acquisition guidance

Apply `reference/doctrine/acquisition-guidance-catalog.md` (Applicability Matrix — use the `cso-full`/`ota-proposal` row closest to the vehicle):

**Tier 2:** ROM basis per the vehicle — **CSO § 3458** commercial pricing or **10 U.S.C. § 4022** milestone framing; never a FAR BOE.
**Tier 1:** GAO-20-195G four characteristics for defensible ROM sizing; cost framing per DoDI 5000.73.
**Tier 3:** cATO / RAISE 2.0 for any fielding/ATO claim — evidence-cited (IL-6 only in ICOP/PMW-120 context, stated as IATT not ATO).
**Tier 4:** OMB M-25-21/M-25-22 + DoD AI principles for AI claims.
**Tier 5:** two-bucket data rights (DoDI 5010.44) for any produced deliverable; state GPR posture on harness/methodology.
