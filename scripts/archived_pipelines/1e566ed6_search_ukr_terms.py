txt_path = "Typyk_UHKC_ukr.txt"

with open(txt_path, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

matches = []
for idx, line in enumerate(lines):
    line_lower = line.lower()
    if "питан" in line_lower:
        matches.append(f"Line {idx}: {line.strip()}")
    if "бічн" in line_lower:
        matches.append(f"Line {idx}: {line.strip()}")

# Filter for lines that might contain both or are near each other
with open("ukr_terms_search.txt", 'w', encoding='utf-8') as out_f:
    out_f.write("\n".join(matches))

print(f"Wrote {len(matches)} matching lines to ukr_terms_search.txt")
