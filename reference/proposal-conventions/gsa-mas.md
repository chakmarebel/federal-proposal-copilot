# Conventions — GSA MAS-Flighted Task Orders, BPAs, and Schedule Offerings

Calibrated structural and stylistic norms for proposals delivered under the GSA Multiple Award Schedule (MAS) program — including direct Schedule offerings, MAS-flighted multi-vendor BPAs, and task-order competitions issued by an agency under MAS.

**Calibration source:** NGA SABER II vehicle competition (multi-vendor BPA flighted under GSA MAS IT Category) — 4 artifacts (Vol 1 Technical 13pp + Vol 2 Price 2pp + Vol 3 Security 5pp + Vol IV Pricing Workbook xlsx), 2026-04-25.

Companion to:
- [`reference/section-patterns/gsa-mas-task-order.md`](../section-patterns/gsa-mas-task-order.md) — technical volume section structure
- [`reference/section-patterns/security-volume.md`](../section-patterns/security-volume.md) — security volume structure (reusable)
- [`reference/pricing-artifacts/gsa-mas-pricing.md`](../pricing-artifacts/gsa-mas-pricing.md) — price narrative + workbook structure

---

## 1. Three GSA MAS proposal scenarios

Different scenarios → different patterns. Identify which one applies before drafting.

### Scenario A: Direct GSA MAS Schedule offering

**What it is:** The original Schedule submission to GSA. Establishes labor categories, ceiling rates, terms, and conditions that an agency can later order against.

**Audience:** GSA Acquisition Center (not the end-user agency).

**Key artifacts:** SF 1449 forms, Schedule template proposal, commercial sales practices disclosure, labor category descriptions, ceiling rate justification.

**Patterns to apply:** Not yet calibrated — the framework does not currently ship a section_patterns id for direct Schedule offerings. When this becomes a priority, calibrate against an actual Schedule submission.

### Scenario B: MAS-flighted multi-vendor BPA / IDIQ competition (CALIBRATED)

**What it is:** An agency issues a competition limited to vendors holding a specific GSA MAS Schedule. Winners get a Blanket Purchase Agreement or IDIQ contract that the agency orders against later.

**Audience:** End-user agency contracting office + technical evaluators.

**Key artifacts:** Multi-volume submission (Technical, Price, Security), each as a standalone PDF + a pricing workbook xlsx attachment.

**Patterns to apply:**
- Technical volume → [`section-patterns/gsa-mas-task-order.md`](../section-patterns/gsa-mas-task-order.md)
- Price volume → [`pricing-artifacts/gsa-mas-pricing.md`](../pricing-artifacts/gsa-mas-pricing.md)
- Security volume → [`section-patterns/security-volume.md`](../section-patterns/security-volume.md)

### Scenario C: Task order under an existing GSA MAS BPA

**What it is:** Once a vendor wins a BPA (Scenario B), the agency issues task orders against that BPA. Each task order is a competition limited to BPA holders.

**Patterns to apply:** Same as Scenario B but typically shorter — page targets reduced ~30-50% because the BPA established the offeror's baseline qualifications. Sub-Factor 1.1 (Corporate Experience) becomes a brief "demonstrated under BPA" reference rather than a full coverage matrix.

---

## 2. Heading conventions

### Sub-Factor numbering carries verbatim

The solicitation's evaluation Sub-Factor numbering (typically 1.1, 1.2, 1.3 under Section M Factor 1) is **carried verbatim into the heading**. Do NOT renumber to your own scheme.

```
1. Sub-Factor 1.1 Corporate Experience       ← solicitation's "Sub-Factor 1.1" preserved exactly
2. Sub-Factor 1.2 Staffing Key Personnel
3. Sub-Factor 1.3 Approach in [Domain]
```

This is **lighter than FAR full-proposal bracketed-PWS-reference convention** (`[PWS X.Y.Z]`) — GSA MAS task-order Sub-Factors are built into the heading title itself rather than appended in brackets.

### Body subsections use ALL-CAPS non-numeric headings

Within Sub-Factor 1.2 (Staffing Key Personnel), each individual's resume is delimited by ALL-CAPS section headers naming the role (`PRINCIPAL SOFTWARE ENGINEER`, `PROJECT MANAGER`, etc.) rather than depth-3 numeric headings (`2.1.1`, `2.1.2`).

Rationale: numeric depth past 1.X.Y in a 13-page volume is over-engineering. The role-name headings provide structure without unnecessary numeric overhead.

### Header strip — letter-spaced acronym expansion

A distinctive GSA MAS task-order header pattern observed in the calibration source:

```
   [Logo]               RESPONSE TO RFQ #HM047620Q0028
                        S O F T W A R E   A Q U A   B A D G E   E N G I N E E R I N G   R E S O U R C E S
                        ─────────────────────────────────────────────────────────────────────────────
```

The program acronym (SABER, BESPIN, CDAO, etc.) is expanded into its letter-spaced full form on the second header line. Pattern: `S A B E R = "Software Aqua Badge Engineering Resources"` rendered with wide letter-spacing on every body page.

This is a strong evaluator-friendly convention — establishes program identity and reinforces customer-language adoption with every page view.

---

## 3. Document structure norms (Scenario B — calibrated)

### Volume sizing

| Volume | Pages | Notes |
|---|---|---|
| Vol 1 — Technical | 13-25 | The bulk of the work |
| Vol 2 — Price (narrative) | 2-3 | Very short — workbook carries the numbers |
| Vol 3 — Security | 5-8 | Standalone supplement |
| Vol IV — Price (workbook) | xlsx | Single sheet typically |
| Attachments | varies | DD 254, FCL Template, PCL Template-FOUO, other agency forms |

**Volume numbering:** Arabic for Vols 1-3; **Roman for Vol IV** to mark the pricing workbook as the definitive numerical artifact distinct from the price narrative.

### Technical volume internal allocation (13-page calibration)

| Section | Pages | % of vol |
|---|---|---|
| Cover | 1 | 8% |
| Sub-Factor 1.1 — Corporate Experience | 2 | 15% |
| Sub-Factor 1.2 — Staffing Key Personnel | 5-8 | 40-60% |
| Sub-Factor 1.3 — Approach | 2-3 | 15-23% |

Sub-Factor 1.2 dominates by page count — this is the section where named individuals and embedded resumes live.

---

## 4. Writing style norms

### Sentence length (per volume)

Calibrated norms differ by volume because each volume has a different rhetorical job:

| Volume | Mean | p90 | Notes |
|---|---|---|---|
| Technical | 22-28 words | ≤45 | Federal density, similar to FAR full proposals |
| Price (narrative) | 35-42 words | ≤90 | Long, formal contracting language is appropriate |
| Security | 28-32 words | ≤95 | Most formal voice in any federal proposal — declarations and commitments |

The technical volume calibration (mean 25.3 in source) matches FAR. The price and security volumes use longer sentences because they are **declarative compliance artifacts**, not narrative arguments.

### Bullet density

**Calibrated 11+ bullets/page average for technical volumes** — high. This is much denser than FAR full proposals (2-6/page) because GSA MAS task-order Sub-Factor responses are by-design list-of-claims documents, not prose-driven narratives.

For Sub-Factor 1.2 (Staffing Key Personnel) specifically, expect 15-25 bullets/page — resumes carry the load.

### Customer-language adoption

Same discipline as FAR full proposals — **use the solicitation's exact terminology**, especially for evaluation factor names, labor-category names, and program-specific acronyms.

The header strip's letter-spaced acronym expansion is a structural manifestation of this discipline (see §2 above).

### Inline emphasis

Calibrated examples use **bold inline emphasis** heavily within bullet text and resume content. Common emphasis targets:
- Technology / tool names ("**Java, JavaScript, and Python**")
- Methodology names ("**DevSecOps**, **TDD**, **CI/CD**")
- Past contract names ("**Air Force Kessel Run software factory**")
- Quantified outcomes ("**team of 12 engineers**", "**$30M dollar program**")

Pattern: 2-5 bolded phrases per bullet is normal. More than 8 starts to lose emphasis (everything bold = nothing bold).

---

## 5. Past Performance discipline (Sub-Factor 1.1)

The single most distinctive structural element of a GSA MAS task-order technical volume is the **Past Performance Coverage Matrix** — a row-per-program × column-per-evaluation-area table with checkmark cells.

See [`section-patterns/gsa-mas-task-order.md`](../section-patterns/gsa-mas-task-order.md) §"Past Performance Coverage Matrix" for the full template.

### Coverage matrix compliance check

- Every column header has a bracketed solicitation reference (e.g., `[SOW 1.2.1, A,B,C,D,F]`)
- Every row is a program/contract the offeror has executed (or an active subcontractor partner has executed)
- Cells use ✓ checkmarks, not text — visual scanability
- For each ✓ cell, the corresponding per-program narrative paragraph below the matrix should explicitly cover that evaluation area
- Mix of commercial and government clients — commercialization potential matters even in vehicle competitions

---

## 6. Resume integration pattern

GSA MAS task-order Key Personnel resumes are **embedded directly in Sub-Factor 1.2** (the technical volume body), not in a separate appendix.

Calibrated resume structure (per individual):
- TECHNICAL COMPETENCIES SUMMARY (bulleted, top of person's section)
- PROFESSIONAL EXPERIENCE (header)
- Per-role: ALL-CAPS ROLE NAME + right-aligned date range
- Per-role: chronologically reverse, with multiple `Project: [Name]` sub-headers within multi-project roles
- Dense bullet content with inline bold emphasis
- 2-4 pages per Key Personnel typical

Different from:
- FAR full proposals (separate Past Performance volume, organized by contract not by person)
- SBIR (resumes in Appendix at end of technical volume)

---

## 7. Compliance traceability

GSA MAS task-orders have **lighter formal compliance traceability** than FAR full proposals:

- **No Section L/M structure** in most cases — the solicitation defines Evaluation Factors and Sub-Factors directly
- **Sub-Factor structure is the response structure** — your headings match the solicitation's Sub-Factor numbering verbatim
- **Past Performance Coverage Matrix is the compliance proof** for Sub-Factor 1.1 — explicit visual mapping of programs to evaluation areas
- **No bracketed PWS references in heading** — Sub-Factor numbering is the brackets

If the framework's `working/compliance-matrix.json` is used, populate it with the Sub-Factor structure rather than full-FAR Section L/M rows.

---

## 8. Multi-volume coordination

When producing volumes for a GSA MAS task-order submission, ensure consistency across:

| Coordination point | Volumes |
|---|---|
| Key personnel names + clearances | Vol 1 (Sub-Factor 1.2 resumes) + Vol 3 (Personnel Clearance Template attachment) |
| Solicitation labor categories | Vol 1 (mentioned in Approach) + Vol 2 (LC mapping table) + Vol IV (rates per LC in xlsx) |
| Past performance contract identifiers | Vol 1 (Coverage Matrix + per-program narratives) |
| Period of performance | Vol 1 + Vol 2 + Vol IV |
| Header-strip program-name expansion | All volumes — letter-spaced expansion identical |
| Distribution-restriction footer | All volumes — same wording verbatim |

---

## 9. Pink-team checklist (GSA MAS task-order-specific)

- [ ] Sub-Factor headings carry solicitation's exact Sub-Factor numbering (1.1, 1.2, 1.3)
- [ ] Past Performance Coverage Matrix present at top of Sub-Factor 1.1
- [ ] Coverage matrix column headers carry bracketed solicitation references
- [ ] Coverage matrix has 4-7 program rows + 5-9 evaluation columns
- [ ] Per-program narratives map back to matrix columns (each ✓ has a corresponding claim)
- [ ] Key Personnel resumes integrated into Sub-Factor 1.2 body (NOT appendix)
- [ ] Resume role headings are ALL-CAPS with right-aligned date ranges
- [ ] Bullet density in Sub-Factor 1.2 ≥10/page
- [ ] Header strip identical across Vol 1 / Vol 2 / Vol 3 (RFQ# + acronym expansion)
- [ ] Acronym expansion on every page header (e.g., "SABER = Software Aqua Badge Engineering Resources")
- [ ] Volume numbering: Arabic 1-3 + Roman IV for pricing workbook
- [ ] All required attachments referenced in security volume actually exist in submission package
- [ ] Solicitation LC names consistent across Vol 1, Vol 2, Vol IV
- [ ] Distribution-restriction footer wording identical across all volumes
- [ ] Cover page on each volume identifies that volume by name + RFQ + program

---

## 10. Calibration changelog

| Date | Source | Volumes calibrated | Notes |
|---|---|---|---|
| 2026-04-25 | NGA SABER II (GSA MAS-flighted multi-vendor BPA) | Tech 13pp + Price 2pp + Security 5pp + Pricing xlsx | Established Scenario B conventions: multi-volume structure, Sub-Factor verbatim numbering, Past Performance Coverage Matrix pattern, embedded-resume convention, letter-spaced acronym header strip, security volume canonical 6-subsection plan, single-sheet pricing workbook with currency/rate format conventions |
