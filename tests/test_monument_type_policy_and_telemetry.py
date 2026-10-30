#!/usr/bin/env python3
"""
Unit Tests for Monument-Type Policy, Signal 5 Codicological Crux Detection,
Next-Line Footnote Rescue, Quote-Protected Footnote Healing, and Telemetry Harvesting.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from orchestrator_state import (
    VALID_MONUMENT_TYPES,
    resolve_monument_type,
    load_monument_scaffold,
)
from run_small_pause_gate import (
    collect_argon_review_signals,
    run_monument_type_gate,
)
from compile_final_edition import (
    stitch_leaf_stream,
    heal_cohort_and_apparatus_text,
    format_liturgical_typography,
    slugify,
)
from hymnographic_gold_normalizer import stitch_2up_hymnographic_stream
from autonomous_orchestrator import _heal_monument_type_structure


def test_13_monument_types_and_registry_classification():
    assert len(VALID_MONUMENT_TYPES) == 13
    registry_path = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    monuments = registry.get("monuments", {})
    assert len(monuments) >= 132
    for m_id, m_cfg in monuments.items():
        m_type = m_cfg.get("monument_type")
        assert m_type in VALID_MONUMENT_TYPES, f"{m_id} has invalid monument_type={m_type}"
        scaffold = load_monument_scaffold(m_id, m_cfg)
        assert "gate_policy" in scaffold
        assert "allowed_h1_patterns" in scaffold
        assert "prompt_guardrails" in scaffold


def test_signal_5_codicological_crux_and_negation_guard(tmp_path: Path):
    draft_path = tmp_path / "cohort1.md"
    src_path = tmp_path / "src1.txt"
    fn_path = tmp_path / "fn1.txt"

    # Leaf p1: has genuine codicological crux in footnote -> QUEUED_FOR_ARGON
    # Leaf p2: has 10 footnotes with negated "without a catchword mismatch" and 0 cruxes -> INFO_TELEMETRY_ONLY
    draft_text = (
        "=== LEAF p1 ===\n"
        "Body text of leaf one with a physical collation anomaly.[^1]\n\n"
        "=== LEAF p2 ===\n"
        "Body text of leaf two with dense scholarly apparatus "
        + " ".join(f"[^{i}]" for i in range(2, 12))
        + "\n"
    )
    src_text = (
        "=== LEAF p1 ===\n"
        "Текст аркуша першого з фізичною колізією в кустоді.\n\n"
        "=== LEAF p2 ===\n"
        "Текст аркуша другого з багатьма примітками для перевірки.\n"
    )
    fn_lines = [
        "[^1]: There is a catchword mismatch between the bottom of fol. 1r and the top of fol. 1v.",
        "[^2]: Transitions smoothly onto fol. 2v without a catchword mismatch or missing folio.",
    ] + [f"[^{i}]: Standard patristic commentary note {i}." for i in range(3, 12)]

    draft_path.write_text(draft_text, encoding="utf-8")
    src_path.write_text(src_text, encoding="utf-8")
    fn_path.write_text("\n".join(fn_lines) + "\n", encoding="utf-8")

    collect_argon_review_signals(
        monument_id="test_trebnyk",
        cohort_num=1,
        ws=tmp_path,
        target_text=draft_path,
        source_file=src_path,
        footnotes_file=fn_path,
        fn_symmetry_passed=True,
        mon_info={"monument_type": "trebnyk_euchologion"},
    )
    q_data = json.loads((tmp_path / "Audit_Reports" / "argon_review_queue.json").read_text(encoding="utf-8"))
    by_leaf = {it["leaf_num"]: it for it in q_data["items"]}
    assert 1 in by_leaf
    assert by_leaf[1]["status"] == "QUEUED_FOR_ARGON"
    assert any("codicological_or_collation_crux" in r for r in by_leaf[1]["reasons"])

    assert 2 in by_leaf
    assert by_leaf[2]["status"] == "INFO_TELEMETRY_ONLY"
    assert all("codicological_or_collation_crux" not in r for r in by_leaf[2]["reasons"])


def test_next_line_footnote_rescue_in_stitchers():
    raw = (
        "=== LEAF p10 ===\n"
        "**[Left Page — Fol. 9v]**[^25]\n"
        "*Troparion:* O Lord, save Thy people.\n"
    )
    stitched, _ = stitch_leaf_stream(raw)
    assert "[^25]" in stitched
    assert "[Left Page" not in stitched

    stitched_2up, _ = stitch_2up_hymnographic_stream(raw)
    assert "[^25]" in stitched_2up
    assert "[Left Page" not in stitched_2up


def test_quote_protected_footnote_healing_and_dialogue_typography():
    fn_sample = (
        '[^732]: Anti-slop adherence: translated "Why" instead of banned "Wherefore".\n'
        '[^733]: Mandate adherence: "made marvelous" used instead of banned "wondrous".\n'
        '[^3249]: Prohibiting pseudo-archaic *wherefore*.\n'
        '[^3903]: Wednesday before Ascension (the Apodosis or Leave-taking of Pascha).\n'
    )
    healed_fn, _ = heal_cohort_and_apparatus_text(fn_sample, is_footnotes=True)
    assert 'banned "Wherefore"' in healed_fn
    assert 'banned "wondrous"' in healed_fn
    assert "pseudo-archaic *wherefore*" in healed_fn
    assert "Apodosis or Apodosis" not in healed_fn

    dlg = "**Priest:** For Thou art the King of peace, and unto Thee do we send up glory.[^15]"
    formatted = format_liturgical_typography(dlg)
    assert "King of peace" in formatted
    assert "[^15]" in formatted


def test_slugify_strips_html_and_cyrillic():
    h = 'ORDER OF HOLY BAPTISM <a id="чїнъ-крщенїа"></a> (Чїнъ крщенїа)[^10]'
    assert slugify(h) == "order-of-holy-baptism"


def test_monument_type_gate_and_auto_healer(tmp_path: Path):
    draft_path = tmp_path / "cohort_trebnyk.md"
    raw = (
        "=== LEAF p1 ===\n"
        "# PART I: THE ORDER OF HOLY BAPTISM\n\n"
        "*Priest:* Blessed is the Kingdom of the Father, and of the Son, and of the Holy Spirit.\n"
    )
    healed, mod = _heal_monument_type_structure(raw, "trebnyk_euchologion")
    assert mod is True
    assert "**Priest:** Blessed is the Kingdom" in healed
    draft_path.write_text(healed, encoding="utf-8")
    res = run_monument_type_gate("test_trebnyk", {"monument_type": "trebnyk_euchologion"}, draft_path)
    assert res["passed"] is True
