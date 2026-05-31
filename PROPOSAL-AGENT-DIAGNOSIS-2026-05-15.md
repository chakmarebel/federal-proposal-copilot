# Federal Proposal Agent — Diagnostic Report

**Date:** 2026-05-15
**Investigator:** Claude (diagnostic session)
**Reported symptoms:** (a) graphics not generating the way they should; (b) papers formatting weirdly. Bill suspected structural corruption.
**Scope:** `.claude/skills/`, `tools/`, `scripts/`, `reference/graphic-templates/`, recent proposal outputs, git/worktree state.

---

## Bottom line

**There is no structural corruption.** All 25 skills, the skill registry, the
graphic-template library, and the git object database are intact and valid.

Both symptoms have concrete, evidenced root causes — and **neither is caused by
the "5 skills/registry moves" session.** That session's edits (YAML frontmatter,
`SKILLS.md` index, `conflicts_with`) all landed cleanly and pass every validator.
The `.skill-log` logging convention it added was fully reverted in commit
`19616d2` and leaves zero trace.

The real causes are:

1. **Formatting symptom** — `tools/md_to_docx.py`, the Word converter that
   *every* framework export is required to use, has **no fenced-code-block
   (` ``` `) support**. Anything inside a ` ``` ` block — an ASCII diagram, a
   budget table, a schedule — is rendered as ordinary proportional-font
   paragraphs, one Word paragraph per line, with 6 pt gaps. It comes out garbled.
2. **Graphics symptom** — two separate things: (G1) the most recent proposal
   (`vulcan-jatf`) never ran `/proposal-graphics` at all; its architecture figure
   was hand-drawn as ASCII art *inside a draft* instead of going through the
   HTML→PNG pipeline. (G2) `dod-openweight-whitepaper` contains four
   byte-identical copies of `socpac`'s graphics, producing duplicate/conflicting
   figure numbers.

A third, real issue surfaced during the investigation: **both mandatory
pre-submit gate scripts crash** when a Word lock file is present. This one is
**already fixed** on branch `fix/proposal-agent-diagnosis` (see Fix #1).

---

## What is NOT wrong (corruption ruled out)

| Checked | Result |
|---|---|
| 25 × `SKILL.md` YAML frontmatter | All valid. All 5 required keys (`name`, `description`, `phase`, `composes`, `conflicts_with`) present. All `phase` values legal. No malformed indentation, no unclosed blocks, no duplicate keys. |
| `SKILL.md` truncation | None. All code fences balanced; all files match `HEAD` exactly; `git status` on `.claude/skills/` is clean. The Edit-truncation bug noted in the 5-moves session report did **not** affect this repo. |
| `python scripts/skill-graph.py --validate-only` | `OK: 25 skills, all phase / composes / conflicts_with references valid` |
| `python scripts/build-skills-index.py --check` | `OK: SKILLS.md is up to date` |
| `git fsck` | Clean (one dangling blob — normal, harmless). |
| `.skill-log` logging convention | Added in `51646d4`, **reverted in `19616d2`**. Zero references anywhere in the repo. It is **not** leaking into output documents. |
| `SKILL-MERGE-PROPOSAL.md` merges | **None executed.** `new-proposal` and `import-from-capture` both still exist as separate skills with mutual `conflicts_with`. Only the `conflicts_with` frontmatter sharpening was applied, exactly as the audit said it would be. |
| `conflicts_with` discipline (process-bleed) | Intact. `proposal-writer` ↔ `proposal-editor` carry mutual `conflicts_with`; the writer/editor boundary is documented in both SKILL bodies. No regression. |
| `.claude/` config | `skills/`, `launch.json`, `settings.local.json` present. No `settings.json` (not required). No broken JSON. |

**5-moves session verdict: not implicated.** Its three artifacts on disk
(`SKILLS.md`, the frontmatter on every skill, `SKILL-MERGE-PROPOSAL.md`) are all
well-formed and validate. Clear it as a suspect.

---

## Worktree / tree state

- `git worktree list` registers **only 2** worktrees: the main tree and this
  diagnostic worktree. Not 16+.
- `.claude/worktrees/` on disk contains **6 directories**. Four are empty stale
  dirs (`affectionate-yonath-07b075`, `laughing-herschel-2247ba`,
  `priceless-leavitt-81f89a`, `trusting-lewin-9599ae`). One
  (`thirsty-lichterman-1ee311`) is a **non-empty orphaned snapshot** — it has
  `README.md`, `SKILLS.md`, `proposals/`, `reference/`, etc. dated 2026-05-12,
  but **no `.git` file and no `.claude/` directory**.
- **This does not affect running skills.** Skills execute from
  `.claude/skills/` in the main tree. The orphan has no `.claude/skills/`, so it
  cannot be a source of stale skills. The skills Bill runs are authoritative and
  match `HEAD`.
- These directories are harmless clutter. Cleanup is recommended but flagged for
  Bill — see Fix #6 (not auto-applied, per the don't-delete-worktrees rule).

---

## Symptom 1 — "papers formatting weirdly"

### Root cause: `tools/md_to_docx.py` cannot render fenced code blocks

**File:** `tools/md_to_docx.py`, function `convert_md_to_doc` (lines 186–281).

The converter handles H1–H4, bold/italic/code spans, tables, bullet/numbered
lists, blockquotes, and `---`. It has **no branch for ` ``` ` fenced code
blocks** — the supported-markdown list in its own docstring (lines 23–32) omits
them entirely.

When a draft contains a ` ``` ` block, the parser's `while` loop reaches the
fence line, fails every `if` branch (it is not blank, not metadata, not a
heading, not a table, not a bullet, not a blockquote), and falls through to the
final `else` at line 275 — **"regular paragraph."** Result:

- The ` ``` ` markers render as literal body paragraphs containing `` ``` ``.
- Every line inside the block renders as a separate `Normal`-style paragraph in
  **Calibri 11 pt (proportional)** with `space_after = 6 pt`.

For an ASCII diagram this is fatal: box-drawing characters do not align in a
proportional font, and the 6 pt inter-paragraph gap explodes the diagram
vertically. The figure becomes unreadable.

### Evidence

`proposals/vulcan-jatf/drafts/system-blueprint.md` lines 38–100 contain a
62-line fenced ASCII architecture diagram (the WarClaw/EVELYN block diagram).
Extracting the rendered `proposals/vulcan-jatf/drafts/system-blueprint.docx`
with `python-docx` shows every diagram line as:

```
style = 'Normal'   font = 'Calibri'   text = '│  ┌────────▼──────────────...'
```

i.e. the box art is sitting in the document body as proportional-font
paragraphs. (The box-drawing characters even crash naive `print()` on a Windows
console — they are unmistakably in the `.docx` body text.)

### Why it surfaced now (not a regression)

`tools/md_to_docx.py` was added in a single commit (`c435b08`) and **has never
been modified since.** It never supported fences. The symptom appeared now
because `vulcan-jatf` (drafted today, 2026-05-15) is the first recent proposal
to put an ASCII diagram *inside a markdown draft* rather than authoring it as an
HTML graphic. Earlier proposals (`extic-26-2`, `nato-diana`) kept diagrams in
`graphics/*.html`, so the gap never bit.

### This is the mandated export path

`export-proposal/SKILL.md` line 82 states, in bold: *"Use the shared Python
conversion script — do NOT delegate to anthropic-skills:docx."* So **every**
framework `.docx` export goes through this converter. Any draft with a fenced
block is affected — not just `vulcan-jatf`.

### Secondary latent defects in the same converter (not currently triggered)

- **H5/H6 headings** (`#####`, `######`) are not matched (only H1–H4). They fall
  through to body paragraphs and render with literal `#####`. No current draft
  uses them.
- **Lines beginning `*Note`** are silently dropped (line 212). A draft that
  legitimately starts a line with the word "Note" in italics would lose it.
- **One markdown line = one Word paragraph.** Hard-wrapped markdown paragraphs
  (multiple lines, no blank line between) become multiple Word paragraphs.
  Current drafts use one-line-per-paragraph, so this is dormant.

---

## Symptom 2 — "graphics not generating the way they should"

Two independent problems.

### G1 — `vulcan-jatf` never ran the graphics pipeline

`proposals/vulcan-jatf/` has **no `graphics/` directory** and **no
`working/graphics-brief.md`.** `working/activity.md` logs only `new-proposal`
and the manual-review skills — `proposal-graphics` was never invoked, even
though it is in this proposal type's `required_skills`
(`working/proposal-type.md`, `type_id: ota-white-paper`).

Instead, the architecture figure was hand-authored as an ASCII fence inside
`drafts/system-blueprint.md`. So "graphics not generating right" is literally
true: the figure that should be an HTML→PNG graphic is text in a draft — and
then Symptom 1 mangles it on export.

**The pipeline itself is healthy.** `proposal-graphics/SKILL.md`,
`scripts/render-graphic.py`, and the template library
(`reference/graphic-templates/three-tier-architecture/`, `capability-matrix/`,
plus five branded overrides in `my-company/graphic-templates/`) are all intact
and well-formed. `extic-26-2` used the pipeline correctly and has proper
`graphics/*.html` + `graphics/rendered/*.png` + `working/graphics-brief.md`.
This is a **workflow-was-skipped** problem, not a broken-tool problem.

### G2 — Cross-proposal graphics contamination (socpac → dod-openweight-whitepaper)

`proposals/dod-openweight-whitepaper/graphics/` contains four files that are
**byte-identical** to `proposals/socpac/graphics/`:

| File | socpac | dod-openweight-whitepaper |
|---|---|---|
| `fig1-enterprise-tactical-lifecycle.html` | original | identical copy |
| `fig2-deployment-lifecycle.html` | original | identical copy |
| `fig3-hardware-tiers.html` | original | identical copy |
| `fig4-pilot-schedule.html` | original | identical copy |

Same content, same mtimes (2026-05-12 17:17–17:19). `dod-openweight-whitepaper`
*also* has its own distinct set (`fig1-capabilities.html`,
`fig3-architecture.html`, `fig4-lifecycle-loop.html`). The result: that
proposal now has **two `fig1`s, two `fig3`s, two `fig4`s** and **no
`graphics-brief.md`** to say which is current.

**Likely cause:** `dod-openweight-whitepaper` was bootstrapped by copying the
`socpac` directory wholesale (their `working/activity.md` files also share
*identical* 2026-05-13 entries, and both carry a `white-paper-v4-revised.md`).
This is a plausible way to start a similar proposal — but it left stale
duplicate graphics behind.

**Risk:** `/export-proposal` embeds graphics by figure reference. Conflicting
`fig1/fig3/fig4` names mean the wrong graphic can land in the Word doc. This is
**per-proposal data mess, not framework corruption** — flagged for Bill, not
auto-fixed (deleting proposal files is out of scope per instructions).

---

## Additional real issue — pre-submit gates crash on Word lock files

**Files:** `scripts/lint-document-structure.py` (line 262),
`scripts/check-strengths.py` (line 160).

Both glob `final/docx/*.docx` and pass every match to `python-docx`'s
`Document()`. When Bill has a proposal's Word doc open, Word writes a
`~$<name>.docx` **owner-lock stub** — a tiny non-zip file (the one found here,
`proposals/vulcan-jatf/final/docx/~$stem-blueprint.docx`, is 162 bytes and
begins with the literal text `William Bal`). `Document()` raises
`zipfile.BadZipFile: File is not a zip file` and the script aborts.

CLAUDE.md marks these two scripts as the **mandatory pre-submit gate**. So with
a Word doc open, the gate cannot run. Confirmed by reproduction:
`lint-document-structure.py --proposal vulcan-jatf` crashed with `BadZipFile`.

**This is fixed** — see Fix #1.

---

## Minor — `export-proposal/SKILL.md` internal contradiction

The skill's `description` (line 3) says it *"Uses the anthropic-skills
docx/xlsx/pptx skills for conversion."* The body (lines 82, 132) says the
opposite, in bold: *"do NOT delegate to anthropic-skills:docx / :xlsx."* The
body is authoritative (the workspace uses `tools/md_to_docx.py`). Cosmetic, but
it should be reconciled so the description does not mislead. Flagged, not
auto-fixed.

---

## Confirmed vs. hypothesis

| Finding | Status |
|---|---|
| `md_to_docx.py` has no fenced-code-block handling | **Confirmed** — code inspection + rendered `.docx` extraction |
| `vulcan-jatf` skipped `/proposal-graphics` | **Confirmed** — no `graphics/` dir, no brief, activity log |
| socpac graphics duplicated into dod-openweight-whitepaper | **Confirmed** — byte-identical files |
| dod-openweight-whitepaper was copy-bootstrapped from socpac | **Hypothesis** (strong) — identical activity-log entries and shared draft names; not proven |
| Pre-submit gates crash on `~$` lock files | **Confirmed** — reproduced the crash |
| No structural corruption | **Confirmed** — validators, fsck, frontmatter parse all clean |
| 5-moves session not implicated | **Confirmed** — its artifacts validate |
| H5+/`*Note`/line-wrap converter defects | **Confirmed in code**, not currently triggered by any draft |

Nothing in this report is an unevidenced guess. The one item marked Hypothesis
(how the socpac/dod duplication happened) does not change any fix — the fix is
the same regardless of how the copies got there.

---

## Prioritized fix list

> **Update 2026-05-15:** Bill authorized "fix everything." Fixes #1, #2, #4, #5,
> and #6 are applied (details below). Fix #3 is a content decision left open.

#### Fix #1 — Skip `~$` Word lock stubs in the pre-submit gate globs ✅ DONE
- **Repairs:** `lint-document-structure.py` and `check-strengths.py` crashing
  with `BadZipFile` whenever a Word doc is open — i.e. the mandatory pre-submit
  gate.
- **Change:** filter filenames starting with `~$` out of both `*.docx` globs.
- **Risk:** **Very low.** `~$*` files are never real documents; excluding them
  is unambiguously correct.
- **Status:** committed on branch `fix/proposal-agent-diagnosis`
  (commit `90787e4`). Verified: with the filter, all 4 real `vulcan-jatf` docx
  open cleanly and the lock stub is excluded.

#### Fix #2 — Fenced-code-block + H5/H6 support in `tools/md_to_docx.py` ✅ DONE
- **Repairs:** the formatting symptom — garbled ASCII diagrams / code blocks /
  pre-formatted tables in every exported `.docx`.
- **Change:** added `process_code_block()` — collects each ` ``` ` block
  verbatim and renders it in **Courier New, auto-sized 5–9 pt** so the widest
  line fits the 6.0" text column; added H5/H6 heading handling; updated the
  docstring's supported-markdown list.
- **Risk:** Low. Contained to one function; only changes ` ``` ` blocks and
  H5/H6 (both rendered wrong before). The `*Note`-drop behaviour was left as-is
  — it is documented intentional behaviour, not a defect.
- **Status:** committed `2e45fa0` on `fix/proposal-agent-diagnosis`. Verified by
  re-rendering `vulcan-jatf/drafts/system-blueprint.md` to a scratch `.docx`:
  all 55 ASCII-diagram lines now render in Courier New (was Calibri).

#### Fix #3 — `vulcan-jatf` architecture figure ⚠ PARTIAL — needs Bill
- The diagram now renders correctly as a monospace block once Fix #2 reaches the
  export path (see "Action required" below). That resolves the *formatting*.
- Whether the WarClaw/EVELYN diagram should instead be a proper HTML→PNG figure
  via `/proposal-graphics` (recommended, consistent with `extic-26-2`) is a
  content call left to Bill — say the word and I will run `/proposal-graphics`
  for `vulcan-jatf`.

#### Fix #4 — Duplicate graphics in `dod-openweight-whitepaper` ✅ DONE
- **Repairs:** the G2 contamination — conflicting `fig1/fig3/fig4`.
- **Change:** per Bill's decision, the May-12 set is canonical. The older
  April-9 set (`fig1-capabilities`, `fig3-architecture`, `fig4-lifecycle-loop`,
  HTML + PNG) was **moved** — not deleted — into
  `proposals/dod-openweight-whitepaper/graphics/_superseded/`. `graphics/` now
  holds one clean set. Move is reversible.
- **Open item (flagged, not fixed):** `dod-openweight-whitepaper` still has no
  `working/graphics-brief.md`, and its May-12 figures are byte-identical to
  `socpac`'s. Bill confirmed they are the intended set; if those figures should
  diverge from socpac's, regenerate them via `/proposal-graphics`.

#### Fix #5 — `export-proposal/SKILL.md` description vs. body ✅ DONE
- **Change:** the description now says export uses the shared Python converters
  (`tools/md_to_docx.py`, `tools/compliance_to_xlsx.py`) and `anthropic-skills:pptx`
  — matching the skill body.
- **Status:** committed `68582f5` on `fix/proposal-agent-diagnosis`.

#### Fix #6 — Orphaned worktree directories ✅ MOSTLY DONE
- **Change:** ran `git worktree prune`; removed 3 of the 4 empty stale dirs
  (`affectionate-yonath-07b075`, `laughing-herschel-2247ba`,
  `trusting-lewin-9599ae`).
- **Leftovers for Bill:**
  - `priceless-leavitt-81f89a` — empty, but a process held a handle on it
    (`Device or resource busy`); remove it after the holding process exits.
  - `thirsty-lichterman-1ee311` — the non-empty 2026-05-12 snapshot. It contains
    a `proposals/socpac/` directory; per Bill's instruction it was **left
    untouched** so Bill can diff it against the live `socpac` before deciding.

---

## Status summary

| Fix | What | Status |
|---|---|---|
| #1 | `~$` lock-stub filter in gate scripts | ✅ committed `90787e4` |
| #2 | fenced-code-block + H5/H6 in `md_to_docx.py` | ✅ committed `2e45fa0` |
| #4 | quarantine stale `dod-openweight-whitepaper` graphics | ✅ done (filesystem move) |
| #5 | `export-proposal` description corrected | ✅ committed `68582f5` |
| #6 | worktree cleanup | ✅ 3 dirs removed; 2 leftovers flagged |
| #3 | `vulcan-jatf` figure as graphic vs. monospace block | ⚠ Bill's content call |

All four framework-code/doc fixes are on branch **`fix/proposal-agent-diagnosis`**
(4 commits + this report). Filesystem changes (#4, #6) are in the main tree and
are not git-tracked (`proposals/` and `.claude/worktrees/` are gitignored).

## Action required from Bill

1. **Close Word**, then re-export `vulcan-jatf` so `system-blueprint.docx` picks
   up the Fix #2 converter. While Word held `system-blueprint.docx` open this
   session, its `.docx` could not be overwritten. Command:
   `python tools/md_to_docx.py --proposal vulcan-jatf` (or re-run `/export-proposal`).
   The other `vulcan-jatf` docx have no code blocks and need no re-export.
2. **Review and merge `fix/proposal-agent-diagnosis`** into `main` so the
   converter fix and gate fix are the default going forward.
3. **Decide Fix #3** — tell me if you want the `vulcan-jatf` architecture
   diagram rebuilt as a real graphic via `/proposal-graphics`.
4. **Clear the two worktree leftovers** — remove `priceless-leavitt-81f89a` once
   free; diff and remove `thirsty-lichterman-1ee311` once confirmed redundant.
