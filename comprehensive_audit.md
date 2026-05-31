# Comprehensive Translation & Compliance Audit
## Dolnytsky Typikon — Scientific Edition
**Last Updated:** May 31, 2026

---

> [!NOTE]
> For the complete, authoritative technical state of the project, including terminology decisions, pipeline history, and full asset inventory, please see [`_brain/PROJECT_BRAIN_PRINT.md`](_brain/PROJECT_BRAIN_PRINT.md).

## 1. Audit Layer Status Summary

A series of strict compliance and structural audits have been performed to ensure the translation is rubrically and structurally sound. 

| Audit Layer | Status | What It Covered |
|---|---|---|
| **Structural Integrity** | ✅ Complete | Enumerated list sequence matching, paragraph volume comparison, and byte-size ratios between Ukrainian and English source files. Confirms no paragraphs were dropped. |
| **Visual Rubrical (Footnote) Audit** | ✅ Complete | Verified the physical placement and sequencing of 785+ footnote markers across all 287 pages of the 2010 Ukrainian source PDF. |
| **Vocabulary Unification** | ✅ Complete | 25 distinct liturgical terminology drift groups were standardized across all files (e.g., *Tserkovne Oko*, *Sluzhebnik*). |
| **Typographical Polish** | ✅ Complete | Enforcement of smart quotes, em-dashes, and trailing whitespace cleanup. |
| **Hieratic Pronoun Audit** | ✅ Complete | Enforcement of capitalized deity pronouns (Thee, Thou, Thy, etc.). |
| **Calendar Symbol Audit** | ✅ Complete | Verified that all special calendar classification symbols in Part 3 (Menaion) were preserved. |
| **Translation Accuracy** | ❌ Pending | Requires a Ukrainian-literate reviewer to do a line-by-line semantic verification of the English text against the Ukrainian source. |

---

## 2. What the "Visual Rubrical Audit" Accomplished

The Visual Rubrical Audit (detailed in `visual_audit_log.md`) was a massive **footnote-placement verification**. It compared footnote marker positions in the English text against their physical positions on the 2010 Ukrainian source PDF pages. 

**What it verified:**
- Footnote marker sequence has no gaps.
- Footnote markers are placed on the correct sentence.
- Footnote definitions in `Final_footnotes.txt` match the 2010 source.
- Publisher anomalies (e.g., duplicate `[^3]`) were correctly reconciled without losing data.

**What it did NOT verify:**
- Whether the underlying English *translation* of the rubrics is semantically accurate.

---

## 3. Key Compliance Decisions

1. **Book Titles**: All liturgical book titles (*Tserkovne Oko*, *Sluzhebnik*, *Chasoslovets*) are treated as proper names and NOT translated.
2. **Deity Capitalization**: Strict enforcement of capitalization for pronouns referring to God.
3. **Edition Fidelity**: The source text is strictly the 2010 Lviv reprint. If the English translation deviated due to AI referencing an older or alternate edition, it was corrected to match the 2010 Ukrainian text.

---

## 4. Next Steps & Open Work

1. **Semantic Translation Audit:** The primary remaining QA step is a human review of the translation accuracy.
2. **Historical Fidelity Audit:** Validating Latin-derived terms (e.g., Monstrance, Dalmatic) against the Eastern liturgical context.
3. **Publishing Pipeline:** Creating a Pandoc or LaTeX script to compile the final text files and footnotes into a finalized PDF or Word document for publication.
