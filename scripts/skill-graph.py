#!/usr/bin/env python3
"""Render the skill dependency DAG and validate composes/conflicts_with references.

This is what makes the `composes` and `conflicts_with` frontmatter fields earn
their keep — without this script they're decorative; with it they're a queryable
dependency graph and an integrity check on the skill catalog.

Examples:
  python scripts/skill-graph.py                       # mermaid DAG to stdout
  python scripts/skill-graph.py --format list         # plain text
  python scripts/skill-graph.py --validate-only       # CI gate (exit 1 on bad refs)
  python scripts/skill-graph.py --phase drafting      # subgraph for one phase
"""

import argparse
import re
import sys
from pathlib import Path


def parse_frontmatter(text: str) -> dict:
    text = text.replace("\r\n", "\n").lstrip("﻿")
    m = re.match(r"---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm: dict = {}
    for line in m.group(1).split("\n"):
        line = re.sub(r"\s+#.*$", "", line)  # strip inline comments
        if not line.strip() or ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith("["):
            inner = v[1:].split("]", 1)[0].strip()
            v = [x.strip() for x in inner.split(",") if x.strip()]
        fm[k.strip()] = v
    return fm


def load_skills(skills_dir: Path) -> dict[str, dict]:
    skills: dict[str, dict] = {}
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        skills[skill_md.parent.name] = parse_frontmatter(
            skill_md.read_text(encoding="utf-8-sig")
        )
    return skills


def validate(skills: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    valid_phases = {"setup", "capture", "planning", "drafting", "review", "submission", "inspection"}
    for name, fm in skills.items():
        phase = fm.get("phase")
        if not phase:
            errors.append(f"{name}: missing phase")
        elif isinstance(phase, str) and phase not in valid_phases:
            errors.append(f"{name}: invalid phase {phase!r} (valid: {sorted(valid_phases)})")
        for field in ("composes", "conflicts_with"):
            refs = fm.get(field, []) or []
            if isinstance(refs, str):
                continue  # empty or malformed; non-blocking
            for ref in refs:
                if ref not in skills:
                    errors.append(f"{name}: {field} references unknown skill {ref!r}")
    return errors


def render_mermaid(skills: dict[str, dict], phase_filter: str | None = None) -> str:
    lines = ["```mermaid", "graph TD"]
    in_scope = {n for n, fm in skills.items() if not phase_filter or fm.get("phase") == phase_filter}
    for name in sorted(skills):
        fm = skills[name]
        composes = fm.get("composes", []) or []
        if isinstance(composes, str):
            continue
        for upstream in composes:
            if phase_filter and name not in in_scope and upstream not in in_scope:
                continue
            lines.append(f"  {upstream} --> {name}")
    # nodes with no edges (orphans) still appear in the graph for completeness
    for name in sorted(skills):
        if phase_filter and skills[name].get("phase") != phase_filter:
            continue
        has_edge = False
        for n, fm in skills.items():
            composes = fm.get("composes", []) or []
            if isinstance(composes, str):
                continue
            if name in composes or (n == name and composes):
                has_edge = True
                break
        if not has_edge:
            lines.append(f"  {name}")
    lines.append("```")
    return "\n".join(lines)


def render_list(skills: dict[str, dict]) -> str:
    lines = []
    for name in sorted(skills):
        fm = skills[name]
        phase = fm.get("phase", "?")
        composes = fm.get("composes", []) or []
        conflicts = fm.get("conflicts_with", []) or []
        if isinstance(composes, str):
            composes = []
        if isinstance(conflicts, str):
            conflicts = []
        lines.append(f"{name}  [{phase}]")
        if composes:
            lines.append(f"  composes:        {', '.join(composes)}")
        if conflicts:
            lines.append(f"  conflicts_with:  {', '.join(conflicts)}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--skills-dir", default=".claude/skills", help="Directory of <skill-name>/SKILL.md")
    ap.add_argument("--format", choices=["mermaid", "list"], default="mermaid")
    ap.add_argument("--phase", help="Render only one phase (subgraph)")
    ap.add_argument("--validate-only", action="store_true", help="Exit 1 if any reference is broken")
    args = ap.parse_args()

    skills_dir = Path(args.skills_dir)
    if not skills_dir.exists():
        print(f"No skills dir at {skills_dir}", file=sys.stderr)
        return 2

    skills = load_skills(skills_dir)
    errors = validate(skills)
    if errors:
        print("VALIDATION FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    if args.validate_only:
        print(f"OK: {len(skills)} skills, all phase / composes / conflicts_with references valid")
        return 0

    if args.format == "mermaid":
        print(render_mermaid(skills, args.phase))
    else:
        print(render_list(skills))
    return 0


if __name__ == "__main__":
    sys.exit(main())
