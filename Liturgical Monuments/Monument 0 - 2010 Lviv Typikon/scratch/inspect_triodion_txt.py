import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

txt_lines = Path('Final/Final_Dolnytsky_part4_triodion.txt').read_text(encoding='utf-8').splitlines()

# Search for matches in txt:
queries = [
    "Have mercy on us, O God\", dismissal for the dead",
    "Lord, have mercy\" (40), \"Thou Who at all times",
    "4 Stichera of the Praises of the Fathers",
    "Trisagion with 3 prostrations, and after \"Our Father",
    "17th Kathisma (\"The Blameless\")",
    "It is a good thing\" once, Trisagion with \"Our Father",
    "To Thee belongs glory",
    "At the last sticheron of the Aposticha",
    "Lord, I have cried\" - in Tone 2, with the usual censing"
]

for q in queries:
    for idx, l in enumerate(txt_lines, 1):
        if q.lower() in l.lower():
            print(f"TXT L{idx}: {l[:75]}")
            for j in range(max(1, idx-2), min(len(txt_lines), idx+4)):
                print(f"   L{j}: {txt_lines[j-1][:75]}")
            print("-" * 50)
            break
