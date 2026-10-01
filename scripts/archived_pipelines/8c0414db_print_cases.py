import json

with open("json_db/02a_logic_general.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for k, v in data.get("logic_definitions", {}).items():
    if not isinstance(v, dict):
        continue
    print(f"{k}: {v.get('title')}")
