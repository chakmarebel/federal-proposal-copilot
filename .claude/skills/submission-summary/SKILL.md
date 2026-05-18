---
name: submission-summary
description: Use this skill immediately after a solicitation is in hand to produce a one-page summary of exactly what the customer requires us to submit — response format, volume/section structure, page or word limits, pricing artifact, due date, and submission mechanics — before any planning or generation begins.
phase: capture
composes: [opportunity-quick-look, capture-portal-structure]
conflicts_with: []  # proposal-manager consumes this as its authoritative response-requirements source rather than re-extracting
---

# Submission Summary Skill

## Purpose

State, on one page, **exactly what the customer is asking us to submit** — before any analysis, planning, or drafting begins.

The shape of the deliverable governs everything downstream: a 3-volume, 10-page effort with a ROM is a different job than a 5-volume full proposal with a priced cost volume. Today that information is scattered — partly in `working/proposal-type.md` (the generic type), partly buried inside `working/proposal-plan.md` (extracted late, by `proposal-manager`). Nobody sees the deliverable shape, plainly and early, before tokens are spent generating against an assumed structure.

This skill produces that artifact: a factual, at-a-glance specification of the submission. It answers, in the first line, "what are we handing over?" — format, volume count, page limit, pricing, due date.

This is the deliverable spec. It is **not** strategy — no win themes, no approach, no solution.

## When to Use

Run **immediately after** `/new-proposal` (or `/import-from-capture`) and `/opportunity-quick-look`, and **before** `/proposal-manager`. It is one of the first things done once the decision to pursue is made.

For web-form submissions, run it **after** `/capture-portal-structure` — the captured portal format is the authoritative source for section structure and character limits, and this summary rolls it up into human-readable form.

Recommended workflow:

```
/new-proposal
/opportunity-quick-look
/capture-portal-structure   (only when submission_mechanism: web-form)
/submission-summary         <<< here — confirm the deliverable shape
/proposal-manager
```

## Inputs

### Always read

1. `working/proposal-type.md` — the generic type classification, `page_target`, `section_patterns`, `submission_mechanism`, `pricing_artifact`. This skill records what *this specific solicitation* requires, which may differ from the generic template defaults.
2. **The solicitation's instructions to offerors, directly** — every relevant file in `inputs/00_priority/`. Specifically the part that tells offerors what to submit: FAR Section L, OTA submission instructions, BAA proposal-preparation instructions, CSO/RWP instructions, SBIR solicitation instructions, or the web-form portal.

### Read if relevant

- `inputs/00_priority/portal-format.md` — if `submission_mechanism: web-form` and `/capture-portal-structure` has run. **Authoritative** for section structure and character/word limits on web-form submissions.
- `working/quick-look.md` — if `/opportunity-quick-look` ran (its submission-mechanism factor is a starting point).
- `working/section-budgets.md` — if `/capture-portal-structure` produced it.

If `inputs/00_priority/` is empty, tell the user to drop the solicitation there first and stop.

## Output

Write **one file**:

```
working/submission-summary.md
```

Then surface it to the user for confirmation (see Confirmation Gate).

## Structure of `working/submission-summary.md`

```markdown
# Submission Summary — [Proposal Name]

**[Headline line — one sentence.]**
Example: "White paper, single document, 5-page limit, ROM pricing, submitted by email — due 2026-06-03 1700 ET."
Example: "FAR full proposal, 3 volumes (Technical 25 pg / Cost no limit / Past Performance 10 pg), priced cost volume, uploaded to SAM.gov — due 2026-07-15 1400 ET."

## Submission Profile

| Field | Value |
|---|---|
| Response format | [white paper / full proposal / solution brief / quad chart / RFI response / ...] |
| Submission mechanism | [email / document-upload / web-form] |
| Number of volumes / files | [N — list them] |
| Due date / time / timezone | [exact] |
| Questions deadline | [date or "none stated"] |
| Submission method / portal | [email address / SAM.gov / portal URL / ...] |
| File format(s) | [PDF / DOCX / ...] |
| File naming convention | [as stated, or "not stated"] |
| Classification / distribution marking | [as required, or "not stated"] |
| POC | [name + email from the solicitation] |

## Volume / Section Breakdown

| Volume / Section | Page or Word Limit | Objective — what it must accomplish / what is evaluated | Required? |
|---|---|---|---|
| [e.g. Volume I — Technical Approach] | [25 pages] | [Demonstrate the technical solution against the SOO] | Required |
| [e.g. Volume II — Cost] | [no limit] | [Priced cost volume with BOEs] | Required |
| [...] | | | |

## Pricing / Cost Deliverable

[What pricing artifact is required — ROM range / OTA milestone schedule / CSO commercial pricing / full FAR cost volume / none — and which volume it lives in. If no pricing is requested, say so explicitly.]

## Required Attachments / Forms

[Resumes, past-performance questionnaires, reps & certifications, OCI disclosures, SF-form X, etc. — or "none stated".]

## Formatting Constraints

[Font, point size, margins, line spacing, page size — only what the solicitation explicitly states. If the solicitation is silent, write "not stated — workspace default applies".]

## What Is NOT Required

[Explicitly call out things sometimes expected but not asked for here — e.g. "No cost volume requested — do not include pricing", "No past performance volume", "No oral presentation". This prevents over-building.]

## Open Questions

[Ambiguities about the submission requirements that should be resolved — ideally before the questions deadline. If none, write "none".]
```

## Rules

- **Extract, do not infer.** Quote the solicitation's own words for every limit. If a limit is not stated, write "not stated" — never guess a page count.
- **Page limits are load-bearing.** Get them exact. Record whether each limit is per-volume or total, and whether cover pages, tables of contents, glossaries, and appendices count against it. This is the single most consequential field on the page.
- **Web-form precedence.** When `submission_mechanism: web-form` and `inputs/00_priority/portal-format.md` exists, the portal format is authoritative for section structure and character limits. This summary rolls it up; it does not override it.
- **Flag conflicts.** If the solicitation PDF and the portal (or `proposal-type.md` defaults) disagree on structure or limits, record the conflict in Open Questions — do not silently pick one.
- **Facts only.** No win themes, no approach, no solution design. This is a spec of the container, not the content.
- **One page.** If the breakdown runs long, the solicitation's submission instructions are unusually complex — summarize and point to the source section, do not transcribe.

## Confirmation Gate

After writing `working/submission-summary.md`, **stop** and emit a **decision card** (per [`reference/schemas/decision-card.schema.json`](../../../reference/schemas/decision-card.schema.json)) — present it to the user in chat, and append it as one JSON line to `working/decision-cards.jsonl`:

```json
{"schema_version":"decision-card.v1","gate_id":"submission-summary-confirmation","proposal_id":"<slug>","generated_by":"submission-summary","generated_at":"<timestamp>","decision":"Confirm the deliverable shape before planning begins.","artifact":"working/submission-summary.md","recommendation":"Confirm as captured","confidence":"<High|Medium|Low>","rationale":"<one or two sentences — note any field that was 'not stated' and had to be left open>","risk_if_wrong":"Every downstream stage is built against the wrong format, volume count, or page budget.","on_approval":"/proposal-manager builds the plan and compliance matrix against this shape","human_time_estimate":"2 minutes","approve_action":"/proposal-manager","review_required":true}
```

Surface the **headline line and the volume/section breakdown** with the card and say:

> Confirm this is the submission shape before we run `/proposal-manager`. If the format, volume count, or page limits are wrong, everything downstream is built against the wrong target. A wrong deliverable spec is the most expensive error in the pipeline — cheaper to catch here than at export. Pay particular attention to any field marked "not stated."

`review_required` is `true`: confidence is only as good as the solicitation's clarity, so the human confirms the shape — especially the page limits and volume count.

## Integration With Downstream Skills

- **`/proposal-manager`** reads `working/submission-summary.md` as the **authoritative source for response requirements**. It does not re-extract format, volumes, page limits, or due date — it consumes this file and builds the compliance matrix and proposal structure against the confirmed shape.
- **`/proposal-writer`** produces one draft per volume/section in the breakdown — no more, no fewer.
- **`/capture-portal-structure`** (web-form) and this skill are complementary: the portal capture is the detailed mechanics, this summary is the human-readable rollup.
- **`/export-proposal`** checks the final package against this summary — volume count, file format, naming convention.

## Activity Trail

On completion, append one line to `working/activity.md`:

```
## <timestamp> — submission-summary — <format>, <N volumes/sections>, <page limit>, <pricing artifact> → working/submission-summary.md
```

Append one JSON line to `working/ai-runs.jsonl` per [`reference/schemas/ai-run.schema.json`](../../../reference/schemas/ai-run.schema.json) with `job_type: "planning"` and `skill: "submission-summary"`.

## Final Rule

This skill describes the container, not the content. One page, factual, confirmed by a human before planning begins. That is the whole job.
