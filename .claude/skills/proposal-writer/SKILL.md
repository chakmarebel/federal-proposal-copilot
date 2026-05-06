---
name: proposal-writer
description: Use this skill to draft concise, evaluator-friendly proposal text from the approved solution architecture and requirement mapping. Reads from working/ files and writes drafts to drafts/ directory.
---

# Proposal Writer Skill

## Purpose
Turn approved solution strategy and architecture into proposal-ready narrative saved to local draft files.

## Inputs
Read in this order:
1. `working/proposal-type.md` — **read first.** If this skill is in `skipped_skills`, exit with "Skipped for type <type_id>." Adapt tone, section set, and page targets to `evaluator_framing` + `page_target` + `section_patterns`.
2. `working/compliance-matrix.md` (if it exists) — this is the traceability map. Every section you draft must update it (see "Compliance Matrix Maintenance" below).
3. `working/proposal-plan.md` — eval criteria and win themes
4. `working/requirement-matrix.md`
5. `working/capability-matrix.md`
6. `working/assumptions-and-risks.md`
7. `working/solution-strategy.md`
8. `working/architecture-concept.md`
9. `working/storyboard.md` (if exists)
10. **`reference/section-patterns/<section_patterns>.md`** — derive from `section_patterns` field in `working/proposal-type.md`. E.g., if the type is `far-rfp`, its `section_patterns: full-proposal` → read `reference/section-patterns/full-proposal.md`. This file declares the section order, required/optional sections, per-section templates, and which winning patterns apply per section.
11. **`reference/proposal-conventions/<vehicle-id>.md` (if it exists)** — calibrated structural and stylistic conventions for this proposal type, distilled from winning examples. Apply heading numbering conventions (bracketed solicitation refs where applicable), sentence-length norms, customer-language-adoption discipline, bullet/figure density. Mapping:
    - `section_patterns: full-proposal` → `reference/proposal-conventions/far-rfp.md`
    - `section_patterns: sbir` → `reference/proposal-conventions/sbir.md`
    - `section_patterns: gsa-mas-task-order` → `reference/proposal-conventions/gsa-mas.md` (also produces a separate Security Volume per `reference/section-patterns/security-volume.md` when the solicitation requires cleared work)
    - Other patterns: fall through to section-patterns alone if no convention file exists yet.

## Outputs

**Output filenames derive from the pattern file's `section_order`, not hardcoded.** Reading `reference/section-patterns/<section_patterns>.md` yields a list of section ids; the writer produces one file per required section (and each optional section where source material exists):

```
drafts/<section-id>.md
```

**Dispatch by `section_patterns`:**

| `section_patterns` (from proposal-type.md) | Typical draft files produced |
|---|---|
| `full-proposal` | executive-summary.md, problem-statement.md, capability-overview.md, technical-approach.md, management-approach.md, past-performance.md, path-forward.md, conclusion.md |
| `white-paper` | executive-summary.md, problem-statement.md, proposed-approach.md, outcomes-and-value.md, team-and-credibility.md (optional), rom-or-next-steps.md (optional) |
| `baa` | executive-summary.md, research-hypothesis.md, technical-approach.md, work-plan-and-milestones.md, principal-investigator-bio.md, prior-research-results.md (optional), schedule-and-gates.md |
| `ota` | executive-summary.md, statement-of-objectives-response.md, prototype-project-scope.md, technical-approach.md, milestone-schedule.md, team-composition.md, data-rights-assertions.md, follow-on-production.md |
| `sbir` | identification-and-significance.md, phase-i-feasibility-or-phase-ii-prototype.md, technical-objectives.md, work-plan.md, key-personnel.md, commercialization-plan.md, budget-narrative.md |
| `rfi` | cover-letter.md, question-by-question-response.md, capability-summary.md |
| `sources-sought` | company-identification.md, relevant-experience-table.md, capability-summary.md |
| `rom` | rom.md (single-file artifact, with section_order's subsections as H2 headings within) |

**Rule:** Do NOT produce drafts for sections not listed in the pattern's `section_order`. If the solicitation calls for a section that isn't in the current pattern set, either (a) add it to the pattern file (update the registry too) or (b) note it as an override in the proposal-brief.

## Writing Rules
- Write to score
- Be concise
- Avoid repeating the same point in multiple sections
- Use explicit technical language
- Avoid unsupported adjectives
- Make strengths easy for evaluators to find
- Reduce perceived execution risk
- **Apply the four writing patterns** per `reference/proposal-writing-patterns.md` (see next section)
- Do not label or reference writing patterns explicitly in the output. Patterns are applied implicitly and must not appear in the text.

## Winning Patterns (mandatory, type-gated)

Read `reference/proposal-writing-patterns.md` before drafting. It defines four patterns and specifies which apply to each proposal type:

| Pattern | Purpose |
|---|---|
| **Theme statement** | First sentence of every major section — states *what*, *why it matters to the Government*, and *proof hook* |
| **Discriminator proof point** | Claim + concrete evidence + relevance to eval criterion + scope reference — at least one per scoring section |
| **Action caption** | Text under every graphic that asserts what the graphic *proves*, not what it shows |
| **Ghosting** | Positive framing of your approach that implicitly contrasts with a known competitor weakness (never name the competitor) |

**Applicability dispatch:**

1. Read `working/proposal-type.md` → note the `type_id`
2. Look up that type in the applicability table in `reference/proposal-writing-patterns.md`
3. For each pattern marked "Required," the writer MUST apply it. For "Recommended," apply if section length supports it. For "Not applicable," do not force it.

**Inputs for pattern application:**
- **Theme statements** — use win themes from `working/proposal-plan.md` (the themes `proposal-manager` extracted)
- **Discriminator proof points** — use discriminators from `working/proposal-plan.md` and, if Phase C is enabled (i.e., `my-company/evidence-ledger.json` exists), **cite evidence items by ID** in an inline HTML comment after each proof-point claim:
  ```
  Our platform operated at [customer] for 14 months in disconnected mode. <!-- evidence: EV-022 -->
  ```
  HTML comments are invisible in markdown render and docx export but machine-readable for tooling. Multiple IDs allowed: `<!-- evidence: EV-022, EV-055 -->`.
  If you make a claim but cannot find a matching evidence item in the ledger, **mark it explicitly** with `<!-- evidence: CLAIM-UNSUPPORTED -->` so `/evidence-check` and Gold Team can surface it. Do NOT silently make unsupported claims.
  See `reference/schemas/evidence-ledger.schema.json` for the ledger format and `reference/examples/evidence-ledger.example.json` for an example. Precedence for citation sources: `my-company/evidence-ledger.json` > `drafts/past-performance.md` (as prose reference) > `inputs/02_yourCompany/past-performance.md`.
- **Action captions** — for each graphic referenced, read its brief in `working/graphics-brief.md` and cite the asserted proof
- **Ghosting** — read `working/competitor-assessment.md`. Only ghost weaknesses explicitly documented there. If competitor-assessment is absent (e.g., skipped for this type), do not invent ghosts.

**Red-team integration.** The Gold Team pass (`red-team-review --mode=gold`) scores these four patterns against the rubric in `reference/evaluator-rubrics/`. Producing them on the first draft is the writer's job; fixing their absence in Gold Team is expensive rework. Write to pass Gold Team the first time.

## Section Standard
For each major section, in order:

1. **Theme statement** (1 sentence — what/why/proof hook) — see Pattern 1
2. **Point** — the main claim of this section
3. **How the solution works** — technical substance
4. **Discriminator proof point** (at least 1 per scoring section) — see Pattern 2
5. **Tie to requirement or mission outcome** — connect to Section M / evaluation criterion
6. **Why the team is credible** — cite past performance or credentials
7. **Evaluator takeaway** — close with the one thing the evaluator should remember
8. **Graphic references** — each with an action caption per Pattern 3

Ghosting (Pattern 4) is woven into the narrative where applicable — typically in the *how the solution works* and *discriminator* subsections, not as its own block.

**Don't box-check.** Forcing a theme statement onto a 200-word boilerplate section makes it worse. These patterns apply to **scoring sections** — the technical approach, management approach, past performance, differentiators, risk reduction, etc. Reps and certs, CDRL lists, staffing rosters, and similar structural content get only what the solicitation requires.

## Compliance Matrix Maintenance

If `working/compliance-matrix.md` exists, every draft section you write or update **must** update the matrix. This is non-negotiable — the matrix is how the writer hands off to compliance-check and red-team.

For each section drafted:
1. Identify which Req IDs the section addresses (read the matrix, find rows whose Requirement text is treated in this section).
2. For each matching row, set:
   - **Section:** the draft filename + heading path (e.g., `drafts/technical-approach.md §3.2`)
   - **Page:** leave as `TBD` until the final Word doc is assembled (or fill with an estimate)
   - **Status:** `Drafted` if you wrote substantive coverage; `Partial` if you only touched it lightly and it needs more; leave as `Planned` if you explicitly deferred it.
   - **Evidence:** a 1-line note pointing to the evidence (e.g., "PBKDF2 rationale in §3.2; architecture graphic in Figure 3")
3. If you find a requirement with no obvious home, do NOT assign it to an unrelated section. Leave it `Planned`, and flag it for the next compliance-check run.
4. Do not flip rows to `Covered` yourself — that's for compliance-check after a coverage heuristic pass, or a human confirming.
5. Never delete rows. Never edit the Requirement text column. Never renumber Req IDs.

After drafts are updated, recommend the user run `/compliance-check` to recompute counters and flag gaps.

## Final Pass
Always perform:
- Redundancy cleanup
- Unsupported-claim check
- Requirement coverage check (now via compliance-matrix.md)
- Clarity tightening

## Critical Rule
**All draft content must be written to files in drafts/ — not just displayed in chat.**

## Activity Trail
On completion, append to `working/activity.md`:

```
## <timestamp> — proposal-writer — drafted/updated <N sections>, <M matrix rows updated> → drafts/
```

## Lessons Learned (Calibration Session — White Paper Drafting)

### Section Structure
- **Overview sections must be tight (~200 words).** Section 3 "What is it" should introduce the platform and list 3 core functions as bullets. Detail lives in Section 4 subsections. Never repeat capability details in both.
- **Closing pivot sentence connects sections.** End the overview with "The following section describes how these capabilities address each challenge" — explicitly hands off to the detail section.
- **Problem statements lead with what's broken.** "Enterprise AI assumes connectivity — that assumption fails" is stronger than "We need to enable disconnected AI."

### Editorial Standards
- Single space after periods (never double)
- "Government" not "Govt" in formal white papers
- "Department of War (DoW)" — verify intentional terminology with the author
- Normalize section numbering: "5." not "5.0"
- Use proper Word heading styles (Heading1/Heading2), never manual bold on Normal paragraphs
- Acronyms defined on first use, then abbreviated: "subject matter expert (SME)"

### Tone Calibration
- Position data capture at the edge as **optional** — "when operational data is available" rather than "data captured at the edge is continuously leveraged"
- Avoid implying mandatory collection that could trigger security/privacy concerns
- Frame commitments as what your company **will deliver**, not what the customer must do
- Use "[Your Company] or Government-provided" rather than "ours or Govt-provided"

### Document Formatting (Word)
- Apply Heading1 to numbered sections, Heading2 to sub-sections — enables TOC and navigation
- Times New Roman throughout (body, headers, footers)
- Header: right-aligned document title, with centered "UNCLASSIFIED" above
- Footer: left-aligned "Company | Document Title", right-aligned "Page X"
- Figure captions belong in the document text below each image, not embedded in the graphic
- Add classification marking (UNCLASSIFIED) and distribution statement (A, D, or F)
- Remove blank spacer paragraphs — use proper paragraph spacing instead

### Submission Package
- Cover page as standalone docx: classification marking, title, subtitle, prepared-for, date, POC, distribution statement
- Submission email: CTO-friendly (60-second read), three bullets (operational now, delivery commitment, low barrier), clear ask
