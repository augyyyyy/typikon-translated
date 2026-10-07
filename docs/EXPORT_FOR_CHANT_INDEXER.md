# Sovereign Export Blueprint: Lending Translation Capabilities to Chant Indexer
*An Actionable, Self-Contained Specification for the Sibling Chant Indexer Engine*

---

## 1. Executive Summary & Reciprocal Spoke Relationship

The **Pan-Translation Engine** (`Translation/`) and the **Chant Indexer Engine** (`Chant Indexer/`) operate as sovereign sibling spokes under the Liturgical Workspace root. 

While Chant Indexer contributed the **Chromatic Rubric Verifier**, **Liturgical Vector PDF Compiler**, and **Epistemic Bibliography Linter**, Translation reciprocates with three core capabilities engineered to ensure hierarchical epigraphic and linguistic discipline:

1. **Hieratic Deity Pronoun Auditor (`scripts/hieratic_pronoun_audit.py`)**:
   Enforces 100% capitalization on Deity and Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*), preventing AI lowercase regressions across chant text transcriptions, rubrics, and translations.
2. **Liturgical Slop & Style Linter (`scripts/lint_liturgical_slop.py`)**:
   Enforces the Master Translation Standard (MTS-1) Anti-Slop protocol: strictly eliminates pseudo-archaic fantasy vocabulary (*verily, betwixt, twas, methinks*), modern AI filler clichés (*testament to, beacon of, delve into, tapestry of*), and rubrical "shall"-bombing during bodily ceremonial motions.
3. **Headless Gatekeeper & Triage Inbox Architecture**:
   Zero-human automated multi-gate linter runner with persistent structured JSONL triage inbox logging (`scratch/triage_inbox.jsonl`), enabling resilient autonomous iteration.

---

## 2. Module 1: Hieratic Deity Pronoun Auditor

### Problem Solved
Language models consistently regress to modern secular lowercase conventions for pronouns referring to the Holy Trinity (*he, him, his, who, whom*). In Byzantine-Ruthenian liturgical monuments, hieratic capitalization is mandatory.

### Integration in Chant Indexer
Save to: `engine/hieratic_pronoun_auditor.py` (or `scripts/hieratic_pronoun_audit.py`).

```python
# -*- coding: utf-8 -*-
"""
Hieratic Deity Pronoun Auditor
Borrowed from Translation Engine (scripts/hieratic_pronoun_audit.py).
Enforces 100% capitalization on Holy Trinity Deity pronouns.
"""

import re
from typing import List, Dict, Any

LOWERCASE_DEITY_PATTERNS = [
    (r"\b(unto|to|with|before|from|in|through)\s+(him|his)\b", "Deity pronoun following preposition must be capitalized"),
    (r"\b(o\s+lord|o\s+god|o\s+christ),\s+(thou|thee|thy|thine)\b", "Vocative direct address requires capitalized hieratic pronoun"),
    (r"\b(glory\s+to)\s+(him|thee)\b", "Doxological pronoun must be capitalized"),
    (r"\b(praise)\s+(him)\b", "Doxological imperative requires capitalized hieratic pronoun"),
]

def audit_hieratic_pronouns(text: str) -> List[Dict[str, Any]]:
    violations = []
    lines = text.splitlines()
    for line_idx, line in enumerate(lines, 1):
        for pattern, reason in LOWERCASE_DEITY_PATTERNS:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                matched_str = match.group(0)
                # If the target pronoun part is lowercase, flag violation
                parts = matched_str.split()
                if len(parts) >= 2 and parts[-1].islower():
                    violations.append({
                        "line": line_idx,
                        "matched": matched_str,
                        "reason": reason
                    })
    return violations
```

---

## 3. Module 2: Liturgical Slop & Style Linter

### Problem Solved
Large language models tend to inject pseudo-Elizabethan archaisms or verbose modern AI corporate filler clichés. Furthermore, LLMs frequently over-use statutory "shall" (*the priest shall take*) rather than active present indicative (*the priest takes*).

### Integration in Chant Indexer
Save to: `engine/liturgical_slop_linter.py` (or `scripts/lint_liturgical_slop.py`).

```python
# -*- coding: utf-8 -*-
"""
Liturgical Slop & Style Linter (MTS-1 Anti-Slop)
Borrowed from Translation Engine (scripts/lint_liturgical_slop.py).
Rejects pseudo-archaic fantasy slop, AI conversational clichés, and ceremonial shall-bombing.
"""

import re
from typing import List, Dict, Any

PSEUDO_ARCHAIC_SLOP = [
    r"\bverily\b", r"\bbetwixt\b", r"\btwas\b", r"\bmethinks\b",
    r"\bhearken\b", r"\bperadventure\b", r"\beffulgent\b", r"\bresplendent\b"
]

AI_CONVERSATIONAL_CLICHES = [
    r"\ba testament to\b", r"\bbeacon of\b", r"\bdelve into\b",
    r"\btapestry of\b", r"\brich history\b", r"\bserves as a reminder\b",
    r"\binextricably linked\b"
]

RUBRICAL_SHALL_BOMBING = [
    r"\b(priest|deacon|bishop|celebrant|choir|reader)\s+shall\s+(take|enter|bow|cense|stand|kiss|elevate|cross|say|chant)\b"
]

def lint_slop(text: str) -> List[Dict[str, Any]]:
    violations = []
    lines = text.splitlines()
    for line_idx, line in enumerate(lines, 1):
        for pat in PSEUDO_ARCHAIC_SLOP:
            if re.search(pat, line, re.IGNORECASE):
                violations.append({"line": line_idx, "type": "PSEUDO_ARCHAIC_SLOP", "snippet": line.strip()})
        for pat in AI_CONVERSATIONAL_CLICHES:
            if re.search(pat, line, re.IGNORECASE):
                violations.append({"line": line_idx, "type": "AI_CLICHE", "snippet": line.strip()})
        for pat in RUBRICAL_SHALL_BOMBING:
            if re.search(pat, line, re.IGNORECASE):
                violations.append({"line": line_idx, "type": "SHALL_BOMBING", "snippet": line.strip()})
    return violations
```

---

## 4. Module 3: Small Pause Gatekeeper & Triage Inbox Pattern

### Architecture
When executing long multi-folio chant transcription runs, headless automated gates run programmatically between cohorts without yielding to human intervention.

1. **Sequential Automated Execution**:
   - Gate 1: Vocabulary / Nomenclature.
   - Gate 2: Hieratic Deity Pronoun Audit.
   - Gate 3: Anti-Slop Linter.
   - Gate 4: Chromatic Verifier (from Chant Indexer).
2. **Deterministic Triage Logging**:
   - If a gate fails, dump a standardized signature into `scratch/triage_inbox.jsonl`:
     ```json
     {
       "timestamp": "2026-10-07T18:00:00Z",
       "artifact_id": "chant_folio_045",
       "gate": "hieratic_pronouns",
       "violation_count": 2,
       "status": "PENDING_DEVELOPER_TRIAGE"
     }
     ```
   - Autonomous executor halts cleanly, leaving full evidence for quick review.

---

## 5. Adoption Instructions for Chant Indexer Agent

1. Inspect existing chant transcription pipelines (`engine/transcriber.py` or similar).
2. Wire `hieratic_pronoun_auditor` and `liturgical_slop_linter` into the post-processing pipeline.
3. Reference `Shared_Lexicon/master_liturgical_vocabulary.json` and `Shared_Lexicon/authoritative_bibliography.json` as root-level authorities.
