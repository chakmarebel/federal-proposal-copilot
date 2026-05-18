#!/usr/bin/env python3
"""prose-lint.py — deterministic AI-smell / prose-quality lint for proposal drafts.

This is NOT a beauty judge. It catches mechanical patterns that reliably make
proposal prose feel artificial or leak internal process vocabulary into
customer-facing text. Run it before /export-proposal.

Two severities:
  HIGH     — must not ship: the section-sign glyph, internal process vocabulary
             leaking into customer-facing prose. Exit code 1.
  ADVISORY — worth a look: banned marketing words, "we will" stacking, repeated
             paragraph openings. Exit code 0 (informational).

Usage:
  python scripts/prose-lint.py --proposal <slug>     # scans proposals/<slug>/drafts/*.md
  python scripts/prose-lint.py path/to/file.md ...   # scans the given files

Scope: top-level drafts/*.md only. drafts/loose/ (pre-bind Pass 1 drafts) is
skipped — loose drafts are allowed to be rough.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# --- HIGH: internal process vocabulary that must never reach customer-facing prose.
# Only unambiguously-internal terms; words like "evaluator" or "gate" are omitted
# because they appear legitimately in federal proposal prose.
PROCESS_TERMS = [
    "narrative spine", "storyboard", "draft-loose", "bind pass", "gold team",
    "red team", "red-team", "white glove", "white-glove", "compliance matrix",
    "win theme", "win-theme", "ghosting", "discriminator proof point",
    "narrative operating mode", "operating mode", "capture-intent",
    "proposal-writer", "proposal-editor", "evidence ledger", "section pattern",
    "CLAIM-UNSUPPORTED",
]

# --- ADVISORY: marketing words. Kept in sync with reference/editorial-voice-guide.md.
BANNED_WORDS = [
    "cutting-edge", "cutting edge", "innovative", "robust", "seamless",
    "transformative", "best-in-class", "world-class", "next-generation",
    "game-changing", "holistic", "synergy", "synergies", "utilize", "utilizes",
    "utilizing", "scalable", "end-to-end",
]
# "leverage" in any form — the editorial voice guide bans it; prefer use/apply/extend.
LEVERAGE = re.compile(r"\bleverag(?:e|es|ed|ing)\b", re.IGNORECASE)

WE_WILL_THRESHOLD = 8  # occurrences per file before it reads as a "we will" wall

HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_noise(text: str) -> list[tuple[int, str]]:
    """Return [(line_number, line)] with HTML comments blanked and fenced code
    blocks dropped. Line numbers are 1-based and refer to the original file."""
    out: list[tuple[int, str]] = []
    in_fence = False
    for i, raw in enumerate(text.splitlines(), start=1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        out.append((i, HTML_COMMENT.sub("", raw)))
    return out


def lint_file(path: Path) -> list[tuple[str, int, str]]:
    """Return findings as (severity, line_no, message)."""
    findings: list[tuple[str, int, str]] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = strip_noise(text)

    we_will = 0
    for ln, line in lines:
        low = line.lower()

        if "§" in line:
            findings.append(("HIGH", ln, "section-sign glyph (§) — spell out 'Section'"))

        for term in PROCESS_TERMS:
            if re.search(r"\b" + re.escape(term) + r"\b", low):
                findings.append(("HIGH", ln, f"internal process vocabulary leaked: '{term}'"))

        for w in BANNED_WORDS:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                findings.append(("ADVISORY", ln, f"marketing word: '{w}'"))
        if LEVERAGE.search(line):
            findings.append(("ADVISORY", ln, "'leverage' — use 'use', 'apply', or 'extend'"))

        we_will += len(re.findall(r"\bwe will\b", low))

    if we_will > WE_WILL_THRESHOLD:
        findings.append(("ADVISORY", 0, f"'we will' appears {we_will}x — vary commitment phrasing"))

    # Repeated paragraph openings: first 3 words of each body paragraph.
    blob = "\n".join(l for _, l in lines)
    openers: dict[str, int] = {}
    for para in re.split(r"\n\s*\n", blob):
        p = para.strip()
        if not p or p.startswith(("#", "|", "-", "*", ">", "1.", "2.", "3.")):
            continue
        words = re.findall(r"[A-Za-z][\w'-]*", p)
        if len(words) >= 3:
            key = " ".join(w.lower() for w in words[:3])
            openers[key] = openers.get(key, 0) + 1
    for key, count in openers.items():
        if count >= 3:
            findings.append(("ADVISORY", 0, f"{count} paragraphs open with '{key}...' — vary openings"))

    return findings


def resolve_files(args: argparse.Namespace) -> list[Path]:
    if args.proposal:
        drafts = REPO_ROOT / "proposals" / args.proposal / "drafts"
        if not drafts.is_dir():
            sys.exit(f"prose-lint: no drafts directory at {drafts}")
        return sorted(drafts.glob("*.md"))
    return [Path(f) for f in args.files]


def main() -> int:
    ap = argparse.ArgumentParser(description="AI-smell / prose-quality lint for proposal drafts.")
    ap.add_argument("--proposal", help="proposal slug — scans proposals/<slug>/drafts/*.md")
    ap.add_argument("files", nargs="*", help="explicit markdown files to scan")
    args = ap.parse_args()

    files = resolve_files(args)
    if not files:
        sys.exit("prose-lint: nothing to scan (give --proposal <slug> or file paths)")

    high_total = 0
    adv_total = 0
    for path in files:
        if not path.is_file():
            print(f"  skip (not found): {path}")
            continue
        findings = lint_file(path)
        high = [f for f in findings if f[0] == "HIGH"]
        adv = [f for f in findings if f[0] == "ADVISORY"]
        high_total += len(high)
        adv_total += len(adv)
        if not findings:
            print(f"OK    {path.name}")
            continue
        print(f"{'FAIL' if high else 'warn'}  {path.name}  ({len(high)} high, {len(adv)} advisory)")
        for sev, ln, msg in findings:
            loc = f"L{ln}" if ln else "file"
            print(f"        [{sev:8}] {loc}: {msg}")

    print()
    print(f"prose-lint: {high_total} HIGH, {adv_total} ADVISORY across {len(files)} file(s)")
    if high_total:
        print("HIGH findings must be resolved before export.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
