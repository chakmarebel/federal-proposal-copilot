# 03 — Walking Through Your First Proposal

A guided tour from "I have a solicitation" to "I have a submission package." Use a real, low-stakes solicitation (an SBIR topic, an RFI, or a sources sought) for the first run.

## Step 0 — Pick a proposal type

The framework supports many federal proposal vehicles, each with different rules:

| Type | When to use |
|---|---|
| `far-rfp` | FAR Part 15 RFP with full Section L/M (most competitive RFPs) |
| `idiq-to` | Standalone task order under non-MAS IDIQ |
| `gsa-mas-task-order` | Multi-vendor task order or BPA under a GSA MAS Schedule |
| `sbir` | SBIR/STTR Phase I, II, or Direct-to-Phase-II |
| `baa` | Broad Agency Announcement (research) |
| `ota` | Other Transaction Authority prototype |
| `cso` | Commercial Solutions Opening |
| `rfi` | Request for Information (no award) |
| `sources-sought` | Sources Sought / market research notice |
| `white-paper` | Capability paper / unsolicited proposal |
| `rom` | Rough Order of Magnitude pricing response |

Browse [reference/proposal-types/](../../reference/proposal-types/) for the full catalog including page targets, required artifacts, and skill chain.

## Step 1 — Scaffold the workspace

```
/new-proposal
```

The skill asks for:
1. Short name (becomes directory name — e.g., "agency-x-rfi", "sbir-fy26-topic1")
2. Full title (cover-page text)
3. Customer/program (e.g., "Air Force Research Lab, Information Directorate")
4. Due date
5. Proposal type (from the menu above)

It creates:
```
proposals/<short-name>/
├── inputs/
│   ├── 00_priority/      <- DROP YOUR SOLICITATION HERE
│   ├── 01_customer/
│   ├── 02_yourCompany/
│   ├── 03_teammates/
│   ├── 04_patterns/
│   ├── 05_graphic_standards/
│   └── 06_notes/
├── working/
├── drafts/
├── graphics/
├── reviews/
└── final/
```

It also writes `working/proposal-type.md` declaring the type's required skills, page targets, and pricing artifact. **All subsequent skills read this file first** to know which workflow applies.

## Step 2 — Drop the solicitation

Save the solicitation PDF/DOCX/Markdown into `proposals/<short-name>/inputs/00_priority/`. Optionally also drop:
- Customer briefings, prior RFIs, market-research notes → `inputs/01_customer/`
- Your company's relevant capability docs → `inputs/02_yourCompany/`
- Teammate capability docs (if teaming) → `inputs/03_teammates/`
- Reference architectures from prior wins → `inputs/04_patterns/`

Plain `.md` files are fastest because Claude reads them directly. PDFs/DOCX work but the AI does extra parsing.

## Step 3 — Run `/proposal-manager`

```
/proposal-manager
```

This is the most important skill in the chain. It produces:

| Output | What it is |
|---|---|
| `working/proposal-plan.md` | Win themes, evaluation criteria, bid/no-bid rationale |
| `working/compliance-matrix.md` | Every requirement, mapped to a compliance row, with status tracking |
| `working/requirement-matrix.md` | Solution-side view: requirements grouped by capability area |

Read these. Edit them by hand if the AI got something wrong. The compliance matrix in particular is the spine of the rest of the work — every subsequent skill updates it.

## Step 4 — Optional capture skills

For competitive bids, run these before drafting:

```
/customer-intel               # Open-source research on the customer
/competitor-assessment        # Bidder Comparison Chart, teaming gaps
/capture-scorecard            # 9-dimension go/no-go check
```

For lighter-weight bids (RFIs, SBIRs, white papers), the proposal type often skips these — check `working/proposal-type.md` to see what's gated for your type.

## Step 5 — Architect the solution

```
/proposal-solution-architect
```

Produces `working/architecture-concept.md`, `working/solution-strategy.md`, `working/capability-matrix.md`, `working/assumptions-and-risks.md`.

**Review these before drafting.** Solution architecture decisions made here shape every section. If the AI misunderstood something, fix it now — fixing it after drafting is expensive.

## Step 6 — Build the past performance section

```
/past-performance
```

Maps your past performance repository to evaluation criteria, drafts PPQ narratives if required, builds the Past Performance Coverage Matrix (the highest-leverage compliance artifact for many vehicle competitions).

## Step 7 — Pricing

```
/pricing-analyst
```

The skill dispatches based on `pricing_artifact` in `working/proposal-type.md`:
- `rom` → ROM range markdown (white papers, RFIs)
- `sbir-budget` → SBIR line-item budget xlsx
- `gsa-mas-pricing` → labor-category × period workbook
- `ota-milestones` → milestone payment schedule
- `cso-commercial` → commercial pricing
- `far-cost-volume` → full FAR cost volume with BOEs

Output lands in `working/pricing-inputs.md` plus a vehicle-specific artifact in `final/`.

## Step 8 — Graphics

```
/proposal-graphics
```

Drafts graphics brief in `working/graphics-brief.md`, renders parametric HTML templates to `graphics/`, and (if Chrome is installed) screenshots them to PNG in `graphics/rendered/`.

The framework ships parametric templates for common patterns:
- Three-tier architecture
- Capability matrix
- Lifecycle loop
- Swim-lane timeline
- Past performance coverage matrix

See [reference/graphic-templates/](../../reference/graphic-templates/) for the catalog.

## Step 9 — Draft

```
/proposal-writer
```

Drafts every required section into `drafts/`. Each section follows the standard pattern:
1. Theme statement (1 sentence — what / why / proof hook)
2. Point — the main claim
3. How the solution works
4. Discriminator proof point (with evidence citation)
5. Tie to requirement / mission outcome
6. Why the team is credible
7. Evaluator takeaway

The writer also updates `working/compliance-matrix.md` with section/page coverage as it drafts.

## Step 10 — Review

```
/red-team-review
```

Runs the Shipley color-team chain:
- **Pink** — compliance review (every requirement covered?)
- **Red** — narrative review (writes to score?)
- **Gold** — mock evaluation (rubric-driven, with pWin estimate)
- **White Glove** — final QA (typos, formatting, page-limit check)

Or run a specific mode:
```
/red-team-review --mode=pink
/red-team-review --mode=gold
/red-team-review --mode=white-glove
```

Findings land in `reviews/`. Address the high-priority items, then re-run the writer to fix.

## Step 11 — Export

```
/export-proposal
```

Converts markdown drafts to native Office formats. Output:
```
final/
├── docx/
├── xlsx/
├── pptx/
├── pdf/             # produced by you via Word's Save As PDF
└── graphics-png/
```

Open the .docx files in Word, do a final visual pass, save as PDF, submit.

## Quick reference: full chain

```
/new-proposal
/proposal-manager
/customer-intel             # if applicable
/competitor-assessment      # if applicable
/capture-scorecard          # if applicable
/proposal-solution-architect
/past-performance
/pricing-analyst
/proposal-graphics
/proposal-writer
/red-team-review
/export-proposal
```

`/status` at any time shows pipeline state, compliance coverage, and the next recommended command.
