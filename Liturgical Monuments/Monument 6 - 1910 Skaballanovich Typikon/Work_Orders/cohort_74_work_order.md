# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 74

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 74  
**Physical Leaves**: Physical pages 731 to 740 (`p731.png` through `p740.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2373]` (Notes 539–552 of Volume II, mapping to global indices `[^2373]` through `[^2386]`, 14 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 74 Content Roadmap**:
   - `p731`–`p733`: THE GREAT READING (`ЧТЕНИЕ ВЕЛИКОЕ`):
     - `p731`: Patristic readings after Artoklasia (*Orig. p. 616*): Reading from the Acts of the Apostles, the Epistles, or St. John Chrysostom. Note 539 -> `[^2373]`.
     - `p732`: Liturgical solemnity and selection of reading texts (*Orig. p. 617*): Selection of pericopes suited to feast days; reading posture. Note 540 -> `[^2374]`.
     - `p733`: Monastic practice in the Russian Church (*Orig. p. 618*): Solovki Monastery and Valaam traditions; Greek and Athonite customs. Notes 541, 542 -> `[^2375]`, `[^2376]`.
   - `p734`–`p737`: FRACTION AND CONSUMPTION OF BREAD AND WINE (`ХЛЕБОЛОМЛЕНИЕ И ПОЧЕРПАНИЕ`):
     - `p734`: Distribution of the blessed bread and wine (*Orig. p. 619*): Cellarer and brethren; sustenance during nocturnal vigil (0 footnotes on p734).
     - `p735`: Sluzhebnik rubrics on the virtues of blessed bread (*Orig. p. 620*): "Blessed bread is an aid against all evils if received with faith" (0 footnotes on p735).
     - `p736`: Comparison of 17th-century printed Sluzhebniki (*Orig. p. 621*): Moscow editions of 1602 and 1647; Kyiv Mohyla Sluzhebnik of 1629. Notes 543, 544 -> `[^2377]`, `[^2378]`.
     - `p737`: Ancient ascetical witnesses (*Orig. p. 622*): Miracles of St. Anthony the Great; concluding synthesis of Great Vespers. Note 545 -> `[^2379]`.
   - `p738`–`p740`: NON-ORTHODOX VESPERS (`ИНОСЛАВНЫЕ ВЕЧЕРНИ`):
     - `p738`: Comparative Liturgical Overview (*Orig. p. 623*): Comparison of Byzantine Vespers with Western and Oriental non-Orthodox traditions. Notes 546, 547 -> `[^2380]`, `[^2381]`.
     - `p739`: Western Catholic Vespers and Compline (*Orig. p. 624*): Roman Breviary, Gallican and Mozarabic elements. Notes 548–551 -> `[^2382]`–`[^2385]`.
     - `p740`: Protestant and Anglican Evening Offices (*Orig. p. 625*): Anglican Book of Common Prayer Evensong; Lutheran afternoon services. Note 552 -> `[^2386]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[539]` through `[552]` in the body text must be mapped to `[^2373]` through `[^2386]`.
   - Corresponding definitions are located on leaves `p996` and `p997` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2373]: ...` through `[^2386]: ...` in `1910_skaballanovich_typikon_cohort74_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Great Reading`, `Artoklasia`, `Sluzhebnik`, `Typikon`, `Evensong`, `Breviary`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort74_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort74_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort74_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p731.png` through `p740.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p731 through p740).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort74_raw_draft.md` with footnote markers `[^2373]` through `[^2386]`.
4. Extract and translate footnote definitions 539 through 552 from leaves `p996`–`p997` into `1910_skaballanovich_typikon_cohort74_footnotes.txt` as `[^2373]: ...` through `[^2386]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort74_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort74_footnotes.txt" --cohort 74`
