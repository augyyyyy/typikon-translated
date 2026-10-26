import sys
import re
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent

for mon_dir in sorted((PROJECT_ROOT / "Liturgical Monuments").glob("Monument *")):
    cohorts_dir = mon_dir / "Cohorts"
    if not cohorts_dir.exists():
        cohorts_dir = mon_dir / "Draft"
    if not cohorts_dir.exists():
        continue
    
    files = list(cohorts_dir.glob("*.md"))
    if not files:
        continue
        
    leaf_markers = set()
    for f in files:
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r'(?:\[[^\]]*(?:Page|Leaf|Folio|Blank)[^\]]*\]|<!--\s*LEAF[^>]*-->|===\s*LEAF[^=]+===|\*?\((?:Physical Page|Physical pp\.|Physical Leaf|Book Page|Leaf\s+p?|Blank)[^)]*\)\*?)', text, re.IGNORECASE):
            leaf_markers.add(m.group(0))
            
    print(f"{mon_dir.name}: {len(leaf_markers)} unique leaf marker strings")
    samples = sorted(list(leaf_markers))[:5]
    for s in samples:
        print(f"   {s}")
