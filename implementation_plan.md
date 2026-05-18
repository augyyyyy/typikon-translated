# Global Visual & Rubrical Audit: Dolnytsky Typikon (Detailed)

This plan outlines the systematic, page-by-page visual audit of the entire Dolnytsky Typikon English translation corpus, starting from the absolute beginning (`pre part 1`). This process will strictly utilize the raw primary source images (`.jpg` files) to guarantee 100% rubrical, philological, and choreographic fidelity.

## Objective
To perform a ground-up validation of all English texts against the Ukrainian 2010 Lviv Edition (`Typyk UHKC pdf` directory), ensuring:
1.  **Perfect Footnote Synchronization:** Every `[^n]` marker in the text matches the physical superscripts in the 2010 edition.
2.  **Zero Hallucinations:** Eradication of any phantom anchors, OCR drift, or AI-generated interpolations.
3.  **Absolute Rubrical Fidelity:** Translation accuracy regarding terminology, sequences, and layout.

## Execution Strategy & Logging Protocol

To ensure seamless model-to-model handoff ("model transfer on the spot"), every single step will be documented in a persistent artifact: `visual_audit_log.md`.

### The Visual Audit Loop (Per Image)
For every single image (`.jpg`), the agent will execute the following loop:
1.  **Fetch Image**: Load `Typyk UHKC(укр)-XXX.jpg` via the `view_file` tool to ingest the visual data.
2.  **Identify Text Bounds**: Locate the corresponding English text bounds in the relevant `Final_Dolnytsky_*.txt` file.
3.  **Comparative Analysis**: Compare the Ukrainian visual source against the English text line-by-line.
    *   Verify footnote superscript placements (`1`, `2`, `3` in the image -> `[^1]`, `[^2]`, `[^3]` in the text).
    *   Verify formatting (bolding, indentation, headers).
    *   Verify terminology against the `vocabulary_standardization_matrix.md`.
4.  **Log Findings**: Write an explicit, timestamped entry in `visual_audit_log.md` detailing the image number, the corresponding English text lines, any discrepancies found, and the specific correction action taken.
5.  **Execute Correction**: Apply the fix to the `Final_Dolnytsky_*.txt` file.
6.  **Mark Task Complete**: Update `task.md`.

## Current Progress (April 25, 2026)
- **Phase 1 (Intro)**: Complete (Images 001-005)
- **Phase 2 (Part 1)**: Complete (Images 006-022)
- **Phase 3 (Part 2)**: In Progress (Resuming at Image 030)
