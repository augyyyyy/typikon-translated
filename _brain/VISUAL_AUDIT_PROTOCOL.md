# Visual Rubrical Audit — Protocol & Progress

## What This Audit Is

A **page-by-page footnote placement verification** comparing footnote marker positions in the English Final text against their physical superscript positions on the 2010 Ukrainian source PDF page images.

### What It Checks

| ✅ Checked | ❌ NOT Checked |
|---|---|
| Footnote marker sequence (no gaps) | Whether the English *translation* is accurate |
| Footnote marker *placement* on correct sentence | Whether rubrical instructions are correctly rendered |
| Footnote *definition* matches the 2010 source | Whether liturgical terminology is contextually correct |
| Publisher anomalies (e.g., duplicate `[^3]`) | Paragraph-level translation fidelity |

> **Bottom line:** The visual rubrical audit is a **footnote QA pass**, not a translation audit.

> **⚠️ KNOWN HAZARD: Do NOT get sidetracked by "edition analysis."**  
> The 2010 Lviv book is the ONLY source. If the English text doesn't match the 2010 Ukrainian image, correct the English. Do not speculate about "1899 text contamination" or spend time analyzing which edition a passage came from. This exact mistake derailed a previous session at Images 120–125 (Annunciation section). See `DECISION_LOG.md` → Decision 0.

## Execution Protocol

For every single image (`.jpg`), execute the following loop:

1. **Fetch Image**: Load `Typyk UHKC(укр)-XXX.jpg` from the `Typyk UHKC pdf/` directory.
2. **Identify Text Bounds**: Locate the corresponding English text bounds in the relevant `Final_Dolnytsky_*.txt` file.
3. **Comparative Analysis**: Compare the Ukrainian visual source against the English text line-by-line.
   - Verify footnote superscript placements (`1`, `2`, `3` in image → `[^1]`, `[^2]`, `[^3]` in text).
   - Verify formatting (bolding, indentation, headers).
   - Verify terminology against the `vocabulary_standardization_matrix.md`.
4. **Log Findings**: Write an explicit, timestamped entry in `visual_audit_log.md` detailing the image number, corresponding English text lines, discrepancies, and correction actions.
5. **Execute Correction**: Apply fixes to the `Final_Dolnytsky_*.txt` file.
6. **Mark Task Complete**: Update `task.md`.

## Progress Tracker

### Phase 1: Introduction (Images 001–005) → ✅ COMPLETE
- **File:** `Final_Dolnytsky_intro.txt`
- **Footnotes verified:** `[^1]`

### Phase 2: Part 1 — Structure (Images 006–022) → ✅ COMPLETE
- **File:** `Final_Dolnytsky_part1_structure.txt`
- **Footnotes verified:** `[^2]` through `[^43]`
- **Corrections:**
  - Missing 2010 publisher footnote `[^3]` on Page 6 — injected
  - Misplaced `[^16]` — relocated from Page 7 to Page 11
  - Page 16 anomalous `^3` (publisher misprint) → anchored as `[^3a]`

### Phase 3: Part 2 — General Rubrics (Images 023–053) → ✅ COMPLETE
- **File:** `Final_Dolnytsky_part2_general_rubrics.txt`
- **Footnotes verified:** `[^44]` through `[^240]`
- **Corrections:**
  - `[^75]` and `[^76]` moved to correct location on Page 29

### Phase 4: Part 3 — Menaion (Images 054–124) → ✅ COMPLETE (to Image 124)
- **File:** `Final_Dolnytsky_part3_menaion.txt`
- **Footnotes verified:** `[^241]` through ~`[^430]`
- **Corrections (Images 054–115):**
  - Phantom `[^244]` anchors removed from Lines 36, 37, 41, 43 (Image 055)
  - `[^245]` moved to correct rubrical location (Image 055)
  - `[^381]` removed from Christmas Eve, added to Forerunner Entrance
  - Phantom `[^388]` removed from Page 109, real `[^388]` added to Page 111
  - Footnote definitions `[^380]` and `[^381]` inserted, `382`–`388` range re-indexed
- **Corrections (Images 116–124, Annunciation section):**
  - Annunciation Sections 4–11 (March 25): English text corrected to match 2010 Ukrainian
  - `[^407]`, `[^408]`, `[^409]`, `[^413]` placed correctly
  - `[^418]`, `[^419]`, `[^420]` recovered and anchored in Section 13
  - March 26 (Apodosis): Expanded from 7 cases to 9 cases per the 2010 text
  - `[^422]`, `[^424]`, `[^425]`, `[^430]` anchored

### Phase 5: Part 3 continued + Parts 4–5 (Images 125–287) → ❌ NOT STARTED
- **Resume at:** Image 125
- **⚠️ Known issue at Image 125:** There appears to be content between March 26 and April 23 that the English file skips. The previous model searched extensively but never resolved this. See `OPEN_WORK.md` → Priority 1 for full forensic detail of what was searched and what remains unknown. The text likely already exists in RAW or English Broken — find it, don't re-translate.
- **Remaining images:** 163
- **Estimated footnotes:** `[^430]`+ through `[^785]`

## Image-to-File Mapping

| Image Range | File | Content |
|---|---|---|
| 001–005 | `Final_Dolnytsky_intro.txt` | Introduction |
| 006–022 | `Final_Dolnytsky_part1_structure.txt` | Part I: Structure |
| 023–053 | `Final_Dolnytsky_part2_general_rubrics.txt` | Part II: General Rubrics |
| 054–146 | `Final_Dolnytsky_part3_menaion.txt` | Part III: Menaion |
| 147–210 | `Final_Dolnytsky_part4_triodion.txt` | Part IV: Triodion |
| 211–247 | `Final_Dolnytsky_part5_temple.txt` | Part V: Temple/Calendar |
| 248–287 | `Final_Dolnytsky_appendix.txt` | Ordo Celebrationis (Appendix) |

## Known Publisher Anomalies

| Page | Issue | Resolution |
|---|---|---|
| Page 16 (Image 016) | Duplicate `^3` in footnote sequence (24, **3**, 25, 26, 27) | Anchored as `[^3a]` to maintain unique markdown keys |

## Persistent Log

The detailed per-image audit log is maintained in the project root:
→ `visual_audit_log.md` (1,734 lines as of May 2026)
