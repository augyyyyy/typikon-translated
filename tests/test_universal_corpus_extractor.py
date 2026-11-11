#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit & Integration Tests for Universal Atomic Liturgical Corpus Extractor
and 1-Up / 2-Up Podoben Grid Coordinate Resolution.
"""

from __future__ import annotations

import json
from pathlib import Path

from scripts.generate_podoben_grid import extract_podoben_grid_data, match_podoben_model
from scripts.hymnographic_gold_normalizer import generate_propers_corpus
from scripts.universal_corpus_extractor import (
    VALID_UNIT_CLASSES,
    align_bilingual_leaf_blocks,
    classify_attestation_mode,
    detect_office_slug_from_text,
    detect_section_slug_from_text,
    extract_monument_atomic_corpus,
    is_pure_italic_rubric,
    load_primitives_data,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_podoben_grid_zero_p1_clamping_and_zero_unknowns() -> None:
    """Verifies that 1-up and 2-up Octoechoi resolve multi-leaf coordinates and zero UNKNOWN models."""
    for mon_id, min_leaves in (
        ("1895_lviv_octoechos", 100),
        ("1491_krakow_fiol_octoechos", 30),
        ("1600s_prykarpattia_ms_octoechos", 10),
        ("1630_lviv_octoechos", 80),
    ):
        invocations, summary, _, _ = extract_podoben_grid_data(mon_id)
        assert len(invocations) >= 20
        unique_leaves = {inv["leaf"] for inv in invocations}
        assert len(unique_leaves) >= min_leaves, f"{mon_id} clamped to {len(unique_leaves)} leaves"
        unknowns = [inv for inv in invocations if "UNKNOWN" in inv["model_id"]]
        assert not unknowns, f"{mon_id} produced UNKNOWN models: {unknowns[:3]}"
        assert len(summary["tones_represented"]) >= 5
        for inv in invocations[:10]:
            assert "byzantine_greek_automelon" not in inv


def test_match_podoben_model_aliases_slavonic_and_dynamic_minting() -> None:
    """Verifies English alias matching, Slavonic Tier-2 stem matching, and dynamic EXT_ minting."""
    pod_catalog, _ = load_primitives_data()

    # English alias + abbreviated Slavonic witness
    m_id, title, _ = match_podoben_model(
        '*Tone 1, Podoben: "Thy tomb, O Savior" (Гро́бъ тво́й Сп҃се):*',
        "Гро́бъ тво́й Сп҃се",
        1,
        pod_catalog,
    )
    assert m_id == "POD.T1.GROB_TVOI_SPASE"
    assert title == "While the soldiers were guarding Thy tomb"

    # Extended Pan-Byzantine Automelon ('Joseph was amazed' / 'Удивися Иосиф')
    m_id2, title2, greek2 = match_podoben_model(
        '*Theotokion, Tone 4, Podoben: "Joseph marveled" (Удивися Иосиф):*',
        "Удивися Иосиф",
        4,
        pod_catalog,
    )
    assert m_id2 == "POD.T4.UDIVISIA_IOSIF"
    assert greek2 == "Κατεπλάγη Ἰωσήφ"

    # Dynamic minting for custom Triodion/Pentecostarion Automelon
    m_id3, title3, _ = match_podoben_model(
        '*Tone 6, Podoben: "Today the grace of the Spirit" (Днесь благодать):*',
        "Днесь благодать",
        6,
        pod_catalog,
    )
    assert m_id3.startswith("POD.T6.EXT_")
    assert title3 == "Today the grace of the Spirit"


def test_t1_anchor_synchronized_bilingual_leaf_aligner() -> None:
    """Verifies T-1: English editorial notes or rubrics do not shift Slavonic hymn blocks, and unmatched blocks get None."""
    eng_blocks = [
        {"text": '*On "Lord, I have cried", Stichera, Tone 1, Podoben: "O all-lauded Martyrs":*'},
        {"text": "[Editorial Note: Missing initial capital in folio]"},
        {"text": "*Another rubric inserted in translation only.*"},
        {"text": "Accept our evening prayers, O holy Lord, and grant us remission of sins."},
        {"text": "**Glory... Both now...** *Theotokion:*"},
        {"text": "Let us hymn the Virgin Mary, the glory of the whole world."},
        {"text": "Trailing unmatched English block on leaf boundary."},
    ]
    slav_blocks = [
        {"text": "На Гд҃и воззва́хъ поста́вимъ стїхѡ́въ ѕ҃, гла́съ а҃. Подо́бенъ: Всехва́льнїи мч҃ницы:"},
        {"text": "Вече́рняя на́ша мл҃твы прїими́, ст҃ы́й Гд҃и, и пода́ждь на́мъ ѡставле́нїе грѣхѡ́въ."},
        {"text": "Сла́ва, и ны́нѣ, Бг҃оро́диченъ: Всемї́рную сла́ву, ѿ человѣ́къ прозя́бшую."},
    ]
    aligned = align_bilingual_leaf_blocks(slav_blocks, eng_blocks)
    assert len(aligned) == len(eng_blocks)
    # Rubric aligns to Slavonic rubric
    assert aligned[0] is not None and "На Гд҃и воззва́хъ" in aligned[0]["text"]
    # Editorial note and translation-only rubric do NOT consume Slavonic hymn stanzas
    assert aligned[1] is None
    assert aligned[2] is None
    # First hymn stanza aligns to "Вечерняя наша молитвы"
    assert aligned[3] is not None and "Вече́рняя на́ша" in aligned[3]["text"]
    # Doxology / Theotokion aligns to "Слава, и ныне"
    assert (aligned[4] is not None and "Сла́ва" in aligned[4]["text"]) or (
        aligned[5] is not None and "Всемї́рную сла́ву" in aligned[5]["text"]
    )
    # Unmatched trailing block gets None instead of repeating s_list[-1]
    assert aligned[6] is None


def test_t2_and_t4_procedural_detectors_and_italic_rubric_filtering() -> None:
    """Verifies T-2 inline italic office/section detection and T-4 safe multi-line italic rubric filtering."""
    assert detect_office_slug_from_text("*At Great Vespers*") == "vespers"
    assert detect_office_slug_from_text("*On Saturday Evening at Little Vespers*") == "sat_vespers"
    assert detect_office_slug_from_text("*On Sunday Morning, at Matins*") == "sun_matins"
    assert detect_office_slug_from_text("**AT GREAT VESPERS**") == "vespers"
    assert detect_section_slug_from_text('*On "Lord, I have cried", we insert 6 Stichera:*')[0] == "stichera_lord_i_call"
    assert detect_section_slug_from_text('*At "Lord, I call:" Stichera of the Resurrection, Tone 3:*')[0] == "stichera_lord_i_call"
    assert detect_section_slug_from_text("*Resurrectional Stichera. Tone 1:*")[0] == "stichera_lord_i_call"
    assert detect_section_slug_from_text("*At the Litiya, Stichera:*")[0] == "stichera_litiya"
    assert detect_section_slug_from_text("*At the Aposticha, Stichera of the Resurrection:*")[0] == "stichera_aposticha"
    assert detect_section_slug_from_text("*At the Praises, 4 Stichera:*")[0] == "stichera_praises"
    assert detect_section_slug_from_text("*Ode 3. Heirmos:*") == ("canon_ode_3", "Canon — Ode 3", 3)
    assert detect_section_slug_from_text("*Sessional Hymn, Tone 4:*")[0] == "sessionals"
    assert detect_section_slug_from_text("*Kontakion, Tone 2:*")[0] == "kontakion_ikos"

    # T-4: Multi-line italic rubric with trailing footnote or continuation -> True
    assert is_pure_italic_rubric(
        "*If the Nativity of the Forerunner falls on Sunday,\nwe sing the Resurrectional Stichera first, and then those of the Forerunner.* [^12]"
    )
    assert is_pure_italic_rubric(
        "*Wait for the Priest to exclaim:* (cont. on fol. 2r)"
    )
    # T-4: Two-span italic role + italic hymn body -> False (must remain PROPER_HYMN)
    assert not is_pure_italic_rubric(
        "*Theotokion:* *O pure Mother of God, forsake us not in our afflictions, but intercede for our souls.*"
    )
    assert not is_pure_italic_rubric(
        "*Ode 1. Heirmos:* *Having passed through the water as upon dry land, Israel escaped the malice of Egypt.*"
    )
    # T-4: Plain hymn text with trailing italic refrain -> False
    assert not is_pure_italic_rubric(
        "Come, O faithful, let us worship the life-creating Cross of the Lord. *Twice.*"
    )

    # Attestation mode classification (T-6)
    assert classify_attestation_mode('**"God is the Lord"** *and the Troparion.*') == "INCIPIT_ONLY_POINTER"
    assert classify_attestation_mode("See above on the first Sunday of Lent.") == "DELEGATED_TO_COMMON"
    assert classify_attestation_mode("Accept our evening prayers, O holy Lord, and grant us remission of sins.") == "ATTESTED_FULL"


def test_universal_extractor_horologion_and_liturgikon_5_classes() -> None:
    """Verifies 5-class extraction, 4-shard routing, v4.0.0 schema, and SGC-02 dual provenance."""
    hor_payload = extract_monument_atomic_corpus("1491_krakow_fiol_horologion", sync_hub=False)
    assert hor_payload["corpus_schema"] == "4.0.0"
    hor_units = hor_payload["units"]
    assert len(hor_units) > 500
    hor_classes = hor_payload["summary"]["counts_by_unit_class"]
    assert hor_classes["PROPER_HYMN"] > 100
    assert hor_classes["RUBRIC_OR_STATUTE"] > 100

    lit_payload = extract_monument_atomic_corpus("1604_striatyn_balaban_liturgikon", sync_hub=False)
    assert lit_payload["corpus_schema"] == "4.0.0"
    lit_units = lit_payload["units"]
    assert len(lit_units) > 500
    lit_classes = lit_payload["summary"]["counts_by_unit_class"]
    assert lit_classes["SACERDOTAL_PRAYER"] >= 50
    assert lit_classes["LITANY_OR_DIALOGUE"] >= 200
    assert lit_classes["RUBRIC_OR_STATUTE"] >= 200

    valid_shards = {
        "01_ordinarium_primitives.json",
        "02_sticherarion.json",
        "03_irmologion.json",
        "04_kanonnik.json",
    }
    valid_att = {"ATTESTED_FULL", "INCIPIT_ONLY_POINTER", "DELEGATED_TO_COMMON"}
    for u in lit_units[:50] + hor_units[:50]:
        assert u["unit_class"] in VALID_UNIT_CLASSES
        assert u["target_shard"] in valid_shards
        assert u["physical_unit_id"] == u["corpus_id"]
        assert "internal_coordinates" in u
        assert u["attestation_mode"] in valid_att
        assert "structural_id" not in u
        assert "greek_incipit" not in u
        prov = u["cohort_provenance"]
        assert len(prov["source_sha256"]) == 64
        assert prov["source_format"] == "TEXT_LINES"
        assert prov["start_line"] >= 1
        assert prov["end_line"] >= prov["start_line"]
        assert len(prov["verbatim_source"]) > 0
        if u.get("slavonic_diplomatic"):
            s_prov = u["slavonic_provenance"]
            assert s_prov is not None
            assert len(s_prov["source_sha256"]) == 64
            assert s_prov["source_format"] == "TEXT_LINES"
            assert s_prov["start_line"] >= 1
            assert s_prov["end_line"] >= s_prov["start_line"]
            assert len(s_prov["verbatim_source"]) > 0


def test_t3_t5_t9_octoechos_and_typikon_tabula_rasa_purity() -> None:
    """Verifies T-3 Octoechos overwrite, T-4 Typikon zero propers, and T-5..T-9 front-matter exclusion & SGC-06 purity."""
    # T-4: Typikon produces zero PROPER_HYMN units
    typ_payload = extract_monument_atomic_corpus("1899_dolnytsky_typikon", sync_hub=False)
    assert typ_payload["summary"]["counts_by_unit_class"]["PROPER_HYMN"] == 0

    # T-3 + T-5..T-9: 1630 Lviv Octoechos propers regeneration via normalizer convergence
    propers_payload = generate_propers_corpus("1630_lviv_octoechos")
    assert propers_payload["corpus_schema"] == "4.0.0"
    items = propers_payload["items"]
    assert len(items) > 1000
    p7_items = [it for it in items if it["leaf"] == "p7"]
    # Leaf p7 has 7 Stichera on Lord I have cried (3 Resurrectional + 4 Anatolian), each 100% aligned to Slavonic
    assert len(p7_items) == 7, f"Expected 7 Stichera on p7 of 1630_lviv_octoechos, got {len(p7_items)}"
    assert all(it["slavonic_diplomatic"] for it in p7_items)
    assert "Вече" in p7_items[0]["slavonic_diplomatic"]
    for it in items:
        # T-8: Zero front-matter leaves p1..p6 in 1630 Lviv Octoechos propers
        leaf_num = int(str(it["leaf"]).lstrip("p"))
        assert leaf_num >= 7, f"Front-matter paratext leaked on leaf {it['leaf']}: {it['physical_unit_id']}"
        assert it["physical_unit_id"].startswith("OCT.1630_LVIV_OCTOECHOS.")
        assert "internal_coordinates" in it
        assert str(it["internal_coordinates"]["local_slot_suffix"]).startswith("_")
        assert it["attestation_mode"] in ("ATTESTED_FULL", "INCIPIT_ONLY_POINTER", "DELEGATED_TO_COMMON")
        assert "cohort_provenance" in it
        assert "structural_id" not in it
        assert "greek_incipit" not in it

    # Level A (same-column uppercase-initial separation) & Level B (Option 2B 1:2 sub-slicing) on p9
    by_id = {it["physical_unit_id"]: it for it in items}
    u12 = by_id["OCT.1630_LVIV_OCTOECHOS.C001.P0009.U012"]
    u13 = by_id["OCT.1630_LVIV_OCTOECHOS.C001.P0009.U013"]
    assert "Заченши" in u12["slavonic_diplomatic"]
    assert "Ты бѡ еси" in u13["slavonic_diplomatic"]
    assert u12["slavonic_provenance"]["start_line"] == u13["slavonic_provenance"]["start_line"]
    assert u12["slavonic_provenance"]["end_line"] == u13["slavonic_provenance"]["end_line"]

    u18 = by_id["OCT.1630_LVIV_OCTOECHOS.C001.P0009.U018"]
    u19 = by_id["OCT.1630_LVIV_OCTOECHOS.C001.P0009.U019"]
    assert "Внегда скорбѣти ми" in u18["slavonic_diplomatic"]
    assert "Пустыннымъ непрестанно" in u19["slavonic_diplomatic"]
    assert u18["slavonic_provenance"]["start_line"] == 435
    assert u19["slavonic_provenance"]["start_line"] == 436


def test_option_2b_unit_sub_slicing_and_ready_metadata() -> None:
    """Verifies Option 2B punctuation-anchored 1:2 sub-slicing in align_bilingual_leaf_blocks() and resolve_monument_year()."""
    from scripts.universal_corpus_extractor import (
        CANONICAL_RECENSION_WITNESS_ID,
        CANONICAL_WITNESS_PRIORITY_ORDER,
        resolve_monument_recension_stratum,
        resolve_monument_year,
    )

    assert resolve_monument_year("1630_lviv_octoechos", {"title": "Lviv Printed Octoechos (1630)"}) == 1630
    assert resolve_monument_year("1600s_prykarpattia_ms_octoechos", {"title": "Prykarpattia MS"}) == 1600

    s_1630 = resolve_monument_recension_stratum("1630_lviv_octoechos", {"title": "Lviv Printed Octoechos (1630)"})
    assert s_1630["canonical_recension_witness_id"] == "kyivan_ruthenian_critical"
    assert s_1630["historical_stratum"] == "PRE_NIKONIAN_KYIVAN_STAUROPEGION"
    assert s_1630["stratum_witness_id"] == "kyivan_prenikonian_critical"
    assert s_1630["stratum_primacy_rank"] == 1

    s_1761 = resolve_monument_recension_stratum("1761_pochayiv_menaion_september", {"title": "1761 Pochayiv Menaion"})
    assert s_1761["canonical_recension_witness_id"] == "kyivan_ruthenian_critical"
    assert s_1761["historical_stratum"] == "POST_ZAMOSC_POCHAIV_GALICIAN"
    assert s_1761["stratum_witness_id"] == "galician_synodal_critical"
    assert s_1761["stratum_primacy_rank"] == 2

    assert CANONICAL_RECENSION_WITNESS_ID == "kyivan_ruthenian_critical"
    assert CANONICAL_WITNESS_PRIORITY_ORDER.index("kyivan_ruthenian_critical") == 3
    assert CANONICAL_WITNESS_PRIORITY_ORDER.index("kyivan_ruthenian_critical") < CANONICAL_WITNESS_PRIORITY_ORDER.index("st_sergius")

    slav_blocks = [
        {
            "text": "Заченши Вл̃дки прїателище: избави насъ падшихъ лютѣ во пропасть ѿ неразумїя, и прегрѣшенїи и скорбеи. Ты бѡ еси грѣшникомъ Сп̃сенїе, и помощъ, и крѣпкая помощница: и спасаеши рабы твоя.",
            "start_line": 424,
            "end_line": 428,
            "verbatim_source": "Заченши Вл̃дки прїателище...",
            "source_file": "1630_lviv_octoechos_cohort1_source.txt",
            "source_sha256": "a" * 64,
        },
        {
            "text": "Слава, и нынѣ: Заступнице хрїстїаномъ непостыдная.",
            "start_line": 429,
            "end_line": 430,
            "verbatim_source": "Слава, и нынѣ...",
            "source_file": "1630_lviv_octoechos_cohort1_source.txt",
            "source_sha256": "a" * 64,
        },
    ]
    eng_blocks = [
        {
            "text": "*Theotokion:* Having conceived the Receptacle of the Master, deliver us who have fallen grievously into the abyss of ignorance, and of transgressions and sorrows."
        },
        {
            "text": "For Thou art the Salvation of sinners, and help, and a mighty helper, and Thou savest Thy servants."
        },
        {
            "text": "**Glory... Both now...** O unashamed Intercessor of Christians."
        },
    ]
    aligned = align_bilingual_leaf_blocks(slav_blocks, eng_blocks)
    assert aligned[0] is not None and aligned[0]["text"].startswith("Заченши")
    assert "Ты бѡ еси" not in aligned[0]["text"]
    assert aligned[1] is not None and aligned[1]["text"].startswith("Ты бѡ еси")
    assert aligned[0]["start_line"] == 424 and aligned[1]["start_line"] == 424
    assert aligned[0]["end_line"] == 428 and aligned[1]["end_line"] == 428
    assert aligned[2] is not None and "Заступнице" in aligned[2]["text"]


def test_step1_and_step2_generalized_subslicing_prefix_stripping_and_calendar_coords() -> None:
    """Verifies 1:K sub-slicing (K=3), strip_slavonic_leading_role_prefix(), and Fixed-Cycle calendar parsing."""
    from scripts.universal_corpus_extractor import (
        parse_fixed_calendar_month_day,
        strip_slavonic_leading_role_prefix,
    )

    # 1. Decision 2: strip_slavonic_leading_role_prefix strips chained/inline role & doxology headers
    raw_slav = "Бг҃оро́диченъ: Всемї́рную сла́ву, ѿ человѣ́къ прозя́бшую, и Влады́ку ро́ждшую."
    stripped = strip_slavonic_leading_role_prefix(raw_slav)
    assert stripped.startswith("Всемї́рную сла́ву")
    raw_ode = "Пѣ́снь г҃. І҆рмо́съ: Твоя́ пѣсносло́вцы, Бц҃е, живоно́сный исто́чниче."
    assert strip_slavonic_leading_role_prefix(raw_ode).startswith("Твоя́ пѣсносло́вцы")

    # 2. Decision 3: Generalized 1:3 sub-slicing with slice_index and slice_total in provenance
    slav_3 = [
        {
            "text": (
                "Прїиди́те вѣ́рнїи, животворя́щему Дре́ву поклони́мся, на не́мже Хрⷭ҇то́съ Ца́рь сла́вы во́лею ру́цѣ распросте́ръ. "
                "Вознесе́ ны на пе́рвое блаже́нство, я́же пре́жде вра́гъ сла́стїю укра́дъ, изгна́ны ѿ Бг҃а сотвори́. "
                "Прїиди́те вѣ́рнїи, Дре́ву поклони́мся, и́мже сподо́бихомся неви́димыхъ врагѡ́въ сокруша́ти главы́."
            ),
            "provenance": {
                "source_file": "cohort1_source.txt",
                "source_sha256": "b" * 64,
                "source_format": "TEXT_LINES",
                "start_line": 10,
                "end_line": 18,
                "verbatim_source": "Прїиди́те вѣ́рнїи...",
            },
        }
    ]
    eng_3 = [
        {"text": "Come, O faithful, let us worship the life-creating Tree, on which Christ the King of glory voluntarily stretched out His hands."},
        {"text": "He raised us up to the original blessedness, whom the enemy had previously robbed through pleasure and made exiles from God."},
        {"text": "Come, O faithful, let us worship the Tree, by which we have been counted worthy to crush the heads of the invisible enemies."},
    ]
    aligned_3 = align_bilingual_leaf_blocks(slav_3, eng_3)
    assert all(a is not None for a in aligned_3)
    for idx in range(3):
        assert aligned_3[idx]["alignment_method"] == "SUB_SLICED_1_TO_K"
        assert aligned_3[idx]["provenance"]["slice_index"] == idx + 1
        assert aligned_3[idx]["provenance"]["slice_total"] == 3
        assert aligned_3[idx]["provenance"]["start_line"] == 10
        assert aligned_3[idx]["provenance"]["end_line"] == 18

    # 3. Decision 1: Fixed-Cycle calendar date parsing without Podoben "On the third day" false positive
    m_num, m_name, d_num = parse_fixed_calendar_month_day(
        "*On the same month, the 2nd day: Of the holy Martyrs Akindynos, Pegasios, and those with them.*",
        11,
        "November",
    )
    assert (m_num, m_name, d_num) == (11, "November", 2)

    m_num2, m_name2, d_num2 = parse_fixed_calendar_month_day(
        '*Tone 1, Podoben: "On the third day" (Трїдне́венъ):*',
        11,
        "November",
    )
    assert (m_num2, m_name2, d_num2) == (11, "November", None)

    # 4. Plain-text weekday/service headers in 1630 Lviv Octoechos
    assert detect_office_slug_from_text('ON THURSDAY EVENING, AT "LORD, I HAVE CRIED"', "thursday", "octoechos") == "vespers"
    assert detect_section_slug_from_text('ON THURSDAY EVENING, AT "LORD, I HAVE CRIED"')[0] == "stichera_lord_i_call"
    assert detect_office_slug_from_text("ON FRIDAY, AT MATINS", "friday", "octoechos") == "matins"



