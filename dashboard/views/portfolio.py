"""Portfolio view — every proposal in one table."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.loaders import ProposalSummary, load_all_proposals


def _fmt_date(d: str | None) -> str:
    return d or "—"


def _fmt_pct(v: float | None) -> str:
    if v is None:
        return "—"
    return f"{v:.0f}%"


def _fmt_cost(usd: float, estimated: bool) -> str:
    if usd == 0:
        return "—"
    suffix = "~" if estimated else ""
    return f"{suffix}${usd:,.2f}"


def _pipeline_progress(s: ProposalSummary) -> str:
    """Return 'N/M' counting completed required skills over total required."""
    if not s.required_skills:
        return "—"
    done = sum(1 for sk in s.required_skills if sk in s.completed_skills)
    return f"{done}/{len(s.required_skills)}"


def _migration_badge(s: ProposalSummary) -> str:
    if s.v15_migrated:
        return "✅ v1.5"
    if s.has_proposal_type:
        return "⏳ partial"
    return "📄 pre-v1.5"


def render():
    st.title("Portfolio")
    st.caption("All proposals. Click a row to drill in on the Proposal view.")

    summaries: list[ProposalSummary] = load_all_proposals()

    if not summaries:
        st.info(
            "No proposals found under `proposals/`. Run `/new-proposal` inside Claude Code to scaffold one.\n\n"
            "If you have proposals elsewhere, verify the framework is running from the repo root "
            "(`C:\\Users\\wbal9\\Claude Code Projects\\federal-proposal-assistant`)."
        )
        return

    # Summary metrics
    total = len(summaries)
    migrated = sum(1 for s in summaries if s.v15_migrated)
    due_soon = sum(1 for s in summaries if s.due_date)  # simple count
    total_spend = sum(s.ai_total_cost_usd for s in summaries)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Proposals", total)
    c2.metric("v1.5 migrated", f"{migrated} / {total}")
    c3.metric("With due date", due_soon)
    c4.metric("Total spend (est.)", f"~${total_spend:,.2f}" if total_spend else "—")

    st.divider()

    # Build the DataFrame
    rows = []
    for s in summaries:
        rows.append(
            {
                "Proposal": s.slug,
                "Migration": _migration_badge(s),
                "Type": s.type_id,
                "Due": _fmt_date(s.due_date),
                "Pipeline": _pipeline_progress(s),
                "Coverage": _fmt_pct(s.coverage_pct),
                "Evidence": _fmt_pct(s.evidence_coverage_pct),
                "Gaps": s.compliance_gap if s.has_compliance_json else "—",
                "Gold": s.gold_team_pwin or ("—" if not s.gold_team_exists else "✓"),
                "Spend": _fmt_cost(s.ai_total_cost_usd, s.ai_cost_is_estimated),
                "Last activity": s.last_activity_ts.strftime("%Y-%m-%d %H:%M") if s.last_activity_ts else "—",
            }
        )

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # Detail selector
    st.subheader("Open a proposal")
    slug = st.selectbox("Select", options=[s.slug for s in summaries], key="portfolio_selector")
    if st.button("Open", type="primary"):
        st.session_state["selected_proposal"] = slug
        st.session_state["view"] = "proposal"
        st.rerun()

    with st.expander("Legend"):
        st.markdown(
            """
            - **Migration** — 📄 pre-v1.5 (no `proposal-type.md`), ⏳ partial (has type, missing JSON sidecars), ✅ v1.5 (fully migrated)
            - **Pipeline** — completed required skills / total required (per `working/proposal-type.md`)
            - **Coverage** — compliance matrix coverage_pct (Covered + Drafted) / Total
            - **Evidence** — Phase C evidence_coverage_pct (supported citations / total claim markers)
            - **Gaps** — rows with Status = `Gap` in the compliance matrix
            - **Gold** — Gold Team pWin (from `reviews/gold-team-scorecard.md`)
            - **Spend** — sum of `cost_estimate_usd` across `working/ai-runs.jsonl` (`~` prefix means estimates based on null token counts)
            """
        )
