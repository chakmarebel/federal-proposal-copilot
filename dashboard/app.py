"""
Federal Proposal Assistant — Dashboard entrypoint.

Run from the repo root:
    streamlit run dashboard/app.py

The app has a sidebar selector for four views:
    - Portfolio       — all proposals at a glance
    - Proposal        — detail view for the selected proposal
    - Spend           — AI cost aggregated across all proposals
    - Evidence Ledger — browse the evidence library
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Ensure repo root is on sys.path so `from dashboard.xxx import yyy` works
# regardless of the cwd Streamlit is launched from.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dashboard.config import APP_ICON, APP_TITLE  # noqa: E402
from dashboard.views import ledger, portfolio, proposal, spend  # noqa: E402


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### {APP_TITLE}")
        st.caption("v1.5 Phase B — read-only dashboard")

        view = st.radio(
            "View",
            options=["Portfolio", "Proposal", "Spend", "Evidence Ledger"],
            key="view_selector",
            label_visibility="collapsed",
        )

        st.divider()
        st.caption(
            "Paths:\n"
            f"- Proposals: `{(REPO_ROOT / 'proposals').relative_to(REPO_ROOT)}/`\n"
            f"- Company:   `{(REPO_ROOT / 'my-company').relative_to(REPO_ROOT)}/`\n"
        )
        st.caption(
            "This dashboard is **read-only**. To change proposal state, "
            "edit the markdown or run a skill in Claude Code."
        )

        # Quick-jump if a proposal is in session
        if "selected_proposal" in st.session_state:
            st.divider()
            st.caption(f"Selected proposal: **{st.session_state['selected_proposal']}**")

    # Dispatch by view choice
    # Allow programmatic navigation from portfolio → proposal by setting session_state['view']
    current_view = st.session_state.get("view") or view
    # clear the override after using it once
    if "view" in st.session_state:
        del st.session_state["view"]

    if current_view == "Portfolio":
        portfolio.render()
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
