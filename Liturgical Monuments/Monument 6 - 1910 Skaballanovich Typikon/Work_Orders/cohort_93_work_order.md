# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 93

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 93  
**Physical Leaves**: Physical pages 921 to 930 (`p921.png` through `p930.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2776]` (Notes 942–958 of Volume II, mapping to global indices `[^2776]` through `[^2792]`, 17 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 93 Content Roadmap**:
   - `p921`–`p924`: COMPARATIVE LECTIONARY SYSTEMS: SYRIAN AND NESTORIAN SUNDAY PERICOPES:
     - `p921`: Pericopes of the rich young ruler; reconciliation in Christ (Rom. 5:1–5); call of the Apostles (Matt. 4:12–25).
     - `p922`: Syriac Lectionary system: Feast day and Sunday cycles; Jacobite and Nestorian traditions. Notes 942–944 -> `[^2776]`–`[^2778]`.
     - `p923`: Sundays after Pentecost in the West Syrian rite: Table of Epistles and Gospels.
     - `p924`: Pre-Lenten and Lenten Sunday readings: Meatfare Sunday, Cheesefare Sunday; fasting rubrics. Notes 945–949 -> `[^2779]`–`[^2783]`.
   - `p925`–`p928`: WESTERN COMPARATIVE LECTIONARY SYSTEMS (ROMAN, LUTHERAN, ANGLICAN):
     - `p925`: Sunday Liturgical Readings in the West: Structural architecture of Epistle and Gospel pairings throughout the liturgical year.
     - `p926`: Trinity season readings: Ministry of letter and spirit (2 Cor. 3:4–11); Good Samaritan (Luke 10:23–37); Christ the Mediator (Gal. 3:16–22); The Ten Lepers (Luke 17:11–19).
     - `p927`: Epiphany and Pre-Lenten cycles: Parable of the tares (Matt. 13:24–30); praise of Thessalonians (1 Thess. 1:2–10); mustard seed (Matt. 13:31–35). Note 950 -> `[^2784]`.
     - `p928`: Comparative textual tables: Anglican Book of Common Prayer, Lutheran Agende, and Roman Missal pericopes. Notes 951–957 -> `[^2785]`–`[^2791]`.
   - `p929`–`p930`: ANCIENT ORIENTAL SYSTEMS (ARMENIAN AND COPTIC):
     - `p929`: Patristic readings during Paschaltide: Catholic Epistles and Acts of the Apostles; Baumstark and Conybeare studies. Note 958 -> `[^2792]`.
     - `p930`: The Armenian Lectionary: Systematic thematic structure; preservation of ancient Jerusalem 5th-century cathedral typikon order.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[942]` through `[958]` in the body text must be mapped to `[^2776]` through `[^2792]`.
   - Corresponding definitions are located on leaf `p1016` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (and cached in `scratch/cohort91_96_endnotes_raw.txt`).
   - Write exact matching footnote definitions `[^2776]: ...` through `[^2792]: ...` in `1910_skaballanovich_typikon_cohort93_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Pericope`, `Lectionary`, `Syrian Jacobite`, `Nestorian`, `Armenian`, `Coptic`, `Epistle`, `Gospel`, `Roman Missal`, `Book of Common Prayer`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort93_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort93_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort93_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p921.png` through `p930.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p921 through p930).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort93_raw_draft.md` with footnote markers `[^2776]` through `[^2792]`.
4. Extract and translate footnote definitions 942 through 958 from leaf `p1016` into `1910_skaballanovich_typikon_cohort93_footnotes.txt` as `[^2776]: ...` through `[^2792]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort93_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort93_footnotes.txt" --cohort 93`
