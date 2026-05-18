---
name: import-from-capture
description: Import a fully-qualified opportunity from the capture-pipeline and scaffold a proposal workspace pre-populated with solicitation facts, Go/No-Go assessment, customer POCs, and competitive intel. Use when a Prospects → Pursuing decision has been made in capture-pipeline and you want to start the proposal without re-typing the context.
phase: setup
composes: [setup-company]
conflicts_with: [new-proposal]  # if no capture-pipeline export exists, use new-proposal instead
---

# Import from Capture

## Purpose

Bridge the handoff between the capture-pipeline (upstream: identify,
qualify, decide to pursue) and the federal-proposal-assistant workspace
(downstream: write the proposal). The capture side already knows the
opportunity intimately — solicitation facts, NAICS, set-aside, scoring,
Go/No-Go assessment, suggested teaming partners, customer POCs, next
steps, and activity history. This skill pulls all of that across in one
shot and pre-populates the proposal workspace so `/proposal-manager`
has capture intel without re-deriving anything.

## When to Use

- A Prospects → Pursuing decision has been made in capture-pipeline
- User says "import this opportunity", "pull in capture intel",
  "start proposal from capture", "import from BD pipeline"
- After the user has clicked **📤 Export for Proposal** on the
  opportunity detail page in capture-pipeline

## Prerequisites

- `/setup-company` has been run (`my-company/` exists)
- User has a capture export JSON file ready. Three ways to get one:
  1. **Download from the web UI**: click the *📤 Export for Proposal*
     button on the opportunity detail page; browser saves a
     `capture-<slug>-<id>.json` file.
  2. **Fetch from a deployed instance URL**: if the user has a
     capture-pipeline URL + opportunity id, this skill can fetch
     the JSON directly via WebFetch (no manual download needed).
  3. **Paste the JSON** into the chat; this skill parses it inline.

## Inputs

One of the three above. The skill accepts:

- A local file path: `./downloads/capture-ai-edge-124.json`,
  `C:\Users\...\Downloads\capture-...\.json`, etc.
- A URL to the export endpoint: `https://bd.example-pipeline.com/opportunity/124/export`
- A JSON payload pasted directly into the chat

## Workflow

### Step 1: Obtain the Capture Payload

Ask the user (skip any that's already provided):

1. Which capture-pipeline instance and opportunity? *(Optional — if
   they give you a URL or file path, proceed.)*
2. File path OR URL OR paste the JSON.

Resolve the input:

- **File path** → use the `Read` tool. Confirm the file exists; if
  not, suggest they re-download from the detail page.
- **URL** → use the `WebFetch` tool. URL must end in
  `/opportunity/<id>/export`. Tell the user that Cloudflare Access
  or app-password auth may block the fetch — if so, they need to
  download via the browser button instead.
- **Pasted JSON** → parse directly from the chat.

Validate:

- Top-level object has `schema_version`, `opportunity`, `scores`.
- `schema_version` starts with `1.` (major-version bump means the
  schema changed and this skill needs updating — warn the user).
- `opportunity.title` is non-empty.

If validation fails: stop, report what's missing, don't proceed.

### Step 2: Propose a Short Name

Derive a short directory name from `opportunity.title` using these
rules:

- Lowercase, replace non-alphanumeric with hyphens, collapse runs
- Truncate to 40 chars
- Drop leading/trailing hyphens

Show the user the proposed short name and confirm before creating
directories. They can override (e.g., shorter, more memorable). This
is the directory under `proposals/` — irreversible without a rename,
so get agreement.

### Step 3: Confirm Capture Mode

Read `my-company/capture-profile.md` if it exists.

Map the capture-pipeline `notice_type` + `scores.rules_status` to a
sensible default:

- SBIR / CSO / OTA / BAA / White Paper (any notice type matching) →
  **Responsive**
- Full & Open RFP / IDIQ Task Order / Recompete → **Full Capture**
- Anything with `rules_status == "sub"` → **Responsive** (we're the
  sub, the prime drives the full capture effort)

Confirm with user before proceeding.

### Step 4: Scaffold the Proposal Directory

Use the **same scaffold contract as `/new-proposal`** — refer to `.claude/skills/new-proposal/SKILL.md` (Steps 2, 3, 3b) for the authoritative layout and seeding logic. Re-stating here only for visibility; if the two ever drift, `/new-proposal` is canonical:

```
proposals/<short-name>/
├── inputs/
│   ├── 00_priority/
│   ├── 01_customer/
│   ├── 02_yourCompany/        ← seed from my-company/ (NOT 02_company)
│   ├── 03_teammates/
│   ├── 04_patterns/
│   ├── 05_graphic_standards/
│   └── 06_notes/
├── working/
├── drafts/
├── graphics/
├── reviews/
└── final/                     ← scaffolded for /export-proposal
    ├── docx/
    ├── xlsx/
    ├── pptx/
    ├── pdf/
    └── graphics-png/
```

Seed `inputs/02_yourCompany/` the same way `/new-proposal` does:

- Copy `my-company/company-description.md`
- Copy `my-company/capabilities.md`
- Copy `my-company/contract-vehicles.md`
- Copy `my-company/past-performance.md`
- Copy `my-company/components-table.md` (if present)

Copy `my-company/distribution-statements.md` → `inputs/00_priority/` (falling back to `reference/distribution-statements.md` if the company-specific version is absent).

### Step 4b: Seed proposal-type.md and activity.md (mandatory — current contract)

**This step was missing in the original import-from-capture flow and is mandatory now.** Without it, downstream skills (`/status`, `/compliance-check`, `/red-team-review`, `/pricing-analyst`, `/export-proposal`) cannot determine the proposal type and will refuse to run.

1. **Determine the proposal type from the capture payload.** The capture payload's `opportunity.notice_type` (or `parent_solicitation_number` pattern) typically maps to a registry type:
   - `Solicitation` / `Combined Synopsis/Solicitation` with FAR clauses → `far-rfp`
   - `Commercial Solutions Opening` (CSO) → `cso-brief` (Phase 1) or `cso-full` (Phase 2)
   - `Broad Agency Announcement` → `baa`
   - `Other Transaction` notices → `ota-white-paper` or `ota-proposal`
   - `SBIR/STTR Topic Notice` → `sbir-phase1` or `sbir-phase2`
   - `Sources Sought` → `sources-sought`
   - `Request for Information` → `rfi`
   - `Request for White Papers` (unsolicited context) → `white-paper`
   - Ambiguous → ask the user, list the registry from `reference/proposal-types/`

2. **Copy the chosen type file:** `reference/proposal-types/<type_id>.md` → `working/proposal-type.md`. Do NOT edit the registry file. If the user overrides anything (e.g., "treat as Full Capture"), add an `# Overrides` section below the frontmatter of the copy only.

3. **Seed `working/activity.md`:** copy `templates/working/activity.md` → `working/activity.md`, then append:
   ```
   ## <timestamp> — import-from-capture — imported opp <opportunity_number> from capture-pipeline, type=<type_id> → proposals/<short-name>/
   ```

If no registry type clearly fits, exit the import with: "Unable to auto-determine proposal type from capture payload. Please run `/new-proposal` manually and pick from the registry." Do not scaffold a workspace without `proposal-type.md`.

### Step 5: Pre-Populate Capture Intel

Write the following files from the capture payload. Each one
contains structured content the downstream skills can read as-is
(no further parsing required).

**`inputs/00_priority/what-matters.md`** — drop in `payload.proposal_kickoff_markdown`
unchanged. The capture-pipeline already rendered this as a clean
markdown summary with opportunity basics, financials, Go/No-Go
assessment, and next steps. `/proposal-manager` reads this first
as its capture-intel anchor.

**`inputs/00_priority/solicitation-facts.md`** — build from `payload.opportunity`:

```markdown
# Solicitation Facts

- **Title:** {opportunity.title}
- **Solicitation #:** `{opportunity.solicitation_number}`
- **Parent CSO/BAA:** `{opportunity.parent_solicitation_number}` (if different)
- **Agency:** {opportunity.agency}
- **Office:** {opportunity.office}
- **Notice type:** {opportunity.notice_type}
- **NAICS:** {classification.naics_code}
- **Set-aside:** {classification.set_aside}
- **Posted:** {opportunity.posted_date}
- **Response deadline:** {opportunity.response_deadline}
- **SAM.gov link:** {opportunity.url}

## Solicitation Summary (from SAM.gov)

{opportunity.summary}

## Description

{opportunity.description}
```

**`inputs/01_customer/customer-pocs.md`** — from `payload.next_steps.customer_pocs`:

```markdown
# Customer POCs (from capture intel)

These were identified during the capture phase. The `/customer-intel`
skill will enrich this with agency mission, buying history, and
relationship gaps.

{for each POC:}
## {poc.name} — {poc.title}

- **Role in process:** {poc.role_in_process}
- **Source:** {poc.source}  _(solicitation = named in RFP; inferred = surfaced by AI)_
- **Notes:** {poc.notes}
```

Skip this file if `next_steps.customer_pocs` is empty.

**`inputs/03_teammates/suggested-partners.md`** — from `payload.next_steps.partners`:

```markdown
# Suggested Teaming Partners (from capture intel)

AI-generated candidates from the capture-pipeline's quick-vet.
Review critically — these are hints, not commitments.

{for each partner:}
## {partner.name} — {partner.role} ({partner.strength} fit)

{partner.rationale}
```

Skip if empty.

**`working/capture-intel.json`** — save the full JSON payload
unchanged. Provides a durable audit trail and lets any future
skill re-parse the original capture context if it needs detail
that didn't make it into the rendered markdown.

### Step 6: Write the Proposal Brief

Write `working/proposal-brief.md` using the standard template
(see `/new-proposal`), but pre-fill what the capture payload
knows:

```markdown
# {opportunity.title}

## Basics
- **Short name:** <short-name>
- **Proposal type:** <inferred — SBIR / CSO / OTA / BAA / etc. — from notice_type>
- **Customer:** {opportunity.agency} / {opportunity.office}
- **Due date:** {opportunity.response_deadline}
- **Created:** {today}
- **Source:** Imported from capture-pipeline (opp id {opportunity.id})

## Capture Mode
**<Responsive | Full Capture>**  ← confirmed in Step 3

## Capture Context
- **Rules score:** {scores.rules_score} ({scores.rules_status})
- **AI fit score:** {scores.llm_score}/10 — {scores.llm_action}
- **Prime feasibility:** {assessment.prime_feasibility.verdict}
- **Sub feasibility:** {assessment.sub_feasibility.verdict}
- **Technical alignment:** {assessment.technical_alignment.verdict}
- **Competitive position:** {assessment.competitive_position.verdict} (incumbent risk: {assessment.competitive_position.incumbent_risk})

## Financial Shape (AI-inferred, confirm before pricing)
- **Estimated TCV:** {financials.tcv_display}
- **Period of performance:** {financials.period_of_performance.value}
- **Contract vehicle:** {classification.contract_vehicle.value}
- **Incumbent:** {context.incumbent.value}

## Key Questions
1. What problem does the customer have?
2. What is our unique value for this customer?
3. What specific commitments can we make?
4. What proof points are most relevant?
5. Who is the decision maker?

## Next Steps
1. Review `inputs/00_priority/what-matters.md` — the capture Go/No-Go
   assessment and next-step recommendations are there.
2. Drop the full solicitation PDF into `inputs/00_priority/` (the
   capture payload has the SAM.gov summary but not the full text).
3. Run `/customer-intel` to enrich POCs with agency mission and
   buying history.
4. Run `/proposal-manager` to analyze the solicitation and build the
   compliance framework. It will read the capture intel automatically.
5. Continue the standard workflow (architect → past performance →
   pricing → graphics → writer → red team).
```

### Step 7: Confirm and Report

Tell the user:

1. What was created and where.
2. What files were pre-populated vs. still empty.
3. What's missing that they should add:
   - Full solicitation PDF (the capture summary is a truncated excerpt)
   - Any additional customer context they have from prior
     relationships that the LLM couldn't know
   - Teammate POCs or agreements
4. Which skill to run next — usually `/proposal-manager` directly
   (capture intel is richer than a cold start, so we can skip
   `/customer-intel` on the first pass).

## Rules

- **Never overwrite an existing `proposals/<short-name>/` directory.**
  If the short name collides, suggest an alternative and confirm.
- **Preserve the full capture JSON** in `working/capture-intel.json`
  for downstream reference — don't discard data because a specific
  skill doesn't need it today.
- **Don't fabricate** fields missing from the payload. If
  `assessment` is null, say so in the brief ("Capture assessment not
  available — run AI Score on the opportunity in capture-pipeline and
  re-export"); don't generate a fake one.
- **Respect AI-inferred source tags.** Fields with
  `source: ai_quickvet` should be flagged as needing confirmation in
  the proposal brief and working files — they're starting points, not
  facts.

## Output Format

At the end, emit a compact status summary:

```
✅ Imported opportunity #124 "AI for Tactical Edge Decision Support"
   Workspace: proposals/ai-tactical-edge-decision-support/
   Capture mode: Responsive (SBIR)

   Pre-populated from capture:
   • inputs/00_priority/what-matters.md          ← Go/No-Go + Next Steps
   • inputs/00_priority/solicitation-facts.md    ← Title, agency, NAICS, deadline
   • inputs/01_customer/customer-pocs.md         ← 2 POCs (1 from solicitation, 1 inferred)
   • inputs/03_teammates/suggested-partners.md   ← 3 AI-suggested primes
   • working/capture-intel.json                  ← Full raw JSON payload
   • working/proposal-brief.md                   ← Pre-filled brief with capture context

   Seeded from my-company/:
   • inputs/02_yourCompany/company-description.md
   • inputs/02_yourCompany/capabilities.md
   • inputs/02_yourCompany/contract-vehicles.md
   • inputs/02_yourCompany/past-performance.md

   Still needed from you:
   • Full solicitation PDF → inputs/00_priority/solicitation.md (or .pdf)
   • Any prior customer relationship context → inputs/01_customer/
   • Teammate commitments / LOAs → inputs/03_teammates/

   Next skill to run: /proposal-manager
```
