# Work Order: Tolkovy Typikon of Mikhail Skaballanovich (Kyiv, 1910–1915) — Cohort 92

**Document ID**: `1910_skaballanovich_typikon`  
**Cohort Number**: 92  
**Physical Leaves**: Physical pages 911 to 920 (`p911.png` through `p920.png`, 10 leaves total)  
**Starting Footnote Index**: `[^2759]` (Notes 925–941 of Volume II, mapping to global indices `[^2759]` through `[^2775]`, 17 footnotes total)  
**Governing Genre Register**: **SCHOLARLY_CRITICAL** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/` and electronic concordance in `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf`.
2. **Register Enforcement (Scholarly_critical)**: Rigorous academic, liturgical commentary translation. Active Present Indicative for rubrical movements.
3. **Cohort 92 Content Roadmap**:
   - `p911`–`p915`: THE ALLELUIA & ALLELUIARION OF THE DIVINE LITURGY (*АЛЛИЛУИА И АЛЛИЛУИАРИИ НА ЛИТУРГИИ*):
     - `p911`: Tone 5 Alleluiarion: The hopeful character of Tone 5 (musical and theological parallel to Tone 1; "Because Thou, Lord, art my refuge"); Eight Tones system. Notes 925, 926 -> `[^2759]`, `[^2760]`.
     - `p912`: History of the Liturgical Alleluia (*Orig. p. 754*): Transition from responsorial psalmody to independent jubilus / chant with verses. Note 927 -> `[^2761]`.
     - `p913`: Western Parallels and the Neumatic Jubilus (*Orig. p. 755*): The Roman Alleluia and its melodic jubilatio / melismatic extension; vivacity and solemn energy. Notes 928–930 -> `[^2762]`–`[^2764]`.
     - `p914`: Comparative Liturgics of the Alleluia (*Orig. p. 756*): Chanting Alleluia 3-fold in Coptic, Mozarabic, and Nestorian Liturgies; priest pronouncing Alleluia after Psalm 33 verses. Notes 931–935 -> `[^2765]`–`[^2769]`.
     - `p915`: The Sunday Resurrection Alleluiaria of the Octoechos (*Orig. p. 757*): In contrast to the variable prokeimena, the Sunday Alleluiaria are strictly tied to the Tone. Note 936 -> `[^2770]`.
   - `p916`–`p918`: THE SCRIPTURAL READINGS (EPISTLE & GOSPEL) (*ЧТЕНИЕ АПОСТОЛА И ЕВАНГЕЛИЯ*):
     - `p916`: The Epistle (*Apostol*): Reading from the Pauline Epistles or Catholic Epistles; liturgical preparation and censing during Alleluia. Note 937 -> `[^2771]`.
     - `p917`: Dialogue and Blessing (*Orig. p. 758*, *759*): Priest imparting peace to the reader: "Peace to thee that announcest good tidings"; deacon proclaiming the Gospel pericope. Notes 938–940 -> `[^2772]`–`[^2774]`.
     - `p918`: Ancient Formulae of Reading (*Orig. p. 760*): Western "Fratres" for Pauline Epistles and "In illo tempore" for Gospels. Note 941 -> `[^2775]`.
   - `p919`–`p920`: THE SYSTEMATIC CYCLE OF THE 32 SUNDAY READINGS:
     - `p919`: Systematic distribution of Sunday Epistles and Gospels throughout the ecclesiastical year (*Orig. p. 761*): 10th to 20th Sunday after Pentecost; Gospel of the demoniac (Matt. 17:14–23). (0 footnotes on p919).
     - `p920`: 21st to 32nd Sunday after Pentecost (*Orig. p. 762*): Epistle to Timothy (1 Tim. 4:9–15); Zacchaeus Sunday (Luke 19:1–10). (0 footnotes on p920).
4. **Footnote Monotonic Bijectivity**:
   - Every marker `[925]` through `[941]` in the body text must be mapped to `[^2759]` through `[^2775]`.
   - Corresponding definitions are located on leaves `p1015`–`p1016` of `1910-1915-Skaballanovich-Tolkovy-Typikon-Complete.pdf` (and cached in `scratch/cohort91_96_endnotes_raw.txt`).
   - Write exact matching footnote definitions `[^2759]: ...` through `[^2775]: ...` in `1910_skaballanovich_typikon_cohort92_footnotes.txt`.
5. **Canonical Realia & Loanwords**: `Alleluia`, `Alleluiarion`, `Jubilus`, `Epistle`, `Apostol`, `Gospel`, `Evangelion`, `In illo tempore`, `Zacchaeus Sunday`.
6. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
7. **Anti-Slop Enforcement**: Strictly ban pseudo-archaic slop (*"wherefore"*, *"verily"*, *"betwixt"*, *"methinks"*, *"twas"*; zero shall-bombing; use "wonderful in the saints" for *дивен во святых*).
8. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\1910_skaballanovich_typikon_cohort92_source.txt`
- **Draft Markdown Translation**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort92_raw_draft.md`
- **Cohort Footnotes File**: `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Draft\1910_skaballanovich_typikon_cohort92_footnotes.txt`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p911.png` through `p920.png` in `Liturgical Monuments\Monument 6 - 1910 Skaballanovich Typikon\Source Text\images` and PDF.
2. Transcribe Russian source text leaf-by-leaf with headers `=== LEAF p{N} ===` (for each leaf p911 through p920).
3. Translate and critically audit into MTS-1 compliant scholarly critical text in `1910_skaballanovich_typikon_cohort92_raw_draft.md` with footnote markers `[^2759]` through `[^2775]`.
4. Extract and translate footnote definitions 925 through 941 from leaves `p1015`–`p1016` into `1910_skaballanovich_typikon_cohort92_footnotes.txt` as `[^2759]: ...` through `[^2775]: ...`.
5. Run the Small Pause Gatekeeper suite before finishing:
   `py scripts/run_small_pause_gate.py --draft "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort92_raw_draft.md" --footnotes "Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Draft/1910_skaballanovich_typikon_cohort92_footnotes.txt" --cohort 92`
