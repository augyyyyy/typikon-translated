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
