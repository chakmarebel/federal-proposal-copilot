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
required_skills: [ordered list of skill slugs the workflow needs]
skipped_skills: [skill slugs NOT used for this type]
section_patterns: <patterns-set-id>   # maps to reference/section-patterns/
compliance_sources: [L, M, PWS, SOO, SOW, EvaluationCriteria, StatementOfObjectives, ...]
evaluator_framing: <one-line mental model>
typical_duration: <string, e.g. "2-3 weeks" | "3-5 days">
notes: <free text>
```

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
3. Adapt output to match page_target, pricing_artifact, pp_required, evaluator_framing
4. Use section-patterns/<patterns-set-id>.md for section templates
```

## Adding a new type

Create a new `<type_id>.md` with the frontmatter above + a short body explaining evaluator mindset, required sections, and common pitfalls. Add a row to the table above. That's it — no skill code changes required.
