# 41-Monument Engine-Parity & Redo Stratification Report

- **Generated At**: `2026-11-10T23:45:00Z`
- **Governing Standards**: `.agents/AGENTS.md` (Rules 1–22), `../GLOBAL_SYSTEM_RULES.md` (§7 & §8 `SGC-01`..`SGC-06`), `../Shared_Lexicon/MASTER_TRANSLATION_STANDARD.md` (`MTS-1`)
- **Total Registered Monuments Evaluated**: `41` (`17,054` physical facsimile leaves)
  - **Sealed `completed` Monuments**: `40` (`15,964` physical leaves, `1,543` canonical cohorts across `39` cohort-based monuments + `7` Parts in `2010_lviv_typikon`, `52,136` bijective footnotes, `183,087` atomic units across `40` `*_atomic_corpus.json` files and `33` `*_propers_corpus.json` files)
  - **Rule 18 Pre-Rerun Archived & Phase-0-Locked `paused` Monument**: `1` (`1895_dmitrievsky_vol1`, `1,090` physical leaves)

---

## 1. Executive Summary of Toolchain, Registry & Adversarial Review Upgrades (Wave 0)

1. **Rule 22 (`SGC-06` *Tabula Rasa*) Digest & Primitives Registry Remediation**:
   - Normalized `PRIM.VERSE.PS92_1B` (`has established`), `PRIM.VERSE.PS92_5` (`befits Thy house`), `HEIRMOS.T4.ODE5` (`saith` $\rightarrow$ `says`), `HEIRMOS.T4/T5/T6/T7.ODE9` (`Birthgiver`, lowercase Marian pronouns), and `PRIM.TROPARION.REJOICE_VIRGIN` (`"Fruit of thy womb"`) in `data/liturgical_primitives_registry.json` and `data/byzantine_automela_concordance.json`.
   - Upgraded `generate_father_paul_digest()` in `scripts/hymnographic_gold_normalizer.py` to enforce zero `0 leaves` / `[Not attested in monument]` ghost rows, zero `| Byzantine Greek |` columns in internal Sections 1–3, runtime `assert len(loci_list) > 0`, and Section 4 comparative quarantine across all 6 Octoechos `*_primitives_review.md` digests (automatically regenerated in Step 10.6 of `scripts/compile_final_edition.py` for 1-up Octoechoi including `1895_lviv_octoechos`).
   - Extended `RE_PAGE_HEADER` and `RE_COLUMN_HEADER` in `scripts/hymnographic_gold_normalizer.py` to rescue `[^N]` footnote citations placed inside or outside bold folio wrappers (e.g., `**[Right Page — Folio 137r][^213]**` in `1630_lviv_octoechos`).
2. **Compiler, Structural Auditor, & Pronoun Gate Parity (`scripts/compile_final_edition.py`, `scripts/verify_publication_edition.py`, `scripts/structural_audit.py`, `scripts/hieratic_pronoun_audit.py`)**:
   - Unified `slugify()` across compiler and Gate 3 auditor to preserve Greek (`\u0370-\u03FF\u1F00-\u1FFF`) and accented Latin (`\w`) while stripping `<a id="...">` tags, `[^N]` citations, and parenthetical Cyrillic; added `_deduplicate_html_anchors()` (`0` duplicate `<a id>` tags across all 40 monuments).
   - Updated `_build_part_slug_map()` and `extract_headings_and_anchors()` to index `<a id="...">` anchors on Mandate 8 inline bold rubric headers (`**<Title>** <a id="..."></a>`), and scoped `part0` master-title anchor deduplication strictly to the opening `#` H1 line.
   - Upgraded `heal_mixed_script_homoglyphs()` to full 3-script homoglyph healing (`_SLAV_STRICT_RE` / `_CYR_EXCLUSIVE_RE` / `_GRK_DISTINCT_RE` / `_LAT_TO_GRK_MAP`, running across cohorts, footnotes, and 2-up stitched bodies), eliminating all intra-token mixed-script homoglyphs across all 40 publication editions while preserving Slavistic transliteration (`Dѣva`, `Krestъ`, `vъ`, `vѣkъ`) and diplomatic woodcut forms (`HMДEMYIΣ`, `INЦI`, `ΘЄѠ`, `ѲY`, `ΘV`).
   - Hardened `scripts/hieratic_pronoun_audit.py` (removing non-human cosmic/ecclesial nouns from `HUMAN_INDICATORS` and adding a direct doxological `glory to thee` check) and `scripts/structural_audit.py` (enforcing Mandate 8 `lvl < 3` across all cohort files while distinguishing bold section numbers from quoted/bracketed statutes).
3. **Universal Atomic Corpus Extractor & Test Sandbox Isolation (`scripts/universal_corpus_extractor.py`, `tests/test_bookend_model_routing.py`)**:
   - Fixed `is_cued_choral_hymn` classification (`1604_striatyn_balaban_liturgikon` upgraded to `11` propers, passing Gate 7D), tightened `batch_extract_all_completed()` strictly to `status == "completed"`, routed `--sync-hub` through sanitized `get_hub_inbox()`, sanitized `/` and spaces in `hub_inbox_folder` for 6 monuments in `Liturgical Monuments/codex_registry.json`, and sandboxed `REGISTRY_FILE` in `tests/test_bookend_model_routing.py` so `pytest` never mutates `1630_lviv_octoechos` in live `codex_registry.json`.
4. **Vault Hygiene, Source-Text Decontamination & Cohort Normalization Across 40 Monuments**:
   - Deleted all `102` `*-Augustine-PC.jpg` sync-conflict image duplicates; repaired subagent self-talk, `<ctrl95>` tokenizer leaks, and Latin/Greek homoglyphs across `308` `Source Text/*.txt` files; hydrated `687` Latin-transliterated `Podoben:` headings with parenthetical Cyrillic witnesses; normalized all legacy `H3+` (`###`/`####`) headings and pre-leaf wrapper banners across `Cohorts/` (`0` `structural_audit.py` failures across all `1,543` canonical cohort files, with `O(1)` `[\"“«*]*` prefix matching and TOC leader-dot exemption); added `part1` (`MONTH OF MAY`) to `1761_pochaiv_minea_09_may`; and sealed `1630_lviv_octoechos` as `"status": "completed", "active": false`.

---

## 2. Four-Tier Stratification Matrix Across All 41 Monuments (`17,054` Physical Leaves)

| Stratification Tier | Count | Physical Leaves | Monuments & Remediations Executed |
| :--- | :---: | :---: | :--- |
| **Tier 0 / Tier 1: Deterministic Engine Recompile & Cohort Normalization** | `31` | `11,212` | `2010_lviv_typikon` (`287` leaves; Gate 5A Cyrillic, Greek `[^531]`/`[^533]`, & mid-line `###` healed), `1852_doskovsky_typikon` (`141`), `1630_lviv_octoechos` (`267`; sealed `completed`, rescued `[^213]`), `1629_kyiv_octoechos` (`295`; Marian pronouns normalized), `1905_lviv_nativity_theophany` (`296`), `1906_lviv_triodion_lenten` (`532`), `1907_lviv_pentecostarion` (`671`), `1640_kyiv_triodion` (`896`), `1895_lviv_octoechos` (`1,029`; `SGC-06` digest regenerated), `1491_krakow_fiol_horologion` (`582`), `1600s_prykarpattia_ms_octoechos` (`222`), `1604_striatyn_balaban_liturgikon` (`293`; `11` propers), `1606_striatyn_balaban_trebnyk` (`1,401`), `1773_pochaiv_general_menaion` (`152`), `1738_univ_festal_offices` (`23`), `1741_pochaiv_festal_offices` (`30`), `1757_pochaiv_festal_offices` (`22`), `1785_kyiv_caves_fathers_services` (`157`), `1716_kyiv_marian_canons_octoechos` (`246`), `1617_kyiv_kopystensky_horologion` (`216`), `1761_pochaiv_minea_01_sep`..`04_dec` & `06_feb`..`12_aug` (`3,464` leaves across 11 volumes, including `1761_09_may` 2-Part `part0`+`part1` slicing). |
| **Tier 2: Surgical Native Gemini Vision Facsimile & Cohort Patch (`<= 5%` Scope, Rule 18)** | `9` | `4,752` | 1. **`1891_lviv_synod` (`278` leaves)**: Audited `Page_0128`–`0129`, `0138`, `0219.jpg`; stripped trailing inline `## Footnotes` across 14 cohorts (`278/278` in `Final_footnotes.txt`), restored printed `— 1.`/`[5.]`/`[10.]` statute markers, balanced `(**крестопоклонну**)` on `p276`, removed meta-bullet on `p278` (`0` `SGC-02` outliers).<br>2. **`1899_dolnytsky_typikon` (`591` leaves)**: Audited `Page_0145`–`0148`, `0212`, `0455.jpg`; verified 9 footnote-split leaves; replaced paraphrased `=== LEAF p146 ===`..`p148` (`cohort8`) AND fabricated/truncated footnotes `[^272]`–`[^273]` in `Final_footnotes.txt` with verbatim translations from 300 DPI ink.<br>3. **`1901_mikita_typikon` (`320` leaves)**: Audited `Page_0258.jpg` (`cohort26`), confirming `80w` body + `469w` in `[^275]` (`ratio=1.34`), zero omission.<br>4. **`1888_violakis_typikon` (`1,170` leaves)**: Audited `Page_0904.jpg`; removed 5 duplicate inline apparatus blocks on `p904, 968, 994, 1004, 1006` (`cohort91, 97, 100, 101`), bringing all 5 leaves inside `[2.19, 2.72]`.<br>5. **`1910_skaballanovich_typikon` (`1,022` leaves)**: Audited `Page_0989.jpg`; restored printed `(?)` in place of `[?]` on `p989` (`cohort99`).<br>6. **`1642_lviv_slozka_pentecostarion` (`441` leaves)**: Audited `Page_0111, 0113, 0114, 0116, 0118, 0120, 0121, 0287.jpg`; remediated all Rule 16 / `PE-HSG-04` full-text expansions across Royal Hours leaves `p111, 113, 114, 116, 118, 120, 121` (`cohort12`–`cohort13`), corrected misread pericopa `111` (`р҃аі`), Folio `107` (`р҃з`), and `1st Hour` (`на а҃-мъ Часѣ́`) in `Source Text/` & `[^373]`/`[^376]`, restored `in Palestine` on `p121`, and realigned `=== LEAF p287 ===` in `cohort29`.<br>7. **`1491_krakow_fiol_octoechos` (`345` leaves)**: Audited `Page_0024.jpg` & `Page_0193.jpg`; resolved `[?]` on `p24` (`ко̃ · ст̃оцꙋ`) and `p193` (`да и а́зъ бл[а]годарествено въ`).<br>8. **`1761_pochaiv_minea_05_jan` (`450` leaves)**: Audited `Page_0067.jpg`; repaired `Не поRangeжи́ша` $\rightarrow$ `Не послужи́ша` in `cohort7_source.txt:148` and `Final_footnotes.txt:444`.<br>9. **`1763_kyiv_caves_fathers_services` (`135` leaves)**: Audited `Page_0033.jpg`; repaired `хотя́щымъ meanings нынѣ̀` $\rightarrow$ `хотѧ́ща мѧ̀ ны́нѣ` in `cohort4_source.txt:84` and re-translated the Ode 9 stanza in `cohort4.md:129`. |
| **Tier 3: Rule 18 Pre-Rerun Archival & Phase 0 Bookend Lock (`> 20%` Incomplete)** | `1` | `1,090` | **`1895_dmitrievsky_vol1` (`paused`, `1,090` leaves)**: Inspected 8 bookend leaves (`Page_0001`–`0005.jpg`, `Page_1088`–`1090.jpg`) under Rule 14 Hard Vision Cap; archived all `88` partial files (including all `218` scholarly footnotes) + SHA-256 `archive_manifest.json` to `archive/pre_rerun_20261110_213709/`; purged all stale `Inbox/1895_Dmitrievsky_Opisanie_Vol1/` files and `translation_1895_dmitrievsky_vol1.ready.json`; wrote `Audit_Reports/phase0_preflight_brief.json` and `orchestrator_state.json` (`PHASE_0_ARGON_PLANNING_LOCKED`) for dedicated hybrid execution. |

---

## 3. Global Corpus, Telemetry & Verification Summary (`40 / 40` Sealed Monuments)

- **Universal Atomic Liturgical Corpus (`v4.0.0`, `Audit_Reports/ATOMIC_CORPUS_LEDGER.md`)**:
  - **Total Atomic Units (`40` Monuments)**: **`183,087`**
    - `PROPER_HYMN`: `80,592` (across `33` propers-bearing monuments; `7` Typikon/Synodal/Scholarly monuments strictly `0` propers)
    - `SACERDOTAL_PRAYER`: `803`
    - `LITANY_OR_DIALOGUE`: `3,932`
    - `FIXED_ORDINARY_OR_LECTION`: `17,850`
    - `RUBRIC_OR_STATUTE`: `79,910`
  - **4-Shard `Shared_Lexicon` Routing**:
    - `01_ordinarium_primitives.json`: `102,495`
    - `02_sticherarion.json`: `31,436`
    - `03_irmologion.json`: `9,660`
    - `04_kanonnik.json`: `39,496`
- **Hub Inbox Synchronization**:
  - Purged `144` stale/duplicate files across `19` obsolete Hub Inbox folders (`1895_Dmitrievsky_Opisanie_Vol1`, legacy `Pochayiv` spelling folders, and split-slash folders) and synchronized exactly `40` completed monument directories, `handoff_note.md`, `40` `translation_<monument_id>.ready.json` tickets, and `translation_corpus_manifest.ready.json` (`40` ready, `33` propers-bearing) to `../Typikon Coded/Data/Inbox/`.
- **Quality Gate Verification**:
  - `scripts/verify_publication_edition.py --all-completed`: **`40 / 40` PASSED** across Gates 1–8 (`Composite PHI = 100.0 / 100.0`, `0` V5C fake-archaisms, `0` V11 sandbox violations, `0` unresolved quarantines, `0` broken TOC anchors, `0` `[?]`/`[lacuna]` markers, `0` `SGC-06` leaks).
  - `scripts/structural_audit.py`: **`0` failures** across all `1,543` canonical cohort files (`2.89s`).
  - `py -m pytest tests/ -v`: **`76 / 76` passed** (`18.95s`).
