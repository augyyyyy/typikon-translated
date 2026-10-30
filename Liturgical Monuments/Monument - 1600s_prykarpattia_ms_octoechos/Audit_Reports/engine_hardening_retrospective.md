# Post-Run Engine Hardening Retrospective: 17th-Century Carpathian-Galician Manuscript Octoechos (`1600s_prykarpattia_ms_octoechos`)

**Monument ID:** `1600s_prykarpattia_ms_octoechos`  
**Title:** 17th-Century Carpathian-Galician Manuscript Octoechos (*Октоїх рукописний, Прикарпаття, XVII ст.*, Dovhopole Dedication 1707 AD, Accession `МКДУ 13962 СД-319`)  
**Physical Span:** 222 leaves (`p1`–`p222`) across 23 translation cohorts  
**Total Slavonic Source Words:** 57,985  
**Total English Words (`Cohorts/` / `complete.md`):** 94,689 / 88,262  
**Master Footnotes (`_footnotes.md`):** 236 (100% bijective symmetry)  
**Extracted Propers Corpus (`_propers_corpus.json`):** 3,125 items  
**Attested Podoben Invocations (`_podoben_grid.json`):** 20 invocations across 5 Tones (`[1, 3, 4, 6, 8]`)  
**Hymnographic Normalization Drift Events (`_drift_ledger.json`):** 110 events  

---

## 1. Cohort Velocity & Bottleneck Autopsy

### 1.1 Complete 23-Cohort Empirical Telemetry Table

Wall-clock subagent durations were extracted directly from the `invoke_subagent` $\rightarrow$ `SYSTEM_MESSAGE` timestamps in `transcript_full.jsonl`, paired with `Work_Orders/` vs. `Audit_Reports/cohort*_small_pause_report.json` filesystem timestamps and internal subagent transcript step/tool counts.

| Cohort | Physical Leaves | Subagent ID | Subagent Wall-Clock (s / min) | Full Gate Cycle (s) | Slavonic Words | English Words | Footnotes | Subagent Steps | Shell Cmds (`run_command`) | File Edits (`edit_file`) | Liturgical & Codicological Scope |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **C01** | `p1`–`p10` | `c6aadf90` | 1,062.0s (17.7m) | 1,075.9s | 1,365 | 2,074 | 13 | 126 | 34 | 0 | Front binding, 1707 Dovhopole dedication (`p3`), Table of Tones (`p4`), Resurrection miniature (`p6`), `# TONE 1` Sat. Vespers |
| **C02** | `p11`–`p20` | `3ec4a55a` | 900.0s (15.0m) | 915.8s | 2,513 | 3,878 | 17 | 56 | 5 | 0 | Tone 1 Sun. Matins Sessional Hymns, Gradual Antiphons, Resurrection/Cross-Resurrection/Theotokos Canons |
| **C03** | `p21`–`p30` | `6d8e044d` | 835.0s (13.9m) | 851.0s | 2,642 | 3,874 | 13 | 64 | 5 | 1 | Tone 1 Praises & Beatitudes; `# TONE 2` (`p24`, `fol. 19r`) Sat. Vespers & Sun. Matins Odes 1–6 |
| **C04** | `p31`–`p40` | `3a4b580b` | 866.0s (14.4m) | 880.1s | 2,565 | 3,940 | 11 | 67 | 9 | 0 | Tone 2 Sun. Matins Odes 6–9, Praises, Beatitudes |
| **C05** | `p41`–`p50` | `41c5165d` | 738.0s (12.3m) | 750.9s | 2,340 | 3,578 | 10 | 72 | 9 | 1 | `# TONE 3 (fol. 37)` (`p42`) ornamental headpiece, Sat. Vespers, Sun. Matins Odes 1–5 |
| **C06** | `p51`–`p60` | `13fb8987` | 1,019.0s (17.0m) | 1,036.9s | 2,555 | 4,029 | 10 | 82 | 9 | 0 | Tone 3 Odes 5–9, Praises, Beatitudes; `# TONE 4 (fol. 54)` (`p59`) Sat. Vespers |
| **C07** | `p61`–`p70` | `a044e9d0` | 796.0s (13.3m) | 807.4s | 2,515 | 3,797 | 10 | 57 | 7 | 0 | Tone 4 Aposticha, Sun. Matins Sessional Hymns, Gradual Antiphons, Canons Odes 1–7 |
| **C08** | `p71`–`p80` | `e7e1588c` | 879.0s (14.7m) | 894.5s | 2,479 | 3,784 | 10 | 78 | 12 | 3 | Tone 4 Odes 7–9, Praises, Beatitudes; `# TONE 5` (`p76`, `fol. 71r`) Sat. Vespers & Sun. Matins Ode 1 |
| **C09** | `p81`–`p90` | `b2bbc9fa` | 837.0s (13.9m) | 848.4s | 2,649 | 4,268 | 10 | 70 | 9 | 0 | Tone 5 Sun. Matins Canons Odes 1–9, Praises |
| **C10** | `p91`–`p100` | `b162b7de` | 1,041.0s (17.4m) | 1,055.6s | 2,673 | 4,042 | 10 | 94 | 17 | 0 | Tone 5 Beatitudes; `# TONE 6` (`p92`, `fol. 87r`) Sat. Vespers & Sun. Matins Canons Odes 1–6 |
| **C11** | `p101`–`p110` | `6416f7c4` | 1,383.0s (23.1m) | 1,401.7s | 2,655 | 4,082 | 10 | 101 | 18 | 0 | Tone 6 Odes 6–9, Praises, Beatitudes; `# TONE 7` (`p109`, `fol. 103r`, paper repair patch over headpiece) |
| **C12** | `p111`–`p120` | `0fdedb8f` | 910.0s (15.2m) | 922.0s | 2,634 | 3,983 | 10 | 68 | 7 | 0 | Tone 7 Sun. Matins Canons Odes 1–8 |
| **C13** | `p121`–`p130` | `45a364d1` | 790.0s (13.2m) | 810.0s | 2,572 | 3,948 | 10 | 70 | 7 | 1 | Tone 7 Ode 9, Praises, Beatitudes; `# TONE 8` (`p125`, `fol. 119r`) Sat. Vespers & Sun. Matins Odes 1–3 |
| **C14** | `p131`–`p140` | `faf0cc7f` | 1,042.0s (17.4m) | 1,055.7s | 2,471 | 3,855 | 10 | 83 | 14 | 2 | Tone 8 Sun. Matins Canons Odes 3–9, Praises, Beatitudes |
| **C15** | `p141`–`p150` | `a2bc868f` | 1,029.0s (17.1m) | 1,043.2s | 2,740 | 4,120 | 10 | 72 | 7 | 0 | Weekday Octoechos Cycle begins (Mon.–Sat. Vespers/Matins propers & Canons, Tone 1–2) |
| **C16** | `p151`–`p160` | `8a16a9ce` | 1,039.0s (17.3m) | 1,054.0s* | 2,791 | 4,230 | 10 | 75 | 10 | 4 | Weekday Octoechos Cycle (Tones 2–3 Weekday Canons, Stichera, Lectionary pericopes) |
| **C17** | `p161`–`p170` | `adc17477` | 1,392.0s (23.2m) | 1,408.5s | 3,073 | 4,703 | 10 | 133 | 35 | 0 | Weekday Octoechos Cycle (`p164` & `p165` duplicate exposure of `fols. 159v–160r`) |
| **C18** | `p171`–`p180` | `947a2bcb` | 1,371.0s (22.9m) | 1,392.4s | 3,092 | 5,076 | 10 | 92 | 18 | 4 | Weekday Octoechos Cycle (Tones 4–5 Weekday Canons, Epistle/Gospel readings; peak English word count) |
| **C19** | `p181`–`p190` | `f721e451` | 1,123.0s (18.7m) | 1,144.1s | 3,079 | 4,739 | 10 | 102 | 19 | 3 | Weekday Octoechos Cycle (Tones 5–6 Weekday Canons & Stichera) |
| **C20** | `p191`–`p200` | `f6823323` | 1,184.0s (19.7m) | 1,199.0s* | 3,216 | 5,035 | 10 | 83 | 18 | 0 | Weekday Octoechos Cycle (Tones 6–7 Weekday Canons; peak Slavonic word count: 3,216 words) |
| **C21** | `p201`–`p210` | `51b39937` | 1,285.0s (21.4m) | 1,304.7s | 2,911 | 4,701 | 10 | 96 | 22 | 0 | Weekday Octoechos Cycle (Tone 8 Weekday Canons, Martyr/Departed Stichera) |
| **C22** | `p211`–`p220` | `8e833ebc` | 889.0s (14.8m) | 909.4s | 2,351 | 3,273 | 10 | 72 | 12 | 0 | `# EXAPOSTILARIA AND EVANGELICAL STICHERA` (`p212`): 11 Eothina, Gregory of Sinai Triadica (`p218`), rear flyleaf (`p220`) |
| **C23** | `p221`–`p222` | `43f0b797` | 183.0s (3.0m) | 190.9s | 113 | 141 | 2 | 44 | 1 | 0 | Rear calfskin binding board with Golgotha Cross medallion (`p221`) and spine (`p222`) |
| **TOTAL** | **222 leaves** | **23 workers** | **23,313.0s (388.6m)** | **23,661.3s** | **57,985** | **88,262** | **236** | **1,857** | **304** | **19** | **Mean: 1,013.6s (16.9m) / cohort** |

*\*Note on `cohort16_small_pause_report.json` and `cohort20_small_pause_report.json` filesystem `mtime`s: During Cohort 17 (`step 78`) and Cohort 21 (`step 71`), the respective `Flash` subagents executed `python scripts/run_small_pause_gate.py --cohort 16` and `--cohort 20` on the preceding cohort before running their own cohort number, shifting the on-disk report `mtime`s by `+514.7s` and `+775.1s` respectively.*

### 1.2 Autopsy of the 3 Slowest Cohorts

1. **Rank #1 Slowest — Cohort 17 (`1,392.0s / 23.2 min`, `p161`–`p170`, 133 steps, 35 shell commands, 4,703 English words)**:
   - **Codicological & Visual Bottleneck**: Physical leaves `p164` (`Page_0164.jpg`) and `p165` (`Page_0165.jpg`) are **duplicate photographic exposures** of the exact same manuscript opening (`folios 159v–160r`).
   - **Prompt & Tooling Bottleneck**: Upon discovering that `Page_0165.jpg` duplicated `Page_0164.jpg`, the `Flash` worker executed **20+ exploratory shell commands** (`steps 21..96`: `Get-FileHash`, `PIL.ImageChops` pixel difference checks, `git log -S duplicate`, and grepping `SPARSE_EXEMPT_KEYWORDS` in `scripts/run_small_pause_gate.py`) to determine how to populate `=== LEAF p165 ===` without triggering an `SGC-02` draft-to-source length ratio violation or duplicating liturgical stanzas in the compiled edition.
   - **Script Density**: Beyond `p165`, the remaining 9 leaves belong to the compressed Weekday Octoechos section (`33–35` lines/page of smaller semi-uncial hand), yielding `3,073` Slavonic words (`4,703` English words).

2. **Rank #2 Slowest — Cohort 11 (`1,383.0s / 23.1 min`, `p101`–`p110`, 101 steps, 18 shell commands, 4,082 English words)**:
   - **Codicological & Visual Bottleneck**: On `p109` (`fol. 103r`, the opening of `# TONE 7`), an antique **paper repair patch** is pasted directly across the upper margin and ornamental headpiece, partially obscuring the opening Slavonic lines.
   - **Prompt & Tooling Bottleneck**: The subagent spent **12 shell commands** (`steps 33..70`) cropping the damaged header region with `PIL.Image` (`crop_p109_patch.jpg`) and running Python scripts to search parallel Octoechos workspaces (`1629_kyiv_octoechos` and `1895_lviv_octoechos`) to reconstruct the covered lines philologically (`[...]` with footnote apparatus). Several of these ad-hoc `python -c` commands crashed on Windows `cp1252` stdout (`UnicodeEncodeError`) before the subagent added `sys.stdout.reconfigure(encoding='utf-8')`.

3. **Rank #3 Slowest — Cohort 18 (`1,371.0s / 22.9 min`, `p171`–`p180`, 92 steps, 18 shell commands, 4 file edits, 5,076 English words)**:
   - **Codicological Density**: Cohort 18 had the **highest English word volume in the entire codex** (`5,076` English words from `3,092` Slavonic words across 10 dense weekday leaves containing Tone 4–5 Weekday Canons, Stichera, and Lectionary Epistle/Gospel pericopes).
   - **Linter Repair Loop**: First-pass execution of `scripts/lint_liturgical_slop.py` (`step 59`) failed with **4 `pseudo_archaic_slop` violations** (`'wherefore'` on lines 229, 343, 400 and `'Hearken'` in `Ps. 44:11` on line 349), requiring 4 sequential `edit_file` calls (`steps 61..67`) and re-execution of the individual linters (`steps 69..87`).
   - **Exploratory Registry Queries**: The subagent also spent 7 shell commands (`steps 31..51`) inspecting `codex_registry.json` and `data/liturgical_primitives_registry.json` (hitting `UnicodeEncodeError` twice).

---

## 2. Small Pause Gate, Deterministic Self-Healing & Flash Failure Modes

### 2.1 Complete Catalog of Anomalies Caught or Healed Across Phase 1 & Phase 2

| Stage & Gate / Mechanism | Affected Cohorts | Occurrences | Exact Empirical Anomaly & Resolution |
| :--- | :--- | :---: | :--- |
| **Phase 1: Gate 1A (`Shared_Lexicon/lint_vocabulary.py`)** | `C03` | 1 | Caught forbidden Graecism `*Resurrection Apolytikion, Tone 2:*` on `C03:L190`; subagent replaced with `*Resurrection Troparion, Tone 2:*`. |
| **Phase 1: Gate 1B (`scripts/lint_liturgical_slop.py` — `pseudo_archaic_slop`)** | `C18`, `C19` | 7 | Caught `'wherefore'` / `'Wherefore'` (`C18:L229, L343, L400`; `C19:L150, L273, L343`) and `'Hearken'` in `Ps. 44:11` (`C18:L349`). Subagents manually replaced with `'therefore'` and `'Give ear'`. |
| **Phase 1: Gate 1B (`scripts/lint_liturgical_slop.py` — `archaic_rubrical_verb_drift`)** | `C08`, `C16` | 5 | Caught `'maketh'` (`C16:L204`) and `'taketh'` (`C16:L240, L274`), plus subagent self-edits on `'becometh'` (`C08:L43`) and `'granteth'` (`C16:L240`). **Crucially, `lint_liturgical_slop.py` missed 31 other 3rd-person `-eth` verbs across 10 cohorts (see below).** |
| **Phase 1: Gate 2 (`scripts/hieratic_pronoun_audit.py`)** | `C05`, `C08`, `C13`, `C14` | 6 (All False Positives) | Proximity regex (`deity_terms` within 120 chars of lowercase `thou/thee/thy/thine/he/him/his`) triggered 6 false positives on pronouns referring to **Satan/the enemy** (`C08:L80` `'the Almighty Lord, crushing him'` $\rightarrow$ rewritten as `'crushing the adversary'`; `C14:L108` `'hoping in Thee, O Lord, I vanquish him!'` $\rightarrow$ rewritten as `'I vanquish the enemy!'`), **Christ's Tomb** (`C05:L305` `'worship thee, O Life-Giving Tomb; for Christ, truly our God'` $\rightarrow$ capitalized `'Thee'`), and **the Theotokos** (`C08:L281` `'thy warm protection... Mother of the Most High God'` $\rightarrow$ reordered to `'Mother of God, the Most High'`; `C13:L111` `'O Birthgiver of God; thou bearest in thine arms'` $\rightarrow$ hyphenated `'Birth-giver'` to evade regex). |
| **Phase 1: Gate 1C (`scripts/chromatic_rubric_verifier.py`)** | `C01`–`C23` | 222 leaves checked | Emitted non-blocking warnings on flyleaves, binding boards (`p1–p2`, `p221–p222`), and oxidized/darkened cinnabar rubrics; 0 blocking failures. |
| **Phase 2: Compiler Step 3 (`heal_cohort_and_apparatus_text()` in `scripts/compile_final_edition.py`)** | `C01, C03, C04, C05, C10, C12, C13, C16, C18, C20` (10 cohorts) | 31 tokens across 24 lines | Healed 31 residual 3rd-person `-eth` verbs that `lint_liturgical_slop.py` failed to flag during Phase 1: `becometh` $\rightarrow$ `becomes` (5x: `C01:L82, C03:L180, C05:L57, C10:L114, C12:L28`), `rejecteth` $\rightarrow$ `rejects` (4x: `C16:L215`), `rejoiceth` $\rightarrow$ `rejoices` (2x: `C04:L219, L222`), `hymneth` $\rightarrow$ `hymns` (2x: `C04:L219, L222`), `cometh` $\rightarrow$ `comes` (2x: `C12:L209, C20:L365`), `heareth` $\rightarrow$ `hears` (2x: `C16:L215`), `granteth` $\rightarrow$ `grants` (2x: `C18:L160, L382`), `entreateth` $\rightarrow$ `entreats` (2x: `C18:L224, L274`), and 1x each of `honoreth` (`C01:L108`), `dwelleth` (`C04:L132`), `magnifieth` (`C04:L306`), `knoweth` (`C13:L221`), `fainteth` (`C18:L157`), `beareth` (`C18:L191`), `adorneth` (`C18:L242`), `looseth` (`C18:L245`), `draweth` (`C18:L281`), `submitteth` (`C18:L299`). |
| **Phase 2: Hymnographic Gold Normalizer (`scripts/hymnographic_gold_normalizer.py`)** | `C01`–`C22` | 110 drift events | Deterministically normalized 52 Weekday Canon Heirmoi (`WEEKDAY_HEIRMOS_ALIGNED`), 36 fixed Psalm *stichoi* (`PSALM_VERSE_NORMALIZED`), 3 Tier-3 source psalm variants (`PSALM_VERSE_TIER3_SOURCE_VARIANT`), 18 explicit Podoben headers (`PODOBEN_NORMALIZED`), and 1 `Tone and Podoben the same` header (`PODOBEN_SAME_NORMALIZED` on `C12:p112`). |

### 2.2 Guardrails & Deterministic Healers to Eliminate 100% of Recurring `Flash` Mistakes at the Source

1. **Eliminate the Gate 1B vs. Gate 4 `-eth` Linter Split (`scripts/lint_liturgical_slop.py` & `scripts/run_small_pause_gate.py`)**:
   - Currently, `PROHIBITED_CATEGORIES["archaic_rubrical_verb_drift"]` in `scripts/lint_liturgical_slop.py` (line 53) only checks 13 hardcoded verbs (`singeth|proclaimeth|censeth|entereth|maketh|readeth|beginneth|taketh|vesteth|boweth|kisseth|turneth|standeth`). Meanwhile, `verify_publication_edition.py` (Gate 4) and `compile_final_edition.py` (`_convert_3rd_person_eth_token`) enforce a universal `\b[A-Za-z]+eth\b` check (minus `ETH_NOUN_WHITELIST`).
   - **Fix**: Import and execute `heal_cohort_and_apparatus_text()` directly inside `run_small_pause_gate.py` *before* running Gates 1A–4 (so `'wherefore'` $\rightarrow$ `'therefore'`, `'hearken'` $\rightarrow$ `'give ear'`, `Apolytikion` $\rightarrow$ `Troparion`, and all `\b[A-Za-z]+eth\b` verbs are deterministically healed in-place on `Draft/*_raw_draft.md` before the gate checks run), and replace the 13-verb list in `lint_liturgical_slop.py` with the universal `ETH_NOUN_WHITELIST` regex.
2. **Eliminate Marian & Adversary False Positives in `scripts/hieratic_pronoun_audit.py`**:
   - When a stanza is tagged `*Theotokion:*`, `*Staurotheotokion:*`, or contains Marian vocatives (`O Virgin`, `O Mother of God`, `O Birthgiver of God`, `O Sovereign Lady`, `O all-immaculate one`), 2nd-person pronouns (`thou, thee, thy, thine`) refer to the Mother of God even when divine titles (`God`, `Lord`, `Christ`, `Creator`, `Most High`) appear in the same clause. Similarly, 3rd-person masculine object pronouns following verbs of defeat (`crushing him`, `vanquish him`, `choked him`, `trampled him`) refer to the adversary/serpent, not Christ.
   - **Fix**: Add a clause-level Marian vocative exemption for `thou/thee/thy/thine` and an adversarial-verb exemption (`(?:crush(?:ing|ed)?|vanquish(?:ing|ed)?|trampl(?:ing|ed)?|slay(?:ing)?|overthrew|bound|cast\s+down)\s+him\b`) in `scripts/hieratic_pronoun_audit.py`.

---

## 3. Argon Review Queue Signal Precision (`argon_review_queue.json`)

### 3.1 Empirical Signal Distribution Across All 222 Physical Leaves

During the Phase 1 sprint, `argon_review_queue.json` recorded **0 queued leaves** and **0 quarantined leaves**. Auditing the underlying raw leaf metrics across all 222 physical leaves reveals why all 4 signals remained at zero and where 2 genuine codicological cruxes escaped queuing:

| Signal | Threshold in `run_small_pause_gate.py` | Empirical Distribution Across `p1`–`p222` | Queued Count | Assessment |
| :--- | :--- | :--- | :---: | :--- |
| **Signal 1: Epigraphic Uncertainty / Lacuna Markers** | Literal `[?]`, `[illegible]`, `[lacuna]`, `[damaged]`, `[corrupt]` | `0` literal tags used; subagents instead wrote **379 editorial restorations `[...]` across 221 leaves** (running headers `[Sunday.]`, faded margins, and the `p109` paper repair patch) paired with explanatory footnotes. | 0 | **False-Negative Gap**: Subagents describe physical damage in prose footnotes (`"partially obscured by a paper repair patch"`) rather than emitting literal `[lacuna]` or `[damaged]` tags in the body. |
| **Signal 2: Borderline `SGC-02` Length Ratio** | `< 0.50` or `> 2.20` on non-sparse leaves | **Min:** `0.870` (`p165`) \| **Max:** `1.485` (`p51`) \| **Mean:** `1.264`. All 222 leaves fell tightly within `[0.870, 1.485]`. | 0 | **High Precision (0 False Positives)**: Because subagents wrote mirrored Slavonic/English codicological descriptions on sparse leaves (`p1–p6`, `p165`, `p220–p222`), no false-positive ratio spikes occurred. |
| **Signal 3: High-Complexity Tables or Dense Apparatus** | `>= 5` Markdown table rows OR `>= 5` footnotes on 1 leaf | **Table rows:** `0` across all 222 leaves (`p4` Table of Tones was rendered as prose rubrics). **Footnotes/leaf:** Max `3` (`p3, p9, p10, p11, p12`), Mean `1.06` (`236` total). | 0 | **Calibrated for Printed Books, Too High for Manuscripts**: Manuscript cohorts average 10–13 footnotes per 10-leaf cohort (`1.0–1.7` per leaf); a leaf with `3` footnotes (`p3` dedication, `p9`) is already in the 99th percentile of manuscript apparatus density. |
| **Signal 4: Unresolved Quarantine** | `status == "QUARANTINED_FOR_ARGON"` | `0` cohorts failed Small Pause Gatekeeper. | 0 | **Exact**: 23/23 cohorts passed all gates on first orchestrator verification. |

### 3.2 Calibration Recommendations for Manuscript Codices

1. **Expand Signal 1 Regex to Scan Footnotes & Codicological Brackets for Physical Damage / Duplicate Exposure Keywords**:
   - In `scripts/run_small_pause_gate.py`, Signal 1 only checks body text for `\[(?:\?|illegible|lacuna|damaged|corrupt)[^\]]*\]`.
   - On `p109` (`Cohort 11`), a pasted paper repair patch covered the top of `# TONE 7`, and the subagent reconstructed the text in `[...]` while documenting the `"paper repair patch"` in footnote `[^109]`. On `p165` (`Cohort 17`), the leaf was a `"duplicate photographic exposure"` of `p164`.
   - **Calibration**: Extend Signal 1 in `run_small_pause_gate.py` to also scan the leaf's body and paired footnotes for `\b(?:paper\s+repair|repair\s+patch|obscured\s+by|torn\s+margin|duplicate\s+(?:photographic\s+)?exposure|missing\s+folio|reconstructed\s+from)\b` so genuine physical manuscript cruxes are automatically queued for Phase 2 Argon verification.
2. **Lower Signal 3 Footnote Density Threshold from `>= 5` to `>= 3` for Single-Column Manuscripts**:
   - While polyglot printed editions (`1630_lviv_octoechos`) frequently place 5+ footnotes on a single 2-up folio opening, 1-up or small-format manuscripts rarely exceed 3 footnotes on a single leaf (`p3` Dovhopole dedication leaf had 3 footnotes). Lowering the footnote signal threshold to `>= 3` when `total_physical_pages < 350` will route high-apparatus dedication/colophon leaves to Argon review.

---

## 4. Monument-Type & Compiler Edge Cases (`compile_final_edition.py`)

Five concrete compiler and verifier edge cases surfaced during Phase 2 compilation of `1600s_prykarpattia_ms_octoechos`:

### 4.1 Dynamic `publication_spec` Not Persisted to `codex_registry.json` (`scripts/compile_final_edition.py` line 1025)
- **Symptom**: When `UniversalPublicationEngine` ran on `1600s_prykarpattia_ms_octoechos` (which used `mode: "universal_dynamic_h1"` scaffolded spec with `"parts": []`), `_slice_parts()` dynamically discovered all 9 `# ...` H1 headings (`Part 0` + `Parts 1–9`) and populated `self.pub_spec["parts"] = dynamic_parts` in memory, but **did not write `self.pub_spec` back to `Liturgical Monuments/codex_registry.json`**. Immediately afterward, `verify_publication_edition.py` aborted at line 116 with: `ERROR: Monument '1600s_prykarpattia_ms_octoechos' has no publication_spec in codex_registry.json!`.
- **Root Cause**: `_slice_parts()` persisted `self.pub_spec` inside the `else:` branch (for Layout-B Weekday auto-expansion on lines 1061–1080) but omitted `atomic_update_registry()` inside the `if getattr(self, "_is_scaffolded_pub_spec", False):` branch (line 1025).

### 4.2 Zero 2-Up Seams Stitched (`209` Unstitched `...` Leaf Boundaries in `complete.md`)
- **Symptom**: `process_monument_cohorts()` in `scripts/hymnographic_gold_normalizer.py` reported: `Successfully stitched 0 2-up seams; 110 drift events tracked.` Inspecting `Final MD/1600s_prykarpattia_ms_octoechos_complete.md` reveals **209 lines beginning with `...`** and **218 lines ending with `...`** across leaf boundaries (e.g., `C01:L38` `Encompass Zion... for He is our God...` followed on `p8` by `...Who delivered us from our iniquities.`).
- **Root Cause (`scripts/hymnographic_gold_normalizer.py`, `stitch_2up_hymnographic_stream`, lines 970–1053)**:
  1. When `stitch_2up_hymnographic_stream()` matches `RE_LEAF_BANNER` (`=== LEAF pN ===` at line 970), it updates `locus.update_leaf(int(m_leaf.group(1)))` but **never sets `pending_milestone = locus.get_milestone()`**. Instead, `pending_milestone` is only set when `RE_PAGE_HEADER` (`**[Left Page - Folio X]**`) or `RE_COLUMN_HEADER` (`**[Column A]**`) matches (lines 979, 988). Because subagents obeyed Statutory Mandate #3 (no synthetic `[Left Page]` / `[Column A]` headers), `pending_milestone` remained `None` across all 222 leaves, completely bypassing `if pending_milestone and output_lines:` at line 1020!
  2. Furthermore, on nearly every leaf of this manuscript, the scribe wrote a centered running header at the top of the page (`[Saturday.]`, `[Sunday.]`, `[Monday.]`, or `(fol. 37)[^55]`). Because `RE_PAGE_HEADER` does not match bracketed liturgical day running headers (`^\[(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Tone\s+[1-8])[^\]]*\]$`), those running headers are emitted as regular lines into `output_lines` *between* the trailing `...` of leaf $p_k$ and the leading `...` of leaf $p_{k+1}$, blocking adjacency stitching.

### 4.3 `_propers_corpus.json` Metadata Collapse (`"office": "Front Matter"`, `"ode": null`, and Tone 8 Absorption)
- **Symptom**: Auditing `Final MD/1600s_prykarpattia_ms_octoechos_propers_corpus.json` (`3,125` items) revealed three structural metadata defects:
  1. `"office"` is `"Front Matter"` for **100% of items (`3,125 / 3,125`)**.
  2. `"ode"` is `null` for **100% of items (`3,125 / 3,125`)**.
  3. `"tone"` distribution is `{1: 246, 2: 216, 3: 235, 4: 240, 5: 242, 6: 253, 7: 253, 8: 1425, 0: 15}` — **1,425 items (45.6% of the codex)** were assigned to `tone: 8`!
- **Root Cause (`scripts/hymnographic_gold_normalizer.py`, `process_monument_cohorts` & `generate_propers_corpus`, lines 1480–1585 & 1867–1965)**:
  1. In `process_monument_cohorts()`, `all_stitched_cohorts` is collected *before* `format_hymnographic_stanzas_and_headings()` promotes inline italic office rubrics into `## ...` H2 headings (or the inline rubrics in `1600s_prykarpattia_ms_octoechos` use manuscript phrasings like `*On Saturday Evening, at Little Vespers, Stichera...*` that only match when `para.startswith("#")` in `generate_propers_corpus()` line 1911). Because `Cohorts/*.md` has **zero `##` headings** and **zero `#### Ode N` headings** (odes are inline `*Ode N. Heirmos:*`), `generate_propers_corpus()` never updates `current_office` from its initial value `"Front Matter"` and never updates `current_ode` from `None`.
  2. In Cohorts 15–21 (`p141`–`p210`), the manuscript contains the consolidated Weekday Octoechos Cycle (Tones 1–8 Weekday Vespers/Matins) introduced by inline italic rubrics (`*Tone 1. On Monday Evening...*`, `*Tone 2...*`) rather than `# TONE N` H1 banners, followed by `# EXAPOSTILARIA AND EVANGELICAL STICHERA` in Cohort 22 (`p212`). Because `generate_propers_corpus()` only updates `current_tone` on `# ... TONE N` headings (line 1913), `current_tone` stayed locked at `8` from Cohort 13 (`p125`) all the way to the end of the codex (`p222`).

### 4.4 Gate 7E Hardcoded 8-Tone Podoben Threshold (`scripts/verify_publication_edition.py` line 633)
- **Symptom**: Gate 7E initially failed with: `[FAIL] Gate 7E: Podoben grid incomplete (invocations=20, tones=[1, 3, 4, 6, 8])`.
- **Root Cause**: Line 633 required `len(grid_tones) < 8`, assuming every Octoechos physically prints explicit `Podoben:` rubrics in all 8 tones. While the 650-page printed `1630_lviv_octoechos` has 100+ Podoben rubrics across all 8 tones, the 222-leaf Carpathian manuscript omits `Podoben:` incipit tags in Tones 2, 5, and 7 (writing only `*Sticheron 1:*` or `*Other Stichera...*`), physically attesting explicit `Podoben:` rubrics in 5 tones (`[1, 3, 4, 6, 8]`, 20 invocations).

### 4.5 Gate 7F Cross-Deliverable Podoben Parity Mismatch (`scripts/hymnographic_gold_normalizer.py` line 1656)
- **Symptom**: Gate 7F initially failed with `complete.md=20, _podoben_grid.json=20, _primitives_review.md=19`.
- **Root Cause**: `generate_father_paul_digest()` overrode `total_pod_invocations` (20) by counting `r"\bpodoben:"` across raw `Cohorts/*cohort*.md` files on disk (19), missing the 20th invocation on `C12:p112` (`*Other Stichera, to the Holy Forerunner John, Tone and Podoben the same:*`) which was normalized in memory into `*Podoben: "The same Tone and Podoben" (Гла́съ и҆ подо́бенъ то́йже):*` inside `all_stitched_cohorts`.

---

## 5. Granular Atomic Tagging Blueprint (Propers & Non-Propers)

To enable a universal atomic extractor (`scripts/extract_atomic_corpus.py`) to tag **100.0% of `1600s_prykarpattia_ms_octoechos`** into `{monument_id}_atomic_corpus.json`, we audited all **5,303 non-empty lines** across all 23 `Cohorts/*.md` files.

### 5.1 Architectural Requirement: Two-Line Stateful Role Binding & Seam Continuity
In manuscript cohorts, subagents format liturgical units in two ways:
1. **Single-Line Inline Format (`~5%` of stanzas)**: `*Troparion:* Body text...` on a single line.
2. **Two-Line Split Rubric-Then-Body Format (`~95%` of stanzas)**: Line $N$ is a standalone italic role rubric (`*Troparion 1:*`, `*Ode 3. Heirmos:*`, `*Both now... Theotokion:*`), and Line $N+1$ is the untagged stanza body (`Receive our evening prayers...`). Furthermore, **209 stanzas** split across `=== LEAF pN ===` (and 16 across cohort boundaries) with an intervening running header (`[Sunday.]`, `(fol. 37)[^55]`) before the `...continuation` line.

By maintaining an `active_role` state machine that (a) updates when a standalone role rubric `*...*` is encountered, and (b) persists across `=== LEAF pN ===` and running headers `[Sunday.]` / `(fol. N)` when the next text line starts with `...`, the regex blueprint below achieves **100.00% classification coverage (`5,303 / 5,303` lines, `0` unclassified)**.

### 5.2 Complete Inventory of Atomic Liturgical Unit Classes (`5,303 / 5,303` Lines)

#### A. Structural & Codicological Paratext (`4` Classes — `513` Lines)
| Atomic Unit Class ID | Line Count | Exact Markdown / Regex Pattern in `Cohorts/*.md` |
| :--- | :---: | :--- |
| `STRUCT.LEAF_BOUNDARY` | 222 | `^===\s*LEAF\s+p(\d+)\s*===$` |
| `STRUCT.H1_MONUMENT_OR_PART_HEADING` | 9 | `^#\s+([^\n#]+)$` (`# TONE 1`..`# TONE 8`, `# EXAPOSTILARIA AND EVANGELICAL STICHERA`) |
| `PARATEXT.RUNNING_HEADER_OR_FOLIO_TAG` | 268 | `^(?:\[(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Tone\s+[1-8]|Octoechos|Service|Canon|flyleaf|recto|verso)[^\]]*\]|\((?:fol\.|f\.)\s*[^)]+\)|\[57\]|MKDU|13962|SD-319)(?:\s*\[\^\d+\])?$` |
| `PARATEXT.CODICOLOGICAL_AND_DEDICATION` | 14 | `^\[(?:Binding|On\s+the\s+|Verso\s+of|Facing\s+|Miniature|Ornamental|Illuminated|Woodcut|Blank|Flyleaf|Front|Rear|Spine|Lower\s+Margin|Upper\s+Margin|Archival|Page_0165|Running\s+header|Catchword|Top\s+|Left\s+|Right\s+|Pasted).*\]` or donor dedication lines on `p3` (`^(?:To\s+the\s+glory\s+of\s+the\s+Holy|Father,\s+and\s+Son|Through\s+the\s+zeal\s+of\s+His\s+servant)`) |

#### B. Variable Propers (`17` Classes — `2,243` Stanza/Header Lines + `1,924` Paired Role Rubric Lines)
| Atomic Unit Class ID | Stanza / Header Lines | Triggering Inline or Preceding Role Rubric Regex |
| :--- | :---: | :--- |
| `PROPER.CANON_TROPARION` | 1,068 | `^\*(?:(?:\[[^\]]+\]\s*)?(?:Troparion(?:\s+\d+)?|Another(?:\s+Troparion)?(?:\s+\d+)?|Refrain\s+\d+|Ode\s+[1-9]\.\s*Troparion(?:\s+\d+)?)(?:\s*\([^)]+\))?(?:\s*\[[^\]]+\])?):?\*` |
| `PROPER.THEOTOKION_DOGMATIKON` | 425 | `^\*[^\n*]*\b(?:Theotokion|Dogmatic\s+Theotokion|Mother\s+of\s+God)(?:\s*[^*:]*):?\*` |
| `PROPER.STICHERON` | 254 | `^\*[^\n*]*\b(?:Sticheron|Stichera|Anatolian|Alphabetical|Lord,\s+I\s+have\s+cried|Aposticha|Praises)(?:\s+\d+)?(?:\s*[^*:]*):?\*` |
| `PROPER.CANON_HEIRMOS` | 126 | `^\*[^\n*]*\bHeirmos(?:\s*[^*:]*):?\*` |
| `PROPER.MARTYRICON` | 96 | `^\*[^\n*]*\b(?:Martyricon|To\s+the\s+Martyrs|Of\s+the\s+Martyrs)(?:\s+\d+)?(?:\s*[^*:]*):?\*` |
| `PROPER.SESSIONAL_HYMN_KATHISMA` | 78 | `^\*[^\n*]*\bSessional\s+Hymn(?:\s+\d+)?(?:\s*[^*:]*):?\*` |
| `PROPER.GRADUAL_ANTIPHON` | 44 | `^\*[^\n*]*\b(?:Antiphon\s+\d+|Song\s+of\s+Ascents)(?:\s*[^*:]*):?\*` |
| `PROPER.PODOBEN_MODEL_RUBRIC` | 29 | `^\*(?:[^\n*]*?\bPodoben:|\bPodoben:|[^\n*]*Tone\s+and\s+Podoben\s+the\s+same:)[^\n*]*\*(?:\s*\[\^\d+\])?$` |
| `PROPER.STAUROTHEOTOKION` | 27 | `^\*[^\n*]*\b(?:Staurotheotokion|Cross-Theotokion|Cross-Resurrection\s+Theotokion)(?:\s*[^*:]*):?\*` |
| `PROPER.EXAPOSTILARION_SVITYLEN` | 26 | `^\*[^\n*]*\b(?:Exapostilarion|Exapostilaria|Light-Hymn|Photagogikon)(?:\s+\d+)?(?:\s*[^*:]*):?\*` |
| `PROPER.TRINITY_TROPARION_TRIADIKON` | 25 | `^\*[^\n*]*\b(?:Trinity\s+Hymn|Triadikon|Triadica|To\s+the\s+Most\s+Holy\s+Trinity)(?:\s*[^*:]*):?\*` |
| `PROPER.IKOS` | 21 | `^\*[^\n*]*\bIkos(?:\s*[^*:]*):?\*` |
| `PROPER.EVANGELICAL_STICHERON_EOTHINON` | 20 | `^\*[^\n*]*\b(?:Evangelical\s+Sticheron|Eothinon)\b[^*:]*:?\*` |
| `PROPER.NEKROSIMON_DEPARTED` | 15 | `^\*[^\n*]*\b(?:For\s+the\s+Departed|Hymn\s+for\s+the\s+Departed|To\s+the\s+Departed)(?:\s*[^*:]*):?\*` |
| `PROPER.KONTAKION` | 14 | `^\*[^\n*]*\bKontakion(?:\s*[^*:]*):?\*` |
| `PROPER.BEATITUDES_TROPARION` | 11 | `^\*[^\n*]*\bBeatitudes?(?:\s+Troparion)?(?:\s+\d+)?(?:\s*[^*:]*):?\*` |
| `PROPER.HYPAKOE_AND_APOLYTIKION` | 12 | `^\*[^\n*]*\b(?:Hypakoe|Resurrection\s+Troparion|Dismissal\s+Troparion)(?:\s*[^*:]*):?\*` (`8` Hypakoe + `4` Dismissal Troparia) |

#### C. Fixed Non-Propers (`4` Classes — `126` Scriptural/Chant Lines + `451` Procedural Office Rubrics)
| Atomic Unit Class ID | Line Count | Exact Markdown / Regex Pattern in `Cohorts/*.md` |
| :--- | :---: | :--- |
| `NONPROPER.PROCEDURAL_OFFICE_RUBRIC` | 451 | Standalone `*...*` rubrics specifying service transitions, liturgical actions, or canon titles (`^\*(?:On\s+(?:Saturday|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday)|At\s+(?:Little\s+Vespers|Great\s+Vespers|Matins|the\s+Midnight\s+Office|the\s+Aposticha|the\s+Praises|the\s+Divine\s+Liturgy)|Canon\s+to|Another\s+Canon|After\s+the)[^\n*]*\*(?:\s*\[\^\d+\])?$`) |
| `NONPROPER.FIXED_PSALM_STICHOS_VERSE` | 92 | `^\*(?:Verse(?:\s+\d+)?|Stichos(?:\s+\d+)?):\*?\s*.+$` or `^\*Holiness\s+becomes\s+Thy\s+house[^\n]*\*$` |
| `NONPROPER.LECTIONARY_EPISTLE_GOSPEL_PERICOPE` | 26 | `^(?:\*[^\n*]*\b(?:Epistle|Gospel|Reading)\b[^*:]*:\*\s*.+|Brethren:\s+.+|The\s+Lord\s+said(?:\s+unto\s+His\s+disciples)?:\s+.+)$` (Weekday Liturgy Epistle & Gospel readings in Cohorts 16–20) |
| `NONPROPER.PROKEIMENON_ALLELUIA_CHANTS` | 8 | `^\*[^\n*]*\b(?:Prokeimenon|Alleluia)(?:\s*[^*:]*):?\*\s*.+$` |

*(Note: Because an Octoechos is a Choir/Chanter's book of variable propers rather than a Priest's Sluzhebnik/Trebnyk, Sacerdotal Secret Prayers, Litanies, and Sacramental Formulas have `0` occurrences in this codex.)*

---

## 6. Top 5 Concrete Engine Hardening Recommendations

Based on the empirical evidence from `1600s_prykarpattia_ms_octoechos`, here are the top 5 ranked code and template hardening changes for the cross-wave System Hardening Implementation Plan:

### Rank 1: Enable Leaf-Banner (`=== LEAF pN ===`) & Running-Header Seam Stitching in `scripts/hymnographic_gold_normalizer.py`
- **Target File & Function**: `scripts/hymnographic_gold_normalizer.py` $\rightarrow$ `stitch_2up_hymnographic_stream()` (lines 970–1053) and `RE_PAGE_HEADER` (line 915).
- **Empirical Evidence**: `stitch_2up_hymnographic_stream()` stitched **0 out of 209** mid-sentence leaf boundaries in `1600s_prykarpattia_ms_octoechos` because `m_leaf = RE_LEAF_BANNER.match(line)` (line 970) calls `locus.update_leaf(...)` without setting `pending_milestone = locus.get_milestone()`, and top-of-page manuscript running headers (`[Saturday.]`, `[Sunday.]`, `(fol. 37)[^55]`) are not consumed as page-header metadata, blocking adjacency between the trailing `...` of leaf $p_k$ and the leading `...` of leaf $p_{k+1}$.
- **Actionable Change**:
  1. In `m_leaf = RE_LEAF_BANNER.match(line)` (line 972), set `pending_milestone = locus.get_milestone()`.
  2. Add `RE_RUNNING_HEADER = re.compile(r"^(?:\[(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Tone\s+[1-8])[^\]]*\]|\((?:fol\.|f\.)\s*([0-9]+[rv]?)\))(?:\s*(\[\^\d+\]))?$", re.IGNORECASE)` inside `stitch_2up_hymnographic_stream()` so top-of-page running headers update `locus` / `pending_footnote` without breaking mid-sentence seam stitching across `=== LEAF pN ===`.

### Rank 2: Make `generate_propers_corpus()` Parse Inline Italic Office, Ode, and Weekday Tone Rubrics in `scripts/hymnographic_gold_normalizer.py`
- **Target File & Function**: `scripts/hymnographic_gold_normalizer.py` $\rightarrow$ `generate_propers_corpus()` (lines 1867–1985) and `format_hymnographic_stanzas_and_headings()` (lines 1218–1278).
- **Empirical Evidence**: Because `1600s_prykarpattia_ms_octoechos` strictly obeyed Statutory Mandate #3 (no synthetic `##` or `#### Ode N` headings; all office, ode, and weekday transitions are inline italic rubrics `*...*`), `generate_propers_corpus()` left `"office": "Front Matter"` on **3,125 / 3,125 items**, `"ode": null` on **3,125 / 3,125 items**, and assigned **1,425 items** (including Tones 1–7 Weekday propers in Cohorts 15–21 and the Exapostilaria/Eothina in Cohort 22) to `"tone": 8`.
- **Actionable Change**:
  1. In `generate_propers_corpus()`, detect inline italic transitions even when `not para.startswith("#")`:
     - Update `current_ode` whenever `re.search(r"\bOde\s+([1-9])\b", clean_para, re.I)` matches.
     - Update `current_office` whenever `clean_para` starts with `*` and matches day/service keywords (`On Saturday Evening`, `At Little Vespers`, `At Great Vespers`, `At Matins`, `On Sunday Morning`, `On Monday Evening`, `On Tuesday...`, etc.).
     - Update `current_tone` whenever an inline weekday/exapostilaria rubric specifies `\bTone\s+([1-8])\b` (`*Tone 1. On Monday Evening...*`, `*Evangelical Sticheron N, Tone N:*`).
  2. When a standalone italic role rubric (`*Troparion 1:*`) is followed by its stanza paragraph on the next block, merge the role tag into the stanza's `hymn_type` classification before emitting the corpus item.

### Rank 3: Unify Gate 1B (`scripts/lint_liturgical_slop.py`) 3rd-Person `-eth` Linter with Gate 4 & Pre-Gate Self-Healer (`scripts/run_small_pause_gate.py`)
- **Target Files & Functions**: `scripts/lint_liturgical_slop.py` $\rightarrow$ `PROHIBITED_CATEGORIES["archaic_rubrical_verb_drift"]` (line 51) & `lint_slop()`; `scripts/run_small_pause_gate.py` $\rightarrow$ `run_gatekeeper()`.
- **Empirical Evidence**: `lint_liturgical_slop.py` checks only 13 hardcoded `-eth` verbs, missing **31 occurrences of 15 other 3rd-person `-eth` verbs across 24 lines in 10 cohorts** (`becometh` 5x, `rejecteth` 4x, `rejoiceth` 2x, `hymneth` 2x, `cometh` 2x, `heareth` 2x, `granteth` 2x, `entreateth` 2x, etc.), which were only healed later during Phase 2 compilation (`heal_cohort_and_apparatus_text()`). Meanwhile, Cohorts 16, 18, and 19 wasted 11 `edit_file` calls manually fixing `'maketh'`, `'taketh'`, `'wherefore'`, and `'Hearken'`.
- **Actionable Change**:
  1. Replace the 13-verb regex in `scripts/lint_liturgical_slop.py` with the universal `\b([A-Za-z]+eth)\b` check filtered by `ETH_NOUN_WHITELIST` from `scripts/verify_publication_edition.py`.
  2. Invoke `heal_cohort_and_apparatus_text()` at the start of `scripts/run_small_pause_gate.py` (before running Gates 1A–4) so 1-to-1 vocabulary (`Apolytikion` $\rightarrow$ `Troparion`), `-eth` verbs (`becometh` $\rightarrow$ `becomes`), and slop tokens (`wherefore` $\rightarrow$ `therefore`, `hearken` $\rightarrow$ `give ear`) are deterministically healed in `Draft/*_raw_draft.md` on the first pass.

### Rank 4: Add Marian (`Theotokion`) & Adversary Clause Exemptions to `scripts/hieratic_pronoun_audit.py`
- **Target File & Function**: `scripts/hieratic_pronoun_audit.py` $\rightarrow$ `audit_pronouns()` (lines 90–145).
- **Empirical Evidence**: All **6 Gate 2 failures** across the entire 222-leaf run (`C05:L305`, `C08:L80`, `C08:L281`, `C13:L111` x2, `C14:L108`) were **false positives** where a Divine noun (`Almighty Lord`, `O Lord`, `Christ, truly our God`, `Mother of the Most High God`, `Birthgiver of God`) fell within the 120-character proximity window of a lowercase pronoun referring to **Satan/the enemy** (`crushing him`, `I vanquish him!`), **Christ's Tomb** (`worship thee, O Life-Giving Tomb`), or **the Theotokos** (`unto thee... Mother of the Most High God`, `O Birthgiver of God; thou bearest in thine arms`). To pass Gate 2, subagents were forced to rewrite `'him'` as `'the adversary'`/`'the enemy'`, capitalize `'Thee'` for an inanimate tomb, or hyphenate `'Birth-giver'`.
- **Actionable Change**:
  1. Exempt lowercase `thou/thee/thy/thine` when the paragraph is tagged `*Theotokion*` / `*Staurotheotokion*` or contains Marian vocatives (`O Virgin`, `O Mother of God`, `O Birthgiver of God`, `O Sovereign Lady`, `O Bride of God`, `O all-immaculate one`, `O Life-Giving Tomb`).
  2. Exempt lowercase `him` when immediately preceded by adversarial verbs (`(?:crush(?:ing|ed)?|vanquish(?:ing|ed)?|chok(?:ing|ed)|trampl(?:ing|ed)?|bound|cast\s+down|overthrew|put\s+to\s+shame)\s+him\b`).

### Rank 5: Pre-Render Attested Podoben Table & Exact CLI Gate Command in `data/templates/work_order_template.md`
- **Target File & Function**: `data/templates/work_order_template.md` and `scripts/autonomous_orchestrator.py` $\rightarrow$ `generate_work_order()`.
- **Empirical Evidence**: Across the 23 cohorts, `Flash` subagents executed **304 shell commands** (`13.2` commands/cohort; up to `34–35` commands in Cohorts 1 and 17), spending 5–8 minutes per cohort running ad-hoc `python -c` queries against `data/liturgical_primitives_registry.json` and `codex_registry.json` (repeatedly crashing on Windows `cp1252` `UnicodeEncodeError`), checking `--help` flags on linter scripts, and in two cases (`Cohort 17` and `Cohort 21`) accidentally running `run_small_pause_gate.py` on the *previous* cohort number (`--cohort 16` and `--cohort 20`).
- **Actionable Change**:
  1. In `data/templates/work_order_template.md`, include the compact lookup table of the 46 canonical Podoben incipits (or instruct subagents that `hymnographic_gold_normalizer.py` automatically normalizes Podoben incipits during Phase 2, so they must never query `data/liturgical_primitives_registry.json` via shell commands).
  2. Explicitly forbid running individual linter scripts with `--help` or inspecting `codex_registry.json`, and provide the **single exact verification command** (`py scripts/run_small_pause_gate.py --monument {{MONUMENT_ID}} --cohort {{COHORT_NUM}}`) with `-X utf8` / `PYTHONUTF8=1` pre-configured.
