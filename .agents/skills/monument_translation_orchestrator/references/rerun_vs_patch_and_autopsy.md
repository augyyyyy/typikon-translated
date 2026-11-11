# Breakthrough Invalidation, Re-Run vs. Patch Decision Matrix & Process Autopsy (`Rule 18`)

## 1. Objective 4-Criterion Decision Matrix (`Rule 18`)
When a developmental breakthrough or systemic defect is discovered (e.g., new vision capabilities, glossary overhauls, discoverable leaf caches, or structural engine upgrades), evaluate whether to apply a targeted **In-Place Patch** or execute a **Complete Automated Re-Run**:

| Criterion | In-Place Patch Path | Complete Automated Re-Run Path |
| :--- | :--- | :--- |
| **1. Epigraphic Integrity** | Physical leaf images and raw transcriptions in `Source Text/` are 100% intact and complete (`0%` missing leaves). | Missing leaves discovered, misordered folios, corrupt OCR layers, or epigraphic omissions (`> 5%`). |
| **2. Deterministic Solvability** | Defect is isolatable via deterministic Python AST, regex, or glossary mapper (e.g., 1-to-1 terminology replacement, footnote numbering shift, leaf banner normalization). | Defect requires holistic semantic or syntactic re-translation across multiple paragraphs from the physical page scans. |
| **3. Defect Scope** | Defect affects `<= 5%` of paragraphs or leaves across the monument. | Defect affects `> 20%` of paragraphs/leaves or alters fundamental document structure. |
| **4. Lifecycle Phase** | Intermediate draft phase or minor post-assembly errata. | Pre-assembly raw draft or systematic breakthrough rendering existing drafts obsolete. |

## 2. Mandatory Pre-Rerun Archiving & Delta Audit Protocol
1. **Timestamped Pre-Rerun Archive**:
   - Before triggering any complete re-run of a cohort or monument, existing cohort markdown, source text, and footnote files MUST be archived into a timestamped directory:
     `<workspace>/archive/pre_rerun_YYYYMMDD_HHMMSS/`
   - Note: `verify_ecosystem_integrity.py` automatically excludes `archive/` and `pre_rerun_*` directories from active AST scans.
2. **Post-Rerun Programmatic Delta Audit**:
   - After the re-run completes, execute a programmatic Delta Audit comparing the new output against `archive/pre_rerun_YYYYMMDD_HHMMSS/` to verify that zero prior human corrections, verified glosses, or footnote citations were lost.

## 3. Forensic Process Autopsy (`PA-NNN`) & Trajectory Auditing (`Vectors 5C, 7, 11, 12`)
- `scripts/audit_transcript_trajectory.py` programmatically audits subagent execution trajectories and builds `Audit_Reports/process_autopsy_report.json`:
  - **Vector 5C (`audit_source_orthographic_authenticity`)**: Detects and heals synthetic Church Slavonic orthographic hypercorrections (e.g., fake `Ѿ` / `ѿ` substitutions in `Слава Отцю` or `отцевъ`).
  - **Vector 11 (`audit_cohort_subagent_trajectory`)**: Verifies from `.system_generated/logs/transcript.jsonl` that the worker subagent inspected 100% of assigned `Page_{p:04d}.jpg` leaves via `read_file`/`view_file` (`unviewed_leaves == []`) and made zero `search_web` calls (`contaminated_leaves == []`).
  - **Vector 12 (`build_monument_process_autopsy`)**: Computes the monument's Epigraphic Fidelity Score (`phi_score`, requiring `100.0` for Grand Pause sealing).
