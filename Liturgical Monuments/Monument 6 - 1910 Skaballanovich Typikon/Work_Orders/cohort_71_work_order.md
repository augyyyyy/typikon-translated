# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 71

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 71  
**Physical Leaves**: Physical pages 701 to 710 (`p701.png` through `p710.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2303]` (Notes 469–502 of Volume II, mapping to global indices `[^2303]` through `[^2336]`, 34 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 71 Content Roadmap**:
   - `p701`–`p710`: THE LITIYA AT GREAT VESPERS (`ЛИТИЯ` — *Litiya / Liti / Procession*):
     - `p701`: Introduction to the Litiya (*Orig. p. 586*): Follows the Litany of Supplication and Prayer of the Bowing of Heads; origin and meaning of the Greek term *litē* (entreaty, supplication, procession). Notes 469, 470 -> `[^2303]`, `[^2304]`.
     - `p702`: History of Litai in Constantinople and Jerusalem (*Orig. p. 587*): Processions to urban churches and shrines during public calamities (earthquakes, droughts, barbarian invasions); St. John Chrysostom's nocturnal anti-Arian litai. Notes 471–477 -> `[^2305]`–`[^2311]`.
     - `p703`: Early Typikon Redactions of the Litiya (*Orig. p. 588*): Evolution from city-wide processions to monastic narthex processions in Sabbaite and Studite typika; Moscow Synodal MSS. Notes 478–482 -> `[^2312]`–`[^2316]`.
     - `p704`: The Procession to the Narthex (*Pritvor* / *Katēchoumena*, *Orig. p. 589*): Clergy exit through the Royal Doors with candles and incense; censing of the holy icons, abbot, and brethren; Old Believer and Greek Euchologion rubrics. Notes 483–489 -> `[^2317]`–`[^2323]`.
     - `p705`: Stichera of the Litiya (*Orig. p. 590*): Stichera of the temple dedication / patron saint and of the Menaion; rubrics for Sunday when temple is dedicated to the Mother of God or a Saint. Notes 490–492 -> `[^2324]`–`[^2326]`.
     - `p706`: Musical Execution and Doxastikon (*Orig. p. 591*): Singing "Glory..." (Doxastikon) of the saint or Aposticha of Matins; alternate choral practices in ancient Slavic manuscripts. Note 493 -> `[^2327]`.
     - `p707`: The Litiya Petitions (*Molitva litii*, *Orig. p. 592*): "Save, O God, Thy people, and bless Thine inheritance..."; prayers for the peace of the world, civil authorities, hierarchy, all Christians. Notes 494–496 -> `[^2328]`–`[^2330]`.
     - `p708`: Multi-Fold "Lord, have mercy" (*Orig. p. 593*): Choral responses: 40 times, 30 times, 50 times, 3 times; symbolic liturgical numbers (0 footnotes on p708).
     - `p709`: Commemoration of Saints in the Litiya Prayers (*Orig. p. 594*): The Great Hierarchs (Basil, Gregory the Theologian, John Chrysostom), Apostles, Martyrs, Ascetics. Notes 497–499 -> `[^2331]`–`[^2333]`.
     - `p710`: Monastic Commemorations (*Orig. p. 595*): Commemorating the Archimandrite, Abbot, or local superior in monastic vs secular parishes; ancient Slavonic Euchologia. Notes 500–502 -> `[^2334]`–`[^2336]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[469]` through `[502]` in the body text must be mapped to `[^2303]` through `[^2336]`.
   - Corresponding definitions are located on leaves `p991`, `p992`, and `p993` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2303]: ...` through `[^2336]: ...` in `1910_skaballanovich_typikon_cohort71_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Litiya`, `Narthex`, `Pritvor`, `Stichera`, `Doxastikon`, `Euchologion`, `Typikon`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort71_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort71_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort71_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p701.png` through `p710.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p701 through p710).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort71_raw_draft.md` with footnote markers `[^2303]` through `[^2336]`.
4. Extract and translate footnote definitions 469 through 502 from leaves `p991`–`p993` into `1910_skaballanovich_typikon_cohort71_footnotes.txt` as `[^2303]: ...` through `[^2336]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort71_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort71_footnotes.txt" --cohort 71`
