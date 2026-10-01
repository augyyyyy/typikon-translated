txt_path = "Typyk_UHKC_ukr.txt"

with open(txt_path, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

# Find the start of the TOC
start_idx = -1
for idx, line in enumerate(lines):
    if "ЗМІСТ" in line:
        start_idx = idx
        break

if start_idx == -1:
    start_idx = 0

# Extract from line 200 of TOC to line 350
toc_content_remaining = lines[start_idx+200:start_idx+350]

with open("ukr_toc_remaining.txt", 'w', encoding='utf-8') as out_f:
    out_f.write("\n".join(toc_content_remaining))

print(f"Extracted remaining TOC lines to ukr_toc_remaining.txt")
