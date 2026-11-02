# Work Order: 1716 Kyiv-Pechersk Lavra Theotokarion / Eight-Tone Marian Canons (Богородичник / Канони Богородиці Осмогласні, Київ: Друкарня Лаври, 1716) — Cohort 20

**Document ID**: `1716_kyiv_marian_canons_octoechos`  
**Cohort Number**: 20  
**Physical Leaves**: Physical pages 191 to 200 (`Page_0191.jpg` through `Page_0200.jpg`, 10 leaves total)  
**Starting Footnote Index**: `[^246]`  
**Governing Genre Register**: **HYMNOGRAPHIC** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument - 1716_kyiv_marian_canons_octoechos\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/`. Distinguish red cinnabar rubrics (render in italics `*...*`) from black text (render in standard Roman).
2. **Register Enforcement (Hymnographic)**: Concise, imperative, Active Present Indicative for rubrical movements.
3. **Canonical Realia & Loanwords**: `Tetrapod`, `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
4. **Father Paul Doxology & Anti-Slop Standard**: Banned phrase *"for ever and ever"* (use *"unto ages of ages"*). Strictly ban pseudo-archaic slop (`wherefore` -> use `therefore`; `wondrous` -> use `marvelous`; `verily` -> use `truly`; `hearken` -> use `give ear`; `resplendent`/`effulgent` -> use `radiant`; never use 3rd-person `-eth` verbs: `singeth`, `proclaimeth`, `censeth`, `entereth`, `maketh`, `readeth`, `beginneth`, `taketh`, `vesteth`, `boweth`, `kisseth`, `turneth`, `standeth`, `cometh`, `sayeth`, `giveth`, `believeth`, `forgiveth`, `partaketh`, `rebuketh`).
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*). Keep human/Marian/adversary pronouns lowercase (*thee/thy/thou* when addressing the *Birthgiver of God / Mother of God / Theotokos*, and *him/his* for clergy, saints, or the *serpent/enemy*).
6. **Scripture & Psalter**: Septuagint (LXX) versification mandatory.
7. **Footnote Monotonic Bijectivity**: Every marker `[^N]` in body text MUST have an exact corresponding entry `[^N]:` in the footnotes file. Never attach `[^N]` directly to a `**[Left/Right Page — Fol. Xr]**` 2-up spread milestone or `=== LEAF pN ===` banner; always attach `[^N]` to a surviving heading or content line.
8. **Strict Epigraphic Markdown Discipline**: Never invent or interpolate modern liturgical office or structural headings (`### At Vespers`, `### At Matins`, `### Canon...`, `#### Ode...`). Liturgical rubrics, genre indicators, ode numbers, troparion labels, kathismata, and prosomoia must be rendered strictly as inline italicized text (e.g. `*Ode 1, Tone 2. Heirmos:*`, `*Troparion:*`, `*Sessional Hymn, Tone 2:*`). Markdown headings (`#` and authorized `##` service/day openings) are strictly restricted to decorative headpieces explicitly sanctioned in the publication spec and present on the physical page. Never emit `###` or `####` headings in hymnographic codices.
9. **Canonical 3-Layer Melodic Model (`Podoben`) Law**: Render all melodic model headings (`Подо́бенъ` / `Самогла́сенъ`) strictly using the canonical English incipit from `data/liturgical_primitives_registry.json` followed by the parenthetical Slavonic witness in inline italics: `*Tone N, Podoben: "<Canonical English Incipit>" (<Slavonic Witness>):*`. Never use transliterated-first or square-bracketed model headings.
10. **Structured Liturgical Stanzas & Dialogue Typography**: Format each Heirmos, Troparion, Theotokion, and Sticheron as a distinct stanza/paragraph preceded by its inline italicized role tag (`*Ode N. Heirmos:*`, `*Troparion:*`, `*Theotokion:*`). Format litany/Liturgy speaker labels in bold (`**Priest:**`, `**Deacon:**`, `**Reader:**`, `**Choir:**`) and ceremonial actions in active-present italics (`*...*`). Preserve literal colometric breathing-pause asterisks (`*`) in `Source Text/` and convert them into natural English punctuation (commas, semicolons, colons) in `Draft/`.
11. **Diachronic Drift Invariance & Recensional Fidelity**: Identical original-language terms, rubrical formulas, and hymnographic phrases MUST be translated identically using the canonical shared lexicon so zero artificial translator drift is introduced across monuments. Conversely, when the physical printed recension genuinely differs in wording, syntax, or rubrical prescription from other editions, translate the actual printed text strictly as inked without silent harmonization, and document significant pre-Nikonian, Ruthenian, or Greek-collated variants in `[^N]`. Render internal page/folio cross-references in body prose as `(see fol. N)[^M]` (never bare `[Page N]` or `[Leaf pN]` brackets, which fail Gate 1) and place the physical leaf coordinate in `[^M]:`.
12. **Front-Matter Paratext, Heraldic *Virshi*, *Prosta Mova* Prefaces, Vacat Folios & Parenthetical Cyrillic**: Render Baroque heraldic coat-of-arms poetry (*вірші на герб*) in formal rhythmic unrhymed verse with heraldic notes; translate Early Modern Ruthenian (*prosta mova*) prefaces (*Премова* / *До Чителника*) in elevated 17th-century theological prose with marginal Scriptural/Patristic citations mapped to `[^N]`; translate Imperial, Papal, Archiepiscopal, and civic titulature with 100% diplomatic completeness; and provide symmetric diplomatic descriptions in both `Source Text/` and `Draft/` on binding/engraving/frontispiece leaves so `SGC-02` length ratios remain within `[0.80, 1.50]`. Represent blank folios and flyleaves strictly as `*(Vacat — Fol. Xv: Unnumbered blank verso)*` or `*(Flyleaf — Archival binding sheet)*` (never square-bracketed `[Blank leaf...]`). Render all inline Slavonic/Cyrillic script witnesses or table numerals in **parentheses** `(*Слава...*)`, **never in square brackets** `[Слава...]`.
13. **Patristic Hagiography & Synaxarion Prose Diction**: When translating narrative *Synaxaria*, Patristic Homilies (Chrysostom, Basil, Gregory the Theologian, John Damascene, Theodore the Studite), or Martyrological Passions embedded inside liturgical codices, maintain elevated classical patristic English prose. Strictly forbid pseudo-archaic AI vocabulary (`peradventure`, `verily`, `betwixt`, `twas`, `methinks`, `hearken`, `wherefore`, `forsooth`, `haply`, `albeit`) and `-eth` 3rd-person singular verbs across both body text and footnotes.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument - 1716_kyiv_marian_canons_octoechos\Source Text\1716_kyiv_marian_canons_octoechos_cohort20_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument - 1716_kyiv_marian_canons_octoechos\Draft\1716_kyiv_marian_canons_octoechos_cohort20_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument - 1716_kyiv_marian_canons_octoechos\Draft\1716_kyiv_marian_canons_octoechos_cohort20_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `Page_0191.jpg` through `Page_0200.jpg` in `Liturgical Monuments\Monument - 1716_kyiv_marian_canons_octoechos\Source Text\images`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p191 through p200).
3. Translate unabridged into `1716_kyiv_marian_canons_octoechos_cohort20_raw_draft.md` with inline footnote markers `[^N]`. When a new Tone or major rear section begins on a leaf, emit its canonical H1 Markdown header on its own line: `# TONE 1`, `# TONE 2`, `# TONE 3`, `# TONE 4`, `# TONE 5`, `# TONE 6`, `# TONE 7`, `# TONE 8`, `# WEEKDAY OCTOECHOS` (when weekday offices are consolidated after Tone 8), `# EXAPOSTILARIA AND EVANGELICAL STICHERA`, `# ASCETIC HOMILIES AND COLOPHON`, or `# GENERAL PARASTAS (OFFICE FOR THE DEPARTED)`.
4. Write footnote definitions into `1716_kyiv_marian_canons_octoechos_cohort20_footnotes.txt` starting at `[^246]`.
5. **Incremental 2–3 Leaf Disk Flush Protocol**: Flush transcribed and translated leaves to disk incrementally every **2 to 3 physical leaves** (`write_file` on the first 2–3 leaves, then `write_file(Append=True)` or `edit_file` for each subsequent 2–3 leaf batch) so output turn limits never truncate the final leaves of long Patristic homilies or Synaxaria.
6. **Do NOT invoke `run_small_pause_gate.py` manually**: Once all three files (`Source Text`, `Draft MD`, `Footnotes`) are written with every `=== LEAF pN ===` boundary present, finish your turn immediately so the parent orchestrator (`autonomous_orchestrator.py --verify-cohort`) can run deterministic self-healing prior to gate verification.


---

## 4. Monument-Type (`octoechos`) & Codicological Guardrails
**Execution Guardrails**:
- Enforce the 3-Layer Melodic Model (Podoben) Standard: *Tone N, Podoben: "<Canonical English Incipit>" (<Slavonic Witness>):*.
- Format every Ode, Heirmos, Troparion, and Theotokion as an inline italic role tag (*Ode N. Heirmos:*, *Troparion:*, *Theotokion:*), never as ### or #### headings.
- When consolidated Weekday Offices follow Tone 8, emit `# WEEKDAY OCTOECHOS` at their opening leaf.


---

## 5. Preceding Cohort Continuity Context (Cohort 19 -> Cohort 20)
- **Previous Cohort**: Cohort 19 (ended on physical leaf `p190`)
- **Last Attested Folio/Page Reference**: `Fol. 180r` (verify sequential foliation/quire continuity on your first leaf; flag any physical jump in a footnote)
- **Trailing 3 Lines of Previous Cohort**:
  > Surrender me not unto enemies, O Pure One, who greatly seek my ruin because of my sins: but by thy tender mercy snatch me from their harm. Glory:
  > *Troparion:*
  > Knowing Thee, O Christ, to be the God of all and the Creator of all: upon Thee alone have we placed the hope of our salvation,
