---
name: liturgical_text_auditor
description: Audits Slavonic/Ukrainian-to-English liturgical text translations using Native Gemini Vision, enforcing 1:1 structural segment alignment, SGC-02 word-ratio parity, and zero omitted sentences or glossary drift.
---

# Liturgical Text Auditor Skill Guidelines

When executing a bilingual text alignment audit or translation verification across `Source Text/`, `Draft/`, `Cohorts/`, or `Final/`:

## 1. Native Gemini Vision & Canonical Witness Hierarchy (`Rule 1` & `Rule 3`)
* All primary-source audits operate exclusively via **Native Gemini Vision** (`view_file`/`read_file` on 300 DPI leaf scans in `Source Text/images/`) and deterministic Python validators.
* **Prohibition of Third-Party APIs**: All external LLM/OCR APIs (including DeepSeek, OpenAI, and Anthropic) are permanently prohibited (`Rule 1`).
* **Monument Witness Authority**: Verify each monument against its own physical 300 DPI facsimile (`Rule 16` & `SGC-06`), using `../Shared_Lexicon/typikon_recension_grid.json` (Kachmar Diagnostic Grid) and `scripts/recension_detector.py` to document recensional variants across historical witnesses (e.g., 1720 Zamość Synod, 1761 Pochaiv Menaion, 1852 Doskovsky, 1888 Violakis, 1891 Lviv Synod, 1899 Dolnytsky Typikon, 1901 Mikita, 1910 Skaballanovich, 2010 Lviv Typikon) in footnotes `[^N]`.

## 2. Logical & Semantic Chunking Rules (`Rule 2`)
* Never split files by naive character counts that sever sentences or paragraphs.
* Align `Source Text/` and `Draft/` segments by matching explicit structural boundaries:
  1. Physical leaf banners (`=== LEAF pN ===`) and 2-up spread milestones (`**[Left/Right Page — Fol. Xr]**`).
  2. Authorized Part/Service headings (`#`, `##`), Roman numeral points (`I.`, `II.`, `III.`), and numbered statutes (`1.`, `2.`, `§ 1.`).
* Keep individual comparison chunks under `15,000` characters; if a single section exceeds `15,000` characters, subdivide strictly at sentence boundaries (`. `, `? `, `! ` followed by a space).

## 3. Discrepancy Flagging Protocol (`SGC-02` & `PE-HSG-03`)
Check and report:
1. **Dropped Sentences or Rubrics**: Any sentence, parenthetical rubric, or marginal citation present in `Source Text/` that is absent in `Draft/`.
2. **Unwritten Incipit Expansion (`Rule 16` / `PE-HSG-04`)**: Any abbreviated Slavonic incipit (*titlo* shorthand) expanded into a full unwritten prayer in the English body text.
3. **Per-Leaf Density & Parity (`PE-HSG-03`)**: Non-blank leaves must satisfy `>= 50` alphanumeric chars, `>= 10` words, and `Source Text/` ↔ `Draft/` word-ratio bounds (`[0.35, 3.00]`).
4. **Glossary, Pronoun & Footnote Bijectivity**: Verify zero forbidden terms (`../Shared_Lexicon/lint_vocabulary.py`), 100% Deity pronoun capitalization (`scripts/hieratic_pronoun_audit.py`), and 1:1 `[^N]` ↔ `[^N]:` symmetry (`scripts/reconcile_footnotes.py`).

## 4. On-Demand Reference Playbook
* [`references/chunking_and_alignment_rules.md`](references/chunking_and_alignment_rules.md) — Deterministic structural-key alignment algorithm, `SGC-02` ratio diagnostics, and `recension_detector.py` audit workflow.
