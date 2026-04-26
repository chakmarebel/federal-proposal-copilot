"""
Dashboard selftest — verify loaders work against current workspace data.

Run from repo root:
    python dashboard/selftest.py

Does NOT require Streamlit — it's a pure loader check. Intended to be run as a
pre-launch sanity check or as part of the smoke-test pipeline.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dashboard.config import EVIDENCE_LEDGER_JSON, PROPOSALS_DIR  # noqa: E402
from dashboard.loaders import (  # noqa: E402
    list_proposals,
    load_all_ai_runs,
    load_all_proposals,
    load_evidence_citation_counts,
    load_evidence_ledger,
)


def ok(msg: str) -> None:
    print(f"  [OK]  {msg}")


def info(msg: str) -> None:
    print(f"  [..]  {msg}")


def warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def section(title: str) -> None:
    print()
    print(f"-- {title} --")


def main() -> int:
    print("Dashboard selftest — reading workspace data without Streamlit")
    print(f"Repo root: {REPO_ROOT}")

    # ── Proposals dir
    section("proposals/")
    if not PROPOSALS_DIR.exists():
        warn(f"{PROPOSALS_DIR} does not exist. Dashboard will show empty portfolio.")
    else:
        paths = list_proposals()
        info(f"found {len(paths)} proposal(s)")
        for p in paths:
            info(f"  - {p.name}")

    # ── Per-proposal loader sanity
    section("per-proposal summaries")
    summaries = load_all_proposals()
    if not summaries:
        warn("no summaries loaded")
    else:
        for s in summaries:
            flags = []
            if s.has_proposal_type:    flags.append("type")
            if s.has_proposal_plan_json: flags.append("plan.json")
            if s.has_compliance_json:  flags.append("compliance.json")
            if s.has_ai_runs:          flags.append(f"ai-runs({s.ai_run_count})")
            if s.gold_team_exists:     flags.append("gold")
            migration = "v1.5" if s.v15_migrated else ("partial" if s.has_proposal_type else "pre-v1.5")
            ok(f"{s.slug:<30} [{migration:>9}]  type={s.type_id:<20}  flags=[{', '.join(flags) or '-'}]")

    # ── Spend aggregation
    section("AI runs aggregation")
    df = load_all_ai_runs()
    info(f"rows: {len(df)}")
    if not df.empty:
        info(f"total cost (est.): ${df['cost_usd'].sum():.2f}")
        info(f"columns: {list(df.columns)}")

    # ── Evidence ledger
    section("evidence ledger")
    if not EVIDENCE_LEDGER_JSON.exists():
        warn(f"{EVIDENCE_LEDGER_JSON} does not exist — Phase C ledger view will show empty state")
    else:
        ledger = load_evidence_ledger()
        if ledger is None:
            warn(f"{EVIDENCE_LEDGER_JSON} exists but failed to parse")
            return 1
        items = ledger.get("items", [])
        ok(f"ledger parses — {len(items)} item(s), schema_version={ledger.get('schema_version')}")
        cites = load_evidence_citation_counts()
        info(f"citations found across drafts: {sum(cites.values())} (spanning {len(cites)} unique IDs)")

    print()
    print("Selftest complete. If no [WARN] or fatal messages above, dashboard should launch cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
