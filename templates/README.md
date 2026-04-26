# Proposal Templates

This directory contains the empty scaffold for a new proposal. The `/new-proposal` skill copies this structure and seeds it with boilerplate.

## Directory Structure
```
templates/
├── inputs/
│   ├── 00_priority/            ← Solicitation, eval criteria, distribution statement
│   ├── 01_customer/            ← Mission context, problem statement, constraints
│   ├── 02_yourCompany/         ← Our capabilities, past performance, components
│   ├── 03_teammates/           ← Partner capabilities (if teaming)
│   ├── 04_patterns/            ← Reference architectures, win themes from past efforts
│   ├── 05_graphic_standards/   ← Brand templates, visual standards (INPUTS only — rendered output goes to graphics/)
│   └── 06_notes/               ← Raw notes, meeting inputs, call summaries
├── working/                    ← Analysis artifacts (requirement matrix, solution strategy, activity log)
├── drafts/                     ← Proposal section drafts
├── graphics/                   ← Rendered HTML graphics (OUTPUTS)
└── reviews/                    ← Red team notes, compliance checks, gap logs
```

## Quick Start
1. Run `/new-proposal` — it will create a named copy of this structure and ask you to pick a proposal type
2. Drop your source materials into `inputs/`
3. Follow the `required_skills` list in `working/proposal-type.md` — type-specific workflow
4. Run `/status` any time to see pipeline progress and next action
