#!/usr/bin/env python3
"""Compute the discipline-lift metric from accumulated Gold Team snapshots.

Every Gold Team / mock-evaluation run appends one scored snapshot to
reviews/gold-team-history.jsonl (see reference/schemas/gold-team-snapshot.schema.json).
This script turns that series into the number the evaluator-upstream discipline is
supposed to produce: did the first-pass (baseline) score converge toward the final
score, and did the unsupported-claim density fall?

Reads:
  reviews/gold-team-history.jsonl   the append-only snapshot series
  drafts/*.md                       current word count + CLAIM-UNSUPPORTED markers
                                    (top level only; drafts/loose/ excluded)

Writes:
  reviews/lift.md                   the lift report (regenerated each run)

Usage:
  python scripts/compute-lift.py --proposal <slug>
  python scripts/compute-lift.py --selftest

Exit codes:
  0 = report produced (or selftest passed)
  1 = no snapshot history yet (nothing to compute)
  2 = usage or environment error
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).parent.parent

PWIN_ORDINAL = {"very low": 1, "low": 2, "moderate": 3, "high": 4}


def load_history(history_path: Path) -> list[dict]:
    if not history_path.exists():
        return []
    entries: list[dict] = []
    for line_no, line in enumerate(history_path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            print(f"WARNING: skipping malformed line {line_no} in {history_path.name}", file=sys.stderr)
            continue
        if isinstance(entry, dict):
            entries.append(entry)
    return entries


def draft_stats(drafts_dir: Path) -> tuple[int, int]:
    """(word_count, unsupported_claim_count) across top-level drafts/*.md."""
    words = 0
    unsupported = 0
    if drafts_dir.is_dir():
        for path in sorted(drafts_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            unsupported += len(re.findall(r"CLAIM-UNSUPPORTED", text))
            text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
            words += len(text.split())
    return words, unsupported


def _issues(entry: dict) -> int:
    counts = entry.get("counts") or {}
    return (
        int(counts.get("weaknesses") or 0)
        + int(counts.get("significant_weaknesses") or 0)
        + int(counts.get("deficiencies") or 0)
    )


def _strengths(entry: dict) -> int:
    counts = entry.get("counts") or {}
    return int(counts.get("strengths") or 0) + int(counts.get("significant_strengths") or 0)


def _pwin_ord(entry: dict) -> int | None:
    pwin = entry.get("pwin")
    return PWIN_ORDINAL.get(pwin.strip().lower()) if isinstance(pwin, str) else None


def compute_lift(history: list[dict], word_count: int, unsupported_count: int) -> dict:
    scored = [entry for entry in history if _pwin_ord(entry) is not None]
    baseline = scored[0] if scored else None
    current = scored[-1] if scored else None
    density = round(unsupported_count / (word_count / 1000), 2) if word_count else 0.0
    return {
        "review_count": len(history),
        "scored_count": len(scored),
        "baseline_pwin": baseline.get("pwin") if baseline else None,
        "current_pwin": current.get("pwin") if current else None,
        "pwin_delta": (_pwin_ord(current) - _pwin_ord(baseline)) if (baseline and current) else None,
        "baseline_strengths": _strengths(baseline) if baseline else 0,
        "current_strengths": _strengths(current) if current else 0,
        "baseline_issues": _issues(baseline) if baseline else 0,
        "current_issues": _issues(current) if current else 0,
        "word_count": word_count,
        "unsupported_claim_count": unsupported_count,
        "unsupported_claim_density": density,
        "series": [
            {
                "timestamp": entry.get("timestamp", ""),
                "mode": entry.get("mode", ""),
                "pwin": entry.get("pwin"),
                "strengths": _strengths(entry),
                "issues": _issues(entry),
                "unsupported": entry.get("unsupported_claim_count"),
            }
            for entry in history
        ],
    }


def render_report(proposal: str, lift: dict) -> str:
    def fmt(value) -> str:
        return "n/a" if value is None else str(value)

    delta = lift["pwin_delta"]
    if delta is None:
        trajectory = "Not enough scored runs to compute a trajectory (need at least one snapshot with a pWin)."
    elif lift["scored_count"] < 2:
        trajectory = "One scored run so far. This run is the baseline; lift appears after the next review."
    elif delta > 0:
        trajectory = f"pWin improved {fmt(lift['baseline_pwin'])} -> {fmt(lift['current_pwin'])} across {lift['scored_count']} scored runs."
    elif delta == 0:
        trajectory = f"pWin held at {fmt(lift['current_pwin'])} across {lift['scored_count']} scored runs."
    else:
        trajectory = f"pWin regressed {fmt(lift['baseline_pwin'])} -> {fmt(lift['current_pwin'])}. Review what changed between runs."

    series_rows = "\n".join(
        f"| {entry['timestamp'] or '?'} | {entry['mode'] or '?'} | {fmt(entry['pwin'])} | {entry['strengths']} | {entry['issues']} | {fmt(entry['unsupported'])} |"
        for entry in lift["series"]
    ) or "| _(no snapshots)_ | | | | | |"

    return f"""# Discipline Lift -- {proposal}

**Date:** {date.today().isoformat()}
**Source:** reviews/gold-team-history.jsonl ({lift['review_count']} snapshot(s), {lift['scored_count']} scored)

## Headline

{trajectory}

| Metric | Baseline (first scored run) | Current (latest scored run) |
|---|---|---|
| pWin | {fmt(lift['baseline_pwin'])} | {fmt(lift['current_pwin'])} |
| Strengths (S + SS) | {lift['baseline_strengths']} | {lift['current_strengths']} |
| Issues (W + SW + D) | {lift['baseline_issues']} | {lift['current_issues']} |

## Unsupported-Claim Density (current drafts)

- Draft word count (drafts/*.md, top level): **{lift['word_count']}**
- CLAIM-UNSUPPORTED markers: **{lift['unsupported_claim_count']}**
- Density: **{lift['unsupported_claim_density']} per 1,000 words**

## Run Series

| Timestamp | Mode | pWin | Strengths | Issues | Unsupported |
|---|---|---|---|---|---|
{series_rows}

## How to read this

The evaluator-upstream discipline (evaluation model + factor-keyed storyboard injected
into the draft prompt) is working when the FIRST Gold Team run of each successive bid
starts closer to the final run: the baseline pWin climbs, the issue count at baseline
falls, and the post-Gold-Team edit ratio shrinks. Within a single bid, this report shows
whether review-and-patch cycles are converging.
"""


def selftest() -> int:
    failures: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            failures.append(name)

    history = [
        {"schema_version": "gold-team-snapshot.v1", "timestamp": "2026-06-01T10:00:00Z",
         "proposal_id": "selftest", "mode": "mock-eval", "pwin": "Low",
         "counts": {"strengths": 2, "significant_strengths": 0, "weaknesses": 5,
                    "significant_weaknesses": 2, "deficiencies": 1},
         "unsupported_claim_count": 9},
        {"schema_version": "gold-team-snapshot.v1", "timestamp": "2026-06-05T10:00:00Z",
         "proposal_id": "selftest", "mode": "mock-eval", "pwin": "Moderate",
         "counts": {"strengths": 4, "significant_strengths": 1, "weaknesses": 2,
                    "significant_weaknesses": 0, "deficiencies": 0},
         "unsupported_claim_count": 2},
        {"schema_version": "gold-team-snapshot.v1", "timestamp": "2026-06-06T10:00:00Z",
         "proposal_id": "selftest", "mode": "lightweight", "pwin": None,
         "counts": {"strengths": 0, "weaknesses": 0, "deficiencies": 0}},
    ]
    lift = compute_lift(history, word_count=2000, unsupported_count=3)
    check("review count", lift["review_count"] == 3)
    check("scored count excludes null pwin", lift["scored_count"] == 2)
    check("baseline pwin", lift["baseline_pwin"] == "Low")
    check("current pwin", lift["current_pwin"] == "Moderate")
    check("pwin delta", lift["pwin_delta"] == 1)
    check("baseline issues", lift["baseline_issues"] == 8)
    check("current issues", lift["current_issues"] == 2)
    check("strengths counted with SS", lift["baseline_strengths"] == 2 and lift["current_strengths"] == 5)
    check("density", lift["unsupported_claim_density"] == 1.5)
    check("series length", len(lift["series"]) == 3)

    empty = compute_lift([], word_count=0, unsupported_count=0)
    check("empty history safe", empty["baseline_pwin"] is None and empty["unsupported_claim_density"] == 0.0)

    report = render_report("selftest", lift)
    check("report headline", "pWin improved Low -> Moderate" in report)
    check("report density", "1.5 per 1,000 words" in report)

    if failures:
        print("SELFTEST FAILED:")
        for name in failures:
            print(f"  - {name}")
        return 1
    print("SELFTEST OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--proposal", help="proposals/<slug> to operate on")
    parser.add_argument("--selftest", action="store_true", help="run the embedded deterministic self-test")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if not args.proposal:
        parser.error("--proposal is required (or use --selftest)")

    prop_dir = WORKSPACE_ROOT / "proposals" / args.proposal
    if not prop_dir.is_dir():
        print(f"ERROR: proposal directory not found: {prop_dir}", file=sys.stderr)
        return 2

    history = load_history(prop_dir / "reviews" / "gold-team-history.jsonl")
    if not history:
        print(
            "No Gold Team snapshot history at reviews/gold-team-history.jsonl. "
            "Run /red-team-review with a scoring mode first -- each run appends one snapshot.",
            file=sys.stderr,
        )
        return 1

    word_count, unsupported = draft_stats(prop_dir / "drafts")
    lift = compute_lift(history, word_count, unsupported)
    report = render_report(args.proposal, lift)
    reviews_dir = prop_dir / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)
    (reviews_dir / "lift.md").write_text(report, encoding="utf-8")
    print(report)
    print(f"-> wrote {reviews_dir / 'lift.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
