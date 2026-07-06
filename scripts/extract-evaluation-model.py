#!/usr/bin/env python3
"""Extract this solicitation's evaluation model into a typed, human-curatable running log.

The evaluation model answers "how will we be judged" the same way the compliance matrix
answers "what must we cover": typed rows with provenance, curated by a human. Kinds:

  factor      a scored evaluation factor ("will be evaluated", "basis for award", ...)
  weighting   a relative-importance statement ("significantly more important than", ...)
  pass-fail   a disqualifier or gate ("pass/fail", "eliminated from competition", ...)
  constraint  a submission constraint (page limit, font, deadline) -- counted only in
              Section L/M context, so a page count in a capability deck is noise

Deterministic baseline (this script) is the offline path; the proposal-manager skill's
AI enrichment pass may append additional rows with origin "ai-inferred" (no source
sentence -- never silently mixed with cited rows). Ported from the proposal-workbench
reference implementation (backend/app/services/evaluation_model.py).

Running-log discipline: re-extraction replaces ONLY rows with status "extracted" whose
origin is not "manual". Rows a human confirmed, edited, or rejected -- and manual rows --
always survive. Rejected rows stay in the table but are excluded from the drafting
context block.

The markdown table in working/evaluation-model.md is the source of truth (humans edit
Status / Kind / text there). working/evaluation-model.json and the "Drafting Context
Block" section of the .md are derived on every run.

Usage:
  # Extract (or re-extract, preserving reviewed rows) from inputs/00_priority/
  python scripts/extract-evaluation-model.py --proposal <slug>

  # Re-derive the JSON sidecar + context block from the hand-edited table,
  # WITHOUT re-extracting (use after curating the table)
  python scripts/extract-evaluation-model.py --proposal <slug> --resync

  # Print the prompt-injectable context block to stdout
  python scripts/extract-evaluation-model.py --proposal <slug> --print-context

  # Deterministic self-test (no proposal needed)
  python scripts/extract-evaluation-model.py --selftest

Exit codes:
  0 = success
  1 = no criteria found / missing inputs
  2 = usage or environment error
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

EVALUATION_KINDS = ("factor", "weighting", "pass-fail", "constraint")
ORIGINS = ("extracted", "ai-inferred", "manual")
STATUSES = ("extracted", "confirmed", "edited", "rejected")
REVIEWED_STATUSES = {"confirmed", "edited", "rejected"}

# --- classification patterns (ported from proposal-workbench evaluation_model.py) ---

FACTOR_PATTERN = re.compile(
    r"\b(will be evaluated|evaluation (?:factor|criteri|of)|basis for award|best value|"
    r"technical (?:merit|approach|acceptability)|past performance will|adjectival|"
    r"government will (?:evaluate|assess|consider|rate|score)|evaluated on|scored on)\b",
    re.IGNORECASE,
)
WEIGHTING_PATTERN = re.compile(
    r"\b(significantly (?:more|less) important than|(?:more|less) important than|significantly more|approximately equal|"
    r"equal(?:ly)? (?:important|weighted)|in descending order of importance|relative (?:importance|weight)|"
    r"when combined|trade-?off|weighted)\b",
    re.IGNORECASE,
)
PASS_FAIL_PATTERN = re.compile(
    r"\b(pass/fail|acceptable/unacceptable|go/no-?go|eliminat\w+ from (?:the )?competition|"
    r"will not be (?:considered|evaluated) (?:if|unless)|must \w+ to be considered|disqualif)\b",
    re.IGNORECASE,
)
CONSTRAINT_PATTERN = re.compile(
    r"\b(no more than \d+|page limit|pages? (?:or fewer|maximum)|font|margins?|"
    r"due (?:by|date|no later)|deadline|submission deadline|submit(?:ted)? (?:via|through|by)|file format)\b",
    re.IGNORECASE,
)

# Section-context detection for solicitation text rendered to markdown. A heading or
# short standalone line flips the context for the sentences that follow it.
SECTION_L_PATTERN = re.compile(
    r"\b(section\s+l\b|instructions(?:,| to| for) offerors|proposal (?:preparation|submission) instructions)",
    re.IGNORECASE,
)
SECTION_M_PATTERN = re.compile(
    r"\b(section\s+m\b|evaluation (?:criteria|factors|approach)|basis for award|evaluation of (?:proposals|offers))",
    re.IGNORECASE,
)


def classify_evaluation_sentence(text: str, section_key: str = "") -> str | None:
    """Type a sentence into the evaluation model, or None when it isn't evaluator-facing.

    Order matters: pass/fail and weighting language are more specific signals than the
    generic factor pattern, and constraints only count when stated by Section L/M-ish
    text (a page limit in a capability deck is noise).
    """
    if PASS_FAIL_PATTERN.search(text):
        return "pass-fail"
    if WEIGHTING_PATTERN.search(text) and (FACTOR_PATTERN.search(text) or section_key == "section-m"):
        return "weighting"
    if FACTOR_PATTERN.search(text) or section_key == "section-m":
        return "factor"
    if CONSTRAINT_PATTERN.search(text) and section_key in {"section-l", "section-m"}:
        return "constraint"
    return None


def split_sectioned_sentences(content: str) -> list[tuple[str, str]]:
    """Yield (sentence, section_key) pairs, tracking Section L/M context from headings."""
    results: list[tuple[str, str]] = []
    section_key = ""
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        is_headingish = raw_line.lstrip().startswith("#") or (len(line) <= 90 and not line.endswith("."))
        if is_headingish:
            heading_text = line.lstrip("#* ").strip()
            if SECTION_M_PATTERN.search(heading_text):
                section_key = "section-m"
                continue
            if SECTION_L_PATTERN.search(heading_text):
                section_key = "section-l"
                continue
            if raw_line.lstrip().startswith("#"):
                # A heading that names neither L nor M resets the context.
                section_key = ""
                continue
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            sentence = " ".join(sentence.split()).strip()
            if 30 <= len(sentence) <= 400:
                results.append((sentence, section_key))
    return results


def _weight_phrase(text: str) -> str:
    match = WEIGHTING_PATTERN.search(text)
    return match.group(0).lower() if match else ""


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


# --- markdown running-log table (source of truth) ---

TABLE_COLUMNS = ["ID", "Kind", "Criterion", "Weight", "Notes", "Source", "Section", "Origin", "Status"]


def _escape_cell(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def _unescape_cell(value: str) -> str:
    return (value or "").replace("\\|", "|").strip()


def parse_evaluation_model_md(text: str) -> list[dict]:
    """Recover criterion rows from the markdown table. Tolerant of hand edits."""
    rows: list[dict] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [_unescape_cell(cell) for cell in re.split(r"(?<!\\)\|", stripped.strip("|"))]
        if len(cells) < 9 or cells[0] in {"ID", ""} or set(cells[0]) <= {"-", " ", ":"}:
            continue
        if not re.fullmatch(r"EC-\d+", cells[0]):
            continue
        kind = cells[1].lower()
        origin = cells[7].lower()
        status = cells[8].lower()
        rows.append({
            "id": cells[0],
            "kind": kind if kind in EVALUATION_KINDS else "factor",
            "criterion": cells[2],
            "weight_text": cells[3],
            "detail": cells[4],
            "source_file": cells[5],
            "source_section": cells[6],
            "origin": origin if origin in ORIGINS else "extracted",
            "status": status if status in STATUSES else "extracted",
        })
    for ordinal, row in enumerate(rows, start=1):
        row["ordinal"] = ordinal
    return rows


def render_context_block(rows: list[dict], limit_per_kind: int = 12) -> str:
    """The prompt-injectable block pinning drafting and review to THIS solicitation's rubric."""
    active = [row for row in rows if row["status"] != "rejected" and row["criterion"].strip()]
    if not active:
        return ""
    labels = {
        "factor": "Evaluation factors",
        "weighting": "Relative weighting",
        "pass-fail": "Pass/fail and disqualifiers",
        "constraint": "Submission constraints",
    }
    lines = [
        "# This Solicitation's Evaluation Model",
        "Score and shape the response against these specific criteria. They override generic rubric doctrine when they conflict:",
    ]
    for kind in EVALUATION_KINDS:
        entries = [row for row in active if row["kind"] == kind]
        if not entries:
            continue
        lines.append(f"\n## {labels[kind]}")
        for row in entries[:limit_per_kind]:
            weight = f" [{row['weight_text']}]" if row["weight_text"] else ""
            detail = f" -- {row['detail']}" if row["detail"] else ""
            if row["origin"] == "ai-inferred":
                source = " (ai-inferred)"
            elif row["source_file"]:
                source = f" (source: {row['source_file']})"
            else:
                source = ""
            lines.append(f"- {row['id']}: {row['criterion']}{weight}{detail}{source}")
    return "\n".join(lines)


def render_evaluation_model_md(proposal: str, rows: list[dict]) -> str:
    header = "| " + " | ".join(TABLE_COLUMNS) + " |"
    divider = "|" + "|".join(["---"] * len(TABLE_COLUMNS)) + "|"
    body = []
    for row in rows:
        body.append("| " + " | ".join(_escape_cell(str(row.get(key, ""))) for key in (
            "id", "kind", "criterion", "weight_text", "detail", "source_file", "source_section", "origin", "status",
        )) + " |")
    context = render_context_block(rows)
    context_section = context if context else "_No active criteria yet._"
    return f"""# Evaluation Model -- {proposal}

This solicitation's rubric as a typed running log. **The table below is the source of
truth; curate it by hand.** Set Status to `confirmed` (row is right), `edited` (you
changed it -- also fine to just edit the text and set this), or `rejected` (noise; the
row is kept here but excluded from the drafting context). Add your own rows with Origin
`manual`. Re-running the extractor preserves every confirmed/edited/rejected/manual row
and replaces only unreviewed `extracted` rows.

After hand-editing, resync the derived outputs:
`python scripts/extract-evaluation-model.py --proposal {proposal} --resync`

## Criteria

{header}
{divider}
{chr(10).join(body) if body else "_(empty)_"}

Kinds: `factor` (scored factor) | `weighting` (relative importance) | `pass-fail` (gate/disqualifier) | `constraint` (submission constraint).
Origins: `extracted` (pattern match with provenance) | `ai-inferred` (model enrichment, no source sentence) | `manual` (human-added).

## Drafting Context Block

<!-- DERIVED: regenerated from the table on every script run. Do not hand-edit below this line. -->

{context_section}
"""


def build_json_sidecar(proposal: str, rows: list[dict]) -> dict:
    return {
        "schema_version": "evaluation-model.v1",
        "generated_by": "extract-evaluation-model.py",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "proposal_name": proposal,
        "criteria": rows,
        "summary": {
            "total": len(rows),
            "confirmed": sum(1 for row in rows if row["status"] in {"confirmed", "edited"}),
            "factors": sum(1 for row in rows if row["kind"] == "factor"),
            "weighting": sum(1 for row in rows if row["kind"] == "weighting"),
            "pass_fail": sum(1 for row in rows if row["kind"] == "pass-fail"),
            "constraints": sum(1 for row in rows if row["kind"] == "constraint"),
            "rejected": sum(1 for row in rows if row["status"] == "rejected"),
            "ai_inferred": sum(1 for row in rows if row["origin"] == "ai-inferred"),
        },
    }


def merge_extraction(existing: list[dict], sources: list[tuple[str, str]]) -> tuple[list[dict], int, int]:
    """Re-extract over sources, preserving reviewed/manual rows. Returns (rows, created, preserved)."""
    preserved = [
        row for row in existing
        if row["origin"] == "manual" or row["status"] in REVIEWED_STATUSES
    ]
    seen: set[str] = {_norm(row["criterion"]) for row in preserved}
    next_id = max(
        (int(row["id"].split("-")[1]) for row in existing if re.fullmatch(r"EC-\d+", row["id"])),
        default=0,
    ) + 1
    created = 0
    rows = list(preserved)
    for filename, content in sources:
        for sentence, section_key in split_sectioned_sentences(content):
            kind = classify_evaluation_sentence(sentence, section_key)
            if kind is None:
                continue
            key = _norm(sentence)
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "id": f"EC-{next_id}",
                "kind": kind,
                "criterion": sentence,
                "weight_text": _weight_phrase(sentence) if kind == "weighting" else "",
                "detail": "",
                "source_file": filename,
                "source_section": section_key,
                "origin": "extracted",
                "status": "extracted",
            })
            next_id += 1
            created += 1
    for ordinal, row in enumerate(rows, start=1):
        row["ordinal"] = ordinal
    return rows, created, len(preserved)


# --- proposal I/O ---

def read_source_files(prop_dir: Path) -> list[tuple[str, str]]:
    priority = prop_dir / "inputs" / "00_priority"
    sources: list[tuple[str, str]] = []
    if priority.is_dir():
        for path in sorted(priority.glob("*.md")) + sorted(priority.glob("*.txt")):
            if path.name == "portal-format.md":
                continue
            sources.append((path.name, path.read_text(encoding="utf-8", errors="replace")))
    return sources


def load_existing_rows(model_md: Path) -> list[dict]:
    if not model_md.exists():
        return []
    return parse_evaluation_model_md(model_md.read_text(encoding="utf-8", errors="replace"))


def write_outputs(prop_dir: Path, proposal: str, rows: list[dict]) -> None:
    working = prop_dir / "working"
    working.mkdir(parents=True, exist_ok=True)
    (working / "evaluation-model.md").write_text(
        render_evaluation_model_md(proposal, rows), encoding="utf-8"
    )
    (working / "evaluation-model.json").write_text(
        json.dumps(build_json_sidecar(proposal, rows), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# --- self-test ---

SELFTEST_SOLICITATION = """\
# Section M -- Evaluation Factors for Award

The Government will evaluate proposals on technical merit and operational utility.
Technical approach is significantly more important than price when combined.
Offerors that fail the demonstration will be eliminated from the competition.

# Section L -- Instructions to Offerors

The technical volume shall not exceed the page limit of 10 pages including figures.

# Company Background

Our deck has a page limit of 20 slides for internal use.
"""


def selftest() -> int:
    failures: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            failures.append(name)

    # 1. Classification: kinds + section gating.
    rows, created, _ = merge_extraction([], [("solicitation.md", SELFTEST_SOLICITATION)])
    kinds = {row["criterion"][:30]: row["kind"] for row in rows}
    check("factor classified", any(k == "factor" for k in kinds.values()))
    check("weighting classified", any(k == "weighting" for k in kinds.values()))
    check("pass-fail classified", any(k == "pass-fail" for k in kinds.values()))
    check("constraint in Section L counted",
          any(row["kind"] == "constraint" and row["source_section"] == "section-l" for row in rows))
    check("constraint outside L/M ignored",
          not any("20 slides" in row["criterion"] for row in rows))
    check("provenance recorded", all(row["source_file"] == "solicitation.md" for row in rows))

    # 2. Running-log discipline: reviewed and manual rows survive; unreviewed are replaced.
    rows[0]["status"] = "confirmed"
    rows[1]["status"] = "rejected"
    manual = {
        "id": "EC-99", "kind": "factor", "criterion": "Implied: DDIL operation is a hot button.",
        "weight_text": "", "detail": "", "source_file": "", "source_section": "",
        "origin": "manual", "status": "confirmed", "ordinal": 99,
    }
    rows.append(manual)
    rows2, _, preserved_count = merge_extraction(rows, [("solicitation.md", SELFTEST_SOLICITATION)])
    ids2 = {row["id"] for row in rows2}
    check("confirmed row preserved", rows[0]["id"] in ids2)
    check("rejected row preserved", rows[1]["id"] in ids2)
    check("manual row preserved", "EC-99" in ids2)
    check("preserved count", preserved_count == 3)
    check("no duplicate criteria", len({_norm(row["criterion"]) for row in rows2}) == len(rows2))
    check("re-extraction refills unreviewed", len(rows2) == len(rows))

    # 3. Markdown round-trip: render -> parse recovers the rows.
    md = render_evaluation_model_md("selftest", rows2)
    parsed = parse_evaluation_model_md(md)
    check("md round-trip count", len(parsed) == len(rows2))
    check("md round-trip statuses",
          [row["status"] for row in parsed] == [row["status"] for row in rows2])

    # 4. Context block: rejected excluded, ai-inferred labeled, grouped by kind.
    rows2.append({
        "id": "EC-100", "kind": "factor", "criterion": "Inferred priority on transition path.",
        "weight_text": "", "detail": "", "source_file": "", "source_section": "",
        "origin": "ai-inferred", "status": "extracted", "ordinal": 100,
    })
    block = render_context_block(rows2)
    rejected_text = rows[1]["criterion"]
    check("context excludes rejected", rejected_text not in block)
    check("context labels ai-inferred", "(ai-inferred)" in block)
    check("context grouped", "## Evaluation factors" in block and "## Submission constraints" in block)
    check("context cites source", "(source: solicitation.md)" in block)

    # 5. Determinism: same input -> identical rows.
    again, _, _ = merge_extraction([], [("solicitation.md", SELFTEST_SOLICITATION)])
    first, _, _ = merge_extraction([], [("solicitation.md", SELFTEST_SOLICITATION)])
    check("deterministic", first == again)

    if failures:
        print("SELFTEST FAILED:")
        for name in failures:
            print(f"  - {name}")
        return 1
    print(f"SELFTEST OK ({created} criteria extracted in fixture)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--proposal", help="proposals/<slug> to operate on")
    parser.add_argument("--resync", action="store_true",
                        help="re-derive JSON + context block from the hand-edited table; no re-extraction")
    parser.add_argument("--print-context", action="store_true",
                        help="print the drafting context block to stdout and exit")
    parser.add_argument("--selftest", action="store_true", help="run the embedded deterministic self-test")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if not args.proposal:
        parser.error("--proposal is required (or use --selftest)")

    prop_dir = WORKSPACE_ROOT / "proposals" / args.proposal
    if not prop_dir.is_dir():
        print(f"ERROR: proposal directory not found: {prop_dir}", file=sys.stderr)
        return 2

    model_md = prop_dir / "working" / "evaluation-model.md"
    existing = load_existing_rows(model_md)

    if args.print_context:
        block = render_context_block(existing)
        print(block if block else "(no evaluation model captured for this proposal)")
        return 0

    if args.resync:
        if not existing:
            print(f"ERROR: nothing to resync -- {model_md} is missing or has no rows", file=sys.stderr)
            return 1
        write_outputs(prop_dir, args.proposal, existing)
        print(f"Resynced {len(existing)} criteria -> working/evaluation-model.md + .json")
        return 0

    sources = read_source_files(prop_dir)
    if not sources:
        print(f"ERROR: no source files in {prop_dir / 'inputs' / '00_priority'}", file=sys.stderr)
        return 1
    rows, created, preserved = merge_extraction(existing, sources)
    write_outputs(prop_dir, args.proposal, rows)
    print(
        f"Extracted {created} new criteria from {len(sources)} source file(s); "
        f"preserved {preserved} reviewed/manual row(s); total {len(rows)} "
        f"-> working/evaluation-model.md + .json"
    )
    if created == 0 and not rows:
        print("NOTE: no evaluator-facing sentences matched. If the solicitation states criteria "
              "implicitly, add rows manually (Origin: manual) or run the proposal-manager "
              "enrichment step.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
