---
name: capture-portal-structure
description: Capture the section structure, character/word limits, metadata fields, and submission mechanics of a web-form submission portal before drafting. Run when working/proposal-type.md declares submission_mechanism web-form. Writes inputs/00_priority/portal-format.md and working/section-budgets.md.
phase: capture
composes: [opportunity-quick-look]
conflicts_with: []  # only producer of portal-format.md; only runs for web-form submissions
---

# Capture Portal Structure Skill

## Purpose
Capture the actual section structure, character/word limits, metadata fields, and submission mechanics of a web-form submission portal — **before** drafting narrative. Prevents the expensive failure mode where a proposal is drafted against an assumed structure and then discovered to require wholesale compression or rewriting when the real portal limits are revealed.

Produces both a proposal-local artifact (`inputs/00_priority/portal-format.md`) and, for novel portals, a draft entry for the framework-wide library at `reference/portal-formats/<portal-id>.md`.

## When to Use
- A new proposal is being scaffolded and `working/proposal-type.md` declares `submission_mechanism: web-form`
- `/opportunity-quick-look` flagged the submission as going through a registration-gated portal (DIANA, DIU CSO Phase 1, some SBIR topic portals, Challenge.gov, AFWERX Open Topic, xTech, NSIN prizes, Valid Evaluation, etc.)
- User says "capture the portal structure", "set up the format reference", or has just registered for a portal and wants to seed format data

## When NOT to Use
- Submission is via email or SAM.gov PDF upload — in those cases Section L of the solicitation is the format authority and `/proposal-manager` extracts it directly
- Portal is just a file-upload mechanism with no unique section structure — same as above
- Opportunity has not yet been triaged (`/opportunity-quick-look`) — do that first

## Inputs

Read in this order:

1. `working/proposal-type.md` — confirm `submission_mechanism: web-form`. If absent or set to something else, ask the user whether to proceed anyway.
2. `working/quick-look.md` — pick up the portal name and registration notes (if quick-look captured them).
3. `reference/portal-formats/` — check whether a format for this portal already exists. **If it does, the short path is:**
   - Read the existing reference file
   - Copy it to `inputs/00_priority/portal-format.md` with a header note: "Inherited from `reference/portal-formats/<portal-id>.md` on YYYY-MM-DD. Verify against live portal before drafting."
   - Tell the user to spot-check the live portal and flag any changes
   - Exit — no need to re-capture a known portal

## Workflow (novel portal, no reference file exists)

### Step 1: Confirm the user has registered

The portal structure cannot be captured without access. Ask:

> "Have you registered for the [portal name] portal and can you see the submission form? If not, complete registration first — the public-facing challenge/solicitation page doesn't show the actual section structure."

If no, stop and ask the user to register, then resume.

### Step 2: Guided capture

Walk the user through the portal submission form section by section. For each piece of information the portal collects, ask the user to paste or describe what they see. Capture to `inputs/00_priority/portal-format.md` using the structure in `reference/portal-formats/_template.md`. At minimum:

1. **Portal metadata fields.** Every top-level input that isn't narrative content — title, TRL, system type, agency selector, keywords, etc. Capture field name, type (text/select/number), any enum values, character limit.
2. **Sections.** Each narrative section the portal expects. Capture:
   - Section ID and portal label (use the portal's exact wording)
   - Character limit or word limit (confirm including/excluding spaces — test with a filler string if unclear)
   - Instructions text (copy verbatim from the portal into a summary field)
   - Required vs. optional
3. **Images and attachments.** Count allowed, format, size limits, content rules ("diagrams only" vs. "any").
4. **Formatting quirks.** Markdown support, line-break handling, Unicode, how HTML/markup renders.
5. **Agreements and opt-outs.** Every checkbox the user has to click at submission. Flag strategic opt-outs (IP sharing, identity disclosure, export-control assertions) for a human decision.
6. **Submission mechanics.** Save-and-resume, edit-after-submit, confirmation mechanism.

### Step 3: Derive the section budget table

After capture, produce a section-budget table in `working/` that `/proposal-manager` and `/proposal-writer` will consume:

```markdown
# Section Budgets (derived from portal-format.md)

| Section ID | Portal Label | Char Limit | Safety Margin (2%) | Working Budget |
|---|---|---|---|---|
| SF-1 | Technical Solution | 1,500 | 30 | 1,470 |
| ... | ... | ... | ... | ... |
```

Write to `working/section-budgets.md`. `/proposal-writer` will read this and write to budget on first draft.

### Step 4: Offer to contribute back to the library

If no reference file existed for this portal, offer:

> "This is a new portal for the library. Shall I promote this capture to `reference/portal-formats/<portal-id>.md` so the next proposal against this portal inherits it?"

If yes:
- Create `reference/portal-formats/<portal-id>.md` from the proposal-local capture
- Strip proposal-specific notes (e.g., "we will use TRL 7") and keep only general portal structure
- Add a row to the README table in `reference/portal-formats/README.md`

### Step 5: Verify and exit

Tell the user:
1. Portal format captured to `inputs/00_priority/portal-format.md`
2. Section budgets derived to `working/section-budgets.md`
3. (If applicable) Added to framework library at `reference/portal-formats/<portal-id>.md`
4. Next step: `/proposal-manager` — it will refuse to proceed without this file when `submission_mechanism: web-form`

## Workflow (known portal, reference file exists)

Short path:

1. Copy `reference/portal-formats/<portal-id>.md` → `inputs/00_priority/portal-format.md`
2. Prepend a header note: "Inherited from `reference/portal-formats/<portal-id>.md` on YYYY-MM-DD. Last verified against live portal: [date from reference file]. Spot-check live portal before drafting."
3. Generate `working/section-budgets.md` from the inherited limits.
4. Remind the user to spot-check: portal owners change limits, add fields, or reword instructions without announcement. A 30-second scan of the live portal is cheap insurance.

## Critical Rules

- **Never estimate portal limits.** If the user can't see them, stop and wait. Estimation here causes the exact failure mode this skill exists to prevent.
- **Capture character limits precisely.** Characters-including-spaces is the default for most portals; confirm if stated otherwise. Word limits and character-excluding-spaces limits require different budget math.
- **Capture formatting quirks the first time.** Knowing on day 1 that a portal strips markdown saves re-drafting on day 14.
- **Strip HTML comments from counts.** Drafts often contain `<!-- evidence: EV-XXX -->` markers. These count toward portal limits when pasted. Note this in formatting quirks.
- **Flag strategic opt-outs to a human.** Don't silently default-accept IP sharing, identity disclosure, or export-control assertions.

## Output Files

- **`inputs/00_priority/portal-format.md`** — proposal-local portal reference (always)
- **`working/section-budgets.md`** — derived per-section character budgets (always)
- **`reference/portal-formats/<portal-id>.md`** — framework library entry (only if novel portal; only with user consent)

## Activity Trail

Append to `working/activity.md`:

```
## <timestamp> — capture-portal-structure — captured <N sections>, <M metadata fields> for <portal-name>; contributed to library: <yes/no> → inputs/00_priority/portal-format.md
```

## Handoff to Downstream Skills

After this skill runs, `/proposal-manager`, `/proposal-solution-architect`, `/proposal-writer`, and `/compliance-check` all read `inputs/00_priority/portal-format.md` + `working/section-budgets.md`:

- `/proposal-manager` uses section labels and limits to structure the proposal plan
- `/proposal-writer` writes to per-section character budgets
- `/compliance-check` verifies each section stays within its portal limit
- `/export-proposal` strips markdown formatting before producing portal-ready plain text

## Lessons Learned

### From the NATO DIANA submission (2026-04-23)
- The challenge PDF described the opportunity at high level but said nothing about the portal's 4-SF / 5-LF structure or the 750/12,000/3,500 char limits.
- Drafts written against an assumed structure cost ~40% of the session's token budget to compress and restructure.
- The competitor-comparison requirement in LF-2 Technical Merit was discovered only at portal-format capture. A non-responsive draft would have shipped without this gate.
- LF-5 Company and Commercial had six required topics in 3,500 chars — the tightest section in the Long Form. Budget-first writing (section-budgets.md fed to proposal-writer) would have eliminated the compression cycles.
