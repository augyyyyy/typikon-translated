# Scholarly Drift & Seam-Stitching Audit Report: 1629 Kyiv Octoechos

- **Monument ID**: `1629_kyiv_octoechos`
- **Total 2-Up Mid-Sentence Seams Stitched**: 0 boundaries
- **Inline Locus Milestones Inserted**: `[f. XvA]`, `[f. XvB]` across all 267 leaves
- **Total Primitive Normalization & Drift Events**: 64 (`27` Podobens, `5` Psalm Stichoi, `32` Weekday Heirmoi)
- **Pre-Normalization AI Translation Drift Unified**: 57 occurrences
- **Source-Text (1630 Slavonic) Tier 3 Variations Preserved**: 0 events

---

## 1. Summary of 3-Tier Source Drift Engine

1. **Tier 1 (Typographic / Titlo Equivalence)**: Strips accents, titla, and sacred abbreviations (`бг҃` -> `богъ`). Unified silently to canonical English.
2. **Tier 2 (Orthographic / Phonological Variant)**: Harmonizes Ruthenian/Church Slavonic vowel and yer reflexes (`ѡ`/`о`, `ѣ`/`е`, `ꙋ`/`у`). Unified to canonical English while logging orthographic drift.
3. **Tier 3 (Lexical / Syntactic / Recensional Variant)**: Genuine source variations in the 1630 print. **Preserved as distinct English translations** and annotated.

---

## 2. Complete Podoben & Rubric Drift Log

| Type | Locus | ID | 1630 Slavonic Witness | Pre-Normalization Cohort Text | Canonical Normalized Reading |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `PODOBEN_NORMALIZED` | `C01:p7` | `POD.T1.GROB_TVOI_SPASE` | *Гро́бъ тво́й* | Podoben: Thy Tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_NORMALIZED` | `C01:p9` | `POD.T1.GROB_TVOI_SPASE` | *Гро́бъ тво́й* | Podoben: Thy Tomb | **While the soldiers were guarding Thy tomb** |
| `PODOBEN_SAME_NORMALIZED` | `C03:p27` | `POD.T1.SAME` | *то́йже* | *Other Stichera, to the Bodiless Hosts. Podoben: the same.* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C05:p50` | `POD.T2.EGDA_OT_DREVA` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C05:p50` | `POD.T2.SAME` | *то́йже* | *Podoben: The same.* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C06:p56` | `POD.T3.KRASOTE_DEVSTVA` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: Awed by the beauty of thy virginity | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C06:p58` | `POD.T3.DEVA_DNESS` | *Дѣ́ва дне́сь* | Podoben: Today the Virgin | **Today the Virgin** |
| `PODOBEN_NORMALIZED` | `C08:p73` | `POD.T3.VELIA_KRESTA_TVOEGO` | *Ве́лія Крⷭ҇та̀ твоегѡ̀ Гдⷭ҇и* | Model: Great is the power of Thy Cross, O Lord | **Great is the power of Thy Cross, O Lord** |
| `PODOBEN_NORMALIZED` | `C08:p79` | `POD.T4.SKORO_PREDVARI` | *Ско́рѡ предварѝ* | Model: Speedily anticipate | **Speedily anticipate** |
| `PODOBEN_NORMALIZED` | `C09:p81` | `POD.T4.VOZNESYISYA_NA_KREST` | *Вознесы́йся на Крⷭ҇тъ во́лею* | Model: Thou Who wast lifted up upon the Cross | **Thou Who wast lifted up upon the Cross** |
| `PODOBEN_NORMALIZED` | `C10:p98` | `POD.T4.DALS_ESI_ZNAMENIE` | *Да́лъ є҆сѝ зна́менїе* | Model: Thou hast given a sign | **Thou hast given a sign** |
| `PODOBEN_NORMALIZED` | `C10:p98` | `POD.T4.YAKO_DOBLYA` | *Я҆́кѡ до́бля* | Model: As one noble | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C11:p104` | `POD.T5.SLOVO_SOBEZNACHALNOE` | *Собезнача́льное Сло́во* | Model: Co-unoriginate Word | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C11:p106` | `POD.T5.SLOVO_SOBEZNACHALNOE` | *Собезнача́льное Сло́во* | Model: Co-unoriginate Word | **The Word co-unoriginate** |
| `PODOBEN_SAME_NORMALIZED` | `C13:p123` | `POD.T5.SAME` | *то́йже* | *Other Stichera to the Bodiless Powers. Podoben: The same:* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C14:p131` | `POD.T6.EZHE_O_NAS` | *Е҆́же ѡ҆ на́съ* | Model: Fulfilling the dispensation for us | **Fulfilling the dispensation for our sake** |
| `PODOBEN_NORMALIZED` | `C15:p148` | `POD.T6.ANGELSKIYA_SILY` | *А҆́гг҃льскія си́лы* | Model: The angelic hosts go before | **The Angelic Powers** |
| `PODOBEN_NORMALIZED` | `C15:p149` | `POD.T6.TRIDNEVEN_VOSKRESL_ESI` | *Тридне́вно воскре́слъ е҆сѝ* | Model: Risen on the third day | **Having risen on the third day** |
| `PODOBEN_NORMALIZED` | `C16:p154` | `POD.T7.IZHE_MENE_RADI` | *И҆́же менѐ ра́ди* | Model: He Who for my sake | **He Who for my sake** |
| `PODOBEN_NORMALIZED` | `C16:p155` | `POD.T7.OGNYA_SVETLEE` | *О҆гня̀ свѣтлѣ́е* | Model: Brighter than fire | **Brighter than fire** |
| `PODOBEN_NORMALIZED` | `C22:p211` | `POD.T2.EGDA_OT_DREVA` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C24:p240` | `POD.T4.YAKO_DOBLYA` | *Я҆́кѡ до́бля* | Model: As one noble | **As one valiant among martyrs** |
| `PODOBEN_NORMALIZED` | `C26:p253` | `POD.T5.PREPODOBNE_OTCHE` | *Преподо́бне ѻ҆́тче* | Model: O venerable father | **O venerable father** |
| `PODOBEN_SAME_NORMALIZED` | `C26:p254` | `POD.T5.SAME` | *то́йже* | *Other Stichera to the Most Holy Theotokos, same Tone and Model melody:* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C26:p255` | `POD.T5.RADUISYA_ZHIVONOSNYI_KRESTE` | *Ра́дꙋйся живоно́сный Крⷭ҇те* | Model: Rejoice, life-bearing | **Rejoice, O life-bearing Cross** |
| `PODOBEN_NORMALIZED` | `C26:p258` | `POD.T5.SLOVO_SOBEZNACHALNOE` | *Собезнача́льное Сло́во* | Model: Co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_SAME_NORMALIZED` | `C27:p268` | `POD.T6.SAME` | *то́йже* | *Other Stichera, same Tone and model melody:* | **The same (то́йже)** |