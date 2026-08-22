---
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
