# Autonomous Monument Translation Directive: Typik of Fr. Isidore Dolnytsky (Lviv Stauropegion, 1899)
## Complete Unabridged Translation Execution Specification across All 30 Cohorts

> [!IMPORTANT]
> **Sovereign Autonomous Execution Mandate (Rule 14 of `.agents/AGENTS.md`)**  
> This directive equips the Automator / Worker Agent with the **complete codex partition schedule and autonomous loop controller** for **Typik of Fr. Isidore Dolnytsky (Lviv Stauropegion, 1899)** (591 physical pages).  
> **Zero Inter-Cohort Human Stalls**: The Automator executes continuously through Cohort 1 to Cohort 30, triggering backend Small Pause Gates (`scripts/run_small_pause_gate.py`) automatically between cohorts.  
> Execution yields to the Human Operator **strictly and exclusively at the Sovereign Grand Pause** when 100% of all 591 leaves are translated and assembled (`remaining_pages == 0`).

---

## 1. Codex Transmission Metadata & Conservation Scope
* **Monument ID**: `1899_dolnytsky_typikon`
* **Title**: Typik of Fr. Isidore Dolnytsky (Lviv Stauropegion, 1899)
* **Source Facsimile**: `Historical Typikons/1899-Typik-Dolnytsky-Church-Slavonic-Facsimile.pdf`
* **Total Physical Pages**: **591 leaves**
* **Cohort Bounding**: Strictly **20 physical pages** per cohort ($15 \le C \le 25$, final cohort = 11 leaves)
* **Total Scheduled Cohorts**: **30 cohorts**
* **Governing Register**: **RUBRICAL** (Per Master Translation Standard MTS-1)
* **Mathematical Conservation**:
  $$\mathbf{Total\ Physical\ Pages\ in\ Codex} \equiv \sum_{k=1}^{30} C_k = (29 \times 20) + 11 = 591 \text{ Leaves (100.0% Closed Conservation)}$$

---

## 2. Inviolable Liturgical Translation Standards (MTS-1 / TA-1)

### A. Universal Native Vision Mandate (Physical Ink Sovereignty)
* Inspect each 300 DPI image (`p{N}.png`) in `Liturgical Monuments/Monument 2 - 1899 Dolnytsky Typikon/Source Text/images/` directly.
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

For each cohort $k \in [1, 30]$:

```
[COHORT LOOP: k = 1 to 30]
  1. INGESTION : Verify/render 300 DPI leaves p{start}..p{end} in 'Liturgical Monuments/Monument 2 - 1899 Dolnytsky Typikon/Source Text/images/'
  2. TRANSCRIPTION : Transcribe source ink into 'Liturgical Monuments/Monument 2 - 1899 Dolnytsky Typikon/Source Text/1899_dolnytsky_typikon_cohort{k}_source.txt'
  3. TRANSLATION : Draft unabridged English into 'Liturgical Monuments/Monument 2 - 1899 Dolnytsky Typikon/Draft/1899_dolnytsky_typikon_cohort{k}_raw_draft.md'
  4. FOOTNOTES : Write definitions into 'Liturgical Monuments/Monument 2 - 1899 Dolnytsky Typikon/Draft/1899_dolnytsky_typikon_cohort{k}_footnotes.txt'
  5. SMALL PAUSE GATE : Run 'python scripts/run_small_pause_gate.py --monument 1899_dolnytsky_typikon --cohort {k}'
     - Gate 1: Shared_Lexicon/lint_vocabulary.py (0 violations)
     - Gate 2: scripts/hieratic_pronoun_audit.py (100% Deity capitalization)
     - Gate 3: scripts/reconcile_footnotes.py (1:1 footnote parity)
     - Gate 4: scripts/structural_audit.py (unbroken sequence)
  6. INTEGRATION : Run 'python scripts/assemble_and_sync_hub.py --monument 1899_dolnytsky_typikon --cohort {k}'
     - Promotes Draft -> Final MD & Final
     - Appends footnotes to Final_footnotes.txt
     - Advances ACTIVE_ORCHESTRATOR_STATE.json
  7. NEXT COHORT : If k < 30, immediately advance to cohort k+1. DO NOT pause for human input!
[END LOOP at k = 30 -> REACHED SOVEREIGN GRAND PAUSE]
```

---

## 4. Complete Codex Partition Schedule (30 Cohorts)

| Cohort | Physical Pages | Leaf Count | Status | Target Deliverables |
|---|---|---|---|---|
| **Cohort 01** | pp. 1–20 | 20 leaves | `PENDING` | `cohort01_source.txt` / `raw_draft.md` |
| **Cohort 02** | pp. 21–40 | 20 leaves | `PENDING` | `cohort02_source.txt` / `raw_draft.md` |
| **Cohort 03** | pp. 41–60 | 20 leaves | `PENDING` | `cohort03_source.txt` / `raw_draft.md` |
| **Cohort 04** | pp. 61–80 | 20 leaves | `PENDING` | `cohort04_source.txt` / `raw_draft.md` |
| **Cohort 05** | pp. 81–100 | 20 leaves | `PENDING` | `cohort05_source.txt` / `raw_draft.md` |
| **Cohort 06** | pp. 101–120 | 20 leaves | `PENDING` | `cohort06_source.txt` / `raw_draft.md` |
| **Cohort 07** | pp. 121–140 | 20 leaves | `PENDING` | `cohort07_source.txt` / `raw_draft.md` |
| **Cohort 08** | pp. 141–160 | 20 leaves | `PENDING` | `cohort08_source.txt` / `raw_draft.md` |
| **Cohort 09** | pp. 161–180 | 20 leaves | `PENDING` | `cohort09_source.txt` / `raw_draft.md` |
| **Cohort 10** | pp. 181–200 | 20 leaves | `PENDING` | `cohort10_source.txt` / `raw_draft.md` |
| **Cohort 11** | pp. 201–220 | 20 leaves | `PENDING` | `cohort11_source.txt` / `raw_draft.md` |
| **Cohort 12** | pp. 221–240 | 20 leaves | `PENDING` | `cohort12_source.txt` / `raw_draft.md` |
| **Cohort 13** | pp. 241–260 | 20 leaves | `PENDING` | `cohort13_source.txt` / `raw_draft.md` |
| **Cohort 14** | pp. 261–280 | 20 leaves | `PENDING` | `cohort14_source.txt` / `raw_draft.md` |
| **Cohort 15** | pp. 281–300 | 20 leaves | `PENDING` | `cohort15_source.txt` / `raw_draft.md` |
| **Cohort 16** | pp. 301–320 | 20 leaves | `PENDING` | `cohort16_source.txt` / `raw_draft.md` |
| **Cohort 17** | pp. 321–340 | 20 leaves | `PENDING` | `cohort17_source.txt` / `raw_draft.md` |
| **Cohort 18** | pp. 341–360 | 20 leaves | `PENDING` | `cohort18_source.txt` / `raw_draft.md` |
| **Cohort 19** | pp. 361–380 | 20 leaves | `PENDING` | `cohort19_source.txt` / `raw_draft.md` |
| **Cohort 20** | pp. 381–400 | 20 leaves | `PENDING` | `cohort20_source.txt` / `raw_draft.md` |
| **Cohort 21** | pp. 401–420 | 20 leaves | `PENDING` | `cohort21_source.txt` / `raw_draft.md` |
| **Cohort 22** | pp. 421–440 | 20 leaves | `PENDING` | `cohort22_source.txt` / `raw_draft.md` |
| **Cohort 23** | pp. 441–460 | 20 leaves | `PENDING` | `cohort23_source.txt` / `raw_draft.md` |
| **Cohort 24** | pp. 461–480 | 20 leaves | `PENDING` | `cohort24_source.txt` / `raw_draft.md` |
| **Cohort 25** | pp. 481–500 | 20 leaves | `PENDING` | `cohort25_source.txt` / `raw_draft.md` |
| **Cohort 26** | pp. 501–520 | 20 leaves | `PENDING` | `cohort26_source.txt` / `raw_draft.md` |
| **Cohort 27** | pp. 521–540 | 20 leaves | `PENDING` | `cohort27_source.txt` / `raw_draft.md` |
| **Cohort 28** | pp. 541–560 | 20 leaves | `PENDING` | `cohort28_source.txt` / `raw_draft.md` |
| **Cohort 29** | pp. 561–580 | 20 leaves | `PENDING` | `cohort29_source.txt` / `raw_draft.md` |
| **Cohort 30** | pp. 581–591 | 11 leaves | `PENDING` | `cohort30_source.txt` / `raw_draft.md` |

---

## 5. Sovereign Grand Pause Termination
When Cohort 30 completes its Small Pause Gate and final integration:
- `remaining_pages == 0`
- The entire 591-page codex is assembled in `Liturgical Monuments/Monument 2 - 1899 Dolnytsky Typikon/Final MD/1899_dolnytsky_typikon_complete.md`
- Deliverables are synchronized to `Projects/Typikon Coded/Data/Inbox/1899_Dolnytsky_Typikon/`
- Automator halts and delivers the final Grand Pause notification to the Human Operator.
