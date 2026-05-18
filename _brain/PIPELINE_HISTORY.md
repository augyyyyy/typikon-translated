# Pipeline History — Processing Phases

A chronological record of all major processing phases that transformed raw AI chat outputs into the current Final files.

---

## Phase 0: Raw Translation (Multiple Chat Sessions)

**When:** Early 2026  
**What:** The Dolnytsky Typikon was translated from Ukrainian to English across many separate AI chat sessions. Each session produced a chunk of translated text with inline footnote markers.  
**Output:** 5 RAW files in `RAW/` directory (127 KB – 710 KB each)  
**Issues:** Fragmented across sessions, inconsistent terminology, duplicate chunks, AI conversational artifacts mixed in.

---

## Phase 1: Programmatic Cleanup & Stitching

**When:** April 2026  
**Scripts:** `phase1_cleanup.py`, `phase1v2_stitch.py`, `phase1v3_manual.py`, `phase1v4_final.py`

### Phase 1 v1: RAW Cleanup
- Stripped AI conversational artifacts (greetings, confirmations, etc.)
- Deduplicated repeated chunks (Parts 1 & 4 had duplicates)
- Extracted 969 footnote markers across 5 parts
- **Output:** `scratch/CLEANED_RAW_PART{1-5}_TRANSLATION.txt`

### Phase 1 v2: Footnote Marker Stitching
- Attempted to stitch 969 markers from RAW into English Broken text using fuzzy 4-word context matching
- **Result:** 82% success (796/969 placed, 173 failed)
- **Root Causes of Failures:**
  1. Smart quote mismatch (RAW uses `''""`; English Broken uses `'"`)
  2. Duplicate marker extraction (Parts 1 & 4)
  3. Heavy text reformatting (Part 5 — only 58% success)
- **Output:** `scratch/STITCHED_dolnytsky_part{1-5}_*.txt`

### Phase 1 v3: AI-Driven Manual Placement
- Used AI to read each RAW context snippet and find correct insertion point
- Handled the 173 failed markers, especially Part 5's reformatted text

### Phase 1 v4: Final Stitching
- Combined all successful placements
- **Output:** `scratch/STITCHED_v3_dolnytsky_*.txt` (final intermediate versions)

---

## Phase 2: Semantic Audit & Footnote Compilation

**When:** April 2026  
**Scripts:** `compile_and_format_footnotes.py`, `reconcile_footnotes.py`

- Extracted all 785 unique footnote translations from RAW chat transcripts
- Converted inline markers from `^[N]` to `[^N]` (Markdown standard)
- Appended footnote definitions to bottom of each part file
- Created master `Final_footnotes.txt` with all 785 definitions
- Performed structural integrity audit (enumerated list sequence matching, paragraph volume comparison)
- **Result:** 100% sequence match. No dropped paragraphs.

---

## Phase 3: Typographical Polish

**When:** April 2026  
**Script:** `phase3_polish.py`

- Standardized curly/smart quotes → straight quotes
- Normalized em-dashes
- Cleaned double-spaces and trailing whitespace
- **Output:** The 8 `Final/` files in their base form

---

## Phase 4: Vocabulary Standardization

**When:** April 24–25, 2026  
**Scripts:** `full_terminology_audit.py`, `standardize_vocabulary.py`, `polish_vocabulary.py`, `fix_known_terminology.py` (rounds 1–3), `unify_book_titles.py`

- Identified and adjudicated 25 drift groups
- Applied canonical forms across all 8 Final files
- Created `vocabulary_standardization_matrix.md`
- **Result:** Zero rejected variants in any Final file

---

## Phase 5: Visual Rubrical Audit (Ongoing)

**When:** April 24, 2026 → present  
**Method:** Manual page-by-page comparison of English text against 2010 Ukrainian source page images

- Verified Images 001–146 (Intro, Part 1, Part 2, and the entirety of Part 3 Menaion).
- Resolved major desynchronizations: the "Matrix Error / Ghost Loop" hallucination, March 26 boundary logic gaps, Annunciation structural interpolation drift, and July 31/August 1 transition rubrics.
- Purged trailing duplicate footnote blocks from Part 3.
- Documented findings in `visual_audit_log.md` (2,165+ lines).
- Embedded permanent tracking artifacts directly into repository `_brain/` folder.
- **Status:** Part 3 100% complete. Overall audit ~51% complete. Resume at Image 147 (Part 4 Triodion).

---

## Intermediate File Versions (scratch/)

| Generation | Files | Description |
|---|---|---|
| `CLEANED_RAW_*` | 5 files | RAW with AI artifacts stripped |
| `STITCHED_*` | 5 files | First-pass footnote stitching |
| `STITCHED_v2_*` | 5 files | Improved quote normalization |
| `STITCHED_v3_*` | 7 files | Final intermediate + appendix + footnotes |

All intermediate files are preserved in `scratch/` for provenance tracking.
