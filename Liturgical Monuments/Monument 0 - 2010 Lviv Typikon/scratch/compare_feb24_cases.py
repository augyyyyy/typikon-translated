from pathlib import Path

txt_lines = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8').splitlines()
md_lines = Path('Final MD/Final_Dolnytsky_part3_menaion.md').read_text(encoding='utf-8').splitlines()

# Print Case headers in TXT
for i in range(1240, 1420):
    l = txt_lines[i]
    if any(l.startswith(f"{n}. FINDING") for n in range(1, 13)):
        print(f"TXT L{i+1}: {l}")

print("\n--- Searching MD for Case mentions ---")
for i in range(2540, 2820):
    l = md_lines[i]
    if 'finding' in l.lower() or 'case' in l.lower() or 'cheesefare' in l.lower():
        print(f"MD L{i+1}: {l[:80]}")
