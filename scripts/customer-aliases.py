#!/usr/bin/env python3
"""Report and maintain the customer alias map.

Customer breadth — how many DISTINCT organizations asked for a capability — is the primary
ranking dimension in the demand signal brief. That makes the customer string a ranking input,
not a label: two spellings of one organization double its apparent reach and push a theme up
the list. `reference/customer-aliases.tsv` is the curated fix.

This script never edits that file. It reports what the register currently contains and
PROPOSES grouping candidates for a human to accept by editing the TSV. Deciding that two
government organizations are "the same customer" is a judgment about buying activities and
budgets, and a string-similarity score has no business making it.

Usage:
  python scripts/customer-aliases.py --report     # canonical groupings in force today
  python scripts/customer-aliases.py --suggest    # unmapped names that may be duplicates
  python scripts/customer-aliases.py --impact     # what the map changes in the ranking
  python scripts/customer-aliases.py --selftest

Exit codes:
  0 = success (or selftest passed)
  2 = usage or environment error
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))
import demand_signal_core as core  # noqa: E402

REGISTER = WORKSPACE_ROOT / "signals" / "demand-signals.jsonl"
DISTINCT_FILE = WORKSPACE_ROOT / "reference" / "customer-distinct.tsv"

# Tokens that carry no organizational identity — matching on these produces nonsense pairs
# ("U.S. Army" and "U.S. Navy" share two of three tokens).
STOPWORDS = {
    "u.s.", "us", "the", "of", "and", "department", "office", "command", "center", "centre",
    "agency", "directorate", "systems", "national", "joint", "defense", "defence", "force",
    "forces", "united", "states", "program", "programs", "division", "wing", "group",
}


def tokens(name: str) -> set[str]:
    parts = re.split(r"[^A-Za-z0-9.]+", name.lower())
    return {p for p in parts if p and p not in STOPWORDS and len(p) > 1}


def load_distinct_families(path: Path | None = None) -> list[tuple[str, set[str]]]:
    """Parse reference/customer-distinct.tsv into [(label, {lowercased names}), ...].

    A missing file is not fatal — nothing is suppressed and every candidate is proposed.
    """
    src = path or DISTINCT_FILE
    families: list[tuple[str, set[str]]] = []
    if not src.exists():
        return families
    for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        label = parts[0].strip()
        members = {m.strip().lower() for m in parts[1].split("|") if m.strip()}
        if len(members) >= 2:
            families.append((label, members))
    return families


def suppressed_by(a: str, b: str, families: list[tuple[str, set[str]]]) -> str | None:
    """Return the family label if this pair is a recorded not-a-duplicate decision."""
    la, lb = a.strip().lower(), b.strip().lower()
    for label, members in families:
        if la in members and lb in members:
            return label
    return None


def lead_token(name: str) -> str | None:
    """First significant token, in order — the organizational head of the name."""
    for part in re.split(r"[^A-Za-z0-9.]+", name.lower()):
        if part and part not in STOPWORDS and len(part) > 1:
            return part
    return None


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


def cmd_report(signals: list[dict]) -> int:
    aliases = core.load_customer_aliases(refresh=True)
    groups: dict[str, Counter] = defaultdict(Counter)
    for s in signals:
        raw = s["customer"]
        groups[core.canonical_customer(raw, aliases)][raw] += 1

    raw_count = len({s["customer"] for s in signals})
    print(f"{raw_count} raw customer strings -> {len(groups)} canonical customers "
          f"({len(aliases)} alias rules in force)\n")
    for canon in sorted(groups):
        variants = groups[canon]
        total = sum(variants.values())
        if len(variants) == 1 and canon in variants:
            print(f"  {total:>3}  {canon}")
        else:
            print(f"  {total:>3}  {canon}   <- merged")
            for raw, n in variants.most_common():
                marker = " (canonical)" if raw == canon else ""
                print(f"       {n:>3}  {raw}{marker}")
    return 0


def cmd_suggest(signals: list[dict]) -> int:
    """Propose candidate groupings among names the map does not already merge."""
    aliases = core.load_customer_aliases(refresh=True)
    families = load_distinct_families()
    counts = Counter(s["customer"] for s in signals)
    names = sorted(counts)
    canon = {n: core.canonical_customer(n, aliases) for n in names}

    suppressed = 0
    pairs: list[tuple[float, str, str, str]] = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if canon[a] == canon[b]:
                continue  # already merged by the alias map
            if suppressed_by(a, b, families):
                suppressed += 1
                continue  # recorded as a confirmed-distinct pair
            ta, tb = tokens(a), tokens(b)
            if not ta or not tb:
                continue
            shared = ta & tb
            if not shared:
                continue
            overlap = len(shared) / min(len(ta), len(tb))
            if overlap < 0.5:
                continue
            # A single shared word is only meaningful when it LEADS both names — that is the
            # shape of an org and its sub-unit ("AFRL" / "AFRL Information Directorate").
            # Without this, any two names containing "space" or "army" look identical:
            # "AFRL Space Vehicles Directorate" and "U.S. Space Force" are not the same
            # customer, and a proposal list full of pairs like that stops being read.
            if len(shared) == 1:
                lead_a, lead_b = lead_token(a), lead_token(b)
                if not (lead_a and lead_a == lead_b and lead_a in shared):
                    continue
            if ta == tb:
                why = "identical significant tokens"
            elif ta < tb or tb < ta:
                why = f"one is a superset of the other ({', '.join(sorted(shared))})"
            else:
                why = f"share {', '.join(sorted(shared))}"
            pairs.append((overlap, a, b, why))

    tail = (f" ({suppressed} pair(s) suppressed by reference/customer-distinct.tsv)"
            if suppressed else "")
    if not pairs:
        print(f"No grouping candidates{tail}. Every remaining name looks distinct.")
        return 0

    pairs.sort(key=lambda p: -p[0])
    print(f"{len(pairs)} candidate pair(s){tail}. These are PROPOSALS — nothing is applied.\n")
    print("Merge only if the two names are the same BUYING ACTIVITY. Separate program offices")
    print("inside one agency are separate customers; collapsing them understates real breadth.\n")
    for overlap, a, b, why in pairs:
        print(f"  [{overlap:.2f}] {a!r} ({counts[a]})")
        print(f"         {b!r} ({counts[b]})")
        print(f"         {why}")
    print("\nTo accept one, add a line to reference/customer-aliases.tsv:")
    print("  <raw name><TAB><canonical name><TAB><why>")
    return 0


def cmd_impact(signals: list[dict]) -> int:
    """Show which themes the alias map actually changes, and by how much."""
    aliases = core.load_customer_aliases(refresh=True)
    if not aliases:
        print("No alias rules in force — the map changes nothing.")
        return 0
    per_theme_raw: dict[str, set] = defaultdict(set)
    per_theme_canon: dict[str, set] = defaultdict(set)
    for s in signals:
        per_theme_raw[s["capability_theme"]].add(s["customer"])
        per_theme_canon[s["capability_theme"]].add(core.canonical_customer(s["customer"], aliases))

    changed = [(t, len(per_theme_raw[t]), len(per_theme_canon[t]))
               for t in per_theme_raw if len(per_theme_raw[t]) != len(per_theme_canon[t])]
    if not changed:
        print(f"{len(aliases)} alias rule(s) in force, but no theme's customer count changes.")
        print("The duplicate spellings do not co-occur on any single theme.")
        return 0
    print(f"{len(aliases)} alias rule(s) change the customer count on {len(changed)} theme(s):\n")
    for theme, before, after in sorted(changed, key=lambda x: x[1] - x[2], reverse=True):
        print(f"  {theme:34} {before} -> {after} customers")
    print("\nCustomer breadth is the primary ranking dimension, so these themes were ranked "
          "too high before the map was applied.")
    return 0


def selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "aliases.tsv"
        p.write_text(
            "# comment line ignored\n"
            "\n"
            "AFLCMC\tDAF AFLCMC\tsame org\n"
            "Air Force Life Cycle Management Center\tAFLCMC\tchained alias\n"
            "Loop A\tLoop B\tcycle\n"
            "Loop B\tLoop A\tcycle\n"
            "malformed line with no tab\n",
            encoding="utf-8",
        )
        al = core.load_customer_aliases(p)
        assert al == {
            "aflcmc": "DAF AFLCMC",
            "air force life cycle management center": "AFLCMC",
            "loop a": "Loop B",
            "loop b": "Loop A",
        }, al

        assert core.canonical_customer("AFLCMC", al) == "DAF AFLCMC"
        assert core.canonical_customer("aflcmc", al) == "DAF AFLCMC", "match must be case-insensitive"
        assert core.canonical_customer("  AFLCMC  ", al) == "DAF AFLCMC", "must tolerate whitespace"
        # Chained: Air Force LCMC -> AFLCMC -> DAF AFLCMC, resolved without ordering the file.
        assert core.canonical_customer("Air Force Life Cycle Management Center", al) == "DAF AFLCMC"
        # An unmapped name passes through untouched — never guessed.
        assert core.canonical_customer("DARPA", al) == "DARPA"
        assert core.canonical_customer("", al) == ""
        # A cycle must terminate rather than hang.
        assert core.canonical_customer("Loop A", al) in {"Loop A", "Loop B"}

        # A missing file is not fatal: names pass through.
        assert core.load_customer_aliases(Path(tmp) / "nope.tsv") == {}

    # Tokenizer must not propose nonsense from shared boilerplate.
    assert tokens("U.S. Department of Defense (office unresolved)") == {"unresolved"}, \
        tokens("U.S. Department of Defense (office unresolved)")
    assert not (tokens("U.S. Army") & tokens("U.S. Navy (USW acquisition community)")), \
        "service names must not look similar just because both say U.S."
    assert "afrl" in tokens("AFRL Information Directorate (RI)")
    assert lead_token("AFRL Information Directorate (RI)") == "afrl"
    assert lead_token("U.S. Space Force") == "space", lead_token("U.S. Space Force")
    assert lead_token("U.S. Department of Defense") is None, "all-stopword name has no head"

    # A single shared word only counts when it leads BOTH names. The pair that motivated
    # this rule: these share "space" and are emphatically not the same customer.
    a, b = "AFRL Space Vehicles Directorate (RV)", "U.S. Space Force"
    shared = tokens(a) & tokens(b)
    assert shared == {"space"}, shared
    assert not (lead_token(a) == lead_token(b)), "must be rejected as a candidate"
    # ...while a genuine org/sub-unit pair still passes.
    a2, b2 = "AFRL", "AFRL Information Directorate (RI)"
    assert (tokens(a2) & tokens(b2)) == {"afrl"} and lead_token(a2) == lead_token(b2) == "afrl"

    # Confirmed-distinct families suppress within-family pairs only.
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "distinct.tsv"
        d.write_text(
            "# comment\n"
            "AFRL directorates\tAFRL | AFRL Information Directorate (RI) | AFRL Space Vehicles Directorate (RV)\tdistinct budgets\n"
            "Army commands\tU.S. Army | Army Materiel Command (ACC-CTRS)\tdistinct buying activities\n"
            "too short\tOnly One Name\tignored — a family needs 2+ members\n",
            encoding="utf-8",
        )
        fams = load_distinct_families(d)
        assert [lbl for lbl, _ in fams] == ["AFRL directorates", "Army commands"], fams
        assert suppressed_by("AFRL", "AFRL Information Directorate (RI)", fams) == "AFRL directorates"
        assert suppressed_by("afrl", "  AFRL Space Vehicles Directorate (RV) ", fams), "case/whitespace"
        assert suppressed_by("U.S. Army", "Army Materiel Command (ACC-CTRS)", fams) == "Army commands"
        # Cross-family pairs must STILL be proposed — suppression is not a blanket mute.
        assert suppressed_by("AFRL", "U.S. Army", fams) is None
        assert suppressed_by("DARPA", "CDAO", fams) is None
        assert load_distinct_families(Path(tmp) / "absent.tsv") == []

    # The real files must parse; aliases must not self-map; the two files must not disagree.
    real = core.load_customer_aliases(refresh=True)
    for raw, canon in real.items():
        assert raw != canon.lower(), f"{raw} maps to itself"
    real_fams = load_distinct_families()
    for raw, canon in real.items():
        assert not suppressed_by(raw, canon, real_fams), \
            f"{raw!r} is both aliased to {canon!r} and declared distinct from it"
    print(f"SELFTEST PASS — parsing, case/whitespace, chaining, cycle safety, missing-file "
          f"tolerance, tokenizer sanity, family suppression; {len(real)} live alias rule(s) "
          f"and {len(real_fams)} distinct-family record(s) valid and non-contradictory")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--report", action="store_true", help="canonical groupings in force today")
    g.add_argument("--suggest", action="store_true", help="propose candidate merges (never applies)")
    g.add_argument("--impact", action="store_true", help="which themes the map re-ranks")
    g.add_argument("--selftest", action="store_true", help="deterministic offline self-test")
    args = parser.parse_args()

    if args.selftest:
        return selftest()

    signals = load_register()
    if not signals:
        print(f"Register is empty or missing: {REGISTER}", file=sys.stderr)
        return 2
    if args.suggest:
        return cmd_suggest(signals)
    if args.impact:
        return cmd_impact(signals)
    return cmd_report(signals)


if __name__ == "__main__":
    sys.exit(main())
