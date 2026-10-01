# Implementation Plan - John the Baptist Category & Weekday Exceptions

This plan resolves:
1. Correcting the category badge mapping for John the Baptist to return `Prophet` instead of `Forerunner` (since `Forerunner` is a database namespace key rather than a General Menaion commemoration category).
2. The "Default Outline" Exception Gap for June 24, June 29, and August 29 on weekdays, ensuring they drop the Theotokos Canon and daily Liturgy readings.
3. The correct combination of Sunday readings and saint's readings when a Vigil/Polyeleos saint with custom readings falls on a Sunday.
4. Compliance with Dolnytsky citations and other system guidelines.

## Proposed Changes

---

### Component 1: Centralized Category Badge Classification

#### [MODIFY] [calendar.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/engine/calendar.py)
- In `get_liturgical_category`, map `john the baptist`, `john the forerunner`, and `forerunner` to `Prophet` (singular) or `Prophets` (plural).

#### [MODIFY] [main.js](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/cantor_dashboard/main.js)
- In `getLiturgicalCategory`, map `john the baptist`, `john the forerunner`, and `forerunner` to `Prophet`.

---

### Component 2: Weekday Vigil Outlines & Liturgy Readings Exception

#### [MODIFY] [rubrics.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/engine/rubrics.py)
- In `_resolve_rubrics_logic`, check if the day is a weekday (day of week != 0) and falls on June 24, June 29, or August 29.
- If so, override `rubrics["variables"]["matins_canon_distribution"]` to contain only the saint's canon on 12 (dropping the Theotokos canon), citing `Dolnytsky §3.10.2`.

#### [MODIFY] [liturgy.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/engine/resolvers/liturgy.py)
- In `resolve_liturgy_readings`, refactor how the `liturgy_readings` override is processed:
  - Bypassing the early return on Sundays if the saint rank > 1, and instead appending the Sunday readings followed by the saint's overridden readings.
  - Ensuring that weekdays for June 24, June 29, and August 29 return ONLY the saint's readings (suppressing daily lectionary readings), citing `Dolnytsky §3.10.2`.

---

### Component 3: Unit Tests & Verification

#### [MODIFY] [test_ui_classification.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/tests/test_ui_classification.py)
- Add test cases to assert `get_liturgical_category` returns `Prophet` for `**Nativity of St. John the Baptist.**`.

#### [MODIFY] [test_prokeimenon_precedence.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/tests/test_prokeimenon_precedence.py)
- Add test cases verifying:
  - Sunday readings are combined with St. Nicholas readings on Sunday, Dec 6, 2026.
  - Sunday readings are combined with St. John the Baptist readings on Sunday, June 24, 2029.
  - Weekday daily readings are suppressed (saint readings only) on Wednesday, June 24, 2026.

---

## Verification Plan

### Automated Tests
- Run `.\.venv\Scripts\python -m pytest` to verify all tests pass.
- Regenerate the annual almanac: `.\.venv\Scripts\python scripts/generate_annual_almanac.py --year 2026`
- Run the compliance check: `.\.venv\Scripts\python scripts/compliance_gate.py`

### Manual Verification
- Start the server: `.\.venv\Scripts\python cantor_dashboard/server.py`
- Open the dashboard for June 24, 2026.
- Check that the Liturgical Season, Prophet category, Matins canon, and Liturgy readings match the Typikon.
