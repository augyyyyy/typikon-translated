#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_linters_and_gates.py

Hermetic unit tests for the Liturgical Linters & Small Pause Gate suites:
  1. scripts/lint_liturgical_slop.py
  2. scripts/hieratic_pronoun_audit.py
"""

import sys
import unittest
import tempfile
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lint_liturgical_slop import lint_slop, PROHIBITED_CATEGORIES
from hieratic_pronoun_audit import audit_file


class TestLintersAndGates(unittest.TestCase):
    def test_lint_liturgical_slop_clean_text(self):
        """Verifies clean liturgical translation passes without violations."""
        clean_text = (
            "# Divine Liturgy of Saint John Chrysostom\n\n"
            "The priest takes the censer and censes the Holy Table in a circle, "
            "proclaiming: Blessed is the kingdom of the Father and of the Son and of the Holy Spirit, "
            "now and forever, and unto the ages of ages.\n"
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(clean_text)
            f_path = Path(f.name)

        try:
            res = lint_slop(f_path)
            self.assertTrue(res["passed"])
            self.assertEqual(res["violation_count"], 0)
        finally:
            if f_path.exists():
                f_path.unlink()

    def test_lint_liturgical_slop_catches_violations(self):
        """Verifies slop linter detects pseudo-archaisms, AI clichés, and rubrical shall-bombing."""
        dirty_text = (
            "Verily, this holy temple stands as a testament to our rich history. "
            "Betwixt the icons, the deacon shall bow before the Holy Doors.\n"
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(dirty_text)
            f_path = Path(f.name)

        try:
            res = lint_slop(f_path)
            self.assertFalse(res["passed"])
            self.assertGreater(res["violation_count"], 0)
            violations = res["violations"]
            self.assertTrue(any("verily" in v.get("matched_text", "").lower() for v in violations))
            self.assertTrue(any("testament to" in v.get("matched_text", "").lower() for v in violations))
            self.assertTrue(any("shall bow" in v.get("matched_text", "").lower() for v in violations))
        finally:
            if f_path.exists():
                f_path.unlink()

    def test_hieratic_pronoun_audit_clean_text(self):
        """Verifies deity pronoun audit passes when divine pronouns are capitalized and clergy are lowercase."""
        text = (
            "Glory to Thee, our God, glory to Thee. O Heavenly King, Comforter, the Spirit of Truth, "
            "Who art everywhere and fillest all things. Have mercy on us, O Lord, and save us. "
            "The priest bows his head and the deacon departs to the sacristy.\n"
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(text)
            f_path = Path(f.name)

        try:
            res = audit_file(f_path)
            self.assertTrue(res["passed"], f"Expected clean pass, got: {res['violations']}")
            self.assertEqual(res["violation_count"], 0)
        finally:
            if f_path.exists():
                f_path.unlink()

    def test_hieratic_pronoun_audit_catches_lowercase_deity(self):
        """Verifies deity pronoun audit flags lowercase pronouns directly associated with the Godhead."""
        dirty_prayer = "O Lord, hear us, for we worship thee.\n"
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(dirty_prayer)
            f_path = Path(f.name)

        try:
            res = audit_file(f_path)
            self.assertFalse(res["passed"], "Expected audit to fail on lowercase 'thee'")
            self.assertGreater(res["violation_count"], 0)
        finally:
            if f_path.exists():
                f_path.unlink()


if __name__ == "__main__":
    unittest.main()
