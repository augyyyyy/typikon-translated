# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 66

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 66  
**Physical Leaves**: Physical pages 651 to 660 (`p651.png` through `p660.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2167]` (Notes 333–367 of Volume II, mapping to global indices `[^2167]` through `[^2201]`, 35 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 66 Content Roadmap**:
   - `p651`: Psalm 116 and Concluding Lucernarium Verses (*Orig. p. 544*):
     - Psalm 116 ("O praise the Lord, all ye nations; praise Him, all ye people...").
     - Insertion of stichera at the final 10, 8, 6, or 4 verses; ancient liturgical witnesses (Papadopoulos-Kerameus, Studite Hypotyposis, Diatyposis, St. Symeon of Thessalonica, Kekelidze, Goar). Notes 333–340 -> `[^2167]`–`[^2174]`.
   - `p652`–`p657`: THE STICHERA ON "LORD, I HAVE CRIED" (`СТИХИРЫ НА ГОСПОДИ ВОЗЗВАХ`):
     - `p652`: Sizing and Choir Distribution (*Orig. p. 545*): Stichera count on Sundays (10 stichera); alternating choirs (left and right); canonarch rubrics. Notes 341–344 -> `[^2175]`–`[^2178]`.
     - `p653`: The Resurrection Stichera by St. John of Damascus (*Orig. pp. 546–547*): Ancient Sabbaite stichera (*archaia*); doctrinal depth and poetic elegance. Notes 345–352 -> `[^2179]`–`[^2186]`.
     - `p654`: Concurrence with the Menaion and Anatolian Stichera: Integration of festal saints, martyr stichera, and the Octoechos. Notes 353, 354 -> `[^2187]`, `[^2188]`.
     - `p655`: Stichera of Paul of Amorion: Structure and meter (*Orig. p. 548*). (0 footnotes on p655).
     - `p656`: The Dogmatikon / Theotokion (*Orig. p. 549*): "Glory... Both now..."; the Theotokia Dogmatika of the Eight Tones by St. John of Damascus; theological incarnation theology. Notes 355–358 -> `[^2189]`–`[^2192]`.
     - `p657`: Opening of the Royal Doors during the Dogmatikon: Choir singing from the ambo/choirs; preparation for the Entrance. Note 359 -> `[^2193]`.
   - `p658`–`p660`: THE ENTRANCE AT VESPERS (`ВХОД` — *Introitus* / *Hagios Eisodos*):
     - `p658`: Meaning and Symbolism of the Vesperal Entrance (*Orig. p. 550*): Christ the Light entering the world; candle-bearer preceding the deacon and priest; Evergetis and Sabaite traditions. Notes 360–362 -> `[^2194]`–`[^2196]`.
     - `p659`: Historical Evolution of the Entrance (*Orig. p. 551*): Ancient Lucernarium candle lighting (*lucernare*); agape connection; St. Symeon of Thessalonica, Isaiah 6:3. Notes 363–365 -> `[^2197]`–`[^2199]`.
     - `p660`: Ceremonial Execution of the Entrance (*Orig. p. 552*): Deacon making the sign of the cross with the censer, "Wisdom! Stand upright!" (*Sophia, orthoi!*); bowing towards the east and the Royal Doors. Notes 366, 367 -> `[^2200]`, `[^2201]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[333]` through `[367]` in the body text must be mapped to `[^2167]` through `[^2201]`.
   - Corresponding definitions are located on leaves `p984` and `p985` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2167]: ...` through `[^2201]: ...` in `1910_skaballanovich_typikon_cohort66_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Stichera`, `Dogmatikon`, `Theotokion`, `Vesperal Entrance`, `Royal Doors`, `Sluzhebnik`, `Typikon`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort66_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort66_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort66_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p651.png` through `p660.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p651 through p660).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort66_raw_draft.md` with footnote markers `[^2167]` through `[^2201]`.
4. Extract and translate footnote definitions 333 through 367 from leaves `p984`–`p985` into `1910_skaballanovich_typikon_cohort66_footnotes.txt` as `[^2167]: ...` through `[^2201]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort66_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort66_footnotes.txt" --cohort 66`
