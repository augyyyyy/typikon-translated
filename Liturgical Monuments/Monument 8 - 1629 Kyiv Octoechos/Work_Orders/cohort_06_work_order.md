# Work Order: Kyiv-Pechersk Lavra Octoechos (Kyiv, 1629) — Cohort 6

**Document ID**: `1629_kyiv_octoechos`  
**Cohort Number**: 6  
**Physical Leaves**: Physical pages 51 to 60 (`Page_0051.jpg` through `Page_0060.jpg`, 10 leaves total)  
**Starting Footnote Index**: `[^64]`  
**Governing Genre Register**: **HYMNOGRAPHIC** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 8 - 1629 Kyiv Octoechos\Source Text\images`  

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
- **Source Text Transcription**: `Liturgical Monuments\Monument 8 - 1629 Kyiv Octoechos\Source Text\1629_kyiv_octoechos_cohort6_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 8 - 1629 Kyiv Octoechos\Draft\1629_kyiv_octoechos_cohort6_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 8 - 1629 Kyiv Octoechos\Draft\1629_kyiv_octoechos_cohort6_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `Page_0051.jpg` through `Page_0060.jpg` in `Liturgical Monuments\Monument 8 - 1629 Kyiv Octoechos\Source Text\images`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p51 through p60).
3. Translate unabridged into `1629_kyiv_octoechos_cohort6_raw_draft.md` with inline footnote markers `[^N]`. When a new Tone or rear section begins on a leaf, emit its canonical H1 Markdown header on its own line: `# TONE 1`, `# TONE 2`, `# TONE 3`, `# TONE 4`, `# TONE 5`, `# TONE 6`, `# TONE 7`, `# TONE 8`, or `# EXAPOSTILARIA AND EVANGELICAL STICHERA`.
4. Write footnote definitions into `1629_kyiv_octoechos_cohort6_footnotes.txt` starting at `[^64]`.
5. Flush outputs to disk and advance through the autonomous pipeline.


---

## 4. Monument-Specific Codicological & Formatting Guardrails
**Codicological Notes**: p1 and p295 are 1-up outer leather binding boards; p2 through p294 are 2-up open spreads (Left Page = Verso of Folio N-1, Right Page = Recto of Folio N). p2 Right contains the Ruthenian ('prosta mova') preface 'ДО ЧИТЕЛНИКА'; p3 Left contains the full-page woodcut of St. John of Damascus ('К Д'); p3 Right opens Tone 1 ('ВЪ КНИГИ ОКТѠИХЪ ВСКРСНЪ, Гласъ Первый') below the Resurrection woodcut ('В Т'); p293 Right concludes with 'Конецъ Свѣтилнамъ и Троичнамъ'; p294 contains cursive marginalia and Stroev's collation slip (No. 39).

**Flash Execution Guardrails**:
- 2-UP SPREAD & CATCHWORD PROTOCOL: Leaves p2..p294 are 2-up open spreads. Inside each '=== LEAF pN ===' block, emit '**[Left Page — Fol. Nv]**' and '**[Right Page — Fol. Nr]**' in both Source Text and Draft MD. Record bottom-right catchwords as '[Кустод: ...]' in Source Text, complete any hyphenated cross-page word at the page where it begins in Draft MD, and never duplicate catchwords into the English hymn prose.
- H1 LANDMARK DISCIPLINE: Emit top-level H1 headers ('# PREFACE: TO THE READER', '# TONE 1'..'# TONE 8', '# EXAPOSTILARIA AND TRIADIKA') ONLY when a primary ornamental woodcut/vyaz section headpiece opens a new Tone or major book division. NEVER emit H1, H2, H3, or H4 for page running headers ('Гласъ А'..'Гласъ И'), offices, canons, odes, or rear per-tone Exapostilaria/Triadika subheadings ('Свѣтиленъ Гласъ З' -> use inline italic rubric '*Exapostilarion, Tone 7:*').
- COLOMETRIC ASTERISKS & DUAL REGISTER: Preserve literal '*' colometric dividers in Source Text while normalizing superscripts/titla into readable Cyrillic. In Draft MD, convert '*' dividers into natural English punctuation (commas, semicolons, colons) so pairs of '*' never corrupt Markdown italics. Render the p2 Ruthenian ('prosta mova') preface in elevated 17th-century prefatory prose with a linguistic footnote.
- SYMMETRIC PARATEXT & BINDING DESCRIPTIONS (SGC-02 PROTECTION): On binding boards (p1, p295), flyleaves/pastedowns (p2 Left, p294), and woodcut pages (p3 Left/Right), provide symmetric diplomatic descriptions in both Source Text (Russian/Slavonic brackets + verbatim label/marginalia transcription) and Draft MD (English brackets + full translation) so SGC-02 draft-to-source length ratios remain between 0.80 and 1.50.
