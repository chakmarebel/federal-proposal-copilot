#!/usr/bin/env python3
"""Promote adjudicated capture-pipeline candidates into the demand-signal register.

    python scripts/promote-crm-candidates.py \
        --candidates signals/candidates/2026-08-06-crm-candidates.jsonl \
        --decisions  reference/demand-signals/2026-08-06-crm-decisions.tsv
    python scripts/promote-crm-candidates.py ... --apply
    python scripts/promote-crm-candidates.py --selftest

THE MISSING LINK. `ingest-crm-candidates.py` converts the exporter's rows into
candidates and stops, because those candidates carry no `our_status` and the
register requires one. Nothing then moved them the last step. This does, under
the one condition that makes it safe: every row is accounted for by a human
decision, and `our_status` enters as `unknown` — the enum value the schema
defines as "extracted mechanically, not yet reviewed by a human". A CRM signal
is therefore visible to the theme leaderboard immediately and invisible to any
claim about what we can or cannot do until BD says so.

WHY A DECISIONS FILE AND NOT A CLASSIFIER. The capture pipeline does not feed
curated requirement rows. Quick Vet's `key_requirements` mixes real customer
asks with submission mechanics, eligibility rules, and Quick Vet's own guesses
about opportunities whose text it could not read ("Title suggests a
navigator-related pilot effort at Port Hueneme"). On the 2026-08-06 export the
keyword themer matched 149 of 454 and a large share of those were wrong, so
promoting its output would have inflated the leaderboard with clause-compliance
boilerplate. Adjudication is a judgement; this script's job is to make sure the
judgement exists, is complete, and is reviewable — not to make it.

REFUSALS, in order of how much damage they prevent:
  * a candidate with no decision aborts the run. Silence must never read as a
    drop, or the next export quietly shrinks the register.
  * a theme outside reference/capability-themes.md aborts. A typo splits a
    theme and understates its weight, which is the one failure the vocabulary
    file exists to prevent.
  * `hold` never promotes. It marks a real ask the vocabulary has no home for;
    adding that home is a deliberate edit to capability-themes.md.
  * a requirement already in the register under the same customer is skipped,
    so re-running an export is a no-op rather than a doubling.

`bid_impact` IS DROPPED ON PURPOSE. The exporter fills it from Quick Vet's
opportunity-level risk narrative, which means all five requirement lines of a
pursuit receive the same ~900-character blob. The schema calls this field "what
this ask cost us in the bid" — attaching a pursuit's whole risk write-up to one
requirement asserts a causal link nobody established, and would add ~400 KB of
duplicated prose to an append-only file. Carried as null until the exporter can
say something true per line.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from demand_signal_core import load_valid_themes  # noqa: E402

WORKSPACE_ROOT = Path(__file__).parent.parent
REGISTER = WORKSPACE_ROOT / "signals" / "demand-signals.jsonl"
ALIASES = WORKSPACE_ROOT / "reference" / "customer-aliases.tsv"

#: Drop reasons the decisions file may use. A closed set, so a typo in a reason
#: is caught rather than silently becoming a new category in the tally.
DROP_REASONS = {
    "mechanics",       # how to submit — deadlines, page limits, portals, CDRLs
    "posture",         # who may bid — eligibility, clearances, cost share
    "speculation",     # Quick Vet inferring, or admitting the source was empty
    "off-domain",      # a real ask outside the capability space this serves
    "too-generic",     # real, but at a grain no theme can carry
    "stale-closed",    # a prior area of interest the notice marks closed
}

SOURCE_TYPES = {"solicitation", "rfi", "industry-day", "conference", "one-on-one",
                "trial", "demo-feedback", "debrief", "partner"}
STRENGTHS = {"mandatory-passfail", "mandatory-scored", "desired", "curiosity"}


def load_aliases(path: Path | None = None) -> tuple[dict, dict]:
    """(by raw customer string, by source_ref). Missing file is not fatal —
    every name simply passes through as itself."""
    path = path or ALIASES
    by_customer: dict[str, str] = {}
    by_pursuit: dict[str, str] = {}
    if not path.exists():
        return by_customer, by_pursuit
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        kind, key, canonical = parts[0].strip(), parts[1].strip(), parts[2].strip()
        if kind == "customer":
            by_customer[key] = canonical
        elif kind == "pursuit":
            by_pursuit[key] = canonical
    return by_customer, by_pursuit


def canonical_customer(rec: dict, by_customer: dict, by_pursuit: dict) -> str | None:
    """Pursuit override beats spelling normalization beats the raw value."""
    ref = rec.get("source_ref") or ""
    if ref in by_pursuit:
        return by_pursuit[ref]
    raw = (rec.get("customer") or "").strip()
    if not raw:
        return None
    return by_customer.get(raw, raw)


def load_decisions(path: Path) -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) < 2:
            raise ValueError(f"{path.name}:{n}: expected row_id<TAB>verdict[<TAB>value]")
        row_id, verdict = parts[0], parts[1]
        value = parts[2] if len(parts) > 2 else ""
        if verdict not in ("signal", "hold", "drop"):
            raise ValueError(f"{path.name}:{n}: unknown verdict {verdict!r}")
        if row_id in out:
            raise ValueError(f"{path.name}:{n}: {row_id} decided twice")
        out[row_id] = (verdict, value)
    return out


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(text or "").lower()).strip()


def next_signal_id(existing: list[dict]) -> int:
    top = 0
    for row in existing:
        m = re.match(r"^SIG-(\d{4})$", str(row.get("signal_id") or ""))
        if m:
            top = max(top, int(m.group(1)))
    return top + 1


def build(candidates: list[dict], decisions: dict, valid_themes: list[str],
          existing: list[dict], aliases: tuple[dict, dict],
          ingested_on: str) -> tuple[list[dict], dict]:
    """Adjudicated candidates → register rows. Raises on anything unaccounted for."""
    by_customer, by_pursuit = aliases

    undecided = [c["row_id"] for c in candidates if c["row_id"] not in decisions]
    if undecided:
        raise ValueError(
            f"{len(undecided)} candidate(s) have no decision, first: "
            f"{undecided[:5]}. Silence is not a drop — decide them.")
    known = {c["row_id"] for c in candidates}
    stray = sorted(set(decisions) - known)
    if stray:
        raise ValueError(f"decisions for rows not in this export: {stray[:5]}")

    seen = {(_norm(r.get("requirement")), _norm(r.get("customer"))) for r in existing}
    counter = next_signal_id(existing)
    out: list[dict] = []
    stats = {"signals": 0, "held": 0, "dropped": 0, "duplicates": 0,
             "drop_reasons": {}, "holds": {}, "themes": {}, "no_customer": 0}

    for cand in candidates:
        verdict, value = decisions[cand["row_id"]]

        if verdict == "drop":
            if value not in DROP_REASONS:
                raise ValueError(f"{cand['row_id']}: unknown drop reason {value!r}")
            stats["dropped"] += 1
            stats["drop_reasons"][value] = stats["drop_reasons"].get(value, 0) + 1
            continue

        if verdict == "hold":
            if not value:
                raise ValueError(f"{cand['row_id']}: hold needs a proposed theme slug")
            if value in valid_themes:
                raise ValueError(
                    f"{cand['row_id']}: held under {value!r}, which already exists "
                    f"in capability-themes.md — decide it as a signal instead")
            stats["held"] += 1
            stats["holds"][value] = stats["holds"].get(value, 0) + 1
            continue

        if value not in valid_themes:
            raise ValueError(
                f"{cand['row_id']}: theme {value!r} is not in capability-themes.md. "
                f"A theme that is not in the vocabulary splits a real theme in two.")

        customer = canonical_customer(cand, by_customer, by_pursuit)
        if not customer:
            stats["no_customer"] += 1
            raise ValueError(
                f"{cand['row_id']}: no customer, and customer is required. Add a "
                f"`pursuit` line to reference/customer-aliases.tsv for "
                f"{cand.get('source_ref')!r}.")

        key = (_norm(cand["requirement"]), _norm(customer))
        if key in seen:
            stats["duplicates"] += 1
            continue
        seen.add(key)

        source_type = cand.get("source_type") or "solicitation"
        if source_type not in SOURCE_TYPES:
            raise ValueError(f"{cand['row_id']}: bad source_type {source_type!r}")
        strength = cand.get("demand_strength_inferred") or "desired"
        if strength not in STRENGTHS:
            raise ValueError(f"{cand['row_id']}: bad demand_strength {strength!r}")

        out.append({
            "schema_version": "demand-signal.v1",
            "signal_id": f"SIG-{counter:04d}",
            "date_observed": cand["date_observed"],
            "source_type": source_type,
            "source_ref": cand["source_ref"],
            "customer": customer,
            "program": cand.get("program"),
            "proposal_slug": None,
            "requirement": cand["requirement"],
            "capability_theme": value,
            "demand_strength": strength,
            "rubric_weight_pct": None,
            "pursuit_value_usd": cand.get("pursuit_value_usd"),
            "our_status": "unknown",
            # Deliberately null — see the module docstring. The exporter has
            # only an opportunity-level risk narrative to offer here.
            "bid_impact": None,
            "evidence_id": None,
            "cto_disposition": None,
            "cto_disposition_detail": None,
            "cto_disposition_date": None,
            "cto_owner": None,
            "notes": (f"capture-pipeline {cand['row_id']}, ingested {ingested_on}; "
                      f"theme adjudicated by hand; our_status pending BD review"),
        })
        counter += 1
        stats["signals"] += 1
        stats["themes"][value] = stats["themes"].get(value, 0) + 1

    return out, stats


def report(stats: dict, new_rows: list[dict], existing: list[dict]) -> None:
    total = stats["signals"] + stats["held"] + stats["dropped"] + stats["duplicates"]
    print(f"adjudicated            : {total}")
    print(f"  promoted as signals  : {stats['signals']}")
    print(f"  already in register  : {stats['duplicates']}")
    print(f"  held, no theme yet   : {stats['held']}")
    print(f"  dropped              : {stats['dropped']}")
    for reason, n in sorted(stats["drop_reasons"].items(), key=lambda kv: -kv[1]):
        print(f"      {reason:<14} {n}")
    if stats["holds"]:
        print()
        print("HELD — a real ask with no theme. Adding one is an edit to")
        print("reference/capability-themes.md, then re-decide these as signals:")
        for slug, n in sorted(stats["holds"].items(), key=lambda kv: -kv[1]):
            print(f"   {slug:<32} {n}")
    if stats["themes"]:
        print()
        print("themes promoted:")
        for theme, n in sorted(stats["themes"].items(), key=lambda kv: -kv[1]):
            print(f"   {theme:<34} {n}")
    if new_rows:
        customers = {r["customer"] for r in new_rows}
        valued = [r for r in new_rows if r.get("pursuit_value_usd")]
        print()
        print(f"register: {len(existing)} -> {len(existing) + len(new_rows)} signals")
        print(f"distinct customers in this batch: {len(customers)}")
        print(f"carrying a pursuit value        : {len(valued)}")
        if new_rows:
            print(f"signal ids                      : {new_rows[0]['signal_id']} "
                  f"- {new_rows[-1]['signal_id']}")


def selftest() -> int:
    themes = ["air-gap-ddil-deployment", "multimodal-audio"]
    cands = [
        {"row_id": "CRM-1-1", "requirement": "Run inference fully air gapped.",
         "date_observed": "2026-05-01", "source_type": "solicitation",
         "source_ref": "crm:opportunity/1", "customer": "DARPA now",
         "program": None, "pursuit_value_usd": 250000,
         "demand_strength_inferred": "mandatory-scored",
         "bid_impact": "a long opportunity-level risk blob"},
        {"row_id": "CRM-1-2", "requirement": "Submit a white paper of 6 pages.",
         "date_observed": "2026-05-01", "source_type": "solicitation",
         "source_ref": "crm:opportunity/1", "customer": "DARPA now",
         "demand_strength_inferred": "desired"},
        {"row_id": "CRM-1-3", "requirement": "Detect anomalies in cargo manifests.",
         "date_observed": "2026-05-01", "source_type": "rfi",
         "source_ref": "crm:opportunity/1", "customer": "DARPA now",
         "demand_strength_inferred": "desired"},
    ]
    decisions = {
        "CRM-1-1": ("signal", "air-gap-ddil-deployment"),
        "CRM-1-2": ("drop", "mechanics"),
        "CRM-1-3": ("hold", "anomaly-detection-analytics"),
    }
    aliases = ({"DARPA now": "DARPA"}, {})
    rows, stats = build(cands, decisions, themes, [], aliases, "2026-08-06")

    assert stats == {**stats, "signals": 1, "held": 1, "dropped": 1, "duplicates": 0}
    r = rows[0]
    assert r["signal_id"] == "SIG-0001", r
    assert r["our_status"] == "unknown", "a CRM signal is never promoted with a status"
    assert r["customer"] == "DARPA", "the alias was not applied"
    assert r["bid_impact"] is None, "the opportunity-level risk blob leaked through"
    assert r["pursuit_value_usd"] == 250000
    assert r["proposal_slug"] is None
    assert "CRM-1-1" in r["notes"]

    # Ids continue from the register rather than restarting.
    rows2, _ = build(cands, decisions, themes, [{"signal_id": "SIG-0128"}],
                     aliases, "2026-08-06")
    assert rows2[0]["signal_id"] == "SIG-0129", rows2[0]

    # Re-running the same export adds nothing.
    rows3, s3 = build(cands, decisions, themes, rows, aliases, "2026-08-06")
    assert rows3 == [] and s3["duplicates"] == 1, (rows3, s3)

    # Every refusal.
    for bad, why in (
        ({"CRM-1-1": ("signal", "air-gap-ddil-deployment")}, "undecided rows"),
        ({**decisions, "CRM-1-1": ("signal", "typo-theme")}, "unknown theme"),
        ({**decisions, "CRM-1-2": ("drop", "because-i-said-so")}, "unknown reason"),
        ({**decisions, "CRM-1-3": ("hold", "multimodal-audio")}, "hold on a real theme"),
        ({**decisions, "CRM-9-9": ("drop", "mechanics")}, "stray decision"),
    ):
        try:
            build(cands, bad, themes, [], aliases, "2026-08-06")
        except ValueError:
            pass
        else:
            raise AssertionError(f"build() accepted {why}")

    # A signal with no customer and no pursuit override is refused, not guessed.
    nc = [{**cands[0], "customer": None}]
    try:
        build(nc, {"CRM-1-1": ("signal", "air-gap-ddil-deployment")}, themes,
              [], ({}, {}), "2026-08-06")
    except ValueError:
        pass
    else:
        raise AssertionError("build() invented a customer")

    by_c, by_p = load_aliases(ALIASES)
    assert by_c.get("DEF ADVANCED RESEARCH PROJECTS AGCY") == "DARPA", "alias file drifted"
    assert by_p.get("crm:opportunity/693") == "NATO", "pursuit override missing"

    print("selftest: ok")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--candidates")
    ap.add_argument("--decisions")
    ap.add_argument("--register", default=str(REGISTER))
    ap.add_argument("--date", help="ingest date recorded in notes (default: today)")
    ap.add_argument("--apply", action="store_true", help="append to the register")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.candidates or not args.decisions:
        ap.error("--candidates and --decisions are both required")

    cand_path, dec_path = Path(args.candidates), Path(args.decisions)
    for p in (cand_path, dec_path):
        if not p.exists():
            print(f"not found: {p}", file=sys.stderr)
            return 1

    candidates = [json.loads(line) for line in
                  cand_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    decisions = load_decisions(dec_path)
    valid = load_valid_themes()
    reg_path = Path(args.register)
    existing = ([json.loads(line) for line in
                 reg_path.read_text(encoding="utf-8").splitlines() if line.strip()]
                if reg_path.exists() else [])

    if args.date:
        ingested_on = args.date
    else:
        from datetime import date
        ingested_on = date.today().isoformat()

    try:
        rows, stats = build(candidates, decisions, valid, existing,
                            load_aliases(), ingested_on)
    except ValueError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1

    report(stats, rows, existing)

    if not args.apply:
        print()
        print("DRY RUN — nothing written. Re-run with --apply.")
        return 0

    with reg_path.open("a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    print()
    print(f"appended {len(rows)} signals to {reg_path.relative_to(WORKSPACE_ROOT).as_posix()}")
    print("Every one carries our_status=unknown. They rank themes; they do not")
    print("assert coverage. Confirmation supplies BD's read.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
