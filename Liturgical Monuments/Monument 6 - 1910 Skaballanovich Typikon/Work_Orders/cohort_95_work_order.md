# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 95

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 95  
**Physical Leaves**: Physical pages 941 to 950 (`p941.png` through `p950.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2809]` (Notes 975–993 of Volume II, mapping to global indices `[^2809]` through `[^2827]`, 19 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 95 Content Roadmap**:
   - `p941`–`p944`: HISTORY AND RITUAL OF THE ELEVATION OF THE PANAGIA:
     - `p941`: Post-prandial thanksgiving prayer; connection to ancient agape meals. Note 975 -> `[^2809]`.
     - `p942`: Ancient monastic practice of elevating the bread fragment (*ukrukh*): "Glory to Thee, our God, glory to Thee. Glory to the Father and to the Son and to the Holy Spirit. Great is the name of the Holy Trinity. Lord Jesus Christ, help us". Notes 976–980 -> `[^2810]`–`[^2814]`.
     - `p943`: Studite refectory customs: Seating by tables of nine; refectory reading; brothers sitting in head-coverings (*kuvuklia*) during winter. Notes 981, 982 -> `[^2815]`, `[^2816]`.
     - `p944`: Overseer (*nadsmotrshchik*) enforcing silence; cellarer collecting spoons; reader receiving the superior's blessing. Note 983 -> `[^2817]`.
   - `p945`–`p947`: BYZANTINE AND MONASTIC TYPIKA:
     - `p945`: The common blessing: "Lord bless, pray"; priest blessing food and drink: "Christ God, through the prayers of our fathers...". (0 footnotes on p945).
     - `p946`: Hegumen elevating the bread: "Lord Jesus Christ our God, have mercy on us"; deposition of bread on dish. Note 984 -> `[^2818]`.
     - `p947`: Constantinople Pantokrator Monastery Typikon (1136 AD): Comparison of differences; reception of antidoron; three strokes on the wooden semantron. Note 985 -> `[^2819]`.
   - `p948`–`p950`: ANCIENT SLAVIC AND PRINTED REDACTIONS:
     - `p948`: Ancient Slavic liturgical formulas: "Glory to Thee, O King, glory to Thee, O Holy One... Bless me... God save thee". Notes 986–989 -> `[^2820]`–`[^2823]`.
     - `p949`: Post-prandial prayer: "Lord God...". (0 footnotes on p949).
     - `p950`: Marian hymnic invocation: "All generations bless thee, O Virgin Theotokos, most blessed and immaculate Mother of our God..."; "It is Truly Meet" or Megalynarion. Notes 990–993 -> `[^2824]`–`[^2827]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[975]` through `[993]` in the body text must be mapped to `[^2809]` through `[^2827]`.
   - Corresponding definitions are located on leaf `p1017` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (and cached in `scratch/cohort91_96_endnotes_raw.txt`).
   - Write exact matching footnote definitions `[^2809]: ...` through `[^2827]: ...` in `1910_skaballanovich_typikon_cohort95_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Panagia`, `Trapeza`, `Refectory`, `Ukrukh`, `Pantokrator Typikon`, `Kuvuklia`, `Semantron`, `Antidoron`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort95_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort95_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort95_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p941.png` through `p950.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p941 through p950).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort95_raw_draft.md` with footnote markers `[^2809]` through `[^2827]`.
4. Extract and translate footnote definitions 975 through 993 from leaf `p1017` into `1910_skaballanovich_typikon_cohort95_footnotes.txt` as `[^2809]: ...` through `[^2827]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort95_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort95_footnotes.txt" --cohort 95`
