"""Per-proposal detail view."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.config import (
    ACTIVITY_MD,
    COMPLIANCE_GAPS_MD,
    EVIDENCE_CHECK_MD,
    GOLD_TEAM_MD,
    PROPOSALS_DIR,
)
from dashboard.loaders import (
    _parse_activity,
    _read_jsonl,
    load_proposal_summary,
)


def render():
    slug = st.session_state.get("selected_proposal")
    if not slug:
        st.warning("No proposal selected. Go to the Portfolio view and open one.")
        return

    root = PROPOSALS_DIR / slug
    if not root.exists():
        st.error(f"Proposal `{slug}` not found under `proposals/`.")
        return

    s = load_proposal_summary(root)

    # Header
    st.title(s.slug)
    cols = st.columns(4)
    cols[0].markdown(f"**Type**\n\n{s.display_name or s.type_id}")
    cols[1].markdown(f"**Customer**\n\n{s.customer or '—'}")
    cols[2].markdown(f"**Due**\n\n{s.due_date or '—'}")
    cols[3].markdown(f"**Page target**\n\n{s.page_target or '—'}")

    if not s.v15_migrated:
        st.warning(
            "This proposal predates v1.5 Phase A sidecars. "
            "The dashboard is showing what it can infer from the markdown files. "
            "To migrate, run `/compliance-check` and `/proposal-manager` after ensuring `working/proposal-type.md` exists."
        )

    st.divider()

    # ── Pipeline progress
    st.subheader("Pipeline")
    if s.required_skills:
        pipeline_rows = []
        for skill in s.required_skills:
            done = skill in s.completed_skills
            pipeline_rows.append({"#": len(pipeline_rows) + 1, "Skill": skill, "Status": "✓ done" if done else "○ pending"})
        for skill in s.skipped_skills:
            pipeline_rows.append({"#": "—", "Skill": skill, "Status": f"— skipped (type: {s.type_id})"})
        st.dataframe(pd.DataFrame(pipeline_rows), use_container_width=True, hide_index=True)
    else:
        st.caption("No proposal-type declared. Cannot show required-skill pipeline.")

    st.divider()

    # ── Compliance
    st.subheader("Compliance")
    if s.has_compliance_json:
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Total", s.compliance_total)
        c2.metric("Covered", s.compliance_covered)
        c3.metric("Drafted", s.compliance_drafted)
        c4.metric("Planned", s.compliance_planned)
        c5.metric("Partial", s.compliance_partial)
        c6.metric("Gaps", s.compliance_gap)
        if s.coverage_pct is not None:
            st.progress(min(100, int(s.coverage_pct)) / 100, text=f"Coverage: {s.coverage_pct:.0f}% (Covered + Drafted / Total)")
        # Open gaps detail
        gaps_path = root / COMPLIANCE_GAPS_MD
        if gaps_path.exists():
            with st.expander("Open gaps (from reviews/compliance-gaps.md)"):
                try:
                    st.markdown(gaps_path.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    st.caption("Could not read gaps file.")
    else:
        st.caption("No compliance matrix JSON. Run `/compliance-check` to produce one.")

    st.divider()

    # ── Evidence (Phase C)
    st.subheader("Evidence coverage")
    if s.evidence_coverage_pct is not None:
        st.progress(
            min(100, int(s.evidence_coverage_pct)) / 100,
            text=f"Evidence coverage: {s.evidence_coverage_pct:.0f}% of claim markers supported",
        )
    else:
        st.caption("No evidence_coverage metric yet. Run `/evidence-check` to compute.")
    ev_path = root / EVIDENCE_CHECK_MD
    if ev_path.exists():
        with st.expander("Evidence check report"):
            try:
                st.markdown(ev_path.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                st.caption("Could not read evidence-check report.")

    st.divider()

    # ── Gold Team
    st.subheader("Gold Team")
    gt_path = root / GOLD_TEAM_MD
    if s.gold_team_exists:
        st.markdown(f"**pWin estimate:** {s.gold_team_pwin}")
        with st.expander("Full scorecard"):
            try:
                st.markdown(gt_path.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                st.caption("Could not read Gold Team file.")
    else:
        st.caption("Gold Team has not been run. Run `/red-team-review --mode=gold` after drafting is complete.")

    st.divider()

    # ── Recent activity
    st.subheader("Recent activity")
    entries = _parse_activity(root / ACTIVITY_MD)
    if entries:
        recent = list(reversed(entries))[:10]
        act_rows = [
            {
                "When": e["timestamp"].strftime("%Y-%m-%d %H:%M") if e["timestamp"] else e["timestamp_str"],
                "Skill": e["skill"] + (f" [{e['mode']}]" if e["mode"] else ""),
                "Summary": (e["summary"] or "")[:90],
                "Output": e.get("output") or "",
            }
            for e in recent
        ]
        st.dataframe(pd.DataFrame(act_rows), use_container_width=True, hide_index=True)
    else:
        st.caption("No activity log. Skills write to `working/activity.md` on completion.")

    st.divider()

    # ── Spend
    st.subheader("Spend")
    if s.has_ai_runs:
        c1, c2 = st.columns(2)
        c1.metric("AI runs", s.ai_run_count)
        c2.metric(
            "Estimated cost",
            f"${s.ai_total_cost_usd:,.2f}" + ("*" if s.ai_cost_is_estimated else ""),
        )
        if s.ai_cost_is_estimated:
            st.caption("`*` token counts are null in the ledger; cost shown as `$0.00` unless computed from non-null tokens.")

        runs = _read_jsonl(root / "working/ai-runs.jsonl")
        if runs:
            run_df = pd.DataFrame(runs)
            cols_keep = [c for c in ["timestamp", "skill", "job_type", "model", "input_tokens_estimate", "output_tokens_estimate", "cost_estimate_usd"] if c in run_df.columns]
            st.dataframe(run_df[cols_keep], use_container_width=True, hide_index=True)
    else:
        st.caption("No AI runs logged. Skills append to `working/ai-runs.jsonl` per the CLAUDE.md convention.")

    st.divider()

    # ── File links
    st.subheader("Files")
    st.code(f"{root}", language="text")
    st.caption("Open in Explorer or VS Code using your preferred shortcut.")
