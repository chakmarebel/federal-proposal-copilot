# WP-N5 — FPA → copilot SKILL drift reconciliation

**Date:** 2026-05-30
**Scope:** Reconcile per-SKILL drift between `federal-proposal-assistant` and `federal-proposal-copilot`, then expand `tools/sync-from-fpa.sh`'s `SYNC_PATHS` for SKILLs that have no intentional divergence. Sibling of WP-N3.
**Authored by:** Claude (direct), not delegated to Codex — operator has the most context on the cross-repo sync model from WP-N1/N2/N3.

## What this tranche does

The prior cross-app sync work (WP-N1 through WP-N3 + the doctrine-aligned positioning PRs + the WP-N4 FPA→copilot sync mechanism) brought copilot to standalone-readable. Eight SKILL.md files were still flagged as differing between FPA and copilot per the WP-N4 scout. WP-N5 categorizes each diff, applies any accidental drift, documents intentional divergence, and adds eligible SKILLs to `SYNC_PATHS` so future drift auto-flows.

The headline finding: **zero accidental drift.** Every diff was either pure line-ending noise (byte-identical content) or pure intentional company-neutral framing. No content port was needed.

## SKILL-by-SKILL diff inventory

Categorization legend:
- **BYTE_IDENTICAL** — content matches exactly.
- **WHITESPACE_ONLY** — content matches when line endings / trailing whitespace are normalized (CRLF vs LF).
- **INTENTIONAL_COMPANY_NEUTRAL** — FPA has EdgeRunner-specific text; copilot generalizes. Doctrine-correct divergence.
- **INTENTIONAL_OTHER** — copilot uses generic paths / URLs / workspace names; FPA uses Bill-specific or private references. Doctrine-correct divergence.
- **ACCIDENTAL_DRIFT_FPA_AHEAD** — FPA has substantive update copilot lacks; should be ported. None found.
- **ACCIDENTAL_DRIFT_COPILOT_AHEAD** — copilot has substantive update FPA lacks; should be backported. None found.

| SKILL | Diff size | Categorization | Action |
|---|---|---|---|
| `proposal-writer` | 0 lines (MD5 match) | BYTE_IDENTICAL | Added to `SYNC_PATHS` |
| `proposal-manager` | 16 lines (raw) → 0 normalized | WHITESPACE_ONLY | Added to `SYNC_PATHS` |
| `proposal-storyboard` | 98 lines (raw) → 0 normalized | WHITESPACE_ONLY | Added to `SYNC_PATHS` |
| `red-team-review` | 14 lines (raw) → 0 normalized | WHITESPACE_ONLY | Added to `SYNC_PATHS` |
| `narrative-spine` | 2 lines | INTENTIONAL_COMPANY_NEUTRAL ("EdgeRunner capabilities" → "company capabilities") | Documented; stays out |
| `new-proposal` | 2 lines | INTENTIONAL_COMPANY_NEUTRAL ("SOCPAC CTO Bala Selvam" → "Agency innovation office") | Documented; stays out |
| `export-proposal` | 4 lines | INTENTIONAL_OTHER (Windows checkout path → generic) | Documented; stays out |
| `import-from-capture` | 6 lines | INTENTIONAL_OTHER (workspace name + Downloads path + private URL → generic) | Documented; stays out |

## What got ported FPA → copilot

Nothing. Zero accidental drift after categorization.

## What got added to `SYNC_PATHS` in `tools/sync-from-fpa.sh`

Four SKILLs gained automatic FPA-canonical sync:
- `.claude/skills/proposal-writer`
- `.claude/skills/proposal-manager`
- `.claude/skills/proposal-storyboard`
- `.claude/skills/red-team-review`

Future content updates to any of these in FPA flow automatically when the operator runs `tools/sync-from-fpa.sh`. The doctrine guardrail is in the script's comments: do NOT add any skill that has even one company-specific hunk, because the sync overwrites copilot's local content.

## What got documented as intentional divergence

`docs/fpa-sync-model.md`'s "Known divergence (intentional)" section gained per-SKILL entries for narrative-spine, new-proposal, export-proposal, and import-from-capture, each with the specific line-level reason. Format mirrors the existing CLAUDE.md / LICENSE entries so the file stays scannable.

## What stayed out

None as "too entangled." All four intentional-divergence SKILLs have small, well-bounded hunks (1–3 lines each) — the diff is clean. If a future tranche wants to refactor those SKILLs to keep company-specific examples in a separate substrate, it's possible. Not in scope for N5.

## Verification

- **Per-SKILL post-sync diff:** running `tools/sync-from-fpa.sh` after the SYNC_PATHS expansion produces zero net git diff on the 4 added SKILLs (their content was already identical modulo line endings; git's autocrlf absorbs the rest).
- **Idempotency:** running the sync twice produces a single `tools/sync-from-fpa.sh` change (the SYNC_PATHS edit, committed in this tranche) and zero net change on the 4 added SKILLs.
- `python scripts/skill-graph.py --validate-only`: passes (28 skills, all references valid).
- `python scripts/build-skills-index.py --check`: passes (SKILLS.md up to date).

## Out of scope

- Backporting any copilot-side updates to FPA (none found anyway).
- Refactoring the four intentional-divergence SKILLs to extract company-specific examples into a separate substrate.
- Aligning non-SKILL files (CLAUDE.md, README.md, OVERVIEW.md, dashboard/, scripts/, etc.). Each is a separate decision with its own divergence story.
- The "Copilot" name question for public release.
- WP-M8 (calibration corpus consumer) — separate tranche on the workbench side.

## After this PR

Copilot's `SYNC_PATHS` covers 7 paths (the prior 3 from WP-N4 + the 4 from N5). The known-divergence list documents every SKILL that intentionally stays out. The accidental-drift list is empty. The cross-repo sync model is in steady state for the prose-quality + capture-substrate scope.
