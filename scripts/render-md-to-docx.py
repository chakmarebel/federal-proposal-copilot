#!/usr/bin/env python3
"""Render review / reference / lessons-learned .md artifacts to .docx for Word.

Markdown is the authoring format the framework writes in. This script produces
a parallel .docx next to each .md so Bill (and anyone reviewing in Word) can
read them naturally — with headings, tables, lists, and bold/italic preserved.

The .docx files are gitignored along with the rest of the proposal content;
they're regenerated from .md whenever the source changes. Source of truth
remains the .md.

Usage:
  # Single file
  python scripts/render-md-to-docx.py path/to/file.md

  # All .md in a directory (non-recursive)
  python scripts/render-md-to-docx.py reviews/

  # All review + reference artifacts across the workspace, in one shot
  python scripts/render-md-to-docx.py --all

  # Just one proposal's reviews
  python scripts/render-md-to-docx.py --proposal extic-26-2

  # Force re-render even if .docx is newer than .md
  python scripts/render-md-to-docx.py --all --force

By default, .docx lands beside the .md (same directory). Use --docx-subdir
to put outputs in a `docx/` subdirectory instead.
"""

import argparse
import sys
from pathlib import Path

# Windows consoles default to cp1252 and choke on unicode characters in
# print() messages (e.g., the U+2192 right-arrow used below). Force utf-8
# on stdout/stderr so the script runs cleanly on Windows + macOS + Linux.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

# Import the existing markdown→docx converter from tools/
WORKSPACE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "tools"))
try:
    from md_to_docx import convert_md_to_doc, setup_document  # type: ignore
except ImportError as e:
    print(f"ERROR: could not import tools/md_to_docx.py — {e}", file=sys.stderr)
    print("Make sure tools/md_to_docx.py exists and python-docx is installed.", file=sys.stderr)
    sys.exit(2)

try:
    from docx import Document
except ImportError:
    print("ERROR: python-docx not installed. Run: pip install python-docx", file=sys.stderr)
    sys.exit(2)


# Artifacts the framework writes for human review — these get rendered to .docx
# when --all is used. Everything else (drafts, working/, generated indexes) is
# either authored in Word already or doesn't need Word rendering.
REVIEW_GLOBS = [
    "proposals/*/reviews/*.md",
    "proposals/*/working/proposal-plan.md",
    "proposals/*/working/proposal-brief.md",
    "proposals/*/working/compliance-matrix.md",
    "proposals/*/working/architecture-concept.md",
    "proposals/*/working/solution-strategy.md",
    "reference/team-review-rubric.md",
    "SKILLS.md",
    "SKILL-MERGE-PROPOSAL.md",
]


def render_one(md_path: Path, docx_path: Path, force: bool = False) -> tuple[bool, str]:
    """Render md_path → docx_path. Returns (rendered, reason)."""
    if not md_path.exists():
        return False, f"source missing: {md_path}"
    if (
        not force
        and docx_path.exists()
        and docx_path.stat().st_mtime >= md_path.stat().st_mtime
    ):
        return False, "up-to-date"

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    setup_document(doc)
    n = convert_md_to_doc(md_path, doc)
    doc.save(docx_path)
    return True, f"{n} lines"


def target_path(md_path: Path, docx_subdir: bool) -> Path:
    """Pick the .docx output path next to the .md."""
    if docx_subdir:
        return md_path.parent / "docx" / (md_path.stem + ".docx")
    return md_path.with_suffix(".docx")


def collect_files(args: argparse.Namespace) -> list[Path]:
    """Resolve which .md files to render based on CLI args."""
    files: list[Path] = []

    if args.path:
        p = Path(args.path)
        if not p.exists():
            print(f"ERROR: {p} not found", file=sys.stderr)
            sys.exit(1)
        if p.is_file() and p.suffix == ".md":
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(p.glob("*.md")))
        else:
            print(f"ERROR: {p} is not a .md file or directory", file=sys.stderr)
            sys.exit(1)

    if args.proposal:
        prop_dir = WORKSPACE_ROOT / "proposals" / args.proposal
        if not prop_dir.exists():
            print(f"ERROR: proposal {args.proposal} not found at {prop_dir}", file=sys.stderr)
            sys.exit(1)
        files.extend(sorted((prop_dir / "reviews").glob("*.md")))
        for f in (
            prop_dir / "working" / "proposal-plan.md",
            prop_dir / "working" / "proposal-brief.md",
            prop_dir / "working" / "compliance-matrix.md",
        ):
            if f.exists():
                files.append(f)

    if args.all:
        for glob in REVIEW_GLOBS:
            for f in sorted(WORKSPACE_ROOT.glob(glob)):
                files.append(f)

    # Dedup while preserving order
    seen: set[Path] = set()
    uniq: list[Path] = []
    for f in files:
        rp = f.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        uniq.append(f)
    return uniq


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("path", nargs="?", help="Single .md file or directory to render")
    ap.add_argument("--proposal", help="Render reviews + working for one proposal slug")
    ap.add_argument("--all", action="store_true",
                    help="Render every review/reference artifact across the workspace")
    ap.add_argument("--force", action="store_true",
                    help="Re-render even when .docx is newer than .md")
    ap.add_argument("--docx-subdir", action="store_true",
                    help="Write .docx into a docx/ subdirectory instead of beside the .md")
    args = ap.parse_args()

    if not (args.path or args.proposal or args.all):
        ap.print_help()
        return 1

    files = collect_files(args)
    if not files:
        print("No .md files matched.", file=sys.stderr)
        return 1

    rendered = 0
    skipped = 0
    failed = 0
    for md in files:
        out = target_path(md, args.docx_subdir)
        try:
            did_render, reason = render_one(md, out, force=args.force)
            rel_md = md.relative_to(WORKSPACE_ROOT) if md.is_absolute() and WORKSPACE_ROOT in md.parents else md
            if did_render:
                print(f"  [OK]   {rel_md}  →  {out.name}  ({reason})")
                rendered += 1
            else:
                print(f"  [skip] {rel_md}  ({reason})")
                skipped += 1
        except Exception as e:
            print(f"  [FAIL] {md}: {e}", file=sys.stderr)
            failed += 1

    print()
    print(f"Done — rendered: {rendered}, skipped: {skipped}, failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
