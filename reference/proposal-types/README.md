# Proposal Type Registry

One file per proposal type, each with frontmatter declaring the workflow, artifacts, and evaluator framing for that type. `/new-proposal` copies the chosen type file to `working/proposal-type.md` in the proposal workspace; every downstream skill reads that file and adapts.

## Frontmatter schema

```yaml
type_id: <short-id>                   # filename stem
display_name: <human name>            # shown in /new-proposal menu
solicitation_vehicle: <FAR|BAA|CSO|OTA|SBIR|STTR|RFI|SourcesSought|IDIQ|unsolicited>
page_target: <string, e.g. "3-10" or "50 excl. cover">
pricing_artifact: none | rom | sbir-budget | ota-milestones | cso-commercial | far-cost-volume
pp_required: false | true | "relevant-experience"
submission_mechanism: email | document-upload | web-form   # how the proposal physically reaches the customer
portal_id: <portal-id>                # OPTIONAL — set when submission_mechanism: web-form and a reference format exists in reference/portal-formats/<portal-id>.md
required_skills: [ordered list of skill slugs the workflow needs]
skipped_skills: [skill slugs NOT used for this type]
section_patterns: <patterns-set-id>   # maps to reference/section-patterns/
compliance_sources: [L, M, PWS, SOO, SOW, EvaluationCriteria, StatementOfObjectives, ...]
evaluator_framing: <one-line mental model>
typical_duration: <string, e.g. "2-3 weeks" | "3-5 days">
notes: <free text>
```

### `submission_mechanism` values

| Value | Meaning | Format authority |
|---|---|---|
| `email` | Attach the proposal to an email sent to a CO or POC | Whatever the solicitation (or POC) asks for |
| `document-upload` | PDF/Word upload to an agency portal (SAM.gov, etc.) | Section L of the solicitation |
| `web-form` | Paste narrative into portal text fields with hard limits | `reference/portal-formats/<portal-id>.md` (inherited) or `/capture-portal-structure` (novel) |

**Default for existing types is `document-upload`.** Most FAR/BAA/SBIR/OTA submissions go through SAM.gov or an agency upload portal; the format comes from the solicitation itself. Override to `web-form` when the submission portal imposes its own section structure and character limits (DIANA, DIU CSO Phase 1 in some cases, Challenge.gov prizes, AFWERX Open Topic, xTech, NSIN, Valid Evaluation).

### When `submission_mechanism: web-form`, extra workflow applies

1. `/opportunity-quick-look` flags the registration/portal-format gate in the submission-mechanism factor.
2. `/capture-portal-structure` MUST run before `/proposal-manager`. It either inherits a known portal from `reference/portal-formats/<portal-id>.md` or guides the user through a first-time capture.
3. `/proposal-manager` refuses to proceed without `inputs/00_priority/portal-format.md` when `submission_mechanism: web-form`.
4. `/proposal-writer` writes to per-section character budgets from `working/section-budgets.md` on first draft (budget-first, not compression-after).

## Types included

| File | Vehicle | Pricing | PP | Page target |
|---|---|---|---|---|
| [far-rfp.md](far-rfp.md) | FAR Part 15 RFP | far-cost-volume | true | per Section L |
| [idiq-to.md](idiq-to.md) | IDIQ Task Order | far-cost-volume | relevant-experience | short |
| [cso-brief.md](cso-brief.md) | CSO Solution Brief (Phase 1) | none or rom | false | 5-10 |
| [cso-full.md](cso-full.md) | CSO Full Proposal (Phase 2) | cso-commercial | relevant-experience | 15-30 |
| [baa.md](baa.md) | BAA | rom or far-cost-volume | relevant-experience | 15-30 |
| [ota-white-paper.md](ota-white-paper.md) | OTA White Paper | rom | false | 5-10 |
| [ota-proposal.md](ota-proposal.md) | OTA Full Proposal | ota-milestones | relevant-experience | 20-40 |
| [sbir-phase1.md](sbir-phase1.md) | SBIR Phase I | sbir-budget | false | per topic |
| [sbir-phase2.md](sbir-phase2.md) | SBIR Phase II | sbir-budget | true | per topic |
| [white-paper.md](white-paper.md) | Unsolicited / directed WP | none or rom | false | 3-10 |
| [rfi.md](rfi.md) | RFI response | none | false | 5-15 |
| [sources-sought.md](sources-sought.md) | Sources Sought | none | relevant-experience | 2-5 |
| [rom.md](rom.md) | Standalone ROM | rom | false | 1-3 |

## How skills consume this

Every skill's first action should be:

```
1. Read working/proposal-type.md
2. If this skill is in skipped_skills: exit with a note ("Skipped for <type>.")
3. If submission_mechanism: web-form AND inputs/00_priority/portal-format.md is missing:
     - If this skill is /capture-portal-structure: proceed (that's its job)
     - Otherwise: exit with "Portal format not captured. Run /capture-portal-structure first."
4. Adapt output to match page_target, pricing_artifact, pp_required, evaluator_framing
5. Use section-patterns/<patterns-set-id>.md for section templates
6. When submission_mechanism: web-form, use working/section-budgets.md for per-section char limits
```

## Adding a new type

Create a new `<type_id>.md` with the frontmatter above + a short body explaining evaluator mindset, required sections, and common pitfalls. Add a row to the table above. That's it — no skill code changes required.
