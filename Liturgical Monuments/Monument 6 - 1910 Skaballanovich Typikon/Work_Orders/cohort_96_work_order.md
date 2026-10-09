# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 96

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 96  
**Physical Leaves**: Physical pages 951 to 960 (`p951.png` through `p960.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2828]` (Notes 994–1000 of Volume II, mapping to global indices `[^2828]` through `[^2834]`, 7 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 96 Content Roadmap**:
   - `p951`–`p953`: CONCLUSION OF THE RITE OF THE ELEVATION OF THE PANAGIA:
     - `p951`: The Cup of the Theotokos: Archdeacon filling the vessel; weekly priest striking the bell (*kandia*); deacon exclaiming: "Through the prayers of our holy master...". (0 footnotes on p951).
     - `p952`: Patriarchal and episcopal blessing: Seeking forgiveness with a bow; "God forgive and have mercy"; Trisagion, troparion or kontakion. Notes 994–996 -> `[^2828]`–`[^2830]`.
     - `p953`: Historical origins in the Jerusalem Typikon: Early development in the Jerusalem Church; Marian Eucharistic devotion. (0 footnotes on p953).
   - `p954`–`p958`: CHAPTER 3 OF THE TYPIKON: "ON A SAINT HAVING A VIGIL, IF IT FALL ON SUNDAY":
     - `p954`: Title and structural rubrics of Chapter 3 (*O svyatem, imushchem bdeniye, ashche prilunitsya v nedeliu*). (0 footnotes on p954).
     - `p955`: General theological synthesis of Sunday vs Saint commemoration: Harmonizing the joy of the Resurrection with the feast of the Saint. Note 997 -> `[^2831]`.
     - `p956`: Combining Resurrectional hymnography with the Saint's office: Sessional hymns, Polyeleos, and Megalynarion. Note 998 -> `[^2832]`.
     - `p957`: Anabathmoi and Matins Gospel rules: Inviolability of the Sunday Resurrection Gospel at Matins. Note 999 -> `[^2833]`.
     - `p958`: Divine Liturgy rubrics: Entrance troparia, prokeimena, epistle, and gospel order. (0 footnotes on p958).
   - `p959`–`p960`: THE RITE OF THE BLESSING OF KOLIVA (*CHIN BLAGOSLOVENIYA KOLIVA*):
     - `p959`: Connection with Chapter 3: Koliva as festive distinction; St. Theodore the Tyro. Note 1000 -> `[^2834]`.
     - `p960`: Concluding exposition of Volume II: Blessing of Koliva in contemporary practice; celebration of Koliva on Friday of the 1st Week of Great Lent; completion of the monumental second volume of the *Tolkovy Typikon*. (0 footnotes on p960).
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[994]` through `[1000]` in the body text must be mapped to `[^2828]` through `[^2834]`.
   - Corresponding definitions are located on leaf `p1022` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (and cached in `scratch/cohort91_96_endnotes_raw.txt`).
   - Write exact matching footnote definitions `[^2828]: ...` through `[^2834]: ...` in `1910_skaballanovich_typikon_cohort96_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Panagia`, `Kandia`, `Kolyvo`, `Koliva`, `St. Theodore the Tyro`, `Vigil`, `Typikon Chapter 3`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort96_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort96_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort96_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p951.png` through `p960.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p951 through p960).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort96_raw_draft.md` with footnote markers `[^2828]` through `[^2834]`.
4. Extract and translate footnote definitions 994 through 1000 from leaf `p1022` into `1910_skaballanovich_typikon_cohort96_footnotes.txt` as `[^2828]: ...` through `[^2834]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort96_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort96_footnotes.txt" --cohort 96`
