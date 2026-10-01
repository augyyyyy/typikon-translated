import json

with open("json_db/02d_logic_temple.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cases = data.get("specific_cases", {})
print(f"Total specific cases: {len(cases)}")
for k, v in cases.items():
    title = v.get("title", "")
    applies = v.get("applies_to")
    fixed = v.get("fixed_date")
    period = v.get("period")
    keys = list(v.keys())
    print(f"{k}: {title}")
    print(f"    period={period}, fixed={fixed}, applies={applies}")
    print(f"    subkeys={keys}")
