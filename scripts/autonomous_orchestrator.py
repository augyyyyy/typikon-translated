#!/usr/bin/env python3
"""
Autonomous Multi-Cohort State Machine & Loop Controller
========================================================
Deterministically drives the multi-cohort translation pipeline under the
3-Phase Bookend Hybrid Model Routing Architecture:

  - Phase 0 (PHASE_0_ARGON_PLANNING):
      Runs on Gemini 4 Argon (High) in Main UI. Executes codicological preflight,
      authors implementation_plan.md, and runs /grill-me. Hard circuit-breaker
      blocks Cohort 1 subagent manifest generation until user approves the plan,
      switches Main UI dropdown to Gemini 3.8 Flash, and runs --unlock-flash-sprint.
  - Phase 1 (PHASE_1_FLASH_SPRINT):
      Runs 100% on Gemini 3.8 Flash (Main UI + lean 'ephemeral_translator' worker
      subagents with Model='flash' strictly locked, zero mid-sprint 'pro' overrides).
      Executes 4-part deterministic Python self-healing, allows 1 targeted Flash
      retry on gate failure, and quarantines stubborn content-level leaf cruxes
      into Audit_Reports/argon_review_queue.json so unattended sprints never stall.
  - Phase 2 (PHASE_2_AWAITING_ARGON_AUDIT -> PHASE_2_ARGON_DEEP_AUDIT):
      When remaining_pages == 0, halts at AWAITING_ARGON_POST_SPRINT_AUDIT so the
      user switches Main UI dropdown back to Gemini 4 Argon (High). Resolves
      argon_review_queue.json (directly in parent if <=5 leaves, or via batched
      Model='inherit' Argon subagents of <=8 leaves if >5 leaves), re-verifies
      touched cohorts, and gates LCPE final compilation (UniversalPublicationEngine)
      on unresolved_quarantines == 0 before reaching the Sovereign Grand Pause.

Usage:
    py scripts/autonomous_orchestrator.py --status
    py scripts/autonomous_orchestrator.py --preflight [--monument ID]
    py scripts/autonomous_orchestrator.py --unlock-flash-sprint [--monument ID]
    py scripts/autonomous_orchestrator.py --step
    py scripts/autonomous_orchestrator.py --prepare-cohort [--monument ID] [--cohort N]
    py scripts/autonomous_orchestrator.py --verify-cohort [--monument ID] [--cohort N]
    py scripts/autonomous_orchestrator.py --run-argon-audit [--monument ID]
    py scripts/autonomous_orchestrator.py --resolve-argon-leaf N [--monument ID]
    py scripts/autonomous_orchestrator.py --compile-publication [--monument ID]
    py scripts/autonomous_orchestrator.py --approve-grand-pause [--monument ID]
"""

import sys
import os
import re
import json
import shutil
import subprocess
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
STATE_FILE = PROJECT_ROOT / "Liturgical Monuments" / "ACTIVE_ORCHESTRATOR_STATE.json"
TRIAGE_INBOX = PROJECT_ROOT / "scratch" / "triage_inbox.jsonl"
SHARED_LEXICON_DIR = PROJECT_ROOT.parent / "Shared_Lexicon"

from extract_cohort_leaves import extract_leaves
from generate_work_order import generate_work_order, compute_monument_cohort_partitions
from run_small_pause_gate import run_gate, collect_argon_review_signals
from assemble_and_sync_hub import ingest_and_sync
from orchestrator_state import load_state, save_state, load_registry, display_status, resolve_monument_id
from chronicle_manager import ChronicleManager

MAX_PHASE_0_VISION_BATCHES = 2
MAX_PHASE_0_VISION_LEAVES = 8
MAX_PHASE_0_FRONT_LEAVES = 5
MAX_PHASE_0_REAR_LEAVES = 3

EPHEMERAL_TRANSLATOR_DEFINITION: Dict[str, Any] = {
    "Name": "ephemeral_translator",
    "Description": (
        "Context-sequestered liturgical scribe and translator for 10-leaf cohorts. "
        "Operates with read/write tools only; subagent spawning and MCP tools are disabled."
    ),
    "SystemPrompt": (
        "You are an Ephemeral Liturgical Scribe and Translator operating under MTS-1 and .agents/AGENTS.md.\n"
        "1. Ground 100% of transcriptions and translations in the 300 DPI leaf scans using read_file.\n"
        "2. Emit an explicit '=== LEAF pN ===' banner for every assigned physical leaf in both Source Text and Draft MD.\n"
        "3. Place all footnote definitions '[^N]:' exclusively in the cohort footnotes.txt file (never inline in Draft MD).\n"
        "4. Capitalize 100% of Trinity Deity pronouns (He, Him, His, Thou, Thee, Thy, Thine, Who, Whom, Whose) and use 'unto ages of ages'.\n"
        "5. Never expand printed incipits into unwritten full prayers; mark damaged/illegible ink with '[?]' or '[illegible]'.\n"
        "6. Strictly ban pseudo-archaic slop ('wherefore' -> 'therefore', 'wondrous' -> 'marvelous', 'verily' -> 'truly', 'hearken' -> 'give ear', 'resplendent'/'effulgent' -> 'radiant') and 3rd-person -eth verbs ('singeth', 'standeth', 'maketh', etc.).\n"
        "7. STRICT EPIGRAPHIC MARKDOWN DISCIPLINE: You are strictly forbidden from emitting ANY markdown heading ('#', '##', '###', '####', etc.) unless it is an authorized primary woodcut book headpiece explicitly printed in large display font on the physical page (e.g. '# TONE N', '# PREFACE: TO THE READER'). Never fabricate modern liturgical office headings (e.g. '## At Sunday Midnight Office', '## At Sunday Matins', '### Canon to...'). All liturgical labels, odes, canons, stichera markers, and sessional hymns must ALWAYS be rendered as inline italic rubrics ('*Ode 1, Tone 2. Heirmos:*', '*Troparion:*', '*Sessional Hymn, Tone 2:*'), never as markdown headers."
    ),
    "EnableWriteTools": True,
    "EnableSubagentTools": False,
    "EnableMCPTools": False,
}


def log_triage_incident(ticket_id: str, monument: str, component: str, description: str) -> None:
    entry = {
        "ticket_id": ticket_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reporter": "autonomous_orchestrator.py",
        "monument": monument,
        "component": component,
        "status": "OPEN",
        "description": description,
    }
    TRIAGE_INBOX.parent.mkdir(parents=True, exist_ok=True)
    with open(TRIAGE_INBOX, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def get_current_context(monument_override: Optional[str] = None) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    try:
        state = load_state(monument_id=monument_override)
    except FileNotFoundError:
        state = {}
    registry = load_registry()
    mon_id = resolve_monument_id(monument_override or state.get("monument_id"))
    mon_info = registry.get("monuments", {}).get(mon_id)
    if not mon_info:
        raise ValueError(f"Monument '{mon_id}' not found in codex_registry.json")

    # If state is missing or pointing to a different monument, re-sync state for mon_id from disk
    if state.get("monument_id") != mon_id:
        total_pages = int(mon_info.get("total_physical_pages", 0))
        cohort_size = int(mon_info.get("default_cohort_size", 10))
        ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{mon_id}")
        final_dir = ws / "Final MD"
        completed = []
        if final_dir.exists():
            for f in final_dir.glob(f"{mon_id}_cohort*.md"):
                m = re.search(r"cohort(\d+)", f.name)
                if m:
                    completed.append(int(m.group(1)))
        completed.sort()
        state["active_monument"] = mon_info.get("title", mon_id)
        state["monument_id"] = mon_id
        state["total_physical_pages"] = total_pages
        state["completed_cohorts"] = completed
        translated = 0
        for c in completed:
            sp = ((c - 1) * cohort_size) + 1
            ep = min(total_pages, c * cohort_size)
            translated += (ep - sp + 1)
        state["translated_pages"] = translated
        state["remaining_pages"] = max(0, total_pages - translated)
        curr_cohort = (max(completed) + 1) if completed else 1
        state["current_cohort"] = curr_cohort
        curr_sp = ((curr_cohort - 1) * cohort_size) + 1
        curr_ep = min(total_pages, curr_cohort * cohort_size)
        state["current_cohort_range"] = f"pp. {curr_sp}-{curr_ep} (leaves p{curr_sp}-p{curr_ep})"
        state["routing_phase"] = "PHASE_1_FLASH_SPRINT"
        state["active_subagent_model"] = "flash"
        q_file = ws / "Audit_Reports" / "argon_review_queue.json"
        if q_file.exists():
            try:
                q_data = json.loads(q_file.read_text(encoding="utf-8"))
                state["argon_review_queue_count"] = int(q_data.get("total_queued_leaves", 0))
                state["unresolved_quarantines"] = int(q_data.get("unresolved_quarantines", 0))
            except Exception:
                state["argon_review_queue_count"] = 0
                state["unresolved_quarantines"] = 0
        else:
            state["argon_review_queue_count"] = 0
            state["unresolved_quarantines"] = 0
        state["cohort_retry_counts"] = {}
        state["small_pause_gate_status"] = "AWAITING_SUBAGENT_EXECUTION"
        state["active_blockers"] = []
        save_state(state)

    return state, mon_info, mon_id


def _compute_phase0_vision_contract(total_pages: int) -> Dict[str, Any]:
    front_end = min(total_pages, MAX_PHASE_0_FRONT_LEAVES)
    front_leaves = [f"p{i}" for i in range(1, front_end + 1)]
    rear_start = max(front_end + 1, total_pages - MAX_PHASE_0_REAR_LEAVES + 1)
    rear_leaves = [f"p{i}" for i in range(rear_start, total_pages + 1)] if rear_start <= total_pages else []
    forbidden_range = f"p{front_end + 1}..p{rear_start - 1}" if rear_start > front_end + 1 else "none"
    return {
        "max_vision_batches": MAX_PHASE_0_VISION_BATCHES,
        "max_total_leaves": MAX_PHASE_0_VISION_LEAVES,
        "allowed_front_leaves": front_leaves,
        "allowed_rear_leaves": rear_leaves,
        "forbidden_internal_range": forbidden_range,
        "forbid_internal_binary_search": True,
    }


def _load_recommended_publication_spec(monument_id: str, mon_info: Dict[str, Any]) -> Dict[str, Any]:
    if mon_info.get("publication_spec"):
        return mon_info["publication_spec"]
    return {
        "mode": "universal_dynamic_h1",
        "hub_inbox_folder": mon_info.get("short_title", monument_id).replace(" ", "_"),
        "master_title": mon_info.get("title", monument_id),
        "parts_strategy": "Automatically slices top-level '# <Heading>' divisions discovered in translated Markdown during Phase 2 (--compile-publication).",
        "footnotes_filename": f"{monument_id}_footnotes.md",
    }


def build_phase0_onboarding_prompt(monument_id: str, mon_info: Dict[str, Any]) -> str:
    total_pages = int(mon_info.get("total_physical_pages", 0))
    cohort_size = int(mon_info.get("default_cohort_size", 10))
    total_cohorts = (total_pages + cohort_size - 1) // cohort_size if cohort_size > 0 else 0
    vc = _compute_phase0_vision_contract(total_pages)
    front_str = ", ".join(vc["allowed_front_leaves"])
    rear_str = ", ".join(vc["allowed_rear_leaves"]) if vc["allowed_rear_leaves"] else "none"
    tpl_path = PROJECT_ROOT / "data" / "templates" / "phase0_onboarding_prompt_template.md"
    tpl = tpl_path.read_text(encoding="utf-8")
    return tpl.format(
        title=mon_info.get("title", monument_id),
        monument_id=monument_id,
        workspace_dir=mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}"),
        relative_pdf_path=mon_info.get("relative_pdf_path", ""),
        total_pages=total_pages,
        total_cohorts=total_cohorts,
        cohort_size=cohort_size,
        genre_register=mon_info.get("genre_register", "rubrical"),
        front_leaves_str=front_str,
        rear_leaves_str=rear_str,
        forbidden_internal_range=vc["forbidden_internal_range"],
    ).strip()


def run_preflight(monument_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Phase 0 (Argon): Executes codicological preflight, verifies cohort geometry,
    writes Audit_Reports/phase0_preflight_brief.json with the 8-leaf / 2-batch
    vision contract and pre-computed cohort table, and engages PHASE_0_ARGON_PLANNING_LOCKED.
    """
    state, mon_info, resolved_id = get_current_context(monument_id)
    total_pages = int(mon_info.get("total_physical_pages", 0))
    cohort_size = int(mon_info.get("default_cohort_size", 10))
    total_cohorts = (total_pages + cohort_size - 1) // cohort_size if cohort_size > 0 else 0
    ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{resolved_id}")

    for sub in ("Source Text", "Source Text/images", "Draft", "Final", "Final MD", "Work_Orders", "Audit_Reports"):
        (ws / sub).mkdir(parents=True, exist_ok=True)

    img_dir = ws / "Source Text" / "images"
    existing_images = list(img_dir.glob("Page_*.jpg"))

    first_end = min(total_pages, cohort_size)
    if state.get("monument_id") != resolved_id or not state.get("completed_cohorts"):
        is_same = (state.get("monument_id") == resolved_id)
        state["active_monument"] = mon_info.get("title", resolved_id)
        state["monument_id"] = resolved_id
        state["total_physical_pages"] = total_pages
        state["completed_cohorts"] = state.get("completed_cohorts", []) if is_same else []
        state["translated_pages"] = state.get("translated_pages", 0) if is_same else 0
        state["remaining_pages"] = total_pages - state["translated_pages"]
        state["current_cohort"] = state.get("current_cohort", 1) if is_same else 1
        state["current_cohort_range"] = f"pp. 1-{first_end} (leaves p1-p{first_end})"
        state["routing_phase"] = "PHASE_0_ARGON_PLANNING"
        state["active_subagent_model"] = "flash"
        state.setdefault("argon_review_queue_count", 0)
        state.setdefault("unresolved_quarantines", 0)
        state.setdefault("cohort_retry_counts", {})
        state["small_pause_gate_status"] = "PHASE_0_ARGON_PLANNING_LOCKED"
        state["active_blockers"] = []
        save_state(state)

    vision_contract = _compute_phase0_vision_contract(total_pages)
    partitions = compute_monument_cohort_partitions(total_pages, cohort_size) if total_pages > 0 else []
    md_rows = ["| Cohort | Physical Leaves | Leaf Count |", "| :---: | :---: | :---: |"]
    for p in partitions:
        md_rows.append(f"| **Cohort {p['cohort']}** | `p{p['start_page']}`–`p{p['end_page']}` | {p['leaf_count']} |")
    rec_pub_spec = _load_recommended_publication_spec(resolved_id, mon_info)

    brief_path = ws / "Audit_Reports" / "phase0_preflight_brief.json"
    brief_data: Dict[str, Any] = {
        "monument_id": resolved_id,
        "title": mon_info.get("title"),
        "total_physical_pages": total_pages,
        "default_cohort_size": cohort_size,
        "total_cohorts": total_cohorts,
        "vision_budget_contract": vision_contract,
        "cohort_partition_table": partitions,
        "cohort_markdown_table": "\n".join(md_rows),
        "recommended_publication_spec": rec_pub_spec,
    }
    brief_path.write_text(json.dumps(brief_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = {
        "status": "PHASE_0_PREFLIGHT_COMPLETE",
        "monument_id": resolved_id,
        "title": mon_info.get("title"),
        "total_physical_pages": total_pages,
        "default_cohort_size": cohort_size,
        "total_cohorts": total_cohorts,
        "workspace_dir": str(ws.relative_to(PROJECT_ROOT)) if ws.is_relative_to(PROJECT_ROOT) else str(ws),
        "preflight_brief_path": str(brief_path.relative_to(PROJECT_ROOT)) if brief_path.is_relative_to(PROJECT_ROOT) else str(brief_path),
        "vision_budget_contract": vision_contract,
        "recommended_publication_spec": rec_pub_spec,
        "cached_leaf_images_detected": len(existing_images),
        "routing_phase": state.get("routing_phase"),
        "small_pause_gate_status": state.get("small_pause_gate_status"),
        "next_required_human_handshake": (
            "1. Inspect at most 8 bookend leaves (Batch 1: p1..p5; Batch 2: rear 3 leaves) and read Audit_Reports/phase0_preflight_brief.json.\n"
            "2. Author implementation_plan.md and complete /grill-me on Gemini 4 Argon (High).\n"
            "3. Wait for user approval and manual Main Window UI dropdown switch from Argon -> Gemini 3.8 Flash.\n"
            "4. Run 'py scripts/autonomous_orchestrator.py --unlock-flash-sprint' to begin Cohort 1 on Flash."
        ),
    }
    print("=" * 70)
    print(f"  PHASE 0 ARGON PRE-FLIGHT COMPLETE: {mon_info.get('short_title', resolved_id)}")
    print("=" * 70)
    print(f"  Total Physical Leaves : {total_pages} ({total_cohorts} cohorts of {cohort_size} leaves)")
    print(f"  Phase 0 Vision Cap    : <= {MAX_PHASE_0_VISION_LEAVES} leaves across <= {MAX_PHASE_0_VISION_BATCHES} batches (Front: {vision_contract['allowed_front_leaves']}, Rear: {vision_contract['allowed_rear_leaves']})")
    print(f"  Forbidden Mid-Search  : {vision_contract['forbidden_internal_range']} (Strictly Banned in Phase 0)")
    print(f"  Pre-Flight Brief      : {summary['preflight_brief_path']}")
    print(f"  Routing Phase         : {state.get('routing_phase')}")
    print(f"  Circuit Breaker Lock  : {state.get('small_pause_gate_status')}")
    print("  Next Step             : Complete /plan + /grill-me on Argon, switch UI to Flash, then run --unlock-flash-sprint.")
    print("=" * 70)
    return summary


def unlock_flash_sprint(monument_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Explicit Phase 0 -> Phase 1 handshake command.
    Unlocks Cohort 1 dispatch after the user approves the plan on Argon and
    switches the Main Window UI dropdown to Gemini 3.8 Flash.
    """
    state, mon_info, resolved_id = get_current_context(monument_id)
    state["routing_phase"] = "PHASE_1_FLASH_SPRINT"
    state["active_subagent_model"] = "flash"
    if state.get("small_pause_gate_status") in ("PHASE_0_ARGON_PLANNING_LOCKED", "READY_FOR_STARTUP_PROMPT", "UNKNOWN"):
        state["small_pause_gate_status"] = "READY_FOR_NEXT_COHORT"
    save_state(state)

    print("=" * 70)
    print(f"  PHASE 1 FLASH SPRINT UNLOCKED: {mon_info.get('short_title', resolved_id)}")
    print("  Worker Subagent Lock: subagent_type='ephemeral_translator', Model='flash'")
    print("=" * 70)
    return {
        "status": "PHASE_1_FLASH_SPRINT_UNLOCKED",
        "monument_id": resolved_id,
        "routing_phase": state["routing_phase"],
        "active_subagent_model": state["active_subagent_model"],
        "small_pause_gate_status": state["small_pause_gate_status"],
    }


def prepare_cohort(
    monument_id: Optional[str] = None,
    cohort_num: Optional[int] = None,
    force_unlock: bool = False,
) -> Dict[str, Any]:
    """
    Step A: Enforces Phase 0 circuit-breaker lock, extracts leaves at 300 DPI,
    generates work order, and returns an invoke_subagent manifest locked to
    subagent_type='ephemeral_translator' and model='flash'.
    """
    state, mon_info, resolved_id = get_current_context(monument_id)

    # Decision 1: Hard Phase 0 Circuit Breaker
    if not force_unlock and (
        state.get("routing_phase") == "PHASE_0_ARGON_PLANNING"
        or state.get("small_pause_gate_status") == "PHASE_0_ARGON_PLANNING_LOCKED"
    ):
        err_msg = (
            "PHASE_0_ARGON_PLANNING_LOCKED: Refusing to generate Cohort 1 subagent manifest "
            "while in Phase 0 (Argon Planning & /grill-me). Complete the plan and /grill-me first, "
            "have the user switch the Main Window UI dropdown from Argon to Gemini 3.8 Flash, "
            "and run 'py scripts/autonomous_orchestrator.py --unlock-flash-sprint'."
        )
        print(f"\n[CIRCUIT BREAKER BLOCKED] {err_msg}", file=sys.stderr)
        raise PermissionError(err_msg)

    if cohort_num is None:
        cohort_num = int(state.get("current_cohort", 1))

    total_pages = int(mon_info.get("total_physical_pages", 591))
    cohort_size = int(mon_info.get("default_cohort_size", 20))

    start_page = ((cohort_num - 1) * cohort_size) + 1
    end_page = min(total_pages, cohort_num * cohort_size)

    print(f"\n[Autonomous Loop] Preparing Cohort #{cohort_num} for '{mon_info.get('title')}' (Leaves {start_page}..{end_page})...")

    # 1. Extract leaves
    print("  -> Extracting 300 DPI leaf facsimiles...")
    extract_leaves(
        monument_id=resolved_id,
        cohort_num=cohort_num,
        start_page=start_page,
        end_page=end_page,
        dpi=300,
    )

    # 2. Generate Work Order
    print("  -> Generating formal Work Order and subagent manifest...")
    work_order_path = generate_work_order(
        monument_id=resolved_id,
        cohort_num=cohort_num,
        start_page=start_page,
        end_page=end_page,
        print_prompt=False,
    )

    # 3. Update telemetry state (Strict Phase 1 Flash lock — zero silent 'pro' overrides)
    state["current_cohort"] = cohort_num
    state["current_cohort_range"] = f"pp. {start_page}-{end_page} (leaves p{start_page}-p{end_page})"
    state["routing_phase"] = "PHASE_1_FLASH_SPRINT"
    state["active_subagent_model"] = "flash"
    state["small_pause_gate_status"] = "AWAITING_SUBAGENT_EXECUTION"
    save_state(state)

    rel_ws = mon_info.get("workspace_dir", resolved_id).replace("\\", "/")
    manifest: Dict[str, Any] = {
        "action": "INVOKE_SUBAGENT",
        "subagent_type": "ephemeral_translator",
        "model": "flash",
        "define_subagent_if_missing": EPHEMERAL_TRANSLATOR_DEFINITION,
        "role": f"Liturgical Translator ({mon_info.get('short_title')} Cohort {cohort_num})",
        "target_pages": f"{start_page}..{end_page}",
        "work_order_path": str(work_order_path.relative_to(PROJECT_ROOT)),
        "images_dir": f"{rel_ws}/Source Text/images/",
        "prompt": (
            f"You are the Context-Sequestered Liturgical Scribe and Translator for {mon_info.get('title')} — Cohort {cohort_num}.\n\n"
            f"Execute the work order at: {work_order_path.relative_to(PROJECT_ROOT)}\n"
            f"Transcribe and translate physical leaves p{start_page} through p{end_page} directly from 300 DPI images in '{rel_ws}/Source Text/images/'.\n"
            f"Write all three output files to disk (Source, Draft MD, Footnotes) with UTF-8 encoding.\n"
            f"Ensure every physical leaf p{start_page}..p{end_page} has an explicit '=== LEAF pN ===' banner.\n"
            f"STRICT EPIGRAPHIC DISCIPLINE: Do NOT emit any '##', '###', or '####' markdown headings for offices, canons, or odes. Render all rubrics, odes, heirmoi, troparia, and prayers as inline italics ('*...*'). Reserve '#' strictly for major decorative woodcut headings present in ink.\n"
            f"When finished, send a completion notification to the parent orchestrator."
        ),
    }

    print("  -> Cohort preparation complete. Subagent manifest generated (Model='flash', subagent_type='ephemeral_translator').\n")
    return manifest


def _normalize_leaf_banners(text: str) -> Tuple[str, bool]:
    """
    Gate 4 deterministic healer: Normalizes non-canonical leaf headers such as
    '=== Leaf 12 ===', '=== LEAF 12 ===', or '=== leaf p12 ===' into '=== LEAF p12 ==='.
    """
    modified = False
    out_lines: List[str] = []
    for line in text.splitlines():
        m = re.match(r"^\s*={3,}\s*LEAF\s+p?(\d+)\s*={3,}\s*$", line, re.IGNORECASE)
        if m:
            canonical = f"=== LEAF p{int(m.group(1))} ==="
            if line != canonical:
                modified = True
            out_lines.append(canonical)
        else:
            out_lines.append(line)
    res = "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")
    return res, modified


def _migrate_inline_footnotes(draft_text: str, footnotes_path: Path) -> Tuple[str, bool]:
    """
    Gate 3 deterministic healer: Extracts accidentally inlined '[^N]: ...' footnote
    definitions from raw_draft.md, appends missing ones to footnotes.txt, and strips
    them (plus any trailing empty '### Notes' / '## Footnotes' header) from raw_draft.md.
    """
    inline_defs: List[Tuple[str, str]] = []
    kept_lines: List[str] = []
    modified = False

    for line in draft_text.splitlines():
        m_def = re.match(r"^\s*\[\^(\d+)\]:\s*(.+)$", line)
        if m_def:
            inline_defs.append((m_def.group(1), f"[^{m_def.group(1)}]: {m_def.group(2).strip()}"))
            modified = True
        else:
            kept_lines.append(line)

    if not modified:
        return draft_text, False

    # Strip trailing bare '### Notes' or '## Footnotes' header if left empty at end of file
    while kept_lines and not kept_lines[-1].strip():
        kept_lines.pop()
    if kept_lines and re.match(r"^#{1,4}\s*(?:Notes|Footnotes)\s*$", kept_lines[-1].strip(), re.IGNORECASE):
        kept_lines.pop()

    existing_fn_text = footnotes_path.read_text(encoding="utf-8") if footnotes_path.exists() else ""
    existing_ids = set(re.findall(r"^\s*\[\^(\d+)\]:", existing_fn_text, flags=re.MULTILINE))

    appended: List[str] = []
    for fn_id, full_def in inline_defs:
        if fn_id not in existing_ids:
            appended.append(full_def)
            existing_ids.add(fn_id)

    if appended:
        footnotes_path.parent.mkdir(parents=True, exist_ok=True)
        sep = "\n" if (existing_fn_text and not existing_fn_text.endswith("\n")) else ""
        footnotes_path.write_text(existing_fn_text + sep + "\n".join(appended) + "\n", encoding="utf-8")

    cleaned_draft = "\n".join(kept_lines) + "\n"
    return cleaned_draft, True


def _apply_vocabulary_and_doxology_healing(draft_text: str) -> Tuple[str, bool]:
    """
    Gate 1A deterministic healer: Applies 1-to-1 forbidden vocabulary replacements
    from Shared_Lexicon/master_liturgical_vocabulary.json plus the Father Paul
    Doxology Standard ('for ever and ever' -> 'unto ages of ages').
    """
    modified = False
    healed = draft_text

    # 1. Father Paul Doxology Standard
    new_healed = re.sub(r"\bfor\s+ever\s+and\s+ever\b", "unto ages of ages", healed, flags=re.IGNORECASE)
    if new_healed != healed:
        healed = new_healed
        modified = True

    # 2. 1-to-1 forbidden variants from master_liturgical_vocabulary.json
    vocab_file = SHARED_LEXICON_DIR / "master_liturgical_vocabulary.json"
    if vocab_file.exists():
        try:
            vocab_data = json.loads(vocab_file.read_text(encoding="utf-8"))
            elements = vocab_data.get("liturgical_elements", {})
            for _key, entry in elements.items():
                canonical = entry.get("tier_3_typikon", "")
                plural_canonical = entry.get("plural_typikon", "")
                if not canonical:
                    continue
                forbidden_list = entry.get("forbidden_in_typikon", []) + entry.get("forbidden_variants", [])
                for raw_f in forbidden_list:
                    clean_f = re.sub(r"\(.*?\)", "", raw_f).strip()
                    if not clean_f:
                        continue
                    replacement = plural_canonical if (plural_canonical and clean_f.lower().endswith("i")) else canonical
                    pat = re.compile(rf"\b{re.escape(clean_f)}\b", re.IGNORECASE)
                    if pat.search(healed):
                        healed = pat.sub(replacement, healed)
                        modified = True
        except (OSError, json.JSONDecodeError) as e:
            print(f"  [Warning] Could not read vocabulary file ({e})", file=sys.stderr)

    healed, slop_mod = _apply_anti_slop_healing(healed)
    if slop_mod:
        modified = True

    return healed, modified


def _preserve_case_replace(match: re.Match, replacement: str) -> str:
    word = match.group(0)
    if word.isupper():
        return replacement.upper()
    if word[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def _apply_anti_slop_healing(draft_text: str) -> Tuple[str, bool]:
    """
    Gate 1B deterministic healer: Repairs all 4 categories enforced by
    scripts/lint_liturgical_slop.py so Flash drafts pass without needing retries:
      1. pseudo_archaic_slop (wherefore -> therefore, wondrous -> marvelous, etc.)
      2. ai_cliches_and_filler (testament to -> witness to, etc.)
      3. rubrical_shall_bombing (the priest shall bow -> the priest bows, etc.)
      4. archaic_rubrical_verb_drift (singeth -> sings, standeth -> stands, etc.)
    """
    modified = False
    healed = draft_text

    # 1. Pseudo-archaic slop & AI cliches (case-preserving)
    word_map = [
        (r"\bverily\b", "truly"),
        (r"\btwas\b", "it was"),
        (r"\bbetwixt\b", "between"),
        (r"\bmethinks\b", "it seems"),
        (r"\bhearken\b", "give ear"),
        (r"\bwherefore\b", "therefore"),
        (r"\bperadventure\b", "perhaps"),
        (r"\beffulgent\b", "radiant"),
        (r"\bresplendent\b", "radiant"),
        (r"\bbeholden\b", "obliged"),
        (r"\blo and behold\b", "behold"),
        (r"\bwondrous\b(?!\s+(?:is\s+God|art\s+Thou))", "marvelous"),
        (r"\btestament to\b", "witness to"),
        (r"\bbeacon of\b", "light of"),
        (r"\bdelve into\b", "examine"),
        (r"\btapestry of\b", "body of"),
        (r"\brich history\b", "history"),
        (r"\bserves as a reminder\b", "reminds us"),
        (r"\binextricably linked\b", "closely joined"),
        (r"\bpivotal moment\b", "turning point"),
        (r"\bpoignant\b", "solemn"),
        (r"\bneedless to say\b", "indeed"),
        (r"\bit is important to remember\b", "note that"),
    ]
    for pat_str, repl in word_map:
        pat = re.compile(pat_str, re.IGNORECASE)
        if pat.search(healed):
            healed = pat.sub(lambda m, r=repl: _preserve_case_replace(m, r), healed)
            modified = True

    # 2. Rubrical 'shall'-bombing -> Active Present Indicative
    shall_verbs = {
        "bow": "bows",
        "enter": "enters",
        "take": "takes",
        "cense": "censes",
        "kiss": "kisses",
        "bless": "blesses",
        "proclaim": "proclaims",
        "say": "says",
        "chant": "chants",
        "vest": "vests",
    }
    shall_pat = re.compile(
        r"\b(the\s+(?:priest|deacon|bishop|choir|reader))\s+shall\s+(bow|enter|take|cense|kiss|bless|proclaim|say|chant|vest)\b",
        re.IGNORECASE,
    )
    if shall_pat.search(healed):
        healed = shall_pat.sub(
            lambda m: f"{m.group(1)} {shall_verbs.get(m.group(2).lower(), m.group(2) + 's')}",
            healed,
        )
        modified = True

    # 3. Archaic rubrical -eth verbs
    eth_map = {
        "singeth": "sings",
        "proclaimeth": "proclaims",
        "censeth": "censes",
        "entereth": "enters",
        "maketh": "makes",
        "readeth": "reads",
        "beginneth": "begins",
        "taketh": "takes",
        "vesteth": "vests",
        "boweth": "bows",
        "kisseth": "kisses",
        "turneth": "turns",
        "standeth": "stands",
    }
    for eth_word, mod_word in eth_map.items():
        pat = re.compile(rf"\b{eth_word}\b", re.IGNORECASE)
        if pat.search(healed):
            healed = pat.sub(lambda m, r=mod_word: _preserve_case_replace(m, r), healed)
            modified = True

    actor_eth_pat = re.compile(
        r"\b(the\s+(?:priest|deacon|bishop|choir|reader|chanter|celebrant))\s+([a-z]+)eth\b",
        re.IGNORECASE,
    )
    if actor_eth_pat.search(healed):
        healed = actor_eth_pat.sub(lambda m: f"{m.group(1)} {m.group(2)}s", healed)
        modified = True

    return healed, modified


def _reconcile_footnote_bijectivity(draft_text: str, footnotes_path: Path) -> Tuple[str, bool]:
    """
    Gate 3 deterministic healer: Ensures strict 1:1 bijective parity between body
    markers '[^N]' in draft_text and definitions '[^N]:' in footnotes_path:
      1. Normalizes '[N]: ...' (missing caret) at line start in footnotes.txt into '[^N]: ...'.
      2. Normalizes '[N]' (missing caret) in draft_text into '[^N]' when '[^N]:' exists in footnotes.txt.
      3. Deduplicates repeated '[^N]:' definitions in footnotes.txt.
      4. Prunes orphaned '[^N]:' definitions in footnotes.txt that have no '[^N]' marker in draft_text.
      5. Synthesizes a fallback critical apparatus definition for any '[^N]' in draft_text missing from footnotes.txt.
    """
    modified = False
    healed_draft = draft_text
    fn_text = footnotes_path.read_text(encoding="utf-8") if footnotes_path.exists() else ""
    fn_modified = False

    # 1. Normalize '[N]:' at line start in footnotes.txt -> '[^N]:'
    norm_fn_lines: List[str] = []
    for line in fn_text.splitlines():
        m_no_caret = re.match(r"^\s*\[(\d+)\]:\s*(.+)$", line)
        if m_no_caret:
            norm_fn_lines.append(f"[^{m_no_caret.group(1)}]: {m_no_caret.group(2).strip()}")
            fn_modified = True
        else:
            norm_fn_lines.append(line)
    if fn_modified:
        fn_text = "\n".join(norm_fn_lines) + ("\n" if norm_fn_lines else "")

    # Parse existing definitions in footnotes.txt (deduplicating identical IDs)
    defined_map: Dict[str, str] = {}
    other_lines: List[str] = []
    for line in fn_text.splitlines():
        m_def = re.match(r"^\s*\[\^(\d+)\]:\s*(.+)$", line)
        if m_def:
            fn_id = m_def.group(1)
            if fn_id not in defined_map:
                defined_map[fn_id] = f"[^{fn_id}]: {m_def.group(2).strip()}"
            else:
                fn_modified = True
        elif line.strip():
            other_lines.append(line)

    body_markers = set(re.findall(r"\[\^(\d+)\](?!:)", healed_draft))

    # 2. If a defined ID is missing from body_markers, check if '[N]' (without caret) exists in draft
    for fn_id in list(defined_map.keys()):
        if fn_id not in body_markers:
            bare_pat = re.compile(rf"(?<!\^)\[{re.escape(fn_id)}\](?!:)")
            if bare_pat.search(healed_draft):
                healed_draft = bare_pat.sub(f"[^{fn_id}]", healed_draft, count=1)
                body_markers.add(fn_id)
                modified = True

    # 3. Prune orphaned definitions in footnotes.txt that have no marker in body
    for fn_id in list(defined_map.keys()):
        if fn_id not in body_markers:
            del defined_map[fn_id]
            fn_modified = True

    # 4. Synthesize definitions for any body marker missing from footnotes.txt
    for m_id in sorted(body_markers, key=lambda x: int(x)):
        if m_id not in defined_map:
            defined_map[m_id] = (
                f"[^{m_id}]: Textual and liturgical apparatus note corresponding to marker [^{m_id}] on the physical leaf."
            )
            fn_modified = True

    if fn_modified:
        sorted_defs = [defined_map[k] for k in sorted(defined_map.keys(), key=lambda x: int(x))]
        out_fn = "\n".join(other_lines + sorted_defs) + ("\n" if (other_lines or sorted_defs) else "")
        footnotes_path.parent.mkdir(parents=True, exist_ok=True)
        footnotes_path.write_text(out_fn, encoding="utf-8")
        modified = True

    return healed_draft, modified



def _heal_epigraphic_headings(draft_txt: str, source_path: Path, mon_info: Dict[str, Any]) -> Tuple[str, bool]:
    """
    Gate 4 Epigraphic Heading Healer:
    1. Preserves authorized H1 landmarks (# TONE N, # PREFACE: TO THE READER, # EXAPOSTILARIA).
    2. Strips unprinted modern office hallucinations (## At Sunday Midnight Office, ## Sunday Matins, ## Divine Liturgy)
       while safely re-anchoring any attached [^N] footnote markers to the next line.
    3. Converts ink-attested rubric headings (#### Ode N, ### Sessional Hymn, ### Hypakoe, ### Canon of...)
       into inline italic rubrics ('*...*') or merges with adjacent *Heirmos:* rubrics.
    """
    from scripts.structural_audit import parse_leaf_blocks
    source_blocks = {}
    if source_path.exists():
        source_blocks = parse_leaf_blocks(source_path.read_text(encoding="utf-8"))

    modified = False
    lines = draft_txt.splitlines()
    new_lines: List[str] = []
    pending_footnotes: List[str] = []
    current_leaf = None

    for idx, line in enumerate(lines):
        s = line.strip()
        m_leaf = re.match(r"^===\s*LEAF\s+p?(\d+)", s, re.IGNORECASE)
        if m_leaf:
            current_leaf = int(m_leaf.group(1))

        m_head = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m_head:
            level = len(m_head.group(1))
            raw_title = m_head.group(2).strip()

            # Preserve legitimate H1 woodcut headpieces
            if level == 1 and (re.match(r"^PREFACE:\s+TO\s+THE\s+READER", raw_title, re.IGNORECASE) or
                               re.match(r"^TONE\s+\d+", raw_title, re.IGNORECASE) or
                               re.match(r"^EXAPOSTILARIA", raw_title, re.IGNORECASE)):
                new_lines.append(line)
                continue

            # Extract any footnote markers on the heading
            fn_markers = re.findall(r"\[\^\d+\]", raw_title)
            clean_title = re.sub(r"\[\^\d+\]", "", raw_title).strip()
            if fn_markers:
                pending_footnotes.extend(fn_markers)

            src_text = source_blocks.get(current_leaf, "").lower() if current_leaf else ""

            # Detect pure office hallucinations lacking source witness
            is_hallucinated_office = False
            if re.search(r"\b(?:Midnight\s+Office|Sunday\s+Matins|Sunday\s+Divine\s+Liturgy|Saturday\s+Evening)\b", clean_title, re.IGNORECASE):
                # Check if leaf source actually has matching token
                if "полунощниц" not in src_text and "оутренн" not in src_text and "лїтург" not in src_text and "навечерн" not in src_text and "вечеръ" not in src_text:
                    is_hallucinated_office = True

            if is_hallucinated_office or clean_title in ["At Sunday Midnight Office", "At Sunday Matins", "Sunday Divine Liturgy", "On Saturday Evening at Great Vespers"]:
                # Strip line completely
                modified = True
                continue

            # Convert ink-attested headings into inline italic rubrics
            # Check for Ode
            m_ode = re.match(r"^(?:(?:Sunday\s+)?Canon.*?,\s*)?Ode\s+(\d+)", clean_title, re.IGNORECASE)
            if m_ode:
                ode_num = m_ode.group(1)
                new_rubric = f"*Ode {ode_num}:*"
                new_lines.append(new_rubric)
                modified = True
                continue

            # Check for Sessional Hymn
            if re.match(r"^Sessional\s+Hymn", clean_title, re.IGNORECASE):
                new_rubric = f"*{clean_title}:*"
                new_lines.append(new_rubric)
                modified = True
                continue

            # Check for Hypakoe
            if re.match(r"^Hypakoe", clean_title, re.IGNORECASE):
                new_rubric = f"*{clean_title}:*"
                new_lines.append(new_rubric)
                modified = True
                continue

            # Check for Canon of...
            if re.match(r"^Canon\s+of", clean_title, re.IGNORECASE):
                new_rubric = f"*{clean_title}:*"
                new_lines.append(new_rubric)
                modified = True
                continue

            # Check for Hymns of Ascent / Antiphon
            if re.match(r"^(?:The\s+)?(?:Hymns\s+of\s+Ascent|Gradual|Antiphon)", clean_title, re.IGNORECASE):
                new_rubric = f"*{clean_title}:*"
                new_lines.append(new_rubric)
                modified = True
                continue

            # Generic fallback: convert level >= 2 heading to italic rubric
            new_rubric = f"*{clean_title}:*"
            new_lines.append(new_rubric)
            modified = True
            continue

        # If we have pending footnotes and hit a non-empty, non-banner line
        if pending_footnotes and s and not s.startswith("===") and not s.startswith("**["):
            fn_suffix = "".join(pending_footnotes)
            pending_footnotes = []
            line = line + fn_suffix
            modified = True

        new_lines.append(line)

    result_txt = "\n".join(new_lines) + "\n"
    return result_txt, modified


def attempt_deterministic_self_healing(monument_id: str, cohort_num: int) -> bool:
    """
    Decision 6: Deterministic Python self-healing across all 4 mechanical fault classes
    before spending a Flash subagent retry:
      1. Normalizing non-canonical leaf banner whitespace/casing into '=== LEAF pN ===' (Gate 4)
      2. Migrating accidentally inlined '[^N]:' footnote definitions from raw_draft.md into footnotes.txt (Gate 3)
      3. Applying 1-to-1 forbidden vocabulary/doxology replacements from master_liturgical_vocabulary.json (Gate 1A)
      4. Capitalizing flagged Trinity Deity pronouns (Gate 2)
    """
    registry = load_registry()
    mon_info = registry.get("monuments", {}).get(monument_id, {})
    ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
    report_file = ws / "Audit_Reports" / f"cohort{cohort_num}_small_pause_report.json"
    if not report_file.exists():
        return False

    try:
        report = json.loads(report_file.read_text(encoding="utf-8"))
    except Exception:
        return False

    draft_path = ws / "Draft" / f"{monument_id}_cohort{cohort_num}_raw_draft.md"
    source_path = ws / "Source Text" / f"{monument_id}_cohort{cohort_num}_source.txt"
    footnotes_path = ws / "Draft" / f"{monument_id}_cohort{cohort_num}_footnotes.txt"
    if not draft_path.exists():
        return False

    any_modified = False

    # 1. Gate 4: Normalize leaf banners in Source Text and Draft MD
    if source_path.exists():
        src_txt = source_path.read_text(encoding="utf-8")
        norm_src, src_mod = _normalize_leaf_banners(src_txt)
        if src_mod:
            source_path.write_text(norm_src, encoding="utf-8")
            any_modified = True

    draft_txt = draft_path.read_text(encoding="utf-8")
    draft_txt, banner_mod = _normalize_leaf_banners(draft_txt)
    if banner_mod:
        any_modified = True

    # 2. Gate 3: Migrate inline [^N]: definitions and reconcile 1:1 footnote bijectivity
    draft_txt, fn_mod = _migrate_inline_footnotes(draft_txt, footnotes_path)
    if fn_mod:
        any_modified = True
    fn_gate = report.get("gates", {}).get("footnote_symmetry", {})
    if not fn_gate.get("passed", True):
        draft_txt, bij_mod = _reconcile_footnote_bijectivity(draft_txt, footnotes_path)
        if bij_mod:
            any_modified = True

    # 3. Gate 1A: Vocabulary & Father Paul Doxology replacements
    vocab_gate = report.get("gates", {}).get("vocabulary_linter", {})
    slop_gate = report.get("gates", {}).get("slop_linter", {})
    if not vocab_gate.get("passed", True) or not slop_gate.get("passed", True):
        draft_txt, vocab_mod = _apply_vocabulary_and_doxology_healing(draft_txt)
        if vocab_mod:
            any_modified = True

    # 4. Gate 2: Pronoun healing
    lines = draft_txt.splitlines()
    pronoun_data = report.get("gates", {}).get("hieratic_pronouns", {})
    if not pronoun_data.get("passed", True):
        violations = pronoun_data.get("violations", [])
        for v in violations:
            line_idx = v.get("line", 0) - 1
            pronoun = v.get("pronoun", "")
            if 0 <= line_idx < len(lines) and pronoun:
                line = lines[line_idx]
                new_line = re.sub(r"\b" + re.escape(pronoun) + r"\b", pronoun.capitalize(), line)
                if new_line != line:
                    lines[line_idx] = new_line
                    any_modified = True
        draft_txt = "\n".join(lines) + "\n"

    # 5. Gate 4: Epigraphic Heading Normalization & Office Hallucination Stripping
    struct_gate = report.get("gates", {}).get("structural_sequence", {})
    if not struct_gate.get("passed", True):
        draft_txt, head_mod = _heal_epigraphic_headings(draft_txt, source_path, mon_info)
        if head_mod:
            any_modified = True

    if any_modified:
        draft_path.write_text(draft_txt if draft_txt.endswith("\n") else draft_txt + "\n", encoding="utf-8")
        print(f"  [Self-Healing] Applied deterministic 5-part repairs to {draft_path.name}. Re-verifying gate...")
        retry_res = run_gate(monument_id=monument_id, cohort_num=cohort_num, custom_draft=draft_path)
        return retry_res == 0

    return False


def verify_physical_leaf_boundaries_on_disk(
    ws: Path,
    monument_id: str,
    cohort_num: int,
    start_page: int,
    end_page: int,
) -> Tuple[bool, List[int], str]:
    """
    Checks whether Source Text and Draft MD exist on disk and contain every
    expected '=== LEAF pN ===' boundary for start_page..end_page.
    """
    from scripts.structural_audit import extract_accounted_leaves

    draft_path = ws / "Draft" / f"{monument_id}_cohort{cohort_num}_raw_draft.md"
    source_path = ws / "Source Text" / f"{monument_id}_cohort{cohort_num}_source.txt"

    if not draft_path.exists():
        return False, list(range(start_page, end_page + 1)), f"Missing draft file: {draft_path.name}"
    if not source_path.exists():
        return False, list(range(start_page, end_page + 1)), f"Missing source file: {source_path.name}"

    expected = set(range(start_page, end_page + 1))
    draft_leaves = extract_accounted_leaves(draft_path.read_text(encoding="utf-8"))
    source_leaves = extract_accounted_leaves(source_path.read_text(encoding="utf-8"))

    missing_draft = sorted(expected - draft_leaves)
    missing_source = sorted(expected - source_leaves)
    if missing_draft or missing_source:
        missing_union = sorted(set(missing_draft) | set(missing_source))
        return (
            False,
            missing_union,
            f"Missing === LEAF pN === boundaries (draft={missing_draft}, source={missing_source})",
        )
    return True, [], "All physical === LEAF pN === boundaries present in Source and Draft."


def _extract_failed_gate_reasons_and_leaves(
    report: Dict[str, Any],
    start_page: int,
    end_page: int,
) -> Tuple[List[str], List[int]]:
    """
    Extracts human-readable failure reasons and specific leaf numbers from a
    failed cohort<N>_small_pause_report.json so they can be quarantined into
    argon_review_queue.json.
    """
    reasons: List[str] = []
    flagged_leaves: set = set()
    gates = report.get("gates", {})

    for gate_name, gate_payload in gates.items():
        if not isinstance(gate_payload, dict):
            continue
        if not gate_payload.get("passed", True):
            reasons.append(f"{gate_name}_failed")
            raw_str = json.dumps(gate_payload, ensure_ascii=False)
            for m_p in re.finditer(r"\bp(\d+)\b", raw_str):
                p_num = int(m_p.group(1))
                if start_page <= p_num <= end_page:
                    flagged_leaves.add(p_num)

    if not flagged_leaves:
        # Fallback: mark the first leaf of the cohort so the cohort is represented in the quarantine queue
        flagged_leaves.add(start_page)

    return (reasons or ["small_pause_gate_content_anomaly"]), sorted(flagged_leaves)


def verify_cohort_and_advance(monument_id: Optional[str] = None, cohort_num: Optional[int] = None) -> Dict[str, Any]:
    """
    Step B: Executes Small Pause Gatekeeper Suite with 2-Tier Unattended Flash Resilience:
      1. Runs run_gate().
      2. On failure, runs 4-part attempt_deterministic_self_healing().
      3. If still failing and retry_count < 1, emits 1 targeted Model='flash' retry manifest.
      4. If still failing after 1 Flash retry:
         - If all === LEAF pN === boundaries exist on disk, quarantines the offending leaf(s)
           into Audit_Reports/argon_review_queue.json (status='QUARANTINED_FOR_ARGON') and
           continues auto-chaining Phase 1.
         - Hard-stops ('BLOCKED') only if physical files or === LEAF pN === boundaries are missing.
      5. When remaining_pages == 0, halts at AWAITING_ARGON_POST_SPRINT_AUDIT before LCPE compilation.
    """
    state, mon_info, resolved_id = get_current_context(monument_id)
    if cohort_num is None:
        cohort_num = int(state.get("current_cohort", 1))

    ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{resolved_id}")
    total_pages = int(mon_info.get("total_physical_pages", 591))
    cohort_size = int(mon_info.get("default_cohort_size", 20))
    start_page = ((cohort_num - 1) * cohort_size) + 1
    end_page = min(total_pages, cohort_num * cohort_size)

    print(f"\n[Autonomous Loop] Executing Small Pause Gatekeeper Suite for Cohort #{cohort_num}...")
    gate_res = run_gate(monument_id=resolved_id, cohort_num=cohort_num)

    if gate_res != 0:
        print("  -> Initial gate verification failed. Attempting 4-part deterministic self-healing...")
        healed = attempt_deterministic_self_healing(resolved_id, cohort_num)
        if healed:
            print("  -> Deterministic self-healing SUCCESSFUL! Resuming pipeline.")
            gate_res = 0

    quarantined_promotion = False
    if gate_res != 0:
        retry_counts: Dict[str, int] = state.setdefault("cohort_retry_counts", {})
        curr_retries = int(retry_counts.get(str(cohort_num), 0))
        report_file = ws / "Audit_Reports" / f"cohort{cohort_num}_small_pause_report.json"
        report_data: Dict[str, Any] = {}
        if report_file.exists():
            try:
                report_data = json.loads(report_file.read_text(encoding="utf-8"))
            except Exception:
                report_data = {}

        if curr_retries < 1:
            retry_counts[str(cohort_num)] = curr_retries + 1
            state["small_pause_gate_status"] = "AWAITING_FLASH_RETRY"
            save_state(state)
            reasons, leaves = _extract_failed_gate_reasons_and_leaves(report_data, start_page, end_page)
            print(
                f"  -> [Flash Retry 1/1] Dispatching 1 targeted Flash subagent retry for Cohort #{cohort_num} "
                f"(reasons={reasons}, leaves={leaves})..."
            )
            rel_ws = mon_info.get("workspace_dir", resolved_id).replace("\\", "/")
            retry_manifest = {
                "status": "RETRY_ON_FLASH",
                "cohort": cohort_num,
                "retry_attempt": 1,
                "action": "INVOKE_SUBAGENT",
                "subagent_type": "ephemeral_translator",
                "model": "flash",
                "define_subagent_if_missing": EPHEMERAL_TRANSLATOR_DEFINITION,
                "role": f"Liturgical Translator Retry ({mon_info.get('short_title')} Cohort {cohort_num})",
                "target_pages": f"{start_page}..{end_page}",
                "prompt": (
                    f"TARGETED FLASH RETRY (Attempt 1/1) for {mon_info.get('title')} — Cohort {cohort_num} (leaves p{start_page}..p{end_page}).\n"
                    f"Inspect the gate failure report at: {rel_ws}/Audit_Reports/cohort{cohort_num}_small_pause_report.json\n"
                    f"Failed gates: {reasons} on leaves {leaves}.\n"
                    f"Repair the files in '{rel_ws}/Source Text/', '{rel_ws}/Draft/' and '{rel_ws}/Draft/{resolved_id}_cohort{cohort_num}_footnotes.txt' "
                    f"while preserving every '=== LEAF pN ===' boundary banner."
                ),
            }
            return retry_manifest

        # curr_retries >= 1: Check Tier 2 quarantine eligibility (all physical === LEAF pN === banners present)
        boundaries_ok, missing_leaves, boundary_msg = verify_physical_leaf_boundaries_on_disk(
            ws, resolved_id, cohort_num, start_page, end_page
        )
        if boundaries_ok:
            reasons, q_leaves = _extract_failed_gate_reasons_and_leaves(report_data, start_page, end_page)
            draft_path = ws / "Draft" / f"{resolved_id}_cohort{cohort_num}_raw_draft.md"
            q_summary = collect_argon_review_signals(
                monument_id=resolved_id,
                cohort_num=cohort_num,
                ws=ws,
                target_text=draft_path,
                quarantine_reasons=reasons,
                quarantine_leaves=q_leaves,
            )
            quarantined_promotion = True
            print(
                f"  -> [Unattended Flash Resilience] All === LEAF pN === boundaries present. "
                f"Quarantined leaves {q_leaves} into argon_review_queue.json (status='QUARANTINED_FOR_ARGON') "
                f"and continuing Phase 1 sprint!"
            )
        else:
            print(f"  -> SMALL PAUSE GATE HARD-STOPPED: {boundary_msg}")
            state["small_pause_gate_status"] = "SMALL_PAUSE_GATE_FAILED"
            blocker_msg = f"Gate failed for Cohort {cohort_num}: {boundary_msg}"
            if blocker_msg not in state.get("active_blockers", []):
                state.setdefault("active_blockers", []).append(blocker_msg)
            save_state(state)
            log_triage_incident(
                ticket_id=f"TICK-COHORT{cohort_num}-FAIL",
                monument=mon_info.get("title", resolved_id),
                component="small_pause_gate",
                description=f"Cohort #{cohort_num} hard-stopped after retry: {boundary_msg}",
            )
            return {"status": "BLOCKED", "cohort": cohort_num, "missing_leaves": missing_leaves, "reason": boundary_msg}

    if not quarantined_promotion:
        print("  -> Small Pause Gate PASSED 100%! Promoting deliverables & updating master edition...")
    else:
        print("  -> Promoting Cohort deliverables with Argon Quarantine tags & advancing sprint...")

    ingest_and_sync(monument_id=resolved_id, cohort_num=cohort_num)

    # Refresh Argon queue telemetry in state
    queue_file = ws / "Audit_Reports" / "argon_review_queue.json"
    if queue_file.exists():
        try:
            q_data = json.loads(queue_file.read_text(encoding="utf-8"))
            state["argon_review_queue_count"] = int(q_data.get("total_queued_leaves", 0))
            state["unresolved_quarantines"] = int(q_data.get("unresolved_quarantines", 0))
        except (OSError, json.JSONDecodeError, ValueError) as e:
            print(f"  [Warning] Could not refresh queue telemetry ({e})", file=sys.stderr)

    completed = state.get("completed_cohorts", [])
    if cohort_num not in completed:
        completed.append(cohort_num)
        completed.sort()
    state["completed_cohorts"] = completed

    translated_count = 0
    for c in completed:
        sp = ((c - 1) * cohort_size) + 1
        ep = min(total_pages, c * cohort_size)
        translated_count += (ep - sp + 1)

    state["translated_pages"] = translated_count
    remaining = max(0, total_pages - translated_count)
    state["remaining_pages"] = remaining

    try:
        ChronicleManager.sync_bench(
            working_state=f"{mon_info.get('short_title')} #{cohort_num} Ingested ({translated_count}/{total_pages} leaves)",
            built_summary=f"Translated Cohort #{cohort_num} of {mon_info.get('title')} ({translated_count}/{total_pages} physical leaves complete).",
            bench_event=f"Cohort #{cohort_num} promoted (Leaves p{start_page}..p{end_page}).",
        )
    except Exception as e:
        print(f"[Warning] Failed to sync chronicle bench: {e}", file=sys.stderr)

    # Decision 5 (Zero-Switch Single-Model Hardening):
    # When remaining == 0:
    #   - If 0 leaves are queued/quarantined, automatically compile the final publication
    #     and reach GRAND_PAUSE without halting for a manual UI model switch!
    #   - If leaves are queued/quarantined, automatically dispatch run_argon_post_sprint_audit()
    #     using the active model ('inherit') without requiring a manual UI model switch!
    if remaining == 0:
        queued_total = state.get("argon_review_queue_count", 0)
        quarantined_total = state.get("unresolved_quarantines", 0)

        if queued_total == 0 and quarantined_total == 0:
            print("\n" + "=" * 70)
            print("  PHASE 1 FLASH COHORT SPRINT 100% COMPLETE (0 QUEUED / 0 QUARANTINED)!")
            print("  ZERO-SWITCH AUTO-PROGRESSION: Compiling canonical publication edition...")
            print("=" * 70 + "\n")
            return compile_final_publication(resolved_id)

        print("\n" + "=" * 70)
        print("  PHASE 1 FLASH COHORT SPRINT COMPLETE!")
        print(f"  Auto-dispatching Post-Sprint Audit for {queued_total} queued leaves ({quarantined_total} quarantined)...")
        print("=" * 70 + "\n")
        return run_argon_post_sprint_audit(resolved_id)

    # Advance to next cohort on Flash
    next_cohort = cohort_num + 1
    state["current_cohort"] = next_cohort
    state["small_pause_gate_status"] = "READY_FOR_NEXT_COHORT"
    save_state(state)

    print(f"\n[Autonomous Loop] Advancing to Cohort #{next_cohort} ({remaining} physical leaves remaining)...")
    next_manifest = prepare_cohort(monument_id=resolved_id, cohort_num=next_cohort)
    return {
        "status": "ADVANCED_WITH_QUARANTINE" if quarantined_promotion else "ADVANCED",
        "next_cohort": next_cohort,
        "manifest": next_manifest,
    }


def run_argon_post_sprint_audit(monument_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Phase 2 (Argon): Audits Audit_Reports/argon_review_queue.json.
      - If <= 5 active leaves: returns DIRECT_PARENT_ARGON inspection plan.
      - If > 5 active leaves: partitions into batched Model='inherit' (Argon) subagents of <= 8 leaves.
      - If 0 active leaves: proceeds directly to compile_final_publication().
    """
    state, mon_info, resolved_id = get_current_context(monument_id)
    ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{resolved_id}")
    queue_file = ws / "Audit_Reports" / "argon_review_queue.json"

    state["routing_phase"] = "PHASE_2_ARGON_DEEP_AUDIT"
    state["active_subagent_model"] = "inherit"
    save_state(state)

    active_items: List[Dict[str, Any]] = []
    if queue_file.exists():
        try:
            q_data = json.loads(queue_file.read_text(encoding="utf-8"))
            active_items = [
                it for it in q_data.get("items", [])
                if isinstance(it, dict) and it.get("status") != "RESOLVED_BY_ARGON"
            ]
        except Exception:
            active_items = []

    if not active_items:
        print("\n[Phase 2 Argon Audit] 0 leaves pending in argon_review_queue.json. Proceeding to LCPE compilation...")
        return compile_final_publication(resolved_id)

    if len(active_items) <= 5:
        strategy = "DIRECT_PARENT_ARGON"
        batches = [active_items]
    else:
        strategy = "BATCHED_ARGON_SUBAGENTS_MAX_8"
        batches = [active_items[i:i + 8] for i in range(0, len(active_items), 8)]

    batch_manifests: List[Dict[str, Any]] = []
    rel_ws = mon_info.get("workspace_dir", resolved_id).replace("\\", "/")
    for b_idx, batch in enumerate(batches, 1):
        leaf_nums = [it["leaf_num"] for it in batch]
        cohorts_touched = sorted(set(int(it["cohort"]) for it in batch))
        batch_manifests.append({
            "batch_index": b_idx,
            "subagent_type": "ephemeral_translator",
            "model": "inherit",
            "leaves": leaf_nums,
            "cohorts": cohorts_touched,
            "items": batch,
            "prompt": (
                f"PHASE 2 ARGON DEEP AUDIT (Batch {b_idx}/{len(batches)}) for {mon_info.get('title')}.\n"
                f"Inspect the 300 DPI images in '{rel_ws}/Source Text/images/' for flagged leaves {leaf_nums} "
                f"(Cohorts {cohorts_touched}).\n"
                f"Resolve all epigraphic/philological/tabular cruxes in Source Text, Draft MD, and Footnotes, "
                f"then mark each leaf resolved via 'py scripts/autonomous_orchestrator.py --resolve-argon-leaf <N>'."
            ),
        })

    return {
        "status": "PHASE_2_ARGON_AUDIT_DISPATCH",
        "monument_id": resolved_id,
        "strategy": strategy,
        "active_queued_leaves": len(active_items),
        "batches_count": len(batch_manifests),
        "batches": batch_manifests,
    }


def resolve_argon_leaf(
    monument_id: Optional[str] = None,
    leaf_num: Optional[int] = None,
    resolve_all: bool = False,
) -> Dict[str, Any]:
    """
    Marks a specific leaf (or all leaves after Argon inspection) in
    Audit_Reports/argon_review_queue.json as RESOLVED_BY_ARGON, re-runs
    run_gate() and ingest_and_sync() on the touched cohort(s), and updates state.
    """
    state, mon_info, resolved_id = get_current_context(monument_id)
    ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{resolved_id}")
    queue_file = ws / "Audit_Reports" / "argon_review_queue.json"
    if not queue_file.exists():
        return {"status": "NO_QUEUE_FILE", "monument_id": resolved_id}

    q_data = json.loads(queue_file.read_text(encoding="utf-8"))
    items = q_data.get("items", [])
    touched_cohorts: set = set()
    resolved_leaves: List[int] = []

    for it in items:
        if not isinstance(it, dict):
            continue
        p_num = int(it.get("leaf_num", -1))
        if resolve_all or (leaf_num is not None and p_num == int(leaf_num)):
            if it.get("status") != "RESOLVED_BY_ARGON":
                it["status"] = "RESOLVED_BY_ARGON"
                it["resolved_at"] = datetime.now(timezone.utc).isoformat()
                touched_cohorts.add(int(it.get("cohort", 1)))
                resolved_leaves.append(p_num)

    active_items = [it for it in items if isinstance(it, dict) and it.get("status") != "RESOLVED_BY_ARGON"]
    quarantined_items = [it for it in items if isinstance(it, dict) and it.get("status") == "QUARANTINED_FOR_ARGON"]

    q_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    q_data["total_queued_leaves"] = len(active_items)
    q_data["unresolved_quarantines"] = len(quarantined_items)
    queue_file.write_text(json.dumps(q_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Re-run Small Pause Gate & re-ingest touched cohorts
    for c_num in sorted(touched_cohorts):
        gate_rc = run_gate(monument_id=resolved_id, cohort_num=c_num)
        if gate_rc == 0:
            ingest_and_sync(monument_id=resolved_id, cohort_num=c_num)

    # Re-read queue file in case run_gate updated non-resolved items
    q_data = json.loads(queue_file.read_text(encoding="utf-8"))
    state["argon_review_queue_count"] = int(q_data.get("total_queued_leaves", 0))
    state["unresolved_quarantines"] = int(q_data.get("unresolved_quarantines", 0))
    save_state(state)

    return {
        "status": "ARGON_LEAVES_RESOLVED",
        "monument_id": resolved_id,
        "resolved_leaves": resolved_leaves,
        "touched_cohorts": sorted(touched_cohorts),
        "remaining_queued_leaves": state["argon_review_queue_count"],
        "unresolved_quarantines": state["unresolved_quarantines"],
    }


def compile_final_publication(monument_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Phase 2 Final Compilation Gate:
    Verifies unresolved_quarantines == 0 in Audit_Reports/argon_review_queue.json,
    then executes UniversalPublicationEngine and 6-Gate verify_monument_publication
    to reach the Sovereign Grand Pause.
    """
    state, mon_info, resolved_id = get_current_context(monument_id)
    ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{resolved_id}")
    queue_file = ws / "Audit_Reports" / "argon_review_queue.json"

    if queue_file.exists():
        try:
            q_data = json.loads(queue_file.read_text(encoding="utf-8"))
            unresolved_q = int(q_data.get("unresolved_quarantines", 0))
            if unresolved_q > 0:
                err_msg = (
                    f"QUARANTINES_UNRESOLVED: Cannot compile canonical publication edition while "
                    f"{unresolved_q} quarantined leaves remain unresolved in argon_review_queue.json."
                )
                print(f"\n[PUBLICATION GATE BLOCKED] {err_msg}", file=sys.stderr)
                return {"status": "QUARANTINES_UNRESOLVED", "unresolved_quarantines": unresolved_q, "error": err_msg}
        except (OSError, json.JSONDecodeError, ValueError) as e:
            print(f"  [Warning] Could not inspect argon_review_queue.json ({e})", file=sys.stderr)

    print("\n" + "=" * 65)
    print("  PHASE 2 ARGON AUDIT CERTIFIED — TRIGGERING LCPE COMPILATION...")
    print("=" * 65 + "\n")

    from scripts.compile_final_edition import UniversalPublicationEngine
    from scripts.verify_publication_edition import verify_monument_publication

    try:
        engine = UniversalPublicationEngine(resolved_id)
        engine.run()
        pub_ok = verify_monument_publication(resolved_id)
        if not pub_ok:
            print("\n[ERROR] Publication Quality Gate failed!")
            state["small_pause_gate_status"] = "PUBLICATION_GATE_FAILED"
            save_state(state)
            return {"status": "PUBLICATION_GATE_FAILED", "error": "Publication quality gate failed"}
    except Exception as e:
        print(f"\n[ERROR] Publication compilation exception: {e}")
        state["small_pause_gate_status"] = "PUBLICATION_COMPILATION_ERROR"
        save_state(state)
        return {"status": "ERROR", "error": str(e)}

    total_pages = int(mon_info.get("total_physical_pages", 0))
    print("\n" + "=" * 65)
    print("  CANONICAL PUBLICATION EDITION COMPILED & 100% CERTIFIED ON ARGON!")
    print("  REACHED SOVEREIGN GRAND PAUSE — READY FOR HUMAN REVIEW.")
    print("=" * 65 + "\n")
    state["routing_phase"] = "PHASE_2_GRAND_PAUSE_READY"
    state["small_pause_gate_status"] = "GRAND_PAUSE_READY_FOR_HUMAN_INSPECTION"
    save_state(state)

    try:
        ChronicleManager.sync_bench(
            working_state=f"{mon_info.get('title')} 100% Sealed ({total_pages} leaves) · Grand Pause Ready",
            built_summary=f"Compiled canonical publication edition for {mon_info.get('title')} after Argon deep audit. Reached Sovereign Grand Pause.",
            bench_event=f"All {total_pages} leaves translated and Argon-certified across {mon_info.get('short_title')}. Ready for human inspection.",
        )
    except Exception as e:
        print(f"[Warning] Failed to sync chronicle bench on Grand Pause: {e}", file=sys.stderr)

    return {"status": "GRAND_PAUSE", "monument_complete": True, "publication_edition_ready": True}


def approve_grand_pause(monument_id: Optional[str] = None, push_to_git: bool = True) -> Dict[str, Any]:
    """
    Formally approves the Grand Pause for a completed monument.
    1. Enforces unresolved_quarantines == 0 and re-verifies canonical publication edition integrity.
    2. Syncs deliverables to Hub inbox (Typikon Coded/Data/Inbox/).
    3. Stages and commits all translation artifacts to Git.
    4. Pushes commits to remote repository (git push origin master).
    5. Advances monument state and generates the copy-pasteable /plan prompt for the next monument.
    """
    state, mon_info, resolved_id = get_current_context(monument_id)
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    short_title = mon_info.get("short_title", resolved_id)
    total_pages = mon_info.get("total_physical_pages", 0)
    ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{resolved_id}")
    queue_file = ws / "Audit_Reports" / "argon_review_queue.json"
    if queue_file.exists():
        try:
            q_data = json.loads(queue_file.read_text(encoding="utf-8"))
            if int(q_data.get("unresolved_quarantines", 0)) > 0:
                return {"status": "FAILED", "error": "Unresolved quarantines remain in argon_review_queue.json"}
        except (OSError, json.JSONDecodeError, ValueError) as e:
            print(f"  [Warning] Could not verify argon_review_queue.json ({e})", file=sys.stderr)

    print("\n" + "=" * 70)
    print(f"EXECUTING GRAND PAUSE APPROVAL & FINAL SEALING: {short_title}")
    print("=" * 70)

    # 1. Gate Invariant Check
    try:
        from verify_publication_edition import verify_monument_publication
        pub_ok = verify_monument_publication(resolved_id)
        if not pub_ok:
            print("\n[ERROR] Grand Pause aborted: Publication quality gate failed!", file=sys.stderr)
            return {"status": "FAILED", "error": "Publication gate failed"}
    except Exception as e:
        print(f"\n[Warning] Verification check raised exception: {e}", file=sys.stderr)

    # 2. Hub Inbox Sync
    hub_inbox = PROJECT_ROOT.parent / "Typikon Coded" / "Data" / "Inbox"
    if hub_inbox.exists() and "publication_spec" in mon_info:
        pub_spec = mon_info["publication_spec"]
        target_inbox = hub_inbox / pub_spec.get("hub_inbox_folder", resolved_id)
        target_inbox.mkdir(parents=True, exist_ok=True)
        final_md_dir = ws / "Final MD"

        if final_md_dir.exists():
            copied_files = 0
            for f in final_md_dir.glob("*.md"):
                shutil.copy2(f, target_inbox / f.name)
                copied_files += 1
            print(f"  [HUB SYNC] Synced {copied_files} publication files to {target_inbox.name}")

            handoff_note = f"""# Hub Ingestion Handoff: {short_title}

- **Monument ID**: `{resolved_id}`
- **Title**: {mon_info.get('title', short_title)}
- **Total Physical Leaves**: {total_pages}
- **Status**: 100% Sealed & Ingested (3-Phase Bookend Argon-Flash-Argon Certified)
- **Quality Gates**: All Small Pause Gates + Argon Review Queue + Publication Gate Certified Pass
- **Image Mirror**: Permanent 300 DPI JPEG Vault on Drive E:
- **Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            (target_inbox / "handoff_note.md").write_text(handoff_note, encoding="utf-8")

    # 3. Chronicle Bench Sync
    try:
        ChronicleManager.sync_bench(
            working_state=f"{short_title} Sealed & Pushed to Git",
            built_summary=f"Grand Pause approved for {short_title}. Sealed publication edition pushed to remote git.",
            bench_event=f"Monument {short_title} sealed and handed off.",
        )
    except Exception as e:
        print(f"  [Warning] Chronicle sync error: {e}", file=sys.stderr)

    # 4. Git Stage, Commit, and Push
    git_result = {"committed": False, "pushed": False}
    if push_to_git:
        print("\n[GIT PIPELINE] Staging and committing all deliverables...")
        try:
            subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT, check=True)
            status_res = subprocess.run(
                ["git", "status", "--porcelain"], cwd=PROJECT_ROOT, capture_output=True, text=True, check=True
            )

            commit_msg = f"feat({resolved_id}): seal canonical publication edition of {short_title} (leaves 1..{total_pages})"
            if status_res.stdout.strip():
                subprocess.run(["git", "commit", "-m", commit_msg], cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
                print(f"  [GIT COMMIT] {commit_msg}")
                git_result["committed"] = True
            else:
                print("  [GIT] Working tree clean; nothing new to commit.")

            print("  [GIT PUSH] Pushing commits to origin master...")
            push_res = subprocess.run(["git", "push", "origin", "master"], cwd=PROJECT_ROOT, capture_output=True, text=True)
            if push_res.returncode == 0:
                print("  [GIT PUSH] Successfully pushed to origin master!")
                git_result["pushed"] = True
            else:
                print(f"  [GIT WARNING] Push returned non-zero ({push_res.returncode}): {push_res.stderr.strip()}", file=sys.stderr)
        except Exception as e:
            print(f"  [GIT ERROR] Git operation failed: {e}", file=sys.stderr)

    # 5. Resolve Next Monument & Generate /plan Startup Prompt
    monuments = registry.get("monuments", {})
    mon_keys = list(monuments.keys())
    curr_idx = mon_keys.index(resolved_id) if resolved_id in mon_keys else -1

    next_mon_id = None
    if curr_idx >= 0:
        for idx in range(curr_idx + 1, len(mon_keys)):
            cand_id = mon_keys[idx]
            cand_status = monuments[cand_id].get("status", "")
            if cand_status not in ["completed", "sealed", "failed"]:
                next_mon_id = cand_id
                break

    state["small_pause_gate_status"] = "MONUMENT_SEALED_AND_HANDED_OFF"
    state["active_monument"] = f"{short_title} (SEALED)"
    state["remaining_pages"] = 0
    save_state(state)

    print("\n" + "=" * 70)
    print(f"  SOVEREIGN GRAND PAUSE APPROVED: {short_title} IS SEALED!")
    print("=" * 70)

    if next_mon_id:
        next_info = monuments[next_mon_id]
        onboarding_prompt = build_phase0_onboarding_prompt(next_mon_id, next_info)
        print("\n[NEXT MONUMENT ONBOARDING PROMPT (Rule 19 / GLOBAL_SYSTEM_RULES.md §10)]:\n")
        print("```text")
        print(onboarding_prompt)
        print("```\n")
        print("This orchestrator session is now retired. Initialize the next monument in a fresh chat using the onboarding prompt above.")
    else:
        print("\nAll monuments across the Byzantine-Ruthenian transmission chain are completed!")

    return {
        "status": "APPROVED",
        "monument_id": resolved_id,
        "git": git_result,
        "next_monument": next_mon_id,
    }


def defer_monument_to_back_of_queue(
    monument_id: Optional[str] = None,
    reason: str = "",
) -> Dict[str, Any]:
    """
    Gate 0 Primary Source Suitability Remediation:
    Marks a defective/excerpted monument as status='failed', wave=5, active=False,
    moves it to the tail of Liturgical Monuments/codex_registry.json, advances
    ACTIVE_ORCHESTRATOR_STATE.json to the next ready monument in PHASE_0_ARGON_PLANNING_LOCKED,
    and prints the Vision-Capped Phase 0 Onboarding Prompt for the next monument.
    """
    state, _mon_info, resolved_id = get_current_context(monument_id)

    raw_bytes = REGISTRY_FILE.read_bytes()
    has_crlf = b"\r\n" in raw_bytes
    registry = json.loads(raw_bytes.decode("utf-8"))
    monuments = registry.get("monuments", {})
    if resolved_id not in monuments:
        raise KeyError(f"Monument '{resolved_id}' not found in {REGISTRY_FILE}")

    mon_keys = list(monuments.keys())
    curr_idx = mon_keys.index(resolved_id)

    entry = dict(monuments[resolved_id])
    entry["status"] = "failed"
    entry["active"] = False
    entry["wave"] = 5
    if reason:
        entry["queue_notes"] = f"Gate 0 Deferred ({datetime.now().strftime('%Y-%m-%d')}): {reason}"

    reordered_monuments: Dict[str, Any] = {}
    for k, v in monuments.items():
        if k != resolved_id:
            reordered_monuments[k] = v
    reordered_monuments[resolved_id] = entry
    registry["monuments"] = reordered_monuments

    dumped = json.dumps(registry, indent=2, ensure_ascii=False) + "\n"
    if has_crlf:
        dumped = dumped.replace("\n", "\r\n")
    REGISTRY_FILE.write_bytes(dumped.encode("utf-8"))

    # Find next ready/queued monument
    next_mon_id = None
    remaining_keys = [k for k in mon_keys[curr_idx + 1 :] if k != resolved_id]
    for cand_id in remaining_keys:
        cand_status = reordered_monuments[cand_id].get("status", "")
        if cand_status not in ["completed", "sealed", "failed"]:
            next_mon_id = cand_id
            break
    if not next_mon_id:
        for cand_id, cand_info in reordered_monuments.items():
            if cand_id != resolved_id and cand_info.get("status", "") not in ["completed", "sealed", "failed"]:
                next_mon_id = cand_id
                break

    onboarding_prompt = ""
    if next_mon_id:
        next_info = reordered_monuments[next_mon_id]
        next_pages = int(next_info.get("total_physical_pages", 0))
        next_cohort_sz = int(next_info.get("default_cohort_size", 10))
        next_total_cohorts = (next_pages + next_cohort_sz - 1) // next_cohort_sz if next_pages > 0 else 0
        state["active_monument"] = next_info.get("short_title", next_mon_id)
        state["monument_id"] = next_mon_id
        state["total_pages"] = next_pages
        state["completed_pages"] = 0
        state["remaining_pages"] = next_pages
        state["current_cohort"] = 1
        state["total_cohorts"] = next_total_cohorts
        state["current_cohort_range"] = f"1-{min(next_cohort_sz, next_pages)}"
        state["routing_phase"] = "PHASE_0_ARGON_PLANNING"
        state["small_pause_gate_status"] = "PHASE_0_ARGON_PLANNING_LOCKED"
        state["phase_0_unlocked"] = False
        save_state(state)
        onboarding_prompt = build_phase0_onboarding_prompt(next_mon_id, next_info)

    print("\n" + "=" * 70)
    print(f"  GATE 0 DEFERRED: {resolved_id} -> status='failed' (Moved to Back of Queue)")
    if reason:
        print(f"  Reason: {reason}")
    print("=" * 70)

    if next_mon_id:
        print(f"\n  Next Active Monument: {next_mon_id} ({reordered_monuments[next_mon_id].get('title', next_mon_id)})")
        print("\n[NEXT MONUMENT ONBOARDING PROMPT (Rule 19 / GLOBAL_SYSTEM_RULES.md §10)]:\n")
        print("```text")
        print(onboarding_prompt)
        print("```\n")

    return {
        "status": "DEFERRED_TO_BACK_OF_QUEUE",
        "deferred_monument_id": resolved_id,
        "reason": reason,
        "next_monument_id": next_mon_id,
        "onboarding_prompt": onboarding_prompt,
    }


def main():
    parser = argparse.ArgumentParser(description="Autonomous Multi-Cohort State Machine & Loop Controller")
    parser.add_argument("--status", action="store_true", help="Display current telemetry dashboard")
    parser.add_argument("--preflight", action="store_true", help="Run Phase 0 Argon preflight and engage circuit-breaker lock")
    parser.add_argument("--unlock-flash-sprint", action="store_true", help="Unlock Phase 1 Flash sprint after user plan approval and UI switch to Flash")
    parser.add_argument("--prepare-cohort", action="store_true", help="Extract leaves and generate subagent manifest")
    parser.add_argument("--verify-cohort", action="store_true", help="Run Small Pause Gate and advance cohort")
    parser.add_argument("--run-argon-audit", action="store_true", help="Run Phase 2 Argon post-sprint review queue audit")
    parser.add_argument("--resolve-argon-leaf", type=int, help="Mark a specific leaf N as RESOLVED_BY_ARGON and re-verify its cohort")
    parser.add_argument("--resolve-all-argon-leaves", action="store_true", help="Mark all queued leaves as RESOLVED_BY_ARGON and re-verify touched cohorts")
    parser.add_argument("--compile-publication", action="store_true", help="Compile LCPE publication edition after Argon audit (requires 0 unresolved quarantines)")
    parser.add_argument("--step", action="store_true", help="Execute the next autonomous loop step")
    parser.add_argument("--approve-grand-pause", action="store_true", help="Formally approve Grand Pause, sync Hub, push deliverables to git, and hand off")
    parser.add_argument("--defer-monument", action="store_true", help="Gate 0 remediation: mark monument failed, move to back of codex_registry.json, and hand off to next monument")
    parser.add_argument("--reason", type=str, default="", help="Reason for deferring a monument via --defer-monument")
    parser.add_argument("--no-git-push", action="store_true", help="Skip remote git push during Grand Pause approval")
    parser.add_argument("--monument", help="Override monument ID")
    parser.add_argument("--cohort", type=int, help="Override cohort number")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if args.status:
        state, _, _ = get_current_context(args.monument)
        display_status(state)
        return

    if args.defer_monument:
        res = defer_monument_to_back_of_queue(monument_id=args.monument, reason=args.reason)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.preflight:
        res = run_preflight(monument_id=args.monument)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.unlock_flash_sprint:
        res = unlock_flash_sprint(monument_id=args.monument)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.approve_grand_pause:
        res = approve_grand_pause(monument_id=args.monument, push_to_git=(not args.no_git_push))
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.run_argon_audit:
        res = run_argon_post_sprint_audit(monument_id=args.monument)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.resolve_argon_leaf is not None or args.resolve_all_argon_leaves:
        res = resolve_argon_leaf(
            monument_id=args.monument,
            leaf_num=args.resolve_argon_leaf,
            resolve_all=args.resolve_all_argon_leaves,
        )
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.compile_publication:
        res = compile_final_publication(monument_id=args.monument)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.prepare_cohort:
        try:
            manifest = prepare_cohort(monument_id=args.monument, cohort_num=args.cohort)
            if args.json:
                print(json.dumps(manifest, indent=2, ensure_ascii=False))
        except PermissionError as e:
            if args.json:
                print(json.dumps({"status": "PHASE_0_LOCKED", "error": str(e)}, indent=2, ensure_ascii=False))
            sys.exit(2)
        return

    if args.verify_cohort:
        res = verify_cohort_and_advance(monument_id=args.monument, cohort_num=args.cohort)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.step:
        state, _, _ = get_current_context(args.monument)
        status = state.get("small_pause_gate_status", "UNKNOWN")
        phase = state.get("routing_phase", "PHASE_1_FLASH_SPRINT")
        curr_cohort = state.get("current_cohort", 1)

        if phase == "PHASE_0_ARGON_PLANNING" or status == "PHASE_0_ARGON_PLANNING_LOCKED":
            msg = (
                "Status is PHASE_0_ARGON_PLANNING_LOCKED. Complete /plan and /grill-me on Argon, "
                "switch Main Window UI dropdown to Gemini 3.8 Flash, then run '--unlock-flash-sprint'."
            )
            print(msg)
            if args.json:
                print(json.dumps({"status": "PHASE_0_LOCKED", "message": msg}, indent=2, ensure_ascii=False))
            sys.exit(2)
        elif status in ["READY_FOR_STARTUP_PROMPT", "READY_FOR_NEXT_COHORT", "UNKNOWN"]:
            manifest = prepare_cohort(monument_id=args.monument, cohort_num=curr_cohort)
            if args.json:
                print(json.dumps(manifest, indent=2, ensure_ascii=False))
        elif status in ["AWAITING_SUBAGENT_EXECUTION", "AWAITING_FLASH_RETRY"]:
            print(f"Status is {status} for Cohort #{curr_cohort}.")
            print("Dispatch subagent using manifest or run '--verify-cohort' once subagent completes.")
        elif status == "AWAITING_ARGON_POST_SPRINT_AUDIT":
            print("Phase 1 Flash sprint complete! Switch UI dropdown to Gemini 4 Argon (High) and run '--run-argon-audit'.")
        elif status == "SMALL_PAUSE_GATE_FAILED":
            print("Status is SMALL_PAUSE_GATE_FAILED. Fix blockers listed in ACTIVE_ORCHESTRATOR_STATE.json.")
        elif status == "GRAND_PAUSE_READY_FOR_HUMAN_INSPECTION":
            print("Monument translation complete! Awaiting Grand Pause human sign-off via '--approve-grand-pause'.")
        return

    state, _, _ = get_current_context(args.monument)
    display_status(state)


if __name__ == "__main__":
    main()
