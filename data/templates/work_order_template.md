# Work Order: {title} — Cohort {cohort_num}

**Document ID**: `{monument_id}`  
**Cohort Number**: {cohort_num}  
**Physical Leaves**: Physical pages {start_page} to {end_page} (`Page_{start_page:04d}.jpg` through `Page_{end_page:04d}.jpg`, {leaf_count} leaves total)  
**Starting Footnote Index**: `[^{starting_footnote}]`  
**Governing Genre Register**: **{genre_register_upper}** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `{images_rel}`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/`. Distinguish red cinnabar rubrics (render in italics `*...*`) from black text (render in standard Roman).
2. **Register Enforcement ({genre_register_cap})**: Concise, imperative, Active Present Indicative for rubrical movements.
3. **Canonical Realia & Loanwords**: `Tetrapod`, `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
4. **Father Paul Doxology & Anti-Slop Standard**: Banned phrase *"for ever and ever"* (use *"unto ages of ages"*). Strictly ban pseudo-archaic slop (`wherefore` -> use `therefore`; `wondrous` -> use `marvelous`; `verily` -> use `truly`; `hearken` -> use `give ear`; `resplendent`/`effulgent` -> use `radiant`; never use 3rd-person `-eth` verbs: `singeth`, `proclaimeth`, `censeth`, `entereth`, `maketh`, `readeth`, `beginneth`, `taketh`, `vesteth`, `boweth`, `kisseth`, `turneth`, `standeth`).
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
6. **Scripture & Psalter**: Septuagint (LXX) versification mandatory.
7. **Footnote Monotonic Bijectivity**: Every marker `[^N]` in body text MUST have an exact corresponding entry `[^N]:` in the footnotes file.
8. **Strict Epigraphic Markdown Discipline**: Never invent or interpolate modern liturgical office or structural headings (`## At Sunday Midnight Office`, `## At Sunday Matins`, `### Canon...`, `#### Ode...`). Liturgical rubrics, genre indicators, ode numbers, troparion labels, kathismata, and prosomoia must be rendered strictly as inline italicized text (e.g. `*Ode 1, Tone 2. Heirmos:*`, `*Troparion:*`, `*Sessional Hymn, Tone 2:*`). Markdown headings (`#`) are strictly restricted to primary decorative woodcut headpieces (e.g. `# TONE 1`, `# TONE 2`, `# PREFACE: TO THE READER`) explicitly sanctioned in the publication spec and present on the physical page. Any other markdown header (`#`, `##`, `###`, `####`) will trigger an immediate Small Pause Gate failure.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `{source_rel}`
- **Draft Markdown Translation**: `{draft_rel}`
- **Cohort Footnotes File**: `{footnotes_rel}`

---

## 3. Autonomous Execution Instructions
1. Inspect images `Page_{start_page:04d}.jpg` through `Page_{end_page:04d}.jpg` in `{images_rel}`.
2. {transcription_inst}
3. {translation_inst}
4. Write footnote definitions into `{footnotes_name}` starting at `[^{starting_footnote}]`.
5. Flush outputs to disk and advance through the autonomous pipeline.
