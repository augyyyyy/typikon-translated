from pathlib import Path

txt_lines = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8').splitlines()
md_lines = Path('Final MD/Final_Dolnytsky_part3_menaion.md').read_text(encoding='utf-8').splitlines()

target_dupes = [409, 412, 417, 418, 426, 438]

print("=== PART 3 TXT DUPLICATE LOCATIONS ===")
for fn in target_dupes:
    matches = [(i+1, l) for i, l in enumerate(txt_lines) if f"[^{fn}]" in l]
    print(f"\nFN {fn}: {len(matches)} occurrences in TXT")
    for l_num, line in matches:
        print(f"  L{l_num}: {line[:90]}")

print("\n=== PART 3 MD DUPLICATE LOCATIONS ===")
for fn in target_dupes:
    matches = [(i+1, l) for i, l in enumerate(md_lines) if f"[^{fn}]" in l]
    print(f"\nFN {fn}: {len(matches)} occurrences in MD")
    for l_num, line in matches:
        print(f"  L{l_num}: {line[:90]}")
