# Federal Proposal Assistant
### An AI-powered workflow for small defense contractors writing government proposals

---

## The Problem

Federal proposals are won or lost long before the writing starts. The work that actually determines the outcome — understanding the customer, assessing the competition, designing a credible solution, pricing to win — is the hard part. And for a small team, it's often skipped or rushed because there simply isn't enough time or enough people.

Then comes the writing itself. Graphics alone can take days. Compliance reviews get rushed. Red team feedback arrives too late to act on.

This tool changes that.

---

## What It Is

**Federal Proposal Assistant** is an AI workflow built on [Claude Code](https://claude.ai/claude-code) that automates the intellectual work of capture and proposal development — from first look at an opportunity through final submission review.

It's not a template library. It's not a document generator that produces generic text. It's a structured, step-by-step process where AI does the analytical and writing work while you provide the judgment, the relationship knowledge, and the company context.

Built on the Shipley methodology, adapted for small teams that can't run a full BD machine but still need to win competitive work.

---

## What It Does

The workflow covers 11 steps, each handled by a dedicated skill:

| Step | Skill | What It Produces |
|------|-------|-----------------|
| 1 | **Company Setup** | One-time company profile: capabilities, past performance, contract vehicles, brand |
| 2 | **New Proposal** | Workspace scaffold with your boilerplate pre-loaded, capture mode set |
| 3 | **Customer Intel** | Open-source research on the customer + a template for your relationship knowledge |
| 4 | **Proposal Manager** | Compliance framework, bid/no-bid assessment, prime vs. sub decision, win themes |
| 5 | **Competitor Assessment** | Competitive landscape, differentiators, teaming gap analysis, strategy statements |
| 6 | **Capture Scorecard** | 9-dimension readiness check — go/no-go before committing proposal resources |
| 7 | **Solution Architect** | Requirements matrix, capability mapping, solution design, architecture concept |
| 8 | **Past Performance** | Maps your record to evaluation criteria, drafts PPQ narratives |
| 9 | **Pricing Analyst** | Cost model, BOE narratives, cost volume — or lightweight SBIR/OTA/CSO pricing |
| 10 | **Proposal Graphics** | Proposal-ready HTML/SVG graphics — architecture diagrams, timelines, matrices |
| 11 | **Proposal Writer** | Full draft of every section, written to score |
| 12 | **Red Team Review** | Pink (compliance) → Red (narrative) → Gold (mock eval) → White Glove (final QA) |

---

## Who It's For

Small and mid-sized defense contractors who:
- Are writing 5–20 proposals per year without a dedicated BD staff
- Pursue a mix of SBIR, CSO, OTA, BAA, and competitive RFPs
- Lose proposals because of gaps in analysis or writing quality, not gaps in capability
- Spend too much time on graphics, compliance matrices, and boilerplate

The workflow supports two modes:

- **Full Capture** — for competitive RFPs, IDIQ task orders, and recompetes. Complete Shipley-style competitive analysis, formal pricing, PPQ-format past performance.
- **Responsive** — for SBIR, CSO, OTA, BAA, and white papers. Lighter-weight process calibrated to the vehicle, with SBIR budget templates, OTA milestone schedules, and relevant experience narratives instead of formal PPQs.

You set your company's default. You override it per proposal when needed.

---

## What Stays on Your Machine

All of your files — solicitations, drafts, graphics, analysis, past performance, pricing — stay in your local directories. Claude processes them when you run a skill, but nothing is stored in a cloud database, shared with other users, or used to train AI models.

This matters for proposals involving proprietary capabilities, teaming strategies, and customer-sensitive information. Your crown jewels stay on your machine.

---

## The Graphics Difference

For most proposal teams, graphics are the bottleneck — they require a designer who may not understand the technical content, multiple revision cycles, and days of calendar time.

This tool generates proposal-ready graphics as HTML/SVG code that renders in any browser and screenshots directly into Word. Because the AI understands the solution it designed, every box says the right thing and every flow goes the right direction — from the first version. Revisions are conversational: *"make the font larger"* or *"add a third tier"* takes seconds.

Architecture diagrams, execution timelines, capability matrices, objectives graphics — all produced in minutes, not days.

---

## Getting Started

1. Install [Claude Code](https://claude.ai/claude-code) (requires a Claude subscription)
2. Clone the repo: `github.com/[your-github-handle]/federal-proposal-assistant`
3. Run `/setup-company` to create your company profile (one time, ~10 minutes)
4. Drop in a solicitation, run `/new-proposal`, follow the workflow

The first time through takes an hour or two. Once your company profile exists and you've run it once, each subsequent proposal moves faster.

---

*Built from real-world federal proposal experience. Feedback and contributions welcome.*
