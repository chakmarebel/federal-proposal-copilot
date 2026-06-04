#!/usr/bin/env python3
"""prose-lint.py — deterministic AI-smell / prose-quality lint for proposal drafts.

This is NOT a beauty judge. It catches mechanical patterns that reliably make
proposal prose feel artificial or leak internal process vocabulary into
customer-facing text. Run it before /export-proposal.

Two severities:
  HIGH     — must not ship: the section-sign glyph, dashes used as sentence
             punctuation, internal process vocabulary leaking into
             customer-facing prose. Exit code 1.
  ADVISORY — worth a look: banned marketing words, self-narration /
             performative-honesty commentary, prohibited-claim diction without a
             ledger cite, forbidden absolutes, "we will" stacking, repeated
             paragraph openings. Exit code 0 (informational).

Usage:
  python scripts/prose-lint.py --proposal <slug>     # scans proposals/<slug>/drafts/*.md
  python scripts/prose-lint.py path/to/file.md ...   # scans the given files

Scope: top-level drafts/*.md only. drafts/loose/ (pre-bind Pass 1 drafts) is
skipped — loose drafts are allowed to be rough.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# --- Rule set. The rule CONTENT lives in reference/prose-lint-rules.json (a shared,
# syncable data file — see tools/sync-voice-anchors.sh); this script is only the harness.
# A rule added to the JSON propagates here with no code edit, and to the sibling apps
# (federal-proposal-copilot, proposal-workbench) on their next sync.
#
# prose-lint is an export gate, so it FAILS CLOSED: if the rules file is missing or
# malformed, error out (exit 2) rather than silently passing with no rules.
RULES_PATH = REPO_ROOT / "reference" / "prose-lint-rules.json"


def _load_rules() -> dict:
    try:
        return json.loads(RULES_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"prose-lint: rules file not found: {RULES_PATH}", file=sys.stderr)
        raise SystemExit(2)
    except (OSError, ValueError) as exc:
        print(f"prose-lint: could not parse rules file {RULES_PATH}: {exc}", file=sys.stderr)
        raise SystemExit(2)


_RULES = _load_rules()
_TERMS = _RULES.get("term_lists", {})
_PATTERNS = _RULES.get("patterns", {})
_THRESHOLDS = _RULES.get("thresholds", {})

# HIGH: internal process vocabulary that must never reach customer-facing prose.
PROCESS_TERMS = _TERMS.get("process_terms", [])
# ADVISORY: marketing words (mirrors reference/editorial-voice-guide.md).
BANNED_WORDS = _TERMS.get("banned_words", [])
# ADVISORY: self-referential / performative-honesty commentary.
META_COMMENTARY = _TERMS.get("meta_commentary", [])
# ADVISORY: prohibited-claim diction needing an evidence-ledger cite.
PROHIBITED_CLAIM_TERMS = _TERMS.get("prohibited_claim_terms", [])
# ADVISORY: implicit-superiority absolutes.
FORBIDDEN_ABSOLUTES = _TERMS.get("forbidden_absolutes", [])

# HIGH: em-/en-dash or "--" as sentence punctuation. "---" rules and "|---|" separators
# do not match because the double-hyphen forms require surrounding whitespace/word chars.
_NEVER = r"(?!x)x"  # never-matches, if a pattern is absent from the rules file
EM_DASH = re.compile(_PATTERNS.get("em_dash", _NEVER))
# ADVISORY: "leverage" in any form — prefer use/apply/extend.
LEVERAGE = re.compile(_PATTERNS.get("leverage", _NEVER), re.IGNORECASE)

WE_WILL_THRESHOLD = _THRESHOLDS.get("we_will", 8)  # occurrences before it reads as a wall
REPEATED_OPENING_THRESHOLD = _THRESHOLDS.get("repeated_opening", 3)

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

        if EM_DASH.search(line):
            findings.append(("HIGH", ln, "em-dash/en-dash/'--' as sentence punctuation — rewrite with a period, comma, colon, or parentheses"))

        for term in PROCESS_TERMS:
            if re.search(r"\b" + re.escape(term) + r"\b", low):
                findings.append(("HIGH", ln, f"internal process vocabulary leaked: '{term}'"))

        for w in BANNED_WORDS:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                findings.append(("ADVISORY", ln, f"marketing word: '{w}'"))
        if LEVERAGE.search(line):
            findings.append(("ADVISORY", ln, "'leverage' — use 'use', 'apply', or 'extend'"))

        meta_hit = next((phrase for phrase in META_COMMENTARY if phrase in low), None)
        if meta_hit:
            findings.append(("ADVISORY", ln, f"self-referential / performative-honesty commentary: '{meta_hit}' — state the capability and its boundary plainly"))

        for term in PROHIBITED_CLAIM_TERMS:
            if re.search(r"\b" + re.escape(term) + r"\b", low):
                findings.append(("ADVISORY", ln, f"prohibited claim term without verified citation: '{term}' — confirm an evidence-ledger cite or move to a Gaps note"))

        for phrase in FORBIDDEN_ABSOLUTES:
            if phrase in low:
                findings.append(("ADVISORY", ln, f"forbidden absolute: '{phrase}' — replace with a quantified, sourced comparison"))

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
        if count >= REPEATED_OPENING_THRESHOLD:
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
