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
from scripts.universal_corpus_extractor import (
    VALID_UNIT_CLASSES,
    extract_monument_atomic_corpus,
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


def test_universal_extractor_horologion_and_liturgikon_5_classes() -> None:
    """Verifies 5-class extraction, 4-shard routing, and SGC-02 provenance on Horologion & Liturgikon."""
    hor_payload = extract_monument_atomic_corpus("1491_krakow_fiol_horologion", sync_hub=False)
    hor_units = hor_payload["units"]
    assert len(hor_units) > 500
    hor_classes = hor_payload["summary"]["counts_by_unit_class"]
    assert hor_classes["PROPER_HYMN"] > 100
    assert hor_classes["RUBRIC_OR_STATUTE"] > 100

    lit_payload = extract_monument_atomic_corpus("1604_striatyn_balaban_liturgikon", sync_hub=False)
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
    for u in lit_units[:50] + hor_units[:50]:
        assert u["unit_class"] in VALID_UNIT_CLASSES
        assert u["target_shard"] in valid_shards
        prov = u["provenance"]
        assert len(prov["source_sha256"]) == 64
        assert prov["source_format"] == "TEXT_LINES"
        assert prov["start_line"] >= 1
        assert prov["end_line"] >= prov["start_line"]
        assert len(prov["verbatim_source"]) > 0
