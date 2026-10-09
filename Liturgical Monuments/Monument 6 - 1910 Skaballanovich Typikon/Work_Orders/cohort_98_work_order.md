# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 98

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 98  
**Physical Leaves**: Physical pages 971 to 980 (`p971.png` through `p980.png`, 10 leaves total)  
**Starting Footnote Index**: N/A (Volume II Endnotes Folios — Notes 118 through 267 of Volume II)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` (`Page_0971.jpg`..`Page_0980.jpg`) and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (pages 971–980, pre-cached in `scratch/cohort98_source_raw.txt`).
2. **Endnotes Folios Formatting (Volume I Precedent: Cohorts 46–54 & User Decisions A2, A3)**:
   - Format each leaf with banner `=== LEAF p{N} ===` and translate each numbered note sequentially (`118. ...`, `119. ...`, etc.).
   - Leave `1910_skaballanovich_typikon_cohort98_footnotes.txt` empty (0 bytes), as the markdown text itself constitutes the critical notes apparatus.
   - Do NOT insert footnote markers `[^N]` in the markdown text.
3. **Apparatus Epigraphy & Translation Standard**:
   - Translate all Greek, Latin, German, and Church Slavonic patristic citations and critical commentary into fluent, rigorous scholarly English.
   - Preserve technical realia, manuscript shelfmarks, and Greek/Slavonic terms parenthetically.
4. **Cohort 98 Note Coverage (Notes 118–267)**:
   - `p971`–`p973`: Notes 118–158 (Scriptural pericopes; Duhm's *Die Psalmen*; St. Basil; St. John Chrysostom; the Ninth Hour and early Byzantine daily offices; Byzantine court rubrics in *De Cerimoniis Aulae Byzantinae*).
   - `p974`–`p976`: Notes 159–224 (Hieromonk John Rakhmanov; D. Belyaev's *Byzantina*; the Great Euchologion of Spyridon Zervos; incense and light rituals at Vespers; ancient Christian evening psalmody).
   - `p977`–`p980`: Notes 225–267 (Antiphonal choral psalmody of Psalm 103 with refrains *“Blessed art Thou, O Lord”* and *“Wonderful are Thy works, O Lord”*; the kneeling prayers of Pentecost; Migne Latin Patrology; F. E. Brightman's *Liturgies Eastern and Western*; Ivan Karabinov).
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*). Human subjects remain lowercase.
6. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
7. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort98_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort98_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort98_footnotes.txt` (empty file)

---

## 3. Autonomous Execution Instructions
1. Inspect images `p971.png` through `p980.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`.
2. Transcribe Russian source text, Church Slavonic citations, Latin and Greek apparatus leaf-by-leaf with headers `=== LEAF p{N} ===` into `1910_skaballanovich_typikon_cohort98_source.txt`.
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort98_raw_draft.md` with leaf banners and sequential note numbers (`118. ...`, etc.).
4. Create empty `1910_skaballanovich_typikon_cohort98_footnotes.txt`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort98_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort98_footnotes.txt" --cohort 98`
