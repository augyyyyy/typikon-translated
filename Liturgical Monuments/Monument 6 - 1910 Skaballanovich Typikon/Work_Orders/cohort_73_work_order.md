# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 73

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 73  
**Physical Leaves**: Physical pages 721 to 730 (`p721.png` through `p730.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2356]` (Notes 522–538 of Volume II, mapping to global indices `[^2356]` through `[^2372]`, 17 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 73 Content Roadmap**:
   - `p721`–`p722`: "Rejoice, O Virgin Theotokos" Concluded:
     - `p721`: Western and Italian parallels (*Orig. p. 606*): Cryptaferrata MS Falascae (13th c.); comparison of text. Notes 522–525 -> `[^2356]`–`[^2359]`.
     - `p722`: Ancient Sabbaite execution (*Orig. p. 607*): Georgian and Greek MSS on 3-fold execution. Note 526 -> `[^2360]`.
   - `p723`–`p726`: THE BLESSING OF LOAVES, WHEAT, WINE, AND OIL (`БЛАГОСЛОВЕНИЕ ХЛЕБОВ` — *Artoklasia*):
     - `p723`: Historical and Liturgical Meaning (*Orig. p. 608*): Vespers replacing the ancient agape meal; monastic sustenance during the Vigil. Notes 527–530 -> `[^2361]`–`[^2364]`.
     - `p724`: Preparation of the Five Loaves (*Orig. p. 609*): Loaves, wheat, wine, and oil on the litiya tray / table. Note 531 -> `[^2365]`.
     - `p725`: The Prayer of Artoklasia (*Orig. p. 610*): "O Lord Jesus Christ our God, Who didst bless the five loaves in the wilderness..."; historical comparison with ancient Euchologia (0 footnotes on p725).
     - `p726`: Cellarer (*Kelar*) and Rubrics (*Orig. p. 611*): Moscow Synodal MS 332/385; five loaves and wine flagon; ancient Russian monastic typika. Note 532 -> `[^2366]`.
   - `p727`–`p730`: "BLESSED BE THE NAME OF THE LORD" & CONCLUSION OF GREAT VESPERS:
     - `p727`: "Blessed be the name of the Lord from this time forth..." (*Orig. p. 612*): Connection with Divine Liturgy dismissal (0 footnotes on p727).
     - `p728`: Responsorial Psalmody and Liturgy of St. James (*Orig. p. 613*): Messina MS (10th c.); pre-communion chant. Notes 533–535 -> `[^2367]`–`[^2369]`.
     - `p729`: Singing of Psalm 33 (*Orig. p. 614*): "I will bless the Lord at all times..."; distribution of blessed bread and wine to the faithful (0 footnotes on p729).
     - `p730`: Priestly Blessing and Mohyla Sluzhebnik (*Orig. p. 615*): "The blessing of the Lord be upon you..."; Kyiv 1629 Sluzhebnik variants. Notes 536–538 -> `[^2370]`–`[^2372]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[522]` through `[538]` in the body text must be mapped to `[^2356]` through `[^2372]`.
   - Corresponding definitions are located on leaves `p995` and `p996` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2356]: ...` through `[^2372]: ...` in `1910_skaballanovich_typikon_cohort73_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Artoklasia`, `Kelar`, `Litiya`, `Sluzhebnik`, `Typikon`, `Psalm 33`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort73_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort73_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort73_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p721.png` through `p730.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p721 through p730).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort73_raw_draft.md` with footnote markers `[^2356]` through `[^2372]`.
4. Extract and translate footnote definitions 522 through 538 from leaves `p995`–`p996` into `1910_skaballanovich_typikon_cohort73_footnotes.txt` as `[^2356]: ...` through `[^2372]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort73_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort73_footnotes.txt" --cohort 73`
