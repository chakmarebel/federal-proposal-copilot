# Pitch + Demo Readiness Gate

**Applies to:** `type_id: pitch-demo` (CSO/OTA Phase-2 pitch + live/recorded demonstration).
**Origin:** Generalized from the MYSTIC DEPOT Phase II loss analysis (`proposals/mystic-depot/reviews/lessons-learned-mystic-depot.md`, 2026-07). Its reason for existing: a differentiated *concept* whose decisive moments are captured/roadmap rather than built-and-live loses to a plainer capability shown working. This gate makes that failure mode hard to ship.

**Consumed by three skills** (see `reference/proposal-types/pitch-demo.md`):
- `/technical-review --phase=approach` → run **G1–G5** on the storyboard, before graphics/video production.
- `/red-team-review` (Gold) → run the **full gate** on the finished package.
- `/export-proposal` → **any open P0 row is export-blocking.**

**How to run it:** for each row, record `PASS` / `FAIL` / `N/A` with a one-line evidence pointer (slide #, video timestamp, artifact path, or the owner+date of a written confirmation). Write results to `reviews/pitch-demo-readiness-gate.md` in the proposal. A `FAIL` on a **P0** row is not a to-do — it means the concept, the claim, or the maturity label changes before the package moves forward.

---

## The gate

| # | Gate | Priority | PASS means | Failure signature it catches |
|---|---|---|---|---|
| G1 | The exact published grading sentence is extracted, and every demo beat maps to a scored criterion | P0 | A rubric-to-beat map exists; no orphan beats; no scored row without a beat | Demoing the product instead of answering the requirement |
| G2 | Every scored capability is **LIVE or CAPTURED-reproducible AND staged to re-run under Q&A** by a hard date ≥5 business days before record/submission | P0 | Demonstrated on the machine, not described on a slide | "INTEGRATED — LIVE" labels over unbuilt seeds |
| G3 | Every headline claim's demo makes the evaluator's read-back sentence literally true — no stand-ins | P0 | The claim wording == what actually runs | Auditing an abstract agent while claiming to audit a *fielded* system |
| G4 | No scored capability depends on an un-integrated or unconfirmed partner | P0 | Each scored capability has a written owner + `works today / integrated by [date] / roadmap` status | High-value rows parked on a partner's roadmap; pending OCI/teaming confirmations |
| G5 | Every scored admin field (ROM, schedule, data rights/licensing, classified-work posture, OCI, foreign-national) has a non-blank, defensible value | P0 | Zero placeholders on any scored field before the *first* internal review | A `$[X.X]M` ROM or `[confirm terms]` license carried into review |
| G6 | The signature differentiator has concrete, early, live-or-captured proof | P1 | Shown running, not asserted | The one claim only we can make left on the roadmap slide |
| G7 | The mock evaluation is re-run on the **final** package; every maturity-label improvement is backed by a named artifact | P1 | Final self-assessment is at least as harsh as the first honest one, unless real work closed the gap | Optimism drift ("Acceptable" → "Outstanding" with nothing built in between) |
| G8 | An adversarial Q&A murder-board has been held; every `captured` claim has a staged live re-run rehearsed | P1 | Hostile technical questions war-gamed live, not just documented | Captured money-moments that die when an SME asks "run it now" |
| G9 | Teaming and OCI confirmations are received **in writing** before the deck locks | P1 | Signed/emailed confirmations on file | Soft-framed "pending subcontractor confirmation" at submission |
| G10 | **Every line of effort / scored technical dimension** in the solicitation has demonstrated coverage | P0 | Each LOE (e.g., LOE1 harness AND LOE2 methodology) maps to ≥1 demonstrated beat; no whole line left as roadmap | Demoing one LOE and skipping the other (Mystic Depot: LOE2 methodology barely shown) |
| G11 | The talk is **rehearsed end-to-end to the hard time limit with a buffer**, and required/scored content is **front-loaded** | P0 | Timed run-through fits the limit with margin; disclosures, pricing, and follow-on are not stacked in the final slides | Running long on the demo and never presenting the last 2–3 slides — where OCI (§VI) and follow-on (§VIII) lived |

---

## Maturity vocabulary (use verbatim on every capability callout)
`integrated / live` · `captured-reproducible` · `partially implemented` · `on the roadmap`.
A capability may be labeled `integrated`/`live` **only** when a reproducible artifact backs it (G2/G7). If the Invitation Letter mandates specific maturity vocabulary, that language wins.

## The one rule behind all nine
**Answer the requirement, and let the demo be the evidence for the answer.** The correction to a weak pitch is never "demo better" — it is "gate the concept on what runs live against the published criterion by the record date." See also project memory `feedback_bid_maturity_demo_vs_requirement`.
