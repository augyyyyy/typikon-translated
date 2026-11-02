# Work Order: 1616–1617 Kyiv-Pechersk Lavra Horologion of Zacharias Kopystensky (Часослов, Київ: Друкарня Києво-Печерської Лаври, 1616/1617) — Cohort 21

**Document ID**: `1617_kyiv_kopystensky_horologion`  
**Cohort Number**: 21  
**Physical Leaves**: Physical pages 201 to 210 (`Page_0201.jpg` through `Page_0210.jpg`, 10 leaves total)  
**Starting Footnote Index**: `[^514]`  
**Governing Genre Register**: **RUBRICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument - 1617_kyiv_kopystensky_horologion\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/`. Distinguish red cinnabar rubrics (render in italics `*...*`) from black text (render in standard Roman).
2. **Register Enforcement (Rubrical)**: Concise, imperative, Active Present Indicative for rubrical movements.
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
- **Source Text Transcription**: `Liturgical Monuments\Monument - 1617_kyiv_kopystensky_horologion\Source Text\1617_kyiv_kopystensky_horologion_cohort21_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument - 1617_kyiv_kopystensky_horologion\Draft\1617_kyiv_kopystensky_horologion_cohort21_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument - 1617_kyiv_kopystensky_horologion\Draft\1617_kyiv_kopystensky_horologion_cohort21_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `Page_0201.jpg` through `Page_0210.jpg` in `Liturgical Monuments\Monument - 1617_kyiv_kopystensky_horologion\Source Text\images`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p201 through p210).
3. Translate unabridged into `1617_kyiv_kopystensky_horologion_cohort21_raw_draft.md` with inline footnote markers `[^N]`. Emit H1 (`# ...`) at the primary printed book divisions of the Horologion/Chasoslov: `# PREFACE`, `# THE MIDNIGHT OFFICE AND MATINS`, `# THE ORDER OF THE HOURS AND TYPIKA` (or `# THE ORDER OF VESPERS AND COMPLINE`), `# TROPARIA AND KONTAKIA OF THE MENOLOGION`, `# KANONIKON AND SUPPLICATORY CANONS`, `# SELECTED PSALMS FOR FEASTS`, and `# THE PASCHALION AND CALENDAR TABLES`.
4. Write footnote definitions into `1617_kyiv_kopystensky_horologion_cohort21_footnotes.txt` starting at `[^514]`.
5. **Incremental 2–3 Leaf Disk Flush Protocol**: Flush transcribed and translated leaves to disk incrementally every **2 to 3 physical leaves** (`write_file` on the first 2–3 leaves, then `write_file(Append=True)` or `edit_file` for each subsequent 2–3 leaf batch) so output turn limits never truncate the final leaves of long Patristic homilies or Synaxaria.
6. **Do NOT invoke `run_small_pause_gate.py` manually**: Once all three files (`Source Text`, `Draft MD`, `Footnotes`) are written with every `=== LEAF pN ===` boundary present, finish your turn immediately so the parent orchestrator (`autonomous_orchestrator.py --verify-cohort`) can run deterministic self-healing prior to gate verification.


---

## 4. Monument-Type (`horologion`) & Codicological Guardrails
**Execution Guardrails**:
- Never expand abbreviated Slavonic prayer cues (*Тр̃е*, *Ѻ̃че нашъ*, *Г̃и помилуй*) beyond their canonical English equivalent ('*Trisagion*', '*Our Father*', '*Lord, have mercy*') (Rule 16).
- Emit H1 (`# ...`) at primary Horologion section boundaries (`# THE ORDER OF THE TYPIKA...`, `# TROPARIA AND KONTAKIA...`, `# SELECTED PSALMS...`, `# THE PASCHALION...`) so the Menologion, Selected Psalms, and Paschalion slice into distinct modular Parts.
- Always parenthesize Cyrillic table letters and Slavonic incipits `(*...*)`, never square brackets `[...]`.


---

## 5. Preceding Cohort Continuity Context (Cohort 20 -> Cohort 21)
- **Previous Cohort**: Cohort 20 (ended on physical leaf `p200`)
- **Last Attested Folio/Page Reference**: `Fol. 177r` (verify sequential foliation/quire continuity on your first leaf; flag any physical jump in a footnote)
- **Active Section Heading**: `# TROPARIA AND KONTAKIA: RESURRECTIONAL TROPARIA, THEOTOKIA, AND HYPAKOAI OF THE EIGHT TONES[^506]`
- **Trailing 3 Lines of Previous Cohort**:
  > Having learned the radiant proclamation of the Resurrection from the Angel, and cast off the ancestral condemnation, the women disciples of the Lord exultantly 
  > *Theotokion:*
  > The mystery hidden from all ages and unknown to Angels was revealed through thee, O Theotokos, unto them that are upon the earth: God becoming incarnate in unco
