"""
Unit and Integration Tests for Multi-Monument Sequestered Concurrency Hardening.
Verifies strict disambiguation, active lease lifecycle (claim/pause/resume/defer),
interleaved multi-monument cohort progression, atomic registry updates, and
multi-monument Chronicle formatting inside an isolated tmp_path sandbox.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import autonomous_orchestrator as ao
import chronicle_manager as cm
import concurrency_lock as cl
import orchestrator_state as os_mod


def _setup_sandbox(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Dict[str, Any]:
    """
    Configures a completely isolated multi-monument sandbox in tmp_path so no
    production files in Liturgical Monuments/ or project root are ever touched.
    """
    lock_dir = tmp_path / "scratch" / ".locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(cl, "LOCKS_DIR", lock_dir)

    reg_path = tmp_path / "codex_registry.json"
    monkeypatch.setattr(cl, "DEFAULT_REGISTRY_FILE", reg_path)
    state_mirror_path = tmp_path / "ACTIVE_ORCHESTRATOR_STATE.json"
    triage_path = tmp_path / "scratch" / "triage_inbox.jsonl"

    ws_a = tmp_path / "Liturgical Monuments" / "Mon_A"
    ws_b = tmp_path / "Liturgical Monuments" / "Mon_B"
    ws_c = tmp_path / "Liturgical Monuments" / "Mon_C"

    for ws in (ws_a, ws_b, ws_c):
        (ws / "Source Text").mkdir(parents=True, exist_ok=True)
        (ws / "Draft").mkdir(parents=True, exist_ok=True)
        (ws / "Final MD").mkdir(parents=True, exist_ok=True)
        (ws / "Work_Orders").mkdir(parents=True, exist_ok=True)
        (ws / "Audit_Reports").mkdir(parents=True, exist_ok=True)

    tpl_dir = tmp_path / "data" / "templates"
    tpl_dir.mkdir(parents=True, exist_ok=True)
    (tpl_dir / "phase0_onboarding_prompt_template.md").write_text(
        "Orient on and prepare the Phase 0 implementation plan for {title} ({monument_id}).\n",
        encoding="utf-8",
    )

    registry_data: Dict[str, Any] = {
        "monuments": {
            "mon_a": {
                "monument_id": "mon_a",
                "title": "Monument Alpha (1700)",
                "short_title": "1700 Alpha",
                "total_physical_pages": 20,
                "default_cohort_size": 10,
                "genre_register": "rubrical",
                "workspace_dir": str(ws_a),
                "active": False,
                "status": "ready",
                "wave": 1,
                "publication_spec": {
                    "hub_inbox_folder": "1700_Alpha",
                    "master_title": "Monument Alpha (1700)",
                    "parts": [{"id": "part0", "filename": "mon_a_part0.md", "title": "Intro", "start_landmark": None}],
                    "footnotes_filename": "mon_a_footnotes.md",
                },
            },
            "mon_b": {
                "monument_id": "mon_b",
                "title": "Monument Beta (1750)",
                "short_title": "1750 Beta",
                "total_physical_pages": 30,
                "default_cohort_size": 10,
                "genre_register": "hymnographic",
                "workspace_dir": str(ws_b),
                "active": False,
                "status": "ready",
                "wave": 1,
                "publication_spec": {
                    "hub_inbox_folder": "1750_Beta",
                    "master_title": "Monument Beta (1750)",
                    "parts": [{"id": "part0", "filename": "mon_b_part0.md", "title": "Intro", "start_landmark": None}],
                    "footnotes_filename": "mon_b_footnotes.md",
                },
            },
            "mon_c": {
                "monument_id": "mon_c",
                "title": "Monument Gamma (1800)",
                "short_title": "1800 Gamma",
                "total_physical_pages": 40,
                "default_cohort_size": 10,
                "genre_register": "scholarly_critical",
                "workspace_dir": str(ws_c),
                "active": False,
                "status": "ready",
                "wave": 2,
                "publication_spec": {
                    "hub_inbox_folder": "1800_Gamma",
                    "master_title": "Monument Gamma (1800)",
                    "parts": [{"id": "part0", "filename": "mon_c_part0.md", "title": "Intro", "start_landmark": None}],
                    "footnotes_filename": "mon_c_footnotes.md",
                },
            },
        }
    }
    reg_path.write_text(json.dumps(registry_data, indent=2), encoding="utf-8")

    monkeypatch.setattr(os_mod, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(os_mod, "REGISTRY_FILE", reg_path)
    monkeypatch.setattr(os_mod, "STATE_FILE", state_mirror_path)
    monkeypatch.setattr(os_mod, "load_registry", lambda: json.loads(reg_path.read_text(encoding="utf-8")))

    monkeypatch.setattr(ao, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(ao, "REGISTRY_FILE", reg_path)
    monkeypatch.setattr(ao, "TRIAGE_INBOX", triage_path)
    monkeypatch.setattr(ao, "load_registry", lambda: json.loads(reg_path.read_text(encoding="utf-8")))
    monkeypatch.delenv("ACTIVE_MONUMENT_ID", raising=False)

    chronicle_file = tmp_path / "CHRONICLE.md"
    chronicle_file.write_text(
        "# CHRONICLE\n\n"
        "## Today’s Lab Bench (The Present Horizon)\n"
        "**Current Date:** October 27, 2026 · **Active Commit:** `0000000`  \n"
        "**Working State:** Idle\n\n"
        "* **What Was Just Built:** Init.\n"
        "* **What Just Happened on the Bench:** Init.\n\n"
        "---\n\n"
        "## Ledger of Intent\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(cm, "CHRONICLE_PATH", chronicle_file)
    monkeypatch.setattr(cm.ChronicleManager, "CHRONICLE_PATH", chronicle_file)

    return {
        "reg_path": reg_path,
        "state_mirror_path": state_mirror_path,
        "chronicle_file": chronicle_file,
        "ws_a": ws_a,
        "ws_b": ws_b,
        "ws_c": ws_c,
    }


def test_strict_disambiguation_blocks_ambiguous_calls(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """
    Verifies that:
    1. When 1 monument holds active_lease=True, resolve_monument_id(None) auto-resolves it.
    2. When >=2 monuments hold active_lease=True, resolve_monument_id(None) raises RuntimeError
       with '[DISAMBIGUATION REQUIRED]'.
    3. Passing explicit --monument or setting ACTIVE_MONUMENT_ID succeeds cleanly.
    """
    _setup_sandbox(monkeypatch, tmp_path)

    # Lease mon_a only
    ao.run_preflight(monument_id="mon_a")
    assert os_mod.get_active_leased_monuments() == ["mon_a"]
    assert os_mod.resolve_monument_id(None) == "mon_a"

    # Lease mon_b concurrently
    ao.run_preflight(monument_id="mon_b")
    active = os_mod.get_active_leased_monuments()
    assert active == ["mon_a", "mon_b"]

    # Ambiguous call without --monument or ACTIVE_MONUMENT_ID must fail-fast
    with pytest.raises(RuntimeError, match=r"\[DISAMBIGUATION REQUIRED\]"):
        os_mod.resolve_monument_id(None)

    with pytest.raises(RuntimeError, match=r"\[DISAMBIGUATION REQUIRED\]"):
        ao.get_current_context(None)

    # Explicit monument override resolves cleanly
    assert os_mod.resolve_monument_id("mon_a") == "mon_a"
    assert os_mod.resolve_monument_id("mon_b") == "mon_b"

    # Environment variable ACTIVE_MONUMENT_ID resolves cleanly
    monkeypatch.setenv("ACTIVE_MONUMENT_ID", "mon_b")
    assert os_mod.resolve_monument_id(None) == "mon_b"


def test_parallel_status_dashboard_with_multiple_leases(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Verifies that display_parallel_status() outputs both active leased monuments side-by-side.
    """
    _setup_sandbox(monkeypatch, tmp_path)
    ao.run_preflight(monument_id="mon_a")
    ao.run_preflight(monument_id="mon_b")
    ao.unlock_flash_sprint(monument_id="mon_b")

    capsys.readouterr()
    os_mod.display_parallel_status()
    out = capsys.readouterr().out

    assert "PARALLEL SEQUESTERED MONUMENTS TELEMETRY DASHBOARD (2 Active Leases)" in out
    assert "mon_a" in out
    assert "mon_b" in out
    assert "PHASE_0_ARGON_PLANNING" in out
    assert "PHASE_1_FLASH_SPRINT" in out


def test_interleaved_dual_monument_cohort_progression(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """
    Simulates two concurrent chat sessions (Chat A on mon_a, Chat B on mon_b)
    interleaving Phase 0 preflight, unlock, prepare_cohort, and verify_cohort_and_advance
    without state cross-contamination.
    """
    env = _setup_sandbox(monkeypatch, tmp_path)

    # Mock leaf extraction, work order generation, gate, and ingest so we test orchestrator isolation directly
    monkeypatch.setattr(ao, "extract_leaves", lambda **kwargs: [])
    monkeypatch.setattr(
        ao,
        "generate_work_order",
        lambda monument_id, cohort_num, **kwargs: (
            tmp_path / f"{monument_id}_wo_{cohort_num}.md"
        ),
    )
    monkeypatch.setattr(ao, "run_gate", lambda **kwargs: 0)
    monkeypatch.setattr(ao, "ingest_and_sync", lambda **kwargs: None)

    # Chat A and Chat B run Phase 0 preflight and unlock Flash sprint
    ao.run_preflight(monument_id="mon_a")
    ao.run_preflight(monument_id="mon_b")
    ao.unlock_flash_sprint(monument_id="mon_a")
    ao.unlock_flash_sprint(monument_id="mon_b")

    # Interleave prepare_cohort(1) for both monuments
    ao.prepare_cohort(monument_id="mon_a", cohort_num=1)
    ao.prepare_cohort(monument_id="mon_b", cohort_num=1)

    state_a_mid = os_mod.load_state("mon_a")
    state_b_mid = os_mod.load_state("mon_b")
    assert state_a_mid["small_pause_gate_status"] == "AWAITING_SUBAGENT_EXECUTION"
    assert state_b_mid["small_pause_gate_status"] == "AWAITING_SUBAGENT_EXECUTION"

    # Chat B finishes Cohort 1 first (and auto-prepares Cohort 2), then Chat A finishes Cohort 1
    res_b = ao.verify_cohort_and_advance(monument_id="mon_b", cohort_num=1)
    res_a = ao.verify_cohort_and_advance(monument_id="mon_a", cohort_num=1)
    assert res_b["status"] == "ADVANCED"
    assert res_b["manifest"]["action"] == "INVOKE_SUBAGENT"
    assert res_a["status"] == "ADVANCED"
    assert res_a["manifest"]["action"] == "INVOKE_SUBAGENT"

    state_a_after = os_mod.load_state("mon_a")
    state_b_after = os_mod.load_state("mon_b")

    assert state_a_after["completed_cohorts"] == [1]
    assert state_a_after["current_cohort"] == 2
    assert state_a_after["translated_pages"] == 10
    assert state_a_after["remaining_pages"] == 10

    assert state_b_after["completed_cohorts"] == [1]
    assert state_b_after["current_cohort"] == 2
    assert state_b_after["translated_pages"] == 10
    assert state_b_after["remaining_pages"] == 20

    mirror = json.loads(env["state_mirror_path"].read_text(encoding="utf-8"))
    assert "mon_a" in mirror["concurrent_active_monuments"]
    assert "mon_b" in mirror["concurrent_active_monuments"]
    assert mirror["concurrent_active_monuments"]["mon_a"]["current_cohort"] == 2
    assert mirror["concurrent_active_monuments"]["mon_b"]["current_cohort"] == 2


def test_defer_monument_seals_own_state_and_skips_active_parallel_monument(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Verifies that deferring mon_a while mon_b is actively running in another chat:
    1. Marks mon_a as MONUMENT_DEFERRED_GATE_0 (active_lease=False, status='failed').
    2. Leaves mon_b completely untouched on Cohort 5 (active_lease=True).
    3. Recommends mon_c (the next unclaimed monument) in the onboarding prompt without
       prematurely claiming mon_c's active_lease.
    """
    env = _setup_sandbox(monkeypatch, tmp_path)

    # mon_a in Phase 0, mon_b actively running on Cohort 5
    ao.run_preflight(monument_id="mon_a")
    ao.run_preflight(monument_id="mon_b")
    ao.unlock_flash_sprint(monument_id="mon_b")
    st_b = os_mod.load_state("mon_b")
    st_b["current_cohort"] = 5
    st_b["completed_cohorts"] = [1, 2, 3, 4]
    st_b["translated_pages"] = 40
    os_mod.save_state(st_b, "mon_b")

    capsys.readouterr()
    ao.defer_monument_to_back_of_queue("mon_a", "Truncated facsimile scan")
    out = capsys.readouterr().out

    # 1. mon_a state is sealed as deferred with active_lease=False
    st_a_after = os_mod.load_state("mon_a")
    assert st_a_after["small_pause_gate_status"] == "MONUMENT_DEFERRED_GATE_0"
    assert st_a_after["active_lease"] is False
    assert st_a_after["status"] == "failed"

    # 2. mon_b state is completely untouched
    st_b_after = os_mod.load_state("mon_b")
    assert st_b_after["current_cohort"] == 5
    assert st_b_after["completed_cohorts"] == [1, 2, 3, 4]
    assert st_b_after["active_lease"] is True

    # 3. Onboarding prompt recommends mon_c (skipping active mon_b), and mon_c is not leased yet
    assert "mon_c" in out
    assert os_mod.get_active_leased_monuments() == ["mon_b"]

    # 4. Primary mirror preserves mon_b as top-level monument
    mirror = json.loads(env["state_mirror_path"].read_text(encoding="utf-8"))
    assert mirror["monument_id"] == "mon_b"


def test_claim_pause_resume_lifecycle(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """
    Verifies atomic claiming (--claim-next-monument), pausing (--pause-monument),
    and resuming (--resume-monument) across multiple monuments.
    """
    env = _setup_sandbox(monkeypatch, tmp_path)

    # First claim gets mon_a
    claimed_1 = ao.claim_next_monument()
    assert claimed_1["next_monument_id"] == "mon_a"
    assert os_mod.get_active_leased_monuments() == ["mon_a"]

    # Second concurrent claim skips leased mon_a and gets mon_b
    claimed_2 = ao.claim_next_monument()
    assert claimed_2["next_monument_id"] == "mon_b"
    assert os_mod.get_active_leased_monuments() == ["mon_a", "mon_b"]

    # Simulate 2 completed cohort files on disk for mon_a, then pause mon_a
    (env["ws_a"] / "Final MD" / "mon_a_cohort1.md").write_text("=== LEAF p1 ===", encoding="utf-8")
    (env["ws_a"] / "Final MD" / "mon_a_cohort2.md").write_text("=== LEAF p11 ===", encoding="utf-8")
    paused_state = os_mod.pause_monument("mon_a")
    assert paused_state["active_lease"] is False
    assert paused_state["small_pause_gate_status"] == "MONUMENT_PAUSED"
    assert paused_state["completed_cohorts"] == [1, 2]

    # Now only mon_b holds an active lease, so resolve_monument_id(None) auto-resolves mon_b!
    assert os_mod.get_active_leased_monuments() == ["mon_b"]
    assert os_mod.resolve_monument_id(None) == "mon_b"

    # Resume mon_a -> both hold active leases again
    resumed_state = os_mod.resume_monument("mon_a")
    assert resumed_state["active_lease"] is True
    assert resumed_state["small_pause_gate_status"] == "PHASE_0_ARGON_PLANNING_LOCKED"
    assert os_mod.get_active_leased_monuments() == ["mon_a", "mon_b"]


def test_atomic_registry_update_and_multi_monument_chronicle(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """
    Verifies atomic_update_registry() and ChronicleManager multi-monument Working State formatting.
    """
    env = _setup_sandbox(monkeypatch, tmp_path)
    ao.run_preflight(monument_id="mon_a")
    ao.run_preflight(monument_id="mon_b")

    ok = cm.ChronicleManager.sync_bench(
        working_state="1700 Alpha #1 Ingested (10/20 leaves)",
        built_summary="Translated Cohort #1 of Monument Alpha (1700).",
        bench_event="Cohort #1 promoted (Leaves p1..p10).",
    )
    assert ok is True

    updated_md = env["chronicle_file"].read_text(encoding="utf-8")
    assert "1700 Alpha #1 Ingested (10/20 leaves)" in updated_md
    assert "Monument Beta (1750)" in updated_md
    assert "||" in updated_md
