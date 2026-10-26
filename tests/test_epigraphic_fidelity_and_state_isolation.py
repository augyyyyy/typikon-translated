import pytest
import json
from pathlib import Path

from scripts.structural_audit import audit_structure
from scripts.autonomous_orchestrator import _heal_epigraphic_headings, load_registry
from scripts.orchestrator_state import load_state, save_state, resolve_monument_id, get_state_file_path


def test_epigraphic_heading_linter_catches_fabrications(tmp_path):
    # Create draft with fabricated headings
    draft_file = tmp_path / "test_cohort_raw_draft.md"
    content = """=== LEAF p32 ===
## At Sunday Midnight Office
### Canon to the Most Holy Trinity, Tone 2[^37]
#### Ode 1
*Heirmos:* Of old, the all-armed power...
"""
    draft_file.write_text(content, encoding="utf-8")

    res = audit_structure(draft_file, cohort_num=4, monument_id="1629_kyiv_octoechos")
    assert not res["passed"]
    anomalies = " ".join(res["anomalies"])
    assert "PRE_TRAINING_DATA_INCURSION" in anomalies
    assert "EPIGRAPHIC_HEADING_VIOLATION" in anomalies
    assert "At Sunday Midnight Office" in anomalies


def test_epigraphic_heading_linter_passes_woodcut_h1(tmp_path):
    draft_file = tmp_path / "test_cohort_raw_draft.md"
    content = """=== LEAF p1 ===
[Binding description]

=== LEAF p2 ===
# PREFACE: TO THE READER
Know, O pious reader...

=== LEAF p3 ===
# TONE 1
*In the Book of the Octoechos, of the Resurrection. Tone 1:*
Accept our evening prayers, O holy Lord...
"""
    draft_file.write_text(content, encoding="utf-8")

    res = audit_structure(draft_file, cohort_num=1, monument_id="1629_kyiv_octoechos")
    assert res["passed"]
    assert res["headings_count"] == 2
    assert len(res["anomalies"]) == 0


def test_source_aware_heading_self_healing(tmp_path):
    registry = load_registry()
    mon_info = registry["monuments"]["1629_kyiv_octoechos"]

    src_file = tmp_path / "test_source.txt"
    src_file.write_text("=== LEAF p32 ===\nПѣ́снь а҃ , гла́съ в҃ . І҆рмо́съ .\nВо глубинѣ̀ потопѝ...", encoding="utf-8")

    draft_txt = """=== LEAF p32 ===
## At Sunday Midnight Office
### Canon to the Most Holy Trinity, Tone 2[^37]
#### Ode 1
*Heirmos:* Of old, the all-armed power drowned the whole host...
"""
    healed, mod = _heal_epigraphic_headings(draft_txt, src_file, mon_info)
    assert mod is True
    # Pure office hallucination stripped
    assert "At Sunday Midnight Office" not in healed
    # Footnote [^37] re-anchored to the healed rubric line
    assert "[^37]" in healed
    # All ## and ### headings eliminated
    assert not any(l.startswith("#") for l in healed.splitlines())


def test_monument_state_isolation():
    # Verify Monument 8 and Monument 9 resolve to independent isolated files
    p8 = get_state_file_path("1629_kyiv_octoechos")
    p9 = get_state_file_path("1630_lviv_octoechos")
    assert p8 != p9
    assert "Monument 8 - 1629 Kyiv Octoechos" in str(p8)
    assert "Monument 9 - 1630 Lviv Octoechos" in str(p9)

    st8 = load_state("1629_kyiv_octoechos")
    st9 = load_state("1630_lviv_octoechos")
    assert st8["monument_id"] == "1629_kyiv_octoechos"
    assert st9["monument_id"] == "1630_lviv_octoechos"
    assert st9["small_pause_gate_status"] == "MONUMENT_SEALED_AND_HANDED_OFF"
    assert st8["small_pause_gate_status"] in ("READY_FOR_NEXT_COHORT", "GRAND_PAUSE_READY_FOR_HUMAN_INSPECTION", "MONUMENT_SEALED_AND_HANDED_OFF")
