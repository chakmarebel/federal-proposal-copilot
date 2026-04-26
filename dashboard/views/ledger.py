"""Evidence ledger browser — filter by type, approval_status, tags; show citation counts."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.config import EVIDENCE_LEDGER_JSON
from dashboard.loaders import load_evidence_citation_counts, load_evidence_ledger


def render():
    st.title("Evidence Ledger")
    st.caption(f"Source: `{EVIDENCE_LEDGER_JSON.relative_to(EVIDENCE_LEDGER_JSON.parent.parent)}` (gitignored — local to your machine)")

    ledger = load_evidence_ledger()
    if not ledger:
        st.warning(
            "No evidence ledger found at `my-company/evidence-ledger.json`.\n\n"
            "Phase C requires a seeded ledger to activate claim-grounded drafting. "
            "See `reference/examples/evidence-ledger.example.json` for the shape and "
            "`reference/schemas/evidence-ledger.schema.json` for the schema."
        )
        return

    items = ledger.get("items", [])
    if not items:
        st.caption("Ledger exists but has no items.")
        return

    # Header metrics
    owner = ledger.get("owner", "(unspecified owner)")
    st.markdown(f"**Owner:** {owner}  —  **Last updated:** {ledger.get('generated_at', '—')}")

    # Citation counts across all proposals
    citation_counts = load_evidence_citation_counts()

    df = pd.DataFrame(items)
    df["citations"] = df["id"].map(citation_counts).fillna(0).astype(int)

    total = len(df)
    approved = (df["approval_status"] == "approved").sum() if "approval_status" in df.columns else 0
    retired = (df["approval_status"] == "retired").sum() if "approval_status" in df.columns else 0
    restricted = (df["approval_status"] == "restricted").sum() if "approval_status" in df.columns else 0
    cited = (df["citations"] > 0).sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Items", total)
    c2.metric("Approved", approved)
    c3.metric("Restricted", restricted)
    c4.metric("Retired", retired)
    c5.metric("Cited somewhere", f"{cited} / {total}")

    st.divider()

    # Filters
    st.subheader("Filter")
    cols = st.columns(3)
    if "type" in df.columns:
        types = sorted(df["type"].dropna().unique().tolist())
        sel_types = cols[0].multiselect("Type", options=types, default=types)
        df = df[df["type"].isin(sel_types)]
    if "approval_status" in df.columns:
        statuses = sorted(df["approval_status"].dropna().unique().tolist())
        sel_status = cols[1].multiselect("Approval status", options=statuses, default=statuses)
        df = df[df["approval_status"].isin(sel_status)]
    q = cols[2].text_input("Search summary / detail / tags", "")
    if q:
        q_lower = q.lower()
        def _matches(row):
            hay = " ".join(
                str(row.get(k, "")) for k in ("summary", "detail")
            ) + " " + " ".join(row.get("relevance_tags", []) or [])
            return q_lower in hay.lower()
        df = df[df.apply(_matches, axis=1)]

    st.divider()

    # Table
    st.subheader(f"Items ({len(df)})")
    display_cols = [c for c in ["id", "type", "approval_status", "proof_strength", "summary", "citations"] if c in df.columns]
    show_df = df[display_cols].sort_values("id")
    st.dataframe(show_df, use_container_width=True, hide_index=True)

    st.divider()

    # Unused-but-approved callout
    st.subheader("Unused approved evidence")
    unused = df[(df.get("approval_status") == "approved") & (df["citations"] == 0)]
    if unused.empty:
        st.caption("Every approved item has been cited at least once. Nice.")
    else:
        st.caption(
            f"{len(unused)} approved item(s) not cited in any current draft. "
            "These are proof points you have but aren't using — worth a scan when drafting."
        )
        st.dataframe(
            unused[[c for c in ["id", "type", "summary", "relevance_tags"] if c in unused.columns]].sort_values("id"),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # Detail inspector
    st.subheader("Inspect an item")
    if not df.empty:
        sel_id = st.selectbox("Select ID", options=df["id"].sort_values().tolist(), key="ledger_inspect")
        row = df[df["id"] == sel_id].iloc[0].to_dict()
        st.json({k: v for k, v in row.items() if v is not None and v != ""})
