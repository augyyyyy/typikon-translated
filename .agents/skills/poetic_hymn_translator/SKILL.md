---
name: poetic_hymn_translator
description: Performs epigraphically grounded, singable English translations of Church Slavonic hymnography (Stichera, Sessional Hymns, Canons, Exapostilaria), enforcing Slavonic Physical Ink Primacy (Rule 16 & SGC-06), 3-Layer Podoben formatting, and colometric phrasing.
---

# Poetic Hymn Translator Skill Guidelines

When transcribing and translating liturgical hymnography (Octoechos, Triodion, Pentecostarion, Menaion, Anthologion, Irmologion, Akathistnik):

## 1. UTF-8 Strictness & Path Hygiene (`Rule 5` & `Rule 10`)
* All file I/O must explicitly specify `encoding="utf-8"` with `errors="strict"`. Never substitute empty strings or garbled text silently.
* Resolve all file and lexicon paths dynamically via `pathlib.Path` relative to the project root.

## 2. Slavonic Physical Ink Primacy vs. External Greek Concordance (`Rule 16` & `SGC-06`)
* **Primary Witness (Physical Slavonic Ink)**: Translate strictly what is printed in the physical 300 DPI Church Slavonic facsimile (`p1`..`pN`). Never silently alter, omit, or "correct" a printed Ruthenian/Slavonic reading to match a modern Greek Menaion or post-Nikonian Russian Synodal edition (`Mandate 11`).
* **External Comparative Greek Layer (`SGC-06` Epistemic Layering)**: Use Byzantine Greek originals (`data/byzantine_automela_concordance.json`) strictly to clarify obscure Slavonic calques, syntax, or compound epithets, and document significant Greek vs. Slavonic recensional divergences in translator footnotes `[^N]`. Never merge un-invoked external Greek automela into a monument's internal registry.

## 3. Canonical 3-Layer Melodic Model (`Podoben`) & Stanza Formatting (`Mandates 8–10`)
* **3-Layer `Podoben` Heading**: Format every melodic model heading using the canonical English incipit from `data/liturgical_primitives_registry.json` followed by the parenthetical Slavonic witness in inline italics:
  `*Tone N, Podoben: "<Canonical English Incipit>" (<Slavonic Witness>):*`
* **Inline Italic Stanza Role Tags (`H1 & H2` Only)**: Render each Heirmos, Troparion, Theotokion, Stavrotheotokion, Sessional Hymn, Kontakion, and Ikos as a distinct paragraph preceded by its inline italic role tag (`*Ode 1. Heirmos:*`, `*Troparion:*`, `*Theotokion:*`). Never emit `###` or `####` headings.
* **Colometric Asterisks (`*`)**: Preserve literal printed breathing/hemistich asterisks (`*`) in `Source Text/` and convert them into natural, singable English punctuation (commas, semicolons, colons) in `Draft/`.
* **Father Paul Doxology Standard (`MTS-1` Pillar VII)**:
  *"Glory be to the Father, and to the Son, and to the Holy Spirit, now and forever, and unto the ages of ages. Amen."* (Shorthand rubric: *"Glory... Now and forever, and unto the ages of ages:"*; ban *"for ever and ever"*).

## 4. On-Demand Reference Playbook
* [`references/sgc06_tabula_rasa_and_podoben_grid.md`](references/sgc06_tabula_rasa_and_podoben_grid.md) — `SGC-06` (*Tabula Rasa* bottom-up ink construction), 5-tuple attestation locus schema, internal vs. external concordance layering, and `generate_podoben_grid.py` / `generate_liturgical_primitives_registry.py` invariants.
