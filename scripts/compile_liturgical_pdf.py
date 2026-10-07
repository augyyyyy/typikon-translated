# -*- coding: utf-8 -*-
"""
scripts/compile_liturgical_pdf.py

Publication-Grade Liturgical Vector PDF Compiler.
Borrowed and adapted from Chant Indexer (engine/pdf_generator.py).

Features:
- Pure semantic CSS dot-leader Table of Contents (`content: leader('.')`).
- Running headers and folio marginalia via CSS Paged Media (@page).
- Byzantine-Ruthenian liturgical color schemes (Deep Navy #1a365d, Cinnabar #9b111e).
- Table and rubric page-break optimization.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import markdown
except ImportError:
    markdown = None

try:
    from weasyprint import HTML, CSS
except (ImportError, OSError):
    HTML = None
    CSS = None


LITURGICAL_CSS = """
@page {
    size: letter portrait;
    margin: 20mm 15mm 20mm 15mm;
    @top-center {
        content: "BYZANTINE-RUTHENIAN LITURGICAL MONUMENTS";
        font-family: 'Charis SIL', 'Times New Roman', serif;
        font-size: 8pt;
        color: #718096;
        border-bottom: 0.5pt solid #cbd5e0;
        padding-bottom: 2mm;
    }
    @bottom-center {
        content: counter(page);
        font-family: 'Charis SIL', 'Times New Roman', serif;
        font-size: 9pt;
        color: #4a5568;
    }
}

body {
    font-family: 'Charis SIL', 'Cambria', 'Times New Roman', serif;
    font-size: 10.5pt;
    line-height: 1.45;
    color: #1a202c;
    background-color: #ffffff;
}

h1 {
    font-size: 18pt;
    color: #1a365d;
    text-align: center;
    border-bottom: 2pt solid #2b6cb0;
    padding-bottom: 4mm;
    margin-top: 10mm;
    margin-bottom: 6mm;
    page-break-before: always;
}

h2 {
    font-size: 13pt;
    color: #2c5282;
    border-bottom: 1pt solid #e2e8f0;
    padding-bottom: 2mm;
    margin-top: 6mm;
    margin-bottom: 3mm;
    page-break-after: avoid;
}

h3 {
    font-size: 11pt;
    color: #9b111e; /* Cinnabar Red */
    margin-top: 4mm;
    margin-bottom: 2mm;
    page-break-after: avoid;
}

blockquote {
    border-left: 3pt solid #9b111e;
    margin-left: 0;
    padding-left: 4mm;
    color: #4a5568;
    font-style: italic;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 4mm;
    margin-bottom: 4mm;
    font-size: 9pt;
    page-break-inside: avoid;
}

th, td {
    border: 0.5pt solid #cbd5e0;
    padding: 2mm 3mm;
    text-align: left;
}

th {
    background-color: #f7fafc;
    color: #2d3748;
    font-weight: bold;
}

/* Pure CSS Dot Leaders for Table of Contents */
ul.toc {
    list-style: none;
    padding-left: 0;
}

ul.toc li {
    margin-bottom: 2mm;
}

ul.toc a {
    text-decoration: none;
    color: #2b6cb0;
    display: flex;
    justify-content: space-between;
}

ul.toc a::after {
    content: leader('.') " p. " target-counter(attr(href), page);
    color: #a0aec0;
}
"""


def compile_markdown_to_pdf(md_path: Path, output_pdf_path: Optional[Path] = None) -> Path:
    if markdown is None:
        raise RuntimeError("The 'markdown' package is required: pip install markdown")
    if HTML is None:
        raise RuntimeError(
            "The 'weasyprint' package and its underlying GTK/Pango libraries are required: pip install weasyprint"
        )

    md_path = Path(md_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    out_path = output_pdf_path or md_path.with_suffix(".pdf")

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "footnotes", "toc", "fenced_code"]
    )

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{md_path.stem}</title>
</head>
<body>
{html_body}
</body>
</html>"""

    html_doc = HTML(string=full_html)
    css_doc = CSS(string=LITURGICAL_CSS)
    html_doc.write_pdf(target=str(out_path), stylesheets=[css_doc])
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Compile publication-grade liturgical Vector PDF")
    parser.add_argument("--input", required=True, help="Path to input markdown file")
    parser.add_argument("--output", help="Optional output PDF path")
    args = parser.parse_args()

    out = compile_markdown_to_pdf(Path(args.input), Path(args.output) if args.output else None)
    print(f"[SUCCESS] Compiled Vector PDF: {out}")


if __name__ == "__main__":
    main()
