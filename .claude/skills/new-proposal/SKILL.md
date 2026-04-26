---
name: new-proposal
description: Scaffold a new proposal directory from the standard template. Use when starting a new white paper, proposal, or response. Creates the directory structure, copies boilerplate, and guides initial setup.
---

# New Proposal Skill

## Purpose
Create a clean, ready-to-use proposal workspace for a new effort.

## When to Use
- Starting a new white paper, proposal, or RFI response
- User says "new proposal", "start a proposal", "new white paper", or similar

## Workflow

### Step 1: Gather Basic Info
Ask the user for:
1. **Short name** (used as directory name, e.g., "white-paper-fy26", "agency-rfi", "sbir-phase-i")
2. **Full title** (e.g., "[Your Company] Response to [Customer Program]")
3. **Customer/program** (e.g., "[Customer Office], [Decision Maker Title]")
4. **Due date** (if known)

### Step 1b: Select Proposal Type from Registry

Present the menu of registered proposal types from `reference/proposal-types/`:

```
Which proposal type?
  1. far-rfp           — FAR-Based RFP (full proposal)
  2. idiq-to           — IDIQ / GWAC Task Order Response
  3. cso-brief         — CSO Solution Brief (Phase 1)
  4. cso-full          — CSO Full Proposal (Phase 2)
  5. baa               — Broad Agency Announcement
  6. ota-white-paper   — OTA White Paper
  7. ota-proposal      — OTA Full Proposal (Prototype Project)
  8. sbir-phase1       — SBIR Phase I
  9. sbir-phase2       — SBIR Phase II
 10. white-paper       — White Paper (directed or unsolicited)
 11. rfi               — RFI Response
 12. sources-sought    — Sources Sought Response
 13. rom               — Standalone ROM

If the solicitation doesn't fit any of these, pick the closest and note the deviation
in the proposal brief. Don't invent a new type on the fly — if a new type is genuinely
needed, add it to reference/proposal-types/ first.
```

Read the chosen `reference/proposal-types/<type_id>.md` and display its frontmatter
to the user so they can confirm:

- `display_name`, `solicitation_vehicle`, `page_target`
- `pricing_artifact`, `pp_required`
- `required_skills` (the workflow for this type)
- `skipped_skills` (skills NOT used for this type)
- `evaluator_framing` (mental model for writing)

If the user overrides any field (e.g., "treat this as Full Capture even though it's a
white paper"), note the override in the proposal brief — do not modify the registry
file itself.

### Step 1c: Capture Mode (derived)

Capture mode is **derived from the proposal type** but still overridable:
- Types with `pp_required: true` and a FAR pricing artifact default to **Full Capture**
- All other types default to **Responsive**

Confirm the suggested mode or let the user override.

### Step 2: Create Directory Structure
Create `proposals/[short-name]/` with:
```
[short-name]/
├── inputs/
│   ├── 00_priority/
│   ├── 01_customer/
│   ├── 02_yourCompany/
│   ├── 03_teammates/
│   ├── 04_patterns/
│   ├── 05_graphic_standards/    # brand templates + visual standards (inputs)
│   └── 06_notes/
├── working/
├── drafts/                      # markdown authoring layer
├── graphics/                    # rendered HTML graphics (intermediate output)
├── reviews/
└── final/                       # native Office exports (populated by /export-proposal)
    ├── docx/
    ├── xlsx/
    ├── pptx/
    ├── pdf/
    ├── graphics-png/
    └── PACKAGE.md
```

### Step 3: Seed Boilerplate
Copy these reference files into the appropriate input directories:
- `my-company/company-description.md` → `inputs/02_yourCompany/`
- `my-company/contract-vehicles.md` → `inputs/02_yourCompany/`
- `my-company/past-performance.md` → `inputs/02_yourCompany/`
- `my-company/components-table.md` → `inputs/02_yourCompany/`
- `my-company/capabilities.md` → `inputs/02_yourCompany/` (if present — added in 2026-04-22 consolidation)
- `my-company/distribution-statements.md` → `inputs/00_priority/` (company-specific defaults; the framework's generic copy at `reference/distribution-statements.md` is always available as a fallback)

**Precedence:** `my-company/<file>` is the preferred source. If a file doesn't exist in `my-company/`, the framework's generic version at `reference/<file>` is used as a fallback. If neither exists, skip that file and warn the user that they should run `/setup-company` (or manually populate `my-company/`).

### Step 3b: Seed Proposal Type and Activity Trail

Two files every proposal needs for the type-aware workflow and activity tracking:

1. **Copy the selected type file to the workspace:**
   - Copy `reference/proposal-types/<type_id>.md` → `working/proposal-type.md`
   - This is the authoritative type declaration for this proposal. Every skill reads it.
   - If the user overrode any field in Step 1b, edit the copy (not the registry) to reflect the override and add a `# Overrides` section below the frontmatter documenting what was changed and why.

2. **Seed the activity log:**
   - Copy `templates/working/activity.md` → `working/activity.md`
   - Append the initial entry:
     ```
     ## <today> HH:MM — new-proposal — scaffolded <type_id> workspace → proposals/<short-name>/
     ```

### Step 4: Create Proposal Brief

Create `working/proposal-brief.md`. Note the `Proposal Type` section now *points to* `working/proposal-type.md` rather than re-declaring the type inline (single source of truth).

```markdown
# [Full Title]

## Basics
- **Short name:** [short-name]
- **Customer:** [customer/program]
- **Due date:** [date or TBD]
- **Created:** [today's date]

## Proposal Type
See `working/proposal-type.md` for the authoritative type declaration, required skills, skipped skills, pricing artifact, and evaluator framing. All downstream skills read that file.

- **Type:** [display_name] ([type_id])
- **Capture mode:** [Full Capture / Responsive] (derived from type, overridable here)

## Key Questions to Answer
1. What problem does the customer have?
2. What is our company's unique value for this customer?
3. What specific commitments can we make?
4. What proof points are most relevant?
5. Who is the decision maker?

## Next Steps
Run the workflow for this type. The sequence below is the `required_skills` list from
`working/proposal-type.md`; skills in `skipped_skills` are omitted for this type.

[GENERATED: list `required_skills` from the chosen type file as a numbered list, each with a one-line purpose. Skip anything in `skipped_skills`. At the end add: "Run `/status` at any time to see where you are and what's next."]
```

**Important:** Do NOT paste the generic 11-step workflow. Generate the Next Steps list from the chosen type's `required_skills` so the user sees only what applies to this proposal.

### Step 5: Copy Graphics Templates
Copy branded HTML graphic templates from previous proposals (if they exist) into `inputs/05_graphic_standards/` as starting points. These are **inputs** — reference templates for `/proposal-graphics` to adapt. Rendered output will go to the top-level `graphics/` directory during drafting.
- `graphic-1-three-tier-architecture.html`
- `graphic-2-lifecycle-loop.html`
- `graphic-6-capabilities-table.html`
- `graphic-7-objectives.html`
- `graphic-8-operational-capabilities.html`

These are reusable templates — text content changes per proposal, visual structure stays the same.

### Step 6: Confirm Setup
Tell the user:
1. What was created
2. The selected proposal type and its workflow length (how many skills from `required_skills`)
3. What to drop into `inputs/` next
4. Which skill to run first (the first entry in `required_skills` for this type — usually `/opportunity-quick-look` or `/proposal-manager`, but **not always** — white papers and sources-sought start elsewhere)
5. Remind the user they can run `/status` anytime to see progress

### Step 7: Append to Activity Trail

Append one line to `working/activity.md`:

```
## <timestamp> — new-proposal — <type_id> workspace scaffolded, <N> skills in workflow → proposals/<short-name>/
```

## Rules
- Always create the full directory structure, even if some folders will be empty initially
- Always seed the boilerplate files — they save 30+ minutes per proposal
- Always create the proposal brief — it's the anchor document for the effort
- Always copy a proposal-type.md from the registry — never hand-roll one
- Always seed working/activity.md
- If graphic templates exist from a previous proposal, copy them as starting points
- Generate Next Steps from the type's `required_skills`, never the generic 11-step list
