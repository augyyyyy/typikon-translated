#!/usr/bin/env python3
"""
Unit & Integration Tests for the 3-Phase Bookend Hybrid Model Routing Architecture
==================================================================================
Verifies all 6 architectural invariants locked during /grill-me:
  1. Phase 0 (Argon) -> Phase 1 (Flash) Circuit Breaker & --unlock-flash-sprint
  2. Lean 'ephemeral_translator' worker subagent definition & strict Model='flash' lock
  3. 4-Signal Argon Review Queue Collector (Audit_Reports/argon_review_queue.json)
  4. 4-Part Deterministic Python Self-Healing (banners, inline footnotes, vocab/doxology, pronouns)
  5. Two-Tier Unattended Flash Resilience (1 Flash Retry -> Quarantine if === LEAF pN === present; Block if missing)
  6. Phase 2 Argon Deep Audit Batching (<=5 direct vs >5 batched <=8) & Unresolved Quarantine Publication Gate
"""

import sys
import json
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import orchestrator_state
import run_small_pause_gate
import autonomous_orchestrator


def test_phase_0_circuit_breaker_and_unlock(monkeypatch, tmp_path):
    """Decision 1: New monuments start in PHASE_0_ARGON_PLANNING_LOCKED and block Cohort 1 until unlocked."""
    fake_state_file = tmp_path / "ACTIVE_ORCHESTRATOR_STATE.json"
    monkeypatch.setattr(orchestrator_state, "STATE_FILE", fake_state_file)
    monkeypatch.setattr(autonomous_orchestrator, "STATE_FILE", fake_state_file)

    orchestrator_state.set_monument("1895_dmitrievsky_vol1")
    state = orchestrator_state.load_state()
    assert state["monument_id"] == "1895_dmitrievsky_vol1"
    assert state["routing_phase"] == "PHASE_0_ARGON_PLANNING"
    assert state["small_pause_gate_status"] == "PHASE_0_ARGON_PLANNING_LOCKED"
    assert state["active_subagent_model"] == "flash"

    # Attempting to prepare Cohort 1 while in Phase 0 must raise PermissionError
    with pytest.raises(PermissionError, match="PHASE_0_ARGON_PLANNING_LOCKED"):
        autonomous_orchestrator.prepare_cohort(monument_id="1895_dmitrievsky_vol1", cohort_num=1)

    # Unlocking Phase 1 transitions state to PHASE_1_FLASH_SPRINT
    unlock_res = autonomous_orchestrator.unlock_flash_sprint(monument_id="1895_dmitrievsky_vol1")
    assert unlock_res["status"] == "PHASE_1_FLASH_SPRINT_UNLOCKED"
    assert unlock_res["routing_phase"] == "PHASE_1_FLASH_SPRINT"
    assert unlock_res["active_subagent_model"] == "flash"


def test_ephemeral_translator_and_strict_flash_lock(monkeypatch, tmp_path):
    """Decision 2: Worker subagent uses lean 'ephemeral_translator' and strict Model='flash'."""
    fake_state_file = tmp_path / "ACTIVE_ORCHESTRATOR_STATE.json"
    monkeypatch.setattr(orchestrator_state, "STATE_FILE", fake_state_file)
    monkeypatch.setattr(autonomous_orchestrator, "STATE_FILE", fake_state_file)

    orchestrator_state.set_monument("1895_dmitrievsky_vol1")
    autonomous_orchestrator.unlock_flash_sprint(monument_id="1895_dmitrievsky_vol1")

    monkeypatch.setattr(autonomous_orchestrator, "extract_leaves", lambda **kwargs: None)
    fake_wo = PROJECT_ROOT / "Liturgical Monuments" / "Monument 7 - 1895 Dmitrievsky Vol 1" / "Work_Orders" / "WO_Cohort_1.md"
    monkeypatch.setattr(autonomous_orchestrator, "generate_work_order", lambda **kwargs: fake_wo)

    manifest = autonomous_orchestrator.prepare_cohort(monument_id="1895_dmitrievsky_vol1", cohort_num=1)
    assert manifest["action"] == "INVOKE_SUBAGENT"
    assert manifest["subagent_type"] == "ephemeral_translator"
    assert manifest["model"] == "flash"

    defn = manifest["define_subagent_if_missing"]
    assert defn["Name"] == "ephemeral_translator"
    assert defn["EnableWriteTools"] is True
    assert defn["EnableSubagentTools"] is False
    assert defn["EnableMCPTools"] is False


def test_argon_review_queue_4_signals(tmp_path):
    """Decision 3: Verifies all 4 leaf-level signals populate Audit_Reports/argon_review_queue.json."""
    ws = tmp_path / "monument_ws"
    (ws / "Source Text").mkdir(parents=True)
    (ws / "Draft").mkdir(parents=True)
    (ws / "Audit_Reports").mkdir(parents=True)

    source_file = ws / "Source Text" / "test_mon_cohort1_source.txt"
    draft_file = ws / "Draft" / "test_mon_cohort1_raw_draft.md"

    # Leaf 1: Clean leaf (normal ratio ~1.0, no markers, no heavy tables/footnotes)
    # Leaf 2: Signal 1 — Epigraphic uncertainty [?] and [illegible]
    # Leaf 3: Signal 2 — Borderline SGC-02 ratio (< 0.50 on >=120c source)
    # Leaf 4: Signal 3 — High-complexity table (>=5 rows) and >=5 footnotes
    # Leaf 5: Signal 4 — Quarantined override
    src_leaf_1 = "А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я " * 4
    drf_leaf_1 = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f " * 4

    src_leaf_2 = "Текст рукописи с повреждением [?] и утратой строки."
    drf_leaf_2 = "Manuscript text with damage [?] and [illegible] loss of line."

    src_leaf_3 = "Длинный исходный литургический текст устава на церковнославянском языке для проверки соотношения длины перевода и оригинала в системе контроля качества. " * 2
    drf_leaf_3 = "Short English summary text that sits at a 0.35 borderline length ratio for Argon review."

    src_leaf_4 = "Пасхальная таблица и критический аппарат с многочисленными примечаниями."
    drf_leaf_4 = (
        "| Col 1 | Col 2 |\n|---|---|\n"
        "| R1 | V1 [^1] |\n| R2 | V2 [^2] |\n| R3 | V3 [^3] |\n| R4 | V4 [^4] |\n| R5 | V5 [^5] |\n"
    )

    src_leaf_5 = "Обычный лист для проверки карантина после одной попытки."
    drf_leaf_5 = "Standard leaf for testing quarantine override after one retry."

    source_file.write_text(
        f"=== LEAF p1 ===\n{src_leaf_1}\n"
        f"=== LEAF p2 ===\n{src_leaf_2}\n"
        f"=== LEAF p3 ===\n{src_leaf_3}\n"
        f"=== LEAF p4 ===\n{src_leaf_4}\n"
        f"=== LEAF p5 ===\n{src_leaf_5}\n",
        encoding="utf-8",
    )
    draft_file.write_text(
        f"=== LEAF p1 ===\n{drf_leaf_1}\n"
        f"=== LEAF p2 ===\n{drf_leaf_2}\n"
        f"=== LEAF p3 ===\n{drf_leaf_3}\n"
        f"=== LEAF p4 ===\n{drf_leaf_4}\n"
        f"=== LEAF p5 ===\n{drf_leaf_5}\n",
        encoding="utf-8",
    )

    res = run_small_pause_gate.collect_argon_review_signals(
        monument_id="test_mon",
        cohort_num=1,
        ws=ws,
        target_text=draft_file,
        source_file=source_file,
        quarantine_reasons=["structural_sequence_failed"],
        quarantine_leaves=[5],
    )

    assert res["cohort_queued_leaves"] == [2, 3, 4, 5]
    assert res["total_queued_leaves"] == 4
    assert res["unresolved_quarantines"] == 1

    q_data = json.loads((ws / "Audit_Reports" / "argon_review_queue.json").read_text(encoding="utf-8"))
    items_map = {it["leaf_num"]: it for it in q_data["items"]}
    assert 1 not in items_map
    assert any("epigraphic_uncertainty_marker" in r for r in items_map[2]["reasons"])
    assert any("borderline_sgc02_ratio" in r for r in items_map[3]["reasons"])
    assert any("complex_multicolumn_table" in r for r in items_map[4]["reasons"])
    assert any("dense_polyglot_apparatus" in r for r in items_map[4]["reasons"])
    assert items_map[5]["status"] == "QUARANTINED_FOR_ARGON"


def test_4_part_deterministic_self_healing(tmp_path):
    """Decision 6: Verifies banner normalization, inline footnote migration, and vocab/doxology healing."""
    # 1. Leaf banner normalization
    raw_banners = "=== Leaf 1 ===\nText 1\n=== leaf p2 ===\nText 2\n"
    norm_txt, mod_b = autonomous_orchestrator._normalize_leaf_banners(raw_banners)
    assert mod_b is True
    assert "=== LEAF p1 ===" in norm_txt
    assert "=== LEAF p2 ===" in norm_txt

    # 2. Inline footnote migration
    fn_path = tmp_path / "cohort1_footnotes.txt"
    fn_path.write_text("[^1]: Existing note 1.\n", encoding="utf-8")
    draft_with_inline = (
        "=== LEAF p1 ===\nBody text with markers [^1] and [^2].\n\n"
        "### Notes\n"
        "[^2]: Migrated inline note 2.\n"
    )
    cleaned_draft, mod_fn = autonomous_orchestrator._migrate_inline_footnotes(draft_with_inline, fn_path)
    assert mod_fn is True
    assert "[^2]:" not in cleaned_draft
    assert "### Notes" not in cleaned_draft
    fn_contents = fn_path.read_text(encoding="utf-8")
    assert "[^1]: Existing note 1." in fn_contents
    assert "[^2]: Migrated inline note 2." in fn_contents

    # 3. Vocabulary & Doxology replacement
    raw_vocab = "We sing the Kondak and Irmos unto God for ever and ever.\n"
    healed_vocab, mod_v = autonomous_orchestrator._apply_vocabulary_and_doxology_healing(raw_vocab)
    assert mod_v is True
    assert "Kontakion" in healed_vocab
    assert "Heirmos" in healed_vocab
    assert "unto ages of ages" in healed_vocab


def test_two_tier_flash_resilience_boundary_check(tmp_path):
    """Decision 4: Quarantine is permitted only when all physical === LEAF pN === boundaries exist on disk."""
    ws = tmp_path / "ws"
    (ws / "Source Text").mkdir(parents=True)
    (ws / "Draft").mkdir(parents=True)

    src = ws / "Source Text" / "mon_cohort1_source.txt"
    drf = ws / "Draft" / "mon_cohort1_raw_draft.md"

    src.write_text("=== LEAF p1 ===\nSrc 1\n=== LEAF p2 ===\nSrc 2\n", encoding="utf-8")
    drf.write_text("=== LEAF p1 ===\nDrf 1\n=== LEAF p2 ===\nDrf 2\n", encoding="utf-8")

    ok, missing, _msg = autonomous_orchestrator.verify_physical_leaf_boundaries_on_disk(ws, "mon", 1, 1, 2)
    assert ok is True
    assert missing == []

    # Missing leaf p3 should fail the boundary check (triggering a hard-stop BLOCKED instead of quarantine)
    ok2, missing2, _msg2 = autonomous_orchestrator.verify_physical_leaf_boundaries_on_disk(ws, "mon", 1, 1, 3)
    assert ok2 is False
    assert missing2 == [3]


def test_phase_2_argon_audit_batching_and_quarantine_gate(monkeypatch, tmp_path):
    """Decision 5: Verifies <=5 direct vs >5 batched <=8 Argon dispatch and unresolved quarantine compilation block."""
    fake_state_file = tmp_path / "ACTIVE_ORCHESTRATOR_STATE.json"
    monkeypatch.setattr(orchestrator_state, "STATE_FILE", fake_state_file)
    monkeypatch.setattr(autonomous_orchestrator, "STATE_FILE", fake_state_file)

    fake_ws = tmp_path / "mon7_ws"
    (fake_ws / "Audit_Reports").mkdir(parents=True)
    queue_file = fake_ws / "Audit_Reports" / "argon_review_queue.json"

    fake_registry = {
        "monuments": {
            "test_mon": {
                "monument_id": "test_mon",
                "title": "Test Monument",
                "short_title": "Test Mon",
                "total_physical_pages": 100,
                "default_cohort_size": 10,
                "workspace_dir": str(fake_ws),
            }
        }
    }
    monkeypatch.setattr(orchestrator_state, "load_registry", lambda: fake_registry)
    monkeypatch.setattr(autonomous_orchestrator, "load_registry", lambda: fake_registry)

    orchestrator_state.set_monument("test_mon")

    # Case A: 3 queued leaves (<=5 -> DIRECT_PARENT_ARGON) with 1 unresolved quarantine
    items_3 = [
        {"leaf_num": i, "cohort": 1, "status": "QUARANTINED_FOR_ARGON" if i == 1 else "QUEUED_FOR_ARGON", "reasons": ["test"]}
        for i in (1, 2, 3)
    ]
    queue_file.write_text(
        json.dumps({"monument_id": "test_mon", "total_queued_leaves": 3, "unresolved_quarantines": 1, "items": items_3}),
        encoding="utf-8",
    )

    audit_res = autonomous_orchestrator.run_argon_post_sprint_audit("test_mon")
    assert audit_res["strategy"] == "DIRECT_PARENT_ARGON"
    assert audit_res["batches_count"] == 1
    assert audit_res["batches"][0]["model"] == "inherit"

    # Attempting to compile publication while unresolved_quarantines == 1 must be blocked
    comp_blocked = autonomous_orchestrator.compile_final_publication("test_mon")
    assert comp_blocked["status"] == "QUARANTINES_UNRESOLVED"
    assert comp_blocked["unresolved_quarantines"] == 1

    # Case B: 10 queued leaves (>5 -> BATCHED_ARGON_SUBAGENTS_MAX_8: 2 batches of 8 and 2)
    items_10 = [
        {"leaf_num": i, "cohort": 1, "status": "QUEUED_FOR_ARGON", "reasons": ["test"]}
        for i in range(1, 11)
    ]
    queue_file.write_text(
        json.dumps({"monument_id": "test_mon", "total_queued_leaves": 10, "unresolved_quarantines": 0, "items": items_10}),
        encoding="utf-8",
    )
    audit_res_10 = autonomous_orchestrator.run_argon_post_sprint_audit("test_mon")
    assert audit_res_10["strategy"] == "BATCHED_ARGON_SUBAGENTS_MAX_8"
    assert audit_res_10["batches_count"] == 2
    assert len(audit_res_10["batches"][0]["leaves"]) == 8
    assert len(audit_res_10["batches"][1]["leaves"]) == 2


def test_phase_0_vision_budget_contract_and_preflight_brief(monkeypatch, tmp_path):
    """Verifies that run_preflight writes phase0_preflight_brief.json with the 8-leaf / 2-batch vision cap and Octoechos scaffold."""
    fake_state_file = tmp_path / "ACTIVE_ORCHESTRATOR_STATE.json"
    monkeypatch.setattr(orchestrator_state, "STATE_FILE", fake_state_file)
    monkeypatch.setattr(autonomous_orchestrator, "STATE_FILE", fake_state_file)

    fake_ws = tmp_path / "1630_lviv_octoechos_ws"
    images_dir = fake_ws / "Source Text" / "images"
    images_dir.mkdir(parents=True)
    for p in (1, 2, 3, 4, 5, 558, 559, 560):
        (images_dir / f"Page_{p:04d}.jpg").write_bytes(b"fake_jpg")

    fake_registry = {
        "monuments": {
            "1630_lviv_octoechos": {
                "monument_id": "1630_lviv_octoechos",
                "title": "1630 Lviv Octoechos (Sheptytsky Foundation)",
                "short_title": "1630 Lviv Octoechos",
                "total_physical_pages": 560,
                "default_cohort_size": 10,
                "genre_register": "hymnographic_and_rubrical",
                "workspace_dir": str(fake_ws),
                "relative_pdf_path": "2. Historical Liturgical Texts/Octoechos/1630_Lviv_Octoechos.pdf",
            }
        }
    }
    monkeypatch.setattr(orchestrator_state, "load_registry", lambda: fake_registry)
    monkeypatch.setattr(autonomous_orchestrator, "load_registry", lambda: fake_registry)

    res = autonomous_orchestrator.run_preflight("1630_lviv_octoechos")
    assert res["status"] == "PHASE_0_PREFLIGHT_COMPLETE"
    vc = res["vision_budget_contract"]
    assert vc["max_total_leaves"] == 8
    assert vc["max_vision_batches"] == 2
    assert vc["forbid_internal_binary_search"] is True
    assert vc["allowed_front_leaves"] == ["p1", "p2", "p3", "p4", "p5"]
    assert vc["allowed_rear_leaves"] == ["p558", "p559", "p560"]

    pub_spec = res["recommended_publication_spec"]
    assert pub_spec["mode"] == "universal_dynamic_h1"

    brief_path = Path(res["preflight_brief_path"])
    assert brief_path.exists()
    brief_data = json.loads(brief_path.read_text(encoding="utf-8"))
    assert brief_data["vision_budget_contract"]["max_total_leaves"] == 8


def test_phase_0_onboarding_prompt_and_defer_monument(monkeypatch, tmp_path):
    """Verifies build_phase0_onboarding_prompt and defer_monument_to_back_of_queue."""
    fake_state_file = tmp_path / "ACTIVE_ORCHESTRATOR_STATE.json"
    fake_registry_file = tmp_path / "codex_registry.json"
    monkeypatch.setattr(orchestrator_state, "STATE_FILE", fake_state_file)
    monkeypatch.setattr(autonomous_orchestrator, "STATE_FILE", fake_state_file)
    monkeypatch.setattr(orchestrator_state, "STATE_FILE", fake_state_file)
    monkeypatch.setattr(orchestrator_state, "get_state_file_path", lambda mid=None: fake_state_file)
    monkeypatch.setattr(orchestrator_state, "REGISTRY_FILE", fake_registry_file)
    monkeypatch.setattr(autonomous_orchestrator, "REGISTRY_FILE", fake_registry_file)

    fake_registry = {
        "monuments": {
            "1629_kyiv_octoechos": {
                "monument_id": "1629_kyiv_octoechos",
                "title": "1629 Kyiv Lava Octoechos",
                "short_title": "1629 Kyiv Octoechos",
                "status": "ready",
                "active": True,
                "wave": 2,
                "total_physical_pages": 63,
                "default_cohort_size": 10,
                "genre_register": "hymnographic_and_rubrical",
                "workspace_dir": "Liturgical Monuments/Monument 8 - 1629 Kyiv Octoechos",
                "relative_pdf_path": "2. Historical Liturgical Texts/Octoechos/1629_Kyiv.pdf",
            },
            "1630_lviv_octoechos": {
                "monument_id": "1630_lviv_octoechos",
                "title": "1630 Lviv Octoechos (Sheptytsky Foundation)",
                "short_title": "1630 Lviv Octoechos",
                "status": "ready",
                "active": False,
                "wave": 2,
                "total_physical_pages": 560,
                "default_cohort_size": 10,
                "genre_register": "hymnographic_and_rubrical",
                "workspace_dir": "Liturgical Monuments/Monument 9 - 1630 Lviv Octoechos",
                "relative_pdf_path": "2. Historical Liturgical Texts/Octoechos/1630_Lviv.pdf",
            },
        }
    }
    fake_registry_file.write_text(json.dumps(fake_registry, indent=2), encoding="utf-8")
    orchestrator_state.set_monument("1629_kyiv_octoechos")

    defer_res = autonomous_orchestrator.defer_monument_to_back_of_queue(
        monument_id="1629_kyiv_octoechos",
        reason="1904 Titov preface anthology (63 pages), not full Octoechos codex",
    )
    assert defer_res["status"] == "DEFERRED_TO_BACK_OF_QUEUE"
    assert defer_res["deferred_monument_id"] == "1629_kyiv_octoechos"
    assert defer_res["next_monument_id"] == "1630_lviv_octoechos"
    assert "Hard Phase 0 Vision Budget Cap" in defer_res["onboarding_prompt"]
    assert "Absolute Ban on Mid-Codex Binary Searches" in defer_res["onboarding_prompt"]
    assert "--defer-monument" in defer_res["onboarding_prompt"]

    updated_reg = json.loads(fake_registry_file.read_text(encoding="utf-8"))
    keys = list(updated_reg["monuments"].keys())
    assert keys == ["1630_lviv_octoechos", "1629_kyiv_octoechos"]
    assert updated_reg["monuments"]["1629_kyiv_octoechos"]["status"] == "failed"
    assert updated_reg["monuments"]["1629_kyiv_octoechos"]["wave"] == 5


def test_anti_slop_and_footnote_bijectivity_deterministic_healers(tmp_path):
    """Verifies Gate 1B anti-slop healer and Gate 3 footnote bijectivity healer."""
    from lint_liturgical_slop import lint_slop

    raw_slop = (
        "Wherefore we cry unto Thee, O wondrous Savior, verily this is a testament to Thy mercy.\n"
        "The priest shall bow and the choir singeth the hymn while the deacon standeth.\n"
        "Wondrous is God in His saints.\n"
    )
    healed_txt, mod_slop = autonomous_orchestrator._apply_anti_slop_healing(raw_slop)
    assert mod_slop is True
    assert "Therefore we cry" in healed_txt
    assert "marvelous Savior" in healed_txt
    assert "truly this is a witness to" in healed_txt
    assert "The priest bows" in healed_txt
    assert "the choir sings" in healed_txt
    assert "the deacon stands" in healed_txt
    # Preserves canonical scriptural exception 'Wondrous is God'
    assert "Wondrous is God in His saints." in healed_txt

    slop_file = tmp_path / "healed_draft.md"
    slop_file.write_text(healed_txt, encoding="utf-8")
    slop_res = lint_slop(slop_file)
    assert slop_res["passed"] is True
    assert slop_res["violation_count"] == 0

    # Footnote bijectivity healer: missing caret [2] in draft, missing caret [3]: in fn,
    # orphaned [^99]: in fn, and missing definition for [^4]
    fn_file = tmp_path / "cohort_footnotes.txt"
    fn_file.write_text(
        "[^1]: First note.\n"
        "[^2]: Second note.\n"
        "[3]: Third note missing caret.\n"
        "[^99]: Orphaned note with no body marker.\n",
        encoding="utf-8",
    )
    draft_fn = "=== LEAF p1 ===\nText with [^1], bare [2], [^3], and unsupplied [^4].\n"
    healed_draft, mod_fn = autonomous_orchestrator._reconcile_footnote_bijectivity(draft_fn, fn_file)
    assert mod_fn is True
    assert "[^2]" in healed_draft
    healed_fn_txt = fn_file.read_text(encoding="utf-8")
    assert "[^3]: Third note missing caret." in healed_fn_txt
    assert "[^99]:" not in healed_fn_txt
    assert "[^4]:" in healed_fn_txt


def test_zero_switch_end_of_sprint_auto_progression(monkeypatch, tmp_path):
    """Verifies that when remaining_pages == 0 and 0 leaves are queued, verify_cohort_and_advance auto-compiles without halting for a UI switch."""
    fake_state_file = tmp_path / "ACTIVE_ORCHESTRATOR_STATE.json"
    monkeypatch.setattr(orchestrator_state, "STATE_FILE", fake_state_file)
    monkeypatch.setattr(autonomous_orchestrator, "STATE_FILE", fake_state_file)

    fake_ws = tmp_path / "zero_switch_ws"
    (fake_ws / "Audit_Reports").mkdir(parents=True)
    (fake_ws / "Draft").mkdir(parents=True)
    (fake_ws / "Source Text").mkdir(parents=True)

    fake_registry = {
        "monuments": {
            "test_zero_switch": {
                "monument_id": "test_zero_switch",
                "title": "Zero Switch Test Monument",
                "short_title": "Zero Switch Mon",
                "total_physical_pages": 10,
                "default_cohort_size": 10,
                "workspace_dir": str(fake_ws),
            }
        }
    }
    monkeypatch.setattr(orchestrator_state, "load_registry", lambda: fake_registry)
    monkeypatch.setattr(autonomous_orchestrator, "load_registry", lambda: fake_registry)

    orchestrator_state.set_monument("test_zero_switch")
    autonomous_orchestrator.unlock_flash_sprint("test_zero_switch")

    monkeypatch.setattr(autonomous_orchestrator, "run_gate", lambda **kwargs: 0)
    monkeypatch.setattr(autonomous_orchestrator, "ingest_and_sync", lambda **kwargs: None)
    monkeypatch.setattr(
        autonomous_orchestrator,
        "compile_final_publication",
        lambda mon_id=None: {"status": "GRAND_PAUSE", "monument_complete": True, "publication_edition_ready": True},
    )

    res = autonomous_orchestrator.verify_cohort_and_advance(monument_id="test_zero_switch", cohort_num=1)
    assert res["status"] == "AWAITING_ARGON_POST_SPRINT_AUDIT"
    assert res["queued_leaves"] == 0
    assert res["unresolved_quarantines"] == 0

