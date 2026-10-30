# Post-Run Engine Retrospective: 1491 Krakow Octoechos of Schweipolt Fiol (`1491_krakow_fiol_octoechos`)

**Monument ID**: `1491_krakow_fiol_octoechos`  
**Title**: *1491 Krakow Octoechos of Schweipolt Fiol (Осмогласник / Октоїх Швайпольта Фіоля, Краків, 1491)*  
**Codex Class**: Slavic Cyrillic Incunabulum (Protomonument of East Slavic Typography; Wrocław / Breslau Stadtbibliothek Exemplar, Inv. No. 10423-47)  
**Total Physical Leaves**: 345 leaves (172 printed folios + archival target slips + 1866 Breslau collation certificate)  
**Cohorts Executed**: 35 cohorts (Cohorts 1–34 @ 10 leaves; Cohort 35 @ 5 leaves)  
**Total Word Conservation**: 76,884 Slavonic source words $\rightarrow$ 95,554 raw draft words $\rightarrow$ 122,923 complete edition words (ratio `1.286`)  
**Total Critical Apparatus**: 383 bijective footnotes (`[^1]`–`[^383]`)  
**Subagent Retries / Quarantines**: `0` subagent retries, `0` quarantined leaves  

---

## 1. Cohort Velocity & Bottleneck Autopsy

### 1.1 Aggregate Velocity Telemetry
Across the 35 cohorts executed during the Phase 1 `Flash` sprint (`2026-10-29T07:59:03` to `2026-10-29T15:00:05`, total wall-clock elapsed time `7.01 hours`):
- **Mean Subagent Execution Time**: `638.5s` (`10.64 min` per 10-leaf cohort, or `63.9s` per physical 300-DPI leaf).
- **Median Subagent Execution Time**: `625.9s` (`10.43 min`).
- **Fastest 10-Leaf Cohort**: **Cohort 27** (`p261..p270`, Thursday Matins Canons to the Holy Apostles and St. Nicholas in Tone 4) — `407.6s` (`6.79 min`), `2,886` English words, `10` footnotes.
- **Fastest Overall Cohort**: **Cohort 35** (`p341..p345`, 5 leaves: 4 microfilming target slips + 1866 German collation certificate) — `253.7s` (`4.23 min`), `364` English words, `5` footnotes.

### 1.2 Complete 35-Cohort Velocity, Word & Apparatus Ledger

| Cohort | Physical Leaves | Liturgical Scope | Subagent Duration (s / min) | End-to-End Cycle (s / min) | Slavonic Words | English Draft Words | Draft/Source Char Ratio | Footnotes (`[^N]`) |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **C01** | `p1..p10` | Woodcut Crucifixion, Title Incipit, Tone 1 Vespers & Midnight Office | `540.6s` (`9.01m`) | `552.6s` (`9.21m`) | 1,489 | 2,207 | 1.35 | 8 (`[^1]`–`[^8]`) |
| **C02** | `p11..p20` | Tone 1 Midnight Office Dismissal, Royal Litany, Matins Canons Odes 1–5 | `624.0s` (`10.40m`) | `636.0s` (`10.60m`) | 2,334 | 3,401 | 1.59 | 7 (`[^9]`–`[^15]`) |
| **C03** | `p21..p30` | Tone 1 Matins Canons Odes 6–9, Katavasia Crux (`p24`), Praises, Beatitudes | `867.7s` (`14.46m`) | `879.7s` (`14.66m`) | 2,260 | 3,101 | 1.48 | 15 (`[^16]`–`[^30]`) |
| **C04** | `p31..p40` | Tone 1 Liturgy Propers; `# TONE 2` (`p34`) Vespers & Midnight Office | `825.7s` (`13.76m`) | `837.7s` (`13.96m`) | 2,171 | 2,670 | 1.29 | 16 (`[^31]`–`[^46]`) |
| **C05** | `p41..p50` | Tone 2 Sunday Matins Triple Canons Odes 1–7 | `835.0s` (`13.92m`) | `847.0s` (`14.12m`) | 2,217 | 2,801 | 1.34 | 13 (`[^47]`–`[^59]`) |
| **C06** | `p51..p60` | Tone 2 Matins Odes 8–9, Praises, Liturgy; `# TONE 3` (`p60`) | `591.3s` (`9.85m`) | `603.3s` (`10.05m`) | 2,131 | 2,891 | 1.39 | 10 (`[^60]`–`[^69]`) |
| **C07** | `p61..p70` | Tone 3 Vespers, Midnight Office, Matins Kathismata & Anabathmoi | `684.6s` (`11.41m`) | `696.6s` (`11.61m`) | 2,106 | 2,595 | 1.29 | 12 (`[^70]`–`[^81]`) |
| **C08** | `p71..p80` | Tone 3 Sunday Matins Triple Canons Odes 1–7 | `507.5s` (`8.46m`) | `519.5s` (`8.66m`) | 2,185 | 2,798 | 1.35 | 10 (`[^82]`–`[^91]`) |
| **C09** | `p81..p90` | Tone 3 Matins Odes 8–9, Praises, Beatitudes; `# TONE 4` (`p87`) | `640.4s` (`10.67m`) | `770.0s` (`12.83m`) | 2,395 | 2,775 | 1.28 | 10 (`[^92]`–`[^101]`) |
| **C10** | `p91..p100` | Tone 4 Vespers, Midnight Office, Matins Canons Odes 1–4 | `741.5s` (`12.36m`) | `820.2s` (`13.67m`) | 2,305 | 2,667 | 1.29 | 10 (`[^102]`–`[^111]`) |
| **C11** | `p101..p110` | Tone 4 Sunday Matins Triple Canons Odes 5–9, Praises | `815.4s` (`13.59m`) | `913.5s` (`15.22m`) | 2,326 | 2,793 | 1.31 | 10 (`[^112]`–`[^121]`) |
| **C12** | `p111..p120` | Tone 4 Beatitudes & Liturgy; `# TONE 5` (`p114`) Vespers & Midnight Office | `625.9s` (`10.43m`) | `783.8s` (`13.06m`) | 2,300 | 2,614 | 1.27 | 10 (`[^122]`–`[^131]`) |
| **C13** | `p121..p130` | Tone 5 Sunday Matins Triple Canons Odes 1–7 | `790.4s` (`13.17m`) | `860.4s` (`14.34m`) | 2,298 | 3,022 | 1.47 | 10 (`[^132]`–`[^141]`) |
| **C14** | `p131..p140` | Tone 5 Matins Odes 8–9, Praises, Beatitudes; `# TONE 6` (`p139`) | `655.6s` (`10.93m`) | `800.1s` (`13.34m`) | 2,203 | 2,841 | 1.35 | 10 (`[^142]`–`[^151]`) |
| **C15** | `p141..p150` | Tone 6 Vespers, Midnight Office, Matins Canons Odes 1–4 | `594.9s` (`9.91m`) | `729.0s` (`12.15m`) | 2,007 | 2,802 | 1.40 | 9 (`[^152]`–`[^160]`) |
| **C16** | `p151..p160` | Tone 6 Sunday Matins Triple Canons Odes 5–9, Praises | `608.6s` (`10.14m`) | `694.1s` (`11.57m`) | 2,075 | 3,150 | 1.49 | 12 (`[^161]`–`[^172]`) |
| **C17** | `p161..p170` | Tone 6 Beatitudes & Liturgy; `# TONE 7` (`p164`) Vespers & Midnight Office | `577.6s` (`9.63m`) | `728.1s` (`12.13m`) | 2,430 | 2,732 | 1.27 | 13 (`[^173]`–`[^185]`) |
| **C18** | `p171..p180` | Tone 7 Sunday Matins Kathismata, Anabathmoi, Canons Odes 1–6 | `446.8s` (`7.45m`) | `577.9s` (`9.63m`) | 2,375 | 2,874 | 1.35 | 12 (`[^186]`–`[^197]`) |
| **C19** | `p181..p190` | Tone 7 Matins Odes 7–9, Praises, Beatitudes; `# TONE 8` (`p189`) | `557.0s` (`9.28m`) | `611.9s` (`10.20m`) | 2,345 | 2,825 | 1.33 | 14 (`[^198]`–`[^211]`) |
| **C20** | `p191..p200` | Tone 8 Vespers, Midnight Office (`p185`/`p193` cruxes), Matins Odes 1–4 | `689.1s` (`11.49m`) | `872.0s` (`14.53m`) | 2,310 | 2,614 | 1.21 | 17 (`[^212]`–`[^228]`) |
| **C21** | `p201..p210` | Missing Folio `p201` Target, Tone 8 Matins Odes 5–9, Praises | `523.4s` (`8.72m`) | `567.0s` (`9.45m`) | 2,105 | 2,630 | 1.40 | 16 (`[^229]`–`[^244]`) |
| **C22** | `p211..p220` | Tone 8 Liturgy; Weekday Octoechos Opening: Monday Tone 1 Vespers & Matins | `757.8s` (`12.63m`) | `918.1s` (`15.30m`) | 2,516 | 2,943 | 1.31 | 13 (`[^245]`–`[^257]`) |
| **C23** | `p221..p230` | Monday Tone 1 Matins Odes 6–9 & Liturgy; Tuesday Tone 2 Vespers & Kathismata | `668.5s` (`11.14m`) | `842.5s` (`14.04m`) | 2,554 | 3,041 | 1.33 | 11 (`[^258]`–`[^268]`) |
| **C24** | `p231..p240` | Tuesday Tone 2 Matins Canons (Forerunner & Compunction) Odes 1–9, Beatitudes | `773.4s` (`12.89m`) | `871.7s` (`14.53m`) | 2,440 | 2,916 | 1.30 | 10 (`[^269]`–`[^278]`) |
| **C25** | `p241..p250` | Tuesday Liturgy; Wednesday Tone 3 Vespers & Matins Canons Odes 1–5 | `725.3s` (`12.09m`) | `866.5s` (`14.44m`) | 2,473 | 3,017 | 1.31 | 10 (`[^279]`–`[^288]`) |
| **C26** | `p251..p260` | Wednesday Tone 3 Matins Odes 6–9 & Liturgy; Thursday Tone 4 Vespers | `566.5s` (`9.44m`) | `635.5s` (`10.59m`) | 2,409 | 3,133 | 1.39 | 10 (`[^289]`–`[^298]`) |
| **C27** | `p261..p270` | Thursday Tone 4 Matins Canons (Apostles & St. Nicholas) Odes 1–9 | `407.6s` (`6.79m`) | `536.0s` (`8.93m`) | 1,831 | 2,886 | 1.34 | 10 (`[^299]`–`[^308]`) |
| **C28** | `p271..p280` | Thursday Liturgy; Friday Tone 6 Vespers & Matins Canons Odes 1–5 | `560.0s` (`9.33m`) | `744.0s` (`12.40m`) | 1,912 | 2,887 | 1.42 | 10 (`[^309]`–`[^318]`) |
| **C29** | `p281..p290` | Friday Tone 6 Matins Odes 5–9 & Liturgy; Saturday Tone 8 Vespers | `706.6s` (`11.78m`) | `912.8s` (`15.21m`) | 1,918 | 2,975 | 1.48 | 10 (`[^319]`–`[^328]`) |
| **C30** | `p291..p300` | Saturday Tone 8 Matins Canons (All Saints & Departed) Odes 1–9 | `678.2s` (`11.30m`) | `773.5s` (`12.89m`) | 2,279 | 2,829 | 1.40 | 10 (`[^329]`–`[^338]`) |
| **C31** | `p301..p310` | Saturday Liturgy; `# EXAPOSTILARIA AND EVANGELICAL STICHERA` (`p304`, Gospels 1–5) | `493.4s` (`8.22m`) | `616.9s` (`10.28m`) | 2,501 | 2,888 | 1.34 | 10 (`[^339]`–`[^348]`) |
| **C32** | `p311..p320` | Resurrection Matins Gospels 5–10, Exapostilaria & Eothina Stichera 5–10 | `475.2s` (`7.92m`) | `533.3s` (`8.89m`) | 2,647 | 2,991 | 1.33 | 10 (`[^349]`–`[^358]`) |
| **C33** | `p321..p330` | Gospel 11 & Eothinon 11; Lenten Triadica (Tones 1–8); Homily of St. Ephrem | `534.9s` (`8.91m`) | `649.6s` (`10.83m`) | 2,412 | 2,985 | 1.38 | 10 (`[^359]`–`[^368]`) |
| **C34** | `p331..p340` | Sirach & Chrysostom Homilies; Quire Table (`p337`); 1491 Woodcut Colophon (`p338`) | `658.6s` (`10.98m`) | `773.4s` (`12.89m`) | 1,934 | 2,276 | 1.21 | 10 (`[^369]`–`[^378]`) |
| **C35** | `p341..p345` | Missing Blank Folios (`Bl. 171–172`) Targets; 1866 Breslau Collation Certificate | `253.7s` (`4.23m`) | `253.7s` (`4.23m`) | 291 | 364 | 1.08 | 5 (`[^379]`–`[^383]`) |

### 1.3 Autopsy of the 3 Slowest Cohorts
1. **Cohort 3 (`p21..p30` — `867.7s` / `14.46 min` subagent execution; `3,101` words; `15` footnotes)**:
   - **Codicological & Visual Bottleneck**: Dense interleaving of 3 Sunday Matins canons in Tone 1 (Resurrection by John of Damascus, Cross-Resurrection by Cosmas, and Theotokos across Odes 6–9) printed in continuous 25-line incunabular blocks where ode transitions and troparion boundaries are marked only by small inline cinnabar initials.
   - **Epigraphic Crux**: Leaf `p24` contains a damaged/abbreviated composite rubric (`Бж̃твное сїе всѣ ко [?] · цꙋ иже в д̃нь и ли бци`) that required philological collation against the Byzantine Horologion/Octoechos and a detailed scholarly apparatus entry (`[^21]`), plus 14 additional footnotes (`[^16]`–`[^30]`).
2. **Cohort 5 (`p41..p50` — `835.0s` / `13.92 min` subagent execution; `2,801` words; `13` footnotes)**:
   - **Codicological & Visual Bottleneck**: Covers Odes 1 through 7 of the Tone 2 Sunday Matins triple canon. Fiol's woodblock/cast-type ligatures and superscripts (`їѡ`, `бц̃а`, `тр̃о`) are tightly packed without line breaks between stanzas, requiring the `Flash` worker to parse 28 distinct troparia/heirmoi per 2-leaf spread and verify self-checks before flushing.
3. **Cohort 4 (`p31..p40` — `825.7s` / `13.76 min` subagent execution; `2,670` words; `16` footnotes) & Cohort 22 (`p211..p220` — `918.1s` / `15.30 min` end-to-end cycle)**:
   - **Cohort 4 Bottleneck**: Major genre/section transition combining the Tone 1 Sunday Liturgy Scripture readings (Epistle & Gospel), the `# TONE 2` ornamental woodcut headpiece on leaf `p34`, Saturday Great Vespers, and the Sunday Midnight Office Triadikos Canon of Metrophanes of Smyrna, accompanied by `16` scholarly footnotes (2nd highest in the monument).
   - **Cohort 22 Bottleneck**: Highest Slavonic source density up to that point (`2,516` Slavonic words) spanning the transition from Sunday Tone 8 Liturgy into the consolidated Weekday Octoechos (Monday Vespers & Matins Canons of Repentance and Bodiless Powers in Tone 1).

---

## 2. Small Pause Gate, Deterministic Self-Healing & Flash Failure Modes

### 2.1 Complete Catalog of Anomalies Caught & Healed

| ID | Pipeline Stage | Gate / Component | Affected Cohorts / Leaves | Empirical Description | Resolution Mechanism |
|:---:|:---|:---|:---:|:---|:---|
| **SH-01** | Phase 1 Sprint | `run_small_pause_gate.py` (Gate 2: Hieratic Pronouns) | Cohort 7 (`p66`, `p69`) | 2 lowercase Holy Trinity pronouns (`thy`/`him`) in Tone 3 Matins stanzas. | Healed automatically in `< 1s` by `attempt_deterministic_self_healing()` in `scripts/autonomous_orchestrator.py`; passed Gate 2 on immediate re-verification with `0` subagent retries. |
| **SH-02** | Phase 2 Compile | `UniversalPublicationEngine` Step 3 | Cohorts 2, 3, 7, 11, 16, 20, 31 | Minor MTS-1 vocabulary/slop/`-eth` drift inside raw cohort drafts and footnote text (`[Self-Healer] Synchronized MTS-1 vocabulary/slop/-eth healing across 7 cohort files on disk`). | Healed automatically by `_self_heal_cohorts_and_footnotes()` in `scripts/compile_final_edition.py`. |
| **SH-03** | Phase 2 Verify | `verify_publication_edition.py` (Gate 5A: Unparenthesized Cyrillic) | Cohorts 12, 13, 14, 21, 34 (`98` hits across `complete.md` & `part*.md`) | `Flash` workers enclosed Slavonic Heirmos incipits in Tone 5 (`*Ode 3. Heirmos: Establish... [Утверди...]:*`) and Cyrillic quire numerals in the leaf `p337` collation table (`\| 1 [а҃] \|`) in square brackets `[...]` instead of parentheses `(...)`. Because Gate 5A strips `\([^\)]*[\u0400-\u04FF][^\)]*\)` before checking for residual Cyrillic, bracketed Cyrillic triggered 98 Gate 5A failures. | Healed via deterministic regex `\[([^\]\^]*[\u0400-\u04FF\uA640-\uA69F][^\]]*)\]` $\rightarrow$ `(\1)`, converting `[Утверди...]` to `(Утверди...)` while preserving `[^N]` footnote markers. |
| **SH-04** | Phase 2 Verify | `verify_publication_edition.py` (Gate 7A: Unnormalized `Model:`) | Cohort 26 (`p259`, `2` hits) | Rubric `*Other Stichera to the Saint (Nicholas), in the same Tone and Model:*` (rendering Fiol's `гла[съ] и по[добенъ] то[тже]`) matched Gate 7A's forbidden `\bModel:` regex. | Normalized to canonical 3-layer Podoben format: `*Other Stichera to the Saint (Nicholas), in the same Tone, Podoben: "Called from on High" (Званный свыше):*`. |
| **SH-05** | Phase 2 Verify | `verify_publication_edition.py` (Gate 7B: Missing Slavonic Witness on `Podoben:`) | Cohort 8 (`p72`) & Cohort 20 (`p185`) (`4` hits) | (1) Cohort 8 had `*Heirmos: The same (Podoben: "Every nature bends the knee"):*` without the Cyrillic string `(Всяко естество)`. (2) Cohort 20 (`p185`) had `*Kontakion, Tone 8, Podoben:*[^218]` because Fiol's physical leaf printed bare `т҃ъ гла и҃ · по[добенъ]` with no model incipit. | Restored parenthetical Slavonic witnesses `(Всяко естество)` in Cohort 8 and `(*подобенъ*)` in Cohort 20. |
| **SH-06** | Phase 1 Setup | `scripts/extract_cohort_leaves.py` | Cohort 1 (`Source Text/images`) | `Source Text/images` existed as a OneDrive cloud placeholder directory (`reparse tag 0x9000e01a`), causing `mklink /J` to skip junction creation without copying cached JPGs from Drive E. | Patched `scripts/extract_cohort_leaves.py` to explicitly copy `found_file` to `target_local_canon` whenever `target_local_canon` is missing on disk. |

### 2.2 New Deterministic Healers & Template Guardrails to Eliminate 100% of Source Mistakes
1. **Bracketed-Cyrillic Auto-Healer (`SH-03`)**: Add `re.sub(r'\[([^\]\^]*[\u0400-\u04FF\uA640-\uA69F][^\]]*)\]', r'(\1)', text)` directly to `attempt_deterministic_self_healing()` in `scripts/autonomous_orchestrator.py` and `_self_heal_cohorts_and_footnotes()` in `scripts/compile_final_edition.py`.
2. **Same-Tone-and-Model Resolver (`SH-04`)**: In `scripts/hymnographic_gold_normalizer.py`, when a rubric contains `in the same Tone and (?:Model|Podoben)` (`гласъ и подобенъ тотже`), resolve it automatically to the most recently active `Podoben: "<English Incipit>" (<Slavonic Witness>)` in that service or rewrite `and Model:` $\rightarrow$ `to the same melodic model (*подобенъ тотже*):`.
3. **Bare `Podoben:` Guardrail (`SH-05`)**: Update Statutory Mandate 9 in `data/templates/work_order_template.md` to instruct workers: *"When the physical leaf prints a bare `подобенъ` (`по[добенъ]`) without naming the model incipit, render as `*Tone N, Podoben (*подобенъ*):*` so the parenthetical Slavonic witness invariant is preserved."*

---

## 3. Argon Review Queue Signal Precision (`argon_review_queue.json`)

### 3.1 Audit of All 5 Queued Leaves Across Phase 1

| Leaf | Cohort | Triggering Signal in `run_small_pause_gate.py` | Ground-Truth Classification | Philological & Codicological Assessment |
|:---:|:---:|:---|:---:|:---|
| **`p14`** | Cohort 2 | `borderline_sgc02_ratio: 2.74 (draft=3746c, source=1365c)` | **False Positive** *(Liturgical Abbreviation Expansion)* | Leaf `p14` is the Sunday Midnight Office dismissal, Royal Litany, and Matins Six Psalms opening ordo. Fiol prints heavily abbreviated liturgical cues (`Пса̃ · Г̃и въ силѣ твоей... Тр̃е. И по Ѻ̃че нашъ...`). Standard English liturgical rendering of speaker tags (`**Deacon:**`, `**Priest:**`) and abbreviated incipits naturally produces a `2.74` character ratio with zero fabrication. |
| **`p24`** | Cohort 3 | `epigraphic_uncertainty_marker: [?]` | **True Positive** *(Genuine Epigraphic Crux)* | Genuine damaged/abbreviated typeset glyph in Fiol's Ode 6 Katavasia rubric (`Бж̃твное сїе всѣ ко [?] · цꙋ иже в д̃нь`). Properly restored and documented in `[^21]`. |
| **`p193`** | Cohort 20 | `epigraphic_uncertainty_marker: [?]` | **True Positive** *(Genuine Epigraphic Crux)* | Genuine ink smudge/damage on leaf `p193` (`да н[ынѣ [?]ти съ бл[аго]дарественовъ`). Properly restored and documented in apparatus. |
| **`p201`** | Cohort 21 | `epigraphic_uncertainty_marker: [lacuna]` | **True Positive** *(Genuine Physical Lacuna)* | Genuine missing folio in the surviving Wrocław Stadtbibliothek copy, replaced by the Russian archival microfilm target (`ЭТОГО ЛИСТА В КНИГЕ НЕТ`). Documented in `[^238]`. |
| **`p337`** | Cohort 34 | `complex_multicolumn_table: 20 table rows` | **False Positive for Content / True Utility for Gate 5A** | 5-column quire register (`То е́сть личба до то́й книгы...`) spanning 84 gatherings in 20 Markdown table rows. While `Flash` transcribed all 84 quire numbers accurately, Argon review caught the `[а҃]` square-bracketed Cyrillic numerals that triggered Gate 5A. |

### 3.2 Signal Precision & Threshold Calibration Recommendations
- **Overall Precision**: `3 / 5` (`60.0%` strict philological/epigraphic cruxes; `80.0%` actionable when including the `p337` table's `[а҃]` Gate 5A syntax catch).
- **Signal 1 (`epigraphic_uncertainty_marker`: `[?]`, `[lacuna]`)**: `3 / 3` (`100%` precision). Keep threshold unchanged.
- **Signal 2 (`borderline_sgc02_ratio` > `2.20`)**: `0 / 1` (`0%` precision). **Calibration**: In `scripts/run_small_pause_gate.py`, raise the upper `SGC-02` queue threshold from `2.20` to `2.85` whenever the Slavonic source leaf contains $\ge 4$ liturgical ordo abbreviations (`Тр̃е`, `Ѻ̃че нашъ`, `Г̃и помилуй`, `єктеніа`, `Пса̃`).
- **Signal 3 (`complex_multicolumn_table` $\ge 5$ rows)**: `1 / 1` structurally sound, but high value for verifying Cyrillic parenthesis rules in tables. Keep threshold at $\ge 5$ rows.

---

## 4. Monument-Type & Compiler Edge Cases (`compile_final_edition.py`)

1. **Consolidated Weekday Octoechos Slicing (`part8_tone-8.md` = 244.5 KB)**:
   - In the 1491 Krakow Octoechos, Tones 1–7 contain only the **Sunday** services (Saturday Great Vespers, Sunday Midnight Office, Sunday Matins, Sunday Liturgy Beatitudes/Propers), averaging `47 KB–83 KB` per Part (`25–30` leaves each).
   - However, after the Sunday Tone 8 cycle (`pp. 189–214`), Fiol prints the **Consolidated Weekday Octoechos** for the entire week (`pp. 214–303`: Monday Tone 1 for Bodiless Powers, Tuesday Tone 2 for the Forerunner, Wednesday Tone 3 for the Cross/Theotokos, Thursday Tone 4 for the Apostles/St. Nicholas, Friday Tone 6 for the Cross, Saturday Tone 8 for All Saints/Departed) using inline cinnabar rubrics rather than new woodcut headpieces.
   - Because `data/templates/publication_spec_scaffolds.json` (`octoechos` scaffold) only defines `# TONE 1`..`# TONE 8`, `# EXAPOSTILARIA AND EVANGELICAL STICHERA`, and `# GENERAL PARASTAS`, `Part 8` absorbed `115` physical leaves (`pp. 189–303`, `244,534` chars—32.6% of the entire codex).
2. **Rear Ascetic Homilies vs. `# GENERAL PARASTAS` Scaffold Landmark**:
   - The default `octoechos` scaffold anticipates `# GENERAL PARASTAS (OFFICE FOR THE DEPARTED)` as `part10`. In Fiol's 1491 edition, the Saturday Office for the Departed is integrated into the Weekday cycle (`pp. 289–303`), while the rear appendix (`pp. 327–338`, following the 11 Eothina Gospels/Stichera and Lenten Triadica) consists of three **Ascetic Homilies** (*Instruction of St. Ephrem the Syrian*, *Sirach on Childrearing*, *Discourse of St. John Chrysostom*), the 84-quire collation register (`p337`), and Fiol's 1491 Cracow woodcut colophon (`p338`).
3. **`extract_propers_corpus()` State-Tracking Desynchronization with Statutory Mandate 8**:
   - Inspecting `Final MD/1491_krakow_fiol_octoechos_propers_corpus.json` (`2,898` items) revealed a critical state-machine interaction:
     - `office`: `{"Front Matter": 2898}` (`100%` stuck on `'Front Matter'`).
     - `hymn_type`: `{"Sticheron": 2497, "Theotokion": 385, "Kontakion / Ikos": 11, "Stavrotheotokion": 5}` (Canon Troparia and Heirmoi defaulted to `'Sticheron'`).
     - `tone`: `{"8": 1238, "1": 273, "4": 236, "2": 234, "3": 229, "5": 228, "6": 227, "7": 220, "0": 13}` (all Weekday propers in Tones 1, 2, 3, 4, 6 were tagged as `tone=8`).
   - **Root Cause**: Statutory Mandate 8 forbids `### At Vespers` / `### At Matins` markdown headings in hymnographic drafts, requiring inline italicized rubrics (`*On Saturday evening, at "Lord, I have cried"...*`, `*Ode 1. Heirmos:*`). However, `extract_propers_corpus()` in `scripts/hymnographic_gold_normalizer.py` only updates `current_office` when encountering markdown `#`/`##`/`###` headings and only updates `current_tone` on `# TONE N` H1 headers.
4. **`_collect_cohort_files()` Cache Shadowing in `scripts/compile_final_edition.py`**:
   - On the first execution of `--compile-publication`, `UniversalPublicationEngine._archive_cohorts()` moves `Final MD/*cohort*.md` into `Cohorts/`. On any subsequent re-run of `--compile-publication`, `_collect_cohort_files()` reads exclusively from `Cohorts/` first (`lines 956–960`), ignoring newer edits in `Draft/` unless `Cohorts/` is also updated.

---

## 5. Granular Atomic Tagging Blueprint (Propers & Non-Propers)

 across all 35 `Cohorts/*.md` files (`2,614` non-banner paragraphs / `2,898` atomic stanzas), the following regex patterns achieve **100% deterministic classification** of every liturgical unit in `1491_krakow_fiol_octoechos` into `{monument_id}_atomic_corpus.json`:

### 5.1 Variable Propers Inventory (`2,031` Tagged Stanza Blocks + `228` Continuation Stanzas)

| Atomic Class ID | Liturgical Genre | Cohort Count | Canonical Markdown / Regex Pattern (`Cohorts/*.md`) |
|:---|:---|---:|:---|
| `PROPER_CANON_TROPARION` | Canon Troparia (Odes 1–9) | 889 | `^\*(?:Troparion(?:\s+\d+)?(?:,\s*Tone\s+\d+)?)\s*:\*\s+(.+)$` |
| `PROPER_THEOTOKION` | Theotokia & Dogmatika | 302 | `^\*(?:Tone\s+\d+\.\s*)?(?:Theotokion(?:\s+\(\s*Dogmatikon\s*\))?|Another\s+Theotokion)(?:,\s*Tone\s+\d+)?[^*]*?:\*\s*(.+)$` |
| `PROPER_HEIRMOS` | Canon Heirmoi (Odes 1–9) | 298 | `^\*(?:(?:The\s+)?Resurrectional\s+Canon|Another\s+Canon|Canon|Ode\s+\d+)[^*]*?Heirmos:\s*([^*]+?)\*(?:\s+(.+))?$` |
| `PROPER_STICHERON` | Vespers/Praises/Aposticha/Eothina Stichera | 292 | `^\*(?:Sticheron(?:\s+\d+)?|Other\s+Stichera|Tone\s+\d+,\s*Podoben:|Evangelical\s+Sticheron\s+\d+)[^*]*?:\*\s*(.*)$` |
| `PROPER_SESSIONAL_KATHISMA` | Kathisma Sessional Hymns | 52 | `^\*(?:After\s+the\s+\d+(?:st|nd|rd|th)\s+(?:Stichologia|Kathisma)[^*]*?|Sessional\s+Hymn[^*]*?|Another\s+Sessional\s+Hymn[^*]*?):\*\s*(.*)$` |
| `PROPER_KATAVASIA` | Ode Katavasiai | 32 | `^\*Katavasia:\s*([^*]+)\*$` |
| `PROPER_MARTYRIKON` | Hymns to the Martyrs | 32 | `^\*Martyri[ck]on(?:,\s*Tone\s+\d+)?:\*\s*(.+)$` |
| `PROPER_EXAPOSTILARION` | Exapostilaria & Photogogika | 29 | `^\*(?:Exapost[ei]larion(?:\s+\d+)?|Photogogi[ck](?:on)?)[^*]*?:\*\s*(.*)$` |
| `PROPER_ANABATHMOI_ANTIPHON` | Gradual Hymns (Songs of Ascent) | 24 | `^\*(?:Gradual\s+Hymns|Songs\s+of\s+Ascent|Antiphon\s+\d+)[^*]*?:\*\s*(.*)$` |
| `PROPER_STAVROTHEOTOKION` | Cross-Theotokia (Wed/Fri) | 18 | `^\*(?:Staurotheotokion|Stavrotheotokion|Cross-Theotokion)[^*]*?:\*\s*(.+)$` |
| `PROPER_BEATITUDES_TROPARION` | Liturgy Beatitudes Troparia | 16 | `^\*(?:On\s+the\s+Beatitudes|In\s+the\s+Beatitudes|Beatitudes)[^*]*?:\*\s*(.*)$` |
| `PROPER_KONTAKION` | Kontakia (Sunday & Weekday) | 15 | `^\*Kontakion[^*]*?:\*\s*(.*)$` |
| `PROPER_NEKROSIMON` | Hymns for the Departed (Sat) | 14 | `^\*(?:For\s+the\s+Departed|Troparion\s+for\s+the\s+Departed|Another,\s+for\s+the\s+departed)[^*]*?:\*\s*(.+)$` |
| `PROPER_TRIADIKON` | Trinitarian Hymns & Lenten Triadica | 12 | `^\*Triadi[ck]on[^*]*?:\*\s*(.+)$` |
| `PROPER_IKOS` | Ikosi | 8 | `^\*Ikos[^*]*?:\*\s*(.+)$` |
| `PROPER_HYPAKOE` | Sunday Matins Hypakoai | 8 | `^\*(?:Then\s+the\s+)?(?:Hypakoe|Ypako[eë])(?:,\s*Tone\s+\d+)?[^*]*?:\*\s*(.+)$` |

### 5.2 Fixed Non-Propers, Lectionary & Paratext Inventory (`457` Blocks)

| Atomic Class ID | Liturgical / Codicological Genre | Cohort Count | Canonical Markdown / Regex Pattern (`Cohorts/*.md`) |
|:---|:---|---:|:---|
| `NONPROPER_PROCEDURAL_RUBRIC` | Cinnabar Liturgical Ordo Rubrics | 154 | `^\*[^*\n]+\*$` *(excluding inline stanza headers above)* |
| `NONPROPER_DOXOLOGY_HEADER` | `Glory... Both now...` Doxological Tags | 121 | `^\*(?:Glory(?:\.\.\.|,\s*and\s+now|:)|Both\s+now\b)[^*]*?\*\s*(.*)$` |
| `NONPROPER_PATRISTIC_HOMILY_PARA` | Ascetic Homilies (Ephrem, Sirach, Chrysostom) | 48 | Contextual block under `^\*(?:Instruction\s+of\s+Saint\s+Ephrem|Discourse\s+of\s+Saint\s+John\s+Chrysostom|A\s+Discourse\s+on\s+How\s+Parents)[^*]*?:\*` (`pp. 327–336`) |
| `NONPROPER_PSALM_STICHOS_VERSE` | Psalm & Aposticha Verses (`Стихъ`) | 36 | `^\*Verse:\s*([^*]+)\*(?:\s*\[([^\]]+)\])?$` |
| `NONPROPER_PROKEIMENON_ALLELUIA` | Prokeimena, Alleluiaria & Kinonika | 35 | `^\*(?:Prokeimenon|Alleluia|Kinonikon|Communion\s+Hymn)[^*]*?:\*\s*(.*)$` |
| `NONPROPER_LECTIONARY_PERICOPE` | Weekday Epistles/Gospels & 11 Eothina Gospels | 33 | `^\*(?:The\s+Reading\s+is\s+from|Epistle|Gospel|(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh)\s+Matins\s+Resurrection\s+Gospel)[^*]*?:\*\s*(.*)$` |
| `NONPROPER_LITANY_DIALOGUE` | Litany Petitions & Sacerdotal Exclamations | 18 | `^(?:\*\*(?:Priest|Deacon|Reader|Choir|People):\*\*|\*(?:Then\s+the\s+priest|Priest|Deacon):\*)\s*(.+)$` |
| `NONPROPER_PARATEXT_COLLATION` | Woodcuts, Quire Table, Colophon, 1866 Attest | 12 | `^(?:\|.*\||\[(?:Woodcut|Photographic|Mounted|Sixteenth|Circular)[^\]]*\])` |

---

## 6. Top 5 Concrete Engine Hardening Recommendations

### Rank 1: Inline-Rubric State Machine for `office`, `tone`, and `hymn_type` in Propers Corpus Extractor
- **Target Script & Function**: `scripts/hymnographic_gold_normalizer.py` $\rightarrow$ `extract_propers_corpus()`
- **Empirical Evidence**: Because Statutory Mandate 8 bans `### At Vespers` / `### At Matins` headers in hymnographic drafts, `extract_propers_corpus()` left `office="Front Matter"` on `2,898 / 2,898` (`100%`) of items, defaulted `2,497 / 2,898` items to `hymn_type="Sticheron"`, and assigned `1,238 / 2,898` items (including Monday–Friday Weekday propers in Tones 1, 2, 3, 4, 6) to `tone=8`.
- **Actionable Fix**: Update `extract_propers_corpus()` to parse inline italicized rubrics (`^\*.*\*$`) for office transitions (`Vespers` / `Lord, I have cried` $\rightarrow$ `"Great Vespers"`; `Midnight Office` $\rightarrow$ `"Midnight Office"`; `Matins` / `God is the Lord` / `Ode \d+` / `Stichologia` $\rightarrow$ `"Matins"`; `Beatitudes` / `Prokeimenon` / `Epistle` $\rightarrow$ `"Liturgy"`), weekday tone switches (`Tone (\d+)` inside rubrics), and exact stanza role tags (`*Troparion:*` $\rightarrow$ `"Canon Troparion"`, `*Ode \d+.*Heirmos:*` $\rightarrow$ `"Heirmos"`, `*Sessional Hymn*` $\rightarrow$ `"Sessional Hymn"`).

### Rank 2: Deterministic Bracketed-Cyrillic-to-Parentheses Healer (`[Кириллица]` $\rightarrow$ `(Кириллица)`)
- **Target Script & Function**: `scripts/autonomous_orchestrator.py` $\rightarrow$ `attempt_deterministic_self_healing()` and `scripts/compile_final_edition.py` $\rightarrow$ `UniversalPublicationEngine._self_heal_cohorts_and_footnotes()`
- **Empirical Evidence**: `Flash` subagents in Cohorts 12, 13, 14, 21, and 34 wrapped Slavonic Heirmos incipits (`[Коня и всадника...]`) and table numerals (`[а҃]`) in square brackets instead of parentheses, triggering `98` Gate 5A violations in `verify_publication_edition.py`.
- **Actionable Fix**: Add the single deterministic regex pass `re.sub(r'\[([^\]\^]*[\u0400-\u04FF\uA640-\uA69F][^\]]*)\]', r'(\1)', text)` to both self-healers so any bracketed Cyrillic in body or table lines is converted to parentheses before Gate 5A runs, while leaving `[^N]` footnote markers untouched.

### Rank 3: Bare `Podoben` & `Same Tone and Model` Normalizer for Incunabular/Manuscript Rubrics
- **Target Script & Function**: `scripts/hymnographic_gold_normalizer.py` $\rightarrow$ `normalize_podoben_lines()` and `data/templates/work_order_template.md` (Statutory Mandate 9)
- **Empirical Evidence**: Gate 7A failed on `*in the same Tone and Model:*` (Cohort 26, leaf `p259`, translating Fiol's `гла[съ] и по[добенъ] то[тже]`) and Gate 7B failed on `*Kontakion, Tone 8, Podoben:*[^218]` (Cohort 20, leaf `p185`, where Fiol printed bare `по[добенъ]` without an incipit) and `*Heirmos: The same (Podoben: "Every nature bends the knee"):*` (Cohort 8, missing Cyrillic).
- **Actionable Fix**: Enhance `normalize_podoben_lines()` to: (a) replace `in the same Tone and Model:` with the active `Podoben` from the preceding rubric or `in the same Tone and melodic model (*подобенъ тотже*):`, (b) append `(*подобенъ*)` whenever a physical rubric prints bare `Podoben:` without an incipit, and (c) look up missing parenthetical Slavonic witnesses in `data/liturgical_primitives_registry.json` by English incipit.

### Rank 4: Weekday Octoechos & Rear Homiletic Appendix Landmarks in `publication_spec_scaffolds.json`
- **Target Script & Function**: `data/templates/publication_spec_scaffolds.json` (`octoechos` scaffold) & `scripts/compile_final_edition.py` $\rightarrow$ `_slice_into_parts()`
- **Empirical Evidence**: Because Fiol's 1491 Octoechos places the Consolidated Weekday Octoechos (`pp. 214–303`) immediately after Sunday Tone 8 and concludes with Ascetic Homilies + Quire Register + Colophon (`pp. 327–345`), `part8_tone-8.md` ballooned to `244,534` chars (`115` leaves) while `part10` (`# GENERAL PARASTAS`) went unused.
- **Actionable Fix**: Add optional landmarks `# WEEKDAY OCTOECHOS (MONDAY TO SATURDAY)` and `# ASCETIC HOMILIES AND COLOPHON` to the `octoechos` scaffold in `data/templates/publication_spec_scaffolds.json` (and list them in `work_order_template.md` Section 3 Step 3) so composite Sunday+Weekday Octoechos monuments slice cleanly into balanced modular Parts.

### Rank 5: Bi-Directional `Draft/` $\leftrightarrow$ `Cohorts/` Timestamp Sync & Liturgical Ordo `SGC-02` Threshold Calibration
- **Target Script & Function**: `scripts/compile_final_edition.py` $\rightarrow$ `UniversalPublicationEngine._collect_cohort_files()` & `scripts/run_small_pause_gate.py` $\rightarrow$ `collect_argon_review_signals()`
- **Empirical Evidence**: (1) Once `_archive_cohorts()` populates `Cohorts/` on a first compile run, `_collect_cohort_files()` ignores newer edits in `Draft/*_raw_draft.md` or `Final MD/*cohort*.md`. (2) Abbreviated Royal Office / Six Psalms rubrics on leaf `p14` triggered a false-positive `SGC-02` Argon review signal (`ratio=2.74`).
- **Actionable Fix**: (1) In `_collect_cohort_files()`, compare `st_mtime` between `Draft/*cohort{N}_raw_draft.md`, `Final MD/*cohort{N}.md`, and `Cohorts/*cohort{N}.md` and always ingest the newest file. (2) In `collect_argon_review_signals()`, raise the upper `SGC-02` threshold from `2.20` to `2.85` on leaves containing $\ge 4$ abbreviated Slavonic ordo cues (`Тр̃е`, `Ѻ̃че нашъ`, `Г̃и помилуй`, `Пса̃`).
