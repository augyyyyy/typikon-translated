import json

with open("json_db/02a_logic_general.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cases = data.get("logic_definitions", {})

print(f"{'Case ID':<35} | {'Vespers Type':<25} | {'Matins Type':<20} | {'Polyeleos':<10} | {'Doxology':<15}")
print("-" * 115)

for k, v in cases.items():
    if not isinstance(v, dict):
        continue
    cid = v.get("id", k)
    vars_ = v.get("variables", {})
    v_type = vars_.get("vespers_type")
    m_type = vars_.get("matins_type")
    poly = vars_.get("has_polyeleos")
    dox = vars_.get("doxology_type")
    base = v.get("base_template")
    print(f"{cid:<35} | {str(v_type):<25} | {str(m_type):<20} | {str(poly):<10} | {str(dox):<15} (base={base})")
