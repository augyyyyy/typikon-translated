# Implementation Plan - Stamford and Royal Doors Troparia/Kontakia Comparison

This plan outlines the process for comparing every entry in the "Troparia and Kontakia of the year" section (from Stamford's `TROPARIA MENAION.md`) against the corresponding entries in the Royal Doors daily propers database (`text_royaldoors.json`).

## Technical Context & Challenges

1. **Date Resolution**: Stamford's `TROPARIA MENAION.md` lists commemorations sequentially without explicit day numbers. 
   - Most months map 1-to-1 to calendar days.
   - Some months contain **anomalies**:
     - **Rubrics**: Plain text cross-references (e.g. "For the Troparion and Kontakion, see Monday..." in November). These do not contain new hymns and should not increment the calendar day.
     - **Skipped days**: (e.g. Feb 17, June 8, June 30 are skipped in the Stamford list).
     - **Movable Sundays**: Days like `Sunday of Christ the King` (October) or `Sunday of the Holy Forefathers` (December) are inserted between fixed dates.
   - **Solution**: We will implement a procedural date-resolver in Python. It will identify rubrics and movable Sundays using string keywords, apply hardcoded offsets for the 3 skipped days, and sequentially assign fixed dates (`MM_DD`).

2. **Hymn Pairing & Matching**:
   - Royal Doors stores Troparia and Kontakia sequentially in the daily liturgy propers under keys like `liturgy.troparion_1`, `liturgy.troparion_2`, `liturgy.troparion_glory` (often the first Kontakion), and `liturgy.troparion_both_now` (often the second Kontakion).
   - **Solution**: For each resolved date `MM_DD`, we will retrieve all Royal Doors hymns for that date. We will pair each Stamford hymn in the block with its corresponding Royal Doors candidate using Jaccard word-overlap similarity.
   - If Jaccard similarity is below 0.35, we will search all Royal Doors hymns (without date restriction) to catch any off-date matches, but mark them for manual verification.

3. **Comparison & Report Generation**:
   - We will generate a human-readable comparison report `stamford_royaldoors_troparia_comparison.md`.
   - The report will group results by month and day, displaying:
     - The Stamford hymn text.
     - The matching Royal Doors hymn text.
     - A character/line-level diff if they differ.
     - A label if they are identical or if no match was found.

## Proposed Changes

We will not modify any existing source code in the main project. Instead, we will create scratch scripts and output the comparison report:

* **[NEW]** [run_comparison.py](file:///C:/Users/augus/.gemini/antigravity/brain/9025717e-97c6-4ee4-bc59-6a97eba223c0/scratch/run_comparison.py): Python script that parses Stamford blocks, resolves calendar dates, pairs them with Royal Doors entries, and writes the comparison report.
* **[NEW]** [stamford_royaldoors_troparia_comparison.md](file:///C:/Users/augus/.gemini/antigravity/brain/9025717e-97c6-4ee4-bc59-6a97eba223c0/stamford_royaldoors_troparia_comparison.md): The final comparison report.

## Verification Plan

### Manual Verification
- Execute `run_comparison.py` to ensure it parses the entire calendar year without errors.
- Randomly audit matched entries (e.g. Jan 1, Feb 2, Dec 25) to verify the pairing is accurate.
- Confirm the generated markdown report formats diffs correctly.
