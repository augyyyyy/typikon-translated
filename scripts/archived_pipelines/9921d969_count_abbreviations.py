import json
import re
from collections import Counter

calendar_path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\json_db\calendar_dolnytsky.json"

with open(calendar_path, "r", encoding="utf-8") as f:
    db = json.load(f)

abbreviations = Counter()
pattern = r"\b([A-Za-z]+)\.\s+"

for key, day_data in db.items():
    entries = day_data.get("entries", [])
    for entry in entries:
        desc = entry.get("description", "")
        matches = re.findall(pattern, desc)
        for m in matches:
            abbreviations[m] += 1

print("Abbreviation counts:")
for abbr, count in sorted(abbreviations.items(), key=lambda x: -x[1]):
    print(f"- {abbr}. ({count} occurrences)")
