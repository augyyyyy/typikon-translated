# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 90

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 90  
**Physical Leaves**: Physical pages 891 to 900 (`p891.png` through `p900.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2721]` (Notes 887–903 of Volume II, mapping to global indices `[^2721]` through `[^2737]`, 17 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 90 Content Roadmap**:
   - `p891`: CONCLUSION OF THE ALL-NIGHT VIGIL EXPERIMENT:
     - `p891`: Conclusion of the Kyiv Theological Academy All-Night Vigil experiment (*Orig. p. 735*): Chanting the Exapostilaria / Photagogica solo antiphonally in Greek troparion melody; conclusion of the Vigil. (0 footnotes on p891).
   - `p892`–`p896`: THE FIRST HOUR (*ПЕРВЫЙ ЧАС*):
     - `p892`: Relation of the First Hour to the Vigil (*Orig. p. 736*): Historical attachment to Matins; connection between the morning sacrifice and the coming of the True Light. (0 footnotes on p892).
     - `p893`: The Psalms of the First Hour (*Orig. p. 737*): Psalm 5, Psalm 89 ("Lord, Thou hast been our dwelling place in all generations", attributed to Moses), Psalm 100. Notes 887, 888 -> `[^2721]`, `[^2722]`.
     - `p894`: The Troparia and Prayer of the First Hour (*Orig. p. 738*): "In the morning hear my voice, O my King and my God..."; the prayer "O Christ the True Light Who enlightenest and sanctifiest every man that cometh into the world". Notes 889, 890 -> `[^2723]`, `[^2724]`.
     - `p895`: Ancient and Asmatic Redactions of the First Hour (*Orig. p. 739*): "Truly all things are vanity"; 3 prayers in the Sung Office (*Asmatike Akolouthia*). Notes 891–893 -> `[^2725]–[^2727]`.
     - `p896`: Sunday and Festal Features of the First Hour (*Orig. p. 740*): Sunday troparia and kontakia; dismissal rubrics. Note 894 -> `[^2728]`.
   - `p897`–`p899`: THE THIRD HOUR (*ТРЕТИЙ ЧАС*):
     - `p897`: Content of the Third Hour (*Orig. p. 741*): Commemoration of the Descent of the Holy Spirit upon the Apostles at Pentecost (Acts 2:15); Psalms 16, 24, 50. Notes 895–897 -> `[^2729]–[^2731]`.
     - `p898`: Troparion and Theotokion of the Third Hour: "O Lord, Who didst send down Thy Most Holy Spirit at the third hour upon Thine Apostles..."; prayer for the renewal of the Spirit. Note 898 -> `[^2732]`.
     - `p899`: Manuscript Variants and Ancient Horologia (*Orig. p. 743*): Sinai Horologion No. 865 (12th c.); Coptic and Ethiopic parallels. Note 899 -> `[^2733]`.
   - `p900`: THE SIXTH HOUR (*ШЕСТОЙ ЧАС*):
     - `p900`: Content of the Sixth Hour: Commemoration of the Crucifixion of Christ; Psalms 53, 54, 90 ("He that dwelleth in the secret place of the Most High"); the noonday demon (*daimonion mesembrinon*). Notes 900–903 -> `[^2734]–[^2737]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[887]` through `[903]` in the body text must be mapped to `[^2721]` through `[^2737]`.
   - Corresponding definitions are located on leaves `p1013`–`p1014` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (and cached in `scratch/cohort86_90_endnotes_raw.txt`).
   - Write exact matching footnote definitions `[^2721]: ...` through `[^2737]: ...` in `1910_skaballanovich_typikon_cohort90_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `First Hour`, `Third Hour`, `Sixth Hour`, `Christ the True Light`, `Descent of the Holy Spirit`, `Crucifixion`, `Horologion`, `Sinai Horologion`, `Asmatike Akolouthia`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort90_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort90_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort90_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p891.png` through `p900.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p891 through p900).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort90_raw_draft.md` with footnote markers `[^2721]` through `[^2737]`.
4. Extract and translate footnote definitions 887 through 903 from leaves `p1013`–`p1014` into `1910_skaballanovich_typikon_cohort90_footnotes.txt` as `[^2721]: ...` through `[^2737]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort90_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort90_footnotes.txt" --cohort 90`
