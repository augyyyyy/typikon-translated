---
name: liturgical_glossary_enforcer
description: Scans English draft translations to enforce canonical UGCC and MTS-1 terminology from the Shared Lexicon, flag forbidden variants, and verify Hieratic Deity pronoun capitalization and Gate 1B anti-slop compliance.
---

# Liturgical Glossary Enforcer Skill Guidelines

When executing a vocabulary, realia, doxology, or pronoun capitalization check across `Draft/` or `Final/`:

## 1. Forbidden Colon-Split Rule
Never split liturgical lines or glossary entries on bare colons (`:`) without context, because chant headers and rubrics embed colons (`*Tone 1, Podoben: "O all-praised martyrs" (Всехвальніи мученицы):*`). Always parse via structural regexes or explicit field delimiters.

## 2. Master Glossary & `lint_vocabulary.py` Alignment (`../Shared_Lexicon/lint_vocabulary.py`)
* **Liturgical Books & Toponyms**:
  * *Церковне Око* → **Tserkovne Oko** (Forbidden: *Eye of the Church, Oko Tserkovne*)
  * *Трефологіон / Антологіон* → **Anthologion** (Forbidden: *Trephologion*)
  * *Служебник / Требник* → **Sluzhebnik** / **Trebnik** (Forbidden standalone: *Service Book, Book of Needs*)
  * *Почаїв* → **Pochaiv** (Forbidden in body/footnotes: *Pochayiv*)
* **Services & Hours**:
  * *Всенічне* → **All-Night Vigil** (Forbidden: *Vsenichne*)
  * *Повечір'я* → **Compline** (Forbidden: *Povechiria*)
  * *Обідниця* → **Typika** (Forbidden: *Obidnytsia*)
* **Hymnography & Melodic Models**:
  * **3-Layer Melodic Heading**: `*Tone N, Podoben: "<Canonical English Incipit>" (<Slavonic Witness>):*` (Forbidden: *Podiben, Podobny, Mode I, Plagal Mode*).
  * **Narrative Rubrics**: Use **Prosomoion** / **Prosomoia** (or canonical **Podoben**) and **Idiomelon** / **Idiomela**; when citing the Slavonic term *Samohlasen* as a witness, enclose in parenthetical italics `(*Samohlasen*)` so `lint_vocabulary.py` recognizes the witness exemption.
  * *Сідален* → **Sessional Hymn** (Forbidden: *Kathisma hymn*)
  * *Ірмос* → **Heirmos** / **Heirmoi** (Forbidden: *Irmos*)
  * *Прокімен* → **Prokimenon** / **Prokimena** (Forbidden: *Prokeimenon*)
  * *Катізма* → **Kathisma** / **Kathismata** (Forbidden: *Kafisma*)

## 3. Hieratic Deity Pronouns & Father Paul Doxology (`MTS-1` Pillar VII)
* **100% Deity Pronoun Capitalization**: Capitalize *He, Him, His, Who, Whom, Thee, Thou, Thy, Thine* when referring to the Holy Trinity (God, Father, Son, Holy Spirit).
* **Negative Pronoun Guard**: Keep pronouns referring to the Theotokos (*Birthgiver of God / Mother of God*), angels, saints, clergy, or the adversary (*serpent/enemy*) strictly lowercase.
* **Father Paul Doxology**: Enforce *"unto ages of ages"* / *"unto the ages of ages"*; permanently ban *"for ever and ever"*.

## 4. On-Demand Reference Playbooks
* [`references/mts1_registers_and_realia.md`](references/mts1_registers_and_realia.md) — MTS-1 Four Genre Registers, LXX Psalter versification, Byzantine-Ruthenian realia loanwords, and hagiographical titulature.
* [`references/anti_slop_and_pronoun_gates.md`](references/anti_slop_and_pronoun_gates.md) — Gate 1B (`scripts/lint_liturgical_slop.py`) banned `-eth` verbs, pseudo-archaic slop tokens, and `scripts/hieratic_pronoun_audit.py` rules.
