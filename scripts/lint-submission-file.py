#!/usr/bin/env python3
"""lint-submission-file.py — run the prose-lint HIGH rules over the ACTUAL outgoing
submission file (.pdf or .docx), not the markdown sources.

Why this exists (submission-diff calibration, DIA DMA 2026-07-26): once team review
moves to Google Docs, the Doc becomes the source of truth and `drafts/*.md` goes
stale — the submitted PDF contained em-dashes that prose-lint would have blocked,
because the linter never saw the file that was actually uploaded. This script closes
that gap: it extracts text from the final artifact and applies the HIGH rules plus a
bracket-placeholder scan.

Usage:
  python scripts/lint-submission-file.py final/pdf/Proposal.pdf final/docx/ROM.docx
  python scripts/lint-submission-file.py --selftest

Exit codes: 0 clean, 1 HIGH findings, 2 harness error (missing rules / unreadable file).

Notes on PDF extraction noise:
- Running headers/footers repeat per page; findings are reported per page, and
  duplicate (rule, snippet) pairs are collapsed so one header problem = one finding.
- Hyphenation at line breaks can produce false '--'; the em-dash pattern from
  reference/prose-lint-rules.json requires sentence-punctuation context, which
  avoids most of this. Review findings against the file before acting.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
try:  # the section-sign / dash findings themselves contain non-cp1252 characters;
    # without this the gate raises UnicodeEncodeError before printing a single finding.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RULES_PATH = REPO_ROOT / "reference" / "prose-lint-rules.json"

# Bracketed placeholders that must never ship. Three families, because real
# placeholders do not reliably start with a keyword (calibration: the CDAO ADL draft
# carried "[SUBMISSION DATE]", "[OPEN: confirm ...]", and "[Confirm which ...]", none
# of which a start-anchored, case-sensitive pattern catches):
#   1. keyword ANYWHERE inside the bracket, case-insensitive
#   2. "shouty" brackets — ALL-CAPS content that is multi-word or leads into a colon
#      ("[SUBMISSION DATE]", "[MARKINGS DECISION: ...]") while leaving "[USA]",
#      "[1]", "[sic]", "[UNCLASSIFIED]" alone
#   3. empty / punctuation-only brackets ("[]", "[ ]", "[?]", "[...]")
_PLACEHOLDER_KEYWORD = re.compile(
    r"\[[^\]]*\b(?:needs?|tbd|todo|tk|confirm\w*|verif\w+|placeholder|insert"
    r"|fixme|fill[\s-]?in|pending|x{3,})\b[^\]]*\]"
    r"|\[[^\]]*\b(?:open|optional|decision|note|draft)\s*:[^\]]*\]",
    re.IGNORECASE,
)
_PLACEHOLDER_SHOUTY = re.compile(
    r"\[[A-Z][A-Z0-9]*(?:[\s,/&'’-]+[A-Z0-9][A-Z0-9]*)+\]"  # 2+ ALL-CAPS words
    r"|\[[A-Z][A-Z0-9\s,/&'’-]*:[^\]]*\]"                    # ALL-CAPS lead + colon
)
_PLACEHOLDER_EMPTY = re.compile(r"\[\s*[?.…]*\s*\]")

# ALL-CAPS bracketed strings that are legitimate markings, not placeholders.
_SHOUTY_ALLOW = {
    "FOR OFFICIAL USE ONLY",
    "CONTROLLED UNCLASSIFIED INFORMATION",
    "DISTRIBUTION STATEMENT A",
}


def find_bracket_placeholders(line: str) -> list[tuple[int, int]]:
    """Return non-overlapping (start, end) spans of bracketed placeholders."""
    spans: list[tuple[int, int]] = []
    for pattern in (_PLACEHOLDER_KEYWORD, _PLACEHOLDER_SHOUTY, _PLACEHOLDER_EMPTY):
        for m in pattern.finditer(line):
            if pattern is _PLACEHOLDER_SHOUTY:
                inner = line[m.start() + 1:m.end() - 1].strip().rstrip(":").strip()
                if inner.upper() in _SHOUTY_ALLOW:
                    continue
            if any(s < m.end() and m.start() < e for s, e in spans):
                continue  # already reported by an earlier family
            spans.append((m.start(), m.end()))
    return sorted(spans)


def _load_rules() -> dict:
    try:
        return json.loads(RULES_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"lint-submission-file: rules file not found: {RULES_PATH}", file=sys.stderr)
        raise SystemExit(2)
    except (OSError, ValueError) as exc:
        print(f"lint-submission-file: could not parse rules file {RULES_PATH}: {exc}", file=sys.stderr)
        raise SystemExit(2)


def extract_units(path: Path) -> list[tuple[str, str]]:
    """Return [(location_label, text)] units — one per PDF page or docx paragraph/cell."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        try:
            import fitz  # pymupdf
        except ImportError:
            print("lint-submission-file: pymupdf not installed (pip install pymupdf)", file=sys.stderr)
            raise SystemExit(2)
        doc = fitz.open(str(path))
        return [(f"p{i+1}", page.get_text()) for i, page in enumerate(doc)]
    if suffix == ".docx":
        try:
            import docx  # python-docx
        except ImportError:
            print("lint-submission-file: python-docx not installed", file=sys.stderr)
            raise SystemExit(2)
        d = docx.Document(str(path))
        units = [(f"para{i+1}", p.text) for i, p in enumerate(d.paragraphs) if p.text.strip()]
        for ti, t in enumerate(d.tables):
            for ri, row in enumerate(t.rows):
                for cell in row.cells:
                    if cell.text.strip():
                        units.append((f"table{ti+1}r{ri+1}", cell.text))
        return units
    print(f"lint-submission-file: unsupported file type: {path}", file=sys.stderr)
    raise SystemExit(2)


def lint_text_units(units: list[tuple[str, str]], rules: dict) -> list[tuple[str, str, str]]:
    """Return deduplicated findings as (location, rule, snippet)."""
    terms = rules.get("term_lists", {})
    patterns = rules.get("patterns", {})
    process_terms = terms.get("process_terms", [])
    never = r"(?!x)x"
    em_dash = re.compile(patterns.get("em_dash", never))

    findings: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add(loc: str, rule: str, snippet: str) -> None:
        snippet = re.sub(r"\s+", " ", snippet).strip()[:90]
        key = (rule, snippet.lower())
        if key in seen:
            return
        seen.add(key)
        findings.append((loc, rule, snippet))

    for loc, text in units:
        for line in text.splitlines():
            low = line.lower()
            if "§" in line:
                add(loc, "section-sign glyph", line)
            m = em_dash.search(line)
            if m:
                start = max(0, m.start() - 40)
                add(loc, "dash as sentence punctuation", line[start:m.end() + 40])
            for term in process_terms:
                if re.search(r"\b" + re.escape(term) + r"\b", low):
                    add(loc, f"internal process vocabulary: '{term}'", line)
            for start, end in find_bracket_placeholders(line):
                add(loc, "bracketed placeholder shipped", line[max(0, start - 30):end + 30])
    return findings


def selftest() -> int:
    rules = _load_rules()
    units = [
        ("p1", "The team delivers a runtime — and an accreditation path — the team has walked."),
        ("p1", "Contract / program: [NEEDS: BigBear releasable program identifier]"),
        ("p2", "See Section 3.2 for details."),
        ("p2", "Period of performance: six months from award."),
        # placeholders that a start-anchored, case-sensitive pattern used to miss
        ("p3", "Date of submission: [SUBMISSION DATE]"),
        ("p3", "Point of contact: [Confirm POC before release]"),
        ("p3", "[OPEN: confirm active-CAC holders by name]"),
        # legitimate brackets that must NOT be flagged
        ("p4", "Prior work [1] and the note [sic] stay as written."),
        ("p4", "Marked [UNCLASSIFIED] on every page."),
        ("p4", "The banner [FOR OFFICIAL USE ONLY] is a real marking."),
    ]
    findings = lint_text_units(units, rules)
    rules_hit = {f[1].split(":")[0] for f in findings}
    placeholders = [f[2] for f in findings if f[1] == "bracketed placeholder shipped"]
    expected_hits = ("[NEEDS:", "[SUBMISSION DATE]", "[Confirm POC", "[OPEN: confirm")
    missed = [t for t in expected_hits if not any(t in s for s in placeholders)]
    false_pos = [s for s in placeholders
                 if any(t in s for t in ("[1]", "[sic]", "[UNCLASSIFIED]", "OFFICIAL USE"))]
    ok = ("dash as sentence punctuation" in rules_hit
          and not missed
          and not false_pos
          and not any("Section 3.2" in f[2] for f in findings if "glyph" in f[1]))
    if missed:
        print("selftest MISSED placeholders:", missed)
    if false_pos:
        print("selftest FALSE POSITIVES:", false_pos)
    print("selftest findings:")
    for loc, rule, snip in findings:
        print(f"  [{loc}] {rule}: ...{snip}...")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint the actual outgoing submission file (.pdf/.docx) with prose-lint HIGH rules.")
    ap.add_argument("files", nargs="*", help=".pdf or .docx files that will be submitted")
    ap.add_argument("--selftest", action="store_true", help="run deterministic offline self-test")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.files:
        ap.error("give one or more .pdf/.docx files, or --selftest")

    rules = _load_rules()
    total = 0
    for f in args.files:
        path = Path(f)
        if not path.is_file():
            print(f"  skip (not found): {path}")
            continue
        findings = lint_text_units(extract_units(path), rules)
        total += len(findings)
        if not findings:
            print(f"OK    {path.name}")
            continue
        print(f"FAIL  {path.name}  ({len(findings)} HIGH finding(s))")
        for loc, rule, snip in findings:
            print(f"        [{loc}] {rule}: ...{snip}...")

    print()
    print(f"lint-submission-file: {total} HIGH finding(s)")
    if total:
        print("Resolve in the source file (Google Doc / Word) and re-export before uploading.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
