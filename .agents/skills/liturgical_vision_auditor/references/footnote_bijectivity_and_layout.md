# Footnote Monotonic Bijectivity, 2-Up Spreads & Visual Layout Verification

## 1. Footnote Bijectivity Invariant (`Rule 4` & `scripts/reconcile_footnotes.py`)
1. **Strict 1:1 Bijection**:
   - Every footnote marker `[^N]` appearing in a cohort draft or canonical Part file (`Final/<monument>_partK_*.md`) MUST have a unique corresponding `[^N]:` definition in `Final_footnotes.txt` (or `<monument>_cohortK_footnotes.md`), and every `[^N]:` definition must be referenced at least once in the body text.
   - Audit via:
     ```powershell
     py scripts/reconcile_footnotes.py --body "<path/to/body.md>" --footnotes "<path/to/footnotes.txt>"
     ```
2. **Ban on Inlined Body Definitions (`PE-HSG-05`)**:
   - Footnote definitions (`[^N]: ...`) and leaked `### Notes` sections must never appear inside body prose files. During Phase 1, `attempt_deterministic_self_healing()` automatically extracts accidentally inlined `[^N]:` definitions into the cohort footnotes file.
3. **Prohibition of Milestone-Attached Markers (Mandate 7)**:
   - During Phase 2 LCPE compilation (`scripts/compile_final_edition.py`), internal scaffolding banners (`=== LEAF pN ===`) and 2-up spread milestones (`**[Left Page — Fol. Xv]**`, `**[Right Page — Fol. Yr]**`) are stripped or transformed into clean folio headers.
   - Attaching `[^N]` directly to a `=== LEAF pN ===` or `**[Left/Right Page — ...]**` line causes the marker to be stripped during compilation, breaking Gate 3 (`reconcile_footnotes.py`). Always attach `[^N]` to the first actual heading or text paragraph on that page.

---

## 2. Visual Layout, Cinnabar Rubrics & Multi-Column Tables
1. **Cinnabar Rubrical Segregation (`scripts/chromatic_rubric_verifier.py`)**:
   - Historical Church Slavonic codices print ceremonial instructions, tone headers, liturgical role tags, and calendar metadata in red cinnabar ink (*кіновар*), and chanted/spoken prayers in black ink.
   - Render all red cinnabar rubrics in inline italics (`*...*`), speaker labels in bold (`**Priest:**`, `**Deacon:**`, `**Choir:**`, `**Reader:**`), and chanted/spoken text in Roman.
2. **Paschalion, Lunar & Menologion Tables**:
   - Render multi-column tables (Indiction, Solar Circle, Lunar Circle, Key of Boundaries, Foundation, Golden Number) as valid GFM Markdown tables (`| Col 1 | Col 2 | ... |`).
   - Render Slavonic Cyrillic numerals in table cells with Arabic numerals followed by parenthetical italicized Cyrillic witnesses, e.g., `1 (*а̃*)`, `15 (*єІ̃*)` — never in square brackets `[а̃]`, which Gate 1 flags as untranslated Cyrillic in body text.
   - Any leaf containing `>= 5` table rows or `>= 5` footnotes (`>= 8` / `>= 10` on 2-up spreads) is automatically queued into `Audit_Reports/argon_review_queue.json` (Signal 3) for Phase 2 `Argon (High)` visual verification.
