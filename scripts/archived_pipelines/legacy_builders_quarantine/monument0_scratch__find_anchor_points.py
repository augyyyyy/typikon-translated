#!/usr/bin/env python3
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = Path(__file__).resolve().parent.parent / "Final" / "Final_Dolnytsky_appendix.txt"
with open(app_path, "r", encoding="utf-8") as f:
    text = f.read()

points = [
    "51. For the Entrance",
    "71. Then, during the procession",
    "72. At the blessing of loaves",
    "all stand on the sides of the tetrapod in two rows",
    "In the narthex all stand before the closed",
    "One of the soldiers",
    "194.",
    "195.",
    "southern side",
    "208."
]

for p in points:
    idx = text.find(p)
    if idx != -1:
        snippet = text[max(0, idx-20):min(len(text), idx+140)].replace("\n", " // ")
        print(f"FOUND: '{p}' -> {snippet}\n")
    else:
        print(f"NOT FOUND: '{p}'\n")
