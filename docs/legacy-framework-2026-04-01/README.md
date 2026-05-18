# Federal Proposal Assistant

An AI-powered workflow for writing winning federal defense and IC proposals using [Claude Code](https://claude.ai/claude-code).

Drop your solicitation, describe your company, and let AI handle requirements analysis, solution architecture, graphics, drafting, and red-team review.

> **New here?** Start with the [Overview](OVERVIEW.md) — a plain-language introduction to what this tool does and who it's for.

## Quick Start

### Prerequisites
- [Claude Code](https://claude.ai/claude-code) installed
- A Claude account with an active subscription

### Setup (10 minutes)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR-ORG/federal-proposal-assistant.git
cd federal-proposal-assistant

# 2. Open in Claude Code
claude

# 3. Run company setup (one-time)
/setup-company
```

The setup skill will ask for your company name, capabilities, past performance, contract vehicles, and optionally your brand colors. It generates reusable boilerplate files in `my-company/` that every future proposal will reference.

### Start a Proposal

```bash
# 4. Create a new proposal workspace
/new-proposal
```

You'll be asked for the proposal name, customer, and type. Then:

```bash
# 5. Drop your solicitation into the inputs folder
#    (PDF, DOCX, or markdown — Claude will read it)

# 6. Run the workflow in sequence:
/customer-intel                 # Research customer — open source intel + relationship template
/proposal-manager               # Analyze solicitation, compliance framework, win themes, bid/no-bid
/competitor-assessment          # Research competitors, Bidder Comparison Chart, teaming gaps (competitive bids)
/proposal-solution-architect    # Design solution against approved plan + competitor assessment
/past-performance               # Map PP repository to eval criteria, draft PPQ narratives
/pricing-analyst                # Build cost model and cost volume narrative
/proposal-graphics              # Create visual concepts + HTML graphics
/proposal-writer                # Draft all sections
/red-team-review                # Score like a government evaluator
```

## How It Works

### The Workflow

```
Customer Intel → Proposal Plan → Competitor Assessment → Solution Architecture → PP + Pricing → Graphics → Draft → Red Team → Submission
      ↑                ↑                   ↑                       ↑                  ↑              ↑         ↑         ↑
  AI searches      AI builds           AI researches           AI designs          AI maps PP    AI renders  AI writes  AI scores
  open source +    compliance          competitors via         from your           to criteria    HTML files  sections   & rewrites
  you fill in      framework &         open source +           capabilities        + builds
  relationship     win themes          teaming gaps            + competitor        cost volume
  knowledge                                                    assessment
```

### Skills

| Skill | What It Does |
|-------|-------------|
| `/setup-company` | One-time setup — creates your company profile and boilerplate |
| `/new-proposal` | Scaffolds a new proposal workspace with your boilerplate pre-loaded |
| `/customer-intel` | Researches the customer via open source (budget docs, awards history, key personnel, hot buttons) and produces a profile template for you to complete with relationship knowledge |
| `/proposal-manager` | Analyzes the solicitation — builds compliance framework, evaluates criteria, defines win themes, recommends bid/no-bid |
| `/competitor-assessment` | Researches likely competitors via open source, builds weighted Bidder Comparison Chart, identifies teaming gaps, generates strategy statements |
| `/proposal-solution-architect` | Designs the solution against the approved plan and competitor assessment — requirements matrix, capability mapping, architecture concept |
| `/past-performance` | Maps your PP repository to evaluation criteria, selects best references, drafts PPQ narratives and past performance volume |
| `/pricing-analyst` | Builds cost model, BOE narratives, and cost volume draft from the approved architecture |
| `/proposal-writer` | Drafts all proposal sections from the approved architecture |
| `/proposal-graphics` | Creates proposal-ready HTML graphics (architecture diagrams, timelines, matrices) |
| `/red-team-review` | Reviews the draft like a government evaluator — flags gaps, provides specific rewrites |

### Directory Structure

```
federal-proposal-assistant/
├── CLAUDE.md                        ← AI operating instructions
├── .claude/skills/                  ← The 6 skills listed above
├── reference/                       ← Reusable standards
│   ├── style-guide.md               ← Federal proposal writing conventions
│   ├── distribution-statements.md   ← Classification & distribution markings
│   └── section-patterns.md          ← Reusable section templates with placeholders
├── templates/                       ← Empty proposal scaffold (copied by /new-proposal)
├── my-company/                      ← YOUR company profile (generated by /setup-company)
│   ├── company-description.md
│   ├── capabilities.md
│   ├── contract-vehicles.md
│   ├── past-performance.md
│   └── brand-palette.md             ← Optional brand colors for graphics
└── proposals/                       ← Your proposals live here
    └── [proposal-name]/
        ├── inputs/                  ← Source materials
        │   ├── 00_priority/         ← Solicitation, eval criteria
        │   ├── 01_customer/         ← Mission context, constraints
        │   ├── 02_company/          ← Your capabilities (auto-seeded)
        │   ├── 03_teammates/        ← Partner capabilities
        │   ├── 04_patterns/         ← Reference architectures
        │   ├── 05_graphics/         ← HTML graphics (rendered here)
        │   └── 06_notes/            ← Meeting notes, raw inputs
        ├── working/                 ← Analysis artifacts
        ├── drafts/                  ← Proposal sections
        └── reviews/                 ← Red team findings
```

## What You Provide

| Step | What You Drop In | Where |
|------|-----------------|-------|
| 1 | Solicitation / RFP / white paper instructions | `inputs/00_priority/` |
| 2 | Customer context (mission, problem, constraints) | `inputs/01_customer/` |
| 3 | Your capabilities are auto-seeded from `my-company/` | `inputs/02_company/` |
| 4 | Teammate capabilities (if teaming) | `inputs/03_teammates/` |
| 5 | Reference architectures or past winning approaches | `inputs/04_patterns/` |
| 6 | Meeting notes, call summaries, raw inputs | `inputs/06_notes/` |

## What AI Produces

| Output | Location | Format |
|--------|----------|--------|
| Requirement matrix | `working/requirement-matrix.md` | Markdown table |
| Capability mapping | `working/capability-matrix.md` | Markdown table |
| Solution strategy | `working/solution-strategy.md` | Structured markdown |
| Architecture concept | `working/architecture-concept.md` | Structured markdown |
| Graphics specs | `working/graphics-brief.md` | ASCII wireframes + layout instructions |
| Rendered graphics | `inputs/05_graphics/*.html` | Browser-viewable HTML (screenshot for Word) |
| Draft sections | `drafts/*.md` | Proposal-ready markdown |
| Red team findings | `reviews/*.md` | Issue table + recommended rewrites |

## Graphics — Why This Changes Everything

For most proposal teams, graphics are the bottleneck. They require a dedicated graphic designer, multiple briefing cycles, and days of back-and-forth. Often the designer doesn't fully understand the technical content, and the result is either beautiful but inaccurate, or accurate but ugly.

**This tool eliminates that bottleneck.** The same AI that understands your solution architecture produces the visuals — and because it generates code (HTML/SVG), not pixel art, every element is precise, editable, and revision-ready.

### How It Works

Claude doesn't generate images like DALL-E or Midjourney. It writes **HTML and SVG code** that your browser renders as pixel-perfect graphics. This is a fundamental difference:

| | Image Generation AI (DALL-E, Midjourney) | This Tool (HTML/SVG) |
|--|---|---|
| **Output** | Raster image — pixels you can't edit | Structured code — every element is addressable |
| **Accuracy** | Approximate — may hallucinate labels, misspell text | Exact — text, labels, and structure are code, not guesses |
| **Revisions** | Regenerate from scratch and hope | Conversational: "make the font bigger" → CSS change in seconds |
| **Technical content** | Doesn't understand what it's drawing | Reads your architecture docs and draws from understanding |
| **Brand compliance** | No control over colors/fonts | Exact hex codes from your brand palette |
| **Print quality** | Resolution-dependent | Scales perfectly — SVG is resolution-independent |

### Why the Results Are So Good

1. **Context awareness.** Claude reads your solution strategy, architecture, and draft sections *before* generating graphics. Every box says the right thing, every flow goes the right direction, and every commitment matches the text — from the first version.

2. **HTML/SVG is the perfect medium.** Proposal graphics are structured information — boxes, arrows, labels, tables, timelines. They're not photographs. HTML/SVG is literally designed to render structured information, and Claude is exceptionally good at writing it.

3. **Instant iteration.** "Make the font bigger" is a CSS change. "Move the labels above the arrows" is an SVG coordinate adjustment. "Switch to our brand colors" is a hex value replacement. Each revision takes seconds, not a designer's calendar day.

4. **Encoded design knowledge.** The graphics skill contains hard-won lessons: minimum font sizes for half-page print (titles 28px, body 17px+), anti-patterns to avoid (emoji icons, text overlapping arrows, classification badges cluttering boxes), and proven layout patterns. Every graphic starts from a professional foundation.

5. **One person, full capability.** A proposal manager who can't draw a straight line in PowerPoint can now produce architecture diagrams, execution timelines, and capability matrices by describing what they need in plain English.

### What This Replaces

| Traditional Process | This Tool |
|---|---|
| Writer briefs graphic designer (30 min) | Claude reads the architecture directly |
| Designer produces first draft (4-8 hours) | First version generated in under a minute |
| 2-3 revision cycles (1-2 days) | Revisions are conversational, instant |
| Designer may not understand the tech | AI built the architecture *and* the graphic |
| Final graphic is a static image | Final graphic is editable code |
| Brand compliance requires manual checking | Brand palette applied automatically |
| **Total: 1-3 days per graphic** | **Total: 5-15 minutes per graphic** |

### Built-In Graphic Patterns

The skill includes proven patterns for common proposal visuals:

- **Three-tier architecture** — Horizontal bands (Enterprise → GCC → Edge) with registry pills, boundary lines, and flow arrows
- **Lifecycle loop** — Four nodes in a diamond with circular arc arrows and a center concept label
- **Capability matrix** — Products vs. Services two-column layout with accent-colored headers
- **Execution timeline** — Swim lane with parallel workstreams, phase columns, gate markers, and commitment callouts
- **Objectives** — Technical vs. Operational side-by-side with numbered items
- **Operational capabilities** — Row-based feature list with accent bars

### Brand Colors

If you provide brand colors in `my-company/brand-palette.md`, all graphics use your palette automatically. Specify your primary accent, background, text colors, and tier treatments — and every graphic is on-brand from the first render.

If no brand palette is provided, a professional default palette (dark background, clean typography, gold/blue accents) is applied.

## Tips

- **Run skills in order.** The architect skill feeds the writer, which feeds the reviewer. Skipping steps produces weaker output.
- **Iterate on graphics in HTML.** The HTML files are the primary deliverable — edit them directly for refinements rather than regenerating from specs.
- **Red team early.** Run `/red-team-review` on a partial draft to catch structural issues before writing all sections.
- **Captions go in the document, not the graphic.** Keep figure numbers and captions in your Word doc text, not embedded in the HTML graphic.
- **Check the section patterns.** `reference/section-patterns.md` has fill-in-the-blank templates for every standard proposal section.

## Supported Proposal Types

- White papers (unsolicited and directed)
- RFP/RFQ responses
- RFI responses
- BAA submissions
- SBIR/STTR proposals
- OTA white papers and full proposals
- CSO responses

## Security & Data Handling

### Why This Is Better Than Uploading to ChatGPT

When you paste a proposal into ChatGPT or upload documents to a web-based AI, you have **no control over where that data goes.** It's uploaded to a third-party server, potentially used for model training, and you've lost custody of your content. For federal proposals containing proprietary capabilities, pricing strategies, teaming arrangements, and customer-specific intelligence, that's a serious problem.

This tool is different:

| | ChatGPT / Web AI | Federal Proposal Assistant |
|--|---|---|
| **Where files live** | Uploaded to cloud servers you don't control | On your local machine, in folders you own |
| **What you upload** | Entire documents, pasted wholesale | Only the content Claude needs to process for a specific task |
| **Training data** | Your content may train future models | Claude Code conversations are [not used for training](https://www.anthropic.com/policies) |
| **File structure** | Scattered across chat sessions | Organized, version-controlled, reusable across proposals |
| **Institutional memory** | Lost when the chat session ends | Persisted in skills, reference files, and company boilerplate |
| **Audit trail** | None | Git-trackable: every file change is visible |

### What Stays on Your Machine
- All files in `my-company/` — your capabilities, past performance, contract vehicles, pricing
- All files in `proposals/` — solicitations, drafts, analysis, graphics, reviews
- The skills and reference files — they're just local markdown files
- HTML graphics — rendered locally in your browser

### What Is Transmitted to Anthropic's API
When you run a skill, Claude reads files from your local directories and processes them. The **content of those files** passes through Anthropic's API during that processing. This is true of any AI tool that analyzes your documents — the key differences are:

1. **You control which files Claude reads.** It only processes what's in the proposal's `inputs/` and `working/` directories. Sensitive material you don't put there is never touched.
2. **No persistent storage.** Anthropic does not retain your conversation data for model training under their commercial terms.
3. **Selective processing.** Unlike pasting an entire 200-page RFP into ChatGPT, the skills read specific sections for specific tasks.

### Handling Sensitive / CUI / Classified Material

For proposals involving Controlled Unclassified Information (CUI) or sensitive content:

- **Isolate sensitive material.** Keep classified or highly sensitive source documents outside the proposal directory. Manually summarize key points into `inputs/06_notes/` in sanitized form. Claude works from your summaries.
- **Self-hosted API.** Organizations running Claude through AWS Bedrock or GCP Vertex AI keep all API traffic within their own cloud boundary. The skills work identically — just configure Claude Code to point at your endpoint.
- **Air-gapped environments.** When local model support becomes available in Claude Code, the entire workflow runs on-device with zero data transmission.

**Bottom line:** Your proposal files live on your machine, in your Git repo, under your control. AI processes only what you explicitly ask it to, under commercial terms that prohibit training on your data. That's fundamentally different from pasting your company's crown jewels into a chat window.

## Requirements

- Claude Code (CLI) with an active Claude subscription
- A text editor for reviewing outputs
- A browser for viewing HTML graphics
- Microsoft Word or Google Docs for final document assembly

## Contributing

This workflow was developed through real-world federal proposal writing. If you improve a skill or add a new pattern, please contribute it back.

## License

MIT
