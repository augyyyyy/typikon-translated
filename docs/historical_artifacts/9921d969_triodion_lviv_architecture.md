# Triodion Season Paradigms: Lviv 2010 vs. Custom Case Expansions

This document analyzes the general cases for the Triodion/Pentecostarion seasons, compares them to custom case-expansion systems (which define cases beyond Case 20), and explains how **Typikon Coded** adapts these concepts to remain compliant with the authoritative **UGCC Liturgical Directory (Lviv 2010)**.

---

## 1. General Cases for the Triodion Seasons

Liturgically, the Triodion movable cycle (Great Lent) and the Pentecostarion cycle (Eastertide) present unique combinations:

1.  **Pre-Lenten Sundays**: (Publican & Pharisee, Prodigal Son, Meatfare, Cheesefare) — Blend Sunday *Octoechos* with Triodion proper texts.
2.  **Lenten Weekdays**: Strictly aliturgical days or the Liturgy of the Presanctified Gifts (Wednesdays and Fridays).
3.  **Lenten Saturdays**: Dedicated to the departed or specific Lenten commemorations (St. Theodore, Akathist Saturday).
4.  **Lenten Sundays**: St. Basil the Great's Divine Liturgy combined with Triodion canons and the daily Menaion saint.
5.  **Holy Week (The Triduum)**: Highly specialized services (Burial Vespers, Tomb Matins, Vesperal Liturgies).
6.  **Bright Week**: Total dominance of Paschal texts; complete suppression of the *Octoechos* and standard Menaion saints.
7.  **Pentecostarion Sundays**: Blend Sunday Resurrectional propers with Pentecostarion feast themes.

---

## 2. Cases Beyond 20: Case-Expansion Manuals (e.g., Petras)

Liturgical manuals like those of **Father David Petras** often expand the traditional 20 general cases into a flat list of 30+ distinct, hardcoded paradigms. These extra cases typically include:

*   `CASE_23`: Sunday of Great Lent (Resurrection + Triodion + St. Basil Liturgy).
*   `CASE_24`: Weekday of Great Lent (Presanctified Liturgy or Aliturgical days).
*   `CASE_25`: Lazarus Saturday.
*   `CASE_26`: Palm Sunday (Festal Antiphons on Sunday).
*   `CASE_27`: Monday–Wednesday of Passion Week.
*   `CASE_28`: Great Thursday (Vesperal Liturgy of St. Basil).
*   `CASE_29`: Great Friday (Aliturgical, Royal Hours, Burial Vespers).
*   `CASE_30`: Great Saturday (Vesperal Liturgy of St. Basil with "Let all mortal flesh").
*   `CASE_31`: Easter Sunday (Paschal Matins, Hours, Liturgy).
*   `CASE_32`: Bright Week Weekdays (Paschal hours and liturgy).
*   `CASE_33`: Pentecost Sunday (Kneeling Vespers).

While this flat list makes manual lookup simple for a cantor, it introduces **structural redundancy** and drifts from the canonical Lviv Typikon terminology.

---

## 3. Adapting to Strict Lviv 2010 (The Overlay Model)

The authoritative **UGCC Liturgical Directory (Lviv 2010)** follows Isidor Dolnytsky’s *Typikon of the Ruthenian Church* (1899/1904) strictly, keeping the **20 General Cases** as the core framework.

To model the Triodion season without inflating the Case count, **Typikon Coded** implements a **Two-Layer Resolution Architecture**:

```
                  [Date / Pascha Offset Input]
                               |
                               v
               [Layer 1: Base Case Resolution]
          (Resolves to one of the 20 Core Lviv Cases)
                               |
         e.g., Lenten Sunday -> CASE_01 (Sunday Simple)
                               |
                               v
            [Layer 2: Triodion Overlay Resolution]
    (Merges variables from 02c_logic_triodion.json based on offset)
                               |
         - Overwrites Liturgy -> Basil Anaphora
         - Overwrites Antiphons -> Typika / Lenten Beatitudes
         - Inject Matins -> Triodion Canon & small litany inserts
                               |
                               v
                     [Final Book Structure]
```

### Advantages of the Lviv 2010 Overlay Model:
1.  **Canonical Integrity**: The Liturgical Context card dynamically pulls and displays the canonical base case (e.g. `Case 1 — Sunday with Simple Saint`), matching the Lviv 2010 directory.
2.  **No Code Inflation**: Complex seasonal shifts (like Lenten canon ratios or Presanctified Liturgy triggers) are handled via dynamic variable switches in [02c_logic_triodion.json](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Typikon%20Coded/json_db/02c_logic_triodion.json) rather than defining new, redundant Case frameworks.
3.  **Visual Transparency**: The UI displays the *Selected Outlines* (such as `lenten` or `presanctified`) and the *Resolution Trace* to clearly explain the active sub-case overrides without cluttering the primary case classification.
