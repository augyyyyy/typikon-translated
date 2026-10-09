# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 101

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 101  
**Physical Leaves**: Physical pages 1001 to 1010 (`p1001.png` through `p1010.png`, 10 leaves total)  
**Starting Footnote Index**: N/A (Volume II Endnotes Folios — Notes 640 through 879 of Volume II)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` (`Page_1001.jpg`..`Page_1010.jpg`) and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (pages 1001–1010, pre-cached in `scratch/cohort101_source_raw.txt`).
2. **Endnotes Folios Formatting (Volume I Precedent: Cohorts 46–54 & User Decisions A2, A3)**:
   - Format each leaf with banner `=== LEAF p{N} ===` and translate each numbered note sequentially (`640. ...`, `641. ...`, etc.).
   - Note 639 head is on leaf p1000 and body continues onto p1001; continue its translation seamlessly under `=== LEAF p1001 ===`.
   - Leave `1910_skaballanovich_typikon_cohort101_footnotes.txt` empty (0 bytes), as the markdown text itself constitutes the critical notes apparatus.
   - Do NOT insert footnote markers `[^N]` in the markdown text.
3. **Apparatus Epigraphy & Translation Standard**:
   - Translate all Greek, Latin, German, and Church Slavonic patristic citations and critical commentary into fluent, rigorous scholarly English.
   - Preserve technical realia, manuscript shelfmarks, and Greek/Slavonic terms parenthetically.
4. **Cohort 101 Note Coverage (Notes 640–879)**:
   - `p1001`–`p1003`: Notes 640–699 (The hymn *“Having beheld the Resurrection of Christ”*; Psalm 50 and post-Gospel troparia; the Diaconal petition *“Save, O God, Thy people...”*; the Kanon and the 9 Biblical Odes).
   - `p1004`–`p1007`: Notes 700–805 (Structure of the Kanon troparia, Heirmoi, and Katavasiai; classical Palestinian and Studite hymnographers: St. John of Damascus, St. Cosmas of Maiuma, St. Theodore the Studite, St. Joseph the Hymnographer; the 9th Ode and the Megalynarion; the Exapostilaria and the Praises / Lauds).
   - `p1008`–`p1010`: Notes 806–879 (The Great Doxology; the Asmatic Trisagion; the Sunday Dismissal Troparia; concluding Matins litanies and dismissal formulas; the Morning Litiya and procession to the narthex; the Studite Catecheses).
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*). Human subjects remain lowercase.
6. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
7. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort101_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort101_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort101_footnotes.txt` (empty file)

---

## 3. Autonomous Execution Instructions
1. Inspect images `p1001.png` through `p1010.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`.
2. Transcribe Russian source text, Church Slavonic citations, Latin and Greek apparatus leaf-by-leaf with headers `=== LEAF p{N} ===` into `1910_skaballanovich_typikon_cohort101_source.txt`.
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort101_raw_draft.md` with leaf banners and sequential note numbers (`640. ...`, etc.).
4. Create empty `1910_skaballanovich_typikon_cohort101_footnotes.txt`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort101_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort101_footnotes.txt" --cohort 101`
