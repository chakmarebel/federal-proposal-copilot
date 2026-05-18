"""Shared UI utilities — health scoring, next-action logic, stepper labels."""
from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from dashboard.loaders import ProposalSummary

# Short display labels for the pipeline stepper
SKILL_LABELS: dict[str, str] = {
    "opportunity-quick-look": "Quick Look",
    "proposal-manager": "Plan",
    "customer-intel": "Customer",
    "competitor-assessment": "Competitors",
    "capture-scorecard": "Scorecard",
    "proposal-solution-architect": "Architecture",
    "proposal-graphics": "Graphics",
    "past-performance": "Past Perf.",
    "pricing-analyst": "Pricing",
    "proposal-writer": "Draft",
    "compliance-check": "Compliance",
    "evidence-check": "Evidence",
    "red-team-review": "Red Team",
    "export-proposal": "Export",
}

_MIN_DT = datetime.min


def days_until_due(due_date: Optional[str]) -> Optional[int]:
    if not due_date:
        return None
    # Accept plain date "2026-05-01" or full ISO datetime "2026-04-27T23:59:00-04:00"
    try:
        return (date.fromisoformat(due_date[:10]) - date.today()).days
    except (ValueError, IndexError):
        return None


def fmt_due(due_date: Optional[str]) -> str:
    if not due_date:
        return "No due date"
    display = due_date[:10]  # always show only the date portion
    days = days_until_due(due_date)
    if days is None:
        return display
    if days < 0:
        return f"⚠️ {display} ({abs(days)}d overdue)"
    if days == 0:
        return "🚨 Due TODAY"
    if days <= 7:
        return f"🔥 {display} ({days}d)"
    if days <= 14:
        return f"⏰ {display} ({days}d)"
    return f"{display} ({days}d)"


def health_badge(s: ProposalSummary) -> tuple[str, str]:
    """Return (emoji, label) health indicator for a proposal."""
    days = days_until_due(s.due_date)

    if days is not None and days < 0:
        return "🔴", "Overdue"

    if not s.required_skills:
        return "⚪", "Setup needed"

    done = sum(1 for sk in s.required_skills if sk in s.completed_skills)
    total = len(s.required_skills)
    pct = (done / total * 100) if total else 0.0

    # Critical: gaps + due very soon
    if s.compliance_gap > 0 and days is not None and days < 14:
        return "🔴", "At risk"

    # Urgent: due within a week and pipeline not near done
    if days is not None and days < 7 and pct < 80:
        return "🔴", "Urgent"

    # Yellow: compliance gaps present
    if s.compliance_gap > 0:
        return "🟡", "Gaps"

    # Yellow: low coverage or early-stage pipeline
    if s.coverage_pct is not None and s.coverage_pct < 50:
        return "🟡", "In progress"
    if pct < 40:
        return "🟡", "Early stage"

    # Green
    if pct >= 70:
        return "🟢", "On track"

    return "🟡", "In progress"


def next_action(s: ProposalSummary) -> Optional[str]:
    """Return the exact slash-command to run next, or None if pipeline is complete."""
    if not s.required_skills:
        return "/new-proposal"
    for skill in s.required_skills:
        if skill not in s.completed_skills:
            return f"/{skill}"
    return None


def pipeline_progress(s: ProposalSummary) -> tuple[int, int]:
    """Return (done, total) required-skill counts."""
    if not s.required_skills:
        return 0, 0
    done = sum(1 for sk in s.required_skills if sk in s.completed_skills)
    return done, len(s.required_skills)


def urgency_sort_key(s: ProposalSummary):
    """Sort key: soonest due first, then most gaps first."""
    days = days_until_due(s.due_date)
    if days is None:
        days = 9999
    return (max(days, -9999), -(s.compliance_gap or 0))
