---
patterns_id: pitch-demo
display_name: Pitch + Demo (CSO/OTA Phase 2 Down-Select)
typical_length: ≤20 slides + ≤20-min video + short admin/technical-abstract volume
section_order:
  - demo-storyboard
  - pitch-deck
  - video-demonstration
  - admin-technical-abstract
  - rom-and-schedule
  - requirements-crosswalk
  - operational-submission-items
required_sections: [demo-storyboard, pitch-deck, video-demonstration, admin-technical-abstract, rom-and-schedule, requirements-crosswalk]
optional_sections: [operational-submission-items]
---

# Pitch + Demo Section Patterns

Unlike a written volume, the scored "sections" here are **submission artifacts**: a demo storyboard that drives everything, a slide deck, a recorded video, a short admin/technical-abstract volume, and a ROM. The evaluator scores what they watch and what you defend in Q&A. The demo storyboard is the master artifact — the deck, the video, and the crosswalk all derive from it.

Every capability callout in every artifact carries a maturity label using the verbatim vocabulary in `reference/pitch-demo-readiness-gate.md` (or the Invitation Letter's mandated vocabulary if it specifies one).

## demo-storyboard (required — the master artifact)
**Purpose:** The section-by-section (beat-by-beat) plan for the demonstration, keyed to the rubric. This is where the pitch is won or lost.
**Structure (per beat):** evaluator question → scored criterion it earns → what runs on screen → maturity label (`live | captured-reproducible | roadmap`) → proof/data → owner.
**Hard rule:** every beat maps to a scored criterion (readiness gate **G1**); every beat that claims a scored point is `live` or `captured-reproducible` by the record date (**G2**). Orphan beats are cut.
**Produced by:** `/proposal-storyboard`. Gated by `/technical-review --phase=approach` (G1–G5) before graphics/video.

## pitch-deck (required)
**Purpose:** ≤20 slides carrying the argument and the scored admin content the panel reads on screen.
**Structure:** cover (+ restricted-data legend if required) → the problem / the requirement → our answer (grading-sentence spine) → demo arc preview → team → company viability → ROM + schedule → data rights → OCI / foreign-national → close (follow-on production authority).
**Reference graphic:** OV-1 / SV-1 / demo-arc. Keep PowerPoint/Figma-recreatable.
**Pitfall:** do not let the deck reorganize around the product's story; it mirrors the storyboard's rubric spine.

## video-demonstration (required)
**Purpose:** The recorded evidence of the capability, ≤ the stated length.
**Structure:** intro → the graded capability shown end-to-end → the two decisive "money-moment" beats (measurement/scoring readout + the Letter-required worked example) → honest maturity narration throughout.
**Script:** via `/proposal-writer`. **Every claim in the video must survive G2/G3** — what's on camera is what you can re-run in Q&A.

## admin-technical-abstract (required)
**Purpose:** The short written volume backing the scored non-demo criteria.
**Structure:** exec summary → company viability / bona fides → team & management → ROM & pricing structure → schedule & milestone exits → data rights & licensing → classified-work approach → OCI & foreign-national disclosure.
**Pitfall:** IL/ATO claims evidence-cited (IATT ≠ ATO); GPR posture stated on harness/methodology.

## rom-and-schedule (required)
**Purpose:** The scored ROM and notional schedule (within the OTA/PoP cap).
**Reference:** `reference/pricing-artifacts/rom.md`.
**Structure:** ROM range with a one-line basis of estimate → milestone/tier schedule with Government-observable exit criteria → follow-on production positioning (10 U.S.C. 4022(f)) where applicable.
**Hard rule (G5):** no placeholder value at any review. Fill a defensible range with a labeled assumption set on day one.

## requirements-crosswalk (required)
**Purpose:** Map every Invitation-Letter requirement and every scored criterion to where it is demonstrated across the artifacts.
**Structure:** table — Letter requirement → where addressed (artifact + slide/section/timestamp) → coverage (Full / Operational) → discriminator.
**Use:** hand this to the panel as a scoring reference; use it internally to find uncovered rows.

## operational-submission-items (optional / not scored content)
**Purpose:** Track the mechanics — company survey, US-citizen attendee roster, RSVP / 60-min window, Box upload, file naming.
**Structure:** checklist with owner + due date. Handled outside content but submission-blocking.

## Global rules
- **The demo is the proposal.** Concept selection is gated on what runs live by the record date (readiness gate G2), not on the best storyboard.
- **Answer the requirement, not the product.** Every artifact traces to the Letter's grading sentence.
- **Maturity honesty.** No `live`/`integrated` label without a reproducible artifact behind it (G2/G7). Overclaiming dies in 40 minutes of Q&A.
- **No blanks on scored fields** (G5). **No stand-ins** for claimed capability (G3). **No scored capability on an unconfirmed partner** (G4).
- Run the full readiness gate (`reference/pitch-demo-readiness-gate.md`) at Gold Team and again at export; open P0 rows block export.
