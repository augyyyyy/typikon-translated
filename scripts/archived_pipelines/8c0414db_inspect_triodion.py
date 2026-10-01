import json

with open("json_db/02c_logic_triodion.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for k, v in data.get("logic_map", {}).items():
    trig = v.get("triggers", {})
    prio = v.get("priority")
    vars = v.get("variables", {})
    vt = vars.get("vespers_type")
    mt = vars.get("matins_type")
    lt = vars.get("liturgy_type")
    hp = vars.get("has_polyeleos")
    dt = vars.get("doxology_type")
    print(f"{k:32} | prio: {str(prio):3} | trig: {str(trig):30} | V: {str(vt):20} | M: {str(mt):25} | L: {str(lt):20} | P: {str(hp):5} | D: {str(dt):15}")
