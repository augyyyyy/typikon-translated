#!/usr/bin/env python3
"""
Sovereign Translation Orchestrator State Controller
===================================================
Manages telemetry and atomic state transitions for Byzantine-Ruthenian
Typikon monuments in Liturgical Monuments/ACTIVE_ORCHESTRATOR_STATE.json.

Usage:
    python scripts/orchestrator_state.py --status
    python scripts/orchestrator_state.py --set-status <STATUS>
    python scripts/orchestrator_state.py --advance-cohort
    python scripts/orchestrator_state.py --set-monument <monument_id>
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
STATE_FILE = PROJECT_ROOT / "Liturgical Monuments" / "ACTIVE_ORCHESTRATOR_STATE.json"
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"

def load_registry() -> Dict[str, Any]:
    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Codex registry not found at: {REGISTRY_FILE}")
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_state() -> Dict[str, Any]:
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"State file not found at: {STATE_FILE}")
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state: Dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")

def display_status(state: Dict[str, Any]) -> None:
    print("=" * 65)
    print("  SOVEREIGN TRANSLATION ORCHESTRATOR TELEMETRY DASHBOARD")
    print("=" * 65)
    print(f"  Active Monument       : {state.get('active_monument')} [{state.get('monument_id', 'unknown')}]")
    print(f"  Total Physical Pages  : {state.get('total_physical_pages')}")
    print(f"  Completed Cohorts     : {state.get('completed_cohorts')}")
    print(f"  Pages Translated      : {state.get('translated_pages')} / {state.get('total_physical_pages')}")
    print(f"  Pages Remaining       : {state.get('remaining_pages')}")
    print(f"  Current Cohort        : #{state.get('current_cohort')}")
    print(f"  Current Cohort Range  : {state.get('current_cohort_range')}")
    print(f"  Gate Status           : {state.get('small_pause_gate_status')}")
    blockers = state.get('active_blockers', [])
    if blockers:
        print(f"  Active Blockers       : {len(blockers)} BLOCKERS ACTIVE:")
        for b in blockers:
            print(f"    - {b}")
    else:
        print("  Active Blockers       : None (All Clear)")
    
    total = state.get('total_physical_pages', 0)
    done = state.get('translated_pages', 0)
    pct = (done / total * 100) if total > 0 else 0
    bar_width = 30
    filled = int(bar_width * done / total) if total > 0 else 0
    bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"
    print(f"  Codex Progress        : {bar} {pct:.1f}% ({done}/{total} leaves)")
    print("=" * 65)

def set_status(new_status: str) -> None:
    state = load_state()
    old_status = state.get("small_pause_gate_status")
    state["small_pause_gate_status"] = new_status
    save_state(state)
    print(f"Updated gate status: {old_status} -> {new_status}")

def add_blocker(blocker_text: str) -> None:
    state = load_state()
    blockers = state.setdefault("active_blockers", [])
    if blocker_text not in blockers:
        blockers.append(blocker_text)
    save_state(state)
    print(f"Added blocker: {blocker_text}")

def clear_blockers() -> None:
    state = load_state()
    state["active_blockers"] = []
    save_state(state)
    print("Cleared all active blockers.")

def advance_cohort() -> None:
    state = load_state()
    current_cohort = state.get("current_cohort", 1)
    completed = state.setdefault("completed_cohorts", [])
    if current_cohort not in completed:
        completed.append(current_cohort)
    
    # Calculate pages in just completed cohort
    range_str = state.get("current_cohort_range", "")
    # e.g., "pp. 1-20 (leaves p1-p20)"
    cohort_pages = 20
    if "leaves p" in range_str:
        try:
            part = range_str.split("leaves p")[1].split(")")[0]
            start_p, end_p = [int(x) for x in part.split("-p")]
            cohort_pages = (end_p - start_p) + 1
        except Exception:
            cohort_pages = 20

    state["translated_pages"] = state.get("translated_pages", 0) + cohort_pages
    total = state.get("total_physical_pages", 278)
    state["remaining_pages"] = max(0, total - state["translated_pages"])
    
    next_cohort = current_cohort + 1
    state["current_cohort"] = next_cohort
    
    # Calculate next cohort range
    # Next cohort starts right after end_p
    next_start = end_p + 1 if "end_p" in locals() else 21
    registry = load_registry()
    mon_id = state.get("monument_id", "1891_lviv_synod")
    mon_info = registry.get("monuments", {}).get(mon_id, {})
    cohort_size = mon_info.get("default_cohort_size", 20)
    
    next_end = min(total, next_start + cohort_size - 1)
    state["current_cohort_range"] = f"pp. {next_start}-{next_end} (leaves p{next_start}-p{next_end})"
    state["small_pause_gate_status"] = "READY_FOR_STARTUP_PROMPT"
    
    save_state(state)
    print(f"Advanced to Cohort #{next_cohort}: {state['current_cohort_range']}")
    display_status(state)

def set_monument(monument_id: str) -> None:
    registry = load_registry()
    monuments = registry.get("monuments", {})
    if monument_id not in monuments:
        available = ", ".join(monuments.keys())
        raise ValueError(f"Unknown monument ID '{monument_id}'. Available: {available}")
    
    mon = monuments[monument_id]
    total = mon.get("total_physical_pages", 0)
    cohort_size = mon.get("default_cohort_size", 20)
    first_end = min(total, cohort_size)
    
    new_state = {
        "active_monument": mon.get("title", monument_id),
        "monument_id": monument_id,
        "total_physical_pages": total,
        "completed_cohorts": [],
        "translated_pages": 0,
        "remaining_pages": total,
        "current_cohort": 1,
        "current_cohort_range": f"pp. 1-{first_end} (leaves p1-p{first_end})",
        "small_pause_gate_status": "READY_FOR_STARTUP_PROMPT",
        "active_blockers": []
    }
    save_state(new_state)
    print(f"Switched active monument to: {mon.get('title')}")
    display_status(new_state)

def main():
    parser = argparse.ArgumentParser(description="Sovereign Orchestrator State Controller")
    parser.add_argument("--status", action="store_true", help="Display telemetry dashboard")
    parser.add_argument("--set-status", help="Update small_pause_gate_status")
    parser.add_argument("--advance-cohort", action="store_true", help="Advance current cohort to next")
    parser.add_argument("--set-monument", help="Switch active monument by ID")
    parser.add_argument("--add-blocker", help="Register an active blocker")
    parser.add_argument("--clear-blockers", action="store_true", help="Clear all blockers")
    
    args = parser.parse_args()
    
    if args.status or len(sys.argv) == 1:
        display_status(load_state())
    elif args.set_status:
        set_status(args.set_status)
    elif args.advance_cohort:
        advance_cohort()
    elif args.set_monument:
        set_monument(args.set_monument)
    elif args.add_blocker:
        add_blocker(args.add_blocker)
    elif args.clear_blockers:
        clear_blockers()

if __name__ == "__main__":
    main()
