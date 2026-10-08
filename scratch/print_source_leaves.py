import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

src = Path("Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Source Text/1888_violakis_typikon_cohort45_source.txt").read_text(encoding='utf-8')

leaves = re.split(r"(=== LEAF p\d{3} ===\n)", src)
for i in range(1, len(leaves), 2):
    header = leaves[i].strip()
    body = leaves[i+1].strip()
    print(f"==================== {header} ====================")
    print(body[:600])
    print("...\n[Last 200 chars:]\n" + body[-200:] if len(body) > 600 else "")
