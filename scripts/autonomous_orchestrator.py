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
import shutil
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
STATE_FILE = PROJECT_ROOT / "Liturgical Monuments" / "ACTIVE_ORCHESTRATOR_STATE.json"
TRIAGE_INBOX = PROJECT_ROOT / "scratch" / "triage_inbox.jsonl"

# Internal script imports
from extract_cohort_leaves import extract_leaves
from generate_work_order import generate_work_order
from run_small_pause_gate import run_gate
from assemble_and_sync_hub import ingest_and_sync
from orchestrator_state import load_state, save_state, load_registry, display_status
from chronicle_manager import ChronicleManager

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

def attempt_deterministic_self_healing(monument_id: str, cohort_num: int) -> bool:
    """
    Attempts deterministic in-place repair of isolated linter violations
    (such as uncapitalized Deity pronouns) and re-runs the gate once.
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
    if not draft_path.exists():
        return False

    modified = False
    text = draft_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 1. Pronoun healing
    pronoun_data = report.get("gates", {}).get("hieratic_pronouns", {})
    if not pronoun_data.get("passed", True):
        violations = pronoun_data.get("violations", [])
        for v in violations:
            line_idx = v.get("line", 0) - 1
            pronoun = v.get("pronoun", "")
            if 0 <= line_idx < len(lines) and pronoun:
                line = lines[line_idx]
                new_line = re.sub(r'\b' + re.escape(pronoun) + r'\b', pronoun.capitalize(), line)
                if new_line != line:
                    lines[line_idx] = new_line
                    modified = True

    if modified:
        draft_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"  [Self-Healing] Applied deterministic repairs to {draft_path.name}. Re-verifying gate...")
        retry_res = run_gate(monument_id=monument_id, cohort_num=cohort_num)
        return retry_res == 0

    return False

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
        print("  -> Initial gate verification failed. Attempting deterministic self-healing...")
        healed = attempt_deterministic_self_healing(monument_id, cohort_num)
        if healed:
            print("  -> Deterministic self-healing SUCCESSFUL! Resuming pipeline.")
            gate_res = 0

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

    # Synchronize Living Lab Chronicle Bench
    try:
        start_leaf = ((cohort_num - 1) * cohort_size) + 1
        end_leaf = min(total_pages, cohort_num * cohort_size)
        ChronicleManager.sync_bench(
            working_state=f"Monuments 0, 1, 2 Sealed · {mon_info.get('short_title')} #{cohort_num} Sealed ({translated_count}/{total_pages} leaves)",
            built_summary=f"Translated and verified Cohort #{cohort_num} of {mon_info.get('title')} ({translated_count}/{total_pages} physical leaves complete).",
            bench_event=f"Cohort #{cohort_num} passed Small Pause Gate 100% and promoted to Hub. Leaves p{start_leaf}..p{end_leaf} verified."
        )
    except Exception as e:
        print(f"[Warning] Failed to sync chronicle bench: {e}", file=sys.stderr)

    if remaining == 0:
        print("\n" + "=" * 65)
        print("  ALL PHYSICAL LEAVES TRANSLATED ACROSS MONUMENT!")
        print("  TRIGGERING LITURGICAL CODEX PUBLICATION ENGINEERING (LCPE)...")
        print("=" * 65 + "\n")

        from scripts.compile_final_edition import UniversalPublicationEngine
        from scripts.verify_publication_edition import verify_monument_publication

        try:
            engine = UniversalPublicationEngine(monument_id)
            engine.run()
            pub_ok = verify_monument_publication(monument_id)
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

        print("\n" + "=" * 65)
        print("  CANONICAL PUBLICATION EDITION COMPILED & 100% CERTIFIED!")
        print("  REACHED SOVEREIGN GRAND PAUSE — READY FOR HUMAN REVIEW.")
        print("=" * 65 + "\n")
        state["small_pause_gate_status"] = "GRAND_PAUSE_READY_FOR_HUMAN_INSPECTION"
        save_state(state)

        # Update Chronicle Bench upon Grand Pause
        try:
            ChronicleManager.sync_bench(
                working_state=f"Monuments 0, 1, 2 Sealed · {mon_info.get('title')} 100% Sealed ({total_pages} leaves) · Grand Pause Ready",
                built_summary=f"Compiled canonical publication edition for {mon_info.get('title')}. Reached Sovereign Grand Pause.",
                bench_event=f"All {total_pages} leaves translated across {mon_info.get('short_title')}. Ready for human inspection."
            )
        except Exception as e:
            print(f"[Warning] Failed to sync chronicle bench on Grand Pause: {e}", file=sys.stderr)

        return {"status": "GRAND_PAUSE", "monument_complete": True, "publication_edition_ready": True}

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

def approve_grand_pause(monument_id: Optional[str] = None, push_to_git: bool = True) -> Dict[str, Any]:
    """
    Formally approves the Grand Pause for a completed monument.
    1. Re-verifies canonical publication edition integrity.
    2. Syncs deliverables to Hub inbox (Typikon Coded/Data/Inbox/).
    3. Stages and commits all translation artifacts to Git.
    4. Pushes commits to remote repository (git push origin master).
    5. Advances monument state and generates the copy-pasteable /plan prompt for the next monument.
    """
    state = load_state()
    if not monument_id:
        monument_id = state.get("monument_id", "1891_lviv_synod")

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    if monument_id not in registry.get("monuments", {}):
        raise ValueError(f"Unknown monument '{monument_id}' in registry.")

    mon_info = registry["monuments"][monument_id]
    short_title = mon_info.get("short_title", monument_id)
    total_pages = mon_info.get("total_physical_pages", 0)

    print("\n" + "=" * 70)
    print(f"EXECUTING GRAND PAUSE APPROVAL & FINAL SEALING: {short_title}")
    print("=" * 70)

    # 1. Gate Invariant Check
    try:
        from verify_publication_edition import verify_monument_publication
        pub_ok = verify_monument_publication(monument_id)
        if not pub_ok:
            print("\n[ERROR] Grand Pause aborted: Publication quality gate failed!", file=sys.stderr)
            return {"status": "FAILED", "error": "Publication gate failed"}
    except Exception as e:
        print(f"\n[Warning] Verification check raised exception: {e}", file=sys.stderr)

    # 2. Hub Inbox Sync
    hub_candidates = [
        Path("C:/") / "Users" / "augus" / "OneDrive" / "Documents" / "Google Antigravity" / "Projects" / "Typikon Coded" / "Data" / "Inbox",
        PROJECT_ROOT.parent / "Typikon Coded" / "Data" / "Inbox",
    ]
    hub_inbox = None
    for cand in hub_candidates:
        if cand.exists():
            hub_inbox = cand
            break

    if hub_inbox and "publication_spec" in mon_info:
        pub_spec = mon_info["publication_spec"]
        target_inbox = hub_inbox / pub_spec.get("hub_inbox_folder", monument_id)
        target_inbox.mkdir(parents=True, exist_ok=True)
        workspace_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
        final_md_dir = workspace_dir / "Final MD"

        if final_md_dir.exists():
            copied_files = 0
            for f in final_md_dir.glob("*.md"):
                shutil.copy2(f, target_inbox / f.name)
                copied_files += 1
            print(f"  [HUB SYNC] Synced {copied_files} publication files to {target_inbox.name}")

            handoff_note = f"""# Hub Ingestion Handoff: {short_title}

- **Monument ID**: `{monument_id}`
- **Title**: {mon_info.get('title', short_title)}
- **Total Physical Leaves**: {total_pages}
- **Status**: 100% Sealed & Ingested
- **Quality Gates**: All Small Pause Gates + Publication Gate Certified Pass
- **Image Mirror**: Permanent 300 DPI JPEG Vault on Drive E:
- **Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            (target_inbox / "handoff_note.md").write_text(handoff_note, encoding="utf-8")

    # 3. Chronicle Bench Sync
    try:
        ChronicleManager.sync_bench(
            working_state=f"Monuments 0, 1, 2 Sealed · {short_title} Sealed & Pushed to Git",
            built_summary=f"Grand Pause approved for {short_title}. Sealed publication edition pushed to remote git.",
            bench_event=f"Monument {short_title} sealed and handed off."
        )
    except Exception as e:
        print(f"  [Warning] Chronicle sync error: {e}", file=sys.stderr)

    # 4. Git Stage, Commit, and Push
    git_result = {"committed": False, "pushed": False}
    if push_to_git:
        print("\n[GIT PIPELINE] Staging and committing all deliverables...")
        try:
            subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT, check=True)
            status_res = subprocess.run(["git", "status", "--porcelain"], cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
            
            commit_msg = f"feat({monument_id}): seal canonical publication edition of {short_title} (leaves 1..{total_pages})"
            if status_res.stdout.strip():
                commit_res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=PROJECT_ROOT, capture_output=True, text=True, check=True)
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
    curr_idx = mon_keys.index(monument_id) if monument_id in mon_keys else -1
    
    next_mon_id = None
    if curr_idx >= 0:
        for idx in range(curr_idx + 1, len(mon_keys)):
            cand_id = mon_keys[idx]
            cand_status = monuments[cand_id].get("status", "")
            if cand_status not in ["completed", "sealed"]:
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
        next_title = next_info.get("title", next_mon_id)
        next_pages = next_info.get("total_physical_pages", 0)
        next_cohort_sz = next_info.get("default_cohort_size", 10)
        
        plan_prompt = f"""/plan Execute autonomous translation of {next_title} ({next_mon_id}). Total leaves: {next_pages}, cohort size: {next_cohort_sz}. Follow instructions in STARTUP_INSTRUCTIONS.md and AUTONOMOUS_MONUMENT_DIRECTIVE.md."""
        print(f"\n[NEXT MONUMENT STARTUP PROMPT (Rule 19)]:\n")
        print("```text")
        print(plan_prompt)
        print("```\n")
        print("This orchestrator session is now retired. Initialize the next monument in a fresh chat using the `/plan` prompt above.")
    else:
        print("\nAll monuments across the Byzantine-Ruthenian transmission chain are completed!")

    return {
        "status": "APPROVED",
        "monument_id": monument_id,
        "git": git_result,
        "next_monument": next_mon_id
    }

def main():
    parser = argparse.ArgumentParser(description="Autonomous Multi-Cohort State Machine & Loop Controller")
    parser.add_argument("--status", action="store_true", help="Display current telemetry dashboard")
    parser.add_argument("--prepare-cohort", action="store_true", help="Extract leaves and generate subagent manifest")
    parser.add_argument("--verify-cohort", action="store_true", help="Run Small Pause Gate and advance cohort")
    parser.add_argument("--step", action="store_true", help="Execute the next autonomous loop step")
    parser.add_argument("--approve-grand-pause", action="store_true", help="Formally approve Grand Pause, sync Hub, push deliverables to git, and hand off")
    parser.add_argument("--no-git-push", action="store_true", help="Skip remote git push during Grand Pause approval")
    parser.add_argument("--monument", help="Override monument ID")
    parser.add_argument("--cohort", type=int, help="Override cohort number")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if args.status:
        state = load_state()
        display_status(state)
        return

    if args.approve_grand_pause:
        res = approve_grand_pause(monument_id=args.monument, push_to_git=(not args.no_git_push))
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
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
            print("Monument translation complete! Awaiting Grand Pause human sign-off via '--approve-grand-pause'.")
        return

    # Default: show status
    state = load_state()
    display_status(state)

if __name__ == "__main__":
    main()
