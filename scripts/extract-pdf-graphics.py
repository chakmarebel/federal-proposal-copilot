#!/usr/bin/env python3
"""
Render selected pages of a PDF to PNG for visual structural analysis.

Companion to scripts/extract-pdf-patterns.py — that script extracts text
patterns; this one renders pages so a human (or model with vision) can
analyze graphics, layouts, font hierarchy, callout conventions, color
palette structure, and complexity norms.

Output PNGs are written to a temp directory the caller specifies (or a
default tempdir under the system temp folder). The caller is expected to
review the renders, extract STRUCTURAL learning, and DELETE the temp
directory afterward — no source-derived imagery should land in the repo.

Usage:
    python scripts/extract-pdf-graphics.py <pdf> --pages 1,3,8,12 --out /tmp/graphics-analysis
    python scripts/extract-pdf-graphics.py <pdf> --pages 1-5,8,12-15 --dpi 144

DPI 144 is the default — readable at screen size. Use 200+ for fine-detail
inspection (font face, kerning, etc.).
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

import fitz  # PyMuPDF


def parse_page_spec(spec: str, max_page: int) -> list[int]:
    """Parse '1,3,8-12' into [1, 3, 8, 9, 10, 11, 12]. 1-indexed."""
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return [p for p in sorted(set(out)) if 1 <= p <= max_page]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--pages", required=True, help="e.g., '1,3,8-12'")
    ap.add_argument("--out", type=Path, help="Output directory (default: temp dir)")
    ap.add_argument("--dpi", type=int, default=144, help="Render DPI (default 144)")
    args = ap.parse_args(argv)

    if not args.pdf.exists():
        print(f"error: {args.pdf} not found", file=sys.stderr)
        return 1

    out_dir = args.out or Path(tempfile.mkdtemp(prefix="pdf-pages-"))
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(args.pdf))
    n_pages = doc.page_count
    pages = parse_page_spec(args.pages, n_pages)
    if not pages:
        print(f"error: no valid pages in '{args.pages}' (PDF has {n_pages} pages)", file=sys.stderr)
        return 1

    zoom = args.dpi / 72  # PDF point is 1/72 inch
    matrix = fitz.Matrix(zoom, zoom)

    print(f"=== {args.pdf.name} ({n_pages} pages) -> {out_dir} @ {args.dpi} DPI ===")
    rendered: list[Path] = []
    for p in pages:
        page = doc.load_page(p - 1)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        # Pad page number so files sort numerically
        out_path = out_dir / f"page-{p:03d}.png"
        pix.save(str(out_path))
        rendered.append(out_path)
        print(f"  pg {p:>3}: {out_path}  ({pix.width}x{pix.height})")
    doc.close()

    print()
    print(f"Wrote {len(rendered)} PNG(s) to {out_dir}")
    print()
    print("Reminder: this directory holds source-derived imagery. After analysis, delete it:")
    print(f"  rm -rf {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
