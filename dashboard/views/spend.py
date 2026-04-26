"""Spend view — aggregate AI cost across all proposals."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.loaders import load_all_ai_runs


def render():
    st.title("AI Spend")
    st.caption("Aggregated from every proposal's `working/ai-runs.jsonl`.")

    df = load_all_ai_runs()

    if df.empty:
        st.info(
            "No AI runs logged yet. Skills append to `working/ai-runs.jsonl` per the CLAUDE.md "
            "Activity Trail convention. Once proposals have activity, spend will appear here."
        )
        return

    total_runs = len(df)
    total_cost = df["cost_usd"].sum()
    has_tokens = (df["input_tokens"].notna() | df["output_tokens"].notna()).sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total AI runs", total_runs)
    c2.metric("Total cost (est.)", f"${total_cost:,.2f}")
    c3.metric("Runs with token counts", f"{has_tokens} / {total_runs}")

    if has_tokens == 0:
        st.warning(
            "No runs have populated token counts yet. Cost estimates are $0 until skills log real "
            "`input_tokens_estimate` and `output_tokens_estimate` values. This is expected in v1.5 Phase A — "
            "real counts arrive when skills integrate with the Anthropic SDK directly."
        )

    st.divider()

    # By proposal
    st.subheader("By proposal")
    by_prop = (
        df.groupby("proposal_slug", dropna=False)
        .agg(runs=("cost_usd", "count"), cost_usd=("cost_usd", "sum"))
        .sort_values("cost_usd", ascending=False)
        .reset_index()
    )
    st.dataframe(by_prop, use_container_width=True, hide_index=True)
    if not by_prop.empty:
        st.bar_chart(by_prop.set_index("proposal_slug")["cost_usd"])

    st.divider()

    # By skill
    st.subheader("By skill")
    by_skill = (
        df.groupby("skill", dropna=False)
        .agg(runs=("cost_usd", "count"), cost_usd=("cost_usd", "sum"))
        .sort_values("cost_usd", ascending=False)
        .reset_index()
    )
    st.dataframe(by_skill, use_container_width=True, hide_index=True)
    if not by_skill.empty:
        st.bar_chart(by_skill.set_index("skill")["cost_usd"])

    st.divider()

    # By model
    st.subheader("By model")
    by_model = (
        df.groupby("model", dropna=False)
        .agg(runs=("cost_usd", "count"), cost_usd=("cost_usd", "sum"))
        .sort_values("cost_usd", ascending=False)
        .reset_index()
    )
    st.dataframe(by_model, use_container_width=True, hide_index=True)

    st.divider()

    # Top 10 most-expensive individual runs
    st.subheader("Top 10 runs")
    top10 = df.sort_values("cost_usd", ascending=False).head(10)
    cols_show = [c for c in ["timestamp", "proposal_slug", "skill", "job_type", "model", "cost_usd"] if c in top10.columns]
    st.dataframe(top10[cols_show], use_container_width=True, hide_index=True)

    st.divider()

    # Trend by day
    if "timestamp_dt" in df.columns and df["timestamp_dt"].notna().any():
        st.subheader("Trend (daily)")
        trend = (
            df.dropna(subset=["timestamp_dt"])
            .assign(date=lambda d: d["timestamp_dt"].dt.date)
            .groupby("date")
            .agg(cost_usd=("cost_usd", "sum"), runs=("cost_usd", "count"))
            .reset_index()
        )
        st.line_chart(trend.set_index("date")["cost_usd"])
