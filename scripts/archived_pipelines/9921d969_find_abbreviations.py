import json
import re

calendar_path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\json_db\calendar_dolnytsky.json"

with open(calendar_path, "r", encoding="utf-8") as f:
    db = json.load(f)

abbreviations = set()
pattern = r"\b([A-Za-z]+)\.\s+"

for key, day_data in db.items():
    entries = day_data.get("entries", [])
    for entry in entries:
        desc = entry.get("description", "")
        matches = re.findall(pattern, desc)
        for m in matches:
            abbreviations.add(m)

print("Found abbreviations followed by a space:")
for abbr in sorted(abbreviations):
    print(f"- {abbr}.")
