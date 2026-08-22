---
name: liturgical_vision_auditor
description: Audits final English translations against original page-scan images (JPG/PDF) to evaluate layout, heading levels, table structures, en/em dash consistency, and visual footnote positioning.
---

# Liturgical Vision Auditor Skill Guidelines

When executing a visual page scan audit:

## 1. Audit Log Integrity & Visual Log Limits
When interpreting the output of `liturgical_vision_auditor` scripts that produce an audit log, the agent must **not** infer missing entries, interpolate "invisible" elements, or fabricate bounding-box coordinates. If the log reports zero matches for a category the agent expected, it must **explicitly state** that detection failed for that category and **persist this empty result** in any summary. Ghost loops (re-running the detector endlessly because the expected count was not reached) are forbidden; after a maximum of 3 retries, the agent must report the discrepancy and stop. Limit visual screenshots of diffs to 50 per run to prevent disk exhaustion.

## 2. Absolute Path Checks for Image Loaders
All image-loading utilities within the auditor (e.g., `load_image()`) must resolve paths using `pathlib` relative to the project root or an environment-defined data directory. Any hardcoded absolute path in a loader is an immediate regression. Before running a detection, the agent should verify that the loaded image path does not contain a drive letter or known user-specific prefix.

## 3. Footnote Placement Validation
* Visually match footnote markers (e.g. `[^N]`) in the English draft against their physical positions in the page scan.
* Ensure no footnotes are dropped or detached from their corresponding paragraphs.
* Verify the master footnotes file (`Final_footnotes.txt`) contains the definition for every visual footnote present on the page.

## 4. Formatting & Typography Guidelines
* Check heading structures (bolding, italics, underlines) to make sure they correspond to the formatting style of the source scans.
* Ensure proper en dashes (` – `) or em dashes (` — `) are used for sentence ranges and breaks, replacing standard hyphens (`-`).
* Ensure tables are formatted consistently as Markdown tables, preserving original layouts.
