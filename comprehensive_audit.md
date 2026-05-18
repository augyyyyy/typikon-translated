# Comprehensive Translation & Compliance Audit
## Dolnytsky Typikon — Scientific Edition
**Date:** April 25, 2026

---

## Question 1: What is the "Visual Rubrical Audit" actually auditing?

The so-called "visual rubrical audit" (conversation `44514422`) is **not** a translation accuracy audit. It is specifically a **footnote-placement verification** — comparing footnote marker positions in the English text against their positions on the 2010 Ukrainian source PDF pages. What it checks:

| Checked | Not Checked |
|---|---|
| Footnote marker sequence (no gaps) | Whether the English *translation* is accurate |
| Footnote marker *placement* on correct sentence | Whether rubrical instructions are correctly rendered |
| Footnote *definition* matches the 2010 source | Whether liturgical terminology is contextually correct |
| Publisher anomalies (e.g., duplicate `[^3]`) | Paragraph-level translation fidelity |

**Bottom line:** The rubrical audit is a footnote QA pass, not a translation audit. It has verified pages 1–29 (~10% of the source).

---

## Question 2: Has a Translation Accuracy Audit Been Completed?

**No.** No systematic translation accuracy audit has been performed. What *has* been done:

| Audit Layer | Status | What It Covered |
|---|---|---|
| **Structural integrity** | ✅ Done | Enumerated list sequence matching, paragraph volume comparison, byte-size ratios between Ukrainian and English |
| **Footnote placement** | 🔶 10% | Pages 1–29 |
| **Vocabulary unification** | ✅ Done | 25 drift groups standardized across all files |
| **Typographical polish** | ✅ Done | Smart quotes, em-dashes, trailing whitespace |
| **Translation accuracy** | ❌ Not done | No line-by-line verification that the English correctly renders the Ukrainian meaning |
| **System instructions compliance** | ❌ Not done | See Section 3 below |

> [!WARNING]
> The structural audit confirmed that no *paragraphs were dropped*, but it did NOT verify that the *content within each paragraph* was correctly translated. The translation was produced by an AI model across many chat sessions, and no human or machine review of semantic accuracy has been performed.

---

## Question 3: Are Those All the Drift Groups?

**No.** The current `full_terminology_audit.py` monitors **25 drift groups**. All have been adjudicated in the `vocabulary_standardization_matrix.md`.

---

## Question 4: Have the System Instructions Been Followed Throughout?

### Decision: "Tserkovne Oko" vs. "Eye of the Church"

> [!CAUTION]
> **The system instructions explicitly state:**
> *"Tserkovne Oko = Tserkovne Oko (Do not translate as 'Eye of the Church')"*
>
> **The decision (Option A) has been finalized:**
> Revert to **"Tserkovne Oko"** as the canonical form to maintain consistency with the proper names of other liturgical books (Octoechos, Triodion, etc.) and strictly follow system instructions.
>
> **Status:** All occurrences in the `Final/` files have been unified to "Tserkovne Oko" (405 occurrences).

---

## ACTION PLAN

| Priority | Task | Status |
|---|---|---|
| 🔴 1 | **Resume footnote placement audit** — pages 30–287 | 🔶 In Progress |
| 🟡 2 | **Calendar symbol audit** — verify Part 3 Menaion symbol preservation | ❌ Pending |
| 🟡 3 | **Hieratic pronoun completeness audit** — scan for missed lowercase deity pronouns | ❌ Pending |
| 🔵 4 | **Translation accuracy audit** — would require Ukrainian-literate reviewer | ❌ Pending |

---

## Log of Key Decisions

1. **Book Titles**: All liturgical book titles (*Tserkovne Oko*, *Sluzhebnik*, *Chasoslovets*) are treated as proper names and NOT translated.
2. **Footnote misprints**: Publisher duplicate `^3` (Image 016) is anchored as `[^3a]` to maintain unique markdown keys while preserving physical placement.
