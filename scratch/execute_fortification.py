import os
from pathlib import Path

def main():
    print("Executing DeepSeek-Perfected Fortification...")
    
    # 1. Update .agents/AGENTS.md
    agents_path = Path(".agents/AGENTS.md")
    agents_path.parent.mkdir(parents=True, exist_ok=True)
    
    agents_content = r"""# Translation Spoke Master Rules & Operational Standards

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
"""
    with open(agents_path, 'w', encoding='utf-8') as f:
        f.write(agents_content.strip() + "\n")
    print("Updated .agents/AGENTS.md")

    # 2. Update .agents/skills/liturgical_text_auditor/SKILL.md
    text_auditor_path = Path(".agents/skills/liturgical_text_auditor/SKILL.md")
    text_auditor_path.parent.mkdir(parents=True, exist_ok=True)
    text_auditor_content = """---
name: liturgical_text_auditor
description: Audits Ukrainian-to-English liturgical text translations, ensuring 1:1 segment alignment and checking for missing sentences, semantic inaccuracies, or glossary drift.
---

# Liturgical Text Auditor Skill Guidelines

When executing a text audit or translation verification:

## 1. UGCC Authority Decision 0 – The "1899 Edition" Hallucination
The agent must never cite or infer textual authority from a "1899 edition" of the Sluzhebnik or any UGCC liturgical book. The only authorised printed sources are the **Sluzhebnik (1905 Lviv Stauropegion edition)**, the **Tserkovne Oko (1910 Zhovkva edition)**, and the official **Synodal texts of the UGCC** as digitised by the project. Any query for variant readings must default to these sources. If a user mentions "1899", the agent must immediately clarify that no such liturgical edition exists in UGCC tradition and must request the intended reference (likely a typographical error for 1905).

## 2. Text Parsing Guard
When parsing liturgical text files (e.g., `*.txt` outputs of OCR), use only **line-prefixed markers** with `str.startswith()` and `str.endswith()`. For example, a rubric line is identified by `line.startswith('[RUBRIC] ')`. Regular expressions are prohibited for identifying section boundaries because they have historically matched inside rubrics, leading to false-positive splits. If a new marker is needed, it must be registered in the glossary's allowed prefixes list.

## 3. Chunk Boundary Rules & Semantic Alignment
* Compare original Ukrainian segments with English translations.
* Align segments by heading levels (`###`) or itemized lists (`1.`, `2.`, `3.`). Do not use character-based chunking that cuts sentences in half.
* Keep context boundaries under 15,000 characters. For large sections, split dynamically at sentence boundaries (`. `, `? `, `! ` followed by a space).

## 4. DeepSeek v4 Pro Orchestration
* Run text audits with model `deepseek-v4-pro`.
* If reasoning is enabled (default), do not supply legacy parameters like `temperature` or `top_p`.
* Capture the reasoner's output and log it separately inside a `<details><summary>DeepSeek R1 Chain-of-Thought Reasoning</summary>...</details>` markdown block.

## 5. Discrepancy Flagging Protocol
Ensure the model checks for and reports:
1. **Dropped Concepts / Sentences**: Any sentence in the Ukrainian primary source that is absent in the English translation.
2. **Glossary Violations**: Use of forbidden terminology variants (e.g. "Trephologion" instead of canonical **Anthologion**).
3. **Deity Pronoun Capitalization**: Verify all divine addresses (He, Him, His, Who) are capitalized, while others are lowercase.
4. **Footnote Reference Integrity**: Validate that footnote markers in the text correctly match the references.
"""
    with open(text_auditor_path, 'w', encoding='utf-8') as f:
        f.write(text_auditor_content.strip() + "\n")
    print("Updated .agents/skills/liturgical_text_auditor/SKILL.md")

    # 3. Update .agents/skills/liturgical_vision_auditor/SKILL.md
    vision_auditor_path = Path(".agents/skills/liturgical_vision_auditor/SKILL.md")
    vision_auditor_path.parent.mkdir(parents=True, exist_ok=True)
    vision_auditor_content = """---
name: liturgical_vision_auditor
description: Audits final English translations against original page-scan images (JPG/PDF) to evaluate layout, heading levels, table structures, en/em dash consistency, and visual footnote positioning.
---

# Liturgical Vision Auditor Skill Guidelines

When executing a visual page scan audit:

## 1. Audit Log Integrity & Visual Log Limits
When interpreting the output of `liturgical_vision_auditor` scripts that produce an audit log, the agent must **not** infer missing entries, interpolate "invisible" elements, or fabricate bounding-box coordinates. If the log reports zero matches for a category the agent expected, it must **explicitly state** that detection failed for that category and **persist this empty result** in any summary. Ghost loops (re-running the detector endlessly because the expected count was not reached) are forbidden; after a maximum of 3 retries, the agent must report the discrepancy and stop. Limit visual screenshots of diffs to 50 per run to prevent disk exhaustion.

## 2. Absolute Path Checks for Image Loaders
All image-loading utilities within the auditor (e.g., `load_image()`) must resolve paths using `pathlib` relative to the project root or an environment-defined data directory. Any hardcoded absolute path in a loader is an immediate regression. Before running a detection, the agent should verify that the loaded image path does not contain a drive letter or known user-specific prefix.

## 3. Footnote Placement Validation
* Visually match footnote markers (e.g. `[^N]`) in the English draft against their physical positions in the page scan.
* Ensure no footnotes are dropped or detached from their corresponding paragraphs.
* Verify the master footnotes file (`Final_footnotes.txt`) contains the definition for every visual footnote present on the page.

## 4. Formatting & Typography Guidelines
* Check heading structures (bolding, italics, underlines) to make sure they correspond to the formatting style of the source scans.
* Ensure proper en dashes (` – `) or em dashes (` — `) are used for sentence ranges and breaks, replacing standard hyphens (`-`).
* Ensure tables are formatted consistently as Markdown tables, preserving original layouts.
"""
    with open(vision_auditor_path, 'w', encoding='utf-8') as f:
        f.write(vision_auditor_content.strip() + "\n")
    print("Updated .agents/skills/liturgical_vision_auditor/SKILL.md")

    # 4. Update .agents/skills/poetic_hymn_translator/SKILL.md
    poetic_translator_path = Path(".agents/skills/poetic_hymn_translator/SKILL.md")
    poetic_translator_path.parent.mkdir(parents=True, exist_ok=True)
    poetic_translator_content = """---
name: poetic_hymn_translator
description: Performs poetic and singable translations of Church Slavonic hymns (Sessional Hymns, Exapostilaria) to English, using Byzantine Greek as a semantic anchor while preserving Slavonic meter, phrasing, and syllable counts.
---

# Poetic Hymn Translator Skill Guidelines

When translating liturgical hymns poetically:

## 1. UTF-8 Strictness
All binary-to-text conversions (e.g., loading hymn plain-text from legacy file formats, reading API responses) must use `encoding='utf-8'` with `errors='strict'`. If a file is suspected of non-UTF-8 encoding, the translator must fall back to `chardet.detect()` or abort and log an explicit warning. Under no circumstances may an empty string or garbled text be silently substituted.

## 2. API Key and Configuration Loading
API key loader functions must exclusively read credentials from environment variables or a configuration file whose location is set via environment variable. Hardcoded filesystem paths for secrets are strictly prohibited and will be flagged by the anti-pattern searcher.

## 3. The Dual-Source Principle
* **Greek Source**: Use the Greek Menaion to establish the exact theological and semantic meaning, metaphors, and doctrinal nuances.
* **Slavonic Source**: Use the Church Slavonic text (e.g. Pochaiv 1761) to map English syllables, accentuation patterns, and sentence lengths. The target English text should align with the Slavonic structure to preserve singability and rhythm.

## 4. Metrical & Chant Formatting
* Do not force literal translations if they compromise poetic meter or rhythm.
* Insert musical breath marks and phrasing indicators (`*`) to show where cantors should pause or breathe.
* Translate the standard doxology exactly as: *"Glory be to the Father and to the Son and to the Holy Spirit, now and forever and unto the ages of ages. Amen."*
"""
    with open(poetic_translator_path, 'w', encoding='utf-8') as f:
        f.write(poetic_translator_content.strip() + "\n")
    print("Updated .agents/skills/poetic_hymn_translator/SKILL.md")

    # 5. Update .agents/skills/liturgical_glossary_enforcer/SKILL.md
    glossary_enforcer_path = Path(".agents/skills/liturgical_glossary_enforcer/SKILL.md")
    glossary_enforcer_path.parent.mkdir(parents=True, exist_ok=True)
    glossary_enforcer_content = """---
name: liturgical_glossary_enforcer
description: Scans English draft translations to enforce canonical UGCC terminology from the Master Glossary, flag forbidden variants, and verify proper Deity pronoun capitalization.
---

# Liturgical Glossary Enforcer Skill Guidelines

When executing a glossary or capitalization check:

## 1. Forbidden Colon-Split Rule
When parsing glossary entries or liturgical files, never split on colons (`:`) without proper context, because many UGCC terms and titles themselves contain colons (e.g., "Hlas 1: Podoben: ..."). Use a dedicated parser that relies on indentation or explicit delimiters. Any automatic ":-split" heuristic on liturgical lines is prohibited.

## 2. Master Glossary Alignment
* Ensure standard liturgical terms are mapped exactly to canonical variants.
* **Liturgical Books & Documents**:
  * *Церковне Око* → **Tserkovne Oko** (Forbidden: Eye of the Church, Oko Tserkovne)
  * *Трефологіон / Антологіон* → **Anthologion** (Forbidden: Trephologion)
  * *Служебник* → **Sluzhebnik** (Forbidden: Service Book when standalone)
* **Services & Hours**:
  * *Всенічне* → **All-Night Vigil** (Forbidden: Vsenichne)
  * *Повечір'я* → **Compline** (Forbidden: Povechiria)
  * *Обідниця* → **Typika** (Forbidden: Obidnytsia)
* **Hymnography**:
  * *Сідален* → **Sessional Hymn** (Forbidden: Kathisma)
  * *Самогласен* → **Idiomelon** (Forbidden: Samohlasen)
  * *Подібен* → **Prosomoion** (Forbidden: Podiben)
  * *Ірмос* → **Heirmos** / **Heirmoi** (Forbidden: Irmos)
  * *Прокімен* → **Prokimenon** / **Prokimena** (Forbidden: Prokeimenon)
  * *Катізма* → **Kathisma** (Forbidden: Kafisma)

## 3. Deity Capitalization Rules
* Capitalize all pronouns (He, Him, His, Who, Whom, Thee, Thou, Thy, Thine) referring to the Deity (God, Father, Son, Holy Spirit).
* Capitalize divine titles and names.
* Ensure pronouns referring to the Theotokos (Virgin Mary), angels, saints, or human participants remain lowercase.
"""
    with open(glossary_enforcer_path, 'w', encoding='utf-8') as f:
        f.write(glossary_enforcer_content.strip() + "\n")
    print("Updated .agents/skills/liturgical_glossary_enforcer/SKILL.md")
    
    print("Fortification complete!")

if __name__ == "__main__":
    main()
