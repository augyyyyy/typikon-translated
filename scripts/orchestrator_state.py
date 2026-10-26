#!/usr/bin/env python3
"""
Sovereign Translation Orchestrator State Controller
===================================================
Manages telemetry and atomic state transitions for Byzantine-Ruthenian
Typikon monuments in Liturgical Monuments/ACTIVE_ORCHESTRATOR_STATE.json.

Enforces the 3-Phase Bookend Hybrid Model Routing Architecture:
  - Phase 0 (PHASE_0_ARGON_PLANNING): Locked for Argon Pre-Flight, /plan, and /grill-me.
  - Phase 1 (PHASE_1_FLASH_SPRINT): Unattended 100% Flash cohort sprint + argon_review_queue.json.
  - Phase 2 (PHASE_2_AWAITING_ARGON_AUDIT): Argon post-sprint queue audit & LCPE compilation.

Usage:
    python scripts/orchestrator_state.py --status
    python scripts/orchestrator_state.py --set-status <STATUS>
    python scripts/orchestrator_state.py --advance-cohort
    python scripts/orchestrator_state.py --set-monument <monument_id>
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

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


def resolve_monument_id(monument_id: Optional[str] = None, allow_fallback: bool = True) -> str:
    """
    Resolves the target monument ID enforcing strict multi-monument disambiguation:
      1. Explicit monument_id argument (highest priority).
      2. Environment variable ACTIVE_MONUMENT_ID.
      3. If exactly 1 monument has an active unsealed workspace state, auto-resolves to it.
      4. If >=2 monuments have active unsealed states, hard-fails requiring --monument <id>.
      5. Fallback to ACTIVE_ORCHESTRATOR_STATE.json if allow_fallback=True.
    """
    if monument_id and monument_id.strip():
        return monument_id.strip()

    env_id = os.environ.get("ACTIVE_MONUMENT_ID")
    if env_id and env_id.strip():
        return env_id.strip()

    registry = load_registry()
    monuments = registry.get("monuments", {})

    active_unsealed: List[str] = []
    for mid, minfo in monuments.items():
        ws_dir = PROJECT_ROOT / minfo.get("workspace_dir", f"Liturgical Monuments/{mid}")
        state_file = ws_dir / "orchestrator_state.json"
        if state_file.exists():
            try:
                with open(state_file, "r", encoding="utf-8") as sf:
                    st = json.load(sf)
                gate_st = st.get("small_pause_gate_status", "")
                if gate_st != "MONUMENT_SEALED_AND_HANDED_OFF" and st.get("status") != "failed":
                    active_unsealed.append(mid)
            except (json.JSONDecodeError, OSError, KeyError):
                pass

    if len(active_unsealed) == 1:
        return active_unsealed[0]
    elif len(active_unsealed) >= 2:
        if not allow_fallback:
            active_list = ", ".join(active_unsealed)
            raise RuntimeError(
                f"[DISAMBIGUATION REQUIRED] Multiple monuments are currently active in parallel: [{active_list}]. "
                f"You must specify --monument <id> explicitly."
            )

    # Fallback to ACTIVE_ORCHESTRATOR_STATE.json if present
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                st = json.load(f)
            mid = st.get("monument_id")
            if mid and mid in monuments:
                return mid
        except (json.JSONDecodeError, OSError, KeyError):
            pass

    return "1629_kyiv_octoechos"


def get_state_file_path(monument_id: Optional[str] = None) -> Path:
    """Returns the isolated path to <workspace_dir>/orchestrator_state.json for the resolved monument."""
    mon_id = resolve_monument_id(monument_id)
    registry = load_registry()
    mon_info = registry.get("monuments", {}).get(mon_id, {})
    ws_rel = mon_info.get("workspace_dir", f"Liturgical Monuments/{mon_id}")
    return PROJECT_ROOT / ws_rel / "orchestrator_state.json"


def load_state(monument_id: Optional[str] = None) -> Dict[str, Any]:
    """Loads state from the monument's isolated orchestrator_state.json with automatic fallback/seeding."""
    mon_id = resolve_monument_id(monument_id)
    state_path = get_state_file_path(mon_id)

    if state_path.exists():
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
            state["monument_id"] = mon_id
            return state

    # Check if ACTIVE_ORCHESTRATOR_STATE matches this monument
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                st = json.load(f)
            if st.get("monument_id") == mon_id:
                save_state(st, mon_id)
                return st
        except (json.JSONDecodeError, OSError, KeyError):
            pass

    # Synthesize clean default state from registry
    registry = load_registry()
    mon_info = registry.get("monuments", {}).get(mon_id, {})
    total = mon_info.get("total_physical_pages", 0)
    cohort_sz = mon_info.get("default_cohort_size", 10)
    first_end = min(total, cohort_sz)
    is_completed = (mon_info.get("status") == "completed")
    num_cohorts = (total // cohort_sz) + (1 if total % cohort_sz else 0) if total > 0 else 0

    default_state = {
        "active_monument": mon_info.get("title", mon_id),
        "monument_id": mon_id,
        "total_physical_pages": total,
        "completed_cohorts": list(range(1, num_cohorts + 1)) if is_completed else [],
        "translated_pages": total if is_completed else 0,
        "remaining_pages": 0 if is_completed else total,
        "current_cohort": num_cohorts if is_completed else 1,
        "current_cohort_range": f"pp. 1-{first_end} (leaves p1-p{first_end})",
        "routing_phase": "PHASE_2_ARGON_DEEP_AUDIT" if is_completed else "PHASE_0_ARGON_PLANNING",
        "active_subagent_model": "inherit" if is_completed else "flash",
        "argon_review_queue_count": 0,
        "unresolved_quarantines": 0,
        "cohort_retry_counts": {},
        "small_pause_gate_status": "MONUMENT_SEALED_AND_HANDED_OFF" if is_completed else "PHASE_0_ARGON_PLANNING_LOCKED",
        "active_blockers": []
    }
    save_state(default_state, mon_id)
    return default_state


def save_state(state: Dict[str, Any], monument_id: Optional[str] = None) -> None:
    """Saves state to isolated <workspace_dir>/orchestrator_state.json and mirrors to ACTIVE_ORCHESTRATOR_STATE.json."""
    mon_id = monument_id or state.get("monument_id")
    mon_id = resolve_monument_id(mon_id)
    state["monument_id"] = mon_id

    state_path = get_state_file_path(mon_id)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Mirror to global pointer file
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
    print(f"  Routing Phase         : {state.get('routing_phase', 'PHASE_1_FLASH_SPRINT')}")
    print(f"  Subagent Model Lock   : {state.get('active_subagent_model', 'flash')}")
    print(f"  Argon Review Queue    : {state.get('argon_review_queue_count', 0)} queued ({state.get('unresolved_quarantines', 0)} quarantined)")
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


def set_status(new_status: str, monument_id: Optional[str] = None) -> None:
    state = load_state(monument_id=monument_id)
    old_status = state.get("small_pause_gate_status")
    state["small_pause_gate_status"] = new_status
    save_state(state, monument_id=monument_id)
    print(f"Updated gate status: {old_status} -> {new_status}")


def add_blocker(blocker_text: str, monument_id: Optional[str] = None) -> None:
    state = load_state(monument_id=monument_id)
    blockers = state.setdefault("active_blockers", [])
    if blocker_text not in blockers:
        blockers.append(blocker_text)
    save_state(state, monument_id=monument_id)
    print(f"Added blocker: {blocker_text}")


def clear_blockers(monument_id: Optional[str] = None) -> None:
    state = load_state(monument_id=monument_id)
    state["active_blockers"] = []
    save_state(state, monument_id=monument_id)
    print("Cleared all active blockers.")


def advance_cohort(monument_id: Optional[str] = None) -> None:
    state = load_state(monument_id=monument_id)
    current_cohort = state.get("current_cohort", 1)
    completed = state.setdefault("completed_cohorts", [])
    if current_cohort not in completed:
        completed.append(current_cohort)

    range_str = state.get("current_cohort_range", "")
    cohort_pages = 20
    end_p = None
    if "leaves p" in range_str:
        try:
            part = range_str.split("leaves p")[1].split(")")[0]
            start_p, end_p = [int(x) for x in part.split("-p")]
            cohort_pages = (end_p - start_p) + 1
        except (json.JSONDecodeError, OSError, KeyError):
            cohort_pages = 20

    state["translated_pages"] = state.get("translated_pages", 0) + cohort_pages
    total = state.get("total_physical_pages", 278)
    state["remaining_pages"] = max(0, total - state["translated_pages"])

    next_cohort = current_cohort + 1
    state["current_cohort"] = next_cohort

    next_start = (end_p + 1) if end_p is not None else (((next_cohort - 1) * 10) + 1)
    registry = load_registry()
    mon_id = state.get("monument_id", resolve_monument_id(monument_id))
    mon_info = registry.get("monuments", {}).get(mon_id, {})
    cohort_size = mon_info.get("default_cohort_size", 20)

    next_end = min(total, next_start + cohort_size - 1)
    state["current_cohort_range"] = f"pp. {next_start}-{next_end} (leaves p{next_start}-p{next_end})"
    state["small_pause_gate_status"] = "READY_FOR_NEXT_COHORT"

    save_state(state, monument_id=mon_id)
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
        "routing_phase": "PHASE_0_ARGON_PLANNING",
        "active_subagent_model": "flash",
        "argon_review_queue_count": 0,
        "unresolved_quarantines": 0,
        "cohort_retry_counts": {},
        "small_pause_gate_status": "PHASE_0_ARGON_PLANNING_LOCKED",
        "active_blockers": []
    }
    save_state(new_state, monument_id=monument_id)
    print(f"Switched active monument to: {mon.get('title')} (Phase 0 Argon Planning Lock engaged)")
    display_status(new_state)


def main():
    parser = argparse.ArgumentParser(description="Sovereign Orchestrator State Controller")
    parser.add_argument("--monument", help="Target Monument ID")
    parser.add_argument("--status", action="store_true", help="Display telemetry dashboard")
    parser.add_argument("--set-status", help="Update small_pause_gate_status")
    parser.add_argument("--advance-cohort", action="store_true", help="Advance current cohort to next")
    parser.add_argument("--set-monument", help="Switch active monument by ID")
    parser.add_argument("--add-blocker", help="Register an active blocker")
    parser.add_argument("--clear-blockers", action="store_true", help="Clear all blockers")

    args = parser.parse_args()

    if args.status or (len(sys.argv) == 1) or (len(sys.argv) == 3 and args.monument):
        display_status(load_state(monument_id=args.monument))
    elif args.set_status:
        set_status(args.set_status, monument_id=args.monument)
    elif args.advance_cohort:
        advance_cohort(monument_id=args.monument)
    elif args.set_monument:
        set_monument(args.set_monument)
    elif args.add_blocker:
        add_blocker(args.add_blocker, monument_id=args.monument)
    elif args.clear_blockers:
        clear_blockers(monument_id=args.monument)


if __name__ == "__main__":
    main()
