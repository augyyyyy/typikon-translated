import sys
import re
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from scratch.test_multi_monument_stitcher import stitch_leaf_stream

mon_id = "1852_doskovsky_typikon"
cohorts_dir = PROJECT_ROOT / "Liturgical Monuments" / "Monument 4 - 1852 Doskovsky Typikon" / "Cohorts"
c_files = sorted(cohorts_dir.glob("*.md"), key=lambda f: int(re.search(r'cohort(\d+)', f.name).group(1)))
raw = "\n\n".join(cf.read_text(encoding="utf-8") for cf in c_files)

# Clean raw scaffolding
t = re.sub(r"^#+\s*.*?Cohort\s+\d+.*?\n+", "", raw, flags=re.MULTILINE | re.IGNORECASE)
t = re.sub(r"<!--\s*(?:START|END)?\s*COHORT.*?-->\n*", "", t, flags=re.IGNORECASE)
t = re.sub(r"##\s+Table of Contents\s*\n(?:[ \t]*[-*\d\.]+\s+.*?\(#.*?\)\s*\n)+", "", t, flags=re.IGNORECASE)
t = re.sub(r">\s*\[!NOTE\]\s*\n(?:>\s*.*?\n)+", "", t)
t = re.sub(r"##\s+(?:Scholarly Critical Apparatus & Footnotes|Footnotes)\s*\n(?:\[\^\d+\]:.*?\n*)+", "", t, flags=re.IGNORECASE)
t = re.sub(r"^#+\s*Cohort\s+\d+\s+Footnotes.*?\n*", "", t, flags=re.MULTILINE | re.IGNORECASE)

stitched, log = stitch_leaf_stream(t)

# Audit for any severed paragraphs
paras = [p.strip() for p in stitched.split('\n\n') if p.strip()]
cuts = []
for i in range(len(paras)-1):
    curr = paras[i]
    nxt = paras[i+1]
    if curr.startswith('#') or nxt.startswith('#') or curr.startswith('|') or nxt.startswith('|'):
        continue
    core = re.sub(r'(?:\[\^\d+\]|[\]\)\*_`"\'\”\’]|\s)+$', '', curr)
    if not core:
        continue
    if core[-1] not in ('.', '!', '?', ':', ';', '—', '-'):
        if not re.match(r'^(?:[-*+]\s+|\d+[\.)]\s+|☞|☩|>\s*\*\*|\*\*|>)', nxt):
            cuts.append((curr[-50:], nxt[:50]))

print(f"Remaining suspicious cuts in Monument 4: {len(cuts)}")
for c in cuts[:10]:
    print(f"  PRE:  ...{c[0]}")
    print(f"  POST: {c[1]}...")
    print("  ---")
