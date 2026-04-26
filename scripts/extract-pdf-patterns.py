#!/usr/bin/env python3
"""
Extract STRUCTURAL patterns from a winning proposal PDF.

Goal: surface document structure / section-pattern / formatting conventions
WITHOUT exposing prose content that could contaminate future proposals.

Outputs to stdout:
  - Page count
  - Per-page: word count, top-level headings detected, presence of tables/figures
  - All headings (lines that look like H1/H2/H3) — caller can sanitize
  - Word frequency for top 50 terms (helps spot tone/cadence patterns)
  - Sentence length distribution
  - Paragraph density per page
  - Heuristic detection: action captions, theme statements, bullet structure

Caller is expected to read this, extract STRUCTURAL learning, and DELETE the
raw output afterward — no source-derived content should land in the repo.

Usage:
    python scripts/extract-pdf-patterns.py /path/to/proposal.pdf [--full]

--full also prints per-page first-line previews (use with care).
"""
from __future__ import annotations

import argparse
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

import pypdf


HEADING_RE = re.compile(r"^(?:[0-9]+\.[0-9.]*\s+|[IVX]+\.\s+|[A-Z][A-Z\s]{4,}$)")
ACTION_CAPTION_RE = re.compile(r"^(?:figure|fig\.?|table|tbl\.?)\s*\d", re.IGNORECASE)
BULLET_RE = re.compile(r"^\s*[•·▪◦\-\*]\s")
NUMBERED_LIST_RE = re.compile(r"^\s*\d+[\.\)]\s")
SENTENCE_END_RE = re.compile(r"[.!?](?:\s|$)")


def extract_text(pdf_path: Path) -> list[str]:
    reader = pypdf.PdfReader(str(pdf_path))
    return [page.extract_text() or "" for page in reader.pages]


def detect_headings(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or len(line) > 120:
            continue
        if HEADING_RE.match(line):
            out.append(line)
    return out


def detect_action_captions(text: str) -> int:
    return sum(1 for line in text.splitlines() if ACTION_CAPTION_RE.match(line.strip()))


def count_bullets(text: str) -> int:
    return sum(1 for line in text.splitlines() if BULLET_RE.match(line) or NUMBERED_LIST_RE.match(line))


def sentence_lengths(text: str) -> list[int]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [len(s.split()) for s in sentences if 3 <= len(s.split()) <= 100]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--full", action="store_true", help="Print per-page first-line previews")
    args = ap.parse_args(argv)

    if not args.pdf.exists():
        print(f"error: {args.pdf} not found", file=sys.stderr)
        return 1

    pages = extract_text(args.pdf)
    n = len(pages)

    print(f"=== {args.pdf.name} ===")
    print(f"Pages: {n}")
    print()

    # Per-page summary
    print("Per-page summary:")
    print(f"{'pg':>4}  {'words':>6}  {'heads':>5}  {'figs':>4}  {'bullets':>7}  {'1st-heading or H1 hint'}")
    all_headings_per_page = []
    total_words = 0
    total_figs = 0
    total_bullets = 0
    for i, text in enumerate(pages, 1):
        words = len(text.split())
        heads = detect_headings(text)
        figs = detect_action_captions(text)
        bullets = count_bullets(text)
        first_head = heads[0] if heads else ""
        # Print first heading; truncate to 60 chars to avoid leaking too much
        first_head_safe = (first_head[:60] + "…") if len(first_head) > 60 else first_head
        print(f"{i:>4}  {words:>6}  {len(heads):>5}  {figs:>4}  {bullets:>7}  {first_head_safe}")
        all_headings_per_page.append(heads)
        total_words += words
        total_figs += figs
        total_bullets += bullets

    print()
    print(f"TOTALS  {total_words:>6}  {sum(len(h) for h in all_headings_per_page):>5}  {total_figs:>4}  {total_bullets:>7}")

    # Sentence-length distribution
    full_text = "\n".join(pages)
    sl = sentence_lengths(full_text)
    if sl:
        print()
        print("Sentence-length distribution (words/sentence):")
        print(f"  count: {len(sl)}")
        print(f"  mean:  {statistics.mean(sl):.1f}")
        print(f"  median:{statistics.median(sl):.1f}")
        print(f"  p90:   {statistics.quantiles(sl, n=10)[8]:.1f}")
        print(f"  max:   {max(sl)}")

    # Heading taxonomy (deduplicate, keep order)
    seen = set()
    headings_dedup = []
    for hs in all_headings_per_page:
        for h in hs:
            if h not in seen:
                seen.add(h)
                headings_dedup.append(h)
    print()
    print(f"Distinct headings detected: {len(headings_dedup)}")
    print("(printed below — review for structural pattern, do not copy prose)")
    print()
    for h in headings_dedup:
        print(f"  • {h}")

    # Heading-style classification: numbering depth
    print()
    print("Heading numbering-depth distribution:")
    depth_counter = Counter()
    for h in headings_dedup:
        m = re.match(r"^([0-9]+)((?:\.[0-9]+)*)\s", h)
        if m:
            depth = h.count(".", len(m.group(1)) - 1) + (1 if m.group(2) else 0)
            depth_counter[f"{m.group(1)}{m.group(2)}".count(".") + 1] += 1
        else:
            depth_counter["non-numeric"] = depth_counter.get("non-numeric", 0) + 1
    for d, c in sorted(depth_counter.items(), key=lambda kv: str(kv[0])):
        print(f"  depth {d}: {c} headings")

    # Word frequency (filtered)
    common_skip = {"the", "and", "of", "to", "a", "in", "is", "for", "with", "on", "as", "by",
                   "an", "are", "be", "this", "that", "from", "or", "at", "will", "can", "we",
                   "our", "it", "its", "these", "their", "they", "have", "has", "had", "all",
                   "such", "than", "but", "not", "if", "into", "any", "more", "each", "which",
                   "also", "between", "across", "while", "where", "must", "may", "should",
                   "would", "could", "been", "was", "were", "us", "i", "you", "your"}
    words = re.findall(r"\b[a-z]{3,}\b", full_text.lower())
    freq = Counter(w for w in words if w not in common_skip)
    print()
    print("Top 50 content words (sanitize before publishing — may contain proper nouns):")
    for w, c in freq.most_common(50):
        print(f"  {c:>4}  {w}")

    if args.full:
        print()
        print("=== PER-PAGE FIRST-LINE PREVIEWS (handle with care) ===")
        for i, text in enumerate(pages, 1):
            first_line = next((l.strip() for l in text.splitlines() if l.strip()), "")
            print(f"  pg {i:>3}: {first_line[:90]}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
