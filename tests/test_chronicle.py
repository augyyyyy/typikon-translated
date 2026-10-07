#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_chronicle.py

Hermetic unit tests for the Universal Lab Chronicle & Ledger of Intent Framework (LCP v1.0).
Verifies:
  1. Structural integrity of CHRONICLE.md (Chapters 1-4, Lab Bench, Ledger of Intent).
  2. Tabular milestones in the Ledger of Intent.
  3. Programmatic synchronization via ChronicleManager.sync_bench().
  4. Compliance with MTS-1 Anti-Slop standards (Zero pseudo-archaic slop or AI clichés).
"""

import sys
import os
import unittest
import tempfile
import shutil
from pathlib import Path

# Add project root and scripts to sys.path
TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from chronicle_manager import ChronicleManager


class TestLabChronicle(unittest.TestCase):
    def setUp(self):
        self.chronicle_path = ChronicleManager.get_chronicle_path()

    def test_chronicle_file_exists_and_has_chapters(self):
        """Verifies CHRONICLE.md exists and contains the four historical chapters."""
        self.assertTrue(self.chronicle_path.exists(), "CHRONICLE.md should exist at project root")
        text = ChronicleManager.get_chronicle_text()
        self.assertIn("# The Byzantine-Ruthenian Typikon Translation Lab Chronicle: Voyage Towards Complete Monument Transmission", text)
        self.assertIn("## Chapter 1: The Epigraphic Inception & The Native Vision Mandate", text)
        self.assertIn("## Chapter 2: The Two-Chat Stutter & The Inviolable Autonomous Execution Mandate", text)
        self.assertIn("## Chapter 3: The 591-Leaf Marathon, Table Sprawl, and The 10-Leaf Invariant", text)
        self.assertIn("## Chapter 4: The 400-Year Codicological Reorganization & Transmission Chain Scaling", text)
        self.assertIn("## Today’s Lab Bench (The Present Horizon)", text)
        self.assertIn("## The Uncharted Horizon (Ledger of Intent)", text)

    def test_chronicle_ledger_of_intent_table(self):
        """Verifies the Ledger of Intent contains required markers and milestones."""
        text = ChronicleManager.get_chronicle_text()
        self.assertIn("Monument 0: 2010 Lviv Typikon", text)
        self.assertIn("Monument 1: 1891 Lviv Synod", text)
        self.assertIn("Monument 2: 1899 Dolnytsky Typikon", text)
        self.assertIn("Marker 1.0: LCP v1.0 Framework", text)
        self.assertIn("Monument 3: 1901 Mikita Typikon (Part I: Cohorts 1–11)", text)
        self.assertIn("Monument 3: 1901 Mikita Typikon (Part II: Cohorts 12–32)", text)
        self.assertIn("Monument 3: Mikita Grand Pause & Autopsy PA-004", text)

    def test_sync_chronicle_bench_updates_state(self):
        """Verifies sync_bench updates bench attributes and ledger markers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_chronicle = Path(tmpdir) / "CHRONICLE.md"
            shutil.copyfile(self.chronicle_path, temp_chronicle)

            original_path = ChronicleManager.CHRONICLE_PATH
            try:
                ChronicleManager.CHRONICLE_PATH = temp_chronicle
                success = ChronicleManager.sync_bench(
                    commit_hash="abc1234",
                    working_state="Test Execution · 12 / 12 Hermetic Unit Tests Green",
                    built_summary="Institutionalized Marker 1.0 and verified test harness.",
                    bench_event="All hermetic tests passed cleanly in pytest runner.",
                    active_hypothesis="LCP v1.0 framework guarantees zero regression to past crises.",
                    marker_updates={"Marker 1.0: LCP v1.0 Framework": "✅ Sealed"},
                    date_str="October 06, 2026"
                )
                self.assertTrue(success)

                updated_text = ChronicleManager.get_chronicle_text()
                self.assertIn("**Active Commit:** `abc1234`", updated_text)
                self.assertIn("**Working State:** Test Execution · 12 / 12 Hermetic Unit Tests Green", updated_text)
                self.assertIn("Institutionalized Marker 1.0 and verified test harness.", updated_text)
                self.assertIn("| **Marker 1.0: LCP v1.0 Framework** | ✅ Sealed |", updated_text)
            finally:
                ChronicleManager.CHRONICLE_PATH = original_path

    def test_chronicle_passes_validation_and_anti_slop(self):
        """Verifies CHRONICLE.md does not trip structural errors or anti-slop violations."""
        valid, violations = ChronicleManager.validate_chronicle_integrity()
        self.assertTrue(valid, f"Violations found in CHRONICLE.md: {violations}")
        self.assertEqual(len(violations), 0)

    def test_chronicle_get_git_commit(self):
        """Verifies git commit resolution returns a valid short hash or uncommitted marker."""
        commit = ChronicleManager.get_git_commit()
        self.assertIsInstance(commit, str)
        self.assertGreater(len(commit), 0)


if __name__ == "__main__":
    unittest.main()
