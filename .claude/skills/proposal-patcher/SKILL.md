---
name: proposal-patcher
description: Apply audit findings (Gold Team Weaknesses/Deficiencies and evidence-check CLAIM-UNSUPPORTED markers) as surgical fixes to bound drafts. Never rewrites globally. Preserves voice, structure, and all Strengths. Final stage of the Track B white-paper workflow before export.
phase: review
composes: [proposal-writer, evidence-check, red-team-review]
conflicts_with: [proposal-editor]  # proposal-editor does a global editorial pass; patcher is surgical — one does not follow the other
---

# Proposal Patcher Skill

## Purpose

Apply the audit patch list — and only the patch list — to the bound drafts.

The bound drafts (`drafts/<section>.md`) have been written in voice, verified for evidence, and scored by the Gold Team. The audits produced located findings: Weaknesses, Deficiencies, and unsupported-claim flags. This skill resolves exactly those findings — nothing else. The voice and structure installed by the two-pass writer are preserved. The spine's through-line survives.

This is the last content-changing step before `/export-proposal`.

## When to Use

Run after **both** `/evidence-check` and `/red-team-review --mode=gold` have written their findings. Run before `/export-proposal`.

Track B white-paper workflow:
```
/narrative-spine          → human sign-off
/proposal-writer          → draft-loose, then bind
/evidence-check           → CLAIM-UNSUPPORTED findings
/red-team-review          → Gold Team W/D findings
/proposal-patcher         <<< here
/export-proposal
```

Do not run `/proposal-editor` before this skill. They are mutually exclusive final-pass strategies: the editor does a global pass on structure-first prose; the patcher does surgical fixes on narrative-first prose. Running both defeats the purpose of Track B.

## Inputs

### Required — will not proceed without these

1. `reviews/gold-team-scorecard.md` — must exist and contain at least one Weakness (W) or Deficiency (D). If it exists but has only Strengths, confirm with the user before exiting (the drafts may be submittable as-is).
2. `reviews/evidence-check.md` — must exist. If stale (older than any `drafts/*.md` file), warn and recommend re-running `/evidence-check` first.
3. `drafts/<section>.md` — the bound drafts produced by `/proposal-writer --mode=bind`. The loose drafts in `drafts/loose/` are untouched.

### Read if available
- `working/narrative-spine.md` — the through-line the patched drafts must still carry after edits.
- `reviews/technical-review-drafts.md` — if `/technical-review --phase=drafts` was run; include its findings in the patch list.

## Build the Patch List First

Before touching any draft, build a complete patch list. Present it to the user as a table:

| # | Source | Finding Type | Location | Finding Summary | Proposed Fix |
|---|---|---|---|---|---|
| 1 | evidence-check | CLAIM-UNSUPPORTED | drafts/proposed-approach.md §2 | "... 14 months in disconnected mode ..." | Soften to "demonstrated in disconnected conditions" or attach EV-022 if ledger match found |
| 2 | gold-team W | Weakness | drafts/outcomes-and-value.md §1 | "Outcomes not quantified" | Add a specific metric from working/capability-matrix.md |
| ... | | | | | |

**Then stop and confirm.** Ask the user: "This is the patch list — N findings. Shall I apply all, or are there any you want to skip or handle manually?"

This is deliberate. The patch list is cheap to review and expensive to undo. Bill's judgment at this point is higher-value than the agent's — he knows which Gold Team findings reflect real gaps vs. scoring bias.

After confirmation, apply the patches.

## Patch Rules

### What to patch (in order)

**1. Deficiencies (D) — must address**

A Deficiency is a material gap that would likely result in an Unacceptable rating if unaddressed. For each D:
- Locate the referenced section and paragraph.
- Make the minimal addition or change that addresses the stated gap.
- Write in the section's existing voice — match cadence, sentence length, register.
- Do not write a new section; add to the section that should carry the point.
- If a Deficiency cannot be addressed without fabricating a capability or past performance, flag it for the user: `<!-- PATCH-BLOCKED: <D-item> — cannot address without unsupported claim. User action required. -->`. Do not invent.

**2. Weaknesses (W) — address where the fix is clear**

A Weakness reduces the rating but does not make the section Unacceptable. For each W:
- Same surgical approach: locate, add minimally, match voice.
- If the fix would require a significant structural change (reordering sections, adding >100 words to a section already at its word budget), flag for the user rather than silently overbuilding: `<!-- PATCH-NOTE: W-item addressed partially — consider full revision if this factor is decision-critical. -->`.

**3. CLAIM-UNSUPPORTED markers — resolve**

For each `<!-- evidence: CLAIM-UNSUPPORTED -->` found in the bound drafts:
- Check `my-company/evidence-ledger.json` again — evidence may have been added since bind ran.
  - If a matching evidence entry exists: attach the ID (`<!-- evidence: EV-NNN -->`). Do not change the claim text.
  - If no evidence exists: soften or qualify the claim to match what *is* demonstrable, and remove the marker. Write the softer version in voice — don't just prepend "We believe that..."
  - If the claim is central and cannot be softened without gutting the argument: leave the marker, add `<!-- PATCH-BLOCKED: CLAIM-UNSUPPORTED — user must supply evidence or remove claim. -->`.
- Never delete a claim without notifying the user in the patch log.

### What NOT to patch

- **Strengths (S).** If Gold Team identified a Strength in a section, do not modify that section for any reason other than an explicit D or W finding in the same section. Do not "improve" Strengths — the risk of degrading them outweighs any benefit.
- **Sections with no findings.** Do not edit sections that Gold Team found acceptable and that have no CLAIM-UNSUPPORTED markers. Zero-finding sections are done.
- **Voice or style.** Do not tighten prose, cut marketing language, or improve rhythm. That was proposal-editor's job — and in Track B, the loose draft's voice was intentional. Patcher is not an editor.
- **Structure.** Do not reorder sections, split or merge paragraphs, or add new sections unless a Deficiency explicitly requires missing content that has no existing home.
- **The narrative spine.** Do not change the positioning line or through-line. If a Gold Team finding seems to require repositioning the whole proposal, flag it for the user — that is a spine revision, not a patch.

## Output

### 1. Pre-patch backup

Before modifying any file, write the current bound draft to a backup:
```
reviews/pre-patch/<section-id>.md
```
Do this for every file you will modify. The backup is the restore point if Bill disagrees with a patch.

### 2. Patched drafts in place

Apply all confirmed patches directly to `drafts/<section-id>.md`. The patched file is what `/export-proposal` will read.

### 3. Patch log

Write `reviews/patch-log.md`:

```markdown
# Patch Log — [Proposal Name]

**Generated:** <timestamp>
**Findings reviewed:** <N total>
**Patches applied:** <N applied>
**Blocked / flagged for user:** <N>

## Applied Patches

| # | Source | Type | Location | Change Summary |
|---|---|---|---|---|
| 1 | evidence-check | CLAIM-UNSUPPORTED resolved | drafts/proposed-approach.md L42 | Attached EV-022; claim text unchanged |
| 2 | gold-team W2 | Weakness addressed | drafts/outcomes-and-value.md §1 | Added "reduces operator decision time by ~40% (EVELYN bench, EV-031)" |

## Blocked / User Action Required

| # | Source | Type | Location | Why Blocked | Required Action |
|---|---|---|---|---|---|
| 3 | gold-team D1 | Deficiency | drafts/team-and-credibility.md | No evidence for claimed ATO experience | User must supply evidence or remove claim |

## Untouched Strengths (preserved)

| Section | Gold Team Strength | Action |
|---|---|---|
| drafts/problem-statement.md | "Compelling problem framing grounded in customer language" | No touch |
```

## After Patching

1. Tell the user how many findings were resolved, how many were blocked, and list the blocked items prominently.
2. Recommend: "Review `reviews/patch-log.md` and resolve any PATCH-BLOCKED items. When ready, run `/export-proposal`."
3. If any Deficiencies remain unresolved (blocked), do NOT recommend `/export-proposal` — the draft has a material gap. Flag it explicitly.

## Discipline Rules

- **One finding, one fix.** Each patch addresses one finding. Do not use a finding as an excuse to improve nearby prose.
- **Minimum effective dose.** The right patch is the smallest change that addresses the finding. A one-sentence addition beats a paragraph rewrite.
- **The voice stays.** Patches must sound like the surrounding prose. If you cannot patch in voice, note it and let the user handle it.
- **Spine check after patching.** After all patches are applied, re-read `working/narrative-spine.md` and verify the through-line still reads cleanly across the patched drafts. If a patch inadvertently broke the through-line, note it in the patch log.

## Activity Trail

On completion, append to `working/activity.md`:
```
## <timestamp> — proposal-patcher — <N> patches applied, <M> blocked → reviews/patch-log.md
```

Append one JSON line to `working/ai-runs.jsonl` per [`reference/schemas/ai-run.schema.json`](../../../reference/schemas/ai-run.schema.json):
```json
{"schema_version":"ai-run.v1","timestamp":"<timestamp>","skill":"proposal-patcher","proposal_id":"<slug>","job_type":"review","provider":"anthropic","model":"claude-opus-4-7","input_tokens_estimate":null,"output_tokens_estimate":null,"cost_estimate_usd":null,"notes":"<N> patches applied, <M> blocked"}
```

## Final Rule

The patcher's job is to close the audit's gap list — no more, no less. Every word it doesn't change is a word the writer earned. The voice stays. The spine stays. The Strengths stay.
