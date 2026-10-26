# Translation Spoke Master Rules & Operational Standards

## Preamble & Global Rules Inheritance
This workspace inherits and enforces all compliance protocols, API configurations, and general code safety standards defined in the parent root:
* [GLOBAL_SYSTEM_RULES.md](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/GLOBAL_SYSTEM_RULES.md)

You must strictly comply with the Honesty Protocol, the Evidence Gate, Banned Phrases, UTF-8 Enforcement, Dynamic Path Resolution, the Native Gemini Vision Mandate (Zero Third-Party APIs), the Exclusive Write-Ownership Matrix (§7 — exclusive write owner of `Projects/Translation/` with narrow Drive E carve-out to registered `JPGs/` extraction vaults in `codex_registry.json`), and the Universal Ground-Truth & Anti-Potemkin Law (`SGC-01`..`SGC-04`, §8) defined therein.

---

## Re-Onboarding & Verification Protocol
Upon any context reset, restart, or when the agent observes a suspicion of state hallucination, the agent **must first** execute the status check script:
```powershell
python scratch/search_anti_patterns.py
```
The status output must be compared with the last known "golden" baseline. If the script reports newly introduced violations, the agent halts all code-modifying tasks and notifies the human operator before proceeding. The agent must **never** execute any modification, file I/O, or tool call until this verification passes or is explicitly waived by the operator.

---

## The Master Rules & Codified Anti-Patterns

### 1. Native Gemini Vision Mandate & Prohibition of Third-Party APIs
* The Translation spoke operates exclusively using **Native Gemini Vision** (`view_file` on 300 DPI leaf images) and context-sequestered Antigravity subagents (`invoke_subagent`).
* All third-party LLM/Vision APIs (including DeepSeek, OpenAI, Anthropic, and external OCR endpoints) are permanently prohibited across all active pipelines.
* Legacy scripts referencing third-party APIs must remain isolated in `scripts/archived_pipelines/` and must never be invoked during production runs.

### 2. Logical & Semantic Chunking Engine
* Naive character-based chunking splits paragraphs arbitrarily and breaks semantic context, causing false positives and alignment mismatches.
* Split files dynamically by logical boundary tags such as:
  * Chapter headers (`###`)
  * Roman numeral points (`I.`, `II.`, `III.`)
  * Arabic numeral bullet lists (`1.`, `2.`, `3.`)
* Align English and Ukrainian chunks by matching these structural keys rather than assuming a simple row-by-row `zip()`.
* If a single section exceeds 15,000 characters, subdivide it only at sentence boundaries (`. `, `? `, `! ` followed by a space), never in the middle of a paragraph.

### 3. Liturgical Translation, Native Vision & Master Standard (MTS-1)
* All translations across all monuments must strictly comply with the **Master Translation Standard (MTS-1)** codified in:
  `C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Shared_Lexicon\MASTER_TRANSLATION_STANDARD.md`
* **Universal Native Vision Mandate**: 100% of translated texts begin with 300 DPI image extraction and direct Gemini Native Vision transcription. Digital texts or existing drafts are strictly secondary concordances.
* **The Four Registers**: Agents must apply the appropriate genre register (Juridical, Rubrical, Hymnographic, Scholarly).
* **Scripture & Psalter**: Septuagint (LXX) numbering is mandatory; Masoretic references in brackets in footnotes only.
* **Rubrical Mood**: Use Active Present Indicative for ceremonial actions; reserve "shall" for statutory legal mandates.
* **Realia & Melodic Models**: Use technical loanwords (*Tetrapod, Klepalo, Aer, Kolyvo, Plashchanytsia, Sluzhebnik*) and Ruthenian chant headings (*Tone 1–8*, *Podoben: "[Incipit]"*).
* **Pronouns & Doxology**: 100% capitalization on Deity Trinity pronouns (*He, Him, His, Thou, Thee*); enforce the Father Paul Doxology Standard (ban *"for ever and ever"*).

### 4. Footnote Referencing Protocol
* Every footnote marker `[^N]` in a Part file MUST have a corresponding `[^N]:` definition in `Final_footnotes.txt`, and vice versa.
* Never inline footnote definitions in the body text of a Part file (except where structurally required). Maintain footnote descriptions in the master footnotes file.

### 5. Path Enforcement Policy
* All new and modified Python scripts MUST use `from pathlib import Path` and calculate project-relative paths.
* Any reference to user home directories or network shares must go through environment variables (e.g., `os.environ.get('TRANSLATION_DATA')`).
* Hardcoded absolute filesystem paths are strictly prohibited and will be flagged by the anti-pattern searcher.

### 6. P01 – Fabricated Progress Narrative
Never claim a script has successfully run, parsed, or generated a file without pasting the validation output, file size, or line count diff as proof. If you lack evidence, you must state: *"I have not verified this claim."*

### 7. P03 – Exploratory Drift
Stay strictly on the task defined in the approved implementation plan. Do not restructure unrelated directories unless explicitly requested.

### 8. P04 – Bare except
Bare except blocks are prohibited. You must specify the exception type or log it explicitly.

### 9. P05 – Hardcoded Absolute Path
Do not hardcode paths. Always resolve paths relative to the project root or via environment variables.

### 10. P09 – Missing Encoding Declaration
Always specify `encoding='utf-8'` in all file open operations for text.

### 11. P12 – State Hallucination
Do not invent logs, confirmation messages, or file states. Every statement about existing content must be backed by a recent tool call.

### 12. Pre-Flight Checklist (Before ANY Modification)
Before editing or running any scripts/files, you MUST:
1. Verify you have read `.agents/AGENTS.md`.
2. Inspect the file map and understand the target directory (`Final/` and `Final MD/` for deliverables, `scratch/` for utilities).
3. Confirm that no third-party API calls are introduced and all paths use `pathlib.Path` relative to project root or canonical environment variables.

### 13. Post-Flight Checklist & Handoff (After ANY Modification)
After modifying files or completing audits:
1. Run `git diff --stat` to verify changes.
2. Run a dry run or test suite (`py -m pytest tests/ -v`) of any modified verifiers or linters, and run `python "../scripts/verify_ecosystem_integrity.py" --spoke "Translation"`.
3. Update the global notice board at `GLOBAL_ECOSYSTEM_STATE.md` if shipping a new translation segment.
4. Copy finalized deliverables to the Hub's inbox: `C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Inbox\`.
5. Write a `handoff_note.md` in the Inbox detailing what was translated and any terminology considerations.

---

### 14. Inviolable Autonomous Execution, Subagent Isolation & 3-Phase Bookend Hybrid Model Routing Rule
* **3-Phase Bookend Hybrid Model Routing Architecture**:
  * **Phase 0 (`PHASE_0_ARGON_PLANNING` — Main UI on `Gemini 4 Argon (High)`)**:
    * Every new monument initializes in `PHASE_0_ARGON_PLANNING` (`small_pause_gate_status = "PHASE_0_ARGON_PLANNING_LOCKED"`).
    * The orchestrator runs `py scripts/autonomous_orchestrator.py --preflight --monument <ID>`, which writes `<workspace>/Audit_Reports/phase0_preflight_brief.json` containing the deterministic Phase 0 Vision Budget Contract (`max_vision_leaves = 8`, `max_vision_batches = 2`) and the genre-scaffolded `recommended_publication_spec` from `data/templates/publication_spec_scaffolds.json`.
    * **Hard Phase 0 Argon Vision Budget Cap (`<= 8` Leaves / `<= 2` Batches)**:
      * During Phase 0 on `Argon (High)`, the agent may inspect at most **8 physical 300-DPI leaf images across at most 2 `read_file` tool-call batches**:
        * **Batch 1 (Front Bookend — Max 5 Leaves)**: `Page_0001.jpg` through `Page_0005.jpg` (cover, title page, frontispieces, preface/TOC opening, first text leaf).
        * **Batch 2 (Rear Bookend — Max 3 Leaves)**: `Page_(N-2).jpg` through `Page_N.jpg` (closing colophon, rear index/table, final folio).
      * **Absolute Ban on Mid-Codex Visual Binary Searches**: Inspecting internal leaves `p6` through `p(N-3)` during Phase 0 to hunt for internal section/Tone boundaries is strictly prohibited. Instead, Phase 0 uses the deterministic `recommended_publication_spec` scaffold, Phase 1 `Flash` workers emit canonical H1 headings (`# Tone N`, `# Canon ...`, `# Part ...`) when encountered on the physical page, and Phase 2 (`--compile-publication`) binds `start_landmark` regexes against actual translated headings on disk.
    * **Gate 0 Primary Source Suitability Check & Fast-Fail Deferral (`--defer-monument`)**:
      * Immediately after inspecting Batch 1 (`p1`–`p5`), if the source PDF is discovered to be a modern excerpted edition, secondary academic monograph, or severely defective/truncated scan rather than a complete historical codex, the agent must **immediately halt further image inspection** (do not read Batch 2 or write a translation plan), report the Gate 0 defect to the human operator, and upon confirmation execute `py scripts/autonomous_orchestrator.py --defer-monument --monument <ID> --reason "..."` to mark the monument `"status": "failed"` (`"wave": 5`), move it to the back of `Liturgical Monuments/codex_registry.json`, and emit the next monument's onboarding prompt.
    * **Hard Circuit-Breaker**: `prepare_cohort()` and `--step` are **programmatically blocked** from emitting a Cohort 1 subagent manifest until the human operator approves `implementation_plan.md`, switches the Main Window UI dropdown from `Argon` $\rightarrow$ `Gemini 3.8 Flash`, and the agent executes `py scripts/autonomous_orchestrator.py --unlock-flash-sprint`.
  * **Phase 1 (`PHASE_1_FLASH_SPRINT` — Main UI + Subagents Locked to `Gemini 3.8 Flash`)**:
    * **Lean Custom Worker Subagent (`ephemeral_translator`)**: Defined via `define_subagent` (`EnableWriteTools=True`, `EnableSubagentTools=False`, `EnableMCPTools=False`) and invoked with `Model="flash"` strictly locked across 100% of Phase 1 cohorts and retries (zero silent mid-sprint `"pro"` overrides).
    * **Automated `argon_review_queue.json` Collector**: `scripts/run_small_pause_gate.py` automatically scans every `=== LEAF pN ===` block and queues a leaf into `Audit_Reports/argon_review_queue.json` on 4 signals:
      1. Epigraphic uncertainty / lacuna markers (`[?]`, `[illegible]`, `[lacuna]`, `[damaged]`, `[corrupt]`).
      2. Borderline `SGC-02` draft-to-source length ratios (`< 0.50` or `> 2.20` on non-sparse leaves).
      3. High-complexity Paschalion/multi-column tables (`>= 5` table rows) or dense polyglot apparatus (`>= 5` footnotes on 1 leaf).
      4. Quarantined leaves (`status="QUARANTINED_FOR_ARGON"`).
    * **Two-Tier Unattended Flash Resilience**: On a Small Pause Gate failure, the orchestrator first runs 4-part deterministic Python self-healing (`attempt_deterministic_self_healing()`: leaf banner normalization, inline `[^N]:` footnote migration, 1-to-1 forbidden vocabulary/doxology replacement, and Deity pronoun capitalization), then allows **1 targeted `Flash` subagent retry**. If a content/linter/ratio/footnote anomaly still persists after 1 retry, as long as all expected physical `=== LEAF pN ===` boundaries exist on disk, the offending leaf(s) are quarantined into `argon_review_queue.json` (`status="QUARANTINED_FOR_ARGON"`) and Phase 1 continues auto-chaining non-stop. Hard-stops (`BLOCKED`) occur only if physical files or `=== LEAF pN ===` boundaries are missing.
  * **Phase 2 (`PHASE_2_AWAITING_ARGON_AUDIT` $\rightarrow$ `PHASE_2_ARGON_DEEP_AUDIT` — Main UI Switched Back to `Gemini 4 Argon (High)`)**:
    * When `remaining_pages == 0`, the orchestrator halts at `AWAITING_ARGON_POST_SPRINT_AUDIT` so the human operator can switch the Main Window UI dropdown from `Flash` $\rightarrow$ `Gemini 4 Argon (High)`.
    * Running `py scripts/autonomous_orchestrator.py --run-argon-audit` resolves `argon_review_queue.json` (directly in parent `Argon` if $\le 5$ leaves, or via batched `Model="inherit"` `Argon` subagents of $\le 8$ leaves if $> 5$ leaves), re-verifies touched cohorts, and gates LCPE final compilation (`--compile-publication` / `UniversalPublicationEngine`) on `unresolved_quarantines == 0` before presenting the Sovereign Grand Pause.
* **Prohibition of the Two-Chat Copy-Paste Anti-Pattern**:
  * The Orchestrator must **never** generate prompts instructing the human operator to "copy and paste into another chat" or yield turns waiting for human relay.
  * All worker delegations must be executed programmatically via `invoke_subagent`.
* **Grand Pause Approval as Chat Lifecycle Boundary & Automated Git Push Pipeline**:
  * Human operator approval of the Grand Pause marks the **functional conclusion and retirement of that orchestrator chat session**.
  * Formal approval is executed via `py scripts/autonomous_orchestrator.py --approve-grand-pause` (or agent directive upon human approval).
  * **Automated Sealing Pipeline**:
    1. **Publication Gate Assertion**: Re-verifies `unresolved_quarantines == 0`, canonical publication edition integrity, and leaf conservation.
    2. **Hub Inbox Synchronization**: Copies sealed markdown deliverables to `Typikon Coded/Data/Inbox/` and updates `handoff_note.md`.
    3. **Automated Git Push**: Stages all deliverables (`git add .`), creates canonical commit (`feat(<monument>): seal canonical publication edition (leaves 1..N)`), and pushes cleanly to upstream remote (`git push origin master`).
    4. **Sequential Handoff Prompt**: Resolves the next monument in registry and outputs the copy-pasteable `/plan` startup prompt (Rule 19).
  * The Orchestrator must **never automatically roll into or begin processing the next monument within the same conversation context**.
  * Each monument in the transmission chain begins in a dedicated, fresh conversation to preserve context isolation, eliminate token memory saturation, and enforce independent lifecycle constraints.

---

### 15. Closed Mathematical Leaf Conservation Law & Universal Facsimile Indexing
* **Absolute Ban on Out-of-Order Cohort Indexing**:
  * All translation cohorts across every monument must be numbered and executed strictly $1 \dots N$ in monotonically ascending physical PDF facsimile leaf order, starting unconditionally at physical leaf `p1`.
  * Ad-hoc calibration cohorts executed on rear matter (e.g. testing concluding decrees or fasting rules before chapter 1) under temporary cohort numbering are strictly prohibited.
* **Coordinate System Disambiguation (Leaf Index vs. Printed Page Number)**:
  * In historical codices, physical PDF leaf numbers and internal printed book page numbers diverge whenever unnumbered front matter exists ($\mathbf{Book\ Page} = \mathbf{PDF\ Leaf} - \mathbf{Front\ Matter\ Offset}$).
  * All work orders, cohort partitions, extraction batches, and filenames MUST operate exclusively in **Physical PDF Leaf Index coordinates**. Printed book page numbers are recorded parenthetically in leaf banners for scholarly cross-reference only.
* **Closed Mathematical Leaf Conservation Invariant**:
  * The Master Assembler (`scripts/assemble_and_sync_hub.py`) enforces a closed set-union conservation law prior to producing any complete edition or syncing to the Hub:
    $$\bigcup_{k} \mathbf{Leaves}(C_k) \equiv \{1, 2, \dots, \mathbf{Total\ Physical\ Pages}\}$$
  * If $\min(\mathbf{Leaves}) \neq 1$, or an internal leaf chasm exists, or tail-end folios are missing, assembly must hard-abort with a fatal exit code.
* **Inter-Cohort Monotonic Continuity Gate**:
  * The Small Pause Gatekeeper (`scripts/structural_audit.py`) programmatically audits every cohort $K > 1$ against cohort $K-1$, asserting:
    $$\min(\mathbf{Leaves}_K) \le \max(\mathbf{Leaves}_{K-1}) + 1$$
  * Any unmapped gap between cohorts halts autonomous progression immediately.

---

### 16. Strict Epigraphic Fidelity & Incipit Preservation
* **Grounding in Physical Ink**: All translation and transcription must be strictly grounded in the high-resolution 300 DPI page scan images. Digital text layers, OCR, and existing drafts serve strictly as secondary concordances.
* **Prohibition of Unwritten Incipit Expansions**:
  * Historical liturgical codices frequently record only the opening words (incipit) of a prayer, troparion, or litany (e.g. `**"God is the Lord"**`, `**"Lord, have mercy"**`, `**"Glory..."**`).
  * Translators are **strictly prohibited** from expanding an incipit into a full unwritten liturgical text in the translation body unless that full text is physically printed on the leaf.
* **Brackets and Footnotes for Editorial Restorations**:
  * Any lacuna, damaged glyph, illegible phrase, or necessary syntactic restoration MUST be enclosed in square brackets `[...]`.
  * Significant contextual restorations or variant citations must be documented in a corresponding footnote `[^N]` rather than interpolated silently into the body text.

---

### 17. Empirical Discourse & Anti-Slop Protocol
* **Empirical Engineering Tone**:
  * Agents must communicate in a factual, dry, evidence-backed tone.
  * Rhetorical puffery, marketing superlatives, self-congratulatory claims, and metaphorical flourishes (e.g., "melodic DNA", "twin pillars", "profound reframing", "rich tapestry") are strictly prohibited in agent conversations and documentation.
  * Every progress statement must be verified by a concrete tool call, citing exit codes, line numbers, byte diffs, or file paths.
* **Anti-Slop Linter Enforcement (Gate 1B)**:
  * All draft and final translations are subjected to `scripts/lint_liturgical_slop.py`.
  * The linter rejects:
    1. Pseudo-archaic AI fantasy vocabulary (*verily, betwixt, twas, methinks, hearken, wherefore* in body rubrics, *peradventure, effulgent, resplendent, lo and behold*).
    2. AI conversational clichés and filler (*testament to, beacon of, delve into, tapestry of, rich history, serves as a reminder, inextricably linked*).
    3. Rubrical 'shall'-bombing in ceremonial actions (active present indicative is mandatory for bodily motions; "shall" is reserved strictly for juridical statutes).

---

### 18. Breakthrough Invalidation & Re-Run vs. Patch Decision Protocol
When a major developmental breakthrough occurs (e.g., new OCR/vision models, glossary overhauls, discoverable leaf caches, structural engine redesigns), agents and human operators evaluate whether to execute an automated complete re-run or apply targeted in-place patches using the following objective 4-criterion decision matrix:

| Criterion | In-Place Patch Path | Complete Automated Re-Run Path |
|---|---|---|
| **Epigraphic Integrity** | Physical leaf images and raw transcriptions are 100% intact and complete. | Missing leaves discovered, misordered folios, corrupt OCR layers, or epigraphic omissions ($> 5\%$). |
| **Deterministic Solvability** | Defect is isolatable via deterministic Python AST, regex, or glossary mapper (e.g. terminology find-and-replace, footnote numbering shift). | Defect requires holistic semantic or syntactic re-translation across multiple paragraphs. |
| **Defect Scope** | Defect affects $\le 5\%$ of paragraphs or leaves across the monument. | Defect affects $> 20\%$ of paragraphs or alters fundamental document structure. |
| **Lifecycle Phase** | Intermediate draft phase or minor post-assembly errata. | Pre-assembly raw draft or systematic breakthrough rendering existing drafts obsolete. |

* **Mandatory Pre-Rerun Archiving Protocol**:
  * Before triggering any complete re-run of a cohort or monument, the existing cohort markdown and footnote files MUST be archived into a timestamped directory: `archive/pre_rerun_YYYYMMDD_HHMMSS/`.
  * A programmatic Delta Audit must be executed after the re-run to verify that no prior human corrections or verified glosses were lost.

---

### 19. Granular Onboarding Prompts for Next Monument Sessions (`GLOBAL_SYSTEM_RULES.md` §10)
* **Codified Format**: Whenever an agent completes a monument handoff, defers a monument via `--defer-monument`, provisions startup instructions, or responds to a "prompt for the next monument" request, the onboarding prompt **MUST** be generated via `build_phase0_onboarding_prompt()` (`data/templates/phase0_onboarding_prompt_template.md`) and provided as an explicit, copy-pasteable `text` code block obeying `GLOBAL_SYSTEM_RULES.md` §10:
  1. **Zero Slash Commands Inside Copy Block**: Never include `/plan`, `/grill-me`, or any `/command` inside the copyable prompt block (the human operator handles `/plan` and `/grill-me` in the UI input bar).
  2. **Zero Auto-Execution Directives**: Never instruct the incoming agent to execute Cohort 1, unlock the sprint, or mutate files on Turn 1.
  3. **Hard Phase 0 Vision Budget Cap & Gate 0 Fast-Fail Clause**: Every onboarding prompt must explicitly state the **8-leaf / 2-batch vision cap** (`Batch 1: Page_0001..Page_0005`, `Batch 2: Page_(N-2)..Page_N`), the **absolute ban on mid-codex visual binary searches** (`p6`..`p(N-3)`), the instruction to run `py scripts/autonomous_orchestrator.py --preflight --monument <ID>` and consume `Audit_Reports/phase0_preflight_brief.json`, and the **Gate 0 Primary Source Suitability Fast-Fail** (`--defer-monument`) rule.
  4. **Granular Context, Infinitive Opening & Turn-1 Planning Stop**: Open with a clean infinitive phrase (`Orient on and prepare the Phase 0 translation architecture for...`), granularly introduce the monument's codicological metadata, and instruct the incoming agent to author `implementation_plan.md` (`RequestFeedback: true`, `UserFacing: true`) and **STOP** for human planning and `/grill-me` alignment before executing any cohorts.
* **Prohibition of Narrative-Only Handoffs**: An agent must never announce that startup files have been generated without simultaneously providing the exact copy-pasteable onboarding prompt block in the message output.

---

### 20. Canonical Drive E: Master Asset Vault & Storage Tiering Mandate
* **External Single Source of Truth**:
  * `E:\Google Drive\Liturgical Library\` (specifically `E:\Google Drive\Liturgical Library\2. Historical Liturgical Texts\Typikons_and_Ordines\<Stem>\JPGs\` for historical Typika and the corresponding `<canonical_mirror_dir>\JPGs\` defined in `Liturgical Monuments/codex_registry.json`) is the immutable canonical master vault for all 300 DPI high-resolution page rasters across all monuments.
  * Image format is strictly standardized to **300 DPI JPEG (Quality 92)** with 4-digit zero-padded indexing (`Page_0001.jpg`), matching the Chant Indexer spoke specification.
* **Prohibition of Local Raster Bloat on Drive C:**:
  * Multi-gigabyte image sets must **never** reside natively on Drive C:, as OneDrive synchronization congests cloud bandwidth and consumes local SSD capacity.
  * All workspace image folders (`Liturgical Monuments/<Monument>/Source Text/images/`) must be transparently mapped via **NTFS Directory Junctions** (`mklink /J`) pointing to their corresponding Drive E: master vault directory.
* **Two-Tier Extraction Hierarchy**:
  * `scripts/extract_cohort_leaves.py` must enforce a 2-tier lookup: Tier 1 verifies existing Drive E: vault images (`Page_{p:04d}.jpg`); Tier 2 renders missing pages directly to Drive E: as quality-92 JPEGs (`Page_{p:04d}.jpg`). Creating `p{p}.jpg` or `p{p}.png` hardlink aliases on Drive E: is strictly prohibited, as cloud sync clients upload hardlinks as duplicate files.
  * PyMuPDF rendering from source PDF is prohibited when a leaf is already present in the Drive E: vault.
* **Drive E Recursive `.rglob()` Law (§6.1)**:
  * Because nested subfolders in the Drive E Liturgical Library may be reorganized at any time, all scripts scanning Drive E vaults (`scripts/extract_cohort_leaves.py`, `scripts/sync_drive_e_asset_mirror.py`, `scripts/verify_publication_edition.py`) must resolve leaf rasters and source PDFs dynamically via recursive `.rglob("Page_*.jpg")` and `.rglob(pdf_name)` searches rather than brittle single-level path joins.

---

### 21. Potemkin Epigraphy & Header-Span Goodhart Gaming (`PE-HSG-01`..`05` / `SGC-Translation`)
Nested under the ecosystem-wide **Synthetic Goodhart Compliance (`SGC-01`..`SGC-05`)** law in `GLOBAL_SYSTEM_RULES.md` §8:
* **`PE-HSG-01` (Ban on Synthetic Transcription & Hardcoded Prose Builders)**:
  * Python builder scripts must never embed hardcoded multiline liturgical prose, synthetic Slavonic/Greek reconstructions, or programmatic placeholder injections (`[INSERT DIAGRAM/TABLE HERE FROM ORIGINAL PDF]`, `(Translator's Note:...)`). All document templates must reside in external `.md` files under `data/templates/`.
* **`PE-HSG-02` (Ban on Range-Interpolated Leaf Conservation)**:
  * Range-spanning headers (`## ... (pp. X-Y)` or `Regex #5` interpolation) are permanently prohibited from satisfying leaf conservation in `scripts/assemble_and_sync_hub.py` or `scripts/structural_audit.py`. Every physical leaf `pN` must possess an explicit individual `=== LEAF pN ===` boundary banner.
* **`PE-HSG-03` (3-Tier `SGC-02` Ground-Truth & Primary-Source Bijection)**:
  * Every leaf block in `Source Text/`, `Draft/`, `Cohorts/`, and `Final/` must pass per-leaf character and word density thresholds (`>= 50` alphanumeric characters and `>= 10` words per non-blank leaf) and `Source Text/` $\leftrightarrow$ `Cohorts/` word-ratio parity (`[0.35, 3.00]`), enforced by `scripts/structural_audit.py` and Gate 6 of `scripts/verify_publication_edition.py`.
* **`PE-HSG-04` (Ban on Unverified Incipit Expansion)**:
  * Translators and scripts are prohibited from replacing printed incipits with unverified external full-text maps or silent liturgical interpolations.
* **`PE-HSG-05` (Apparatus & Summary Block Isolation)**:
  * Leaked `### Notes` headers, inline footnote definitions inside body prose, and pre-written summary blocks or agent internal reasoning notes are prohibited inside canonical publication files and enforced by Gate 1 and Gate 5 of `scripts/verify_publication_edition.py`.
* **Shared Atomic Liturgical Corpus Integration (§7)**:
  * When referencing standard fixed liturgical prayers or psalmody in `Shared_Lexicon/Atomic_Liturgical_Corpus/`, scripts and validators must consume the canonical 4-shard atomic files (`01_horologion_and_fixed_prayers.json`, `02_octoechos_and_menaion_propers.json`, `03_triodion_and_pentecostarion.json`, `04_euchologion_and_sacraments.json`) read-only and never write to `Shared_Lexicon/Atomic_Liturgical_Corpus/`.

---

### 22. Universal Epigraphic Grounding & Anti-Pretraining Incursion Law (`SGC-06` / Rule 22)
* **The Root Problem (Pre-Training Data Incursion)**: LLM agents carry latent pre-trained assumptions from modern liturgical handbooks, standard Byzantine Greek automela compendia, and 19th/20th-century Russian Synodal rubrics. Conflating internal codex evidence with external pre-trained tradition—or projecting external taxonomies onto historical monuments—is a critical failure mode that corrupts the empirical integrity of our research.
* **Invariant Principles**:
  1. **Tabula Rasa Internal Ground Truth**: Every monument's internal index, primitives registry, подобен grid, or rubric catalog must be constructed **100% bottom-up from the physical ink of its leaves (`p1`..`pN`)**.
  2. **Zero Internal Model Hallucination**: No liturgical model, category, or hymnographic primitive may appear in an internal monument dataset unless it possesses $\ge 1$ verified physical attestation tuple on a physical leaf:
     $$\mathbf{Attestation\ Locus} \equiv \big\langle \mathbf{Physical\ Folio\ \&\ Column},\ \mathbf{Leaf\ Number},\ \mathbf{Liturgical\ Office},\ \mathbf{Verbatim\ Slavonic\ Rubric},\ \mathbf{Governed\ Incipit} \big\rangle$$
  3. **Strict Epistemic Layering (Internal vs. External Concordance)**:
     - **Internal Primary Source Layer**: Contains ONLY what is physically printed in that monument.
     - **External Comparative Layer**: Broad Byzantine Greek roots, post-Nikonian variants, cross-monument links, and general automela concordances MUST be strictly quarantined in separate comparative datasets (e.g. `data/byzantine_automela_concordance.json`, dedicated concordance appendices, or Section 4 of review digests). They must NEVER be merged into primary internal registries or presented as internal codex evidence.
  4. **Prohibition of Negative Hallucinations / Ghost Stubs**: Internal codex grids and registries must never list un-invoked external textbook models with blank (`—`) or zero (`0`) attestations as if the historical codex was deficient or omitted them. A monument is its own primary witness; missing an external model belonging to a different liturgical cycle (e.g. Menaion or Horologion) is not a codex defect.
  5. **Programmatic Assertion Gate**: Every primitives registry and podoben grid builder must programmatically assert that 100% of items in any primary monument registry satisfy `len(attested_loci) > 0`. Empty or un-attested stubs are rejected at runtime.

