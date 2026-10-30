# Scholarly Drift & Seam-Stitching Audit Report: 17th-Century Carpathian-Galician Manuscript Octoechos

- **Monument ID**: `1600s_prykarpattia_ms_octoechos`
- **Total 2-Up Mid-Sentence Seams Stitched**: 0 boundaries (`0` sub-clause seam overlaps deduplicated)
- **Inline Locus Milestones Inserted**: `[f. XvA]`, `[f. XrA]` across all 222 leaves
- **Total Primitive Normalization & Drift Events**: 110 (`19` Podobens/Pokoin, `39` Psalm Stichoi, `52` Weekday Heirmoi, `0` Seam Deduplications)
- **True Pre-Normalization AI Translation Drift Unified**: 81 occurrences
- **Source-Text (1630 Slavonic) Scribal Truncations & Tier 3 Variations Classified**: 13 events

---

## 1. Summary of 3-Tier Source & Scribal Drift Engine

1. **Tier 1 (Typographic / Titlo Equivalence)**: Strips accents, titla, and sacred abbreviations (`бг҃` -> `богъ`). Unified silently to canonical English.
2. **Tier 2 (Orthographic / Phonological Variant)**: Harmonizes Ruthenian/Church Slavonic vowel and yer reflexes (`ѡ`/`о`, `ѣ`/`е`, `ꙋ`/`у`, `ᲂу`/`у`). Unified to canonical English while logging orthographic drift.
3. **Scribal Incipit Truncation (`SCRIBAL_INCIPIT_TRUNCATION`)**: The printer/scribe abbreviated the model incipit on the physical leaf (e.g. `По̀, Дв҃аа` for `Дѣ́ва дне́сь`, or omitted `Подо́бенъ` before the incipit). Classified as a scribal convention, never counted as AI translation error.
4. **Tier 3 (Lexical / Syntactic / Recensional Variant)**: Genuine source variations in the 1630 print. **Preserved as distinct English translations** and annotated.

---

## 2. Complete Podoben & Rubric Drift Log

| Type | Locus | ID | Drift Tier | 1630 Slavonic Witness | Pre-Normalization Cohort Text | Canonical Normalized Reading |
| :--- | :---: | :--- | :---: | :--- | :--- | :--- |
| `PODOBEN_NORMALIZED` | `C01:p9` | `POD.T1.GROB_TVOI_SPASE` | `SCRIBAL_INCIPIT_TRUNCATION` | *Гробъ твои* | Podoben: While the soldiers were guarding Thy tomb" (Гробъ твои) (fol. 5) | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C02:p11` | `POD.T1.NEBESNYKH_CHINOV` | `TIER_0_EXACT` | *Небе́сныхъ чинѡ́въ* | Podoben:  | **Joy of the heavenly ranks** |
| `PODOBEN_NORMALIZED` | `C07:p70` | `POD.T4.YAVILSYA_ESI_DNESS` | `SCRIBAL_INCIPIT_TRUNCATION` | *Явился еси* | Podoben: Thou hast appeared today" (Явился еси):* (fol. 66) | **Thou hast appeared today** |
| `PODOBEN_NORMALIZED` | `C10:p96` | `POD.T6.EZHE_O_NAS` | `TIER_3_LEXICAL_RECENSIONAL` | *"Еже ѡ насъ" (Исполнивъ смотрѣніе)* | Podoben: Fulfilling the dispensation for our sake | **Fulfilling the dispensation for our sake** |
| `PODOBEN_NORMALIZED` | `C10:p97` | `POD.T6.EZHE_O_NAS` | `TIER_3_LEXICAL_RECENSIONAL` | *"Еже ѡ насъ" (Исполнивъ смотрѣніе)* | Podoben: Fulfilling the dispensation for our sake | **Fulfilling the dispensation for our sake** |
| `PODOBEN_NORMALIZED` | `C13:p130` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_3_LEXICAL_RECENSIONAL` | *Повеленное таинственно (Повеленное)* | Podoben: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C14:p131` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_3_LEXICAL_RECENSIONAL` | *Повеленное таинственно (Повеленное)* | Podoben: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C15:p146` | `POD.T8.GOSPODI_ASHCHE_I_NA_SUDISHCHI` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Господи, аще и на судищи* | Podoben: O Lord, though [Thou didst stand] at the judgment seat | **O Lord, though Thou didst stand before the tribunal** |
| `PODOBEN_NORMALIZED` | `C15:p147` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_0_EXACT` | *Повелѣ́нное та́инственно* | Podoben: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C16:p157` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C16:p157` | `POD.T8.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera, to the Holy Forerunner John, Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C17:p169` | `POD.T3.VELIA_KRESTA_TVOEGO` | `TIER_0_EXACT` | *Ве́лія Крⷭ҇та̀ твоегѡ̀ Гдⷭ҇и* | Podoben: Great is the power of Thy Cross | **Great is the power of Thy Cross, O Lord** |
| `PODOBEN_NORMALIZED` | `C18:p179` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant among martyrs | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C19:p183` | `POD.T3.DEVA_DNESS` | `TIER_0_EXACT` | *Дѣ́ва дне́сь* | Podoben: Today the Virgin | **Today the Virgin** |
| `PODOBEN_NORMALIZED` | `C20:p199` | `POD.T8.CHTO_VAS_NARECHEM` | `SCRIBAL_INCIPIT_TRUNCATION` | *Что вы наречемъ* | Podoben: What shall we call you | **What shall we call you, O holy ones** |
| `PODOBEN_NORMALIZED` | `C21:p201` | `POD.T8.PREMUDROSTI_NASTAVNICHE` | `TIER_0_EXACT` | *Премꙋ́дрости наста́вниче* | Podoben: Guiding unto wisdom | **Guiding unto wisdom** |
| `PODOBEN_NORMALIZED` | `C21:p202` | `POD.T8.YAKO_NACHATKI_ESTESTVA` | `TIER_0_EXACT` | *Я҆́кѡ нача́тки е҆стества̀* | Podoben: As first-fruits of nature | **As first-fruits of nature** |
| `PODOBEN_NORMALIZED` | `C21:p207` | `POD.T8.CHTO_VAS_NARECHEM` | `SCRIBAL_INCIPIT_TRUNCATION` | *Что вы наречемъ* | Podoben: What shall we call you, O holy ones | **What shall we call you, O holy ones** |
| `PODOBEN_NORMALIZED` | `C21:p208` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `SCRIBAL_INCIPIT_TRUNCATION` | *О преслав* | Podoben: O most marvelous wonder | **O most marvelous wonder** |