# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 78

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 78  
**Physical Leaves**: Physical pages 771 to 780 (`p771.png` through `p780.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2436]` (Notes 602–614 of Volume II, mapping to global indices `[^2436]` through `[^2448]`, 13 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 78 Content Roadmap**:
   - `p771`–`p773`: CONCLUSION OF THE SESSIONAL HYMNS & PATRISTIC READINGS:
     - `p771`: Sessional Theotokia in the Octoechos (*Orig. p. 656*): Kyiv-Pechersk Lavra traditions (Notes 602–604 -> `[^2436]`–`[^2438]`).
     - `p772`: Patristic readings following the Kathismata (*Orig. p. 657*): Reading from St. John Chrysostom or the Homilies of the Fathers (0 footnotes on p772).
     - `p773`: Western comparisons (*Orig. p. 658*): Roman Breviary Nocturn readings and blessings. Note 605 -> `[^2439]`.
   - `p774`–`p775`: THE AMOMOS / 17TH KATHISMA (`НЕПОРОЧНЫ` — *Amōmos* / Psalm 118):
     - `p774`: Psalm 118 on Sundays (*Orig. p. 659*): Meaning of "Blessed are the undefiled in the way"; Christological walking in the law of the Lord (0 footnotes on p774).
     - `p775`: Replacement of Amomos by Polyeleos (*Orig. p. 660*): Sabbaite vs Studite practice; weekday vs festal usage (0 footnotes on p775).
   - `p776`–`p780`: THE POLYELEOS & GREAT CENSING (`ПОЛИЕЛЕЙ И КАЖДЕНИЕ ВЕЛИКОЕ`):
     - `p776`: Meaning of the Polyeleos (*Orig. p. 661*): "Praise ye the name of the Lord" (Pss. 134–135); "For His mercy endureth forever" (*Polyeleos* / "Many Mercies"). Notes 606–608 -> `[^2440]`–`[^2442]`.
     - `p777`: The Liturgical Climax of the All-Night Vigil (*Orig. p. 662*): Lighting of all church lamps, polycandela, and opening of Royal Doors. Note 609 -> `[^2443]`.
     - `p778`: History of the Polyeleos (*Orig. p. 663*): Symeon of Thessalonica; 7th-century Jerusalem Canonarion (Kekelidze); ancient Slavic codices. Notes 610, 611 -> `[^2444]`, `[^2445]`.
     - `p779`: The Great Censing at the Polyeleos (*Orig. p. 664*): Priest and deacon censing the whole church, iconostasis, choirs, and people; Moscow manuscripts. Notes 612, 613 -> `[^2446]`, `[^2447]`.
     - `p780`: Choral performance and festal refrains (*Orig. p. 665*): Royal Hours of Theophany comparison; Megalynaria on feast days. Note 614 -> `[^2448]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[602]` through `[614]` in the body text must be mapped to `[^2436]` through `[^2448]`.
   - Corresponding definitions are located on leaves `p998`–`p1000` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2436]: ...` through `[^2448]: ...` in `1910_skaballanovich_typikon_cohort78_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Amomos`, `Polyeleos`, `Kathisma`, `Sessional Hymn`, `Theotokion`, `Great Censing`, `Typikon`, `Sluzhebnik`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort78_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort78_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort78_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p771.png` through `p780.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p771 through p780).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort78_raw_draft.md` with footnote markers `[^2436]` through `[^2448]`.
4. Extract and translate footnote definitions 602 through 614 from leaves `p998`–`p1000` into `1910_skaballanovich_typikon_cohort78_footnotes.txt` as `[^2436]: ...` through `[^2448]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort78_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort78_footnotes.txt" --cohort 78`
