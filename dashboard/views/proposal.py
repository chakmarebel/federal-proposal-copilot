"""Per-proposal detail view — command bar, tabbed layout, visual pipeline stepper."""
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
from dashboard.views.helpers import (
    SKILL_LABELS,
    fmt_due,
    health_badge,
    next_action,
    pipeline_progress,
)

_STEPS_PER_ROW = 7


def _render_stepper(s) -> None:
    """Visual pipeline stepper: ✅ done / ▶️ current / ○ pending."""
    if not s.required_skills:
        st.caption(
            "No `working/proposal-type.md` found — cannot show pipeline. "
            "Run `/new-proposal` to set one up."
        )
        return

    completed_set = set(s.completed_skills)
    current_found = False
    steps: list[tuple[str, str]] = []

    for skill in s.required_skills:
        if skill in completed_set:
            status = "done"
        elif not current_found:
            status = "current"
            current_found = True
        else:
            status = "pending"
        steps.append((skill, status))

    for row_start in range(0, len(steps), _STEPS_PER_ROW):
        row = steps[row_start : row_start + _STEPS_PER_ROW]
        cols = st.columns(len(row))
        for col, (skill, status) in zip(cols, row):
            num = s.required_skills.index(skill) + 1
            label = SKILL_LABELS.get(skill, skill)
            with col:
                if status == "done":
                    st.markdown(f"✅ **{num}**\n\n{label}")
                elif status == "current":
                    st.markdown(f"▶️ **{num}**\n\n**{label}**")
                else:
                    st.markdown(f"○ {num}\n\n{label}")
        if row_start + _STEPS_PER_ROW < len(steps):
            st.write("")  # gap between rows

    if s.skipped_skills:
        st.caption(
            f"Skipped for type `{s.type_id}`: "
            + ", ".join(f"`{sk}`" for sk in s.skipped_skills)
        )


def render() -> None:
    slug = st.session_state.get("selected_proposal")
    if not slug:
        st.warning("No proposal selected. Go to **Triage** and click **Open →**.")
        return

    root = PROPOSALS_DIR / slug
    if not root.exists():
        st.error(f"Proposal `{slug}` not found under `proposals/`.")
        return

    s = load_proposal_summary(root)
    badge, _label = health_badge(s)
    cmd = next_action(s)

    # ── Header
    st.title(f"{badge}  {s.slug}")

    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f"**Type**\n\n{s.display_name or s.type_id or '—'}")
    m2.markdown(f"**Customer**\n\n{s.customer or '—'}")
    m3.markdown(f"**Due**\n\n{fmt_due(s.due_date)}")
    m4.markdown(f"**Pages**\n\n{s.page_target or '—'}")

    if not s.v15_migrated:
        st.warning(
            "Pre-v1.5 proposal: JSON sidecars not found. "
            "Dashboard shows what it can infer from markdown files. "
            "Run `/compliance-check` and ensure `working/proposal-type.md` exists to fully migrate."
        )

    # ── Command bar
    st.write("")
    if cmd:
        with st.container(border=True):
            st.markdown("#### What to run next")
            bar_cmd, bar_prog = st.columns([2, 3])
            with bar_cmd:
                st.code(cmd, language="bash")
            with bar_prog:
                done, total_req = pipeline_progress(s)
                if total_req:
                    st.progress(
                        done / total_req,
                        text=f"Pipeline: {done} / {total_req} skills complete",
                    )
    else:
        st.success(
            "✅ All required skills complete — ready for `/export-proposal` or a final Gold Team review."
        )

    st.divider()

    # ── Tabs
    tab_pipe, tab_comp, tab_ev, tab_rev, tab_spend = st.tabs(
        ["Pipeline", "Compliance", "Evidence", "Reviews", "Spend"]
    )

    # ────────────────────────────────────────────────
    # Pipeline tab
    # ────────────────────────────────────────────────
    with tab_pipe:
        st.subheader("Skill Pipeline")
        _render_stepper(s)

        if s.required_skills:
            st.divider()
            st.subheader("Detail")
            rows = []
            for skill in s.required_skills:
                done_bool = skill in s.completed_skills
                if done_bool:
                    status_str = "✅ done"
                elif cmd == f"/{skill}":
                    status_str = "▶ next"
                else:
                    status_str = "○ pending"
                rows.append({
                    "#": s.required_skills.index(skill) + 1,
                    "Skill": skill,
                    "Status": status_str,
                })
            for skill in s.skipped_skills:
                rows.append({
                    "#": "—",
                    "Skill": skill,
                    "Status": f"⏭ skipped ({s.type_id})",
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Recent activity")
        entries = _parse_activity(root / ACTIVITY_MD)
        if entries:
            recent = list(reversed(entries))[:8]
            act_rows = [
                {
                    "When": (
                        e["timestamp"].strftime("%Y-%m-%d %H:%M")
                        if e["timestamp"]
                        else e["timestamp_str"]
                    ),
                    "Skill": e["skill"] + (f" [{e['mode']}]" if e["mode"] else ""),
                    "Summary": (e["summary"] or "")[:100],
                }
                for e in recent
            ]
            st.dataframe(pd.DataFrame(act_rows), use_container_width=True, hide_index=True)
        else:
            st.caption("No activity logged. Skills write to `working/activity.md` on completion.")

    # ────────────────────────────────────────────────
    # Compliance tab
    # ────────────────────────────────────────────────
    with tab_comp:
        st.subheader("Compliance Coverage")
        if s.has_compliance_json:
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            c1.metric("Total", s.compliance_total)
            c2.metric("Covered", s.compliance_covered)
            c3.metric("Drafted", s.compliance_drafted)
            c4.metric("Planned", s.compliance_planned)
            c5.metric("Partial", s.compliance_partial)
            c6.metric("Gaps", s.compliance_gap)

            if s.coverage_pct is not None:
                st.progress(
                    min(100, int(s.coverage_pct)) / 100,
                    text=f"Coverage: {s.coverage_pct:.0f}% (Covered + Drafted / Total)",
                )

            gaps_path = root / COMPLIANCE_GAPS_MD
            if gaps_path.exists():
                with st.expander("Open gaps — reviews/compliance-gaps.md"):
                    try:
                        st.markdown(gaps_path.read_text(encoding="utf-8", errors="replace"))
                    except OSError:
                        st.caption("Could not read gaps file.")
        else:
            st.info(
                "No compliance JSON yet. Run `/compliance-check` to generate it. "
                "The skill produces `working/compliance-matrix.json` which powers this view."
            )

    # ────────────────────────────────────────────────
    # Evidence tab
    # ────────────────────────────────────────────────
    with tab_ev:
        st.subheader("Evidence Coverage")
        if s.evidence_coverage_pct is not None:
            st.progress(
                min(100, int(s.evidence_coverage_pct)) / 100,
                text=f"Evidence: {s.evidence_coverage_pct:.0f}% of claim markers supported",
            )
        else:
            st.info(
                "No evidence coverage data. Run `/evidence-check` (Phase C) after drafting to compute."
            )

        ev_path = root / EVIDENCE_CHECK_MD
        if ev_path.exists():
            with st.expander("Evidence check report — reviews/evidence-check.md"):
                try:
                    st.markdown(ev_path.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    st.caption("Could not read evidence-check file.")

    # ────────────────────────────────────────────────
    # Reviews tab
    # ────────────────────────────────────────────────
    with tab_rev:
        st.subheader("Gold Team")
        gt_path = root / GOLD_TEAM_MD
        if s.gold_team_exists:
            st.metric("pWin Estimate", s.gold_team_pwin)
            with st.expander("Full Gold Team scorecard"):
                try:
                    st.markdown(gt_path.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    st.caption("Could not read Gold Team scorecard.")
        else:
            st.info(
                "Gold Team review has not been run. "
                "Run `/red-team-review --mode=gold` after `/proposal-writer` and `/compliance-check`."
            )

    # ────────────────────────────────────────────────
    # Spend tab
    # ────────────────────────────────────────────────
    with tab_spend:
        st.subheader("AI Spend")
        if s.has_ai_runs:
            sc1, sc2 = st.columns(2)
            sc1.metric("AI runs logged", s.ai_run_count)
            sc2.metric(
                "Estimated cost",
                f"${s.ai_total_cost_usd:,.2f}" + (" *" if s.ai_cost_is_estimated else ""),
            )
            if s.ai_cost_is_estimated:
                st.caption(
                    "\\* Token counts are null in the ledger; cost shows `$0.00` "
                    "until skills log real `input_tokens_estimate` values."
                )

            runs = _read_jsonl(root / "working/ai-runs.jsonl")
            if runs:
                run_df = pd.DataFrame(runs)
                cols_keep = [
                    c for c in [
                        "timestamp", "skill", "job_type", "model",
                        "input_tokens_estimate", "output_tokens_estimate", "cost_estimate_usd",
                    ]
                    if c in run_df.columns
                ]
                st.dataframe(run_df[cols_keep], use_container_width=True, hide_index=True)
        else:
            st.info(
                "No AI runs logged. Skills append to `working/ai-runs.jsonl` per the CLAUDE.md "
                "Activity Trail convention."
            )

        st.caption(f"Proposal files: `{root}`")
