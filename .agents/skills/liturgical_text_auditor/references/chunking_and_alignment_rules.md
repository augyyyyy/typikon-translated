# Logical Chunking, Bilingual Structural Alignment & `SGC-02` Parity Rules

## 1. Deterministic Structural-Key Chunking Engine (`Rule 2`)
Naive character-based chunking splits paragraphs mid-sentence and breaks bilingual alignment. Always partition and align `Source Text/` and `Draft/` files using hierarchical structural keys:

| Priority | Boundary Type | Canonical Pattern / Delimiter |
| :-: | :--- | :--- |
| **1** | **Physical Leaf Boundary** | `^=== LEAF p(\d+) ===$` (Mandatory 1:1 bijection across `Source Text/`, `Draft/`, `Cohorts/`, and `Final/`). |
| **2** | **2-Up Spread Milestone** | `^\*\*\[(?:Left|Right) Page — [^\]]+\]\*\*$` (When a single physical leaf scan captures a two-page opening). |
| **3** | **Authorized Headings** | `^#\s+` (Part landmark) or `^##\s+` (Primary service/day headpiece). |
| **4** | **Numbered Statutes / Rubrics** | Roman numerals (`I.`, `II.`, `III.`), Arabic numerals (`1.`, `2.`, `3.`), or section signs (`§ 1.`). |
| **5** | **Sentence Subdivision (`> 15,000` chars)** | Split only on `(?<=[.?!])\s+` (sentence-terminal punctuation followed by whitespace), never mid-clause. |

---

## 2. `SGC-02` Three-Tier Ground-Truth & Primary-Source Bijection (`PE-HSG-03`)
Enforced by `scripts/structural_audit.py` during Phase 1 Small Pause Gates and by Gate 6 of `scripts/verify_publication_edition.py` during Phase 2 compilation:

1. **Minimum Non-Blank Leaf Density**:
   - Every non-sparse, non-vacat `=== LEAF pN ===` block in both `Source Text/` and `Draft/` must contain `>= 50` alphanumeric characters and `>= 10` words.
   - Blank folios, flyleaves, and full-page engravings must use symmetric diplomatic descriptions or canonical vacat markers (`*(Vacat — Fol. Xv: Unnumbered blank verso)*`) in both `Source Text/` and `Draft/` so length ratios remain within `[0.80, 1.50]`.
2. **Draft-to-Source Length & Word-Ratio Bounds**:
   - Hard publication gate bounds: `[0.35, 3.00]`.
   - Phase 1 `argon_review_queue.json` Signal 2 threshold: flags non-sparse leaves with ratio `< 0.50` (potential omission/truncation) or `> 2.20` (potential `Rule 16` unwritten incipit expansion) for Phase 2 `Argon` visual inspection.
3. **Orthographic Authenticity (`Vector 5C`)**:
   - `scripts/audit_transcript_trajectory.py` audits `Source Text/` for synthetic Church Slavonic hypercorrections (such as replacing printed `от` with `ѿ` in `Слава Отцю`) and heals them deterministically.

---

## 3. Quantitative Recension Affinity Auditing (`scripts/recension_detector.py`)
Run on any completed monument or cohort to classify recensional markers against `../Shared_Lexicon/typikon_recension_grid.json`:
```powershell
py scripts/recension_detector.py --target "<workspace>"
```
Evaluates the 5 Kachmar diagnostic dimensions: (1) Prosphora count (1 vs. 4 vs. 5), (2) Creed *Filioque* treatment, (3) Third Hour Epiclesis presence/absence, (4) Hierarchical commemoration formulas, and (5) Ruthenian chant/realia markers (*Samohlasen, Podoben, Tetrapod, Klepalo*).
