---
name: dashboard
description: Launch the local read-only Streamlit dashboard that shows portfolio-wide proposal state (compliance coverage, evidence coverage, Gold Team pWin, AI spend) by reading the v1.5 JSON sidecars produced by proposal-manager, compliance-check, and evidence-check. Use when the user wants a wide-angle view of all proposals at once, wants to spot-check token spend, or wants to browse the evidence ledger. The dashboard is read-only — it never modifies proposal files.
phase: inspection
composes: [proposal-manager, compliance-check, evidence-check]
conflicts_with: [status]  # portfolio-wide Streamlit; use status for per-proposal CLI summary
---

# /dashboard

## Purpose

Phase B of v1.5. Provides a local web dashboard at `http://localhost:8501` that visualizes everything the framework already produces on disk. Not a replacement for `/status` — this is the portfolio-wide view, `/status` is the current-proposal view.

## How it launches

Simple subprocess launch. The dashboard is a Streamlit app at `dashboard/app.py`.

```bash
# From repo root
streamlit run dashboard/app.py
```

Opens the default browser automatically. Server stops when you Ctrl+C the terminal.

## Skill behavior

1. **Check prerequisites.** Verify Streamlit is importable:
   ```bash
   python -c "import streamlit" 2>/dev/null
   ```
   If the import fails, instruct the user to install:
   ```bash
   pip install -r dashboard/requirements.txt
   ```
   Then exit.

2. **Run the selftest first** to catch loader issues before launching:
   ```bash
   python dashboard/selftest.py
   ```
   If any warnings appear (e.g., missing evidence ledger, pre-v1.5 proposals), surface them to the user but don't block launch.

3. **Launch the app** in a subprocess the user can see:
   ```bash
   streamlit run dashboard/app.py
   ```
   Report the URL (`http://localhost:8501` by default per `dashboard/.streamlit/config.toml`) so the user can open it manually if the browser doesn't auto-launch.

4. **Do not wait for the app to exit.** Streamlit is a long-running server. Return control to the user immediately after launching.

## Views the dashboard provides

- **Portfolio** — every proposal in one table with migration status, pipeline progress, compliance coverage, evidence coverage, Gold Team pWin, and spend
- **Proposal** — per-proposal detail: pipeline, compliance counters, evidence coverage, Gold Team scorecard, recent activity, spend breakdown
- **Spend** — AI cost aggregated across all proposals, grouped by proposal / skill / model, with top-10 most-expensive runs and daily trend
- **Evidence Ledger** — browse `my-company/evidence-ledger.json`, filter by type/status/tags, see citation counts across drafts, surface unused approved evidence

## Things to tell the user after launch

- Dashboard reads but never writes. Editing is still done in markdown or via other skills.
- If a proposal shows "pre-v1.5" in the migration column, it just means the JSON sidecars from Phase A aren't present yet — the proposal still works, it just shows less structured detail in the dashboard.
- Token counts are often null in Phase A. Spend shows `$0` when counts are null. Real counts come from future SDK integration.

## Activity trail

Do NOT append to `working/activity.md` — this skill is read-only (like `/status`). If logging the launch is useful for token-spend tracking (it isn't — no AI calls made), that would also be skipped.

## When not to use

- During a drafting session inside Claude Code — use `/status` instead for a quick current-proposal view
- When the user just wants to see one proposal's state
- Before v1.5 Phase A has been run (proposals without JSON sidecars show mostly empty — not useful)
