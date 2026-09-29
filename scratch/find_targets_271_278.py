import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

txt = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8')
lines = txt.splitlines()

targets = [
    (271, "Protection"),
    (272, "11 October falls on a Sunday"),
    (273, "sluzhebnyky"),
    (274, "earthquake"),
    (275, "earthquake"),
    (276, "weekday to Sunday"),
    (277, "Saint with Vigil"),
    (278, "Philip")
]

for fn_id, q in targets:
    found = False
    for idx, l in enumerate(lines, 1):
        if q.lower() in l.lower():
            print(f"FN {fn_id} ('{q}') -> L{idx}: {l[:85]}")
            found = True
            if fn_id not in [273, 274, 275]: # only print first match unless looking for specifics
                break
    if not found:
        print(f"FN {fn_id} ('{q}') -> NOT FOUND")
