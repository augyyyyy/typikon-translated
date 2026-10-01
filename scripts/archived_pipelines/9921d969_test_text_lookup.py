import json
with open("json_db/02c_logic_triodion.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for name, rule in data.get("logic_map", {}).items():
    p = rule.get("priority", 0)
    if p >= 80:
        print(f"Name: {name}, Priority: {p}, Title: {rule.get('title')}")
        if "variables" in rule:
            print(f"  Variables: {list(rule['variables'].keys())}")
