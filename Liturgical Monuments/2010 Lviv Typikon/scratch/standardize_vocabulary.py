#!/usr/bin/env python3
"""
Phase 1.5: Cross-Part Vocabulary Standardization
==================================================
All 5 parts + appendix were translated in separate AI chat instances,
leading to terminology drift. This script enforces a single vocabulary
across all files based on the master glossary.

Key fixes:
1. Leavetaking / Leave-taking → Apodosis  
2. Prokeimenon → Prokimenon
3. Irmos → Heirmos (standardize to scholarly transliteration)
4. Epitaphios → Shroud [Epitaphios]
5. Menaia → Menaia (keep as valid plural, but flag)
6. Theotokia → keep (valid plural)
7. Idiomela → keep (valid plural)
8. Prosomoia → keep (valid plural)
9. Deity pronoun capitalization (context-aware)
"""

import re
import os
import json

SCRATCH = r"e:\Google Antigravity\Projects\Translation\scratch"
REPORT_DIR = os.path.join(SCRATCH, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

FILES = [
    "STITCHED_v3_dolnytsky_part1_structure.txt",
    "STITCHED_v3_dolnytsky_part2_general_rubrics.txt",
    "STITCHED_v3_dolnytsky_part3_menaion.txt",
    "STITCHED_v3_dolnytsky_part4_triodion.txt",
    "STITCHED_v3_dolnytsky_part5_temple.txt",
    "STITCHED_v3_dolnytsky_appendix.txt",
]

# =============================================================================
# 1. TERM REPLACEMENTS (case-sensitive where needed)
# =============================================================================

# Simple word-boundary replacements (case-insensitive, preserve original casing pattern)
REPLACEMENTS = [
    # --- LITURGICAL TERMS ---
    # Apodosis: multiple wrong variants
    (r'\b[Ll]eavetaking\b', 'Apodosis'),
    (r'\b[Ll]eave-[Tt]aking\b', 'Apodosis'),
    (r'\b[Ll]eave [Tt]aking\b', 'Apodosis'),
    
    # Prokimenon: Greek transliteration variants
    (r'\bProkeimenon\b', 'Prokimenon'),
    (r'\bProkeimena\b', 'Prokimena'),  # plural form
    
    # Heirmos: standardize from "Irmos" to "Heirmos"
    # Must be careful not to match "Irmos" inside other words
    (r'\bIrmos\b', 'Heirmos'),
    (r'\bIrmoi\b', 'Heirmoi'),  # plural
    
    # Epitaphios: per glossary, should be "Shroud"
    # But keep the original in brackets for scholarly reference
    (r'\bEpitaphios\b', 'Shroud [Epitaphios]'),
    # Avoid double-bracketing if already done:
    # "Shroud [Epitaphios] [Epitaphios]" → catch later
    
    # --- LESS COMMON VARIANTS ---
    (r'\bLity\b', 'Litiya'),
    (r'\bLitia\b', 'Litiya'),
]

# Replacements that need more care (context-sensitive)
# These are applied after the basic ones
CONTEXT_REPLACEMENTS = [
    # Remove double-brackets from Shroud fix:
    # "Shroud [Epitaphios] [Epitaphios]" → "Shroud [Epitaphios]"
    (r'Shroud \[Epitaphios\] \[Epitaphios\]', 'Shroud [Epitaphios]'),
    # If "Shroud" was already present, don't get "Shroud [Epitaphios]" when
    # the original was already "Shroud [Epitaphios]" — this is a no-op
]


# =============================================================================
# 2. DEITY PRONOUN CAPITALIZATION
# =============================================================================

# Words that indicate a divine subject on the same line
DIVINE_INDICATORS = [
    r'\bGod\b', r'\bLord\b', r'\bChrist\b', r'\bJesus\b',
    r'\bSavior\b', r'\bSaviour\b', r'\bAlmighty\b',
    r'\bHoly Spirit\b', r'\bHoly Ghost\b',
    r'\bThou\b', r'\bThee\b', r'\bThy\b', r'\bThine\b',
    r'\bMost High\b', r'\bCreator\b', r'\bRedeemer\b',
    r'\bMaster\b',  # In liturgical context, often refers to God
]

# Pronouns to capitalize when in divine context
PRONOUNS_TO_CAP = {
    r'\bhe\b': 'He',
    r'\bhim\b': 'Him', 
    r'\bhis\b': 'His',
    r'\bwho\b': 'Who',
    r'\bwhom\b': 'Whom',
    r'\bhimself\b': 'Himself',
}

# Phrases where lowercase pronouns are about HUMANS, not God
# (to avoid over-capitalization)
HUMAN_EXEMPT = [
    r'the priest.*\b(he|him|his)\b',
    r'the deacon.*\b(he|him|his)\b',
    r'the reader.*\b(he|him|his)\b', 
    r'the server.*\b(he|him|his)\b',
    r'the bishop.*\b(he|him|his)\b',
    r'the saint.*\b(he|him|his)\b',
    r'who has\b',  # "who has" is usually relative, not divine
    r'who does\b',
    r'everyone who\b',
    r'one who\b',
    r'he who\b',  # ambiguous — skip
]


def is_divine_context(line):
    """Check if a line has divine subject indicators."""
    for pattern in DIVINE_INDICATORS:
        if re.search(pattern, line):
            return True
    return False


def is_human_ref(line, match_start, match_end):
    """Check if a pronoun match is likely referring to a human, not God."""
    # Get the text before the pronoun
    before = line[:match_start].lower()
    # Common patterns: "the priest... he" — pronoun refers to priest
    human_subjects = ['priest', 'deacon', 'reader', 'server', 'bishop', 
                       'celebrant', 'concelebrant', 'faithful', 'singer',
                       'cantor', 'psalmist', 'emperor', 'patriarch']
    # If the most recent noun-subject is a human, don't capitalize
    # Simple heuristic: find last occurrence of human vs divine subjects
    last_human = -1
    for h in human_subjects:
        idx = before.rfind(h)
        if idx > last_human:
            last_human = idx
    
    last_divine = -1
    for pattern in DIVINE_INDICATORS:
        for m in re.finditer(pattern.lower(), before):
            if m.end() > last_divine:
                last_divine = m.end()
    
    # If human subject is closer to the pronoun, it's likely human ref
    if last_human > last_divine:
        return True
    return False


def capitalize_deity_pronouns(text):
    """Context-aware capitalization of pronouns referring to God."""
    lines = text.split('\n')
    new_lines = []
    changes = 0
    
    for line in lines:
        if not is_divine_context(line):
            new_lines.append(line)
            continue
        
        new_line = line
        for pattern, replacement in PRONOUNS_TO_CAP.items():
            def replacer(m):
                nonlocal changes
                # Don't capitalize if it's likely a human reference
                if is_human_ref(new_line, m.start(), m.end()):
                    return m.group()
                # Don't capitalize at start of sentence (already handled)
                # Don't capitalize "who" in relative clauses about humans
                if replacement == 'Who' and m.start() > 0:
                    before = new_line[:m.start()].rstrip()
                    if before.endswith(',') or before.endswith('that'):
                        return m.group()  # relative clause
                changes += 1
                return replacement
            
            new_line = re.sub(pattern, replacer, new_line)
        
        new_lines.append(new_line)
    
    return '\n'.join(new_lines), changes


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("PHASE 1.5: CROSS-PART VOCABULARY STANDARDIZATION")
    print("=" * 80)
    
    report = {}
    
    for fname in FILES:
        fpath = os.path.join(SCRATCH, fname)
        if not os.path.exists(fpath):
            print(f"  SKIP: {fname}")
            continue
        
        print(f"\n--- Processing {fname} ---")
        
        with open(fpath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        original_len = len(text)
        file_changes = {}
        
        # Step 1: Apply term replacements
        for pattern, replacement in REPLACEMENTS:
            matches = list(re.finditer(pattern, text))
            if matches:
                count = len(matches)
                text = re.sub(pattern, replacement, text)
                file_changes[f"{pattern} → {replacement}"] = count
                print(f"  {pattern} -> {replacement}: {count} replacements")
        
        # Step 2: Context-sensitive fixes
        for pattern, replacement in CONTEXT_REPLACEMENTS:
            matches = list(re.finditer(re.escape(pattern) if not pattern.startswith('\\') else pattern, text))
            if matches:
                count = len(matches)
                text = text.replace(pattern, replacement)
                file_changes[f"context: {pattern[:30]}"] = count
        
        # Step 3: Deity pronoun capitalization
        text, pronoun_changes = capitalize_deity_pronouns(text)
        if pronoun_changes > 0:
            file_changes["deity_pronoun_caps"] = pronoun_changes
            print(f"  Deity pronoun capitalization: {pronoun_changes} changes")
        
        # Save
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        report[fname] = file_changes
    
    # Save report
    report_path = os.path.join(REPORT_DIR, "vocabulary_standardization.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Summary
    print(f"\n{'=' * 80}")
    print("VOCABULARY STANDARDIZATION COMPLETE")
    print(f"{'=' * 80}")
    
    total_changes = 0
    for fname, changes in report.items():
        file_total = sum(changes.values())
        total_changes += file_total
        print(f"  {fname}: {file_total} changes")
    print(f"  TOTAL: {total_changes} changes")
    print(f"\nReport: {report_path}")


if __name__ == '__main__':
    main()
