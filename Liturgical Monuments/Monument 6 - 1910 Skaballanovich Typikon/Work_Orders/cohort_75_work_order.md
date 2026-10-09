# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 75

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 75  
**Physical Leaves**: Physical pages 741 to 750 (`p741.png` through `p750.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2387]` (Notes 553–563 of Volume II, mapping to global indices `[^2387]` through `[^2397]`, 11 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 75 Content Roadmap**:
   - `p741`–`p743`: THE BEGINNING OF MATINS & THE BELL-PEAL (`НАЧАЛО УТРЕНИ`):
     - `p741`: Introduction to Festal Matins (*Orig. p. 626*): The second and primary part of the All-Night Vigil; bell chime for Matins (*Zvon k utrene*) (0 footnotes on p741).
     - `p742`: Bell rubrics and ancient Sluzhebniki (*Orig. p. 627*): Old Believer typika, Moscow 1602/1647 Sluzhebnik three-fold peal. Note 553 -> `[^2387]`.
     - `p743`: Western monastic comparisons (*Orig. p. 628*): Rule of St. Benedict c. 8; commentators on Benedictine Nocturns. Notes 554, 555 -> `[^2388]`, `[^2389]`.
   - `p744`–`p748`: THE SIX PSALMS (`ШЕСТОПСАЛМИЕ` — *Hexapsalmos*):
     - `p744`: Structural Architecture of the Six Psalms (*Orig. p. 629*): Psalms 3, 37, 62, 87, 102, 142; standing in silence; extinguishing lights (0 footnotes on p744).
     - `p745`: Exegetical and liturgical balance of the psalms (*Orig. p. 630*): Selection of morning versicles. Note 556 -> `[^2390]`.
     - `p746`: Rubrics for superior and brethren (*Orig. p. 631*): Standing up at the conclusion of the Great Reading; "Amen"; ancient Sabbaite codices. Note 557 -> `[^2391]`.
     - `p747`: History and Origin of the Hexapsalmos (*Orig. p. 632*): Monastic origin in Palestine; transition from cathedral vigils; Greek and Slavic witnesses. Notes 558–562 -> `[^2392]`–`[^2396]`.
     - `p748`: Middle Doxology ("Glory... Alleluia") (*Orig. p. 633*): Printed Greek Horologion, Moscow 1658 Horologion comparisons. Note 563 -> `[^2397]`.
   - `p749`–`p750`: THE TWELVE MORNING PRAYERS (`УТРЕННИЕ МОЛИТВЫ` — *Euchai Orthrinai*):
     - `p749`: Priest reciting the 12 morning prayers before the Royal Doors (*Orig. p. 634*) (0 footnotes on p749).
     - `p750`: Theological content of the 12 prayers (*Orig. p. 635*): Petitions for all estates of Christians; priestly exclamation (0 footnotes on p750).
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[553]` through `[563]` in the body text must be mapped to `[^2387]` through `[^2397]`.
   - Corresponding definitions are located on leaf `p997` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2387]: ...` through `[^2397]: ...` in `1910_skaballanovich_typikon_cohort75_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Matins`, `Orthros`, `Hexapsalmos`, `Six Psalms`, `Euchai Orthrinai`, `Sluzhebnik`, `Typikon`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort75_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort75_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort75_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p741.png` through `p750.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p741 through p750).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort75_raw_draft.md` with footnote markers `[^2387]` through `[^2397]`.
4. Extract and translate footnote definitions 553 through 563 from leaf `p997` into `1910_skaballanovich_typikon_cohort75_footnotes.txt` as `[^2387]: ...` through `[^2397]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort75_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort75_footnotes.txt" --cohort 75`
