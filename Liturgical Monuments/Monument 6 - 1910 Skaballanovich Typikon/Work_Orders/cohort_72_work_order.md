# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 72

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 72  
**Physical Leaves**: Physical pages 711 to 720 (`p711.png` through `p720.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2337]` (Notes 503–521 of Volume II, mapping to global indices `[^2337]` through `[^2355]`, 19 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 72 Content Roadmap**:
   - `p711`–`p713`: Conclusion of the Litiya at Great Vespers:
     - `p711`: Commemoration of the living and deceased from diptychs / commemoration books (*pomennik* / *synaxarion*, *Orig. p. 596*): Protracted singing of "Lord, have mercy" (*provolokom*). Notes 503, 504 -> `[^2337]`, `[^2338]`.
     - `p712`: Posture of Body at the Prayer "O Master Great in Mercy" (*Orig. p. 597*): Kneeling or bowing; Georgian MS ("preklonshim nam kolena"), ancient Greek Euchologia. Note 505 -> `[^2339]`.
     - `p713`: Concluding Invocations of the Saints (*Orig. p. 598*): St. Nicholas of Myra, St. Athanasius of Alexandria, local patronal saints. Notes 506–508 -> `[^2340]–[^2342]`.
   - `p714`–`p716`: THE APOSTICHA (`СТИХОВНЫ` — *Eis ton stichon* / *Aposticha*):
     - `p714`: Character and Structure of the Aposticha (*Orig. p. 599*): Meaning of *eis ton stichon*; second and concluding cycle of stichera at Vespers. Notes 509–512 -> `[^2343]–[^2346]`.
     - `p715`: Sunday Resurrection Stichera and Theotokia (*Orig. p. 600*): St. John of Damascus; eight tones; non-variable Sunday character. Note 513 -> `[^2347]`.
     - `p716`: Inviolability of Sunday Aposticha (*Orig. p. 601*): Why Sunday aposticha are never replaced or omitted even at feasts (0 footnotes on p716).
   - `p717`–`p718`: "NOW LETTEST THOU THY SERVANT DEPART" (`НЫНЕ ОТПУЩАЕШИ` — *Nunc Dimittis*):
     - `p717`: Meaning and Scripture Foundation (*Orig. p. 602*): Canticle of St. Simeon the God-Receiver (Luke 2:29–32); evening completion of life and history. Notes 514–517 -> `[^2348]–[^2351]`.
     - `p718`: Execution and Recitation in Ancient Typika (*Orig. p. 603*): Chanted vs read by the superior or senior elder; ancient Sabbaite codices. Note 518 -> `[^2352]`.
   - `p719`–`p720`: DISMISSAL TROPARIA & "REJOICE, O VIRGIN THEOTOKOS" (`БОГОРОДИЦЕ ДЕВО`):
     - `p719`: The Dismissal Troparia at Vespers (*Orig. p. 604*): Place and evolution of the troparion; connection with the Kontakion. Note 519 -> `[^2353]`.
     - `p720`: "Rejoice, O Virgin Theotokos" (*Orig. p. 605*): The Byzantine Ave Maria; angelical salutation (Luke 1:28, 42); 3-fold singing at Saturday Vigil. Notes 520, 521 -> `[^2354]`, `[^2355]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[503]` through `[521]` in the body text must be mapped to `[^2337]` through `[^2355]`.
   - Corresponding definitions are located on leaves `p993`, `p994`, and `p995` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2337]: ...` through `[^2355]: ...` in `1910_skaballanovich_typikon_cohort72_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Litiya`, `Aposticha`, `Nunc Dimittis`, `Bogoroditse Devo`, `Pomennik`, `Sluzhebnik`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort72_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort72_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort72_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p711.png` through `p720.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p711 through p720).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort72_raw_draft.md` with footnote markers `[^2337]` through `[^2355]`.
4. Extract and translate footnote definitions 503 through 521 from leaves `p993`–`p995` into `1910_skaballanovich_typikon_cohort72_footnotes.txt` as `[^2337]: ...` through `[^2355]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort72_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort72_footnotes.txt" --cohort 72`
