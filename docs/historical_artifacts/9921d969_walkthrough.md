# Saint Category Splitting Fix & Verification Walkthrough

We have successfully diagnosed, corrected, and verified the category splitting regression that caused Saint Triphyllius (and other saints) to incorrectly display as `[SAINT]`. Additionally, we have cleaned up the "Service Title" row on the liturgical context panel and resolved the Apostles' Fast logic bug.

## 1. Root Cause of the St. Triphyllius Regression

The root cause was **index alignment drift** caused by mismatched splitting logic between the backend (`engine/calendar.py`) and the frontend (`cantor_dashboard/main.js`):

1. **Backend Splitting**: The backend centralized category classifier parsed multiple commemorations by splitting on periods (`\.\s+`).
2. **Abbreviation Breakage**: Since `"St."` (Saint) ends with a period, the backend split `"St. Triphyllius, Bishop of Leucosia."` into:
   - `parts[0]`: `"St"` (classified as `"Saint"`)
   - `parts[1]`: `"Triphyllius, Bishop of Leucosia"` (classified as `"Hierarch"`)
3. **Frontend Mismatch**: The frontend did not split on dots; it only split on `" and "`, `" & "`, or `";"`. Hence, it saw only **one** commemoration: `"St. Triphyllius, Bishop of Leucosia"`.
4. **Incorrect Badge Mapping**: The frontend requested the category at index 0 of the backend's array (`ctx.saint_categories[0]`), which was `"Saint"` (derived from the broken `"St"` prefix).

## 2. Similar Regressions Found (Prophet/Prop. Cases)

By scanning the Dolnytsky calendar database (`json_db/calendar_dolnytsky.json`) for abbreviation patterns ending in a period, we identified:
- `Prop.` (Prophet) - 12 occurrences
- `Ven.` (Venerable) - 98 occurrences
- `St.` (Saint) - 45 occurrences
- `Ap.` (Apostle) - 20 occurrences
- `Sts.` (Saints) - 2 occurrences

While `St.`, `Ven.`, and `Ap.` were included in the negative lookbehind pattern, **`Prop.` was omitted**. Consequently:
* Every commemoration beginning with `"Prop."` (such as `"Prop. Nahum."` or `"Prop. Habakkuk."`) was split incorrectly into `['Prop', 'Nahum']`.
* This caused the primary saint to display as `Prop` (badge `[PROPHET]`) and the actual name `Nahum` to be treated as a secondary saint (badge `[SAINT]`).

## 3. Service Title Row Clean-up

Previously, the **"Service Title"** row displayed a mix of saint names, feast names, and special services (making it inconsistent across days). It has been refactored in [cantor_dashboard/main.js](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon Coded/cantor_dashboard/main.js#L740-L784) to be exclusive to special services:
* **Special Structures**: Shows special service names (e.g., `"Bridegroom Matins"`, `"Passion Matins"`, `"Tomb Matins"`, `"Bright Matins"`, `"Liturgy of the Presanctified Gifts"`, or `"Royal Hours of Theophany/Nativity/Great Friday"`).
* **Solemnity Vigil/Feasts**: Shows Vigil names (e.g., `"Vigil Service (Euthymius the Great)"`) and Great Feast names (e.g., `"THEOPHANY OF OUR LORD"`).
* **Standard Days**: Displays `"Standard Sunday Services"` or `"Standard Daily Services"` instead of redundantly repeating the saint's name.

## 4. Apostles' Fast Fasting Logic Bug

### Problem
The engine previously failed to apply Lviv Synod fasting rules for the **Apostles' Fast** season (which begins on the Monday after All Saints and runs through the Eve of the feast of Saints Peter and Paul on June 28). Monday, June 15, 2026 was incorrectly marked as `no_fast` instead of a fast day.

### Solution
1. **Engine Update**: Added a check in [engine/resolvers/ceremonial.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/engine/resolvers/ceremonial.py#L78-L93) to detect the Apostles' Fast range (`pascha_offset >= 57` and date on/before June 28).
2. **Fasting Days**: Applied a strict/simple fast (`fast_day` with Lviv Synod citation) to Mondays, Wednesdays, and Fridays during this season, while preserving standard rank-based festal relaxations (e.g., allowing oil and wine for St. Theodore Stratelates on June 8 or fish for St. Onuphrius on June 12).
3. **Unit Tests**: Added comprehensive test cases in [tests/test_gold_standard_truth.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/tests/test_gold_standard_truth.py#L46-L65) to cover fast start/end, fasting days, non-fasting days (Tuesdays/Thursdays/Saturdays/Sundays), and all festal relaxations.

## 5. John the Baptist Category Badge Correction

We mapped `John the Baptist`, `John the Forerunner`, and `Forerunner` to the General Menaion service category `Prophet` in:
- Backend: [engine/calendar.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/engine/calendar.py#L45-L46)
- Frontend: [cantor_dashboard/main.js](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/cantor_dashboard/main.js#L367-L369)

This enforces that St. John the Baptist is celebrated under the standard General Menaion service category of `Prophet` rather than arbitrary titles.

## 6. Sunday Combined Readings Override Fix

We refactored `resolve_liturgy_readings` in [engine/resolvers/liturgy.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/engine/resolvers/liturgy.py#L929-L1034):
- **Weekday & Simple Sunday Overrides**: Returns overridden readings directly for weekdays and Sundays without Vigil/Polyeleos saints (such as Triodion Sundays).
- **Vigil/Polyeleos Sunday Overrides**: Combines the Sunday resurrectional readings with the saint's overridden readings on Sundays when a Vigil or Polyeleos saint is commemorated.
- **Double Nesting Prevention**: Safely extracts the list from dictionary overrides to prevent duplicate wrapping.

## 7. Remediation & Verification

We completed the following verification steps:
1. **Regex Alignment**: Added `(?<!\bProp)` to the negative lookbehind regexes in both [engine/calendar.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/engine/calendar.py#L413) and [cantor_dashboard/main.js](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/cantor_dashboard/main.js#L768).
2. **Almanac Regeneration**: Regenerated the annual almanac database (`json_db/almanac/annual_almanac_2026.json`) to incorporate correct, non-split categories and updated liturgical variable distributions.
3. **Test Suite**: Ran `pytest` verifying that all **318 tests pass successfully** (including new precedence tests).
4. **Compliance Gate**: Ran `compliance_gate.py` verifying that post-flight checks pass.
