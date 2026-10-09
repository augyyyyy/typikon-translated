# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 67

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 67  
**Physical Leaves**: Physical pages 661 to 670 (`p661.png` through `p670.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2202]` (Notes 368–394 of Volume II, mapping to global indices `[^2202]` through `[^2228]`, 27 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 67 Content Roadmap**:
   - `p661`–`p667`: History and Redactions of the Vesperal Entrance:
     - `p661`: Entrance rubrics in the Diataxis of Patriarch Philotheus Kokkinos (*Orig. p. 553*): Comparison between ancient Greek manuscripts and later printed editions (0 footnotes on p661).
     - `p662`: Ancient Georgian and Slavic witnesses (*Orig. p. 554*): Tbilisi MS 86, Moscow Synodal MSS; priest entering without deacon. Note 368 -> `[^2202]`.
     - `p663`: Censing the Holy Table after the Entrance: Goar *Euchologion*, Constantinople Hieratikon. Notes 369, 370 -> `[^2203]`, `[^2204]`.
     - `p664`: The Holy Sepulchre Typikon in Jerusalem (*Orig. p. 555*): Procession into the Anastasis cave / tomb of the Lord (0 footnotes on p664).
     - `p665`: Imperial Entrance at Hagia Sophia (*Orig. p. 556*): Constantine Porphyrogenitus *De Cerimoniis*; emperor's veneration and incense offering; Belyaev *Byzantina*. Notes 371, 372 -> `[^2205]`, `[^2206]`.
     - `p666`: Civil and Court Analogues in Byzantium (*Orig. p. 557*): Candle-bearers and heralds in royal processions; Codinus *De Officiis*; Balsamon, Tobler, Dmitrievsky. Notes 373–379 -> `[^2207]`–`[^2213]`.
     - `p667`: Ancient Russian Hierarchical Entrance Rites (*Orig. p. 558*): *Stoglav* Council of 1551; Archbishop Ambrose, Golubtsov *Chinovniki*. Notes 380, 381 -> `[^2214]`, `[^2215]`.
   - `p668`–`p669`: "O GLADSOME LIGHT" (`СВЕТЕ ТИХИЙ` — *Phos Hilaron*):
     - `p668`: The Evening Hymn *Phos Hilaron* (*Orig. p. 559*): Spiritual light of Christ; singing at the lighting of the lamps. Notes 382–384 -> `[^2216]`–`[^2218]`.
     - `p669`: Authorship and Patristic Attestation (*Orig. p. 560*): St. Sophronius of Jerusalem vs earlier 2nd–3rd century anonymous origin; St. Basil the Great *De Spiritu Sancto* c. 29 citing Athenogenes; Ethiopic Church Order candle prayer. Notes 385–387 -> `[^2219]`–`[^2221]`.
   - `p670`: THE PROKEIMENON AND OLD TESTAMENT READINGS (`ПРОКИМЕН И ПАРЕМИИ`):
     - `p670`: The Evening Prokeimenon (*Orig. p. 561*): Saturday evening Great Prokeimenon "The Lord is King, He is clothed with majesty"; Sunday and weekday prokeimena; Old Believer and ancient Slavic variants. Notes 388–394 -> `[^2222]`–`[^2228]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[368]` through `[394]` in the body text must be mapped to `[^2202]` through `[^2228]`.
   - Corresponding definitions are located on leaves `p985` to `p987` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2202]: ...` through `[^2228]: ...` in `1910_skaballanovich_typikon_cohort67_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Phos Hilaron`, `Prokeimenon`, `Paroemia`, `Diataxis`, `Euchologion`, `Stoglav`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort67_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort67_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort67_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p661.png` through `p670.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p661 through p670).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort67_raw_draft.md` with footnote markers `[^2202]` through `[^2228]`.
4. Extract and translate footnote definitions 368 through 394 from leaves `p985`–`p987` into `1910_skaballanovich_typikon_cohort67_footnotes.txt` as `[^2202]: ...` through `[^2228]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort67_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort67_footnotes.txt" --cohort 67`
