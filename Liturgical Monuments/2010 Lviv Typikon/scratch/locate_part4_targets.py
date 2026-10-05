import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent.parent

txt_path = root / "Final/Final_Dolnytsky_part4_triodion.txt"
md_path = root / "Final MD/Final_Dolnytsky_part4_triodion.md"

txt_lines = txt_path.read_text(encoding='utf-8').splitlines()
md_lines = md_path.read_text(encoding='utf-8').splitlines()

queries = {
    502: "Canon of the Theotokos",
    516: "Martyric Sessional Hymn of the Octoechos",
    518: "Great Compline",
    519: "to the end of Vespers",
    545: "Kondakion of the Triodion",
    547: "current tone the second",
    561: "Glory to Thee, our God, glory to Thee",
    576: "GREAT THURSDAY",
    579: "More honorable",
    640: "Week of Thomas and Mid-Pentecost",
    643: "Leavetaking of the Resurrection"
}

for fid, q in queries.items():
    print(f"=== FN {fid} (query: '{q}') ===")
    print(" TXT matches:")
    for idx, l in enumerate(txt_lines):
        if q.lower() in l.lower():
            print(f"  L{idx+1:4d}: {l[:110]}")
    print(" MD matches:")
    for idx, l in enumerate(md_lines):
        if q.lower() in l.lower():
            print(f"  L{idx+1:4d}: {l[:110]}")
