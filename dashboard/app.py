"""
Federal Proposal Copilot — Dashboard entrypoint.

Run from the repo root:
    streamlit run dashboard/app.py

Views:
    Triage        — all proposals sorted by urgency, health badges, next-action commands
    Proposal      — detail view for the selected proposal (tabbed, with command bar)
    Spend         — AI cost aggregated across all proposals
    Evidence Ledger — browse the evidence library
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dashboard.config import APP_ICON, APP_TITLE  # noqa: E402
from dashboard.views import ledger, spend, triage  # noqa: E402
from dashboard.views import proposal  # noqa: E402


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    with st.sidebar:
        st.markdown(f"### {APP_TITLE}")
        st.caption("v1.5 Phase B — read-only dashboard")

        view = st.radio(
            "View",
            options=["Triage", "Proposal", "Spend", "Evidence Ledger"],
            key="view_selector",
            label_visibility="collapsed",
        )

        st.divider()

        if "selected_proposal" in st.session_state:
            st.caption(f"Selected: **{st.session_state['selected_proposal']}**")
            if st.button("← Back to Triage", key="sidebar_back"):
                st.session_state["view"] = "Triage"
                st.rerun()
            st.divider()

        st.caption(
            "**Read-only.** Edit proposal files or run skills in Claude Code; "
            "the dashboard reflects changes on next load."
        )
        st.caption(
            f"Proposals: `{(REPO_ROOT / 'proposals').relative_to(REPO_ROOT)}/`\n\n"
            f"Company:   `{(REPO_ROOT / 'my-company').relative_to(REPO_ROOT)}/`"
        )

    # Programmatic navigation (e.g. Triage "Open →" button sets session_state["view"])
    current_view = st.session_state.pop("view", None) or view

    if current_view == "Triage":
        triage.render()
    elif current_view == "Proposal":
        proposal.render()
    elif current_view == "Spend":
        spend.render()
    elif current_view == "Evidence Ledger":
        ledger.render()
    else:
        st.error(f"Unknown view: {current_view}")


if __name__ == "__main__":
    main()
