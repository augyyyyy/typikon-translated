# Work Order: Kyiv-Pechersk Lenten Triodion (Petro Mohyla, Kyiv, 1640) — Cohort 81

**Document ID**: `1640_kyiv_triodion`  
**Cohort Number**: 81  
**Physical Leaves**: Physical pages 801 to 810 (`Page_0801.jpg` through `Page_0810.jpg`, 10 leaves total)  
**Starting Footnote Index**: `[^2664]`  
**Governing Genre Register**: **HYMNOGRAPHIC** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 15 - 1640 Kyiv Lenten Triodion\Source Text\images`  

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
11. **Diachronic Drift Invariance & Recensional Fidelity**: Identical original-language terms, rubrical formulas, and hymnographic phrases MUST be translated identically using the canonical shared lexicon so zero artificial translator drift is introduced across monuments. Conversely, when the physical printed recension genuinely differs in wording, syntax, or rubrical prescription from other editions, translate the actual printed text strictly as inked without silent harmonization, and document significant pre-Nikonian, Ruthenian, or Greek-collated variants in `[^N]`. Render internal page/folio cross-references in body prose as `(see fol. N)[^M]` (never bare `[Page N]` or `[Leaf pN]` brackets, which fail Gate 1) and place the physical leaf coordinate in `[^M]:`.
12. **Front-Matter Paratext, Heraldic *Virshi*, *Prosta Mova* Prefaces & State Titulature**: Render Baroque heraldic coat-of-arms poetry (*вірші на герб*) in formal rhythmic unrhymed verse with heraldic notes; translate Early Modern Ruthenian (*prosta mova*) prefaces (*Премова* / *До Чителника*) in elevated 17th-century theological prose with marginal Scriptural/Patristic citations mapped to `[^N]`; translate Imperial, Papal, Archiepiscopal, and civic titulature with 100% diplomatic completeness; and provide symmetric diplomatic descriptions in both `Source Text/` and `Draft/` on binding/engraving/frontispiece leaves so `SGC-02` length ratios remain within `[0.80, 1.50]`.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 15 - 1640 Kyiv Lenten Triodion\Source Text\1640_kyiv_triodion_cohort81_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 15 - 1640 Kyiv Lenten Triodion\Draft\1640_kyiv_triodion_cohort81_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 15 - 1640 Kyiv Lenten Triodion\Draft\1640_kyiv_triodion_cohort81_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `Page_0801.jpg` through `Page_0810.jpg` in `Liturgical Monuments\Monument 15 - 1640 Kyiv Lenten Triodion\Source Text\images`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p801 through p810).
3. Translate unabridged into `1640_kyiv_triodion_cohort81_raw_draft.md` with inline footnote markers `[^N]`. Emit clear H1 Markdown headers (`# PART I: ...`, `# PART II: ...`, `# APPENDIX: ...`) at major structural divisions of the codex.
4. Write footnote definitions into `1640_kyiv_triodion_cohort81_footnotes.txt` starting at `[^2664]`.
5. Flush outputs to disk and advance through the autonomous pipeline.


---

## 4. Monument-Specific Codicological & Formatting Guardrails
**Codicological Notes**: 1-up single-column printed folios (896 physical leaves). p1 is ornate architectural Lavra title page ('ТРИѠДІѠНЪ сирѣчь ТРІПѢСНЕЦЪ... Ѡ Еллинскагѡ изслѣдованъ', AM 7148 / AD 1640); p2 is coat of arms and Baroque heraldic verse panegyric to Teodor Proskura-Sushchansky; p3 is Metropolitan Petro Mohyla's Dedicatory Epistle; p4-p5+ contain the Theological Foreword ('Премова'); p870-p896 contain the unabridged hagiographical 'Life of St. Mary of Egypt' by St. Sophronius of Jerusalem concluding on p896 (f. 284v) with 'АМИНЬ'.

**Flash Execution Guardrails**:
- 1-UP GEOMETRY & RUNNING PAGINATION: Every image Page_0001.jpg..Page_0896.jpg is a 1-up single folio leaf. Never emit 2-up '[Left Page]' or '[Right Page]' tags, and never emit standalone '[Page N]' or '[Leaf pN]' bracket lines in Draft MD (which fail Gate 1). Only use the required '=== LEAF pN ===' delimiter banner per physical leaf.
- H1 & H2 LANDMARK DISCIPLINE: Emit H1 ('# ...') at the 5 major Part divisions defined in publication_spec ('# PRE-LENTEN PERIOD', '# THE HOLY AND GREAT FORTY DAYS', '# LAZARUS SATURDAY AND PALM SUNDAY', '# GREAT AND HOLY PASSION WEEK', '# THE LIFE OF OUR VENERABLE MOTHER MARY OF EGYPT'). Render internal day/service openings and narrative sections of the Life of St. Mary as H2 ('## ...'), and all sub-services, hours, canons, odes, heirmoi, troparia, and stichera as inline italic rubrics ('*...*'), never as '###' or '####'.
- BAROQUE HERALDIC VIRSHI & MOHYLA RUTHENIAN PREFACE: Render the p2 Proskura-Sushchansky heraldic coat-of-arms verse in formal rhythmic unrhymed verse with heraldic notes. Translate Petro Mohyla's Early Modern Ruthenian dedicatory epistle and Theological Foreword ('Премова', p3-p10+) in an elevated 17th-century theological prose register, mapping all marginal Scriptural and Patristic citations to footnotes '[^N]'.
- 3-LAYER PODOBEN & PRE-NIKONIAN KYIVAN FIDELITY ('Ѡ Еллинскагѡ изслѣдованъ'): Format all melodic model headings strictly as '*Tone N, Podoben: "<Canonical English Incipit>" (<Slavonic Witness>):*'. Translate the 1640 Greek-collated Kyivan text strictly as printed without silent harmonization to later Synodal editions, documenting significant pre-Nikonian Kyivan readings in footnotes '[^N]'.
- GATE-1-SAFE CROSS-REFERENCES & SYMMETRIC PARATEXT (SGC-02 PROTECTION): Render internal folio cross-references in body prose as '(see fol. N)[^M]'; place the physical leaf coordinate in '[^M]:'. On woodcut/heraldic frontispiece leaves (p1-p2), provide symmetric diplomatic descriptions in both Source Text and Draft MD so SGC-02 length ratios remain within [0.80, 1.50].
