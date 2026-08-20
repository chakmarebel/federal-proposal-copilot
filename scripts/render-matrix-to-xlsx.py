#!/usr/bin/env python3
"""
render-matrix-to-xlsx.py — Render any matrix-style markdown to a formatted Excel workbook.

Matrices (capability, requirement, risk, traceability) are working tables: reviewers sort,
filter, add a column, and hand them back. Word cannot do any of that. This is the general
renderer for those artifacts, the .xlsx counterpart to scripts/render-md-to-docx.py.

Each markdown heading that contains one or more pipe tables becomes a worksheet. Prose under
those headings is preserved on a final "Notes" sheet, so nothing is lost in translation.
Verdict cells (green/yellow/red markers, or words like Gap / Covered / Major) are colour-coded,
header rows are frozen and filterable, and column widths are content-proportional.

Usage:
    python scripts/render-matrix-to-xlsx.py proposals/<slug>/working/capability-matrix.md
    python scripts/render-matrix-to-xlsx.py --proposal <slug>            # all matrices
    python scripts/render-matrix-to-xlsx.py --proposal <slug> --out-dir final/xlsx
    python scripts/render-matrix-to-xlsx.py --selftest

By default the .xlsx lands beside the .md, matching render-md-to-docx.py's behaviour. The .md
stays the source of truth; the .xlsx is a derived artifact.
"""

import argparse
import io
import re
import sys
import tempfile
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("ERROR: openpyxl not installed. Run: pip install openpyxl", file=sys.stderr)
    sys.exit(1)

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

# Matrix artifacts --proposal / --all pick up. Glob patterns, so naming variants are caught
# (requirement-matrix / requirements-matrix, pp-relevance-matrix, capability-matrix-webai).
MATRIX_GLOBS = [
    "working/*matrix*.md",
    "working/assumptions-and-risks.md",
    "working/storyboard-coverage-map.md",
]

# Files matching a matrix glob that are prose, not tables. build_workbook() already skips
# anything with no tables, so this list is only to keep the sweep output quiet.
NOT_A_MATRIX = {"webai-matrix-cover-note.md"}

# compliance-matrix.md has a dedicated renderer that produces a richer workbook
# (Matrix / Summary / Gaps / By-Section sheets with status roll-ups). Defer to it rather
# than flattening the matrix generically.
DEFER_TO_SPECIALIST = {
    "compliance-matrix.md": "python tools/compliance_to_xlsx.py --proposal <slug>",
}

# Stamped into every workbook this tool writes. An .xlsx without it was hand-built or produced
# by another tool, and is never overwritten — not even under --force. This guard exists because
# a --force sweep destroyed four hand-curated workbooks on 2026-08-20; two were recoverable via
# their specialist tool, two were not.
PROVENANCE = "render-matrix-to-xlsx"

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY, LIGHT_BLUE, WHITE = "1F3864", "DCE6F1", "FFFFFF"
GREEN_BG, YELLOW_BG, RED_BG, GREY_BG = "C6EFCE", "FFEB9C", "FFC7CE", "E0E0E0"
GREEN_FG, YELLOW_FG, RED_FG, GREY_FG = "276221", "7D6608", "9C0006", "444444"

HEADER_FONT = Font(name="Calibri", bold=True, color=WHITE, size=10)
BODY_FONT = Font(name="Calibri", size=10)
TITLE_FONT = Font(name="Calibri", bold=True, size=13, color=NAVY)
SUBTITLE_FONT = Font(name="Calibri", italic=True, size=10, color="595959")
HEADER_FILL = PatternFill("solid", fgColor=NAVY)
ALT_FILL = PatternFill("solid", fgColor=LIGHT_BLUE)

WRAP = Alignment(wrap_text=True, vertical="top")
WRAP_CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")

# Verdict vocabulary. Order matters — first match wins, so specific before generic.
VERDICT_RULES = [
    (GREEN_BG, GREEN_FG, ["🟢", "strong", "covered", "green", "complete", "yes", "low"]),
    (YELLOW_BG, YELLOW_FG, ["🟡", "partial", "yellow", "moderate", "medium", "planned",
                            "drafted", "open item", "unconfirmed", "hold"]),
    (RED_BG, RED_FG, ["🔴", "gap", "red", "major", "fatal", "severe", "high",
                      "blocker", "missing", "no bid", "disqualifying"]),
    (GREY_BG, GREY_FG, ["n/a", "exception", "not applicable", "—", "-"]),
]

# A column is treated as a verdict column only if its header says so. This keeps a
# "Requirement" cell that happens to contain the word "high" from being painted red.
VERDICT_HEADER_PAT = re.compile(
    r"verdict|status|coverage|gap|risk|rating|severity|likelihood|impact|signal|score|"
    r"maturity|priority|e/i|assessment",
    re.I,
)

MAX_COL_WIDTH, MIN_COL_WIDTH = 62, 8
MAX_SHEET_NAME = 31
ILLEGAL_SHEET_CHARS = re.compile(r"[\[\]:*?/\\]")


def thin_border():
    s = Side(style="thin", color="BFBFBF")
    return Border(left=s, right=s, top=s, bottom=s)


# ── Markdown parsing ─────────────────────────────────────────────────────────
def split_row(line):
    """Split a markdown table row into cells, honouring \\| escapes."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    parts, buf, esc = [], "", False
    for ch in line:
        if esc:
            buf += ch
            esc = False
        elif ch == "\\":
            esc = True
        elif ch == "|":
            parts.append(buf.strip())
            buf = ""
        else:
            buf += ch
    parts.append(buf.strip())
    return parts


def is_separator(line):
    s = line.strip().strip("|")
    return bool(s) and all(c in " -:|" for c in s) and "-" in s


def clean_cell(text):
    """Strip markdown inline syntax that Excel cannot render."""
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)   # links → label
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)          # bold
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)  # italic
    text = re.sub(r"`([^`]+)`", r"\1", text)                # code
    text = text.replace("<br>", "\n").replace("<br/>", "\n")
    return text.strip()


def parse_markdown(text):
    """
    Parse into [{'heading', 'level', 'tables': [[row, ...], ...], 'prose': [str, ...]}].
    A section is opened by any heading; tables and prose accumulate under the current one.
    """
    sections = []
    current = {"heading": None, "level": 0, "tables": [], "prose": []}
    lines = text.splitlines()
    i = 0
    in_code = False

    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            current["prose"].append(line)
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            if current["heading"] is not None or current["tables"] or current["prose"]:
                sections.append(current)
            current = {"heading": clean_cell(m.group(2)), "level": len(m.group(1)),
                       "tables": [], "prose": []}
            i += 1
            continue

        # A table needs a header row followed by a separator row.
        if "|" in line and i + 1 < len(lines) and is_separator(lines[i + 1]):
            header = split_row(line)
            rows = [[clean_cell(c) for c in header]]
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append([clean_cell(c) for c in split_row(lines[i])])
                i += 1
            width = len(rows[0])
            rows = [r[:width] + [""] * (width - len(r)) for r in rows]
            current["tables"].append(rows)
            continue

        current["prose"].append(line)
        i += 1

    if current["heading"] is not None or current["tables"] or current["prose"]:
        sections.append(current)
    return sections


# ── Formatting ────────────────────────────────────────────────────────────────
def verdict_style(value):
    """Return (fill, font) for a verdict cell, or (None, None) if nothing matches."""
    v = value.strip().lower()
    if not v:
        return None, None
    for bg, fg, tokens in VERDICT_RULES:
        for tok in tokens:
            # Symbols match anywhere; words must match as whole words.
            if not tok.isalpha() and tok in v:
                return PatternFill("solid", fgColor=bg), Font(name="Calibri", size=10, color=fg)
            if tok.isalpha() and re.search(rf"\b{re.escape(tok)}\b", v):
                return PatternFill("solid", fgColor=bg), Font(name="Calibri", size=10, color=fg)
    return None, None


def sheet_name(raw, used):
    """Excel-safe, unique, ≤31 chars."""
    name = ILLEGAL_SHEET_CHARS.sub("-", raw or "Sheet").strip() or "Sheet"
    # Drop "A. " / "3. " section prefixes — sheet order already conveys sequence, and the
    # prefix spends characters from a 31-char budget. Strip all of them or none, never some.
    name = re.sub(r"^[A-Za-z0-9]{1,2}\.\s+", "", name)
    name = name[:MAX_SHEET_NAME]
    base, n = name, 2
    while name.lower() in used:
        suffix = f" ({n})"
        name = base[: MAX_SHEET_NAME - len(suffix)] + suffix
        n += 1
    used.add(name.lower())
    return name


def compute_widths(rows):
    """Content-proportional widths, capped so one long cell cannot blow out the sheet."""
    widths = []
    for col in range(len(rows[0])):
        lengths = []
        for r in rows:
            cell = r[col] if col < len(r) else ""
            for seg in str(cell).split("\n"):
                lengths.append(len(seg))
        if not lengths:
            widths.append(MIN_COL_WIDTH)
            continue
        longest = max(lengths)
        # Use a high percentile rather than the max so a single outlier does not dominate.
        ordered = sorted(lengths)
        p85 = ordered[int(len(ordered) * 0.85)] if len(ordered) > 3 else longest
        width = max(MIN_COL_WIDTH, min(MAX_COL_WIDTH, int(max(p85 * 1.15, longest * 0.5)) + 2))
        widths.append(width)
    return widths


def write_table(ws, rows, start_row, title=None):
    """Write one table. Returns the next free row."""
    r = start_row
    if title:
        c = ws.cell(row=r, column=1, value=title)
        c.font = Font(name="Calibri", bold=True, size=11, color=NAVY)
        r += 2

    header = rows[0]
    verdict_cols = {i for i, h in enumerate(header) if VERDICT_HEADER_PAT.search(h or "")}
    border = thin_border()

    for i, val in enumerate(header):
        c = ws.cell(row=r, column=i + 1, value=val)
        c.font, c.fill, c.alignment, c.border = HEADER_FONT, HEADER_FILL, WRAP_CENTER, border
    header_row = r
    r += 1

    for n, row in enumerate(rows[1:]):
        for i, val in enumerate(row):
            c = ws.cell(row=r, column=i + 1, value=val)
            c.font, c.alignment, c.border = BODY_FONT, WRAP, border
            styled = False
            if i in verdict_cols:
                fill, font = verdict_style(val)
                if fill:
                    c.fill, c.font, c.alignment = fill, font, WRAP_CENTER
                    styled = True
            if not styled and n % 2 == 1:
                c.fill = ALT_FILL
        r += 1

    for i, w in enumerate(compute_widths(rows)):
        letter = get_column_letter(i + 1)
        if ws.column_dimensions[letter].width in (None, 0):
            ws.column_dimensions[letter].width = w
        else:
            ws.column_dimensions[letter].width = max(ws.column_dimensions[letter].width, w)

    # Filter + freeze only for the first table on a sheet; multiple ranges are not supported.
    if start_row <= 3:
        last_col = get_column_letter(len(header))
        ws.auto_filter.ref = f"A{header_row}:{last_col}{r - 1}"
        ws.freeze_panes = ws.cell(row=header_row + 1, column=1)

    return r + 2


def build_workbook(md_path, out_path):
    text = Path(md_path).read_text(encoding="utf-8")
    sections = parse_markdown(text)

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    used, notes = set(), []
    doc_title = next((s["heading"] for s in sections if s["level"] == 1 and s["heading"]),
                     Path(md_path).stem)

    for sec in sections:
        prose = "\n".join(sec["prose"]).strip()
        if not sec["tables"]:
            if prose:
                notes.append((sec["heading"] or doc_title, prose))
            continue

        ws = wb.create_sheet(sheet_name(sec["heading"] or doc_title, used))
        row = 1
        if sec["heading"]:
            c = ws.cell(row=1, column=1, value=sec["heading"])
            c.font = TITLE_FONT
            row = 3

        for n, table in enumerate(sec["tables"]):
            row = write_table(ws, table, row,
                              title=None if n == 0 else f"Table {n + 1}")

        if prose:
            notes.append((sec["heading"] or doc_title, prose))

    if notes:
        ws = wb.create_sheet(sheet_name("Notes", used))
        ws.column_dimensions["A"].width = 118
        c = ws.cell(row=1, column=1, value=f"{doc_title} — narrative notes")
        c.font = TITLE_FONT
        c2 = ws.cell(row=2, column=1,
                     value="Prose from the source markdown, preserved so the workbook carries "
                           "the full artifact. Source of truth: " + Path(md_path).name)
        c2.font = SUBTITLE_FONT
        r = 4
        for heading, body in notes:
            h = ws.cell(row=r, column=1, value=heading)
            h.font = Font(name="Calibri", bold=True, size=11, color=NAVY)
            r += 1
            b = ws.cell(row=r, column=1, value=body.strip())
            b.font, b.alignment = BODY_FONT, WRAP
            ws.row_dimensions[r].height = min(400, 15 * (body.count("\n") + 2))
            r += 2

    if not wb.sheetnames:
        return False, "no tables found"

    wb.properties.creator = PROVENANCE
    wb.properties.description = (
        f"Generated by {PROVENANCE} from {Path(md_path).name}. "
        "The markdown is the source of truth; edits made here are not written back."
    )

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    return True, f"{len(wb.sheetnames)} sheet(s)"


def is_ours(path):
    """True if this .xlsx was generated by this tool (safe to overwrite)."""
    try:
        wb = openpyxl.load_workbook(path)
        return (wb.properties.creator or "") == PROVENANCE
    except Exception:                                           # noqa: BLE001
        return False


# ── Selftest ──────────────────────────────────────────────────────────────────
SELFTEST_MD = """# Test Matrix

Intro prose that belongs on the Notes sheet.

## A. First block

| Req | Requirement | Verdict |
|---|---|---|
| R-01 | Something with a high bar in the text | 🟢 |
| R-02 | Another | 🔴 Gap |
| R-03 | Third `code` and **bold** | 🟡 Partial |

## Gaps

### G-1 — a gap
Narrative only, no table here.
"""


def selftest():
    ok = True

    def check(label, cond):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond

    print("render-matrix-to-xlsx selftest")

    secs = parse_markdown(SELFTEST_MD)
    check("parses 4 sections", len(secs) == 4)
    tbl = secs[1]["tables"][0]
    check("table has header + 3 rows", len(tbl) == 4)
    check("strips inline markdown", tbl[3][1] == "Third code and bold")

    check("green verdict styled", verdict_style("🟢")[0] is not None)
    check("red verdict styled", verdict_style("🔴 Gap")[0].fgColor.rgb.endswith(RED_BG))
    check("yellow verdict styled", verdict_style("🟡 Partial")[0].fgColor.rgb.endswith(YELLOW_BG))
    check("empty verdict unstyled", verdict_style("")[0] is None)
    check("verdict header detected", bool(VERDICT_HEADER_PAT.search("Verdict")))
    check("prose column not a verdict column", not VERDICT_HEADER_PAT.search("Requirement"))

    check("sheet name truncated", len(sheet_name("x" * 60, set())) <= MAX_SHEET_NAME)
    u = set()
    sheet_name("Dup", u)
    check("duplicate sheet names disambiguated", sheet_name("Dup", u) != "Dup")
    check("illegal chars replaced", "/" not in sheet_name("a/b:c", set()))
    check("escaped pipe preserved", split_row(r"| a \| b | c |") == ["a | b", "c"])

    with tempfile.TemporaryDirectory() as td:
        md = Path(td) / "t.md"
        md.write_text(SELFTEST_MD, encoding="utf-8")
        out = Path(td) / "t.xlsx"
        built, msg = build_workbook(md, out)
        check("workbook written", built and out.exists())
        wb = openpyxl.load_workbook(out)
        check("table sheet + notes sheet created", len(wb.sheetnames) == 2)
        ws = wb[wb.sheetnames[0]]
        check("header frozen", ws.freeze_panes is not None)
        check("autofilter set", ws.auto_filter.ref is not None)
        check("notes sheet carries prose",
              "Narrative only" in str(wb[wb.sheetnames[-1]]["A"][-1].value or "")
              or any("Narrative only" in str(c.value or "")
                     for c in wb[wb.sheetnames[-1]]["A"]))

        # Provenance guard — the protection against clobbering hand-built workbooks.
        check("generated workbook is recognised as ours", is_ours(out))
        foreign = Path(td) / "foreign.xlsx"
        fwb = openpyxl.Workbook()
        fwb.active["A1"] = "hand-built"
        fwb.save(foreign)
        check("hand-built workbook is not claimed as ours", not is_ours(foreign))
        check("unreadable file is not claimed as ours",
              not is_ours(Path(td) / "does-not-exist.xlsx"))

    check("compliance-matrix defers to its specialist tool",
          "compliance-matrix.md" in DEFER_TO_SPECIALIST)
    check("section prefixes stripped consistently",
          sheet_name("E. Scored content", set()) == "Scored content"
          and sheet_name("3. Outcomes", set()) == "Outcomes")

    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def matrices_for(base):
    """Every matrix-style .md under one proposal directory, deduped and ordered."""
    found = []
    for pattern in MATRIX_GLOBS:
        for p in sorted(base.glob(pattern)):
            if p.name not in NOT_A_MATRIX and p not in found:
                found.append(p)
    return found


def main():
    ap = argparse.ArgumentParser(description="Render matrix markdown to a formatted .xlsx")
    ap.add_argument("paths", nargs="*", help="markdown file(s) to render")
    ap.add_argument("--proposal", help="render the matrix set for one proposal slug")
    ap.add_argument("--all", action="store_true",
                    help="sweep every proposal in the workspace")
    ap.add_argument("--out-dir", help="output directory (default: beside the .md)")
    ap.add_argument("--force", action="store_true",
                    help="re-render even when the .xlsx is newer than the .md")
    ap.add_argument("--adopt-existing", action="store_true",
                    help="one-time migration: also overwrite unstamped outputs, treating them "
                         "as previous runs of this tool. Only use when you know no hand-built "
                         "workbook sits at a target path.")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    targets = [Path(p) for p in args.paths]

    if args.proposal:
        base = WORKSPACE_ROOT / "proposals" / args.proposal
        if not base.is_dir():
            print(f"ERROR: no proposal at {base}", file=sys.stderr)
            return 1
        targets += matrices_for(base)

    if args.all:
        proposals_dir = WORKSPACE_ROOT / "proposals"
        for slug in sorted(p for p in proposals_dir.iterdir() if p.is_dir()):
            targets += matrices_for(slug)

    if not targets:
        print("Nothing to render. Pass a path, --proposal <slug>, or --all.", file=sys.stderr)
        return 1

    rendered = skipped = failed = 0
    current_group = None
    for md in targets:
        if not md.is_file():
            print(f"  [SKIP] {md} (not found)")
            skipped += 1
            continue

        # Group output by proposal so a workspace sweep stays readable.
        try:
            group = md.relative_to(WORKSPACE_ROOT / "proposals").parts[0]
        except ValueError:
            group = md.parent.name
        if group != current_group:
            print(f"\n{group}")
            current_group = group

        if md.name in DEFER_TO_SPECIALIST and not args.paths:
            print(f"  [SKIP] {md.name} (use: {DEFER_TO_SPECIALIST[md.name]})")
            skipped += 1
            continue

        out = (Path(args.out_dir) / (md.stem + ".xlsx")) if args.out_dir \
            else md.with_suffix(".xlsx")

        # Never overwrite a workbook this tool did not write, whatever --force says.
        if out.exists() and not is_ours(out) and not args.adopt_existing:
            print(f"  [KEEP] {md.name} -> {out.name} was not generated by this tool; "
                  f"left untouched")
            skipped += 1
            continue

        if not args.force and out.exists() and out.stat().st_mtime >= md.stat().st_mtime:
            print(f"  [SKIP] {md.name} (up to date)")
            skipped += 1
            continue

        try:
            built, msg = build_workbook(md, out)
        except Exception as e:                                  # noqa: BLE001
            print(f"  [FAIL] {md.name}: {e}")
            failed += 1
            continue
        if built:
            print(f"  [OK]   {md.name}  ->  {out.name}  ({msg})")
            rendered += 1
        else:
            print(f"  [SKIP] {md.name}: {msg}")
            skipped += 1

    print(f"\nDone — rendered: {rendered}, skipped: {skipped}, failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
