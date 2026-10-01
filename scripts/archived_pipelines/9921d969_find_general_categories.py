import json
import re

db_path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\json_db\st_sergius\text_st_sergius.json"

with open(db_path, "r", encoding="utf-8") as f:
    # Since it is a very large JSON, we can read it line-by-line using regex or parse key by key if memory permits.
    # Parsing it as json:
    db = json.load(f)

general_categories = set()
for key in db.keys():
    if key.startswith("general."):
        parts = key.split(".")
        if len(parts) >= 2:
            general_categories.add(parts[1])

print("Unique General categories in text_st_sergius.json:")
for cat in sorted(general_categories):
    print(f"  - {cat}")
