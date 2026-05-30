# WP-N3 -- Copilot Prose-Quality Doctrine Port

## Goal

Bring federal-proposal-copilot to parity with federal-proposal-assistant (FPA) post-WP-N2 for the shared prose-quality scope: canonical prose doctrine, voice anchors, reframe/polish guardrails, and skill input wiring.

N3 runs in copilot only. It does not touch proposal-workbench, federal-proposal-assistant, or the in-flight `codex/public-sanitized-release` branch. The branch target is copilot `origin/main`.

## Current State To Build On

Copilot `origin/main` already includes the doctrine-aligned positioning work. N3 builds from that baseline and keeps copilot company-neutral.

### Pass A -- Track A Inventory

Scouting result against copilot `origin/main`:

| Track A item | Status | Evidence |
|---|---|---|
| A1 narrative spine + human signoff | PRESENT | `.claude/skills/narrative-spine/SKILL.md` has `Human Sign-Off Gate`, requires stop after writing `working/narrative-spine.md`, and emits a decision card with `review_required: true`. |
| A2 loose/bind split | PRESENT | `.claude/skills/proposal-writer/SKILL.md` documents `draft-loose`, `bind`, and `full`; Pass 1 suspends evidence markers, compliance-matrix updates, mandatory section template, and pattern enforcement. |
| A4 section-opening de-mandate | PRESENT | Proposal writer says not to open every section with the same theme-statement formula and to vary openings; editorial guide also says not to open every section with the same formula. |
| A6 rubric inversion | PRESENT | Proposal writer's draft-loose suspended list includes `No writing "to pass Gold Team."` |
| A3 voice anchors | MISSING | No `reference/voice-anchors/` directory and no voice-anchor input entries in writer/spine before N3. |
| Reframe/polish and ventriloquism guard | MISSING | `reference/editorial-voice-guide.md` had no `Voice doctrine -- reframe, then polish` section before N3. |

The handoff said copilot had `PROPOSAL-AGENT-DIAGNOSIS-2026-05-15.md` and `PROPOSAL-AGENT-REDESIGN-2026-05-15.md` at top level. Current `origin/main` does not contain those files. N3 therefore references the FPA originals conceptually through the synced doctrine and FPA post-N2 parity target, but does not add or recreate those diagnosis/redesign docs.

### Canonical Parity Target

N3 aligns copilot with FPA `origin/main` after WP-N2 merge (`4f991e7`) for prose-quality scope:

- `tools/sync-voice-anchors.sh`
- `reference/PROSE-QUALITY-DOCTRINE.md`
- `reference/voice-anchors/*.md`
- `reference/editorial-voice-guide.md` voice-doctrine and voice-anchor sections
- `reference/style-guide.md` doctrine cross-reference
- `.claude/skills/proposal-writer/SKILL.md` voice-anchor input entry
- `.claude/skills/narrative-spine/SKILL.md` voice-anchor input entry
- `CLAUDE.md` doctrine cross-reference

Anything outside prose-quality remains intentionally out of scope. Copilot and FPA differ in company-neutral wording, public-release positioning, and other repository-specific content.

## Implementation

### 1. Add The Sync Script

Copy proposal-workbench's `tools/consumer-sync-template.sh` to:

```text
tools/sync-voice-anchors.sh
```

Keep the defaults unchanged:

- `WORKBENCH_REPO=chakmarebel/proposal-workbench`
- `WORKBENCH_REF=master`
- `DEST_DOCTRINE=reference/PROSE-QUALITY-DOCTRINE.md`
- `DEST_ANCHORS=reference/voice-anchors`

Make the script executable.

### 2. Run The Sync

Run the script from the copilot repo root. It creates:

- `reference/PROSE-QUALITY-DOCTRINE.md`
- `reference/voice-anchors/vulcan-jatf-opening.md`
- `reference/voice-anchors/socpac-section-3-4.md`
- `reference/voice-anchors/bill-passage.md`

`bill-passage.md` remains a comment-only placeholder.

Implementation verification may use the script's documented `WORKBENCH_REPO` and `WORKBENCH_REF` overrides against a local proposal-workbench checkout if the default SSH GitHub path is unavailable or waits on authentication. The shipped script still keeps the default SSH settings.

### 3. Inline Operative Voice Doctrine

Insert the same operative sections FPA received in WP-N2 into `reference/editorial-voice-guide.md`, before `Editorial Objective`:

- `## Voice doctrine -- reframe, then polish`
- `## Voice anchors -- imitation, not rules`

The section names ventriloquism, preserves the reframe -> polish ordering, includes bounded epistemic phrasing examples, and points to `reference/PROSE-QUALITY-DOCTRINE.md` as canonical.

### 4. Wire Voice Anchors Into Skills

Add the FPA WP-N2 voice-anchor input entry to `.claude/skills/proposal-writer/SKILL.md`:

```markdown
**`reference/voice-anchors/*.md`** -- voice cadence exemplars. Read these BEFORE composing the loose draft. Imitate their rhythm and clinical confidence; do NOT reuse their content. Anchors take precedence over a banned-words list when the two conflict. (Canonical source: `reference/PROSE-QUALITY-DOCTRINE.md`.)
```

Add the FPA WP-N2 voice-anchor input entry to `.claude/skills/narrative-spine/SKILL.md`:

```markdown
**`reference/voice-anchors/*.md`** -- voice cadence exemplars. Read these before drafting the spine. Imitate their rhythm and clinical confidence; do NOT reuse their content. The spine is the first place voice matters, and getting its cadence right carries forward through the writer. (Canonical source: `reference/PROSE-QUALITY-DOCTRINE.md`.)
```

Numbering is adjusted to fit each skill's input list.

### 5. Gap-Close Track A Divergences

Pass A found no missing A1, A2, A4, or A6 mechanics in copilot. No gap-close edits were required beyond A3 voice anchors and the reframe/polish doctrine.

### 6. Cross-Reference The Doctrine

Add the FPA WP-N2 pointer to `CLAUDE.md`:

```markdown
**Voice doctrine.** See `reference/PROSE-QUALITY-DOCTRINE.md` (canonical, synced from `chakmarebel/proposal-workbench` via `tools/sync-voice-anchors.sh`).
```

Add a short pointer to `reference/style-guide.md`:

```markdown
Voice doctrine lives in `reference/PROSE-QUALITY-DOCTRINE.md`; operative drafting guidance is in `reference/editorial-voice-guide.md`.
```

## Determinism

N3 is documentation and skill-instruction work only. It adds no model calls and no runtime behavior.

For a fixed `WORKBENCH_REPO` and `WORKBENCH_REF`, the sync script deterministically replaces the synced doctrine file and voice-anchor directory with canonical upstream copies.

## Acceptance Criteria

- `tools/sync-voice-anchors.sh` exists and is executable.
- `reference/PROSE-QUALITY-DOCTRINE.md` exists and matches the workbench canonical doctrine.
- `reference/voice-anchors/` contains the three canonical anchor files.
- Running the sync script twice is idempotent.
- `reference/editorial-voice-guide.md` contains the same operative voice-doctrine and voice-anchor sections FPA received in WP-N2.
- `proposal-writer` and `narrative-spine` list `reference/voice-anchors/*.md` as mandatory inputs.
- Copilot has no missing A1/A2/A4/A6 Track A prose mechanics after N3.
- Skill graph validation passes.
- Skill index check passes.
- Post-N3 diffs against FPA post-N2 show no prose-quality-scope gap; remaining diffs are repository-specific, company-neutral copilot differences.

## Test Plan

Run from the copilot repo root:

```bash
tools/sync-voice-anchors.sh
tools/sync-voice-anchors.sh
git diff --exit-code -- reference/PROSE-QUALITY-DOCTRINE.md reference/voice-anchors tools/sync-voice-anchors.sh
python scripts/skill-graph.py --validate-only
python scripts/build-skills-index.py --check
```

Compare post-N3 copilot files against FPA post-N2:

```bash
git diff --no-index <fpa-proposal-writer> .claude/skills/proposal-writer/SKILL.md
git diff --no-index <fpa-narrative-spine> .claude/skills/narrative-spine/SKILL.md
git diff --no-index <fpa-editorial-voice-guide> reference/editorial-voice-guide.md
```

Report remaining diffs and classify them as prose-quality scope or repo-specific divergence.

## Out Of Scope

- Building an automated FPA -> copilot sync mechanism.
- Any copilot/FPA divergence outside prose-quality scope.
- Touching `codex/public-sanitized-release`.
- Adding the FPA diagnosis/redesign docs to copilot.
- WP-M6 or future workbench M-series changes.

## File By File

- `WP-N3-PROSE-QUALITY-PORT-2026-05-30.md`: this spec.
- `tools/sync-voice-anchors.sh`: copied consumer sync script.
- `reference/PROSE-QUALITY-DOCTRINE.md`: synced canonical doctrine.
- `reference/voice-anchors/*.md`: synced canonical anchors.
- `reference/editorial-voice-guide.md`: inline operative voice doctrine.
- `reference/style-guide.md`: doctrine pointer.
- `CLAUDE.md`: doctrine pointer.
- `.claude/skills/proposal-writer/SKILL.md`: voice-anchor input entry.
- `.claude/skills/narrative-spine/SKILL.md`: voice-anchor input entry.

## Sequencing

1. Branch `pe-n3-prose-quality-port` from copilot `origin/main`.
2. Scout copilot Track A state and FPA post-N2 reference state.
3. Write this spec with the Pass A inventory.
4. Copy and chmod the sync script.
5. Run the sync.
6. Inline voice doctrine and wire skill inputs.
7. Add CLAUDE/style-guide cross-references.
8. Run sync idempotence, skill validation, index check, and FPA diff checks.
9. Commit, push, and open a PR.
