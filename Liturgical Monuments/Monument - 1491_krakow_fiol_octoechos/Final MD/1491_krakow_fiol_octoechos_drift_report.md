# Scholarly Drift & Seam-Stitching Audit Report: 1491 Krakow Octoechos of Schweipolt Fiol

- **Monument ID**: `1491_krakow_fiol_octoechos`
- **Total 2-Up Mid-Sentence Seams Stitched**: 0 boundaries (`0` sub-clause seam overlaps deduplicated)
- **Inline Locus Milestones Inserted**: `[f. XvA]`, `[f. XrA]` across all 345 leaves
- **Total Primitive Normalization & Drift Events**: 60 (`32` Podobens/Pokoin, `15` Psalm Stichoi, `13` Weekday Heirmoi, `0` Seam Deduplications)
- **True Pre-Normalization AI Translation Drift Unified**: 45 occurrences
- **Source-Text (1491 Slavonic) Scribal Truncations & Tier 3 Variations Classified**: 4 events

---

## 1. Summary of 3-Tier Source & Scribal Drift Engine

1. **Tier 1 (Typographic / Titlo Equivalence)**: Strips accents, titla, and sacred abbreviations (`бг҃` -> `богъ`). Unified silently to canonical English.
2. **Tier 2 (Orthographic / Phonological Variant)**: Harmonizes Ruthenian/Church Slavonic vowel and yer reflexes (`ѡ`/`о`, `ѣ`/`е`, `ꙋ`/`у`, `ᲂу`/`у`). Unified to canonical English while logging orthographic drift.
3. **Scribal Incipit Truncation (`SCRIBAL_INCIPIT_TRUNCATION`)**: The printer/scribe abbreviated the model incipit on the physical leaf (e.g. `По̀, Дв҃аа` for `Дѣ́ва дне́сь`, or omitted `Подо́бенъ` before the incipit). Classified as a scribal convention, never counted as AI translation error.
4. **Tier 3 (Lexical / Syntactic / Recensional Variant)**: Genuine source variations in the 1491 print. **Preserved as distinct English translations** and annotated.

---

## 2. Complete Podoben & Rubric Drift Log

| Type | Locus | ID | Drift Tier | 1491 Slavonic Witness | Pre-Normalization Cohort Text | Canonical Normalized Reading |
| :--- | :---: | :--- | :---: | :--- | :--- | :--- |
| `PODOBEN_NORMALIZED` | `C04:p32` | `POD.T1.VSEKHVALNII_MUCHENITSY` | `TIER_3_LEXICAL_RECENSIONAL` | *прехвалнїи ц̃ї* | Podoben: O all-praised martyrs | **O all-lauded martyrs** |
| `PODOBEN_NORMALIZED` | `C04:p38` | `POD.T2.VYSHNIKH_ISHCHA` | `TIER_3_LEXICAL_RECENSIONAL` | *Въ вышнихъ ища :~* | Podoben: Seeking the highest | **Seeking the highest** |
| `PODOBEN_NORMALIZED` | `C06:p58` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the Tree | **When from the Tree** |
| `PODOBEN_NORMALIZED` | `C07:p63` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: Awed by the beauty of thy virginity" (Красотѣ дѣвства твоего):* Undivided and consubstantial Trinity, have mercy on them that bow down before Thee and hymn Thee piously, and who cry unceasingly; graciously gather by Thy mercy into the church of Thy possession | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C07:p69` | `POD.T3.KRASOTE_DEVSTVA` | `TIER_0_EXACT` | *Красотѣ̀ дѣ́вства твоегѡ̀* | Podoben: Awed by the beauty of thy virginity" (Красотѣ дѣвства твоего):* Awed by the beauty of thy virginity and by thy most radiant purity, Gabriel marvelled and cried unto thee, O Birthgiver of God: "What worthy praise can I offer unto thee? And what shall I call thee? I am in doubt and astonished! Therefore, as I was commanded, I cry unto thee: Rejoice, full of grace, the Lord is with thee! | **Beholding the beauty of thy virginity** |
| `PODOBEN_NORMALIZED` | `C10:p91` | `POD.T4.SKORO_PREDVARI` | `TIER_0_EXACT` | *Ско́рѡ предварѝ* | Podoben: Speedily anticipate | **Speedily anticipate** |
| `PODOBEN_NORMALIZED` | `C10:p93` | `POD.T4.VOZNESYISYA_NA_KREST` | `TIER_0_EXACT` | *Вознесы́йся на Крⷭ҇тъ во́лею* | Podoben: Thou Who wast lifted up | **Thou Who wast lifted up upon the Cross** |
| `PODOBEN_NORMALIZED` | `C12:p118` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Podoben: Co-unoriginate" (Собезначальное):* Let us fall down in faith, crying from the heart: Have mercy on us, Thine unworthy servants, O most good Trinity: Father, Son, and Holy Spirit! Have compassion, O Merciful One, upon Thine own flock which Thou hast acquired, that it may unceasingly glorify Thy goodness! | **The Word co-unoriginate** |
| `PODOBEN_NORMALIZED` | `C12:p119` | `POD.T5.SLOVO_SOBEZNACHALNOE` | `TIER_0_EXACT` | *Собезнача́льное Сло́во* | Podoben: Co-unoriginate | **The Word co-unoriginate** |
| `PODOBEN_SAME_NORMALIZED` | `C14:p137` | `POD.T5.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Bodiless Powers, the same prosomoion:* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C15:p143` | `POD.T6.ANGELSKIYA_SILY` | `TIER_0_EXACT` | *А҆́гг҃льскія си́лы* | Podoben: The Angelic Hosts" (Ангельскыя силы):* As God look down from heaven and behold our lowliness, as Thou art compassionate, and have mercy, O Lover of mankind, most good One, and as from rain grant us hope to receive forgiveness of our evil transgressions; therefore be Thou our Savior [and be with us], and none shall be against us! | **The Angelic Powers** |
| `PODOBEN_NORMALIZED` | `C15:p145` | `POD.T6.EZHE_O_NAS` | `TIER_0_EXACT` | *Е҆́же ѡ҆ на́съ* | Podoben: Having Fulfilled the Dispensation" (Иже о нас съвръшив):* O Father, with the Son [and] with the Holy Spirit: look upon us who cry unto Thee with faith, glorifying Thy dominion, O greatly Merciful, with fiery tongues; knowing no other nature beside Thee, have mercy upon those who glorify Thee: if Thou art with us, none shall be against us! | **Fulfilling the dispensation for our sake** |
| `PODOBEN_NORMALIZED` | `C17:p162` | `POD.T6.VSE_OTLOZHSHE` | `TIER_0_EXACT` | *Всѐ ѿло́жше* | Podoben: Having laid aside all earthly hope | **Having laid aside all earthly hope** |
| `PODOBEN_SAME_NORMALIZED` | `C17:p162` | `POD.T6.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera of the Bodiless Powers, Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_SAME_NORMALIZED` | `C19:p187` | `POD.T7.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera of the Bodiless Powers, Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_SAME_NORMALIZED` | `C22:p214` | `POD.T8.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Angels, Tone 8, Podoben: The same:* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C23:p228` | `POD.T2.EGDA_OT_DREVA` | `TIER_0_EXACT` | *Е҆гда̀ ѿ дре́ва* | Podoben: When from the tree | **When from the Tree** |
| `PODOBEN_SAME_NORMALIZED` | `C23:p229` | `POD.T2.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Forerunner, Tone 2, Podoben: The same:* | **The same (то́йже)** |
| `PODOBEN_NORMALIZED` | `C24:p235` | `POD.T3.DEVA_DNESS` | `TIER_0_EXACT` | *Дѣ́ва дне́сь* | Melodic Model: Today the Virgin" (Дѣва днесь):* Today the barren woman gives birth to the Forerunner of Christ, and he is the fulfillment of all prophecy; for Whom | **Today the Virgin** |
| `PODOBEN_NORMALIZED` | `C24:p239` | `POD.EXAP.ZHENY_USLYSHITE` | `TIER_0_EXACT` | *Же́ны оу҆слы́шите* | Podoben: Hear, Ye Women" (Женъ оуслыши):* O most glorious prophet and Forerunner of grace, who didst preach repentance of salvation unto all, and didst point out the Lamb Who takes away the transgressions of the world, O blessed one: pray Him now to have mercy upon the world! | **Give ear, ye women** |
| `PODOBEN_NORMALIZED` | `C25:p243` | `POD.T3.VELIA_KRESTA_TVOEGO` | `TIER_0_EXACT` | *Ве́лія Крⷭ҇та̀ твоегѡ̀ Гдⷭ҇и* | Podoben: Great Is the Power of Thy Cross | **Great is the power of Thy Cross, O Lord** |
| `PODOBEN_NORMALIZED` | `C26:p258` | `POD.T4.ZVANNYI_SVYSHE` | `TIER_0_EXACT` | *Зва́нный свы́ше* | Podoben: Called from on High | **Being called from on high** |
| `PODOBEN_NORMALIZED` | `C26:p259` | `POD.T4.ZVANNYI_SVYSHE` | `TIER_0_EXACT` | *Зва́нный свы́ше* | Podoben: Called from on High | **Being called from on high** |
| `PODOBEN_NORMALIZED` | `C28:p273` | `POD.T6.VSE_OTLOZHSHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Все оупованіе·* | Podoben: Having placed all their hope | **Having laid aside all earthly hope** |
| `PODOBEN_NORMALIZED` | `C28:p273` | `POD.T6.VSE_OTLOZHSHE` | `TIER_3_LEXICAL_RECENSIONAL` | *Все оупованіе·* | Podoben: Having placed all their hope" (Все упование):* Rejoice, O life-bearing Cross, invincible victory of piety, gate of Paradise, confirmation of the faithful, rampart of the Church, | **Having laid aside all earthly hope** |
| `PODOBEN_SAME_NORMALIZED` | `C28:p274` | `POD.T6.SAME` | `TIER_0_EXACT` | *то́йже* | *Other Stichera to the Theotokos, Tone and Podoben the same:* | **The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)** |
| `PODOBEN_NORMALIZED` | `C29:p283` | `POD.T4.VOZNESYISYA_NA_KREST` | `TIER_0_EXACT` | *Вознесы́йся на Крⷭ҇тъ во́лею* | Podoben: Thou Who wast lifted up upon the Cross" (Вознесыйся на Крестъ):* Thou Who wast lifted up upon the Cross of Thine own will, grant Thy compassions unto Thy new community that is named after Thee, O Christ God; make glad our faithful rulers by Thy power, granting them victories over their adversaries, having Thine alliance, a weapon of peace, an invincible trophy! | **Thou Who wast lifted up upon the Cross** |
| `PODOBEN_NORMALIZED` | `C29:p287` | `POD.EXAP.ZHENY_USLYSHITE` | `TIER_0_EXACT` | *Же́ны оу҆слы́шите* | Podoben: Give ear, ye women" (Жены услышите):* Rejoice, O most holy Cross, unconquerable wall of the world, refuge of the afflicted, and guardian of sacred men, defense of soldiers, conquering barbarians, crown of the Apostles, and salvation of the faithful! | **Give ear, ye women** |
| `PODOBEN_NORMALIZED` | `C29:p289` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Podoben: O most marvelous wonder | **O most marvelous wonder** |
| `PODOBEN_NORMALIZED` | `C29:p289` | `POD.T8.O_PRESLAVNAGO_CHUDESE` | `TIER_0_EXACT` | *Ѡ пресла́внагѡ чꙋдесѐ* | Podoben: O most marvelous wonder" (О преславное чудо):* Shining with spiritual rays, ye choirs, proclaim the noetic Sun rising from the overshadowed mountain, from the all-pure Virgin; and now receiving the fulfillment thereof with joy, through your all-pure prayers beseech Him to deliver all from condemnation and cruel torment on the fearful Day, by your supplications! | **O most marvelous wonder** |
| `PODOBEN_NORMALIZED` | `C29:p290` | `POD.T8.MUCHENITSY_GOSPODNI` | `TIER_0_EXACT` | *Мч҃ницы Гдⷭ҇ни* | Podoben: Martyrs of the Lord" (Мученицы Господни):* Martyrs of the Lord, every place ye sanctify | **Martyrs of the Lord** |
| `PODOBEN_NORMALIZED` | `C31:p301` | `POD.EXAP.ZHENY_USLYSHITE` | `TIER_0_EXACT` | *Же́ны оу҆слы́шите* | Podoben: Give ear, ye women | **Give ear, ye women** |