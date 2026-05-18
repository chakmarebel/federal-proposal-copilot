---
name: proposal-manager
description: Use this skill to analyze a solicitation and build a proposal plan before solution design begins. Extracts response type, page limits, section structure, evaluation criteria, win themes, and bid/no-bid assessment. Reads from inputs/ and writes to working/proposal-plan.md.
phase: planning
composes: [opportunity-quick-look, capture-portal-structure]
conflicts_with: []  # central planning hub; sole producer of proposal-plan.md + compliance-matrix seed
---

# Proposal Manager Skill

## Purpose
Bridge the gap between a blank proposal workspace and the technical solution design. Before the architect designs anything and before the writer drafts anything, this skill reads the solicitation and produces a complete proposal plan that governs every subsequent step.

## When to Use
- A solicitation, RFP, RFI, white paper request, BAA, or CSO has been dropped into `inputs/00_priority/`
- User says "analyze the solicitation", "build the proposal plan", or runs this after `/new-proposal`
- Immediately after `/new-proposal` and before `/proposal-solution-architect`

## Inputs
Read in this order:
1. `working/proposal-type.md` — **read first.** Declares `compliance_sources` (which parts of the solicitation drive the compliance matrix), `pricing_artifact`, `evaluator_framing`, and `submission_mechanism`. If missing, instruct user to run `/new-proposal` and stop.
2. **Portal format gate.** If `working/proposal-type.md` declares `submission_mechanism: web-form`:
   - Check for `inputs/00_priority/portal-format.md`. If absent, exit immediately with: "Submission is to a web-form portal but no portal format has been captured. Run `/capture-portal-structure` first — it either inherits a known portal from `reference/portal-formats/` or guides you through a first-time capture after you register on the portal. Without this, I cannot produce a valid proposal plan because the real section structure and character limits are unknown."
   - If present, read it. The portal's section labels and character limits become the authoritative structure for this proposal plan; they override whatever section list the solicitation PDF implies.
   - Also read `working/section-budgets.md` (produced by `/capture-portal-structure`) if present — this is what `/proposal-writer` will use for per-section budget-first drafting.
3. `working/submission-summary.md` — **the confirmed deliverable spec (produced by `/submission-summary`).** Authoritative source for response format, volume/section structure, page limits, pricing artifact, and due date. Use it for Step 2 instead of re-extracting. If it is missing, recommend the user run `/submission-summary` first.
4. All files in `inputs/00_priority/` — solicitation, evaluation criteria, instructions to offerors (excluding `portal-format.md`, already read above if applicable)
5. All files in `inputs/01_customer/` — customer context, mission, constraints
6. `working/proposal-brief.md` — created by `/new-proposal`
7. `reference/narrative-operating-modes.md` — use `page_target`, `submission_mechanism`, and `evaluator_framing` to recommend the proposal's prose mode.

If `inputs/00_priority/` is empty, tell the user to drop the solicitation there first and stop.

**Skip check:** If this skill appears in `skipped_skills` of the proposal type (it shouldn't for any type in the registry, but check anyway), exit with "Skipped for type <type_id>."

## Workflow

### Step 1: Classify the Opportunity
Determine:
- **Response type:** RFP / RFQ / RFI / White Paper / BAA / SBIR / STTR / OTA / CSO
- **Evaluation approach:** Best Value / LPTA / Fixed-price / Sole-source / Advisory
- **Competition type:** Full & Open / Small Business Set-Aside / Sole Source / Task Order
- **Contract type if applicable:** FFP / CPFF / T&M / IDIQ
- **Incumbent advantage:** Is there a known incumbent? Who?
- **Page/volume constraints:** Hard limits, if any

### Step 2: Extract Response Requirements

**If `working/submission-summary.md` exists, it is authoritative.** Copy its submission profile and volume/section breakdown into the proposal plan rather than re-extracting. The extraction guidance below applies only when the summary is absent — and in that case, recommend the user run `/submission-summary` first.

**If `submission_mechanism: web-form`** (and `inputs/00_priority/portal-format.md` has been read): pull section structure, labels, and character/word limits from the portal format file — NOT from the solicitation PDF. The solicitation describes the opportunity; the portal format describes the actual submission mechanics. Where they conflict, the portal format wins.

Pull from the portal format:
- Portal section list with labels and hard character/word limits (the `working/section-budgets.md` table)
- Required metadata fields (title length, TRL selector, system type enum, etc.)
- Image/attachment rules
- Agreements and opt-outs requiring human decisions
- Submission mechanics (save-and-resume, edit-after-submit, confirmation)

**If `submission_mechanism: document-upload` or `email`**: pull from the solicitation:
- Required sections/volumes and their page limits
- Required fonts, margins, file formats
- Required attachments (past performance forms, resumes, certifications)
- Proposal due date, submission method, and POC
- Any questions/clarifications deadline

### Step 3: Build the Compliance Framework
Create a table of every stated requirement the proposal must address:

| ID | Requirement | Source (Section) | Mandatory/Desired | Addressed By | Notes |
|----|-------------|-----------------|-------------------|--------------|-------|

Flag:
- Requirements with no obvious capability match → will become gaps for the architect
- Ambiguous requirements that need assumption documentation
- Requirements that imply certifications, clearances, or registrations we must confirm

### Step 3b: Seed the Compliance Matrix

The compliance framework above is the **analysis view**. The compliance matrix is the **living artifact** that the writer and compliance-check will maintain through submission. Seed it now.

1. Copy `reference/compliance-matrix-template.md` → `working/compliance-matrix.md` if it does not already exist.
2. Scope the matrix to the `compliance_sources` declared in `working/proposal-type.md`. Only extract rows from those sources (e.g., if `compliance_sources: [L, M]`, do not seed rows from the PWS unless PWS is also listed).
3. For each "shall" statement or scored evaluation factor in those sources, add one row:
   - **Req ID:** stable identifier (e.g., `L.3.2.1`, `M.2`, `PWS.4.5` — use the solicitation's own numbering where possible)
   - **Source:** which compliance source (L / M / PWS / SOW / EvaluationCriteria / SOO)
   - **Requirement:** verbatim text, trimmed to ≤200 chars (don't paraphrase)
   - **Section:** tentative section assignment (Technical Vol §3.2, Management Vol §2.1, etc.) — this is a recommendation; the architect and writer may reassign
   - **Page:** leave blank (filled by writer)
   - **Status:** `Planned`
   - **Evidence:** blank (filled by writer)
4. If the proposal type declares `compliance_sources: []` (white-paper, rfi, rom, sources-sought), **do not create a matrix**. Note in the proposal plan that compliance tracking is not applicable for this type.

### Step 4: Analyze Evaluation Criteria
Extract all stated evaluation factors and subfactors:

| Factor | Subfactor | Weight / Order of Importance | Evaluation Standard | Your Strength |
|--------|-----------|------------------------------|--------------------|--------------------|

Note:
- Which factors are most heavily weighted
- Which factors are easy wins vs. competitive battlegrounds
- Whether price is evaluated separately or as a factor in best value

### Step 5: Prime vs. Sub Decision
Before scoring bid/no-bid, make the prime vs. sub call. This shapes every downstream decision — competitive strategy, teaming, pricing, and proposal structure all differ fundamentally based on this.

**Bid as Prime when:**
- Your company has the customer relationship and technical lead
- You can credibly perform the majority of work (typically 51%+)
- You have relevant past performance at comparable scope and dollar value
- Winning as prime advances your strategic positioning in this customer/domain

**Bid as Sub when:**
- A large prime has the customer relationship and you do not
- Your capability fills a specific gap in their solution but you can't cover the full scope
- The contract value or complexity exceeds your current capacity as prime
- Subcontracting builds a customer reference you can prime a follow-on

**Conditional: Sub with intent to Prime the follow-on** — a valid strategy for early-stage companies. Document this intent explicitly.

Record the decision: **PRIME / SUB / PRIME-SUB TEAMING (co-prime) / CONDITIONAL**

If bidding as sub: note which prime(s) to approach and what work share your company brings to the team.

---

### Step 6: Bid/No-Bid Assessment
Score each factor and produce a recommendation. For **prime bids**, all factors apply. For **sub bids**, skip factors marked *(prime only)*.

| Factor | Question | Score (1-5) | Notes |
|--------|---------|-------------|-------|
| Technical alignment | Do we have capabilities that directly address the core requirements? | | |
| Customer alignment | Have we worked with this specific program office or below? *(prime only)* | | |
| Relevant experience | Do we have past performance at equivalent scope and dollar value? *(prime only)* | | |
| Incumbency | Is the incumbent vulnerable? Are we positioned to unseat them? *(prime only)* | | N/A if no incumbent |
| Customer mission familiarity | Do we understand this customer's specific mission domain (C2, ISR, logistics, etc.)? | | |
| Contract size fit | Is the contract value appropriate for our current scale and capacity? *(prime only)* | | |
| Competitive position | Can we win against likely competitors in this role? | | |
| Customer relationship | Do we know the decision maker or have a path to them? | | |
| Pricing competitiveness | Can we price to win at an acceptable margin? | | |
| Resource availability | Do we have the people to execute the work AND write the proposal? | | |
| Strategic value | Does winning this advance our positioning in this customer/domain? | | |

**Scoring:** 5=strong yes, 4=likely yes, 3=neutral/uncertain, 2=likely no, 1=significant gap

**Threshold guidance:**
- Average ≥ 4.0 → BID
- Average 3.0–3.9 → CONDITIONAL BID (state conditions)
- Average < 3.0 → NO-BID
- Any single factor scored 1 → flag as a blocking risk before proceeding

**Recommendation:** BID / NO-BID / CONDITIONAL BID (with conditions stated)

### Step 7: Define Win Themes
Write 3-5 win themes. Each must:
- Map directly to an evaluation factor
- Reference a specific company capability or proof point
- Be expressible in one sentence

Format:
| Theme | Evaluation Factor | Proof Point |
|-------|------------------|-------------|

### Step 8: Write the Proposal Plan
Write all findings to `working/proposal-plan.md` using this structure:

```markdown
# Proposal Plan — [Proposal Name]

## Opportunity Classification
- Type:
- Evaluation approach:
- Competition:
- Contract type:
- Incumbent:
- **Prime vs. Sub decision:** [PRIME / SUB / CO-PRIME / CONDITIONAL]
- **If sub:** Target prime(s) and your company's work share:

## Response Requirements
- Due date:
- Submission method:
- Questions deadline:
- Page limits: [by volume/section]
- Format requirements:
- Required attachments:
- POC:

## Compliance Framework
[compliance table]

## Evaluation Criteria Analysis
[evaluation table]

## Bid/No-Bid Assessment
[scoring table]
**Recommendation:**

## Win Themes
[win themes table]

## Open Questions / Assumptions
[list of ambiguities to resolve before writing]

## Recommended Proposal Structure
[include the recommended narrative operating mode and why it fits this opportunity]
[proposed outline with section owners and page budget]
```

## Output Files

Produce **all three** on every successful run:

1. **`working/proposal-plan.md`** — the narrative plan (human-readable)
2. **`working/proposal-plan.json`** — structured sidecar conforming to [`reference/schemas/proposal-plan.schema.json`](../../../reference/schemas/proposal-plan.schema.json) (machine-readable; consumed by dashboard + downstream skills)
3. **`working/compliance-matrix.md`** — living traceability artifact (unless `compliance_sources` is empty for this type)

The `.md` and `.json` forms must stay in sync on every invocation — write both atomically. Humans can edit the markdown freely; on the next `/proposal-manager` run, the JSON is regenerated. If a user hand-edits the JSON, that edit is preserved only until the next run.

### Schema-compliant JSON sidecar

When writing `working/proposal-plan.json`, include:
- `schema_version: "proposal-plan.v1"` (exact string)
- `generated_by: "proposal-manager"`
- `generated_at`: current ISO-8601 timestamp
- `proposal_name`, `type_id` (from `working/proposal-type.md`)
- `narrative_operating_mode` with `mode`, `rationale`, and `primary_reader_need` from `reference/narrative-operating-modes.md`
- `classification`, `response_requirements`, `evaluation_factors`, `win_themes`, `discriminators`, `ghosting_targets`, `bid_nobid`, `assumptions`, `open_questions`, `due_date`, `customer_name`, `agency`

Every `evaluation_factor`, `win_theme`, and `discriminator` gets a stable `id` (e.g., `EF-1`, `WT-1`, `DS-1`) so other skills and the dashboard can reference them.

See the schema file for field definitions, enum values, and validation rules.

## Activity Trail

On completion, append to `working/activity.md` (one line):

```
## <timestamp> — proposal-manager — <N requirements seeded>, <M eval factors>, bid/no-bid: <GO/NO-GO/CONDITIONAL> → working/proposal-plan.md + working/proposal-plan.json + working/compliance-matrix.md
```

Also append one JSON line to `working/ai-runs.jsonl` per [`reference/schemas/ai-run.schema.json`](../../../reference/schemas/ai-run.schema.json) with `job_type: "planning"`. If the skill made multiple model calls (e.g., one for extraction, one for win-theme generation), log each one.

## Rules
- Pull every requirement directly from the solicitation text — do not invent or assume
- Flag every gap explicitly; the architect will address them
- Win themes must connect to specific proof points, not general claims
- If evaluation weights are not stated, infer priority from order listed and section prominence
- If this is a white paper with no formal evaluation criteria, infer criteria from the stated purpose and decision maker

## After Running This Skill
Tell the user:
1. Bid/no-bid recommendation with rationale
2. Top 3 compliance risks (requirements with no obvious match)
3. Win theme summary
4. Suggested next step: `/proposal-solution-architect`

## Lessons Learned

### On White Papers
- White papers rarely state explicit evaluation criteria — infer from the office, the stated problem, and the decision maker's known priorities. For SOCPAC-type submissions, operational utility and DDIL compatibility were the implied discriminators even though never stated.
- For CDAO/DIU-type solicitations, evaluation innovation and mission-representative benchmarking matter more than past performance volume.

### On Win Themes
- Generic themes ("we're the best") fail. Win themes must be specific: "[Model Name] matches [Competitor Model] on military tasks while running air-gapped on a laptop" is a win theme. "We have deep military AI expertise" is not.
- Three themes is usually the right number. Five or more dilutes focus.

### On Compliance Frameworks
- Government evaluators score compliance before they score merit. A technically brilliant proposal that misses a formatting requirement or skips a required section can be disqualified outright.
- Build the compliance table first — before writing a single word of the proposal.
