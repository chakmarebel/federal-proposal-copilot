---
patterns_id: gsa-mas-task-order
display_name: GSA MAS-Flighted Task Order / BPA Competition
typical_length: 13-25pp Technical + 2-3pp Price + 5-8pp Security + Pricing Workbook (xlsx)
section_order:
  - cover-page
  - sub-factor-corporate-experience
  - sub-factor-staffing-key-personnel
  - sub-factor-approach
required_sections: [cover-page, sub-factor-corporate-experience, sub-factor-staffing-key-personnel, sub-factor-approach]
optional_sections: []
---

# Section Patterns — GSA MAS-Flighted Task Order / BPA Competition

For multi-vendor task-order or BPA competitions issued **under a GSA MAS Schedule** (e.g., GSA MAS Information Technology category). The agency competes a specific scope of work; offerors hold an existing GSA Schedule and respond with a vehicle-specific technical, price, and (if cleared) security submission.

**Distinct from:**
- A direct GSA MAS Schedule offering (the original Schedule submission — different patterns)
- A FAR Part 15 RFP (full Section L/M structure — uses `full-proposal` patterns)
- A standalone IDIQ task order under a non-MAS contract (uses `idiq-to` registry type with `full-proposal` patterns)

**Calibrated against winning examples** — most recent: NGA SABER II (GSA MAS-flighted multi-vendor BPA), 2026-04-25.

## Multi-volume structure

The submission is split across multiple discrete volumes, each a standalone artifact. The technical volume uses the section patterns documented here; price and security volumes use their own dedicated patterns.

| Volume | File | Patterns reference | Typical length |
|---|---|---|---|
| Vol 1 — Technical | `Vol 1 Technical.pdf` | This file (gsa-mas-task-order) | 13-25 pp |
| Vol 2 — Price (narrative) | `Vol 2 Price.pdf` | See `reference/pricing-artifacts/gsa-mas-pricing.md` | 2-3 pp |
| Vol 3 — Security | `Vol 3 Security.pdf` | See `reference/section-patterns/security-volume.md` | 5-8 pp |
| Vol IV — Price (workbook) | `Vol IV Price-Attach.xlsx` | See `reference/pricing-artifacts/gsa-mas-pricing.md` | (xlsx) |
| Attachments | DD Form 254, Facility Clearance Template, Personnel Clearance Template (FOUO), other agency-specific forms | n/a — see security-volume pattern | (forms) |

**Volume naming convention:** Volumes 1, 2, 3 use Arabic; Vol IV uses Roman to mark the pricing workbook as the "definitive numerical artifact" separate from the price narrative.

## Heading numbering convention

Sub-Factor structure mirrors the solicitation's evaluation factors (Section M). Body subsections within each Sub-Factor use **non-numeric headings in ALL CAPS** for organizational clarity rather than deeper numeric depth.

```
1. Sub-Factor 1.1 Corporate Experience
   (body — narrative + Past Performance Coverage Matrix)

2. Sub-Factor 1.2 Staffing Key Personnel
   (body — per-person resumes with role-name headings)
   TECHNICAL COMPETENCIES SUMMARY
   PROFESSIONAL EXPERIENCE
   [ROLE NAME — e.g., PRINCIPAL SOFTWARE ENGINEER]
   [ROLE NAME — e.g., PROJECT MANAGER]

3. Sub-Factor 1.3 Approach in [Domain] Environment
   (body — methodology / process narrative)
```

Note: solicitation Sub-Factor numbering (1.1, 1.2, 1.3) is **carried verbatim into the heading**. Do not renumber. Evaluators score Sub-Factor 1.X by reading "your" Sub-Factor 1.X.

## cover-page (required)

GSA MAS task-order responses use a **plain cover** similar to SBIR — no decorative graphics, brand-on-name only, generous whitespace.

Required elements:
- Volume designator (e.g., "Technical Volume" / "Price Volume" / "Security Volume")
- Solicitation/RFQ number (e.g., "RFQ #HM047620Q0028")
- Program name (often as both acronym and expansion: "SABER II — Software Aqua Badge Engineering Resources")
- Offeror identification (Company name + brand)
- Date

Each volume has its own cover with the volume name prominent.

## sub-factor-corporate-experience (required)

**Section 1 of the technical volume.** Demonstrates the offeror's organizational capability via past contracts that map to the solicitation's stated work scope.

### Structure

1. **Lead-in paragraph (1-2 sentences):** name the offeror + key teaming partner(s); preview that "the following [N] programs from companies in Section X" demonstrate the experience required.
2. **Past Performance Coverage Matrix (table — see below):** the structural heart of this section.
3. **Per-program narrative paragraphs (5-8 paragraphs):** one paragraph per program, in heavy bullet/highlight style.

### Past Performance Coverage Matrix

A row-per-program × column-per-evaluation-area table with checkmark cells indicating which programs cover which evaluation areas. Each column header carries a bracketed solicitation reference.

```
                    ┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
                    │ Eval Area 1  │ Eval Area 2  │ Eval Area 3  │ Eval Area 4  │ Eval Area 5  │ Eval Area 6  │ Eval Area 7  │
                    │ [SOW 1.2.1,  │ [SOW 1.2.1,  │ [SOW 1.2.1,  │ [SOW 1.2.1,  │ (SOW 1.1)    │ (SOW 1.2)    │ Multiple Sec │
                    │ A,B,C,D,F]   │ E]           │ G]           │ H]           │              │              │ Env          │
┌───────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ Program/Customer  │      ✓       │      ✓       │      ✓       │      ✓       │      ✓       │      ✓       │      ✓       │
│ Name 1            │              │              │              │              │              │              │              │
│ Program/Customer  │      ✓       │      ✓       │              │      ✓       │      ✓       │              │      ✓       │
│ Name 2            │              │              │              │              │              │              │              │
│ ...               │              │              │              │              │              │              │              │
└───────────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

**Calibrated structure:**
- 4-7 program rows (commercial mix preferred for commercialization scoring)
- 5-9 evaluation-area columns
- Each column header has a 1-2 line label + a bracketed `[SOW X.Y.Z, A,B,C]` reference identifying which evaluation areas it represents
- Cells use ✓ checkmarks (not text — visual scanability matters)

This matrix is the **single most important graphic** in a GSA MAS task-order technical volume. It lets the evaluator verify Sub-Factor 1.1 coverage in 30 seconds.

### Per-program narrative pattern

Following the matrix, write 1 paragraph per program (~6-8 paragraphs total) describing how that specific contract demonstrates relevant experience. Heavy use of:
- **Bold inline emphasis** for key claims and proof points
- Customer-language adoption (use the solicitation's exact terms)
- Specific metrics (team sizes, dollar values, durations)
- Direct mapping back to evaluation-area column headers

## sub-factor-staffing-key-personnel (required)

**Section 2 of the technical volume.** The longest and most technically detailed section — typically 5-8 pages of a 13-page volume.

### Structure (calibrated)

```
2. Sub-Factor 1.2 Staffing Key Personnel

[1-2 paragraph lead-in: staffing approach, total headcount, key personnel name list]

[For each Key Personnel — typically 3-5 individuals:]

  TECHNICAL COMPETENCIES SUMMARY
  [List of technical capabilities this person brings — bulleted]

  PROFESSIONAL EXPERIENCE

  [PRIOR ROLE NAME — e.g., PRINCIPAL SOFTWARE ENGINEER]   [Date Range — right-aligned]
  [Sub-line: Company / Project context]
  - Bulleted accomplishment 1
  - Bulleted accomplishment 2
  - Bulleted accomplishment 3
  ...

  [NEXT ROLE NAME — e.g., PROJECT MANAGER]   [Date Range — right-aligned]
  - Bulleted accomplishments...

  ...continues across multiple pages per person
```

### Resume integration pattern (calibrated)

GSA MAS task-order resumes are **embedded in the technical volume body**, NOT in an appendix. Each Key Personnel resume is 2-4 pages of dense bulleted detail, organized chronologically (most recent first) with multiple project-specific sub-headings within each role.

This is **different from**:
- FAR full proposals (separate Past Performance volume)
- SBIR (resumes in Appendix at the end)

The rationale: GSA MAS task-order evaluations score Sub-Factor 1.2 against specific named individuals. Putting the resume content directly under Sub-Factor 1.2 makes the evaluator's job easy.

### Per-role formatting

```
[ROLE NAME IN ALL CAPS]                                              [MM/YYYY – MM/YYYY]
[Optional sub-header: Project / Program context]
- Action-verb bullet describing accomplishment, with **inline-bolded keywords** for technical skills/tools
- Quantified outcome bullet ($N, N people, N% improvement)
- ...
```

For multi-project roles within a single company, add `Project: [Project Name]` sub-headers between bullet groups:

```
[ROLE NAME]                                                          [MM/YYYY – MM/YYYY]
- Initial accomplishment bullets (general scope)
Project: [Project Name 1]
- Project-specific bullet
- Project-specific bullet
Project: [Project Name 2]
- Project-specific bullet
```

### Bullet density (calibrated)

**11+ bullets/page average** — much higher than other proposal types. Sub-Factor 1.2 is dense by design; evaluators want to scan capabilities, not read prose.

## sub-factor-approach (required)

**Section 3 of the technical volume.** Describes the offeror's methodology for performing the work — typically the most narrative-prose-heavy section of the volume.

### Structure

1. **Lead-in:** name the methodology / framework (Agile, DevOps, SAFe, custom)
2. **Methodology subsections (4-6 of them):** each ~half-page describing one aspect of the approach
3. **Tools & ceremonies:** describe specific tooling and recurring activities (sprint planning, retros, daily standups)
4. **Deliverables cadence:** how the methodology produces customer-facing artifacts on what schedule

Use customer-language adoption from the solicitation's "Approach" requirements. If the solicitation references DevSecOps, Agile, or specific frameworks (e.g., Scaled Agile Framework), use those exact terms.

## Multi-volume coordination

When producing volumes for a GSA MAS task-order submission:

| Coordination point | Volumes affected | Discipline |
|---|---|---|
| Key personnel names + clearance levels | Vol 1 (Sub-Factor 1.2) + Vol 3 (Personnel Clearance attachment) | Names must match exactly between technical resume content and the FOUO clearance template |
| Labor-category mapping | Vol 1 (Approach mentions LCATs) + Vol 2 (Price narrative LC mapping table) + Vol IV (xlsx rates per LC) | Solicitation LC names must be consistent across all three volumes |
| Past performance contract identifiers | Vol 1 (PP Coverage Matrix) + corporate citations | Contract numbers and customer names must match across the matrix and the per-program narratives |
| Total ceiling / period of performance | Vol 1 (mentions in approach) + Vol 2 (price narrative) + Vol IV (totals in xlsx) | Period of performance must match across all three |

## Pink-team checklist (gsa-mas-task-order-specific)

Augments the existing checks:

- [ ] Sub-Factor headings carry the solicitation's exact Sub-Factor numbering (1.1, 1.2, 1.3)
- [ ] Past Performance Coverage Matrix present in Sub-Factor 1.1, with bracketed eval-area references in column headers
- [ ] Per-program narratives map back to matrix columns (each ✓ in the matrix corresponds to a claim in the narrative)
- [ ] Key Personnel resumes integrated into Sub-Factor 1.2 body (not appendix)
- [ ] Resumes use ALL-CAPS role-name headings with right-aligned date ranges
- [ ] Resumes contain Project: sub-headers within multi-project roles
- [ ] Bullet density in Sub-Factor 1.2 ≥10/page (this section is by-design dense)
- [ ] Solicitation LCAT names appear consistently across Vol 1, Vol 2, Vol IV
- [ ] Header strip identical across all volumes (Vol 1, Vol 2, Vol 3) — same RFQ#, same program name expansion
- [ ] All required attachments referenced in security volume actually exist in submission package (DD 254, FCL Template, PCL Template-FOUO)
- [ ] Cover page on each volume identifies that volume specifically (Volume name + RFQ + program)
