---
name: proposal-writer
description: Draft evaluator-ready proposal sections from the approved narrative spine and solution architecture, in two passes — draft-loose (confident, in-voice prose) then bind (evidence, verification, compliance). Drafts to the selected narrative operating mode. Writes to drafts/.
phase: drafting
composes: [narrative-spine, proposal-storyboard, proposal-solution-architect, capture-intent]
conflicts_with: [proposal-editor]  # don't run a separate style/compression pass; that's proposal-editor's job
---

# Proposal Writer Skill

## Purpose
Turn the approved narrative spine and solution architecture into proposal-ready section drafts saved to local files.

## The Two-Pass Model

The writer runs in **two passes**, because composing a compelling argument and verifying every fact are different cognitive jobs — and doing them at once produces stilted, slot-filled prose. The first pass writes the argument; the second pass makes it traceable.

| Mode | What it does | Reads | Writes |
|---|---|---|---|
| `draft-loose` (Pass 1) | Writes each section as a confident, in-voice argument from the narrative spine, in the selected narrative operating mode. Evidence markers, the section completeness checklist, pattern enforcement, and compliance-matrix updates are **suspended**. | spine, storyboard, capture-intent, architecture, voice guide, operating modes | `drafts/loose/<section-id>.md` |
| `bind` (Pass 2) | Takes the loose draft and makes it submission-ready: attaches evidence citations, verifies every claim, flags unsupported claims, adds any genuinely missing scoring element, updates the compliance matrix. Touches prose **only** for verification — never for style. | the loose draft + evidence ledger, compliance matrix, proposal-plan, competitor-assessment | `drafts/<section-id>.md` |
| `full` (default) | Runs `draft-loose` then `bind` for each section, in sequence. | — | both |

**Invocation.** `/proposal-writer` with no mode runs `full`. `/proposal-writer --mode=draft-loose` or `--mode=bind` runs a single pass — useful for inspecting the loose draft before binding, or re-binding after a hand edit.

**Why the split.** When generation has to satisfy the compliance matrix, the pattern checklist, the section template, and the evidence protocol *while* composing, there is no room left to invent rhythm — the result reads like filled-in slots. `draft-loose` gives composition full freedom; `bind` does verification afterward, on real prose, without touching cadence.

> Note: this skill has two senses of "mode." The **pass mode** (`draft-loose` / `bind` / `full`) selects which pass runs. The **narrative operating mode** (`compressed-brief`, `solution-brief`, etc., below) is the prose strategy for the response. Every `draft-loose` run is written in one narrative operating mode.

## Inputs

### Always read (mandatory)
1. `working/proposal-type.md` — **read first.** If this skill is in `skipped_skills`, exit with "Skipped for type <type_id>." Adapt tone, section set, and page targets to `evaluator_framing` + `page_target` + `section_patterns`.
2. **`working/narrative-spine.md`** — **read second, as primary orientation.** The approved one-page argument the whole proposal makes (produced by `/narrative-spine`). Every section drafted advances one movement of this argument. Do not invent a new argument — draft the one the spine commits to. If `working/narrative-spine.md` does not exist, recommend the user run `/narrative-spine` first; proceed only if the storyboard is strong enough to draft from on its own.
3. `working/proposal-plan.md` — eval criteria and win themes.
4. `working/solution-strategy.md`
5. `working/architecture-concept.md`
6. **`reference/section-patterns/<section_patterns>.md`** — derived from `section_patterns` in `working/proposal-type.md`. Declares section order, required/optional sections, per-section purpose.
7. **`reference/editorial-voice-guide.md`** — voice discipline applies in **both** passes. Loose is free in form and confidence; it is not free to be sloppy or to use marketing language.
8. **`reference/narrative-operating-modes.md`** — the prose strategy for the response. Select the operating mode before `draft-loose` begins (see "Narrative Operating Mode" below).
9. `working/compliance-matrix.md` — the traceability map. Required reading for `bind` (see "Compliance Matrix Maintenance"); not needed for `draft-loose`.

### Read if relevant
- `working/storyboard.md` — if `/proposal-storyboard` was run; the section-by-section decomposition of the spine. Primary `draft-loose` planning input when present. Carries the per-section `Reader Movement`, `Narrative Mode`, `Transition Job`, and `Compression Rule` fields.
- `working/capture-intent.md` — strategic guidance: customer beliefs, **prohibited claims**, posture, ghosting direction. Binding on **both** passes — `draft-loose` may not make claims capture-intent prohibits.
- `working/requirement-matrix.md`, `working/capability-matrix.md`, `working/assumptions-and-risks.md` — grounding for the relevant sections.
- `my-company/evidence-ledger.json` — required for `bind` when Phase C is enabled (evidence citation).
- `working/competitor-assessment.md` — for ghosting; only ghost weaknesses documented here.
- `working/graphics-brief.md` — for action captions in `bind`.
- **`reference/proposal-conventions/<vehicle-id>.md`** — calibrated conventions, when a convention file exists. Mapping: `full-proposal`→`far-rfp.md`; `sbir`→`sbir.md`; `gsa-mas-task-order`→`gsa-mas.md` (plus a Security Volume per `reference/section-patterns/security-volume.md` when cleared work is required); `white-paper`→`white-paper.md`; other patterns fall through to section-patterns alone.

## Outputs

**Output filenames derive from the pattern file's `section_order`, not hardcoded.** Reading `reference/section-patterns/<section_patterns>.md` yields a list of section ids; the writer produces one file per required section (and each optional section where source material exists).

- `draft-loose` writes `drafts/loose/<section-id>.md`
- `bind` reads `drafts/loose/<section-id>.md` and writes `drafts/<section-id>.md`

The loose draft is **kept**, not overwritten — it is the inspectable record of the argument before verification, and the input `bind` re-reads.

**Dispatch by `section_patterns`:**

| `section_patterns` | Typical draft files produced |
|---|---|
| `full-proposal` | executive-summary.md, problem-statement.md, capability-overview.md, technical-approach.md, management-approach.md, past-performance.md, path-forward.md, conclusion.md |
| `white-paper` | executive-summary.md, problem-statement.md, proposed-approach.md, outcomes-and-value.md, team-and-credibility.md (optional), rom-or-next-steps.md (optional) |
| `baa` | executive-summary.md, research-hypothesis.md, technical-approach.md, work-plan-and-milestones.md, principal-investigator-bio.md, prior-research-results.md (optional), schedule-and-gates.md |
| `ota` | executive-summary.md, statement-of-objectives-response.md, prototype-project-scope.md, technical-approach.md, milestone-schedule.md, team-composition.md, data-rights-assertions.md, follow-on-production.md |
| `sbir` | identification-and-significance.md, phase-i-feasibility-or-phase-ii-prototype.md, technical-objectives.md, work-plan.md, key-personnel.md, commercialization-plan.md, budget-narrative.md |
| `rfi` | cover-letter.md, question-by-question-response.md, capability-summary.md |
| `sources-sought` | company-identification.md, relevant-experience-table.md, capability-summary.md |
| `rom` | rom.md (single-file artifact, with section_order's subsections as H2 headings within) |

**Rule:** Do NOT produce drafts for sections not listed in the pattern's `section_order`. If the solicitation calls for a section not in the current pattern set, either (a) add it to the pattern file (update the registry too) or (b) note it as an override in the proposal-brief.

## Narrative Operating Mode

Before `draft-loose` begins, select one **narrative operating mode** for the response. The mode is the prose strategy — it controls how much setup, depth, and explanation the writing can afford. It is the difference between a draft that fits its proposal type and one the editor has to rescue.

1. Read `working/proposal-type.md` and `reference/narrative-operating-modes.md`. If `/proposal-storyboard` recorded a mode in its header, use that; the storyboard and the writer must agree.
2. Select one mode for the response from `page_target`, `submission_mechanism`, and `evaluator_framing`:
   - `compressed-brief` — 1–5 page briefs, short white papers, tight web-form fields
   - `solution-brief` — 5–10 page CSO / OTA / white-paper responses
   - `scored-volume` — FAR, IDIQ, OTA full, and CSO full proposals
   - `technical-merit` — SBIR and BAA responses
   - `market-research` — RFI and sources-sought
   - `pricing-artifact` — ROM and price narratives
3. Apply the mode from the first sentence — to paragraph length, amount of setup, technical depth, and use of bullets. Do not leave length or register correction for the editor.

**Mode discipline.** A two-page white paper does not get a full conceptual tutorial. A scored FAR volume does not get airy thought-leadership prose. An RFI does not get win-theme theatrics. A ROM does not get a sales arc. When in doubt, choose the shorter, plainer mode — overexplaining is the default failure.

---

## Pass 1 — Draft-Loose

**Goal:** write each section as a confident argument a senior capture lead would make explaining the case to a sharp colleague — in the selected narrative operating mode. Make the case; sound like a person.

**Suspended in this pass** — do not do any of these now, they belong to `bind`:
- No `<!-- evidence: -->` markers.
- No compliance-matrix updates.
- No mandatory eight-element section template, in any order.
- No mechanical four-pattern enforcement.
- No writing "to pass Gold Team."

**Do:**
- **Draft the spine's argument, in the operating mode.** Each section advances one movement of `working/narrative-spine.md` (the storyboard, if present, says which), at the depth and length the operating mode allows.
- **Move the reader.** Each section should move the evaluator from one belief to the next — problem recognized → answer understood → feasibility believed → risk reduced → next action obvious. Use the storyboard's `Reader Movement` and `Transition Job` fields when present; infer them when not. A section that only "tells the reader more about our capability" is not earning its place.
- **Open concern-first.** Lead with the customer's mission problem, the evaluator's question, a load-bearing number, or a blunt statement of stakes — whatever states the section's point fastest. Do **not** open with a dramatized or cinematic scene ("Picture the demonstration room...", "In August, four personas will..."); staged openings read as cheesy and weaken the impression that the team understands the mission. Do **not** open every section with the same theme-statement formula. Vary openings across sections — the human element comes from visible command of the problem, not theatrics.
- **Make transitions carry meaning.** Connect sections by consequence, selection, proof, or decision — not by announcing structure ("This section discusses...", "The following paragraphs describe...").
- **Write in voice.** Apply `reference/editorial-voice-guide.md`: direct, clinical, operationally credible; no marketing adjectives; observable facts over claims. Loose means free in *form and confidence* — not free to be sloppy.
- **Assert with confidence.** You may state claims that will need evidence — `bind` will check them and attach citations or flag gaps. Write the strong version now; do not pre-hedge every sentence.

**Honesty boundary — loose is not a license to fabricate.**
- Do NOT invent capabilities, past performance, customers, certifications, or numbers. Every fact must trace to the architecture, solution strategy, or source material.
- Do NOT make any claim `working/capture-intent.md` lists under "Proposal Must Avoid" / prohibited claims. Form is free; prohibited claims are still prohibited.
- If you need a fact you do not have, write the sentence and leave a `[NEEDS: <what>]` marker inline rather than inventing it.

**Output:** `drafts/loose/<section-id>.md`. Clean prose — no evidence markers, no matrix notes.

---

## Pass 2 — Bind

**Goal:** make the loose draft submission-ready and fully traceable **without rewriting it for style.** Bind preserves the loose draft's voice and structure. It touches prose only to attach evidence, soften an unsupported or risky claim, or add a genuinely missing scoring element.

For each loose draft, in order:

### 1. Verify and cite every claim

Check every factual claim against `working/architecture-concept.md`, `working/solution-strategy.md`, and `my-company/evidence-ledger.json` (when Phase C is enabled).

- For a claim with backing evidence, attach an HTML-comment citation: `Our platform operated at [customer] for 14 months in disconnected mode. <!-- evidence: EV-022 -->`. HTML comments are invisible in markdown render and docx export but machine-readable. Multiple IDs allowed: `<!-- evidence: EV-022, EV-055 -->`.
- For a claim with **no** ledger backing, mark it explicitly: `<!-- evidence: CLAIM-UNSUPPORTED -->`. Do NOT delete the claim and do NOT silently launder it into confident prose. If the claim is also strategically risky, soften, localize, or qualify it — then keep the marker.
- Resolve every `[NEEDS: ...]` marker from Pass 1 — supply the fact if it exists, or convert to `CLAIM-UNSUPPORTED` and flag for the user.
- Precedence for citation sources: `my-company/evidence-ledger.json` > `drafts/past-performance.md` > `inputs/02_yourCompany/past-performance.md`. See `reference/schemas/evidence-ledger.schema.json`.

### 2. Check — do not enforce — the winning patterns

Read `reference/proposal-writing-patterns.md` and the type's pattern applicability table. The four patterns (theme statement, discriminator proof point, action caption, ghosting) are a **completeness check on the loose draft, not a generation template.**

For each scoring section, confirm it lands: a clear point up front, at least one discriminator proof point, a tie to the evaluation criterion / requirement, team credibility, and an evaluator takeaway. If one is **genuinely missing** *and* adding it strengthens the section, add it — minimally, in the section's own voice, where the argument naturally wants it.

- Do NOT reorder the loose draft to match a fixed element sequence.
- Do NOT add a pattern to check a box. A forced theme statement on a 200-word boilerplate section makes it worse.
- **Respect the operating mode.** In `compressed-brief` and `solution-brief` modes, do not add every pattern element — the shortest sequence that lands the movement (claim, mechanism, proof, value, next action) is correct, and an element that makes the prose feel procedural should be folded into the sentence that already carries the point. `scored-volume` sections carry the full set; `market-research` and `pricing-artifact` carry almost none.
- Patterns apply to **scoring sections** (technical approach, management, past performance, differentiators, risk). Reps and certs, CDRL lists, staffing rosters get only what the solicitation requires.
- **White papers:** apply theme statement and discriminator proof point where a section makes a scoring claim; skip the discriminator/credibility/ghosting sequence in informational sections. Self-positioning stays in the dedicated position section, never in evidence tables.
- **Ghosting:** only ghost competitor weaknesses documented in `working/competitor-assessment.md`. If it is absent, do not invent ghosts.
- **Action captions:** for each referenced graphic, read its brief in `working/graphics-brief.md` and write a caption that asserts what the graphic *proves*.

### 3. Update the compliance matrix

If `working/compliance-matrix.md` exists, every section bound **must** update it — this is how the writer hands off to compliance-check and red-team.

For each section:
1. Identify which Req IDs the section addresses (find rows whose Requirement text is treated in this section).
2. For each matching row set: **Section** (draft filename + heading path, e.g. `drafts/technical-approach.md Section 3.2`); **Page** (`TBD` until the Word doc is assembled); **Status** (`Drafted` for substantive coverage, `Partial` for light coverage needing more, leave `Planned` if explicitly deferred); **Evidence** (a 1-line pointer).
3. If a requirement has no obvious home, do NOT assign it to an unrelated section — leave it `Planned` and flag it for compliance-check.
4. Do not flip rows to `Covered` — that is compliance-check's call, or a human's.
5. Never delete rows, never edit the Requirement text column, never renumber Req IDs.

After binding, recommend the user run `/compliance-check`.

---

## Final Pass (after `bind` or `full`)
- Redundancy check — the same point should not be argued in two sections.
- Narrative-mode check — the prose matches the selected operating mode; no over-explaining for the type, no under-explaining.
- Reader-movement check — each section moves the evaluator; transitions carry consequence, selection, proof, or decision.
- Unsupported-claim check — every `CLAIM-UNSUPPORTED` marker is intentional and flagged, not an oversight.
- Requirement coverage check — via the compliance matrix.
- Spine check — every section still advances its movement of the narrative spine; the through-line survives.

## Critical Rule
**All draft content must be written to files (`drafts/loose/` and `drafts/`) — not just displayed in chat.**

## Activity Trail
On completion, append to `working/activity.md`:

```
## <timestamp> — proposal-writer [<mode>] — drafted/bound <N sections>, <M matrix rows updated> → drafts/
```

Append one JSON line per pass to `working/ai-runs.jsonl` per [`reference/schemas/ai-run.schema.json`](../../../reference/schemas/ai-run.schema.json) with `job_type: "drafting"` and `notes` recording the pass mode and the narrative operating mode.
