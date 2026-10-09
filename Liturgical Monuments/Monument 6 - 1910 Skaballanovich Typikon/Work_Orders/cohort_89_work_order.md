# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 89

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 89  
**Physical Leaves**: Physical pages 881 to 890 (`p881.png` through `p890.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2714]` (Notes 880–886 of Volume II, mapping to global indices `[^2714]` through `[^2720]`, 7 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 89 Content Roadmap**:
   - `p881`: THE STUDITE CATECHESIS CONCLUDED:
     - `p881`: Studite Catecheses concluded (*Orig. p. 727*): Exhortations and reproaches to the brethren ("My brethren and fathers"); reading posture and abbot's blessing. Notes 880–882 -> `[^2714]`–`[^2716]`.
   - `p882`–`p884`: NON-ORTHODOX MATINS (*ИНОСЛАВНЫЕ УТРЕНИ*):
     - `p882`: Comparative overview (*Orig. p. 728*): Differences between Byzantine Matins and Western/Eastern non-Orthodox morning offices. (0 footnotes on p882).
     - `p883`: Western Roman Catholic and Ambrosian Matins (*Orig. p. 729*): Nocturns, readings, responsories; penitential troparia and Gospel readings (Luke 11:5–13, Mark 13:32–37). Notes 883–885 -> `[^2717]`–`[^2719]`.
     - `p884`: Anglican and Protestant Morning Offices (*Orig. p. 730*): Anglican Morning Prayer / Matins; "O Lord, open Thou our lips...", Psalm 50, Psalm 69; Gloria Patri. Note 886 -> `[^2720]`.
   - `p885`–`p890`: PRACTICAL FEASIBILITY OF THE ENTIRE ALL-NIGHT VIGIL TYPIKON (*ПРАКТИЧЕСКАЯ ОСУЩЕСТВИМОСТЬ ВСЕГО УСТАВА ВСЕНОЩНОЙ*):
     - `p885`: Mikhail Skaballanovich's celebrated historical experiment: Celebration of the complete All-Night Vigil without cuts at the Kyiv Theological Academy church. (0 footnotes on p885).
     - `p886`: Participation of Academy students and faculty (*Orig. p. 731*): Course distribution, choir organization, solemn preparation. (0 footnotes on p886).
     - `p887`: The Vigil begins at sunset (*Orig. p. 732*): Closed royal doors, priest standing before the analogion at the right solea throughout the night; opening psalm. (0 footnotes on p887).
     - `p888`: Choral execution of the Kathismata and Stichera (*Orig. p. 733*): Kyiv-Pechersk Lavra chant; antiphonal alternation between choirs; bass soloists. (0 footnotes on p888).
     - `p889`: The Great Patristic Readings during the Vigil (*Orig. p. 734*): Readings from the Acts and St. John Chrysostom at the left solea analogion; brethren sitting and listening. (0 footnotes on p889).
     - `p890`: The Kanon and conclusion at dawn: The triumphant, victorious melody of the Kyiv-Pechersk Lavra Kanon; culmination in the Great Doxology and dawn dismissal. (0 footnotes on p890).
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[880]` through `[886]` in the body text must be mapped to `[^2714]` through `[^2720]`.
   - Corresponding definitions are located on leaves `p1012`–`p1013` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (and cached in `scratch/cohort86_90_endnotes_raw.txt`).
   - Write exact matching footnote definitions `[^2714]: ...` through `[^2720]: ...` in `1910_skaballanovich_typikon_cohort89_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `All-Night Vigil`, `Kyiv Theological Academy`, `Kyiv-Pechersk Lavra chant`, `Great Reading`, `Analogion`, `Solea`, `Studite Catechesis`, `Non-Orthodox Matins`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort89_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort89_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort89_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p881.png` through `p890.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p881 through p890).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort89_raw_draft.md` with footnote markers `[^2714]` through `[^2720]`.
4. Extract and translate footnote definitions 880 through 886 from leaves `p1012`–`p1013` into `1910_skaballanovich_typikon_cohort89_footnotes.txt` as `[^2714]: ...` through `[^2720]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort89_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort89_footnotes.txt" --cohort 89`
