# Monument 6: 1910 Skaballanovich Typikon — Worker Startup & Autonomous Execution Guide

## Executive Charter & Operational Mandate
* **Monument ID**: `1910_skaballanovich_typikon`
* **Title**: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915)
* **Scope**: 1,022 physical facsimile pages (Monotonically indexed $p1 \dots p1022$, 10 leaves per cohort = **103 cohorts**; Cohorts 1–102: 10 leaves, Cohort 103: 2 leaves)
* **Role**: Sequestered Liturgical Translation Automator & Vision Transcriber
* **Operating Standard**: Master Translation Standard (MTS-1) per `Shared_Lexicon/MASTER_TRANSLATION_STANDARD.md`
* **Governing Genre Register**: **SCHOLARLY CRITICAL / RUBRICAL** (Historical-liturgical commentary, patristic citations, ancient typika comparisons, and rubrical synthesis)
* **Autonomous Rule**: Rule 14 of `.agents/AGENTS.md` (Autonomous execution with zero inter-cohort human stalls; halt strictly at Sovereign Grand Pause when `remaining_pages == 0`).

---

## Copy-Paste Startup Prompt for New Chat Session
```text
/plan Orchestrate and execute Monument 6: 1910 Skaballanovich Typikon (1,022 physical pages, 103 cohorts). Read `Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/STARTUP_INSTRUCTIONS.md` and `AUTONOMOUS_MONUMENT_DIRECTIVE.md`. Enforce MTS-1 and `.agents/AGENTS.md`. Formulate a comprehensive 4-phase implementation plan covering pre-flight validation, Cohort 1 baseline execution, autonomous multi-cohort looping, and Grand Pause Hub synchronization.
```

---

## Workspace Directory Map
* **Workspace Root**: `Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon`
  - `Source Text/images/`: 300 DPI high-resolution page rasters (`Page_0001.jpg`..`Page_1022.jpg` via NTFS junction to Drive E: master vault)
  - `Source Text/`: Ink transcriptions (`1910_skaballanovich_cohort{k}_source.txt`)
  - `Draft/`: Draft translations (`1910_skaballanovich_cohort{k}_raw_draft.md`) and cohort footnotes (`1910_skaballanovich_cohort{k}_footnotes.txt`)
  - `Final/`: Promoted cohort files and cumulative `Final_footnotes.txt`
  - `Final MD/`: Assembled complete monument edition (`1910_skaballanovich_typikon_complete.md`)
  - `Work_Orders/`: Cohort-by-cohort specifications (`cohort_01_work_order.md`, etc.)
  - `Audit_Reports/`: Small pause gate JSON reports (`cohort{k}_small_pause_report.json`)
  - `AUTONOMOUS_MONUMENT_DIRECTIVE.md`: Master 103-cohort partition schedule.

---

## Technical Directives & Translation Standards (MTS-1)
1. **Physical Ink Witness**:
   Mikhail Skaballanovich's *Tolkovy Typikon* is the paramount Russian/Ukrainian pre-revolutionary academic commentary on the Byzantine-Slavic Typikon.
   - Grounding in physical ink: Inspect 300 DPI page scans directly.
   - Scholarly critical register: Translate Russian narrative exposition, Greek/Slavonic incipits, and liturgical rubrics into idiomatic, rigorous scholarly English adhering to MTS-1.
2. **Dual Incipits**:
   - Provide bold English incipits followed by italicized Slavonic/Greek original in parentheses, e.g. **"Lord, I have cried"** (*Господи воззвахъ* / *Κύριε ἐκέκραξα*).
3. **Rubrical Register**:
   - Use **Active Present Indicative** for ceremonial motions (*"The priest enters the sanctuary..."*).
   - Reserve *"shall"* exclusively for statutory decrees; ban rubrical "shall"-bombing.
4. **Deity Pronouns**:
   - 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
5. **Father Paul Doxology Standard**:
   - Use *"now and forever, and unto the ages of ages. Amen."*
   - Strictly prohibit the phrase *"for ever and ever"*.
6. **Psalter & Scripture**:
   - Mandatory Septuagint (LXX) versification with bracketed Masoretic parallels.
7. **Canonical UGCC Realia**:
   - `Tetrapod` (never "center table"), `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
8. **Closed Mathematical Leaf Conservation**:
   - Every physical leaf must have a banner `=== LEAF p{N} ===` (with parenthetical printed page reference).
   - Continuous monotonic indexing without skipping or reordering leaves.
9. **Footnote Bijectivity**:
   - Monotonic continuous indices `[^N]` in body text matching exact definitions `[^N]:` in the footnotes file.

---

## Multi-Cohort Autonomous Execution Loop
For each cohort $k = 1 \dots 103$:
1. Prepare work order `cohort_{k}_work_order.md`.
2. Dispatch subagent via `invoke_subagent`.
3. Worker transcribes leaves and drafts MTS-1 translation with bijective footnotes.
4. Worker executes `py scripts/run_small_pause_gate.py --monument 1910_skaballanovich_typikon --cohort {k}`.
5. On exit code 0, parent orchestrator executes `py scripts/assemble_and_sync_hub.py --monument 1910_skaballanovich_typikon --cohort {k}`.
6. Commit to git and advance immediately to cohort $k+1$ without pausing.
7. Upon completing Cohort 103 (`remaining_pages == 0`), halt at Grand Pause.
