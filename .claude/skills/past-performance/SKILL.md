---
name: past-performance
description: Use this skill to map your company's past performance repository to current evaluation criteria, identify the most relevant entries, draft PPQ-style narratives, and produce a past performance volume or section. Reads from my-company/past-performance.md (or inputs/02_yourCompany/past-performance.md if seeded there by /new-proposal) and writes to drafts/past-performance.md.
phase: drafting
composes: [proposal-manager]
conflicts_with: []  # unique drafting role
---

# Past Performance Skill

## Capture Mode
**Read `working/proposal-brief.md` before proceeding.** Check:
- `Capture Mode:` — Full Capture or Responsive
- `Proposal type:` — determines the expected past performance format

- **Full Capture** → run the complete workflow below (formal PPQ blocks, relevance matrix, past performance volume)
- **Responsive** → skip to [Responsive Mode](#responsive-mode) at the bottom of this skill

If the field is blank, ask the user before proceeding.

## Purpose
Transform your company's past performance record into proposal-ready narratives that directly address the evaluator's scoring criteria. Past performance is both a scored factor (when required) and a credibility multiplier across every other section — it converts claims into proof.

## When to Use
- Solicitation requires a past performance volume or section
- Past performance is a scored evaluation factor
- Any proposal section where capabilities need to be substantiated with evidence
- Run after `/proposal-manager` (need eval criteria) and in parallel with `/proposal-writer`

## Inputs
Read before starting:
1. `working/proposal-plan.md` — past performance evaluation criteria, scoring approach, number of references required, recency requirements (typically 3–5 years)
2. `my-company/past-performance.md` — your company's master past performance repository
3. `working/capability-matrix.md` (if exists) — to map PP entries to required capabilities
4. `inputs/00_priority/` — solicitation for any specific PPQ form requirements or formatting

## Step 1: Audit the Repository
Read `my-company/past-performance.md` and assess what's there vs. what evaluators need:

**What evaluators typically require per reference:**
- Contract number / award number
- Contract value (total and/or annual)
- Period of performance (start → end dates)
- Customer agency and POC (name, phone, email)
- Scope / description of work
- Relevance to current opportunity (scope, complexity, dollar value)
- Performance outcomes / CPAR rating equivalent
- Measurable results (quantified where possible)

**Flag any entries missing required fields.** Tell the user what gaps exist and ask them to fill in what they can before drafting narratives. Present as a structured request:

```
The following past performance entries are missing information needed for full PPQ narratives.
Please provide what you can:

[Entry: [Customer A Unit 1] — SOF AI Pilot]
- Contract number: [needed]
- Contract value: [needed]
- Period of performance: [needed]
- Government POC: [needed]
- Measurable outcomes: [needed — e.g., reduction in mission planning time, user adoption rate, assessment results]

[Entry: [Customer B] — [Program Name]]
- Contract number: [needed]
- Contract value: [needed]
- Period of performance: [needed]
- Government POC: [needed]
- Measurable outcomes: [needed]
```

Proceed with drafting using whatever information is available. Clearly mark fields as [TO BE PROVIDED] where data is missing.

## Step 2: Map Entries to Evaluation Criteria
Using the evaluation criteria from `working/proposal-plan.md`, score each past performance entry for relevance:

| PP Entry | Eval Factor 1 | Eval Factor 2 | Eval Factor 3 | Overall Relevance | Recency |
|----------|--------------|--------------|--------------|-------------------|---------|
| [Customer A Unit 1] | High / Med / Low | | | | Within 3yr? |
| [Customer B] | | | | | |
| [Research Agreement 1] | | | | | |
| [etc.] | | | | | |

**Selection criteria:**
- Prioritize entries with HIGH relevance to the most heavily weighted evaluation factors
- Prioritize recent (within 3–5 years, per solicitation recency requirement)
- Prioritize entries with quantifiable outcomes
- Match the number of references to the solicitation requirement (typically 3–5)

Recommend which entries to include and which to hold in reserve.

## Step 3: Draft PPQ Narratives
For each selected past performance entry, draft a narrative using this structure:

**Format 1: Standard PPQ Block (for past performance volume)**
```
CONTRACT INFORMATION
Contract/Award Number: [number or TO BE PROVIDED]
Contracting Agency: [agency name]
Contract Value: [$ value or TO BE PROVIDED]
Period of Performance: [start] – [end]
Contract Type: [FFP / CPFF / T&M / Other Agreement]
Government POC: [name, phone, email — or TO BE PROVIDED]

SCOPE OF WORK
[2–3 sentences: what your company did, for whom, in what operational context]

RELEVANCE TO CURRENT REQUIREMENT
[1–2 sentences: explicitly map scope/complexity/dollar value to the solicitation's relevance standard]

PERFORMANCE OUTCOMES
[3–5 bullet points of measurable results:
- Deployed [X] models to [Y] operational units within [timeframe]
- Achieved [metric] on military benchmark [benchmark name]
- Received [rating/feedback] from [government POC/evaluator]
- [other quantified outcome]
]
```

**Format 2: Narrative Summary (for capability section or executive summary)**
```
[Company] has [deployed / delivered / demonstrated] [capability] for [customer] [context].
[Specific outcome with metric if available.] [Why this is relevant to the current requirement.]
```

## Step 4: Draft the Past Performance Volume/Section
Structure depends on solicitation requirements. Default structure:

```markdown
# Past Performance

## Summary
[2–3 sentences: number of references, types of work, overall performance record]
[Your Company] has [X] active operational deployments and [Y] active research agreements
across [customer types]. All programs are currently active and operational.

## Reference [1]: [Customer Name — Program Name]
[PPQ block]

## Reference [2]: [Customer Name — Program Name]
[PPQ block]

## Reference [3]: [Customer Name — Program Name]
[PPQ block]

## Research Agreements and Collaborative Programs
[Brief table or narrative of research agreements — these demonstrate
technical credibility and government endorsement even if not scorable PP references]

## Published Research
[1 paragraph: reference published benchmark papers as evidence of technical
depth and peer-reviewed capability validation — cite my-company/published-research.md]
```

## Output Files
**Always write to disk — do not just display in chat.**

- `drafts/past-performance.md` — complete past performance section/volume
- `working/pp-relevance-matrix.md` — relevance mapping table (if useful for the team)

## Guidance on Framing Past Performance

### How to Frame Each Deployment Type

**SOF / Special Forces Deployments:**
- Frame as: operational deployment in the most demanding, resource-constrained environment in the US military
- Emphasize: disconnected operations, mission-critical reliability, operator adoption
- Relevance argument: "If it works for Special Forces in the field, it works for any military application"

**Conventional Force Deployments:**
- Frame as: deployment at scale, demonstrating broader applicability beyond SOF
- Emphasize: integration with existing C2 infrastructure, multi-unit deployment

**Research Agreements:**
- These are NOT scored past performance references for most solicitations
- Do include them in capability sections as evidence of government endorsement and co-development partnerships
- Frame as: "active collaboration with [lab] to advance [specific research area]"

**Published Research:**
- Not past performance in the traditional sense, but powerful credibility evidence
- Use in the past performance section's opening narrative and in capability descriptions
- Key claims: relevant benchmarks, model performance comparisons

### Handling Thin Past Performance
Early-stage companies have a strong but limited record. When past performance is a heavy evaluation factor:
- Lead with operational deployments — these are real, operationally validated
- Supplement with research agreements as evidence of government trust
- Use published benchmarks as proxy credibility
- Be explicit about recency
- Consider whether a teaming partner's past performance can fill scope gaps

### Procurement Status
Always include in past performance section when relevant:
- Any marketplace "Awardable" status (e.g., [Procurement Vehicle]) — enables direct procurement, signals government vetting

## Rules
- Never fabricate contract numbers, values, ratings, or POC information
- Mark every missing field clearly as [TO BE PROVIDED] — do not estimate or guess
- Quantify outcomes wherever possible; "improved performance" is not a result
- Relevance must be explicitly argued — evaluators won't make the connection for you
- Match the number of references to what the solicitation requires — do not include more
- If recency requirement (e.g., "within 3 years") cannot be met by a reference, flag it before including

---

## Responsive Mode

For SBIR, CSO, OTA, BAA, and white papers — past performance is usually framed as **Relevant Experience** rather than a scored, formal volume. The goal is credibility, not compliance.

Operational pilots with real end users and active research agreements are ideal for these vehicles. Evaluators in innovation programs want to see real-world use, not contractor performance ratings.

### What to Call It
- SBIR / BAA: **"Team Qualifications and Relevant Experience"** — not "Past Performance"
- CSO / OTA: **"Prior Work and Operational Validation"** — evaluators want proof of concept, not PPQs
- White Paper: **"[Your Company] — Operational Track Record"**

### Responsive Workflow

**Step 1:** Read `my-company/past-performance.md` and identify all relevant deployments, research agreements, and published research.

**Step 2:** Match entries to what the customer values (from `working/proposal-plan.md` or stated evaluation criteria). For responsive vehicles, relevance usually means:
- Has it been tested in the relevant environment? (DDIL, air-gapped, tactical, operational)
- Have real end users adopted it? (Operators, not just lab evaluators)
- Is there a government institution willing to vouch for it? (Research agreement = endorsement)

**Step 3:** Draft a narrative "Relevant Experience" section — no tables, no contract numbers required unless specified:

```markdown
## Relevant Experience and Operational Validation

[Your Company] has [X] active operational deployments and [Y] active government research
partnerships. All programs are ongoing.

**Operational Deployments**
[Your Company] is currently deployed with [multiple units] across [Customer A]
and the SOF schoolhouse — where it supports mission planning and knowledge management
in operationally representative environments.
[Your Company] is also deployed with [Customer B] under the [Program Name] program,
demonstrating applicability beyond SOF to conventional force operations.

These deployments represent the most demanding operational test environment available:
resource-constrained, frequently disconnected, and mission-critical. The fact that special
operations units have adopted [Your Company] as a mission tool — not just evaluated it in a lab —
validates the approach in a way that no laboratory benchmark can replicate.

**Government Research Partnerships**
[Your Company] holds active research agreements with:
- [Research Agreement 1]
- [Research Agreement 2]
- [Additional research collaborations as applicable]

These agreements represent formal government endorsement of the research direction
and provide co-development pathways for mission-specific model adaptation.

**Published Research**
[Your Company] has published peer-quality research papers directly relevant to this effort:
- *[Benchmark Paper 1]* — first benchmark dataset for measuring military LLM refusal rates; demonstrates
  that commercial AI models refuse up to 98.2% of legitimate military queries
- *[Model Name]* — demonstrates [Competitor Model] parity on military task performance while running
  locally on edge hardware, with no statistically significant regression on general benchmarks

**Procurement Status**
[Your Company] holds [Procurement Vehicle] "Awardable" status, enabling direct procurement by
government customers without a separate competitive process.
```

**Step 4:** Write to `drafts/past-performance.md`.

### Responsive Rules
- Do not use "CPAR", "PPQ", or "Past Performance Questionnaire" language — it implies a scored formal process that doesn't apply
- Do not include contract numbers unless the vehicle specifically asks for them
- Quantify outcomes wherever possible ("three SFGs" not "multiple units")
- Frame pilots as operational validation, not beta testing
- Always include published research and research agreements as credibility evidence

---

## After Running This Skill
Tell the user:
1. Which past performance entries were selected and why
2. What fields are missing and need to be provided before final submission
3. Any relevance gaps — evaluation factors with no matching past performance
4. Confirm that `drafts/past-performance.md` was written
