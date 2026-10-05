#!/usr/bin/env python3
"""
Autonomous Multi-Cohort State Machine & Loop Controller
========================================================
Deterministically drives the multi-cohort translation pipeline from leaf extraction
through subagent manifest generation, Small Pause gatekeeping, and Hub synchronization.

Enforces Section 14 of .agents/AGENTS.md:
  - Zero-human intermediate pauses between cohorts.
  - Generates subagent manifests for native invoke_subagent calls.
  - Halts exclusively on blocker failure or final monument Grand Pause.

Usage:
    py scripts/autonomous_orchestrator.py --status
    py scripts/autonomous_orchestrator.py --step
    py scripts/autonomous_orchestrator.py --prepare-cohort [--monument ID] [--cohort N]
    py scripts/autonomous_orchestrator.py --verify-cohort [--monument ID] [--cohort N]
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Typikons" / "codex_registry.json"
STATE_FILE = PROJECT_ROOT / "Typikons" / "ACTIVE_ORCHESTRATOR_STATE.json"
TRIAGE_INBOX = PROJECT_ROOT / "scratch" / "triage_inbox.jsonl"

# Internal script imports
from extract_cohort_leaves import extract_leaves
from generate_work_order import generate_work_order
from run_small_pause_gate import run_gate
from assemble_and_sync_hub import ingest_and_sync
from orchestrator_state import load_state, save_state, load_registry, display_status

def log_triage_incident(ticket_id: str, monument: str, component: str, description: str) -> None:
    entry = {
        "ticket_id": ticket_id,
        "timestamp": json.loads(json.dumps(Path(__file__).stat().st_mtime)),  # timestamp seed
        "reporter": "autonomous_orchestrator.py",
        "monument": monument,
        "component": component,
        "status": "OPEN",
        "description": description
    }
    TRIAGE_INBOX.parent.mkdir(parents=True, exist_ok=True)
    with open(TRIAGE_INBOX, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def get_current_context() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    state = load_state()
    registry = load_registry()
    mon_id = state.get("monument_id", "1899_dolnytsky_typikon")
    mon_info = registry.get("monuments", {}).get(mon_id)
    if not mon_info:
        raise ValueError(f"Monument '{mon_id}' not found in codex_registry.json")
    return state, mon_info

def prepare_cohort(monument_id: Optional[str] = None, cohort_num: Optional[int] = None) -> Dict[str, Any]:
    """
    Step A: Extract leaves at 300 DPI, generate work order, and return invoke_subagent manifest.
    """
    state, mon_info = get_current_context()
    if monument_id:
        mon_info = load_registry()["monuments"][monument_id]
    else:
        monument_id = state.get("monument_id", "1899_dolnytsky_typikon")

    if cohort_num is None:
        cohort_num = state.get("current_cohort", 1)

    total_pages = mon_info.get("total_physical_pages", 591)
    cohort_size = mon_info.get("default_cohort_size", 20)

    start_page = ((cohort_num - 1) * cohort_size) + 1
    end_page = min(total_pages, cohort_num * cohort_size)

    print(f"\n[Autonomous Loop] Preparing Cohort #{cohort_num} for '{mon_info.get('title')}' (Leaves {start_page}..{end_page})...")

    # 1. Extract leaves
    print("  -> Extracting 300 DPI PNG leaf facsimiles...")
    extract_leaves(
        monument_id=monument_id,
        cohort_num=cohort_num,
        start_page=start_page,
        end_page=end_page,
        dpi=300
    )

    # 2. Generate Work Order
    print("  -> Generating formal Work Order and subagent manifest...")
    work_order_path = generate_work_order(
        monument_id=monument_id,
        cohort_num=cohort_num,
        start_page=start_page,
        end_page=end_page,
        print_prompt=False
    )

    # 3. Update telemetry state
    state["current_cohort"] = cohort_num
    state["current_cohort_range"] = f"pp. {start_page}-{end_page} (leaves p{start_page}-p{end_page})"
    state["small_pause_gate_status"] = "AWAITING_SUBAGENT_EXECUTION"
    save_state(state)

    rel_ws = mon_info.get("workspace_dir", monument_id).replace("\\", "/")
    manifest = {
        "action": "INVOKE_SUBAGENT",
        "subagent_type": "self",
        "role": f"Liturgical Translator ({mon_info.get('short_title')} Cohort {cohort_num})",
        "target_pages": f"{start_page}..{end_page}",
        "work_order_path": str(work_order_path.relative_to(PROJECT_ROOT)),
        "images_dir": f"{rel_ws}/Source Text/images/",
        "prompt": (
            f"You are the Context-Sequestered Liturgical Scribe and Translator for {mon_info.get('title')} — Cohort {cohort_num}.\n\n"
            f"Execute the work order at: {work_order_path.relative_to(PROJECT_ROOT)}\n"
            f"Transcribe and translate physical leaves p{start_page} through p{end_page} directly from 300 DPI images in '{rel_ws}/Source Text/images/'.\n"
            f"Write all three output files to disk (Source, Draft MD, Footnotes) with UTF-8 encoding.\n"
            f"When finished, send a completion notification to the parent orchestrator."
        )
    }

    print("  -> Cohort preparation complete. Subagent manifest generated.\n")
    return manifest

def verify_cohort_and_advance(monument_id: Optional[str] = None, cohort_num: Optional[int] = None) -> Dict[str, Any]:
    """
    Step B: Execute Small Pause Gatekeeper Suite, assemble complete edition, and advance state.
    """
    state, mon_info = get_current_context()
    if monument_id:
        mon_info = load_registry()["monuments"][monument_id]
    else:
        monument_id = state.get("monument_id", "1899_dolnytsky_typikon")

    if cohort_num is None:
        cohort_num = state.get("current_cohort", 1)

    print(f"\n[Autonomous Loop] Executing Small Pause Gatekeeper Suite for Cohort #{cohort_num}...")
    gate_res = run_gate(monument_id=monument_id, cohort_num=cohort_num)

    if gate_res != 0:
        print("  -> SMALL PAUSE GATE FAILED! Halting autonomous advancement.")
        state["small_pause_gate_status"] = "SMALL_PAUSE_GATE_FAILED"
        if f"Gate failed for Cohort {cohort_num}" not in state.get("active_blockers", []):
            state.setdefault("active_blockers", []).append(f"Gate failed for Cohort {cohort_num}")
        save_state(state)
        log_triage_incident(
            ticket_id=f"TICK-COHORT{cohort_num}-FAIL",
            monument=mon_info.get("title", monument_id),
            component="small_pause_gate",
            description=f"Cohort #{cohort_num} failed Small Pause verification."
        )
        return {"status": "BLOCKED", "cohort": cohort_num}

    print("  -> Small Pause Gate PASSED 100%! Promoting deliverables & updating master edition...")
    ingest_and_sync(monument_id=monument_id, cohort_num=cohort_num)

    # Update completed cohorts
    completed = state.get("completed_cohorts", [])
    if cohort_num not in completed:
        completed.append(cohort_num)
        completed.sort()
    state["completed_cohorts"] = completed

    # Calculate page progress
    cohort_size = mon_info.get("default_cohort_size", 20)
    total_pages = mon_info.get("total_physical_pages", 591)
    
    # Calculate pages done based on completed cohorts
    translated_count = 0
    for c in completed:
        sp = ((c - 1) * cohort_size) + 1
        ep = min(total_pages, c * cohort_size)
        translated_count += (ep - sp + 1)

    state["translated_pages"] = translated_count
    remaining = max(0, total_pages - translated_count)
    state["remaining_pages"] = remaining

    if remaining == 0:
        print("\n" + "=" * 65)
        print("  ALL PHYSICAL LEAVES TRANSLATED ACROSS MONUMENT!")
        print("  REACHED SOVEREIGN GRAND PAUSE — READY FOR HUMAN INSPECTION.")
        print("=" * 65 + "\n")
        state["small_pause_gate_status"] = "GRAND_PAUSE_READY_FOR_HUMAN_INSPECTION"
        save_state(state)
        return {"status": "GRAND_PAUSE", "monument_complete": True}

    # Advance to next cohort
    next_cohort = cohort_num + 1
    state["current_cohort"] = next_cohort
    state["small_pause_gate_status"] = "READY_FOR_NEXT_COHORT"
    save_state(state)

    print(f"\n[Autonomous Loop] Advancing to Cohort #{next_cohort} ({remaining} physical leaves remaining)...")
    next_manifest = prepare_cohort(monument_id=monument_id, cohort_num=next_cohort)
    return {
        "status": "ADVANCED",
        "next_cohort": next_cohort,
        "manifest": next_manifest
    }

def main():
    parser = argparse.ArgumentParser(description="Autonomous Multi-Cohort State Machine & Loop Controller")
    parser.add_argument("--status", action="store_true", help="Display current telemetry dashboard")
    parser.add_argument("--prepare-cohort", action="store_true", help="Extract leaves and generate subagent manifest")
    parser.add_argument("--verify-cohort", action="store_true", help="Run Small Pause Gate and advance cohort")
    parser.add_argument("--step", action="store_true", help="Execute the next autonomous loop step")
    parser.add_argument("--monument", help="Override monument ID")
    parser.add_argument("--cohort", type=int, help="Override cohort number")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if args.status:
        state = load_state()
        display_status(state)
        return

    if args.prepare_cohort:
        manifest = prepare_cohort(monument_id=args.monument, cohort_num=args.cohort)
        if args.json:
            print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return

    if args.verify_cohort:
        res = verify_cohort_and_advance(monument_id=args.monument, cohort_num=args.cohort)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.step:
        state = load_state()
        status = state.get("small_pause_gate_status", "UNKNOWN")
        curr_cohort = state.get("current_cohort", 1)

        if status in ["READY_FOR_STARTUP_PROMPT", "READY_FOR_NEXT_COHORT", "UNKNOWN"]:
            manifest = prepare_cohort(monument_id=args.monument, cohort_num=curr_cohort)
            if args.json:
                print(json.dumps(manifest, indent=2, ensure_ascii=False))
        elif status == "AWAITING_SUBAGENT_EXECUTION":
            print(f"Status is AWAITING_SUBAGENT_EXECUTION for Cohort #{curr_cohort}.")
            print("Dispatch subagent using manifest or run '--verify-cohort' once subagent completes.")
        elif status == "SMALL_PAUSE_GATE_FAILED":
            print(f"Status is SMALL_PAUSE_GATE_FAILED. Fix blockers listed in ACTIVE_ORCHESTRATOR_STATE.json.")
        elif status == "GRAND_PAUSE_READY_FOR_HUMAN_INSPECTION":
            print("Monument translation complete! Awaiting Grand Pause human sign-off.")
        return

    # Default: show status
    state = load_state()
    display_status(state)

if __name__ == "__main__":
    main()
