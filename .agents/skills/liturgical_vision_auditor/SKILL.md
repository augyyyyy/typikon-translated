---
name: liturgical_vision_auditor
description: Audits English liturgical translations against 300 DPI page-scan images using Native Gemini Vision, enforcing leaf conservation, H1/H2 heading discipline, cinnabar rubric italics, table layout, and 1:1 footnote bijectivity.
---

# Liturgical Vision Auditor Skill Guidelines

When executing a visual page-scan audit against 300 DPI rasters (`Page_{p:04d}.jpg` in `Source Text/images/`):

## 1. Epigraphic & Visual Audit Integrity (`Rule 1`, `Rule 6`, `Rule 16`)
* Inspect physical 300 DPI page scans directly via `view_file`/`read_file`. Never infer missing entries, interpolate unwritten elements, or fabricate bounding-box coordinates.
* All image paths must resolve dynamically via `pathlib.Path` relative to the project root or the monument's NTFS junction (`Liturgical Monuments/<Monument>/Source Text/images/`).
* Run automated structural and chromatic verifiers alongside visual inspection:
  * `py scripts/structural_audit.py --monument <ID> --cohort <K>` — Verifies `=== LEAF pN ===` monotonic continuity and `SGC-02` density.
  * `py scripts/chromatic_rubric_verifier.py` — Verifies red cinnabar rubrics are rendered in italics (`*...*`) and black ink in Roman.
  * `py scripts/verify_publication_edition.py --monument <ID>` — Runs the 6-Gate Liturgical Canonical Publication Edition (LCPE) audit.

## 2. Footnote Placement & Monotonic Bijectivity (`Rule 4` & Mandate 7)
* Visually match footnote markers (`[^N]`) in `Draft/` or `Final/` against marginal glosses, scriptural citations, or recensional apparatus on the physical page scan.
* Never attach a footnote marker `[^N]` directly to a `=== LEAF pN ===` banner or a `**[Left/Right Page — Fol. Xr]**` 2-up spread milestone; always attach `[^N]` to a surviving heading or body line so LCPE milestone stripping never orphans `[^N]`.
* Verify 1:1 bidirectional symmetry between body markers `[^N]` and definitions `[^N]:` in `Final_footnotes.txt` via `scripts/reconcile_footnotes.py`.

## 3. Epigraphic Typography & Heading Hierarchy (Mandates 8, 10, 12)
* **`H1 & H2` Only**: Reserve `#` for `publication_spec` Part landmarks and `##` for primary day/service headpieces; render sub-services, offices, canons, odes, heirmoi, troparia, and rubrics as inline italics (`*...*`), never `###` or `####`.
* **Tables, Vacat Folios & Parenthetical Cyrillic**: Preserve multi-column Paschalion and Menologion tables as Markdown tables; format blank leaves as `*(Vacat — Fol. Xv: Unnumbered blank verso)*`; parenthesize all inline Cyrillic witnesses `(*...*)` (never square-bracketed `[...]`).

## 4. On-Demand Reference Playbooks
* [`references/footnote_bijectivity_and_layout.md`](references/footnote_bijectivity_and_layout.md) — Footnote reconciliation rules, 2-up spread milestone handling, and chromatic/table layout verification.
* [`references/sgc_potemkin_and_publication_gates.md`](references/sgc_potemkin_and_publication_gates.md) — `PE-HSG-01`..`05` Anti-Potemkin invariants, 6-Gate `verify_publication_edition.py` specifications, and 4-shard `Shared_Lexicon` read-only consumption.
