# 01 — Install Prerequisites

Detailed installation guide. If you've already worked through [QUICKSTART.md](../../QUICKSTART.md) and everything passed, skip this.

## Required

### Claude Code

The framework runs as a set of Claude Code "skills" — slash commands that invoke the AI with a structured prompt and toolset.

- Download: [claude.ai/claude-code](https://claude.ai/claude-code)
- Sign in with your Claude account (paid subscription required)
- Verify: `claude --version`

Three install variants exist (CLI, desktop app, IDE extension). The framework works with all three. CLI is most flexible for proposal workflows.

### Git

For cloning the repo and tracking your own changes.

- Windows: [git-scm.com/download/win](https://git-scm.com/download/win) — installs Git Bash, which the smoke test uses
- macOS: `brew install git` or [git-scm.com/download/mac](https://git-scm.com/download/mac)
- Linux: `apt install git` / `dnf install git` / etc.

Verify: `git --version`

### Python 3.10+

Used by helper scripts (graphic rendering, smoke test parsing, dashboard).

- Download: [python.org/downloads](https://www.python.org/downloads/)
- **Windows users:** check "Add Python to PATH" during install
- Verify: `python --version`

After installing Python, install the helper packages used by scripts and dashboard:
```bash
pip install streamlit pyyaml jsonschema
```

## Optional

### Google Chrome (for graphic rendering)

The `proposal-graphics` skill renders HTML figures to PNG via headless Chrome.

- Download: [chrome.google.com](https://www.google.com/chrome)
- Verify: `chrome --version` *(Windows: chrome may not be on PATH; that's fine — the skill calls it via full path)*

If you don't install Chrome, you can still produce HTML graphics; PNG conversion just needs to happen externally before Word embedding.

### Anthropic Office skills (for export)

The `/export-proposal` skill delegates Office format conversion to:
- `anthropic-skills:docx` (Word)
- `anthropic-skills:xlsx` (Excel)
- `anthropic-skills:pptx` (PowerPoint)

Install via Claude Code's skill marketplace inside Claude Code:
```
/skill install anthropic-skills:docx
/skill install anthropic-skills:xlsx
/skill install anthropic-skills:pptx
```

### GitHub CLI (`gh`) — for forking / contributing

If you plan to push changes to a fork or contribute back, install [gh](https://cli.github.com/) and authenticate:
```bash
gh auth login
```

### Microsoft Office (for reviewing output)

The framework produces .docx, .xlsx, .pptx — you'll want Office (or LibreOffice) to review and convert to PDF for submission.

## Verifying everything

```bash
git clone https://github.com/chakmarebel/federal-proposal-copilot.git
cd federal-proposal-copilot
bash scripts/smoke-test.sh
```

Expected: all checks pass (the count varies as the framework grows — anything in the 250+ range with no failures is good). If anything fails, see [05-troubleshooting.md](05-troubleshooting.md).
