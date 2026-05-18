#!/usr/bin/env python3
"""
Apply Cross-Reference Anchor Tags
===================================
Converts literal page references ("see the rule on p. 154") into
machine-parseable anchor tags:

    "see the rule on p. 154" → "see the rule on p. 154 [→REF:p154]"

Tag format: [→REF:pNNN] or [→REF:pNNN-NNN]

These tags use Dolnytsky's original 1899 pagination. When the document
is finally formatted, a script can resolve these into hyperlinks
or actual page numbers in the new edition.

This is ADDITIVE — the tag is appended, preserving fidelity to the source.
"""
import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

final_dir = r'e:\Google Antigravity\Projects\Translation\Final'

# Pattern to match page references WITHOUT an existing tag
# Matches: "on p. 154", "here on p. 157-158", "see p. 154", etc.
# Negative lookahead prevents double-tagging
page_ref_re = re.compile(
    r'((?:on|see|See)\s+(?:the\s+rule\s+)?(?:given\s+)?(?:before\s+)?(?:here\s+)?(?:on\s+)?(?:pp?\.\s*)(\d+(?:-\d+)?))'
    r'(?!\s*\[→REF:)'
)

total_tags = 0
for name in sorted(os.listdir(final_dir)):
    if not name.endswith('.txt'):
        continue
    filepath = os.path.join(final_dir, name)
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    original = text
    file_count = [0]  # mutable container for closure
    
    def add_tag(m):
        full_match = m.group(1)
        page_num = m.group(2)
        tag = f' [→REF:p{page_num}]'
        file_count[0] += 1
        return full_match + tag
    
    text = page_ref_re.sub(add_tag, text)
    
    if text != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'{name}: {file_count[0]} cross-reference tags added')
        total_tags += file_count[0]
    else:
        print(f'{name}: no changes')

print(f'\n=== TOTAL: {total_tags} cross-reference tags added ===')
