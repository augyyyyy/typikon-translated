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
