# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 76

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 76  
**Physical Leaves**: Physical pages 751 to 760 (`p751.png` through `p760.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2398]` (Notes 564–582 of Volume II, mapping to global indices `[^2398]` through `[^2416]`, 19 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 76 Content Roadmap**:
   - `p751`–`p753`: THE TWELVE MORNING PRAYERS CONCLUDED (`УТРЕННИЕ МОЛИТВЫ`):
     - `p751`: History of the Morning Prayers (*Orig. p. 636*): Comparison with ancient cathedral vigils in Hagia Sophia; Euchologion of Barberini gr. 336.
     - `p752`: Development in monastic euchologia (*Orig. p. 637*): Sinai ascetics, Evergetis Typikon, and Philotheus Kokkinos Diataxis.
     - `p753`: Priestly posture and rubrics (*Orig. p. 638*): Recitation before the Holy Doors bareheaded; manuscript variants. Notes 564–566 -> `[^2398]`–`[^2400]`.
   - `p754`–`p755`: THE GREAT LITANY AT MATINS (`ВЕЛИКАЯ ЕКТЕНИЯ НА УТРЕНИ`):
     - `p754`: Position of the Great Litany (*Orig. p. 639*): Comparison with Great Vespers; priestly exclamation "For unto Thee is due all glory, honor, and worship...". Note 567 -> `[^2401]`.
     - `p755`: Liturgical significance and connection to the dawn (*Orig. p. 640*): Transition from nocturnal silence to choral psalmody. Notes 568, 569 -> `[^2402]`, `[^2403]`.
   - `p756`–`p760`: "GOD IS THE LORD" & "ALLELUIA" (`БОГ ГОСПОДЬ И АЛЛИЛУИА`):
     - `p756`: Psalm 117 verses and the proclamation "God is the Lord and hath appeared unto us" (*Orig. p. 641*): Theological Christological meaning of the epiphany of Christ into the world. Notes 570, 571 -> `[^2404]`, `[^2405]`.
     - `p757`: Historical origin of "God is the Lord" (*Orig. p. 642*): Ancient Palestinian and Sabbaite traditions; contrast with Lenten Alleluia. Notes 572–576 -> `[^2406]`–`[^2410]`.
     - `p758`: Choral and diaconal execution (*Orig. p. 643*): Deacon chanting the 4 verses at the ambo; Kyiv-Pechersk Lavra rubrics. Note 577 -> `[^2411]`.
     - `p759`: "Alleluia" on fasting days (*Orig. p. 644*): The Triadica (Troitsy); Trinity troparia of the Eight Tones. Notes 578, 579 -> `[^2412]`, `[^2413]`.
     - `p760`: Evolution of "God is the Lord" in 17th-century printed books (*Orig. p. 645*): Moscow 1602, 1647, 1658 and Petro Mohyla 1629 Sluzhebniki; Greek Horologia. Notes 580–582 -> `[^2414]`–`[^2416]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[564]` through `[582]` in the body text must be mapped to `[^2398]` through `[^2416]`.
   - Corresponding definitions are located on leaves `p997` and `p998` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2398]: ...` through `[^2416]: ...` in `1910_skaballanovich_typikon_cohort76_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Matins`, `Orthros`, `Euchai Orthrinai`, `Great Litany`, `God is the Lord`, `Alleluia`, `Triadica`, `Sluzhebnik`, `Typikon`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort76_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort76_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort76_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p751.png` through `p760.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p751 through p760).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort76_raw_draft.md` with footnote markers `[^2398]` through `[^2416]`.
4. Extract and translate footnote definitions 564 through 582 from leaves `p997`–`p998` into `1910_skaballanovich_typikon_cohort76_footnotes.txt` as `[^2398]: ...` through `[^2416]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort76_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort76_footnotes.txt" --cohort 76`
