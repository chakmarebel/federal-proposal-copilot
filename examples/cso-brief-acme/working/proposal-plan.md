# Proposal Plan — CSO-JED-25-GenAI-01

**Produced by:** `/proposal-manager`
**Date:** 2026-04-22

## Opportunity Classification
- **Type:** CSO Solution Brief (Phase 1)
- **Evaluation approach:** Best-value concept competition against named Areas of Interest (AoI-1 through AoI-4)
- **Competition:** Multiple awards expected; selected vendors invited to Phase 2
- **Contract type:** No Phase 1 award; Phase 2 anticipated as commercial-item agreement
- **Incumbent:** None

## Response Requirements

| Element | Source | Limit |
|---|---|---|
| Cover page | CSO-JED-25-GenAI-01 §Submission | Required |
| Executive summary | CSO §Submission | 1 page |
| Technical approach | CSO §Submission | 3-5 pages |
| Deployment path | CSO §Submission | 1-2 pages |
| ROM | CSO §Submission | 1-2 pages |
| Commercial-item justification | CSO §Submission | 0.5-1 page |
| **Total page limit** | | **10 pages** |
| Font size | CSO §Submission | 12-point min |

## Evaluation Criteria (from CSO §Evaluation Criteria, in order of importance)

| # | Factor | Weight | Our Strength |
|---|---|---|---|
| 1 | Commercial Maturity | Most Important | **STRONG** — 14-month DDIL deployment at [redacted DoD customer] |
| 2 | Coverage of AoI-1 through AoI-4 | 2nd | **STRONG** on AoI-1, -2, -3; **MODERATE** on AoI-4 (IL5 path, not complete) |
| 3 | Path to Deployment | 3rd | **STRONG** — 90-day IOC commitment |
| 4 | Affordability | 4th | **MODERATE** — premium vs. "cloud-retrofit" competitors, but justified |
| 5 | Commercial-Item Basis | 5th (gate) | **STRONG** — $4M ARR commercial, non-govt customers |

## Areas of Interest Coverage

| AoI | Coverage | Evidence |
|---|---|---|
| AoI-1 On-Device Inference | Direct | Deployed inference engine operates on ruggedized Intel NUC / Dell Latitude Rugged |
| AoI-2 Disconnected Operation | Direct | 14-month zero-connectivity deployment at [customer]; auto-resync on reconnection |
| AoI-3 Model Specialization | Direct | LoRA adapter pipeline, 60-day adapter delivery for prior mission sets |
| AoI-4 Security Posture | Partial | FedRAMP Moderate in progress; IL5 assessment roadmap defined, 18-month path |

## Win Themes (defined here, reinforced in every major section)

1. **"Disconnected is the default, not an edge case."** Our platform was designed for DDIL from day one; it is not a cloud-native system with edge retrofitted. (Ghosting opportunity: known competitors are cloud-retrofits.)

2. **"Commercial today, mission-ready tomorrow."** Validated by paying commercial customers; mission specialization path is proven, not promised.

3. **"Operational within the quarter."** 90 days from award to first operational capability, on hardware JED already fields.

## Discriminators (each requires a proof point per Pattern 2)

| Discriminator | Proof Point | Evidence Type |
|---|---|---|
| Proven DDIL deployment | 14-month continuous operation at [redacted DoD customer], zero cloud dependency | Deployed customer reference |
| On-device fine-tuning | LoRA adapter pipeline delivering specialized adapters in 60 days for prior mission sets | Internal benchmark + customer delivery |
| Three-program DARPA continuity | PI led MS3, CCU, and Assured Autonomy in adjacent topics | Named key personnel with specific credentials |
| Commercial revenue base | $4M ARR across non-government customers; not a research-funded startup | Commercial sales history |

## Ghosting Targets

Known likely competitors in this CSO (from market intel, not formal competitor-assessment — skipped for `cso-brief` type):

- **Competitor pattern: "Cloud-retrofit"** — major cloud providers offering edge inference that requires periodic re-sync. **Ghost:** frame our architecture as disconnected-by-design, not disconnected-capable.
- **Competitor pattern: "Research startup with TRL-4 claims"** — demo-ware without commercial deployment. **Ghost:** emphasize commercial revenue, deployed customer, commercial-item status.

Rules: never name a competitor; use generic category framings ("cloud-retrofit solutions," "research-grade approaches").

## Recommended Proposal Structure

1. **Cover page**
2. **Executive Summary** (1 page) — applies all 4 winning patterns
3. **Technical Approach** (3 pages) — on-device inference architecture, disconnected operation, adapter path, IL5 posture
4. **Deployment Path** (1.5 pages) — 90-day IOC, hardware, integration
5. **ROM** (1.5 pages) — range, assumptions, validity (per `reference/pricing-artifacts/rom.md`)
6. **Commercial-Item Justification** (1 page) — FAR 2.101 basis, commercial sales evidence
7. **Graphics:** one figure (system architecture) with action caption

## Bid/No-Bid Assessment

**GO.** Strong alignment with JED hot buttons. Proven commercial deployment. Path to IL5 is the weakest element but has a credible roadmap. Phase 1 cost is time only (no funding at this stage).

## Open Questions / Assumptions

- Assumption: JED's "ruggedized edge hardware" includes Intel NUC-class devices (our validated target). If they require more constrained hardware (e.g., handhelds), we need clarification.
- Assumption: 10-page limit excludes cover page. Will confirm in Q&A if offered.
- Open: unclear whether prior CLS work counts as AoI-3 evidence without renaming.
