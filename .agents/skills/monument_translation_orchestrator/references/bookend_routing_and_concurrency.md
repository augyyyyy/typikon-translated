# 3-Phase Bookend Hybrid Model Routing & Sequestered Concurrency Playbook

## 1. Phase 0: Bookend Planning (`PHASE_0_ARGON_PLANNING` — `Gemini 4 Argon (High)`)

### 1.1 Preflight & Vision Budget Contract
1. Initialize or inspect the target monument:
   ```powershell
   py scripts/autonomous_orchestrator.py --preflight --monument <ID>
   ```
2. This writes `<workspace>/Audit_Reports/phase0_preflight_brief.json` containing:
   - `max_vision_leaves = 8` and `max_vision_batches = 2`
   - Genre-scaffolded `recommended_publication_spec` from `data/templates/publication_spec_scaffolds.json`
   - Physical scan orientation diagnostics
3. **Hard Phase 0 Argon Vision Budget Cap (`<= 8` Leaves / `<= 2` Batches)**:
   - **Batch 1 (Front Bookend — Max 5 Leaves)**: `Page_0001.jpg` through `Page_0005.jpg` (cover, title page, frontispieces, preface/TOC opening, first text leaf).
   - **Batch 2 (Rear Bookend — Max 3 Leaves)**: `Page_(N-2).jpg` through `Page_N.jpg` (closing colophon, rear index/table, final folio).
   - **Absolute Ban on Mid-Codex Visual Binary Searches**: Inspecting internal leaves `p6` through `p(N-3)` during Phase 0 to hunt for internal section/Tone boundaries is strictly prohibited. Phase 1 `Flash` workers emit canonical H1 headings (`# TONE N`, `# PART ...`) when encountered on the physical page, and Phase 2 (`--compile-publication`) binds `start_landmark` regexes against actual translated headings on disk.
4. **Scan Orientation Normalization (`--rotate-jpgs`)**:
   - If Batch 1 reveals rotated physical scans (`90°`, `180°`, or `270°`), normalize the entire JPG vault upfront before unlocking Phase 1:
     ```powershell
     py scripts/autonomous_orchestrator.py --rotate-jpgs 90 --monument <ID>
     ```

### 1.2 Gate 0 Primary Source Suitability Check & Fast-Fail Deferral (`--defer-monument`)
- Immediately after inspecting Batch 1 (`p1`–`p5`), if the source PDF is discovered to be a modern excerpted edition, secondary academic monograph, or severely defective/truncated scan rather than a complete historical codex:
  1. **Halt further image inspection immediately** (do not read Batch 2 or write a translation plan).
  2. Report the Gate 0 defect to the human operator.
  3. Upon confirmation, execute:
     ```powershell
     py scripts/autonomous_orchestrator.py --defer-monument --monument <ID> --reason "<Defect Summary>"
     ```
  4. This marks the monument `"status": "failed"` (`"wave": 5`), moves it to the back of `Liturgical Monuments/codex_registry.json`, and emits the next monument's Rule 19 onboarding prompt.

### 1.3 Phase 0 → Phase 1 Circuit-Breaker (`--unlock-flash-sprint`)
- `prepare_cohort()` and `--step` are programmatically blocked from emitting a Cohort 1 subagent manifest while `small_pause_gate_status == "PHASE_0_ARGON_PLANNING_LOCKED"`.
- After the human operator approves `implementation_plan.md` and switches the Main Window UI dropdown from `Argon` → `Gemini 3.8 Flash`, unlock the sprint:
  ```powershell
  py scripts/autonomous_orchestrator.py --unlock-flash-sprint --monument <ID>
  ```

---

## 2. Phase 1: Unattended Flash Sprint (`PHASE_1_FLASH_SPRINT` — `Gemini 3.8 Flash`)

### 2.1 Lean Custom Worker Subagent (`ephemeral_translator`)
- Define via `define_subagent` (`EnableWriteTools=True`, `EnableSubagentTools=False`, `EnableMCPTools=False`) and invoke with `Model="flash"` strictly locked across 100% of Phase 1 cohorts and retries (zero silent mid-sprint `"pro"` overrides).
- Runtime tool calls are enforced by `.agents/scripts/governance_gate.py` (`PreToolUse` hook):
  1. Blocks `search_web` (`Rule 1` & `Rule 16`).
  2. Blocks `.py` generator script creation (`SGC-01A`) and restricts file writes strictly to `Source Text/`, `Draft/`, `Audit_Reports/`, `scratch/`, or `.gemini/antigravity/brain/`.
  3. Blocks network queries, orthographic regex gaming (`от` → `ѿ`), and execution of engine gate scripts via `run_command`.

### 2.2 Automated `argon_review_queue.json` Collector (4 Signals)
`scripts/run_small_pause_gate.py` scans every `=== LEAF pN ===` block and queues a leaf into `Audit_Reports/argon_review_queue.json` on 4 signals:
1. **Epigraphic uncertainty / lacuna markers**: `[?]`, `[illegible]`, `[lacuna]`, `[damaged]`, `[corrupt]`.
2. **Borderline `SGC-02` draft-to-source length ratios**: `< 0.50` or `> 2.20` on non-sparse leaves (or genre-specific `sgc02_min_ratio` / `sgc02_max_ratio` in `publication_spec_scaffolds.json`).
3. **High-complexity tables or apparatus**: `>= 5` Markdown table rows or `>= 5` footnotes on a single leaf (`>= 8` / `>= 10` for 2-up spreads per genre policy).
4. **Quarantined leaves**: `status="QUARANTINED_FOR_ARGON"` after retry exhaustion.

### 2.3 Two-Tier Unattended Flash Resilience & 4-Part Self-Healing
When `--verify-cohort --monument <ID>` runs:
1. **Tier 1 (`attempt_deterministic_self_healing()`)**:
   - Normalizes `=== LEAF pN ===` banners.
   - Migrates accidentally inlined `[^N]:` footnote definitions from body prose into the cohort footnotes file and re-indexes monotonic sequences.
   - Applies 1-to-1 forbidden vocabulary, `-eth` verb, and Father Paul Doxology replacements.
   - Applies deterministic Holy Trinity Deity pronoun capitalization.
2. **Tier 2 (Single Targeted `Flash` Retry + Quarantine Continuation)**:
   - If a gate failure remains after Tier 1, the orchestrator allows **1 targeted `Flash` subagent retry**.
   - If a content, linter, ratio, or footnote anomaly still persists after 1 retry, as long as all expected physical `=== LEAF pN ===` boundaries exist on disk, the offending leaf(s) are quarantined into `argon_review_queue.json` (`status="QUARANTINED_FOR_ARGON"`) and Phase 1 continues auto-chaining non-stop.
   - Hard-stops (`BLOCKED`) occur only if physical files or `=== LEAF pN ===` boundaries are missing.

---

## 3. Phase 2: Argon Deep Audit & Grand Pause Sealing (`Gemini 4 Argon (High)`)

1. **Transition to Phase 2**:
   - When `remaining_pages == 0`, the orchestrator halts at `AWAITING_ARGON_POST_SPRINT_AUDIT` so the operator can switch the Main Window UI dropdown from `Flash` → `Gemini 4 Argon (High)`.
2. **Deep Audit Execution (`--run-argon-audit`)**:
   ```powershell
   py scripts/autonomous_orchestrator.py --run-argon-audit --monument <ID>
   ```
   - Resolves `argon_review_queue.json` directly in parent `Argon` if `<= 5` leaves, or via batched `Model="inherit"` `Argon` subagents of `<= 8` leaves if `> 5` leaves, then re-verifies touched cohorts.
3. **Canonical Publication Compilation (`--compile-publication`)**:
   ```powershell
   py scripts/autonomous_orchestrator.py --compile-publication --monument <ID>
   ```
   - Gated on `unresolved_quarantines == 0`. Runs `UniversalPublicationEngine` (`scripts/compile_final_edition.py`) and 6-Gate LCPE verification (`scripts/verify_publication_edition.py`).
4. **Sovereign Grand Pause & Automated Sealing (`--approve-grand-pause`)**:
   ```powershell
   py scripts/autonomous_orchestrator.py --approve-grand-pause --monument <ID>
   ```
   - Re-verifies `unresolved_quarantines == 0`, publication edition integrity, and leaf conservation.
   - Copies sealed deliverables to `../Typikon Coded/Data/Inbox/` and updates `handoff_note.md`.
   - Stages and commits scoped monument paths (`feat(<monument>): seal canonical publication edition (leaves 1..N)`) and pushes to `origin master`.
   - Emits the next monument's Rule 19 copy-pasteable `[/plan](slashCommand;plan)` startup prompt and **retires the current chat session**.

---

## 4. Multi-Monument Sequestered Concurrency Protocol

- **Explicit Target Binding (`--monument <ID>`)**: Every mutating orchestrator and gate CLI call MUST pass `--monument <ID>` (or set `$env:ACTIVE_MONUMENT_ID="<ID>"`).
- **Disambiguation Circuit-Breaker (`[DISAMBIGUATION REQUIRED]`)**: When `>= 2` monuments hold `active_lease=True`, calling any mutating script without `--monument <ID>` or `ACTIVE_MONUMENT_ID` raises `RuntimeError("[DISAMBIGUATION REQUIRED]...")`. Calling read-only `py scripts/autonomous_orchestrator.py --status` displays the **Parallel Sequestered Monuments Telemetry Dashboard**.
- **Lease Lifecycle Commands**:
  - Claim next unclaimed `"ready"` monument: `py scripts/autonomous_orchestrator.py --claim-next-monument`
  - Pause active lease: `py scripts/autonomous_orchestrator.py --pause-monument --monument <ID>`
  - Resume paused lease: `py scripts/autonomous_orchestrator.py --resume-monument --monument <ID>`
- **Cross-Process Locking (`scripts/concurrency_lock.py`)**: Protects `Liturgical Monuments/codex_registry.json`, `CHRONICLE.md`, `ACTIVE_ORCHESTRATOR_STATE.json`, `scratch/triage_inbox.jsonl`, and `.git/index`. Grand Pause commits use `git commit --only ... -- <scoped_paths>`.
