#!/usr/bin/env python3
"""Extract candidate demand signals from existing proposal analysis artifacts.

The requirement and capability matrices already in this workspace are a record of customers
telling us what they need — including, in the Gap/Risk columns, an honest account of what we
could not answer. This script harvests those rows mechanically into candidate demand signals
so the register can be seeded from real pipeline history instead of starting empty.

It is deliberately a FIRST PASS, not the final word:

  * capability_theme is only SUGGESTED, by keyword match against reference/capability-themes.md.
    A human or /capture-demand-signals confirms or corrects it before the record is appended
    to signals/demand-signals.jsonl.
  * our_status is inferred from the gap/coverage prose and may be wrong; 'unknown' is emitted
    when the prose does not support an inference.
  * Mechanical submission requirements (cover pages, page limits, POC blocks) are dropped.
    They are not demand signals and telling engineering about them wastes the channel.

Reads:
  proposals/<slug>/working/requirement-matrix.md    scored + implied requirements, Gap/Risk column
  proposals/<slug>/working/capability-matrix.md     capability coverage + gap tables
  proposals/<slug>/working/proposal-type.md         display_name, for the program field

Writes:
  signals/candidates/<date>-candidates.jsonl        candidate records for confirmation

Usage:
  python scripts/extract-demand-signals.py --all
  python scripts/extract-demand-signals.py --proposal dia-dma-frontier-llm
  python scripts/extract-demand-signals.py --all --stats-only
  python scripts/extract-demand-signals.py --selftest

Exit codes:
  0 = candidates written (or selftest passed)
  1 = no candidates found
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
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))
import demand_signal_core as core  # noqa: E402  (needs WORKSPACE_ROOT on the path first)

# The mechanics rule is shared with the capture-pipeline ingest so the two
# cannot drift about what belongs in the register. Cross-checking them is
# what surfaced `address` matching the verb rather than a mailing address.
MECHANICAL_PATTERNS = core.MECHANICAL_PATTERNS

# ---------------------------------------------------------------------------
# Column identification. Matrix headers vary across 40 proposals; match on
# substrings rather than demanding one canonical header row.
# ---------------------------------------------------------------------------

REQUIREMENT_HEADERS = (
    "requirement", "criterion", "outcome", "exemplar effect", "needed capability",
    "objective", "question", "capability needed", "threat phase", "gap",
)
# Columns that carry the honest assessment of whether we can do it.
GAP_HEADERS = ("gap", "risk", "delta", "coverage", "notes", "severity", "build notes")
STRENGTH_HEADERS = ("explicit", "exp/imp", "requirement type", "type")
SOURCE_HEADERS = ("source", "where")
ID_HEADERS = ("id", "#", "req id")

# Rows that are submission mechanics, not capability demand.

# Rows that are our own internal framing rather than a customer ask. These appear
# mostly in capability matrices, which mix "what they want" with "how we will pitch it."
INTERNAL_FRAMING = re.compile(
    r"^(why\b|problem framing|bid scope|win theme|discriminator|ghost|so what|"
    r"sf-\d+|tr-\d+\b|theme\b|narrative|graphic|figure \d|section \d|"
    r"state (current )?trl|trl,? mrl|proposal|response|volume \d)",
    re.IGNORECASE,
)
# A row whose "requirement" is only a heading number or a bare label carries no ask.
BARE_LABEL = re.compile(r"^[\d.\s]+$|^\**[\d.]+\**\s*[-–—]?\s*$")

# ---------------------------------------------------------------------------
# Theme suggestion. Keyword lists are intentionally narrow: a miss produces
# theme_suggestion=null (a human classifies it), which is far cheaper than a
# confident wrong theme silently polluting the leaderboard.
# ---------------------------------------------------------------------------

def load_valid_themes() -> list[str]:
    """Delegate to the shared core so the vocabulary has exactly one reader."""
    try:
        return core.load_valid_themes()
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)


def suggest_theme(text: str, valid: list[str]) -> tuple[str | None, int]:
    """Delegate to the shared core (see demand_signal_core.THEME_KEYWORDS)."""
    return core.suggest_theme(text, valid)


# ---------------------------------------------------------------------------
# Markdown pipe-table parsing
# ---------------------------------------------------------------------------

def split_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def is_divider(line: str) -> bool:
    return bool(re.match(r"^\|[\s:|-]+\|?\s*$", line.strip()))


def parse_tables(md: str) -> list[tuple[list[str], list[list[str]]]]:
    """Return [(header_cells, [row_cells, ...]), ...] for every pipe table in the document."""
    tables: list[tuple[list[str], list[list[str]]]] = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < len(lines) and is_divider(lines[i + 1]):
            header = split_row(line)
            rows: list[list[str]] = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not is_divider(lines[i]):
                    rows.append(split_row(lines[i]))
                i += 1
            if rows:
                tables.append((header, rows))
            continue
        i += 1
    return tables


def find_column(header: list[str], candidates: tuple[str, ...], exclude: set[int] | None = None) -> int | None:
    exclude = exclude or set()
    for idx, cell in enumerate(header):
        if idx in exclude:
            continue
        low = cell.lower()
        for cand in candidates:
            if cand in low:
                return idx
    return None


# ---------------------------------------------------------------------------
# Field inference
# ---------------------------------------------------------------------------

STATUS_SHIPPING = re.compile(
    r"\b(no gap|none\b|no risk|proven|already|deployed|fielded|full coverage|"
    r"strong\b|complete\b|covered\b)", re.IGNORECASE,
)
STATUS_GAP = re.compile(
    r"(^\W*gap\b|\b(full gap|complete gap|entirely outside|no capability|"
    r"does not (build|have|exist)|not develop|not built|not validated|"
    r"requires? a .*partner|teaming (partner|required)|decline))",
    re.IGNORECASE,
)
STATUS_PROTOTYPE = re.compile(
    r"\b(partial|prototype|trl ?[1-7]\b|in progress|adaptation|extension|claimed extension|"
    r"not demonstrated|not productiz|path, not|research|crada)", re.IGNORECASE,
)


# Short cells are grades, not prose. A grade word carries MAGNITUDE, not goodness: "HIGH"
# means a big number of whatever the column measures. Under a Coverage heading a big number
# means we have the capability; under a Gap Severity heading the same word means we do not.
# Polarity therefore comes from the header. A few words (green, red) are inherently polar
# and are read directly.
GRADE_MAG_LARGE = re.compile(r"^\W*(strong|full|complete|high|critical|severe|direct hit)\W*$", re.IGNORECASE)
GRADE_MAG_MID = re.compile(r"^\W*(partial|medium|moderate|yellow|some|adjacent)\W*$", re.IGNORECASE)
GRADE_MAG_SMALL = re.compile(r"^\W*(none|no|low|minimal|absent|missing|n/?a)\W*$", re.IGNORECASE)
GRADE_POLAR_GOOD = re.compile(r"^\W*(green|yes|covered)\W*$", re.IGNORECASE)
GRADE_POLAR_BAD = re.compile(r"^\W*(red|blocker)\W*$", re.IGNORECASE)


def column_polarity(header_cell: str, column_values: list[str]) -> str:
    """Decide whether a column measures what we HAVE ('coverage') or what is MISSING ('gap').

    The header is the first signal, but it lies often enough to matter: several matrices head a
    column "Gap / Risk" and then fill it with coverage grades ("Full", "Strong"). Reading that
    column with gap polarity inverts every row in the table — a fully covered requirement
    becomes a top-priority gap, and the real gap in the same column reads as unknown. So when
    the values themselves look like coverage grades, the values win.
    """
    header_low = header_cell.lower()
    header_says_gap = any(w in header_low for w in ("gap", "risk", "severity", "delta", "missing"))
    header_says_coverage = any(w in header_low for w in ("coverage", "contribution"))

    grades_large = grades_small = graded = 0
    for raw in column_values:
        cleaned = re.sub(r"[*`]", "", raw or "").strip()
        if not cleaned or len(cleaned.split()) > 3:
            continue
        if GRADE_MAG_LARGE.search(cleaned):
            grades_large += 1
            graded += 1
        elif GRADE_MAG_SMALL.search(cleaned) or GRADE_MAG_MID.search(cleaned):
            grades_small += 1
            graded += 1

    # "Full" / "Strong" repeated down a gap-headed column is a coverage grade, not a claim that
    # the gap is total. Nobody documents a table where most requirements are complete failures.
    if header_says_gap and graded >= 3 and grades_large > grades_small:
        return "coverage"
    if header_says_gap:
        return "gap"
    if header_says_coverage:
        return "coverage"
    return "gap"


def infer_status(gap_text: str, polarity: str = "gap") -> str:
    """Infer BD's status from the gap/coverage cell. Polarity comes from column_polarity()."""
    if not gap_text:
        return "unknown"
    cleaned = re.sub(r"[*`]", "", gap_text).strip()
    if not cleaned or cleaned in {"-", "–", "—", "N/A", "n/a", "TBD"}:
        return "unknown"

    if len(cleaned.split()) <= 3:
        if GRADE_POLAR_GOOD.search(cleaned):
            return "shipping"
        if GRADE_POLAR_BAD.search(cleaned):
            return "gap"
        if GRADE_MAG_MID.search(cleaned):
            return "prototype"
        large = bool(GRADE_MAG_LARGE.search(cleaned))
        small = bool(GRADE_MAG_SMALL.search(cleaned))
        if large or small:
            if polarity == "coverage":
                return "shipping" if large else "gap"
            return "gap" if large else "shipping"

    if STATUS_GAP.search(cleaned):
        return "gap"
    if STATUS_PROTOTYPE.search(cleaned):
        return "prototype"
    if STATUS_SHIPPING.search(cleaned):
        return "shipping"
    return "unknown"


def infer_strength(strength_text: str, source_text: str) -> str:
    low = f"{strength_text} {source_text}".lower()
    if "pass/fail" in low or "pass-fail" in low or "threshold" in low:
        return "mandatory-passfail"
    if "rubric" in low or re.search(r"\d+\s?%", low):
        return "mandatory-scored"
    if "implicit" in low or "implied" in low or "desired" in low:
        return "desired"
    if "explicit" in low:
        return "mandatory-scored"
    return "desired"


def extract_weight(text: str) -> float | None:
    m = re.search(r"(\d{1,3}(?:\.\d)?)\s?%", text)
    if m:
        val = float(m.group(1))
        if 0 < val <= 100:
            return val
    return None


def read_program(slug_dir: Path) -> str | None:
    ptype = slug_dir / "working" / "proposal-type.md"
    if ptype.exists():
        for line in ptype.read_text(encoding="utf-8", errors="replace").splitlines()[:25]:
            m = re.match(r"^display_name:\s*(.+?)\s*$", line)
            if m:
                return m.group(1)
    return None


def read_matrix_title(path: Path) -> str | None:
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:5]:
        m = re.match(r"^#\s+(.*)", line)
        if m:
            return m.group(1).strip()
    return None


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

# requirement-matrix.md is the high-precision source: one row per customer ask, with an
# honest Gap/Risk column. capability-matrix.md is opt-in because it interleaves customer
# asks with our own pitch framing, and a register that shows engineering our win themes
# instead of their requirements loses the audience on the first read.
PRIMARY_SOURCE = "requirement-matrix.md"
SECONDARY_SOURCE = "capability-matrix.md"


def extract_from_proposal(slug_dir: Path, valid_themes: list[str], include_capability: bool = False) -> list[dict]:
    candidates: list[dict] = []
    program = read_program(slug_dir)
    source_files = [PRIMARY_SOURCE] + ([SECONDARY_SOURCE] if include_capability else [])
    for fname in source_files:
        path = slug_dir / "working" / fname
        if not path.exists():
            continue
        md = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(WORKSPACE_ROOT).as_posix()
        for header, rows in parse_tables(md):
            req_idx = find_column(header, REQUIREMENT_HEADERS)
            if req_idx is None:
                continue
            gap_idx = find_column(header, GAP_HEADERS, exclude={req_idx})
            strength_idx = find_column(header, STRENGTH_HEADERS, exclude={req_idx, gap_idx or -1})
            source_idx = find_column(header, SOURCE_HEADERS, exclude={req_idx})
            id_idx = find_column(header, ID_HEADERS)
            # Polarity is a property of the TABLE, decided once from the whole column, not
            # re-guessed per row from the header alone.
            gap_header = header[gap_idx] if gap_idx is not None and len(header) > gap_idx else ""
            polarity = column_polarity(
                gap_header,
                [r[gap_idx] for r in rows if gap_idx is not None and len(r) > gap_idx],
            ) if gap_idx is not None else "gap"
            for row in rows:
                if len(row) <= req_idx:
                    continue
                requirement = re.sub(r"\*\*|`", "", row[req_idx]).strip()
                if len(requirement) < 12:
                    continue
                if MECHANICAL_PATTERNS.search(requirement):
                    continue
                if INTERNAL_FRAMING.match(requirement) or BARE_LABEL.match(requirement):
                    continue
                gap_text = row[gap_idx].strip() if gap_idx is not None and len(row) > gap_idx else ""
                strength_text = row[strength_idx] if strength_idx is not None and len(row) > strength_idx else ""
                source_text = row[source_idx] if source_idx is not None and len(row) > source_idx else ""
                row_id = row[id_idx].strip() if id_idx is not None and len(row) > id_idx else ""
                # Theme suggestion sees the requirement plus the response prose, which
                # often names the capability more explicitly than the requirement does.
                theme, hits = suggest_theme(" ".join(row), valid_themes)
                anchor = f"#{re.sub(r'[^A-Za-z0-9-]', '', row_id)}" if row_id else ""
                candidates.append({
                    "proposal_slug": slug_dir.name,
                    "program": program,
                    "source_file": fname,
                    "source_ref": f"{rel}{anchor}",
                    "row_id": row_id or None,
                    "requirement": requirement,
                    "gap_text": gap_text or None,
                    "theme_suggestion": theme,
                    "theme_confidence": hits,
                    "our_status_inferred": infer_status(gap_text, polarity),
                    "demand_strength_inferred": infer_strength(strength_text, source_text),
                    "rubric_weight_pct": extract_weight(f"{source_text} {strength_text}"),
                })
    return candidates


def dedupe(candidates: list[dict]) -> list[dict]:
    """Requirement and capability matrices restate the same ask; keep the richer row."""
    seen: dict[tuple[str, str], dict] = {}
    for cand in candidates:
        key = (cand["proposal_slug"], re.sub(r"\W+", "", cand["requirement"].lower())[:80])
        prior = seen.get(key)
        if prior is None:
            seen[key] = cand
            continue
        score = (bool(cand["gap_text"]), cand["theme_confidence"])
        prior_score = (bool(prior["gap_text"]), prior["theme_confidence"])
        if score > prior_score:
            seen[key] = cand
    return list(seen.values())


def print_stats(candidates: list[dict]) -> None:
    by_theme: dict[str, int] = {}
    unclassified = 0
    for c in candidates:
        if c["theme_suggestion"]:
            by_theme[c["theme_suggestion"]] = by_theme.get(c["theme_suggestion"], 0) + 1
        else:
            unclassified += 1
    print(f"\nCandidates: {len(candidates)}  ({unclassified} need human classification)")
    print(f"Proposals contributing: {len({c['proposal_slug'] for c in candidates})}")
    status_counts: dict[str, int] = {}
    for c in candidates:
        status_counts[c["our_status_inferred"]] = status_counts.get(c["our_status_inferred"], 0) + 1
    print("Inferred status: " + ", ".join(f"{k}={v}" for k, v in sorted(status_counts.items())))
    print("\nSuggested themes by frequency:")
    for theme, count in sorted(by_theme.items(), key=lambda kv: -kv[1]):
        print(f"  {count:>3}  {theme}")


def selftest() -> int:
    valid = load_valid_themes()
    md = """
# Requirement Matrix — Selftest

| ID | Requirement | Source | Exp/Imp | Response Approach | Gap/Risk |
|---|---|---|---|---|---|
| R1 | Operate fully air-gapped with no connectivity | LOE1; Rubric 10% | Explicit | On-device runtime | No gap — proven capability |
| R2 | Support progressive model upgrades across the air gap | LOE1-o4 | Explicit | Model registry | Full gap — no concrete mechanism |
| R3 | Cover page with Company Name, Address, POC | Instructions | Explicit | Standard block | None |
| R4 | Conduct an autonomous rigging operation | Question 2 | Explicit | Decline | Full gap — entirely outside our product line |
"""
    tables = parse_tables(md)
    assert len(tables) == 1, f"expected 1 table, got {len(tables)}"
    header, rows = tables[0]
    assert len(rows) == 4, f"expected 4 rows, got {len(rows)}"

    req_idx = find_column(header, REQUIREMENT_HEADERS)
    assert req_idx == 1, f"requirement column should be 1, got {req_idx}"
    gap_idx = find_column(header, GAP_HEADERS, exclude={req_idx})
    assert gap_idx == 5, f"gap column should be 5, got {gap_idx}"

    assert MECHANICAL_PATTERNS.search("Cover page with Company Name, Address, POC")
    assert not MECHANICAL_PATTERNS.search("Operate fully air-gapped with no connectivity")
    assert INTERNAL_FRAMING.match("Why visualization UI — dynamic priority bars")
    assert INTERNAL_FRAMING.match("Problem framing — theater context")
    assert not INTERNAL_FRAMING.match("Operate fully air-gapped with no connectivity")
    assert BARE_LABEL.match("**5.1.2.2**")
    assert not BARE_LABEL.match("5.1.2.2 Secure software distribution")

    assert infer_status("No gap — proven capability") == "shipping"
    assert infer_status("Full gap — no concrete mechanism") == "gap"
    assert infer_status("Partial — TRL 6 prototype") == "prototype"
    assert infer_status("") == "unknown"
    assert infer_status("—") == "unknown"
    # Polarity: the same magnitude word inverts with the column heading.
    for cell, header, expected in [
        ("Strong", "Coverage", "shipping"),
        ("Strong", "Gap/Risk", "gap"),
        ("**HIGH**", "Gap", "gap"),
        ("**CRITICAL**", "Gap / Team Coverage Needed", "gap"),
        ("None", "Coverage", "gap"),
        ("None", "Gap/Risk", "shipping"),
        ("Partial", "Coverage", "prototype"),
        ("Partial", "Gap", "prototype"),
        ("🟡 Partial", "Coverage", "prototype"),
        ("Green", "Gap/Risk", "shipping"),
        ("Red", "Coverage", "gap"),
        ("**Gap** - sustained session not validated; 2-week sprint", "Gap/Risk", "gap"),
    ]:
        polarity = "coverage" if header.lower().startswith("coverage") else "gap"
        got = infer_status(cell, polarity)
        assert got == expected, f"infer_status({cell!r}, {polarity!r}) = {got}, expected {expected}"

    # Column polarity comes from the header UNLESS the values contradict it.
    assert column_polarity("Coverage", ["Full", "Partial", "Full"]) == "coverage"
    assert column_polarity("Gap / Risk", ["Medium - 2 weeks", "HIGH", "CRITICAL"]) == "gap"
    assert column_polarity("Gap / Team Coverage Needed", ["prose here", "more prose"]) == "gap"
    # The real-world inversion this guards: a "Gap / Risk" column filled with coverage grades.
    # Read with gap polarity it inverts every row in the table.
    assert column_polarity(
        "Gap / Risk", ["Full", "Full", "Full", "Full", "Gap - not validated"]
    ) == "coverage", "a gap-headed column full of 'Full' grades is really a coverage column"

    assert infer_strength("Explicit", "LOE1; Rubric 10%") == "mandatory-scored"
    assert infer_strength("Implicit", "Problem statement") == "desired"
    assert extract_weight("Rubric Air-Gapped 10%") == 10.0
    assert extract_weight("no percentage here") is None

    t1, _ = suggest_theme("Operate fully air-gapped with no connectivity on-device runtime", valid)
    assert t1 == "air-gap-ddil-deployment", f"got {t1}"
    t2, _ = suggest_theme("Support progressive model upgrades across the air gap", valid)
    assert t2 in {"cross-domain-model-update", "air-gap-ddil-deployment"}, f"got {t2}"
    # Rigging now classifies — vocabulary v2 added robotic-autonomy-control for exactly this.
    t3, _ = suggest_theme("Conduct an autonomous rigging operation with a robotic arm", valid)
    assert t3 == "robotic-autonomy-control", f"got {t3}"
    # Text with no capability content at all must stay unclassified rather than be guessed.
    t4, _ = suggest_theme("Submissions will be accepted until the announced closing time", valid)
    assert t4 is None, f"content-free text should not be classified, got {t4}"

    deduped = dedupe([
        {"proposal_slug": "x", "requirement": "Operate air-gapped", "gap_text": None, "theme_confidence": 1},
        {"proposal_slug": "x", "requirement": "Operate air-gapped", "gap_text": "Full gap", "theme_confidence": 1},
    ])
    assert len(deduped) == 1 and deduped[0]["gap_text"] == "Full gap", "dedupe should keep the richer row"

    print(f"SELFTEST PASS — {len(valid)} themes loaded, table parse + inference + dedupe verified")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--proposal", help="single proposal slug")
    group.add_argument("--all", action="store_true", help="every proposal in proposals/")
    parser.add_argument("--stats-only", action="store_true", help="print the summary without writing candidates")
    parser.add_argument(
        "--include-capability-matrix", action="store_true",
        help="also harvest working/capability-matrix.md (lower precision — mixes customer asks with our own pitch framing)",
    )
    parser.add_argument("--out", help="output path (default signals/candidates/<today>-candidates.jsonl)")
    parser.add_argument("--selftest", action="store_true", help="run the embedded deterministic self-test")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if not args.proposal and not args.all:
        parser.error("--proposal <slug> or --all is required (or use --selftest)")

    valid_themes = load_valid_themes()
    proposals_root = WORKSPACE_ROOT / "proposals"
    if args.proposal:
        slug_dirs = [proposals_root / args.proposal]
        if not slug_dirs[0].is_dir():
            print(f"ERROR: no such proposal: {args.proposal}", file=sys.stderr)
            return 2
    else:
        slug_dirs = sorted(d for d in proposals_root.iterdir() if d.is_dir() and not d.name.startswith("_"))

    candidates: list[dict] = []
    for slug_dir in slug_dirs:
        candidates.extend(extract_from_proposal(slug_dir, valid_themes, args.include_capability_matrix))
    candidates = dedupe(candidates)
    candidates.sort(key=lambda c: (c["proposal_slug"], c["source_file"], c["row_id"] or ""))

    if not candidates:
        print("No candidate signals found.", file=sys.stderr)
        return 1

    print_stats(candidates)

    if args.stats_only:
        return 0

    out_path = Path(args.out) if args.out else (
        WORKSPACE_ROOT / "signals" / "candidates" / f"{date.today().isoformat()}-candidates.jsonl"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for cand in candidates:
            fh.write(json.dumps(cand, ensure_ascii=False) + "\n")
    try:
        shown = out_path.relative_to(WORKSPACE_ROOT).as_posix()
    except ValueError:
        shown = str(out_path)
    print(f"\nWrote {len(candidates)} candidates -> {shown}")
    print("Next: confirm themes and status, then append confirmed records to signals/demand-signals.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
