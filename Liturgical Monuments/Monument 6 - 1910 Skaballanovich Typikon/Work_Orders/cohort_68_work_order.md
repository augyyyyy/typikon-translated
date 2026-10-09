# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 68

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 68  
**Physical Leaves**: Physical pages 671 to 680 (`p671.png` through `p680.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2229]` (Notes 395–425 of Volume II, mapping to global indices `[^2229]` through `[^2259]`, 31 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 68 Content Roadmap**:
   - `p671`–`p678`: The Vesperal Prokeimenon Concluded:
     - `p671`: The Prokeimenon in the Russian Church (*Stoglav* Council of 1551 disputes). Note 395 -> `[^2229]`.
     - `p672`: The General Character of the Vesperal Prokeimenon (*Orig. p. 562*): Distinction between festal and weekday prokeimena (0 footnotes on p672).
     - `p673`: Ancient Responsorial Psalmody in the 4th–5th Centuries (*Orig. p. 563*): St. John Chrysostom, St. Basil the Great, Western parallels. Notes 396–400 -> `[^2230]`–`[^2234]`.
     - `p674`: Diaconal Acclamations at the Prokeimenon (*Orig. p. 564*): "Wisdom!", "Let us attend!", "Peace to all!"; patristic witnesses (Tertullian, Chrysostom). Notes 401–407 -> `[^2235]`–`[^2241]`.
     - `p675`: Liturgy of St. James and Byzantine dialogues (*Orig. p. 565*): Orlov, Brightman. Notes 408–414 -> `[^2242]`–`[^2248]`.
     - `p676`: Posture of Clergy during the Prokeimenon (*Orig. p. 566*): Sitting at the synthronon / high place. Note 415 -> `[^2249]`.
     - `p677`: Musical Architecture of the Great Saturday Prokeimenon (*Orig. p. 567*): Psalm 92 with its 3 verses; 4 1/2-fold execution. Notes 416–419 -> `[^2250]`–`[^2253]`.
     - `p678`: Theological Exegesis of Psalm 92: "The Lord is King, He is clothed with majesty". Note 420 -> `[^2254]`.
   - `p679`–`p680`: PART 2 OF VESPERS & THE AUGMENTED LITANY (`2-Я ЧАСТЬ ВЕЧЕРНИ И СУГУБАЯ ЕКТЕНИЯ`):
     - `p679`: Transition from Psalmody to Petitionary Prayer (*Orig. p. 568*): Meaning of the second part of Vespers. Note 421 -> `[^2255]`.
     - `p680`: The Augmented Litany (*Сугубая ектения* / *Ektēnēs Hiketeia*, *Orig. p. 569*): "Let us say with all our soul and with all our mind..."; the 3-fold "Lord, have mercy". Notes 422–425 -> `[^2256]`–`[^2259]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[395]` through `[425]` in the body text must be mapped to `[^2229]` through `[^2259]`.
   - Corresponding definitions are located on leaves `p987` to `p989` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2229]: ...` through `[^2259]: ...` in `1910_skaballanovich_typikon_cohort68_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Prokeimenon`, `Augmented Litany`, `Stoglav`, `Synthronon`, `Sluzhebnik`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort68_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort68_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort68_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p671.png` through `p680.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p671 through p680).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort68_raw_draft.md` with footnote markers `[^2229]` through `[^2259]`.
4. Extract and translate footnote definitions 395 through 425 from leaves `p987`–`p989` into `1910_skaballanovich_typikon_cohort68_footnotes.txt` as `[^2229]: ...` through `[^2259]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort68_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort68_footnotes.txt" --cohort 68`
