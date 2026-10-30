#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sovereign Translation Orchestrator State Controller
===================================================
Manages per-monument isolated telemetry (<workspace_dir>/orchestrator_state.json),
multi-monument active lease disambiguation, pause/resume transitions, and
atomic state mirroring to Liturgical Monuments/ACTIVE_ORCHESTRATOR_STATE.json.

Enforces the 3-Phase Bookend Hybrid Model Routing Architecture:
  - Phase 0 (PHASE_0_ARGON_PLANNING): Locked for Argon Pre-Flight, /plan, and /grill-me.
  - Phase 1 (PHASE_1_FLASH_SPRINT): Unattended 100% Flash cohort sprint + argon_review_queue.json.
  - Phase 2 (PHASE_2_AWAITING_ARGON_AUDIT): Argon post-sprint queue audit & LCPE compilation.

Usage:
    python scripts/orchestrator_state.py --status [--monument <id>]
    python scripts/orchestrator_state.py --set-status <STATUS> --monument <id>
    python scripts/orchestrator_state.py --advance-cohort --monument <id>
    python scripts/orchestrator_state.py --set-monument <monument_id>
    python scripts/orchestrator_state.py --pause-monument --monument <id>
    python scripts/orchestrator_state.py --resume-monument --monument <id>
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from concurrency_lock import atomic_write_json, atomic_update_registry

STATE_FILE = PROJECT_ROOT / "Liturgical Monuments" / "ACTIVE_ORCHESTRATOR_STATE.json"
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
SCAFFOLDS_FILE = PROJECT_ROOT / "data" / "templates" / "publication_spec_scaffolds.json"

VALID_MONUMENT_TYPES = (
    "typikon",
    "octoechos",
    "lenten_triodion",
    "pentecostarion",
    "anthologion",
    "akathistnik",
    "irmologion",
    "horologion",
    "psalter",
    "euchologion_liturgikon",
    "trebnyk_euchologion",
    "juridical_synodal",
    "lexicon_scholarly",
)

INACTIVE_GATE_STATUSES = {
    "MONUMENT_SEALED_AND_HANDED_OFF",
    "MONUMENT_DEFERRED_GATE_0",
    "MONUMENT_PAUSED",
}
INACTIVE_MONUMENT_STATUSES = {
    "completed",
    "sealed",
    "failed",
    "paused",
}


def resolve_monument_type(monument_id: str, mon_info: Optional[Dict[str, Any]] = None) -> str:
    """
    Deterministically resolves a monument's specific liturgical type across all 13
    classes in publication_spec_scaffolds.json.
    """
    info = mon_info or {}
    explicit = str(info.get("monument_type", "")).strip().lower()
    if explicit in VALID_MONUMENT_TYPES:
        return explicit

    mid = (monument_id or "").strip().lower()
    title = str(info.get("title", "")).lower()
    genre = str(info.get("genre_register", "")).lower()
    combined = f"{mid} {title}"

    if any(k in mid for k in ("lexicon", "paterikon", "limonar", "dmitrievsky", "conybeare", "sheptytsky", "skaballanovich")):
        return "lexicon_scholarly"
    if any(k in mid for k in ("octoechos", "osmohlasnyk")):
        return "octoechos"
    if any(k in mid for k in ("pentecostarion", "flowery_triodion", "paschal_office")):
        return "pentecostarion"
    if "triodion" in mid:
        return "lenten_triodion"
    if any(k in mid for k in ("anthologion", "menaion", "minea", "festal_offices", "fathers_services", "bohorodychnyk", "izbornyk", "nativity_theophany")):
        return "anthologion"
    if any(k in mid for k in ("akafist", "akathist", "theotokos_canon")):
        return "akathistnik"
    if any(k in combined for k in ("irmologion", "heirmologion", "glasopisets")):
        return "irmologion"
    if any(k in mid for k in ("horologion", "chasoslov", "jamagirk")):
        return "horologion"
    if any(k in mid for k in ("psalter", "brashno_dukhovnoe")):
        return "psalter"
    if any(k in mid for k in ("liturgikon", "archieratikon", "sluzhebnyk")):
        return "euchologion_liturgikon"
    if any(k in mid for k in ("trebnyk", "molytvoslov", "communion_rule", "euchologion")):
        return "trebnyk_euchologion"
    if any(k in mid for k in ("synod", "palinodia", "knyzhytsia", "basilian_", "zamoysky")) and "sabbas" not in mid:
        return "juridical_synodal"
    if any(k in combined for k in ("typikon", "ustav", "poluustav", "oko_", "sabbas", "violakis", "ordo_celebrationis")):
        return "typikon"
    if genre == "juridical":
        return "juridical_synodal"
    if genre == "scholarly_critical":
        return "lexicon_scholarly"
    return "typikon"


def load_monument_scaffold(monument_id: str, mon_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Loads the monument-type scaffold and gate_policy from data/templates/publication_spec_scaffolds.json.
    """
    mon_type = resolve_monument_type(monument_id, mon_info)
    if not SCAFFOLDS_FILE.exists():
        return {"monument_type": mon_type, "gate_policy": {}, "prompt_guardrails": [], "allowed_h1_patterns": [], "parts": []}
    try:
        data = json.loads(SCAFFOLDS_FILE.read_text(encoding="utf-8"))
        by_type = data.get("scaffolds_by_monument_type", {})
        if mon_type in by_type:
            res = dict(by_type[mon_type])
            res["monument_type"] = mon_type
            return res
        fallback = dict(data.get("default", {}))
        fallback["monument_type"] = mon_type
        return fallback
    except (OSError, json.JSONDecodeError):
        return {"monument_type": mon_type, "gate_policy": {}, "prompt_guardrails": [], "allowed_h1_patterns": [], "parts": []}


def load_registry() -> Dict[str, Any]:
    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Codex registry not found at: {REGISTRY_FILE}")
    with open(REGISTRY_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def _resolve_workspace_dir(mon_id: str, mon_info: Dict[str, Any]) -> Path:
    ws_rel = mon_info.get("workspace_dir", f"Liturgical Monuments/{mon_id}")
    ws_path = Path(ws_rel)
    return ws_path if ws_path.is_absolute() else (PROJECT_ROOT / ws_path)


def get_active_leased_monuments() -> List[str]:
    """
    Returns all monument IDs that currently hold an active, unsealed, unpaused
    execution lease in their isolated <workspace_dir>/orchestrator_state.json.
    """
    try:
        registry = load_registry()
    except FileNotFoundError:
        return []
    monuments = registry.get("monuments", {})
    active_leased: List[str] = []

    for mid, minfo in monuments.items():
        if minfo.get("status", "") in INACTIVE_MONUMENT_STATUSES:
            continue
        ws_dir = _resolve_workspace_dir(mid, minfo)
        state_file = ws_dir / "orchestrator_state.json"
        if not state_file.exists():
            continue
        try:
            with open(state_file, "r", encoding="utf-8") as sf:
                st = json.load(sf)
            gate_st = st.get("small_pause_gate_status", "")
            st_status = st.get("status", "")
            has_lease = st.get("active_lease", True)
            if (
                gate_st not in INACTIVE_GATE_STATUSES
                and st_status not in INACTIVE_MONUMENT_STATUSES
                and has_lease is not False
            ):
                active_leased.append(mid)
        except (json.JSONDecodeError, OSError, KeyError):
            pass

    return active_leased


def get_concurrent_active_monuments_map() -> Dict[str, Dict[str, Any]]:
    """
    Builds a live summary map of all monuments currently holding an active lease.
    """
    try:
        registry = load_registry()
    except FileNotFoundError:
        return {}
    monuments = registry.get("monuments", {})
    active_ids = get_active_leased_monuments()
    summary_map: Dict[str, Dict[str, Any]] = {}

    for mid in active_ids:
        minfo = monuments.get(mid, {})
        ws_dir = _resolve_workspace_dir(mid, minfo)
        state_file = ws_dir / "orchestrator_state.json"
        if not state_file.exists():
            continue
        try:
            st = json.loads(state_file.read_text(encoding="utf-8"))
            summary_map[mid] = {
                "monument_id": mid,
                "active_monument": st.get("active_monument", minfo.get("title", mid)),
                "routing_phase": st.get("routing_phase", "PHASE_1_FLASH_SPRINT"),
                "current_cohort": st.get("current_cohort", 1),
                "current_cohort_range": st.get("current_cohort_range", ""),
                "translated_pages": st.get("translated_pages", 0),
                "total_physical_pages": st.get("total_physical_pages", minfo.get("total_physical_pages", 0)),
                "remaining_pages": st.get("remaining_pages", 0),
                "small_pause_gate_status": st.get("small_pause_gate_status", "UNKNOWN"),
                "argon_review_queue_count": st.get("argon_review_queue_count", 0),
                "unresolved_quarantines": st.get("unresolved_quarantines", 0),
                "active_lease": st.get("active_lease", True),
            }
        except (json.JSONDecodeError, OSError):
            pass

    return summary_map


def select_next_unclaimed_monument(exclude_ids: Optional[List[str]] = None) -> Optional[str]:
    """
    Resolves the next monument in codex_registry.json that is not completed,
    sealed, failed, paused, or currently leased by an active parallel chat.
    """
    registry = load_registry()
    monuments = registry.get("monuments", {})
    excluded = set(exclude_ids or []) | set(get_active_leased_monuments())

    for mid, minfo in monuments.items():
        if mid in excluded:
            continue
        cand_status = minfo.get("status", "")
        if cand_status in ("completed", "sealed", "failed", "in_progress", "paused"):
            continue
        ws_dir = _resolve_workspace_dir(mid, minfo)
        state_file = ws_dir / "orchestrator_state.json"
        if state_file.exists():
            try:
                st = json.loads(state_file.read_text(encoding="utf-8"))
                if (
                    st.get("small_pause_gate_status") in ("MONUMENT_SEALED_AND_HANDED_OFF", "MONUMENT_DEFERRED_GATE_0", "MONUMENT_PAUSED")
                    or st.get("status") in ("completed", "sealed", "failed", "paused")
                ):
                    continue
                if st.get("active_lease") is True:
                    continue
            except (json.JSONDecodeError, OSError):
                pass
        return mid

    return None


def resolve_monument_id(monument_id: Optional[str] = None, allow_fallback: bool = False) -> str:
    """
    Resolves the target monument ID enforcing strict multi-monument disambiguation:
      1. Explicit monument_id argument (highest priority).
      2. Environment variable ACTIVE_MONUMENT_ID.
      3. If >=2 monuments hold active leases and allow_fallback is False, raises RuntimeError.
      4. If exactly 1 monument holds an active lease, auto-resolves to it.
      5. Fallback to ACTIVE_ORCHESTRATOR_STATE.json if present.
    """
    if monument_id and monument_id.strip():
        return monument_id.strip()

    env_id = os.environ.get("ACTIVE_MONUMENT_ID")
    if env_id and env_id.strip():
        return env_id.strip()

    active_leased = get_active_leased_monuments()
    if len(active_leased) == 1:
        return active_leased[0]
    elif len(active_leased) >= 2 and not allow_fallback:
        active_list = ", ".join(active_leased)
        raise RuntimeError(
            f"[DISAMBIGUATION REQUIRED] Multiple monuments are currently active in parallel: [{active_list}]. "
            f"You must specify --monument <id> explicitly (or set ACTIVE_MONUMENT_ID)."
        )

    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                st = json.load(f)
            mid = st.get("monument_id")
            registry = load_registry()
            if mid and mid in registry.get("monuments", {}):
                return mid
        except (json.JSONDecodeError, OSError, KeyError):
            pass

    return "1629_kyiv_octoechos"


def get_state_file_path(monument_id: Optional[str] = None) -> Path:
    """Returns the isolated path to <workspace_dir>/orchestrator_state.json for the resolved monument."""
    mon_id = resolve_monument_id(monument_id)
    registry = load_registry()
    mon_info = registry.get("monuments", {}).get(mon_id, {})
    ws_dir = _resolve_workspace_dir(mon_id, mon_info)
    return ws_dir / "orchestrator_state.json"


def load_state(monument_id: Optional[str] = None) -> Dict[str, Any]:
    """Loads state from the monument's isolated orchestrator_state.json with automatic fallback/seeding."""
    mon_id = resolve_monument_id(monument_id)
    state_path = get_state_file_path(mon_id)

    if state_path.exists():
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
            state["monument_id"] = mon_id
            return state

    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                st = json.load(f)
            if st.get("monument_id") == mon_id:
                save_state(st, mon_id)
                return st
        except (json.JSONDecodeError, OSError, KeyError):
            pass

    registry = load_registry()
    mon_info = registry.get("monuments", {}).get(mon_id, {})
    total = int(mon_info.get("total_physical_pages", 0))
    cohort_sz = int(mon_info.get("default_cohort_size", 10))
    first_end = min(total, cohort_sz)
    reg_status = mon_info.get("status", "")
    is_completed = reg_status in ("completed", "sealed")
    is_paused = reg_status == "paused"
    num_cohorts = (total // cohort_sz) + (1 if total % cohort_sz else 0) if total > 0 else 0

    default_state: Dict[str, Any] = {
        "active_monument": mon_info.get("title", mon_id),
        "monument_id": mon_id,
        "status": reg_status or "ready",
        "active_lease": (reg_status == "in_progress"),
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
        "small_pause_gate_status": (
            "MONUMENT_SEALED_AND_HANDED_OFF"
            if is_completed
            else ("MONUMENT_PAUSED" if is_paused else "PHASE_0_ARGON_PLANNING_LOCKED")
        ),
        "active_blockers": [],
    }
    save_state(default_state, mon_id)
    return default_state


def save_state(state: Dict[str, Any], monument_id: Optional[str] = None) -> None:
    """
    Saves state atomically to isolated <workspace_dir>/orchestrator_state.json and
    mirrors to ACTIVE_ORCHESTRATOR_STATE.json (enriched with concurrent_active_monuments).
    """
    mon_id = monument_id or state.get("monument_id")
    mon_id = resolve_monument_id(mon_id)
    state["monument_id"] = mon_id
    state["updated_at"] = datetime.now(timezone.utc).isoformat()

    gate_st = state.get("small_pause_gate_status", "")
    if gate_st in INACTIVE_GATE_STATUSES or state.get("status") in INACTIVE_MONUMENT_STATUSES:
        state["active_lease"] = False
    elif "active_lease" not in state:
        state["active_lease"] = True

    state_path = get_state_file_path(mon_id)
    state_copy = {k: v for k, v in state.items() if k != "concurrent_active_monuments"}
    atomic_write_json(state_path, state_copy, lock_name=f"state_{mon_id}")

    concurrent_map = get_concurrent_active_monuments_map()
    if not state_copy.get("active_lease", False) and concurrent_map:
        primary_id = next(iter(concurrent_map.keys()))
        if STATE_FILE.exists():
            try:
                existing_mirror = json.loads(STATE_FILE.read_text(encoding="utf-8"))
                if existing_mirror.get("monument_id") in concurrent_map:
                    primary_id = existing_mirror["monument_id"]
            except (json.JSONDecodeError, OSError):
                pass
        primary_path = get_state_file_path(primary_id)
        try:
            mirror_payload = json.loads(primary_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            mirror_payload = dict(state_copy)
    else:
        mirror_payload = dict(state_copy)
    mirror_payload["concurrent_active_monuments"] = concurrent_map
    atomic_write_json(STATE_FILE, mirror_payload, lock_name="orchestrator_state")


def pause_monument(monument_id: str) -> Dict[str, Any]:
    """
    Marks a monument as MONUMENT_PAUSED, releases its active_lease so it does not
    trigger multi-monument disambiguation blocks while shelved, and syncs completed
    cohorts from disk.
    """
    registry = load_registry()
    mon_info = registry.get("monuments", {}).get(monument_id)
    if not mon_info:
        raise ValueError(f"Unknown monument ID '{monument_id}'")

    state = load_state(monument_id=monument_id)
    total_pages = int(mon_info.get("total_physical_pages", state.get("total_physical_pages", 0)))
    cohort_size = int(mon_info.get("default_cohort_size", 10))
    ws = _resolve_workspace_dir(monument_id, mon_info)
    final_md_dir = ws / "Final MD"

    disk_completed: List[int] = []
    if final_md_dir.exists():
        for f in final_md_dir.glob(f"{monument_id}_cohort*.md"):
            m = re.search(r"cohort(\d+)", f.name)
            if m:
                disk_completed.append(int(m.group(1)))
    if disk_completed:
        merged_completed = sorted(set(state.get("completed_cohorts", [])) | set(disk_completed))
        state["completed_cohorts"] = merged_completed
        translated = 0
        for c in merged_completed:
            sp = ((c - 1) * cohort_size) + 1
            ep = min(total_pages, c * cohort_size)
            translated += (ep - sp + 1)
        state["translated_pages"] = translated
        state["remaining_pages"] = max(0, total_pages - translated)
        next_c = max(merged_completed) + 1
        next_sp = ((next_c - 1) * cohort_size) + 1
        next_ep = min(total_pages, next_c * cohort_size)
        state["current_cohort"] = next_c
        state["current_cohort_range"] = f"pp. {next_sp}-{next_ep} (leaves p{next_sp}-p{next_ep})"

    old_gate = state.get("small_pause_gate_status", "READY_FOR_NEXT_COHORT")
    if old_gate != "MONUMENT_PAUSED":
        state["pre_pause_gate_status"] = old_gate
    state["status"] = "paused"
    state["active_lease"] = False
    state["small_pause_gate_status"] = "MONUMENT_PAUSED"

    def _mark_paused(reg: Dict[str, Any]) -> None:
        if monument_id in reg.get("monuments", {}):
            reg["monuments"][monument_id]["status"] = "paused"
            reg["monuments"][monument_id]["active"] = False

    if REGISTRY_FILE.exists():
        atomic_update_registry(_mark_paused, registry_path=REGISTRY_FILE)

    save_state(state, monument_id=monument_id)

    print(f"Paused monument '{monument_id}' (active_lease=False, completed_cohorts={len(state.get('completed_cohorts', []))}).")
    return state


def resume_monument(monument_id: str) -> Dict[str, Any]:
    """
    Re-acquires active_lease=True on a paused monument and restores its gate status.
    """
    registry = load_registry()
    if monument_id not in registry.get("monuments", {}):
        raise ValueError(f"Unknown monument ID '{monument_id}'")

    state = load_state(monument_id=monument_id)
    restored_gate = state.pop("pre_pause_gate_status", None) or "READY_FOR_NEXT_COHORT"
    if restored_gate == "MONUMENT_PAUSED":
        restored_gate = "READY_FOR_NEXT_COHORT"
    state["status"] = "in_progress"
    state["active_lease"] = True
    state["small_pause_gate_status"] = restored_gate

    def _mark_in_progress(reg: Dict[str, Any]) -> None:
        if monument_id in reg.get("monuments", {}):
            reg["monuments"][monument_id]["status"] = "in_progress"
            reg["monuments"][monument_id]["active"] = True

    if REGISTRY_FILE.exists():
        atomic_update_registry(_mark_in_progress, registry_path=REGISTRY_FILE)

    save_state(state, monument_id=monument_id)

    print(f"Resumed monument '{monument_id}' (active_lease=True, gate={restored_gate}).")
    return state


def display_parallel_status() -> None:
    """
    Displays a side-by-side telemetry table of all concurrently leased monuments.
    """
    concurrent_map = get_concurrent_active_monuments_map()
    print("=" * 88)
    print(f"  PARALLEL SEQUESTERED MONUMENTS TELEMETRY DASHBOARD ({len(concurrent_map)} Active Leases)")
    print("=" * 88)
    if not concurrent_map:
        print("  No monuments currently hold an active execution lease.")
        print("=" * 88)
        return

    header = f"  {'Monument ID':<28} | {'Phase':<24} | {'Cohort':<8} | {'Progress':<15} | {'Gate Status'}"
    print(header)
    print("  " + "-" * 84)
    for mid, info in concurrent_map.items():
        phase = str(info.get("routing_phase", ""))[:24]
        cohort = f"#{info.get('current_cohort', 1)}"
        done = info.get("translated_pages", 0)
        total = info.get("total_physical_pages", 0)
        pct = (done / total * 100.0) if total > 0 else 0.0
        prog = f"{done}/{total} ({pct:.0f}%)"
        gate = info.get("small_pause_gate_status", "")
        print(f"  {mid:<28} | {phase:<24} | {cohort:<8} | {prog:<15} | {gate}")
    print("=" * 88)


def display_status(state: Dict[str, Any]) -> None:
    concurrent_map = state.get("concurrent_active_monuments") or get_concurrent_active_monuments_map()
    if len(concurrent_map) >= 2:
        display_parallel_status()

    print("=" * 65)
    print("  SOVEREIGN TRANSLATION ORCHESTRATOR TELEMETRY DASHBOARD")
    print("=" * 65)
    print(f"  Active Monument       : {state.get('active_monument')} [{state.get('monument_id', 'unknown')}]")
    print(f"  Active Lease Held     : {state.get('active_lease', True)}")
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
    blockers = state.get("active_blockers", [])
    if blockers:
        print(f"  Active Blockers       : {len(blockers)} BLOCKERS ACTIVE:")
        for b in blockers:
            print(f"    - {b}")
    else:
        print("  Active Blockers       : None (All Clear)")

    total = state.get("total_physical_pages", 0)
    done = state.get("translated_pages", 0)
    pct = (done / total * 100) if total > 0 else 0
    bar_width = 30
    filled = int(bar_width * done / total) if total > 0 else 0
    bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"
    print(f"  Codex Progress        : {bar} {pct:.1f}% ({done}/{total} leaves)")
    print("=" * 65)


def set_status(new_status: str, monument_id: Optional[str] = None) -> None:
    mon_id = resolve_monument_id(monument_id)
    state = load_state(monument_id=mon_id)
    old_status = state.get("small_pause_gate_status")
    state["small_pause_gate_status"] = new_status
    save_state(state, monument_id=mon_id)
    print(f"Updated gate status ({mon_id}): {old_status} -> {new_status}")


def add_blocker(blocker_text: str, monument_id: Optional[str] = None) -> None:
    mon_id = resolve_monument_id(monument_id)
    state = load_state(monument_id=mon_id)
    blockers = state.setdefault("active_blockers", [])
    if blocker_text not in blockers:
        blockers.append(blocker_text)
    save_state(state, monument_id=mon_id)
    print(f"Added blocker ({mon_id}): {blocker_text}")


def clear_blockers(monument_id: Optional[str] = None) -> None:
    mon_id = resolve_monument_id(monument_id)
    state = load_state(monument_id=mon_id)
    state["active_blockers"] = []
    save_state(state, monument_id=mon_id)
    print(f"Cleared all active blockers ({mon_id}).")


def advance_cohort(monument_id: Optional[str] = None) -> None:
    mon_id = resolve_monument_id(monument_id)
    state = load_state(monument_id=mon_id)
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
        except (ValueError, IndexError):
            cohort_pages = 20

    state["translated_pages"] = state.get("translated_pages", 0) + cohort_pages
    total = state.get("total_physical_pages", 278)
    state["remaining_pages"] = max(0, total - state["translated_pages"])

    next_cohort = current_cohort + 1
    state["current_cohort"] = next_cohort

    next_start = (end_p + 1) if end_p is not None else (((next_cohort - 1) * 10) + 1)
    registry = load_registry()
    mon_info = registry.get("monuments", {}).get(mon_id, {})
    cohort_size = mon_info.get("default_cohort_size", 20)

    next_end = min(total, next_start + cohort_size - 1)
    state["current_cohort_range"] = f"pp. {next_start}-{next_end} (leaves p{next_start}-p{next_end})"
    state["small_pause_gate_status"] = "READY_FOR_NEXT_COHORT"

    save_state(state, monument_id=mon_id)
    print(f"Advanced {mon_id} to Cohort #{next_cohort}: {state['current_cohort_range']}")
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

    new_state: Dict[str, Any] = {
        "active_monument": mon.get("title", monument_id),
        "monument_id": monument_id,
        "status": "in_progress",
        "active_lease": True,
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
        "active_blockers": [],
    }
    save_state(new_state, monument_id=monument_id)
    print(f"Switched active monument to: {mon.get('title')} (Phase 0 Argon Planning Lock engaged)")
    display_status(new_state)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sovereign Orchestrator State Controller")
    parser.add_argument("--monument", help="Target Monument ID")
    parser.add_argument("--status", action="store_true", help="Display telemetry dashboard")
    parser.add_argument("--set-status", help="Update small_pause_gate_status")
    parser.add_argument("--advance-cohort", action="store_true", help="Advance current cohort to next")
    parser.add_argument("--set-monument", help="Switch active monument by ID")
    parser.add_argument("--pause-monument", action="store_true", help="Pause a monument and release its active lease")
    parser.add_argument("--resume-monument", action="store_true", help="Resume a paused monument and acquire its active lease")
    parser.add_argument("--add-blocker", help="Register an active blocker")
    parser.add_argument("--clear-blockers", action="store_true", help="Clear all blockers")

    args = parser.parse_args()

    if args.pause_monument:
        if not args.monument:
            raise ValueError("You must specify --monument <id> with --pause-monument.")
        pause_monument(args.monument)
        return
    if args.resume_monument:
        if not args.monument:
            raise ValueError("You must specify --monument <id> with --resume-monument.")
        resume_monument(args.monument)
        return

    if args.status or (len(sys.argv) == 1) or (len(sys.argv) == 3 and args.monument):
        if not args.monument and len(get_active_leased_monuments()) >= 2:
            display_parallel_status()
        else:
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
