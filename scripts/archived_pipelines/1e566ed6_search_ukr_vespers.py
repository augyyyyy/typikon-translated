import os

path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\Typyk_UHKC_ukr_utf8.txt"
if not os.path.exists(path):
    print("File does not exist")
    sys.exit()

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
found = False
for idx, line in enumerate(lines):
    if "Мала вечірня" in line or "Малої вечірні" in line or "малу вечірню" in line:
        if "Зміст" in line or "ЗМІСТ" in line or idx < 300: # skip TOC
            continue
        print(f"--- Match at line {idx+1} ---")
        start = max(0, idx - 10)
        end = min(len(lines), idx + 15)
        for j in range(start, end):
            print(f"{j+1}: {lines[j]}")
        found = True

if not found:
    print("No match found")
