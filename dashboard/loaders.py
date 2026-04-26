"""
Loaders for every file the dashboard consumes.

Each loader returns a best-effort dict/list/DataFrame. None or empty result means
"not present" — dashboard views show "not migrated" rather than crashing.

All loaders are pure-read. Never writes.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import yaml

from dashboard.config import (
    ACTIVITY_MD,
    AI_RUNS_JSONL,
    COMPLIANCE_GAPS_MD,
    COMPLIANCE_MATRIX_JSON,
    EVIDENCE_CHECK_MD,
    EVIDENCE_LEDGER_JSON,
    GOLD_TEAM_MD,
    PROPOSALS_DIR,
    PROPOSAL_PLAN_JSON,
    PROPOSAL_PLAN_MD,
    PROPOSAL_TYPE_MD,
)
from dashboard.pricing import estimate_cost_usd


# ───────────────────────────────────────────────────────────────
# Data classes
# ───────────────────────────────────────────────────────────────

@dataclass
class ProposalSummary:
    """One row in the portfolio view. Everything the portfolio needs at a glance."""
    slug: str
    root: Path
    type_id: str = "(unknown)"
    display_name: str = ""
    customer: str = ""
    due_date: Optional[str] = None
    page_target: str = ""

    # Pipeline
    required_skills: list[str] = field(default_factory=list)
    skipped_skills: list[str] = field(default_factory=list)
    completed_skills: list[str] = field(default_factory=list)
    last_activity_ts: Optional[datetime] = None
    last_activity_summary: str = ""

    # Compliance
    compliance_total: int = 0
    compliance_covered: int = 0
    compliance_drafted: int = 0
    compliance_planned: int = 0
    compliance_partial: int = 0
    compliance_gap: int = 0
    coverage_pct: Optional[float] = None
    evidence_coverage_pct: Optional[float] = None

    # Reviews
    gold_team_exists: bool = False
    gold_team_pwin: str = ""

    # Spend
    ai_run_count: int = 0
    ai_total_cost_usd: float = 0.0
    ai_cost_is_estimated: bool = True  # True when any run had null tokens

    # Migration status
    has_proposal_type: bool = False
    has_proposal_plan_json: bool = False
    has_compliance_json: bool = False
    has_ai_runs: bool = False
    v15_migrated: bool = False  # True when ALL core sidecars are present


# ───────────────────────────────────────────────────────────────
# File readers
# ───────────────────────────────────────────────────────────────

def _read_yaml_frontmatter(path: Path) -> Optional[dict]:
    """Read YAML frontmatter from a markdown file. Returns None if no frontmatter."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    # Frontmatter is between two '---' lines at top of file
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None


def _read_json(path: Path) -> Optional[dict]:
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _read_jsonl(path: Path) -> list[dict]:
    """Read a JSONL file. Silently skips malformed lines."""
    out: list[dict] = []
    if not path.exists():
        return out
    try:
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return out


# Activity.md parsing — extract each "## <ts> — <skill> — <summary>" line
ACTIVITY_LINE_RE = re.compile(
    r"^##\s+(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)\s+—\s+"
    r"(?P<skill>[a-z0-9\-_]+)(?:\s+\[(?P<mode>[a-z0-9\-_ ]+)\])?\s+—\s+"
    r"(?P<summary>.+?)(?:\s+→\s+(?P<output>.+?))?$"
)


def _parse_activity(path: Path) -> list[dict]:
    """Parse activity.md into a list of structured entries."""
    if not path.exists():
        return []
    entries: list[dict] = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = ACTIVITY_LINE_RE.match(line.strip())
            if m:
                ts_str = m.group("ts").replace(" ", "T")
                try:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                except ValueError:
                    ts = None
                entries.append(
                    {
                        "timestamp": ts,
                        "timestamp_str": m.group("ts"),
                        "skill": m.group("skill"),
                        "mode": m.group("mode"),
                        "summary": m.group("summary"),
                        "output": m.group("output"),
                    }
                )
    except OSError:
        pass
    return entries


# Extract pWin from gold-team-scorecard.md (simple regex on the summary line)
GOLD_PWIN_RE = re.compile(r"pWin Estimate:\s*\*{0,2}([A-Za-z\- ]+?)\*{0,2}\s*(?:$|\n)", re.MULTILINE)


def _parse_gold_team(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = GOLD_PWIN_RE.search(text)
    return m.group(1).strip() if m else "(present, pWin unparsed)"


# ───────────────────────────────────────────────────────────────
# Proposal discovery
# ───────────────────────────────────────────────────────────────

def list_proposals() -> list[Path]:
    """Return every proposal root directory under PROPOSALS_DIR."""
    if not PROPOSALS_DIR.exists():
        return []
    return sorted([p for p in PROPOSALS_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")])


def load_proposal_summary(proposal_root: Path) -> ProposalSummary:
    """Build a ProposalSummary for one proposal directory. Best-effort — never throws."""
    summary = ProposalSummary(slug=proposal_root.name, root=proposal_root)

    # ── proposal-type.md (YAML frontmatter)
    type_path = proposal_root / PROPOSAL_TYPE_MD
    type_fm = _read_yaml_frontmatter(type_path)
    if type_fm:
        summary.has_proposal_type = True
        summary.type_id = type_fm.get("type_id", "(unknown)")
        summary.display_name = type_fm.get("display_name", "")
        summary.page_target = str(type_fm.get("page_target", ""))
        summary.required_skills = list(type_fm.get("required_skills", []))
        summary.skipped_skills = list(type_fm.get("skipped_skills", []))

    # ── proposal-plan.json (Phase A sidecar) — fallback to .md if json absent
    plan_json = _read_json(proposal_root / PROPOSAL_PLAN_JSON)
    if plan_json:
        summary.has_proposal_plan_json = True
        summary.customer = plan_json.get("customer_name", "") or plan_json.get("agency", "")
        summary.due_date = plan_json.get("due_date")
    else:
        # Fallback: peek into proposal-plan.md for a date line
        plan_md = proposal_root / PROPOSAL_PLAN_MD
        if plan_md.exists():
            try:
                text = plan_md.read_text(encoding="utf-8", errors="replace")
                m = re.search(r"(?i)(?:due|response deadline)[:\s]+(\d{4}-\d{2}-\d{2})", text)
                if m:
                    summary.due_date = m.group(1)
            except OSError:
                pass

    # ── compliance-matrix.json (Phase A sidecar)
    cmat = _read_json(proposal_root / COMPLIANCE_MATRIX_JSON)
    if cmat:
        summary.has_compliance_json = True
        s = cmat.get("summary", {}) or {}
        summary.compliance_total = s.get("total", 0) or 0
        summary.compliance_covered = s.get("covered", 0) or 0
        summary.compliance_drafted = s.get("drafted", 0) or 0
        summary.compliance_planned = s.get("planned", 0) or 0
        summary.compliance_partial = s.get("partial", 0) or 0
        summary.compliance_gap = s.get("gap", 0) or 0
        summary.coverage_pct = s.get("coverage_pct")
        summary.evidence_coverage_pct = s.get("evidence_coverage_pct")

    # ── activity.md (narrative log) — find completed skills + last entry
    activity_entries = _parse_activity(proposal_root / ACTIVITY_MD)
    if activity_entries:
        completed = {e["skill"] for e in activity_entries if e["skill"]}
        summary.completed_skills = sorted(completed)
        timestamps = [e["timestamp"] for e in activity_entries if e["timestamp"]]
        if timestamps:
            summary.last_activity_ts = max(timestamps)
        last = activity_entries[-1]
        summary.last_activity_summary = (last.get("summary") or "")[:120]

    # ── Gold Team scorecard
    gt_path = proposal_root / GOLD_TEAM_MD
    if gt_path.exists():
        summary.gold_team_exists = True
        summary.gold_team_pwin = _parse_gold_team(gt_path) or "(present)"

    # ── ai-runs.jsonl (Phase A ledger)
    runs = _read_jsonl(proposal_root / AI_RUNS_JSONL)
    summary.ai_run_count = len(runs)
    summary.has_ai_runs = len(runs) > 0
    any_real = False
    total = 0.0
    for r in runs:
        cost = r.get("cost_estimate_usd")
        if cost is None:
            cost = estimate_cost_usd(
                r.get("model"),
                r.get("input_tokens_estimate"),
                r.get("output_tokens_estimate"),
            )
        if cost is None:
            continue
        total += float(cost)
        if r.get("input_tokens_estimate") or r.get("output_tokens_estimate"):
            any_real = True
    summary.ai_total_cost_usd = total
    summary.ai_cost_is_estimated = not any_real

    # ── Migration status flag
    summary.v15_migrated = (
        summary.has_proposal_type
        and summary.has_proposal_plan_json
        and summary.has_compliance_json
    )

    return summary


def load_all_proposals() -> list[ProposalSummary]:
    return [load_proposal_summary(p) for p in list_proposals()]


# ───────────────────────────────────────────────────────────────
# Spend aggregation
# ───────────────────────────────────────────────────────────────

def load_all_ai_runs() -> pd.DataFrame:
    """Aggregate every proposal's ai-runs.jsonl into a single DataFrame."""
    rows: list[dict] = []
    for p in list_proposals():
        runs = _read_jsonl(p / AI_RUNS_JSONL)
        for r in runs:
            cost = r.get("cost_estimate_usd")
            if cost is None:
                cost = estimate_cost_usd(
                    r.get("model"),
                    r.get("input_tokens_estimate"),
                    r.get("output_tokens_estimate"),
                )
            rows.append(
                {
                    "proposal_id": r.get("proposal_id") or p.name,
                    "proposal_slug": p.name,
                    "timestamp": r.get("timestamp"),
                    "skill": r.get("skill"),
                    "job_type": r.get("job_type"),
                    "model": r.get("model"),
                    "input_tokens": r.get("input_tokens_estimate"),
                    "output_tokens": r.get("output_tokens_estimate"),
                    "cost_usd": float(cost) if cost is not None else 0.0,
                    "notes": r.get("notes", ""),
                }
            )
    df = pd.DataFrame(rows)
    if not df.empty and "timestamp" in df.columns:
        df["timestamp_dt"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    return df


# ───────────────────────────────────────────────────────────────
# Evidence ledger
# ───────────────────────────────────────────────────────────────

def load_evidence_ledger() -> Optional[dict]:
    if not EVIDENCE_LEDGER_JSON.exists():
        return None
    return _read_json(EVIDENCE_LEDGER_JSON)


# Scan drafts across all proposals to count citations of each evidence id
EVIDENCE_CITATION_RE = re.compile(r"<!--\s*evidence:\s*([^-][^>]*?)\s*-->")


def load_evidence_citation_counts() -> dict[str, int]:
    """For every evidence ID found in any drafts/*.md across all proposals, count citations."""
    counts: dict[str, int] = {}
    for p in list_proposals():
        drafts_dir = p / "drafts"
        if not drafts_dir.exists():
            continue
        for draft in drafts_dir.rglob("*.md"):
            try:
                text = draft.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in EVIDENCE_CITATION_RE.finditer(text):
                for ev_id in (x.strip() for x in m.group(1).split(",")):
                    if ev_id:
                        counts[ev_id] = counts.get(ev_id, 0) + 1
    return counts
