# Work Order: Lviv Stauropegion Paschal Pentecostarion (Lviv, 1907) — Cohort 12

**Document ID**: `1907_lviv_pentecostarion`  
**Cohort Number**: 12  
**Physical Leaves**: Physical pages 111 to 120 (`Page_0111.jpg` through `Page_0120.jpg`, 10 leaves total)  
**Starting Footnote Index**: `[^197]`  
**Governing Genre Register**: **HYMNOGRAPHIC** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 12 - 1907 Lviv Pentecostarion\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/`. Distinguish red cinnabar rubrics (render in italics `*...*`) from black text (render in standard Roman).
2. **Register Enforcement (Hymnographic)**: Concise, imperative, Active Present Indicative for rubrical movements.
3. **Canonical Realia & Loanwords**: `Tetrapod`, `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
4. **Father Paul Doxology & Anti-Slop Standard**: Banned phrase *"for ever and ever"* (use *"unto ages of ages"*). Strictly ban pseudo-archaic slop (`wherefore` -> use `therefore`; `wondrous` -> use `marvelous`; `verily` -> use `truly`; `hearken` -> use `give ear`; `resplendent`/`effulgent` -> use `radiant`; never use 3rd-person `-eth` verbs: `singeth`, `proclaimeth`, `censeth`, `entereth`, `maketh`, `readeth`, `beginneth`, `taketh`, `vesteth`, `boweth`, `kisseth`, `turneth`, `standeth`).
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
6. **Scripture & Psalter**: Septuagint (LXX) versification mandatory.
7. **Footnote Monotonic Bijectivity**: Every marker `[^N]` in body text MUST have an exact corresponding entry `[^N]:` in the footnotes file.
8. **Strict Epigraphic Markdown Discipline**: Never invent or interpolate modern liturgical office or structural headings (`### At Vespers`, `### At Matins`, `### Canon...`, `#### Ode...`). Liturgical rubrics, genre indicators, ode numbers, troparion labels, kathismata, and prosomoia must be rendered strictly as inline italicized text (e.g. `*Ode 1, Tone 2. Heirmos:*`, `*Troparion:*`, `*Sessional Hymn, Tone 2:*`). Markdown headings (`#` and authorized `##` service/day openings) are strictly restricted to decorative headpieces explicitly sanctioned in the publication spec and present on the physical page. Never emit `###` or `####` headings in hymnographic codices.
9. **Canonical 3-Layer Melodic Model (`Podoben`) Law**: Render all melodic model headings (`Подо́бенъ` / `Самогла́сенъ`) strictly using the canonical English incipit from `data/liturgical_primitives_registry.json` followed by the parenthetical Slavonic witness in inline italics: `*Tone N, Podoben: "<Canonical English Incipit>" (<Slavonic Witness>):*`. Never use transliterated-first or square-bracketed model headings.
10. **Structured Liturgical Stanzas & Dialogue Typography**: Format each Heirmos, Troparion, Theotokion, and Sticheron as a distinct stanza/paragraph preceded by its inline italicized role tag (`*Ode N. Heirmos:*`, `*Troparion:*`, `*Theotokion:*`). Format litany/Liturgy speaker labels in bold (`**Priest:**`, `**Deacon:**`, `**Reader:**`, `**Choir:**`) and ceremonial actions in active-present italics (`*...*`). Preserve literal colometric breathing-pause asterisks (`*`) in `Source Text/` and convert them into natural English punctuation (commas, semicolons, colons) in `Draft/`.
11. **Recensional Variants, Patristic Homilies & Gate-1-Safe Cross-References**: Translate the physical printed recension strictly as inked without silent harmonization to Nikonian or modern received editions; document significant pre-Nikonian, Ruthenian, or Greek-collated variants in `[^N]`. Render internal page/folio cross-references in body prose as `(see fol. N)[^M]` (never bare `[Page N]` or `[Leaf pN]` brackets, which fail Gate 1) and place the physical leaf coordinate in `[^M]:`.
12. **Front-Matter Paratext, Heraldic *Virshi*, *Prosta Mova* Prefaces & State Titulature**: Render Baroque heraldic coat-of-arms poetry (*вірші на герб*) in formal rhythmic unrhymed verse with heraldic notes; translate Early Modern Ruthenian (*prosta mova*) prefaces (*Премова* / *До Чителника*) in elevated 17th-century theological prose with marginal Scriptural/Patristic citations mapped to `[^N]`; translate Imperial, Papal, Archiepiscopal, and civic titulature with 100% diplomatic completeness; and provide symmetric diplomatic descriptions in both `Source Text/` and `Draft/` on binding/engraving/frontispiece leaves so `SGC-02` length ratios remain within `[0.80, 1.50]`.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 12 - 1907 Lviv Pentecostarion\Source Text\1907_lviv_pentecostarion_cohort12_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 12 - 1907 Lviv Pentecostarion\Draft\1907_lviv_pentecostarion_cohort12_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 12 - 1907 Lviv Pentecostarion\Draft\1907_lviv_pentecostarion_cohort12_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `Page_0111.jpg` through `Page_0120.jpg` in `Liturgical Monuments\Monument 12 - 1907 Lviv Pentecostarion\Source Text\images`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p111 through p120).
3. Translate unabridged into `1907_lviv_pentecostarion_cohort12_raw_draft.md` with inline footnote markers `[^N]`. Emit clear H1 Markdown headers (`# PART I: ...`, `# PART II: ...`, `# APPENDIX: ...`) at major structural divisions of the codex.
4. Write footnote definitions into `1907_lviv_pentecostarion_cohort12_footnotes.txt` starting at `[^197]`.
5. Flush outputs to disk and advance through the autonomous pipeline.


---

## 4. Monument-Specific Codicological & Formatting Guardrails
**Codicological Notes**: 1-up single-column printed liturgical folios (Physical Leaf = Printed Folio + 5 across p6..p671). p1..p5 are unnumbered front matter (p1 Preface to Readers 'ОТВѢТЪ КЪ ЧИТАТЕЛЕМЪ', p2 1907 Stauropegion Master Title Page, p3 Dormition Church & Korniakt Bell Tower plate, p4-p5 Pope Pius X, Emperor Franz Joseph I, Metropolitan Andrey Sheptytsky, and Bishops Chekhovych & Khomyshyn approbations); p669-p671 (fols. 333-335) contain the concluding Typikon rubrics for Paschaltide Menaion combinations, the 11 Matins Resurrection Gospel Pillars, and colophon 'Конецъ, и Бгу слава'.

**Flash Execution Guardrails**:
- 1-UP GEOMETRY & RUNNING PAGINATION: Every image Page_0001.jpg..Page_0671.jpg is a 1-up single folio leaf. Never emit 2-up '[Left Page]' or '[Right Page]' tags, and never emit standalone '[Page N]' or '[Leaf pN]' bracket lines in Draft MD (which fail Gate 1). Only use the required '=== LEAF pN ===' delimiter banner per physical leaf.
- H1 & H2 LANDMARK DISCIPLINE: Emit H1 ('# ...') at the major Paschaltide Part divisions defined in publication_spec ('# GREAT AND HOLY PASCHA AND BRIGHT WEEK', '# SUNDAY OF SAINT THOMAS', '# SUNDAY OF THE MYRRH-BEARING WOMEN', '# SUNDAY OF THE PARALYTIC AND MID-PENTECOST', '# SUNDAY OF THE SAMARITAN WOMAN', '# SUNDAY OF THE BLIND MAN AND FEAST OF THE ASCENSION', '# GREAT FEAST OF HOLY PENTECOST AND ALL SAINTS', '# TYPIKON APPENDIX: PASCHALTIDE MENAION COMBINATIONS AND GOSPEL PILLARS'). Render internal day/service openings and the 3 Pentecost Kneeling Prayer stations as H2 ('## ...'), and all sub-services, hours, canons, odes, heirmoi, troparia, and stichera as inline italic rubrics ('*...*'), never as '###' or '####'.
- 3-LAYER PODOBEN & STANZA DISCIPLINE: Format all melodic model headings strictly using the canonical 3-layer format: '*Tone N, Podoben: "<Canonical English Incipit>" (<Slavonic Witness>):*'. Format each Heirmos, Troparion, Theotokion, and Sticheron as a distinct stanza/paragraph preceded by its inline italic role tag ('*Ode N. Heirmos:*', '*Troparion:*', '*Theotokion:*').
- EPIGRAPHIC FIDELITY, PASCHAL HOMILY & STATE TITULATURE: Translate the 1907 Church Slavonic text (including the Paschal Catechetical Homily of St. John Chrysostom) strictly as printed, noting significant divergences from Greek/received editions in footnotes '[^N]'. Render all Austro-Hungarian imperial, parliamentary, and hierarchical titles on p4-p5 in full diplomatic English.
- GATE-1-SAFE CROSS-REFERENCES & SYMMETRIC PARATEXT (SGC-02 PROTECTION): Render internal folio cross-references in body prose as '(see fol. N)[^M]' without expanding unwritten incipits; place the physical leaf coordinate ('Physical Leaf pN = Printed Folio + 5') in '[^M]:'. On frontispiece/plate leaves (p2-p3), provide symmetric diplomatic descriptions in both Source Text and Draft MD so SGC-02 length ratios remain within [0.80, 1.50].
