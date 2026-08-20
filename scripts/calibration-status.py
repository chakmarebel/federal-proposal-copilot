#!/usr/bin/env python3
"""calibration-status.py — make the calibration corpus's emptiness visible.

The calibration corpus (corpus/calibration/) is the framework's flagship
learning loop, but it stays empty because feeding it is friction and nothing
nags. This script reports, at a glance:

  - how many calibration entries exist (and their phase)
  - how many proposals look SUBMITTED but have NO calibration entry
    (the backfill gap — the highest-value thing to feed)

"Submitted" is inferred from artifacts, since the repo has no explicit status
field: a proposal counts as submitted if its final/ directory holds at least one
real file (an /export-proposal package). This is the same signal /capture-submission
Phase 2 keys off.

Exit codes:
  0  clean report (or --selftest passed)
  3  with --strict: there is at least one submitted proposal with no calibration
     entry (use in CI / pre-release to keep the corpus from silently rotting)

Usage:
  python scripts/calibration-status.py
  python scripts/calibration-status.py --strict     # non-zero if backfill gap > 0
  python scripts/calibration-status.py --json        # machine-readable
  python scripts/calibration-status.py --selftest
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Force UTF-8 stdout so box-drawing / check glyphs survive on Windows consoles
# (default cp1252) and in CI redirection alike.
try:  # pragma: no cover - environment dependent
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent.parent
PROPOSALS = ROOT / "proposals"
CALIBRATION = ROOT / "corpus" / "calibration"

# Corpus entries that are structure, not real per-slug data.
RESERVED = {"_template", "README.md"}


def final_file_count(proposal_dir: Path) -> int:
    """Count real files under a proposal's final/ dir (submission artifacts)."""
    final = proposal_dir / "final"
    if not final.is_dir():
        return 0
    return sum(1 for p in final.rglob("*") if p.is_file())


def scan(root: Path):
    """Return (proposals, entries) summaries for a given repo root."""
    proposals_dir = root / "proposals"
    calibration_dir = root / "corpus" / "calibration"

    proposals = []
    if proposals_dir.is_dir():
        for d in sorted(proposals_dir.iterdir()):
            if not d.is_dir() or d.name.startswith("_"):
                continue
            n_final = final_file_count(d)
            proposals.append(
                {"slug": d.name, "submitted": n_final > 0, "final_files": n_final}
            )

    entries = {}
    if calibration_dir.is_dir():
        for d in sorted(calibration_dir.iterdir()):
            if not d.is_dir() or d.name in RESERVED:
                continue
            manifest = d / "manifest.json"
            status = "unknown"
            if manifest.is_file():
                try:
                    status = json.loads(manifest.read_text(encoding="utf-8")).get(
                        "status", "unknown"
                    )
                except (json.JSONDecodeError, OSError):
                    status = "malformed-manifest"
            has_auto = (d / "auto-draft").is_dir()
            has_final = (d / "final-submitted").is_dir()
            entries[d.name] = {
                "slug": d.name,
                "status": status,
                "has_auto_draft": has_auto,
                "has_final_submitted": has_final,
            }

    return proposals, entries


def build_report(root: Path):
    proposals, entries = scan(root)
    entry_slugs = set(entries)
    submitted = [p for p in proposals if p["submitted"]]
    submitted_slugs = {p["slug"] for p in submitted}

    # Backfill gap: submitted proposals with no calibration entry.
    backfill = sorted(
        (p for p in submitted if p["slug"] not in entry_slugs),
        key=lambda p: -p["final_files"],
    )

    return {
        "total_proposals": len(proposals),
        "submitted_proposals": len(submitted),
        "calibration_entries": len(entries),
        "entries": entries,
        "backfill_candidates": backfill,
        "submitted_slugs": sorted(submitted_slugs),
    }


def print_report(rep) -> None:
    print("── Calibration corpus status ──")
    print(f"  Proposals total:        {rep['total_proposals']}")
    print(f"  Proposals submitted:    {rep['submitted_proposals']}  (final/ has artifacts)")
    print(f"  Calibration entries:    {rep['calibration_entries']}")
    print()

    if rep["calibration_entries"] == 0:
        print("  ⚠ The calibration corpus is EMPTY.")
        print("    Every submitted proposal edited by hand is training signal being thrown away.")
        print("    See corpus/calibration/README.md — this is the flagship learning loop.")
    else:
        print("  Entries:")
        for slug, e in rep["entries"].items():
            flags = []
            if e["has_auto_draft"]:
                flags.append("auto-draft")
            if e["has_final_submitted"]:
                flags.append("final-submitted")
            print(f"    - {slug}  [{e['status']}]  {' + '.join(flags) or '(empty)'}")
    print()

    n = len(rep["backfill_candidates"])
    if n:
        print(f"  ⚠ {n} submitted proposal(s) have NO calibration entry (backfill gap):")
        for p in rep["backfill_candidates"]:
            print(f"      {p['slug']}  ({p['final_files']} final artifact(s))")
        print()
        print("  To start an entry (snapshots drafts/ → auto-draft, seeds manifest + edit-notes):")
        print(f"      bash scripts/new-calibration-entry.sh {rep['backfill_candidates'][0]['slug']}")
        print("  Then fill edit-notes.md and run /capture-submission (Phase 2) after review.")
    else:
        if rep["submitted_proposals"]:
            print("  ✓ Every submitted proposal has a calibration entry.")
    print()


def selftest() -> int:
    import tempfile

    print("── calibration-status --selftest ──")
    rc = 0
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # Proposal A: submitted (has final/ file), no calibration entry -> backfill.
        (root / "proposals" / "alpha" / "final" / "docx").mkdir(parents=True)
        (root / "proposals" / "alpha" / "final" / "docx" / "vol1.docx").write_text("x")
        # Proposal B: not submitted (empty final/).
        (root / "proposals" / "bravo" / "final").mkdir(parents=True)
        # Proposal C: submitted AND has a calibration entry.
        (root / "proposals" / "charlie" / "final").mkdir(parents=True)
        (root / "proposals" / "charlie" / "final" / "p.pdf").write_text("x")
        (root / "corpus" / "calibration" / "charlie" / "auto-draft").mkdir(parents=True)
        (root / "corpus" / "calibration" / "charlie" / "manifest.json").write_text(
            json.dumps({"status": "pre-edit"})
        )
        # Reserved dirs must be ignored.
        (root / "corpus" / "calibration" / "_template").mkdir(parents=True)
        (root / "corpus" / "calibration" / "README.md").write_text("readme")

        rep = build_report(root)

        def check(label, cond):
            nonlocal rc
            if cond:
                print(f"  ✓ {label}")
            else:
                print(f"  ✗ FAIL: {label}")
                rc = 1

        check("counts 3 proposals", rep["total_proposals"] == 3)
        check("counts 2 submitted (alpha, charlie)", rep["submitted_proposals"] == 2)
        check("counts 1 calibration entry (charlie)", rep["calibration_entries"] == 1)
        check(
            "_template/README are not counted as entries",
            "_template" not in rep["entries"] and "README.md" not in rep["entries"],
        )
        backfill_slugs = {p["slug"] for p in rep["backfill_candidates"]}
        check("backfill gap = {alpha} only", backfill_slugs == {"alpha"})
        check("bravo (unsubmitted) not in backfill", "bravo" not in backfill_slugs)

    print()
    print("  ✓ SELFTEST PASSED" if rc == 0 else "  ✗ SELFTEST FAILED")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(description="Report calibration corpus coverage vs submitted proposals.")
    ap.add_argument("--strict", action="store_true", help="exit 3 if any submitted proposal lacks a calibration entry")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--selftest", action="store_true", help="run the offline self-test")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    rep = build_report(ROOT)
    if args.json:
        print(json.dumps(rep, indent=2))
    else:
        print_report(rep)

    if args.strict and rep["backfill_candidates"]:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
