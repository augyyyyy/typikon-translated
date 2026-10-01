import os
import re

txt_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\Typyk_UHKC_ukr.txt"
out_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\ukr_daily_matins.txt"

if not os.path.exists(txt_path):
    print("Ukrainian txt file not found!")
    exit(1)

with open(txt_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find matches for "ЧИН ПОВСЯКДЕННОЇ УТРЕНІ"
matches = list(re.finditer(r'ЧИН ПОВСЯКДЕННОЇ УТРЕНІ', text, re.IGNORECASE))
print(f"Found {len(matches)} matches.")

if len(matches) > 1:
    # Use the second match (after the TOC)
    start_pos = matches[1].start()
    # Find next section "ЧИН ЗВИЧАЙНИХ ЧАСІВ" or "ЧИН ЗВИЧАЙНИХ"
    end_m = re.search(r'ЧИН ЗВИЧАЙНИХ ЧАСІВ', text[start_pos:], re.IGNORECASE)
    if end_m:
        end_pos = start_pos + end_m.start()
    else:
        end_pos = start_pos + 4000
    
    with open(out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(text[start_pos:end_pos])
    print("Ukrainian Daily Matins written to:", out_path)
else:
    print("Not enough matches found!")
