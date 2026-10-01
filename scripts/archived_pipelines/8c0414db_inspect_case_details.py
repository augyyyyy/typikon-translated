import json

with open("json_db/02d_logic_temple.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cases = data.get("specific_cases", {})
for cid, cdata in cases.items():
    print(f"=== {cid} ===")
    print(f"Title: {cdata.get('title')}")
    print(f"Period: {cdata.get('period')}")
    print(f"Keys: {list(cdata.keys())}")
    if "variables" in cdata:
        print(f"Variables: {cdata['variables']}")
    else:
        print("Variables: None")
    if "overrides" in cdata:
        print(f"Overrides: {cdata['overrides']}")
