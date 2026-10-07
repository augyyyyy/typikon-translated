# Translation Spoke Master Rules & Operational Standards

## Preamble & Global Rules Inheritance
This workspace inherits and enforces all compliance protocols, API configurations, and general code safety standards defined in the parent root:
* [GLOBAL_SYSTEM_RULES.md](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/GLOBAL_SYSTEM_RULES.md)

You must strictly comply with the Honesty Protocol, the Evidence Gate, Banned Phrases, UTF-8 Enforcement, Dynamic Path Resolution, and DeepSeek V4 API Orchestration rules defined therein.

---

## Re-Onboarding & Verification Protocol
Upon any context reset, restart, or when the agent observes a suspicion of state hallucination, the agent **must first** execute the status check script:
```powershell
python scratch/search_anti_patterns.py
```
The status output must be compared with the last known "golden" baseline. If the script reports newly introduced violations, the agent halts all code-modifying tasks and notifies the human operator before proceeding. The agent must **never** execute any modification, file I/O, or tool call until this verification passes or is explicitly waived by the operator.

---

## The 12 Master Rules & Codified Anti-Patterns

### 1. Unified DeepSeek V4 Pro API Standard
* The Translation spoke operates exclusively using the DeepSeek API.
* Always resolve keys via `get_deepseek_key()` to support local, workspace, and global `.env` files.
* For reasoning-intensive text audits, always use `deepseek-v4-pro` and ensure that thinking mode is correctly configured:
  * For direct HTTP POST requests, pass `"thinking": {"type": "enabled"}` at the root level of the payload.
  * For OpenAI SDK client requests, pass `extra_body={"thinking": {"type": "enabled"}}`.

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
2. Inspect the file map and understand the target directory (`Final/` for deliverables, `scratch/` for utilities).
3. Confirm the DeepSeek API configuration standard is applied to the script.

### 13. Post-Flight Checklist & Handoff (After ANY Modification)
After modifying files or completing audits:
1. Run `git diff --stat` to verify changes.
2. Run a dry run of the verifiers if they were modified to ensure API connection and key resolution functions.
3. Update the global notice board at `GLOBAL_ECOSYSTEM_STATE.md` if shipping a new translation segment.
4. Copy finalized deliverables to the Hub's inbox: `C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Inbox\`.
5. Write a `handoff_note.md` in the Inbox detailing what was translated and any terminology considerations.

---

### 14. Inviolable Autonomous Execution & Subagent Isolation Rule
* **Canonical Architecture**:
  * **Parent Orchestrator Session**: Stays in the primary chat, driving the multi-cohort loop controller (`scripts/autonomous_orchestrator.py`).
  * **Context-Sequestered Subagent (via `invoke_subagent`)**: Worker subagents spawned natively in the background with isolated context for transcription and drafting. The parent orchestrator never ingests raw images or massive leaf transcriptions directly into its primary context.
  * **Small Pause Gate**: 100% automated, zero-human Python linter suite (`scripts/run_small_pause_gate.py`). Runs headlessly and programmatically in seconds between cohorts.
  * **Grand Pause**: The **sole** human checkpoint, occurring strictly and exclusively when 100% of all physical leaves across the entire monument are translated and assembled (`remaining_pages == 0`).
* **Inviolable Autonomous Execution Rule**:
  * The Orchestrator is **strictly prohibited from yielding execution to the Human Operator between cohorts during production codex processing**.
  * If a Small Pause Gate passes, the next cohort **MUST be dispatched immediately via `invoke_subagent`**.
  * The agent may only halt execution when `active_blockers` is non-empty (and logged in `scratch/triage_inbox.jsonl`) or when `remaining_pages == 0` (Grand Pause).
* **Prohibition of the Two-Chat Copy-Paste Anti-Pattern**:
  * The Orchestrator must **never** generate prompts instructing the human operator to "copy and paste into another chat" or yield turns waiting for human relay.
  * All worker delegations must be executed programmatically via `invoke_subagent`.
* **Grand Pause Approval as Chat Lifecycle Boundary & Automated Git Push Pipeline**:
  * Human operator approval of the Grand Pause marks the **functional conclusion and retirement of that orchestrator chat session**.
  * Formal approval is executed via `py scripts/autonomous_orchestrator.py --approve-grand-pause` (or agent directive upon human approval).
  * **Automated Sealing Pipeline**:
    1. **Publication Gate Assertion**: Re-verifies canonical publication edition integrity and leaf conservation.
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

### 19. Mandatory `/plan` Prefix for all New Session Startup Prompts
* **Codified Format**: Whenever an agent completes a monument handoff, provisions startup instructions, or outputs a startup prompt for a new chat session, the prompt **MUST ALWAYS** be provided as an explicit, copy-pasteable code block prefixed with the `/plan` slash command:
  ```text
  /plan [Instruction payload specifying monument ID, total pages, cohort sizing, STARTUP_INSTRUCTIONS.md, and execution directive]
  ```
* **Operational Rationale**: Starting the prompt with `/plan` ensures the user can copy, paste, and run (or tweak) the prompt to force the newly initialized chat session directly into planning mode before any code execution or file modification occurs.
* **Prohibition of Narrative-Only Handoffs**: An agent must never announce that startup files have been generated without simultaneously providing the exact `/plan`-prefixed code block in the message output.

---

### 20. Canonical Drive E: Master Asset Vault & Storage Tiering Mandate
* **External Single Source of Truth**:
  * `E:\Google Drive\Liturgical Library\3. Modern Service Books and Typikons\Typikon\Historical Typikons\<Stem>\JPGs\` is the immutable canonical master vault for all 300 DPI high-resolution page rasters across all monuments.
  * Image format is strictly standardized to **300 DPI JPEG (Quality 92)** with 4-digit zero-padded indexing (`Page_0001.jpg`), matching the Chant Indexer spoke specification.
* **Prohibition of Local Raster Bloat on Drive C:**:
  * Multi-gigabyte image sets must **never** reside natively on Drive C:, as OneDrive synchronization congests cloud bandwidth and consumes local SSD capacity.
  * All workspace image folders (`Liturgical Monuments/<Monument>/Source Text/images/`) must be transparently mapped via **NTFS Directory Junctions** (`mklink /J`) pointing to their corresponding Drive E: master vault directory.
* **Two-Tier Extraction Hierarchy**:
  * `scripts/extract_cohort_leaves.py` must enforce a 2-tier lookup: Tier 1 verifies existing Drive E: vault images; Tier 2 renders missing pages directly to Drive E: as quality-92 JPEGs and creates compatibility aliases (`p{p}.jpg`, `p{p}.png`).
  * PyMuPDF rendering from source PDF is prohibited when a leaf is already present in the Drive E: vault.

