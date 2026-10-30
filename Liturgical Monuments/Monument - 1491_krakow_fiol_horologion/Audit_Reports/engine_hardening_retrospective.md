# Post-Run Engine Hardening Retrospective: 1491 Krakow Horologion of Schweipolt Fiol (`1491_krakow_fiol_horologion`)

- **Monument ID**: `1491_krakow_fiol_horologion`
- **Title**: *1491 Krakow Horologion of Schweipolt Fiol (Часослов Швайпольта Фіоля, Краків, 1491)*
- **Physical Scale**: 582 physical facsimile leaves (`Page_0001.jpg` – `Page_0582.jpg`, 1-up quarto format) across **59 cohorts** (`Cohorts 1–59`)
- **Total Corpus Yield**:
  - **Source Transcription (`Source Text/`)**: 101,931 words (877,412 chars across 59 files)
  - **Draft Body Translation (`Draft/` & `Cohorts/`)**: 131,187 words (1,268,286 chars in `complete.md`)
  - **Critical Apparatus (`Final_footnotes.txt` & `footnotes.md`)**: **1,365 bijective footnotes** (`[^1]`–`[^1365]`, 78,966 words / 503,797 chars)
  - **Combined English Output (Body + Apparatus)**: **210,153 words** (207,924 compiled words in `complete.md` + local notes)
- **Audit Timestamp**: `2026-10-30T12:52:00-04:00`

---

## 1. Cohort Velocity & Bottleneck Autopsy

### 1.1 Global Cohort Velocity Telemetry (Cohorts 1–59)
Wall-clock subagent execution durations were measured from exact `invoke_subagent` tool-return timestamps to `<SYSTEM_MESSAGE>` completion timestamps in `transcript.jsonl`, alongside filesystem deltas (`Work_Orders/cohort_N_work_order.md` mtime to `Draft/*_footnotes.txt` mtime):

| Metric | Value | Notes |
|---|---|---|
| **Total Cohorts Executed** | **59** | Cohorts 1–58 (10 leaves each), Cohort 59 (2 leaves: `p581`–`p582`) |
| **Total Active Subagent Runtime** | **43,516.0 s (12.09 hours)** | Pure `Gemini 3.8 Flash` worker execution time |
| **Mean Cohort Duration** | **737.6 s (12.29 min)** | ~73.8 seconds per physical leaf |
| **Median Cohort Duration** | **685.0 s (11.42 min)** | Interquartile range: `595s` – `842s` |
| **Fastest Cohort** | **Cohort #59: 434.0 s (7.23 min)** | 2 leaves (`p581`–`p582`, rear flyleaves & marginalia, 560 total words) |
| **Fastest 10-Leaf Cohort** | **Cohort #45: 474.0 s (7.90 min)** | `p441`–`p450` (Lenten Triodion prose synaxaria, 2,329 draft words, 12 footnotes) |
| **Slowest Cohort** | **Cohort #58: 1,718.0 s (28.63 min)** | `p571`–`p580` (Acrostic Penitential Canon + Fiol 1491 Colophon, 97 footnotes) |
| **Subagent Retries Required** | **0 / 59 (0.0%)** | `cohort_retry_counts == {}` in `orchestrator_state.json` |

### 1.2 Autopsy of the 3 Slowest Cohorts (+ Notable Runner-Up)

| Rank | Cohort & Leaf Range | Active Subagent Time (Filesystem Delta) | Source Words | Draft Body Words | Footnotes Count (Words) | Total Output Words | Primary Bottleneck Classification |
|---|---|---|---|---|---|---|---|
| **1 (Slowest)** | **Cohort #58** (`p571`–`p580`) | **1,718.0 s / 28.63 m** (`1,537.1 s`) | 1,271 | 1,704 | **97** (2,958 w) | **4,662 w** | Acrostic reconstruction + 1491 woodcut/colophon diplomatic apparatus + internal subagent gate pre-check |
| **2** | **Cohort #1** (`p1`–`p10`) | **1,310.0 s / 21.83 m** (`1,235.0 s`) | 1,196 | 1,984 | **24** (765 w) | **2,749 w** | Cold-start *vyaz* title decipherment + 8-Tone Triadika/Photagogica setup + internal gate failure/repair |
| **3** | **Cohort #56** (`p551`–`p560`) | **1,156.0 s / 19.27 m** (`1,073.1 s`) | 1,591 | 2,134 | **141** (4,111 w) | **6,245 w** | Extreme apparatus density (`14.1 notes/leaf`, 4,111 footnote words) on Polyeleos/Megalynaria incipits |
| *4 (Runner-Up)* | **Cohort #40** (`p391`–`p400`) | **1,062.0 s / 17.70 m** (`1,086.4 s`) | 1,928 | 2,299 | **22** (735 w) | **3,034 w** | Physical binding transposition of Folio 210 (`p395`–`p396`) requiring codicological cross-collation |

#### Detailed Root-Cause Breakdown:
1. **Cohort #58 (`p571`–`p580`, 28.63 min)**:
   - **Codicological & Visual Bottleneck**: Combined three distinct genres in a single 10-leaf window: (i) the conclusion of the Pre-Communion confessional enumeration of sins (`p571`–`p572`), (ii) the Tone 6 Sessional Hymns and Acrostic Penitential Canon unto Our Lord Jesus Christ (`p572`–`p579`, carrying the Slavonic acrostic *Очию моею плачь прийди* / *"Come, weeping of mine eyes"* across Odes 1–6), and (iii) leaf `p580`, featuring the full-page architectural woodcut printer's device of the Royal Capital City of Krakow (*herb Krakowa* and Schweipolt Fiol's `S V F I O L` monogram) and the landmark 1491 Cyrillic colophon under King Casimir IV.
   - **Apparatus & Self-Verification Bottleneck**: To satisfy Statutory Mandate 12 (100% diplomatic completeness on civic/royal titulature and symmetric woodcut descriptions) and annotate every acrostic stanza and scriptural allusion, the subagent generated **97 footnotes (2,958 words — 1.74x the length of the body translation)** and executed `run_small_pause_gate.py` inside its own turn before returning.
2. **Cohort #1 (`p1`–`p10`, 21.83 min)**:
   - **Visual & Epigraphic Bottleneck**: Leaf `p2` contains the ornamental woodcut headpiece and dense Cyrillic *vyaz* (*в'язь*, ligatured display calligraphy) incipit (*Начало с Богомъ Часословцю...*), followed immediately by the 8-Tone cycle of Midnight Office Triadika (*Троичны*) and Matins Photagogica (*Свѣтилна*, `p2`–`p6`) and the Weekday Exapostilaria (`p7`–`p10`).
   - **Internal Gate Failure Loop**: As logged in `scratch/triage_inbox.jsonl` (`2026-10-29T12:17:56Z`), the subagent ran `run_small_pause_gate.py` internally, hit a first-pass gate failure, edited the files to fix it, and re-ran the gate before yielding its turn (`12:21:25Z`), adding ~4 minutes of extra tool calls inside the subagent conversation.
3. **Cohort #56 (`p551`–`p560`, 19.27 min)**:
   - **Extreme Footnote Generation Bottleneck**: Leaves `p551`–`p560` contain the Festive Polyeleos Selected Psalm verses (*Припѣвы*) for Pascha/Thomas Sunday, Ascension, Pentecost, Transfiguration, and St. John the Forerunner, followed on `p557` by the Festal Megalynaria (*Величанія*). Because each leaf contains 12–18 individual clipped psalm verses printed as 1-line incipits, the subagent attached an LXX/Masoretic + Slavonic witness footnote to every single verse—producing **141 footnotes (4,111 words of apparatus + 2,134 body words = 6,245 total words)** in a single cohort (`14.1 footnotes/leaf`).

---

## 2. Small Pause Gate, Deterministic Self-Healing & Flash Failure Modes

### 2.1 Comprehensive Catalog of Gate & Compiler Anomalies
Across all 59 cohorts, **36 cohorts** logged pre-check or initial-check entries in `scratch/triage_inbox.jsonl`, **33 / 59 cohorts (55.9%)** triggered orchestrator `attempt_deterministic_self_healing()` during `--verify-cohort` (100% of which self-healed on the first pass without a single subagent retry), **13 / 59 cohorts** had residual footnote/body `-eth` or vocabulary tokens healed during `compile_final_edition.py` Step 3, and **4 / 59 cohorts** failed `verify_publication_edition.py` Gate 5A prior to targeted remediation:

| Stage & Gate | Cohorts Affected | Total Instances | Exact Failure Signatures Observed | Resolution Mechanism |
|---|---|---|---|---|
| **Phase 1 Gate 1A (`lint_vocabulary.py`)** | **15 / 59 cohorts** (`#17, #23, #24, #28, #30, #32, #33, #35, #37, #40, #41, #42, #50, #51, #53`) | ~28 tokens | `Flash` emitted `Sedalen` (for `Sessional Hymn`), `Irmos` (for `Heirmos`), `Apolytikion` (for `Troparion`), or `"for ever and ever"` (for `"unto ages of ages"`). | 100% auto-healed by `_apply_vocabulary_and_doxology_healing()` in `autonomous_orchestrator.py`. |
| **Phase 1 Gate 2 (`hieratic_pronoun_audit.py`)** | **14 / 59 cohorts** (`#10, #13, #20, #21, #22, #25, #32, #33, #34, #36, #37, #47, #48, #57`) | 20 pronouns | Lowercase `he`, `him`, `his`, `thou`, `thee`, `thy` referring to Christ or God the Father inside dense psalm stichoi or subordinate clauses (`"who... in his mercy"`). | 100% auto-healed by `hieratic_pronoun_audit.py --fix` inside `attempt_deterministic_self_healing()`. |
| **Phase 1 Gate 1B (`lint_liturgical_slop.py`)** | **7 / 59 cohorts** (`#3, #6, #9, #14, #18, #27, #39`) | 10 tokens | `wondrous` outside `"Wondrous is God in His saints"`, `wherefore` in rubrics, `verily`, and rubrical `the priest shall...` / `-eth` forms (`readeth`, `singeth`). | 100% auto-healed by `_apply_anti_slop_healing()` in `autonomous_orchestrator.py`. |
| **Phase 1 Gate 4 (`structural_audit.py`)** | **2 / 59 cohorts** (`#6` on `p55`; `#53` on `p529`) | 2 headings | `UNSANCTIONED_H1_HEADING`: `# THE ORDER OF THE TYPIKA, WHICH IS THE OBEDNITSA` (`p55`) and `# SELECTED PSALMS FOR SOLEMN COMMEMORATIONS AND FEASTS OF THE LORD[^864]` (`p529`). | Auto-demoted to inline italics `*...*` by `_heal_epigraphic_headings()`. *(Note: caused Part-slicing skew; see §4.1).* |
| **Phase 1 Gate 3 (`reconcile_footnotes.py`)** | **0 / 59 cohorts** at orchestrator gate | 0 | Zero orphaned or missing footnotes across all 1,365 notes (`[^1]`–`[^1365]`). | `_reconcile_footnote_bijectivity()` and subagent pre-checks maintained 100% parity. |
| **Phase 1 Gate 1C (`chromatic_rubric_verifier.py`)** | **57 / 59 cohorts** (non-blocking warnings) | ~240 leaf warnings | `[GATE 1C WARNING] Leaf pN rubric lacks verified red pigment` on black-ink rubrics or faded cinnabar in the 1491 exemplar. | Non-blocking warning (`PASSED`). |
| **Phase 2 Step 3 (`heal_cohort_and_apparatus_text`)** | **13 / 59 cohorts** | ~35 tokens | Residual 3rd-person `-eth` verbs (`hath`, `doth`, `shineth`, `granteth`) inside hymn body stanzas or `footnotes.txt` quotes (e.g. Cohort 17 `"My heart hath poured forth"`). | Auto-healed in-place across `Cohorts/` and `footnotes.txt` by `compile_final_edition.py`. |
| **Phase 2 Gate 5A (`verify_publication_edition.py`)** | **4 / 59 cohorts** (`#17, #18, #44, #59`) | **9 source lines** (18 gate errors across `complete.md` + parts) | **Unparenthesized Cyrillic in square brackets**: `[Всемирная радость]` (`c17:L3`), `[Крест начертав]` (`c17:L11`, `c18:L59`), Cyrillic/Greek homoglyph hybrid `[κελεύсате]` (`c44:L15, L18`), and `[ѿ а в г д]`, `[дєду • Бойсько • корну • рокъ]`, `[филипыкъ дѣ҃ • съвѧ...]`, `[свѧтаа троица]` (`c59:L14–20`). | Required manual Python regex patch during Phase 2 before `--compile-publication` passed Gate 5A. |

### 2.2 New Deterministic Healers & Template Guardrails Needed at the Source
1. **Universal Square-Bracketed Cyrillic & Greek Homoglyph Sanitizer (Eliminates 100% of Gate 5A Failures)**:
   - **Root Cause**: `Flash` subagents intermittently use square brackets `[Крест начертав]` or `[ѿ а в г д]` when glossing an original Slavonic incipit or marginal inscription inside an already-italicized rubric (`*...*`), or mix Cyrillic homoglyphs (`с, а, е, о, р, х`) into Greek liturgical exclamations (`[κελεύсате]`).
   - **Deterministic Fix**: Add two regex passes to both `_apply_vocabulary_and_doxology_healing()` in `scripts/autonomous_orchestrator.py` and `heal_cohort_and_apparatus_text()` in `scripts/compile_final_edition.py`:
     1. Convert square-bracketed Cyrillic strings in body lines into MTS-1 parenthetical italics:
        `re.sub(r"\[([^\[\]\n]*[\u0400-\u04FF][^\[\]\n]*)\]", lambda m: f"(*{m.group(1).strip('* ')}*)", line)` (excluding `[Acrostic: ...]`).
     2. Normalize mixed Greek+Cyrillic tokens (any word containing both `[\u0370-\u03FF\u1F00-\u1FFF]` and `[\u0400-\u04FF]`) by mapping Cyrillic homoglyphs (`а->α, в->β, е->ε, и->η, к->κ, м->μ, н->ν, о->ο, р->ρ, с->σ, т->τ, у->υ, ф->φ, х->χ`) to pure Greek Unicode.
2. **Pre-Flight Footnote & Non-Rubric `-eth` Verb Healer in Phase 1 (`autonomous_orchestrator.py`)**:
   - Currently, `_apply_anti_slop_healing()` in `scripts/autonomous_orchestrator.py` (lines 742–769) only normalizes a hardcoded 13-verb `eth_map` plus `actor_eth_pat` on `draft_text`, whereas `compile_final_edition.py` (lines 360–435) uses the comprehensive 120-verb `EXACT_ETH_VERB_MAP` + morphological stem converter across both body and footnotes. Unifying `_apply_anti_slop_healing()` to import and call `_convert_3rd_person_eth_token()` from `compile_final_edition.py` on both `draft_text` and `footnotes_path` will eliminate the 13-cohort discrepancy between Phase 1 and Phase 2.
3. **Subagent Self-Check Guardrail in `data/templates/work_order_template.md`**:
   - Subagents running `run_small_pause_gate.py` internally polluted `scratch/triage_inbox.jsonl` with 36 entries and added 2–4 minutes of latency per cohort, even though `autonomous_orchestrator.py --verify-cohort` runs `attempt_deterministic_self_healing()` automatically in `< 0.5s`. `work_order_template.md` §3 should explicitly instruct `ephemeral_translator` subagents **not** to invoke `run_small_pause_gate.py` via `run_command` (or `run_small_pause_gate.py` should only append to `triage_inbox.jsonl` when `--log-triage` is passed by the orchestrator *after* deterministic self-healing fails).

---

## 3. Argon Review Queue Signal Precision (`argon_review_queue.json`)

### 3.1 Empirical Breakdown of the 73 Queued Leaves
Out of **582 physical leaves**, `run_small_pause_gate.py` queued **73 leaves (12.5% of the codex)** across 14 cohorts (`Cohorts #18, #46, #47, #49–#59`):

| Signal Category | Leaves Triggered | % of Queued (`N=73`) | % of Codex (`N=582`) | Cohorts Affected | True Epigraphic / Philological Cruxes | False-Positive Signal Noise |
|---|---|---|---|---|---|---|
| **Signal 1: `epigraphic_uncertainty`** (`[?]`, `[illegible]`, `[lacuna]`) | **0** | 0.0% | 0.0% | None | 0 | 0 |
| **Signal 2: `borderline_sgc02_ratio`** (`< 0.50` or `> 2.20`) | **12** *(7 pure + 5 overlap)* | 16.4% | 2.1% | `#18` (`p171`), `#46` (`p451,452,455,459`), `#47` (`p468`), `#49` (`p488,489,490`), `#50` (`p494,499`), `#52` (`p511`) | **1** (`p490` Bright Friday monastic ossuary rubric) | **11 / 12 (91.7% noise)** — ratios `2.23`–`2.83` caused by abbreviated Slavonic Triodion rubrics expanding into full English syntax |
| **Signal 3: `dense_polyglot_apparatus`** (`>= 5` footnotes or `>= 5` table rows) | **66** *(61 pure + 5 overlap)* | 90.4% | 11.3% | `#49`–`#51`, `#53`–`#59` (**100% of leaves in Cohorts 55–58**: `p541`–`p580`) | **3** (`p490` ossuary rubric, `p580` Fiol colophon, `p581` Barvinok 1924 note & 16th-c. pen trials) | **63 / 66 (95.5% noise)** — routine LXX/Masoretic psalm verse citations on Selected Psalms (`p531`–`p556`), Megalynaria (`p557`–`p563`), and Pre-Communion canons (`p564`–`p579`) |
| **Signal 4: `QUARANTINED_FOR_ARGON`** | **0** | 0.0% | 0.0% | None | 0 | 0 |
| **Total Unique Queued Leaves** | **73** | **100.0%** | **12.5%** | **14 cohorts** | **3 / 73 (4.1% precision)** | **70 / 73 (95.9% false-positive noise)** |

### 3.2 Missed False Negatives (True Codicological Cruxes Not Queued)
Conversely, two major mid-codex physical anomalies in the 1491 Krakow Horologion were **not** queued into `argon_review_queue.json` because they had `< 5` footnotes on the leaf and `SGC-02` ratios around `1.35`–`1.55`:
1. **Leaf `p346` (Cohort #35)**: The massive historical quire lacuna in the Krakow exemplar where the Menologion jumps mid-page from February 5 (St. Agatha) directly to May 7 (Apparition of the Precious Cross), omitting 3 months of the calendar (`[^395]`).
2. **Leaves `p395`–`p396` (Cohort #40)**: The physical binding transposition of Folio 210 in the exemplar (`[^449]`), where the conclusion of July 24 (St. Christina and Sts. Boris & Gleb) and July 25 (Dormition of St. Anna) are bound out of sequence.

### 3.3 Calibration Recommendations for Horologion / Liturgical Compendium Genres
1. **Raise `dense_polyglot_apparatus` Footnote Threshold from `>= 5` to `>= 12` (or Exclude Pure Scripture/Incipit Citations)**:
   - In anthology sections (Selected Psalms / Polyeleos, Megalynaria, Pre-Communion Psalms), a single page contains 10–18 short psalm verses, and diligent subagents attach an LXX citation footnote to each verse, causing **100% of leaves `p541`–`p580` (40 consecutive leaves)** to flood `argon_review_queue.json`. Raising the threshold in `scripts/run_small_pause_gate.py` (line 175) from `>= 5` to `>= 12` footnotes per leaf—or counting only footnotes > 250 characters / containing `lacuna|transpos|corrupt|variant|colophon|marginal|unclear`—reduces false positives on `1491_krakow_fiol_horologion` from **66 leaves down to 4 leaves** while capturing 100% of true codicological cruxes (`p346`, `p395`, `p490`, `p580`, `p581`).
2. **Relax Upper `SGC-02` Borderline Ratio for Abbreviated Rubrical Directories from `2.20` to `2.65`**:
   - Church Slavonic rubrical directories (*Уставъ*) use heavily abbreviated *titlo* shorthand (`гл҃етъ іерє́й`, `поклонъ г҃`, `стїхъ`, `трп҃рь`) where 800 characters of Cyrillic routinely translate to 1,900–2,100 characters of grammatical English (`ratio = 2.25–2.50`). Increasing the upper `borderline_sgc02_ratio` trigger in `scripts/run_small_pause_gate.py` from `2.20` to `2.65` eliminates 10 of the 12 ratio false positives while still catching genuine hallucinations (`> 2.65`).

---

## 4. Monument-Type & Compiler Edge Cases (`compile_final_edition.py`)

### 4.1 Edge Case 4A: `universal_dynamic_h1` Part-Slicing Skew in Multi-Section Horologia
- **Observed Phenomenon**: The 1491 Krakow Horologion was compiled under `"mode": "universal_dynamic_h1"`, slicing the 582 leaves into 8 modular files (`part0`..`part7`) with severe size asymmetry:
  - `part0_front_matter.md`: `p1` (**4.0 KB**)
  - `part1_tone-1-trinity-hymns-and-photagogica.md`: `p2`–`p6` (**10.0 KB**)
  - `part2_exapostilaria-of-the-week.md`: `p7`–`p122` (**204.3 KB** — swallowed the entire Daily Office cycle: Midnight Office, Matins, Hours 1/3/6/9, Typika, Refectory, Vespers, and Great Compline under the misleading filename/title `EXAPOSTILARIA OF THE WEEK`!)
  - `part3_part-ii-troparia-and-kontakia-throughout.md`: `p123`–`p140` (**26.7 KB**)
  - `part4_part-iii-menologion.md`: `p141`–`p563` (**978.3 KB** — swallowed the Menologion `p141`–`p420`, Lenten Triodion `p421`–`p460`, Passion Week `p461`–`p480`, Pentecostarion `p481`–`p528`, Selected Psalms `p529`–`p556`, and Megalynaria `p557`–`p563` into a single 1 MB Part file!)
  - `part5_part-iv-rule-for-holy-communion.md`: `p564`–`p579` (**38.6 KB**)
  - `part6_part-v-printers-colophon-and-civic-arms-.md`: `p580` (**2.6 KB**)
  - `part7_part-vi-rear-endpapers-and-archival-marg.md`: `p581`–`p582` (**3.8 KB**)
- **Root Cause in Engine Code**:
  1. In `scripts/structural_audit.py` (lines 253–256) and `scripts/autonomous_orchestrator.py` (`_heal_epigraphic_headings`, lines 891–895), the global H1 whitelist unconditionally allows `^#\s+TONE\s+\d+` and `^#\s+EXAPOSTILARIA` (which are Part-level divisions in an **Octoechos**, but minor opening sub-tables on `p2` and `p7` of a **Horologion**).
  2. Conversely, when Cohort 6 (`p55`) emitted `# THE ORDER OF THE TYPIKA, WHICH IS THE OBEDNITSA` (failed `^#\s+ORDER\s+OF ` because of the leading article `THE `) and Cohort 53 (`p529`) emitted `# SELECTED PSALMS FOR SOLEMN COMMEMORATIONS AND FEASTS OF THE LORD[^864]` (lacked a `PART N:` prefix), Gate 4 flagged them as `UNSANCTIONED_H1_HEADING` and `_heal_epigraphic_headings()` demoted them to inline italics `*...*`, preventing `UniversalPublicationEngine._slice_parts()` from slicing the Typika/Vespers/Compline or the Triodion/Pentecostarion/Selected Psalms into their own modular Parts.

### 4.2 Edge Case 4B: Footnote Markers (`[^N]`) Leaking into Dynamic Part Titles & 40-Char Mid-Word Filename Truncation
- **Observed Phenomenon**:
  - In `codex_registry.json` and `handoff_note.md`, `part5`, `part6`, and `part7` were registered with raw footnote markers embedded inside their canonical titles and regexes:
    - `"title": "PART IV: RULE FOR HOLY COMMUNION[^1205]"`
    - `"title": "PART V: PRINTER'S COLOPHON AND CIVIC ARMS OF KRAKOW (1491)[^1354]"`
    - `"title": "PART VI: REAR ENDPAPERS AND ARCHIVAL MARGINALIA[^1359]"`
  - Furthermore, `slug = slugify(h1_title)[:40].strip("_")` in `scripts/compile_final_edition.py` (line 1015) sliced at character 40 without stripping trailing hyphens (`-`) or respecting word boundaries, producing `..._part6_part-v-printers-colophon-and-civic-arms-.md` (trailing hyphen before `.md`) and `..._part7_part-vi-rear-endpapers-and-archival-marg.md` (cut mid-word `marg`).
- **Root Cause in Engine Code**: `UniversalPublicationEngine._slice_parts()` (`scripts/compile_final_edition.py` lines 1011–1025) captures `m_h1.group(1).strip()` verbatim without stripping `\s*\[\^\d+\]` for `title` and `slug`, and calls `.strip("_")` on a hyphen-delimited slug (`slugify()` uses `-`, not `_`!).

### 4.3 Edge Case 4C: Mid-Sentence Seam Stitching Across 1-Up Quarto Page Breaks with Footnotes
- `stitch_leaf_stream()` in `scripts/compile_final_edition.py` stitched 3 mid-sentence page breaks cleanly across the 582 leaves. However, on leaves where a subagent attached a footnote marker `[^N]` to the final incomplete word/clause of leaf `pK` (e.g., `...we say [the verses]:[^209]` or rubric continuations `_...according to custom._` at the top of `p(K+1)` starting with an ellipsis `...`), `stitch_leaf_stream()` left the leading `...` continuation fragment as a separate paragraph (e.g., `cohort17.md:L3` `...universal joy`, `cohort17.md:L11` `...faithful...`, `cohort18.md:L59` `*...according to custom.*`, `cohort44.md:L18` `*...Command!"*`).

---

## 5. Granular Atomic Tagging Blueprint (Propers & Non-Propers)

To enable deterministic extraction of 100% of `1491_krakow_fiol_horologion` into `{monument_id}_atomic_corpus.json`, we audited all 59 `Cohorts/*.md` files (582 leaves, 2,400+ tagged structural blocks). Below is the complete inventory of **Variable Propers** and **Fixed Non-Propers** present in the 1491 Krakow Horologion, with their exact counts and regex patterns:

### 5.1 Variable Propers Inventory (Hymnographic & Calendar-Dependent Units)

| Atomic Unit Class | Code / Tag ID | Count in `Cohorts/*.md` | Exact Markdown / Regex Pattern in `Cohorts/*.md` |
|---|---|---|---|
| **Kontakion Stanzas** | `PROPER_KONTAKION` | **257** | `^\*(?:Another\s+)?Kontakion(?:\s+of\s+[^,*]+)?(?:,\s*Tone\s+[1-8])?(?:,\s*Podoben:[^*]+)?:\*(?:\[\^\d+\])?\s*(.*)$` |
| **Menologion / Synaxarion Day Rubrics** | `PROPER_MENOLOGION_DAY` | **230** | `^\*(?:Month\s+of\s+[A-Z][a-z]+|On\s+the\s+\d+(?:st|nd|rd|th)\s+day|In\s+the\s+same\s+month|Synaxarion)\b[^*]*\*(?:\[\^\d+\])?` |
| **Troparion / Apolytikion Stanzas** | `PROPER_TROPARION` | **223** | `^\*(?:Another\s+)?Troparion(?:\s+of\s+[^,*]+)?(?:,\s*Tone\s+[1-8])?:\*(?:\[\^\d+\])?\s*(.*)$` |
| **3-Layer Melodic Model (`Podoben`) Headings** | `PROPER_PODOBEN_HEADER` | **121** | `\*[^\n*]*?Tone\s+([1-8]),\s*Podoben:\s*"([^"]+)"\s*\(([^)]+)\)[^*]*\*` |
| **Theotokion & Stavrotheotokion Stanzas** | `PROPER_THEOTOKION` | **88** | `^\*(?:Cross-|Stavro)?[Tt]heotokion(?:\s*,\s*Tone\s+[1-8])?[^*]*:\*(?:\[\^\d+\])?\s*(.*)$` |
| **Festal Megalynaria (Magnifications)** | `PROPER_MEGALYNARION` | **38** | `(?:^\*Megalynarion[^*]*:\*|^\*\*We\s+magnify\s+(?:Thee|you)\b[^\n]*)` |
| **Stichera (Idiomela & Prosomoia)** | `PROPER_STICHERON` | **17** | `^\*(?:Sticheron|Stichera|Idiomelon|Prosomoia|On\s+the\s+Praises|On\s+"Lord,\s+I\s+have\s+cried")\b[^*]*\*(?:\[\^\d+\])?` |
| **Sessional Hymns (*Kathismata / Sedalny*)** | `PROPER_SESSIONAL_HYMN` | **15** | `^\*(?:Sessional\s+[Hh]ymn|Kathisma)(?:\s*,\s*Tone\s+[1-8])?[^*]*:\*(?:\[\^\d+\])?\s*(.*)$` |
| **Exapostilaria & Photagogica (*Svitilna*)** | `PROPER_EXAPOSTILARION` | **14** | `^\*(?:Exapostilarion|Photagogikon|Hymn\s+of\s+Light)[^*]*:\*(?:\[\^\d+\])?\s*(.*)$` |
| **Canon Odes & Heirmoi** | `PROPER_CANON_ODE_HEIRMOS` | **12** | `^\*(?:Ode|Canticle)\s+([1-9])(?:\s*,\s*Tone\s+[1-8])?\.\s*Heirmos:\*(?:\[\^\d+\])?\s*(.*)$` |
| **Prokeimena & Alleluiaria** | `PROPER_PROKEIMENON` | **7** | `^\*(?:Great\s+)?Prokeimenon(?:\s*,\s*Tone\s+[1-8])?[^*]*:\*(?:\[\^\d+\])?\s*(.*)$` |
| **Ikos Stanzas** | `PROPER_IKOS` | **1** | `^\*Ikos:\*(?:\[\^\d+\])?\s*(.*)$` |

### 5.2 Fixed Non-Propers Inventory (Horologion Ordinary, Rubrics, Psalms & Prayers)

| Atomic Unit Class | Code / Tag ID | Count in `Cohorts/*.md` | Exact Markdown / Regex Pattern in `Cohorts/*.md` |
|---|---|---|---|
| **Procedural & Ceremonial Rubrics** | `NONPROPER_PROCEDURAL_RUBRIC` | **701** | `^\*(?!(?:Troparion|Kontakion|Theotokion|Cross-Theotokion|Ode\s+\d|Sessional|Exapostilarion|Photagogikon|Sticheron|Verse|Glory|Both\s+now|Psalm\s+\d|Prayer))[^*\n]+\*(?:\[\^\d+\])?$` |
| **Physical Leaf Boundary Markers** | `META_LEAF_BOUNDARY` | **582** | `^===\s+LEAF\s+p(\d+)\s+===$` |
| **Psalm Verses / Polyeleos Stichoi (`*Verse:*`)** | `NONPROPER_STICHOS_VERSE` | **95** | `^\*Verse(?:\s+\d+)?:\*(?:\[\^\d+\])?\s*(.*)$` |
| **Liturgical Dialogue & Litany Labels** | `NONPROPER_DIALOGUE_UTTERANCE` | **51** | `^\*\*(Priest|Deacon|Reader|Choir|People|Ecclesiarch|Superior|Canonarch):\*\*\s*(.*)$` |
| **Doxology & Triadikon Connectors** | `NONPROPER_DOXOLOGY_TAG` | **26** | `^\*(Glory\s+to\s+the\s+Father[^*]*|Glory\.\.\.\s*Both\s+now\.\.\.|Both\s+now\s+and\s+ever[^*]*)\*(?:\[\^\d+\])?\s*(.*)$` |
| **Major Codex Part Landmarks (`H1`)** | `META_PART_LANDMARK_H1` | **7** | `^#\s+([^\n#]+)$` |
| **Fixed Psalms & Scriptural Canticles** | `NONPROPER_FIXED_PSALM` | **6** | `^\*Psalm\s+(\d+)\b[^*]*\*(?:\[\^\d+\])?` |
| **Named Sacerdotal & Horologion Prayers** | `NONPROPER_NAMED_PRAYER` | **6** | `^\*(?:A\s+)?Prayer\s+(?:of|to|after|before)\b[^*]*\*(?:\[\^\d+\])?` |
| **Primary Service / Office Headpieces (`H2`)** | `NONPROPER_OFFICE_HEADER_H2` | **5** | `^##\s+([^\n#]+)$` |
| **Patristic Catechetical Homilies** | `PROPER_PATRISTIC_HOMILY` | **1** *(5 leaves: `p476`–`p480`)* | Chrysostom Paschal Catechetical Word (*Paul's mouth: Christ's mouth... If anyone is devout and a lover of God...*) |

---

## 6. Top 5 Concrete Engine Hardening Recommendations

Based on the empirical evidence from all 59 cohorts of `1491_krakow_fiol_horologion`, we rank the top 5 highest-leverage code and template modifications for the cross-wave System Hardening Plan:

### Rank 1: Strip Footnote Markers & Fix Hyphen Truncation in Dynamic H1 Part Slicing (`scripts/compile_final_edition.py`)
- **Target File & Function**: `scripts/compile_final_edition.py` $\rightarrow$ `UniversalPublicationEngine._slice_parts()` (lines 1011–1025).
- **Empirical Evidence**: In `1491_krakow_fiol_horologion`, H1 headings with attached footnotes (`# PART IV: RULE FOR HOLY COMMUNION[^1205]`, `# PART V: ...[^1354]`, `# PART VI: ...[^1359]`) leaked raw `[^N]` strings into `codex_registry.json` Part titles and `handoff_note.md`, while `slugify(h1_title)[:40].strip("_")` failed to strip trailing hyphens (`-`), producing `..._part6_part-v-printers-colophon-and-civic-arms-.md` and mid-word truncated `..._part7_part-vi-rear-endpapers-and-archival-marg.md`.
- **Concrete Code Change**:
  1. Strip footnote markers before storing `clean_h1_title = re.sub(r"\s*\[\^\d+\]", "", raw_h1_title).strip()`.
  2. Match `start_landmark` with an optional trailing footnote pattern: `rf"^#\s+{re.escape(clean_h1_title)}(?:\s*\[\^\d+\])*$"`.
  3. Truncate `slug` cleanly on word boundaries and strip `-_`: `slug = re.sub(r"-[^-]*$", "", slugify(clean_h1_title)[:45]).strip("-_") or pid`.

### Rank 2: Auto-Parenthesize Square-Bracketed Cyrillic & Sanitize Greek/Cyrillic Homoglyphs in Phase 1 & Phase 2 (`scripts/autonomous_orchestrator.py` & `scripts/compile_final_edition.py`)
- **Target Files & Functions**:
  - `scripts/autonomous_orchestrator.py` $\rightarrow$ `_apply_vocabulary_and_doxology_healing()` (lines 618–661)
  - `scripts/compile_final_edition.py` $\rightarrow$ `heal_cohort_and_apparatus_text()` (lines 592–629)
- **Empirical Evidence**: The **only** blocker during Phase 2 compilation (`verify_publication_edition.py` Gate 5A) was 9 lines across Cohorts 17, 18, 44, and 59 where `Flash` subagents enclosed Cyrillic incipits/pen-trials in square brackets (`[Всемирная радость]`, `[Крест начертав]`, `[ѿ а в г д]`, `[свѧтаа троица]`) or contaminated a Greek liturgical exclamation with Cyrillic homoglyphs (`[κελεύсате]`).
- **Concrete Code Change**:
  1. Add a universal regex converting square-bracketed Cyrillic in body lines to MTS-1 parenthetical italics: `re.sub(r"\[([^\[\]\n]*[\u0400-\u04FF][^\[\]\n]*)\]", lambda m: m.group(0) if "Acrostic:" in m.group(1) else f"(*{m.group(1).strip('* ')}*)", healed)`.
  2. Add a Greek-Cyrillic homoglyph sanitizer that detects any token containing both Greek (`[\u0370-\u03FF\u1F00-\u1FFF]`) and Cyrillic (`[\u0400-\u04FF]`) characters and transliterates lookalike Cyrillic codepoints (`а, в, е, и, к, м, н, о, р, с, т, у, ф, х`) to their canonical Greek Unicode equivalents.

### Rank 3: Genre-Scoped H1 Landmarks for Horologion / Compendium Codices (`scripts/structural_audit.py` & `data/templates/publication_spec_scaffolds.json`)
- **Target Files & Functions**:
  - `scripts/structural_audit.py` $\rightarrow$ `audit_structure()` (lines 241–265)
  - `scripts/autonomous_orchestrator.py` $\rightarrow$ `_heal_epigraphic_headings()` (lines 889–896)
  - `data/templates/publication_spec_scaffolds.json`
- **Empirical Evidence**: Allowing `^#\s+TONE\s+\d+` and `^#\s+EXAPOSTILARIA` globally while rejecting `# THE ORDER OF THE TYPIKA...` (`p55`) and `# SELECTED PSALMS...` (`p529`) caused `part2` (`exapostilaria-of-the-week.md`, 204 KB) to swallow the entire Daily Office and `part4` (`part-iii-menologion.md`, 978 KB) to swallow the Menologion, Triodion, Pentecostarion, and Selected Psalms.
- **Concrete Code Change**:
  1. Scope `^#\s+TONE\s+\d+` as an H1 landmark strictly to `octoechos` / `heirmologion` monuments; in `horologion` monuments, demote `# TONE N` and `# EXAPOSTILARIA` inside the Daily Office to `##` (H2).
  2. Expand the H1 landmark regex in `structural_audit.py` line 256 and `_heal_epigraphic_headings()` line 894 to allow optional leading `THE ` and major compendium divisions: `r"^#\s+(?:THE\s+)?(?:PART\s+[IVXLCDM\d]+|CHAPTER\s+\d+|SECTION\s+[IVXLCDM\d]+|APPENDIX|TABLE\s+OF\s+CONTENTS|ORDER\s+OF|MENOLOGION|SYNAXARION|TRIODION|PENTECOSTARION|SELECTED\s+PSALMS|PASCHALION|COLOPHON)\b"`.

### Rank 4: Recalibrate `argon_review_queue.json` Thresholds & Add Codicological Anomaly Keywords (`scripts/run_small_pause_gate.py`)
- **Target File & Function**: `scripts/run_small_pause_gate.py` $\rightarrow$ `update_argon_review_queue()` (lines 103–230).
- **Empirical Evidence**: 73 leaves (12.5% of the codex) were queued into `argon_review_queue.json`, of which **70 / 73 (95.9%) were false-positive noise** (66 leaves triggered by `>= 5` routine scripture/incipit footnotes on Selected Psalms and Megalynaria; 11 leaves triggered by `2.23–2.50` SGC-02 ratios on abbreviated Slavonic rubrics), while genuine physical anomalies on `p346` (Feb 5 $\rightarrow$ May 7 quire lacuna) and `p395`–`p396` (Folio 210 binding transposition) were missed.
- **Concrete Code Change**:
  1. Increase the `dense_polyglot_apparatus` footnote count threshold from `>= 5` to `>= 12` footnotes per leaf (or count only footnotes exceeding 220 chars).
  2. Increase the upper `borderline_sgc02_ratio` threshold for rubrical/compendium monuments from `2.20` to `2.65`.
  3. Add an explicit codicological anomaly scanner on cohort footnotes and body text (`\b(?:lacuna|missing\s+quire|transpos(?:ed|ition)|misbound|foliation\s+jump|colophon|autograph|pen\s+trial)\b`) so genuine physical defects like `p346` and `p395` are deterministically queued for Argon verification.

### Rank 5: Unify Phase 1 & Phase 2 `-eth` Verb Healing and Suppress Subagent Pre-Flight Triage Noise (`scripts/autonomous_orchestrator.py` & `data/templates/work_order_template.md`)
- **Target Files & Functions**:
  - `scripts/autonomous_orchestrator.py` $\rightarrow$ `_apply_anti_slop_healing()` (lines 741–771) and `attempt_deterministic_self_healing()`
  - `scripts/run_small_pause_gate.py` $\rightarrow$ `main()` (triage logging block)
  - `data/templates/work_order_template.md` (§3 Autonomous Execution Instructions)
- **Empirical Evidence**: Phase 1 `_apply_anti_slop_healing()` only checked 13 hardcoded `-eth` verbs on `draft_text`, leaving 13 cohorts with residual `-eth` verbs (`hath`, `doth`, `shineth`, `granteth`) in body or footnotes that had to be healed later in Phase 2 (`compile_final_edition.py` Step 3). Meanwhile, subagents invoking `run_small_pause_gate.py` inside their own turns wrote 36 premature failure records to `scratch/triage_inbox.jsonl` before the orchestrator's deterministic self-healer even ran.
- **Concrete Code Change**:
  1. Import `_convert_3rd_person_eth_token` and `heal_cohort_and_apparatus_text` from `scripts/compile_final_edition.py` directly into `attempt_deterministic_self_healing()` in `scripts/autonomous_orchestrator.py`, running it across both `raw_draft.md` and `footnotes.txt` during Phase 1 `--verify-cohort`.
  2. Only log failures to `scratch/triage_inbox.jsonl` in `autonomous_orchestrator.py` *after* `attempt_deterministic_self_healing()` fails to resolve a gate violation, keeping `triage_inbox.jsonl` 100% free of transient pre-heal noise.
