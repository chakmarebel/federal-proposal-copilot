#!/usr/bin/env python3
"""Backfill reviews/gold-team-history.jsonl from an existing gold-team-scorecard.md.

The lift metric (scripts/compute-lift.py) needs an accumulated snapshot series, but
proposals reviewed before the evaluator-upstream port only have the (overwritten)
scorecard markdown. This script parses that scorecard leniently into one
gold-team-snapshot.v1 line so the history starts with a real baseline instead of cold.

Parsing is best-effort because scorecard formats vary (formal S/W/D, lightweight
reader response, rubric-weighted variants). Rules:
  - pWin: hybrid values are normalized DOWN conservatively ("Moderate-High" -> Moderate);
    the raw wording is preserved in notes. Unparseable -> null.
  - factor ratings: table rows containing an adjectival rating word; when a row shows
    movement ("Good-at-risk -> Good"), the LAST rating in the row wins.
  - counts: finding headings ("#### Strength N", "#### Significant Weakness: ...").
    Zero is a valid result for scorecards without S/W/D structure.
  - timestamp: the scorecard's **Date:** line (midnight Z); falls back to file mtime.

Idempotent: skips a proposal whose history already contains a "backfilled" entry for
the same scorecard date. Appends only; never rewrites existing lines.

Usage:
  python scripts/backfill-gold-snapshots.py --proposal <slug>
  python scripts/backfill-gold-snapshots.py --all
  python scripts/backfill-gold-snapshots.py --selftest
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).parent.parent

PWIN_WORDS = ["very low", "low", "moderate", "high"]  # ascending; conservative pick = lowest present
PWIN_CANON = {"very low": "Very Low", "low": "Low", "moderate": "Moderate", "high": "High"}
RATING_WORDS = ["Outstanding", "Good", "Acceptable", "Marginal", "Unacceptable"]


def parse_date(text: str) -> str | None:
    match = re.search(r"\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})", text)
    return f"{match.group(1)}T00:00:00Z" if match else None


def parse_pwin(text: str) -> tuple[str | None, str | None]:
    """Returns (canonical_pwin, raw_phrase). Hybrids normalize to the LOWER tier."""
    match = re.search(r"pWin(?:\s+Estimate)?\s*[:=]\s*\**([^\n*|]+)", text, re.IGNORECASE)
    if not match:
        return None, None
    raw = " ".join(match.group(1).split()).strip(" .")
    lowered = raw.lower()
    present = [word for word in PWIN_WORDS if re.search(rf"\b{word}\b", lowered)]
    if "very low" in present and "low" in present:
        present.remove("low")  # "very low" contains "low"; don't double-count
    if not present:
        return None, raw
    return PWIN_CANON[present[0]], raw  # PWIN_WORDS is ascending -> first = most conservative


def parse_factor_ratings(text: str) -> list[dict]:
    ratings: list[dict] = []
    rating_pattern = re.compile(r"\b(" + "|".join(RATING_WORDS) + r")\b")
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip().strip("*").strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() in {"factor", "rubric factor", "#", "criterion", ""}:
            continue
        if set(cells[0]) <= {"-", " ", ":"}:
            continue
        found = rating_pattern.findall(stripped)
        if not found:
            continue
        factor = cells[0] if not cells[0].isdigit() else (cells[1] if len(cells) > 1 else cells[0])
        ratings.append({"factor": factor[:120], "rating": found[-1]})
    return ratings


def parse_counts(text: str) -> dict:
    def count(pattern: str) -> int:
        return len(re.findall(pattern, text, re.MULTILINE))

    significant_strengths = count(r"^#{3,5}\s*Significant Strength\b")
    significant_weaknesses = count(r"^#{3,5}\s*Significant Weakness\b")
    return {
        "strengths": count(r"^#{3,5}\s*Strength\b"),
        "significant_strengths": significant_strengths,
        "weaknesses": count(r"^#{3,5}\s*Weakness\b"),
        "significant_weaknesses": significant_weaknesses,
        "deficiencies": count(r"^#{3,5}\s*Deficiency\b"),
    }


def build_snapshot(proposal: str, scorecard_text: str, mtime_iso: str) -> dict:
    pwin, raw_pwin = parse_pwin(scorecard_text)
    timestamp = parse_date(scorecard_text) or mtime_iso
    notes = "backfilled from gold-team-scorecard.md (lenient parse)"
    if raw_pwin and (pwin is None or raw_pwin.lower() != (pwin or "").lower()):
        notes += f"; raw pWin: {raw_pwin}"
    return {
        "schema_version": "gold-team-snapshot.v1",
        "timestamp": timestamp,
        "proposal_id": proposal,
        "mode": "backfill",
        "pwin": pwin,
        "factor_ratings": parse_factor_ratings(scorecard_text),
        "counts": parse_counts(scorecard_text),
        "draft_word_count": None,
        "unsupported_claim_count": None,
        "notes": notes,
    }


def backfill_proposal(prop_dir: Path) -> str:
    scorecard = prop_dir / "reviews" / "gold-team-scorecard.md"
    if not scorecard.exists():
        return "no scorecard"
    history_path = prop_dir / "reviews" / "gold-team-history.jsonl"
    text = scorecard.read_text(encoding="utf-8", errors="replace")
    mtime_iso = datetime.fromtimestamp(scorecard.stat().st_mtime, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    snapshot = build_snapshot(prop_dir.name, text, mtime_iso)

    if history_path.exists():
        for line in history_path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (
                isinstance(entry, dict)
                and entry.get("mode") == "backfill"
                and entry.get("timestamp") == snapshot["timestamp"]
            ):
                return "already backfilled"

    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(snapshot, ensure_ascii=False) + "\n")
    pwin = snapshot["pwin"] or "n/a"
    return (
        f"backfilled (pWin {pwin}, {len(snapshot['factor_ratings'])} factor ratings, "
        f"counts {snapshot['counts']})"
    )


SELFTEST_SCORECARD = """\
# Gold Team Mock Evaluation -- Selftest

**Date:** 2026-05-05 (re-run after tone sweep)
**Evaluator profile:** Mock evaluator.

| Factor | Importance | Rating | Rationale (1-line) |
|---|---|---|---|
| EF-1 Maturity | Most Important | **Good** | solid |
| EF-2 Alignment | Important | Good-at-risk -> **Good** | improved |
| EF-3 Price | | Favorable (no adjectival rating) | n/a |

## pWin Estimate: **Moderate-High** (conditional)

### Strengths

#### Strength 1: deployment record
- **Basis:** cite

#### Significant Strength: air-gapped operation
- **Basis:** cite

### Weaknesses

#### Weakness 1: unnamed personnel
- **Basis:** cite

### Deficiencies
(None)
"""


def selftest() -> int:
    failures: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            failures.append(name)

    snapshot = build_snapshot("selftest", SELFTEST_SCORECARD, "2026-06-10T00:00:00Z")
    check("date from scorecard", snapshot["timestamp"] == "2026-05-05T00:00:00Z")
    check("hybrid pwin normalized down", snapshot["pwin"] == "Moderate")
    check("raw pwin kept in notes", "Moderate-High" in (snapshot["notes"] or ""))
    ratings = {entry["factor"]: entry["rating"] for entry in snapshot["factor_ratings"]}
    check("plain rating parsed", ratings.get("EF-1 Maturity") == "Good")
    check("movement row takes last rating", ratings.get("EF-2 Alignment") == "Good")
    check("non-adjectival row skipped", "EF-3 Price" not in ratings)
    counts = snapshot["counts"]
    check("strength heading counted", counts["strengths"] == 1)
    check("significant strength counted", counts["significant_strengths"] == 1)
    check("weakness counted", counts["weaknesses"] == 1)
    check("deficiency zero", counts["deficiencies"] == 0)

    pwin, raw = parse_pwin("## pWin Estimate: Very Low\n")
    check("very low not double-counted", pwin == "Very Low" and raw == "Very Low")
    pwin, _ = parse_pwin("**Awardability posture:** strong\n")
    check("no pwin -> none", pwin is None)

    if failures:
        print("SELFTEST FAILED:")
        for name in failures:
            print(f"  - {name}")
        return 1
    print("SELFTEST OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--proposal", help="proposals/<slug> to backfill")
    parser.add_argument("--all", action="store_true", help="backfill every proposal with a scorecard")
    parser.add_argument("--selftest", action="store_true", help="run the embedded deterministic self-test")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if not args.proposal and not args.all:
        parser.error("--proposal <slug> or --all is required (or use --selftest)")

    proposals_root = WORKSPACE_ROOT / "proposals"
    if args.all:
        targets = sorted(path for path in proposals_root.iterdir() if path.is_dir())
    else:
        targets = [proposals_root / args.proposal]

    any_done = False
    for prop_dir in targets:
        if not prop_dir.is_dir():
            print(f"ERROR: proposal directory not found: {prop_dir}", file=sys.stderr)
            return 2
        result = backfill_proposal(prop_dir)
        if result != "no scorecard" or not args.all:
            print(f"{prop_dir.name}: {result}")
        if result.startswith("backfilled"):
            any_done = True
    return 0 if (any_done or args.all) else 1


if __name__ == "__main__":
    sys.exit(main())
