# Reconcile References to the Unified Master File

We will point all references in the `Typikon Coded` project (comments, annotations, and JSON rules) from the split markdown files to the unified master file (`Dolnytsky_Typikon_Master.md`), making the project self-contained and clean.

## Proposed Changes

### 1. Unified Search and Replace in Project Files

We will run a script to perform a global search-and-replace across all `.json`, `.py`, and `.md` files in the repository.

*   `Final_Dolnytsky_part1_structure.md` -> `Dolnytsky_Typikon_Master.md`
*   `Final_Dolnytsky_part2_general_rubrics.md` -> `Dolnytsky_Typikon_Master.md`
*   `Final_Dolnytsky_part3_menaion.md` -> `Dolnytsky_Typikon_Master.md`
*   `Final_Dolnytsky_part4_triodion.md` -> `Dolnytsky_Typikon_Master.md`
*   `Final_Dolnytsky_part5_temple.md` -> `Dolnytsky_Typikon_Master.md`
*   `Final_footnotes.md` -> `Dolnytsky_Typikon_Master.md`
*   `Final_Dolnytsky_appendix.md` -> `Dolnytsky_Typikon_Master.md`
*   `Final_Dolnytsky_glossary.md` -> `Dolnytsky_Typikon_Master.md`
*   `Final_Dolnytsky_intro.md` -> `Dolnytsky_Typikon_Master.md`

This will preserve all section codes (e.g., `2.1.3.4` or `4.1.10.2.3`), which are unique and refer to paragraphs that correspond exactly to the Master file headings.

### 2. Refactor deepseek_compliance_audit.py

We will update [deepseek_compliance_audit.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/scripts/deepseek_compliance_audit.py) to dynamically extract the Glossary, Triodion, and Menaion sections directly from [Dolnytsky_Typikon_Master.md](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/Data/Service%20Books/Typikon/Dolnytsky_Typikon_Master.md):

*   **Glossary**: Slices text from the line starting with `# 6.3 Glossary` (or containing "Glossary") to `## 6.4 Footnotes`.
*   **Part 3 (Menaion)**: Slices text from `# PART III` to `# PART IV`.
*   **Part 4 (Triodion)**: Slices text from `# PART IV` to `# PART V`.
*   The Menaion section will then be sliced by month as before.

## Verification Plan

### Automated Tests
- Execute `python -m pytest` to verify that the core engine tests are passing.
- Run `python scripts/deepseek_compliance_audit.py --date 2026-02-01 --service vespers` (or similar) to verify that the auditor successfully reads and slices the master file.
