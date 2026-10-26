#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_sgc02_validators.py

Hermetic unit tests for SGC-02 / PE-HSG (Potemkin Epigraphy & Header-Span Goodhart Gaming)
validators across:
  1. scripts/assemble_and_sync_hub.py (extract_accounted_leaves without Regex #5 range interpolation)
  2. scripts/structural_audit.py (extract_accounted_leaves, parse_leaf_blocks, and audit_file)
  3. scripts/verify_publication_edition.py (PLACEHOLDER_PATTERNS)
  4. Externalized templates in data/templates/
"""

import re
import sys
import tempfile
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import assemble_and_sync_hub
import structural_audit
import verify_publication_edition


class TestSGC02Validators(unittest.TestCase):
    def test_range_header_interpolation_rejected(self):
        """Verifies PE-HSG-02: Range headers like (pp. 10-20) do NOT fabricate leaf indices p10..p20."""
        synthetic_range_text = (
            "## Chapters I-V (pp. 10-20)\n\n"
            "This synthetic block spans eleven pages without individual leaf banners.\n"
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(synthetic_range_text)
            f_path = Path(f.name)

        try:
            hub_leaves = assemble_and_sync_hub.extract_accounted_leaves(f_path)
            audit_leaves = structural_audit.extract_accounted_leaves(synthetic_range_text)
            self.assertEqual(hub_leaves, set(), "Range header must not interpolate leaf numbers in assemble_and_sync_hub")
            self.assertEqual(audit_leaves, set(), "Range header must not interpolate leaf numbers in structural_audit")
        finally:
            if f_path.exists():
                f_path.unlink()

    def test_explicit_leaf_headers_extracted_accurately(self):
        """Verifies explicit individual leaf banners (=== LEAF pN ===) are extracted 1:1."""
        valid_leaf_text = (
            "=== LEAF p1 ===\n"
            "First leaf liturgical rubric text with sufficient epigraphic substance.\n\n"
            "=== LEAF p2 ===\n"
            "Second leaf liturgical rubric text with sufficient epigraphic substance.\n"
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(valid_leaf_text)
            f_path = Path(f.name)

        try:
            hub_leaves = assemble_and_sync_hub.extract_accounted_leaves(f_path)
            audit_leaves = structural_audit.extract_accounted_leaves(valid_leaf_text)
            self.assertEqual(hub_leaves, {1, 2})
            self.assertEqual(audit_leaves, {1, 2})
        finally:
            if f_path.exists():
                f_path.unlink()

    def test_hollow_stub_leaf_detected_by_structural_audit(self):
        """Verifies PE-HSG-03: Hollow stub leaf blocks fail SGC-02 density thresholds."""
        hollow_text = (
            "=== LEAF p1 ===\n"
            "Stub.\n\n"
            "=== LEAF p2 ===\n"
            "Before the beginning of Great Vespers, the priest vested in the epitrachelion and phelonion "
            "censes the holy table around from all four sides according to the ancient custom.\n"
        )
        blocks = structural_audit.parse_leaf_blocks(hollow_text)
        self.assertEqual(set(blocks.keys()), {1, 2})
        self.assertLess(len(blocks[1]), 10)
        self.assertGreaterEqual(len(blocks[2]), 50)

        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write("=== LEAF p1 ===\nabc\n")
            f_path = Path(f.name)

        try:
            res = structural_audit.audit_structure(f_path, cohort_num=1)
            self.assertFalse(res["passed"])
            self.assertTrue(any("Empty or trivial leaf block" in a for a in res["anomalies"]))
        finally:
            if f_path.exists():
                f_path.unlink()

    def test_potemkin_placeholders_flagged_by_gate1(self):
        """Verifies PE-HSG-01 & PE-HSG-05: Gate 1 patterns detect diagram placeholders and translator notes."""
        samples = [
            "[INSERT DIAGRAM/TABLE HERE FROM ORIGINAL PDF]",
            "(Translator's Note: Pages 245-248 are omitted due to complexity.)",
            "[Summary: This section summarizes the fasts.]",
            "[Page 244]",
            "places Them on the skynia^[A] on the folded iliton",
        ]
        for sample in samples:
            matched = any(
                re.search(pat, sample, flags=re.IGNORECASE | re.MULTILINE)
                for pat, _ in verify_publication_edition.PLACEHOLDER_PATTERNS
            )
            self.assertTrue(matched, f"Expected Gate 1 placeholder pattern to flag: {sample!r}")

    def test_externalized_templates_exist(self):
        """Verifies PE-HSG-01: Externalized markdown templates exist in data/templates/."""
        templates_dir = PROJECT_ROOT / "data" / "templates"
        for tpl_name in (
            "dolnytsky_1899_master_toc.md",
            "monument_startup_directive_template.md",
            "work_order_template.md",
        ):
            tpl_path = templates_dir / tpl_name
            self.assertTrue(tpl_path.exists(), f"Missing externalized template: {tpl_path}")
            self.assertGreater(len(tpl_path.read_text(encoding="utf-8")), 100)


if __name__ == "__main__":
    unittest.main()
