# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 77

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 77  
**Physical Leaves**: Physical pages 761 to 770 (`p761.png` through `p770.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2417]` (Notes 583–601 of Volume II, mapping to global indices `[^2417]` through `[^2435]`, 19 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 77 Content Roadmap**:
   - `p761`–`p762`: THE TROPARIA AFTER "GOD IS THE LORD" (`ТРОПАРИ ПО БОГ ГОСПОДЬ`):
     - `p761`: Structure of the Sunday Troparia (*Orig. p. 646*): Resurrection Dismissal Troparion (Apolytikion) of the tone, "Glory... Both now...", Resurrection Theotokion. Notes 583–585 -> `[^2417]`–`[^2419]`.
     - `p762`: Theotokia of the dismissal (*Theotokia Apolytikia*) in the Octoechos (*Orig. p. 647*): Historical evolution from the ancient Sabbaite troparia; Papadopoulos-Kerameus Analecta. Note 586 -> `[^2420]`.
   - `p763`–`p767`: THE PSALTER KATHISMATA AT MATINS (`КАФИЗМЫ НА УТРЕНИ`):
     - `p763`: Distribution of the 20 Kathismata at Matins (*Orig. p. 648*): Two or three kathismata; division into three staseis ("Glories"); sitting during psalmody.
     - `p764`: Choral execution and antiphonal chanting (*Orig. p. 649*): Left and right choirs; ancient Slavic 14th-century Typika (Moscow Synodal MS 328/383). Notes 587, 588 -> `[^2421]`, `[^2422]`.
     - `p765`: Little Litanies following each Kathisma (*Orig. p. 650*): "Again and again in peace..."; priestly exclamations. Notes 589, 590 -> `[^2423]`, `[^2424]`.
     - `p766`: History of continuous psalmody at Matins (*Orig. p. 651*): Proskynetarion, Pseudo-Athanasius *De Virginitate*, Ethiopic nocturnal office (Turaev). Notes 591–596 -> `[^2425]`–`[^2430]`.
     - `p767`: Patristic and manuscript witnesses (*Orig. p. 652*): Pitra *Juris ecclesiastici*, Mai *Nova Patrum Bibliotheca*, Dmitrievsky. Notes 597–600 -> `[^2431]`–`[^2434]`.
   - `p768`–`p770`: THE SESSIONAL HYMNS AFTER THE KATHISMATA (`СЕДАЛЬНЫ ПО КАФИЗМАХ` — *Kathismata* / *Sessionalia*):
     - `p768`: Meaning and nature of the Sessional Hymns (*Orig. p. 653*): Chanted while sitting (sedal'ny); reflection upon the Mystery of Christ's Resurrection. Note 601 -> `[^2435]`.
     - `p769`: Authorship and liturgical antiquity of the Sunday Sessional Hymns (*Orig. p. 654*): St. John of Damascus; historical layers of the Octoechos (0 footnotes on p769).
     - `p770`: Structure of the Sunday Sessional Hymns (*Orig. p. 655*): Two sessional hymns per kathisma, followed by Theotokion; musical models (*podobny*) (0 footnotes on p770).
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[583]` through `[601]` in the body text must be mapped to `[^2417]` through `[^2435]`.
   - Corresponding definitions are located on leaf `p998` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
   - Write exact matching footnote definitions `[^2417]: ...` through `[^2435]: ...` in `1910_skaballanovich_typikon_cohort77_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Matins`, `Kathisma`, `Kathismata`, `Sessional Hymn`, `Sedalen`, `Octoechos`, `Apolytikion`, `Theotokion`, `Typikon`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort77_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort77_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort77_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p761.png` through `p770.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p761 through p770).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort77_raw_draft.md` with footnote markers `[^2417]` through `[^2435]`.
4. Extract and translate footnote definitions 583 through 601 from leaf `p998` into `1910_skaballanovich_typikon_cohort77_footnotes.txt` as `[^2417]: ...` through `[^2435]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort77_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort77_footnotes.txt" --cohort 77`
