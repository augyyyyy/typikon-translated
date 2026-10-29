# Scholarly Drift & Seam-Stitching Audit Report: 1895 Lviv Complete Octoechos

- **Monument ID**: `1895_lviv_octoechos`
- **Total 2-Up Mid-Sentence Seams Stitched**: 0 boundaries (`0` sub-clause seam overlaps deduplicated)
- **Inline Locus Milestones Inserted**: `[f. XvA]`, `[f. XrA]` across all 1029 leaves
- **Total Primitive Normalization & Drift Events**: 386 (`194` Podobens/Pokoin, `192` Psalm Stichoi, `0` Weekday Heirmoi, `0` Seam Deduplications)
- **True Pre-Normalization AI Translation Drift Unified**: 116 occurrences
- **Source-Text (1895 Slavonic) Scribal Truncations & Tier 3 Variations Classified**: 78 events

---

## 1. Summary of 3-Tier Source & Scribal Drift Engine

1. **Tier 1 (Typographic / Titlo Equivalence)**: Strips accents, titla, and sacred abbreviations (`бг҃` -> `богъ`). Unified silently to canonical English.
2. **Tier 2 (Orthographic / Phonological Variant)**: Harmonizes Ruthenian/Church Slavonic vowel and yer reflexes (`ѡ`/`о`, `ѣ`/`е`, `ꙋ`/`у`, `ᲂу`/`у`). Unified to canonical English while logging orthographic drift.
3. **Scribal Incipit Truncation (`SCRIBAL_INCIPIT_TRUNCATION`)**: The printer/scribe abbreviated the model incipit on the physical leaf (e.g. `По̀, Дв҃аа` for `Дѣ́ва дне́сь`, or omitted `Подо́бенъ` before the incipit). Classified as a scribal convention, never counted as AI translation error.
4. **Tier 3 (Lexical / Syntactic / Recensional Variant)**: Genuine source variations in the 1895 print. **Preserved as distinct English translations** and annotated.

---

## 2. Complete Podoben & Rubric Drift Log

| Type | Locus | ID | Drift Tier | 1895 Slavonic Witness | Pre-Normalization Cohort Text | Canonical Normalized Reading |
| :--- | :---: | :--- | :---: | :--- | :--- | :--- |
| `PODOBEN_NORMALIZED` | `C01:p4` | `POD.T1.NEBESNYKH_CHINOV` | `TIER_0_EXACT` | *Небе́сныхъ чинѡ́въ* | Podoben: Joy of the heavenly ranks | **Joy of the heavenly ranks** |
| `PODOBEN_NORMALIZED` | `C02:p14` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C02:p16` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C02:p18` | `POD.T1.KAMENI_ZAPECHATLENU` | `TIER_0_EXACT` | *Ка́мени запеча́танꙋ* | Podoben: When the stone had been sealed | **When the stone had been sealed** |
| `PODOBEN_NORMALIZED` | `C02:p19` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C03:p26` | `POD.T1.EGDA_PRIIDESHI` | `TIER_3_LEXICAL_RECENSIONAL` | *Є҆гда̀ прїи́деши* | Podoben: When Thou shalt come | **When Thou shalt come** |
| `PODOBEN_NORMALIZED` | `C04:p32` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Прехва́льнїи мꙋ́ченици* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C04:p32` | `POD.T1.SAME` | `TIER_0_EXACT` | *то́йже* | *Tone and Podoben the same.* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C04:p33` | `POD.T1.NEBESNYKH_CHINOV` | `TIER_0_EXACT` | *Небе́сныхъ чинѡ́въ* | Podoben: Joy of the heavenly ranks | **Joy of the heavenly ranks** |
| `PODOBEN_NORMALIZED` | `C04:p36` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C04:p38` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C04:p39` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C05:p49` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_0_EXACT` | *Прехва́льніи мꙋ́ченицы* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C05:p49` | `POD.T1.SAME` | `TIER_0_EXACT` | *то́йже* | *Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C06:p52` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: Thy tomb, O Savior | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C06:p55` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: Thy tomb, O Savior | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C07:p65` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Прехва́льнїи мꙋ́ченици* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C07:p66` | `POD.T1.NEBESNYKH_CHINOV` | `TIER_0_EXACT` | *Небе́сныхъ чинѡ́въ* | Podoben: Joy of the heavenly ranks | **Joy of the heavenly ranks** |
| `PODOBEN_NORMALIZED` | `C07:p67` | `POD.T1.NEBESNYKH_CHINOV` | `TIER_0_EXACT` | *Небе́сныхъ чинѡ́въ* | Podoben: Joy of the heavenly ranks | **Joy of the heavenly ranks** |
| `PODOBEN_NORMALIZED` | `C08:p72` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: Thy tomb, O Savior | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C09:p82` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_0_EXACT` | *Прехва́льніи мꙋ́ченицы* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C09:p83` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_0_EXACT` | *Прехва́льніи мꙋ́ченицы* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C09:p83` | `POD.T1.NEBESNYKH_CHINOV` | `TIER_0_EXACT` | *Небе́сныхъ чинѡ́въ* | Podoben: Joy of the heavenly ranks | **Joy of the heavenly ranks** |
| `PODOBEN_NORMALIZED` | `C09:p86` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: Thy tomb, O Savior | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C10:p98` | `POD.T1.NEBESNYKH_CHINOV` | `TIER_0_EXACT` | *Небе́сныхъ чинѡ́въ* | Podoben: Joy of the heavenly ranks | **Joy of the heavenly ranks** |
| `PODOBEN_NORMALIZED` | `C10:p99` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Прехва́льнїи мꙋ́ченици* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C10:p99` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Прехва́льнїи мꙋ́ченици* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C10:p100` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_0_EXACT` | *Прехва́льніи мꙋ́ченицы* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C11:p103` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C12:p114` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_0_EXACT` | *Прехва́льніи мꙋ́ченицы* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C12:p115` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_0_EXACT` | *Прехва́льніи мꙋ́ченицы* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C13:p121` | `POD.T1.GROB_TVOI_SPASE` | `TIER_0_EXACT` | *Гро́бъ тво́й Сп҃се* | Podoben: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C14:p132` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_0_EXACT` | *Прехва́льніи мꙋ́ченицы* | Podoben: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C14:p135` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C15:p143` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C15:p145` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C16:p158` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C16:p158` | `POD.T2.SAME` | `TIER_0_EXACT` | *то́йже* | *Tone and Podoben the same.* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C17:p162` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C17:p164` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C18:p173` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C18:p174` | `POD.T2.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera, to the Holy John the Forerunner, Tone and Podoben the same.* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C18:p177` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C18:p179` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C19:p190` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C20:p191` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C20:p192` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C20:p196` | `POD.T2.VYSHNIKH_ISHCHA` | `TIER_0_EXACT` | *Вы́шнихъ и҆щѧ̀* | Podoben: Seeking the highest | **Seeking the highest** |
| `PODOBEN_NORMALIZED` | `C20:p197` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C20:p197` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C21:p205` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C21:p206` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C21:p207` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C22:p213` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C23:p222` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C23:p222` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C23:p223` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C23:p223` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C23:p226` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C24:p238` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C24:p238` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C25:p244` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being the wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C26:p254` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C27:p265` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: Beholding the beauty of thy virginity" (Красотѣ̀ дѣ́вства):* O undivided and inseparable Trinity! Have mercy upon us who worship Thee, and hymn Thee piously, and unceasingly cry unto Thee: Save those whom Thou hast gathered for the sake of the mercy of Thy tender compassion, in Thy holy church, to glorify Thy dominion; for as Thou art merciful, Thou knowest the weakness of our heart | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C27:p267` | `POD.T3.DEVA_DNESS` | `TIER_0_EXACT` | *Дѣ́ва дне́сь* | Podoben: Today the Virgin" (Дѣ́ва дне́сь):* When Thou comest upon earth, O Master, to judge all whom Thou didst fashion from the earth according to Thine image, show compassion as Thou art merciful, and deliver all from Thy righteous judgment; and send us not into the fire of Gehenna, as Thou alone art Christ, the abundantly merciful | **Today the Virgin** |
| `PODOBEN_NORMALIZED` | `C27:p269` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: Beholding the beauty of thy virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C28:p275` | `POD.T3.DEVA_DNESS` | `TIER_0_EXACT` | *Дѣ́ва дне́сь* | Podoben: Today the Virgin | **Today the Virgin** |
| `PODOBEN_NORMALIZED` | `C29:p281` | `POD.T3.VELIA_MUCHENIK_TVOIKH` | `TIER_0_EXACT` | *Ве́лія мꙋ́ченикъ твои́хъ* | Podoben: Great is the power of Thy martyrs | **Great is the power of Thy martyrs** |
| `PODOBEN_NORMALIZED` | `C29:p284` | `POD.T3.BOZHESTVENNYYA_VERY` | `TIER_3_LEXICAL_RECENSIONAL` | *Бж҃твенныя* | Podoben: Of the divine faith | **Of the divine faith** |
| `PODOBEN_NORMALIZED` | `C29:p287` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_3_LEXICAL_RECENSIONAL` | *г҃-мъ стїхосло́вїи, сѣда́ленъ, Гла́съ г҃. (Подо́бенъ красотѣ̀ Дѣ́вства:)* | Podoben: Beholding the beauty of thy virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C30:p296` | `POD.T3.KRESTOOBRAZNO` | `TIER_0_EXACT` | *Крⷭ҇тоѡбра́зно* | Podoben: In the likeness of the Cross | **In the likeness of the Cross** |
| `PODOBEN_NORMALIZED` | `C30:p300` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: Beholding the beauty of thy virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C31:p303` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_3_LEXICAL_RECENSIONAL` | *г҃-мъ стїхосло́вїи, сѣда́лны, Гла́съ а҃. (Подо́бенъ: Красотѣ̀ дѣ́вства:)* | Podoben: Beholding the beauty of thy virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C32:p313` | `POD.T3.VELIA_MUCHENIK_TVOIKH` | `TIER_0_EXACT` | *Ве́лія мꙋ́ченикъ твои́хъ* | Podoben: Great is the power of Thy martyrs | **Great is the power of Thy martyrs** |
| `PODOBEN_NORMALIZED` | `C32:p319` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: Beholding the beauty of thy virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C32:p319` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: Beholding the beauty of thy virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C33:p329` | `POD.T3.VELIA_MUCHENIK_TVOIKH` | `SCRIBAL_INCIPIT_TRUNCATION` | *Ве́лїа мꙋ́ченикъ* | Podoben: Great is the power of Thy martyrs | **Great is the power of Thy martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C33:p330` | `POD.T3.SAME` | `TIER_0_EXACT` | *то́йже* | *If there be no Menaion, we sing Stichera to the holy Wonderworker Nicholas. Tone and podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C35:p345` | `POD.T3.POSTAVISHA_TRIDESYATE` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Поста́виша трї́десѧте* | Podoben: They weighed thirty pieces of silver | **They weighed thirty pieces of silver** |
| `PODOBEN_NORMALIZED` | `C37:p362` | `POD.T3.VELIA_MUCHENIK_TVOIKH` | `SCRIBAL_INCIPIT_TRUNCATION` | *Ве́лїа мꙋ́ченикъ* | Podoben: Great is the power of Thy martyrs | **Great is the power of Thy martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C37:p362` | `POD.T3.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Martyrs, same Tone and Podoben (то́йже подо́бенъ):* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C38:p378` | `POD.T3.VELIA_KRESTA_TVOEGO` | `SCRIBAL_INCIPIT_TRUNCATION` | *Ве́лїа крⷭ҇та̀ твоегѡ̀* | Podoben: Great is the power of Thy Cross, O Lord | **Great is the power of Thy Cross, O Lord** |
| `PODOBEN_NORMALIZED` | `C39:p381` | `POD.T4.ZVANNYI_SVYSHE` | `TIER_0_EXACT` | *Зва́нный свы́ше* | Podoben: Being called from on high | **Being called from on high** |
| `PODOBEN_NORMALIZED` | `C39:p383` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Podoben: O most marvelous wonder | **O most marvelous wonder** |
| `PODOBEN_NORMALIZED` | `C39:p389` | `POD.T4.SKORO_PREDVARI` | `TIER_0_EXACT` | *Ско́рѡ предварѝ* | Podoben: Speedily anticipate | **Speedily anticipate** |
| `PODOBEN_NORMALIZED` | `C40:p391` | `POD.T4.VOZNESYISYA_NA_KREST` | `TIER_0_EXACT` | *Вознесы́йся на Крⷭ҇тъ во́лею* | Podoben: Thou Who wast lifted up upon the Cross | **Thou Who wast lifted up upon the Cross** |
| `PODOBEN_NORMALIZED` | `C40:p399` | `POD.T4.YAVILSYA_ESI_DNESS` | `TIER_0_EXACT` | *Я҆ви́лся е҆сѝ дне́сь* | Podoben: Thou hast appeared today | **Thou hast appeared today** |
| `PODOBEN_NORMALIZED` | `C41:p406` | `POD.T4.DALS_ESI_ZNAMENIE` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Да́лъ є҆сѝ зна́менїе* | Podoben: Thou hast given a sign | **Thou hast given a sign** |
| `PODOBEN_NORMALIZED` | `C41:p406` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant among martyrs | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C42:p412` | `POD.T4.SKORO_PREDVARI` | `TIER_0_EXACT` | *Ско́рѡ предварѝ* | Podoben: Speedily anticipate | **Speedily anticipate** |
| `PODOBEN_NORMALIZED` | `C43:p422` | `POD.T4.ZVANNYI_SVYSHE` | `TIER_0_EXACT` | *Зва́нный свы́ше* | Podoben: Being called from on high | **Being called from on high** |
| `PODOBEN_NORMALIZED` | `C43:p422` | `POD.T4.KHOTEKH_SLEZAMI` | `TIER_0_EXACT` | *Хотѣ́хъ слеза́ми* | Podoben: With tears I desired | **With tears I desired** |
| `PODOBEN_NORMALIZED` | `C44:p439` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant among martyrs | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C44:p439` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant among martyrs | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C44:p440` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant among martyrs | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C44:p440` | `POD.T4.ZVANNYI_SVYSHE` | `TIER_0_EXACT` | *Зва́нный свы́ше* | Podoben: Being called from on high | **Being called from on high** |
| `PODOBEN_NORMALIZED` | `C46:p454` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant among martyrs | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C46:p455` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant among martyrs | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C47:p461` | `POD.T4.SKORO_PREDVARI` | `TIER_0_EXACT` | *Ско́рѡ предварѝ* | Podoben: Speedily anticipate | **Speedily anticipate** |
| `PODOBEN_NORMALIZED` | `C47:p462` | `POD.T4.SKORO_PREDVARI` | `TIER_0_EXACT` | *Ско́рѡ предварѝ* | Podoben: Speedily anticipate | **Speedily anticipate** |
| `PODOBEN_NORMALIZED` | `C48:p471` | `POD.T4.DALS_ESI_ZNAMENIE` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Да́лъ є҆сѝ зна́менїе* | Podoben: Thou hast given a sign | **Thou hast given a sign** |
| `PODOBEN_NORMALIZED` | `C48:p471` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant among martyrs | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C48:p472` | `POD.T4.ZVANNYI_SVYSHE` | `TIER_1_TYPOGRAPHIC_TITLO` | *: Зва́нный свы́ше* | Podoben: Being called from on high | **Being called from on high** |
| `PODOBEN_NORMALIZED` | `C49:p487` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant among martyrs | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C49:p488` | `POD.T4.DALS_ESI_ZNAMENIE` | `TIER_0_EXACT` | *Да́лъ е҆сѝ зна́меніе* | Podoben: Thou hast given a sign | **Thou hast given a sign** |
| `PODOBEN_SAME_NORMALIZED` | `C49:p488` | `POD.T4.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Martyrs, same Tone and Podoben (то́йже подо́бенъ):* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C51:p503` | `POD.T4.DALS_ESI_ZNAMENIE` | `TIER_0_EXACT` | *Да́лъ е҆сѝ зна́меніе* | Podoben: Thou hast given a sign | **Thou hast given a sign** |
| `PODOBEN_NORMALIZED` | `C51:p506` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_0_EXACT` | *Ра́дꙋйся по́стникѡвъ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C53:p524` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Podoben: The Word co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C53:p530` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Ра́дꙋйсѧ по́стникѡвъ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C54:p531` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_0_EXACT` | *Ра́дꙋйся по́стникѡвъ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C54:p537` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_1_TYPOGRAPHIC_TITLO` | *Собезна́чальное Сло́во* | Podoben: The Word co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C55:p545` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Ра́дꙋйсѧ по́стникѡвъ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_SAME_NORMALIZED` | `C55:p546` | `POD.T5.SAME` | `TIER_0_EXACT` | *то́йже* | *Tone and podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C55:p550` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Podoben: The Word co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C56:p552` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_1_TYPOGRAPHIC_TITLO` | *Собезна́чальное Сло́во* | Podoben: The Word co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C57:p562` | `POD.T5.RADUISYA_POSTNIKOV` | `SCRIBAL_INCIPIT_TRUNCATION` | *Ра́дꙋйсѧ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C57:p564` | `POD.T5.PREPODOBNE_OTCHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Преподо́бне Ѻ҆́ч҃е* | Podoben: O venerable father | **O venerable father** |
| `PODOBEN_NORMALIZED` | `C57:p569` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Podoben: The Word co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C58:p577` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Ра́дꙋйсѧ по́стникѡвъ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C58:p578` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Ра́дꙋйсѧ по́стникѡвъ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_SAME_NORMALIZED` | `C58:p579` | `POD.T5.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Holy Wonderworker Nicholas, Tone 5. The same Podoben (то́йже подо́бенъ):* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C59:p582` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Podoben: Co-beginningless Word | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C59:p584` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Podoben: Co-beginningless Word | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C60:p593` | `POD.T5.PREPODOBNE_OTCHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Преподо́бне ѻ҆́ч҃е* | Podoben: O venerable father | **O venerable father** |
| `PODOBEN_SAME_NORMALIZED` | `C60:p594` | `POD.T5.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Theotokos, Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C60:p594` | `POD.T5.RADUISYA_POSTNIKOV` | `SCRIBAL_INCIPIT_TRUNCATION` | *Ра́дꙋйсѧ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C60:p600` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Podoben: The Word co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C61:p607` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Ра́дꙋйсѧ по́стникѡвъ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C61:p608` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Ра́дꙋйсѧ по́стникѡвъ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C63:p623` | `POD.T5.RADUISYA_POSTNIKOV` | `SCRIBAL_INCIPIT_TRUNCATION` | *Ра́дꙋйсѧ* | Podoben: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C63:p626` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Podoben: Having laid aside all earthly hope | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C64:p634` | `POD.T6.EZHE_O_NAS` | `TIER_3_LEXICAL_RECENSIONAL` | *Є҆́же ѡ҆ на́съ соверши́въ* | Podoben: Fulfilling the dispensation for our sake | **Fulfilling the dispensation for our sake** |
| `PODOBEN_NORMALIZED` | `C64:p636` | `POD.T6.EZHE_O_NAS` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Є҆́же ѡ҆ на́съ* | Podoben: Fulfilling the dispensation for our sake | **Fulfilling the dispensation for our sake** |
| `PODOBEN_NORMALIZED` | `C66:p651` | `POD.T6.ANGELSKIYA_SILY` | `TIER_3_LEXICAL_RECENSIONAL` | *А҆́гг҃лскїѧ си́лы* | Podoben: The Angelic Powers | **The Angelic Powers** |
| `PODOBEN_NORMALIZED` | `C66:p652` | `POD.T6.TRIDNEVEN_VOSKRESL_ESI` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Тридне́внѡ воскре́слъ є҆сѝ* | Podoben: Having risen on the third day | **Having risen on the third day** |
| `PODOBEN_NORMALIZED` | `C66:p658` | `POD.T6.VSE_OTLOZHSHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Оу҆пова́нїе* | Podoben: The Hope | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C68:p672` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Podoben: Having laid all their hope | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C69:p682` | `POD.T6.TRIDNEVEN_VOSKRESL_ESI` | `TIER_3_LEXICAL_RECENSIONAL` | *Тридне́внѡ воскре́слъ є҆сѝ* | Podoben: Having risen on the third day | **Having risen on the third day** |
| `PODOBEN_SAME_NORMALIZED` | `C69:p682` | `POD.T6.SAME` | `TIER_0_EXACT` | *то́йже* | *Then the Stichera from the Menaion for the Saint, if there be any. If not, these Stichera: Tone and podoben the same.* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C69:p688` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Podoben: Having laid aside all earthly hope | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C70:p697` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Podoben: Having laid aside all earthly hope | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C70:p697` | `POD.T6.TRIDNEVEN_VOSKRESL_ESI` | `TIER_0_EXACT` | *Тридне́вно воскре́слъ е҆сѝ* | Podoben: Having risen on the third day | **Having risen on the third day** |
| `PODOBEN_NORMALIZED` | `C71:p704` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Podoben: Having laid aside all earthly hope | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C72:p712` | `POD.T6.ANGELSKIYA_SILY` | `TIER_0_EXACT` | *А҆́гг҃льскія си́лы* | Podoben: The Angelic Powers | **The Angelic Powers** |
| `PODOBEN_SAME_NORMALIZED` | `C72:p712` | `POD.T6.SAME` | `TIER_0_EXACT` | *то́йже* | *Tone and Podoben the same.* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C72:p713` | `POD.T6.TRIDNEVEN_VOSKRESL_ESI` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Тридне́внѡ воскре́слъ є҆сѝ* | Podoben: Having risen on the third day | **Having risen on the third day** |
| `PODOBEN_NORMALIZED` | `C73:p729` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Podoben: Having laid aside all earthly hope | **Having laid aside all earthly hope** |
| `PODOBEN_SAME_NORMALIZED` | `C73:p730` | `POD.T6.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Martyrs, Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C75:p744` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Podoben: Having laid aside all earthly hope | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C75:p749` | `POD.T2.EGDA_OT_DREVA` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Є҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C76:p755` | `POD.T7.IZHE_MENE_RADI` | `TIER_3_LEXICAL_RECENSIONAL` | *И҆́же менѐ ра́ди* | Podoben: He Who for my sake | **He Who for my sake** |
| `PODOBEN_NORMALIZED` | `C76:p756` | `POD.T7.OGNYA_SVETLEE` | `TIER_3_LEXICAL_RECENSIONAL` | *О҆гнѧ̀ свѣтлѣ́йши* | Podoben: Brighter than fire | **Brighter than fire** |
| `PODOBEN_NORMALIZED` | `C78:p771` | `POD.T7.DNES_BDIT_IUDA` | `TIER_3_LEXICAL_RECENSIONAL` | *Дне́сь бди́тъ І҆ꙋ́да* | Podoben: Today Judas watches | **Today Judas watches** |
| `PODOBEN_NORMALIZED` | `C78:p772` | `POD.T7.NE_KTOMU_VOZBRANENI` | `TIER_0_EXACT` | *Не ктомꙋ̀ возбране́ни е҆смы̀* | Podoben: No longer are we forbidden | **No longer are we forbidden** |
| `PODOBEN_NORMALIZED` | `C78:p777` | `POD.T7.PLOD_CHREVA` | `SCRIBAL_INCIPIT_TRUNCATION` | *Пло́дъ чре́ва* | Podoben: Fruit of thy womb | **Fruit of thy womb** |
| `PODOBEN_NORMALIZED` | `C79:p786` | `POD.T7.DNES_BDIT_IUDA` | `TIER_3_LEXICAL_RECENSIONAL` | *Дне́сь бди́тъ І҆ꙋ́да* | Podoben: Today Judas watches | **Today Judas watches** |
| `PODOBEN_NORMALIZED` | `C80:p791` | `POD.T7.PLOD_CHREVA` | `TIER_0_EXACT` | *Пло́дъ чре́ва твоегѡ̀* | Podoben: Fruit of thy womb | **Fruit of thy womb** |
| `PODOBEN_NORMALIZED` | `C81:p801` | `POD.T7.NE_KTOMU_VOZBRANENI` | `TIER_3_LEXICAL_RECENSIONAL` | *Не ктомꙋ̀ возбраня́еми є҆смы̀* | Podoben: No longer are we forbidden | **No longer are we forbidden** |
| `PODOBEN_NORMALIZED` | `C81:p802` | `POD.T7.DNES_BDIT_IUDA` | `TIER_3_LEXICAL_RECENSIONAL` | *Дне́сь бди́тъ І҆ꙋ́да* | Podoben: Today Judas watches | **Today Judas watches** |
| `PODOBEN_NORMALIZED` | `C82:p817` | `POD.T7.NE_KTOMU_VOZBRANENI` | `TIER_3_LEXICAL_RECENSIONAL` | *Не ктомꙋ̀ возбраня́еми є҆смы̀* | Podoben: No longer are we forbidden | **No longer are we forbidden** |
| `PODOBEN_SAME_NORMALIZED` | `C82:p817` | `POD.T7.SAME` | `TIER_0_EXACT` | *то́йже* | *Tone and Podoben the same.* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C83:p823` | `POD.T7.PLOD_CHREVA` | `SCRIBAL_INCIPIT_TRUNCATION` | *Пло́дъ чре́ва* | Podoben: Fruit of thy womb | **Fruit of thy womb** |
| `PODOBEN_NORMALIZED` | `C84:p832` | `POD.T7.NE_KTOMU_VOZBRANENI` | `TIER_0_EXACT` | *Не ктомꙋ̀ возбране́ни е҆смы̀* | Podoben: No longer are we forbidden | **No longer are we forbidden** |
| `PODOBEN_NORMALIZED` | `C84:p833` | `POD.T7.DNES_BDIT_IUDA` | `TIER_0_EXACT` | *Дне́сь бди́тъ І҆ю́да* | Podoben: Today Judas watches | **Today Judas watches** |
| `PODOBEN_NORMALIZED` | `C85:p846` | `POD.T7.NE_KTOMU_VOZBRANENI` | `TIER_0_EXACT` | *Не ктомꙋ̀ возбране́ни е҆смы̀* | Podoben: No longer are we forbidden | **No longer are we forbidden** |
| `PODOBEN_NORMALIZED` | `C87:p864` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Podoben: O most marvelous wonder | **O most marvelous wonder** |
| `PODOBEN_NORMALIZED` | `C87:p866` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant among martyrs | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C88:p873` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_0_EXACT` | *Повелѣ́нное та́инственно* | Podoben: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C88:p875` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_0_EXACT` | *Повелѣ́нное та́инственно* | Podoben: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C89:p884` | `POD.T8.YAKO_NACHATKI_ESTESTVA` | `TIER_0_EXACT` | *Я҆́кѡ нача́тки е҆стества̀* | Podoben: As first-fruits of nature | **As first-fruits of nature** |
| `PODOBEN_NORMALIZED` | `C89:p890` | `POD.T8.GOSPODI_ASHCHE_I_NA_SUDISHCHI` | `TIER_0_EXACT` | *Гдⷭ҇и, а҆́ще и҆ на сꙋди́щи* | Podoben: O Lord, though Thou didst stand before the tribunal | **O Lord, though Thou didst stand before the tribunal** |
| `PODOBEN_NORMALIZED` | `C90:p891` | `POD.T8.GOSPODI_ASHCHE_I_NA_SUDISHCHI` | `TIER_0_EXACT` | *Гдⷭ҇и, а҆́ще и҆ на сꙋди́щи* | Podoben: O Lord, though Thou didst stand before the tribunal | **O Lord, though Thou didst stand before the tribunal** |
| `PODOBEN_NORMALIZED` | `C90:p891` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Podoben: O most marvelous wonder | **O most marvelous wonder** |
| `PODOBEN_NORMALIZED` | `C90:p892` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Podoben: O most marvelous wonder | **O most marvelous wonder** |
| `PODOBEN_NORMALIZED` | `C90:p898` | `POD.T8.POVELENNOE_TAINSTVENNO` | `SCRIBAL_INCIPIT_TRUNCATION` | *Повелѣ́нное* | Podoben: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C91:p906` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Podoben: O most marvelous wonder | **O most marvelous wonder** |
| `PODOBEN_NORMALIZED` | `C91:p907` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Podoben: O most marvelous wonder | **O most marvelous wonder** |
| `PODOBEN_NORMALIZED` | `C93:p923` | `POD.T8.MUCHENITSY_GOSPODNI` | `TIER_0_EXACT` | *Мч҃ницы Гдⷭ҇ни* | Podoben: Martyrs of the Lord | **Martyrs of the Lord** |
| `PODOBEN_NORMALIZED` | `C93:p924` | `POD.T8.GOSPODI_ASHCHE_I_NA_SUDISHCHI` | `TIER_0_EXACT` | *Гдⷭ҇и, а҆́ще и҆ на сꙋди́щи* | Podoben: O Lord, though Thou didst stand before the tribunal | **O Lord, though Thou didst stand before the tribunal** |
| `PODOBEN_NORMALIZED` | `C93:p928` | `POD.T8.PREMUDROSTI_NASTAVNICHE` | `SCRIBAL_INCIPIT_TRUNCATION` | *Премꙋ́дрости* | Podoben: Guiding unto wisdom | **Guiding unto wisdom** |
| `PODOBEN_NORMALIZED` | `C93:p929` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_0_EXACT` | *Повелѣ́нное та́инственно* | Podoben: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C94:p940` | `POD.T8.GOSPODI_ASHCHE_I_NA_SUDISHCHI` | `TIER_0_EXACT` | *Гдⷭ҇и, а҆́ще и҆ на сꙋди́щи* | Podoben: O Lord, though Thou didst stand before the tribunal | **O Lord, though Thou didst stand before the tribunal** |
| `PODOBEN_NORMALIZED` | `C95:p947` | `POD.T8.POVELENNOE_TAINSTVENNO` | `SCRIBAL_INCIPIT_TRUNCATION` | *Повелѣ́нное* | Podoben: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C96:p956` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Podoben: O most marvelous wonder | **O most marvelous wonder** |
| `PODOBEN_SAME_NORMALIZED` | `C96:p956` | `POD.T8.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera, to the Most Holy Theotokos, Tone 8, Same Podoben.* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C97:p962` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_0_EXACT` | *Повелѣ́нное та́инственно* | Podoben: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C98:p974` | `POD.T8.CHTO_VAS_NARECHEM` | `SCRIBAL_INCIPIT_TRUNCATION` | *Что̀ ва́съ нарече́мъ* | Podoben: What shall we call you, O holy ones | **What shall we call you, O holy ones** |
| `PODOBEN_NORMALIZED` | `C98:p980` | `POD.T8.PREMUDROSTI_NASTAVNICHE` | `TIER_0_EXACT` | *Премꙋ́дрости наста́вниче* | Podoben: Guiding unto wisdom | **Guiding unto wisdom** |
| `PODOBEN_NORMALIZED` | `C99:p990` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Podoben: O most marvelous wonder | **O most marvelous wonder** |
| `PODOBEN_NORMALIZED` | `C101:p1006` | `POD.EXAP.ZHENY_USLYSHITE` | `TIER_1_TYPOGRAPHIC_TITLO` | *Жены̀ оу҆слы́шите* | Podoben: Give ear, ye women | **Give ear, ye women** |
| `PODOBEN_NORMALIZED` | `C101:p1006` | `POD.EXAP.ZHENY_USLYSHITE` | `TIER_1_TYPOGRAPHIC_TITLO` | *Жены̀ оу҆слы́шите* | Podoben: Thou Who didst adorn heaven with stars | **Give ear, ye women** |
| `PODOBEN_NORMALIZED` | `C101:p1007` | `POD.EXAP.ZHENY_USLYSHITE` | `TIER_1_TYPOGRAPHIC_TITLO` | *Жены̀ оу҆слы́шите* | Podoben: Give ear, ye women | **Give ear, ye women** |
| `PODOBEN_NORMALIZED` | `C101:p1007` | `POD.EXAP.ZHENY_USLYSHITE` | `TIER_1_TYPOGRAPHIC_TITLO` | *Жены̀ оу҆слы́шите* | Podoben: Give ear, ye women | **Give ear, ye women** |