# Decision Log — Key Editorial & Technical Decisions

All major decisions made across the project's history, distilled from 25+ conversation sessions.

---

## ⚠️ Decision 0: There Is No "1899 Edition" (FOUNDATIONAL RULE)
**Date:** Established repeatedly; formalized May 2026  
**Context:** Multiple AI sessions have independently "discovered" that the English text looks different from what they expect, and concluded it was "translated from the 1899 edition." This has caused models to waste entire sessions rewriting sections, losing their place, and creating more problems than they solve.  
**Decision:** **The 2010 Lviv Ukrainian book is the only source. There is no "1899 edition" in our workflow.** If the English doesn't match the 2010 Ukrainian pages, fix it by translating the 2010 Ukrainian. Do not speculate about historical editions. Do not frame corrections as "removing 1899 artifacts." Just compare English to 2010 Ukrainian and fix mismatches.  
**Incident:** Conversation `3a3b4dfc` (April 25–26, 2026) — the model spent an entire session on Images 120–125 (Annunciation, March 25) "discovering 1899 text," rewriting Sections 4–11, and eventually getting lost at the "Key of the Boundaries" gap between March 26 and April 23.

---

## Decision 1: Book Title Policy — Proper Names Only
**Date:** April 25, 2026  
**Context:** System instructions mandated `Tserkovne Oko = Tserkovne Oko (Do not translate)`, but earlier editorial work had overridden this to "Eye of the Church" for readability.  
**Decision:** **Revert to "Tserkovne Oko"** as the canonical form. Extend the same principle to *Sluzhebnik* (not "Service Book").  
**Rationale:** Octoechos ≠ "Eight Tones"; Triodion ≠ "Three-Ode Book"; Horologion ≠ "Book of Hours." All liturgical book titles are proper names.  
**Impact:** 405 occurrences of "Tserkovne Oko" and 67 of "Sluzhebnik/Sluzhebnyky" unified across all 8 Final files.

---

## Decision 2: Publisher Misprint `^3` on Page 16
**Date:** April 24, 2026  
**Context:** The 2010 Ukrainian source has footnote sequence `24, 3, 25, 26, 27` on Page 16. The `^3` is a printing error by the 2010 publisher.  
**Decision:** Anchor as `[^3a]` to maintain unique markdown keys while preserving physical placement fidelity to the 2010 edition.  
**Rationale:** The translation must faithfully reflect the 2010 edition, including its printing anomalies, while maintaining valid markdown syntax.

---

## Decision 3: Footnote Syntax — Markdown Standard
**Date:** April 2026  
**Context:** Original translations used `^[N]` inline syntax. For MS Word / Pandoc import, the standard `[^N]` / `[^N]:` syntax is preferred.  
**Decision:** Convert all markers to `[^N]` inline and `[^N]: text` definitions at the bottom of each file.  
**Impact:** All 785 footnotes converted. Word will auto-generate native page footnotes from this syntax.

---

## Decision 4: Epitaphios vs. Shroud Coexistence
**Date:** April 2026  
**Context:** "Epitaphios" (Greek, 26 occurrences) and "Shroud" (English, 58 occurrences) both appear in the text.  
**Decision:** Both are permitted to coexist. "Epitaphios" is the Greek scholarly term for the liturgical object; "Shroud" is the English rubrical translation.  
**Rationale:** These are distinct concepts in scholarly usage, not terminological drift.

---

## Decision 5: Megalynaria vs. Magnification Coexistence
**Date:** April 2026  
**Context:** "Megalynaria" (Greek, 11 occurrences) and "Magnification" (English, 30 occurrences) both appear.  
**Decision:** Both permitted. "Megalynaria" is a distinct Greek scholarly term used in source-citation contexts.

---

## Decision 6: Prokimenon vs. Prokeimenon
**Date:** April 2026  
**Context:** Both spellings appeared in the translation.  
**Decision:** **Prokimenon** / **Prokimena** (pl.) is canonical. "Prokeimenon" is forbidden.  
**Rationale:** Follows the dominant Slavonic transliteration convention used in the UHKC tradition.

---

## Decision 7: Heirmos vs. Irmos
**Date:** April 2026  
**Context:** Both spellings appeared.  
**Decision:** **Heirmos** / **Heirmoi** (pl.) / **Heirmologion** (book) is canonical. "Irmos" / "Irmoi" / "Irmologion" forbidden.  
**Rationale:** Preserves the aspirated Greek etymon (εἱρμός).

---

## Decision 8: Pochaiv Transliteration
**Date:** April 2026  
**Context:** Three variants appeared: Pochayiv, Pochaev, Pochaiv.  
**Decision:** **Pochaiv** is canonical. 274 total occurrences unified.  
**Rationale:** Standard Ukrainian romanization (no medial -y- or Russian -ev).

---

## Decision 9: Processing Pipeline — Hybrid Approach
**Date:** April 2026  
**Context:** Programmatic stitching of footnote markers from RAW translations achieved 82% success (796/969). 173 markers failed, especially in Part 5 (58% success) due to heavy text reformatting.  
**Decision:** Use a **hybrid approach**: improved script for quote normalization + AI-driven manual placement for remaining failures.  
**Impact:** All 969 markers successfully placed. Zero missing footnotes in Final files.

---

## Decision 10: Visual Audit Scope
**Date:** April 2026  
**Context:** The "visual rubrical audit" was initially understood as a full translation accuracy check.  
**Decision:** Clarified scope: The audit is specifically a **footnote-placement verification** — not a translation accuracy audit. A true translation accuracy audit would require a Ukrainian-literate reviewer.  
**Status:** Ongoing. ~51% complete (Images 001–146; Part 3 Menaion 100% complete).

---

## Decision 11: Hieratic Pronoun Application
**Date:** April 2026  
**Context:** System instructions require Thee/Thou/Thy for divine address.  
**Decision:** Applied via automated scripts. Completeness audit pending (edge cases possible).  
**Status:** Enforced but not fully verified.

---

## Decision 12: Foreign-Language Footnote Citations
**Date:** April 2026  
**Context:** Footnotes contain extensive Greek, Latin, and Church Slavonic citations.  
**Decision:** Preserve all foreign-language citations **as-is** in their original script for historical fidelity (philological standard). Only the Ukrainian commentary is translated.

---

## Decision 13: Calendar Service-Rank Tags
**Date:** 2026  
**Context:** Part 5 Menologion needed a machine-readable tagging system for feast ranks.  
**Decision:** Standardized tags: `[LORD]`, `[MOG]`, `[VIGIL]`, `[POL]`, `[GT DOX]`, `[6 SM]`, `[4 A+G]`, `[4 TR]`, `[4 NO]`.  
**Impact:** Used by the Typikon Coded engine for automated digest generation.

---

## Decision 14: Matrix Error Remediation & Footnote Architecture
**Date:** May 2026  
**Context:** Auditing models previously fell into a "Ghost Loop" where hallucinated entries desynchronized physical image tracking after Image 124. Simultaneously, inline text expansion and duplicate footnote accumulation created trailing structural bloat.  
**Decision:** Mandated the absolute truncation of fabricated logs to restore pure physical tracking. Established the architectural standard that inline file footnote markers are managed directly within the primary text files, while `Final_footnotes.txt` serves as the centralized master compilation. Extraneous appended footnote blocks are strictly purged to restore natural part boundaries.  
**Impact:** Concluded Part 3 Menaion with pristine 1-to-1 physical mapping through Image 146. Embedded all tracking state natively into repository `_brain/` directory.
