# FPA → copilot sync model

## Canonical sources

This repo (`federal-proposal-copilot`) is the **distributable mirror** of `federal-proposal-assistant`. The two should operate the same on shared content. Three categories of content:

1. **Shared canonical (synced from FPA).** Files that should stay in sync between FPA and copilot, modulo the mechanical transforms below. Listed in `tools/sync-from-fpa.sh`'s `SYNC_PATHS`. Run the script to pull current state; commit the result.
2. **Workbench canonical (synced from proposal-workbench).** Prose-quality doctrine, universal doctrine knowledge, voice anchors, and the shared prose-lint rule set. Listed in `tools/sync-voice-anchors.sh`. Same pull-side pattern, same neutralization.
3. **Copilot-specific (never synced).** `LICENSE`, `QUICKSTART.md`, the company-neutral framing in `CLAUDE.md`, the public-facing `README.md` / `OVERVIEW.md` distribution wording. These stay local to copilot and accumulate intentional divergence.

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

To sync content that has not been pushed to FPA's main yet, point the script at a local checkout:

```bash
FPA_LOCAL="/path/to/federal-proposal-assistant" ./tools/sync-from-fpa.sh
```

The script prints the local HEAD it read. If that working tree was dirty, say so in the commit message — the recorded sha alone will not reproduce the result.

## Adding a path to the canonical-sync surface

Edit `tools/sync-from-fpa.sh` and add the path to `SYNC_PATHS`. Run the script. Commit both the script change and the newly-synced content together.

Before adding a path, ask what kind of divergence it has:

- **Mechanical divergence** (the company's name, a product name, a CAGE code, an operator's local path) — **add it.** `tools/neutralize-company.sed` rewrites those on every sync, so the file stays on the surface and keeps receiving upstream improvements.
- **Editorial divergence** (a hand-written company-neutral rewording that no table can produce) — **do not add it.** Syncing would overwrite the rewording. It goes on the intentional-divergence list below.

The distinction matters because a hand-neutralized file has to be frozen off the surface forever, and frozen content goes stale. Prefer refactoring FPA so the company-specific part lives in a substrate the table can reach.

## Refreshing voice anchors and prose-quality doctrine

Run `tools/sync-voice-anchors.sh` (pulls from `proposal-workbench`). It applies the same neutralization and the same leak-scan gate. See `reference/PROSE-QUALITY-DOCTRINE.md` for the canonical doctrine that script syncs.

## Why pull-side, consumer-owned

No automated cross-repo CI. Each consumer (copilot) owns when it pulls. The cost is occasional drift; the benefit is no inter-repo coupling and no surprises in a downstream repo on a day the upstream lands an unfinished change.

## Current sync surface

**Reference docs** — `PROPOSAL-AGENT-DIAGNOSIS-2026-05-15.md`, `PROPOSAL-AGENT-REDESIGN-2026-05-15.md`, `docs/AGENT-ORIENTATION.md`, `docs/BD-CTO-DEMAND-SIGNAL-SYNC.md`.

**Skills** — `proposal-patcher`, `proposal-writer`, `proposal-manager`, `proposal-storyboard`, `red-team-review`, `adversarial-review`, `capture-demand-signals`.

**Reference data** — `adversarial-personas.md`, `preventable-gold-team-findings.md`, `pitch-demo-readiness-gate.md`, `capability-themes.md`, `customer-aliases.tsv`, `prose-lint-rules.json`.

**Proposal types + section patterns** — a type and its section pattern sync together, or the type declares a pattern file that isn't there. Currently `baa-white-paper`, `marketplace-video-pitch`, `pitch-demo`, `unsolicited-proposal`, `white-paper`, both `README.md` files, and `portal-formats/colosseum.md`.

**Voice doctrine** — `voice-profiles/proposal.md`, the `voice-pairs/proposal` paired-example corpus, and `voice-anchors/`. All three are drawn from real drafts, so the neutralize transform carries them.

**Feature scripts** — the evaluator-upstream toolchain (`extract-evaluation-model.py`, `compute-lift.py`, `backfill-gold-snapshots.py`), the lint gates (`prose-lint.py`, `lint-document-structure.py`, `lint-submission-file.py`, `check-strengths.py`), the renderers (`render-matrix-to-xlsx.py`, `render-md-to-docx.py`), the calibration pair (`calibration-status.py`, `new-calibration-entry.sh`), the demand-signal machinery (`demand_signal_core.py`, `extract-demand-signals.py`, `ingest-crm-candidates.py`, `promote-crm-candidates.py`, `build-demand-signal-workbook.py`, `build-demand-signal-brief.py`, `customer-aliases.py`), and the repo-hygiene tooling (`check-git-boundary.sh`, `install-hooks.sh`, `backup-company-assets.py`).

**Shared converters** — `tools/md_to_docx.py`, `tools/polish_docx.py`.

**JSON schemas** — `evaluation-model`, `gold-team-snapshot`, `adversarial-round`, `demand-signal`.

Surface grows as more cross-repo-shared content is identified. **Rule of thumb: when a feature spans a skill plus supporting scripts, schemas, or reference data, add *all* of those paths in the same PR — a skill synced without its scripts is worse than not synced.**

### Three steps the sync applies after copy

1. **`$id`-host normalization.** Schema `$id` namespaces are rewritten `federal-proposal-assistant.local` → `federal-proposal-copilot.local`, so schemas stay on the surface without importing FPA's identity. Idempotent.

2. **Company neutralization.** `tools/neutralize-company.sed` strips the upstream company's identity: company and product names, CAGE/UEI, address, leadership names, the standing corporate facts that the section patterns inline as a drafting shortcut, and the operator's local Windows paths. Shared with `tools/sync-voice-anchors.sh` so both upstreams are stripped the same way. Every rule is idempotent.

   Two rules are deliberately absent, both because an over-broad rewrite corrupted meaning:
   - The bare repo name `federal-proposal-assistant` is **not** rewritten. It names a repo, not a company, and the shared doctrine names all three sibling repos in one sentence — rewriting it there produced "copilot, and copilot." Only the owner-qualified forms (`chakmarebel/…`, the GitHub URL) are rewritten, because those leak an account.
   - The two product names map to **distinct** placeholders (`[Runtime Product]`, `[Reasoning Product]`). Collapsing both to one placeholder turned a voice anchor describing a two-layer stack into "[Your Product] and [Your Product] form a two-layer stack."

   The general lesson: a neutralization rule that is correct token-by-token can still be wrong sentence-by-sentence. Read the resulting prose, not just the diff stat.

3. **Index regeneration.** `scripts/build-skills-index.py` runs so `SKILLS.md` never drifts from the synced SKILL.md frontmatter.

### The leak-scan gate

`tools/leak-scan.sh` greps the whole distributable tree for a list of company-identity markers and exits non-zero on any survivor. Both sync scripts run it as their closing step, so a sync that would publish an identifier **fails loudly instead of committing quietly**.

The neutralize table is only ever as complete as the last thing someone noticed. The scan is the part that notices. When it reports a survivor:

```
LEAK  reference/section-patterns/unsolicited-proposal.md:133:... Bellevue, Washington ...
```

add a rule to `tools/neutralize-company.sed` and re-run the sync. **Do not hand-edit the synced file** — the next sync overwrites the fix and the leak returns.

Run it standalone any time: `./tools/leak-scan.sh` (or `--list` to see the markers). It scans tracked and untracked-but-not-ignored files; ignored paths (`my-company/`, `signals/`, `proposals/`) are never published and are skipped.

## Known divergence (intentional)

These files differ between FPA and copilot for company-neutralization or distribution reasons that no mechanical table can produce. They MUST NOT be added to `SYNC_PATHS`.

**Workspace contract / company context:**
- `CLAUDE.md`: FPA hard-codes one company; copilot is company-neutral with a `/setup-company` first-run step.

**SKILL.md files with company-specific examples in FPA / generic copilot wording:**
- `.claude/skills/narrative-spine/SKILL.md`: FPA names its own capabilities; copilot says "company capabilities."
- `.claude/skills/new-proposal/SKILL.md`: FPA uses a real customer-program example; copilot uses "Agency innovation office."
- `.claude/skills/export-proposal/SKILL.md`: FPA hard-codes the operator's local Windows checkout path; copilot uses `/path/to/federal-proposal-copilot`. Two lines.
- `.claude/skills/import-from-capture/SKILL.md`: FPA names its own workspace, a local `Downloads` path, and a private pipeline URL; copilot uses the copilot workspace name, `%USERPROFILE%\Downloads`, and `bd.example-pipeline.com`.

**Distribution-only content (copilot only):**
- `LICENSE`, `QUICKSTART.md`.

**FPA-only content, deliberately not mirrored:**
- `signals/` (the demand-signal register) and `reference/demand-signals/` (adjudication decisions) — verbatim customer requirements and our own gap admissions. copilot carries the *machinery* to build a register, never a populated one.
- `scripts/backfill-demand-signals.py` — inlines real customer names and gap admissions in its curation table.
- The evidence-check / warrant integration (`evidence_check_core.py`, `check-canonical-symbols.py`, `docs/canonical-symbols.json`, `docs/DECISION-canonical-ownership.md`) — depends on a private sibling repo.
- BD collateral: `reference/contracting-paths*.md`, `reference/ota-consortium-memberships.md`, `reference/arl-baa-*.md`, the weekly growth-update template and `compact-weekly-docx.py`.
- Proposal-local one-off exporters (`tse17-export.py`, `build_dgs_capability_matrix_xlsx.py`) — hardcoded to a single solicitation's format.
- `reference/doctrine/*.pdf` — large government source documents; the catalog that cites them is what matters.
- `dashboard/`, `scrubs/`, and similar operational working artifacts.

**Index / metadata files (regenerated from frontmatter):**
- `SKILLS.md`: auto-generated via `scripts/build-skills-index.py`. Don't sync directly; the sync regenerates it.

## Known divergence (drift — to be reconciled)

- `scripts/promote-crm-candidates.py --selftest` fails in **both** repos: it asserts an alias mapping (`DEF ADVANCED RESEARCH PROJECTS AGCY` → `DARPA`) that `reference/customer-aliases.tsv` no longer contains. This is an upstream defect mirrored faithfully, not sync damage — either the alias rows were lost or the assertion is stale, and deciding which requires knowing whether the demand brief's customer-breadth counts are currently wrong. Fix in FPA, then re-sync. Do not patch it here.
