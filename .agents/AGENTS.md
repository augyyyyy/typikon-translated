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

### 3. Liturgical Translation & Glossary Guardrails
* Divine addresses must be translated as "Thee," "Thou," "Thy," "Thine," etc., or follow local parish custom. Ensure pronoun capitalization rules are strictly checked (e.g. He, Him, His for the Deity).
* Ensure the canonical English terms in `SYSTEM_INSTRUCTIONS.md` are used, with zero tolerance for forbidden variants (e.g., *Sluzhebnik* must not be translated as generic "Service Book" when standalone).
* Reference the gold standard examples for detailed rubrics and footnote placements.

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
