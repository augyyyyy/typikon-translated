import json

calendar_path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\json_db\calendar_dolnytsky.json"

with open(calendar_path, "r", encoding="utf-8") as f:
    db = json.load(f)

keywords = ["Apostles.", "Stratelates.", "Dormition."]

for key, day_data in db.items():
    entries = day_data.get("entries", [])
    for entry in entries:
        desc = entry.get("description", "")
        for kw in keywords:
            if kw in desc:
                print(f"Key: {key} | Keyword: {kw} | Description: {desc}")
