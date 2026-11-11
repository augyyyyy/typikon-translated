# Anti-Potemkin Laws (`PE-HSG-01`..`05`) & 6-Gate Publication Verification (`Rule 21`)

## 1. Potemkin Epigraphy & Header-Span Goodhart Gaming (`PE-HSG-01`..`05`)
Nested under `GLOBAL_SYSTEM_RULES.md` §8 (`SGC-01`..`SGC-05`):

| Rule Code | Violation Vector | Enforcement Gate & Mandate |
| :--- | :--- | :--- |
| **`PE-HSG-01`** | **Synthetic Transcription & Hardcoded Prose Builders** | Python scripts must never embed hardcoded multiline liturgical prose, synthetic Slavonic/Greek reconstructions, or programmatic placeholder injections (`[INSERT DIAGRAM/TABLE HERE FROM ORIGINAL PDF]`, `(Translator's Note:...)`). All document templates must reside in external `.md` files under `data/templates/`. Enforced by `../scripts/verify_ecosystem_integrity.py` Gate 3 and `governance_gate.py` (`SGC-01A`). |
| **`PE-HSG-02`** | **Range-Interpolated Leaf Conservation** | Range-spanning headers (`## ... (pp. X-Y)` or `Regex #5` interpolation) are permanently prohibited from satisfying leaf conservation in `scripts/assemble_and_sync_hub.py` or `scripts/structural_audit.py`. Every physical leaf `pN` (`1..Total_Pages`) must possess an explicit individual `=== LEAF pN ===` boundary banner. |
| **`PE-HSG-03`** | **3-Tier `SGC-02` Ground-Truth & Primary-Source Bijection** | Every non-blank leaf block in `Source Text/`, `Draft/`, `Cohorts/`, and `Final/` must satisfy per-leaf character and word density thresholds (`>= 50` alphanumeric characters and `>= 10` words) and `Source Text/` ↔ `Cohorts/` word-ratio parity (`[0.35, 3.00]`), enforced by `scripts/structural_audit.py` and Gate 6 of `scripts/verify_publication_edition.py`. |
| **`PE-HSG-04`** | **Unverified Incipit Expansion** | Translators and scripts are prohibited from replacing printed incipits (`**"God is the Lord"**`, `**"Glory..."**`, *titlo* shorthand) with unverified external full-text maps or silent liturgical interpolations (`Rule 16`). |
| **`PE-HSG-05`** | **Apparatus & Summary Block Isolation** | Leaked `### Notes` headers, inline footnote definitions (`[^N]:`) inside body prose, and pre-written summary blocks or agent internal reasoning notes are prohibited inside canonical publication files and enforced by Gates 1 and 5 of `scripts/verify_publication_edition.py`. |

---

## 2. The 6-Gate Liturgical Canonical Publication Edition (LCPE) Verifier (`scripts/verify_publication_edition.py`)
Run during Phase 2 (`--compile-publication` and `--approve-grand-pause`):
```powershell
py scripts/verify_publication_edition.py --monument <ID>
```

| Gate | Name | Verification Checks |
| :-: | :--- | :--- |
| **Gate 1** | **Scaffolding & Cyrillic Leak Audit** | Zero raw `=== LEAF pN ===` banners in compiled `Final/` Parts; zero leaked `### Notes` headers; zero unparenthesized Cyrillic outside `(*...*)`; zero `[Page N]` / `[Leaf pN]` / `[Blank leaf]` brackets; zero placeholder tags. |
| **Gate 2** | **Heading Hierarchy & Markdown Discipline** | Enforces monument's `allowed_h1_patterns` from `publication_spec_scaffolds.json`; rejects forbidden `###` or `####` headings in hymnographic codices; verifies Part files are non-empty and properly ordered. |
| **Gate 3** | **Global Footnote Bijectivity** | Asserts 100% 1:1 bidirectional symmetry (`[^N]` in `Final/part*.md` ↔ `[^N]:` in `Final/Final_footnotes.txt`) with monotonic numbering `1..M`. |
| **Gate 4** | **MTS-1 Vocabulary, Slop & Pronoun Compliance** | Runs `../Shared_Lexicon/lint_vocabulary.py`, `scripts/lint_liturgical_slop.py` (Gate 1B), and `scripts/hieratic_pronoun_audit.py` across all compiled Part and footnote files. |
| **Gate 5** | **Apparatus Isolation & Quarantine Resolution** | Asserts `unresolved_quarantines == 0` in `Audit_Reports/argon_review_queue.json` and zero inline footnote definitions in body files. |
| **Gate 6** | **Closed Leaf Conservation & `SGC-02` 3-Tier Bijection** | Asserts $\bigcup_k \mathbf{Leaves}(C_k) \equiv \{1, \dots, N\}$ across `Source Text/` and `Cohorts/`, non-blank leaf density (`>= 50` chars, `>= 10` words), and word-ratio parity (`[0.35, 3.00]`). |

---

## 3. Shared Atomic Liturgical Corpus Integration (`GLOBAL_SYSTEM_RULES.md` §7)
When referencing fixed liturgical prayers or psalmody in `../Shared_Lexicon/Atomic_Liturgical_Corpus/`, scripts and validators must consume the canonical 4-shard files (`01_horologion_and_fixed_prayers.json`, `02_octoechos_and_menaion_propers.json`, `03_triodion_and_pentecostarion.json`, `04_euchologion_and_sacraments.json`) strictly **read-only** and never write to `Shared_Lexicon/Atomic_Liturgical_Corpus/`.
