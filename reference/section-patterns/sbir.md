---
patterns_id: sbir
display_name: SBIR / STTR (Phase I, Phase II, Direct-to-Phase-II)
typical_length: 15-25pp for Direct-to-Phase-II; 15-20pp for Phase I; 25-40pp for traditional Phase II
section_order:
  - cover-page
  - objective
  - scope
  - background
  - phase-ii-technical-objectives
  - task-technical-requirements
  - deliverables
  - related-work
  - capabilities
  - resume-appendix
required_sections: [cover-page, objective, scope, background, phase-ii-technical-objectives, task-technical-requirements, deliverables, related-work, resume-appendix]
optional_sections: [capabilities]
---

# SBIR / STTR Section Patterns

SBIR = feasibility (Phase I), prototype (Phase II), or accelerated prototype (Direct-to-Phase-II). Topic-specific, small-biz-owned IP, commercialization-scored. Follow the topic description verbatim.

**Calibrated against winning examples** — most recent: Direct-to-Phase-II AFWERX/BESPIN-flighted SBIR, 15 pages, 2026-04-25. See [`reference/proposal-conventions/sbir.md`](../proposal-conventions/sbir.md) for structural and stylistic conventions.

## Direct-to-Phase-II (D2P2) variants

Direct-to-Phase-II SBIRs skip Phase I and go straight to prototype development. The technical volume is **shorter** (15-20 pp typical) than a traditional Phase II (25-40 pp) because the topic context is already established. Direct-to-Phase-II proposals must demonstrate that prior commercial work substitutes for Phase I feasibility — usually proven via a "Related Work" section showing comparable prior projects.

The section_order above is calibrated for Direct-to-Phase-II structure (Objective → Scope → Background → Tasks → Deliverables → Related Work → Capabilities → Resumes). Traditional Phase II proposals expand the technical-objectives section and add a Phase I results summary at the start.

## Heading numbering convention

SBIR uses a simple decimal hierarchy that maps directly to the topic's task structure. Typical depth-3 max, occasional depth-4 within tasks:

```
4 Technical Approach
4.1 Objective
4.2 Scope
4.3 Background
4.4 Task / Technical Requirements
4.4.1 Task 1 - Discovery and Planning
4.4.2 Task 2 - Alpha Development
4.4.3 Task 3 - Beta Development
4.4.4 Task 4 - Operational Deployment
```

Each `Task N` subsection has a structured **Subtask × Delivery × Deliverable × Acceptance Criteria** table — see the task-technical-requirements section pattern below.

## cover-page (required)

SBIR cover pages are **plain, text-heavy, and unbranded** — different from FAR full-proposal covers. The topic identification, proposal number, and company identifiers carry the load. No background color, no decorative graphics.

**Required elements:**
- Title block (centered, bold serif): "Proposal for SBIR [NN.N] [Program Type]" + topic line + "Topic # [TOPIC-NUMBER]"
- Customer line: "for / DEPARTMENT OF DEFENSE SMALL BUSINESS INNOVATION RESEARCH (SBIR) PROGRAM"
- Two-column block (left/right): "Prepared for / Prepared by"
  - Left: Customer POC (AFWERX / NIH PO / other agency POC) — name, phone, email, address
  - Right: Company name (in brand color), address, phone, contact (CEO/PI), CAGE Code, DUNS, SBA SID
- Volume designator (small): "Volume II - Technical Volume"
- Proposal Number (small)
- Date
- Distribution restriction (small italic, bottom)

**Style rules:**
- White background — no brand color fill
- Logo placement is right side under "Prepared by," NOT a large hero element
- Text-only — no decorative geometric patterns, no photo, no figure
- Black text throughout, brand color reserved for company name only

## objective (required)

Single subsection (typical depth: 4.1 in topic-numbered structure). Brief statement (~half page) of what Phase II will achieve. Two-three paragraphs naming:

1. The technical objective (what gets built/proven)
2. The user/customer benefit (who wins, how)
3. The path to operational deployment (how this becomes real)

## scope (required)

What Phase II covers and what it explicitly excludes (~half page). Bullets acceptable. Frames the boundaries that the Tasks will operationalize.

## background (required)

~1 page. Establishes the technical and operational context the topic addresses. For Direct-to-Phase-II, this section also briefly summarizes prior commercial work that substitutes for Phase I feasibility.

**Pattern:** open with a problem statement, then bridge to "[Your Company] is uniquely positioned because..."

## phase-ii-technical-objectives (required)

Numbered list of 3-5 measurable technical objectives the Phase II prototype will achieve. Each objective:

- Single sentence with subject + action verb + measurable outcome
- Tied to the topic's stated requirements
- Listed in priority order (objective 1 most critical)

**Template:**
```
Objective 1: [Verb] [a flexible/adaptable/X system / approach] for [stakeholders/use case] to [measurable outcome].
Objective 2: [Verb] and maintain [a well-organized X / service / tool] to [outcome].
Objective 3: [Verb] [the operational deployment / Y / Z].
```

## task-technical-requirements (required)

The structural heart of an SBIR Phase II proposal. Decomposes Phase II into 3-5 sequential tasks (typical: Discovery → Alpha → Beta → Operational Deployment), each with the same internal structure.

### Per-task pattern

```
4.4.N Task N - [Task Name]

[1-2 paragraph narrative of the task's purpose and approach]

Table N: [Task Name] Subtasks

| TASK | SUBTASK | EXPECTED DELIVERY | DELIVERABLE | ACCEPTANCE CRITERIA |
|------|---------|-------------------|-------------|---------------------|
| (rotated vertical text spanning all rows: "Task N: [Task Name]") | Subtask 1 description | Award + N months | Specific artifact | Criteria for acceptance |
| | Subtask 2 description | Award + N months | Specific artifact | Criteria for acceptance |
| | Subtask 3 description | Award + N months | Specific artifact | Criteria for acceptance |
```

### Subtask table conventions

- **5-column structure** is canonical: TASK | SUBTASK | EXPECTED DELIVERY | DELIVERABLE | ACCEPTANCE CRITERIA
- **TASK column** uses rotated vertical text (90°) spanning all rows of that task — visually identifies which task block the row belongs to
- **EXPECTED DELIVERY** uses "Award + N months" or "Award + N-N months" notation (not absolute dates — Phase II awards have variable start dates)
- **DELIVERABLE** column names the specific artifact (document, code, demo, deployment)
- **ACCEPTANCE CRITERIA** is concrete and verifiable — not "Government approval" but "Tested with N users at IL-N environment" or similar
- Header row in dark fill, white bold text
- Bullets within cells use ▶ chevron markers

## deliverables (required)

Explicit list of what Phase II ships. Mix of SBIR-mandated and topic-specific:

**SBIR-mandated:**
- Final Report (typically 30 days after Phase II completion)
- Quarterly Status Reports (every 90 days during performance)
- Status Reports (more frequent — monthly or as required)
- Small Business Online Success Stories (post-Phase-II, when commercial traction exists)

**Topic-specific:**
- Add deliverables called out in the topic description verbatim
- Map each to the corresponding Task N table

Use bullet format. 5-10 bullets typical.

## related-work (required)

For Direct-to-Phase-II, this section is **how you prove Phase I is unnecessary**. For traditional Phase II, this section reinforces commercialization potential. Either way, calibration shows it's structured as 2-4 project narratives.

### Per-project pattern

```
6.N [Project Name] ([Customer Type, parenthetical])

[1-2 paragraphs of narrative describing the project, customer pain solved, and outcomes]

Phases applied / Methodologies:
- [Phase 1, e.g., Discovery and Ideation]
- [Phase 2, e.g., Concepting]
- [Phase 3, e.g., Planning]
- [Phase 4, e.g., Agile Development (Design, Build, Test)]
- [Phase 5, e.g., Deployment]
```

**Customer type tagging:** put the customer category in the heading parenthetical for evaluator scanability:
- `(Commercial client)`
- `(Classified Intelligence Community (IC) project)`
- `(DoD Service Branch project)`
- `(Other Government Agency)`

**Pattern justification:** evaluators score commercialization potential. Showing 2+ commercial clients alongside government work proves dual-use viability — a high-yield SBIR scoring lever.

## capabilities (optional)

`Section 7` in the calibrated structure. Used to deepen the technical credibility story when page budget allows.

Subsections:
- `7.1 [Tailored framework / methodology]` — your distinctive approach (e.g., a Capability Maturity Framework, an architecture pattern, a delivery methodology)
- `7.2 [DevOps CI/CD Pipeline / Technical Architecture]` — operational infrastructure underlying the prototype
- `7.3 [Catalog / Reusable Assets]` — what you bring to bear that competitors don't

Each subsection: 1-2 paragraphs + 1 figure if applicable.

## resume-appendix (required for Direct-to-Phase-II)

Full resumes of key personnel — typically 1-2 pages per person. Required for D2P2 because there's no Phase I to establish credibility; the team must be presented in full.

### Per-resume pattern

```
Appendix [Letter] — Resume [Name], [Role/Title]

SUMMARY OF QUALIFICATIONS
- 3-5 bullet points (▶ chevron markers) summarizing experience
- Quantify where possible (years, dollar value of past programs, team sizes)

TECHNOLOGY EXPERTISE

| Category | Specifics |
|---|---|
| [e.g., eCommerce] | [specific products, frameworks, libraries] |
| [e.g., Languages] | [J2EE, SQL, ...] |
| [e.g., Web Development] | [HTML, frameworks, libraries] |
| [e.g., Big Data] | [tools used] |
| [...] | [...] |

EMPLOYMENT HISTORY

[Company] ([Date Range]) - [Role/Title]
[Sub-line: division/program if applicable]
- Role description bullet
- Accomplishment bullet (with quantified impact)
- Accomplishment bullet

[Next Company] ([Date Range]) - [Role/Title]
- ...

EDUCATION
[Degree], [Institution], [Year]
```

**Resume key personnel:**
- **Principal Investigator (required)** — full resume, listed first
- Technical Lead (if different from PI)
- Commercialization Lead (if your team has one)
- Optional: 1-2 other key SMEs whose names appear in Tasks


**Purpose:** Why this problem, why now, why it matters to the agency.
**Structure:** Agency mission context → specific gap the topic identifies → significance of solving it.
**Cite the topic number and description verbatim** — evaluators check.

## phase-i-feasibility-or-phase-ii-prototype (required)
**Purpose:** The research/development plan.
- **Phase I:** Feasibility study — what will be tested in 6 (DoD) or 6-12 (civilian) months, typically $75K-$300K.
- **Phase II:** Prototype development — built on Phase I results, typically 24 months and $750K-$2M.
**Structure:** Objectives → approach → expected results.

## technical-objectives (required)
**Purpose:** Measurable goals for the phase.
**Structure:** 3-5 numbered objectives, each with: description, measurable success criterion, risk.

## work-plan (required)
**Purpose:** Tasks, schedule, deliverables.
**Structure:** Task breakdown (WBS-style) → timeline (months 1-6 or 1-24) → deliverables per task.

## related-work (optional, recommended for Phase II)
**Purpose:** Prior research that informs this proposal.
**Phase II:** Include Phase I results summary.
**Phase I:** Include prior relevant work by the team.

## key-personnel (required)
**Purpose:** Who does the work. PI + other key personnel.
**Structure:** Per-person: role, hours, qualifications, prior SBIR experience (if any).
**SBIR rule:** PI commitment ≥51% employment during performance period (Phase I).

## commercialization-plan (required)
**Purpose:** **Scored in every phase.** Who will buy this in Phase III? Why will they buy? How do we transition?
**Structure:** Target market → Phase III customers (named if possible) → go-to-market → existing commitments (letters of intent if available — scoring lift).
**Pitfall:** Weak commercialization = low score even if technical is strong.

## budget-narrative (required)
**Purpose:** Cost narrative supporting the budget xlsx.
**Reference:** `reference/pricing-artifacts/sbir-budget.md`
**Structure:** Per-category discussion (labor, materials, travel, subs, indirects, fee) — tying cost to scope.
**Export:** `final/docx/` narrative + `final/xlsx/sbir-budget.xlsx` (workbook is primary artifact).

## data-rights (optional but recommended)
**Purpose:** Explicit SBIR data rights assertion.
**Authority:** SBIR/STTR Policy Directive (NOT DFARS 252.227).
**Structure:** What data will carry SBIR markings; duration.

## Global rules
- **Topic cap check.** Budget cannot exceed topic cap. `/export-proposal` verifies.
- **Prime work share.** Phase I ≥67%, Phase II ≥50%.
- **PI ≥51% commitment** Phase I.
- **Follow the topic description.** Evaluators compare your response against the topic verbatim.
- **Commercialization plan is not optional, even in Phase I.**
