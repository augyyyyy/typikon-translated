import glob
import json

print("=== MENAION ANOMALY AUDIT ===")

for f in sorted(glob.glob("json_db/02b_*.json")):
    with open(f, encoding="utf-8") as fp:
        data = json.load(fp)
    for d, ddata in data.get("month_settings", {}).get("days", {}).items():
        rk = ddata.get("rank")
        bt = ddata.get("base_template")
        tk = ddata.get("title_key", "")
        pd = ddata.get("period", "")
        variants = ddata.get("variants")
        
        # 1. Check rank type
        if isinstance(rk, int):
            print(f"[INT RANK] {f} Day {d}: rank={rk}, title={ddata.get('feast_title')}")
            
        # 2. Check Sunday templates used as base_template
        if bt in ["CASE_01", "CASE_04", "CASE_06", "CASE_08", "CASE_11", "CASE_13", "CASE_15", "CASE_17", "CASE_19"]:
            print(f"[SUNDAY BASE] {f} Day {d} ({tk}): base_template={bt}, rank={rk}")
            
        # 3. Check Marian feasts
        if ("theotokos" in str(tk) or "theotokos" in str(rk) or "marian" in str(tk)) and pd not in ["afterfeast", "forefeast", "apodosis"]:
            if bt not in ["CASE_12", "CASE_11", "CASE_05", "CASE_07", "CASE_02"]:
                print(f"[MARIAN FEAST NOT 12/11/5/7/2] {f} Day {d} ({tk}): base_template={bt}, rank={rk}")
                
        # 4. Check Afterfeasts and Forefeasts
        if pd == "afterfeast" and bt not in ["CASE_14", "CASE_13", "CASE_16", "CASE_15", "CASE_18", "CASE_17"]:
            print(f"[AFTERFEAST WRONG BT] {f} Day {d} ({tk}): base_template={bt}, rank={rk}")
        if pd == "forefeast" and bt not in ["CASE_09", "CASE_08"]:
            print(f"[FOREFEAST WRONG BT] {f} Day {d} ({tk}): base_template={bt}, rank={rk}")
        if pd == "apodosis" and bt not in ["CASE_20", "CASE_19"]:
            print(f"[APODOSIS WRONG BT] {f} Day {d} ({tk}): base_template={bt}, rank={rk}")
