# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 64

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 64  
**Physical Leaves**: Physical pages 631 to 640 (`p631.png` through `p640.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2110]` (Notes 276–318 of Volume II, mapping to global indices `[^2110]` through `[^2152]`, 43 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 64 Content Roadmap**:
   - `p631`–`p637`: Conclusion of the Great Litany:
     - `p631`: The Congregational Response "Lord, have mercy" (*Kyrie eleison*, *Orig. p. 530*): Spiritual and theological depths; crying out for divine mercy in all tribulations. Notes 276–281 -> `[^2110]`–`[^2115]`.
     - `p632`: Western vs Eastern practices (*Orig. p. 531*): Pope Gregory the Great's letter on *Kyrie eleison* and *Christe eleison*; alternating clergy and people. Notes 282–286 -> `[^2116]`–`[^2120]`.
     - `p633`: The Exclamation of the Priest concluding the Great Litany (*Orig. p. 532*): "For unto Thee is due all glory, honor, and worship..." (*Hoti prepei soi pasa doxa...*); evolution of doxological formulae. Notes 287–296 -> `[^2121]`–`[^2130]`.
     - `p634`–`p635`: Petitions for Civil Authorities in East and West (*Orig. pp. 533–534*): Baruch, 1 Timothy 2:1–2, Roman Canon of the Mass (*Te Igitur*), Mozarabic and Gallican practices. Notes 297–309 -> `[^2131]`–`[^2143]`.
     - `p636`: The Great Litany at Vespers and Matins (*Orig. p. 535*): Transferred from the Divine Liturgy; liturgical differences. (0 footnotes on p636).
     - `p637`: Diataxis of Patriarch Philotheus Kokkinos: Rubrics for priest saying the Great Litany if deacon is vesting for the third antiphon of the Psalter. Notes 310–312 -> `[^2144]`–`[^2146]`.
   - `p638`–`p640`: "BLESSED IS THE MAN" (`БЛАЖЕН МУЖ` — The First Kathisma at Vespers):
     - `p638`: The Kathisma at Vespers: Why the First Kathisma (Psalms 1, 2, 3) is sung at Saturday Great Vespers; continuous psalmody beginning the liturgical week. Note 313 -> `[^2147]`.
     - `p639`: Messianic and Christological interpretation of Psalm 1, 2, 3: Christ Himself as the true "Blessed Man" Who walks not in the counsel of the ungodly; His passion and resurrection. Notes 314–316 -> `[^2148]`–`[^2150]`.
     - `p640`: Musical and liturgical execution of "Blessed is the Man": Singing with Alleluia refrain; ancient Georgian (13th c.) and Slavic manuscripts. Notes 317, 318 -> `[^2151]`, `[^2152]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[276]` through `[318]` in the body text must be mapped to `[^2110]` through `[^2152]`.
   - Corresponding definitions are located in the Volume II Endnotes apparatus on leaves `p981` to `p983` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2110]: ...` through `[^2152]: ...` in `1910_skaballanovich_typikon_cohort64_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Great Litany`, `Kyrie Eleison`, `Blessed is the Man`, `First Kathisma`, `Diataxis`, `Sluzhebnik`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort64_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort64_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort64_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p631.png` through `p640.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p631 through p640).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort64_raw_draft.md` with footnote markers `[^2110]` through `[^2152]`.
4. Extract and translate footnote definitions 276 through 318 from leaves `p981`–`p983` into `1910_skaballanovich_typikon_cohort64_footnotes.txt` as `[^2110]: ...` through `[^2152]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort64_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort64_footnotes.txt" --cohort 64`
