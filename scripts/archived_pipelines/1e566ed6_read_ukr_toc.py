import re

txt_path = "Typyk_UHKC_ukr_utf8.txt"

with open(txt_path, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

# Search for structural words or common headers
toc_lines = []
for idx, line in enumerate(lines):
    line_stripped = line.strip()
    if any(keyword in line_stripped.upper() for keyword in ["ЗМІСТ", "ЧАСТИНА", "ГЛАВА", "УТРЕНЯ", "ВЕЧІРНЯ", "ЧАСИ"]):
        toc_lines.append(f"Line {idx}: {line_stripped}")

out_path = "ukr_toc_search.txt"
with open(out_path, 'w', encoding='utf-8') as out_f:
    out_f.write("\n".join(toc_lines))

print(f"Wrote {len(toc_lines)} lines containing keywords to {out_path}")
