---
name: liturgical_glossary_enforcer
description: Scans English draft translations to enforce canonical UGCC terminology from the Master Glossary, flag forbidden variants, and verify proper Deity pronoun capitalization.
---

# Liturgical Glossary Enforcer Skill Guidelines

When executing a glossary or capitalization check:

## 1. Forbidden Colon-Split Rule
When parsing glossary entries or liturgical files, never split on colons (`:`) without proper context, because many UGCC terms and titles themselves contain colons (e.g., "Hlas 1: Podoben: ..."). Use a dedicated parser that relies on indentation or explicit delimiters. Any automatic ":-split" heuristic on liturgical lines is prohibited.

## 2. Master Glossary Alignment
* Ensure standard liturgical terms are mapped exactly to canonical variants.
* **Liturgical Books & Documents**:
  * *Церковне Око* → **Tserkovne Oko** (Forbidden: Eye of the Church, Oko Tserkovne)
  * *Трефологіон / Антологіон* → **Anthologion** (Forbidden: Trephologion)
  * *Служебник* → **Sluzhebnik** (Forbidden: Service Book when standalone)
* **Services & Hours**:
  * *Всенічне* → **All-Night Vigil** (Forbidden: Vsenichne)
  * *Повечір'я* → **Compline** (Forbidden: Povechiria)
  * *Обідниця* → **Typika** (Forbidden: Obidnytsia)
* **Hymnography**:
  * *Сідален* → **Sessional Hymn** (Forbidden: Kathisma)
  * *Самогласен* → **Idiomelon** (Forbidden: Samohlasen)
  * *Подібен* → **Prosomoion** (Forbidden: Podiben)
  * *Ірмос* → **Heirmos** / **Heirmoi** (Forbidden: Irmos)
  * *Прокімен* → **Prokimenon** / **Prokimena** (Forbidden: Prokeimenon)
  * *Катізма* → **Kathisma** (Forbidden: Kafisma)

## 3. Deity Capitalization Rules
* Capitalize all pronouns (He, Him, His, Who, Whom, Thee, Thou, Thy, Thine) referring to the Deity (God, Father, Son, Holy Spirit).
* Capitalize divine titles and names.
* Ensure pronouns referring to the Theotokos (Virgin Mary), angels, saints, or human participants remain lowercase.
