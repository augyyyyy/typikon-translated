# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 97

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 97  
**Physical Leaves**: Physical pages 961 to 970 (`p961.png` through `p970.png`, 10 leaves total)  
**Starting Footnote Index**: N/A (Volume II Endnotes Folios — Notes 1 to ~117 of Volume II)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` (`Page_0961.jpg`..`Page_0970.jpg`) and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (pages 961–970).
2. **Endnotes Folios Formatting (Volume I Precedent: Cohorts 46–54)**:
   - Leaves 961–970 contain the first 10 leaves of Skaballanovich's critical apparatus for Volume II: *Примечания* (Notes to Volume II).
   - In accordance with the user-approved decision (Decision A2), format each leaf with banner `=== LEAF p{N} ===` and translate each numbered note sequentially (`1. ...`, `2. ...`, etc.).
   - Leave `1910_skaballanovich_typikon_cohort97_footnotes.txt` empty (0 bytes), as the markdown text itself constitutes the critical notes apparatus.
3. **Apparatus Epigraphy & Translation Standard (Decision A3)**:
   - Translate all patristic Greek, Latin, German, and Church Slavonic citations and scholarly commentary into fluent, rigorous scholarly English.
   - Preserve technical Greek terms, Slavonic incipits, manuscript shelfmarks, and key realia parenthetically (e.g., `*τύπος*`, `*τυπικός*`, `*ordo*`, `*Stoglav*`).
4. **Cohort 97 Note Coverage**:
   - `p961`: Heading `### Notes to Volume II: Explanatory Typikon`; Notes 1–10 (Etymology and usage of *typos* and *typikon* in Plutarch, Philostratus, Socrates Scholasticus, Clement of Alexandria, Origen, Basil the Great, Athanasius, John Chrysostom, Cyril of Alexandria; ancient euchologia and monastic charters).
   - `p962`: Notes 11–21 (Manuscript codices: Moscow Synodal MS 328/383, 329/384, Sofia MS 1052; Goar's *Euchologion*; Philotheus Kokkinos *Diataxis*; early printed Typika).
   - `p963`: Notes 22–30 (The structure of Little Vespers; incense offerings; light and lamp lighting; Palestinian vs Studite usages).
   - `p964`: Notes 31–43 (The opening blessing *“Blessed is our God...”*; the Trisagion Prayers; Psalm 103; the Great Litany petitions).
   - `p965`: Notes 44–77 (Kathisma psalmody; the *Kathisma* verses; the Little Litany after psalmody; the singing of *“Lord, I have cried”* and Tone structures).
   - `p966`: Notes 78–93 (St. Sozomen, Archbishop Philaret Gumilevsky; demonic temptations during psalmody; the doxological formulas; beginning of Note 93 on the Alleluia).
   - `p967`: Note 93 continued (Monumental historical excursus on the twofold vs threefold Alleluia controversy; the Stoglav Council of 1551; the Life of St. Euphrosynus of Pskov; patriarchal decrees).
   - `p968`: Note 93 concluded and Notes 94–105 (Third-century Trinitarian dogmatics; Tertullian; ancient Jewish and early Christian psalmody; the Evening Entrance and *Phos Hilaron*).
   - `p969`: Notes 106–117 (Manuscript Horologia in Moscow Synodal and Typographical libraries; Boris Turaev's *Ethiopic Horologion*; Dmitrievsky *Typika*; start of Note 117 on Roman Breviary capitula).
   - `p970`: Note 117 concluded and following notes (Comparative analysis of Western Roman Catholic Divine Office hours: capitula, responsories, Preces, collect prayers, Prime and Compline parallels).
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*). Human subjects remain lowercase.
6. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
7. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort97_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort97_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort97_footnotes.txt` (empty file)

---

## 3. Autonomous Execution Instructions
1. Inspect images `p961.png` through `p970.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`.
2. Transcribe Russian source text, Church Slavonic citations, Latin and Greek apparatus leaf-by-leaf with headers `=== LEAF p{N} ===` into `1910_skaballanovich_typikon_cohort97_source.txt`.
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort97_raw_draft.md` with leaf banners and sequential note numbers (`1. ...`, `2. ...`).
4. Create empty `1910_skaballanovich_typikon_cohort97_footnotes.txt`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort97_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort97_footnotes.txt" --cohort 97`
