#!/usr/bin/env python3
"""Turn the capture pipeline's requirement export into demand-signal candidates.

    python scripts/ingest-crm-candidates.py --file crm-demand-candidates.jsonl
    python scripts/ingest-crm-candidates.py --file <f> --stats-only
    python scripts/ingest-crm-candidates.py --selftest

WHY A SECOND FEEDER. The register was backfilled from 12 proposal requirement
matrices — pursuits that reached a bid. The capture pipeline holds Quick Vet's
`key_requirements` for every vetted opportunity: on the live instance that is
475 requirement lines across 96 opportunities, observed at TRIAGE rather than at
proposal and therefore months earlier. Same register, wider and earlier aperture.

It also carries `pursuit_value_usd`, which §9 question 5 names as the reason
dollar-weighted ranking is dark.

THIS SCRIPT OWNS THE VOCABULARY, THE EXPORTER DOES NOT. The capture side sends
`capability_theme`, `demand_strength` and `our_status` as null on purpose — a
second classifier would silently split a theme and understate its weight, and
the other two are judgements it cannot make. Classification happens here,
through the same `demand_signal_core.suggest_theme` the matrix extractor uses,
so there is exactly one reader of `reference/capability-themes.md`.

WHAT IT REFUSES TO INFER. `our_status` stays null. The matrix extractor reads it
from a Gap/Risk column; Quick Vet writes no coverage judgement, and inventing
one would put BD's opinion into the register without BD having formed it. These
candidates therefore REQUIRE the confirmation step — they cannot be promoted
unattended. `demand_strength` takes the modal verb as weak evidence only where
the register's own rule would land in the same place.

OVERLAP IS REPORTED, NOT RESOLVED. A pursuit can exist as both a CRM opportunity
and a proposal here; ingesting both would double every theme it touches. There
is no shared key, so the overlap is detected by title similarity and REPORTED.
Fusing two records on a fuzzy match would corrupt the register silently, and the
curated matrix row should win anyway — that is a human call.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from demand_signal_core import (  # noqa: E402
    MECHANICAL_PATTERNS, load_valid_themes, suggest_theme)

WORKSPACE_ROOT = Path(__file__).parent.parent
PROPOSALS_DIR = WORKSPACE_ROOT / "proposals"

#: The register's own mechanics rule, shared with the matrix extractor so the
#: two cannot drift about what belongs in the register. The exporter flags
#: mechanics too; where the two disagree the count is reported, which is how a
#: drifting rule on either side becomes visible instead of quietly changing the
#: corpus. That cross-check is what surfaced the `address` over-match.

#: Overlap threshold for "this CRM pursuit may already be a proposal here".
#: Set high: a false pair costs a look, a page of them means the report is
#: ignored — the same reasoning the capture side's duplicate detector uses.
_OVERLAP_FLOOR = 0.6
_STOP = {"the", "a", "an", "of", "for", "and", "to", "in", "on", "sbir", "phase",
         "i", "ii", "iii", "rfi", "rfp", "sources", "sought"}


def _tokens(title: str) -> set[str]:
    words = re.split(r"[^a-z0-9]+", str(title or "").lower())
    return {w for w in words if w and w not in _STOP and len(w) > 1}


def _overlap(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def infer_strength(modal: str | None) -> str:
    """Map the modal verb onto the register's strength vocabulary.

    `shall`/`must` is binding federal drafting, but the enum also splits
    pass/fail from scored and nothing here reads a rubric — so a binding verb
    lands on `mandatory-scored`, which is what the matrix extractor returns for
    an explicit requirement with no stated weight. Everything else takes the
    same `desired` default the extractor uses, rather than a fresh guess.
    """
    if modal in ("shall", "must", "required"):
        return "mandatory-scored"
    return "desired"


def proposal_titles() -> dict[str, set[str]]:
    """Slug → title tokens, for the overlap report. Reads the proposal's own
    quick-look or plan heading; falls back to the slug."""
    out: dict[str, set[str]] = {}
    if not PROPOSALS_DIR.exists():
        return out
    for slug_dir in sorted(p for p in PROPOSALS_DIR.iterdir() if p.is_dir()):
        title = slug_dir.name.replace("-", " ")
        for candidate in ("working/quick-look.md", "working/proposal-plan.md"):
            path = slug_dir / candidate
            if not path.exists():
                continue
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:40]:
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            break
        out[slug_dir.name] = _tokens(title)
    return out


def convert(records: list[dict], valid_themes: list[str]) -> tuple[list[dict], dict]:
    """CRM export rows → candidates in the shape the confirmation step expects."""
    out: list[dict] = []
    stats = {
        "read": len(records),
        "dropped_mechanics": 0,
        "dropped_too_short": 0,
        "mechanics_disagreement": 0,
        "themed": 0,
        "unthemed": 0,
        "with_value": 0,
    }
    for rec in records:
        requirement = str(rec.get("requirement") or "").strip()
        if len(requirement) < 12:
            stats["dropped_too_short"] += 1
            continue
        ours = bool(MECHANICAL_PATTERNS.search(requirement))
        theirs = bool(rec.get("likely_mechanics"))
        if ours != theirs:
            stats["mechanics_disagreement"] += 1
        if ours:
            stats["dropped_mechanics"] += 1
            continue

        theme, hits = suggest_theme(requirement, valid_themes)
        if theme:
            stats["themed"] += 1
        else:
            stats["unthemed"] += 1
        if rec.get("pursuit_value_usd"):
            stats["with_value"] += 1

        out.append({
            # No proposal here — the pursuit never became one, which is the
            # point of this feeder.
            "proposal_slug": None,
            "program": rec.get("program"),
            "source_system": "capture-pipeline",
            "source_file": None,
            "source_ref": rec.get("source_ref"),
            "row_id": rec.get("candidate_id"),
            "customer": rec.get("customer"),
            "date_observed": rec.get("date_observed"),
            "source_type": rec.get("source_type") or "solicitation",
            "requirement": requirement,
            "gap_text": None,
            "theme_suggestion": theme,
            "theme_confidence": hits,
            # Deliberately null: Quick Vet writes no coverage judgement, and
            # BD's read is not the capture tool's to invent. Confirmation must
            # supply it, so these cannot be promoted unattended.
            "our_status_inferred": None,
            "demand_strength_inferred": infer_strength(rec.get("modal_verb")),
            "rubric_weight_pct": None,
            "pursuit_value_usd": rec.get("pursuit_value_usd"),
            "bid_impact": rec.get("bid_impact"),
            "deal_stage": rec.get("deal_stage"),
            "solicitation_url": rec.get("solicitation_url"),
            "opportunity_title": rec.get("opportunity_title"),
        })
    return out, stats


def overlap_report(candidates: list[dict], titles: dict[str, set[str]]) -> list[dict]:
    """CRM pursuits that may already exist here as a proposal.

    Reported per PURSUIT, not per requirement line — one pursuit matching a
    proposal is one decision, and listing it once per requirement would bury it.
    """
    by_pursuit: dict[str, str] = {}
    for c in candidates:
        ref = c.get("source_ref") or ""
        if ref and ref not in by_pursuit:
            by_pursuit[ref] = c.get("opportunity_title") or ""
    found = []
    for ref, title in by_pursuit.items():
        toks = _tokens(title)
        best, score = None, 0.0
        for slug, ttoks in titles.items():
            s = _overlap(toks, ttoks)
            if s > score:
                best, score = slug, s
        if best and score >= _OVERLAP_FLOOR:
            found.append({"source_ref": ref, "crm_title": title,
                          "proposal_slug": best, "score": round(score, 2)})
    return sorted(found, key=lambda f: -f["score"])


def print_stats(stats: dict, candidates: list[dict], overlaps: list[dict]) -> None:
    print(f"read from export        : {stats['read']}")
    print(f"  dropped as mechanics  : {stats['dropped_mechanics']}")
    print(f"  dropped as too short  : {stats['dropped_too_short']}")
    print(f"candidates written      : {len(candidates)}")
    print(f"  theme suggested       : {stats['themed']}")
    print(f"  no theme matched      : {stats['unthemed']}  (confirmation assigns one)")
    print(f"  carrying a value      : {stats['with_value']}")
    print()
    # A disagreement is not an error on either side; it is the two rules
    # drifting apart, which is worth seeing before it changes the corpus.
    print(f"mechanics-rule disagreements with the exporter: {stats['mechanics_disagreement']}")
    by_theme: dict[str, int] = {}
    for c in candidates:
        if c["theme_suggestion"]:
            by_theme[c["theme_suggestion"]] = by_theme.get(c["theme_suggestion"], 0) + 1
    if by_theme:
        print()
        print("top suggested themes:")
        for theme, n in sorted(by_theme.items(), key=lambda kv: -kv[1])[:12]:
            print(f"   {theme:<38} {n}")
    print()
    if overlaps:
        print(f"POSSIBLE OVERLAP with existing proposals: {len(overlaps)} pursuit(s).")
        print("Nothing is merged — the curated matrix row should win. Review:")
        for o in overlaps[:12]:
            print(f"   {o['score']:.2f}  {o['crm_title'][:44]:<44} ~ {o['proposal_slug']}")
    else:
        print("No pursuit overlaps an existing proposal by title.")


def selftest() -> int:
    themes = ["air-gap-ddil-deployment", "multimodal-audio"]
    recs = [
        {"requirement": "The system shall run inference fully air gapped in a DDIL environment.",
         "modal_verb": "shall", "source_ref": "crm:opportunity/1", "candidate_id": "CRM-1-1",
         "customer": "DARPA", "pursuit_value_usd": 250000, "likely_mechanics": False,
         "opportunity_title": "Air gapped inference pilot"},
        {"requirement": "Responses shall not exceed 10 pages and use 12 point font.",
         "modal_verb": "shall", "source_ref": "crm:opportunity/1", "candidate_id": "CRM-1-2",
         "likely_mechanics": True},
        {"requirement": "short", "candidate_id": "CRM-1-3"},
    ]
    out, stats = convert(recs, themes)
    assert stats["read"] == 3, stats
    assert stats["dropped_mechanics"] == 1, stats
    assert stats["dropped_too_short"] == 1, stats
    assert len(out) == 1, out

    c = out[0]
    assert c["our_status_inferred"] is None, "status must never be inferred here"
    assert c["demand_strength_inferred"] == "mandatory-scored", c
    assert c["pursuit_value_usd"] == 250000, c
    assert c["row_id"] == "CRM-1-1", c
    assert c["proposal_slug"] is None, c

    # A non-binding verb takes the extractor's own default rather than a guess.
    out2, _ = convert([{"requirement": "The system should support audio transcription.",
                        "modal_verb": "should", "candidate_id": "CRM-2-1"}], themes)
    assert out2[0]["demand_strength_inferred"] == "desired", out2

    # Overlap is reported per pursuit and never merged.
    ov = overlap_report(out, {"air-gapped-inference-pilot": _tokens("Air gapped inference pilot")})
    assert len(ov) == 1 and ov[0]["score"] >= _OVERLAP_FLOOR, ov
    assert overlap_report(out, {"something-else": _tokens("Totally unrelated widget")}) == []

    # The exporter's flag and this side's rule agreeing is not assumed.
    _o3, s3 = convert([{"requirement": "Submit the proposal via the DSIP portal.",
                        "likely_mechanics": False, "candidate_id": "CRM-3-1"}], themes)
    assert s3["mechanics_disagreement"] == 1, s3

    print("selftest: ok")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", help="the capture pipeline's candidates .jsonl")
    ap.add_argument("--out", help="output path (default signals/candidates/<today>-crm-candidates.jsonl)")
    ap.add_argument("--stats-only", action="store_true", help="report without writing")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.file:
        ap.error("--file <export.jsonl> is required (or use --selftest)")

    src = Path(args.file)
    if not src.exists():
        print(f"not found: {src}", file=sys.stderr)
        return 1

    records = []
    for i, line in enumerate(src.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except ValueError:
            print(f"  line {i}: unparsable, skipped", file=sys.stderr)

    valid = load_valid_themes()
    candidates, stats = convert(records, valid)
    overlaps = overlap_report(candidates, proposal_titles())
    print_stats(stats, candidates, overlaps)

    if args.stats_only:
        return 0

    out_path = Path(args.out) if args.out else (
        WORKSPACE_ROOT / "signals" / "candidates" /
        f"{date.today().isoformat()}-crm-candidates.jsonl")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for c in candidates:
            fh.write(json.dumps(c, sort_keys=True) + "\n")
    print()
    print(f"wrote {len(candidates)} candidates → {out_path.relative_to(WORKSPACE_ROOT).as_posix()}")
    print("These carry no `our_status`. Confirm them before they enter the register.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
