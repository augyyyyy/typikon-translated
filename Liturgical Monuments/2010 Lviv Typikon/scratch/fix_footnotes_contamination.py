#!/usr/bin/env python3
"""
Prune Contaminated Footnotes in Final_footnotes.txt
===================================================
Removes accidentally appended Appendix Chunks 74, 75, and 77 from
Footnotes 763, 767, and 780, restoring them to their authentic definitions.
"""

from pathlib import Path
import re
import sys

def get_project_root() -> Path:
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "Final").exists():
            return parent
    return Path(__file__).resolve().parent.parent

def main():
    root = get_project_root()
    fn_path = root / "Final" / "Final_footnotes.txt"
    with open(fn_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig_len = len(content)
    print(f"Original Final_footnotes.txt length: {orig_len:,} characters")

    # 1. Clean Footnote 763
    clean_763 = '[^763]: These gifts are arranged according to such a scheme so that the blessing of the priest depicts upon them the sign of the cross: loaf • wine • • oil • wheat.'
    pat_763 = re.compile(r'\[\^763\]:.*?(?=\n\[\^764\]:)', re.DOTALL)
    if not pat_763.search(content):
        print("Error: Could not find Footnote 763 pattern")
        sys.exit(1)
    content = pat_763.sub(clean_763, content)

    # 2. Clean Footnote 767
    clean_767 = '[^767]: Such a shortening is generally practiced, therefore we present it here as an appendix.'
    pat_767 = re.compile(r'\[\^767\]:.*?(?=\n\[\^768\]:)', re.DOTALL)
    if not pat_767.search(content):
        print("Error: Could not find Footnote 767 pattern")
        sys.exit(1)
    content = pat_767.sub(clean_767, content)

    # 3. Clean Footnote 780
    clean_780 = '[^780]: This prayer is not read before the icon of the Savior, because it is -- "behind the ambo". Its content is directed to the "Father of Lights" (not to Christ), and the conclusion -- Trinitarian.'
    pat_780 = re.compile(r'\[\^780\]:.*?(?=\n\[\^781\]:)', re.DOTALL)
    if not pat_780.search(content):
        print("Error: Could not find Footnote 780 pattern")
        sys.exit(1)
    content = pat_780.sub(clean_780, content)

    new_len = len(content)
    pruned_bytes = orig_len - new_len
    print(f"New Final_footnotes.txt length: {new_len:,} characters")
    print(f"Successfully pruned {pruned_bytes:,} characters of redundant body text!")

    with open(fn_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Updated Final/Final_footnotes.txt successfully.")

if __name__ == "__main__":
    main()
