# Framework Audit — 2026-05-06

Scope: full read of [CLAUDE.md](../CLAUDE.md), [OVERVIEW.md](../OVERVIEW.md), [README.md](../README.md), every `SKILL.md` under [.claude/skills/](../.claude/skills/), the proposal-type registry under [reference/proposal-types/](../reference/proposal-types/), the worked example under [examples/cso-brief-acme/](../examples/cso-brief-acme/), and `git log -30`.

Working hypothesis from the user: the framework is over-engineered, and skill prose is leaking process language into the proposal text the evaluator reads. The audit confirms the hypothesis with specific evidence, but the leak is concentrated in a small number of places, not pervasive.

---

## 1. Executive summary

- **Process bleed is real and the worst offender is the canonical worked example.** [examples/cso-brief-acme/drafts/executive-summary.md](../examples/cso-brief-acme/drafts/executive-summary.md) embeds five inline `*[Pattern N: ...]*` annotations directly in the deliverable. The file has a header note saying "Remove before submission" but it lives in `drafts/` — the directory the framework defines as the authoring layer that flows into `final/`. The "annotations" pattern is documented nowhere in any SKILL.md; it appears to be a teaching hack invented for the example and then frozen in. This is the single most damaging artifact in the repository because it is held up in [examples/cso-brief-acme/README.md](../examples/cso-brief-acme/README.md) as the model output to learn from.
- **There is no dedicated "editor" skill.** The user mentioned one. The closest things in the repo are the "Final Pass" subsection in [proposal-writer/SKILL.md:130-134](../.claude/skills/proposal-writer/SKILL.md) (four lines) and the White Glove mode of [red-team-review/SKILL.md:327-364](../.claude/skills/red-team-review/SKILL.md). Either the user is misremembering, the skill exists in a different worktree, or the editor is a gap they intended to add and didn't. Worth a clarifying question — flagged in §8.
- **The Shipley vocabulary is mostly contained.** "Shipley", "Gold Team", "compliance-check", "color team", "pWin", "discriminator", "win theme", "ghosting" appear in 13 of 21 SKILL.md files but do not bleed into the cso-brief example's drafts/ outside the Pattern annotations. The risk is not that this language is showing up in proposals today — it's that the skills *direct* the writer to apply patterns by name (e.g., "Apply Pattern 1 — theme statement"), and the example demonstrates labeling those applications inline. Future Claude runs will copy the demonstration.
- **Two skills are doing identical work in different files.** [compliance-check/SKILL.md](../.claude/skills/compliance-check/SKILL.md) and [red-team-review/SKILL.md](../.claude/skills/red-team-review/SKILL.md) compliance-check mode are largely the same skill. red-team-review explicitly says "Run `/compliance-check` first ... don't duplicate the diffing work here" but compliance-check still re-checks page limits, formatting, attachments, and graphics conventions. The user runs both, gets two outputs, and now has to reconcile.
- **proposal-writer is overloaded.** It owns drafting, four-pattern application, evidence citation marker insertion, compliance-matrix maintenance, white-paper compression, *and* a "Final Pass" QA. [proposal-writer/SKILL.md](../.claude/skills/proposal-writer/SKILL.md) is 216 lines and the longest single set of writing instructions in the framework. This is where the process language is most concentrated and where the "tell Claude to label its own moves" temptation is strongest.
- **red-team-review has expanded to a Shipley-canonical 6-team model with backward-compatibility aliases.** [red-team-review/SKILL.md:14-37](../.claude/skills/red-team-review/SKILL.md) now declares 9 mode names (`blue`, `black-hat`, `storyboard-pink`, `pink`, `red`, `mock-eval`, `gold`, `white-glove`, `lessons-learned`, `full`) plus historical aliases. For a small-team workflow this is over-specified. Three modes (compliance, narrative review, final QA) cover the actual usage in the example.
- **The smoke test fails on 8 missing scaffold directories** — `templates/inputs/00_priority`, `01_customer`, `02_yourCompany`, `03_teammates`, `04_patterns`, `06_notes`, `templates/drafts`, `templates/reviews`. These were excluded by the gitignore added in commit [51ade0c](.) (gitignore added `working/` but those template dirs were also empty). Easy fix: add `.gitkeep` files. Diagnosed in §7.
- **Recent commits are mostly additive, none destructive.** Last 10 commits add `/capture-portal-structure`, `/capture-submission`, the calibration corpus, the methodology library, the portal-formats library, the white-paper convention file, and the NATO DIANA graphics. They refine prompts but don't remove anything. The framework grows, never sheds.

---

## 2. Recent additions table

Skills/files modified in the last ~10 commits ([git log --stat -10](.)):

| Skill / File | Stated intent | Verdict | One-line rationale |
|---|---|---|---|
| [capture-portal-structure/SKILL.md](../.claude/skills/capture-portal-structure/SKILL.md) (commit 60d9039) | Capture web-form portal limits before drafting; stop the NATO DIANA "compress 40% of tokens" failure mode | **Keep** | Solves a real failure documented at [proposal-graphics/SKILL.md:135](../.claude/skills/capture-portal-structure/SKILL.md). Tightly scoped, doesn't overlap. |
| [capture-submission/SKILL.md](../.claude/skills/capture-submission/SKILL.md) (commit 48918f9) | Snapshot AI draft + final submission for calibration corpus | **Keep** | Read-only against drafts and final, no process-bleed risk, well-scoped. |
| `corpus/calibration/` + lessons-learned mode in red-team-review (commit 48918f9) | Diff auto-draft vs. submitted to surface framework improvement signal | **Keep, watch** | Right idea; the framework-improvement proposals it produces will be valuable *if and only if* the user runs it. None have been generated yet (no completed corpus entries in the worktree). |
| Methodology library (`reference/methodology/`, commit ce88fa7) + Shipley-canonical color modes in red-team-review (c36d16b) | Document Shipley alignment + add Blue, Black Hat, Storyboard-Pink modes | **Refactor** | The methodology library itself is fine as a reference. But adding 5 new modes to red-team-review without retiring any creates a 9-mode skill that no small team will use end-to-end. Recommend deprecating Blue / Black Hat / Storyboard-Pink as separate modes — they're capture-phase activities that belong upstream of red-team-review entirely (in `/capture-scorecard` or a new `/capture-review` if needed). |
| [proposal-writer/SKILL.md](../.claude/skills/proposal-writer/SKILL.md) refinements (commit c36d16b) — added the four-pattern enforcement block + evidence citation marker convention | Make Gold-Team-passing drafts on first pass | **Refactor** | The intent is right. The implementation creates the bleed risk. See §3 for specific edits. |
| [red-team-review/SKILL.md](../.claude/skills/red-team-review/SKILL.md) refinements (c36d16b) — Phase C evidence integration, white-paper word count gate | Catch unsupported claims and white-paper length blowouts | **Keep** | Good additions. The Lessons Learned section at line 441-end duplicates the SOCPAC lesson set already in proposal-writer; consolidate into one place — see §4. |
| [export-proposal/SKILL.md](../.claude/skills/export-proposal/SKILL.md) refinements (c36d16b) | Native .docx/.xlsx/.pptx output via shared Python tools | **Keep** | Right architecture. The `tools/md_to_docx.py` + `tools/compliance_to_xlsx.py` move (commit c435b08) is correct — bypassing anthropic-skills:docx for proposal-specific styling is the right tradeoff. |
| Portal-formats library (`reference/portal-formats/`, commit a91817c) + DIANA seed entry | Reusable portal-format library | **Keep** | Net-new value. The `_template.md` + `diana.md` seed is exactly the right shape. |
| White-paper conventions (`reference/proposal-conventions/white-paper.md`, commit a91817c) | Calibrate white-paper voice from real submissions | **Keep** | Calibration approach is sound. |
| `tools/compliance_to_xlsx.py` + `tools/md_to_docx.py` (commit c435b08) | Office conversion without depending on anthropic-skills | **Keep** | Reduces external skill dependency, gives proposal-specific styling control. |
| 3 NATO DIANA graphics (commits acf2c23, 3860a6a) | Long-form proposal visuals for active proposal | **Out of audit scope** | These are proposal artifacts, not framework changes. They live in a worktree branch used for one specific proposal. |

**No "editor" skill found in the recent commit history.** Searched [.claude/skills/](../.claude/skills/) directory listing, ran `git log --all --oneline | grep -i edit`, grepped SKILL.md files for "editor". Nothing matches. If the user added one in a different branch, the worktree at `claude/modest-kapitsa-c6bab0` doesn't contain it.

---

## 3. Process-bleed risk (the central concern)

This section quotes the specific text the user wants to know about. The audit found three categories: (1) the example demonstrates inline pattern labeling, (2) skills instruct Claude to apply patterns *by name* without saying "don't label them in the output", and (3) a single skill embeds methodology references inside section structure that will leak.

### 3.1 The worked example labels its own moves in the deliverable file

This is the worst offender by far because it is actively held up as the model.

**File:** [examples/cso-brief-acme/drafts/executive-summary.md](../examples/cso-brief-acme/drafts/executive-summary.md)

[examples/cso-brief-acme/drafts/executive-summary.md:3](../examples/cso-brief-acme/drafts/executive-summary.md):
> *(Annotations in italics show which winning pattern each passage applies. Remove before submission.)*

[examples/cso-brief-acme/drafts/executive-summary.md:7](../examples/cso-brief-acme/drafts/executive-summary.md):
> **On-device inference is not a product feature — it is the architectural foundation of Acme AI, validated by 14 months of disconnected operation at a DoD customer at the scale JED requires.** *[Pattern 1: Theme statement — states what (on-device foundation), why (disconnected validated at scale), proof hook (14-month DoD deployment).]*

[examples/cso-brief-acme/drafts/executive-summary.md:13](../examples/cso-brief-acme/drafts/executive-summary.md):
> 1. **Proven DDIL deployment.** ... (AoI-1, AoI-2). *[Pattern 2: Discriminator proof point — specific claim, specific evidence, tied to eval criteria.]*

[examples/cso-brief-acme/drafts/executive-summary.md:23](../examples/cso-brief-acme/drafts/executive-summary.md):
> See **Figure 1 (Three-tier architecture)** — ... *[Pattern 3: Action caption reference — the writer points to the figure AND restates what it proves, so the evaluator who skims only the text still gets the point.]*

[examples/cso-brief-acme/drafts/executive-summary.md:28](../examples/cso-brief-acme/drafts/executive-summary.md):
> - Named technical lead (Dr. [PI] — PI on three DARPA programs in adjacent topics) committed through Phase 2 delivery *[Pattern 2: Discriminator proof point — named personnel with specific credentials.]*

Why this is bad:
1. The file lives in `drafts/`, which `/export-proposal` reads to produce `final/docx/*.docx`. Per [export-proposal/SKILL.md:240-249](../.claude/skills/export-proposal/SKILL.md): "Do not regenerate content. Export reads what's in `drafts/` — it does not re-write, re-summarize, or improve. If content is wrong, fix it in `.md` and re-export." The `tools/md_to_docx.py` script strips HTML comments but italicized `*[...]*` markdown is not a comment — it's italic prose. It would ship to Word.
2. The "Remove before submission" instruction is inside the file. The export tool doesn't read it. The next time someone runs `/export-proposal` on this example (or copies its pattern to a new proposal), the annotations export.
3. The annotation convention is not documented in any SKILL.md. It was invented for this example and is now training data for every future proposal-writer invocation that reads the example as a pattern.
4. [examples/cso-brief-acme/README.md:18](../examples/cso-brief-acme/README.md) instructs the user to read this file as the canonical demonstration of "all four writing patterns." Future Claude runs reading this README before drafting will copy the labeling style.

**Fix priority: Now.** Move the annotations out of `drafts/` entirely. Either delete them, or move them to `working/pattern-walkthrough.md` and update the README to point there.

### 3.2 proposal-writer instructs Claude to apply patterns *by name* — and then the example demonstrates labeling them in the output

The skill itself doesn't tell Claude to label patterns inline. But it doesn't tell Claude *not to*, and it uses pattern names heavily as section structure.

**File:** [.claude/skills/proposal-writer/SKILL.md](../.claude/skills/proposal-writer/SKILL.md)

[proposal-writer/SKILL.md:63-72](../.claude/skills/proposal-writer/SKILL.md):
> ## Winning Patterns (mandatory, type-gated)
>
> Read `reference/proposal-writing-patterns.md` before drafting. It defines four patterns and specifies which apply to each proposal type:
>
> | Pattern | Purpose |
> | **Theme statement** | First sentence of every major section ... |
> | **Discriminator proof point** | Claim + concrete evidence + relevance ... |
> | **Action caption** | Text under every graphic that asserts what the graphic *proves* ... |
> | **Ghosting** | Positive framing of your approach that implicitly contrasts with a known competitor weakness ...

[proposal-writer/SKILL.md:95-106](../.claude/skills/proposal-writer/SKILL.md) (Section Standard):
> 1. **Theme statement** (1 sentence — what/why/proof hook) — see Pattern 1
> 2. **Point** — the main claim of this section
> 3. **How the solution works** — technical substance
> 4. **Discriminator proof point** (at least 1 per scoring section) — see Pattern 2
> ...
> 8. **Graphic references** — each with an action caption per Pattern 3

The intent is right (apply the patterns), but the recipe is "produce these labeled blocks in order." A reasonable Claude reading this in conjunction with the example will produce text with labeled blocks. The fix is a single sentence: **"Apply the patterns in the prose. Never label them in the output text itself. The patterns are technique, not content."**

[proposal-writer/SKILL.md:80-90](../.claude/skills/proposal-writer/SKILL.md) (evidence citation):
> - **Discriminator proof points** — use discriminators from `working/proposal-plan.md` and, if Phase C is enabled (i.e., `my-company/evidence-ledger.json` exists), **cite evidence items by ID** in an inline HTML comment after each proof-point claim:
>   ```
>   Our platform operated at [customer] for 14 months in disconnected mode. <!-- evidence: EV-022 -->
>   ```

This one is OK. HTML comments are stripped by `tools/md_to_docx.py` (per [export-proposal/SKILL.md:121](../.claude/skills/export-proposal/SKILL.md): "<!-- comments --> stripped"). They're a defensible internal mechanism. The risk is very low.

### 3.3 red-team-review embeds methodology vocabulary in the rubric output structure

[red-team-review/SKILL.md:201-294](../.claude/skills/red-team-review/SKILL.md) — the Gold Team scorecard template uses Shipley vocabulary (Strengths, Significant Strengths, Weaknesses, Significant Weaknesses, Deficiencies, "Appreciably increases", "pWin"). This is **fine** because the Gold Team output goes to `reviews/gold-team-scorecard.md`, never to `drafts/`. Internal review documents should use evaluator vocabulary.

But:

[red-team-review/SKILL.md:165](../.claude/skills/red-team-review/SKILL.md) instructs the writer of the review:
> - **Use the rubric language verbatim.** "Appreciably increases" is an FAR term of art; use it, don't paraphrase.

The risk here is small (the review is internal), but verify nothing from `reviews/` ever gets pasted into `drafts/`. The current exports confirm this — `/export-proposal` only ingests `drafts/`, `working/compliance-matrix.md`, `working/pricing-inputs.md`, and `graphics/`. Reviews don't flow downstream. Net: no fix needed; flag for vigilance.

### 3.4 What the audit *did not* find

Examining [examples/cso-brief-acme/drafts/](../examples/cso-brief-acme/drafts/) (the only completed example workspace):

- **No raw "win theme" labels** in the prose. The themes are applied; they aren't named.
- **No raw "compliance matrix" or "compliance-check" / "Gold Team" / "Phase C" / "color team" / "Shipley" / "pWin" / "discriminator" mentions in `drafts/*.md`.** Confirmed by Grep.
- **No "pre-flight check" boilerplate headers** in drafts.
- **No methodology references** in the actual prose. The drafts read as proposal text, not as a methodology document.

Aside from the Pattern annotations called out in §3.1, the cso-brief example is clean. The risk is that the framework *teaches* Claude to label its work via the example, and that pattern will leak into future proposals where the user doesn't notice in time.

---

## 4. Overlap and redundancy

### 4.1 compliance-check and red-team-review Pink mode

[compliance-check/SKILL.md](../.claude/skills/compliance-check/SKILL.md) (95 lines) and [red-team-review/SKILL.md:55-110](../.claude/skills/red-team-review/SKILL.md) compliance-check (~55 lines) do overlapping work:

- compliance-check writes `reviews/compliance-gaps.md` with the gap list.
- red-team-review Pink reads that file but *also* checks page limits, formatting, attachments, white-paper extras, convention compliance, and graphic compliance.

The red-team Pink mode says it "starts from" the compliance-check output but in practice runs ten more checks. The user gets two output files (`reviews/compliance-gaps.md` and `reviews/pink-team.md`) that report on overlapping issues with different framing.

**Recommendation:** Demote red-team `--mode=pink` to a thin orchestrator. Move all the sub-checks (page limits, formatting, white-paper extras, convention compliance, graphic compliance) into `/compliance-check` itself, or split them into a `/preflight-check` that runs all the structural validations as one pass. red-team-review then only does narrative work (Red Team), rubric scoring (Gold Team), and editorial QA (White Glove). Simpler model.

### 4.2 proposal-writer and red-team-review Lessons Learned blocks duplicate the same SOCPAC content

Both skills embed an identical-or-overlapping "Lessons Learned (SOCPAC Session)" block:

- [proposal-writer/SKILL.md:183-216](../.claude/skills/proposal-writer/SKILL.md) — Section Structure, Editorial Standards, Tone Calibration, Document Formatting, Submission Package
- [red-team-review/SKILL.md:441-473](../.claude/skills/red-team-review/SKILL.md) — Structural Issues, Editorial Issues, Formatting Issues, Tone Issues, Review Delivery Format

Same content, different framing (writer's "do this" vs. reviewer's "catch this"). When the user updates the SOCPAC lessons, they have to remember to update both. Inevitable drift.

**Recommendation:** Move all lessons-learned content into `reference/proposal-conventions/<vehicle>.md` files. Both skills already reference these files. Remove the inline blocks from both SKILL.md files. Single source of truth.

### 4.3 proposal-manager and proposal-writer both maintain the compliance matrix

[proposal-manager/SKILL.md:71-86](../.claude/skills/proposal-manager/SKILL.md) seeds the matrix.
[proposal-writer/SKILL.md:112-128](../.claude/skills/proposal-writer/SKILL.md) updates the matrix as sections land.
[compliance-check/SKILL.md:60-66](../.claude/skills/compliance-check/SKILL.md) recomputes Status by scanning drafts.

Three skills writing one file. The contract — proposal-manager creates, proposal-writer updates Section/Page/Status/Evidence per row, compliance-check recomputes Status from drafts — is documented but split across three places. This is borderline acceptable for a multi-skill workflow, but it's where bugs will hide. Worth a one-paragraph "ownership contract" doc at the top of `working/compliance-matrix.md` (a header comment) that states the rule once.

### 4.4 import-from-capture and new-proposal duplicate scaffolding logic

[import-from-capture/SKILL.md:107-129](../.claude/skills/import-from-capture/SKILL.md) explicitly says "Use the same scaffold contract as `/new-proposal` — refer to `.claude/skills/new-proposal/SKILL.md` (Steps 2, 3, 3b)" then re-states the structure for visibility. This is fine — it acknowledges the duplication and points to the canonical source. Light maintenance burden but documented.

### 4.5 customer-intel and competitor-assessment are clean

Different inputs, different outputs, different downstream consumers. No overlap.

### 4.6 capture-scorecard and opportunity-quick-look are different things

quick-look is a 5-minute triage at first contact. scorecard is a 9-dimension readiness check after capture work has happened. Different timing, different depth. No overlap.

---

## 5. Gaps

Conservative — only flagging gaps with evidence from the actual outputs.

### 5.1 No editor / final-edit skill exists

The "Final Pass" subsection in proposal-writer ([proposal-writer/SKILL.md:130-134](../.claude/skills/proposal-writer/SKILL.md)) is four bullet points: Redundancy cleanup, Unsupported-claim check, Requirement coverage check, Clarity tightening. That's the entire dedicated editing instruction in the framework.

Evidence this is a real gap, from the framework's own Lessons Learned: [proposal-writer/SKILL.md:148](../.claude/skills/proposal-writer/SKILL.md):
> Auto-draft was ~6,800 words; submitted version was ~900 words (~7.5× compression in ~40 minutes). Core failure: length.

A 7.5× compression at the human-edit stage is exactly the symptom of a missing editing pass between proposal-writer and red-team-review. The framework has prevention rules ("Hard cap: 2,000 words") but no skill that does the compression work. Worth considering.

### 5.2 No staff-paper skill

The user mentioned this in the brief. [reference/proposal-types/](../reference/proposal-types/) has 14 entries. None is a staff paper or decision memo. If the user wants one, it's a single new file in `reference/proposal-types/staff-paper.md` plus probably a section pattern. Cheap to add when needed; not a current gap unless an upcoming proposal needs it.

### 5.3 No skill that audits drafts for process language before export

This audit is itself the missing skill. The framework has compliance-check (req coverage) and evidence-check (claim grounding) and red-team Pink (compliance) but nothing that scans `drafts/` for the bleed risk: pattern labels, methodology vocabulary, internal-process boilerplate. A small `/draft-purity-check` would catch §3.1 automatically before the export step.

---

## 6. Specific edits

### Now

**6.1 Strip pattern annotations from the example deliverable.** [examples/cso-brief-acme/drafts/executive-summary.md](../examples/cso-brief-acme/drafts/executive-summary.md):
- Delete the `*(Annotations in italics show ...)*` line at line 3.
- Delete every `*[Pattern N: ...]*` annotation in lines 7, 13, 21, 23, 28.
- Move the explanatory walkthrough to a new file `examples/cso-brief-acme/working/pattern-walkthrough.md` keyed to specific lines.
- Update [examples/cso-brief-acme/README.md:18](../examples/cso-brief-acme/README.md) to read: "drafts/executive-summary.md — clean exemplar of all four writing patterns. See working/pattern-walkthrough.md for line-by-line analysis of which pattern is at work where."

**6.2 Add a no-labeling rule to proposal-writer.** [proposal-writer/SKILL.md:53-62](../.claude/skills/proposal-writer/SKILL.md), in the Writing Rules section, add one bullet:

> - **Apply patterns in the prose. Never label them in the output.** Theme statements, discriminator proof points, action captions, and ghosting are technique. The evaluator should *experience* them, not see them annotated. Inline labels like `[Pattern 1: Theme statement]` belong in working/ analysis, not drafts/.

**6.3 Fix the smoke test.** Add empty `.gitkeep` files (or directory placeholders) for the 8 missing scaffold dirs so [scripts/smoke-test.sh](../scripts/smoke-test.sh) passes:
```
templates/inputs/00_priority/.gitkeep
templates/inputs/01_customer/.gitkeep
templates/inputs/02_yourCompany/.gitkeep
templates/inputs/03_teammates/.gitkeep
templates/inputs/04_patterns/.gitkeep
templates/inputs/06_notes/.gitkeep
templates/drafts/.gitkeep
templates/reviews/.gitkeep
```

### Next

**6.4 Consolidate compliance-check into compliance-check (or split into /preflight-check).** Move the Pink-team-only checks from [red-team-review/SKILL.md:76-100](../.claude/skills/red-team-review/SKILL.md) (page limits, format, attachments, convention compliance, graphics conventions, white-paper additional checks) into [compliance-check/SKILL.md](../.claude/skills/compliance-check/SKILL.md). Then `--mode=pink` becomes a thin re-presentation of the compliance-check output. This eliminates the dual-output-file problem and makes the user's decision tree simpler.

**6.5 Move lessons-learned content out of SKILL.md files.** Migrate the SOCPAC and Senate-PRC lessons from [proposal-writer/SKILL.md:146-216](../.claude/skills/proposal-writer/SKILL.md) and [red-team-review/SKILL.md:441-473](../.claude/skills/red-team-review/SKILL.md) into [reference/proposal-conventions/white-paper.md](../reference/proposal-conventions/white-paper.md) and a new `reference/proposal-conventions/socpac-style.md` (or similar). Both skills already reference convention files; remove the inline duplication.

**6.6 Retire two of the new color-team modes.** [red-team-review/SKILL.md:14-37](../.claude/skills/red-team-review/SKILL.md) has 9 modes. For a small-team workflow, three suffice: compliance (current Pink), narrative (Red), rubric scoring (Gold), editorial QA (White Glove). `blue`, `black-hat`, and `storyboard-pink` are capture-phase activities that don't fit a skill named "review proposal drafts." Move them out (to `/capture-scorecard` or a new dedicated capture-review skill if needed). The framework doesn't need to encode every Shipley canonical step — it needs to be useful for one person writing 5-20 proposals a year, which is what [README.md:51](../README.md) says it's for.

**6.7 Add a "Don't label your moves" rule to proposal-writing-patterns.md.** [reference/proposal-writing-patterns.md](../reference/proposal-writing-patterns.md) is the authority. Add a section after the four patterns:

> ## Patterns are technique, not content
>
> The patterns above describe how to construct prose that scores well. They are not labels to be inserted into the prose. The evaluator should read theme statements, discriminator proof points, action captions, and ghosting *as natural prose* — never as labeled blocks. Inline annotations of pattern usage belong in working/ analysis files. They never appear in drafts/ or final/.

### Later

**6.8 Consider adding a /draft-purity-check skill.** Scans `drafts/*.md` before `/export-proposal` for: pattern labels (`[Pattern N`, `*\[Pattern`, `[Theme statement:`), methodology vocabulary in body text (`Shipley`, `compliance-check`, `Gold Team`, `pWin`, `Phase C`, `compliance matrix scaffolding`), internal review markers that escaped (`TBD:`, `[reviewer note:`), and unstripped `<!-- ... -->` of any kind. Output: `reviews/draft-purity.md`. Run as part of `/export-proposal` preflight.

**6.9 Consider adding an /editor skill.** The "Final Pass" instruction at [proposal-writer/SKILL.md:130-134](../.claude/skills/proposal-writer/SKILL.md) does too little, and the white-paper compression failure documented at [proposal-writer/SKILL.md:148](../.claude/skills/proposal-writer/SKILL.md) is real evidence of a missing pass. Scope: rewrite for length, remove redundancy across sections, tighten verb choice, eliminate filler adjectives, enforce sentence-length norms from `reference/proposal-conventions/<vehicle>.md`. Reads `drafts/`, writes `drafts/` with a backup at `drafts/.pre-edit/`. This is the skill the user may have been remembering.

**6.10 Audit the registry of section-patterns and proposal-conventions.** Not done in this audit. Worth a follow-up read to confirm no process-bleed risk in those reference files before they get pulled into draft generation.

---

## 7. Smoke-test results

**Run:** `bash scripts/smoke-test.sh` from the worktree root.

**Result:** **FAIL** — 8 issues, all in the same category.

```
── Template scaffold consistency ──
  ✗ FAIL: scaffold dir MISSING: templates/inputs/00_priority
  ✗ FAIL: scaffold dir MISSING: templates/inputs/01_customer
  ✗ FAIL: scaffold dir MISSING: templates/inputs/02_yourCompany
  ✗ FAIL: scaffold dir MISSING: templates/inputs/03_teammates
  ✗ FAIL: scaffold dir MISSING: templates/inputs/04_patterns
  ✗ FAIL: scaffold dir MISSING: templates/inputs/06_notes
  ✗ FAIL: scaffold dir MISSING: templates/drafts
  ✗ FAIL: scaffold dir MISSING: templates/reviews

  Checks run: 273
  Passes:     265
  Warnings:   0
  Failures:   8
```

**Diagnosis:** Empty directories don't survive Git checkout. The `templates/` scaffold was likely created with empty subdirs that never got `.gitkeep` placeholders. `templates/inputs/05_graphic_standards/` does exist (because it has files); the others don't.

**Fix:** Per §6.3, add `.gitkeep` files in each of the 8 missing dirs. One-line shell command, instant resolution. Then re-run smoke test — expect 273/273 pass.

**Caveat:** Because this audit is read-only, the fix is *recommended* but not applied. The user should add the placeholders themselves or delegate.

---

## 8. Open questions for the user

1. **The "editor" skill you mentioned** — does it exist in another worktree, or were you remembering an intended skill that was never added? If the latter, see §6.9 for proposed scope.
2. **Are the Pattern annotations in [examples/cso-brief-acme/drafts/executive-summary.md](../examples/cso-brief-acme/drafts/executive-summary.md) intentional teaching scaffolding** (and you accept the risk that future Claude runs will copy the labeling style), **or were they a working note that wasn't cleaned up**? The fix differs.
3. **Should Shipley-canonical color modes (Blue, Black Hat, Storyboard-Pink) stay in the framework** as documented options, or be retired? They are aspirational for a small-team workflow and don't appear in any example or active proposal. Keeping them adds skill-prompt size on every red-team-review invocation.
4. **Do you want a /draft-purity-check skill** that automates §3.x scanning before export? It's cheap (deterministic regex scan, no AI cost) and would catch the kind of bleed this audit found by hand.
5. **Lessons-learned blocks inside SKILL.md files** — refactor into `reference/proposal-conventions/` (per §6.5), or keep inline for proximity to the rule they amend? The cost of refactor is one-time; the cost of duplication is recurring drift.
6. **/proposal-manager seeds the compliance matrix; /proposal-writer maintains it; /compliance-check recomputes it** — is this three-skill ownership working in practice, or have you seen drift? If drift, worth tightening to a "compliance-check is authoritative for Status; nothing else writes Status" rule.
7. **Worktree state.** This audit ran on `claude/modest-kapitsa-c6bab0` (clean). Did anything substantive land on `main` after this branch was created? `git log --oneline main..HEAD` would tell you whether there's drift to resolve.

---

## Appendix — files read in full

- [CLAUDE.md](../CLAUDE.md), [OVERVIEW.md](../OVERVIEW.md), [README.md](../README.md)
- All 21 SKILL.md files under [.claude/skills/](../.claude/skills/)
- [reference/proposal-writing-patterns.md](../reference/proposal-writing-patterns.md)
- [reference/proposal-types/cso-brief.md](../reference/proposal-types/cso-brief.md) (representative; registry of 14 type files listed but not all read)
- [examples/cso-brief-acme/README.md](../examples/cso-brief-acme/README.md)
- [examples/cso-brief-acme/drafts/executive-summary.md](../examples/cso-brief-acme/drafts/executive-summary.md)
- [examples/cso-brief-acme/drafts/rom.md](../examples/cso-brief-acme/drafts/rom.md)
- [examples/cso-brief-acme/working/graphics-brief.md](../examples/cso-brief-acme/working/graphics-brief.md)
- [examples/cso-brief-acme/reviews/gold-team-scorecard.md](../examples/cso-brief-acme/reviews/gold-team-scorecard.md)
- `git log --oneline -30`, `git log --stat -10`, `git log --all --oneline | head -50`
- `bash scripts/smoke-test.sh` output

Files not read but referenced in audit (read titles/paths only):
- [reference/methodology/](../reference/methodology/) — Shipley alignment library (commit ce88fa7)
- [reference/proposal-conventions/](../reference/proposal-conventions/) — vehicle conventions
- [reference/section-patterns/](../reference/section-patterns/) — section templates
- [reference/evaluator-rubrics/](../reference/evaluator-rubrics/) — Gold Team rubrics
- [reference/portal-formats/](../reference/portal-formats/) — portal library
- [tools/md_to_docx.py](../tools/md_to_docx.py), [tools/compliance_to_xlsx.py](../tools/compliance_to_xlsx.py)

If a deeper read of any of these would change the picture, flag it and I'll come back.
