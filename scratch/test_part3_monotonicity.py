import re
from pathlib import Path

for path_str in ['Final/Final_Dolnytsky_part3_menaion.txt', 'Final MD/Final_Dolnytsky_part3_menaion.md']:
    p = Path(path_str)
    text = p.read_text(encoding='utf-8')
    matches = [(m.start(), int(m.group(1))) for m in re.finditer(r'\[\^(\d+)\]', text)]
    print(f"\n=== Footnotes in {path_str} (Total: {len(matches)}) ===")
    
    # Check counts
    counts = {}
    for pos, fn in matches:
        counts[fn] = counts.get(fn, 0) + 1
    
    dupes = {fn: c for fn, c in counts.items() if c > 1}
    if dupes:
        print(f"Duplicates: {dupes}")
    else:
        print("No duplicates!")

    # Check order around 240-285
    filtered = [(pos, fn) for pos, fn in matches if 240 <= fn <= 285]
    print(f"Footnotes in range 240-285: {[fn for _, fn in filtered]}")
