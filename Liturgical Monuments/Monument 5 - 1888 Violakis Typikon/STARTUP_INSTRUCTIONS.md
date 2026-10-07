# Monument 5: 1888 Violakis Typikon — Worker Startup & Autonomous Execution Guide

## Executive Charter & Operational Mandate
* **Monument ID**: `1888_violakis_typikon`
* **Title**: Typikon of the Great Church of Christ by George Violakis (Constantinople 1888 / Denver Bilingual Edition)
* **Scope**: 1,170 physical facsimile pages (Monotonically indexed $p1 \dots p1170$, 10 leaves per cohort = **117 cohorts**)
* **Role**: Sequestered Liturgical Translation Automator & Vision Transcriber
* **Operating Standard**: Master Translation Standard (MTS-1) per `Shared_Lexicon/MASTER_TRANSLATION_STANDARD.md`
* **Autonomous Rule**: Rule 14 of `.agents/AGENTS.md` (Autonomous execution with zero inter-cohort human stalls; halt strictly at Sovereign Grand Pause when `remaining_pages == 0`).

---

## Copy-Paste Startup Prompt for New Chat Session
```text
/plan Orchestrate and execute Monument 5: 1888 Violakis Typikon (1,170 physical pages, 117 cohorts). Read `Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/STARTUP_INSTRUCTIONS.md` and `AUTONOMOUS_MONUMENT_DIRECTIVE.md`. Enforce MTS-1 and `.agents/AGENTS.md`. Formulate a 4-phase implementation plan covering pre-flight validation, Cohort 1 baseline execution, autonomous multi-cohort looping, and Grand Pause Hub synchronization.
```

---

## Workspace Directory Map
* **Workspace Root**: `Liturgical Monuments/Monument 5 - 1888 Violakis Typikon`
  - `Source Text/images/`: 300 DPI high-resolution page renders (`p1.png`, `p2.png`, etc.)
  - `Source Text/`: Ink transcriptions (`1888_violakis_typikon_cohort{k}_source.txt`)
  - `Draft/`: Draft translations (`1888_violakis_typikon_cohort{k}_raw_draft.md`) and cohort footnotes (`1888_violakis_typikon_cohort{k}_footnotes.txt`)
  - `Final/`: Promoted cohort files and cumulative `Final_footnotes.txt`
  - `Final MD/`: Assembled complete monument edition (`1888_violakis_typikon_complete.md`)
  - `Work_Orders/`: Cohort-by-cohort specifications (`cohort_01_work_order.md`, etc.)
  - `Audit_Reports/`: Small pause gate JSON reports (`cohort{k}_small_pause_report.json`)
  - `AUTONOMOUS_MONUMENT_DIRECTIVE.md`: Master 117-cohort partition schedule.

---

## Technical Directives & Translation Standards (MTS-1)
1. **Bilingual Codex Nature**:
   The 1888 Violakis facsimile contains authentic Greek text alongside a facing English translation from the Denver edition.
   - Grounding in physical ink: Inspect 300 DPI renders directly.
   - Scholarly critical translation: Audit and rectify the English text into 100% compliance with MTS-1 and canonical Byzantine-Ruthenian liturgical usage.
2. **Rubrical Register**:
   - Use **Active Present Indicative** for ceremonial motions (*"The Priest enters the sanctuary..."*).
   - Reserve *"shall"* exclusively for statutory decrees; ban rubrical "shall"-bombing.
3. **Deity Pronouns**:
   - 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
4. **Father Paul Doxology Standard**:
   - Use *"now and forever, and unto the ages of ages. Amen."*
   - Strictly prohibit the phrase *"for ever and ever"*.
5. **Psalter & Scripture**:
   - Mandatory Septuagint (LXX) numbering.
6. **Canonical Loanwords**:
   - `Tetrapod` (never "center table"), `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
7. **Closed Mathematical Leaf Conservation**:
   - Every physical leaf must have a banner `=== LEAF p{N} ===` (with parenthetical printed book page reference if applicable).
   - Continuous monotonic indexing without skipping or reordering leaves.
8. **Footnote Bijectivity**:
   - Monotonic continuous indices `[^N]` in body text matching exact definitions `[^N]:` in the footnotes file.

---

## Multi-Cohort Autonomous Execution Loop
For each cohort $k = 1 \dots 117$:

1. **Leaf Ingestion**:
   Verify leaves `p{start}.png` to `p{end}.png` in `Source Text/images/`. If needed, extract via:
   ```powershell
   py scripts/extract_cohort_leaves.py --monument 1888_violakis_typikon --cohort {k}
   ```
2. **Transcription**:
   Transcribe leaf-by-leaf ink into `Source Text/1888_violakis_typikon_cohort{k}_source.txt`.
3. **Translation**:
   Draft MTS-1 text into `Draft/1888_violakis_typikon_cohort{k}_raw_draft.md`.
   Record footnotes into `Draft/1888_violakis_typikon_cohort{k}_footnotes.txt`.
4. **Small Pause Gate Verification**:
   Execute the automated 5-gate verification suite:
   ```powershell
   py scripts/run_small_pause_gate.py --monument 1888_violakis_typikon --cohort {k}
   ```
   Ensures zero vocabulary violations, zero AI liturgical slop, 100% Deity capitalization, 1:1 footnote parity, and structural continuity.
5. **Assembly & Hub Sync**:
   Execute post-flight integration and promote deliverables:
   ```powershell
   py scripts/assemble_and_sync_hub.py --monument 1888_violakis_typikon --cohort {k}
   ```
6. **Autonomous Transition**:
   Immediately proceed to cohort $k+1$. Never halt or yield turns between cohorts.
7. **Grand Pause**:
   Halt only when cohort 117 is sealed and `remaining_pages == 0`.

---

## Instructions for the Initial Implementation Plan (/plan)
Upon receiving the startup prompt:
1. Review this document and `Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/AUTONOMOUS_MONUMENT_DIRECTIVE.md`.
2. Formulate a comprehensive, phased **Implementation Plan**:
   - **Phase 1: Environment & Pre-Flight Validation**: State confirmation, directory verification, Cohort 1 leaf verification.
   - **Phase 2: Cohort 1 Execution**: Transcription, MTS-1 drafting, footnotes, gate execution, and initial assembly.
   - **Phase 3: Autonomous Multi-Cohort Pipeline Cadence**: Systematic batch processing of cohorts 2 through 117 with zero human stalls.
   - **Phase 4: Sovereign Grand Pause & Final Hub Synchronization**: Complete codex assembly, 1:1 footnote audit, and publication delivery to Hub Inbox.
3. Present the plan to the user for review (allowing the user to choose to commence or grill via `/grill-me`).
