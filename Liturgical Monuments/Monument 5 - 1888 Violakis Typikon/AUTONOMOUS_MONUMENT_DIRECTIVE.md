# Autonomous Monument Translation Directive: Typikon of the Great Church of Christ by George Violakis (1888, Bilingual)
## Complete Unabridged Translation Execution Specification across All 117 Cohorts

> [!IMPORTANT]
> **Sovereign Autonomous Execution Mandate (Rule 14 of `.agents/AGENTS.md`)**  
> This directive equips the Automator / Worker Agent with the **complete codex partition schedule and autonomous loop controller** for **Typikon of the Great Church of Christ by George Violakis (1888, Bilingual)** (1170 physical pages).  
> **Zero Inter-Cohort Human Stalls**: The Automator executes continuously through Cohort 1 to Cohort 117, triggering backend Small Pause Gates (`scripts/run_small_pause_gate.py`) automatically between cohorts.  
> Execution yields to the Human Operator **strictly and exclusively at the Sovereign Grand Pause** when 100% of all 1170 leaves are translated and assembled (`remaining_pages == 0`).

---

## 1. Codex Transmission Metadata & Conservation Scope
* **Monument ID**: `1888_violakis_typikon`
* **Title**: Typikon of the Great Church of Christ by George Violakis (1888, Bilingual)
* **Source Facsimile**: `Historical Typikons/1888-Violakis-Typikon-Bilingual-Greek-English.pdf`
* **Total Physical Pages**: **1170 leaves**
* **Cohort Bounding**: Strictly **10 physical pages** per cohort ($15 \le C \le 25$, final cohort = 10 leaves)
* **Total Scheduled Cohorts**: **117 cohorts**
* **Governing Register**: **RUBRICAL** (Per Master Translation Standard MTS-1)
* **Mathematical Conservation**:
  $$\mathbf{Total\ Physical\ Pages\ in\ Codex} \equiv \sum_{k=1}^{117} C_k = (116 \times 10) + 10 = 1170 \text{ Leaves (100.0% Closed Conservation)}$$

---

## 2. Inviolable Liturgical Translation Standards (MTS-1 / TA-1)

### A. Universal Native Vision Mandate (Physical Ink Sovereignty)
* Inspect each 300 DPI image (`p{N}.png`) in `Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Source Text/images/` directly.
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

For each cohort $k \in [1, 117]$:

```
[COHORT LOOP: k = 1 to 117]
  1. INGESTION : Verify/render 300 DPI leaves p{start}..p{end} in 'Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Source Text/images/'
  2. TRANSCRIPTION : Transcribe source ink into 'Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Source Text/1888_violakis_typikon_cohort{k}_source.txt'
  3. TRANSLATION : Draft unabridged English into 'Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Draft/1888_violakis_typikon_cohort{k}_raw_draft.md'
  4. FOOTNOTES : Write definitions into 'Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Draft/1888_violakis_typikon_cohort{k}_footnotes.txt'
  5. SMALL PAUSE GATE : Run 'python scripts/run_small_pause_gate.py --monument 1888_violakis_typikon --cohort {k}'
     - Gate 1: Shared_Lexicon/lint_vocabulary.py (0 violations)
     - Gate 2: scripts/hieratic_pronoun_audit.py (100% Deity capitalization)
     - Gate 3: scripts/reconcile_footnotes.py (1:1 footnote parity)
     - Gate 4: scripts/structural_audit.py (unbroken sequence)
  6. INTEGRATION : Run 'python scripts/assemble_and_sync_hub.py --monument 1888_violakis_typikon --cohort {k}'
     - Promotes Draft -> Final MD & Final
     - Appends footnotes to Final_footnotes.txt
     - Advances ACTIVE_ORCHESTRATOR_STATE.json
  7. NEXT COHORT : If k < 117, immediately advance to cohort k+1. DO NOT pause for human input!
[END LOOP at k = 117 -> REACHED SOVEREIGN GRAND PAUSE]
```

---

## 4. Complete Codex Partition Schedule (117 Cohorts)

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
| **Cohort 15** | pp. 141–150 | 10 leaves | `PENDING` | `cohort15_source.txt` / `raw_draft.md` |
| **Cohort 16** | pp. 151–160 | 10 leaves | `PENDING` | `cohort16_source.txt` / `raw_draft.md` |
| **Cohort 17** | pp. 161–170 | 10 leaves | `PENDING` | `cohort17_source.txt` / `raw_draft.md` |
| **Cohort 18** | pp. 171–180 | 10 leaves | `PENDING` | `cohort18_source.txt` / `raw_draft.md` |
| **Cohort 19** | pp. 181–190 | 10 leaves | `PENDING` | `cohort19_source.txt` / `raw_draft.md` |
| **Cohort 20** | pp. 191–200 | 10 leaves | `PENDING` | `cohort20_source.txt` / `raw_draft.md` |
| **Cohort 21** | pp. 201–210 | 10 leaves | `PENDING` | `cohort21_source.txt` / `raw_draft.md` |
| **Cohort 22** | pp. 211–220 | 10 leaves | `PENDING` | `cohort22_source.txt` / `raw_draft.md` |
| **Cohort 23** | pp. 221–230 | 10 leaves | `PENDING` | `cohort23_source.txt` / `raw_draft.md` |
| **Cohort 24** | pp. 231–240 | 10 leaves | `PENDING` | `cohort24_source.txt` / `raw_draft.md` |
| **Cohort 25** | pp. 241–250 | 10 leaves | `PENDING` | `cohort25_source.txt` / `raw_draft.md` |
| **Cohort 26** | pp. 251–260 | 10 leaves | `PENDING` | `cohort26_source.txt` / `raw_draft.md` |
| **Cohort 27** | pp. 261–270 | 10 leaves | `PENDING` | `cohort27_source.txt` / `raw_draft.md` |
| **Cohort 28** | pp. 271–280 | 10 leaves | `PENDING` | `cohort28_source.txt` / `raw_draft.md` |
| **Cohort 29** | pp. 281–290 | 10 leaves | `PENDING` | `cohort29_source.txt` / `raw_draft.md` |
| **Cohort 30** | pp. 291–300 | 10 leaves | `PENDING` | `cohort30_source.txt` / `raw_draft.md` |
| **Cohort 31** | pp. 301–310 | 10 leaves | `PENDING` | `cohort31_source.txt` / `raw_draft.md` |
| **Cohort 32** | pp. 311–320 | 10 leaves | `PENDING` | `cohort32_source.txt` / `raw_draft.md` |
| **Cohort 33** | pp. 321–330 | 10 leaves | `PENDING` | `cohort33_source.txt` / `raw_draft.md` |
| **Cohort 34** | pp. 331–340 | 10 leaves | `PENDING` | `cohort34_source.txt` / `raw_draft.md` |
| **Cohort 35** | pp. 341–350 | 10 leaves | `PENDING` | `cohort35_source.txt` / `raw_draft.md` |
| **Cohort 36** | pp. 351–360 | 10 leaves | `PENDING` | `cohort36_source.txt` / `raw_draft.md` |
| **Cohort 37** | pp. 361–370 | 10 leaves | `PENDING` | `cohort37_source.txt` / `raw_draft.md` |
| **Cohort 38** | pp. 371–380 | 10 leaves | `PENDING` | `cohort38_source.txt` / `raw_draft.md` |
| **Cohort 39** | pp. 381–390 | 10 leaves | `PENDING` | `cohort39_source.txt` / `raw_draft.md` |
| **Cohort 40** | pp. 391–400 | 10 leaves | `PENDING` | `cohort40_source.txt` / `raw_draft.md` |
| **Cohort 41** | pp. 401–410 | 10 leaves | `PENDING` | `cohort41_source.txt` / `raw_draft.md` |
| **Cohort 42** | pp. 411–420 | 10 leaves | `PENDING` | `cohort42_source.txt` / `raw_draft.md` |
| **Cohort 43** | pp. 421–430 | 10 leaves | `PENDING` | `cohort43_source.txt` / `raw_draft.md` |
| **Cohort 44** | pp. 431–440 | 10 leaves | `PENDING` | `cohort44_source.txt` / `raw_draft.md` |
| **Cohort 45** | pp. 441–450 | 10 leaves | `PENDING` | `cohort45_source.txt` / `raw_draft.md` |
| **Cohort 46** | pp. 451–460 | 10 leaves | `PENDING` | `cohort46_source.txt` / `raw_draft.md` |
| **Cohort 47** | pp. 461–470 | 10 leaves | `PENDING` | `cohort47_source.txt` / `raw_draft.md` |
| **Cohort 48** | pp. 471–480 | 10 leaves | `PENDING` | `cohort48_source.txt` / `raw_draft.md` |
| **Cohort 49** | pp. 481–490 | 10 leaves | `PENDING` | `cohort49_source.txt` / `raw_draft.md` |
| **Cohort 50** | pp. 491–500 | 10 leaves | `PENDING` | `cohort50_source.txt` / `raw_draft.md` |
| **Cohort 51** | pp. 501–510 | 10 leaves | `PENDING` | `cohort51_source.txt` / `raw_draft.md` |
| **Cohort 52** | pp. 511–520 | 10 leaves | `PENDING` | `cohort52_source.txt` / `raw_draft.md` |
| **Cohort 53** | pp. 521–530 | 10 leaves | `PENDING` | `cohort53_source.txt` / `raw_draft.md` |
| **Cohort 54** | pp. 531–540 | 10 leaves | `PENDING` | `cohort54_source.txt` / `raw_draft.md` |
| **Cohort 55** | pp. 541–550 | 10 leaves | `PENDING` | `cohort55_source.txt` / `raw_draft.md` |
| **Cohort 56** | pp. 551–560 | 10 leaves | `PENDING` | `cohort56_source.txt` / `raw_draft.md` |
| **Cohort 57** | pp. 561–570 | 10 leaves | `PENDING` | `cohort57_source.txt` / `raw_draft.md` |
| **Cohort 58** | pp. 571–580 | 10 leaves | `PENDING` | `cohort58_source.txt` / `raw_draft.md` |
| **Cohort 59** | pp. 581–590 | 10 leaves | `PENDING` | `cohort59_source.txt` / `raw_draft.md` |
| **Cohort 60** | pp. 591–600 | 10 leaves | `PENDING` | `cohort60_source.txt` / `raw_draft.md` |
| **Cohort 61** | pp. 601–610 | 10 leaves | `PENDING` | `cohort61_source.txt` / `raw_draft.md` |
| **Cohort 62** | pp. 611–620 | 10 leaves | `PENDING` | `cohort62_source.txt` / `raw_draft.md` |
| **Cohort 63** | pp. 621–630 | 10 leaves | `PENDING` | `cohort63_source.txt` / `raw_draft.md` |
| **Cohort 64** | pp. 631–640 | 10 leaves | `PENDING` | `cohort64_source.txt` / `raw_draft.md` |
| **Cohort 65** | pp. 641–650 | 10 leaves | `PENDING` | `cohort65_source.txt` / `raw_draft.md` |
| **Cohort 66** | pp. 651–660 | 10 leaves | `PENDING` | `cohort66_source.txt` / `raw_draft.md` |
| **Cohort 67** | pp. 661–670 | 10 leaves | `PENDING` | `cohort67_source.txt` / `raw_draft.md` |
| **Cohort 68** | pp. 671–680 | 10 leaves | `PENDING` | `cohort68_source.txt` / `raw_draft.md` |
| **Cohort 69** | pp. 681–690 | 10 leaves | `PENDING` | `cohort69_source.txt` / `raw_draft.md` |
| **Cohort 70** | pp. 691–700 | 10 leaves | `PENDING` | `cohort70_source.txt` / `raw_draft.md` |
| **Cohort 71** | pp. 701–710 | 10 leaves | `PENDING` | `cohort71_source.txt` / `raw_draft.md` |
| **Cohort 72** | pp. 711–720 | 10 leaves | `PENDING` | `cohort72_source.txt` / `raw_draft.md` |
| **Cohort 73** | pp. 721–730 | 10 leaves | `PENDING` | `cohort73_source.txt` / `raw_draft.md` |
| **Cohort 74** | pp. 731–740 | 10 leaves | `PENDING` | `cohort74_source.txt` / `raw_draft.md` |
| **Cohort 75** | pp. 741–750 | 10 leaves | `PENDING` | `cohort75_source.txt` / `raw_draft.md` |
| **Cohort 76** | pp. 751–760 | 10 leaves | `PENDING` | `cohort76_source.txt` / `raw_draft.md` |
| **Cohort 77** | pp. 761–770 | 10 leaves | `PENDING` | `cohort77_source.txt` / `raw_draft.md` |
| **Cohort 78** | pp. 771–780 | 10 leaves | `PENDING` | `cohort78_source.txt` / `raw_draft.md` |
| **Cohort 79** | pp. 781–790 | 10 leaves | `PENDING` | `cohort79_source.txt` / `raw_draft.md` |
| **Cohort 80** | pp. 791–800 | 10 leaves | `PENDING` | `cohort80_source.txt` / `raw_draft.md` |
| **Cohort 81** | pp. 801–810 | 10 leaves | `PENDING` | `cohort81_source.txt` / `raw_draft.md` |
| **Cohort 82** | pp. 811–820 | 10 leaves | `PENDING` | `cohort82_source.txt` / `raw_draft.md` |
| **Cohort 83** | pp. 821–830 | 10 leaves | `PENDING` | `cohort83_source.txt` / `raw_draft.md` |
| **Cohort 84** | pp. 831–840 | 10 leaves | `PENDING` | `cohort84_source.txt` / `raw_draft.md` |
| **Cohort 85** | pp. 841–850 | 10 leaves | `PENDING` | `cohort85_source.txt` / `raw_draft.md` |
| **Cohort 86** | pp. 851–860 | 10 leaves | `PENDING` | `cohort86_source.txt` / `raw_draft.md` |
| **Cohort 87** | pp. 861–870 | 10 leaves | `PENDING` | `cohort87_source.txt` / `raw_draft.md` |
| **Cohort 88** | pp. 871–880 | 10 leaves | `PENDING` | `cohort88_source.txt` / `raw_draft.md` |
| **Cohort 89** | pp. 881–890 | 10 leaves | `PENDING` | `cohort89_source.txt` / `raw_draft.md` |
| **Cohort 90** | pp. 891–900 | 10 leaves | `PENDING` | `cohort90_source.txt` / `raw_draft.md` |
| **Cohort 91** | pp. 901–910 | 10 leaves | `PENDING` | `cohort91_source.txt` / `raw_draft.md` |
| **Cohort 92** | pp. 911–920 | 10 leaves | `PENDING` | `cohort92_source.txt` / `raw_draft.md` |
| **Cohort 93** | pp. 921–930 | 10 leaves | `PENDING` | `cohort93_source.txt` / `raw_draft.md` |
| **Cohort 94** | pp. 931–940 | 10 leaves | `PENDING` | `cohort94_source.txt` / `raw_draft.md` |
| **Cohort 95** | pp. 941–950 | 10 leaves | `PENDING` | `cohort95_source.txt` / `raw_draft.md` |
| **Cohort 96** | pp. 951–960 | 10 leaves | `PENDING` | `cohort96_source.txt` / `raw_draft.md` |
| **Cohort 97** | pp. 961–970 | 10 leaves | `PENDING` | `cohort97_source.txt` / `raw_draft.md` |
| **Cohort 98** | pp. 971–980 | 10 leaves | `PENDING` | `cohort98_source.txt` / `raw_draft.md` |
| **Cohort 99** | pp. 981–990 | 10 leaves | `PENDING` | `cohort99_source.txt` / `raw_draft.md` |
| **Cohort 100** | pp. 991–1000 | 10 leaves | `PENDING` | `cohort100_source.txt` / `raw_draft.md` |
| **Cohort 101** | pp. 1001–1010 | 10 leaves | `PENDING` | `cohort101_source.txt` / `raw_draft.md` |
| **Cohort 102** | pp. 1011–1020 | 10 leaves | `PENDING` | `cohort102_source.txt` / `raw_draft.md` |
| **Cohort 103** | pp. 1021–1030 | 10 leaves | `PENDING` | `cohort103_source.txt` / `raw_draft.md` |
| **Cohort 104** | pp. 1031–1040 | 10 leaves | `PENDING` | `cohort104_source.txt` / `raw_draft.md` |
| **Cohort 105** | pp. 1041–1050 | 10 leaves | `PENDING` | `cohort105_source.txt` / `raw_draft.md` |
| **Cohort 106** | pp. 1051–1060 | 10 leaves | `PENDING` | `cohort106_source.txt` / `raw_draft.md` |
| **Cohort 107** | pp. 1061–1070 | 10 leaves | `PENDING` | `cohort107_source.txt` / `raw_draft.md` |
| **Cohort 108** | pp. 1071–1080 | 10 leaves | `PENDING` | `cohort108_source.txt` / `raw_draft.md` |
| **Cohort 109** | pp. 1081–1090 | 10 leaves | `PENDING` | `cohort109_source.txt` / `raw_draft.md` |
| **Cohort 110** | pp. 1091–1100 | 10 leaves | `PENDING` | `cohort110_source.txt` / `raw_draft.md` |
| **Cohort 111** | pp. 1101–1110 | 10 leaves | `PENDING` | `cohort111_source.txt` / `raw_draft.md` |
| **Cohort 112** | pp. 1111–1120 | 10 leaves | `PENDING` | `cohort112_source.txt` / `raw_draft.md` |
| **Cohort 113** | pp. 1121–1130 | 10 leaves | `PENDING` | `cohort113_source.txt` / `raw_draft.md` |
| **Cohort 114** | pp. 1131–1140 | 10 leaves | `PENDING` | `cohort114_source.txt` / `raw_draft.md` |
| **Cohort 115** | pp. 1141–1150 | 10 leaves | `PENDING` | `cohort115_source.txt` / `raw_draft.md` |
| **Cohort 116** | pp. 1151–1160 | 10 leaves | `PENDING` | `cohort116_source.txt` / `raw_draft.md` |
| **Cohort 117** | pp. 1161–1170 | 10 leaves | `PENDING` | `cohort117_source.txt` / `raw_draft.md` |

---

## 5. Sovereign Grand Pause Termination
When Cohort 117 completes its Small Pause Gate and final integration:
- `remaining_pages == 0`
- The entire 1170-page codex is assembled in `Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Final MD/1888_violakis_typikon_complete.md`
- Deliverables are synchronized to `Projects/Typikon Coded/Data/Inbox/1888_Violakis_Typikon/`
- Automator halts and delivers the final Grand Pause notification to the Human Operator.
