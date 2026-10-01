# Implementation Plan — Granular Heading Citation Model

This plan outlines the changes required to implement a granular, high-precision heading-level citation model across all Typikon source files. 

The goal is to ensure that all headings (including low-level sub-sections) are uniquely and hierarchically numbered so that they can be easily referenced, while preserving the clean, uncluttered reading flow of the liturgical prose itself.

---

## User Review Required

> [!NOTE]
> **No Paragraph-Level Clutter (Gap D Resolved)**
> In response to user feedback, we have **removed paragraph-level numbering (e.g., `[1]`, `[2]`) entirely** from this plan. The body text, speaker cues (`> **Priest**:`), and litanies will remain clean and unnumbered.

---

## Proposed Changes

We will create a python script `apply_citation_model.py` in the scratch directory to perform heading normalization and numbering programmatically and reliably on all source files.

### 1. Splitting Unnumbered Dense Prose (Gap A)
We will split the identified dense sections into standard numbered rubrics:
* **[Daily Matins](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/Data/Service%20Books/Typikon/Final_Dolnytsky_part1_structure.md#L946):** `### 1.5.3 Order of Daily Matins`
  * Split its 7 paragraphs into numbered rubrics: `##### 1.`, `##### 2.`, etc., before applying the global numbering.
* **[Exaltation of the Cross](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/Data/Service%20Books/Typikon/Final_Dolnytsky_part3_menaion.md#L45):** `### 3.1.4 14 September: Universal Exaltation of the Precious Cross`
  * Convert its uppercase sub-headers (e.g. `PREPARATION OF THE PRECIOUS CROSS`) into standard `####` Level 4 headings.

### 2. Numbering Level 4 and Level 5 Headings (Gap B & C)
Every heading level will be prepended with its fully qualified hierarchical path:
* **Level 4 (`####`):** Numbered sequentially under the parent Level 3 heading.
  * *Example:* `#### Beginning` under `### 1.2.2` becomes `#### 1.2.2.4.1 Beginning` (where `1.2.2.4` is the parent H3 path).
* **Level 5 (`#####`):** Numbered sequentially under the parent Level 4 heading.
  * *Example:* `##### Vesting...` under `#### 1.2.1.1` becomes `##### 1.2.1.1.1 Vesting...`.
* **Level 6 (`######`):** Numbered sequentially under the parent Level 5 heading.

---

## Verification Plan

### Automated Verification
1. Run `apply_citation_model.py` to update all source files.
2. Compile the master file `Dolnytsky_Typikon_Master.md`.
3. Run `verify_links.py` to ensure that all internal links (including TOC links) are still **100% resolved** and match their new fully qualified heading anchors.

### Manual Verification
1. Review a diff of a section (e.g., the Vespers Conclusion block) to verify the final rendering aesthetics.

