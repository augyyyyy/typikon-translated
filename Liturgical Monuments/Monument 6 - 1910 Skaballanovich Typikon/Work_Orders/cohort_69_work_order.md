# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 69

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 69  
**Physical Leaves**: Physical pages 681 to 690 (`p681.png` through `p690.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2260]` (Notes 426–448 of Volume II, mapping to global indices `[^2260]` through `[^2282]`, 23 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 69 Content Roadmap**:
   - `p681`–`p690`: History and Textual Evolution of the Augmented Litany (`Сугубая ектения` — *Ektenēs Hiketeia*):
     - `p681`: Theological depth and concentration of prayer (*Orig. p. 570*): Intense supplication; etymology of Greek *kopiaō* (Matt. 6:28). Note 426 -> `[^2260]`.
     - `p682`: Primitive Forms in Early Byzantine Liturgies (*Orig. p. 571*): The 17-petition litany in Barberini gr. 336; deēthōmen biddings. Note 427 -> `[^2261]`.
     - `p683`: Ancient Redactions of St. John Chrysostom and St. Basil: Comparison of petitions across Italian and Oriental codices. Note 428 -> `[^2262]`.
     - `p684`: Petitions for Health, Salvation, and Forgiveness (*Orig. p. 572*): The "plodonosyashchikh" (those who bear fruit and do good works) bidding; historical development. Notes 429–431 -> `[^2263]`–`[^2265]`.
     - `p685`: Slavic Manuscripts of the 14th–16th Centuries (*Orig. p. 573*): "Rtsom vsi...", "Gospodi Vsederzhitelyu..."; comparison of Moscow Synodal MSS. Notes 432, 433 -> `[^2266]`, `[^2267]`.
     - `p686`: Petitions for the Hierarchy and Brotherhood (*Orig. p. 574*): Monastic commemorations in ancient Rus' (0 footnotes on p686).
     - `p687`: Kyivan and Ruthenian Redactions (*Orig. p. 575*): Kyiv Mohyla Sluzhebnik of 1629; 15th–16th century variants. Notes 434–438 -> `[^2268]`–`[^2272]`.
     - `p688`: Comparison with Early Printed Venetian and Moscow Editions (*Orig. p. 576*): 1519 Bozidar Vukovic, 1602 Venice, 1655 Patriarch Nikon. Notes 439, 440 -> `[^2273]`, `[^2274]`.
     - `p689`: Constantinople vs Jerusalem Redactions (*Orig. p. 577*): Differences in the dismissal petitions; Orlov, Dmitrievsky. Notes 441–444 -> `[^2275]`–`[^2278]`.
     - `p690`: 12-Fold and 40-Fold "Lord, have mercy" (*Orig. p. 578*): Monastic psalmody practices and liturgical multiplication. Notes 445–448 -> `[^2279]`–`[^2282]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[426]` through `[448]` in the body text must be mapped to `[^2260]` through `[^2282]`.
   - Corresponding definitions are located on leaves `p989` and `p990` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2260]: ...` through `[^2282]: ...` in `1910_skaballanovich_typikon_cohort69_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Augmented Litany`, `Ektenes`, `Sluzhebnik`, `Typikon`, `Barberini Euchologion`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort69_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort69_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort69_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p681.png` through `p690.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p681 through p690).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort69_raw_draft.md` with footnote markers `[^2260]` through `[^2282]`.
4. Extract and translate footnote definitions 426 through 448 from leaves `p989`–`p990` into `1910_skaballanovich_typikon_cohort69_footnotes.txt` as `[^2260]: ...` through `[^2282]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort69_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort69_footnotes.txt" --cohort 69`
