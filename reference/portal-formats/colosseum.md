# Colosseum (ONI / ONIX Marketplace) — Portal Conventions Sheet
**Scope note:** Colosseum is a **document-upload** portal (PDF attachments), **not** a character-limit
web form. Per this library's README it is technically out of the char-limit scope — this file is kept
as a **conventions sheet** for the recurring ONI/ONIX OTA marketplace, because the *conventions*
(separate ROM upload, no-CUI rule, AI-rubric scoring, ROM-minimum pricing, formatting-discretion)
repeat across challenges and are worth inheriting. It defines **no character limits** — the format
authority is the solicitation's page limit + required-content list.

**Platform:** gocolosseum.org, operated by One Nation Innovation (ONI). Award vehicle: ONIX OTA in coordination with ACC-RI.
**Seen on:** AFRICOM Joint Warfighter Innovation Challenge (May 2026); DIA DMA Frontier-Class LLM Challenge (Jul 2026).
**Last verified against live portal:** 2026-07-21 (DIA DMA submit page).

---

## Submission form — upload slots (.pdf only)
| Slot | Typical requirement | Notes |
|---|---|---|
| Cover Page | Optional | Title / POC / classification marking; can also live on the Proposal's first page |
| **Proposal** | **Required** | Full technical response + any mandated 1-pagers (Company/POC, Past Performance) |
| **ROM (Rough Order of Magnitude)** | **Required** (when the challenge asks for cost) | **Separate upload — do NOT fold ROM into the Proposal PDF.** Standalone pricing artifact. |
| Supplemental Materials | Optional | Graphics/figures/extra artifacts |

- **File format:** `.pdf` only. Submit enables once required slots are filled.
- **No portal metadata fields** (no title/TRL/keyword/system-type inputs).
- **No character/word limits.** Page limits (typ. "short response 2–10 pp" + separate 1-pagers) come from the solicitation and are honor-system, not portal-enforced.

## ⛔ NO CUI (hard rule)
Portal notice: *"DO NOT upload documents or video containing CUI. If you must include CUI … contact
info@gocolosseum.org."* All uploads must be **UNCLASSIFIED / non-CUI**. Run a CUI scrub before upload.
(This is a public platform — separate concern from a bidder's internal tooling compliance.)

## Scoring & formatting conventions
- **ONI scores with AI-powered rubric tools + SME review.** Write for the scanner: give **each rubric
  criterion an explicit labeled heading or a visible mapping-table row** so the AI tool locates every
  scored item. Explicit criterion-mapping beats dense prose.
- The portal exposes a **Rubric tab** with weighted criteria — capture it; it is the compliance spine.
- Formatting is respondent's discretion (ONI: listed standards are "merely a suggestion"; they forward
  submissions to the government regardless of formatting compliance). Standard 12pt / 1" / single-space is fine.
- OTA pathway: **no** FAR certs/reps, **no** consortium membership, **no** quad chart, **no** orals (unless a specific challenge asks).

## Pricing convention
- **ROM minimum** — rough order of magnitude by milestone with a milestone/payment schedule and 2–3
  stated assumptions. No FAR cost volume, no BOEs, no fringe/overhead rates. Delivered as the separate ROM PDF.

## Typical required-content checklist (varies per challenge — confirm on the Rubric tab)
Period of Performance · Applicable Documents · Technical Approach · Deliverables · Schedule w/
Milestones · Payment Schedule · Patents/Data Rights · Costs by Milestone/ROM · Company/POC 1-pager · Past Performance 1-pager.

## Timeline convention
ONI runs a fast OTA machine — "rapid down-select within 30–45 days of posting" is typical language; SABRE
executed one RFI-to-award in 40 days. Deadlines are sometimes vague in the challenge PDF — **confirm the
exact due date/time in-portal.**

## Pitfalls (learned)
- **ROM belongs in its own upload** (DIA DMA). Folding it into the Proposal (as africom-jwic initially planned) leaves the required ROM slot empty.
- **Page-limit ambiguity:** "2–10 pages including technical concept" + separate 1-pagers → treat the 2–10 as the technical concept; 1-pagers are additional pages in the Proposal PDF. Not enforced, but respect it.
- **CUI scrub is easy to forget** on reused past-performance/deployment text — gate it before export.
