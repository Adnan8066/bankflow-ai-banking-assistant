#!/usr/bin/env python3
"""Rasterize a PDF into page PNGs for visual QA (pypdfium2 based).

Usage: python pdf_to_png.py input.pdf out_dir [dpi] [first] [last]
"""
from __future__ import annotations

import sys
from pathlib import Path

import pypdfium2 as pdfium


def main() -> None:
    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 110
    first = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    last = int(sys.argv[5]) if len(sys.argv) > 5 else 0

    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    total = len(pdf)
    stop = last if last else total
    scale = dpi / 72

    for index in range(first - 1, min(stop, total)):
        page = pdf[index]
        image = page.render(scale=scale).to_pil()
        target = out_dir / f"page-{index + 1:04d}.png"
        image.save(target)
    print(f"pdf pages: {total}; wrote {max(0, min(stop, total) - first + 1)} png(s) to {out_dir}")


if __name__ == "__main__":
    main()
