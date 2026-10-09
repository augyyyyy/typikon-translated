# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 63

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 63  
**Physical Leaves**: Physical pages 621 to 630 (`p621.png` through `p630.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2100]` (Notes 266–275 of Volume II, mapping to global indices `[^2100]` through `[^2109]`)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 63 Content Roadmap**:
   - `p621`–`p626`: Comparative Liturgical History of the Great Litany:
     - `p621`: The Litanies of the Armenian Liturgy (*Ekteniya armyanskoy liturgii*, *Orig. p. 520*): Diaconal biddings closely mirroring Byzantine synapte. Note 266 -> `[^2100]`.
     - `p622`: Western Gallican and Mozarabic Litanies (*Orig. p. 521*): Prayers for pope, bishop, rulers, clergy, people, weather, fruits, travelers, captives; *Kyrie eleison* and *Christe eleison*. Note 267 -> `[^2101]`.
     - `p623`–`p625`: The Ancient Slavic Great Litany in archaic codices (23+ petitions, *Orig. pp. 522–524*):
       - `p623`: The 23 petitions of the ancient Slavic Liturgy of St. John Chrysostom and St. Basil the Great in 13th–14th century manuscripts (0 footnotes on p623).
       - `p624`: Detailed breakdown of ancient petitions (for patience, for those in sins/falls, for virgins, widows, orphans, childbearing, travelers, captives; *Testamentum Domini* parallel). Note 268 -> `[^2102]`.
       - `p625`: Kneeling posture in ancient intercession; Apostolic Constitutions parallel. Notes 269, 270 -> `[^2103]`, `[^2104]`.
     - `p626`: Congregational response "Lord, have mercy" (*Kyrie eleison*) in Apostolic Constitutions and ancient liturgies (*Orig. p. 525*). Note 271 -> `[^2105]`.
   - `p626`–`p630`: THE GREAT LITANY IN THE LITURGY OF ST. JAMES AND BYZANTINE CODICES:
     - `p626`: Great Litany in the Liturgy of the Apostle James: Comparison between the Rossano, Paris, and Messina codices (*Orig. p. 525*).
     - `p627`: Petitions for the Patriarch, hierarchy, civil rulers, and people in St. James (*Orig. p. 526*). Note 272 -> `[^2106]`. (Appears before royal and city petitions in Paris MS 476).
     - `p628`: Petitions for cities, villages, monasteries, seafarers, travelers, prisoners, the sick, and afflicted (*Orig. p. 527*). Note 273 -> `[^2107]`.
     - `p629`: Commemoration of the Most Holy Theotokos, Apostles, Prophets, and all saints; 3-fold "Lord, have mercy" (*Orig. p. 528*). Note 274 -> `[^2108]`.
     - `p630`: Evolution of civil ruler petitions in Slavic manuscripts (*Orig. p. 529*): Ancient Kyivan Rus' redactions ("for our grand prince, his boyars, and warriors") down to the 15th–17th centuries; Orlov, Dmitrievsky, Kekelidze. Note 275 -> `[^2109]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[266]` through `[275]` in the body text must be mapped to `[^2100]` through `[^2109]`.
   - Corresponding definitions are located in the Volume II Endnotes apparatus on leaves `p980` to `p981` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2100]: ...` through `[^2109]: ...` in `1910_skaballanovich_typikon_cohort63_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Great Litany`, `Synapte`, `Liturgy of St. James`, `Apostolic Constitutions`, `Sluzhebnik`, `Testamentum Domini`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort63_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort63_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort63_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p621.png` through `p630.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text, Church Slavonic incipits, and Greek/Armenian/Latin citations leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p621 through p630).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort63_raw_draft.md` with footnote markers `[^2100]` through `[^2109]`.
4. Extract and translate footnote definitions 266 through 275 from leaves `p980`–`p981` into `1910_skaballanovich_typikon_cohort63_footnotes.txt` as `[^2100]: ...` through `[^2109]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort63_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort63_footnotes.txt" --cohort 63`
