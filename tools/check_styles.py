#!/usr/bin/env python3
"""Inspect the DOCX styles to confirm formatting rules (black headings, no title border)."""
from __future__ import annotations

import sys
import zipfile

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def main() -> None:
    path = sys.argv[1]
    with zipfile.ZipFile(path) as archive:
        root = etree.fromstring(archive.read("word/styles.xml"))

    for style_id in ("Title", "Heading1", "Heading2", "Heading3", "CodeBlock", "Normal"):
        found = root.xpath(f'//w:style[@w:styleId="{style_id}"]', namespaces=NS)
        if not found:
            print(f"{style_id}: not found")
            continue
        style = found[0]
        colors = style.xpath(".//w:rPr/w:color", namespaces=NS)
        borders = style.xpath(".//w:pPr/w:pBdr", namespaces=NS)
        fonts = style.xpath(".//w:rPr/w:rFonts", namespaces=NS)
        sizes = style.xpath(".//w:rPr/w:sz", namespaces=NS)
        color_desc = etree.tostring(colors[0]).decode() if colors else "none"
        font_desc = fonts[0].get(f"{{{W}}}ascii") if fonts else "none"
        size_desc = sizes[0].get(f"{{{W}}}val") if sizes else "none"
        print(
            f"{style_id}: color={color_desc} | paragraph_borders={len(borders)} "
            f"| font={font_desc} | half_points={size_desc}"
        )


if __name__ == "__main__":
    main()
