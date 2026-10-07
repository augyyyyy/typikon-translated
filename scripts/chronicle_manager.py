#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/chronicle_manager.py

Programmatic Synchronization Engine for the Universal Lab Chronicle (LCP v1.0).
Provides programmatic and CLI access to read, validate, and synchronize
CHRONICLE.md's 'Today's Lab Bench' and 'Ledger of Intent'.
"""

import sys
import os
import re
import json
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CHRONICLE_PATH = PROJECT_ROOT / "CHRONICLE.md"
SLOP_LINTER = SCRIPT_DIR / "lint_liturgical_slop.py"


class ChronicleManager:
    """
    Authoritative state controller and synchronizer for CHRONICLE.md.
    """
    CHRONICLE_PATH = CHRONICLE_PATH

    @classmethod
    def get_chronicle_path(cls) -> Path:
        return cls.CHRONICLE_PATH

    @classmethod
    def get_chronicle_text(cls) -> str:
        if not cls.CHRONICLE_PATH.exists():
            return "CHRONICLE.md not found at project root."
        with open(cls.CHRONICLE_PATH, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def get_git_commit(cls) -> str:
        try:
            res = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                timeout=5
            )
            if res.returncode == 0:
                return res.stdout.strip()
        except Exception as e:
            print(f"[Warning] Failed to resolve git commit: {e}", file=sys.stderr)
        return "uncommitted"

    @classmethod
    def validate_chronicle_integrity(cls) -> Tuple[bool, List[str]]:
        violations: List[str] = []
        if not cls.CHRONICLE_PATH.exists():
            return False, ["CHRONICLE.md does not exist at project root."]

        text = cls.get_chronicle_text()

        # Check required architectural sections
        required_headers = [
            "# The Byzantine-Ruthenian Typikon Translation Lab Chronicle: Voyage Towards Complete Monument Transmission",
            "## Chapter 1: The Epigraphic Inception & The Native Vision Mandate",
            "## Chapter 2: The Two-Chat Stutter & The Inviolable Autonomous Execution Mandate",
            "## Chapter 3: The 591-Leaf Marathon, Table Sprawl, and The 10-Leaf Invariant",
            "## Chapter 4: The 400-Year Codicological Reorganization & Transmission Chain Scaling",
            "## Today’s Lab Bench (The Present Horizon)",
            "## The Uncharted Horizon (Ledger of Intent)",
        ]

        for hdr in required_headers:
            if hdr not in text:
                violations.append(f"Missing required section header: '{hdr}'")

        # Check Ledger milestones
        required_markers = [
            "Monument 0: 2010 Lviv Typikon",
            "Monument 1: 1891 Lviv Synod",
            "Monument 2: 1899 Dolnytsky Typikon",
            "Marker 1.0: LCP v1.0 Framework",
            "Monument 3: 1901 Mikita Typikon (Part I: Cohorts 1–11)",
            "Monument 3: 1901 Mikita Typikon (Part II: Cohorts 12–32)",
            "Monument 3: Mikita Grand Pause & Autopsy PA-004",
        ]

        for marker in required_markers:
            if marker not in text:
                violations.append(f"Missing required Ledger marker: '{marker}'")

        # Run anti-slop linter if script is present
        if SLOP_LINTER.exists():
            try:
                from lint_liturgical_slop import lint_slop
                res = lint_slop(cls.CHRONICLE_PATH)
                if not res.get("passed", True):
                    for item in res.get("violations", []):
                        violations.append(f"Slop violation ({item.get('category')}): '{item.get('matched_text')}' on line {item.get('line')}")
            except Exception as e:
                violations.append(f"Failed to execute slop linter: {e}")

        return len(violations) == 0, violations

    @classmethod
    def sync_bench(
        cls,
        commit_hash: Optional[str] = None,
        working_state: Optional[str] = None,
        built_summary: Optional[str] = None,
        bench_event: Optional[str] = None,
        active_hypothesis: Optional[str] = None,
        marker_updates: Optional[Dict[str, str]] = None,
        date_str: Optional[str] = None
    ) -> bool:
        if not cls.CHRONICLE_PATH.exists():
            return False

        with open(cls.CHRONICLE_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        git_rev = commit_hash or cls.get_git_commit()
        now_date = date_str or datetime.now(timezone.utc).strftime("%B %d, %Y")

        # Update Current Date
        content = re.sub(
            r"\*\*Current Date:[*]{2}\s*[^\n·]+",
            f"**Current Date:** {now_date} ",
            content
        )

        # Update Active Commit
        if git_rev and git_rev != "uncommitted":
            content = re.sub(
                r"\*\*Active Commit:[*]{2}\s*`[^`]+`",
                f"**Active Commit:** `{git_rev}`",
                content
            )

        # Update Working State
        if working_state:
            content = re.sub(
                r"(\*\*Working State:[*]{2}\s*)[^\n]+",
                rf"\g<1>{working_state}",
                content
            )

        # Update What Was Just Built
        if built_summary:
            content = re.sub(
                r"(\*\s+\*\*What Was Just Built:[*]{2}\s*)[^\n]+",
                rf"\g<1>{built_summary}",
                content
            )

        # Update Bench Event
        if bench_event:
            content = re.sub(
                r"(\*\s+\*\*What Just Happened on the Bench:[*]{2}\s*)[^\n]+",
                rf"\g<1>{bench_event}",
                content
            )

        # Update Active Hypothesis
        if active_hypothesis:
            content = re.sub(
                r"(\*\s+\*\*Active Hypothesis:[*]{2}\s*)[^\n]+",
                rf"\g<1>{active_hypothesis}",
                content
            )

        # Update Ledger of Intent markers
        if marker_updates:
            for marker_name, new_status in marker_updates.items():
                pattern = rf"(\|\s*\*\*{re.escape(marker_name)}[^*]*\*\*\s*\|)\s*[^|]+?\s*(\|)"
                content = re.sub(pattern, rf"\g<1> {new_status} \g<2>", content)

        with open(cls.CHRONICLE_PATH, "w", encoding="utf-8") as f:
            f.write(content)

        return True


def display_status() -> None:
    if not CHRONICLE_PATH.exists():
        print(f"CHRONICLE.md not found at: {CHRONICLE_PATH}")
        return

    text = ChronicleManager.get_chronicle_text()
    bench_match = re.search(r"## Today’s Lab Bench \(The Present Horizon\)(.*?)(?=## The Uncharted Horizon|\Z)", text, re.DOTALL)
    ledger_match = re.search(r"## The Uncharted Horizon \(Ledger of Intent\)(.*?)\Z", text, re.DOTALL)

    print("=" * 70)
    print("  UNIVERSAL LAB CHRONICLE TELEMETRY (LCP v1.0)")
    print("=" * 70)
    if bench_match:
        print(bench_match.group(0).strip())
    print("-" * 70)
    if ledger_match:
        print(ledger_match.group(0).strip())
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Chronicle Manager for Translation spoke.")
    parser.add_argument("--status", action="store_true", help="Display current Lab Bench and Ledger status.")
    parser.add_argument("--validate", action="store_true", help="Validate CHRONICLE.md structural integrity and slop.")
    parser.add_argument("--sync", action="store_true", help="Synchronize Lab Bench with active git commit.")
    parser.add_argument("--sync-test-count", type=str, help="Update Working State test count (e.g. '12 / 12 Hermetic Unit Tests Green').")

    args = parser.parse_args()

    if args.status:
        display_status()
        return

    if args.validate:
        valid, violations = ChronicleManager.validate_chronicle_integrity()
        if valid:
            print("[PASS] CHRONICLE.md passed structural integrity and slop audits.")
            sys.exit(0)
        else:
            print(f"[FAIL] CHRONICLE.md has {len(violations)} violations:")
            for v in violations:
                print(f"  - {v}")
            sys.exit(1)

    if args.sync:
        commit = ChronicleManager.get_git_commit()
        success = ChronicleManager.sync_bench(commit_hash=commit)
        if success:
            print(f"[SUCCESS] Lab Bench synced to commit `{commit}`.")
        else:
            print("[FAIL] Could not sync Lab Bench.", file=sys.stderr)
            sys.exit(1)

    if args.sync_test_count:
        curr_text = ChronicleManager.get_chronicle_text()
        m = re.search(r"\*\*Working State:[*]{2}\s*(.*?)(?=\s*·\s*\d+\s*/\s*\d+\s*Hermetic|\n)", curr_text)
        prefix = m.group(1) if m else "Monuments 0, 1, 2 Sealed · Mikita Typikon Cohorts 1–11 Sealed"
        new_state = f"{prefix.strip()} · {args.sync_test_count}"
        success = ChronicleManager.sync_bench(working_state=new_state)
        if success:
            print(f"[SUCCESS] Working state updated to: {new_state}")
        else:
            print("[FAIL] Could not update working state.", file=sys.stderr)
            sys.exit(1)

    if not any(vars(args).values()):
        parser.print_help()


if __name__ == "__main__":
    main()
