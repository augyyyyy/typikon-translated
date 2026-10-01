#!/usr/bin/env python3
"""
Clean contaminated footnotes 763, 767, 780 in Final MD/Final_footnotes.md
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

proj_root = Path(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation")
md_path = proj_root / "Final MD" / "Final_footnotes.md"

with open(md_path, "r", encoding="utf-8", newline="") as f:
    content = f.read()

crlf = "\r\n" if "\r\n" in content else "\n"

clean_replacements = [
    (
        763,
        764,
        f"[^763]: These gifts are arranged according to such a scheme so that the blessing of the priest depicts upon them the sign of the cross: loaf • wine • • oil • wheat.{crlf}{crlf}"
    ),
    (
        767,
        768,
        f"[^767]: Such a shortening is generally practiced, therefore we present it here as an appendix.{crlf}{crlf}"
    ),
    (
        780,
        781,
        f"[^780]: This prayer is not read before the icon of the Savior, because it is -- \"behind the ambo\". Its content is directed to the \"Father of Lights\" (not to Christ), and the conclusion -- Trinitarian.{crlf}{crlf}"
    )
]

print(f"Original Final MD/Final_footnotes.md size: {len(content)} chars")

for fn, next_fn, clean_text in clean_replacements:
    start_k = f"[^{fn}]:"
    end_k = f"[^{next_fn}]:"
    s_idx = content.find(start_k)
    e_idx = content.find(end_k)
    if s_idx != -1 and e_idx != -1:
        print(f"Cleaning FN {fn}: stripping {e_idx - s_idx} chars -> replacing with {len(clean_text)} chars")
        content = content[:s_idx] + clean_text + content[e_idx:]
    else:
        print(f"ERROR: Could not find markers for FN {fn}")

with open(md_path, "w", encoding="utf-8", newline="") as f:
    f.write(content)

print(f"Cleaned Final MD/Final_footnotes.md size: {len(content)} chars")
