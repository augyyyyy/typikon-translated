# Autonomous Monument Translation Directive: Typikon of Fr. Jacob Doskovsky (Peremyshl, 1852)
## Complete Unabridged Translation Execution Specification across All 15 Cohorts

> [!IMPORTANT]
> **Sovereign Autonomous Execution Mandate (Rule 14 of `.agents/AGENTS.md`)**  
> This directive equips the Automator / Worker Agent with the **complete codex partition schedule and autonomous loop controller** for **Typikon of Fr. Jacob Doskovsky (Peremyshl, 1852)** (141 physical facsimile leaves / ~280 printed book pages).  
> **Zero Inter-Cohort Human Stalls**: The Automator executes continuously through Cohort 1 to Cohort 15, triggering backend Small Pause Gates (`scripts/run_small_pause_gate.py`) automatically between cohorts.  
> Execution yields to the Human Operator **strictly and exclusively at the Sovereign Grand Pause** when 100% of all 141 leaves are translated and assembled (`remaining_pages == 0`).

---

## 1. Codex Transmission Metadata & Conservation Scope
* **Monument ID**: `1852_doskovsky_typikon`
* **Title**: Typikon of Fr. Jacob Doskovsky (Peremyshl, 1852)
* **Church Slavonic Title**: *Тvпїко́нъ, си́рѣчь : Оу҆ста́въ церковнагѡ пѣ́нїа и҆ ѡ҆со́беннагѡ правилочте́нїа... сочине́нъ и напеча́танъ въ Перемышли, въ Книгопеча́тни собо́рнои ру́сскои Капитꙋ́лы, 1852*
* **Author**: Fr. Jacob [Yakiv] Doskovsky, Vicar in Peremyshliany (`Їа́кѡвъ Доско́вскїй, Вика́рїй въ Пере́мышлан`)
* **Press & Date**: Printing House of the Ruthenian Cathedral Chapter, Peremyshl; completed 23 October 1852 O.S.
* **Source Facsimile**: `Historical Typikons/1852-Typikon-Doskovsky.pdf`
* **Total Physical Pages**: **141 leaves** (Leaf `p1` is single title page; leaves `p2`–`p141` are two-page spreads containing 272 numbered book pages + 6 unnumbered table/index pages = ~280 printed book pages total)
* **Spread Coordinate Demarcation**: Primary leaf banner `<!-- LEAF: p{N} -->` at the top of each spread, with sub-delimiters `[Book Page {L}]` and `[Book Page {R}]` indicating internal page turns.
* **Cohort Bounding**: Strictly **10 physical facsimile leaves** per cohort (final Cohort 15 = 1 leaf)
* **Total Scheduled Cohorts**: **15 cohorts**
* **Governing Register**: **RUBRICAL** (Per Master Translation Standard MTS-1)
* **Mathematical Conservation**:
  $$\mathbf{Total\ Physical\ Pages\ in\ Codex} \equiv \sum_{k=1}^{15} C_k = (14 \times 10) + 1 = 141 \text{ Leaves (100.0% Closed Conservation)}$$

---

## 2. Inviolable Liturgical Translation Standards (MTS-1 / TA-1)

### A. Universal Native Vision Mandate (Physical Ink Sovereignty)
* Inspect each 300 DPI image (`p{N}.png`) in `Liturgical Monuments/Monument 4 - 1852 Doskovsky Typikon/Source Text/images/` directly.
* Cinnabar Rubrics: Red ink is visually identified and rendered in ceremonial italics (`*...*`); black ink is rendered in spoken/chanted prayers, psalmody, and hymnography.

### B. Ceremonial / Rubrical Register Norms (RUBRICAL)
* Concise, imperative, and active: Use **Active Present Indicative** for all rubrical actions (*"The Priest enters the sanctuary, venerates the Holy Table, and begins..."*).
* Absolute prohibition of gratuitous legalistic *"shall"*s in ordinary liturgical rubrics.

### C. Byzantine-Ruthenian Realia & Melodic Headings
* Technical Loanwords mandatory: `Tetrapod` (never "center table"), `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
* Ruthenian Chant Headings: Tone designations must be **`Tone 1`** through **`Tone 8`** (never Greek "Mode I").
* Model Melodies: **`Podoben: "[Canonical Incipit]"`**, **`Samohlasen`** (proper melody), **`Samopodoben`**.
* Dual Incipits: Bold English followed by italicized Slavonic (*"Lord, I have cried"* (*Господи воззвахъ*)).

### D. Father Paul Doxology Standard & Hieratic Pronouns
* Full choral: *"Glory be to the Father, and to the Son, and to the Holy Spirit, now and forever, and unto the ages of ages. Amen."*
* Shorthand rubric: *"Glory... Now and forever, and unto the ages of ages:"*
* **Strict Ban**: The phrase *"for ever and ever"* is 100% prohibited.
* **100% Deity Pronoun Capitalization**: Mandatory capitalization for Divine Persons (*He, Him, His, Thou, Thee, Thy, Thine*). Clergy, celebrants, saints, and rubrical "he" remain lowercase.

### E. Scripture & Psalter (Septuagint LXX)
* Mandatory Septuagint versification across all psalm citations and biblical references.

### F. Footnote Bijectivity
* Continuous monotonic numbering across the monument: Every `[^N]` in body text must have a matching `[^N]:` definition.

---

## 3. Autonomous Multi-Cohort Loop Controller Specification

For each cohort $k \in [1, 15]$:

```
[COHORT LOOP: k = 1 to 15]
  1. INGESTION : Verify/render 300 DPI leaves p{start}..p{end} in 'Liturgical Monuments/Monument 4 - 1852 Doskovsky Typikon/Source Text/images/'
  2. TRANSCRIPTION : Transcribe source ink into 'Liturgical Monuments/Monument 4 - 1852 Doskovsky Typikon/Source Text/1852_doskovsky_typikon_cohort{k}_source.txt'
  3. TRANSLATION : Draft unabridged English into 'Liturgical Monuments/Monument 4 - 1852 Doskovsky Typikon/Draft/1852_doskovsky_typikon_cohort{k}_raw_draft.md'
  4. FOOTNOTES : Write definitions into 'Liturgical Monuments/Monument 4 - 1852 Doskovsky Typikon/Draft/1852_doskovsky_typikon_cohort{k}_footnotes.txt'
  5. SMALL PAUSE GATE : Run 'python scripts/run_small_pause_gate.py --monument 1852_doskovsky_typikon --cohort {k}'
     - Gate 1: Shared_Lexicon/lint_vocabulary.py (0 violations)
     - Gate 2: scripts/hieratic_pronoun_audit.py (100% Deity capitalization)
     - Gate 3: scripts/reconcile_footnotes.py (1:1 footnote parity)
     - Gate 4: scripts/structural_audit.py (unbroken sequence)
  6. INTEGRATION : Run 'python scripts/assemble_and_sync_hub.py --monument 1852_doskovsky_typikon --cohort {k}'
     - Promotes Draft -> Final MD & Final
     - Appends footnotes to Final_footnotes.txt
     - Advances ACTIVE_ORCHESTRATOR_STATE.json
  7. NEXT COHORT : If k < 15, immediately advance to cohort k+1. DO NOT pause for human input!
[END LOOP at k = 15 -> REACHED SOVEREIGN GRAND PAUSE]
```

---

## 4. Complete Codex Partition Schedule (15 Cohorts)

| Cohort | Physical Pages | Leaf Count | Status | Target Deliverables |
|---|---|---|---|---|
| **Cohort 01** | pp. 1–10 | 10 leaves | `PENDING` | `cohort01_source.txt` / `raw_draft.md` |
| **Cohort 02** | pp. 11–20 | 10 leaves | `PENDING` | `cohort02_source.txt` / `raw_draft.md` |
| **Cohort 03** | pp. 21–30 | 10 leaves | `PENDING` | `cohort03_source.txt` / `raw_draft.md` |
| **Cohort 04** | pp. 31–40 | 10 leaves | `PENDING` | `cohort04_source.txt` / `raw_draft.md` |
| **Cohort 05** | pp. 41–50 | 10 leaves | `PENDING` | `cohort05_source.txt` / `raw_draft.md` |
| **Cohort 06** | pp. 51–60 | 10 leaves | `PENDING` | `cohort06_source.txt` / `raw_draft.md` |
| **Cohort 07** | pp. 61–70 | 10 leaves | `PENDING` | `cohort07_source.txt` / `raw_draft.md` |
| **Cohort 08** | pp. 71–80 | 10 leaves | `PENDING` | `cohort08_source.txt` / `raw_draft.md` |
| **Cohort 09** | pp. 81–90 | 10 leaves | `PENDING` | `cohort09_source.txt` / `raw_draft.md` |
| **Cohort 10** | pp. 91–100 | 10 leaves | `PENDING` | `cohort10_source.txt` / `raw_draft.md` |
| **Cohort 11** | pp. 101–110 | 10 leaves | `PENDING` | `cohort11_source.txt` / `raw_draft.md` |
| **Cohort 12** | pp. 111–120 | 10 leaves | `PENDING` | `cohort12_source.txt` / `raw_draft.md` |
| **Cohort 13** | pp. 121–130 | 10 leaves | `PENDING` | `cohort13_source.txt` / `raw_draft.md` |
| **Cohort 14** | pp. 131–140 | 10 leaves | `PENDING` | `cohort14_source.txt` / `raw_draft.md` |
| **Cohort 15** | pp. 141–141 | 1 leaves | `PENDING` | `cohort15_source.txt` / `raw_draft.md` |

---

## 5. Sovereign Grand Pause Termination
When Cohort 15 completes its Small Pause Gate and final integration:
- `remaining_pages == 0`
- The entire 141-page codex is assembled in `Liturgical Monuments/Monument 4 - 1852 Doskovsky Typikon/Final MD/1852_doskovsky_typikon_complete.md`
- Deliverables are synchronized to `Projects/Typikon Coded/Data/Inbox/1852_Doskovsky_Typikon/`
- Automator halts and delivers the final Grand Pause notification to the Human Operator.
