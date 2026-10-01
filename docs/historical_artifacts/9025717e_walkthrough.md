# Walkthrough - Stamford vs Royal Doors Troparia & Kontakia Translation Evolution

We have successfully standardized the Stamford Divine Office's "Troparia and Kontakia of the Year" calendar appendix (focusing strictly on Troparia and Kontakia, excluding dismissals/rubrics) and traced their year-by-year translation evolution against the Royal Doors Daily Propers database from 2017 to 2026, including a comparative assessment against the unabridged Lambertsen (St. Sergius) translations.

## Changes Made

1. **Standardization Pipeline**:
   - Developed `scratch/standardize_stamford.py` to parse the raw array list in `Stamford Divine Office/JSON_MD/TROPARIA MENAION.md`.
   - Resolved dates for all fixed commemorations, skipped days (Feb 17, June 8, June 30), and movable Sundays.
   - Split combined OCR strings into structured database entries mapping flat keys (`menaion.[date_or_tag].liturgy.[hymn_type]_[index]`) to values containing `"content"`, `"tone"`, and `"rubric"`.
   - Saved the standardized database to `text_stamford_troparia.json`.

2. **liturgically-Aware Yearly Evolution & Lambertsen Assessment**:
   - Developed `scratch/run_comparison_yearly.py` to merge both `text_royaldoors.json` (latest 2025–2026) and `text_royaldoors_old.json` (historical 2017–2024).
   - Developed `scratch/analyze_translation_evolution.py` to semantically classify matched Stamford keys into: **Always Stamford**, **Started as Stamford** (and changed), and **Never Stamford** categories.
   - Performed similarity audits comparing UGCC translations (Stamford, Royal Doors) to ROCOR translations (Lambertsen/St. Sergius) using `text_st_sergius.json` as the Lambertsen benchmark.
   - Saved the final reports to `stamford_royaldoors_troparia_comparison_yearly.md` and `translation_evolution_analysis.md`.

## Verification & Key Findings

### 1. Royal Doors Translation Evolution (188 Keys Analyzed)
* **Never Stamford (71.8% / 135 keys):** Royal Doors used a different translation from Stamford from its very first match.
* **Always Stamford (5.9% / 11 keys):** Royal Doors matched Stamford verbatim across all matched years.
* **Started as Stamford & Changed (1.1% / 2 keys):** Royal Doors began using the Stamford translation but subsequently revised it (e.g. spelling shift of "Simeon" to "Symeon" on Feb 3, and minor pointing tweaks).
* **No Match (21.3% / 40 keys):** Local/custom feasts.

### 2. Lambertsen (St. Sergius) Assessment
* **Lineage Gap:** Both Stamford (0.28 Jaccard) and Royal Doors (0.32 Jaccard) show very low similarity to Lambertsen (St. Sergius).
* **Duality Cause:** Stamford and Royal Doors belong to the **UGCC Greek-Catholic Galician lineage**, while Lambertsen belongs to the **ROCOR Slavonic-Orthodox lineage** (highly academic, archaic English terms like "first-formed" vs "first man", and different spelling conventions).
* **No Convergence:** Royal Doors has not shifted closer to Lambertsen over time; they are pursuing their own internal vocabulary standardization guidelines.
