#!/usr/bin/env python3
"""Build the demand signal review workbook (.xlsx) — and read the answers back.

Everything in the demand signal brief is a table, and a Word document is the wrong container
for a table: it cannot be sorted, filtered, or pivoted, and the disposition answers have to be
transcribed by hand afterwards. BD transcription is the weakest link in the loop, so this
script removes it. Vincent's shop types into a dropdown; --ingest reads the same file back and
updates the register.

Sheets:
  Decisions      the five ranked exposure decisions, one row each, with the ask to answer
  Gap Queue      the write-back surface: every open item, disposition dropdown + owner column
  Exposure Map   every theme with the arithmetic visible, sortable
  All Signals    the whole register, autofiltered and frozen — the pivot-table source
  Themes         the controlled vocabulary, so a reader can check what a theme means

Usage:
  python scripts/build-demand-signal-workbook.py
  python scripts/build-demand-signal-workbook.py --ingest signals/briefs/<file>.xlsx
  python scripts/build-demand-signal-workbook.py --ingest <file> --dry-run
  python scripts/build-demand-signal-workbook.py --selftest

Exit codes:
  0 = workbook written, or dispositions ingested (or selftest passed)
  1 = register empty or missing
  2 = usage error or an invalid disposition value in an ingested file
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))
import demand_signal_core as core  # noqa: E402

REGISTER = WORKSPACE_ROOT / "signals" / "demand-signals.jsonl"
OUT_DIR = WORKSPACE_ROOT / "signals" / "briefs"

DISPOSITIONS = ["already-exists-ask-me", "building", "planned", "needs-scoping", "wont-build"]

HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=10)
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")  # the cells we are asking them to fill
BODY_FONT = Font(size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
TOP = Alignment(vertical="top")


def load_register() -> list[dict]:
    if not REGISTER.exists():
        return []
    out = []
    for line in REGISTER.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def style_header(ws, widths: list[int], freeze: str = "A2") -> None:
    for idx, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(idx)].width = width
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.freeze_panes = freeze
    ws.row_dimensions[1].height = 30


def write_rows(ws, rows: list[list], wrap_cols: set[int] | None = None) -> None:
    wrap_cols = wrap_cols or set()
    for row in rows:
        ws.append(row)
    for r in ws.iter_rows(min_row=2):
        for cell in r:
            cell.font = BODY_FONT
            cell.alignment = WRAP if cell.column in wrap_cols else TOP


def sheet_decisions(wb: Workbook, exposure: list[dict], signals: list[dict]) -> None:
    ws = wb.create_sheet("Decisions")
    ws.append(["#", "Capability theme", "Exposure", "Customers asking", "What they asked (verbatim)",
               "What we can prove", "What it has already cost", "What we need from you"])
    decisions = [r for r in exposure if r["exposure"] > 0][:5]
    rows = []
    for i, row in enumerate(decisions, 1):
        ask = max(
            (s for s in signals if s["capability_theme"] == row["theme"]),
            key=lambda s: (s["demand_strength"].startswith("mandatory"), s["date_observed"]),
            default=None,
        )
        proof = {
            "none": "NOTHING in the evidence ledger carries this theme",
            "weak": f"only {row['evidence_count']} ledger item(s) — one anecdote, not proof",
            "strong": f"{row['evidence_count']} ledger items cover the theme",
        }[row["proof"]]
        if row["evidence_ids"]:
            proof += f" ({', '.join(row['evidence_ids'])})"
        cost = "\n".join(
            f"• {e['customer']} ({e['signal_id']}): {e['bid_impact']}" for e in row["examples"][:3]
        ) or "No bid has paid for this yet."
        rows.append([
            i, row["theme"], row["exposure"],
            f"{row['customer_count']}: " + ", ".join(row["customers"][:5]),
            (ask["requirement"] if ask else ""), proof, cost, decision_ask(row),
        ])
    write_rows(ws, rows, wrap_cols={4, 5, 6, 7, 8})
    style_header(ws, [4, 32, 9, 30, 52, 34, 46, 44])


def decision_ask(row: dict) -> str:
    classes = row["classes"]
    if classes.get("hard-gap"):
        return ("Build, or confirm wont-build so BD teams for it instead of hedging. "
                "Either answer is useful; silence is not.")
    if classes.get("unproven-claim"):
        return ("Confirm whether this is real and citable. If it is, it needs a ledger entry; "
                "if not, BD stops claiming it.")
    if row["proof"] == "none":
        return "Name what covers this today, or tell us nothing does."
    if row["hedges"] and row["proof"] == "strong":
        return ("Theme is evidenced but these asks still cost a hedge. Confirm the specific "
                "capability exists and is citable, or that it is out of scope.")
    if classes.get("enablement"):
        return "Point BD at what already covers this."
    return "Confirm the theme is on the roadmap and name an owner."


def sheet_gap_queue(wb: Workbook, signals: list[dict], by_theme: dict[str, dict]) -> None:
    """The write-back surface. Yellow columns are the ones we are asking them to fill."""
    ws = wb.create_sheet("Gap Queue")
    ws.append(["Signal", "Class", "Customer", "The ask", "Theme", "Strength",
               "What it cost us", "CTO disposition", "Detail / target quarter", "Owner"])
    rows = []
    for sig in signals:
        proof = by_theme.get(sig["capability_theme"], {}).get("proof", "none")
        cls = core.classify_signal(sig, proof)
        if cls not in {"hard-gap", "unproven-claim", "enablement"}:
            continue
        rows.append([
            sig["signal_id"], cls, sig["customer"], sig["requirement"], sig["capability_theme"],
            sig["demand_strength"], sig.get("bid_impact") or "",
            sig.get("cto_disposition") or "", sig.get("cto_disposition_detail") or "",
            sig.get("cto_owner") or "",
        ])
    # Hard gaps first: engineering's items above the ones that are probably BD's.
    order = {"hard-gap": 0, "unproven-claim": 1, "enablement": 2}
    rows.sort(key=lambda r: (order.get(r[1], 9), r[0]))
    write_rows(ws, rows, wrap_cols={4, 7, 9})
    style_header(ws, [10, 18, 30, 60, 30, 17, 46, 22, 30, 14])

    last = max(ws.max_row, 2)
    dv = DataValidation(type="list", formula1='"' + ",".join(DISPOSITIONS) + '"',
                        allow_blank=True, showDropDown=True)
    dv.error = "Pick one of the five dispositions, or leave it blank."
    dv.prompt = ("already-exists-ask-me / building / planned / needs-scoping / wont-build. "
                 "wont-build is a useful answer — it tells BD to team for it.")
    ws.add_data_validation(dv)
    dv.add(f"H2:H{last}")
    for col in ("H", "I", "J"):
        for r in range(2, last + 1):
            ws[f"{col}{r}"].fill = INPUT_FILL
    ws.auto_filter.ref = f"A1:J{last}"


def sheet_exposure(wb: Workbook, exposure: list[dict]) -> None:
    ws = wb.create_sheet("Exposure Map")
    ws.append(["Capability theme", "Exposure", "Customers", "Signals", "Mandatory",
               "Ledger items", "Proof", "Bids hedged", "Hard gaps", "Enablement misses",
               "Who is asking"])
    rows = [[
        r["theme"], r["exposure"], r["customer_count"], r["signals"], r["mandatory"],
        r["evidence_count"], r["proof"], r["hedges"],
        r["classes"].get("hard-gap", 0), r["classes"].get("enablement", 0),
        ", ".join(r["customers"]),
    ] for r in exposure]
    write_rows(ws, rows, wrap_cols={11})
    style_header(ws, [32, 10, 11, 9, 11, 13, 9, 12, 11, 18, 60])
    ws.auto_filter.ref = f"A1:K{max(ws.max_row, 2)}"


def sheet_all_signals(wb: Workbook, signals: list[dict], by_theme: dict[str, dict]) -> None:
    """The pivot-table source: one row per ask, every field, filterable."""
    ws = wb.create_sheet("All Signals")
    ws.append(["Signal", "Date", "Customer", "Program", "Pursuit", "Source type", "Strength",
               "Theme", "Class", "Our status", "CTO disposition", "Owner", "Rubric %",
               "The ask", "What it cost us", "Evidence", "Source reference"])
    rows = []
    for s in signals:
        proof = by_theme.get(s["capability_theme"], {}).get("proof", "none")
        rows.append([
            s["signal_id"], s["date_observed"], s["customer"], s.get("program") or "",
            s.get("proposal_slug") or "", s["source_type"], s["demand_strength"],
            s["capability_theme"], core.classify_signal(s, proof), s["our_status"],
            s.get("cto_disposition") or "", s.get("cto_owner") or "",
            s.get("rubric_weight_pct") or "", s["requirement"], s.get("bid_impact") or "",
            s.get("evidence_id") or "", s["source_ref"],
        ])
    write_rows(ws, rows, wrap_cols={14, 15})
    style_header(ws, [10, 11, 28, 30, 20, 13, 17, 30, 17, 12, 20, 12, 9, 60, 44, 10, 50])
    ws.auto_filter.ref = f"A1:Q{max(ws.max_row, 2)}"


def sheet_themes(wb: Workbook) -> None:
    ws = wb.create_sheet("Themes")
    ws.append(["Capability theme", "Ledger evidence tags", "Has evidence mapping"])
    rows = []
    for theme in core.load_valid_themes():
        tags = core.EVIDENCE_TAGS.get(theme, ())
        rows.append([theme, ", ".join(tags) if tags else "", "yes" if tags else "NO — reads as unproven"])
    write_rows(ws, rows, wrap_cols={2})
    style_header(ws, [34, 80, 26])


def build(signals: list[dict], out_path: Path) -> Path:
    valid = core.load_valid_themes()
    exposure = core.compute_exposure(signals, valid)
    by_theme = {r["theme"]: r for r in exposure}

    wb = Workbook()
    wb.remove(wb.active)
    sheet_decisions(wb, exposure, signals)
    sheet_gap_queue(wb, signals, by_theme)
    sheet_exposure(wb, exposure)
    sheet_all_signals(wb, signals, by_theme)
    sheet_themes(wb)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    return out_path


# ---------------------------------------------------------------------------
# Reading the answers back — the half that removes hand transcription
# ---------------------------------------------------------------------------

def ingest(xlsx_path: Path, signals: list[dict], today: date,
           dry_run: bool = False) -> tuple[list[str], list[str]]:
    """Apply Gap Queue dispositions to the register. Returns (changes, problems)."""
    wb = load_workbook(xlsx_path, data_only=True)
    if "Gap Queue" not in wb.sheetnames:
        return [], [f"{xlsx_path.name}: no 'Gap Queue' sheet"]
    ws = wb["Gap Queue"]
    header = [str(c.value or "").strip() for c in ws[1]]
    try:
        i_id = header.index("Signal")
        i_disp = header.index("CTO disposition")
        i_detail = header.index("Detail / target quarter")
        i_owner = header.index("Owner")
    except ValueError as exc:
        return [], [f"{xlsx_path.name}: expected column missing ({exc})"]

    by_id = {s["signal_id"]: s for s in signals}
    changes: list[str] = []
    problems: list[str] = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        sid = str(row[i_id] or "").strip()
        if not sid:
            continue
        sig = by_id.get(sid)
        if sig is None:
            problems.append(f"{sid}: not in the register (renamed or deleted?)")
            continue
        disp = str(row[i_disp] or "").strip()
        if not disp:
            continue
        if disp not in DISPOSITIONS:
            problems.append(f"{sid}: '{disp}' is not a valid disposition")
            continue
        detail = str(row[i_detail] or "").strip() or None
        owner = str(row[i_owner] or "").strip() or None
        if (sig.get("cto_disposition"), sig.get("cto_disposition_detail"), sig.get("cto_owner")) == \
                (disp, detail, owner):
            continue
        changes.append(
            f"{sid} {sig['capability_theme']}: "
            f"{sig.get('cto_disposition') or '(none)'} -> {disp}"
            + (f" [{owner}]" if owner else "")
        )
        if not dry_run:
            sig["cto_disposition"] = disp
            sig["cto_disposition_detail"] = detail
            sig["cto_owner"] = owner
            # Only stamp the date when the answer itself changed, so an unchanged row
            # re-ingested next week does not look freshly answered.
            sig["cto_disposition_date"] = today.isoformat()
    return changes, problems


def write_register(signals: list[dict]) -> None:
    with REGISTER.open("w", encoding="utf-8") as fh:
        for sig in signals:
            fh.write(json.dumps(sig, ensure_ascii=False) + "\n")


def selftest() -> int:
    import tempfile
    valid = core.load_valid_themes()
    signals = [
        {"schema_version": "demand-signal.v1", "signal_id": "SIG-0001", "date_observed": "2026-07-01",
         "source_type": "solicitation", "source_ref": "proposals/x/working/requirement-matrix.md#R1",
         "customer": "DIA", "program": "DMA", "proposal_slug": "x",
         "requirement": "Support progressive model upgrades across the air gap.",
         "capability_theme": "cross-domain-model-update", "demand_strength": "mandatory-scored",
         "our_status": "gap", "bid_impact": "Bid the path, not the capability.",
         "cto_disposition": None, "cto_disposition_detail": None, "cto_owner": None,
         "cto_disposition_date": None, "evidence_id": None, "rubric_weight_pct": 10},
        {"schema_version": "demand-signal.v1", "signal_id": "SIG-0002", "date_observed": "2026-08-10",
         "source_type": "conference", "source_ref": "notes.md", "customer": "USSOCOM",
         "program": None, "proposal_slug": None,
         "requirement": "Cite the doctrine paragraph behind every answer.",
         "capability_theme": "output-verification-attribution", "demand_strength": "desired",
         "our_status": "shipping", "bid_impact": None, "cto_disposition": None,
         "cto_disposition_detail": None, "cto_owner": None, "cto_disposition_date": None,
         "evidence_id": None, "rubric_weight_pct": None},
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = build(signals, Path(tmp) / "wb.xlsx")
        wb = load_workbook(path)
        assert wb.sheetnames == ["Decisions", "Gap Queue", "Exposure Map", "All Signals", "Themes"], \
            wb.sheetnames
        gq = wb["Gap Queue"]
        assert gq.max_row >= 2, "gap queue must contain the open item"
        assert gq["A2"].value == "SIG-0001", gq["A2"].value
        assert gq.freeze_panes == "A2" and gq.auto_filter.ref.startswith("A1:")
        assert len(gq.data_validations.dataValidation) == 1, "disposition dropdown missing"
        assert wb["All Signals"].max_row == 3, "every signal belongs on All Signals"

        # Round-trip: write a disposition into the sheet, ingest it, confirm the register moved.
        gq["H2"] = "wont-build"
        gq["I2"] = "no cross-domain transfer planned"
        gq["J2"] = "Vincent"
        gq["H3"] = "not-a-real-disposition" if gq.max_row >= 3 else None
        wb.save(path)

        today = date(2026, 8, 20)
        changes, problems = ingest(path, signals, today, dry_run=True)
        assert any("SIG-0001" in c and "wont-build" in c for c in changes), changes
        assert signals[0]["cto_disposition"] is None, "dry run must not mutate the register"

        changes, problems = ingest(path, signals, today)
        assert signals[0]["cto_disposition"] == "wont-build", signals[0]
        assert signals[0]["cto_owner"] == "Vincent"
        assert signals[0]["cto_disposition_date"] == "2026-08-20"
        # An unchanged re-ingest must be a no-op, not a fresh date stamp.
        signals[0]["cto_disposition_date"] = "2026-08-20"
        changes2, _ = ingest(path, signals, date(2026, 9, 1))
        assert not any("SIG-0001" in c for c in changes2), f"re-ingest should be a no-op: {changes2}"
        assert signals[0]["cto_disposition_date"] == "2026-08-20", "date must not be re-stamped"

        # A junk value is reported, never written.
        wb2 = load_workbook(path)
        wb2["Gap Queue"]["H2"] = "definitely-maybe"
        wb2.save(path)
        _, problems = ingest(path, signals, today)
        assert any("not a valid disposition" in p for p in problems), problems
        assert signals[0]["cto_disposition"] == "wont-build", "invalid value must not overwrite"

    print(f"SELFTEST PASS — {len(valid)} themes, workbook build + dropdown + "
          "disposition round-trip + invalid-value rejection verified")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ingest", help="read dispositions back from a completed workbook")
    parser.add_argument("--dry-run", action="store_true", help="with --ingest, report without writing")
    parser.add_argument("--selftest", action="store_true", help="deterministic offline self-test")
    args = parser.parse_args()

    if args.selftest:
        return selftest()

    signals = load_register()
    if not signals:
        print(f"Register is empty or missing: {REGISTER}", file=sys.stderr)
        return 1

    if args.ingest:
        path = Path(args.ingest)
        if not path.exists():
            print(f"ERROR: no such file: {path}", file=sys.stderr)
            return 2
        changes, problems = ingest(path, signals, date.today(), dry_run=args.dry_run)
        for p in problems:
            print(f"PROBLEM: {p}", file=sys.stderr)
        if not changes:
            print("No new dispositions found.")
            return 2 if problems else 0
        print(f"{len(changes)} disposition(s) {'to apply' if args.dry_run else 'applied'}:")
        for c in changes:
            print(f"  {c}")
        if not args.dry_run:
            write_register(signals)
            print(f"\nUpdated {REGISTER.relative_to(WORKSPACE_ROOT).as_posix()}")
            print("Next: rebuild the brief, and add a claim-envelope row for anything now provable.")
        return 2 if problems else 0

    out = build(signals, OUT_DIR / f"{date.today().isoformat()}-demand-signals.xlsx")
    print(f"Wrote {out.relative_to(WORKSPACE_ROOT).as_posix()}  ({len(signals)} signals)")
    print("Send this instead of the .docx. Yellow columns on 'Gap Queue' are theirs to fill.")
    print(f"When it comes back: python scripts/build-demand-signal-workbook.py --ingest <file>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
