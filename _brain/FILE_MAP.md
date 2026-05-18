# File Map — Complete Project Inventory

All files in `E:\Google Antigravity\Projects\Translation\` with descriptions and roles.

---

## Final Files (Production — The Deliverables)

| File | Size | Content |
|---|---|---|
| `Final/Final_Dolnytsky_intro.txt` | 16 KB | Introduction and translator's preface |
| `Final/Final_Dolnytsky_part1_structure.txt` | 82 KB | Part I: Structure of Divine Services |
| `Final/Final_Dolnytsky_part2_general_rubrics.txt` | 143 KB | Part II: General Rubrics |
| `Final/Final_Dolnytsky_part3_menaion.txt` | 310 KB | Part III: Individual Rubrics for the Menaion (largest file) |
| `Final/Final_Dolnytsky_part4_triodion.txt` | 265 KB | Part IV: Triodion Rubrics |
| `Final/Final_Dolnytsky_part5_temple.txt` | 121 KB | Part V: Temple Rubrics + Calendar/Menologion |
| `Final/Final_Dolnytsky_appendix.txt` | 304 KB | Appendix with liturgical tables |
| `Final/Final_footnotes.txt` | 371 KB | Master footnote corpus (785 definitions) |
| `Final/vocabulary_standardization_matrix.md` | 11 KB | Terminology audit verdicts (25 drift groups) |

## Primary Source Materials

### Ukrainian Source PDFs
| File | Size | Content |
|---|---|---|
| `Ukrainian PDFs/Intro.pdf` | 320 KB | Ukrainian source — Introduction |
| `Ukrainian PDFs/Part 1.pdf` | 512 KB | Ukrainian source — Part I |
| `Ukrainian PDFs/Part 2.pdf` | 731 KB | Ukrainian source — Part II |
| `Ukrainian PDFs/Part 3.pdf` | 1.4 MB | Ukrainian source — Part III |
| `Ukrainian PDFs/Part 4.pdf` | 1.2 MB | Ukrainian source — Part IV |
| `Ukrainian PDFs/Part 5.pdf` | 1.9 MB | Ukrainian source — Part V |

### Ukrainian Source TXTs (OCR Extractions)
| File | Content |
|---|---|
| `Ukrainian TXTs/Intro.txt` | OCR text of Introduction |
| `Ukrainian TXTs/Part 1.txt` – `Part 5.txt` | OCR text of Parts 1–5 |
| `Ukrainian TXTs/Appendix.txt` | OCR text of Appendix |
| `Ukrainian TXTs/Footnotes.txt` | OCR text of all footnotes (line-based numbering) |

### Page Images (2010 Lviv Edition)
| Directory | Files | Purpose |
|---|---|---|
| `Typyk UHKC pdf/` | 287 JPG images (`001`–`287`) | Individual page scans for visual audit comparison |

## Intermediate / Working Files

### RAW Translations (Original AI Chat Outputs)
| File | Content |
|---|---|
| `RAW/RAW_PART1_TRANSLATION.txt` – `RAW_PART5_TRANSLATION.txt` | Original fragmented AI translation outputs |

### English Broken (Pre-Final Versions)
| Directory | Content |
|---|---|
| `English Broken/` | Earlier English translation attempts (pre-standardization) |

## Processing Scripts (`scratch/`)

### Pipeline Scripts (Historical — Already Executed)
| Script | Purpose |
|---|---|
| `phase1_cleanup.py` | Strip AI artifacts, deduplicate RAW files |
| `phase1v2_stitch.py` | Stitch footnote markers from RAW into English Broken |
| `phase1v3_manual.py` | AI-driven manual marker placement for failed stitches |
| `phase1v4_final.py` | Final stitching pass |
| `phase3_polish.py` | Typographical polish (quotes, dashes, whitespace) |
| `compile_and_format_footnotes.py` | Compile master footnote file |
| `reconcile_footnotes.py` | Cross-reference footnote definitions |
| `standardize_vocabulary.py` | Apply vocabulary unification rules |
| `polish_vocabulary.py` | Second-pass vocabulary corrections |
| `fix_known_terminology.py` / `round2` / `round3` | Incremental terminology fixes |
| `unify_book_titles.py` | Tserkovne Oko / Sluzhebnik unification |
| `stitch_2010_markers.py` | Stitch 2010 edition-specific markers |

### Audit & Analysis Scripts
| Script | Purpose |
|---|---|
| `full_terminology_audit.py` | Master 25-group terminology scanner |
| `terminology_audit.py` | Earlier terminology audit |
| `footnote_audit.py` | Footnote sequence validation |
| `structural_audit.py` | Paragraph/list sequence comparison |
| `system_instructions_audit.py` | Check compliance with system instructions |
| `hieratic_pronoun_audit.py` | Scan for missed Thee/Thou/Thy |
| `calendar_xref_audit.py` | Calendar cross-reference validation |
| `check_missing_footnotes.py` | Find missing footnote definitions |

### Injection Scripts (Targeted Fixes)
| Script | Purpose |
|---|---|
| `inject_243_255.py` – `inject_272_278_fix.py` | Targeted footnote marker injection for specific page ranges |
| `insert_placeholders.py` / `insert_part5_placeholders.py` | Placeholder insertion for missing markers |
| `apply_xref_tags.py` | Apply service-rank cross-reference tags |

### Data Files
| File | Purpose |
|---|---|
| `footnote_mapping.json` | 253 KB — Master footnote-to-position mapping |
| `typikon_terms.txt` | 57 KB — Draft glossary appendix |
| `missing_footnotes_details.txt` | 24 KB — Report of originally missing footnotes |
| `pronoun_audit.txt` | 9 KB — Hieratic pronoun audit results |
| `cross_block.txt` | 6 KB — Cross-reference data block |

## Project Metadata (Root)

| File | Purpose |
|---|---|
| `project_status_report.md` | Executive status summary |
| `comprehensive_audit.md` | Detailed audit findings & action plan |
| `implementation_plan.md` | Visual audit execution plan |
| `task.md` | Current task checklist |
| `visual_audit_log.md` | 131 KB — Detailed per-image audit log (2,165+ lines) |

## Resources

| File | Purpose |
|---|---|
| `Resources/system instructions typikon.txt` | Canonical translation rules (the "constitution") |
| `Resources/Guide 1.pdf` / `Guide 2.pdf` | Reference guides |
