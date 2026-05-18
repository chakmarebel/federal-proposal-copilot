#!/usr/bin/env python3
"""Summarize skill invocation activity across all proposals.

Reads the existing per-proposal activity logs at proposals/<slug>/working/activity.md
(each line: '## YYYY-MM-DD HH:MM — <skill> [<mode>] — <summary> → <output>') and
produces a cross-proposal call-count summary. No separate skill log to maintain.

Examples:
  python scripts/skill-stats.py
  python scripts/skill-stats.py --since 2026-05-01
  python scripts/skill-stats.py --per-skill proposal-writer
  python scripts/skill-stats.py --proposals-dir /alt/path/proposals
"""

import argparse
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# Matches: "## 2026-05-11 14:30 — proposal-writer [mode] — summary → output"
# The mode is optional. The arrow is optional (some entries don't have one).
ENTRY_RE = re.compile(
    r"^##\s+"
    r"(?P<ts>\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?)\s*"
    r"[—-]+\s*"
    r"(?P<skill>[a-z][a-z0-9-]*)"
    r"(?:\s*\[(?P<mode>[^\]]+)\])?"
    r"\s*[—-]+\s*"
    r"(?P<summary>.*?)$"
)


def parse_ts(s: str) -> datetime | None:
    s = s.strip().replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Aggregate skill calls from activity.md files.")
    ap.add_argument("--proposals-dir", default="proposals",
                    help="Path containing per-proposal directories (default: proposals)")
    ap.add_argument("--since", help="ISO date or datetime; only count entries on/after this time")
    ap.add_argument("--per-skill", help="Show only entries for this skill, with proposal + summary")
    args = ap.parse_args()

    root = Path(args.proposals_dir)
    if not root.exists():
        print(f"No proposals directory at {root}.", file=sys.stderr)
        return 1

    since_dt = parse_ts(args.since) if args.since else None
    if args.since and not since_dt:
        print(f"Could not parse --since={args.since!r}", file=sys.stderr)
        return 2

    counts: Counter[str] = Counter()
    by_proposal: defaultdict[str, Counter[str]] = defaultdict(Counter)
    detail: list[tuple[str, str, str, str]] = []  # (ts, proposal, skill, summary)
    files_read = 0

    for activity in sorted(root.glob("*/working/activity.md")):
        proposal = activity.parts[-3]  # proposals/<slug>/working/activity.md
        files_read += 1
        for raw in activity.read_text(encoding="utf-8", errors="replace").splitlines():
            m = ENTRY_RE.match(raw.strip())
            if not m:
                continue
            ts, skill, summary = m.group("ts"), m.group("skill"), m.group("summary")
            if since_dt:
                entry_dt = parse_ts(ts)
                if entry_dt and entry_dt < since_dt:
                    continue
            if args.per_skill and skill != args.per_skill:
                continue
            counts[skill] += 1
            by_proposal[proposal][skill] += 1
            detail.append((ts, proposal, skill, summary))

    if args.per_skill:
        print(f"{args.per_skill}: {counts[args.per_skill]} call(s) across {len({p for _, p, _, _ in detail})} proposal(s)")
        for ts, proposal, _, summary in detail:
            print(f"  {ts}  [{proposal}]  {summary}")
    else:
        total = sum(counts.values())
        print(f"Total skill calls: {total}  (files read: {files_read}, distinct skills: {len(counts)})")
        print()
        print("By skill:")
        for skill, n in counts.most_common():
            print(f"  {n:>4}  {skill}")
        if by_proposal:
            print()
            print("By proposal:")
            for proposal, c in sorted(by_proposal.items()):
                print(f"  [{proposal}] {sum(c.values())} call(s), {len(c)} skill(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
