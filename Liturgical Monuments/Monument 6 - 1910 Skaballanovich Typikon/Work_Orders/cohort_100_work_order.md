# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 100

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 100  
**Physical Leaves**: Physical pages 991 to 1000 (`p991.png` through `p1000.png`, 10 leaves total)  
**Starting Footnote Index**: N/A (Volume II Endnotes Folios — Notes 458 through 639 of Volume II)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` (`Page_0991.jpg`..`Page_1000.jpg`) and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (pages 991–1000, pre-cached in `scratch/cohort100_source_raw.txt`).
2. **Endnotes Folios Formatting (Volume I Precedent: Cohorts 46–54 & User Decisions A2, A3)**:
   - Format each leaf with banner `=== LEAF p{N} ===` and translate each numbered note sequentially (`458. ...`, `459. ...`, etc.).
   - Note 457 continues from leaf p990 onto p991; continue its translation seamlessly under `=== LEAF p991 ===`.
   - Leave `1910_skaballanovich_typikon_cohort100_footnotes.txt` empty (0 bytes), as the markdown text itself constitutes the critical notes apparatus.
   - Do NOT insert footnote markers `[^N]` in the markdown text.
3. **Apparatus Epigraphy & Translation Standard**:
   - Translate all Greek, Latin, German, and Church Slavonic patristic citations and critical commentary into fluent, rigorous scholarly English.
   - Preserve technical realia, manuscript shelfmarks, and Greek/Slavonic terms parenthetically.
4. **Cohort 100 Note Coverage (Notes 458–639)**:
   - `p991`–`p993`: Notes 458–503 (Vesperal Prokeimena of the Eight Tones; Old Testament readings / Paremias; the Augmented Litany at Vespers *“Let us say with our whole soul...”*).
   - `p994`–`p996`: Notes 504–549 (The evening prayer *“Vouchsafe, O Lord, to keep us this night without sin”*; the Litany of Supplication; the Prayer at the Bowing of Heads; the Litiya and procession to the narthex).
   - `p997`–`p1000`: Notes 550–639 (The Blessing of the Five Loaves / Artoklasia; the Troparion *“O Virgin Theotokos, rejoice”*; the Six Psalms of Matins / Hexapsalmos; *“God is the Lord”* and the Troparia; the Kathismata and Sessional Hymns; the Polyeleos and Megalynarion; the Anabathmoi and the Matins Resurrection Gospel).
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*). Human subjects remain lowercase.
6. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
7. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort100_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort100_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort100_footnotes.txt` (empty file)

---

## 3. Autonomous Execution Instructions
1. Inspect images `p991.png` through `p1000.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`.
2. Transcribe Russian source text, Church Slavonic citations, Latin and Greek apparatus leaf-by-leaf with headers `=== LEAF p{N} ===` into `1910_skaballanovich_typikon_cohort100_source.txt`.
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort100_raw_draft.md` with leaf banners and sequential note numbers (`458. ...`, etc.).
4. Create empty `1910_skaballanovich_typikon_cohort100_footnotes.txt`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort100_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort100_footnotes.txt" --cohort 100`
