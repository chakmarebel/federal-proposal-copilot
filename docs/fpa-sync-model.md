# FPA → copilot sync model

## Canonical sources

This repo (`federal-proposal-copilot`) is the **distributable mirror** of `federal-proposal-assistant`. The two should operate the same on shared content. Three categories of content:

1. **Shared canonical (synced from FPA).** Files that should stay byte-identical between FPA and copilot. Listed in `tools/sync-from-fpa.sh`'s `SYNC_PATHS`. Run the script to pull current state; commit the result.
2. **Workbench canonical (synced from proposal-workbench).** Prose-quality doctrine + voice anchors. Listed in `tools/sync-voice-anchors.sh`. Same pull-side pattern.
3. **Copilot-specific (never synced).** `LICENSE`, `QUICKSTART.md`, the company-neutral framing in `CLAUDE.md` and SKILL files, the public-facing `README.md` / `OVERVIEW.md` distribution wording. These stay local to copilot and accumulate intentional divergence.

## Workflow

When meaningful changes accumulate on FPA's main:

```bash
# From the copilot repo root
./tools/sync-from-fpa.sh
git diff                              # review what changed
git add <synced paths>
git commit -m "chore(sync): pull FPA main @ <short-sha>"
git push
# Open PR; merge after review.
```

## Adding a path to the canonical-sync surface

Edit `tools/sync-from-fpa.sh` and add the path to `SYNC_PATHS`. Run the script. Commit both the script change and the newly-synced content together.

Before adding a path, check: does this file have company-specific framing in FPA that should NOT cross over to copilot? If yes, do NOT add it — it's an intentional-divergence file. If you want to share the structure but not the specifics, the FPA file should first be refactored to keep company-specific content in a separate company-neutral substrate.

## Refreshing voice anchors and prose-quality doctrine

Run `tools/sync-voice-anchors.sh` (pulls from `proposal-workbench`). See `reference/PROSE-QUALITY-DOCTRINE.md` for the canonical doctrine that script syncs.

## Why pull-side, consumer-owned

No automated cross-repo CI. Each consumer (copilot) owns when it pulls. The cost is occasional drift; the benefit is no inter-repo coupling and no surprises in a downstream repo on a day the upstream lands an unfinished change.

## Current sync surface (as of this commit)

Three canonical paths:
- `PROPOSAL-AGENT-DIAGNOSIS-2026-05-15.md` — the empirical prose-quality diagnosis that `reference/PROSE-QUALITY-DOCTRINE.md` cites.
- `PROPOSAL-AGENT-REDESIGN-2026-05-15.md` — the proposed redesign (Track A items A1–A6, Track B narrative-first tool) that the M-series operationalized in proposal-workbench and that FPA + copilot consume via the doctrine.
- `.claude/skills/proposal-patcher/` — the Track B audit-driven patcher skill that replaces `/proposal-editor` for white papers.
- `.claude/skills/proposal-writer/` — added WP-N5. No intentional divergence from FPA.
- `.claude/skills/proposal-manager/` — added WP-N5. No intentional divergence from FPA.
- `.claude/skills/proposal-storyboard/` — added WP-N5. No intentional divergence from FPA.
- `.claude/skills/red-team-review/` — added WP-N5. No intentional divergence from FPA.

Surface grows as more cross-repo-shared content is identified.

## Known divergence (intentional)

These files differ between FPA and copilot for company-neutralization or distribution reasons. They MUST NOT be added to `SYNC_PATHS` — running the sync would overwrite the divergent framing with FPA's company-specific content.

**Workspace contract / company context:**
- `CLAUDE.md`: FPA hard-codes EdgeRunner; copilot is company-neutral with a `/setup-company` first-run step.

**SKILL.md files with company-specific examples in FPA / generic copilot wording** (per WP-N5 diff inventory):
- `.claude/skills/narrative-spine/SKILL.md`: FPA says "EdgeRunner capabilities," copilot says "company capabilities." One line.
- `.claude/skills/new-proposal/SKILL.md`: FPA uses "SOCPAC CTO Bala Selvam" as the customer-program example; copilot uses "Agency innovation office." One line.
- `.claude/skills/export-proposal/SKILL.md`: FPA hard-codes Bill's local Windows checkout path (`C:/Users/wbal9/.../federal-proposal-assistant`); copilot uses `/path/to/federal-proposal-copilot`. Two lines (appears twice in usage examples).
- `.claude/skills/import-from-capture/SKILL.md`: FPA mentions the `federal-proposal-assistant` workspace name, Bill's Windows `Downloads` path, and the private `bd.edgerunner-pipeline.com` URL; copilot uses the `federal-proposal-copilot` workspace name, `%USERPROFILE%\Downloads`, and `bd.example-pipeline.com`. Three lines.

**Distribution-only content (copilot only):**
- `LICENSE`, `QUICKSTART.md`: copilot-only public-distribution content.

**Working artifacts (FPA only):**
- `dashboard/`, `scrubs/`, and similar operational content: FPA-only working artifacts.

**Index / metadata files (regenerated from frontmatter):**
- `SKILLS.md`: auto-generated from each SKILL.md's frontmatter via `scripts/build-skills-index.py`. Will naturally differ if either repo gains/removes a skill the other lacks. Don't sync directly; regenerate after a sync run if needed.

## Known divergence (drift — to be reconciled)

This list grows when scout passes identify files that diverged accidentally and should be brought back into sync. **Empty as of WP-N5** — the prior 4-skill scout-pass found that "drifting" SKILLs were either byte-identical (modulo line endings) or had purely intentional company-neutral hunks. Zero accidental drift remained.
