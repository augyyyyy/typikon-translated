import json
import re

calendar_path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\json_db\calendar_dolnytsky.json"

with open(calendar_path, "r", encoding="utf-8") as f:
    db = json.load(f)

for key, day_data in db.items():
    entries = day_data.get("entries", [])
    for entry in entries:
        desc = entry.get("description", "")
        if "Prop. " in desc:
            print(f"Key: {key} | Description: {desc}")
