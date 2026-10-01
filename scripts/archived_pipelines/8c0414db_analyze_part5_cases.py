import json

with open("json_db/02d_logic_temple.json", "r", encoding="utf-8") as f:
    temple_json = json.load(f)

cases = temple_json.get("specific_cases", {})

for cid, cdata in cases.items():
    print(f"==================================================")
    print(f"CASE ID: {cid}")
    print(f"TITLE:   {cdata.get('title')}")
    print(f"PERIOD:  {cdata.get('period')}")
    print(f"APPLIES: {cdata.get('applies_to')}")
    print(f"BASE:    {cdata.get('base_rubric') or cdata.get('base') or cdata.get('rule')}")
    if "transfer_rules" in cdata or "action" in cdata or "transfers" in cdata:
        print(f"TRANSFER: {cdata.get('transfer_rules') or cdata.get('action') or cdata.get('transfers')}")
