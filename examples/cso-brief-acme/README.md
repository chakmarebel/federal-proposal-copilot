# Example: CSO Solution Brief — Acme AI for Joint Expeditionary Directorate

**Fictional.** This is a worked example of a `cso-brief` proposal workspace, used to teach the framework's conventions end-to-end. Any resemblance to real programs is coincidental.

## Scenario

- **Solicitation:** CSO-JED-25-GenAI-01 (fictional) — Joint Expeditionary Directorate seeks commercial on-device generative AI solutions for disconnected operations
- **Company:** Acme AI (fictional) — small business, on-device inference platform
- **Type:** `cso-brief` (CSO Solution Brief, Phase 1) — 5-10 pages, ROM pricing, no past-performance volume

## Guided tour

Read in this order to see the framework in action:

1. **[working/proposal-type.md](working/proposal-type.md)** — copied from `reference/proposal-types/cso-brief.md`, governs the whole workflow. Note `required_skills`, `skipped_skills`, `pricing_artifact: rom`, `compliance_sources: [EvaluationCriteria, AreasOfInterest]`.
2. **[working/proposal-brief.md](working/proposal-brief.md)** — anchor doc created by `/new-proposal`, points to the type file.
3. **[inputs/00_priority/cso-announcement.md](inputs/00_priority/cso-announcement.md)** — the solicitation (fictional).
4. **[working/proposal-plan.md](working/proposal-plan.md)** — output of `/proposal-manager`. Shows eval criteria extracted, win themes defined, discriminators named.
5. **[working/compliance-matrix.md](working/compliance-matrix.md)** — seeded by `/proposal-manager`, updated by `/proposal-writer`. Status column shows mix of `Drafted` and `Planned`.
6. **[working/graphics-brief.md](working/graphics-brief.md)** — one figure with a full **action caption** (Pattern 3). Notice the "What this graphic proves" field.
7. **[drafts/executive-summary.md](drafts/executive-summary.md)** — exemplifies all four writing patterns: theme statement, discriminator proof points, action caption reference, and ghosting.
8. **[drafts/rom.md](drafts/rom.md)** — ROM pricing per `reference/pricing-artifacts/rom.md`. Notice: range, not point estimate; assumptions; no CLINs; no BOEs.
9. **[reviews/gold-team-scorecard.md](reviews/gold-team-scorecard.md)** — Gold Team output in Lightweight Reader Response mode (appropriate for `cso-brief` since it lacks Section M).
10. **[working/activity.md](working/activity.md)** — chronological trail showing each skill invocation.

## What to learn from each file

| File | Teaches |
|---|---|
| `proposal-type.md` | How type declaration drives the workflow |
| `proposal-plan.md` | How to extract eval criteria + define themes/discriminators rigorously |
| `compliance-matrix.md` | The seven-column living artifact, with varied Status values |
| `graphics-brief.md` | Action captions that assert what a graphic *proves*, not shows |
| `executive-summary.md` | All four writing patterns applied to one short section |
| `rom.md` | Range + assumptions + validity window — NOT a cost volume |
| `gold-team-scorecard.md` | Rubric-based evaluator-voice scoring, with rewrites |
| `activity.md` | How the one-line append convention tells the story |

## What this example does NOT show

- FAR Part 15 Section L/M traceability (use a `far-rfp` example for that)
- Full past-performance volume (use `far-rfp` or `sbir-phase2`)
- OTA milestone-payment schedule (use `ota-proposal`)
- Complete technical volume — we show the executive summary only to keep this example compact

More example types will ship as the framework matures. Contributions welcome.
