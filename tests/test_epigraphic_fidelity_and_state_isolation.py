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


def test_2up_seam_stitcher_bold_page_banners_and_overlap_dedup():
    from scripts.hymnographic_gold_normalizer import stitch_2up_hymnographic_stream

    sample_stream = """=== COHORT_BOUNDARY 1 ===
=== LEAF p10 ===
**[Left Page — Fol. 5v]**
We hymn the Savior and magnify the [first-enthroned bishop]. [^28]
=== COHORT_BOUNDARY 2 ===
=== LEAF p11 ===
**[Right Page — Fol. 6r]**
*(Dogmatikon, concluded):*
first-enthroned hierarch and the intercessor for our souls.
"""
    stitched, events = stitch_2up_hymnographic_stream(sample_stream)
    assert len(events) == 1
    assert "[f. 6rA]" in stitched
    assert "[^28]" in stitched
    assert "[first-enthroned bishop]" not in stitched
    assert "magnify the [^28] [f. 6rA] first-enthroned hierarch" in stitched


def test_rubric_to_h2_promotion_and_consolidated_weekday_h1_injection():
    from scripts.hymnographic_gold_normalizer import format_hymnographic_stanzas_and_headings

    sample_codex = """# TONE 8
*On Saturday evening, at "Lord, I have cried," Tone 8:*
Evening hymn text.
*On Sunday at Matins, Canon to the Holy and Life-Originating Trinity, Tone 8. Ode 1:*
Trinity canon text.
*At Matins, at "God is the Lord", the Sunday Troparion:*
Matins text.
*On Sunday, the Beatitudes, Tone 8:*
Beatitudes text.
*On Sunday Evening, at "Lord, I have cried," Penitential Stichera, Tone 8:*
Sunday evening text.
*On Monday at Matins, after the 1st Kathisma: Sessional Hymns, Tone 1:*
Monday matins text.
*On Monday evening, at "Lord, I have cried": Idiomelon Stichera, Tone 2:*
Monday evening text.
"""
    formatted = format_hymnographic_stanzas_and_headings(sample_codex)
    assert "## SATURDAY EVENING: VESPERS (TONE 8)" in formatted
    assert "## SUNDAY MIDNIGHT OFFICE (TONE 8)" in formatted
    assert "## SUNDAY MATINS (TONE 8)" in formatted
    assert "## SUNDAY LITURGY: THE BEATITUDES (TONE 8)" in formatted
    assert "## SUNDAY EVENING VESPERS (TONE 8)" in formatted
    assert "# WEEKDAY OFFICES OF THE OCTOECHOS (MONDAY THROUGH SATURDAY)" in formatted
    assert "## MONDAY MATINS: REPENTANCE AND THE BODILESS POWERS" in formatted
    assert "## MONDAY EVENING VESPERS (FOR TUESDAY)" in formatted


def test_3layer_podoben_normalization_and_scribal_truncation():
    from scripts.hymnographic_gold_normalizer import HymnographicNormalizer

    norm = HymnographicNormalizer()

    # 1. Scribal incipit truncation (e.g. 'По̀, Дв҃аа' vs 'Дѣ́ва дне́сь') -> SCRIBAL_INCIPIT_TRUNCATION, is_ai_drift=False
    line1, ev1 = norm.normalize_podoben_line(
        '*Podoben: "The Virgin" (По̀, Дв҃аа):*',
        ["Дв҃аа"],
        current_tone=3,
        c_idx=6,
        leaf_num=58,
    )
    assert '"Today the Virgin"' in line1
    assert ev1 is not None
    assert ev1["primitive_id"] == "POD.T3.DEVA_DNESS"
    assert ev1["drift_tier"] == "SCRIBAL_INCIPIT_TRUNCATION"
    assert ev1["is_ai_drift"] is False

    # 2. Scribe omitted Podoben label ('[Подо́бенъ:] И҆́же менера́ди') + translator used 'Prosomoion:' -> is_ai_drift=True
    line2, ev2 = norm.normalize_podoben_line(
        "*Sessional Hymn, Tone 7. Prosomoion: He Who for my sake:*",
        ["[Подо́бенъ:] И҆́же менера́ди"],
        current_tone=7,
        c_idx=17,
        leaf_num=165,
    )
    assert '*Podoben: "He Who for my sake" ([Подо́бенъ:] И҆́же менера́ди):*' in line2
    assert ev2 is not None
    assert ev2["scribal_omitted_label"] is True
    assert ev2["is_ai_drift"] is True

    # 3. Nekrosimon -> *Hymn for the Departed (Поко́инъ):*
    line3, ev3 = norm.normalize_podoben_line(
        "*Nekrosimon:* [^274]",
        [],
        current_tone=6,
        c_idx=27,
        leaf_num=266,
    )
    assert line3 == "*Hymn for the Departed (Поко́инъ):* [^274]"
    assert ev3 is not None
    assert ev3["type"] == "POKOIN_ABBREV_CORRECTED"


def test_5rule_seam_deduplication_and_anaphora_guard():
    from scripts.hymnographic_gold_normalizer import deduplicate_seam_overlap

    # Rule 0: Hyphenated word split across seam
    p0, c0 = deduplicate_seam_overlap("Who upon virginal ha- [^10]", "nds borne on high")
    assert p0 == "Who upon virginal hands [^10]"
    assert c0 == "borne on high"

    # Rule 1: Mid-phrase bracketed catchword
    p1, c1 = deduplicate_seam_overlap(
        "and we anoint thee, [first-enthroned bishop] of the people of Myra",
        "first-enthroned bishop, and intercessor for our souls.",
    )
    assert "[first-enthroned bishop]" not in p1
    assert "anoint thee," in p1

    # Rule 4b: Opening sub-clause repeating previous clause
    p4, c4 = deduplicate_seam_overlap(
        "save those who put their trust in thee,",
        "save those who put their trust in thee, O only all-hymned Mother.",
    )
    assert c4 == "O only all-hymned Mother."

    # Anaphora Guard: Do not trim legitimate 'Rejoice...' refrains
    pa, ca = deduplicate_seam_overlap(
        "Rejoice, O unwedded Bride!",
        "Rejoice, O unwedded Bride, salvation of the faithful.",
    )
    assert ca.startswith("Rejoice, O unwedded Bride")


def test_universal_cohort_and_apparatus_healer():
    from scripts.compile_final_edition import heal_cohort_and_apparatus_text

    raw_body = (
        "\ufeff[17th-century marginalia: \"сто рословъ нинець\" (one hundred words)]\n"
        "*Nekrosimon:*\n"
        "He showeth mercy and trampleth down death, as Thou art God Who hast risen<sup>1</sup>.\n"
    )
    healed_body, mod_b = heal_cohort_and_apparatus_text(raw_body, is_footnotes=False)
    assert mod_b is True
    assert not healed_body.startswith("\ufeff")
    assert '"one hundred words" (*сто рословъ нинець*)' in healed_body
    assert "*Hymn for the Departed (Поко́инъ):*" in healed_body
    assert "shows mercy and tramples down death" in healed_body
    assert "Thou art God Who hast risen¹." in healed_body

    raw_fn = "[^9]: The Irmos and Sedalen and Apolytikion form a poignant beacon of hope for the Nekrosimon."
    healed_fn, mod_f = heal_cohort_and_apparatus_text(raw_fn, is_footnotes=True)
    assert mod_f is True
    assert "Irmos" not in healed_fn
    assert "Sedalen" not in healed_fn
    assert "Apolytikion" not in healed_fn
    assert "poignant" not in healed_fn
    assert "beacon of" not in healed_fn
    assert "Hymn for the Departed (Поко́инъ)" in healed_fn


def test_grand_pause_requires_explicit_human_signoff():
    from scripts.autonomous_orchestrator import approve_grand_pause

    res = approve_grand_pause(monument_id="1629_kyiv_octoechos", push_to_git=False, confirm_human_signoff=False)
    assert res["status"] == "BLOCKED_AWAITING_HUMAN_SIGNOFF"


