import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect the English text in Final_Dolnytsky_part3_menaion.txt
en_text = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8')
en_lines = en_text.splitlines()

# Test finding matching phrases for a few key footnotes:
test_queries = [
    (241, "Service of the Indiction"),
    (242, "Synaxis of the Most Holy Theotokos in Miasena"),
    (243, "from the canon to the end is Great"),
    (244, "Both now: to the Synaxis"),
    (245, "Both now: to the Indiction. Everything else"),
    (246, "on the 9th - Resurrectional"),
    (247, "Saturday before the Exaltation"),
    (254, "12 SEPTEMBER"),
    (258, "Lviv Synod allows dairy products"),
    (271, "decision of the Synod of Lviv"),
    (272, "If 11 October falls on a Sunday"),
    (278, "Philip's Fast")
]

for fn_id, q in test_queries:
    found = False
    for idx, l in enumerate(en_lines, 1):
        if q.lower() in l.lower():
            print(f"FN {fn_id} -> Found at L{idx}: {l[:80]}")
            found = True
            break
    if not found:
        print(f"FN {fn_id} -> NOT FOUND with query '{q}'")
