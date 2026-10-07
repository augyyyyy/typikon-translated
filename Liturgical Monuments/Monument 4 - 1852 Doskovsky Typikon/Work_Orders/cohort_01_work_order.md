# Work Order: Typikon of Fr. Jacob Doskovsky (Peremyshl, 1852) — Cohort 1

**Document ID**: `1852_doskovsky_typikon`  
**Cohort Number**: 1  
**Physical Leaves**: Physical facsimile leaves p1 to p10 (`p1.png` through `p10.png`, 10 leaves total)  
**Book Page Concordance**:
- `p1.png`: Book Page [1] (Title Page)
- `p2.png`: Book Pages [2] (Epigraphs) & [3] (Beginning of General Rule)
- `p3.png` through `p10.png`: Book Pages 4 through 19 (Small Vespers, All-Night Vigil, Great Vespers)
**Starting Footnote Index**: `[^1]`  
**Governing Genre Register**: **RUBRICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 4 - 1852 Doskovsky Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/`. Distinguish red cinnabar rubrics (render in italics `*...*`) from black text (render in standard Roman).
2. **Register Enforcement (Rubrical)**: Concise, imperative, Active Present Indicative for rubrical movements (*"The Priest enters the sanctuary, kisses the Holy Table, and begins..."*). Absolute ban on legalistic "shall".
3. **Canonical Realia & Loanwords**: `Tetrapod`, `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
4. **Father Paul Doxology Standard**: Complete ban on *"for ever and ever"*; mandatory: *"now and forever, and unto the ages of ages"*.
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*). Celebrants, saints, and human rubrical actors remain lowercase.
6. **Scripture & Psalter**: Septuagint (LXX) versification mandatory.
7. **Footnote Monotonic Bijectivity**: Every marker `[^N]` in body text MUST have an exact corresponding entry `[^N]:` in the footnotes file.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 4 - 1852 Doskovsky Typikon\Source Text\1852_doskovsky_typikon_cohort1_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 4 - 1852 Doskovsky Typikon\Draft\1852_doskovsky_typikon_cohort1_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 4 - 1852 Doskovsky Typikon\Draft\1852_doskovsky_typikon_cohort1_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p1.png` through `p10.png` in `Liturgical Monuments\Monument 4 - 1852 Doskovsky Typikon\Source Text\images` using `view_file`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{N} ===` and page sub-headers `--- Page {L} ---` / `--- Page {R} ---`.
3. Translate unabridged into `1852_doskovsky_typikon_cohort1_raw_draft.md` with primary spread banner `<!-- LEAF: p{N} -->` and sub-markers `[Book Page {L}]` and `[Book Page {R}]`, with inline footnote markers `[^N]`.
4. Write footnote definitions into `1852_doskovsky_typikon_cohort1_footnotes.txt` starting at `[^1]`.
5. Flush outputs to disk and advance through the autonomous pipeline.

