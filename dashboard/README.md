# Federal Proposal Copilot — Dashboard

Local read-only Streamlit dashboard. Reads JSON sidecars produced by Phase A (`working/compliance-matrix.json`, `working/proposal-plan.json`, `working/ai-runs.jsonl`) and Phase C (`my-company/evidence-ledger.json`), plus `working/activity.md`, to show portfolio-wide proposal state at a glance.

**This is part of v1.5 Phase B. See [../docs/v1.5-plan.md](../docs/v1.5-plan.md).**

## Design principles

1. **Read-only.** Dashboard never writes to `proposals/`, `my-company/`, or anywhere else. All data comes from skills; the dashboard visualizes.
2. **Local-only.** No auth, no deployment, no web. Runs on `localhost`. `my-company/` and `proposals/` stay gitignored; the dashboard reads them from local disk.
3. **Graceful degradation.** If a proposal hasn't been migrated to v1.5 sidecars yet, it shows as "not migrated" rather than crashing. Same for missing evidence ledger.
4. **Streamlit, not a real app.** Phase B is deliberately lightweight. If this outgrows Streamlit, that's a signal to move toward v2, not to rebuild the dashboard.

## Install

One-time:

```bash
cd dashboard
pip install -r requirements.txt
```

Or with the Claude Code Python environment of your choice (conda, venv, uv).

## Launch

```bash
# From repo root
streamlit run dashboard/app.py
```

Or via the `/dashboard` skill inside Claude Code:

```
/dashboard
```

Opens at `http://localhost:8501` by default (Streamlit default) or `http://localhost:8765` if configured in `.streamlit/config.toml`.

## Views

| View | Reads | Shows |
|---|---|---|
| **Portfolio** | `proposals/*/working/proposal-type.md`, `proposal-plan.json`, `compliance-matrix.json`, `activity.md`, `ai-runs.jsonl` | All proposals in one table — type, due, stage, compliance %, evidence coverage, Gold Team pWin, spend |
| **Proposal** | Same files, per-proposal | Pipeline progress, compliance + evidence coverage, Gold Team findings, recent activity, spend breakdown |
| **Spend** | `proposals/*/working/ai-runs.jsonl` | Total spend, spend by proposal, spend by skill, trend, top runs |
| **Evidence Ledger** | `my-company/evidence-ledger.json` | Ledger browser — filter by type, approval status, tags; usage counts across proposals |

## Quick sanity check

Run the selftest to verify loaders work against your current data:

```bash
python dashboard/selftest.py
```

Reports how many proposals were found, how many have each sidecar, and whether the evidence ledger parses.

## Limitations

- Token/cost estimates rely on skills populating `ai-runs.jsonl`. In Phase A, token fields are often null (real counts come from Anthropic SDK integration in a later phase). Cost aggregates show `$0.00` for nulls and an "(estimates pending)" note.
- Proposals created before v1.5 Phase A lack JSON sidecars. Dashboard shows them with "not migrated" markers; the markdown files remain the authoritative source for pre-sidecar proposals.
- No write operations. To update status, edit the markdown and re-run the appropriate skill.

## What this is NOT

- Not a proposal editor (drafts are edited in the editor of your choice)
- Not a real-time collaboration tool (single-user, read-only)
- Not a replacement for `/status` (you can still run `/status` inside Claude Code — this is the wide-angle view)
