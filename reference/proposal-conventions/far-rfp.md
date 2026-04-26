# Conventions — FAR-Based Full Proposals (Technical Volume)

Calibrated structural and stylistic norms for FAR Part 15 full proposals, IDIQ task orders, CSO full proposals, and BAA full proposals. Companion to [`reference/section-patterns/full-proposal.md`](../section-patterns/full-proposal.md).

**Calibration source:** Air Force IDIQ technical volume (52 pages), 2026-04-23. No source content reproduced; only abstracted patterns.

---

## 1. Heading conventions

### Numbering depth

- **4 levels of numeric headings is normal** for a 30-75 page technical volume. Most subsections live at depth 4 (e.g., 2.2.1.1).
- **Depth observed:** ~depth 2 (20%), depth 3 (10%), depth 4 (40%), non-numeric (30% — these are the major non-numbered sections like "Executive Summary" and TOC entries).
- **Cap at depth 4.** Depth 5 (e.g., 2.2.1.1.1) loses readability and is a Pink-team finding.

### Bracketed solicitation references

Every body-section heading carries a bracketed reference to its solicitation source. **This is the single most important traceability discipline in winning federal full proposals.**

Pattern: `<our-section-#> <Title> [<Solicitation Reference>]`

Examples (generic):
```
2.2.1.1 [Topic] [PWS 2.1.1]
2.2.2 [Topic Area] [PWS 2.2]
6.3 Transition-In Plan [Section L.4.2]
```

### Heading-to-PWS mirroring

For solicitations that publish a PWS / SOO / SOW with numbered sections, the technical volume should mirror that hierarchy 1:1. If the PWS has 2.1.1 / 2.1.2 / 2.1.3, the technical volume responds with a corresponding 2.2.1.1 / 2.2.1.2 / 2.2.1.3 (offset by a leading "2." prefix for the volume's own section numbering).

This mirroring lets a Section M evaluator score by walking the solicitation top-to-bottom, finding each requirement directly in your headings.

### Title-case discipline

- All-caps for cover-page elements only (Volume title, "POINT OF CONTACT," distribution statement)
- Title Case for section headings ("Data Acquisition" not "Data acquisition" or "DATA ACQUISITION")
- Sentence case acceptable for subheadings beneath depth 3 if the section calls for narrative flow

---

## 2. Document structure norms

### Page allocation

For a typical 50-page technical volume:

| Element | Page allocation | Notes |
|---|---|---|
| Cover + transmittal | 1-2 | Cover page, optional transmittal letter |
| TOC + acronym list | 1-2 | Detailed multi-level TOC with dot leaders |
| Front matter (figures, classification cover) | 2-4 | Cover graphic, distribution statement, classification cover sheet if applicable |
| **Front-matter total** | **~7-8 (12-15% of total)** | |
| Executive Summary | 3-4 | One section, 7-8% of total volume |
| Technical Approach intro + commitments | 1-2 | Five-Commitments opener (see section-patterns) |
| Technical Approach by PWS | 18-25 | Bulk of the volume; 1:1 with PWS |
| Service Summary / GFP / General Info | 3-5 | Section H content + admin |
| Past Performance | 4-6 | Per Section L instructions on PP volume |
| Management Approach | 4-6 | Org, communication, risk, QA, schedule |
| Path Forward / Conclusion | 1-2 | Brief close |

### TOC discipline

- Multi-level TOC with dot leaders (`...`) and right-aligned page numbers
- TOC depth matches body heading depth (typically depth 4)
- TOC entries match heading text exactly — including bracketed solicitation references
- Optional: separate **List of Figures** and **List of Tables** entries on the TOC page

---

## 3. Writing style norms

### Sentence length

Federal full-proposal style is **dense, technically grounded, comma-heavy**. Calibrated norms:

- **Mean sentence length:** 22-28 words
- **Median:** 22-26 words
- **p90:** ≤45 words
- **Maximum:** 60-70 words; anything above 80 is Pink-team flag

Do **not** compress to 15-word "punchy" prose. Federal evaluators expect technical density.

### Paragraph length

- **3-6 sentences typical.** Single-sentence paragraphs are appropriate for transitions and theme statements.
- **8+ sentence paragraphs** flag for splitting — likely covers more than one idea.

### Bullet density

- **2-6 bullets/page** average across body sections
- **Bullet-heavy concentration** (10+ bullets/page) is appropriate for management/admin sections (Section 6 General Information) and lists of commitments
- **Avoid** bullets in narrative paragraphs — federal style uses prose with comma-separated lists, not nested bulleting

### Figure density

- **1-2 figures per body page** average
- **Front-matter pages** can carry 5-15 figures (cover graphics, brand elements, classification covers)
- **Every figure has at least one in-text reference** ("see Figure 3"); orphaned figures are a Pink-team finding
- Figure captions follow the action-caption pattern (see `reference/proposal-writing-patterns.md` Pattern 3)

### Graphics conventions (illustrator-grade)

A separate convention library distills layout, typography, color-palette, and complexity norms calibrated against winning proposals produced by professional proposal-design illustrators. **Every graphic in a FAR full proposal should match one of the 7 patterns documented there**, not be invented ad-hoc.

See [`reference/graphic-templates/illustrator-conventions.md`](../graphic-templates/illustrator-conventions.md) for:

- Page-level layout taxonomy (cover, TOC, body single-column, body+sidebar, body+figure, compliance-table)
- Mandatory header/footer strips (identical on every body page)
- Typography hierarchy with calibrated size ratios
- 5-role color palette structure (primary, accent, secondary, tile-palette, light-fill)
- 7-pattern graphic taxonomy (3-tier band, callout sidebar, N-column capability tiles, hub-and-spoke, maturity curve, compliance table, process flow)
- Icon usage discipline
- Element-density norms per page type
- "Lead-in label" in-body pattern (bold accent-color label + colon + body text — substitutes for fine-grained sub-headings)
- Pink-team checklist additions for graphics review

### Customer-language adoption

**The single highest-leverage writing discipline.** Use the customer's own framework terminology consistently — do not invent synonyms.

- If the solicitation defines a 7-attribute data framework with specific terms (e.g., "Visible / Accessible / Understandable / Linked / Trusted / Interoperable / Secure"), use those exact terms verbatim, in headings and prose, repeatedly.
- If the solicitation uses "Subject Matter Experts (SMEs)," do not use "experts" or "specialists" or "personnel" — use "SMEs."
- If the solicitation uses a specific verb ("operationalize," "instantiate," "harmonize"), pick it up.
- Adopting the customer's vocabulary signals that the offeror has read the solicitation carefully AND aligns culturally. Inventing synonyms signals the opposite.

Calibrated observation: in a 26,000-word winning technical volume, the customer's seven framework terms each appeared 50-58 times. The writer maintained vocabulary discipline at the section, paragraph, and sentence level.

### Voice

- **Active voice for offeror commitments:** "[Company] will deliver..." not "Deliverables will be provided by..."
- **Passive voice acceptable for descriptions of conditions/requirements:** "Where data is unclassified, ..."
- **First-person plural ("we") is fine** when the offeror is the subject; avoid "we" in third-person descriptions of architectures or processes
- **No future-tense hedging** ("could," "may," "might"); use definite "will" for commitments

---

## 4. Compliance traceability

### Section L / Section M crosswalks

Calibration shows winning proposals carry **two complementary compliance disciplines**:

1. **Heading-level traceability:** every body section heading carries `[PWS X.Y.Z]` or `[Section L.X]` or `[Section M Factor X]`
2. **Compliance-matrix traceability:** a separate compliance matrix (often in the cost volume appendix or as a standalone deliverable) maps every "shall" in the solicitation to a section/page in the proposal

The framework's `working/compliance-matrix.json` (Phase A sidecar) should produce both views — one as a heading-cross-check, one as the formal matrix.

### Section M scoring alignment

Section M evaluators score by factor and subfactor. Calibration suggests:

- **Reorder volume sections to match Section M factor order** if it differs from PWS order
- **Where a single response section addresses multiple Section M factors,** call them out explicitly in the heading bracket: `[PWS 2.1; Section M Factor 1.A]`
- **Any section that doesn't help Section M scoring is filler** — cut or move to an appendix

---

## 5. Five-Commitment opener (Technical Approach introduction)

Calibrated as a high-yield pattern: open Section 2 (Technical Approach) with a numbered list of 4-6 commitments before diving into PWS-by-PWS detail. See [`reference/section-patterns/full-proposal.md`](../section-patterns/full-proposal.md) §"Technical Approach Introduction Pattern" for the full template.

Calibration data: 5 commitments typical, each ~2-3 sentences, each tying back to a PWS area or evaluation factor.

---

## 6. Cross-volume coordination (multi-volume proposals)

For FAR full proposals with multiple volumes (Tech / Mgmt / PP / Cost):

- **Theme statements repeat across volumes** without redundancy — same theme stated through each volume's lens (technical theme → management theme → past-performance theme → cost theme)
- **Discriminators get cited 1-2 times per volume** — over-citing the same proof point dilutes; under-citing leaves it on the table
- **Past performance references must align with what the technical volume claims** — if Tech Vol claims a deployment, PP Vol must back it with a contract reference
- **Cost volume narrative should reference the technical volume by section** — "Per Tech Vol §2.2.1.1, [Company] will..."

---

## 7. Word-frequency calibration

A useful sanity check: top content words should reflect customer terminology, not company marketing terms.

Calibration sample (Air Force IDIQ technical volume, ~26,000 body words):
- Top customer-domain term appeared **868 times** (a generic noun central to the program — "data" in this case)
- Top company-name appeared **298 times** (offeror's brand)
- Common process noun appeared **163 times** ("approach")
- Customer organization abbreviation **134 times** ("USAF")

The pattern: **customer terminology should dominate, offeror brand should be present but not loudest.** A volume where the offeror brand is the top word is over-marketing.

---

## 8. Pink-team checklist (calibrated)

Augments the existing `reference/evaluator-rubrics/` and Pink-team checks in `red-team-review`:

- [ ] Every body-section heading has a bracketed solicitation reference
- [ ] Heading hierarchy mirrors PWS hierarchy (or Section L instructions)
- [ ] TOC matches body headings exactly
- [ ] Mean sentence length in body sections is 22-28 words (use `scripts/extract-pdf-patterns.py` post-export to verify)
- [ ] Customer's framework terminology used verbatim, consistently
- [ ] Every figure has an in-text reference
- [ ] No orphan headings (depth 5) or single-subsection sections (one-child syndrome)
- [ ] Front-matter ≤ 15% of total page count
- [ ] Five-Commitment opener present at start of Technical Approach (or equivalent)
- [ ] Section H / General Information present if solicitation requires
- [ ] Conclusion ≤ 2 pages

---

## Calibration changelog

| Date | Source | Pages | Changes triggered |
|---|---|---|---|
| 2026-04-23 | Air Force IDIQ technical volume | 52 | Added bracketed-PWS heading convention, calibrated sentence-length norms, added General Information / Section H pattern, codified Five-Commitment opener, established customer-language adoption discipline |
