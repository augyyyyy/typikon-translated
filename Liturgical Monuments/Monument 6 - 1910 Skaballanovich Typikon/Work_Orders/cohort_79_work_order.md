# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 79

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 79  
**Physical Leaves**: Physical pages 781 to 790 (`p781.png` through `p790.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2449]` (Notes 615–628 of Volume II, mapping to global indices `[^2449]` through `[^2462]`, 14 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 79 Content Roadmap**:
   - `p781`–`p783`: THE RESURRECTIONAL EVLOGETARIA (`НЕПОРОЧНЫ / ТРОПАРИ ПО НЕПОРОЧНАХ` — *Evlogētaria*):
     - `p781`: "Blessed art Thou, O Lord, teach me Thy statutes" (*Orig. p. 666*): The assembly of the angels was amazed beholding Thee among the dead.
     - `p782`: Ancient Sabbaite and Greek Horologia witnesses (*Orig. p. 667*): Papadopoulos-Kerameus Analecta, Horologion rubrics. Notes 615, 616 -> `[^2449]`, `[^2450]`.
     - `p783`: The Little Litany following the Evlogetaria (*Orig. p. 668*): Venice Euchologia, Petro Mohyla 1629 Sluzhebnik, and Moscow 1602/1647 editions. Note 617 -> `[^2451]`.
   - `p784`–`p785`: THE HYPAKOE (`ИПАКОИ` — *Hypakoē*):
     - `p784`: Meaning and patristic etymology (*Orig. p. 669*): Attentive hearing of the Resurrection message; St. Athanasius, St. John Chrysostom, St. Augustine. Notes 618–621 -> `[^2452]`–`[^2455]`.
     - `p785`: Musical execution and liturgical position (*Orig. p. 670*): Chanted on Sundays in place of Sessional hymn after the 3rd Kathisma (0 footnotes on p785).
   - `p786`–`p788`: THE ANABATHMOI / HYMNS OF DEGREES (`СТЕПЕННЫ` — *Anabathmoi*):
     - `p786`: Gradual Psalms (Pss. 119–133) in the Octoechos (*Orig. p. 671*): Three antiphons for Tones 1–7, four antiphons for Tone 8; theological Pneumatology of the Holy Spirit (0 footnotes on p786).
     - `p787`: Authorship of St. Theodore the Studite and St. Joseph the Hymnographer (*Orig. p. 672*): Nikephoros Kallistos, Nicodemus the Hagiorite *Nea Klimax*, Archbishop Modest. Notes 622–625 -> `[^2456]`–`[^2459]`.
     - `p788`: Musical performance and manuscript history (*Orig. p. 673*): Kekelidze, Moscow Rumiantsev MS Sev. 491/35, Moscow Synodal MSS. Note 626 -> `[^2460]`.
   - `p789`–`p790`: THE MATINS PROKEIMENON (`ПРОКИМЕН УТРЕНИ`):
     - `p789`: Structure and festal versicle (*Orig. p. 674*): Deacon exclaiming the prokeimenon; antiphonally chanted by choirs; comparison with Vesperal Prokeimenon. Note 627 -> `[^2461]`.
     - `p790`: Rubrics of ancient Greek and Slavic Typika (*Orig. p. 675*): Proskynetarion, Holy Sepulchre practices; transition to the Matins Gospel. Note 628 -> `[^2462]`.
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[615]` through `[628]` in the body text must be mapped to `[^2449]` through `[^2462]`.
   - Corresponding definitions are located on leaf `p1000` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2449]: ...` through `[^2462]: ...` in `1910_skaballanovich_typikon_cohort79_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Evlogetaria`, `Hypakoe`, `Anabathmoi`, `Hymns of Degrees`, `Prokeimenon`, `Octoechos`, `Typikon`, `Sluzhebnik`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort79_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort79_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort79_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p781.png` through `p790.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p781 through p790).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort79_raw_draft.md` with footnote markers `[^2449]` through `[^2462]`.
4. Extract and translate footnote definitions 615 through 628 from leaf `p1000` into `1910_skaballanovich_typikon_cohort79_footnotes.txt` as `[^2449]: ...` through `[^2462]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort79_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort79_footnotes.txt" --cohort 79`
