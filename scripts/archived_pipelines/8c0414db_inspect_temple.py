import json

with open("json_db/02d_logic_temple.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for case_id in ["case_1a", "case_1b", "case_3", "case_9", "case_19", "case_20"]:
    case = data["specific_cases"][case_id]
    print(f"=== {case_id}: {case.get('title')} ===")
    for k, v in case.items():
        if isinstance(v, dict):
            print(f"  {k}: dict keys -> {list(v.keys())}")
        elif isinstance(v, list):
            print(f"  {k}: list len -> {len(v)}")
        else:
            print(f"  {k}: {v}")
