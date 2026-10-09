# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 103 (FINAL COHORT)

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 103  
**Physical Leaves**: Physical pages 1021 to 1022 (`p1021.png` and `p1022.png`, 2 leaves total)  
**Starting Footnote Index**: N/A (Volume II Endnotes Folios — Notes 996 through 1000 of Volume II)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` (`Page_1021.jpg`, `Page_1022.jpg`) and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (pages 1021–1022, pre-cached in `scratch/cohort103_source_raw.txt`).
2. **Final Monument Leaves & Leaf Conservation Law (Rule 15)**:
   - Cohort 103 contains the final two leaves of the monument (`p1021` and `p1022`), bringing the cumulative translated leaves to exactly 1,022 / 1,022 physical leaves (`remaining_pages == 0`).
   - Format each leaf with banner `=== LEAF p{N} ===` and translate each numbered note sequentially (`996. ...`, `997. ...`, etc.).
   - Note 995 citation begins on leaf p1020; continue its translation seamlessly under `=== LEAF p1021 ===`.
   - Leave `1910_skaballanovich_typikon_cohort103_footnotes.txt` empty (0 bytes).
3. **Cohort 103 Note Coverage (Notes 996–1000)**:
   - `p1021`: Continuation of Note 995; Note 996 (Pseudo-Kodinos *De officialibus*, p. 7; comprehensive comparative analysis of the Roman Breviary refectory table blessing: *prandium* and *coena*, *Benedicite*, *Oculi omnium*, *Pater noster*, *Mensae caelestis*, *Tu autem Domine*, *Agimus tibi gratias*, *Dispersit dedit pauperibus*, *Edent pauperes*, Holy Week and Paschal table blessings; *Breviarium Romanum*, Ratisbon, 1897).
   - `p1022`: Note 996 concluded; Note 997 (Monthly feast cycles in ancient Coptic and Abyssinian Churches; weekly commemoration of Christ's death and resurrection); Note 998 (The Megalynarion as a later addition unto the Polyeleos); Note 999 (Ancient Paschal troparia after Great Doxology); Note 1000 (Etymology of *kollyba* and the apparition of St. Theodore the Tyro to the bishop). Note 1000 is the final word of the monument!
4. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*). Human subjects remain lowercase.
5. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
6. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort103_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort103_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort103_footnotes.txt` (empty file)

---

## 3. Autonomous Execution Instructions
1. Inspect images `p1021.png` and `p1022.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`.
2. Transcribe Russian source text, Church Slavonic citations, Latin and Greek apparatus leaf-by-leaf with headers `=== LEAF p{N} ===` into `1910_skaballanovich_typikon_cohort103_source.txt`.
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort103_raw_draft.md` with leaf banners and sequential note numbers (`996. ...`, etc.).
4. Create empty `1910_skaballanovich_typikon_cohort103_footnotes.txt`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort103_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort103_footnotes.txt" --cohort 103`
