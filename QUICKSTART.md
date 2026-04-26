# Quickstart

A 30-minute walkthrough for first-time users. By the end you'll have:
- The framework cloned and verified
- Your company profile populated
- A test proposal scaffolded and analyzed end-to-end

If anything breaks, jump to [docs/getting-started/05-troubleshooting.md](docs/getting-started/05-troubleshooting.md).

---

## 1. Install prerequisites (5 min)

| Tool | Why | How |
|---|---|---|
| **[Claude Code](https://claude.ai/claude-code)** | Runs the AI skills | Download installer; sign in with your Claude account |
| **Git** | Clone the repo | [git-scm.com](https://git-scm.com) (Windows: includes Git Bash) |
| **Python 3.10+** | Smoke test, dashboard, helper scripts | [python.org](https://python.org) — make sure "Add to PATH" is checked |
| **Google Chrome** *(optional)* | Renders proposal graphics from HTML to PNG | [chrome.google.com](https://www.google.com/chrome) |

**Verify:**
```bash
claude --version
git --version
python --version
```

If all three respond, you're ready.

---

## 2. Clone the repo (1 min)

```bash
git clone https://github.com/chakmarebel/federal-proposal-copilot.git
cd federal-proposal-copilot
```

Run the smoke test to confirm every required file is present:
```bash
bash scripts/smoke-test.sh
```

You should see `268/268 checks passed` (or similar). If you see failures, see [troubleshooting](docs/getting-started/05-troubleshooting.md).

---

## 3. Set up your company profile (10 min)

Open the repo in Claude Code:
```bash
claude
```

Then run the setup skill:
```
/setup-company
```

The skill will walk you through:
- **Company identity** — name, location, CAGE, UEI, NAICS codes
- **Capabilities** — what you do, in 3–7 bullets
- **Past performance** — 3–5 contracts the framework can cite as proof points
- **Contract vehicles** — GSA MAS, IDIQs, BPAs, OTAs you can sell through
- **Brand** *(optional)* — logo, colors, tagline for graphics

This populates `my-company/` — a directory the framework reads on every proposal. **You only do this once.** Updates happen incrementally as your company evolves.

> **Important:** `my-company/` is gitignored. Your company data never leaves your machine.

For deeper guidance on populating `my-company/`, see [docs/getting-started/02-company-profile.md](docs/getting-started/02-company-profile.md).

---

## 4. Walk through your first proposal (15 min)

**Pick a real or test solicitation.** A small SBIR topic or RFI works well for the first run — they're short and cover the full skill chain.

### 4a. Create the workspace
```
/new-proposal
```

The skill asks for short name, full title, customer, due date, and proposal type. It scaffolds:
```
proposals/<your-name>/
├── inputs/                 # drop your solicitation here
├── working/                # AI analysis lands here
├── drafts/                 # proposal sections
├── graphics/               # rendered figures
├── reviews/                # red-team output
└── final/                  # native-Office submission package
```

### 4b. Drop the solicitation
Save the solicitation PDF / DOCX / Markdown into:
```
proposals/<your-name>/inputs/00_priority/
```

### 4c. Run the analysis chain
```
/proposal-manager
```
This is the workhorse. It reads the solicitation, extracts evaluation criteria, builds the compliance matrix, drafts win themes, and gives a bid/no-bid recommendation. Output lands in `working/`.

```
/proposal-solution-architect
```
Designs the technical solution against the compliance matrix. Outputs requirement → capability mapping, architecture concept, assumptions and risks.

```
/proposal-graphics
```
Drafts a graphics brief and renders proposal-ready HTML figures (architecture diagrams, capability matrices, timelines).

```
/proposal-writer
```
Drafts every required section, written to score against the rubric. Updates the compliance matrix with section/page coverage.

```
/red-team-review
```
Runs the review chain: Pink (compliance) → Red (narrative) → Gold (mock evaluation) → White Glove (final QA). Findings land in `reviews/`.

```
/export-proposal
```
Converts markdown drafts into native Office formats (.docx, .xlsx, .pptx) plus PNG graphics for Word embed. Output in `final/`.

### 4d. Check progress at any time
```
/status
```
Read-only summary of pipeline state, compliance coverage, and the next recommended command.

---

## 5. Optional: launch the dashboard

If you want a portfolio view across multiple proposals:
```bash
python -m streamlit run dashboard/app.py
```

Open `http://localhost:8501` in your browser.

---

## What's next

- **Detailed setup**: [docs/getting-started/01-install.md](docs/getting-started/01-install.md)
- **Populating `my-company/` well**: [docs/getting-started/02-company-profile.md](docs/getting-started/02-company-profile.md)
- **Skill catalog and when to use each**: [docs/getting-started/04-skills-reference.md](docs/getting-started/04-skills-reference.md)
- **Proposal-type registry** (FAR RFP, SBIR, GSA MAS, OTA, BAA, CSO, RFI, white paper, ROM): [reference/proposal-types/](reference/proposal-types/)
- **Methodology library** (Shipley alignment, color teams, capture planning, BD process): [reference/methodology/](reference/methodology/)

---

## Getting help

- **Smoke test fails** → [docs/getting-started/05-troubleshooting.md](docs/getting-started/05-troubleshooting.md)
- **A skill says "Skipped for type ..."** → that's expected; the proposal type registry filters which skills apply per proposal vehicle. See `working/proposal-type.md` in your active proposal.
- **Issues / bugs** → file at [github.com/chakmarebel/federal-proposal-copilot/issues](https://github.com/chakmarebel/federal-proposal-copilot/issues)
