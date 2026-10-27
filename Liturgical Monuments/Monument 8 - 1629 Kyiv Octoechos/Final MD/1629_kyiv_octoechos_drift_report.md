# Scholarly Drift & Seam-Stitching Audit Report: 1629 Kyiv-Pechersk Octoechos

- **Monument ID**: `1629_kyiv_octoechos`
- **Total 2-Up Mid-Sentence Seams Stitched**: 305 boundaries (`71` sub-clause seam overlaps deduplicated)
- **Inline Locus Milestones Inserted**: `[f. XvA]`, `[f. XrA]` across all 295 leaves
- **Total Primitive Normalization & Drift Events**: 150 (`42` Podobens/Pokoin, `5` Psalm Stichoi, `32` Weekday Heirmoi, `71` Seam Deduplications)
- **True Pre-Normalization AI Translation Drift Unified**: 137 occurrences
- **Source-Text (1629 Slavonic) Scribal Truncations & Tier 3 Variations Classified**: 16 events

---

## 1. Summary of 3-Tier Source & Scribal Drift Engine

1. **Tier 1 (Typographic / Titlo Equivalence)**: Strips accents, titla, and sacred abbreviations (`бг҃` -> `богъ`). Unified silently to canonical English.
2. **Tier 2 (Orthographic / Phonological Variant)**: Harmonizes Ruthenian/Church Slavonic vowel and yer reflexes (`ѡ`/`о`, `ѣ`/`е`, `ꙋ`/`у`, `ᲂу`/`у`). Unified to canonical English while logging orthographic drift.
3. **Scribal Incipit Truncation (`SCRIBAL_INCIPIT_TRUNCATION`)**: The printer/scribe abbreviated the model incipit on the physical leaf (e.g. `По̀, Дв҃аа` for `Дѣ́ва дне́сь`, or omitted `Подо́бенъ` before the incipit). Classified as a scribal convention, never counted as AI translation error.
4. **Tier 3 (Lexical / Syntactic / Recensional Variant)**: Genuine source variations in the 1629 print. **Preserved as distinct English translations** and annotated.

---

## 2. Complete Podoben & Rubric Drift Log

| Type | Locus | ID | Drift Tier | 1629 Slavonic Witness | Pre-Normalization Cohort Text | Canonical Normalized Reading |
| :--- | :---: | :--- | :---: | :--- | :--- | :--- |
| `PODOBEN_NORMALIZED` | `C01:p7` | `POD.T1.GROB_TVOI_SPASE` | `SCRIBAL_INCIPIT_TRUNCATION` | *Гро́бъ тво́й* | Podoben: Thy Tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C01:p9` | `POD.T1.GROB_TVOI_SPASE` | `SCRIBAL_INCIPIT_TRUNCATION` | *Гро́бъ тво́й* | Podoben: Thy Tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C03:p27` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `SCRIBAL_INCIPIT_TRUNCATION` | *Прехва́лныи* | Podoben: O most praised martyrs | **O all-lauded martyrs** |
| `PODOBEN_SAME_NORMALIZED` | `C03:p27` | `POD.T1.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera, to the Bodiless Hosts. Podoben: the same.* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C04:p33` | `POD.T2.VYSHNIKH_ISHCHA` | `TIER_0_EXACT` | *Вы́шнихъ и҆щѧ̀* | Prosomoion: Having sought the things on high | **Seeking the highest** |
| `PODOBEN_NORMALIZED` | `C04:p35` | `POD.T2.VYSHNIKH_ISHCHA` | `TIER_0_EXACT` | *Вы́шнихъ и҆щѧ̀* | Prosomoion: Having sought the things on high | **Seeking the highest** |
| `PODOBEN_NORMALIZED` | `C05:p50` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C05:p50` | `POD.T2.SAME` | `TIER_0_EXACT` | *то́йже* | *Podoben: The same.* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C06:p56` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: Awed by the beauty of thy virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C06:p58` | `POD.T3.DEVA_DNESS` | `SCRIBAL_INCIPIT_TRUNCATION` | *Дв҃аа* | Podoben: Today the Virgin | **Today the Virgin** |
| `PODOBEN_NORMALIZED` | `C08:p73` | `POD.T3.VELIA_KRESTA_TVOEGO` | `TIER_3_LEXICAL_RECENSIONAL` | *Ве́ліа крⷭ҇та твое́го Гдⷭ҇и си́ла* | Model: Great is the power of Thy Cross, O Lord | **Great is the power of Thy Cross, O Lord** |
| `PODOBEN_NORMALIZED` | `C08:p79` | `POD.T4.SKORO_PREDVARI` | `TIER_0_EXACT` | *Ско́рѡ предварѝ* | Model: Speedily anticipate | **Speedily anticipate** |
| `PODOBEN_NORMALIZED` | `C09:p81` | `POD.T4.VOZNESYISYA_NA_KREST` | `SCRIBAL_INCIPIT_TRUNCATION` | *Вознесы́йсѧ на крⷭ҇тъ* | Model: Thou Who wast lifted up upon the Cross | **Thou Who wast lifted up upon the Cross** |
| `PODOBEN_NORMALIZED` | `C10:p98` | `POD.T4.DALS_ESI_ZNAMENIE` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Да́лъ є҆сѝ зна́менїе* | Model: Thou hast given a sign | **Thou hast given a sign** |
| `PODOBEN_NORMALIZED` | `C10:p98` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Model: As one noble | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C11:p104` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Model: Co-unoriginate Word | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C11:p106` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Model: Co-unoriginate Word | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C13:p122` | `POD.T5.RADUISYA_POSTNIKOV` | `TIER_3_LEXICAL_RECENSIONAL` | *Ра́дꙋйсѧ по́стническїи* | Podoben: Rejoice, thou bearer of the ascetic life | **Rejoice, O container of ascetics** |
| `PODOBEN_SAME_NORMALIZED` | `C13:p123` | `POD.T5.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Bodiless Powers. Podoben: The same:* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C13:p129` | `POD.T6.EZHE_O_NAS` | `TIER_3_LEXICAL_RECENSIONAL` | *Єже ѡ на* | Podoben: Having fulfilled the dispensation | **Fulfilling the dispensation for our sake** |
| `PODOBEN_NORMALIZED` | `C14:p131` | `POD.T6.EZHE_O_NAS` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Єже ѡ насъ* | Model: Fulfilling the dispensation for us | **Fulfilling the dispensation for our sake** |
| `PODOBEN_NORMALIZED` | `C15:p148` | `POD.T6.ANGELSKIYA_SILY` | `TIER_0_EXACT` | *А҆́гг҃льскія си́лы* | Model: The angelic hosts go before | **The Angelic Powers** |
| `PODOBEN_NORMALIZED` | `C15:p149` | `POD.T6.TRIDNEVEN_VOSKRESL_ESI` | `TIER_0_EXACT` | *Тридне́вно воскре́слъ е҆сѝ* | Model: Risen on the third day | **Having risen on the third day** |
| `PODOBEN_NORMALIZED` | `C16:p154` | `POD.T7.IZHE_MENE_RADI` | `TIER_0_EXACT` | *И҆́же менѐ ра́ди* | Model: He Who for my sake | **He Who for my sake** |
| `PODOBEN_NORMALIZED` | `C16:p155` | `POD.T7.OGNYA_SVETLEE` | `TIER_2_ORTHOGRAPHIC_PHONOLOGICAL` | *Огнѧ свѣтлѣе* | Model: Brighter than fire | **Brighter than fire** |
| `PODOBEN_NORMALIZED` | `C18:p172` | `POD.T7.DNES_BDIT_IUDA` | `TIER_3_LEXICAL_RECENSIONAL` | *Дне́сь бди́тъ І҆ꙋ́да* | Model melody: Today Judas watches | **Today Judas watches** |
| `PODOBEN_NORMALIZED` | `C18:p173` | `POD.T7.NE_KTOMU_VOZBRANENI` | `SCRIBAL_INCIPIT_TRUNCATION` | *Не ктомꙋ̀ возбранѧ́еми* | Model melody: No longer forbidden | **No longer are we forbidden** |
| `PODOBEN_NORMALIZED` | `C18:p178` | `POD.T8.POVELENNOE_TAINSTVENNO` | `SCRIBAL_INCIPIT_TRUNCATION` | *Повеле́нное* | Model melody: That which was commanded secretly | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C18:p180` | `POD.T8.POVELENNOE_TAINSTVENNO` | `TIER_3_LEXICAL_RECENSIONAL` | *Повеле́нное та́инство* | Model melody: That which was commanded secretly | **That which was commanded mystically** |
| `PODOBEN_NORMALIZED` | `C20:p196` | `POD.T8.GOSPODI_ASHCHE_I_NA_SUDISHCHI` | `SCRIBAL_INCIPIT_TRUNCATION` | *Гдⷭ҇и а҆́ще на сꙋди́щи* | Model melody: O Lord, though before the judgment seat | **O Lord, though Thou didst stand before the tribunal** |
| `PODOBEN_NORMALIZED` | `C21:p208` | `POD.EXAP.ZHENY_USLYSHITE` | `TIER_0_EXACT` | *Же́ны оу҆слы́шите* | Podoben: Give ear, ye women | **Give ear, ye women** |
| `PODOBEN_NORMALIZED` | `C22:p211` | `POD.T2.EGDA_OT_DREVA` | `TIER_3_LEXICAL_RECENSIONAL` | *Е҆гда̀ ѿ дре́ва тя̀* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C22:p213` | `POD.T2.MILOSERDIA_SUSHCHI` | `TIER_0_EXACT` | *Милосе́рдія сꙋ́щи и҆сто́чникъ* | Podoben: Being tenderly compassionate | **Being the wellspring of loving-kindness** |
| `PODOBEN_NORMALIZED` | `C23:p226` | `POD.T3.VELIA_MUCHENIK_TVOIKH` | `TIER_0_EXACT` | *Ве́лія мꙋ́ченикъ твои́хъ* | Podoben: The great martyrs | **Great is the power of Thy martyrs** |
| `PODOBEN_NORMALIZED` | `C24:p240` | `POD.T4.YAKO_DOBLYA` | `TIER_0_EXACT` | *Я҆́кѡ до́бля* | Model: As one noble | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C26:p253` | `POD.T5.PREPODOBNE_OTCHE` | `TIER_0_EXACT` | *Преподо́бне ѻ҆́тче* | Model: O venerable father | **O venerable father** |
| `PODOBEN_SAME_NORMALIZED` | `C26:p254` | `POD.T5.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Most Holy Theotokos, same Tone and Model melody:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C26:p255` | `POD.T5.RADUISYA_ZHIVONOSNYI_KRESTE` | `TIER_0_EXACT` | *Ра́дꙋйся живоно́сный Крⷭ҇те* | Model: Rejoice, life-bearing | **Rejoice, O life-bearing Cross** |
| `PODOBEN_NORMALIZED` | `C26:p258` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Model: Co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C27:p267` | `POD.T6.VSE_OTLOZHSHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Все ᲂу҆пова́нїе* | Model melody: Having placed all their hope | **Having laid aside all earthly hope** |
| `PODOBEN_SAME_NORMALIZED` | `C27:p268` | `POD.T6.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera, same Tone and model melody:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C28:p279` | `POD.T6.VSE_OTLOZHSHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Всѐ ᲂу҆пова́нїе* | model melody: Having placed all their hope | **Having laid aside all earthly hope** |