# Implementation Plan: Expand Dolnytsky Typikon Implementation Reference

This plan outlines the updates to [DOLNYTSKY_IMPLEMENTATION.md](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/docs/DOLNYTSKY_IMPLEMENTATION.md) to comprehensively document the logic engine's coverage of the Triodion moveable cycle, Pentecostarion moveable cycle, collision logic, seasonal Katavasiae, and temple/patronal overrides.

## User Review Required

> [!NOTE]
> This update is purely documentation-focused to align the master `DOLNYTSKY_IMPLEMENTATION.md` reference with the v0.5.0 logic engine implementation. No codebase logic or JSON rules will be altered.

## Open Questions

- *Are there any additional local custom rubrics (e.g. from the Stamford recension) that should be explicitly called out alongside the Lviv Synod mandates?*

## Proposed Changes

### Documentation

#### [MODIFY] [DOLNYTSKY_IMPLEMENTATION.md](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/docs/DOLNYTSKY_IMPLEMENTATION.md)
We will expand the file (currently 243 lines) to cover:
1. **Group F: The Triodion Moveable Cycle (Lent & Holy Week)**: Document the paradigms for Pre-Lenten Sundays, Soul Saturdays, Lenten Sundays (Orthodoxy, Gregory Palamas, etc.), Great Canon Thursday, Akathist Saturday, Lazarus Saturday, Palm Sunday, and Holy Week days (Presanctified Liturgy settings and Great Friday/Saturday Tomb Matins).
2. **Group G: The Pentecostarion Moveable Cycle**: Document Pascha/Bright Week suppression logic, Pentecostarion Sundays (Thomas, Myrrhbearers, Paralytic, Samaritan, Blind Man, Fathers of 1st Council, All Saints), and major Pentecostarion feasts (Mid-Pentecost, Ascension, Pentecost, Holy Spirit Monday).
3. **Group H: Ruthenian Mandates**: Document the Lviv Synod moveable feasts (Corpus Christi / Feast of the Eucharist, Friday of the Co-suffering of the Theotokos).
4. **Section 4: Collision Overrides**: Document the collision rules in `02k_logic_collisions.json` (such as Kyrio-Pascha, Annunciation falling during Lent/Holy Week/Pascha, and St. George/Menaion feast transfers).
5. **Section 5: Seasonal Katavasia Selection**: Document the seasonal irmos lookup rules in `02e_logic_katavasia.json` and year-round immovable/movable date ranges in `katavasia_seasons.json`.
6. **Section 6: Temple/Patronal Override Logic**: Detail the Patronal Feast logic from `02d_logic_temple.json`, including the 6 general rules, the Apodosis rule, processing guidelines, and specific transfer actions (e.g., transferring from Holy Week or Cheesefare).
7. **Section 7: Minor and Secondary Services**: Document the logic and structure handling for Small Vespers, Litiya, Midnight Office variants, and Royal Hours.

## Verification Plan

### Manual Verification
- We will review the final `DOLNYTSKY_IMPLEMENTATION.md` document for spelling, markdown link formatting (ensuring file links point to correct paths using `file://` scheme), and accuracy against the source JSON files (`02c_logic_triodion.json`, `02d_logic_temple.json`, `02e_logic_katavasia.json`, and `02k_logic_collisions.json`).
- Ensure no code files were modified by running `git status`.
