# Monument 7: 1895 Dmitrievsky Opisanie Vol. 1 (Typika) — Worker Startup & Autonomous Execution Guide

## Executive Charter & Operational Mandate
* **Monument ID**: `1895_dmitrievsky_vol1`
* **Title**: Opisanie Liturgicheskikh Rukopisei Vol. 1: Typika (Aleksei Dmitrievsky, Kyiv, 1895)
* **Scope**: 1,090 physical facsimile leaves (Monotonically indexed $p1 \dots p1090$, 10 leaves per cohort = **109 cohorts**; exactly 10 leaves per cohort)
* **Role**: Sequestered Liturgical Translation Automator & Vision Transcriber
* **Operating Standard**: Master Translation Standard (MTS-1) per `Shared_Lexicon/MASTER_TRANSLATION_STANDARD.md`
* **Governing Genre Register**: **SCHOLARLY CRITICAL / RUBRICAL** (Monumental critical descriptions and complete manuscript transcriptions of historical Byzantine, Sinaitic, Sabbaite, Studite, and Athonite Typika codices, with extensive Greek and Church Slavonic apparatus)
* **Autonomous Rule**: Rule 14 of `.agents/AGENTS.md` (Autonomous execution with zero inter-cohort human stalls; halt strictly at Sovereign Grand Pause when `remaining_pages == 0`).

---

## Copy-Paste Startup Prompt for New Chat Session (Rule 19)
```text
/plan Orchestrate and execute Monument 7: 1895 Dmitrievsky Opisanie Vol. 1 (Typika) (1,090 physical pages, 109 cohorts). Read `Liturgical Monuments/Monument 7 - 1895 Dmitrievsky Vol 1/STARTUP_INSTRUCTIONS.md` and `AUTONOMOUS_MONUMENT_DIRECTIVE.md`. Enforce MTS-1 and `.agents/AGENTS.md`. Formulate a comprehensive 4-phase implementation plan covering pre-flight validation, Cohort 1 baseline execution, autonomous multi-cohort looping, and Grand Pause Hub synchronization.
```

---

## Workspace Directory Map
* **Workspace Root**: `Liturgical Monuments/Monument 7 - 1895 Dmitrievsky Vol 1`
  - `Source Text/images/`: 300 DPI high-resolution page rasters (`Page_0001.jpg`..`Page_1090.jpg` via NTFS junction to Drive E: master vault)
  - `Source Text/`: Ink transcriptions (`1895_dmitrievsky_vol1_cohort{k}_source.txt`)
  - `Draft/`: Draft translations (`1895_dmitrievsky_vol1_cohort{k}_raw_draft.md`) and cohort footnotes (`1895_dmitrievsky_vol1_cohort{k}_footnotes.txt`)
  - `Final/`: Promoted cohort files and cumulative `Final_footnotes.txt`
  - `Final MD/`: Assembled complete monument edition (`1895_dmitrievsky_vol1_complete.md`)
  - `Work_Orders/`: Cohort-by-cohort specifications (`cohort_01_work_order.md`, etc.)
  - `Audit_Reports/`: Small pause gate JSON reports (`cohort{k}_small_pause_report.json`)
  - `Cohorts/`: Intermediate cohort backups
  - `AUTONOMOUS_MONUMENT_DIRECTIVE.md`: Master 109-cohort partition schedule.

---

## Technical Directives & Translation Standards (MTS-1)
1. **Physical Ink Witness & Paleographical Rigor**:
   Aleksei Dmitrievsky's *Opisanie Liturgicheskikh Rukopisei* (Description of Liturgical Manuscripts), Vol. 1: *Typika* (Kyiv, 1895) is the preeminent global critical edition of ancient Byzantine, Sinaitic, Jerusalem, and Mount Athos Typika.
   - Grounding in physical ink: Inspect 300 DPI page scans directly from the Drive E: master vault.
   - Scholarly critical register: Translate Russian commentary, analytical introductions, and paleographical apparatus into fluent, rigorous scholarly English.
   - Greek & Church Slavonic Transcription and Translation: Dmitrievsky publishes extensive verbatim codex texts in Byzantine Greek and Church Slavonic. For narrative, rubrics, and commentary, translate into scholarly English while preserving technical liturgical realia and incipits parenthetically.
2. **Dual Incipits & Chant Realia**:
   - Provide bold English incipits followed by italicized Greek/Slavonic originals in parentheses, e.g. **"Lord, I have cried"** (*Κύριε ἐκέκραξα* / *Господи воззвахъ*).
   - Ruthenian/Byzantine tone headings: `Tone 1` through `Tone 8`.
3. **Rubrical Register Norms**:
   - Use **Active Present Indicative** for ceremonial and bodily motions (*"The priest enters the sanctuary..."*).
   - Absolute prohibition of gratuitous *"shall"*s in rubrics.
4. **Deity Pronouns**:
   - 100% mandatory capitalization for Holy Trinity Divine Persons (*He, Him, His, Thou, Thee, Thy, Thine*).
5. **Father Paul Doxology Standard**:
   - Choral: *"Glory be to the Father, and to the Son, and to the Holy Spirit, now and forever, and unto the ages of ages. Amen."*
   - Strictly prohibit *"for ever and ever"*.
6. **Psalter & Scripture**:
   - Mandatory Septuagint (LXX) versification with bracketed Masoretic parallels.
7. **Closed Mathematical Leaf Conservation**:
   - Every physical facsimile leaf must have a banner `=== LEAF p{N} ===` (with parenthetical printed page reference).
   - Continuous monotonic indexing without skipping or reordering leaves ($p1 \dots p1090$).
8. **Footnote Bijectivity**:
   - Monotonic continuous numbering across the monument: Every `[^N]` in body text must have a matching `[^N]:` definition.

---

## Multi-Cohort Autonomous Execution Loop
For each cohort $k = 1 \dots 109$:
1. Prepare work order `cohort_{k}_work_order.md`.
2. Dispatch subagent via `invoke_subagent`.
3. Worker transcribes leaves and drafts MTS-1 translation with bijective footnotes.
4. Worker executes `py scripts/run_small_pause_gate.py --monument 1895_dmitrievsky_vol1 --cohort {k}`.
5. On exit code 0, parent orchestrator executes `py scripts/assemble_and_sync_hub.py --monument 1895_dmitrievsky_vol1 --cohort {k}`.
6. Commit to git and advance immediately to cohort $k+1$ without pausing.
7. Upon completing Cohort 109 (`remaining_pages == 0`), halt at Sovereign Grand Pause.
