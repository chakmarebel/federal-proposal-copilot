# Conventions — SBIR / STTR / Direct-to-Phase-II

Calibrated structural and stylistic norms for SBIR proposals (Phase I, Phase II, Direct-to-Phase-II) and STTR. Companion to [`reference/section-patterns/sbir.md`](../section-patterns/sbir.md), [`reference/graphic-templates/pitch-deck-conventions.md`](../graphic-templates/pitch-deck-conventions.md), and [`reference/pricing-artifacts/sbir-budget.md`](../pricing-artifacts/sbir-budget.md).

**Calibration source:** Direct-to-Phase-II SBIR (AFWERX/BESPIN) — 15-page technical volume + 15-slide pitch deck + 4-sheet milestone-payment workbook, 2026-04-25. No source content reproduced; only abstracted patterns.

---

## 1. Heading conventions

### Numbering depth

- **Depth 3 maximum.** Most subsections live at depth 2 (4.1) or depth 3 (4.4.1). Depth 4 is rare and a Pink-team finding for SBIR (FAR full proposals tolerate depth 4; SBIR does not — 15-25 pages doesn't earn it).
- **Section numbering tracks the topic structure** — `4 Technical Approach`, `4.1 Objective`, `4.4.1 Task 1`, etc. The numbering should mirror the topic description's structure where possible.
- **Bracketed solicitation references are NOT used in SBIR** the way they are in FAR full proposals. SBIR topic structure IS the response structure; bracketed `[Topic 3.1]` references are redundant.

### Title-case discipline

- Section headings use **Title Case with em-dash separators**: `4.4.1 Task 1 — Discovery and Planning`
- Em-dashes (—) preferred over hyphens (-) for the title separator
- All-caps reserved for cover-page elements and table header rows only

### Section-heading naming

Calibrated patterns:
- `Phase II Technical Objectives` (not "Technical Objectives" alone — the "Phase II" qualifier matters for SBIR scoring)
- `Task N — [Active Verb-Noun Phrase]` (e.g., "Task 1 — Discovery and Planning", "Task 4 — Operational Deployment")
- `Related Work` (not "Past Performance" — SBIR convention)
- `Capabilities` (not "Technical Capabilities" or "Architecture")
- `Appendix [Letter] — Resume [Name], [Role]`

---

## 2. Document structure norms

### Page allocation (Direct-to-Phase-II, 15-page calibration)

| Element | Pages | % | Notes |
|---|---|---|---|
| Cover | 1 | 7% | Plain text-heavy cover, no decoration |
| TOC | 0-1 | 0-7% | Often omitted for ≤15 page volumes; required for >20 page |
| Section 1-3 (front, intro, abstract) | 0-1 | 0-7% | Sometimes folded into Objective/Background |
| Objective + Scope + Background | 1-2 | 7-13% | Concise framing |
| Phase II Technical Objectives | 0.5 | 3% | Numbered list, half-page |
| Task / Technical Requirements | 4-6 | 30-40% | The structural heart — 1-2 pages per Task with subtask table |
| Deliverables | 0.5 | 3% | Bullet list |
| Related Work | 1-2 | 7-13% | 2-4 project narratives |
| Capabilities (optional) | 1-2 | 7-13% | When page budget allows |
| Resume Appendices | 2-4 | 13-25% | 1-2 pages per key personnel |

For traditional Phase II (25-40 pp), expand Tasks to 8-12 pages and Resumes to 4-6 pages. Keep front-matter / cover / Objective stable.

### Cover page conventions

**SBIR covers are intentionally plain.** Calibrated structure:

```
┌──────────────────────────────────────────────────┐
│                                                  │
│              Proposal for SBIR [NN.N]            │
│       Program Broad Agency Announcement (BAA)    │
│                                                  │
│             Direct to Phase II Open Topic:       │
│       [Topic title — descriptive]                │
│              (Topic # AFXXX-XXXX)                │
│                                                  │
│                       for                        │
│  DEPARTMENT OF DEFENSE SMALL BUSINESS            │
│  INNOVATION RESEARCH (SBIR) PROGRAM              │
│                                                  │
│                                                  │
│   Prepared for:           Prepared by:           │
│                                                  │
│   [POC Name]              [COMPANY NAME — brand] │
│   [Customer Org]                                 │
│   [Phone]                 [Address]              │
│   [Email]                 [Phone]                │
│                                                  │
│                           Contact: [Name, Role]  │
│                           [phone, email]         │
│                                                  │
│                           CAGE Code: XXXXX       │
│                           DUNS: NNNNNNNNN        │
│                           SBA SID: XXXXXXXXX     │
│                                                  │
│                                                  │
│   Volume II – Technical Volume                   │
│   Proposal Number: AFXXX-DXXX                    │
│   [Date]                                         │
│                                                  │
│   This proposal includes data that shall not be  │
│   disclosed... [distribution restriction —       │
│   small italic, 7-8pt, 1-3 lines]                │
└──────────────────────────────────────────────────┘
```

**Style rules:**
- White background (no brand color fill)
- Black text throughout, brand color reserved for company name only
- Logo placement: right side, under "Prepared by" — modest, not hero
- No decorative geometric patterns, no photos
- Generous whitespace
- Topic identification (number + title) is the most prominent text after the title block

### Header / footer strip (lighter than FAR)

**Header strip** (every body page, top):
- Left: small company logo (wordmark or mark)
- Center: `TOPIC # AFXXX-XXXX – DIRECT TO PHASE 2 OPEN TOPIC` (small caps, ~9pt)
- Center-below: `PROPOSAL NUMBER: AFXXX-DXXX` (small caps, ~9pt)
- Right: `SBIR [NN.N]` (small caps, ~9pt)
- Thin red rule below

**Footer strip** (every body page, bottom):
- Left: page number (single digit, no "Page" prefix)
- Right: `Volume II – Technical Volume / [Date]`
- Bottom: distribution restriction (italic, ~7pt, 1 line)
- Thin rule above

The header/footer is **lighter** than FAR full proposals — narrower vertical span, less branding, focused on identification. Typical SBIR aesthetic: "we're here to communicate the technical content; the wrapper should disappear."

---

## 3. Writing style norms

### Sentence length

Calibrated norms:
- **Mean sentence length:** 22-26 words (slightly tighter than FAR full at 22-28)
- **Median:** 20-24 words
- **p90:** ≤42 words
- **Maximum:** 60-70 words; >80 is Pink-team flag

### Paragraph length

- **3-5 sentences typical** (slightly shorter than FAR full proposals)
- Single-sentence paragraphs OK for transitions

### Bullet density

- **2-4 bullets/page** average across body sections
- Higher density (5-10 bullets/page) appropriate for Deliverables section, Tasks where subtasks list themselves, and Resume sections
- Tables (subtask tables) are dense and allowed to break the bullet-density norm

### Figure density

- **0.4-0.7 figures/page** (lower than FAR full at 1-2/page)
- SBIR is a **text-and-table-dense** format — graphics support the narrative but don't dominate
- When graphics appear, they are typically architecture diagrams, workflow flows, or framework illustrations — not capability tiles or ecosystem maps (those go in the pitch deck instead)

### Customer-language adoption

Same discipline as FAR full proposals — **use the topic description's exact terminology.** SBIR topics are written by program managers who care about specific phrases; using their phrases verbatim signals topic alignment.

If the topic uses "innovative defense-related dual-purpose technologies/solutions," your proposal uses that exact phrase. Don't compress to "dual-use defense tech."

### Voice

- **Active voice for company commitments:** "[Company] will deliver..." not "Deliverables will be provided by..."
- **First-person plural ("we") is fine** when discussing approach or methodology
- **No future-tense hedging** ("could," "may") — definite "will" for commitments

---

## 4. SBIR-specific structural elements

### Subtask × Delivery × Deliverable × Acceptance Criteria table

The single most distinctive SBIR Phase II structural element. Every `Task N` subsection has a 5-column table of this format. See [`reference/section-patterns/sbir.md`](../section-patterns/sbir.md) §"task-technical-requirements" for the canonical template.

**Calibration norms:**
- 3-7 subtasks per task (4-5 typical)
- Delivery in "Award + N months" or "Award + N-N months" format
- Acceptance criteria are concrete and testable, not "government approval"
- Bullets in cells use ▶ chevron markers

### Deliverables section pattern

A separate section (typical depth-1: `5 Deliverables`) listing what Phase II ships, mixing SBIR-mandated (Final Report, Quarterly Status Reports, Status Reports, Small Business Online Success Stories) with topic-specific deliverables. Bullet format, 5-10 bullets typical.

### Related Work as Phase-I substitute (D2P2 only)

Direct-to-Phase-II proposals must demonstrate that prior commercial work substitutes for Phase I feasibility. The `Related Work` section carries this load with 2-4 project narratives, each:

- Heading with customer category in parenthetical: `6.1 [Project Name] (Commercial client)`
- 1-2 paragraphs of narrative
- Bulleted phase/methodology applied (Discovery and Ideation, Concepting, Planning, Agile Development, Deployment)

Mix of commercial and government clients is high-yield for commercialization-potential scoring.

### Resume Appendix structure

Required for D2P2; recommended for traditional Phase II.

Per-resume structure (1-2 pages):
1. Section header: `Appendix [Letter] — Resume [Name], [Role]`
2. SUMMARY OF QUALIFICATIONS — 3-5 chevron-bulleted statements
3. TECHNOLOGY EXPERTISE — 2-column categorized table
4. EMPLOYMENT HISTORY — chronological reverse, role-by-role with bulleted accomplishments
5. EDUCATION — 1-line degree entries

---

## 5. Cross-volume coordination (SBIR multi-volume submissions)

SBIR submissions typically include multiple volumes:
- Volume 1 — Cost Volume (separate workbook, see [`reference/pricing-artifacts/sbir-budget.md`](../pricing-artifacts/sbir-budget.md))
- Volume 2 — Technical Volume (covered by these conventions)
- Volume 3 — Company Commercialization Report (separate format, agency-specific)
- Volume 4 — Supporting Documents (varies)
- Volume 5 — Pitch Deck / Quad Chart (covered by [`reference/graphic-templates/pitch-deck-conventions.md`](../graphic-templates/pitch-deck-conventions.md))

**Cross-volume consistency:**
- The technical objectives in Volume 2 must match the milestone payments in Volume 1 (cost) — every objective ties to a milestone
- The pitch deck (Volume 5) summarizes the technical volume — same task structure, same key personnel, same commercialization story
- The pitch deck addresses evaluation criteria explicitly (Criteria A: technical merit, Criteria B: ability to accomplish + commercialize, Criteria C: commercialization potential) — see pitch-deck conventions

---

## 6. Compliance traceability

SBIR has weaker formal compliance traceability than FAR Section L/M:

- **No Section L/M structure to mirror.** The topic description IS the requirements doc.
- **Compliance matrix is optional** but useful when topic descriptions are long. Map each topic-stated requirement to a Task or subtask in the technical volume.
- **Topic alignment matters more than formal compliance:** evaluators score "does this proposal directly address the topic's stated needs" — read the topic carefully, mirror its structure and vocabulary.

---

## 7. Pink-team checklist (SBIR-calibrated)

Augments the existing checks in `red-team-review`:

- [ ] Topic number and title appear on the cover and in the header strip
- [ ] Heading numbering tracks topic structure (4.1 / 4.4.1 etc.)
- [ ] Every Task has a 5-column Subtask × Delivery × Deliverable × Acceptance Criteria table
- [ ] Acceptance criteria are concrete and testable (not "government approval")
- [ ] Deliverables section explicitly lists SBIR-mandated reports + topic-specific
- [ ] Related Work section has 2-4 project narratives with customer category tags
- [ ] At least one commercial client appears in Related Work (commercialization potential)
- [ ] Key personnel resumes (Appendix) are 1-2 pages each, with chevron-bulleted qualifications
- [ ] Mean sentence length 22-26 words
- [ ] Cover page is plain (white background, no decorative pattern, brand color on company name only)
- [ ] Header/footer strip is identical on every body page
- [ ] Page count within topic-stated range (verify against topic description)
- [ ] Pitch deck (Volume 5) addresses Criteria A/B/C explicitly
- [ ] Cost volume milestones match technical objectives in Volume 2

---

## 8. Calibration changelog

| Date | Source | Pages | Changes triggered |
|---|---|---|---|
| 2026-04-25 | Direct-to-Phase-II SBIR (AFWERX/BESPIN) | 15 + 15 slides + 4-sheet xlsx | Established this convention library: D2P2 variant separation, calibrated cover-page conventions (plain, text-heavy), header/footer strip pattern, 5-column subtask table format, customer-category-tagged Related Work, 2-page resume appendix structure, sentence-length norms, figure-density calibration (0.4-0.7/page vs FAR's 1-2/page) |
