# Work Order: Lviv Printed Octoechos (Lviv Stauropegion, 1630) — Cohort 22

**Document ID**: `1630_lviv_octoechos`  
**Cohort Number**: 22  
**Physical Leaves**: Physical pages 211 to 220 (`Page_0211.jpg` through `Page_0220.jpg`, 10 leaves total)  
**Starting Footnote Index**: `[^290]`  
**Governing Genre Register**: **HYMNOGRAPHIC** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 9 - 1630 Lviv Octoechos\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/`. Distinguish red cinnabar rubrics (render in italics `*...*`) from black text (render in standard Roman).
2. **Register Enforcement (Hymnographic)**: Concise, imperative, Active Present Indicative for rubrical movements.
3. **Canonical Realia & Loanwords**: `Tetrapod`, `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
4. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
6. **Scripture & Psalter**: Septuagint (LXX) versification mandatory.
7. **Footnote Monotonic Bijectivity**: Every marker `[^N]` in body text MUST have an exact corresponding entry `[^N]:` in the footnotes file.
8. **Universal Heading Hierarchy (Phase 2 Auto-Slicing)**: Reserve top-level H1 headers (`# ...`) strictly for major codex-level divisions (e.g., a new Tone, Month, Book, Rite/Liturgy, Part, or Rear Appendix marked by a primary headpiece/title). Use `##` (H2) and `###` (H3) for daily offices, canons, odes, and internal sub-sections.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 9 - 1630 Lviv Octoechos\Source Text\1630_lviv_octoechos_cohort22_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 9 - 1630 Lviv Octoechos\Draft\1630_lviv_octoechos_cohort22_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 9 - 1630 Lviv Octoechos\Draft\1630_lviv_octoechos_cohort22_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `Page_0211.jpg` through `Page_0220.jpg` in `Liturgical Monuments\Monument 9 - 1630 Lviv Octoechos\Source Text\images`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p211 through p220).
3. Translate unabridged into `1630_lviv_octoechos_cohort22_raw_draft.md` with inline footnote markers `[^N]`. When a new Tone or rear section begins on a leaf, emit its canonical H1 Markdown header on its own line: `# TONE 1`, `# TONE 2`, `# TONE 3`, `# TONE 4`, `# TONE 5`, `# TONE 6`, `# TONE 7`, `# TONE 8`, or `# EXAPOSTILARIA AND EVANGELICAL STICHERA`.
4. Write footnote definitions into `1630_lviv_octoechos_cohort22_footnotes.txt` starting at `[^290]`.
5. Flush outputs to disk and advance through the autonomous pipeline.
