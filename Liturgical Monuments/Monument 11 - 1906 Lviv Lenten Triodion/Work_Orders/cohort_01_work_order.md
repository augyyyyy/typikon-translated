# Work Order: Lviv Stauropegion Lenten Triodion (Lviv, 1906) — Cohort 1

**Document ID**: `1906_lviv_triodion_lenten`  
**Cohort Number**: 1  
**Physical Leaves**: Physical pages 1 to 10 (`Page_0001.jpg` through `Page_0010.jpg`, 10 leaves total)  
**Starting Footnote Index**: `[^1]`  
**Governing Genre Register**: **HYMNOGRAPHIC** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 11 - 1906 Lviv Lenten Triodion\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/`. Distinguish red cinnabar rubrics (render in italics `*...*`) from black text (render in standard Roman).
2. **Register Enforcement (Hymnographic)**: Concise, imperative, Active Present Indicative for rubrical movements.
3. **Canonical Realia & Loanwords**: `Tetrapod`, `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
4. **Father Paul Doxology & Anti-Slop Standard**: Banned phrase *"for ever and ever"* (use *"unto ages of ages"*). Strictly ban pseudo-archaic slop (`wherefore` -> use `therefore`; `wondrous` -> use `marvelous`; `verily` -> use `truly`; `hearken` -> use `give ear`; `resplendent`/`effulgent` -> use `radiant`; never use 3rd-person `-eth` verbs: `singeth`, `proclaimeth`, `censeth`, `entereth`, `maketh`, `readeth`, `beginneth`, `taketh`, `vesteth`, `boweth`, `kisseth`, `turneth`, `standeth`).
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
6. **Scripture & Psalter**: Septuagint (LXX) versification mandatory.
7. **Footnote Monotonic Bijectivity**: Every marker `[^N]` in body text MUST have an exact corresponding entry `[^N]:` in the footnotes file.
8. **Strict Epigraphic Markdown Discipline**: Never invent or interpolate modern liturgical office or structural headings (`## At Sunday Midnight Office`, `## At Sunday Matins`, `### Canon...`, `#### Ode...`). Liturgical rubrics, genre indicators, ode numbers, troparion labels, kathismata, and prosomoia must be rendered strictly as inline italicized text (e.g. `*Ode 1, Tone 2. Heirmos:*`, `*Troparion:*`, `*Sessional Hymn, Tone 2:*`). Markdown headings (`#`) are strictly restricted to primary decorative woodcut headpieces (e.g. `# TONE 1`, `# TONE 2`, `# PREFACE: TO THE READER`) explicitly sanctioned in the publication spec and present on the physical page. Any other markdown header (`#`, `##`, `###`, `####`) will trigger an immediate Small Pause Gate failure.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 11 - 1906 Lviv Lenten Triodion\Source Text\1906_lviv_triodion_lenten_cohort1_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 11 - 1906 Lviv Lenten Triodion\Draft\1906_lviv_triodion_lenten_cohort1_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 11 - 1906 Lviv Lenten Triodion\Draft\1906_lviv_triodion_lenten_cohort1_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `Page_0001.jpg` through `Page_0010.jpg` in `Liturgical Monuments\Monument 11 - 1906 Lviv Lenten Triodion\Source Text\images`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p1 through p10).
3. Translate unabridged into `1906_lviv_triodion_lenten_cohort1_raw_draft.md` with inline footnote markers `[^N]`. Emit clear H1 Markdown headers (`# PART I: ...`, `# PART II: ...`, `# APPENDIX: ...`) at major structural divisions of the codex.
4. Write footnote definitions into `1906_lviv_triodion_lenten_cohort1_footnotes.txt` starting at `[^1]`.
5. Flush outputs to disk and advance through the autonomous pipeline.


---

## 4. Monument-Specific Codicological & Formatting Guardrails
**Codicological Notes**: 1-up single-column printed liturgical folios (Physical Leaf = Printed Page + 4 across p5..p532). p1..p4 are unnumbered front matter (p1 title page with Stauropegion seal, p2 Dormition church bell tower engraving, p3 Sheptytsky/Chekhovych/Khomyshyn hierarchy blessing leaf, p4 opening prayer to Jesus Christ); p5..p532 are printed pages 1..528 concluding with colophon 'Конецъ и Бгу Слава' on p532 (fol. 528).

**Flash Execution Guardrails**:
- 1-UP GEOMETRY & RUNNING PAGINATION: Every image Page_0001.jpg..Page_0532.jpg is a 1-up single folio leaf. Never emit 2-up '[Left Page]' or '[Right Page]' tags, and never emit standalone '[Page N]' or '[Leaf pN]' bracket lines in Draft MD (which fail Gate 1). Only use the required '=== LEAF pN ===' delimiter banner per physical leaf.
- H1 & H2 LANDMARK DISCIPLINE: Emit H1 ('# ...') at major liturgical divisions: '# PRE-LENTEN PERIOD' (p5 Sunday of Publican & Pharisee), '# FIRST WEEK OF THE GREAT FAST' (Clean Week / Great Canon), '# SECOND WEEK OF THE GREAT FAST', '# THIRD WEEK OF THE GREAT FAST', '# FOURTH WEEK OF THE GREAT FAST', '# FIFTH WEEK OF THE GREAT FAST', '# SIXTH WEEK OF THE GREAT FAST (PALM WEEK)', '# LAZARUS SATURDAY AND PALM SUNDAY', '# GREAT AND HOLY PASSION WEEK', and '# MARKIAN CHAPTERS (ANNUNCIATION DURING LENT)' (p530). Render internal day/service openings as H2 ('## ...'), and sub-services, hours, canons, odes, troparia, and stichera as inline italic rubrics ('*...*'), never as deep H3/H4 heading bloat.
- COLOMETRIC ASTERISKS & LITURGICAL ACCENTS: Preserve literal '*' chanter breathing-pause asterisks in Source Text. In Draft MD, convert '*' dividers into natural English punctuation (commas, semicolons, colons) so pairs of '*' never corrupt Markdown italics. Format litany, dialogue, and Liturgy speaker labels in bold ('**Priest:**', '**Deacon:**', '**Reader:**', '**Choir:**') and ceremonial actions in italics ('*...*') with active present indicative verbs.
- GATE-1-SAFE CROSS-REFERENCES & SYMMETRIC PARATEXT (SGC-02 PROTECTION): Render internal page/folio cross-references in body text as '(see fol. 285)[^N]' without expanding unwritten incipits; place the physical leaf coordinate ('Physical Leaf pN = Printed Page + 4') in the footnote definition '[^N]:'. On non-hymnic frontispieces (p1 title page, p2 Dormition tower engraving, p3 blessing leaf, p4 opening prayer), provide symmetric diplomatic descriptions and complete translations so SGC-02 length ratios remain between 0.80 and 1.50.
- PRESERVATION OF INCIPITS & NO EXPANSION (RULE 16): When hymns, troparia, or prayers are printed only by their incipits (e.g., '**"Lord, have mercy"**', '**"Glory..."**), translate strictly the printed words in quotation marks and never interpolate unwritten strophes into the translation body.
