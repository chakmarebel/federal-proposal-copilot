---
patterns_id: full-proposal
display_name: FAR Full Proposal (Technical Volume)
typical_length: 30-75 pages per volume (per Section L)
section_order:
  - cover-and-front-matter
  - executive-summary
  - technical-approach-introduction
  - technical-approach-by-pws
  - service-summary
  - gfp-and-equipment
  - general-information
  - past-performance
  - management-approach
  - path-forward
  - conclusion
required_sections:
  - cover-and-front-matter
  - executive-summary
  - technical-approach-introduction
  - technical-approach-by-pws
  - past-performance
  - management-approach
optional_sections:
  - service-summary
  - gfp-and-equipment
  - general-information
  - path-forward
  - conclusion
---

# Section Patterns — FAR Full Proposal (Technical Volume)

Reusable section structures for federal full proposals (FAR Part 15 RFPs, IDIQ task orders, CSO full proposals). Each pattern includes a template with `[PLACEHOLDER]` markers. Replace placeholders with proposal-specific content.

**Calibrated against winning examples** — most recent calibration: 2026-04-23, against an Air Force IDIQ technical volume. See [`reference/proposal-conventions/far-rfp.md`](../proposal-conventions/far-rfp.md) for the structural conventions distilled from that calibration.

## Heading conventions (mandatory for FAR full proposals)

Every section/subsection heading carries a **bracketed solicitation reference** so a Section M evaluator can verify coverage at a glance:

```
2.2.1.1 Data Acquisition [PWS 2.1.1]
2.2.2 Agile Algorithm Solutions [PWS 2.2]
6.3 Transition-In Plan [Section L.4.2]
```

Pattern: `<our-section-#> <Section Title> [<Solicitation Reference>]`

The bracketed reference may cite PWS, SOW, Section L instructions, Section M factors, or CDRLs depending on what the solicitation calls for. **One section heading should never reference more than one or two solicitation locations** — if it would, split the section.

**1:1 PWS-to-section mirroring** is the gold standard: if the solicitation has PWS 2.1.1 / 2.1.2 / 2.1.3, your technical volume responds with a 1:1 subsection structure. Evaluators scan for this discipline.

## Writing style baseline (federal full proposals)

Calibrated norms from winning examples — your drafts should land within these ranges. Deviations either way are a flag.

- **Mean sentence length:** 22–28 words (federal style is dense; do NOT compress to 15-word "punchy")
- **p90 sentence length:** ≤45 words
- **Paragraph length:** 3–6 sentences typical; 8+ flags as needs-trimming
- **Bullet density:** 2–6 bullets/page average; bullet-heavy pages (>10) belong in management/admin sections
- **Figure density:** 1–2 figures per body page; front matter may concentrate (cover, brand)
- **Customer-language adoption:** use the customer's exact framework terminology consistently. If the solicitation defines a 7-attribute data framework, use those 7 terms verbatim in headings and prose. Do NOT invent synonyms.
- **In-text figure refs:** every figure has at least one in-text reference ("see Figure 3"). Figures floating without text refs are a Pink-team finding.

## Front-matter allocation

Calibrated norm: ~12-15% of total volume page count is front matter (cover, transmittal, TOC, acronym list, classification cover sheets). For a 50-page volume, expect 6-8 front-matter pages. The technical body starts ~p7-p8.

---

## Executive Summary Pattern

Three paragraphs: context, solution, value. Typically 1-2 pages.

### Structure
1. **Context (4-6 sentences).** State the customer's challenge using their language. Reference the solicitation. Establish urgency or strategic importance.
2. **Solution (4-6 sentences).** Describe your approach. Name specific capabilities, technologies, and differentiators. Connect to the customer's stated needs.
3. **Value (3-5 sentences).** Quantify outcomes where possible. State risk reduction. Close with a forward-looking commitment.

### Template

```
[CUSTOMER_AGENCY] faces [CORE_CHALLENGE] as [CONTEXT_FOR_URGENCY]. [SOLICITATION_REFERENCE]
identifies the need for [STATED_NEED], requiring [KEY_REQUIREMENTS]. Without action,
[CONSEQUENCE_OF_INACTION].

[COMPANY_NAME] proposes [SOLUTION_NAME], a [BRIEF_ARCHITECTURE_DESCRIPTION] that
[PRIMARY_CAPABILITY]. Our approach [DIFFERENTIATOR_1] and [DIFFERENTIATOR_2], built on
[PAST_PERFORMANCE_EVIDENCE]. [SOLUTION_NAME] addresses [SOLICITATION_REFERENCE] requirements
by [HOW_REQUIREMENTS_ARE_MET].

This approach delivers [QUANTIFIED_OUTCOME_1] and [QUANTIFIED_OUTCOME_2], reducing
[SPECIFIC_RISK] while [ADDITIONAL_BENEFIT]. [COMPANY_NAME] is prepared to [IMMEDIATE_NEXT_STEP]
within [TIMELINE] of award, with full operational capability by [TARGET_DATE].
```

---

## Problem Statement Pattern

Three challenges, problem-first framing, pivot to solution. Typically 0.5-1 page.

### Structure
1. **Opening (2-3 sentences).** Frame the operational environment and the stakes.
2. **Challenge 1.** Most critical problem. Concrete, specific, traceable to the solicitation.
3. **Challenge 2.** Second problem. Different dimension (technical, operational, or organizational).
4. **Challenge 3.** Third problem. Often addresses scale, speed, or integration.
5. **Pivot (2-3 sentences).** Transition from problems to your approach without yet describing the solution in detail.

### Template

```
[CUSTOMER_AGENCY] operates in [OPERATIONAL_ENVIRONMENT] where [STRATEGIC_CONTEXT]. The mission
demands [MISSION_REQUIREMENT], yet current approaches face three critical challenges.

**[CHALLENGE_1_NAME].** [DESCRIPTION_OF_CHALLENGE_1]. Today, [CURRENT_STATE_METRIC_OR_PAIN].
This results in [IMPACT_ON_MISSION].

**[CHALLENGE_2_NAME].** [DESCRIPTION_OF_CHALLENGE_2]. Existing tools [CURRENT_LIMITATION],
forcing [WORKAROUND_OR_CONSEQUENCE].

**[CHALLENGE_3_NAME].** [DESCRIPTION_OF_CHALLENGE_3]. As [SCALE_OR_SPEED_FACTOR] increases,
[CONSEQUENCE_OF_NOT_ADDRESSING].

Addressing these challenges requires [TYPE_OF_APPROACH] -- one that [KEY_ATTRIBUTE_1],
[KEY_ATTRIBUTE_2], and [KEY_ATTRIBUTE_3]. The following sections describe [COMPANY_NAME]'s
approach to delivering this capability.
```

---

## Capability Overview Pattern

200-word introduction, core bullets, past performance bridge, transition. Typically 1-1.5 pages.

### Structure
1. **Introduction (150-200 words).** What you bring and why it matters to this customer.
2. **Core capabilities (3-5 bullets).** Each bullet: capability name + one-sentence evidence.
3. **Past performance bridge (2-3 sentences).** Connect capabilities to deployments.
4. **Transition (1 sentence).** Lead into detailed sections.

### Template

```
[COMPANY_NAME] brings [YEARS_OR_DEPTH] of experience in [DOMAIN] to [CUSTOMER_AGENCY]'s
[PROGRAM_OR_MISSION]. Our [PRODUCT_OR_PLATFORM] [WHAT_IT_DOES], enabling [CUSTOMER_BENEFIT].
[COMPANY_NAME] has deployed [PRODUCT_OR_CAPABILITY] across [NUMBER] [CUSTOMER_TYPE] customers,
including [NAMED_CUSTOMER_1] and [NAMED_CUSTOMER_2], delivering [QUANTIFIED_RESULT].

Our approach to [SOLICITATION_TOPIC] is grounded in the following core capabilities:

- **[CAPABILITY_1_NAME].** [WHAT_IT_DOES]. [EVIDENCE: deployment, benchmark, or result].
- **[CAPABILITY_2_NAME].** [WHAT_IT_DOES]. [EVIDENCE: deployment, benchmark, or result].
- **[CAPABILITY_3_NAME].** [WHAT_IT_DOES]. [EVIDENCE: deployment, benchmark, or result].
- **[CAPABILITY_4_NAME].** [WHAT_IT_DOES]. [EVIDENCE: deployment, benchmark, or result].

These capabilities are not theoretical. [COMPANY_NAME] currently supports [ACTIVE_CUSTOMER]
in [RELEVANT_MISSION], where [PRODUCT_OR_CAPABILITY] [DEMONSTRATED_RESULT]. This operational
experience directly informs our approach to [SOLICITATION_REQUIREMENT].

The following sections detail [COMPANY_NAME]'s technical approach, management plan, and
past performance.
```

---

## Technical Approach Introduction Pattern (the "Five Commitments" opener)

Calibrated from winning examples: the technical approach section often opens with a **numbered list of 4-6 high-level commitments** that frame the entire approach before diving into PWS-by-PWS detail. This gives evaluators a one-page mental model of what the offeror is committing to before they have to track section-by-section detail.

### Structure

1. **Opening sentence (1):** State the technical approach in one sentence — name the operating principle.
2. **Commitments list (4-6 numbered items):** Each item starts with a subject phrase (e.g., "Team Octo SMEs will...", "Our engineering team will...", "[Company] will...") + a verb + a specific commitment + a phrase tying back to a customer outcome or a PWS area.
3. **Transition (1-2 sentences):** Bridge to the detailed PWS-by-PWS subsections that follow.

### Template

```
[COMPANY_NAME]'s technical approach for [PROGRAM_NAME] is built on [OPERATING_PRINCIPLE]
that delivers [CUSTOMER_OUTCOME] across all [N] PWS task areas.

1. [Subject phrase] will [verb] [specific commitment 1] using [methodology / asset / partner],
   directly addressing [PWS reference] and supporting [evaluation factor].

2. [Subject phrase] will [verb] [specific commitment 2] [...]

3. [Subject phrase] will [verb] [specific commitment 3] [...]

4. [Subject phrase] will [verb] [specific commitment 4] [...]

5. [Subject phrase] will [verb] [specific commitment 5] [...]

The following subsections describe how each commitment is realized across the [N] PWS task
areas, with traceability to [Section L instruction or PWS reference] in each subsection
heading.
```

### Patterns to apply

1 (theme statement on the opening sentence), 2 (each commitment IS a discriminator + proof point — Phase C citation per commitment when ledger supports it), 4 (ghosting via the "operating principle" — frame in a way that implicitly contrasts a competitor pattern without naming).

### Pitfalls

- **Vague commitments.** "We will use best practices" is not a commitment; it's marketing. Each item must say what specifically gets done.
- **More than 6 commitments.** Loses the "evaluator's mental model" benefit. Compress.
- **Commitment that doesn't tie back to a PWS or eval factor.** If a commitment doesn't help the evaluator score, it's filler.

---

## Technical Approach Subsection Pattern

For each major technical area within the proposal. Repeatable for each requirement cluster.

### Structure
1. **Problem context (1-2 sentences).** What requirement or challenge this subsection addresses.
2. **Solution (3-6 sentences).** What you propose, how it works, key technical details.
3. **Evidence (2-3 sentences).** Past performance, test results, or benchmarks.
4. **Commitment (1-2 sentences).** Specific deliverable, milestone, or performance target.
5. **Takeaway (1 sentence).** The key point for the evaluator.

### Template

```
### [SUBSECTION_TITLE]

[SOLICITATION_REFERENCE] requires [SPECIFIC_REQUIREMENT]. [BRIEF_CONTEXT_FOR_WHY_THIS_MATTERS].

[COMPANY_NAME] addresses this requirement through [APPROACH_NAME], which [HOW_IT_WORKS].
[TECHNICAL_DETAIL_1]. [TECHNICAL_DETAIL_2]. This approach [ADVANTAGE_OVER_ALTERNATIVES]
because [TECHNICAL_RATIONALE].

[COMPANY_NAME] demonstrated this capability at [CUSTOMER_OR_TEST_ENVIRONMENT], where
[PRODUCT_OR_METHOD] [ACHIEVED_RESULT]. [QUANTIFIED_METRIC] confirmed [PERFORMANCE_CLAIM].

Under this effort, [COMPANY_NAME] will deliver [SPECIFIC_DELIVERABLE] by [MILESTONE_DATE],
achieving [PERFORMANCE_TARGET].

This approach gives [CUSTOMER_AGENCY] [ONE_SENTENCE_VALUE_STATEMENT].
```

---

## Management Approach Pattern

Organizational structure, communication, risk management, quality, schedule. Typically 2-4 pages.

### Template

```
## Management Approach

### Organization and Staffing

[COMPANY_NAME] assigns a dedicated [ROLE_TITLE] to lead this effort, supported by
[TEAM_STRUCTURE]. [FIGURE_REFERENCE] shows the organizational structure.

| Role | Responsibility | Qualifications |
|------|---------------|----------------|
| [ROLE_1] | [RESPONSIBILITY] | [QUALIFICATION] |
| [ROLE_2] | [RESPONSIBILITY] | [QUALIFICATION] |
| [ROLE_3] | [RESPONSIBILITY] | [QUALIFICATION] |

### Communication Plan

[COMPANY_NAME] maintains [CADENCE] communication with [CUSTOMER_AGENCY]:

| Activity | Frequency | Format | Participants |
|----------|-----------|--------|-------------|
| Status Report | [FREQUENCY] | [FORMAT] | [WHO] |
| Technical Review | [FREQUENCY] | [FORMAT] | [WHO] |
| Executive Briefing | [FREQUENCY] | [FORMAT] | [WHO] |

Escalation follows a [TIMEFRAME] protocol: [LEVEL_1] resolves within [TIME], unresolved
issues escalate to [LEVEL_2] within [TIME].

### Risk Management

[COMPANY_NAME] identifies and mitigates risks throughout the period of performance:

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [RISK_1] | [L/M/H] | [L/M/H] | [MITIGATION_STRATEGY] |
| [RISK_2] | [L/M/H] | [L/M/H] | [MITIGATION_STRATEGY] |
| [RISK_3] | [L/M/H] | [L/M/H] | [MITIGATION_STRATEGY] |

### Quality Assurance

Deliverables are verified through [QA_PROCESS] before submission. [COMPANY_NAME] applies
[STANDARD_OR_FRAMEWORK] to [WHAT_IS_VERIFIED]. [QUALITY_METRIC] is tracked and reported
in [REPORT_TYPE].

### Schedule

[FIGURE_REFERENCE] presents the program schedule with key milestones:

| Phase | Duration | Key Milestone | Deliverable |
|-------|----------|--------------|-------------|
| Phase 1: [NAME] | [DURATION] | [MILESTONE] | [DELIVERABLE] |
| Phase 2: [NAME] | [DURATION] | [MILESTONE] | [DELIVERABLE] |
| Phase 3: [NAME] | [DURATION] | [MILESTONE] | [DELIVERABLE] |
```

---

## General Information / Section H Pattern (admin and contract-management content)

Federal full proposals — especially IDIQs and task orders — frequently require an admin/operational section addressing FAR Section H clauses + Section L instructions. Calibrated from winning examples, this section typically appears late in the technical volume (after Management Approach, before Past Performance) and contains 8-12 short subsections (≤1 page each).

### Typical subsection set

Pick the subset the solicitation requires; cite the Section L / Section H reference in each heading per the bracketed-reference convention.

```
6.1 Scheduling [Section H.X / L.Y]
6.2 Kickoff Meeting [Section L.Y]
6.3 Transition-In Plan [Section L.Y]
6.4 Performance Management [Section H.X]
6.5 Quality Control [Section H.X]
6.6 Emergency Contingency [Section H.X]
6.7 Contractor Conduct [Section H.X]
6.8 Security [Section H.X]
6.9 Travel (Task Order conditions) [Section H.X]
6.10 OCONUS Travel [Section H.X]
6.11 Employee Conduct [Section H.X]
6.12 Miscellaneous [Section H.X]
```

### Structure (per subsection)

1. **Heading with bracketed reference**
2. **One paragraph** (3-6 sentences) describing the offeror's specific approach to that admin item
3. **Optional bullet list** if the solicitation calls for specific commitments (e.g., kickoff agenda items, transition-in milestones)

### Template (single subsection)

```
### [SUBSECTION_NUMBER] [Topic] [Section H.X / L.Y]

[Company] will [specific action / commitment] [within timeframe / per standard]. [How this is
operationalized: tools, processes, named owners, frequency, integration with other PMP elements].
[Tie back to mission outcome or risk-reduction.]

[OPTIONAL_BULLET_LIST_IF_SOLICITATION_CALLS_FOR_IT]
```

### Patterns to apply

Pattern 2 (discriminator) is light here — most subsections are baseline compliance, not differentiation. Don't force win themes into Section 6.

### Pitfalls

- **Boilerplate templates from prior contracts** — easy to copy/paste old transition-in plans. Update for current solicitation; CO will spot-check.
- **Missing the Section L bracketed ref** — these subsections are most often where evaluators verify Section H/L coverage exists.
- **Over-padding.** Each subsection should be ≤1 page. Section 6 is admin scaffolding, not a place to re-make win themes.

---

## Past Performance Section Pattern

For formal past performance volumes or sections. Repeatable per reference.

### Template

```
## Past Performance

### [PROJECT_NAME]

**Customer:** [AGENCY_AND_OFFICE]
**Contract Number:** [NUMBER]
**Period of Performance:** [START] -- [END]
**Contract Type:** [FFP/T&M/CPFF/etc.]
**Contract Value:** [VALUE]

**Relevance to Current Effort:**
[2-3 sentences explaining why this past performance is relevant to the current solicitation.
Map specific tasks performed to current requirements.]

**Scope of Work:**
[COMPANY_NAME] [PAST_TENSE_DESCRIPTION_OF_WORK]. Key activities included
[ACTIVITY_1], [ACTIVITY_2], and [ACTIVITY_3].

**Results:**
- [QUANTIFIED_RESULT_1]
- [QUANTIFIED_RESULT_2]
- [QUANTIFIED_RESULT_3]

**Point of Contact:**
[NAME], [TITLE]
[ORGANIZATION]
[PHONE] | [EMAIL]

---

[Repeat for each past performance reference]
```

---

## Path Forward / Pilot Plan Pattern

Phased approach with concrete timelines. Typically 1-2 pages.

### Template

```
## Path Forward

[COMPANY_NAME] proposes a [NUMBER]-phase approach to deliver [CAPABILITY] to
[CUSTOMER_AGENCY], with initial capability within [QUICK_START_TIMELINE] of award.

### Phase 1: [PHASE_NAME] ([DURATION], [START_CONDITION])

Within [TIMEFRAME] of [TRIGGER], [COMPANY_NAME] will:
- [ACTION_1] -- [PURPOSE_AND_OUTCOME]
- [ACTION_2] -- [PURPOSE_AND_OUTCOME]
- [ACTION_3] -- [PURPOSE_AND_OUTCOME]

**Exit Criteria:** [WHAT_MUST_BE_TRUE_TO_PROCEED]

### Phase 2: [PHASE_NAME] ([DURATION])

Building on Phase 1 results, [COMPANY_NAME] will:
- [ACTION_1] -- [PURPOSE_AND_OUTCOME]
- [ACTION_2] -- [PURPOSE_AND_OUTCOME]
- [ACTION_3] -- [PURPOSE_AND_OUTCOME]

**Exit Criteria:** [WHAT_MUST_BE_TRUE_TO_PROCEED]

### Phase 3: [PHASE_NAME] ([DURATION])

Full operational deployment includes:
- [ACTION_1] -- [PURPOSE_AND_OUTCOME]
- [ACTION_2] -- [PURPOSE_AND_OUTCOME]
- [ACTION_3] -- [PURPOSE_AND_OUTCOME]

**Steady-State Outcome:** [WHAT_THE_CUSTOMER_HAS_WHEN_COMPLETE]

[FIGURE_REFERENCE] summarizes the timeline and key milestones.
```

---

## Conclusion Pattern

Two paragraphs: opportunity restatement and customer value. Typically 0.5-1 page.

### Structure
1. **Paragraph 1 (3-4 sentences).** Restate the opportunity and your commitment. Reference the solicitation. Summarize your approach in one sentence.
2. **Paragraph 2 (3-4 sentences).** What the customer gains. Concrete outcomes. Close with a call to action or readiness statement. Do not introduce new information.

### Template

```
## Conclusion

[SOLICITATION_REFERENCE] represents [CHARACTERIZATION_OF_OPPORTUNITY] for [CUSTOMER_AGENCY]
to [DESIRED_OUTCOME]. [COMPANY_NAME] is committed to supporting this mission through
[BRIEF_APPROACH_SUMMARY]. Our team brings [KEY_DIFFERENTIATOR] and [YEARS/DEPTH] of
experience in [RELEVANT_DOMAIN].

By selecting [COMPANY_NAME], [CUSTOMER_AGENCY] gains [CONCRETE_OUTCOME_1],
[CONCRETE_OUTCOME_2], and [CONCRETE_OUTCOME_3]. [COMPANY_NAME] is prepared to
[IMMEDIATE_ACTION] within [TIMELINE] of award and welcomes the opportunity to
[NEXT_STEP -- e.g., discuss our approach, demonstrate our platform, begin the pilot].
```
