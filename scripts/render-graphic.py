#!/usr/bin/env python3
"""
Render a parametric graphic template to HTML by substituting data from a JSON file.

Usage:
    python scripts/render-graphic.py <template.html> <data.json> <output.html>

Placeholder syntax (see reference/graphic-templates/README.md):
    {{field}}                   — simple substitution from data["field"]
    {{a.b.c}}                   — dotted path: data["a"]["b"]["c"]
    {{array.0.name}}            — array index: data["array"][0]["name"]
    <!-- REPEAT:items --> ... <!-- END:REPEAT -->
                                — render the inner block once per item in data["items"]
                                  with {{item.field}} inside

Missing paths render as the original placeholder text, with a warning on stderr.
Use --strict to exit non-zero on any unresolved placeholder.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}")
REPEAT_BLOCK_RE = re.compile(
    r"<!--\s*REPEAT:([a-zA-Z0-9_.]+)\s*-->(.*?)<!--\s*END:REPEAT\s*-->",
    re.DOTALL,
)


def resolve_path(data: Any, path: str) -> Any:
    """Walk a dotted path into nested dicts/lists. Returns None if not found."""
    cur: Any = data
    for key in path.split("."):
        if cur is None:
            return None
        if isinstance(cur, list):
            try:
                idx = int(key)
                cur = cur[idx] if 0 <= idx < len(cur) else None
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict):
            cur = cur.get(key)
        else:
            return None
    return cur


def render_placeholders(text: str, data: Any, strict: bool = False, warnings: list[str] | None = None) -> str:
    def repl(m: re.Match[str]) -> str:
        path = m.group(1)
        value = resolve_path(data, path)
        if value is None:
            msg = f"unresolved placeholder: {{{{{path}}}}}"
            if warnings is not None:
                warnings.append(msg)
            print(f"  warn: {msg}", file=sys.stderr)
            if strict:
                sys.exit(2)
            return m.group(0)  # leave original placeholder
        return str(value)

    return PLACEHOLDER_RE.sub(repl, text)


def render_repeat_blocks(text: str, data: Any, strict: bool = False, warnings: list[str] | None = None) -> str:
    def repl(m: re.Match[str]) -> str:
        array_path = m.group(1)
        block = m.group(2)
        items = resolve_path(data, array_path)
        if not isinstance(items, list):
            msg = f"REPEAT target is not an array: {array_path}"
            if warnings is not None:
                warnings.append(msg)
            print(f"  warn: {msg}", file=sys.stderr)
            if strict:
                sys.exit(2)
            return ""
        out_parts = []
        for i, item in enumerate(items):
            # Inside a REPEAT block, `item` and `item_index` are available in addition to the global data root
            scope = {"item": item, "item_index": i, **({} if not isinstance(data, dict) else data)}
            out_parts.append(render_placeholders(block, scope, strict=strict, warnings=warnings))
        return "".join(out_parts)

    return REPEAT_BLOCK_RE.sub(repl, text)


def render(template: str, data: Any, strict: bool = False) -> str:
    warnings: list[str] = []
    # REPEAT blocks first (so placeholders inside them can reference {{item.*}})
    step1 = render_repeat_blocks(template, data, strict=strict, warnings=warnings)
    step2 = render_placeholders(step1, data, strict=strict, warnings=warnings)
    if warnings:
        print(f"  {len(warnings)} unresolved placeholder(s).", file=sys.stderr)
    return step2


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("template", type=Path, help="Path to template.html")
    ap.add_argument("data", type=Path, help="Path to data.json")
    ap.add_argument("output", type=Path, help="Path to write filled HTML")
    ap.add_argument("--strict", action="store_true", help="Exit non-zero on any unresolved placeholder")
    args = ap.parse_args(argv)

    if not args.template.exists():
        print(f"error: template not found: {args.template}", file=sys.stderr)
        return 1
    if not args.data.exists():
        print(f"error: data not found: {args.data}", file=sys.stderr)
        return 1

    template = args.template.read_text(encoding="utf-8")
    with args.data.open(encoding="utf-8") as f:
        data = json.load(f)

    # Strip comment-only top-level fields from data (e.g., "_comment")
    if isinstance(data, dict):
        data = {k: v for k, v in data.items() if not k.startswith("_")}

    output = render(template, data, strict=args.strict)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(f"  wrote {args.output} ({len(output):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
