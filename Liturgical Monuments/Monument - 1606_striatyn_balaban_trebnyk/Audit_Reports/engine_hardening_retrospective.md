# Post-Run Engine Retrospective: 1606 Striatyn Euchologion / Trebnyk (`1606_striatyn_balaban_trebnyk`)

- **Monument ID**: `1606_striatyn_balaban_trebnyk`
- **Title**: *1606 Striatyn Euchologion / Trebnyk of Teodor & Hedeon Balaban (Молитвенник альбо Требник, Стрятин: Друкарня Балабанів, 1606)*
- **Book Type / Genre Register**: Quarto Church Slavonic Euchologion (*Trebnyk*) & Nomocanon (`1-up` single-page foliated print, 19–20 lines/page)
- **Physical Scale**: `1,401` physical leaves across `141` sequential cohorts (`Cohorts 1–140` at 10 leaves/cohort; `Cohort 141` at 1 leaf)
- **Corpus Yield**:
  - **Source Text (`Source Text/*_source.txt`)**: `134,085` words (`864,608` characters)
  - **English Draft (`Draft/*_raw_draft.md`)**: `173,311` words (`1,034,324` characters)
  - **Critical Apparatus (`Final/Final_footnotes.txt`)**: `4,364` bijective footnotes (`[^1]` through `[^4364]`, `1,251,918` bytes)
  - **Canonical Structural Divisions**: `58` top-level `H1` landmarks (`# PREFACE: TO THE READER` + `# PART I` through `# PART LVII`)

---

## 1. Cohort Velocity & Bottleneck Autopsy

### 1.1 Aggregate Velocity Telemetry (Cohorts 1–141)
Timestamps were extracted across all 141 cohorts by comparing `Work_Orders/cohort_NN_work_order.md` modification times (`wo_mtime`), `Draft/1606_striatyn_balaban_trebnyk_cohortN_raw_draft.md` completion times (`draft_mtime`), and `Audit_Reports/cohortN_small_pause_report.json` gate completion times (`rep_mtime`). Note that `Cohort 1` (`wo_to_draft_sec = 1,123.24s`) had its Small Pause Gate report regenerated during a mid-sprint audit (`wo_to_rep_sec = 32,797.80s`), so single-pass gate velocity statistics below cover `N = 140` contiguous cohorts (`Cohorts 2–141`) plus `Cohort 1`'s active translation window:

| Metric | Value | Notes |
|---|---|---|
| **Total Completed Cohorts** | `141 / 141` (`1,401` leaves) | `100.0%` closed mathematical leaf conservation |
| **Total Active Sprint Wall-Clock Time** | `106,932.61 s` (`29.70 hours`) | Sum of active cohort execution windows (`Cohorts 1–141`) |
| **Mean Cohort Total Duration (`wo -> report`)** | `755.78 s` (`12.60 min`) | `75.58 s / leaf` across `N = 140` contiguous cohorts |
| **Median Cohort Total Duration (`wo -> report`)** | `690.67 s` (`11.51 min`) | `69.07 s / leaf` |
| **Mean Translation & Vision Duration (`wo -> draft`)** | `589.05 s` (`9.82 min`) | `77.9%` of total cohort wall-clock time |
| **Mean Apparatus & Gate Duration (`draft -> report`)** | `166.73 s` (`2.78 min`) | `22.1%` of total cohort wall-clock time (footnotes + gate verification) |
| **Mean Words / Cohort** | `1,229.16` English words (`950.96` Slavonic words) | Mean draft-to-source char ratio: `1.196` |
| **Mean Footnotes / Cohort** | `30.95` footnotes / cohort | `3.11` footnotes / physical leaf |
| **Fastest Full Cohort (10 leaves)** | `Cohort 51` (`419.65 s` / `6.99 min`) | `1,245` words, `24` footnotes (Funeral canon stanzas, low rubrical branching) |
| **Fastest Cohort Overall (1 leaf)** | `Cohort 141` (`206.84 s` / `3.45 min`) | `203` words, `1` footnote (Leaf `p1401` outer binding board) |

### 1.2 Top 10 Slowest Cohorts & Bottleneck Breakdown

| Rank | Cohort | Leaves | `wo -> draft` (s) | `draft -> report` (s) | Total `wo -> report` (s) | English Words | Slavonic Words | Footnotes | Primary Bottleneck Category |
|---|---|---|---|---|---|---|---|---|---|
| **1** | **Cohort 44** | `p431–p440` | `1,238.09` | `652.67` | **`1,890.76`** (`31.5 min`) | `1,175` | `947` | `21` | Dense Eucharistic thanksgiving prayers + transition to `# PART XVIII` (Communion of the Sick in Haste) with heavily abbreviated marginal rubrics and multi-part footnote writing (`652.67s`). |
| **2** | **Cohort 139** | `p1381–p1390` | `1,064.76` | `714.45` | **`1,779.21`** (`29.7 min`) | `1,579` | `931` | `28` | **Highest word count in monument (`1,579` words)**; `# PART LVII: TABLE OF CONTENTS (ОГЛАВЛЕНІЕ ВЪСЛѢДОВАНІЙ)`—10 pages of dense tabular chapter titles + dual Church Slavonic alpha-numeric folio numbers (`а҃`..`хл҃ѕ`) mapped to Arabic numerals. |
| **3** | **Cohort 135** | `p1341–p1350` | `1,162.31` | `240.84` | **`1,403.14`** (`23.4 min`) | `1,299` | `1,102` | `63` | **Nomocanon Penitential Kanonarion** (`# PART LIV` cont.): 42 discrete casuistic canons per 10-leaf span with dense red/black rubric alternation and **63 scholarly footnotes** (3rd highest in monument). |
| **4** | **Cohort 103** | `p1021–p1030` | `779.71` | `569.44` | **`1,349.15`** (`22.5 min`) | `1,205` | `1,101` | `11` | `# PART XXXVIII: PRAYERS FOR EVERY NEED`—casuistic ritual purity prayers (polluted vessels, grain/wine defilement) with dense Levitical/patristic concordances. |
| **5** | **Cohort 47** | `p461–p470` | `620.09` | `627.43` | **`1,247.52`** (`20.8 min`) | `1,173` | `964` | `17` | Canon at the Parting of the Soul from the Body (`# PART XIX`)—first-person dramatic penitential stichera and canon odes with extended apparatus composition (`627.43s`). |
| **6** | **Cohort 45** | `p441–p450` | `879.79` | `352.37` | **`1,232.15`** (`20.5 min`) | `1,184` | `863` | `15` | Opening of `# PART XIX` (Separation of the Soul) + Gate 2 pronoun self-healing cycle (`scratch/triage_inbox.jsonl` event). |
| **7** | **Cohort 41** | `p401–p410` | `362.00` | `864.31` | **`1,226.31`** (`20.4 min`) | `1,118` | `875` | `42` | Pre-Communion prayers of St. Basil, St. John Chrysostom, and St. Symeon Metaphrastes (`# PART XVI`), plus unnumbered printed folio anomaly on `p407` requiring `42` apparatus notes (`864.31s`). |
| **8** | **Cohort 38** | `p371–p380` | `1,012.65` | `156.64` | **`1,169.29`** (`19.5 min`) | `1,133` | `1,028` | `40` | Pre-Communion Canon and Troparia (`# PART XVI`) with dense interlinear cinnabar rubrics and `40` footnotes. |
| **9** | **Cohort 98** | `p971–p980` | `983.59` | `175.23` | **`1,158.82`** (`19.3 min`) | `1,239` | `1,035` | `49` | Opening of `# PART XXXV: THE CONSOLATORY SERVICE (МОЛЕБЕНЪ)`—high density of abbreviated liturgical incipits, litanies, and `49` footnotes. |
| **10** | **Cohort 4** | `p31–p40` | `919.75` | `230.43` | **`1,150.18`** (`19.2 min`) | `1,300` | `903` | `21` | Transition from Naming of a Child (`# PART I`) to `# PART II: CANONS OF THE HOLY APOSTLES CONCERNING HOLY BAPTISM` with woodcut headpiece and marginal citations. |

### 1.3 Autopsy of the 3 Slowest Cohorts
1. **Cohort 44 (`1,890.76s` / `31.5 min`, `p431–p440`)**:
   - **Codicological & Visual Root Cause**: Spans the seam between the concluding Prayers of Thanksgiving after Holy Communion (`# PART XVII`, `p431–p432`, Prayers of St. Basil and St. Symeon Metaphrastes) and `# PART XVIII: THE ORDER OF HOW IT IS BEFITTING TO GIVE COMMUNION TO A SICK PERSON IN HASTE` (`p432–p440`). The sick-communion rite packs rapid alternating cinnabar rubrics, truncated prayer incipits, and conditional rubrical clauses (`*And if the sick person be near unto death...*`) onto every page.
   - **Prompt/Execution Root Cause**: The worker spent `1,238.09s` transcribing and translating the dense conditional rubrics and `652.67s` compiling 21 detailed liturgical footnotes.
2. **Cohort 139 (`1,779.21s` / `29.7 min`, `p1381–p1390`)**:
   - **Codicological & Visual Root Cause**: Contains 10 consecutive leaves of `# PART LVII: TABLE OF CONTENTS (ОГЛАВЛЕНІЕ ВЪСЛѢДОВАНІЙ)`. Each physical page lists 15–22 chapter entries aligned with right-justified Church Slavonic Cyrillic numeral folio references (`Ли́стъ а҃` through `Ли́стъ хл҃ѕ`).
   - **Prompt/Execution Root Cause**: Converting every Slavonic letter-numeral (`рн҃д`, `тм҃ѳ`, `хл҃ѕ`, etc.) into both parenthetical diplomatic Slavonic and verified Arabic folio equivalents (`[Fol. 154]`, `[Fol. 349]`, `[Fol. 636]`) while preserving 1:1 line structure produced the **largest English word count of the entire monument (`1,579` words, `8,444` chars, draft-to-source word expansion `1.70x`)** and required `714.45s` between draft completion and final report verification.
3. **Cohort 135 (`1,403.14s` / `23.4 min`, `p1341–p1350`)**:
   - **Codicological & Visual Root Cause**: Sits in the heart of the Striatyn Nomocanon (`# PART LIV` cont., `p1341–p1350`, fols. `675r–679v`), covering 42 distinct canonical penances (perjury, grave-robbing, sacrilege, clerical usury, sorcery, childbirth in extremis, and the regulations for spiritual fathers hearing confessions of women). Every page alternates 4–6 times between red cinnabar subject headers (`*Of the Holy Fathers:*`, `*Injunctions:*`, `*Concerning Women:*`) and black statutory clauses with marginal Greek/Slavonic canon numbers (`Canon 65 of St. Basil`, `Canon 24 of Ancyra`, etc.).
   - **Prompt/Execution Root Cause**: Annotating every canonical citation generated **63 scholarly footnotes across 10 leaves** (`6.3 footnotes/leaf`, triggering the Argon review queue on 8 of the 10 leaves).

---

## 2. Small Pause Gate, Deterministic Self-Healing & Flash Failure Modes

### 2.1 Complete Catalog of Small Pause Gate Anomalies (`scratch/triage_inbox.jsonl`)
Across `141` cohorts (`1,401` physical leaves), `125` cohorts (`88.7%`) passed all Small Pause Gates on the first verification pass, `15` cohorts (`10.6%`) failed the initial gate pass and were **100% automatically repaired in-place** by `attempt_deterministic_self_healing()` (or a targeted lexicon update on Cohort 106) with **zero subagent retries**, and **only `1` cohort (`Cohort 2`, `0.7%`) required a `Model="flash"` subagent retry**:

| Cohort | Leaves | Timestamp (UTC) | Failing Gate | Exact Failure Mode | Resolution Mechanism |
|---|---|---|---|---|---|
| **2** | `p11–p20` | `2026-10-29T12:33:34Z` | Gate 4 / Gate 2 | Early sprint structural/pronoun alignment on `# PART I` (`Order for the Naming of a Child`). | **1 targeted `Flash` subagent retry** (`cohort_retry_counts: {"2": 1}`); passed 100%. |
| **20** | `p191–p200` | `2026-10-29T16:30:59Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Trinity Deity pronoun (`thy`/`him`/`his`) in Seven-Priest Holy Unction prayers (`# PART XIII`). | Repaired automatically by `attempt_deterministic_self_healing()` Step 4 (pronoun capitalizer). |
| **21** | `p201–p210` | `2026-10-29T16:42:29Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Trinity Deity pronoun in Holy Unction Gospel/prayer sequence. | Repaired automatically by `attempt_deterministic_self_healing()`. |
| **27** | `p261–p270` | `2026-10-29T18:04:02Z` | Gate 1A / Gate 2 | Forbidden vocabulary variant (`leave-taking` instead of `Apodosis` in `[^542]`) + lowercase Deity pronoun in `# PART XIV` (Confession). | Repaired automatically by `attempt_deterministic_self_healing()` Step 3 & Step 4. |
| **45** | `p441–p450` | `2026-10-29T22:33:01Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Deity pronoun in `# PART XIX` (Order at the Separation of the Soul). | Repaired automatically by `attempt_deterministic_self_healing()`. |
| **54** | `p531–p540` | `2026-10-30T00:08:38Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Deity pronoun in `# PART XXI` (Order of Burial stichera/prayers). | Repaired automatically by `attempt_deterministic_self_healing()`. |
| **58** | `p571–p580` | `2026-10-30T00:50:46Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Deity pronoun in `# PART XXV` (The Parastas funeral office). | Repaired automatically by `attempt_deterministic_self_healing()`. |
| **60** | `p591–p600` | `2026-10-30T01:10:05Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Deity pronoun in `# PART XXVI` (Clothing of the Rassa). | Repaired automatically by `attempt_deterministic_self_healing()`. |
| **62** | `p611–p620` | `2026-10-30T01:31:51Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Deity pronoun in `# PART XXVII` (Order of the Little Schema / Mantiya). | Repaired automatically by `attempt_deterministic_self_healing()`. |
| **67** | `p661–p670` | `2026-10-30T02:20:26Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Deity pronoun in `# PART XXVIII` (Order of the Great Angelic Schema). | Repaired automatically by `attempt_deterministic_self_healing()`. |
| **73** | `p721–p730` | `2026-10-30T03:15:47Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Deity pronoun in `# PART XXIX` (Funeral Office for Monks). | Repaired automatically by `attempt_deterministic_self_healing()`. |
| **94** | `p931–p940` | `2026-10-30T07:16:34Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Deity pronoun in `# PART XXXIV` (Kneeling Prayers of Holy Pentecost). | Repaired automatically by `attempt_deterministic_self_healing()`. |
| **100** | `p991–p1000` | `2026-10-30T08:30:02Z` | Gate 1A (`lint_vocabulary.py`) | Forbidden vocabulary in `cohort100_footnotes.txt` (`Irmologion` -> `Heirmologion` in `[^2909]`, `[^2921]`; `Apolytikion` -> `Troparion` in `[^2937]`). | Repaired automatically by `attempt_deterministic_self_healing()` Step 3. |
| **101** | `p1001–p1010` | `2026-10-30T08:41:11Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Deity pronoun in `# PART XXXVII` (`Concerning Stauropegia`). | Repaired automatically by `attempt_deterministic_self_healing()`. |
| **106** | `p1051–p1060` | `2026-10-30T09:45:23Z` | Gate 2 (`hieratic_pronoun_audit.py`) | False-positive human pronoun flag on sacerdotal absolution formula (*"God... forgive thee"* / *"all the saints..."*), where `thee` refers to the human penitent. | Resolved by adding `'saints'` and `'forgive thee'` to `HUMAN_INDICATORS` in `scripts/hieratic_pronoun_audit.py`. |
| **134** | `p1331–p1340` | `2026-10-30T15:30:05Z` | Gate 2 (`hieratic_pronoun_audit.py`) | Uncapitalized Deity pronoun in `# PART LIV` (Nomocanon canonical penances). | Repaired automatically by `attempt_deterministic_self_healing()`. |

### 2.2 Latent Self-Healer Defects Discovered During Compiler Simulation (`heal_cohort_and_apparatus_text`)
When `UniversalPublicationEngine` (`scripts/compile_final_edition.py` Step 4 & Step 5) runs `heal_cohort_and_apparatus_text()` across all 141 cohorts (`32` draft files and `32` footnote files modified), empirical word-by-word diffing exposed **three critical deterministic healer defects**:

1. **Defect 2A — Naive `-eth` Stemmer Corrupts Silent-`e` / `-y` Verbs AND the Biblical Proper Noun `Aseneth` (`scripts/compile_final_edition.py`, `_convert_3rd_person_eth_token`, lines 359–435)**:
   - Because `work_order_template.md` Mandate 4 lists only 13 ceremonial rubrical `-eth` verbs (`singeth, proclaimeth, censeth...`), `Flash` subagents frequently use KJV/LXX `-eth` verbs inside **Scriptural quotations** (`John 6:56`, `1 Cor 13:4–8`, `Ps 90:1–6`, `Job 9:6–7`, `Nahum 1:4`) in both body text and footnotes (`167` total `-eth` tokens across 62 distinct word types).
   - When `heal_cohort_and_apparatus_text()` runs `_convert_3rd_person_eth_token()`, any token not in `NON_VERB_ETH_TOKENS` or `EXACT_ETH_VERB_MAP` has its last 3 characters (`eth`) stripped (`stem = wl[:-3]`) and `"s"` or `"es"` appended.
   - Across `1606_striatyn_balaban_trebnyk`, this naive stemmer **corrupted 12 English word types (17 total occurrences) into misspelled non-words**:
     - **Biblical Proper Noun Corruption**: `Aseneth` (Joseph's wife in the Marriage Service prayers, Cohorts 14 & 15, 3 occurrences: `Draft` Cohort 14 L182, Cohort 15 L26, `footnotes` Cohort 14 `[^199]`) $\rightarrow$ **`"Asens"`**!
     - **Silent-`e` Verb Corruptions**:
       - `believeth` (3x: Cohort 22 L105, Cohort 19 `[^288]`, Cohort 127 `[^3880]`) $\rightarrow$ **`"believs"`**
       - `cleaveth` (1x: Cohort 118 `[^3458]`) $\rightarrow$ **`"cleavs"`**
       - `forgiveth` (1x: Cohort 106 L13) $\rightarrow$ **`"forgivs"`**
       - `partaketh` (1x: Cohort 41 L30) $\rightarrow$ **`"partaks"`**
       - `rebuketh` (1x: Cohort 108 `[^3099]`) $\rightarrow$ **`"rebuks"`**
       - `removeth` (1x: Cohort 135 `[^4136]`) $\rightarrow$ **`"removs"`**
       - `rideth` (1x: Cohort 87 `[^2472]`) $\rightarrow$ **`"rids"`**
       - `wasteth` (1x: Cohort 48 `[^1419]`) $\rightarrow$ **`"wasts"`**
     - **`-ieth` Verb Corruptions**:
       - `drieth` (1x: Cohort 108 `[^3099]`) $\rightarrow$ **`"dris"`**
       - `trieth` (1x: Cohort 7 `[^108]`) $\rightarrow$ **`"tris"`**
     - **Double-`l` Verb Corruption**:
       - `compelleth` (1x: Cohort 114 L25) $\rightarrow$ **`"compells"`**
2. **Defect 2B — Vocabulary Self-Healer Creates Redundant Synonym Doubling (`(the Apodosis or Apodosis of Pascha)`) & Alters Meta-Linguistic Explanations in Footnotes**:
   - In Cohort 128 `[^3903]`, the subagent wrote `(the Apodosis or Leave-taking of Pascha)` to gloss the canonical term. The 1-to-1 regex replacement of `Leave-taking` $\rightarrow$ `Apodosis` turned this into `(the Apodosis or Apodosis of Pascha)`.
   - In Cohorts 30 (`[^732]`, `[^733]`), 33 (`[^902]`), 34 (`[^943]`), 80 (`[^2269]`), and 113 (`[^3249]`), the subagent wrote a philological note explaining why it avoided `"wherefore"` or `"wondrous"` (e.g., `rendered "for this cause" rather than "wherefore"`). Because `slop_map` in `heal_cohort_and_apparatus_text()` blindly replaces `"wherefore"` $\rightarrow$ `"therefore"` and `"wondrous"` $\rightarrow$ `"marvelous"` even inside quoted meta-commentary in footnotes, the footnote was mutated into `rendered "for this cause" rather than "therefore"`.
3. **Defect 2C — `work_order_template.md` Mandate 12 Induces Gate 1 Placeholder Violations on Blank Flyleaves**:
   - `work_order_template.md` Mandate 12 instructs workers to *"provide symmetric diplomatic descriptions in both `Source Text/` and `Draft/` on binding/engraving/frontispiece leaves so `SGC-02` length ratios remain within `[0.80, 1.50]`."*
   - On the 5 blank rear flyleaves (`p1394–p1398` in Cohort 140) and 2 internal blank versos (`p530` / Fol. 264v in Cohort 53; `p544` / Fol. 271v in Cohort 55), the `Flash` workers dutifully wrote `[Blank leaf: verso of the rear free flyleaf (verso of leaf p1394)...]` or `[Blank leaf — Fol. 264v][^1573]`.
   - These lines passed `run_small_pause_gate.py`, but in `verify_publication_edition.py` (`PLACEHOLDER_PATTERNS` line 36: `r"\*?\[Blank\s+[^\]]+\]\*?"`), they are flagged as **Gate 1 Failures (`Blank leaf indicator`)** because `compile_final_edition.py` failed to strip or convert them!

---

## 3. Argon Review Queue Signal Precision (`argon_review_queue.json`)

### 3.1 Signal Distribution Across All 1,401 Physical Leaves
At the conclusion of Phase 1, `Audit_Reports/argon_review_queue.json` contained exactly **`269` queued leaves** (`19.20%` of the 1,401-leaf codex) and **`0` unresolved quarantines**.

| Argon Queue Signal Category | Queued Leaf Count | % of Queue (`N = 269`) | % of Codex (`N = 1,401`) | Empirical Finding |
|---|---|---|---|---|
| **Signal 1: `epigraphic_uncertainty_marker`** (`[?]`, `[illegible]`, `[lacuna]`, `[damaged]`, `[corrupt]`) | **`0`** | `0.0%` | `0.0%` | Zero unresolved bracketed lacuna tags emitted in `Source Text/` or `Draft/`. |
| **Signal 2: `borderline_sgc02_ratio`** (`< 0.50` or `> 2.20` on non-sparse leaves) | **`0`** | `0.0%` | `0.0%` | `100%` of non-sparse leaves stayed within `[0.50, 2.20]` (codex mean `1.196`). |
| **Signal 3A: `complex_multicolumn_table`** (`>= 5` Markdown table rows) | **`0`** | `0.0%` | `0.0%` | Euchologion & TOC (`p1381–p1392`) were formatted as structured paragraphs/lists rather than Markdown pipe tables. |
| **Signal 3B: `dense_polyglot_apparatus`** (`>= 5` footnotes on 1 physical leaf) | **`269`** | **`100.0%`** | **`19.2%`** | **100% of the Argon review queue was triggered solely by `>= 5` footnotes on a single leaf.** |
| **Signal 4: `quarantined_gate_anomaly`** (`status == "QUARANTINED_FOR_ARGON"`) | **`0`** | `0.0%` | `0.0%` | Zero cohorts required quarantine; all 141 cohorts passed Small Pause Gates prior to promotion. |

### 3.2 Footnote Count Distribution & True Crux vs. False-Positive Noise Rate
Across the `269` leaves queued by `dense_polyglot_apparatus` (`>= 5` footnotes/leaf):

| Footnotes on Single Leaf | Queued Leaves (`N = 269`) | % of Queue | Cumulative Leaves If Threshold Raised |
|---|---|---|---|
| **5 footnotes** | `124` | `46.10%` | Threshold `>= 6` retains `145` leaves (`-46.1%` noise reduction) |
| **6 footnotes** | `78` | `29.00%` | Threshold `>= 7` retains `67` leaves (`-75.1%` noise reduction) |
| **7 footnotes** | `39` | `14.50%` | Threshold `>= 8` retains `28` leaves (`-89.6%` noise reduction) |
| **8 footnotes** | `17` | `6.32%` | Threshold `>= 9` retains `11` leaves (`-95.9%` noise reduction) |
| **9 footnotes** | `6` | `2.23%` | Threshold `>= 10` retains `5` leaves (`-98.1%` noise reduction) |
| **10 footnotes** | `4` | `1.49%` | Leaves `p282` (Coh 29), `p860` (Coh 86), `p1342` (Coh 135), `p1392` (Coh 140) |
| **12 footnotes** | `1` | `0.37%` | Leaf `p1391` (Coh 140, concluding TOC & errata) |

* **True Epigraphic / Codicological Crux Rate vs. Signal Noise**:
  * Auditing the footnote bodies and leaf text of all `269` queued leaves for genuine physical, typographical, or pagination cruxes (`missing folio`, `unnumbered leaf`, `cropped marginalia`, `printer's erratum`, `corrupt Slavonic syntax`) identified **only `4` genuine codicological/epigraphic crux leaves (`1.49%` precision)** inside the 269-leaf queue:
    1. `Leaf p407` (`Cohort 41`, 5 footnotes): Unnumbered printed leaf between Fol. 194 and Fol. 195 in the Communion prayers.
    2. `Leaf p1370` (`Cohort 137`, 5 footnotes): Textual ellipsis/variant in the Nomocanon abduction/adultery statutes (`Fol. 689v`).
    3. `Leaf p1391` (`Cohort 140`, 12 footnotes): Concluding Table of Contents (`Оглавленіе`) folio reference discrepancies against actual printed foliation.
    4. `Leaf p1392` (`Cohort 140`, 10 footnotes): Final printed leaf of the Table of Contents (`Fol. 699v`) with unfoliated colophon/index cross-references.
  * The remaining **`265` queued leaves (`98.51%` false-positive signal noise)** are completely clean, high-resolution printed leaves where the translator provided thorough Scriptural (`LXX`/`MT`), patristic (`St. Basil`, `John Jejunator`, `John of Kitros`), and Greek Euchologion (`Goar`) concordances (5–9 footnotes per page).

### 3.3 Genre Calibration Recommendation for Euchologion / Nomocanon Monuments
* In an Euchologion/Trebnyk with a Nomocanon appendix, every page contains multiple short prayers, psalm verses, or canonical rules, each requiring an LXX or patristic citation footnote. Consequently, `>= 5` footnotes/leaf is normal scholarly density (triggered on `19.2%` of the entire book) rather than an anomaly signal.
* **Calibration Fix**:
  1. Raise the `dense_polyglot_apparatus` threshold in `scripts/run_small_pause_gate.py` (line 182) from `>= 5` to **`>= 9` footnotes/leaf** for `euchologion`/`trebnyk`/`nomocanon` monuments (which reduces queue volume on `1606_striatyn_balaban_trebnyk` from `269` leaves to `11` leaves—a **`95.9%` reduction in false positives** while still capturing `p1391` and `p1392`), **OR**
  2. Trigger `dense_polyglot_apparatus` only when `len(fn_markers) >= 6` **AND** at least one footnote on the leaf matches an epigraphic/recensional crux keyword (`r"\b(?:sic|corrupt|misprint|errat|lacuna|illegible|damaged|variant|omits|unnumbered|missing)\b"`).

---

## 4. Monument-Type & Compiler Edge Cases (`compile_final_edition.py`)

Simulating Phase 2 compilation (`UniversalPublicationEngine` in `scripts/compile_final_edition.py`) and `scripts/verify_publication_edition.py` against all 141 cohorts of `1606_striatyn_balaban_trebnyk` (`657` mid-sentence page breaks stitched; `1,007,239` compiled body characters; `4,364 / 4,364` master footnotes) revealed **5 concrete compiler/verifier edge cases specific to 1-up Euchologion/Trebnyk codices**:

### Edge Case 4.1 — `universal_dynamic_h1` Captures Footnote Markers (`[^N]`) Inside `publication_spec` Part Titles & Duplicates 55 Footnotes into `Part 0` TOC
- **Mechanism**: Because `1606_striatyn_balaban_trebnyk` uses the Phase 0 `universal_dynamic_h1` scaffold (`self._is_scaffolded_pub_spec == True`), `UniversalPublicationEngine._slice_parts()` (`scripts/compile_final_edition.py`, lines 1011–1025) extracts every `# ...` line (`m_h1 = re.match(r"^#\s+([^\n#]+)$", line.strip())`) and sets `"title": h1_title` and `"start_landmark": rf"^#\s+{re.escape(h1_title)}$"`.
- **Friction**: In `1606_striatyn_balaban_trebnyk`, **55 of the 58 `# PART ...` H1 headings carry a trailing footnote marker** (e.g., `# PART III: THE ORDER OF THE CATECHUMENATE FOR THOSE WHO WISH TO BE BAPTIZED[^82]`).
  1. `_slice_parts()` stores the literal `[^82]` string inside `ps["title"]` in `codex_registry.json`.
  2. `_build_master_toc()` (lines 1249–1253) then writes `* **[PART III: ...[^82]](#part-iii-...)**` into `master_toc` and `part0_toc` (`note` that `_build_master_toc` strips `[^N]` from `H2` `sub_title` on line 1258 via `re.sub(r"\[\^\d+\]", "", m.group(1))`, but **forgets to strip `[^N]` from `H1` `title` on line 1249**!).
  3. Consequently, `part0` (`1606_striatyn_balaban_trebnyk_part0_front_matter.md`) inherits all 55 part-title footnote citations (`[^82]`..`[^4305]`) inside its Table of Contents, causing `format_footnotes_for_part()` to append 55 unrelated footnote definitions from Parts III–LVII into `Part 0`'s local `### Notes` block!

### Edge Case 4.2 — Unpurged Bracketed Running Headers (`273` Lines in Cohorts 5–33) Intercept 1-Up Mid-Sentence Seam Stitching
- **Mechanism**: Across Cohorts 5–33 (`p41–p330`), the `Flash` subagents transcribed the printed recto/verso running headers at the top of each leaf as bracketed metadata lines immediately below `=== LEAF pN ===`, e.g.:
  - `[Fol. 12r. Running header: Concerning Holy Baptism]`
  - `[Fol. 12v. Running header: Concerning the Canons]`
  - `[Fol. 15v. Decorative woodcut initial O.]`
- **Friction**: `is_explicit_leaf_marker(s)` in `scripts/compile_final_edition.py` (lines 66–92) recognizes `[Leaf p12]` and `Month — 180 — March`, but **does not recognize `^\[Fol\.\s*\d+[rv]?\.\s*Running\s+header:[^\]]+\]$`**.
  - As a result, when a prayer or rubric at the bottom of `Leaf p(N-1)` ends mid-sentence without terminal punctuation, `stitch_leaf_stream()` (lines 133–176) treats `[Fol. Xr. Running header: ...]` as the first content line of `Leaf pN` and **stitches the unfinished sentence of `Leaf p(N-1)` directly into `[Fol. Xr. Running header: ...]`**, leaving the actual continuation of the sentence disconnected on the next line!

### Edge Case 4.3 — Unpurged Inline Seam-Continuation Scaffolding (`92` Lines in Cohorts 127–138)
- **Mechanism**: In the rear liturgical orders and Nomocanon cohorts (`Cohorts 127–138`), `Flash` subagents inserted explicit mid-sentence continuation tags at the bottom and top of leaves:
  - Bottom of leaf: `... [continues onto leaf p1274][^3897]`, `... [continues onto leaf p1337][^4104]`
  - Top of next leaf: `**Priest (continued):** **"...`, `**Bishop / Hierarch (continued):** ...`
- **Friction**:
  1. Neither `is_explicit_leaf_marker()` nor `purge_scaffolding_and_stitch_seams()` strips `(?:\.\.\.\s*)?\[continues\s+onto\s+leaf\s+p?\d+\]` or leadingspeaker `(continued):` tags before running `stitch_leaf_stream()`.
  2. When `stitch_leaf_stream()` joins the two lines across the leaf boundary, `[continues onto leaf p1274]` remains embedded inside the compiled publication paragraph, and when the next leaf begins with `**Priest (continued):**`, `starts_dialogue` (line 144) prevents `stitch_leaf_stream()` from merging the split prayer at all!

### Edge Case 4.4 — `Blank leaf` & `Leaf N` Gate 1 False/True Collisions in `verify_publication_edition.py` (`8` Hits)
- **Mechanism**: In our full-monument compiler simulation, `verify_publication_edition.py` flagged exactly `8` Gate 1 placeholder hits across the 1,401-leaf compiled stream:
  1. **Footnoted Blank Leaves (`2` hits, Cohort 53 `p530` & Cohort 55 `p544`)**: `[Blank leaf — Fol. 264v][^1573]` and `[Blank leaf — Fol. 271v][^1597]`. Because `[^1573]` follows the closing bracket, `is_explicit_leaf_marker()` (`re.fullmatch(r"\*?\[Blank\s+[^\]]+\]\*?", s)`) failed to match it, leaving `[Blank leaf — Fol. 264v][^1573]` in the compiled text where `verify_publication_edition.py` (`re.search(r"\*?\[Blank\s+[^\]]+\]\*?")`) fails Gate 1. Furthermore, if `is_explicit_leaf_marker()` simply deleted the line, `[^1573]` and `[^1597]` would become **orphaned footnote definitions** and fail Gate 2!
  2. **Diplomatic Flyleaf Descriptions (`5` hits, Cohort 140 `p1394–p1398`)**: `[Blank leaf: verso of the rear free flyleaf (verso of leaf p1394). Without any manuscript or printed text...]` (written per Mandate 12 to satisfy `SGC-02` on rear flyleaves). Because they start with `[Blank leaf: ...]`, `verify_publication_edition.py` flags them as academic placeholders.
  3. **Tailpiece Description Mentioning `Leaf 1125` (`1` hit, Cohort 113 `p1125`)**: `*[Leaf 1125 concludes with a decorative woodcut tailpiece vignette of foliate scrollwork.]*` triggers `r"\[(?:Physical\s+Page\s+\d+\s*/\s*)?(?:Book\s+Page|Physical\s+Page|Leaf|Page)\s+\d+[^\]]*\]"`.

### Edge Case 4.5 — `format_liturgical_typography()` Double-Quotes Already-Bolded Spoken Prayers (`**Priest:** **"..."**`)
- **Mechanism**: In `scripts/compile_final_edition.py` (lines 317–325), `format_liturgical_typography()` matches `^(?:>\s*)?(?:The\s+)?(Priest|Deacon|...):\s*(.*)$`:
  ```python
  if rest.startswith('"') or rest.startswith('“') or rest.startswith('*'):
      line = f"> **{role}:** {rest}"
  ```
- **Friction**: When the subagent writes `**Priest:** "Peace be unto all."` (with `**Priest:**` already bolded), `m_dlg` (`r"^(?:>\s*)?(?:The\s+)?(Priest|...):\s*(.*)$"`) **does not match** because of the leading `**` before `Priest:`! Conversely, in `stitch_leaf_stream()` line 144, `starts_dialogue` *does* allow `(?:>\s*)?(?:\*\*)?`. Thus, `format_liturgical_typography()` misses all `1,195` bolded dialogue lines (`**Priest:**`, `**Deacon:**`, `**Choir:**`) in `1606_striatyn_balaban_trebnyk` and never converts them into `> **Role:**` blockquotes!

---

## 5. Granular Atomic Tagging Blueprint (Propers & Non-Propers)

To enable a universal atomic extractor (`scripts/extract_atomic_corpus.py`) to segment `100%` of `1606_striatyn_balaban_trebnyk` (`Cohorts/*.md`) into `1606_striatyn_balaban_trebnyk_atomic_corpus.json`, we inventoried every structural, hymnographic, euchological, and canonical unit class across all `141` cohorts (`3,243` discrete tagged atomic units):

### 5.1 Variable Propers Inventory (`710` Hymnographic & Lectionary Proper Units)

| Atomic Unit Class (`unit_type`) | Count in Codex | Exact Markdown / Regex Pattern in `Cohorts/*.md` | Representative Codex Witness |
|---|---|---|---|
| **`canon_ode_heirmos`** | `74` | `^\*Ode\s+([1-9])(?:,\s*Tone\s+[1-8])?[\.,]?\s*Heirmos\s*:?\*(?:\s*(.+))?$` | `*Ode 1, Tone 4. Heirmos:* Having crossed the depths of the Red Sea...` (`# PART XIII`, Unction Canon) |
| **`standalone_heirmos`** | `17` | `^\*Heirmos(?:\s*\([^\)]+\))?\s*:?\*(?:\s*(.+))?$` | `*Heirmos:* Dry land appeared, and the sea was divided...` (`# PART XXIX`, Monastic Burial) |
| **`canon_troparion`** | `382` | `^\*(?:Troparion|Another\s+Troparion|Refrain)\s*[^*\n]*:\*(?:\s*(.+))?$` | `*Troparion:* Having Thy mercy, O Master, filling all the earth...` (`# PART XIII`, `p173`) |
| **`theotokion_stavrotheotokion`** | `133` | `^\*(?:Theotokion|Stavrotheotokion|Another\s+Theotokion)\s*[^*\n]*:\*(?:\s*(.+))?$` | `*Theotokion:* O pure and unwedded Virgin, who alone didst bring forth...` (`# PART XLIII`, Pestilence Canon) |
| **`sticheron_idiomelon_prosomoion`** | `43` | `^\*(?:Sticher(?:a|on)|Idiomel(?:a|on)|Another\s+Sticheron|Tone\s+[1-8],\s*Podoben)\s*[^*\n]*:\*(?:\s*(.+))?$` | `*Tone 6, Podoben: "Having set all your hope" (Всѧ̀ ѿложи́вше):*` (`# PART XXI`, Burial) |
| **`prokeimenon_alleluia`** | `32` | `^\*(?:Prokeimenon|Alleluia)\s*[^*\n]*:\*(?:\s*(.+))?$` | `*Prokeimenon, Tone 1:* Let Thy mercy, O Lord, be upon us...` (`# PART XIII`, Unction) |
| **`kontakion`** | `18` | `^\*Kontakion\s*[^*\n]*:\*(?:\s*(.+))?$` | `*Kontakion, Tone 8:* With the saints give rest, O Christ, to the souls...` (`# PART XXI`, Burial) |
| **`ikos`** | `5` | `^\*Ikos\s*[^*\n]*:\*(?:\s*(.+))?$` | `*Ikos:* Thou Thyself alone art immortal, Who hast created and fashioned man...` (`# PART XXI`, Burial) |
| **`sessional_hymn`** | `5` | `^\*Sessional\s+Hymn\s*[^*\n]*:\*(?:\s*(.+))?$` | `*Sessional Hymn, Tone 6:* Truly all things are vanity, and life is but a shadow...` (`# PART XXI`, Burial) |
| **`exapostilarion`** | `1` | `^\*(?:Exapostilarion|Hymn\s+of\s+Light)\s*[^*\n]*:\*(?:\s*(.+))?$` | `*Exapostilarion:* Now Have I found a haven...` (`# PART XXIX`, Monastic Funeral) |

### 5.2 Fixed Non-Propers Inventory (`2,533` Euchological, Rubrical & Canonical Units)

| Atomic Unit Class (`unit_type`) | Count in Codex | Exact Markdown / Regex Pattern in `Cohorts/*.md` | Representative Codex Witness |
|---|---|---|---|
| **`h1_part_landmark`** | `58` | `^#\s+(PREFACE:\s+TO\s+THE\s+READER|PART\s+[IVXLCDM]+:\s+.+?)(?:\[\^\d+\])?$` | `# PART IV: THE ORDER OF HOLY BAPTISM[^101]` (`Cohort 7`, `p64`) |
| **`sacerdotal_prayer_rubric_header`** | `161` | `^\*(?:Prayer\b|Another\s+Prayer\b|The\s+Priest\s+prays|Prayer\s+over|Prayer\s+of|Exorcism\b)[^*\n]*\*` | `*Prayer of the First Hour of the Catechumenate:*` / `*First Exorcism:*` (`# PART III`) |
| **`dialogue_priest_speech`** | `506` | `^(?:>\s*)?\*\*Priest(?:\s*\([^\)]+\))?:\*\*\s*(.+)$` | `**Priest:** Blessed is the Kingdom of the Father, and of the Son, and of the Holy Spirit...` |
| **`dialogue_deacon_speech`** | `282` | `^(?:>\s*)?\*\*Deacon(?:\s*\([^\)]+\))?:\*\*\s*(.+)$` | `**Deacon:** In peace, let us pray to the Lord.` |
| **`dialogue_choir_reader_response`** | `407` | `^(?:>\s*)?\*\*(?:Choir|Reader|People|Chanter|Clergy|Bishop\s*/\s*Hierarch|Sponsor|Catechumen|Question|Answer)(?:\s*\([^\)]+\))?:\*\*\s*(.+)$` | `**Choir:** Lord, have mercy.` / `**Reader:** Psalm 50.` |
| **`litany_block`** | `64` | `\b(?:In\s+peace,\s+let\s+us\s+pray\s+to\s+the\s+Lord|Have\s+mercy\s+on\s+us,\s+O\s+God,\s+according\s+to\s+Thy\s+great\s+mercy|Again\s+we\s+pray\s+for)\b` | Great Synaptē, Augmented Litany (`Сугубая`), and Litany for the Departed across Parts I–XLIX |
| **`ecphonesis_exclamation`** | `56` | `\bFor\s+(?:unto\s+Thee\s+is\s+due\s+all\s+glory|Thine\s+is\s+the\s+kingdom|Thou\s+art\s+a\s+merciful\s+and\s+man-befriending\s+God|Thou\s+art\s+the\s+sanctification|Thou\s+art\s+He\s+that\s+blesses)\b` | Sacerdotal doxological exclamations concluding secret and aloud prayers |
| **`sacramental_declarative_formula`** | `16` | `\b(?:The\s+servant\s+of\s+God\s+\[?N\.\]?[,]?\s+is\s+(?:baptized|betrothed|crowned|shorn)|The\s+seal\s+of\s+the\s+gift\s+of\s+the\s+Holy\s+Spirit|forgive\s+and\s+absolve)\b` | Baptismal immersion (`p77`), Chrismation (`p80`), Betrothal (`p125`), Crowning (`p138`), Absolution (`p296`) |
| **`psalm_heading_or_stichos`** | `76` | `^\*(?:Psalm\s+\d+|Verse\s*:?)[^*\n]*\*` | `*Psalm 50:* Have mercy on me, O God...` / `*Psalm 90:* He that dwells in the help of the Most High...` |
| **`lectionary_epistle_gospel`** | `16` | `^\*(?:The\s+Reading\s+is\s+from|The\s+Holy\s+Gospel\s+according\s+to|Gospel\s+according\s+to|Epistle\s+of)[^*\n]*\*` | Seven Epistle & Seven Gospel pericopes in `# PART XIII` (Holy Unction), Marriage, Baptism, Burial |
| **`nomocanon_section_or_canon_rubric`** | `299` | `^\*(?:\d+\.\s*)?(?:Concerning\s+[^*\n]+|Of\s+the\s+Holy\s+Fathers|Injunctions|Statute|Canon\s+\d+[^*\n]*|Degree\s+[^*\n]*):\*(?:\[\^\d+\])?$` | `*Of the Holy Fathers:*`, `*Injunctions:*`, `*18. Concerning Relatives by Marriage:*[^3981]` (`Cohorts 128–138`) |
| **`procedural_rubric_paragraph`** | `592` | `^\*(?!(?:Ode|Heirmos|Troparion|Theotokion|Stavrotheotokion|Kontakion|Ikos|Sessional|Sticher|Idiomel|Exapostilarion|Prokeimenon|Alleluia|Psalm|Verse|Prayer|Exorcism|Concerning|Of the Holy Fathers|Injunctions|Statute))[^*\n]{15,}\*(?:\[\^\d+\])?$` | Ceremonial and rubrical instructions printed in red cinnabar (`*Then the Priest takes the infant...*`) |

---

## 6. Top 5 Concrete Engine Hardening Recommendations

Based on the empirical evidence collected across `1606_striatyn_balaban_trebnyk`, we rank the top 5 highest-leverage code and template changes for the cross-wave System Hardening Implementation Plan:

### Rank 1 (CRITICAL — Prevents Word & Biblical Proper Noun Corruption in Compiled Text)
- **Target**: `scripts/compile_final_edition.py` $\rightarrow$ `NON_VERB_ETH_TOKENS` (line 359), `EXACT_ETH_VERB_MAP` (line 366), and `_convert_3rd_person_eth_token()` (lines 421–435).
- **Empirical Evidence**: In `1606_striatyn_balaban_trebnyk`, `_convert_3rd_person_eth_token()` stripped `-eth` and appended `-s` to 12 word types (17 occurrences), corrupting the biblical proper noun **`Aseneth`** into **`"Asens"`** (3x in Cohorts 14–15) and turning silent-`e` / `-y` / `-ll` verbs into misspelled non-words (**`believs`**, **`cleavs`**, **`forgivs`**, **`partaks`**, **`rebuks`**, **`removs`**, **`rids`**, **`wasts`**, **`dris`**, **`tris`**, **`compells`**).
- **Actionable Fix**:
  1. Add biblical/liturgical proper nouns ending in `-eth` to `NON_VERB_ETH_TOKENS` (and `NON_VERB_ETH_SET` in `scripts/verify_publication_edition.py`): `"aseneth"`, `"japheth"`, `"mephibosheth"`, `"ishbosheth"`, `"gath"`, `"sabbath"`.
  2. Expand `EXACT_ETH_VERB_MAP` with all silent-`e`, `-ieth`, and double-consonant verbs (`believeth -> believes`, `cleaveth -> cleaves`, `forgiveth -> forgives`, `partaketh -> partakes`, `rebuketh -> rebukes`, `removeth -> removes`, `rideth -> rides`, `wasteth -> wastes`, `drieth -> dries`, `trieth -> tries`, `compelleth -> compels`), **AND** replace the fallback stemmer rule in `_convert_3rd_person_eth_token()` so that:
     - If `wl.endswith("ieth")`: `mod = wl[:-4] + "ies"` (fixes `drieth -> dries`, `trieth -> tries`).
     - If `stem.endswith("ll")`: `mod = stem[:-1] + "ls"` when preceded by a multi-syllable prefix (`compelleth -> compels`, `expelleth -> expels`).
     - If `stem` ends in `v` (`believ`, `cleav`, `forgiv`, `remov`) or `C + V + C` where modern English requires silent `e` (`rebuk`, `partak`, `rid`, `wast`): `mod = stem + "es"`.

### Rank 2 (HIGH — Eliminates 55 Duplicated Footnotes in `Part 0` TOC & Dynamic `publication_spec` Titles)
- **Target**: `scripts/compile_final_edition.py` $\rightarrow$ `UniversalPublicationEngine._slice_parts()` (lines 1011–1025) and `_build_master_toc()` (lines 1247–1253).
- **Empirical Evidence**: In `universal_dynamic_h1` mode, 55 of the 58 `# PART ...` H1 headings in `1606_striatyn_balaban_trebnyk` carry trailing footnote markers (`# PART III: ...[^82]`). Because `_slice_parts()` stores the raw `h1_title` (with `[^82]`) into `ps["title"]` and `_build_master_toc()` does not strip `\[\^\d+\]` from `ps["title"]`, all 55 part-heading footnotes are duplicated into the `Part 0` and Master Table of Contents links, polluting `part0_front_matter.md` with 55 foreign footnote definitions.
- **Actionable Fix**:
  1. In `_slice_parts()` (line 1013), strip `\[\^\d+\]` from `clean_h1_title = re.sub(r"\s*\[\^\d+\]", "", h1_title).strip()` before storing `"title": clean_h1_title`, and set `"start_landmark": rf"^#\s+{re.escape(clean_h1_title)}(?:\s*\[\^\d+\])*$"`.
  2. In `_build_master_toc()` (line 1249), strip `\[\^\d+\]` from `title = re.sub(r"\[\^\d+\]", "", ps["title"]).strip()` just as line 1258 already does for `H2` `sub_title`.

### Rank 3 (HIGH — Purges 273 Bracketed Running Headers, 92 Inline `[continues onto leaf...]` Tags & 7 `[Blank leaf...]` Collisions Before Seam Stitching)
- **Target**: `scripts/compile_final_edition.py` $\rightarrow$ `is_explicit_leaf_marker()` (lines 66–92), `stitch_leaf_stream()` (lines 111–176), and `purge_scaffolding_and_stitch_seams()` (lines 200–292).
- **Empirical Evidence**:
  - `273` `[Fol. Xr. Running header: ...]` lines in Cohorts 5–33 were not recognized by `is_explicit_leaf_marker()`, intercepting mid-sentence page breaks during `stitch_leaf_stream()`.
  - `92` inline `... [continues onto leaf pN]` and `**Role (continued):**` markers in Cohorts 127–138 survived into the compiled text or blocked mid-prayer seam stitching.
  - `8` lines (`2` `[Blank leaf — Fol. Xv][^N]` lines, `5` `[Blank leaf: verso of the rear free flyleaf...]` diplomatic flyleaf descriptions from Cohort 140, and `1` `*[Leaf 1125 concludes with a decorative woodcut tailpiece...]*` note) triggered Gate 1 failures in `verify_publication_edition.py`.
- **Actionable Fix**:
  1. In `purge_scaffolding_and_stitch_seams()`, pre-strip inline `(?:\.\.\.\s*)?\[(?:continues\s+onto|continued\s+from)\s+(?:leaf|page|fol\.)\s+[^\]]+\]` and merge split speaker continuations (`^\*\*(?:Priest|Deacon|Bishop\s*/\s*Hierarch)\s*\(continued\):\*\*\s*(?:"|“)?(?:\.\.\.)?`) across leaf breaks.
  2. In `is_explicit_leaf_marker(s)`, add `^\[Fol\.\s*\d+[rv]?\.\s*Running\s+header:[^\]]+\]$`.
  3. For `[Blank leaf ...][^N]` (with a footnote citation) and diplomatic flyleaf descriptions (`[Blank leaf: ...]`), convert `[Blank leaf — Fol. Xv][^N]` into `*[Fol. Xv — Vacat]*[^N]` and `[Blank leaf: <description>]` into `*[Flyleaf — <description>]*` (and `[Leaf 1125 concludes...]` into `*[Folio concludes...]*`) so that zero footnotes are orphaned (`Gate 2` preserved) while zero `Blank leaf` / `Leaf N` placeholder patterns fire in `verify_publication_edition.py` (`Gate 1` 100% clean).

### Rank 4 (MEDIUM-HIGH — Recalibrates Argon Review Queue Signal 3B to Eliminate 98.5% False-Positive Noise on Euchologion/Nomocanon Monuments)
- **Target**: `scripts/run_small_pause_gate.py` $\rightarrow$ `collect_argon_review_signals()` (lines 173–184).
- **Empirical Evidence**: `269 / 269` (`100%`) of the leaves queued in `argon_review_queue.json` for `1606_striatyn_balaban_trebnyk` were triggered solely by `dense_polyglot_apparatus: >= 5 footnotes on leaf`, of which `265` (`98.51%`) were normal scholarly Euchologion/Nomocanon apparatus notes and only `4` (`1.49%`) involved genuine codicological/pagination cruxes.
- **Actionable Fix**:
  - Parameterize the footnote density threshold by genre or raise the flat threshold from `>= 5` to **`>= 9` footnotes/leaf** (reducing `1606_striatyn_balaban_trebnyk`'s queue from `269` to `11` leaves, a `95.9%` noise reduction), while adding a dedicated Signal 1B regex that scans each leaf's corresponding footnote definitions in `cohortN_footnotes.txt` for explicit codicological/epigraphic crux tokens (`r"\b(?:unnumbered|missing\s+folio|pagination\s+error|misprint|erratum|corrupt|lacuna|cropped|damaged)\b"`).

### Rank 5 (MEDIUM — Aligns `format_liturgical_typography()` Dialogue Regex & `work_order_template.md` Guardrails)
- **Target**: `scripts/compile_final_edition.py` $\rightarrow$ `format_liturgical_typography()` (line 317) and `data/templates/work_order_template.md` (Mandates 4, 8, and 12).
- **Empirical Evidence**:
  1. `work_order_template.md` Mandate 10 instructs subagents to format speaker labels in bold (`**Priest:**`, `**Deacon:**`, `**Reader:**`, `**Choir:**`), which the subagents followed `1,195` times across `1606_striatyn_balaban_trebnyk`. However, `format_liturgical_typography()` line 317 uses `r"^(?:>\s*)?(?:The\s+)?(" + roles + r"):\s*(.*)$"`, which fails to match when `**` surrounds the role name!
  2. `work_order_template.md` Mandate 4 bans 13 rubrical `-eth` verbs (`singeth, proclaimeth...`) but does not explicitly tell workers to modernize `-eth` verbs inside **Scriptural quotations and footnotes** (`eateth, drinketh, dwelleth, cometh, maketh`), which accounted for `92%` of all `-eth` tokens healed during compilation.
  3. `work_order_template.md` Mandate 12 tells workers to write diplomatic descriptions on blank flyleaves, without warning that `[Blank leaf: ...]` triggers Gate 1 in `verify_publication_edition.py`.
- **Actionable Fix**:
  1. Update `format_liturgical_typography()` line 317 to `r"^(?:>\s*)?(?:\*\*)?(?:The\s+)?(" + roles + r")(?:\s*\([^\)]+\))?:(?:\*\*)?\s*(.*)$"` (matching `stitch_leaf_stream()` line 144).
  2. Update `data/templates/work_order_template.md` Mandate 4 to explicitly ban 3rd-person `-eth` verbs in **both Scriptural quotations and footnotes** (`eateth -> eats`, `drinketh -> drinks`, `dwelleth -> dwells`, `cometh -> comes`, `maketh -> makes`), and update Mandate 12 to prescribe `*[Flyleaf / Vacat: <diplomatic description>]*` instead of `[Blank leaf: ...]`.
