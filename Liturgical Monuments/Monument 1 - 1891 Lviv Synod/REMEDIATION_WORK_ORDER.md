# Comprehensive Remediation Work Order: 1891 Lviv Provincial Synod
## Surgical Restoration of Missing Leaves (Leaves p241–p244 & p275–p278)

> [!IMPORTANT]
> **Mission Objective**:
> Restore 100% Closed Mathematical Leaf Conservation ($278 / 278 \text{ physical leaves}$) to **Monument 1: Acts and Decrees of the Ruthenian Provincial Synod of Lviv (1891)**.
> This work order translates the 8 missing folios, splices them seamlessly into the master complete edition, re-indexes the footnotes, executes the 4-gate verification suite, and syncs the sealed deliverables to the Hub Inbox.

---

## 1. Context & Forensic Diagnosis
During the initial translation of Monument 1, an unmapped gap occurred due to coordinate system conflation:
* **Cohort 14** concluded at **PDF Leaf p240** (Book Page 236) in the middle of a sentence opening *Chapter IV: On Parochial Competition*.
* **Cohort 1** resumed at **PDF Leaf p245** (Book Page 241) at Point 4 of *Titulus XI: On Fasts*.
* **The Missing Core Decrees (Leaves p241–p244 / Book pp. 237–240)**:
  - Completion of Titulus IX Chapter IV (*Concursus*).
  - The entirety of **TITULUS X. On Monks (*О монахахъ*)** (Basilian Order, Dobromyl Reform, vows, discipline, schools, pastoral care).
  - The opening of **TITULUS XI. On Fasts (*О постахъ*)** (Fast vs. Abstinence preamble, and Points 1, 2, and 3).
* **The Missing Tail Leaves (Leaves p275–p278)**:
  - Official printed Synodal Errata (*Похибки друкарски*) and concluding archival accession matter.

---

## 2. Inviolable Liturgical Translation Standards (MTS-1)
* **Governing Register**: **JURIDICAL** (Prescriptive statutory verbs: *"The parish priest shall be bound under pain of..."*).
* **Native Vision Mandate**: Inspect high-resolution 300 DPI images directly in `Typikons/1891 Lviv Synod/Source Text/images/` (`p241.png` through `p244.png` and `p275.png` through `p278.png`).
* **Canonical Realia**: Use canonical loanwords (`Tetrapod`, `Klepalo`, `Aer`, `Sluzhebnik`, `Trebnik`, `Kryloshany`, `Basilian`, `Archimandrite`, `Protohegumen`, `Hegumen`).
* **Pronouns & Doxology**:
  - 100% capitalization on Trinity Deity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*). Clergy, monks, and human actors remain lowercase.
  - Ban *"for ever and ever"*; use *"now and forever, and unto the ages of ages"*.
* **Scripture**: Septuagint (LXX) versification mandatory.

---

## 3. Action Steps for Sequestered Worker

### Step 1: Transcribe and Translate Leaves p241–p244
1. **Source Transcriptions**:
   - Inspect `Source Text/images/p241.png` through `p244.png`.
   - Write Church Slavonic / Ruthenian transcription into `Source Text/1891_synod_remediation_core_source.txt`.
2. **English Translation**:
   - Write translated markdown into `Draft/1891_synod_remediation_core_draft.md`.
   - Ensure the opening sentence of Leaf p241 perfectly completes the sentence cut off at Leaf p240:
     - End of Leaf p240: *"The governance of souls is the art of arts, the holiness corresponding unto this office so transcendent, that the Church to..."*
     - Start of Leaf p241: *"...wards its execution hath established strict examinations..."* (transcribe and translate the exact physical ink on p241).
   - Fully translate **TITULUS X. On Monks (*О монахахъ*)**.
   - Fully translate Points 1, 2, and 3 of **TITULUS XI. On Fasts (*О постахъ*)** so that Point 3 leads seamlessly into Point 4 on Leaf p245 (*"4. The Fast before the Dormition..."*).
   - Any scholarly footnotes must be documented in `Draft/1891_synod_remediation_footnotes.txt`.

### Step 2: Transcribe and Translate Leaves p275–p278
1. Inspect `Source Text/images/p275.png` through `p278.png`.
2. Translate the official Synodal Errata (*Похибки друкарски*) into `Draft/1891_synod_remediation_errata_draft.md`.
3. Format each erratum with the cited page, original reading, and corrected reading.

### Step 3: Splice into Master Complete Editions
1. **Splice Core Decrees**:
   - In `Typikons/1891 Lviv Synod/Final MD/1891_lviv_synod_complete.md`:
   - Locate `=== LEAF p240 ===` and the break before `=== LEAF p245 ===` (or `<!-- START COHORT 1891_synod_cohort1 -->`).
   - Insert the translated text of Leaves `p241`, `p242`, `p243`, and `p244` with proper leaf banners (`=== LEAF p241 ===`, etc.).
2. **Append Tail Matter**:
   - At the very end of `1891_lviv_synod_complete.md` (after Leaf `p274` and the Papal Confirmation decree), append the translated Synodal Errata (`=== LEAF p275 ===` and `=== LEAF p276 ===`) and archival collation (`=== LEAF p277 ===`, `=== LEAF p278 ===`).
3. **Synchronize Plain Text**:
   - Update `Typikons/1891 Lviv Synod/Final/1891_lviv_synod_complete.txt` to mirror the markdown edition.

### Step 4: Reconcile Footnotes Monotonically
1. Merge new footnote definitions into `Typikons/1891 Lviv Synod/Final/Final_footnotes.txt`.
2. Renumber all footnote markers `[^N]` in `1891_lviv_synod_complete.md` from `1` to `N` monotonically.
3. Verify that every `[^N]` in the body text corresponds exactly to `[^N]:` in `Final_footnotes.txt` (100% bijective parity).

### Step 5: Execute Small Pause Gatekeeper Suite
Run the standard verification commands from the project root:
```powershell
# 1. Master Lexicon Vocabulary Lint (0 violations required)
python Shared_Lexicon/lint_vocabulary.py "Typikons/1891 Lviv Synod/Final MD/1891_lviv_synod_complete.md"

# 2. Hieratic Pronoun Audit (100% Trinity capitalization required)
python scripts/hieratic_pronoun_audit.py "Typikons/1891 Lviv Synod/Final MD/1891_lviv_synod_complete.md"

# 3. Footnote Bijectivity Verification
python scripts/reconcile_footnotes.py --text "Typikons/1891 Lviv Synod/Final MD/1891_lviv_synod_complete.md" --footnotes "Typikons/1891 Lviv Synod/Final/Final_footnotes.txt"

# 4. Anti-Pattern Baseline
python scratch/search_anti_patterns.py
```

### Step 6: Synchronize Deliverables to Hub Inbox
Copy the updated files to the Typikon Coded Hub:
* Target: `Projects/Typikon Coded/Data/Inbox/1891_Lviv_Provincial_Synod/`
* Files:
  - `1891_lviv_synod_complete.md`
  - `1891_lviv_synod_complete.txt`
  - `Final_footnotes.txt`
  - `handoff_note.md` (Update stating that Titulus X and 278/278 physical leaves are fully restored and certified).

---
