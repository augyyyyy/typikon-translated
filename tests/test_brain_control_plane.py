#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regression test suite for the Translation Spoke Brain Control Plane:
1. .agents/AGENTS.md byte budget (< 16,000 B), Rules 1..22 completeness, and zero backslashes.
2. Progressive-disclosure skills (.agents/skills/*/SKILL.md < 4,000 B + references/*.md) and total .agents/ < 250 KB.
3. Relocation and sanitization of Audit_Reports/ARTIFACT_REGISTRY.md (zero root stub, zero null bytes, zero backslashes).
4. .agents/scripts/governance_gate.py Line-0 subagent detection (preventing false-positive sandboxing when reading AGENTS.md).
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
AGENTS_DIR = PROJECT_ROOT / ".agents"
AGENTS_MD = AGENTS_DIR / "AGENTS.md"
SKILLS_DIR = AGENTS_DIR / "skills"
GOVERNANCE_GATE = AGENTS_DIR / "scripts" / "governance_gate.py"

EXPECTED_SKILLS = {
    "monument_translation_orchestrator": [
        "bookend_routing_and_concurrency.md",
        "house_style_and_work_order_mandates.md",
        "drive_e_vault_and_extraction.md",
        "rerun_vs_patch_and_autopsy.md",
    ],
    "liturgical_glossary_enforcer": [
        "mts1_registers_and_realia.md",
        "anti_slop_and_pronoun_gates.md",
    ],
    "liturgical_text_auditor": [
        "chunking_and_alignment_rules.md",
    ],
    "liturgical_vision_auditor": [
        "footnote_bijectivity_and_layout.md",
        "sgc_potemkin_and_publication_gates.md",
    ],
    "poetic_hymn_translator": [
        "sgc06_tabula_rasa_and_podoben_grid.md",
    ],
}

HARDCODED_WIN_PATH_RE = re.compile(r"(?<![A-Za-z])[A-Za-z]:\\(?![ntrsdwbB+*?])")


def test_agents_md_compression_and_rules_1_to_22_completeness() -> None:
    assert AGENTS_MD.is_file(), ".agents/AGENTS.md must exist"
    raw_bytes = AGENTS_MD.read_bytes()
    size_bytes = len(raw_bytes)
    assert size_bytes < 16000, (
        f".agents/AGENTS.md must be strictly < 16,000 bytes (got {size_bytes} B) "
        f"to prevent truncation at Antigravity's 24,000-byte cliff."
    )

    text = raw_bytes.decode("utf-8")
    for rule_num in range(1, 23):
        pat = re.compile(rf"###\s+{rule_num}\.\s+")
        assert pat.search(text), f"Rule {rule_num} heading ('### {rule_num}. ') missing from .agents/AGENTS.md"

    # Required ecosystem Gate 1 tokens
    for required_token in (
        "GLOBAL_SYSTEM_RULES.md",
        "Exclusive Write-Ownership Matrix",
        "SGC-01",
        "SGC-06",
        "verify_ecosystem_integrity.py",
    ):
        assert required_token in text, f"Required governance token '{required_token}' missing from .agents/AGENTS.md"

    # Zero backslashes and zero hardcoded Windows drive paths
    assert "\\" not in text, ".agents/AGENTS.md must contain zero backslash characters"
    assert not HARDCODED_WIN_PATH_RE.search(text)


def test_progressive_disclosure_skills_and_total_agents_budget() -> None:
    assert SKILLS_DIR.is_dir(), ".agents/skills/ directory must exist"

    discovered_skills = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}
    assert discovered_skills == set(EXPECTED_SKILLS.keys()), (
        f"Expected skills {set(EXPECTED_SKILLS.keys())}, found {discovered_skills}"
    )

    for skill_name, expected_refs in EXPECTED_SKILLS.items():
        skill_dir = SKILLS_DIR / skill_name
        skill_md = skill_dir / "SKILL.md"
        assert skill_md.is_file(), f"Missing {skill_name}/SKILL.md"

        skill_bytes = skill_md.read_bytes()
        assert 500 <= len(skill_bytes) < 4000, (
            f"{skill_name}/SKILL.md must be strictly < 4,000 bytes (got {len(skill_bytes)} B)"
        )

        skill_text = skill_bytes.decode("utf-8")
        assert skill_text.startswith("---\n"), f"{skill_name}/SKILL.md must start with YAML frontmatter"
        fm_end = skill_text.find("\n---\n", 4)
        assert fm_end != -1, f"{skill_name}/SKILL.md must close YAML frontmatter with '---'"
        frontmatter = skill_text[4:fm_end]
        assert f"name: {skill_name}" in frontmatter
        assert "description:" in frontmatter

        # Ensure Class 1 DeepSeek orchestration and 1899 hallucination defects remain purged
        for line in skill_text.splitlines():
            low = line.lower()
            if "deepseek" in low:
                assert any(
                    ban_kw in low for ban_kw in ("prohibit", "prohibited", "ban", "banned", "forbid", "never")
                ), f"Unbanned DeepSeek reference in {skill_name}/SKILL.md: {line}"
        assert "1899 edition" not in skill_text.lower()
        assert not HARDCODED_WIN_PATH_RE.search(skill_text)

        ref_dir = skill_dir / "references"
        assert ref_dir.is_dir(), f"Missing references/ directory in {skill_name}"
        for ref_name in expected_refs:
            ref_path = ref_dir / ref_name
            assert ref_path.is_file(), f"Missing reference file {skill_name}/references/{ref_name}"
            ref_text = ref_path.read_text(encoding="utf-8")
            assert len(ref_text) >= 500
            assert not HARDCODED_WIN_PATH_RE.search(ref_text)
            assert f"references/{ref_name}" in skill_text, (
                f"{skill_name}/SKILL.md must link to references/{ref_name}"
            )

    total_agents_bytes = sum(
        p.stat().st_size for p in AGENTS_DIR.rglob("*") if p.is_file() and p.name != "desktop.ini"
    )
    assert total_agents_bytes < 250000, (
        f"Total .agents/ directory size must be < 250,000 bytes (got {total_agents_bytes} B)"
    )


def test_artifact_registry_relocated_and_sanitized() -> None:
    root_registry = PROJECT_ROOT / "ARTIFACT_REGISTRY.md"
    relocated_registry = PROJECT_ROOT / "Audit_Reports" / "ARTIFACT_REGISTRY.md"

    assert not root_registry.exists(), "ARTIFACT_REGISTRY.md must not exist at workspace root (zero root stub)"
    assert relocated_registry.is_file(), "Audit_Reports/ARTIFACT_REGISTRY.md must exist"

    raw = relocated_registry.read_bytes()
    assert b"\x00" not in raw, "Audit_Reports/ARTIFACT_REGISTRY.md must contain zero null bytes (\\x00)"
    text = raw.decode("utf-8")
    assert "Master Historical Artifact Registry" in text
    assert not HARDCODED_WIN_PATH_RE.search(text), (
        "Audit_Reports/ARTIFACT_REGISTRY.md must have zero Windows backslash paths"
    )

    chronicle_text = (PROJECT_ROOT / "CHRONICLE.md").read_text(encoding="utf-8")
    assert "Audit_Reports/ARTIFACT_REGISTRY.md" in chronicle_text
    assert "## Chapter 5:" in chronicle_text
    assert "Marker 3.0: Brain Control-Plane & Progressive-Disclosure Overhaul" in chronicle_text
    assert "Zero Switch Test Monument" not in chronicle_text, (
        "CHRONICLE.md must not be polluted by unsandboxed pytest fixtures"
    )
    assert "\\" not in chronicle_text, "CHRONICLE.md must contain zero backslash characters"


def test_governance_gate_line0_prevents_false_positive_sandboxing(tmp_path: Path) -> None:
    brain_root = tmp_path / "brain"
    env = dict(**os.environ, ANTIGRAVITY_BRAIN_DIR=str(brain_root))

    # Case 1: Non-worker subagent (e.g. Argon / boost investigator) whose Line 0 is a general task,
    # but whose Line 1/2 ingested .agents/AGENTS.md containing "ephemeral_translator" and "work_order_cohort_".
    investigator_cid = "subagent-investigator-001"
    inv_log_dir = brain_root / investigator_cid / ".system_generated" / "logs"
    inv_log_dir.mkdir(parents=True)
    inv_steps = [
        {
            "step_index": 0,
            "source": "SYSTEM",
            "content": "You are DeepInvestigator auditing the Translation control plane.",
        },
        {
            "step_index": 1,
            "source": "TOOL",
            "content": (
                "Read .agents/AGENTS.md: ephemeral_translator executes work_order_cohort_1.md "
                "and writes _raw_draft.md under Statutory Mandates 1-13."
            ),
        },
    ]
    (inv_log_dir / "transcript_full.jsonl").write_text(
        "\n".join(json.dumps(s) for s in inv_steps) + "\n",
        encoding="utf-8",
    )

    proc_inv = subprocess.run(
        [sys.executable, str(GOVERNANCE_GATE)],
        input=json.dumps({
            "conversationId": investigator_cid,
            "toolCall": {"name": "edit_file", "args": {"Path": ".agents/AGENTS.md"}},
        }),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    out_inv = json.loads(proc_inv.stdout.strip())
    assert out_inv["decision"] == "allow", (
        f"Non-worker subagent reading AGENTS.md on step 1 must NOT be sandboxed (got {out_inv})"
    )

    # Case 2: Edge case where Line 0 has step_index != 0 -> must NOT crash or false-lock
    edge_cid = "subagent-edge-002"
    edge_log_dir = brain_root / edge_cid / ".system_generated" / "logs"
    edge_log_dir.mkdir(parents=True)
    (edge_log_dir / "transcript.jsonl").write_text(
        json.dumps({"step_index": 2, "content": "You are ephemeral_translator"}) + "\n",
        encoding="utf-8",
    )
    proc_edge = subprocess.run(
        [sys.executable, str(GOVERNANCE_GATE)],
        input=json.dumps({
            "conversationId": edge_cid,
            "toolCall": {"name": "edit_file", "args": {"Path": ".agents/AGENTS.md"}},
        }),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    out_edge = json.loads(proc_edge.stdout.strip())
    assert out_edge["decision"] == "allow"

    # Case 3: /boost Reviewer/Worker subagent whose step_index == 0 <original_task> or <prior_attempt>
    # quotes WORKER_DISPATCH_SIGNATURES -> must NOT be falsely sandboxed!
    boost_cid = "subagent-boost-reviewer-003"
    boost_log_dir = brain_root / boost_cid / ".system_generated" / "logs"
    boost_log_dir.mkdir(parents=True)
    (boost_log_dir / "transcript_full.jsonl").write_text(
        json.dumps({
            "step_index": 0,
            "source": "SYSTEM",
            "content": (
                "<original_task>Harden governance_gate.py for 'you are ephemeral_translator' "
                "and 'execute the work order at:'</original_task>\n"
                "<prior_attempt>Updated WORKER_DISPATCH_SIGNATURES for context-sequestered "
                "liturgical scribe and translator.</prior_attempt>\n"
                "<instructions>Review the prior attempt.</instructions>"
            ),
        }) + "\n",
        encoding="utf-8",
    )
    proc_boost = subprocess.run(
        [sys.executable, str(GOVERNANCE_GATE)],
        input=json.dumps({
            "conversationId": boost_cid,
            "toolCall": {"name": "edit_file", "args": {"Path": ".agents/scripts/governance_gate.py"}},
        }),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    out_boost = json.loads(proc_boost.stdout.strip())
    assert out_boost["decision"] == "allow", (
        f"/boost reviewer subagent quoting WORKER_DISPATCH_SIGNATURES in <prior_attempt> must NOT be sandboxed (got {out_boost})"
    )

    # Case 4: Flash Retry subagent (TARGETED FLASH RETRY and DELTA-ONLY CONTINUATION RETRY) -> MUST be sandboxed!
    for idx, retry_header in enumerate((
        "TARGETED FLASH RETRY (Attempt 1/1) for 1630 Lviv Octoechos — Cohort 1 (leaves p1..p10).",
        "DELTA-ONLY CONTINUATION RETRY (Attempt 1/1) for 1630 Lviv Octoechos — Cohort 1.",
    )):
        retry_cid = f"subagent-flash-retry-00{idx + 4}"
        retry_log_dir = brain_root / retry_cid / ".system_generated" / "logs"
        retry_log_dir.mkdir(parents=True)
        (retry_log_dir / "transcript_full.jsonl").write_text(
            json.dumps({
                "step_index": 0,
                "source": "SYSTEM",
                "content": retry_header,
            }) + "\n",
            encoding="utf-8",
        )
        proc_retry = subprocess.run(
            [sys.executable, str(GOVERNANCE_GATE)],
            input=json.dumps({
                "conversationId": retry_cid,
                "toolCall": {"name": "search_web", "args": {"query": "slavonic octoechos"}},
            }),
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        out_retry = json.loads(proc_retry.stdout.strip())
        assert out_retry["decision"] == "deny", (
            f"Flash retry worker ({retry_header[:30]}...) MUST be sandboxed against search_web (got {out_retry})"
        )

