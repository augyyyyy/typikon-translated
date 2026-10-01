# Dolnytsky Implementation Gap Analysis

This document outlines the gaps identified in `docs/DOLNYTSKY_IMPLEMENTATION.md` when compared to the active logic engine, specifically regarding Triodion/Pentecostarion logic and other system capabilities.

## 1. The Triodion (Lenten) Moveable Cycle
While the documentation details the 20 general Menaion/Octoechos cases, it completely omits the explicit paradigms modeled in `json_db/02c_logic_triodion.json`. The system actively handles these cases, but they are not documented:
- **Pre-Lenten Sundays**: Publican & Pharisee, Prodigal Son, Meatfare, and Cheesefare.
- **Soul Saturdays**: Meatfare, and the 2nd, 3rd, and 4th Saturdays of Lent.
- **Lenten Sundays**: Orthodoxy, St. Gregory Palamas, Veneration of the Cross, St. John Climacus, St. Mary of Egypt.
- **Special Lenten Days**: Thursday of the Great Canon, Saturday of the Akathist.
- **Holy Week**: Lazarus Saturday, Palm Sunday, Holy Monday-Wednesday (Presanctified), Holy Thursday, Great and Holy Friday (Tomb Matins, Royal Hours), and Holy Saturday.

## 2. The Pentecostarion Moveable Cycle
The entire period from Pascha to All Saints is omitted from the implementation document, despite being fully mapped in the engine:
- **Pascha and Bright Week**: The complete suppression of the Octoechos and unique service structures.
- **Pentecostarion Sundays**: St. Thomas, Myrrh-bearing Women, Paralytic, Samaritan Woman, Blind Man, Fathers of the 1st Council, and All Saints.
- **Major Feasts**: Mid-Pentecost, Ascension, Pentecost, and Monday of the Holy Spirit.

## 3. Ruthenian Lviv Synod Specifics
The logic maps uniquely implement distinct Ruthenian feasts mandated by the Lviv Synod (which are part of the Dolnytsky Typikon Part IV), but these are missing from the documentation:
- **Feast of the Most Holy Eucharist (Corpus Christi)**: Triggered on the Thursday after Trinity Sunday (`pascha_offset: 60`).
- **Friday of the Co-suffering of the Most Holy Theotokos**: Triggered on the Friday after the leavetaking of the Feast of the Eucharist (`pascha_offset: 65`).

## 4. Collision and Concurrency Resolution Matrix
The document briefly mentions that collisions are evaluated against `02k_logic_collisions.json`, but fails to document the actual collision logic matrix. Significant gaps include:
- **Annunciation Collisions**: What happens when Annunciation falls on Pascha, Holy Friday, or a Lenten Weekday (e.g., overriding Presanctified with Vesperal Chrysostom).
- **St. George / Patronal Feasts**: Overrides when a major fixed feast falls during Bright Week.

## 5. Secondary Services & Components
The document focuses heavily on Great Vespers, Matins, and Liturgy. It omits:
- **Katavasia Seasonal Selection**: The logic in `02e_logic_katavasia.json` that determines which seasonal katavasia is sung (e.g., Cross, Nativity, Theotokos) is not documented.
- **Minor Services**: Small Vespers, Midnight Office variants, Litiya, and the Royal Hours (which have their own structural and logical files).
- **Temple/Patronal Math**: It mentions "Temple Priority" but lacks the explicit rules from `02d_logic_temple.json` regarding how a Patronal feast overrides standard Menaion logic or interacts with the Triodion.
