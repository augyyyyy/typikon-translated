import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

src = Path("Liturgical Monuments/Monument 5 - 1888 Violakis Typikon/Source Text/1888_violakis_typikon_cohort45_source.txt").read_text(encoding='utf-8')

leaves = re.split(r"(=== LEAF p\d{3} ===\n)", src)
leaf_dict = {}
for i in range(1, len(leaves), 2):
    header = leaves[i].strip()
    m = re.search(r"p(\d+)", header)
    p_num = int(m.group(1))
    body = leaves[i+1].strip()
    leaf_dict[p_num] = body

for p in range(441, 451):
    print(f"*********************************** LEAF p{p} ***********************************")
    print(leaf_dict[p])
