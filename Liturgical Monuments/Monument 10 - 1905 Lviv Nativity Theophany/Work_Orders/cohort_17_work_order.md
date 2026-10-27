# Work Order: Divine Services for Nativity, Circumcision, and Theophany (Galician Recension, Lviv, 1905) — Cohort 17

**Document ID**: `1905_lviv_nativity_theophany`  
**Cohort Number**: 17  
**Physical Leaves**: Physical pages 161 to 170 (`Page_0161.jpg` through `Page_0170.jpg`, 10 leaves total)  
**Starting Footnote Index**: `[^452]`  
**Governing Genre Register**: **HYMNOGRAPHIC** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 10 - 1905 Lviv Nativity Theophany\Source Text\images`  

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
- **Source Text Transcription**: `Liturgical Monuments\Monument 10 - 1905 Lviv Nativity Theophany\Source Text\1905_lviv_nativity_theophany_cohort17_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 10 - 1905 Lviv Nativity Theophany\Draft\1905_lviv_nativity_theophany_cohort17_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 10 - 1905 Lviv Nativity Theophany\Draft\1905_lviv_nativity_theophany_cohort17_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `Page_0161.jpg` through `Page_0170.jpg` in `Liturgical Monuments\Monument 10 - 1905 Lviv Nativity Theophany\Source Text\images`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p161 through p170).
3. Translate unabridged into `1905_lviv_nativity_theophany_cohort17_raw_draft.md` with inline footnote markers `[^N]`. Emit clear H1 Markdown headers (`# PART I: ...`, `# PART II: ...`, `# APPENDIX: ...`) at major structural divisions of the codex.
4. Write footnote definitions into `1905_lviv_nativity_theophany_cohort17_footnotes.txt` starting at `[^452]`.
5. Flush outputs to disk and advance through the autonomous pipeline.


---

## 4. Monument-Specific Codicological & Formatting Guardrails
**Codicological Notes**: 1-up single-column printed pages (Physical Leaf = Printed Page + 5 across p6..p295). p1..p5 are unnumbered front matter (p1 cloth cover, p2 half-title, p3 Nativity engraving, p4 Zhovkva 1905 Basilian Press title page, p5 Lviv June 21, 1905 Metropolitan Andrey Sheptytsky Imprimatur); p6..p295 are printed pages 1..290; p296 is the unnumbered rear Table of Contents ('Оглавленіе').

**Flash Execution Guardrails**:
- 1-UP GEOMETRY & RUNNING PAGINATION: Every image Page_0001.jpg..Page_0296.jpg is a 1-up single page. Never emit 2-up '[Left Page]' or '[Right Page]' tags, and never emit standalone '[Page N]' or '[Leaf pN]' bracket lines in Draft MD (which fail Gate 1). Only use the required '=== LEAF pN ===' delimiter banner per physical leaf.
- H1 & H2 LANDMARK DISCIPLINE: Emit H1 ('# ...') at the 6 Feast-Cycle Part openings (p6 Royal Hours of Nativity; p71 Great Compline of Nativity; p130 Synaxis of Mother of God & St. Joseph; p177 Vespers of Circumcision & St. Basil; p212 Royal Hours of Theophany; p269 Great Compline of Theophany) and H2 ('## ...') at the remaining 11 service openings from the Оглавленіе (p49, p96, p125, p152, p184, p206, p240, p254, p273, p289, p292, and p296 Original TOC). Render all internal rubrics, Hours, Canons, Odes, Troparia, and Kontakia as inline italic rubrics ('*...*'), never as '###' or '####' headings.
- COLOMETRIC ASTERISKS & DIALOGUE LABELS: Preserve literal '*' chanter breathing-pause asterisks in Source Text. In Draft MD, convert '*' dividers into natural English punctuation (commas, semicolons, colons) so pairs of '*' never corrupt Markdown italics. Format litany and Liturgy speaker labels in bold ('**Priest:**', '**Deacon:**', '**Reader:**', '**Choir:**') and ceremonial rubrics in italics ('*...*').
- GATE-1-SAFE CROSS-REFERENCES & SYMMETRIC PARATEXT (SGC-02 PROTECTION): Render internal page cross-references in body text as '(see p. 285)[^N]' or '(p. 364 [sic; cf. p. 264])[^N]' without expanding incipits and without using '[Leaf ...]' or '[Page ...]' brackets in the body; place the physical leaf coordinate ('Physical Leaf pN = Printed Page + 5') in the footnote definition '[^N]:'. On non-text leaves (p1 front cover, p3 Nativity engraving), provide symmetric diplomatic descriptions in both Source Text and Draft MD so SGC-02 length ratios remain between 0.80 and 1.50.
