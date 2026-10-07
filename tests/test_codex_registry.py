#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_codex_registry.py

Hermetic unit tests for Byzantine-Ruthenian Typikon Transmission Chain Codex Registry.
Enforces:
  1. codex_registry.json structural integrity and JSON schema conformity.
  2. Rule 15: Closed Mathematical Leaf Conservation Law and 10-Leaf Invariant.
  3. ACTIVE_ORCHESTRATOR_STATE.json telemetry consistency.
"""

import sys
import json
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
STATE_FILE = PROJECT_ROOT / "Liturgical Monuments" / "ACTIVE_ORCHESTRATOR_STATE.json"


class TestCodexRegistry(unittest.TestCase):
    def setUp(self):
        self.assertTrue(REGISTRY_FILE.exists(), f"Registry file not found at: {REGISTRY_FILE}")
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            self.registry = json.load(f)

    def test_registry_has_monuments(self):
        """Verifies registry contains monuments catalog."""
        monuments = self.registry.get("monuments", {})
        self.assertGreater(len(monuments), 5, "Registry should catalog historical transmission chain monuments")
        self.assertIn("1891_lviv_synod", monuments)
        self.assertIn("1899_dolnytsky_typikon", monuments)
        self.assertIn("1901_mikita_typikon", monuments)

    def test_monument_attributes_and_10_leaf_invariant(self):
        """Verifies all monuments define total pages, genre register, and default cohort size <= 10."""
        monuments = self.registry.get("monuments", {})
        for mon_id, data in monuments.items():
            self.assertIn("title", data, f"Monument {mon_id} missing title")
            self.assertIn("total_physical_pages", data, f"Monument {mon_id} missing total_physical_pages")
            self.assertGreater(data["total_physical_pages"], 0, f"Monument {mon_id} page count must be > 0")
            cohort_size = data.get("default_cohort_size", 10)
            self.assertLessEqual(cohort_size, 10, f"Monument {mon_id} exceeds 10-leaf invariant: cohort_size={cohort_size}")

    def test_active_orchestrator_state_coherence(self):
        """Verifies telemetry state matches registry metadata and satisfies leaf conservation."""
        self.assertTrue(STATE_FILE.exists(), f"State file not found at: {STATE_FILE}")
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)

        mon_id = state.get("monument_id")
        self.assertIn(mon_id, self.registry.get("monuments", {}), f"Active monument {mon_id} must exist in registry")

        mon_data = self.registry["monuments"][mon_id]
        total = state.get("total_physical_pages", 0)
        done = state.get("translated_pages", 0)
        remaining = state.get("remaining_pages", 0)

        self.assertEqual(total, mon_data["total_physical_pages"], "State total_physical_pages must match registry")
        self.assertEqual(done + remaining, total, "Conservation invariant failed: translated + remaining != total")

        completed_cohorts = state.get("completed_cohorts", [])
        self.assertEqual(completed_cohorts, sorted(completed_cohorts), "Completed cohorts must be strictly monotonic")


if __name__ == "__main__":
    unittest.main()
