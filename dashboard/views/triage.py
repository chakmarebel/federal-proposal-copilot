"""Triage view — all proposals sorted by urgency with health indicators and next-action commands."""
from __future__ import annotations

from datetime import datetime

import streamlit as st

from dashboard.loaders import ProposalSummary, load_all_proposals
from dashboard.views.helpers import (
    fmt_due,
    health_badge,
    next_action,
    pipeline_progress,
    urgency_sort_key,
)

_MIN_DT = datetime.min


def _fmt_coverage(s: ProposalSummary) -> str:
    if s.coverage_pct is None:
        return "—"
    if s.coverage_pct >= 80:
        return f"✅ {s.coverage_pct:.0f}%"
    if s.coverage_pct >= 50:
        return f"⚠️ {s.coverage_pct:.0f}%"
    return f"❌ {s.coverage_pct:.0f}%"


def render() -> None:
    st.title("Proposal Triage")
    st.caption("All proposals, sorted by urgency. Click **Open →** to drill in.")

    summaries: list[ProposalSummary] = load_all_proposals()

    if not summaries:
        st.info(
            "No proposals found under `proposals/`. "
            "Run `/new-proposal` inside Claude Code to scaffold one."
        )
        return

    badges = {s.slug: health_badge(s) for s in summaries}

    # ── Summary strip
    total = len(summaries)
    red    = sum(1 for s in summaries if badges[s.slug][0] == "🔴")
    yellow = sum(1 for s in summaries if badges[s.slug][0] == "🟡")
    green  = sum(1 for s in summaries if badges[s.slug][0] == "🟢")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", total)
    c2.metric("🔴 Needs attention", red)
    c3.metric("🟡 In progress", yellow)
    c4.metric("🟢 On track", green)

    st.divider()

    # ── Controls
    col_sort, col_filter = st.columns([1, 2])
    with col_sort:
        sort_by = st.selectbox(
            "Sort by",
            ["Urgency", "Last activity", "Pipeline %", "Name"],
            key="triage_sort",
        )
    with col_filter:
        show_filter = st.multiselect(
            "Filter by health",
            options=["🔴", "🟡", "🟢", "⚪"],
            default=["🔴", "🟡", "🟢", "⚪"],
            key="triage_filter",
        )

    # ── Sort
    if sort_by == "Urgency":
        ordered = sorted(summaries, key=urgency_sort_key)
    elif sort_by == "Last activity":
        ordered = sorted(
            summaries,
            key=lambda s: s.last_activity_ts or _MIN_DT,
            reverse=True,
        )
    elif sort_by == "Pipeline %":
        def _pct(s: ProposalSummary) -> float:
            done, total_req = pipeline_progress(s)
            return done / total_req if total_req else -1.0
        ordered = sorted(summaries, key=_pct, reverse=True)
    else:
        ordered = sorted(summaries, key=lambda s: s.slug)

    filtered = [s for s in ordered if badges[s.slug][0] in show_filter]

    if not filtered:
        st.info("No proposals match the current filter.")
        return

    st.caption(f"Showing {len(filtered)} of {total} proposals")
    st.write("")

    # ── Proposal cards
    for s in filtered:
        badge, _label = badges[s.slug]
        cmd = next_action(s)
        done, total_req = pipeline_progress(s)

        with st.container(border=True):
            # Row 1 — identity + key metrics + open button
            col_name, col_due, col_cov, col_pipe, col_btn = st.columns([3, 2, 2, 2, 1])

            with col_name:
                st.markdown(f"### {badge} `{s.slug}`")
                parts = [p for p in [s.display_name, s.type_id] if p and p not in ("", "(unknown)")]
                if parts:
                    st.caption(" · ".join(parts))

            with col_due:
                st.caption("Due")
                st.markdown(fmt_due(s.due_date))

            with col_cov:
                st.caption("Coverage")
                st.markdown(_fmt_coverage(s))
                if s.compliance_gap:
                    st.caption(f"⚠️ {s.compliance_gap} gap{'s' if s.compliance_gap != 1 else ''}")

            with col_pipe:
                st.caption("Pipeline")
                if total_req:
                    st.markdown(f"{done} / {total_req} skills")
                    st.progress(done / total_req)
                else:
                    st.caption("No type set")

            with col_btn:
                st.write("")  # vertical alignment nudge
                if st.button("Open →", key=f"open_{s.slug}", type="primary"):
                    st.session_state["selected_proposal"] = s.slug
                    st.session_state["view"] = "Proposal"
                    st.rerun()

            # Row 2 — next action + last activity
            col_cmd, col_act = st.columns([2, 3])

            with col_cmd:
                if cmd:
                    st.caption("Next action")
                    st.code(cmd, language="bash")
                else:
                    st.caption("✅ All required skills complete")

            with col_act:
                if s.last_activity_ts:
                    ts = s.last_activity_ts.strftime("%Y-%m-%d %H:%M")
                    summary = s.last_activity_summary[:80] if s.last_activity_summary else ""
                    st.caption(f"Last: **{ts}**" + (f" — {summary}" if summary else ""))
                else:
                    st.caption("No activity logged yet")
