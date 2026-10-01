txt_path = "Typyk_UHKC_ukr.txt"

with open(txt_path, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

matches = []
for idx, line in enumerate(lines):
    line_lower = line.lower()
    if "xxxi" in line_lower or "додатк" in line_lower:
        # Save line with context (2 lines before and after)
        start = max(0, idx - 2)
        end = min(len(lines), idx + 3)
        context = "\n".join(f"L{i}: {lines[i]}" for i in range(start, end))
        matches.append(f"Match at Line {idx}:\n{context}\n" + "="*50 + "\n")

out_path = "ukr_appendix_search.txt"
with open(out_path, 'w', encoding='utf-8') as out_f:
    out_f.writelines(matches)

print(f"Wrote {len(matches)} matches to {out_path}")
