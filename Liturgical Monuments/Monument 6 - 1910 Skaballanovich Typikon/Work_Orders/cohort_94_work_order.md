# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 94

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 94  
**Physical Leaves**: Physical pages 931 to 940 (`p931.png` through `p940.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2793]` (Notes 959–974 of Volume II, mapping to global indices `[^2793]` through `[^2808]`, 16 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 94 Content Roadmap**:
   - `p931`–`p933`: THE HYMN TO THE THEOTOKOS & THE COMMUNION VERSE:
     - `p931`: Replacement of "It is Truly Meet" by "All of Creation Rejoiceth in Thee" (*O Tebe raduetsia*) at the Divine Liturgy of St. Basil the Great. Notes 959–961 -> `[^2793]`–`[^2795]`.
     - `p932`: Musical performance of *O Tebe raduetsia*: First choir chanting simply (*chyma*) then transitioning to slow solemn Tone 1 chant. Note 962 -> `[^2796]`.
     - `p933`: The Communion Verse (*Kinonikon* / *Prichasten*): History and liturgical antiquity; Psalm 148:1 "Praise the Lord from the heavens"; chanting after the second kinonikon. Notes 963, 964 -> `[^2797]`, `[^2798]`.
   - `p934`–`p935`: POST-COMMUNION PRAYERS & LITURGY DISMISSAL:
     - `p934`: Ancient dialogue between deacon and clergy: "Deacon: Render praises unto God; Clergy: Praise unto Him in the church of the saints..."; priestly thanksgiving prayer. Notes 965–969 -> `[^2799]`–`[^2803]`.
     - `p935`: The Dismissal of the Divine Liturgy: Distribution of antidoron; concluding prayers and thanksgiving of the communicants. Note 970 -> `[^2804]`.
   - `p936`–`p940`: THE ELEVATION OF THE PANAGIA (*CHIN O PANAGII* — *HYPSOSIS TES PANAGIAS*):
     - `p936`: Meaning and Theological Essence: Transfer of blessed bread (*panagia*) from church to refectory (*trapeza*); continuation of the liturgical synaxis at the monastic meal. Note 971 -> `[^2805]`.
     - `p937`: Tripartite structure of the Rite: 1) Procession to the refectory, 2) Meal in holy silence with patristic reading, 3) Thanksgiving and elevation. Notes 972–974 -> `[^2806]`–`[^2808]`.
     - `p938`: Typikon Chapter 35 correlations: "Let each sit in his order with reverence and silence"; refectory as church annex. (0 footnotes on p938).
     - `p939`: The Post-Prandial Elevation: Completion of the meal; preliminary thanksgiving prayer leading into the elevation. (0 footnotes on p939).
     - `p940`: The Elevation Formula: Deacon or cellarer holding the bread with three fingers of both hands, elevating slightly above the icon of the Holy Trinity and proclaiming aloud: "Great is the name..." (0 footnotes on p940).
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[959]` through `[974]` in the body text must be mapped to `[^2793]` through `[^2808]`.
   - Corresponding definitions are located on leaves `p1016`–`p1017` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (and cached in `scratch/cohort91_96_endnotes_raw.txt`).
   - Write exact matching footnote definitions `[^2793]: ...` through `[^2808]: ...` in `1910_skaballanovich_typikon_cohort94_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Panagia`, `Kinonikon`, `Prichasten`, `Antidoron`, `Trapeza`, `Refectory`, `Hypsosis`, `All of Creation Rejoiceth in Thee`, `O Tebe raduetsia`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort94_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort94_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort94_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p931.png` through `p940.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p931 through p940).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort94_raw_draft.md` with footnote markers `[^2793]` through `[^2808]`.
4. Extract and translate footnote definitions 959 through 974 from leaves `p1016`–`p1017` into `1910_skaballanovich_typikon_cohort94_footnotes.txt` as `[^2793]: ...` through `[^2808]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort94_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort94_footnotes.txt" --cohort 94`
