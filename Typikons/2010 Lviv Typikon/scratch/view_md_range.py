from pathlib import Path

md_lines = Path('Final MD/Final_Dolnytsky_part3_menaion.md').read_text(encoding='utf-8').splitlines()

def print_md_range(start_kw, end_kw):
    start = -1
    end = -1
    for i, l in enumerate(md_lines):
        if start == -1 and start_kw.lower() in l.lower():
            start = max(0, i-1)
        if start != -1 and end_kw.lower() in l.lower():
            end = min(len(md_lines), i+3)
            break
    print(f"\n===== MD RANGE: {start_kw} to {end_kw} (L{start+1} - L{end}) =====")
    for j in range(start, end):
        print(f"MD L{j+1}: {md_lines[j]}")

print_md_range("### 3.1.2", "### 3.1.7")
print_md_range("### 3.1.7", "### 3.1.8")
print_md_range("### 3.1.9", "### 3.2.4")
print_md_range("### 3.2.4", "### 3.3.1")
