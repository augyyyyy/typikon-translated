# Work Order: Lviv Flowery Triodion (Pentecostarion) (Mykhailo Slozka, Lviv, 1642) — Cohort 8

**Document ID**: `1642_lviv_slozka_pentecostarion`  
**Cohort Number**: 8  
**Physical Leaves**: Physical pages 71 to 80 (`Page_0071.jpg` through `Page_0080.jpg`, 10 leaves total)  
**Starting Footnote Index**: `[^265]`  
**Governing Genre Register**: **HYMNOGRAPHIC** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 14 - 1642 Lviv Slozka Pentecostarion\Source Text\images`  

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
- **Source Text Transcription**: `Liturgical Monuments\Monument 14 - 1642 Lviv Slozka Pentecostarion\Source Text\1642_lviv_slozka_pentecostarion_cohort8_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 14 - 1642 Lviv Slozka Pentecostarion\Draft\1642_lviv_slozka_pentecostarion_cohort8_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 14 - 1642 Lviv Slozka Pentecostarion\Draft\1642_lviv_slozka_pentecostarion_cohort8_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `Page_0071.jpg` through `Page_0080.jpg` in `Liturgical Monuments\Monument 14 - 1642 Lviv Slozka Pentecostarion\Source Text\images`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p71 through p80).
3. Translate unabridged into `1642_lviv_slozka_pentecostarion_cohort8_raw_draft.md` with inline footnote markers `[^N]`. Emit clear H1 Markdown headers (`# PART I: ...`, `# PART II: ...`, `# APPENDIX: ...`) at major structural divisions of the codex.
4. Write footnote definitions into `1642_lviv_slozka_pentecostarion_cohort8_footnotes.txt` starting at `[^265]`.
5. Flush outputs to disk and advance through the autonomous pipeline.


---

## 4. Monument-Specific Codicological & Formatting Guardrails
**Codicological Notes**: 1-up single-column printed folios (441 physical leaves). p1 is blind-tooled leather binding over wooden boards with brass clasps; p2-p4 are front flyleaves with museum shelfmark 'МКДУ КН-6201 СП-26'; p5 is Folio 1 (а҃) opening with ornate woodcut headpiece and Lazarus Saturday Vespers ('Душеполезную совершивше Четыредесятницу...'); p439-p441 are rear endpapers/flyleaves.

**Flash Execution Guardrails**:
- 1-UP GEOMETRY & RUNNING PAGINATION: Every image Page_0001.jpg..Page_0441.jpg is a 1-up single folio leaf. Never emit 2-up '[Left Page]' or '[Right Page]' tags, and never emit standalone '[Page N]' or '[Leaf pN]' bracket lines in Draft MD (which fail Gate 1). Only use the required '=== LEAF pN ===' delimiter banner per physical leaf.
- H1 & H2 LANDMARK DISCIPLINE: Preserve the historic 1642 Ruthenian Flowery Triodion arrangement opening on Lazarus Saturday (p5 / fol. 1). Emit H1 ('# ...') at the 5 Part divisions defined in publication_spec ('# LAZARUS SATURDAY AND PALM WEEK', '# GREAT AND HOLY PASCHA AND BRIGHT WEEK', '# SUNDAYS AND WEEKS OF PASCHALTIDE', '# FEAST OF THE ASCENSION AND HOLY FATHERS', '# GREAT FEAST OF HOLY PENTECOST AND ALL SAINTS'). Render internal day/service openings as H2 ('## ...'), and all sub-services, canons, odes, heirmoi, troparia, and stichera as inline italic rubrics ('*...*'), never as '###' or '####'.
- 3-LAYER PODOBEN & STANZA DISCIPLINE: Format all melodic model headings strictly using the canonical 3-layer format: '*Tone N, Podoben: "<Canonical English Incipit>" (<Slavonic Witness>):*' (never square-bracketed). Format each Heirmos, Troparion, Theotokion, and Sticheron as a distinct poetic stanza/paragraph preceded by its inline italic role tag ('*Ode N. Heirmos:*', '*Troparion:*', '*Theotokion:*').
- 1642 KYIVAN-GALICIAN RECENSION FIDELITY: Translate the physical 1642 Slozka print strictly as inked without silent harmonization to later Nikonian/Synodal texts, adding concise footnotes '[^N]' where the 1642 Ruthenian text diverges substantially from the standard Byzantine/Synodal textus receptus.
- GATE-1-SAFE CROSS-REFERENCES & SYMMETRIC PARATEXT (SGC-02 PROTECTION): Render internal folio cross-references in body prose as '(see fol. N)[^M]'; place the physical leaf coordinate in '[^M]:'. On binding/flyleaf pages (p1-p4 and p439-p441), provide symmetric diplomatic descriptions in both Source Text and Draft MD so SGC-02 length ratios remain within [0.80, 1.50].
