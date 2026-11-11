#!/usr/bin/env python3
"""
Unit tests for scripts/audit_transcript_trajectory.py and .agents/scripts/governance_gate.py
(Vectors 5C, 7, 11, 12 & Pre-Tool Hook Sandbox).
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from scripts.audit_transcript_trajectory import (
    audit_cohort_subagent_trajectory,
    audit_source_orthographic_authenticity,
    build_monument_process_autopsy,
    discover_cohort_subagent_transcript,
    heal_source_orthographic_hypercorrections,
)


def test_vector_5c_fake_archaism_detection_and_healing(tmp_path: Path) -> None:
    src_file = tmp_path / "test_mon_cohort1_source.txt"
    raw_content = (
        "=== LEAF p1 ===\n"
        "Слава Ѿцю и Сыну и Святому Духу, и нынѣ и присно.\n"
        "Молитвами святыхъ ѿцевъ нашихъ, Господи Іисусе Христе.\n"
    )
    src_file.write_text(raw_content, encoding="utf-8")

    audit_before = audit_source_orthographic_authenticity(src_file)
    assert not audit_before["passed"]
    assert audit_before["violation_count"] == 2
    assert audit_before["violations"][0]["leaf"] == 1

    healed_txt, cnt = heal_source_orthographic_hypercorrections(raw_content)
    assert cnt == 2
    assert "Слава Отцю" in healed_txt
    assert "святыхъ отцевъ" in healed_txt

    src_file.write_text(healed_txt, encoding="utf-8")
    audit_after = audit_source_orthographic_authenticity(src_file)
    assert audit_after["passed"]
    assert audit_after["violation_count"] == 0


def test_vector_11_subagent_trajectory_audit_clean_and_contaminated(tmp_path: Path) -> None:
    brain_root = tmp_path / "brain"
    ws = tmp_path / "Liturgical Monuments" / "test_mon"
    ws.mkdir(parents=True)

    # Create a clean subagent session for cohort 1
    clean_cid = "subagent-clean-001"
    clean_log_dir = brain_root / clean_cid / ".system_generated" / "logs"
    clean_log_dir.mkdir(parents=True)
    clean_steps = [
        {
            "step_index": 0,
            "source": "SYSTEM",
            "type": "USER_INPUT",
            "created_at": "2026-11-02T20:00:00Z",
            "content": "Execute work_order_cohort_1.md for test_mon (test_mon_cohort1_raw_draft.md)",
        },
        {
            "step_index": 1,
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "status": "DONE",
            "created_at": "2026-11-02T20:00:05Z",
            "tool_calls": [
                {"name": "read_file", "args": {"Path": str(ws / "JPGs" / "Page_0001.jpg")}},
                {"name": "read_file", "args": {"Path": str(ws / "JPGs" / "Page_0002.jpg")}},
            ],
        },
        {
            "step_index": 2,
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "status": "DONE",
            "created_at": "2026-11-02T20:00:25Z",
            "tool_calls": [
                {"name": "write_file", "args": {"Path": str(ws / "Draft" / "test_mon_cohort1_raw_draft.md")}},
            ],
        },
    ]
    (clean_log_dir / "transcript.jsonl").write_text(
        "\n".join(json.dumps(s) for s in clean_steps) + "\n",
        encoding="utf-8",
    )

    res_clean = audit_cohort_subagent_trajectory(
        monument_id="test_mon",
        cohort_num=1,
        expected_leaves=[1, 2],
        ws=ws,
        brain_dir=brain_root,
    )
    assert res_clean["transcript_found"]
    assert res_clean["passed"]
    assert res_clean["viewed_leaves"] == [1, 2]
    assert res_clean["unviewed_leaves"] == []
    assert res_clean["contaminated_leaves"] == []

    # Create a contaminated subagent session for cohort 2 (calls search_web on leaf 4)
    bad_cid = "subagent-contaminated-002"
    bad_log_dir = brain_root / bad_cid / ".system_generated" / "logs"
    bad_log_dir.mkdir(parents=True)
    bad_steps = [
        {
            "step_index": 0,
            "source": "SYSTEM",
            "type": "USER_INPUT",
            "created_at": "2026-11-02T21:00:00Z",
            "content": "Execute work_order_cohort_2.md for test_mon (test_mon_cohort2_raw_draft.md)",
        },
        {
            "step_index": 1,
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "status": "DONE",
            "created_at": "2026-11-02T21:00:05Z",
            "tool_calls": [
                {"name": "read_file", "args": {"Path": str(ws / "JPGs" / "Page_0003.jpg")}},
                {"name": "read_file", "args": {"Path": str(ws / "JPGs" / "Page_0004.jpg")}},
                {"name": "search_web", "args": {"query": "Menaion sticheron translation"}},
            ],
        },
    ]
    (bad_log_dir / "transcript.jsonl").write_text(
        "\n".join(json.dumps(s) for s in bad_steps) + "\n",
        encoding="utf-8",
    )

    res_bad = audit_cohort_subagent_trajectory(
        monument_id="test_mon",
        cohort_num=2,
        expected_leaves=[3, 4],
        ws=ws,
        brain_dir=brain_root,
    )
    assert res_bad["transcript_found"]
    assert not res_bad["passed"]
    assert res_bad["contaminated_leaves"] == [4]
    assert res_bad["violations"][0]["type"] == "subagent_web_search_call"


def test_vector_12_process_autopsy_builder(tmp_path: Path) -> None:
    ws = tmp_path / "Liturgical Monuments" / "test_mon"
    audit_dir = ws / "Audit_Reports"
    audit_dir.mkdir(parents=True)
    (audit_dir / "phase0_preflight_brief.json").write_text("{}", encoding="utf-8")
    (audit_dir / "cohort1_small_pause_report.json").write_text(
        json.dumps({
            "overall_status": "PASSED",
            "gates": {
                "orthographic_authenticity_v5c": {"passed": True, "violation_count": 0},
                "subagent_trajectory": {"passed": True, "transcript_found": True, "violations": []},
            },
        }),
        encoding="utf-8",
    )

    autopsy = build_monument_process_autopsy("test_mon", ws, total_pages=10)
    assert autopsy["passed"]
    assert autopsy["phi_score"] == 100.0
    assert (audit_dir / "process_autopsy_report.json").exists()


def test_governance_gate_subagent_sandbox(tmp_path: Path) -> None:
    brain_root = tmp_path / "brain"
    sub_cid = "subagent-worker-999"
    log_dir = brain_root / sub_cid / ".system_generated" / "logs"
    log_dir.mkdir(parents=True)
    (log_dir / "transcript.jsonl").write_text(
        json.dumps({
            "step_index": 0,
            "source": "SYSTEM",
            "content": "You are ephemeral_translator executing work_order_cohort_1.md",
        }) + "\n",
        encoding="utf-8",
    )

    gate_script = PROJECT_ROOT / ".agents" / "scripts" / "governance_gate.py"
    env = dict(**os.environ, ANTIGRAVITY_BRAIN_DIR=str(brain_root))

    # 1. Deny search_web for subagent
    proc_deny_web = subprocess.run(
        [sys.executable, str(gate_script)],
        input=json.dumps({
            "conversationId": sub_cid,
            "toolCall": {"name": "search_web", "args": {"query": "octoechos"}},
        }),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    out_web = json.loads(proc_deny_web.stdout.strip())
    assert out_web["decision"] == "deny"

    # 2. Deny out-of-sandbox edit to scripts/run_small_pause_gate.py
    proc_deny_edit = subprocess.run(
        [sys.executable, str(gate_script)],
        input=json.dumps({
            "conversationId": sub_cid,
            "toolCall": {"name": "edit_file", "args": {"Path": "scripts/run_small_pause_gate.py"}},
        }),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    out_edit = json.loads(proc_deny_edit.stdout.strip())
    assert out_edit["decision"] == "deny"

    # 3. Allow write to Draft/cohort1_raw_draft.md
    proc_allow = subprocess.run(
        [sys.executable, str(gate_script)],
        input=json.dumps({
            "conversationId": sub_cid,
            "toolCall": {
                "name": "write_file",
                "args": {"Path": "Liturgical Monuments/mon1/Draft/mon1_cohort1_raw_draft.md"},
            },
        }),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    out_allow = json.loads(proc_allow.stdout.strip())
    assert out_allow["decision"] == "allow"


def test_discover_cohort_transcript_skips_adversarial_review_envelopes(tmp_path: Path) -> None:
    """Verifies Vector 7/11 transcript discovery ignores Boost <original_task>/<prior_attempt> review sessions."""
    brain_root = tmp_path / "brain"
    rev_log_dir = brain_root / "reviewer-session-001" / ".system_generated" / "logs"
    rev_log_dir.mkdir(parents=True)
    reviewer_step0 = {
        "step_index": 0,
        "source": "SYSTEM",
        "type": "USER_INPUT",
        "created_at": "2026-11-10T22:00:00Z",
        "content": "<original_task>Audit 1899_dolnytsky_typikon for cohort 15 (1899_dolnytsky_typikon_cohort15_raw_draft.md)</original_task><prior_attempt>Done</prior_attempt>",
    }
    (rev_log_dir / "transcript.jsonl").write_text(json.dumps(reviewer_step0) + "\n", encoding="utf-8")
    assert discover_cohort_subagent_transcript("1899_dolnytsky_typikon", 15, brain_dir=brain_root) is None

