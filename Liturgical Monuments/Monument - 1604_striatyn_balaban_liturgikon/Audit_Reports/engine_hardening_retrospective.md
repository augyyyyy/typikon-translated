# Post-Run Engine Retrospective: 1604 Striatyn Liturgikon of Hedeon Balaban (`1604_striatyn_balaban_liturgikon`)

- **Monument ID**: `1604_striatyn_balaban_liturgikon`
- **Canonical Title**: *1604 Striatyn Liturgikon of Hedeon Balaban (Служебник, Стрятин: Друкарня Балабанів, 1604)*
- **Primary Genre & Layout**: `rubrical` (Euchologion / Sluzhebnik) — **2-up open-spread facsimile** (293 physical PDF leaves = 582 printed folio pages)
- **Sprint Execution Topology**: 30 cohorts (`p1`–`p293`; Cohorts 1–29 @ 10 leaves, Cohort 30 @ 3 leaves) executed via `ephemeral_translator` (`Gemini 3.8 Flash`) under Phase 0/2 `Gemini 4 Argon (High)` supervision
- **Machine-Readable Companion**: [`engine_hardening_retrospective.json`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/Liturgical%20Monuments/Monument%20-%201604_striatyn_balaban_liturgikon/Audit_Reports/engine_hardening_retrospective.json)

---

## 1. Cohort Velocity & Bottleneck Autopsy

### 1.1 Sprint-Wide Velocity Summary

| Metric | Value | Notes |
|---|---|---|
| **Total Physical Leaves Processed** | **293 leaves** (582 pages) | 100.0% mathematical leaf conservation (`p1`..`p293`) |
| **Total Subagent Wall-Clock Time** | **21,584.0 sec** (**359.73 min / 6.00 hrs**) | Measured from `invoke_subagent` spawn to subagent completion |
| **Mean / Median Cohort Duration** | **719.5 sec (11.99 min)** / **686.5 sec (11.44 min)** | Across all 30 cohorts |
| **Mean Processing Time per Leaf / Page** | **73.7 sec / physical leaf** (**37.1 sec / printed page**) | 2-up open-spread images at 300 DPI |
| **Total Source Text Transcribed** | **43,962 words** (462,671 bytes) | Diplomatic Church Slavonic / Early Modern Ruthenian |
| **Total English Draft Body Words** | **54,536 words** (339,748 bytes) | Active Present Indicative rubrics + hieratic prayers |
| **Total Scholarly Footnote Words** | **37,027 words** across **951 footnotes** | Exact 1:1 bijective parity (`[^1]`..`[^951]`) |
| **Total Combined Output Volume** | **135,525 words** (**91,563 English words**) | Mean throughput: **376.7 combined words/min** |
| **Subagent Retries / Quarantines** | **0 retries / 0 quarantines** | 100% first-turn completion across all 30 `Flash` cohorts |

### 1.2 Complete 30-Cohort Telemetry Table

| Cohort | Leaves | Leaf Count | Wall-Clock (sec) | Wall-Clock (min) | Sec / Leaf | Source Words | Draft Words (EN) | Footnote Words (EN) | Total EN Words | Footnotes (`[^N]`) | Combined Words/Min |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **C01** | `p1..p10` | 10 | **1,869.0** | **31.15** | 186.9 | 1,542 | 1,856 | 1,178 | 3,034 | 30 (`1..30`) | 146.9 |
| **C02** | `p11..p20` | 10 | 854.0 | 14.23 | 85.4 | 1,501 | 1,777 | 638 | 2,415 | 31 (`31..61`) | 275.1 |
| **C03** | `p21..p30` | 10 | 615.0 | 10.25 | 61.5 | 1,529 | 1,750 | 1,321 | 3,071 | 44 (`62..105`) | 448.8 |
| **C04** | `p31..p40` | 10 | 665.0 | 11.08 | 66.5 | 1,512 | 1,727 | 986 | 2,713 | 34 (`106..139`) | 381.2 |
| **C05** | `p41..p50` | 10 | 555.0 | 9.25 | 55.5 | 1,451 | 1,794 | 1,062 | 2,856 | 23 (`140..162`) | 465.6 |
| **C06** | `p51..p60` | 10 | 735.0 | 12.25 | 73.5 | 1,500 | 1,852 | 809 | 2,661 | 26 (`163..188`) | 339.7 |
| **C07** | `p61..p70` | 10 | 649.0 | 10.82 | 64.9 | 1,471 | 1,785 | 900 | 2,685 | 30 (`189..218`) | 384.2 |
| **C08** | `p71..p80` | 10 | 574.0 | 9.57 | 57.4 | 1,512 | 1,857 | 1,344 | 3,201 | 29 (`219..247`) | 492.6 |
| **C09** | `p81..p90` | 10 | 523.0 | 8.72 | 52.3 | 1,456 | 1,762 | 1,417 | 3,179 | 29 (`248..276`) | 531.7 |
| **C10** | `p91..p100` | 10 | **489.0** | **8.15** | **48.9** | 1,400 | 1,660 | 1,777 | 3,437 | 30 (`277..306`) | **593.5** |
| **C11** | `p101..p110` | 10 | 767.0 | 12.78 | 76.7 | 1,422 | 1,741 | 1,756 | 3,497 | 49 (`307..355`) | 384.8 |
| **C12** | `p111..p120` | 10 | 781.0 | 13.02 | 78.1 | 1,341 | 1,619 | 2,034 | 3,653 | 43 (`356..398`) | 383.7 |
| **C13** | `p121..p130` | 10 | 548.0 | 9.13 | 54.8 | 1,405 | 1,969 | 1,227 | 3,196 | 24 (`399..422`) | 503.8 |
| **C14** | `p131..p140` | 10 | 553.0 | 9.22 | 55.3 | 1,504 | 1,863 | 968 | 2,831 | 20 (`423..442`) | 470.3 |
| **C15** | `p141..p150` | 10 | 572.0 | 9.53 | 57.2 | 1,511 | 1,853 | 795 | 2,648 | 18 (`443..460`) | 436.3 |
| **C16** | `p151..p160` | 10 | 757.0 | 12.62 | 75.7 | 1,504 | 1,662 | 1,366 | 3,028 | 20 (`461..480`) | 359.2 |
| **C17** | `p161..p170` | 10 | 681.0 | 11.35 | 68.1 | 1,402 | 1,609 | 1,282 | 2,891 | 20 (`481..500`) | 378.2 |
| **C18** | `p171..p180` | 10 | 758.0 | 12.63 | 75.8 | 1,469 | 1,934 | 1,139 | 3,073 | 20 (`501..520`) | 359.5 |
| **C19** | `p181..p190` | 10 | 685.0 | 11.42 | 68.5 | 1,586 | 2,116 | 1,350 | 3,466 | 20 (`521..540`) | 442.5 |
| **C20** | `p191..p200` | 10 | 564.0 | 9.40 | 56.4 | 1,513 | 2,003 | 1,332 | 3,335 | 21 (`541..561`) | 515.7 |
| **C21** | `p201..p210` | 10 | 774.0 | 12.90 | 77.4 | 1,426 | 1,781 | 421 | 2,202 | 14 (`562..575`) | 281.2 |
| **C22** | `p211..p220` | 10 | 688.0 | 11.47 | 68.8 | 1,447 | 1,670 | 694 | 2,364 | 15 (`576..590`) | 332.4 |
| **C23** | `p221..p230` | 10 | 551.0 | 9.18 | 55.1 | 1,580 | 2,088 | 1,197 | 3,285 | 24 (`591..614`) | 529.8 |
| **C24** | `p231..p240` | 10 | 823.0 | 13.72 | 82.3 | 1,591 | 1,960 | 922 | 2,882 | 26 (`615..640`) | 326.1 |
| **C25** | `p241..p250` | 10 | 699.0 | 11.65 | 69.9 | 1,632 | 2,362 | 1,247 | 3,609 | 40 (`641..680`) | 449.9 |
| **C26** | `p251..p260` | 10 | 757.0 | 12.62 | 75.7 | 1,692 | 2,431 | 2,221 | **4,652** | **76 (`681..756`)** | 502.8 |
| **C27** | `p261..p270` | 10 | 705.0 | 11.75 | 70.5 | 1,539 | 2,030 | 1,804 | 3,834 | 64 (`757..820`) | 457.3 |
| **C28** | `p271..p280` | 10 | **1,012.0** | **16.87** | 101.2 | 1,368 | 1,742 | 1,451 | 3,193 | 51 (`821..871`) | 270.4 |
| **C29** | `p281..p290` | 10 | **974.0** | **16.23** | 97.4 | 1,241 | 1,730 | 1,672 | 3,402 | 67 (`872..938`) | 286.0 |
| **C30** | `p291..p293` | 3 | 610.0 | 10.17 | **203.3** | 324 | 439 | 360 | 799 | 13 (`939..951`) | 110.5 |

### 1.3 Autopsy of the 3 Slowest Cohorts

1. **Rank #1 Slowest: Cohort 1 (`p1`–`p10`) — 1,869.0 sec (31.15 min | 186.9 sec/leaf | 30 footnotes)**
   - **Codicological & Visual Bottleneck**: Cohort 1 spanned five distinct visual and linguistic regimes across 10 physical spreads:
     - *Leaves `p1`–`p3`*: 17th-century blind-tooled calfskin binding boards, pastedown, and preliminary flyleaves bearing faint 17th–19th c. Polish, Latin, and Cyrillic cursive marginalia (*"Protasy Morych..."*, *"X. Antoni Żukowski, 1825"*).
     - *Leaves `p4`–`p5`*: Architectural woodcut title frame (*СЛУЖЕБНИКЪ*, Striatyn, 7112 / 1604) on `p4R`, followed on `p5L` by the full-page heraldic woodcut of the Balaban Coat of Arms (*Корчак* — three silver rivers) and 10 lines of Baroque Ruthenian syllabic *virshi*.
     - *Leaves `p5R`–`p9R`*: Bishop Hedeon Balaban's 7-page Episcopal Preface in Chancery Ruthenian / Slavonic citing Patriarch Meletios Pegas of Alexandria and the Constantinopolitan Exarchate.
     - *Leaves `p9R`–`p10R`*: Transition to the Diataxis of Patriarch Philotheos Kokkinos (`# PART I: ORDER OF THE DIVINE LITURGY AND DIACONATE`).
   - **Prompt / Gate Bottleneck**: Statutory Mandate 12 required the worker to write symmetric codicological descriptions in both `Source Text/` and `Draft/` on non-text binding/flyleaf pages (`p1`–`p3`) so that character-length ratios remained inside `[0.80, 1.50]`. Furthermore, the subagent executed `run_small_pause_gate.py` inside its own turn (logged in `triage_inbox.jsonl` at `12:20:47Z`) and self-corrected a minor formatting discrepancy before returning.

2. **Rank #2 Slowest: Cohort 28 (`p271`–`p280`) — 1,012.0 sec (16.87 min | 101.2 sec/leaf | 51 footnotes)**
   - **Codicological & Visual Bottleneck (Major Binder's Dislocation)**: Cohort 28 encountered the most severe physical binding dislocation in the Vernadsky National Library exemplar (`Кир. 746`). In Cohort 27 (`p269R`, fol. 269v), the headpiece `## PRAYERS OF LIGHT AT VESPERS` had been followed directly on `p270L` by the *Second* Prayer of Light because Folio 2 of Quire Ya (`ѧ҃ в`, printed pp. 527–528) was missing from its proper place. In Cohort 28, on `p273L` (fol. 273v, p. 536), the Seventh Prayer of Light broke off mid-word (`жили-` / *"habitation"*); on `p273R` (printed p. 527), the missing Folio `ѧ҃ в` suddenly appeared with the duplicate woodcut headpiece `МОЛИТВЫ ВЕЧЕРНЇА` (`## PRAYERS AT VESPERS`) and the First Prayer of Light (`p273R`–`p274L`, pp. 527–528), before `p274R` (fol. 274r, p. 537) resumed the interrupted Seventh Prayer (`-ще. Положи г҃и...`).
   - **Prompt Bottleneck**: Because `generate_work_order.py` does not inject a "Quire & Folio Continuity State" from Cohort $K-1$ into Cohort $K$, the Cohort 28 worker had to deduce independently from the 300-DPI scans why a Vesperal headpiece and Prayer 1 were embedded inside Prayer 7, transcribe the physical leaves strictly in facsimile order (Rule 15), and document the dislocation across 51 footnotes.

3. **Rank #3 Slowest: Cohort 29 (`p281`–`p290`) — 974.0 sec (16.23 min | 97.4 sec/leaf | 67 footnotes)**
   - **Codicological & Apparatus Bottleneck**: Cohort 29 combined 9 leaves of dense Euchologion Matins prayers (Prayers 4–12, featuring heavy LXX Psalter and Pauline allusions requiring 67 footnotes totaling 1,672 words—nearly a 1:1 ratio with the 1,730 body words) with the historical 2-page Striatyn Colophon on `p289R`–`p290R` (pp. 564–565).
   - **Epigraphic Crux**: On `p281L` (fol. 281r, p. 547, line 6 of the Fifth Matins Prayer), the Striatyn compositor set the corrupt word `оу҆́чстии` instead of `ѿч҃е ст҃ый` (*"Holy Father"*), which is explicitly indexed in the rear Errata leaf (`p291L`). Collating this reading and translating the full diplomatic titulature of Bishop Hedeon Balaban and Noble Theodore (Fedir) Balaban accounted for the elevated runtime.
   - *(Per-Leaf Outlier Note)*: **Cohort 30 (`p291`–`p293`, 3 leaves)** took 610.0 sec (**203.3 sec/leaf**) due to deciphering the two-part *Погрѣшеніа* (Errata) apparatus on `p291L` (cross-referencing folios 101 and 224) and authoring symmetric Mandate 12 descriptions for the Vernadsky Library stamps and rear binding boards on `p291R`–`p293R`.

---

## 2. Small Pause Gate, Deterministic Self-Healing & Flash Failure Modes

### 2.1 Phase 1 Small Pause Gate & `attempt_deterministic_self_healing()` Catalog

Across all 30 cohorts, `scratch/triage_inbox.jsonl` recorded **10 initial Small Pause Gate events**:
- **5 In-Subagent Pre-Return Self-Corrections (Cohorts 1, 11, 16, 19, 21)**: The `ephemeral_translator` worker proactively invoked `run_small_pause_gate.py` before ending its turn, caught a minor footnote count or pronoun capitalization slip, repaired the file itself, and returned a 100% passing cohort to the orchestrator.
- **5 Orchestrator Auto-Healed Events (Cohorts 4, 12, 22, 23, 27)**: Caught during the orchestrator's `--verify-cohort` call and **100% repaired in $< 1$ second by `attempt_deterministic_self_healing()`** in [`scripts/autonomous_orchestrator.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/autonomous_orchestrator.py#L215-L340) with zero subagent retries:

| Cohort | Gate Triggered | Exact Anomaly Caught | Deterministic Self-Healer Action (`attempt_deterministic_self_healing()`) |
|---|---|---|---|
| **Cohort 4** | Gate 4 ([`structural_audit.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/structural_audit.py)) | `UNSANCTIONED_H1_HEADING (L188, leaf p39): '# A Brief Explanation Concerning the Holy Proskomedia[^133]' does not match any authorized publication landmark` | **Step 1B (Heading Demotion)**: Automatically demoted unsanctioned `#` $\rightarrow$ `## A Brief Explanation Concerning the Holy Proskomedia[^133]`. |
| **Cohort 12** | Gate 2 ([`hieratic_pronoun_audit.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/hieratic_pronoun_audit.py)) | `1 violations detected` (lowercase Trinity Deity pronoun in prayer clause) | **Step 4 (Deity Pronoun Capitalizer)**: Automatically capitalized the pronoun via context-aware regex. |
| **Cohort 22** | Gate 2 ([`hieratic_pronoun_audit.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/hieratic_pronoun_audit.py)) | `1 violations detected` (lowercase Trinity Deity pronoun in rubric/prayer) | **Step 4 (Deity Pronoun Capitalizer)**: Automatically capitalized the pronoun via context-aware regex. |
| **Cohort 23** | Gate 1A ([`lint_vocabulary.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/ scripts/run_small_pause_gate.py)) | Forbidden vocabulary variant against `master_liturgical_vocabulary.json` | **Step 3 (Lexicon Enforcer)**: Applied 1-to-1 deterministic replacement from `master_liturgical_vocabulary.json`. |
| **Cohort 27** | Gate 1A ([`lint_vocabulary.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/run_small_pause_gate.py)) | Forbidden vocabulary variant against `master_liturgical_vocabulary.json` | **Step 3 (Lexicon Enforcer)**: Applied 1-to-1 deterministic replacement from `master_liturgical_vocabulary.json`. |

### 2.2 Phase 2 Publication Verification Failure Modes (`verify_publication_edition.py`)

While Phase 1 achieved a 100% pass rate with zero retries, Phase 2 compilation (`--compile-publication`) exposed **4 critical gap areas** between Phase 1's `run_small_pause_gate.py` and Phase 2's [`verify_publication_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/verify_publication_edition.py):

1. **Failure Mode A — Mandate 12 vs. Gate 1 `[Blank leaf ...]` Collision (Cohorts 12 & 13, Leaves `p119` & `p127`)**:
   - *What Happened*: On Leaf `p119L` (fol. 119v, blank verso before the Liturgy of St. Basil) and Leaf `p127L` (fol. 127v, blank verso before the engraved portrait of St. Basil), the `Flash` workers obeyed Work Order Statutory Mandate 12 by writing `*[Blank leaf with show-through from the recto]*[^392]` and `*[Blank leaf with show-through from the verso woodcut]*[^415]`. Both passed Phase 1 (`run_small_pause_gate.py`), but failed Phase 2 Gate 1 (`verify_publication_edition.py` L224), which bans `r"\*?\[Blank\s+[^\]]+\]\*?"`.
   - *Source Guardrail & Healer Fix*: Update [`work_order_template.md`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/data/templates/work_order_template.md) Mandate 12 to instruct workers to format blank-page codicological notes using italic parentheses `*(Blank page with show-through...)*` (never square brackets `[Blank ...]`), and add a regex pass in `attempt_deterministic_self_healing()`:
     ```python
     draft_text = re.sub(r"\*?\[([Bb]lank\s+[^\]]+)\]\*?", r"*(\1)*", draft_text)
     ```

2. **Failure Mode B — Stripped 2-Up Milestone Orphaning Footnote Marker `[^516]` (Cohort 18, Leaf `p178`)**:
   - *What Happened*: On Leaf `p178R` (fol. 179r, p. 346), the `Flash` subagent attached footnote marker `[^516]` directly to the 2-up folio milestone header: `**[Right Page — Fol. 179r (p. 346)]**[^516]`. Because `reconcile_footnotes.py` scans the raw draft before milestones are stripped, Cohort 18 passed Gate 3 (`20/20` markers paired). However, during Phase 2 compilation, [`compile_final_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/compile_final_edition.py#L121-L125) (`_purge_and_stitch()`) deletes every `**[Left/Right Page — ...]**` line, which silently destroyed `[^516]` in the body text and triggered `Gate 2 FAILED: Orphaned definitions in master: [516]`.
   - *Source Guardrail & Healer Fix*: In `attempt_deterministic_self_healing()` and `_purge_and_stitch()`, before stripping any `=== LEAF pN ===` or `**[Left/Right Page ...]**` line, extract any trailing `(\[\^\d+\])+` markers and append them to the next non-empty rubric/heading/body line.

3. **Failure Mode C — Unparenthesized Cyrillic in Generated HTML Anchor Slug `<a id="...">` (`compile_final_edition.py` L40)**:
   - *What Happened*: `slugify()` in [`compile_final_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/compile_final_edition.py#L40-L45) uses `re.sub(r'[^\w\s-]', '', cleaned, flags=re.UNICODE)`, which preserves Cyrillic letters from `master_title` inside `<a id="1604-striatyn-liturgikon-of-hedeon-balaban-служебник-стрятин-друкарня-балабанів-1604"></a>` on Line 1 of `_complete.md` and `_part0_front_matter.md`. Because the Cyrillic inside `id="..."` has no parentheses around it, [`verify_publication_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/verify_publication_edition.py#L387-L394) Gate 5A immediately flags Line 1 as `[FAIL] Unparenthesized Cyrillic in body/heading`.
   - *Source Healer Fix*: Strip parenthetical Cyrillic or non-ASCII characters inside `slugify()` (`re.sub(r'[^a-z0-9\s-]', '', cleaned)`) and strip HTML tags (`re.sub(r'<[^>]+>', '', line)`) before running the Gate 5A Cyrillic check in `verify_publication_edition.py`.

4. **Failure Mode D — Nested Parentheses Before Cyrillic in Editorial Notes (Cohort 28, Leaf `p273`)**:
   - *What Happened*: On Leaf `p273R`, the worker wrote an italicized parenthetical editorial note containing both an inner parenthetical page citation `(pp. 527–528)` and a Cyrillic title `` `МОЛИТВЫ ВЕЧЕРНЇА` ``. Gate 5A's single-level regex `re.sub(r'\([^\)]*[\u0400-\u04FF][^\)]*\)', '', line)` stopped at the first closing parenthesis `528)`, leaving the Cyrillic title exposed and failing Gate 5A in Phase 2.
   - *Source Guardrail & Healer Fix*: Port Gate 5A's unparenthesized-Cyrillic check directly into Phase 1's `run_small_pause_gate.py`, and add a deterministic healer in `attempt_deterministic_self_healing()` that wraps bare Cyrillic runs `([\u0400-\u04FF][\u0400-\u04FF\s\u0483-\u0489,.;:!?—–-]*)` in `(*\1*)` when not already enclosed in immediate parentheses.

---

## 3. Argon Review Queue Signal Precision (`argon_review_queue.json`)

### 3.1 Empirical Audit of the 59 Queued Leaves

During Phase 1, `collect_argon_review_signals()` ([`scripts/run_small_pause_gate.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/run_small_pause_gate.py#L188-L255)) queued **59 out of 293 physical leaves (20.14%)** into [`argon_review_queue.json`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/Liturgical%20Monuments/Monument%20-%201604_striatyn_balaban_liturgikon/Audit_Reports/argon_review_queue.json):

| Argon Queue Signal | Queued Leaves | % of Queue | True Positives (Genuine Crux) | False Positives (Signal Noise) | Signal Precision |
|---|---:|---:|---:|---:|---:|
| **Signal 1: `epigraphic_uncertainty`** (`[?]`, `[illegible]`, `[lacuna]`) | 0 | 0.0% | 0 | 0 | N/A |
| **Signal 2: `borderline_sgc02_ratio`** (`< 0.50` or `> 2.20`) | 1 (`p188`) | 1.7% | 0 (expected rubric expansion `2.37`) | 1 | **0.0%** |
| **Signal 3A: `high_complexity_table`** (`>= 5` table rows) | 0 | 0.0% | 0 | 0 | N/A |
| **Signal 3B: `dense_polyglot_apparatus`** (`>= 5` footnotes on leaf) | 58 | 98.3% | **8 leaves** (`p4, p5, p252, p269, p273, p274, p281, p291`) | **50 leaves** | **13.8%** |
| **Signal 4: `QUARANTINED_FOR_ARGON`** (failed 1 retry) | 0 | 0.0% | 0 | 0 | N/A |
| **Total Queued Leaves** | **59** | **100.0%** | **8 leaves** | **51 leaves** | **13.56%** |

### 3.2 Root Cause of the 86.4% False-Positive Rate & Missed False Negatives

1. **Why 50/58 `dense_polyglot_apparatus` Leaves Were False Positives**:
   - `collect_argon_review_signals()` hardcodes `if len(fn_markers) >= 5:` per physical `=== LEAF pN ===` block.
   - However, `1604_striatyn_balaban_liturgikon` is a **2-up open-spread facsimile** where every physical leaf contains **two printed pages** (verso + recto). Five footnotes across two printed pages is only **2.5 footnotes per page**—standard density for Euchologion prayers, litanies, and dismissal formulas (e.g., Cohort 26's Daily and Festal Dismissals had 76 routine patristic/feast footnotes across 10 spreads, queuing 10/10 leaves in Cohort 26 despite zero epigraphic uncertainty).
2. **Why `p188` Triggered a False-Positive `borderline_sgc02_ratio` (`2.37`)**:
   - On Leaf `p188` (Cohort 19, Liturgy of the Presanctified Gifts), the printed Slavonic text uses ultra-compact nomina sacra and liturgical incipits (`Гд҃и воззвахъ`, `Да и҆справитсѧ`, `Слава, и҆ нынѣ`) totaling 935 characters, whereas the idiomatic English rubrical translation naturally expands abbreviated grammatical constructions to 2,220 characters (`ratio = 2.37`).
3. **False Negatives (Genuine Physical Lacunae Missed by the 4 Signals)**:
   - Because Signal 1 only scans the English draft body for literal `[?]`, `[illegible]`, or `[lacuna]` strings, **four major physical binding anomalies and lost leaves** documented by the workers in footnotes with `< 5` footnotes on the leaf were **never queued for Argon**:
     - **Cohort 7 (`p66`–`p67`)**: Binder's transposition of the outer bifolia of Quire Zh (`ж`) and Quire Z (`з`) during historical rebinding (only 3 footnotes on leaf $\rightarrow$ not queued).
     - **Cohort 14 (`p131`, `p133`–`p134`)**: Printer's pagination jump (`241` $\rightarrow$ `244`) and physically lost Folio 132 (pp. 246–247), breaking off the Prayer of the Trisagion mid-sentence (only 2 footnotes on leaf $\rightarrow$ not queued).
     - **Cohort 15 (`p149`–`p150`)**: Physically lost leaf between `p149R` (p. 283) and `p150L` (p. 286), causing a 2-page chasm mid-Cherubic Prayer (only 2 footnotes on leaf $\rightarrow$ not queued).
     - **Cohort 16 (`p159`–`p160`)**: Physically lost leaf between `p159R` (p. 305) and `p160L` (p. 308) mid-Basil Anaphora (only 2 footnotes on leaf $\rightarrow$ not queued).

### 3.3 Genre-Specific Calibration Formula for 2-Up `rubrical` Monuments

1. **Scale Footnote Threshold by `pages_per_leaf`**: Detect 2-up layout (via presence of `**[Left Page` / `**[Right Page` milestones or `codex_registry.json` metadata) and set `max_footnotes_threshold = 5 * pages_per_leaf` (`>= 10` footnotes per physical 2-up leaf, vs. `>= 5` for 1-up leaves). Applying `>= 10` to `1604_striatyn_balaban_liturgikon` immediately drops false positives from 50 to 2 while retaining `p291` (the Errata leaf, 10 footnotes).
2. **Add Signal 5 (`codicological_or_textual_discontinuity`)**: Scan both the leaf's draft block and its paired footnote definitions in `cohortK_footnotes.txt` for keywords indicating physical or textual anomalies:
   ```python
   CRUX_KEYWORDS_RE = re.compile(
       r"\b(?:misbound|transpos(?:ed|ition)|lacuna|missing\s+(?:folio|leaf|page)|"
       r"lost\s+(?:folio|leaf)|compositor|errata|breaks\s+off\s+mid-|out\s+of\s+sequence|sic)\b",
       re.IGNORECASE,
   )
   ```
   This captures 100% of the genuine codicological cruxes (`p66, p67, p131, p133, p149, p159, p269, p273, p281, p291`) with high precision.
3. **Widen `borderline_sgc02_ratio` Upper Bound for `rubrical` Codex Leaves**: Increase the upper `SGC-02` queue threshold from `2.20` to `2.45` for `rubrical` monuments where abbreviated Slavonic rubrics/titla expand in English.

---

## 4. Monument-Type & Compiler Edge Cases (`compile_final_edition.py`)

| Edge Case ID | Component / Function | Empirical Observation in `1604_striatyn_balaban_liturgikon` | Architectural Resolution |
|---|---|---|---|
| **EC-01: 2-Up Mid-Sentence Seam Stitching** | [`compile_final_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/compile_final_edition.py#L140-L157) (`_purge_and_stitch()`) | Across 293 physical leaves, `_purge_and_stitch()` stripped **582** `**[Left/Right Page — Fol. ...]**` milestones and successfully stitched **211 mid-sentence page breaks** where a prayer or rubric began on a verso (`Left Page`) or recto (`Right Page`) and continued in lowercase on the next page. | Works reliably when both lines are plain prose or both are italicized rubrics (`*...*`), but fails if a footnote marker `[^N]` is attached to the stripped milestone line itself (see **EC-02**). |
| **EC-02: Footnote Orphaning on Stripped Milestones** | [`compile_final_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/compile_final_edition.py#L121-L125) | In Cohort 18 Leaf `p178`, `**[Right Page — Fol. 179r (p. 346)]**[^516]` was stripped by `_purge_and_stitch()`, deleting `[^516]` from the compiled body and failing Gate 2 (`Orphaned definitions in master: [516]`). | Before `continue` on stripped `=== LEAF` or `**[Left/Right Page` lines, rescue all `re.findall(r'\[\^\d+\]', stripped)` markers and prepend/append them to the next surviving text line. |
| **EC-03: Cyrillic Leak in Master Title HTML Anchor Slug** | [`compile_final_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/compile_final_edition.py#L40-L45) (`slugify()`) | `slugify(master_title)` preserved Cyrillic from `(Служебник, Стрятин: Друкарня Балабанів, 1604)` inside `<a id="..."></a>` on Line 1 of `_complete.md` and `_part0_front_matter.md`, causing `verify_publication_edition.py` Gate 5A to fail on Line 1. | Restrict `slugify()` to ASCII alphanumeric characters (`re.sub(r'[^a-z0-9\s-]', '', cleaned)`) or strip parenthetical subtitles prior to slug generation. |
| **EC-04: Mandate 12 Blank-Leaf Bracket Collision** | [`verify_publication_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/verify_publication_edition.py#L224) (Gate 1) | Gate 1 bans `r"\*?\[Blank\s+[^\]]+\]\*?"`, colliding with Mandate 12's requirement to describe blank versos (`p119L`, `p127L`) inside woodcut/title cohorts. | Standardize blank-leaf notes to italic parentheses `*(Blank leaf ...)*` in `work_order_template.md` and auto-convert `[Blank ...]` $\rightarrow$ `*(Blank ...)*` in `_purge_and_stitch()`. |
| **EC-05: Universal Gate 1C Cinnabar Warning Noise** | [`chromatic_rubric_verifier.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/chromatic_rubric_verifier.py) | **290 out of 293 leaves (99.0%)** emitted `[GATE 1C WARNING] Leaf pN rubric lacks verified red pigment` because 1604 Striatyn oxidized cinnabar/vermilion ink on yellowed rag paper has lower HSV saturation/hue separation than modern digital red. | Calibrate HSV red/vermilion thresholds for pre-1700 rag-paper scans (allowing warmer orange-brown/brick-red vermilion hues relative to local paper background). |

---

## 5. Granular Atomic Tagging Blueprint (Propers & Non-Propers)

To enable a universal atomic extractor to parse 100% of `1604_striatyn_balaban_liturgikon` (and all sister `rubrical` Euchologia/Sluzhebnyky) from `Cohorts/*.md` into `{monument_id}_atomic_corpus.json`, the following **15 distinct liturgical unit classes** and their exact empirical regex patterns were inventoried across all 30 cohorts:

### 5.1 Structural Containers & Coordinate Milestones

| Atomic Unit Class | Empirical Count | Exact Markdown / Regex Pattern in `Cohorts/*.md` | Extraction Role |
|---|---:|---|---|
| `PART_LANDMARK_H1` | **4** | `^#\s+(PART\s+[IVX]+:\s+.+?)(?:\[\^\d+\])?\s*$` | Top-level codex division (`Part I`..`Part IV`) |
| `SERVICE_HEADPIECE_H2` | **19** | `^##\s+(.+?)(?:\[\^\d+\])?\s*$` | Major office/service boundary (Chrysostom, Basil, Presanctified, Vespers, Matins, Dismissals, Kolyvo, Colophon, Errata) |
| `LEAF_BOUNDARY` | **293** | `^===\s+LEAF\s+p(\d+)\s+===\s*$` | Physical PDF leaf coordinate anchor (`p1`..`p293`) |
| `FOLIO_PAGE_MILESTONE_2UP` | **582** | `^\*\*\[(Left|Right)\s+Page\s+—\s+Fol\.\s+([^\]]+)\]\*\*(?:\[\^\d+\])?\s*$` | Exact recto/verso folio and printed page coordinate (`Fol. 1r`..`Fol. 291v`) |

### 5.2 Fixed Non-Propers (Euchologion Core)

| Atomic Unit Class | Empirical Count | Exact Markdown / Regex Pattern in `Cohorts/*.md` | Liturgical Description |
|---|---:|---|---|
| `SACERDOTAL_PRAYER_HEADER` | **77** | `^\*((?:The\s+)?(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Another)?\s*Prayer\b[^*\n]*)\*(?:\[\^\d+\])?\s*$` | Rubrical title introducing a priestly secret or aloud prayer (e.g., `*The First Prayer of the Faithful, after the unfolding of the eiliton:*`, `*First Prayer at Matins:*`) |
| `PRIEST_UTTERANCE` | **650** | `^\*\*Priest:\*\*\s+(.+)$` | Spoken sacerdotal prayers, blessings, peace greetings, and ecphoneses |
| `DEACON_UTTERANCE` | **404** | `^\*\*Deacon:\*\*\s+(.+)$` | Diaconal litany petitions (Great, Small, Augmented, Catechumens, Faithful, Litiya, Kolyvo), commands (`Bless, master`, `Wisdom! Let us attend`), and incensing formulas |
| `CHOIR_OR_CLERGY_RESPONSE` | **256** | `^\*\*(Choir|People|Choirs|Clergy|Reader|Chanters):\*\*\s+(.+)$` | Fixed choral responses (`Lord, have mercy`, `Grant this, O Lord`, `Amen`, Cherubic Hymn, Anaphora responses) |
| `ECPHONESIS_EXCLAMATION_RUBRIC` | **73** | `\*((?:And\s+the\s+)?(?:Exclamation|exclama[tion]+|Loudly|Aloud)[^*\n]*)\*` | Marker separating the secret body of a sacerdotal prayer from its audible concluding doxology (`*Exclamation:*`) |
| `PROCEDURAL_RUBRIC_ITALIC` | **1,468** | `^\*([^*\n]+)\*(?:\[\^\d+\])?\s*$` | Ceremonial actions in Active Present Indicative (vesting, Proskomedia particle placement, censing, bowing, fraction, communion) |
| `PARATEXT_WOODCUT_OR_BINDING_NOTE` | **24** | `^(?:\*\()?\[(Front|Rear|Verso|First|Second|Ornate|Full-Page|Architectural|Woodcut)[^\]]+\](?:\)\*)?` | Bracketed diplomatic descriptions of binding boards, woodcut engravings (St. John Chrysostom `p43R`, St. Basil `p127R`), heraldic arms (`p5L`), and flyleaves |

### 5.3 Variable Propers Embedded in the Liturgikon

| Atomic Unit Class | Empirical Count | Exact Markdown / Regex Pattern in `Cohorts/*.md` | Liturgical Description |
|---|---:|---|---|
| `WEEKLY_AND_FESTAL_APOLYSIS_RUBRIC` | **25** | `^\*(Dismissal\s+(?:on|for|of)\b[^*\n]+|On\s+(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)\b[^*\n]*dismissal[^*\n]*)\*(?:\[\^\d+\])?\s*$` | Rubrics introducing the 7 Daily Dismissals (Sunday–Saturday) and 18 Dominical/Marian/Sanctoral Festal Dismissals (`p256R`–`p261L`, Cohorts 26–27) |
| `TROPARION_OR_HYPAKOE_STANZA` | **18** | `^\*([^\n*]*\b(?:Troparion|Hypakoe|Kontakion|Theotokion|Sticheron|Stichera|Evlogitaria)\b[^*\n]*)\*(?:\[\^\d+\])?\s*(.*)$` | Embedded hymnographic propers (Proskomedia & Deposition troparia, Paschal hours troparia/hypakoe, St. Basil & St. Gregory Dialogos troparia/kontakia, Resurrectional Evlogitaria, Wine-Blessing troparion) |
| `PODOBEN_MELODIC_HEADER` | **1** | `^\*Tone\s+([1-8]),\s+Podoben:\s+"([^"]+)"\s+\(([^\)]+)\):\*` | 3-layer canonical Podoben header on `p252L` (Cohort 26): `*Tone 6, Podoben: "Having set all aside" (Всеѿложивше):*` |
| `PASCHAL_ODE_EKTENIA_EXCLAMATION` | **9** | `^\*(After\s+the\s+(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth)\s+Ode[^*\n]*)\*` | Special Paschal Matins rubric-exclamation pairs specifying the exact priestly ecphonesis after each Ode of the Paschal Canon (`p263R`–`p264R`, Cohort 27) |

---

## 6. Top 5 Concrete Engine Hardening Recommendations

Based on the empirical evidence from `1604_striatyn_balaban_liturgikon`, we recommend the following **5 ranked code and template hardening upgrades** across `scripts/` and `data/templates/`:

### Rank 1: Rescue Trailing Footnote Markers & Sanitize Blank-Leaf Brackets During Self-Healing and Compilation
- **Target Files & Functions**:
  - [`scripts/compile_final_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/compile_final_edition.py#L111-L165) $\rightarrow$ `_purge_and_stitch()`
  - [`scripts/autonomous_orchestrator.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/autonomous_orchestrator.py#L215-L340) $\rightarrow$ `attempt_deterministic_self_healing()`
  - [`data/templates/work_order_template.md`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/data/templates/work_order_template.md) $\rightarrow$ Statutory Mandate 12
- **Empirical Evidence**: Prevented 3 Phase 2 gate failures in Cohorts 12, 13, and 18 (`*[Blank leaf ...]*` matching Gate 1's `[Blank ...]` regex on `p119`/`p127`, and `**[Right Page — Fol. 179r (p. 346)]**[^516]` losing `[^516]` when `_purge_and_stitch()` stripped the 2-up milestone line).
- **Actionable Implementation**:
  1. In `_purge_and_stitch()`, before skipping any `=== LEAF` or `**[Left/Right Page` line, capture `orphan_fns = re.findall(r'\[\^\d+\]', stripped)` and append them to the next non-empty line in `purged`.
  2. In `attempt_deterministic_self_healing()` and `_purge_and_stitch()`, rewrite `r"\*?\[([Bb]lank\s+[^\]]+)\]\*?"` $\rightarrow$ `r"*(\1)*"`.
  3. In `work_order_template.md` Mandate 12, change the blank-page example to `*(Blank page with show-through from the recto)*`.

### Rank 2: Normalize Argon Queue Footnote Threshold by `pages_per_leaf` (2-Up Aware) & Add Signal 5 (`codicological_discontinuity`)
- **Target Files & Functions**:
  - [`scripts/run_small_pause_gate.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/run_small_pause_gate.py#L188-L255) $\rightarrow$ `collect_argon_review_signals()`
- **Empirical Evidence**: 50 of 59 queued leaves (84.7%) were false positives triggered solely because 2-up spreads contain 2 printed pages (`>= 5` footnotes per spread = only 2.5 footnotes per page), while 4 genuine physical lacunae/transpositions (`p66–p67`, `p133–p134`, `p149–p150`, `p159–p160`) had `< 5` footnotes and were missed.
- **Actionable Implementation**:
  1. Detect 2-up leaves in `collect_argon_review_signals()` (`is_2up = bool(re.search(r"\*\*\[(?:Left|Right)\s+Page", block))`) and set `fn_threshold = 10 if is_2up else 5`.
  2. Add Signal 5 scanning the leaf's draft text and its corresponding footnote definitions for `r"\b(?:misbound|transpos|lacuna|missing\s+(?:folio|leaf|page)|lost\s+(?:folio|leaf)|compositor|errata|breaks\s+off\s+mid-)\b"`.

### Rank 3: Strip Non-ASCII Characters in `slugify()` and Strip HTML Tags Before Gate 5A Cyrillic Verification
- **Target Files & Functions**:
  - [`scripts/compile_final_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/compile_final_edition.py#L40-L45) $\rightarrow$ `slugify()`
  - [`scripts/verify_publication_edition.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/verify_publication_edition.py#L384-L395) $\rightarrow$ `verify_monument_publication()` (Gate 5A)
- **Empirical Evidence**: Every monument whose `master_title` contains a parenthetical Cyrillic title generates `<a id="...-служебник-..."></a>` on Line 1 of `_complete.md` and `_part0_front_matter.md`, which fails Gate 5A because the Cyrillic inside the HTML `id` attribute is not enclosed in `(...)`.
- **Actionable Implementation**:
  1. In `compile_final_edition.py:slugify()`, strip parenthetical substrings and non-ASCII characters: `cleaned = re.sub(r'[^a-z0-9\s-]', '', cleaned)`.
  2. In `verify_publication_edition.py` Gate 5A, strip HTML tags (`clean_line = re.sub(r'<[^>]+>', '', line)`) and iteratively strip innermost parentheses (`while re.search(r'\([^\(\)]*\)', clean_line): clean_line = re.sub(r'\([^\(\)]*\)', '', clean_line)`) so nested parentheses in editorial notes do not cause false positives.

### Rank 4: Unify Phase 1 (`run_small_pause_gate.py`) and Phase 2 (`verify_publication_edition.py`) Linter Invariants
- **Target Files & Functions**:
  - [`scripts/run_small_pause_gate.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/run_small_pause_gate.py) $\rightarrow$ `run_gate()`
  - [`scripts/autonomous_orchestrator.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/autonomous_orchestrator.py) $\rightarrow$ `attempt_deterministic_self_healing()`
- **Empirical Evidence**: All 4 issues that surfaced during Phase 2 compilation (blank-leaf brackets, footnote markers on 2-up milestones, unparenthesized Cyrillic in body notes) were already present in the Phase 1 cohort drafts (`Draft/`) but were not checked by `run_small_pause_gate.py`.
- **Actionable Implementation**: Add lightweight Phase 1 checks in `run_small_pause_gate.py` (and matching deterministic healers in `attempt_deterministic_self_healing()`) for: (a) unparenthesized Cyrillic in body/headings, (b) `[Blank ...]` bracketed placeholders, and (c) `[^N]` markers placed on `=== LEAF` or `**[Left/Right Page` structural lines.

### Rank 5: Inject Inter-Cohort Quire Signature & Folio Continuity State into `generate_work_order.py`
- **Target Files & Functions**:
  - [`scripts/generate_work_order.py`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/scripts/generate_work_order.py) $\rightarrow$ `generate_work_order()`
  - [`data/templates/work_order_template.md`](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Translation/data/templates/work_order_template.md)
- **Empirical Evidence**: In Cohort 27 (`p269R`), Folio 2 of Quire Ya (`ѧ҃ в`, pp. 527–528) was missing after `fol. 269v`, and then appeared misbound in Cohort 28 (`p273R`–`p274L`) inside the Seventh Prayer of Light. Because Cohort 28's work order only included the last 3 lines of prose from Cohort 27 (`inter_cohort_context`), the Cohort 28 worker spent an extra ~5.4 minutes diagnosing the dislocation from scratch.
- **Actionable Implementation**: Have `generate_work_order.py` parse the final `**[Left/Right Page — Fol. ...]**` header and any codicological anomaly footnotes from Cohort $K-1$ and inject a 3-line **Codicological Continuity Header** (`Last Folio/Page`, `Active Service/Section`, and `Open Binding/Lacuna Alerts`) into Cohort $K$'s work order.
