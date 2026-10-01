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
    print("Could not find ЗМІСТ (TOC)")
    start_idx = 0

# Extract 200 lines from the start of the TOC
toc_content = lines[start_idx:start_idx+200]

with open("ukr_toc_extracted.txt", 'w', encoding='utf-8') as out_f:
    out_f.write("\n".join(toc_content))

print(f"Extracted {len(toc_content)} lines starting from line {start_idx} to ukr_toc_extracted.txt")
