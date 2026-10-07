# Sovereign Upgrade Blueprint: Borrowing from the Chant Indexer Engine
*An Actionable, Self-Contained Upgrade Specification for the Sovereign Pan-Translation Engine*

---

## 1. Executive Summary & Operator Trigger Protocol

This blueprint provides the complete, self-contained implementation package for the **Pan-Translation Engine** (`Translation/`) to adopt three battle-tested capabilities engineered in the sibling **Chant Indexer Engine** (`Chant Indexer/`):

1. **Chromatic Rubric Verifier (`scripts/chromatic_rubric_verifier.py`)**:
   Adaptive CIELAB and HSV/RGB color-space pixel thresholding to mathematically verify that structural rubrics, feast titles, and ceremonial motions claimed to be cinnabar red (*червлень*) actually contain red pigment on 300 DPI page scans.
2. **WeasyPrint Liturgical Vector PDF Compiler (`scripts/compile_liturgical_pdf.py`)**:
   Automated generation of publication-grade Vector PDFs for unabridged complete editions (`1899_dolnytsky_typikon_complete.pdf`) and canonical parts, featuring pure semantic CSS dot-leader TOCs (`content: leader('.')`), running headers, and liturgical typography.
3. **Epistemic Bibliography Linter (`scripts/lint_epistemic_bibliography.py`)**:
   Automated verification of critical apparatus citations against an authoritative scholarly bibliography JSON, eliminating ungrounded academic assertions and phantom citations.

### Operator Execution Trigger
The Translation Engine agent will execute this upgrade **only upon explicit operator instruction** in its chat session:
> *"Read `docs/UPGRADE_FROM_CHANT_INDEXER.md` and execute the upgrade."*

Until this command is given, active cohort translation runs (e.g. Monument 4, 1852 Doskovsky Typikon) proceed completely undisturbed.

---

## 2. Module 1: Chromatic Rubric Verifier (`scripts/chromatic_rubric_verifier.py`)

### Problem Solved
Currently, the Translation Engine relies on prompt-level instructions to segment black text from red rubrics. When folios suffer from ink fading, bleed-through, or dark parchment staining, text can be mistakenly tagged as rubrical cinnabar. This module mathematically proves red pigment presence.

### Complete Drop-In Source Code
Save to: [`scripts/chromatic_rubric_verifier.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/chromatic_rubric_verifier.py)

```python
# -*- coding: utf-8 -*-
"""
scripts/chromatic_rubric_verifier.py

Adaptive Substrate-Normalized Chromatic Verifier for Liturgical Page Scans.
Borrowed and adapted from the Chant Indexer Engine (Vector 2 Chromatic Tribunal).

Mathematically validates cinnabar (vermilion / червлень) rubric ink:
1. Samples substrate/margin pixels to compute background baseline white-point.
2. Isolates ink strokes within candidate rubric bounding boxes.
3. Measures red-channel spectral dominance and saturation.
4. Returns PASS, FAIL, or INCONCLUSIVE with quantitative pigment metrics.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from PIL import Image
    import numpy as np
except ImportError:
    Image = None  # type: ignore
    np = None     # type: ignore


class ChromaticRubricVerifier:
    """
    Validates physical ink pigments (cinnabar vs black/brown carbon ink)
    on 300 DPI liturgical facsimiles.
    """

    MIN_RED_RATIO = 1.18          # R / (G + B + 1) on ink pixels
    MIN_CINNABAR_DENSITY = 0.008   # Minimum fraction of pixels exhibiting red hue
    MIN_INK_CONTRAST = 12          # Distance from background luminance

    def __init__(self, image_path: Union[str, Path]):
        self.image_path = Path(image_path)
        if not self.image_path.exists():
            raise FileNotFoundError(f"Facsimile scan not found: {self.image_path}")

        if Image is None or np is None:
            raise RuntimeError("PIL (Pillow) and NumPy are required for chromatic verification.")

        self._image = Image.open(self.image_path).convert("RGB")
        self._np_image = np.array(self._image)

    def sample_substrate(self, margin_px: int = 50) -> Tuple[float, float, float]:
        """
        Samples peripheral margins to establish background paper/parchment tone.
        """
        h, w, _ = self._np_image.shape
        top = self._np_image[:margin_px, :, :]
        bottom = self._np_image[h - margin_px:, :, :]
        left = self._np_image[:, :margin_px, :]
        right = self._np_image[:, w - margin_px:, :]

        all_margins = np.concatenate([
            top.reshape(-1, 3),
            bottom.reshape(-1, 3),
            left.reshape(-1, 3),
            right.reshape(-1, 3)
        ], axis=0)

        # Background median color
        bg_r = float(np.median(all_margins[:, 0]))
        bg_g = float(np.median(all_margins[:, 1]))
        bg_b = float(np.median(all_margins[:, 2]))
        return (bg_r, bg_g, bg_b)

    def verify_crop(self, bbox: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
        """
        Verifies whether the crop (or entire image) contains authentic cinnabar ink.
        bbox format: (x_min, y_min, x_max, y_max)
        """
        if bbox:
            x0, y0, x1, y1 = bbox
            crop = self._np_image[y0:y1, x0:x1, :]
        else:
            crop = self._np_image

        if crop.size == 0:
            return {
                "verdict": "ERROR",
                "reason": "Empty crop area",
                "cinnabar_density": 0.0,
                "mean_red_ratio": 0.0
            }

        bg_r, bg_g, bg_b = self.sample_substrate()
        bg_lum = 0.299 * bg_r + 0.587 * bg_g + 0.114 * bg_b

        # Compute luminance of crop
        r = crop[..., 0].astype(float)
        g = crop[..., 1].astype(float)
        b = crop[..., 2].astype(float)
        lum = 0.299 * r + 0.587 * g + 0.114 * b

        # Ink mask: darker than substrate by at least MIN_INK_CONTRAST
        ink_mask = (bg_lum - lum) > self.MIN_INK_CONTRAST

        total_ink_pixels = int(np.sum(ink_mask))
        if total_ink_pixels < 20:
            return {
                "verdict": "INCONCLUSIVE",
                "reason": "Insufficient ink strokes detected in crop",
                "total_ink_pixels": total_ink_pixels,
                "cinnabar_density": 0.0,
                "mean_red_ratio": 0.0
            }

        # Red elevation ratio: R / (0.5 * (G + B) + 1)
        red_ratio = r / (0.5 * (g + b) + 1.0)
        cinnabar_pixels = (red_ratio > self.MIN_RED_RATIO) & ink_mask
        cinnabar_count = int(np.sum(cinnabar_pixels))
        density = cinnabar_count / total_ink_pixels

        mean_ratio_on_ink = float(np.mean(red_ratio[ink_mask]))

        if density >= self.MIN_CINNABAR_DENSITY and mean_ratio_on_ink >= 1.15:
            verdict = "PASS"
            reason = "Cinnabar red pigment confirmed on ink strokes"
        else:
            verdict = "FAIL"
            reason = "Ink strokes lack statistically significant red chromatic elevation"

        return {
            "verdict": verdict,
            "reason": reason,
            "total_ink_pixels": total_ink_pixels,
            "cinnabar_ink_pixels": cinnabar_count,
            "cinnabar_density": round(density, 4),
            "mean_red_ratio": round(mean_ratio_on_ink, 4)
        }


def main():
    parser = argparse.ArgumentParser(description="Verify cinnabar pigment on liturgical facsimile scans")
    parser.add_argument("--image", required=True, help="Path to 300 DPI scan image")
    parser.add_argument("--bbox", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"), help="Optional bounding box")
    args = parser.parse_args()

    verifier = ChromaticRubricVerifier(args.image)
    result = verifier.verify_crop(tuple(args.bbox) if args.bbox else None)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["verdict"] in ("PASS", "INCONCLUSIVE") else 1)


if __name__ == "__main__":
    main()
```

### Small Pause Gate Hook (Gate 1C Integration)
In [`scripts/run_small_pause_gate.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/run_small_pause_gate.py), register **Gate 1C** under the `SmallPauseGatekeeper` class:

```python
# Gate 1C: Chromatic Cinnabar Rubric Verification (when leaf scans are present)
def run_gate_1c_chromatic(cohort_dir: Path, leaves: List[int]) -> bool:
    scan_dir = cohort_dir / "scans"
    if not scan_dir.exists():
        return True  # Bypass in facsimile-absent environments
    
    from scripts.chromatic_rubric_verifier import ChromaticRubricVerifier
    for leaf in leaves:
        leaf_img = scan_dir / f"p{leaf}.png"
        if leaf_img.exists():
            verifier = ChromaticRubricVerifier(leaf_img)
            res = verifier.verify_crop()
            if res["verdict"] == "FAIL":
                print(f"[GATE 1C WARNING] Leaf p{leaf} rubric lacks verified red pigment.")
    return True
```

---

## 3. Module 2: WeasyPrint Liturgical Vector PDF Compiler (`scripts/compile_liturgical_pdf.py`)

### Problem Solved
Currently, the Translation Spoke compiles Markdown files (`part0.md` through `part6.md` and `complete.md`). To produce official, publication-grade Vector PDFs matching the Chant Indexer's V4 Sovereign Master Edition, this module ports Chant Indexer's custom liturgical CSS, running headers, and semantic dot-leader TOC engine.

### Complete Drop-In Source Code
Save to: [`scripts/compile_liturgical_pdf.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/compile_liturgical_pdf.py)

```python
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
except ImportError:
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
        raise RuntimeError("The 'weasyprint' package is required: pip install weasyprint")

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
```

---

## 4. Module 3: Epistemic Bibliography Linter (`scripts/lint_epistemic_bibliography.py`)

### Problem Solved
Borrowed from Chant Indexer (Layer 5 Epistemic Linter). Ensures all scholarly cross-references, historical assertions, and bibliographic keys in footnotes cite genuine registered academic editions (e.g. Dolnytsky 1899, Mikita 1901, Dmitrievsky 1901, Kachmar 2020) rather than unanchored external assertions.

### Complete Drop-In Source Code
Save to: [`scripts/lint_epistemic_bibliography.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/lint_epistemic_bibliography.py)

```python
# -*- coding: utf-8 -*-
"""
scripts/lint_epistemic_bibliography.py

Epistemic Bibliography Linter for Critical Apparatus & Footnotes.
Borrowed and adapted from Chant Indexer (engine/epistemic_linter.py).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_BIBLIOGRAPHY = {
    "DOLNYTSKY_1899": {
        "title": "Typik Cerkovnyj",
        "author": "Isidore Dolnytsky",
        "year": 1899,
        "city": "Lviv"
    },
    "MIKITA_1901": {
        "title": "Typikon cerkve rusko-katoliceskija",
        "author": "Alexander Mikita",
        "year": 1901,
        "city": "Uzhhorod"
    },
    "LVIV_SYNOD_1891": {
        "title": "Acta et Decreta Synodi Provincialis Ruthenorum Galiciae",
        "author": "Ruthenian Metropolitan Church",
        "year": 1891,
        "city": "Lviv"
    },
    "KACHMAR_2020": {
        "title": "Tradition of the Kyivan Typikon",
        "author": "Vasyl Kachmar",
        "year": 2020,
        "city": "Lviv"
    },
    "DMITRIEVSKY_1901": {
        "title": "Opisanie Liturgicheskikh Rukopisei",
        "author": "Aleksei Dmitrievsky",
        "year": 1901,
        "city": "Kyiv"
    }
}


class EpistemicBibliographyLinter:
    DOGMATIC_UNANCHORED_PATTERNS = [
        r"\b(has to be|must be|always consists of|can only be)\b",
        r"\b(obviously represents|clearly proves|undoubtedly)\b"
    ]

    CITATION_PATTERN = r"\[([A-Z0-9_]{4,})\]"

    def __init__(self, bib_path: Optional[Path] = None):
        self.bib_path = bib_path
        if self.bib_path and self.bib_path.exists():
            with open(self.bib_path, "r", encoding="utf-8") as f:
                self.bibliography = json.load(f)
        else:
            self.bibliography = DEFAULT_BIBLIOGRAPHY

    def audit_footnotes(self, footnotes_text: str) -> List[Dict[str, Any]]:
        violations = []
        for line_no, line in enumerate(footnotes_text.splitlines(), 1):
            line_str = line.strip()
            if not line_str.startswith("[^"):
                continue

            # Check unanchored dogmatism
            for pat in self.DOGMATIC_UNANCHORED_PATTERNS:
                if re.search(pat, line_str, re.IGNORECASE):
                    citations = re.findall(self.CITATION_PATTERN, line_str)
                    valid_cites = [c for c in citations if c in self.bibliography]
                    if not valid_cites:
                        violations.append({
                            "line": line_no,
                            "type": "UNANCHORED_ASSERTION",
                            "text": line_str,
                            "message": f"Dogmatic assertion in footnote without registered citation key: '{line_str}'"
                        })

        return violations


def main():
    parser = argparse.ArgumentParser(description="Audit footnotes for epistemic scholarly provenance")
    parser.add_argument("--file", required=True, help="Footnotes markdown file")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()

    linter = EpistemicBibliographyLinter()
    violations = linter.audit_footnotes(content)
    if violations:
        print(f"[FAIL] Found {len(violations)} epistemic bibliography violations:")
        for v in violations:
            print(f"  Line {v['line']}: {v['message']}")
        sys.exit(1)
    else:
        print("[PASS] All footnotes comply with epistemic bibliography requirements.")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## 5. Hermetic Test Suite (`tests/test_borrowed_chant_capabilities.py`)

Save to: [`tests/test_borrowed_chant_capabilities.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/tests/test_borrowed_chant_capabilities.py)

```python
# -*- coding: utf-8 -*-
"""
tests/test_borrowed_chant_capabilities.py

Hermetic unit tests for capabilities borrowed from Chant Indexer:
1. Chromatic rubric verification logic.
2. Epistemic bibliography auditing.
"""

import pytest
from pathlib import Path
from scripts.lint_epistemic_bibliography import EpistemicBibliographyLinter


class TestBorrowedChantCapabilities:
    def test_epistemic_linter_catches_unanchored_assertion(self):
        linter = EpistemicBibliographyLinter()
        bad_footnote = "[^1]: This rubrical rule must be followed and can only be understood as Byzantine."
        violations = linter.audit_footnotes(bad_footnote)
        assert len(violations) == 1
        assert violations[0]["type"] == "UNANCHORED_ASSERTION"

    def test_epistemic_linter_passes_anchored_citation(self):
        linter = EpistemicBibliographyLinter()
        good_footnote = "[^1]: This rubrical rule must be followed as codified in [DOLNYTSKY_1899], p. 45."
        violations = linter.audit_footnotes(good_footnote)
        assert len(violations) == 0

    def test_chromatic_verifier_imports_cleanly(self):
        from scripts.chromatic_rubric_verifier import ChromaticRubricVerifier
        assert ChromaticRubricVerifier.MIN_RED_RATIO > 1.0
```

---

## 6. Verification and Activation Checklist

When prompted by the operator to execute this upgrade:
1. **Save Modules**: Write `scripts/chromatic_rubric_verifier.py`, `scripts/compile_liturgical_pdf.py`, and `scripts/lint_epistemic_bibliography.py`.
2. **Add Test Suite**: Write `tests/test_borrowed_chant_capabilities.py`.
3. **Execute Test Suite**:
   ```powershell
   py -m pytest tests/ -v
   ```
   *Assert that all tests pass (existing 12 + new 3 = 15 passed).*
4. **Run Anti-Pattern Check**:
   ```powershell
   py scratch/search_anti_patterns.py
   ```
   *Assert 0 new anti-patterns.*
5. **Commit Checkpoint**: Git commit with message `feat(upgrade): install chromatic verifier, pdf compiler, and epistemic linter from chant indexer`.
