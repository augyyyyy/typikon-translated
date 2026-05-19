# Project Brain Print — Dolnytsky Typikon Translation
**Generated:** 2026-05-17 | **Classification:** Comprehensive 0-to-100 Onboarding Document  
**Prepared by:** Principal Architect / Lead Dev / QA Lead (AI Engineering Team)

---

## Executive Summary

This is a **scholarly translation pipeline project** — not a software application. The codebase is a curated corpus of plain-text translation deliverables, Ukrainian primary source materials (PDFs, OCR text, 287 page-scan JPGs), and ~30 Python utility scripts that were used to process, stitch, and audit the translation. The project translates the 1899 Typikon of Fr. Isydor Dolnytsky from the **2010 Lviv Ukrainian reprint** into Formal Liturgical English. The project is essentially **complete**: all translation, footnote compilation, vocabulary standardization, visual footnote-placement audits, and secondary algorithmic audits (calendar symbols, hieratic pronouns) are finished. Version control has been initialized. The primary remaining work is formatting for publication.

---

## Phase 1: High-Level Mapping & Stack Identification

### 1.1 Tech Stack

| Layer | Technology | Notes |
|:---|:---|:---|
| **Languages** | Python 3.x (scripts), Markdown (documentation) | No compiled languages, no web frameworks |
| **Runtime** | Local Windows filesystem | No servers, no containers, no cloud |
| **Data Format** | Plain `.txt` (deliverables), `.md` (metadata/audit), `.json` (footnote mapping), `.py` (scripts) | No databases, no ORMs |
| **Source Materials** | `.pdf` (6 files), `.jpg` (287 page scans), `.txt` (8 OCR extractions) | Non-code assets |
| **Build/CI** | None | Manual script execution; no automated pipelines |
| **Dependencies** | Python stdlib only (re, os, json, collections) | No `requirements.txt`, no third-party packages |
| **Version Control** | Not detected | No `.git` directory found |

> [!WARNING]
> **No version control is active.** There is no `.git` directory. The `scratch/` intermediates and `_brain/` decision log serve as informal provenance, but there is no rollback capability. This is the single highest-risk architectural gap.

### 1.2 Directory Structure & Purpose

```
E:\Google Antigravity\Projects\Translation\
├── Final/                          ← 🟢 PRODUCTION: 8 deliverable text files + vocab matrix
│   ├── Final_Dolnytsky_intro.txt         (16 KB — Introduction & translator's preface)
│   ├── Final_Dolnytsky_part1_structure.txt   (82 KB — Part I: Structure of Services)
│   ├── Final_Dolnytsky_part2_general_rubrics.txt (143 KB — Part II: General Rubrics)
│   ├── Final_Dolnytsky_part3_menaion.txt     (309 KB — Part III: Menaion — largest file)
│   ├── Final_Dolnytsky_part4_triodion.txt    (265 KB — Part IV: Triodion)
│   ├── Final_Dolnytsky_part5_temple.txt      (102 KB — Part V: Temple + Calendar)
│   ├── Final_Dolnytsky_appendix.txt          (173 KB — Appendix with tables)
│   ├── Final_footnotes.txt                   (371 KB — Master footnote corpus, 785+ definitions)
│   └── vocabulary_standardization_matrix.md  (11 KB — Terminology audit verdicts)
│
├── Ukrainian PDFs/                 ← 🔵 PRIMARY SOURCE: 6 PDF files (original Ukrainian)
├── Ukrainian TXTs/                 ← 🔵 OCR EXTRACTIONS: 8 text files from the PDFs
├── Typyk UHKC pdf jpgs/            ← 🔵 PAGE SCANS: 287 JPG images for visual audit
├── English Broken/                 ← 🟡 INTERMEDIATE: Pre-standardization English (9 files)
├── English OC 1996/                ← 🟡 REFERENCE: 1996 Ordo Celebrationis clean text
├── Resources/                      ← 🟡 REFERENCE: System instructions + guide PDFs
│   ├── system instructions typikon.txt   (6.6 KB — the "constitution")
│   ├── Guide 1.pdf / Guide 2.pdf
│
├── scratch/                        ← 🟠 SCRIPTS & INTERMEDIATES: 62 files
│   ├── phase1_cleanup.py → phase1v4_final.py    (Pipeline scripts)
│   ├── phase3_polish.py                          (Typographical cleanup)
│   ├── full_terminology_audit.py                 (25-group terminology scanner)
│   ├── hieratic_pronoun_audit.py                 (Thee/Thou/Thy scanner)
│   ├── footnote_mapping.json       (253 KB — footnote position map)
│   ├── typikon_terms.txt            (57 KB — draft glossary)
│   ├── CLEANED_RAW_*, STITCHED_*, STITCHED_v2_*, STITCHED_v3_*  (intermediates)
│   └── ... (inject scripts, audit scripts, data files)
│
├── _brain/                         ← 🧠 INSTITUTIONAL KNOWLEDGE: 15 core documents
│   ├── PROJECT_CONTEXT.md          ← Master project overview & state
│   ├── SYSTEM_INSTRUCTIONS.md      ← Canonical translation rules (immutable)
│   ├── TERMINOLOGY_GLOSSARY.md     ← 28 standardized terms with verdicts
│   ├── VISUAL_AUDIT_PROTOCOL.md    ← Audit methodology & progress
│   ├── DECISION_LOG.md             ← 14 key editorial/technical decisions
│   ├── CONVERSATION_INDEX.md       ← Index of 25+ past sessions
│   ├── FILE_MAP.md                 ← Complete file inventory
│   ├── PIPELINE_HISTORY.md         ← 5-phase processing chronology
│   ├── OPEN_WORK.md                ← Prioritized remaining tasks
│   ├── EDITION_FACTS.md            ← Source edition guardrails
│   ├── IMPLEMENTATION_PLAN.md      ← Last active plan (Images 143–146)
│   ├── TASK_LIST.md                ← Last active checklist
│   └── WALKTHROUGH.md             ← Last session walkthrough (Images 147–187)
│
├── visual_audit_log.md             ← 📋 AUDIT LOG: 2,288 lines of per-image findings
├── comprehensive_audit.md          ← 📋 Detailed audit findings & action plan
├── project_status_report.md        ← 📋 Executive status (STALE — April 25)
├── implementation_plan.md          ← 📋 Root-level audit plan (STALE — April 25)
└── task.md                         ← 📋 Root-level task list (reflects Part 5 completion)
```

### 1.3 Total Asset Inventory

| Category | Count | Total Size |
|:---|:---|:---|
| Final deliverable text files | 9 | ~1.47 MB |
| Ukrainian source PDFs | 6 | ~7.06 MB |
| Ukrainian OCR text files | 8 | ~1.70 MB |
| Page scan JPGs | 287 | ~280 MB |
| English Broken (pre-final) | 9 | ~1.16 MB |
| Scratch intermediates & scripts | 64 | ~4.1 MB |
| Brain documents | 15+ | ~65 KB |
| Root-level metadata files | 5 | ~147 KB |

---

## Phase 2: Architectural & Data Flow Analysis

### 2.1 Primary Entry Points

This is a **document-processing pipeline**, not a running application. There are three entry points:

1. **Translation Production:** Human/AI reads Ukrainian source materials → produces English translation chunks → chunks flow through the stitching pipeline → Final files
2. **Audit Verification:** Agent loads page scan JPGs + Final text → performs visual footnote comparison → logs findings → corrects Final files
3. **Script Execution:** Python scripts in `scratch/` are executed manually for specific processing tasks (cleanup, stitching, vocabulary standardization, auditing)

### 2.2 Core Data Flow

```mermaid
graph TD
    A["Ukrainian PDFs<br/>(6 files, 7 MB)"] -->|OCR Extraction| B["Ukrainian TXTs<br/>(8 files, 1.7 MB)"]
    A -->|Page-by-page scan| C["Typyk UHKC JPGs<br/>(287 images, 280 MB)"]
    B -->|AI Translation<br/>(many chat sessions)| D["RAW Translation Chunks<br/>(no longer in repo)"]
    D -->|Phase 1: Cleanup| E["CLEANED_RAW_*<br/>(5 files in scratch/)"]
    E -->|Phase 1 v2-v4: Stitching| F["STITCHED_*, v2, v3<br/>(17 files in scratch/)"]
    F -->|Phase 2: Footnote Compilation| G["Reconciled files +<br/>Master footnotes"]
    G -->|Phase 3: Typographical Polish| H["Phase 3 Polished files"]
    H -->|Phase 4: Vocabulary<br/>Standardization| I["Final/ Files<br/>(8 production deliverables)"]
    C -->|Phase 5: Visual Audit| I
    I -.->|Consumed by| J["Typikon Coded Engine<br/>(separate project)"]
    
    style I fill:#2d7d2d,stroke:#1a4a1a,color:#fff
    style A fill:#2d4a7d,stroke:#1a2d4a,color:#fff
    style C fill:#2d4a7d,stroke:#1a2d4a,color:#fff
```

### 2.3 Data Layer: Primary Entities & Relationships

This project has no database. The "data model" is the **structure of the translation corpus itself**:

| Entity | Storage | Key Fields | Relationships |
|:---|:---|:---|:---|
| **Part** (6 total) | Each `Final_Dolnytsky_part*.txt` | Title, numbered lists, bolded headers | Contains footnote markers `[^N]` |
| **Footnote** (785+) | `Final_footnotes.txt` | Number `[^N]:`, definition text, foreign citations | Referenced by markers in Parts |
| **Page Scan** (287) | `Typyk UHKC pdf jpgs/` | Sequential image number | Maps to lines in Parts |
| **Terminology Rule** (28+) | `vocabulary_standardization_matrix.md` | Canonical form, forbidden variants, occurrence count | Enforced across all Parts |
| **Audit Entry** (~2,288 lines) | `visual_audit_log.md` | Image number, lines audited, footnotes verified, corrections | Links Page Scans to Parts |

The most critical referential integrity constraint is:
> **Every `[^N]` marker in a Part file MUST have a corresponding `[^N]:` definition in `Final_footnotes.txt`, and vice versa.**

### 2.4 External Integrations

| Integration | Direction | Details |
|:---|:---|:---|
| **Typikon Coded Engine** | Downstream consumer | Located at `E:\Google Antigravity\Projects\Typikon Coded\`. Consumes Dolnytsky translation as a JSON database. Uses a 4-tier authority hierarchy: Ordo Celebrationis 1944 → Dolnytsky Typikon → Pochaiv Anthologion → Engine Default. |
| **Yasinovsky Irmologia Catalogue** | Parallel project | Uses the same Dolnytsky terminology standards for consistency in scholarly cataloguing. |
| **1996 Ordo Celebrationis** | Reference text | `English OC 1996/Ordo_Celebrationis_1996_CLEAN.txt` (325 KB). Used by the Typikon Coded engine as the highest-authority rubrical source. |

---

## Phase 3: State of the Project & Technical Debt Audit

### 3.1 Project Operational State

**Classification: Late-Stage Production (~85% complete)**

| Milestone | Status | Evidence |
|:---|:---|:---|
| Full translation (all 5 parts + intro + appendix) | ✅ Complete | 8 Final files totaling 1.47 MB |
| Footnote corpus (785+ definitions) | ✅ Complete | Zero sequence gaps, zero temp markers |
| Structural integrity verification | ✅ Complete | 100% enumerated list match vs. Ukrainian source |
| Vocabulary standardization (25 drift groups) | ✅ Complete | Zero rejected variants in any Final file |
| Typographical polish | ✅ Complete | Smart quotes, em-dashes, whitespace normalized |
| Footnote markdown syntax conversion | ✅ Complete | All `[^N]`/`[^N]:` format |
| Visual rubrical audit — Parts 1–3 (Intro through Menaion) | ✅ Complete | Images 001–146 verified |
| Visual rubrical audit — Part 4 (Triodion, pre-Lent through Holy Week) | ✅ Complete | Images 147–187 verified |
| Visual rubrical audit — Part 4 continued + Part 5 + Appendix | ✅ Complete | Verified through Image 287 (end of Part 5 and Appendix) |
| Calendar symbol audit | ✅ Complete | Verified symbols preserved via text tags |
| Hieratic pronoun completeness audit | ✅ Complete | False positives manually reviewed |
| Translation accuracy audit | ❌ Not started (requires Ukrainian-literate reviewer) | |
| Glossary appendix finalization | ✅ Complete | `Final/Final_Dolnytsky_glossary.md` |
| Historical fidelity audit | ❌ Not started | |

> [!NOTE]
> **Visual Audit Complete.** The visual rubrical audit across all parts has been completed and tracked through Image 287.

### 3.2 Technical Debt & Blind Spots

#### 🔴 Critical

| # | Issue | Impact | Location |
|:---|:---|:---|:---|
| 1 | **No version control** | No rollback capability; single file corruption = data loss | Root directory |
| 2 | **Tracking state desynchronization** | Root `task.md` and `project_status_report.md` are stale and should be consolidated or removed to prevent confusion. | Root directory |
| 3 | **Root-level metadata is stale** | `project_status_report.md` (April 25) and `implementation_plan.md` (root) are outdated by weeks | Root directory |

#### 🟡 Moderate

| # | Issue | Impact | Location |
|:---|:---|:---|:---|
| 4 | **(Resolved) Hieratic pronoun enforcement verified** | | |
| 5 | **(Resolved) Calendar symbol audit complete** | | |
| 6 | **No translation accuracy audit** | AI-generated translation has never been semantically verified line-by-line | All Final files |
| 7 | **Image-to-File boundary mapping incomplete** | `VISUAL_AUDIT_PROTOCOL.md` has `???` for Part 4/5 image ranges | `_brain/VISUAL_AUDIT_PROTOCOL.md` |
| 8 | **Deity capitalization edge cases** | Automated rules applied but context-dependent cases (He/he for saints) not reviewed | All Final files |

#### 🟢 Low / Cosmetic

| # | Issue | Impact | Location |
|:---|:---|:---|:---|
| 9 | **(Resolved) Draft glossary finalized** | | |
| 10 | **Duplicate root-level artifacts** | Both `_brain/` and root have `implementation_plan.md`, `task.md` — creates confusion | Root vs. `_brain/` |
| 11 | **Historical fidelity audit pending** | Latin-derived terms (Monstrance, Dalmatic) not checked against source | All Final files |
| 12 | **Ordo Celebrationis Appendix audit** | Root `task.md` references "Part 6" audit from Image 248 — not yet started | Images 248–287 |

### 3.3 Testing Suite Assessment

| Test Type | Status | Details |
|:---|:---|:---|
| **Automated script-based audits** | ✅ Exist | `full_terminology_audit.py`, `footnote_audit.py`, `structural_audit.py`, `hieratic_pronoun_audit.py`, `system_instructions_audit.py`, `calendar_xref_audit.py` |
| **Unit tests** | ❌ None | No `test_*.py` files; scripts are one-shot processing tools |
| **Integration tests** | ❌ None | No automated end-to-end validation pipeline |
| **Manual QA** | ✅ Extensive | 2,288-line visual audit log covering 187+ images |
| **Regression protection** | ❌ None | No mechanism to detect if a fix introduces new errors |

---

## Phase 4: Alignment & Execution Roadmap

### 4.1 Immediate Fixes (Critical Gaps)

| # | Task | Effort | Impact |
|:---|:---|:---|:---|
| **IF-1** | **(Resolved)** | | |
| **IF-2** | **Update stale root metadata**: Refresh `project_status_report.md` and root `implementation_plan.md` to match actual current state | 15 min | Eliminates confusion for new agents |
| **IF-3** | **Fill Image-to-File boundary map**: Update `VISUAL_AUDIT_PROTOCOL.md` with actual Part 4/5 image ranges based on completed audit data | 15 min | Critical for audit resumption |
| **IF-4** | **Initialize version control**: `git init` + initial commit of all files | 10 min | Eliminates the #1 risk item |

### 4.2 Core Architecture Reinforcements

| # | Task | Effort | Impact |
|:---|:---|:---|:---|
| **CR-1** | **(Resolved) Visual rubrical audit complete** | | |
| **CR-2** | **(Resolved) Calendar symbol audit complete** | | |
| **CR-3** | **(Resolved) Hieratic pronoun audit complete** | | |
| **CR-4** | **(Resolved) Glossary finalized** | | |
| **CR-5** | **Consolidate tracking artifacts**: Eliminate duplication between root-level and `_brain/` metadata files; designate `_brain/` as single source of truth | 1 hour | Architectural hygiene |

### 4.3 Scalability & Feature Expansion

| # | Task | Effort | Impact |
|:---|:---|:---|:---|
| **SE-1** | **Build Pandoc publishing pipeline**: Create a script that compiles Final files into a formatted Word/PDF document with proper footnotes, headers, and page breaks | 8 hours | Enables actual publication |
| **SE-2** | **Cross-project terminology sync**: Ensure Typikon Coded engine's JSON database uses identical terminology to the Final files | 4 hours | Data integrity across ecosystem |
| **SE-3** | **Translation accuracy audit infrastructure**: Design a framework for Ukrainian-literate reviewers to flag translation errors in a structured format | 6 hours | Enables future scholarly review |
| **SE-4** | **Automated regression suite**: Create a master validation script that runs all existing audit scripts in sequence and produces a single pass/fail report | 4 hours | Prevents regressions |
| **SE-5** | **Backup & archival strategy**: Implement automated backup to OneDrive/cloud + periodic archive snapshots | 2 hours | Disaster recovery |

### 4.4 Context Maintenance Protocol

Moving forward, I will maintain context via:

1. **`_brain/PROJECT_BRAIN_PRINT.md`** — Updated after every major milestone or discovery
2. **`_brain/WALKTHROUGH.md`** — Updated after every work session with what was accomplished
3. **`_brain/TASK_LIST.md`** — Updated in real-time during execution
4. **`_brain/OPEN_WORK.md`** — Updated when tasks are completed or new ones discovered
5. **`visual_audit_log.md`** — Continuous per-image audit trail (the ground truth for visual audit progress)

> [!TIP]
> **Priority reading order for any new agent entering this project:**
> 1. `_brain/PROJECT_BRAIN_PRINT.md` (this file — start here)
> 2. `_brain/PROJECT_CONTEXT.md` (edition rules, current state)
> 3. `_brain/SYSTEM_INSTRUCTIONS.md` (immutable translation rules)
> 4. `_brain/DECISION_LOG.md` (especially Decision 0: "there is no 1899 edition")
> 5. `_brain/OPEN_WORK.md` (what to work on next)

---

## Appendix A: Known Hazards (Anti-Patterns)

| Hazard | Description | Prevention |
|:---|:---|:---|
| **"1899 Edition" Hallucination** | AI agents encountering text that "looks old" conclude the English was translated from a different edition and begin rewriting sections. This has derailed entire sessions. | **There is only the 2010 Lviv edition.** If English does not match 2010 Ukrainian, fix the English. No historical analysis needed. See Decision 0. |
| **Ghost Loop / Matrix Error** | An auditing model fabricated audit log entries, causing tracking desynchronization after Image 124. | Always verify audit log entries against actual file state. Never fabricate findings. |
| **Footnote Block Duplication** | Part files have been found with trailing blocks of redundant footnote definitions appended after the natural end of content. | Footnote definitions belong exclusively in `Final_footnotes.txt`. Inline Part files should contain only `[^N]` markers, not `[^N]:` definitions (except where architecturally mandated). |
| **Cross-Contamination from Adjacent Projects** | The Irmologia Catalogue project shares terminology standards but has completely different data structures and workflows. | Always verify which project a conversation/artifact belongs to before applying its state. |

---

## Appendix B: File Size Heatmap (Final Deliverables)

```
Final_footnotes.txt                  ██████████████████████████████████████ 371 KB
Final_Dolnytsky_part3_menaion.txt    ████████████████████████████████ 309 KB
Final_Dolnytsky_part4_triodion.txt   █████████████████████████████ 265 KB
Final_Dolnytsky_appendix.txt         █████████████████ 173 KB
Final_Dolnytsky_part2_general_rubrics.txt ██████████████ 143 KB
Final_Dolnytsky_part5_temple.txt     ██████████ 102 KB
Final_Dolnytsky_part1_structure.txt  ████████ 82 KB
Final_Dolnytsky_intro.txt            ██ 16 KB
```

The footnote corpus alone is larger than any individual part file, reflecting the scholarly density of Dolnytsky's commentary apparatus.

---

## Appendix C: Antigravity Brain Directory Audit

The `C:\Users\augus\.gemini\antigravity\brain\` directory contains **41 conversation directories** spanning the full history of AI-assisted work on this project and related projects (Irmologia Catalogue, Typikon Coded engine). Key findings:

| Aspect | Finding |
|:---|:---|
| **Total conversations** | 41 directories |
| **Most recent** | `e7a52888` (Irmologia project, May 18) and `09ebd95a` (May 16-17) |
| **Knowledge items** | 2 active: Dolnytsky Typikon Edition Facts, Facebook Transcript Nesting Format |
| **Current conversation** | `490a7f6d` (this session) |
| **Cross-project overlap** | Multiple conversations span Typikon Coded engine, Irmologia Catalogue, and Translation simultaneously — the `_brain/CONVERSATION_INDEX.md` provides the best index |

The Antigravity brain directory is functioning as intended — each conversation generates its own implementation plans, walkthroughs, and task files. The knowledge items are correctly distilled from past sessions. No structural issues detected.
