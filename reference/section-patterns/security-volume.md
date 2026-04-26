---
patterns_id: security-volume
display_name: Security Volume (cleared-contract supplement)
typical_length: 3-8 pages
section_order:
  - facility-clearance-and-foci
  - personnel-security-clearance
  - security-plan
required_sections: [facility-clearance-and-foci, personnel-security-clearance, security-plan]
optional_sections: []
---

# Section Patterns — Security Volume

A standalone supplemental volume required by **any cleared-contract solicitation** (Secret, Top Secret, SCI, or higher). Used as an attachment to the technical/price submission for FAR full proposals, IDIQ task orders, GSA MAS task orders, OTAs, and SBIRs that contemplate classified work.

**This pattern is reusable across multiple proposal types.** It is not tied to one section_patterns vehicle — proposal-writer should produce a security-volume.md companion when the solicitation requires it, regardless of the parent proposal-type's primary section_patterns.

**Calibrated against winning examples** — most recent: NGA SABER II vehicle competition Volume 3, 5 pages, 2026-04-25.

## Heading numbering convention

Standard depth-2 hierarchy. Section numbers map to the canonical structure (1 / 2 / 3) below. Subsection depth typically 1.1 / 3.1 etc.

## facility-clearance-and-foci (required)

Section 1 of the security volume. Two subsections:

### 1.1 Facility Clearance Level (FCL)

**Purpose:** Declare the offeror's current facility clearance level and reference supporting documentation.

**Pattern (1 paragraph):**
- Lead with the FCL declaration: "[Company] currently holds a [Level — Top Secret / Secret / etc.] Facility Clearance Level (FCL) as required by the DD Form 254."
- Reference supporting attachments: "Evidence of [Company]'s FCL is provided in Attachment N (DD Form 254) and Attachment N+1 (Facility Clearance Level Template)."
- For **subcontractors / teaming partners**: state the partner's FCL on a separate line, with reference to a separate Attachment for that partner.

**Required attachments (named in this subsection):**
- DD Form 254 — Department of Defense Contract Security Classification Specification (covers prime; separate form per subcontractor)
- Facility Clearance Level Template (an agency-specific form summarizing the FCL — sometimes called Facility Security Clearance Form or similar)

### 1.2 Foreign Ownership, Control, or Influence (FOCI)

**Purpose:** Declare FOCI status (or absence thereof) and reference supporting documentation.

**Pattern (1 paragraph):**
- Lead with FOCI declaration: "[Company] has been determined to have **no Foreign Ownership, Control, or Influence (FOCI)** by [agency / DCSA] as documented in Attachment N (FOCI Determination)."
- For **subcontractors / teaming partners**: state each partner's FOCI status separately.
- If FOCI exists and has been mitigated: state the mitigation instrument (Special Security Agreement, Voting Trust, Board Resolution, etc.) and reference the approval letter.

## personnel-security-clearance (required)

Section 2 of the security volume. Single section (no subsections in calibrated source).

**Purpose:** Declare that proposed personnel hold the required clearance level and reference supporting documentation.

**Pattern (1 paragraph + 1 attachment reference):**
- Lead with required clearance level per the solicitation: "The Personnel Security Clearance Level required by the [Solicitation Reference, e.g., RFQ section] is [Top Secret / Secret / Top Secret with SCI eligibility / etc.]."
- State that all proposed personnel meet or exceed this level: "All personnel proposed by [Company] in the Technical Volume hold an active [Level] clearance issued by DCSA."
- Reference the supporting attachment listing each proposed person and their clearance status: "A complete listing of proposed personnel and their clearance status is provided in Attachment N (Personnel Clearance Level Template)."
- **For-Official-Use-Only (FOUO) marking:** the personnel clearance template is typically marked FOUO. Note this in the volume so the attachment is handled correctly.

**Required attachment:**
- Personnel Clearance Level Template (often FOUO-marked) — agency-specific form listing each cleared individual with their clearance level, investigation date, and special-access-program eligibility

## security-plan (required)

Section 3 of the security volume. The body of the volume — describes the offeror's standing security plan and how it applies to the contract.

### Canonical 6-subsection structure

Calibrated against winning examples. All six subsections are typically required; some can be combined when the page budget is tight.

**3.1 Security Procedures**
- Lead-in: state that the security plan is governed by NISPOM (32 CFR Part 117) and the customer's specific security policies (e.g., NSI/NSPM 28 for IC; agency-specific equivalents)
- Brief paragraph naming key procedural elements: training cadence, document control, classified information handling, visitor control, removable media policy
- Reference any agency-specific clauses or directives

**3.2 Security Training**
- Bulleted list of standing training programs:
  - Initial / Refresher Security Training (annual)
  - Derivative Classification Training
  - OPSEC Training
  - Insider Threat Training
- Add agency-specific training if required (e.g., SCI Indoctrination for SCI-cleared programs)

**3.3 Security Portal / Document Management**
- Describe the company's centralized security tooling
- Sub-bulleted list of capabilities:
  - Security clearance lookup and tracking
  - Self-service reporting (foreign travel, adverse contacts, suspicious contacts, cyber intrusions, status changes)
  - Document repository for NISPOM, ISLs, SF 312/NDAs, training certifications
  - Self-service NDA submission and verification

**3.4 Annual Review**
- Brief paragraph stating annual review cadence, who conducts it (Facility Security Officer / FSO), and what triggers more frequent reviews

**3.5 Safeguarding Classified Information**
- Paragraph describing the standard safeguarding posture:
  - Storage of classified material (GSA-approved containers, secured facilities)
  - Classified processing systems (separate, audited, NISPOM-compliant)
  - Transmission protocols (SIPR, JWICS, courier where applicable)
  - Destruction procedures
- Reference NISPOM Chapter 5 (and any agency supplements) as the governing standard

**3.6 Handling Security Incidents and Violations**
- **Two-part structure:**
  1. List of disciplinable violations (with EO 13526 citations):
     - Disclose to unauthorized persons information that is properly classified
     - Classify or continue classification in violation of EO 13526
     - Create or continue a special access program contrary to EO 13526 requirements
     - Contravene any other provision of EO 13526 or its implementing directives
  2. Graduated scale of disciplinary actions:
     - Reprimand
     - Suspension without pay
     - Removal
     - Loss or denial of access to classified information
     - Other sanctions in accordance with applicable laws and agency regulations
- Closing commitment statement on personnel obligation to protect classified information

## Writing style

Security volumes use **the most formal voice in any federal proposal** — calibrated mean sentence length is 30+ words (vs. 22-28 for technical volumes). Long, contractually-precise sentences are appropriate because security volumes are **declarations and commitments** that the contracting officer relies on for the security determination.

Vocabulary is heavily NISPOM-derived: "facility clearance," "personnel security clearance," "classified information," "safeguarding," "disclosure," "graduated disciplinary actions." Use these exact terms. Do NOT invent synonyms.

## Page allocation (calibrated)

For a 5-page security volume:
- Page 1: Sections 1.1 + 1.2 + Section 2 (FCL, FOCI, Personnel)
- Page 2: Sections 3.1 - 3.5 (Security Plan, partial)
- Page 3: Section 3.6 (Incidents and Violations — bulleted)
- Pages 4-5: signature page, attached forms, or appendices

For a longer security volume (8+ pages), expand Sections 3.3 (Security Portal) and 3.5 (Safeguarding) with more detail; keep 3.1, 3.2, 3.4, 3.6 brief.

## Required attachments (separate from the volume itself)

The security volume **references but does not contain** these attachments. Each is a separate file in the submission:

- **DD Form 254** (Contract Security Classification Specification) — one per organization (prime + each subcontractor)
- **Facility Clearance Level Template** — agency-specific FCL summary form
- **Personnel Clearance Level Template** — typically FOUO-marked; lists each cleared individual + clearance status

The technical volume's File Name conventions (e.g., "Attachment 3 - DD254", "Attachment 4 - Facility Clearance Level Template", "Attachment 5 - Personnel Clearance Level Template - FOUO") match the references inside the security volume.

## Pink-team checklist (security-volume-specific)

- [ ] FCL declared with explicit level + supporting attachment reference
- [ ] FOCI status declared (no FOCI / mitigated FOCI with mitigation instrument named)
- [ ] FCL + FOCI declared separately for prime and each subcontractor
- [ ] Required Personnel Security Clearance level matches solicitation
- [ ] Personnel listing references the FOUO-marked Attachment
- [ ] Section 3 Security Plan covers all 6 canonical subsections
- [ ] EO 13526 citations present in Section 3.6
- [ ] NISPOM (32 CFR Part 117) referenced as governing standard
- [ ] Graduated disciplinary actions list complete (5 items minimum)
- [ ] Volume references match the attachment file names in the submission package
- [ ] FOUO-marked attachments are clearly indicated (filename + cover-sheet)
