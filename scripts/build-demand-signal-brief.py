#!/usr/bin/env python3
"""Build the BD to CTO Demand Signal Brief from the demand signal register.

The register (signals/demand-signals.jsonl) is append-only and grows one customer ask at a
time. This script turns it into a decision, not an inventory.

An inventory of what customers asked for is unusable: nobody prioritizes from a 23-row
leaderboard. So the brief crosses demand against PROOF — what my-company/evidence-ledger.json
can actually substantiate per theme — and leads with the five themes where that gap is widest,
each with the verbatim ask, what it has already cost in a bid, and the one question engineering
needs to answer. Everything else is supporting detail behind it.

It also splits open items into classes that are owned differently: a hard gap is engineering's,
an unproven claim is shared, and a gap in a well-evidenced theme is usually BD not knowing what
we can prove. Routing that third class to engineering is how these reviews lose their audience.

The gap queue in Section 4 carries an EMPTY CTO Disposition column as the write-back channel:
Vincent's shop fills it in the .docx, BD transcribes it into the register. See
docs/BD-CTO-DEMAND-SIGNAL-SYNC.md for the full loop.

Reads:
  signals/demand-signals.jsonl              the append-only register
  reference/capability-themes.md            controlled vocabulary (validation)
  my-company/evidence-ledger.json           approved evidence, for the proof side of exposure
  signals/briefs/<prev>-brief-state.json    prior brief snapshot, for the diff section

Writes:
  signals/briefs/<today>-demand-signal-brief.md    the brief
  signals/briefs/<today>-brief-state.json          snapshot for the next brief's diff

Usage:
  python scripts/build-demand-signal-brief.py
  python scripts/build-demand-signal-brief.py --since 2026-07-01
  python scripts/build-demand-signal-brief.py --validate-only
  python scripts/build-demand-signal-brief.py --selftest

Exit codes:
  0 = brief written (or selftest / validation passed)
  1 = register empty or missing
  2 = usage error, or a validation failure that makes the brief untrustworthy
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))
import demand_signal_core as core  # noqa: E402  (needs WORKSPACE_ROOT on the path first)

REGISTER = WORKSPACE_ROOT / "signals" / "demand-signals.jsonl"
BRIEFS_DIR = WORKSPACE_ROOT / "signals" / "briefs"
THEMES_FILE = WORKSPACE_ROOT / "reference" / "capability-themes.md"

OPEN_STATUSES = {"gap", "no-plan"}
STRENGTH_ORDER = {"mandatory-passfail": 0, "mandatory-scored": 1, "desired": 2, "curiosity": 3}
VALID_STATUS = {"shipping", "prototype", "roadmap", "gap", "no-plan", "unknown"}
VALID_DISPOSITION = {"already-exists-ask-me", "building", "planned", "needs-scoping", "wont-build"}
VALID_SOURCE_TYPE = {
    "solicitation", "rfi", "industry-day", "conference", "one-on-one",
    "trial", "demo-feedback", "debrief", "partner",
}
# Sources where the customer said it out loud rather than writing it into a document.
VERBAL_SOURCES = {"conference", "one-on-one", "trial", "demo-feedback", "debrief", "industry-day"}


def load_valid_themes() -> list[str]:
    if not THEMES_FILE.exists():
        print(f"ERROR: missing {THEMES_FILE.name}", file=sys.stderr)
        raise SystemExit(2)
    themes = [
        m.group(1)
        for m in (re.match(r"^\|\s*`([a-z0-9-]+)`\s*\|", line)
                  for line in THEMES_FILE.read_text(encoding="utf-8", errors="replace").splitlines())
        if m
    ]
    if not themes:
        print(f"ERROR: no themes parsed from {THEMES_FILE.name}", file=sys.stderr)
        raise SystemExit(2)
    return themes


def load_register(path: Path) -> list[dict]:
    if not path.exists():
        return []
    signals = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            print(f"WARNING: skipping malformed line {line_no} in {path.name}", file=sys.stderr)
            continue
        if isinstance(rec, dict):
            signals.append(rec)
    return signals


def validate(signals: list[dict], valid_themes: list[str]) -> list[str]:
    """Return a list of problems. Unknown themes are fatal: a typo silently splits a theme
    in two and understates its weight, which is the one error that corrupts the ranking."""
    problems: list[str] = []
    seen_ids: set[str] = set()
    theme_set = set(valid_themes)
    for rec in signals:
        sid = rec.get("signal_id", "<missing>")
        if sid in seen_ids:
            problems.append(f"{sid}: duplicate signal_id")
        seen_ids.add(sid)
        for field in ("signal_id", "date_observed", "source_type", "source_ref",
                      "customer", "requirement", "capability_theme", "demand_strength", "our_status"):
            if not rec.get(field):
                problems.append(f"{sid}: missing required field '{field}'")
        theme = rec.get("capability_theme")
        if theme and theme not in theme_set:
            problems.append(f"{sid}: unknown capability_theme '{theme}' (not in reference/capability-themes.md)")
        if rec.get("our_status") and rec["our_status"] not in VALID_STATUS:
            problems.append(f"{sid}: invalid our_status '{rec['our_status']}'")
        if rec.get("source_type") and rec["source_type"] not in VALID_SOURCE_TYPE:
            problems.append(f"{sid}: invalid source_type '{rec['source_type']}'")
        disp = rec.get("cto_disposition")
        if disp and disp not in VALID_DISPOSITION:
            problems.append(f"{sid}: invalid cto_disposition '{disp}'")
        if rec.get("date_observed"):
            try:
                date.fromisoformat(rec["date_observed"])
            except ValueError:
                problems.append(f"{sid}: date_observed '{rec['date_observed']}' is not ISO-8601")
    return problems


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def theme_rollup(signals: list[dict]) -> list[dict]:
    themes: dict[str, dict] = {}
    for rec in signals:
        t = rec["capability_theme"]
        row = themes.setdefault(t, {
            "theme": t, "total": 0, "mandatory": 0, "open": 0, "verbal": 0,
            "weighted_usd": 0.0, "rubric_pts": 0.0, "customers": set(), "dispositioned": 0,
        })
        row["total"] += 1
        if rec["demand_strength"].startswith("mandatory"):
            row["mandatory"] += 1
        if rec["our_status"] in OPEN_STATUSES:
            row["open"] += 1
        if rec["source_type"] in VERBAL_SOURCES:
            row["verbal"] += 1
        row["weighted_usd"] += float(rec.get("pursuit_value_usd") or 0)
        row["rubric_pts"] += float(rec.get("rubric_weight_pct") or 0)
        row["customers"].add(core.canonical_customer(rec["customer"]))
        if rec.get("cto_disposition"):
            row["dispositioned"] += 1
    rows = list(themes.values())
    for row in rows:
        row["customer_count"] = len(row["customers"])
        row["customers"] = sorted(row["customers"])
    # Rank by breadth of customers first: three agencies asking beats one agency asking
    # three times, which is the distinction a raw count hides.
    rows.sort(key=lambda r: (-r["customer_count"], -r["mandatory"], -r["total"]))
    return rows


def find_disagreements(signals: list[dict]) -> list[dict]:
    """BD and engineering holding different views of the same capability. Both directions
    are actionable, and they route to different owners."""
    out = []
    for rec in signals:
        status, disp = rec["our_status"], rec.get("cto_disposition")
        if not disp:
            continue
        kind = None
        if status in OPEN_STATUSES and disp == "already-exists-ask-me":
            kind = "BD bid it as a gap; engineering says it exists (enablement problem, not engineering)"
        elif status == "shipping" and disp in {"needs-scoping", "building"}:
            kind = "BD is claiming it today; engineering does not consider it done (claim risk)"
        elif status == "roadmap" and disp == "wont-build":
            kind = "BD is promising a roadmap engineering has dropped (claim risk)"
        elif status == "shipping" and disp == "wont-build":
            kind = "BD is claiming a capability engineering will not carry (claim risk)"
        if kind:
            out.append({**rec, "disagreement": kind})
    return out


def days_since(iso: str, today: date) -> int:
    try:
        return (today - date.fromisoformat(iso)).days
    except ValueError:
        return 0


def median(values: list[int]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2


def pursuit_key(signal: dict) -> str | None:
    """What pursuit this ask came from, or None if it came from no pursuit.

    Matrix-backed signals carry `proposal_slug`. Capture-pipeline signals never
    will — the pursuit never became a proposal here, which is the entire point
    of that feeder — but they carry `crm:opportunity/<id>`, which identifies the
    pursuit just as well. Counting only slugs reported "244 asks across 11
    pursuits" on a register where 116 of the asks came from 30 other ones.

    Conference and one-on-one signals may legitimately have neither. Those are
    not pursuits and must not be counted as though they were.
    """
    slug = signal.get("proposal_slug")
    if slug:
        return str(slug)
    ref = str(signal.get("source_ref") or "")
    return ref if ref.startswith("crm:opportunity/") else None


def compute_metrics(signals: list[dict], today: date) -> dict:
    open_signals = [s for s in signals if s["our_status"] in OPEN_STATUSES]
    undispositioned = [s for s in open_signals if not s.get("cto_disposition")]
    pursuits = {k for k in (pursuit_key(s) for s in signals) if k}
    impacted = {s.get("proposal_slug") for s in open_signals if s.get("bid_impact") and s.get("proposal_slug")}
    disposition_pct = (
        100.0 * (len(open_signals) - len(undispositioned)) / len(open_signals) if open_signals else 0.0
    )
    return {
        "total_signals": len(signals),
        "pursuits": len(pursuits),
        "signals_per_pursuit": round(len(signals) / len(pursuits), 1) if pursuits else 0.0,
        "open_gaps": len(open_signals),
        "undispositioned": len(undispositioned),
        "disposition_pct": round(disposition_pct, 1),
        "median_gap_age_days": median([days_since(s["date_observed"], today) for s in undispositioned]),
        "impacted_pursuits": len(impacted),
        "impacted_slugs": sorted(x for x in impacted if x),
        "verbal_share_pct": round(
            100.0 * sum(1 for s in signals if s["source_type"] in VERBAL_SOURCES) / len(signals), 1
        ) if signals else 0.0,
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def esc(text: str | None) -> str:
    """Keep cell text from breaking the markdown table."""
    if not text:
        return ""
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def truncate(text: str | None, limit: int) -> str:
    t = esc(text)
    return t if len(t) <= limit else t[: limit - 1].rstrip() + "…"


def usd(amount: float) -> str:
    if not amount:
        return "—"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    return f"${amount / 1_000:.0f}K"


# The new-signal appendix lists examples, not the whole register — a brief nobody finishes is
# a brief nobody acts on. The cap is always stated in the text so a truncated list never reads
# as a complete one.
SECTION5_PER_THEME_CAP = 3


def triage_signals(signals: list[dict], exposure_by_theme: dict[str, dict]) -> dict[str, list[dict]]:
    """Bucket every signal into its decision class, ordered worst-first within each class."""
    out: dict[str, list[dict]] = {
        "hard-gap": [], "unproven-claim": [], "enablement": [], "proven": [], "unclassified": [],
    }
    for sig in signals:
        proof = exposure_by_theme.get(sig["capability_theme"], {}).get("proof", "none")
        out[core.classify_signal(sig, proof)].append(sig)
    for rows in out.values():
        rows.sort(key=lambda s: (STRENGTH_ORDER.get(s["demand_strength"], 9), s["date_observed"]))
    return out


def pick_representative_ask(signals: list[dict], theme: str) -> dict | None:
    """The ask that best speaks for a theme: hardest demand strength, then most recent.

    Verbatim customer language does the persuading here. A paraphrase of five merged asks
    reads like BD's opinion, which is exactly what engineering discounts.
    """
    candidates = [s for s in signals if s["capability_theme"] == theme]
    if not candidates:
        return None
    return sorted(
        candidates,
        key=lambda s: (STRENGTH_ORDER.get(s["demand_strength"], 9), _neg_date(s["date_observed"])),
    )[0]


def _neg_date(iso: str) -> str:
    """Sort dates descending inside an ascending tuple sort."""
    return "".join(chr(ord("9") - int(c)) if c.isdigit() else c for c in iso)


def decision_ask(row: dict) -> str:
    """The specific question to put to engineering for this theme's dominant class."""
    classes = row["classes"]
    if classes.get("hard-gap"):
        return ("Build, or confirm `wont-build` so BD teams for it instead of hedging. "
                "Either answer is useful; silence is not.")
    if classes.get("unproven-claim"):
        return ("Confirm whether this is real and citable. If it is, it needs a ledger entry so "
                "proposals can use it; if it is not, BD stops claiming it.")
    if row["proof"] == "none":
        return ("Name what covers this today, or tell us nothing does. Recurring demand with no "
                "ledger evidence is where over-claiming starts.")
    if row["hedges"] and row["proof"] == "strong":
        # Theme-level evidence plus a bid we still had to hedge means the shortfall is narrower
        # than the theme. Telling engineering "BD missed it" would be wrong as often as right.
        return ("The theme is well evidenced but these specific asks still cost us a hedge. "
                "Confirm whether the specific capability exists and is citable, or whether it is "
                "genuinely out of scope so BD stops reaching for it.")
    if classes.get("enablement"):
        return ("Point BD at what already covers this — the ledger suggests we can, and BD bid it "
                "as a gap.")
    return "Confirm the theme is on the roadmap and name an owner."


def render_brief(signals: list[dict], since: str | None, prior_state: dict | None, today: date,
                 full: bool = False, ledger: list[dict] | None = None) -> str:
    new_signals = [s for s in signals if not since or s["date_observed"] >= since]
    themes = theme_rollup(signals)
    disagreements = find_disagreements(signals)
    metrics = compute_metrics(signals, today)
    valid_themes = core.load_valid_themes()
    ledger = core.load_ledger() if ledger is None else ledger
    exposure = core.compute_exposure(signals, valid_themes, ledger)
    exposure_by_theme = {r["theme"]: r for r in exposure}
    triage = triage_signals(signals, exposure_by_theme)

    open_signals = sorted(
        (s for s in signals if s["our_status"] in OPEN_STATUSES),
        key=lambda s: (
            bool(s.get("cto_disposition")),
            STRENGTH_ORDER.get(s["demand_strength"], 9),
            s["date_observed"],
        ),
    )

    L: list[str] = []
    A = L.append
    A("# Demand Signal Brief")
    A("")
    period = f"new since {since}" if since else "all signals to date"
    A(f"**Date:** {today.isoformat()} · **Coverage:** {period} · "
      f"**Register:** `signals/demand-signals.jsonl` ({metrics['total_signals']} signals)")
    A("")
    A("**For:** <CTO> and the CTO shop · **From:** BD / Capture · "
      "**Action required:** answer the decisions in Section 1")
    A("")
    A(f"{metrics['total_signals']} customer asks recorded across {metrics['pursuits']} pursuits, "
      "each traceable to a document or a dated note. This brief is not an inventory of them. It "
      "crosses what customers asked against what the evidence ledger can actually substantiate, "
      "and reports where that gap is widest. Sections 1 and 2 are the decisions; everything after "
      "is the supporting detail.")
    A("")

    # 1. The decision list — the whole point of the brief.
    A("## 1. Decisions we need from the CTO shop")
    A("")
    decisions = [r for r in exposure if r["exposure"] > 0][:5]
    if not decisions:
        A("No theme currently shows exposure: every recurring ask is either evidenced or already "
          "dispositioned. Nothing needed this period.")
        A("")
    else:
        A(f"{len(decisions)} of {len(exposure)} themes carry real exposure — recurring demand the "
          "ledger cannot substantiate, or demand that has already cost us something in a bid. "
          "Ranked worst first. Each needs one word back from you plus an owner.")
        A("")
        for i, row in enumerate(decisions, 1):
            ask = pick_representative_ask(signals, row["theme"])
            A(f"### 1.{i} `{row['theme']}` — exposure {row['exposure']}")
            A("")
            A(f"- **Who is asking:** {row['customer_count']} customer(s) — "
              f"{', '.join(row['customers'][:5])}. {row['mandatory']} of {row['signals']} asks were "
              "mandatory or scored.")
            if ask:
                A(f"- **What they asked (verbatim):** \"{truncate(ask['requirement'], 200)}\" "
                  f"({esc(ask['customer'])}, {ask['date_observed']}, `{ask['signal_id']}`)")
            proof_phrase = {
                "none": "**nothing in the evidence ledger** carries this theme",
                "weak": f"only {row['evidence_count']} ledger item(s) touch it, which is one "
                        "anecdote rather than proof across varied asks",
                "strong": f"{row['evidence_count']} ledger items cover it",
            }[row["proof"]]
            A(f"- **What we can prove:** {proof_phrase}"
              + (f" ({', '.join(row['evidence_ids'])})" if row["evidence_ids"] else "") + ".")
            if row["hedges"]:
                A(f"- **What it has already cost:** {row['hedges']} bid(s) hedged, teamed, or "
                  "declined on this theme:")
                for ex in row["examples"][:3]:
                    A(f"    - {esc(ex['customer'])} / {esc(ex.get('program') or '')} "
                      f"(`{ex['signal_id']}`): {truncate(ex['bid_impact'], 160)}")
            A(f"- **What we need from you:** {decision_ask(row)}")
            A("")

    # 2. Triage — the three classes, owned differently.
    A("## 2. What the open items actually are")
    A("")
    A("Every ask we could not answer, split by who owns the fix. The distinction matters: only "
      "the first two classes are engineering's, and sending the third to engineering is how these "
      "reviews lose their audience.")
    A("")
    A("| Class | Count | Whose problem | What it means |")
    A("|---|---|---|---|")
    A(f"| Hard gap | {len(triage['hard-gap'])} | Engineering | We told the customer no, and the "
      "ledger has nothing for the theme. Build, team, or decline on purpose. |")
    A(f"| Unproven claim | {len(triage['unproven-claim'])} | Engineering + BD | We said yes and "
      "the ledger cannot back it. Confirm it is real, or BD stops claiming it. |")
    A(f"| Possible enablement miss | {len(triage['enablement'])} | BD, not engineering | BD "
      "recorded a gap in a theme the ledger evidences well. Likely a communication failure — "
      "confirm against the specific ask before spending engineering time. |")
    A(f"| Unresolved status | {len(triage['unclassified'])} | BD | Backfill artifact: status was "
      "never set. Not an action item for you. |")
    A("")
    for cls, heading in (("hard-gap", "Hard gaps"),
                         ("unproven-claim", "Unproven claims"),
                         ("enablement", "Possible enablement misses")):
        rows = triage[cls]
        if not rows:
            continue
        A(f"**{heading}**")
        A("")
        for s in rows[: (99 if full else 8)]:
            A(f"- `{s['signal_id']}` {esc(s['customer'])} · `{s['capability_theme']}` — "
              f"{truncate(s['requirement'], 130)}")
        if not full and len(rows) > 8:
            A(f"- _...and {len(rows) - 8} more; `--full` lists them_")
        A("")

    # 3. Exposure map — all themes, with the arithmetic visible.
    A("## 3. Exposure map")
    A("")
    A("Every theme in the register. **Exposure** = customers × (1 + mandatory share) × proof "
      "deficit, plus 2 per bid already hedged. Proof deficit is 1.0 when the ledger holds nothing, "
      "0.5 when it holds one or two items, 0 when three or more corroborate. The arithmetic is "
      "deliberately simple enough to check by eye.")
    A("")
    A("| Capability theme | Exposure | Customers | Signals | Mandatory | Ledger items | Proof | Bids hedged |")
    A("|---|---|---|---|---|---|---|---|")
    for row in exposure:
        A(f"| `{row['theme']}` | {row['exposure']} | {row['customer_count']} | {row['signals']} | "
          f"{row['mandatory']} | {row['evidence_count']} | {row['proof']} | {row['hedges']} |")
    A("")
    untagged = [t for t in core.untagged_themes(valid_themes) if t in exposure_by_theme]
    if untagged:
        A("**No evidence-tag mapping exists for:** " + ", ".join(f"`{t}`" for t in untagged) +
          ". These read as unproven by construction. That is correct where the ledger genuinely "
          "holds nothing, and a mapping bug where it does not — worth a look before acting on "
          "their rank.")
        A("")
    A(f"Context: {metrics['verbal_share_pct']}% of signals came from verbal sources (conference, "
      f"one-on-one, trial, debrief), which lead the written requirement by months. "
      f"{metrics['undispositioned']} open items still have no engineering answer, median age "
      f"{metrics['median_gap_age_days']:.0f} days.")
    A("")
    multi = [r for r in themes if r["customer_count"] >= 3]
    if multi:
        A("**Asked by three or more customers:** "
          + ", ".join(f"`{r['theme']}` ({', '.join(r['customers'][:4])})" for r in multi[:6]) + ".")
        A("")

    # 3. Gap queue — the write-back surface
    A("## 4. Open gap queue — write-back surface")
    A("")
    A("Every ask we could not answer. **Fill in the last two columns.** `wont-build` is a "
      "useful answer: it tells BD to team for the theme instead of hedging, earlier and more "
      "cheaply.")
    A("")
    A("| Signal | Age | Customer | The ask | Theme | Strength | What it cost us | CTO disposition | Owner |")
    A("|---|---|---|---|---|---|---|---|---|")
    for s in open_signals:
        age = days_since(s["date_observed"], today)
        A(f"| {s['signal_id']} | {age}d | {esc(s['customer'])} | {truncate(s['requirement'], 110)} | "
          f"`{s['capability_theme']}` | {s['demand_strength'].replace('mandatory-', 'mand-')} | "
          f"{truncate(s.get('bid_impact'), 90)} | {esc(s.get('cto_disposition')) or ''} | "
          f"{esc(s.get('cto_owner')) or ''} |")
    if not open_signals:
        A("| — | | | No open gaps in the register. | | | | | |")
    A("")

    # 4. Disagreements
    A("## 5. Disagreements")
    A("")
    if disagreements:
        A("Rows where BD's read and engineering's disposition do not match. These are the only "
          "items that need meeting time.")
        A("")
        A("| Signal | The ask | BD status | CTO disposition | Why it matters |")
        A("|---|---|---|---|---|")
        for s in disagreements:
            A(f"| {s['signal_id']} | {truncate(s['requirement'], 90)} | `{s['our_status']}` | "
              f"`{s['cto_disposition']}` | {esc(s['disagreement'])} |")
    else:
        A("None recorded. This is expected until the first round of dispositions comes back; "
          "an empty section here after dispositions exist is a good sign, not a missing one.")
    A("")

    # 5. New since last brief
    A("## 6. New signals this period")
    A("")
    if new_signals:
        by_theme: dict[str, list[dict]] = {}
        for s in new_signals:
            by_theme.setdefault(s["capability_theme"], []).append(s)
        if not since:
            A(f"First brief — this is the whole register ({len(new_signals)} signals across "
              f"{len(by_theme)} themes), so the list below shows examples per theme rather than "
              "every row. Section 2 counts all of them; the register itself is complete.")
            A("")
        if not full:
            A(f"Up to {SECTION5_PER_THEME_CAP} shown per theme. Withheld rows are counted, never "
              "silently dropped — run with `--full` for the complete list.")
            A("")
        for theme in sorted(by_theme, key=lambda t: -len(by_theme[t])):
            rows = sorted(by_theme[theme], key=lambda x: x["date_observed"], reverse=True)
            shown = rows if full else rows[:SECTION5_PER_THEME_CAP]
            A(f"**`{theme}`** ({len(rows)})")
            A("")
            for s in shown:
                prog = f" / {s['program']}" if s.get("program") else ""
                A(f"- `{s['signal_id']}` {s['date_observed']} · {esc(s['customer'])}{esc(prog)} "
                  f"({s['source_type']}, {s['demand_strength']}, our status `{s['our_status']}`) — "
                  f"{truncate(s['requirement'], 180)}")
            if len(rows) > len(shown):
                A(f"- _...and {len(rows) - len(shown)} more in the register_")
            A("")
    else:
        A("No new signals this period.")
        A("")

    # 6. Diff
    A("## 7. Change since the last brief")
    A("")
    if prior_state:
        A(f"Prior brief: {prior_state.get('date', 'unknown')} "
          f"({prior_state.get('total_signals', 0)} signals, "
          f"{prior_state.get('undispositioned', 0)} undispositioned gaps).")
        A("")
        prior_themes = prior_state.get("theme_totals", {})
        movers = []
        for row in themes:
            delta = row["total"] - prior_themes.get(row["theme"], 0)
            if delta:
                movers.append((row["theme"], delta, row["theme"] not in prior_themes))
        movers.sort(key=lambda m: -m[1])
        if movers:
            A("| Theme | New signals | Note |")
            A("|---|---|---|")
            for theme, delta, is_new in movers:
                A(f"| `{theme}` | +{delta} | {'new theme this period' if is_new else ''} |")
            A("")
        delta_disp = prior_state.get("undispositioned", 0) - metrics["undispositioned"]
        if delta_disp > 0:
            A(f"Gaps answered since the last brief: **{delta_disp}**.")
        elif delta_disp < 0:
            A(f"Undispositioned gaps grew by **{abs(delta_disp)}**. The queue is filling faster "
              "than it is being answered.")
        else:
            A("No change in the undispositioned gap count.")
        A("")
    else:
        A("This is the first brief. Subsequent briefs diff against the prior snapshot.")
        A("")

    # 7. How to answer
    A("## 8. How to answer")
    A("")
    A("Answer the Section 1 decisions directly, or fill the CTO Disposition and Owner columns "
      "in Section 4 of this document. One of:")
    A("")
    A("| Disposition | Means |")
    A("|---|---|")
    A("| `already-exists-ask-me` | We have this today and BD did not know. Name what covers it. |")
    A("| `building` | In active development. |")
    A("| `planned` | Committed to a quarter. Say which. |")
    A("| `needs-scoping` | Cannot answer yet; needs an engineering conversation. |")
    A("| `wont-build` | Not carrying it. BD will team for it instead. |")
    A("")
    A("BD transcribes your answers back into the register and, when a capability becomes "
      "provable, adds it to `my-company/evidence-ledger.json` so proposals can cite it and the "
      "pre-submit gates protect it. A capability that exists but is not in the ledger is "
      "invisible to the proposal pipeline, which means we do not get credit for it.")
    A("")
    return "\n".join(L) + "\n"


def build_state(signals: list[dict], today: date) -> dict:
    themes = theme_rollup(signals)
    metrics = compute_metrics(signals, today)
    return {
        "date": today.isoformat(),
        "total_signals": metrics["total_signals"],
        "open_gaps": metrics["open_gaps"],
        "undispositioned": metrics["undispositioned"],
        "theme_totals": {r["theme"]: r["total"] for r in themes},
        "max_signal_id": max((s["signal_id"] for s in signals), default=None),
    }


def find_prior_state() -> dict | None:
    if not BRIEFS_DIR.exists():
        return None
    states = sorted(BRIEFS_DIR.glob("*-brief-state.json"))
    if not states:
        return None
    try:
        return json.loads(states[-1].read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def render_docx(md_path: Path) -> None:
    renderer = WORKSPACE_ROOT / "scripts" / "render-md-to-docx.py"
    if not renderer.exists():
        return
    try:
        result = subprocess.run(
            [sys.executable, str(renderer), str(md_path)],
            capture_output=True, text=True, timeout=180,
        )
        if result.returncode == 0:
            print(f"Rendered .docx alongside {md_path.name}")
        else:
            print(f"WARNING: .docx render failed: {result.stderr.strip()[:300]}", file=sys.stderr)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"WARNING: could not run the .docx renderer: {exc}", file=sys.stderr)


def selftest() -> int:
    valid = load_valid_themes()
    today = date(2026, 8, 15)
    signals = [
        {
            "schema_version": "demand-signal.v1", "signal_id": "SIG-0001",
            "date_observed": "2026-07-01", "source_type": "solicitation",
            "source_ref": "proposals/x/working/requirement-matrix.md#R1", "customer": "DIA",
            "program": "DMA", "proposal_slug": "x",
            "requirement": "Support progressive model upgrades across the air gap.",
            "capability_theme": "cross-domain-model-update", "demand_strength": "mandatory-scored",
            "rubric_weight_pct": 10, "pursuit_value_usd": 2_000_000, "our_status": "gap",
            "bid_impact": "Bid the path, not the capability.", "cto_disposition": None,
        },
        {
            "schema_version": "demand-signal.v1", "signal_id": "SIG-0002",
            "date_observed": "2026-08-10", "source_type": "conference",
            "source_ref": "proposals/y/inputs/06_notes/notes.md", "customer": "USSOCOM",
            "program": None, "proposal_slug": "y",
            "requirement": "Move model updates into a closed enclave without a network path.",
            "capability_theme": "cross-domain-model-update", "demand_strength": "curiosity",
            "our_status": "gap", "bid_impact": None,
            "cto_disposition": "already-exists-ask-me", "cto_owner": "Vincent",
        },
        {
            "schema_version": "demand-signal.v1", "signal_id": "SIG-0003",
            "date_observed": "2026-08-12", "source_type": "one-on-one",
            "source_ref": "scrubs/daily-2026-08-12.md", "customer": "Army FCC",
            "requirement": "Cite the doctrine paragraph behind every answer.",
            "capability_theme": "output-verification-attribution", "demand_strength": "desired",
            "our_status": "shipping", "cto_disposition": "needs-scoping",
        },
    ]
    problems = validate(signals, valid)
    assert not problems, f"clean fixture should validate, got {problems}"

    bad = [dict(signals[0], signal_id="SIG-0004", capability_theme="made-up-theme")]
    assert any("unknown capability_theme" in p for p in validate(bad, valid)), "typo theme must be caught"
    dupes = [signals[0], dict(signals[0])]
    assert any("duplicate signal_id" in p for p in validate(dupes, valid)), "duplicate ids must be caught"

    themes = theme_rollup(signals)
    top = themes[0]
    assert top["theme"] == "cross-domain-model-update", f"got {top['theme']}"
    assert top["customer_count"] == 2 and top["total"] == 2 and top["open"] == 2, top
    assert top["verbal"] == 1, f"conference signal should count as verbal, got {top['verbal']}"

    dis = find_disagreements(signals)
    kinds = {d["signal_id"] for d in dis}
    assert kinds == {"SIG-0002", "SIG-0003"}, f"expected two disagreements, got {kinds}"

    m = compute_metrics(signals, today)
    assert m["open_gaps"] == 2 and m["undispositioned"] == 1, m
    assert m["disposition_pct"] == 50.0, m
    assert m["median_gap_age_days"] == 45, m
    assert m["impacted_pursuits"] == 1, m
    # Two slugs; the scrub note is not a pursuit and must not inflate the count.
    assert m["pursuits"] == 2, m

    # A capture-pipeline signal has no slug but is still a pursuit, and two asks
    # from the same opportunity are one pursuit, not two.
    crm = [dict(signals[0], signal_id=f"SIG-01{n}", proposal_slug=None,
                source_ref="crm:opportunity/605") for n in (29, 30)]
    m2 = compute_metrics(signals + crm, today)
    assert m2["pursuits"] == 3, f"CRM pursuits are invisible to the count: {m2}"
    assert {pursuit_key(s) for s in crm} == {"crm:opportunity/605"}
    assert pursuit_key(signals[2]) is None, "a scrub note is not a pursuit"

    brief = render_brief(signals, since="2026-08-01", prior_state={
        "date": "2026-08-01", "total_signals": 1, "undispositioned": 1,
        "theme_totals": {"cross-domain-model-update": 1},
    }, today=today)
    for expected in ("# Demand Signal Brief", "## 4. Open gap queue — write-back surface", "SIG-0001",
                     "cross-domain-model-update", "## 5. Disagreements", "+1"):
        assert expected in brief, f"brief missing {expected!r}"
    assert "SIG-0003" in brief, "shipping-vs-needs-scoping disagreement must surface"
    # Section 5 covers the period only.
    section5 = brief.split("## 6. New signals this period")[1].split("## 7.")[0]
    assert "SIG-0002" in section5 and "SIG-0001" not in section5, "since filter is not applied"

    # A capped Section 5 must say so and must count what it withheld.
    many = [dict(signals[2], signal_id=f"SIG-{i:04d}", date_observed="2026-08-11") for i in range(10, 20)]
    capped = render_brief(signals + many, since="2026-08-01", prior_state=None, today=today)
    body = capped.split("## 6. New signals this period")[1].split("## 7.")[0]
    assert "and 8 more in the register" in body, "withheld rows must be counted in the text"
    uncapped = render_brief(signals + many, since="2026-08-01", prior_state=None, today=today, full=True)
    ubody = uncapped.split("## 6. New signals this period")[1].split("## 7.")[0]
    assert "more in the register" not in ubody, "--full must not truncate"
    assert ubody.count("SIG-00") >= 11, "--full must list every signal"

    # --- Decision-first sections -------------------------------------------------------
    valid = load_valid_themes()
    # A theme with no ledger evidence and a hedged bid must outrank a well-evidenced one.
    fake_ledger = [
        {"id": "EV-001", "approval_status": "approved", "proof_strength": "high",
         "relevance_tags": ["ground-truth"], "summary": "verification"},
        {"id": "EV-002", "approval_status": "approved", "proof_strength": "high",
         "relevance_tags": ["wbom"], "summary": "receipts"},
        {"id": "EV-003", "approval_status": "approved", "proof_strength": "highest",
         "relevance_tags": ["icd-203"], "summary": "tradecraft"},
        {"id": "EV-004", "approval_status": "retired", "proof_strength": "highest",
         "relevance_tags": ["upgrades"], "summary": "retired item must not count"},
    ]
    exp = core.compute_exposure(signals, valid, fake_ledger)
    by_theme = {r["theme"]: r for r in exp}
    assert by_theme["output-verification-attribution"]["proof"] == "strong", by_theme["output-verification-attribution"]
    assert by_theme["cross-domain-model-update"]["proof"] == "none", \
        "a retired ledger item must not count as proof"
    assert exp[0]["theme"] == "cross-domain-model-update", \
        f"unevidenced + hedged theme must rank first, got {exp[0]['theme']}"

    # Both cross-domain asks are gaps in a theme with no ledger evidence: hard gaps.
    tri = triage_signals(signals, by_theme)
    assert [s["signal_id"] for s in tri["hard-gap"]] == ["SIG-0001", "SIG-0002"], tri["hard-gap"]
    assert [s["signal_id"] for s in tri["proven"]] == ["SIG-0003"], tri["proven"]

    # The same gap status in a WELL-EVIDENCED theme is an enablement miss, not engineering's
    # problem — the distinction the triage exists to draw.
    enable_fixture = signals + [dict(
        signals[2], signal_id="SIG-0099", our_status="gap",
        capability_theme="output-verification-attribution",
    )]
    tri2 = triage_signals(enable_fixture, {r["theme"]: r for r in
                                           core.compute_exposure(enable_fixture, valid, fake_ledger)})
    assert [s["signal_id"] for s in tri2["enablement"]] == ["SIG-0099"], tri2["enablement"]
    assert "SIG-0099" not in [s["signal_id"] for s in tri2["hard-gap"]], \
        "a gap in a proven theme must not be routed to engineering as a hard gap"

    rep = pick_representative_ask(signals, "cross-domain-model-update")
    assert rep["signal_id"] == "SIG-0001", "mandatory ask must outrank the newer curiosity ask"
    assert "wont-build" in decision_ask(by_theme["cross-domain-model-update"])

    decision_brief = render_brief(signals, since=None, prior_state=None, today=today,
                                  ledger=fake_ledger)
    for expected in ("## 1. Decisions we need from the CTO shop", "exposure ",
                     "## 2. What the open items actually are", "Hard gap",
                     "Possible enablement miss", "## 3. Exposure map",
                     "nothing in the evidence ledger", "Bid the path"):
        assert expected in decision_brief, f"decision sections missing {expected!r}"
    # The unevidenced theme must be the FIRST decision, not buried.
    first = decision_brief.split("### 1.1 ")[1].split("\n")[0]
    assert "cross-domain-model-update" in first, f"decision 1.1 is {first!r}"

    state = build_state(signals, today)
    assert state["max_signal_id"] == "SIG-0003" and state["total_signals"] == 3, state
    assert esc("a|b") == "a\\|b", "pipe must be escaped or the table breaks"

    print(f"SELFTEST PASS — {len(valid)} themes, validation + rollup + disagreement + "
          "metrics + render + diff verified")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--since", help="ISO date; Section 5 lists signals observed on or after it "
                                        "(default: the prior brief's date)")
    parser.add_argument("--register", help="alternate register path (testing)")
    parser.add_argument("--validate-only", action="store_true", help="validate the register and exit")
    parser.add_argument("--full", action="store_true",
                        help="list every signal in Section 5 instead of capping per theme")
    parser.add_argument("--selftest", action="store_true", help="run the embedded deterministic self-test")
    args = parser.parse_args()

    if args.selftest:
        return selftest()

    register = Path(args.register) if args.register else REGISTER
    valid_themes = load_valid_themes()
    signals = load_register(register)
    if not signals:
        print(f"Register is empty or missing: {register}", file=sys.stderr)
        print("Seed it with: python scripts/extract-demand-signals.py --all", file=sys.stderr)
        return 1

    problems = validate(signals, valid_themes)
    if problems:
        print(f"Register validation found {len(problems)} problem(s):", file=sys.stderr)
        for p in problems[:40]:
            print(f"  - {p}", file=sys.stderr)
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more", file=sys.stderr)
        return 2
    print(f"Register OK — {len(signals)} signals, {len({s['capability_theme'] for s in signals})} themes in use")

    if args.validate_only:
        return 0

    today = date.today()
    prior_state = find_prior_state()
    since = args.since or (prior_state.get("date") if prior_state else None)

    brief = render_brief(signals, since, prior_state, today, full=args.full)
    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    md_path = BRIEFS_DIR / f"{today.isoformat()}-demand-signal-brief.md"
    md_path.write_text(brief, encoding="utf-8")
    state_path = BRIEFS_DIR / f"{today.isoformat()}-brief-state.json"
    state_path.write_text(json.dumps(build_state(signals, today), indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {md_path.relative_to(WORKSPACE_ROOT).as_posix()}")
    render_docx(md_path)
    print("Distribute the .docx (never the .md) — Drive Proposal Repository, then link in Slack.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
