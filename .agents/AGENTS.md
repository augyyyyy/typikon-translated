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

