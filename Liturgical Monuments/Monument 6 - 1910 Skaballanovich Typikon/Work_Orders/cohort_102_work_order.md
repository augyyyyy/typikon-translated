# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 102

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 102  
**Physical Leaves**: Physical pages 1011 to 1020 (`p1011.png` through `p1020.png`, 10 leaves total)  
**Starting Footnote Index**: N/A (Volume II Endnotes Folios — Notes 880 through 995 of Volume II)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` (`Page_1011.jpg`..`Page_1020.jpg`) and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (pages 1011–1020, pre-cached in `scratch/cohort102_source_raw.txt`).
2. **Endnotes Folios Formatting (Volume I Precedent: Cohorts 46–54 & User Decisions A2, A3)**:
   - Format each leaf with banner `=== LEAF p{N} ===` and translate each numbered note sequentially (`880. ...`, `881. ...`, etc.).
   - Note 879 citation head begins on leaf p1010; continue its translation seamlessly under `=== LEAF p1011 ===`.
   - Leave `1910_skaballanovich_typikon_cohort102_footnotes.txt` empty (0 bytes), as the markdown text itself constitutes the critical notes apparatus.
   - Do NOT insert footnote markers `[^N]` in the markdown text.
3. **Apparatus Epigraphy & Translation Standard**:
   - Translate all Greek, Latin, German, and Church Slavonic patristic citations and critical commentary into fluent, rigorous scholarly English.
   - Preserve technical realia, manuscript shelfmarks, and Greek/Slavonic terms parenthetically.
4. **Cohort 102 Note Coverage (Notes 880–995)**:
   - `p1011`–`p1014`: Notes 880–903 (Continuation of Note 879; non-Orthodox morning offices: Roman, Ambrosian, Anglican, Lutheran; the Kyiv Theological Academy All-Night Vigil experiment; the First, Third, and Sixth Hours).
   - `p1014`–`p1018`: Notes 904–974 (Variable parts of the Sunday Divine Liturgy; Typical Antiphons and Beatitudes; Little Entrance; Troparia and Kontakia; Sunday Liturgical Prokeimena of the Eight Tones; Epistle and Gospel lectionary systems: comparative Jacobite, Nestorian, Roman, and Anglican pericope tables; Megalynarion and Communion Verse).
   - `p1018`–`p1020`: Notes 975–995 (The Rite of the Elevation of the Panagia: post-prandial thanksgiving prayers, ancient agape meals, bread fragment *ukrukh*, Studite and Pantokrator Typika, Marian hymnic invocations, and Archbishop Veniamin's *Novaya Skrizhal'*).
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*). Human subjects remain lowercase.
6. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
7. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort102_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort102_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort102_footnotes.txt` (empty file)

---

## 3. Autonomous Execution Instructions
1. Inspect images `p1011.png` through `p1020.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`.
2. Transcribe Russian source text, Church Slavonic citations, Latin and Greek apparatus leaf-by-leaf with headers `=== LEAF p{N} ===` into `1910_skaballanovich_typikon_cohort102_source.txt`.
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort102_raw_draft.md` with leaf banners and sequential note numbers (`880. ...`, etc.).
4. Create empty `1910_skaballanovich_typikon_cohort102_footnotes.txt`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort102_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort102_footnotes.txt" --cohort 102`
