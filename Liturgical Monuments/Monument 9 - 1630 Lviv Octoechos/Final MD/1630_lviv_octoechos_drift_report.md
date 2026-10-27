# Scholarly Drift & Seam-Stitching Audit Report: 1630 Lviv Octoechos

- **Monument ID**: `1630_lviv_octoechos`
- **Total 2-Up Mid-Sentence Seams Stitched**: 466 boundaries (`79` sub-clause seam overlaps deduplicated)
- **Inline Locus Milestones Inserted**: `[f. XvA]`, `[f. XrA]` across all 267 leaves
- **Total Primitive Normalization & Drift Events**: 349 (`150` Podobens/Pokoin, `70` Psalm Stichoi, `50` Weekday Heirmoi, `79` Seam Deduplications)
- **True Pre-Normalization AI Translation Drift Unified**: 296 occurrences
- **Source-Text (1630 Slavonic) Scribal Truncations & Tier 3 Variations Classified**: 77 events

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
| `PODOBEN_NORMALIZED` | `C01:p9` | `POD.T1.KAMENI_ZAPECHATLENU` | `TIER_3_LEXICAL_RECENSIONAL` | *Камени запечат* | Model: When the stone had been sealed | **When the stone had been sealed** |
| `PODOBEN_NORMALIZED` | `C01:p9` | `POD.T1.GROB_TVOI_SPASE` | `TIER_3_LEXICAL_RECENSIONAL` | *Гробъ твои Сп̃се* | Model: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C01:p10` | `POD.T1.EGDA_PRIIDESHI` | `TIER_3_LEXICAL_RECENSIONAL` | *Егда прїидеши* | Model: When Thou shalt come | **When Thou shalt come** |
| `PODOBEN_NORMALIZED` | `C02:p12` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_3_LEXICAL_RECENSIONAL` | *Прехвальніи мч̃нци* | Model: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C02:p12` | `POD.T1.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Bodiless Powers, the same Tone and Model.* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C02:p16` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_3_LEXICAL_RECENSIONAL` | *Прехвальніи мч̃нци* | Model: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C02:p17` | `POD.T1.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Forerunner. The same Model:* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C02:p17` | `POD.T1.GROB_TVOI_SPASE` | `TIER_3_LEXICAL_RECENSIONAL` | *Гробъ твои Сп̃се* | Model: While the soldiers were guarding Thy tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C03:p21` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_3_LEXICAL_RECENSIONAL` | *Прехвальніи мчнци* | Model: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C03:p21` | `POD.T1.NEBESNYKH_CHINOV` | `TIER_3_LEXICAL_RECENSIONAL` | *Небнымъ чиномъ* | Model: Of the heavenly ranks | **Joy of the heavenly ranks** |
| `PODOBEN_NORMALIZED` | `C03:p22` | `POD.T1.GROB_TVOI_SPASE` | `TIER_3_LEXICAL_RECENSIONAL` | *Гробъ твои Сп҃се* | Model: Thy tomb, O Savior | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C03:p25` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_3_LEXICAL_RECENSIONAL` | *Прехвальніи мꙋнци* | Model: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C03:p25` | `POD.T1.NEBESNYKH_CHINOV` | `TIER_0_EXACT` | *Небе́сныхъ чинѡ́въ* | Model: Of the heavenly ranks | **Joy of the heavenly ranks** |
| `PODOBEN_NORMALIZED` | `C03:p29` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_3_LEXICAL_RECENSIONAL` | *Прехвальніи, мꙋнци* | Model: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C03:p29` | `POD.T1.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera, Stavrotheotokia, Tone 1. Model: The same:* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C04:p32` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_3_LEXICAL_RECENSIONAL` | *Прехвальніи мꙋнцы* | Model: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C04:p33` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_3_LEXICAL_RECENSIONAL` | *Прехвальніи мꙋнци* | Model: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C04:p36` | `POD.T2.EGDA_OT_DREVA` | `TIER_3_LEXICAL_RECENSIONAL` | *Егда́ ѡ҆ дре́ва* | Model: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C04:p38` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_3_LEXICAL_RECENSIONAL` | *Прехвальніи мꙋнцы* | Model: O all-lauded martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C04:p39` | `POD.T2.VYSHNIKH_ISHCHA` | `TIER_1_TYPOGRAPHIC_TITLO` | *Вы́шнихъ и҆щѧ* | Model: Seeking the highest | **Seeking the highest** |
| `PODOBEN_NORMALIZED` | `C04:p40` | `POD.T2.VYSHNIKH_ISHCHA` | `TIER_1_TYPOGRAPHIC_TITLO` | *Вы́шнихъ и҆щѧ* | Model: Seeking the highest | **Seeking the highest** |
| `PODOBEN_NORMALIZED` | `C05:p43` | `POD.T2.EGDA_OT_DREVA` | `TIER_3_LEXICAL_RECENSIONAL` | *Егда ѡ древа* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C05:p44` | `POD.T2.SAME` | `TIER_0_EXACT` | *то́йже* | *Tone and Podoben: The same.* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C05:p44` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_3_LEXICAL_RECENSIONAL` | *Милосердіа сꙋщи исто* | Podoben: Being the Wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C05:p47` | `POD.T2.EGDA_OT_DREVA` | `TIER_3_LEXICAL_RECENSIONAL` | *[Егда ѡ древа:]* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C05:p48` | `POD.T2.SAME` | `TIER_0_EXACT` | *то́йже* | *Tone and Podoben: The same.* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C05:p48` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_3_LEXICAL_RECENSIONAL` | *Милосердіа сꙋщи исто* | Podoben: Being the Wellspring of loving-kindness | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C06:p52` | `POD.T2.EGDA_OT_DREVA` | `TIER_1_TYPOGRAPHIC_TITLO` | *Егда́ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C06:p52` | `POD.T2.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Most Holy Theotokos. Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C06:p53` | `POD.T2.MILOSERDIA_SUSHCHI` | `SCRIBAL_INCIPIT_TRUNCATION` | *Милосе́рдїа сꙋ́щи* | Model: Being full of compassion | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C06:p53` | `POD.T2.MILOSERDIA_SUSHCHI` | `SCRIBAL_INCIPIT_TRUNCATION` | *Милосе́рдїа сꙋ́щи* | Model: Being full of compassion | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C06:p56` | `POD.T2.EGDA_OT_DREVA` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Егда́ ѿ дрѣ́ва* | Model: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C06:p56` | `POD.T2.EGDA_OT_DREVA` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Егда́ ѿ дрѣ́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C06:p56` | `POD.T2.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to Saint Nicholas. Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C06:p57` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_3_LEXICAL_RECENSIONAL` | *г҃. стїхолосїи: Гла́с, в҃. По: Милосе́рдїа сꙋ́щи* | Model: Being full of compassion | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C06:p60` | `POD.T2.EGDA_OT_DREVA` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Егда́ ѿ дрѣ́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C06:p60` | `POD.T2.SAME` | `TIER_0_EXACT` | *то́йже* | *Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C07:p61` | `POD.T2.EGDA_OT_DREVA` | `TIER_3_LEXICAL_RECENSIONAL` | *Егда́ ѿ дре́ва та* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C07:p64` | `POD.T2.EGDA_OT_DREVA` | `TIER_1_TYPOGRAPHIC_TITLO` | *Егда́ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C07:p65` | `POD.T2.EGDA_OT_DREVA` | `TIER_1_TYPOGRAPHIC_TITLO` | *Егда́ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C07:p65` | `POD.T2.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Martyrs. Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `POKOIN_ABBREV_CORRECTED` | `C07:p65` | `N/A` | `TIER_1_TYPOGRAPHIC_TITLO` | *Поко́инъ* | *Podoben:* | ***Hymn for the Departed (Поко́инъ):*** |
| `PODOBEN_NORMALIZED` | `C07:p68` | `POD.T2.EGDA_OT_DREVA` | `TIER_3_LEXICAL_RECENSIONAL` | *Егда́ ѿ дре́ва та* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C07:p70` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: At the beauty of virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C08:p71` | `POD.T3.KRASOTE_DEVSTVA` | `SCRIBAL_INCIPIT_TRUNCATION` | *Красотѣ дѣвства* | Podoben: At the beauty of virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C08:p73` | `POD.T3.DELA_DNIA` | `TIER_1_TYPOGRAPHIC_TITLO` | *Дѣла дніа* | Podoben: The works of the day | **The works of the day** |
| `PODOBEN_NORMALIZED` | `C08:p76` | `POD.T3.VELIA_MUCHENIK_TVOIKH` | `TIER_3_LEXICAL_RECENSIONAL` | *Веліа мчникъ твои* | Podoben: Great is the martyr | **Great is the power of Thy martyrs** |
| `PODOBEN_NORMALIZED` | `C08:p76` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: At the beauty of virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C08:p80` | `POD.T3.KRESTOOBRAZNO` | `TIER_3_LEXICAL_RECENSIONAL` | *Кртаѡбразно* | Podoben: In the likeness of the Cross | **In the likeness of the Cross** |
| `PODOBEN_NORMALIZED` | `C09:p81` | `POD.T3.BOZHESTVENNYYA_VERY` | `TIER_3_LEXICAL_RECENSIONAL` | *Бжтвенныя вѣры* | Podoben: Of the divine faith | **Of the divine faith** |
| `PODOBEN_NORMALIZED` | `C09:p81` | `POD.T3.KRASOTE_DEVSTVA` | `SCRIBAL_INCIPIT_TRUNCATION` | *Красотѣ дѣвтва* | Podoben: The beauty of virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C09:p84` | `POD.T3.VELIA_MUCHENIK_TVOIKH` | `TIER_3_LEXICAL_RECENSIONAL` | *Веліа мункъ твои* | Podoben: Great is the power of Thy Martyrs | **Great is the power of Thy martyrs** |
| `PODOBEN_NORMALIZED` | `C09:p85` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: The beauty of virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C09:p89` | `POD.T3.VELIA_MUCHENIK_TVOIKH` | `SCRIBAL_INCIPIT_TRUNCATION` | *Веліа мункъ* | Podoben: Great is the power of Thy Martyrs | **Great is the power of Thy martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C09:p89` | `POD.T3.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to Saint Nicholas, Tone 3. Podoben: The same:* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C10:p93` | `POD.T3.POSTAVISHA_TRIDESYATE` | `TIER_0_EXACT` | *Поста́виша три́десѧте* | Model: They weighed thirty pieces of silver | **They weighed thirty pieces of silver** |
| `PODOBEN_NORMALIZED` | `C10:p97` | `POD.T3.VELIA_MUCHENIK_TVOIKH` | `TIER_3_LEXICAL_RECENSIONAL` | *Веліа му́никъ твоихъ* | Model: Great is the power of Thy martyrs | **Great is the power of Thy martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C10:p97` | `POD.T3.SAME` | `TIER_0_EXACT` | *то́йже* | Tone and Model the same. | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C11:p101` | `POD.T3.VELIA_KRESTA_TVOEGO` | `TIER_3_LEXICAL_RECENSIONAL` | *Ве́ліа Кр́та твое́го Гди* | To: Great is the power of Thy Cross, O Lord | **Great is the power of Thy Cross, O Lord** |
| `PODOBEN_NORMALIZED` | `C11:p102` | `POD.T4.ZVANNYI_SVYSHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Зва́нный бы́вше* | To: Being called from on high | **Being called from on high** |
| `PODOBEN_NORMALIZED` | `C11:p106` | `POD.T4.UDIVISYA_IOSIF` | `SCRIBAL_INCIPIT_TRUNCATION` | *По: [Оу҆диви́ся І҆ѡ́сифъ]* | Resurrectional. Tone 4. To: | **Joseph was amazed** |
| `PODOBEN_NORMALIZED` | `C11:p110` | `POD.T4.DALS_ESI_ZNAMENIE` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Да́лъ есѝ зна́менїе* | To: Thou hast given a sign | **Thou hast given a sign** |
| `PODOBEN_NORMALIZED` | `C11:p110` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | To: As one noble | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C12:p114` | `POD.T4.KHOTEKH_SLEZAMI` | `TIER_0_EXACT` | *Хотѣ́хъ слеза́ми* | To: With tears I desired | **With tears I desired** |
| `PODOBEN_NORMALIZED` | `C12:p119` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | To: As one noble | **As one valiant among martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C12:p119` | `POD.T4.SAME` | `TIER_0_EXACT` | *то́йже* | Tone 4. Same melody. | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C13:p122` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | To: As one noble | **As one valiant among martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C13:p123` | `POD.T4.SAME` | `TIER_0_EXACT` | *то́йже* | Other Stichera to Saint Nicholas, Tone 4. Same melody: | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C13:p127` | `POD.T4.DALS_ESI_ZNAMENIE` | `TIER_3_LEXICAL_RECENSIONAL` | *Да́лъ єсѝ зна́ме* | To: Thou hast given a sign | **Thou hast given a sign** |
| `PODOBEN_NORMALIZED` | `C13:p128` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | To: As one noble | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C14:p132` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Podoben: As one valiant | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C14:p132` | `POD.T4.DALS_ESI_ZNAMENIE` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Да́лъ єсѝ зна́менїе* | Podoben: Thou hast given a sign | **Thou hast given a sign** |
| `PODOBEN_SAME_NORMALIZED` | `C14:p132` | `POD.T4.SAME` | `TIER_0_EXACT` | *то́йже* | Other Stichera to the Holy Martyrs. Tone and Podoben the same: | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `POKOIN_ABBREV_CORRECTED` | `C14:p132` | `N/A` | `TIER_1_TYPOGRAPHIC_TITLO` | *По[ко́инъ]:* | For the Departed: Podoben: | ***Hymn for the Departed (Поко́инъ):*** |
| `PODOBEN_NORMALIZED` | `C14:p136` | `POD.T4.DALS_ESI_ZNAMENIE` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Да́лъ єсѝ зна́менїе* | Podoben: Thou hast given a sign | **Thou hast given a sign** |
| `PODOBEN_NORMALIZED` | `C14:p136` | `POD.T5.RADUISYA_ZHIVONOSNYI_KRESTE` | `SCRIBAL_INCIPIT_TRUNCATION` | *Ра́дꙋйся живоно* | Podoben: Rejoice, life-bearing [Cross] | **Rejoice, O life-bearing Cross** |
| `PODOBEN_NORMALIZED` | `C14:p138` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_3_LEXICAL_RECENSIONAL` | *Собезнача́лно Сло́во* | Podoben: The Word co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C14:p139` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_3_LEXICAL_RECENSIONAL` | *Собезна́чално Слово* | Podoben: The Word co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C15:p142` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Model: Co-unoriginate Word | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C15:p144` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_0_EXACT` | *Ра́дꙋйся по́стникѡвъ* | Model: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C15:p145` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Model: Co-unoriginate Word | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C15:p148` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_0_EXACT` | *Ра́дꙋйся по́стникѡвъ* | Model: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C15:p149` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Model: Co-unoriginate Word | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C16:p152` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Ра́дꙋйсѧ по́стникѡвъ* | Melodic model: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C16:p153` | `POD.T5.PREPODOBNE_OTCHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Преподо́бне ѻ҆́ч҃е* | Melodic model: O venerable father | **O venerable father** |
| `PODOBEN_NORMALIZED` | `C16:p153` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Melodic model: The Word co-beginningless | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C16:p156` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_3_LEXICAL_RECENSIONAL` | *Ра́дꙋйсѧ по́стникѡмъ* | Melodic model: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C16:p156` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_3_LEXICAL_RECENSIONAL` | *Ра́дꙋйсѧ по́стникѡмъ* | Melodic model: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_SAME_NORMALIZED` | `C16:p157` | `POD.T5.SAME` | `TIER_0_EXACT` | *то́йже* | Other Stichera to Saint Nicholas, Tone and melodic model the same: | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C16:p157` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Melodic model: The Word co-beginningless | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C16:p160` | `POD.T5.PREPODOBNE_OTCHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Преподо́бне ѻ҆́ч҃е* | Melodic model: O venerable father | **O venerable father** |
| `PODOBEN_NORMALIZED` | `C17:p161` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_3_LEXICAL_RECENSIONAL` | *Ра́дꙋйсѧ по́стничкѡмъ* | Melodic model: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C17:p161` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Melodic model: The Word co-beginningless | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C17:p164` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_3_LEXICAL_RECENSIONAL` | *Ра́дꙋйся по́стничкѡмъ* | Melodic model: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C17:p164` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_3_LEXICAL_RECENSIONAL` | *Ра́дꙋйся по́стничкѡмъ* | Melodic model: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C17:p168` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_3_LEXICAL_RECENSIONAL` | *Ра́дꙋйся по́стникѡ* | Melodic model: Rejoice, O container of ascetics | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C17:p169` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Melodic model: Having laid all their hope | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C18:p171` | `POD.T6.EZHE_O_NAS` | `TIER_0_EXACT` | *Е҆́же ѡ҆ на́съ* | Model: Fulfilling the dispensation | **Fulfilling the dispensation for our sake** |
| `PODOBEN_NORMALIZED` | `C18:p177` | `POD.T6.ANGELSKIYA_SILY` | `TIER_3_LEXICAL_RECENSIONAL` | *А҆́гг҃лскїѧ си́лы* | Model: The Angelic Hosts | **The Angelic Powers** |
| `PODOBEN_NORMALIZED` | `C18:p177` | `POD.T6.TRIDNEVEN_VOSKRESL_ESI` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Тридне́вно воскре́слъ є҆сѝ* | Model: Having Risen on the Third Day | **Having risen on the third day** |
| `PODOBEN_NORMALIZED` | `C18:p178` | `POD.T6.VSE_OTLOZHSHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Всѐ ᲂу҆пова́нїе* | Model: All my Hope | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C18:p178` | `POD.T6.YAKO_POSUKHU_KHODIV` | `TIER_0_EXACT` | *Я҆́кѡ посꙋ́хꙋ ходи́въ* | Model: Having Walked as on Dry Land | **Having walked as on dry land** |
| `PODOBEN_NORMALIZED` | `C19:p181` | `POD.T6.TRIDNEVEN_VOSKRESL_ESI` | `TIER_0_EXACT` | *Тридне́вно воскре́слъ е҆сѝ* | Model: Having risen on the third day | **Having risen on the third day** |
| `PODOBEN_NORMALIZED` | `C19:p182` | `POD.T6.VSE_OTLOZHSHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Все оу҆пова́нїе на нб҃сѣхъ* | Model: All our hope is in heaven | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C19:p184` | `POD.T6.VSE_OTLOZHSHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Всю̀ ѿложи́вше* | Model: Having laid aside all | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C19:p185` | `POD.T6.TRIDNEVEN_VOSKRESL_ESI` | `TIER_0_EXACT` | *Тридне́вно воскре́слъ е҆сѝ* | Model: Having risen on the third day | **Having risen on the third day** |
| `PODOBEN_SAME_NORMALIZED` | `C19:p185` | `POD.T6.SAME` | `TIER_0_EXACT` | *то́йже* | Tone and Model: The same. | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C19:p185` | `POD.T6.VSE_OTLOZHSHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Все оу҆пова́нїе на нб҃сѣхъ* | Model: All our hope is in heaven | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C19:p188` | `POD.T6.ANGELSKIYA_SILY` | `TIER_3_LEXICAL_RECENSIONAL` | *А҆́ггл҃скїѧ пред̾и́дꙋтъ си́лы* | Model: The angelic hosts shall go before | **The Angelic Powers** |
| `PODOBEN_SAME_NORMALIZED` | `C19:p188` | `POD.T6.SAME` | `TIER_0_EXACT` | *то́йже* | Tone and Model: The same. | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C20:p193` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Model: Having set aside all | **Having laid aside all earthly hope** |
| `PODOBEN_SAME_NORMALIZED` | `C20:p193` | `POD.T6.SAME` | `TIER_0_EXACT` | *то́йже* | Same Tone and Model. | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C20:p196` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Model: Having set aside all | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C20:p200` | `POD.T6.OGNYA_OSTROV` | `TIER_0_EXACT` | *О҆гня̀ ѡ҆стро́въ* | Model: The island of fire | **The island of fire** |
| `PODOBEN_NORMALIZED` | `C21:p205` | `POD.T7.DNES_BDIT_IUDA` | `TIER_1_TYPOGRAPHIC_TITLO` | *Дне́сь бди́тъ Ію́да* | Model: Today Judas watches | **Today Judas watches** |
| `PODOBEN_NORMALIZED` | `C21:p205` | `POD.T7.NE_KTOMU_VOZBRANENI` | `TIER_1_TYPOGRAPHIC_TITLO` | *Не ктомꙋ̀ возбране́ни есмы̀* | Model: We are no longer forbidden | **No longer are we forbidden** |
| `PODOBEN_NORMALIZED` | `C21:p206` | `POD.T7.PLOD_CHREVA` | `SCRIBAL_INCIPIT_TRUNCATION` | *Пло́дъ чре́ва* | Model: Fruit of the womb | **Fruit of thy womb** |
| `PODOBEN_NORMALIZED` | `C21:p208` | `POD.T7.DNES_BDIT_IUDA` | `TIER_1_TYPOGRAPHIC_TITLO` | *Дне́сь бди́тъ Ію́да* | Model: Today Judas watches | **Today Judas watches** |
| `PODOBEN_NORMALIZED` | `C21:p209` | `POD.T7.PLOD_CHREVA` | `TIER_1_TYPOGRAPHIC_TITLO` | *Пло́дъ чре́ва твоегѡ́* | Model: Fruit of Thy womb | **Fruit of thy womb** |
| `PODOBEN_NORMALIZED` | `C22:p212` | `POD.T7.NE_KTOMU_VOZBRANENI` | `TIER_0_EXACT` | *Не ктомꙋ̀ возбране́ни е҆смы̀* | Model: No longer are we forbidden | **No longer are we forbidden** |
| `PODOBEN_NORMALIZED` | `C22:p212` | `POD.T7.DNES_BDIT_IUDA` | `SCRIBAL_INCIPIT_TRUNCATION` | *Дне́сь І҆ꙋ́да* | Model: Today Judas | **Today Judas watches** |
| `PODOBEN_NORMALIZED` | `C22:p216` | `POD.T7.NE_KTOMU_VOZBRANENI` | `TIER_0_EXACT` | *Не ктомꙋ̀ возбране́ни е҆смы̀* | Model: No longer are we forbidden | **No longer are we forbidden** |
| `PODOBEN_SAME_NORMALIZED` | `C22:p217` | `POD.T7.SAME` | `TIER_0_EXACT` | *то́йже* | Tone 7. Same Model: | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C22:p217` | `POD.T7.PLOD_CHREVA` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Пло́дъ чре́ва твое́го* | Model: The fruit of thy womb | **Fruit of thy womb** |
| `PODOBEN_NORMALIZED` | `C22:p220` | `POD.T7.NE_KTOMU_VOZBRANENI` | `TIER_0_EXACT` | *Не ктомꙋ̀ возбране́ни е҆смы̀* | Model: No longer are we forbidden | **No longer are we forbidden** |
| `PODOBEN_NORMALIZED` | `C22:p220` | `POD.T7.DNES_BDIT_IUDA` | `SCRIBAL_INCIPIT_TRUNCATION` | *Дне́сь І҆ꙋ́да* | Model: Today Judas | **Today Judas watches** |
| `PODOBEN_NORMALIZED` | `C23:p223` | `POD.T7.NE_KTOMU_VOZBRANENI` | `TIER_3_LEXICAL_RECENSIONAL` | *Нїкто́мꙋ возбра́няеми* | Model: No longer are we forbidden | **No longer are we forbidden** |
| `POKOIN_ABBREV_CORRECTED` | `C23:p224` | `N/A` | `TIER_1_TYPOGRAPHIC_TITLO` | *Поко́инъ* | Model: | ***Hymn for the Departed (Поко́инъ):*** |
| `POKOIN_ABBREV_CORRECTED` | `C23:p224` | `N/A` | `TIER_1_TYPOGRAPHIC_TITLO` | *Поко́инъ* | Model: | ***Hymn for the Departed (Поко́инъ):*** |
| `PODOBEN_NORMALIZED` | `C23:p227` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_0_EXACT` | *Ра́дꙋйся по́стникѡвъ* | Model: Rejoice | **Rejoice, O container of ascetics** |
| `PODOBEN_NORMALIZED` | `C23:p228` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_1_TYPOGRAPHIC_TITLO` | *Пове́лѣнное та́инственно* | Model: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C23:p229` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_0_EXACT` | *Повелѣ́нное та́инственно* | Model: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C24:p232` | `POD.T8.YAKO_NACHATKI_ESTESTVA` | `TIER_0_EXACT` | *Я҆́кѡ нача́тки е҆стества̀* | Model: As first-fruits of nature | **As first-fruits of nature** |
| `PODOBEN_NORMALIZED` | `C24:p234` | `POD.T8.GOSPODI_ASHCHE_I_NA_SUDISHCHI` | `TIER_1_TYPOGRAPHIC_TITLO` | *Гдⷭи, а҆́ще и҆ на сꙋди́щи* | Model: O Lord, though Thou didst stand before the tribunal | **O Lord, though Thou didst stand before the tribunal** |
| `PODOBEN_NORMALIZED` | `C24:p235` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_3_LEXICAL_RECENSIONAL` | *Повеле́нное таинство* | Model: The commanded mystery | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C24:p238` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Model: O most marvelous wonder | **O most marvelous wonder** |
| `PODOBEN_SAME_NORMALIZED` | `C24:p238` | `POD.T8.SAME` | `TIER_0_EXACT` | *то́йже* | Other Stichera to the Forerunner John. Same Tone and Model: | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C24:p239` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_3_LEXICAL_RECENSIONAL` | *Повеле́нное та́инство* | Model: The commanded mystery | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C25:p242` | `POD.T8.MUCHENITSY_GOSPODNI` | `TIER_3_LEXICAL_RECENSIONAL` | *Мч҃нци Гдⷭ҇ни* | Model: Martyrs of the Lord | **Martyrs of the Lord** |
| `PODOBEN_NORMALIZED` | `C25:p243` | `POD.T8.GOSPODI_ASHCHE_I_NA_SUDISHCHI` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Гдⷭ҇и, аще и на судїщи* | Model: O Lord, though Thou didst stand before the tribunal | **O Lord, though Thou didst stand before the tribunal** |
| `PODOBEN_NORMALIZED` | `C25:p243` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Повеленное таинственно* | Model: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C25:p247` | `POD.T8.GOSPODI_ASHCHE_I_NA_SUDISHCHI` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Гдⷭ҇и, аще и на судїщи* | Model: O Lord, though Thou didst stand before the tribunal | **O Lord, though Thou didst stand before the tribunal** |
| `PODOBEN_NORMALIZED` | `C25:p247` | `POD.T8.GOSPODI_ASHCHE_I_NA_SUDISHCHI` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Гдⷭ҇и, аще и на судїщи* | Model: O Lord, though Thou didst stand before the tribunal | **O Lord, though Thou didst stand before the tribunal** |
| `PODOBEN_NORMALIZED` | `C25:p247` | `POD.T8.PREMUDROSTI_NASTAVNICHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Премꙋдрости напꙋтл* | Model: Guiding unto wisdom | **Guiding unto wisdom** |
| `PODOBEN_NORMALIZED` | `C25:p248` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Повеленное таинственно* | Model: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C26:p251` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_3_LEXICAL_RECENSIONAL` | *О преславное чудо* | Model: O most glorious wonder | **O most marvelous wonder** |
| `PODOBEN_NORMALIZED` | `C26:p252` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_1_TYPOGRAPHIC_TITLO` | *Повелѣнное таинственно* | Model: That which was commanded mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C26:p256` | `POD.T8.CHTO_VAS_NARECHEM` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Что вы наречемъ ст҃ыи;* | Model: What shall we call you, O holy ones? | **What shall we call you, O holy ones** |
| `PODOBEN_NORMALIZED` | `C26:p257` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_0_EXACT` | *Повелѣ́нное та́инственно* | Model: Having received mystically | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C26:p260` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_3_LEXICAL_RECENSIONAL` | *О преславное чудо* | Model: O most glorious wonder | **O most marvelous wonder** |