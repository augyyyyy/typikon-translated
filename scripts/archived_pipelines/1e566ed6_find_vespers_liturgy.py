import os
import re

txt_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\Typyk_UHKC_ukr.txt"
out_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\ukr_search_output.txt"

if not os.path.exists(txt_path):
    print("Ukrainian txt file not found!")
    exit(1)

with open(txt_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for "вечірню з літургією" or "вечірня з літургією" (case-insensitive)
matches = [m.start() for m in re.finditer(r'вечірн[яю] з літургіє[юя]', text, re.IGNORECASE)]

with open(out_path, 'w', encoding='utf-8') as out_f:
    out_f.write(f"Found {len(matches)} matches for 'вечірню з літургією'\n")
    for idx, m_pos in enumerate(matches):
        start = max(0, m_pos - 100)
        end = min(len(text), m_pos + 1500)
        out_f.write(f"\nMatch {idx+1} at index {m_pos}:\n")
        out_f.write(text[start:end])
        out_f.write("\n" + "-" * 50 + "\n")

print("Output written to:", out_path)
