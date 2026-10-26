import sys
import re
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent

for mon_name, rel_path in [
    ("Monument 2 (Dolnytsky)", "Liturgical Monuments/Monument 2 - 1899 Dolnytsky Typikon/Final MD/1899_dolnytsky_typikon_complete.md"),
    ("Monument 1 (Lviv Synod)", "Liturgical Monuments/Monument 1 - 1891 Lviv Synod/Final MD/1891_lviv_synod_complete.md"),
    ("Monument 4 (Doskovsky)", "Liturgical Monuments/Monument 4 - 1852 Doskovsky Typikon/Final MD/1852_doskovsky_typikon_complete.md"),
]:
    fpath = PROJECT_ROOT / rel_path
    if not fpath.exists():
        continue
    text = fpath.read_text(encoding="utf-8")
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    cuts = []
    for i in range(len(paras)-1):
        curr = paras[i]
        nxt = paras[i+1]
        if curr.startswith("#") or nxt.startswith("#") or curr.startswith("|") or nxt.startswith("|"):
            continue
        core = re.sub(r'(?:\[\^\d+\]|[*_`"\'\”\’]|\s)+$', '', curr)
        if not core:
            continue
        if core[-1] not in ('.', '!', '?', ':', ';', '—', '-'):
            if not re.match(r'^(?:[-*+]\s+|\d+\.\s+|☞|☩|>\s*\*\*|\*\*)', nxt):
                cuts.append((core[-50:], nxt[:50]))
    print(f"{mon_name}: {len(cuts)} possible mid-sentence paragraph breaks")
    for c in cuts[:4]:
        print(f"  PRE:  ...{c[0]}")
        print(f"  POST: {c[1]}...")
        print("  ---")
