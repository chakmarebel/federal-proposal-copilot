"""Paths and constants for the dashboard. Everything is relative to the repo root."""
from pathlib import Path

# Repo root is one level up from this file (dashboard/config.py → repo_root/dashboard/ → repo_root)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Top-level directories the dashboard reads
PROPOSALS_DIR = REPO_ROOT / "proposals"
MY_COMPANY_DIR = REPO_ROOT / "my-company"
REFERENCE_DIR = REPO_ROOT / "reference"
DOCS_DIR = REPO_ROOT / "docs"

# Per-proposal sidecar filenames
PROPOSAL_TYPE_MD = "working/proposal-type.md"
PROPOSAL_PLAN_MD = "working/proposal-plan.md"
PROPOSAL_PLAN_JSON = "working/proposal-plan.json"
COMPLIANCE_MATRIX_MD = "working/compliance-matrix.md"
COMPLIANCE_MATRIX_JSON = "working/compliance-matrix.json"
ACTIVITY_MD = "working/activity.md"
AI_RUNS_JSONL = "working/ai-runs.jsonl"
GOLD_TEAM_MD = "reviews/gold-team-scorecard.md"
COMPLIANCE_GAPS_MD = "reviews/compliance-gaps.md"
EVIDENCE_CHECK_MD = "reviews/evidence-check.md"

# Company-wide files
EVIDENCE_LEDGER_JSON = MY_COMPANY_DIR / "evidence-ledger.json"

# UI
APP_TITLE = "Federal Proposal Copilot — Dashboard"
APP_ICON = ":briefcase:"
