# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 70

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 70  
**Physical Leaves**: Physical pages 691 to 700 (`p691.png` through `p700.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2283]` (Notes 449–468 of Volume II, mapping to global indices `[^2283]` through `[^2302]`, 20 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 70 Content Roadmap**:
   - `p691`–`p692`: Prayer of the Augmented Litany:
     - `p691`: The secret prayer of the priest ("O Lord our God, accept this fervent supplication of Thy servants..."). Notes 449–452 -> `[^2283]`–`[^2286]`.
     - `p692`: Rubrics for deacon and priest; exclamation (*Orig. p. 579*) (0 footnotes on p692).
   - `p693`–`p695`: "VOUCHSAFE, O LORD" (`СПОДОБИ ГОСПОДИ` — *Kataxioson Kyrie*):
     - `p693`: The Evening Doxological Prayer: Keeping us this night without sin; praise of God's holy name (0 footnotes on p693).
     - `p694`: Origins and Patristic Parallels (*Orig. p. 580*): Apostolic Constitutions Book VII, c. 48; Gloria in Excelsis link. Note 453 -> `[^2287]`.
     - `p695`: Manuscript Redactions and Variants (*Orig. p. 581*): Comparison with ancient Greek Horologia and Slavic MSS. Note 454 -> `[^2288]`.
   - `p696`–`p700`: THE LITANY OF SUPPLICATION & PRAYER OF THE BOWING OF HEADS (`ПРОСИТЕЛЬНАЯ ЕКТЕНИЯ И МОЛИТВА ГЛАВОПРЕКЛОНЕНИЯ`):
     - `p696`: The Litany of Supplication (*Orig. p. 582*): Meaning of *Aitesis* / *Synapte Plerotike*. Notes 455–457 -> `[^2289]`–`[^2291]`.
     - `p697`: The Six Petitions of Supplication (*Orig. p. 583*): An angel of peace, pardon of sins, a good defense before the judgment seat of Christ; Apostolic Constitutions parallels. Notes 458–462 -> `[^2292]`–`[^2296]`.
     - `p698`: Committal and Priestly Exclamation: "For Thou art a good God and lovest mankind...". Notes 463, 464 -> `[^2297]`, `[^2298]`.
     - `p699`: The Prayer of the Bowing of Heads (*Orig. p. 584*): "O Lord our God, Who didst bow the heavens and come down..."; Syrku *Patriarch Euthymius*. Notes 465–467 -> `[^2299]`–`[^2301]`.
     - `p700`: Priest and Deacon Rubrics (*Orig. p. 585*): "Peace to all!", "Let us bow our heads unto the Lord"; Goar, Dmitrievsky. Note 468 -> `[^2302]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[449]` through `[468]` in the body text must be mapped to `[^2283]` through `[^2302]`.
   - Corresponding definitions are located on leaves `p990` and `p991` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2283]: ...` through `[^2302]: ...` in `1910_skaballanovich_typikon_cohort70_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Kataxioson Kyrie`, `Litany of Supplication`, `Prayer of the Bowing of Heads`, `Sluzhebnik`, `Horologion`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort70_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort70_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort70_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p691.png` through `p700.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p691 through p700).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort70_raw_draft.md` with footnote markers `[^2283]` through `[^2302]`.
4. Extract and translate footnote definitions 449 through 468 from leaves `p990`–`p991` into `1910_skaballanovich_typikon_cohort70_footnotes.txt` as `[^2283]: ...` through `[^2302]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort70_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort70_footnotes.txt" --cohort 70`
