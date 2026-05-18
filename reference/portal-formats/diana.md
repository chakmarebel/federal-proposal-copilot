# DIANA Portal Format Reference
**Source:** `diana-proposal-instructions.docx` (DIANA portal, captured post-registration 2026-04-23)
**Portal platform:** DIANA challenge platform (NATO Defence Innovation Accelerator)
**Applies to:** DIANA open challenges — Short Form (initial) + Long Form (invited)
**Last verified against live portal:** 2026-04-23 (example submission, Decision Superiority for NATO Warfighters)

---

## Portal Metadata (required fields at submission)

| Field | Type | Limit / Enum | Notes |
|---|---|---|---|
| Proposal Title | text | ≤200 chars | Used as the primary identifier throughout the review process |
| TRL Level | select | 1–9 | Match to actual product maturity; evaluators weight TRL ≥6 heavily |
| System Type | select | {Hardware, Software, Both} | |
| System Level | select | {Component, Sub-System, System, Platform} | |
| Video | optional | .mp4, ≤4 min, ≤100 MB | Screen capture with audio narration strongly recommended |

---

## Sections and Limits

**Character limits include spaces and are enforced server-side at submission.** Client-side counters exist but don't always agree with the server; budget ~2% safety margin.

### Short Form — 4 sections, ~1,500 characters each

| Section ID | Portal Label | Char Limit | Instructions Summary |
|---|---|---|---|
| SF-1 | Technical Solution | ~1,500 | Describe what the solution does; highlight what is novel or unique |
| SF-2 | Technical Alignment | ~1,500 | Alignment with challenge statement, desired functional outcomes and exemplar effects; augmentation potential for AI-enabled warfighting platform |
| SF-3 | Integration | ~1,500 | Justify TRL 7+; describe third-party integration support (APIs, connectors); reference previous/in-progress integrations |
| SF-4 | Defence Use Case | ~1,500 | Defence use case in context of challenge statement; extent of validation/testing |

### Long Form — 5 sections, hard char limits

| Section ID | Portal Label | Char Limit | ~Words |
|---|---|---|---|
| LF-1 | Abstract | 750 | ~110 |
| LF-2 | Technical Merit | 12,000 | ~1,800 |
| LF-3 | Technical Suitability | 3,500 | ~525 |
| LF-4 | Defence and Security | 3,500 | ~525 |
| LF-5 | Company and Commercial | 3,500 | ~525 |

### Per-section detailed guidance

#### LF-1: Abstract (750 chars)
One-paragraph "elevator pitch." Should include: what the solution is, how it augments the AI-enabled warfighting platform, the discriminating novelty, and the deployment evidence (TRL + existing customers).

#### LF-2: Technical Merit (12,000 chars)
Must cover: (1) detailed solution description, (2) alignment with challenge statement with explicit mapping to exemplar effects being addressed, (3) articulation of novelty, (4) **comparison to existing state of the art and competitors**. The competitor-comparison requirement is easy to miss — it is required, not optional.

#### LF-3: Technical Suitability (3,500 chars)
Must cover: (1) how solution augments an AI-enabled warfighting platform, (2) TRL 7+ justification, (3) third-party integration support (APIs, connectors), (4) prior/ongoing integrations. Compress aggressively — this section often needs a 60–65% reduction from the natural narrative length.

#### LF-4: Defence and Security (3,500 chars)
Must cover: (1) defence use case within context of an AI-enabled warfighting platform, (2) tactical, operational, and strategic benefits of integration/deployment.

#### LF-5: Company and Commercial (3,500 chars)
Must cover **ALL** of:
- Financial status: revenue, investments, current runway
- Team and resources dedicated to integration/demonstration effort (name the technical lead)
- Risks to achieving integration/demonstration, and mitigations
- Ability to deliver to NATO customers under follow-on contracts
- **Addressable market segments (civilian and defence) beyond this challenge**
- **Commercialisation/exploitation plan**

Six required topics into 3,500 chars is the tightest section in the Long Form. Budget accordingly.

---

## Images and Attachments

- Short Form: up to 2 images
- Long Form: up to 3 images
- Content rule: diagrams/graphics only — no narrative text in images (don't try to bury overflow narrative in image captions)
- Video: optional, format/size limits above

---

## Formatting quirks

- Markdown: not supported in text fields — paste plain text. `**bold**` markers will appear literally as asterisks.
- Line breaks: preserved (one per paragraph is fine).
- Em-dashes and curly quotes: render correctly; count as 1 character each.
- HTML comments (`<!-- evidence: -->` markers): strip before pasting — they count against the character limit.
- Whitespace: preserved, not collapsed.

---

## Agreements and Declarations (required at submission)

- [ ] Terms & Conditions — read and agree (per §7.2(a))
- [ ] Company Identity Confirmation — signatory works for the submitting entity; entity would enter agreement with DIANA if selected
- [ ] Personnel Agreement — key personnel in Step 3 Virtual Panel will be directly involved and available for required travel

## Optional Opt-Outs (decisions required)

DIANA may share with NATO / Allied stakeholders — each is a strategic IP / BD decision:

- [ ] Bidder Identity sharing
- [ ] Bidder Documentation sharing

Flag both for a human decision before submission — defaults to share unless opted out.

---

## Submission Mechanics

- Save-and-resume: yes (draft state persists between sessions)
- Character counters: client-side live, but trust server-side enforcement at submit
- Preview before submit: yes
- Editable after submit: no — submit is final; re-entry requires DIANA admin intervention
- Confirmation: in-portal receipt + email

---

## Known pitfalls

- **Portal registration is required to see the actual format.** The public-facing challenge statement describes the opportunity but not the section structure, char limits, or metadata fields. Register first, capture the structure with `/capture-portal-structure`, then plan and draft.
- **LF-5 is the tightest.** Six required topics in 3,500 chars needs budget-first writing, not compression-after.
- **LF-2 requires competitor comparison.** A draft that skips this is non-responsive even if technically strong.
- **Paste plain text, not markdown.** The portal does not render markdown; asterisks will appear literally.
- **Strip HTML comments.** `<!-- evidence: EV-XXX -->` markers count toward the character limit if left in.

---

## Gap analysis pattern (when adapting a non-DIANA draft to DIANA)

Prior DIANA submissions have shown a consistent compression burden when drafts start from an open-ended narrative:

| Natural draft length | DIANA section | Compression needed |
|---|---|---|
| 8,000–10,000 chars | LF-3 Technical Suitability | 60–65% |
| 7,000–9,000 chars | LF-4 Defence and Security | 55–60% |
| 4,000–5,000 chars | LF-5 Company and Commercial | 30–40% + add commercialisation + addressable markets |

Lesson: for DIANA, budget-first drafting is cheaper than compression-after.
