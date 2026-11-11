# Scholarly Drift & Seam-Stitching Audit Report: 1716 Kyiv-Pechersk Lavra Theotokarion / Eight-Tone Marian Canons

- **Monument ID**: `1716_kyiv_marian_canons_octoechos`
- **Total 2-Up Mid-Sentence Seams Stitched**: 105 boundaries (`7` sub-clause seam overlaps deduplicated)
- **Inline Locus Milestones Inserted**: `[f. XvA]`, `[f. XrA]` across all 246 leaves
- **Total Primitive Normalization & Drift Events**: 15 (`8` Podobens/Pokoin, `0` Psalm Stichoi, `0` Weekday Heirmoi, `7` Seam Deduplications)
- **True Pre-Normalization AI Translation Drift Unified**: 7 occurrences
- **Source-Text (1716 Slavonic) Scribal Truncations & Tier 3 Variations Classified**: 5 events

---

## 1. Summary of 3-Tier Source & Scribal Drift Engine

1. **Tier 1 (Typographic / Titlo Equivalence)**: Strips accents, titla, and sacred abbreviations (`бг҃` -> `богъ`). Unified silently to canonical English.
2. **Tier 2 (Orthographic / Phonological Variant)**: Harmonizes Ruthenian/Church Slavonic vowel and yer reflexes (`ѡ`/`о`, `ѣ`/`е`, `ꙋ`/`у`, `ᲂу`/`у`). Unified to canonical English while logging orthographic drift.
3. **Scribal Incipit Truncation (`SCRIBAL_INCIPIT_TRUNCATION`)**: The printer/scribe abbreviated the model incipit on the physical leaf (e.g. `По̀, Дв҃аа` for `Дѣ́ва дне́сь`, or omitted `Подо́бенъ` before the incipit). Classified as a scribal convention, never counted as AI translation error.
4. **Tier 3 (Lexical / Syntactic / Recensional Variant)**: Genuine source variations in the 1716 print. **Preserved as distinct English translations** and annotated.

---

## 2. Complete Podoben & Rubric Drift Log

| Type | Locus | ID | Drift Tier | 1716 Slavonic Witness | Pre-Normalization Cohort Text | Canonical Normalized Reading |
| :--- | :---: | :--- | :---: | :--- | :--- | :--- |
| `PODOBEN_NORMALIZED` | `C02:p18` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C03:p21` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C03:p29` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C04:p33` | `POD.T1.GROB_TVOI_SPASE` | `SCRIBAL_INCIPIT_TRUNCATION` | *Гро́бъ тво́й* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C05:p48` | `POD.T2.MILOSERDIA_SUSHCHI` | `SCRIBAL_INCIPIT_TRUNCATION` | *Милосе́рдїа сꙋ́щи* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C06:p59` | `POD.T2.MILOSERDIA_SUSHCHI` | `SCRIBAL_INCIPIT_TRUNCATION` | *Милосе́рдїа сꙋ́щи* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C08:p71` | `POD.T3.BOZHESTVENNYYA_VERY` | `TIER_3_LEXICAL_RECENSIONAL` | *Боже́ственныя вѣ́ры* | Podoben: Of the Divine Faith | **Of the divine faith** |
| `PODOBEN_NORMALIZED` | `C08:p75` | `POD.T3.KRASOTE_DEVSTVA` | `SCRIBAL_INCIPIT_TRUNCATION` | *Красотѣ̀ дѣ́вства* | Podoben: The Beauty of Thy Virginity | **Beholding the beauty of thy virginity** |