import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

forbidden_patterns = [
    (r'\bService\s+Book\b', 'Service Book (use Sluzhebnik)'),
    (r'\bTrephologion\b', 'Trephologion (use Anthologion)'),
    (r'\bTrebnyk\b', 'Trebnyk (use Euchologion)'),
    (r'\bTypicon\b', 'Typicon (use Typikon)'),
    (r'\bIrmos\b', 'Irmos (use Heirmos)'),
    (r'\bIrmologion\b', 'Irmologion (use Heirmologion)')
]

final_md = Path('Final MD')
findings = []
for f in sorted(final_md.glob('*.md')):
    if 'glossary' in f.name:
        continue
    lines = f.read_text(encoding='utf-8').splitlines()
    for idx, l in enumerate(lines, 1):
        for pat, desc in forbidden_patterns:
            if re.search(pat, l, re.IGNORECASE):
                findings.append((f.name, idx, desc, l[:70]))

print(f"Total forbidden terminology instances found: {len(findings)}")
for fn, lno, desc, ctx in findings[:25]:
    print(f"  {fn}:L{lno} -> [{desc}] \"{ctx}\"")
