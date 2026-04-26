# 05 — Troubleshooting

Common issues and fixes. If you hit something not covered here, file an issue at [github.com/chakmarebel/federal-proposal-copilot/issues](https://github.com/chakmarebel/federal-proposal-copilot/issues).

## Smoke test fails

```bash
bash scripts/smoke-test.sh
```

### "command not found: bash"

You're on Windows without Git Bash. Install [Git for Windows](https://git-scm.com/download/win), then run from Git Bash, not PowerShell.

### Missing files reported

The smoke test lists exactly which files are missing. Most common cause: an incomplete `git clone` (network interrupted). Try:
```bash
git status        # any untracked files?
git pull          # any commits missing?
```

If clean and still failing, re-clone:
```bash
cd ..
rm -rf federal-proposal-copilot
git clone https://github.com/chakmarebel/federal-proposal-copilot.git
cd federal-proposal-copilot
bash scripts/smoke-test.sh
```

## Skill says "Skipped for type \<type_id\>"

This is **intended behavior**. The proposal-type registry filters which skills apply. If you have a `white-paper` type proposal and run `/competitor-assessment`, you'll see `Skipped for type white-paper` because white papers don't typically require competitive analysis.

To override:
1. Edit `working/proposal-type.md` and remove the skill from `skipped_skills`
2. Re-run the skill

To see which skills apply to your proposal type, read `working/proposal-type.md`.

## Skill says "working/proposal-type.md is missing"

You haven't scaffolded the proposal yet. Run:
```
/new-proposal
```

If you scaffolded but the file is missing, manually copy from `reference/proposal-types/<type-id>.md` to `proposals/<your-name>/working/proposal-type.md`.

## Streamlit dashboard won't start

### `streamlit: command not found`

Install Streamlit and use the python module form on Windows:
```bash
pip install streamlit
python -m streamlit run dashboard/app.py
```

### Port 8501 already in use

```bash
python -m streamlit run dashboard/app.py --server.port 8502
```

## Graphic rendering fails

### `chrome: command not found`

The `proposal-graphics` skill calls `chrome --headless`. If Chrome isn't on PATH:

**Option 1:** Install Chrome and verify it's on PATH (`chrome --version`).

**Option 2:** Skip PNG conversion in the skill output, manually screenshot the HTML files in `graphics/`.

**Option 3:** Edit `scripts/render-graphic.py` to use a different rendering approach (Puppeteer, wkhtmltopdf, etc.).

### `Unresolved placeholder {{...}} in template`

The template references a data field your JSON didn't supply. The error shows which field. Either add the field to your data file, or pass `--no-strict` to skip the check:
```bash
python scripts/render-graphic.py <template> <data> <output>
```
(without `--strict`)

## Path issues on Windows

When passing paths to Python scripts:
- **Use Windows-style paths** in PowerShell: `C:\Users\you\...`
- **Use POSIX-style paths** in Git Bash: `/c/Users/you/...`
- **In `cygpath`-friendly contexts:** `cygpath -w "/c/Users/you/..."` converts POSIX to Windows

If you see `pypdf` or `pathlib` errors complaining about paths, you've likely mixed styles. Stick to one shell per session.

## Skill output looks generic / not tailored

Most likely: `my-company/` is sparse. The AI can only be as specific as your company profile lets it be.

Open these files and add detail:
- `my-company/capabilities.md` — replace generic phrases with technical specifics (numbers, technologies, customer-named outcomes)
- `my-company/past-performance.md` — add quantified outcomes per contract
- `my-company/evidence-ledger.json` — add citable claims

See [02-company-profile.md](02-company-profile.md) for the deep guide.

## Compliance matrix has too many rows / wrong rows

The matrix is auto-generated from solicitation parsing. If `proposal-manager` over-produced or under-produced rows, you can:
- Edit `working/compliance-matrix.md` directly — it's just markdown
- Re-run `/proposal-manager` with feedback like: "the compliance matrix should only include Section L Section M and the SOW. Drop everything else."

The skill is designed to be re-runnable. Each run respects existing `Drafted` / `Covered` status; it won't regress your progress.

## Drafts cite "[Customer]" or "[Your Company]" placeholders

The writer fell back to placeholders because:
1. `my-company/company.md` is missing identity fields, OR
2. The solicitation didn't name the customer in a way `proposal-manager` could extract

Fix:
1. Verify `my-company/company.md` is populated
2. Edit `working/customer-profile.md` to set the customer name explicitly
3. Re-run `/proposal-writer`

## Need more help

Open an issue at [github.com/chakmarebel/federal-proposal-copilot/issues](https://github.com/chakmarebel/federal-proposal-copilot/issues) with:
- What you tried (exact command)
- What happened (full error message)
- Your OS and Python version
- Output of `bash scripts/smoke-test.sh`
