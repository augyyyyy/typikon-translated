# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 99

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 99  
**Physical Leaves**: Physical pages 981 to 990 (`p981.png` through `p990.png`, 10 leaves total)  
**Starting Footnote Index**: N/A (Volume II Endnotes Folios — Notes 268 through 457 of Volume II)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` (`Page_0981.jpg`..`Page_0990.jpg`) and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (pages 981–990, pre-cached in `scratch/cohort99_source_raw.txt`).
2. **Endnotes Folios Formatting (Volume I Precedent: Cohorts 46–54 & User Decisions A2, A3)**:
   - Format each leaf with banner `=== LEAF p{N} ===` and translate each numbered note sequentially (`268. ...`, `269. ...`, etc.).
   - Leave `1910_skaballanovich_typikon_cohort99_footnotes.txt` empty (0 bytes), as the markdown text itself constitutes the critical notes apparatus.
   - Do NOT insert footnote markers `[^N]` in the markdown text.
3. **Apparatus Epigraphy & Translation Standard**:
   - Translate all Greek, Latin, German, and Church Slavonic patristic citations and critical commentary into fluent, rigorous scholarly English.
   - Preserve technical realia, manuscript shelfmarks, and Greek/Slavonic terms parenthetically.
4. **Cohort 99 Note Coverage (Notes 268–457)**:
   - `p981`–`p983`: Notes 268–332 (Vespers psalmody; St. John Chrysostom *In Genesim*; Barberini Euchologion; the Great Litany; prayers of the first and second antiphons; deacon's petitions).
   - `p984`–`p986`: Notes 333–384 (The Kathisma of the Psalter *“Blessed is the man”*; ancient Sabbaite and Studite practices; the Little Litany after psalmody; the troparia of the Resurrection).
   - `p987`–`p990`: Notes 385–457 (The Lucernarium psalmody *“Lord, I have cried”*; stichera distribution on 10, 8, 6; the Dogmatikon hymns of the Eight Tones composed by St. John of Damascus; the Entrance with the Censer; the hymn *Phos Hilaron* and the Vesperal Prokeimena).
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*). Human subjects remain lowercase.
6. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
7. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort99_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort99_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort99_footnotes.txt` (empty file)

---

## 3. Autonomous Execution Instructions
1. Inspect images `p981.png` through `p990.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`.
2. Transcribe Russian source text, Church Slavonic citations, Latin and Greek apparatus leaf-by-leaf with headers `=== LEAF p{N} ===` into `1910_skaballanovich_typikon_cohort99_source.txt`.
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort99_raw_draft.md` with leaf banners and sequential note numbers (`268. ...`, etc.).
4. Create empty `1910_skaballanovich_typikon_cohort99_footnotes.txt`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort99_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort99_footnotes.txt" --cohort 99`
