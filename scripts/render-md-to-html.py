#!/usr/bin/env python3
"""Render proposal draft markdown to self-contained, submission-ready HTML.

Each output is a single .html file with all CSS inline and every figure
embedded inline (as a sandboxed <iframe srcdoc>) — no external dependencies,
nothing to ship alongside it.

Figures are referenced in the markdown with a marker comment:

    <!-- figure: fig1-system-architecture -->

The marker names an HTML graphic in the proposal's `graphics/` directory.
The graphic is embedded at natural size and CSS-scaled to the text column,
so HTML/SVG graphics stay crisp (no rasterization).

Usage:
    python scripts/render-md-to-html.py <file.md> [<file.md> ...] --outdir <dir>
    python scripts/render-md-to-html.py --proposal <slug>

With --proposal, renders the four narrative drafts (whitepaper, system-blueprint,
tech-dev-plan-rom, company-profile) to proposals/<slug>/final/html/.
"""

import argparse
import html
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

# Fallback natural size, used only if a graphic's rendered PNG cannot be
# measured. Real sizes are read at runtime from graphics/rendered/<name>.png.
DEFAULT_FIGURE_SIZE = (1240, 1240)

CONTENT_WIDTH = 816  # px — text column inside the .doc container

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#e9eaec;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
     color:#23262b;line-height:1.62;padding:32px 16px}
.doc{max-width:960px;margin:0 auto;background:#ffffff;padding:60px 72px 72px;
     box-shadow:0 4px 28px rgba(0,0,0,.18);border-radius:4px}
h1{font-size:30px;font-weight:700;color:#191c20;letter-spacing:.2px;
   padding-bottom:12px;border-bottom:3px solid #2f5d8a;margin-bottom:6px}
h2{font-size:21px;font-weight:700;color:#191c20;margin-top:34px;margin-bottom:10px;
   padding-bottom:5px;border-bottom:1px solid #d9dbdf}
h3{font-size:16px;font-weight:700;color:#c81d1d;margin-top:22px;margin-bottom:7px}
h4{font-size:13.5px;font-weight:700;color:#191c20;margin-top:16px;margin-bottom:5px;
   text-transform:uppercase;letter-spacing:.4px}
p{font-size:13.5px;margin:9px 0}
ul,ol{margin:9px 0 9px 26px}
li{font-size:13.5px;margin:4px 0}
strong{font-weight:700;color:#191c20}
em{font-style:italic}
code{font-family:'Consolas',monospace;font-size:12.5px;background:#f0f1f3;
     padding:1px 5px;border-radius:3px}
hr{border:0;border-top:1px solid #d9dbdf;margin:26px 0}
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:12px}
th{background:#191c20;color:#fff;text-align:left;padding:8px 10px;
   font-weight:700;border:1px solid #191c20}
td{padding:7px 10px;border:1px solid #cfd2d6;vertical-align:top}
tr:nth-child(even) td{background:#f5f6f7}
blockquote{margin:12px 0;padding:8px 16px;background:#fbf2f2;
           border-left:3px solid #2f5d8a;font-size:12.5px;color:#3a3d42}
blockquote strong{color:#c81d1d}
.note{font-size:12px;color:#6a6e75;font-style:italic;margin:9px 0}
.figure{margin:22px auto;text-align:center}
.figure .frame{margin:0 auto;overflow:hidden;border-radius:10px;
               box-shadow:0 4px 18px rgba(0,0,0,.28)}
.figure iframe{border:0;display:block}
@media print{
  body{background:#fff;padding:0}
  .doc{box-shadow:none;max-width:100%;padding:0}
  .figure .frame{box-shadow:none;border:1px solid #ccc}
}
"""


def inline_md(text: str) -> str:
    """Escape HTML, then apply inline markdown: **bold**, *italic*, `code`, [link](url)."""
    out = html.escape(text)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                 lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+?)`", r"<code>\1</code>", out)
    return out


def natural_size(name: str, graphics_dir: Path) -> tuple[int, int]:
    """Natural pixel size of a graphic, measured from its rendered PNG.

    /proposal-graphics renders each graphic to graphics/rendered/<name>.png at
    its natural size, so the PNG's dimensions are the size the HTML graphic
    wants to display at. Falls back to a square default if the PNG (or PIL) is
    unavailable — the figure still embeds, just without an exact aspect ratio.
    """
    png = graphics_dir / "rendered" / f"{name}.png"
    try:
        from PIL import Image
        with Image.open(png) as im:
            return im.size
    except Exception:
        return DEFAULT_FIGURE_SIZE


def render_figure(name: str, graphics_dir: Path) -> str:
    """Inline an HTML graphic as a sandboxed, CSS-scaled iframe."""
    fig_path = graphics_dir / f"{name}.html"
    if not fig_path.exists():
        return f'<p class="note">[figure not found: {name}]</p>'
    nat_w, nat_h = natural_size(name, graphics_dir)
    scale = CONTENT_WIDTH / nat_w
    frame_w = round(nat_w * scale)
    frame_h = round(nat_h * scale)
    srcdoc = html.escape(fig_path.read_text(encoding="utf-8"), quote=True)
    return (
        '<div class="figure"><div class="frame" '
        f'style="width:{frame_w}px;height:{frame_h}px">'
        f'<iframe srcdoc="{srcdoc}" scrolling="no" '
        f'style="width:{nat_w}px;height:{nat_h}px;'
        f'transform:scale({scale:.5f});transform-origin:top left"></iframe>'
        "</div></div>"
    )


def render_table(rows: list[str]) -> str:
    parsed = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    parsed = [r for r in parsed if not all(re.fullmatch(r":?-+:?", c or "-") for c in r)]
    if not parsed:
        return ""
    head, *body = parsed
    out = ["<table><thead><tr>"]
    out += [f"<th>{inline_md(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def convert(md_text: str, graphics_dir: Path) -> str:
    # figure markers first — protect them, strip other HTML comments
    md_text = re.sub(r"<!--(?!\s*figure:).*?-->", "", md_text, flags=re.DOTALL)
    lines = md_text.split("\n")
    body: list[str] = []
    i = 0
    list_stack: list[str] = []  # open list tags

    def close_lists(to_level: int = 0):
        while len(list_stack) > to_level:
            body.append(f"</{list_stack.pop()}>")

    while i < len(lines):
        line = lines[i].rstrip()
        s = line.strip()

        if not s:
            close_lists()
            i += 1
            continue

        fig = re.match(r"<!--\s*figure:\s*([\w-]+)\s*-->", s)
        if fig:
            close_lists()
            body.append(render_figure(fig.group(1), graphics_dir))
            i += 1
            continue

        if re.fullmatch(r"-{3,}", s):
            close_lists()
            body.append("<hr>")
            i += 1
            continue

        h = re.match(r"(#{1,4})\s+(.*)", s)
        if h:
            close_lists()
            lvl = len(h.group(1))
            body.append(f"<h{lvl}>{inline_md(h.group(2).strip())}</h{lvl}>")
            i += 1
            continue

        if s.startswith("|"):
            close_lists()
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            body.append(render_table(tbl))
            continue

        if s.startswith("> "):
            close_lists()
            body.append(f"<blockquote>{inline_md(s[2:].strip())}</blockquote>")
            i += 1
            continue

        bullet = re.match(r"^(\s*)[-*]\s+(.*)", line)
        numbered = re.match(r"^(\s*)\d+\.\s+(.*)", line)
        if bullet or numbered:
            m = bullet or numbered
            tag = "ul" if bullet else "ol"
            level = len(m.group(1)) // 2 + 1
            while len(list_stack) < level:
                body.append(f"<{tag}>")
                list_stack.append(tag)
            while len(list_stack) > level:
                body.append(f"</{list_stack.pop()}>")
            body.append(f"<li>{inline_md(m.group(2).strip())}</li>")
            i += 1
            continue

        close_lists()
        if s.startswith("*") and s.endswith("*") and not s.startswith("**"):
            body.append(f'<p class="note">{inline_md(s.strip("*").strip())}</p>')
        else:
            body.append(f"<p>{inline_md(s)}</p>")
        i += 1

    close_lists()
    return "\n".join(body)


def render_file(md_path: Path, out_dir: Path) -> Path:
    graphics_dir = md_path.parent.parent / "graphics"
    md_text = md_path.read_text(encoding="utf-8")
    title_m = re.search(r"^#\s+(.+)$", md_text, flags=re.MULTILINE)
    title = title_m.group(1).strip() if title_m else md_path.stem
    inner = convert(md_text, graphics_dir)
    page = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n</head>\n"
        f"<body>\n<div class=\"doc\">\n{inner}\n</div>\n</body>\n</html>\n"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{md_path.stem}.html"
    out_path.write_text(page, encoding="utf-8")
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Render proposal markdown to self-contained HTML.")
    ap.add_argument("files", nargs="*", help="Markdown file(s) to render")
    ap.add_argument("--proposal", help="Render the 4 narrative drafts for this proposal slug")
    ap.add_argument("--outdir", help="Output directory (default: <proposal>/final/html)")
    args = ap.parse_args()

    targets: list[Path] = []
    out_dir: Path | None = Path(args.outdir) if args.outdir else None

    if args.proposal:
        base = WORKSPACE_ROOT / "proposals" / args.proposal
        for name in ("whitepaper", "system-blueprint", "tech-dev-plan-rom", "company-profile"):
            p = base / "drafts" / f"{name}.md"
            if p.exists():
                targets.append(p)
        if out_dir is None:
            out_dir = base / "final" / "html"
    for f in args.files:
        targets.append(Path(f).resolve())

    if not targets:
        ap.error("no input files (pass file paths or --proposal <slug>)")

    for md_path in targets:
        od = out_dir or (md_path.parent.parent / "final" / "html")
        out = render_file(md_path, od)
        print(f"  [OK]  {md_path.name}  ->  {out}")
    print(f"Done — {len(targets)} file(s) rendered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
