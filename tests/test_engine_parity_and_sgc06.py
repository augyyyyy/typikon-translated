#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Engine Parity, Unicode Homoglyph Healing, Dual-Context TOC Slugify,
Footnote Vocabulary/Stemmer Normalization, and Rule 22 (SGC-06 Tabula Rasa) Digest Generation.
"""

from __future__ import annotations

from pathlib import Path

from scripts.compile_final_edition import (
    heal_cohort_and_apparatus_text,
    heal_mixed_script_homoglyphs,
    slugify as compile_slugify,
)
from scripts import hieratic_pronoun_audit, structural_audit
from scripts.hymnographic_gold_normalizer import (
    HymnographicNormalizer,
    generate_father_paul_digest,
)
from scripts.verify_publication_edition import (
    extract_headings_and_anchors,
    slugify as verify_slugify,
)


def test_slugify_parity_across_greek_diacritics_and_cyrillic() -> None:
    """Verifies identical slug generation between compiler and publication gate auditor."""
    samples = [
        "## ΠΡΟΘΕΩΡΙΑ (PRETHEORY) [^12]",
        "## Titulus I: De Fide Catholica (*О вѣрѣ каѳолической*)",
        "## 14. Święty Jozafat Kuncewicz <a id=\"josaphat\"></a>",
        "## [Order of Great Vespers](#order-of-great-vespers) (Гла́съ а҃)",
    ]
    for sample in samples:
        heading = sample.lstrip("#").strip()
        s_comp = compile_slugify(heading)
        s_ver = verify_slugify(heading)
        assert s_comp == s_ver, f"Slug mismatch for {heading!r}: {s_comp!r} != {s_ver!r}"

    assert compile_slugify("ΠΡΟΘΕΩΡΙΑ (PRETHEORY)") == "προθεωρια-pretheory"
    assert compile_slugify("Titulus I (*О вѣрѣ*) [^4]") == "titulus-i"


def test_extract_headings_and_mandate8_inline_anchors() -> None:
    """Verifies Gate 3 anchor extraction recognizes <a id=\"...\"> tags on Mandate 8 inline bold lines."""
    doc = "\n".join(
        [
            "# PART I: LITURGICAL STATUTES",
            "",
            "## Chapter 1: Preliminary Rubrics (*О уста́вѣ*)",
            "",
            "** Subsection A: On the Klepalo ** <a id=\"on-the-klepalo\"></a>",
            "*At the seventh hour of the night, the paracclesiarch strikes the Klepalo.*",
        ]
    )
    anchors = extract_headings_and_anchors(doc)
    assert "part-i-liturgical-statutes" in anchors
    assert "chapter-1-preliminary-rubrics" in anchors
    assert "on-the-klepalo" in anchors


def test_heal_mixed_script_homoglyphs() -> None:
    """Verifies repair of Cyrillic/Greek/Latin homoglyphs while preserving Slavistic transliteration."""
    # Greek tokens contaminated with Cyrillic homoglyphs
    assert heal_mixed_script_homoglyphs("ἀφοриζέσθω") == "ἀφοριζέσθω"
    assert heal_mixed_script_homoglyphs("πεπεδημένουѕ") == "πεπεδημένους"
    assert heal_mixed_script_homoglyphs("теоρία") == "θεωρία"

    # Cyrillic tokens contaminated with Latin or Greek homoglyphs
    assert heal_mixed_script_homoglyphs("Вавvлонскихъ") == "Вавѵлонскихъ"
    assert heal_mixed_script_homoglyphs("пресла́внагw") == "пресла́внагѡ"
    assert heal_mixed_script_homoglyphs("му́рωне") == "му́рѡне"

    # Latin tokens contaminated with Cyrillic homoglyphs
    assert heal_mixed_script_homoglyphs("eudiallaktоn") == "eudiallakton"

    # Preserved scientific Slavistic transliteration and diplomatic woodcut forms
    preserved = "Dѣva Krestъ vъ vѣkъ HMДEMYIΣ INЦI ΘЄѠ ѲY ΘV"
    assert heal_mixed_script_homoglyphs(preserved) == preserved

    # 3-script upgrades: Cyrillic+Greek with Cyrillic-exclusive chars, Greek+Latin, Cyrillic+Latin short accented tokens
    assert heal_mixed_script_homoglyphs("Ѳеώдωра") == "Ѳеѡ́дѡра"
    assert heal_mixed_script_homoglyphs("Eὐχολόγιον") == "Εὐχολόγιον"
    assert heal_mixed_script_homoglyphs("μou") == "μου"
    assert heal_mixed_script_homoglyphs("ҮМNON") == "ΥΜΝΟΝ"
    assert heal_mixed_script_homoglyphs("дýшy") == "ду́шу"


def test_healer_vocabulary_stemmer_and_table_safe_cyrillic() -> None:
    """Verifies MTS-1 vocabulary healing in footnotes, -eth stemmer accuracy, and table-pipe safety."""
    fn_sample = (
        '[^12]: Compare printed *Apolytikion* and early Service Books; '
        'this poignant rubric notes the priest communicateth and addeth incense while Elisabeth prayeth, '
        'cf. archaic gloss "verily" and doxology "for ever and ever" in secondary editions.'
    )
    healed_fn, changed = heal_cohort_and_apparatus_text(fn_sample, is_footnotes=True)
    assert changed is True
    assert "*Troparion*" in healed_fn
    assert "Sluzhebniks" in healed_fn
    assert "penitential rubric" in healed_fn
    assert "communicates" in healed_fn
    assert "adds" in healed_fn
    assert "Elisabeth prays" in healed_fn
    # Quoted slop token inside footnote is preserved verbatim, while Father Paul Doxology is enforced globally
    assert '"verily"' in healed_fn
    assert '"unto ages of ages"' in healed_fn

    body_table = "| Left Medallion | ІС ХС | Right Medallion | НІ КА |"
    healed_table, table_changed = heal_cohort_and_apparatus_text(body_table, is_footnotes=False)
    assert table_changed is True
    assert healed_table.count("|") == 5
    assert "(*ІС ХС*)" in healed_table
    assert "(*НІ КА*)" in healed_table


def test_sgc06_tabula_rasa_father_paul_digest() -> None:
    """Verifies Rule 22 (SGC-06): zero ghost rows, zero Greek columns in Sections 1-3, and Section 4 quarantine."""
    normalizer = HymnographicNormalizer()
    mon_meta = {
        "publication_year": 1630,
        "short_title": "1630 Lviv Octoechos (Test Fixture)",
        "workspace_dir": "Liturgical Monuments/1630_lviv_octoechos",
    }
    first_stichos = normalizer.stichoi[0]
    first_podoben = normalizer.podobens[0]

    events = [
        {
            "type": "PSALM_VERSE_NORMALIZED",
            "id": first_stichos["id"],
            "locus": "p12 (f. 6vA)",
            "slavonic_source": first_stichos.get("slavonic_canonical", "Изведи из темницы"),
        },
        {
            "type": "PODOBEN_NORMALIZED",
            "primitive_id": first_podoben["id"],
            "locus": "p14 (f. 7vA)",
            "slavonic_source": first_podoben.get("slavonic_canonical", "Небесных чинов"),
        },
    ]
    corpus_items = [
        {
            "tone": 1,
            "ode": 1,
            "hymn_type": "HEIRMOS",
            "leaf": "p18",
            "locus": "f. 9vA",
            "slavonic_diplomatic": "Твоя победительная десница боголепно в крепости прославися",
            "english_cohort_translation": "*Ode 1. Heirmos:* Thy victorious right hand hath been gloriously magnified in strength.",
        }
    ]

    digest = generate_father_paul_digest(
        monument_id="test_sgc06_fixture",
        mon_meta=mon_meta,
        normalizer=normalizer,
        events=events,
        corpus_items=corpus_items,
        stitched_cohorts=['*Tone 1, Podoben: "Joy of the heavenly ranks" (Небесных чинов):*'],
    )

    sec1_to_3, sec4 = digest.split("## 4. Un-Invoked Comparative Automela", maxsplit=1)
    assert "Byzantine Greek" not in sec1_to_3
    assert "0 leaves" not in sec1_to_3
    assert "[Not attested in monument]" not in digest
    assert first_stichos["id"] in sec1_to_3
    assert first_podoben["id"] in sec1_to_3
    assert "Tone 1 Ode 1" not in sec4
    assert "Un-Invoked Psalm Stichoi" in sec4
    assert "Un-Attested Canon Odes" in sec4


def test_hieratic_pronoun_audit_cosmic_nouns_and_doxology(tmp_path: Path) -> None:
    """Verifies cosmic/ecclesial nouns do not mask lowercase Deity pronouns while Marian/apostrophe exceptions pass."""
    bad_cosmic = tmp_path / "bad_cosmic.md"
    bad_cosmic.write_text("O Lord of Heaven and Earth, we praise thy name.\n", encoding="utf-8")
    res_cosmic = hieratic_pronoun_audit.audit_file(bad_cosmic)
    assert res_cosmic["passed"] is False
    assert res_cosmic["violation_count"] == 1

    bad_doxology = tmp_path / "bad_doxology.md"
    bad_doxology.write_text("The Priest says: Glory to thee, O God!\n", encoding="utf-8")
    res_dox = hieratic_pronoun_audit.audit_file(bad_doxology)
    assert res_dox["passed"] is False
    assert res_dox["violation_count"] == 1

    good_marian_and_apostrophe = tmp_path / "good_marian.md"
    good_marian_and_apostrophe.write_text(
        "Glory to thee, O pure Bride of God!\n"
        "O Jordan, what didst thou see when the Lord came unto thee?\n",
        encoding="utf-8",
    )
    res_good = hieratic_pronoun_audit.audit_file(good_marian_and_apostrophe)
    assert res_good["passed"] is True
    assert res_good["violation_count"] == 0


def test_structural_audit_mandate8_headings_and_statute_numbering(tmp_path: Path) -> None:
    """Verifies H3+ cohort headings fail Mandate 8 while bracketed statute restorations and quoted numbers pass."""
    bad_cohort = tmp_path / "sample_cohort1.md"
    bad_cohort.write_text(
        "=== LEAF p1 ===\n"
        "## Order of Great Vespers\n"
        "### Notes\n"
        "*At the tenth hour of the day the paracclesiarch strikes the Klepalo.*\n",
        encoding="utf-8",
    )
    res_bad = structural_audit.audit_structure(bad_cohort, None, 1, monument_id="1899_dolnytsky_typikon")
    assert res_bad["passed"] is False
    assert any("EPIGRAPHIC_HEADING_VIOLATION" in a for a in res_bad["anomalies"])

    good_cohort = tmp_path / "sample_cohort2.md"
    good_cohort.write_text(
        "=== LEAF p2 ===\n"
        "**1. First Section**\n"
        "1. Statute one.\n"
        '"2. Quoted liturgical statute two inside a paragraph does not reset bold section numbering."\n'
        "**2. Second Section**\n"
        "3. Statute three.\n"
        "4. Statute four.\n"
        "[5.] Bracketed Rule 16 editorial restoration of skipped statute numeral.\n"
        "6. Statute six.\n"
        + ("*" * 80) + "\n"
        "12. Apodosis of a Dominical Feast on Sunday . . . . . . 117\n"
        "14. Apodosis of a Dominical Feast on Weekdays . . . . 120\n",
        encoding="utf-8",
    )
    res_good = structural_audit.audit_structure(good_cohort, bad_cohort, 2, monument_id="1891_lviv_synod")
    assert res_good["passed"] is True
    assert res_good["anomalies"] == []
    assert res_good["number_breaks"] == []
