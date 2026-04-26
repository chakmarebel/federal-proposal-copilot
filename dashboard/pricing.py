"""
Model → price table for cost estimation.

Prices in USD per 1M tokens, input/output. Update when Anthropic pricing changes.
Unknown models fall through to `DEFAULT_PRICING`.
"""
from __future__ import annotations

# As of 2026 — update when pricing changes.
# Source: Anthropic pricing page. Kept local to avoid a web dependency.
PRICING_PER_MILLION_TOKENS = {
    # Claude 4.x family
    "claude-opus-4-7":           {"input": 15.0, "output": 75.0},
    "claude-opus-4-7[1m]":       {"input": 15.0, "output": 75.0},
    "claude-opus-4-6":           {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-6":         {"input": 3.0,  "output": 15.0},
    "claude-sonnet-4-5":         {"input": 3.0,  "output": 15.0},
    "claude-haiku-4-5":          {"input": 0.80, "output": 4.00},
    "claude-haiku-4-5-20251001": {"input": 0.80, "output": 4.00},
    # Older families (in case old runs are logged)
    "claude-3-5-sonnet":         {"input": 3.0,  "output": 15.0},
    "claude-3-opus":             {"input": 15.0, "output": 75.0},
    "claude-3-haiku":            {"input": 0.25, "output": 1.25},
}

# Fallback for unknown models — roughly Sonnet pricing
DEFAULT_PRICING = {"input": 3.0, "output": 15.0}


def estimate_cost_usd(model: str | None, input_tokens: float | None, output_tokens: float | None) -> float | None:
    """
    Estimate USD cost for one run. Returns None if we can't estimate (both token counts null).
    Silently applies DEFAULT_PRICING for unknown model IDs.
    """
    if input_tokens is None and output_tokens is None:
        return None
    rates = PRICING_PER_MILLION_TOKENS.get(model, DEFAULT_PRICING) if model else DEFAULT_PRICING
    in_cost = (input_tokens or 0) / 1_000_000 * rates["input"]
    out_cost = (output_tokens or 0) / 1_000_000 * rates["output"]
    return in_cost + out_cost
