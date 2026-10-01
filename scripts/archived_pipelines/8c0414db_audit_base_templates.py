import json
import glob
import os

files = sorted(glob.glob("json_db/02b_*.json"))
report = []

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    month_id = data.get("month_settings", {}).get("month_id")
    days = data.get("month_settings", {}).get("days", {})
    for day_str, day_data in sorted(days.items()):
        if not isinstance(day_data, dict):
            continue
        rank = day_data.get("rank")
        period = day_data.get("period")
        base_tmpl = day_data.get("base_template")
        variants = day_data.get("variants", [])
        title = day_data.get("title_key", "")
        
        # Check suspicious patterns
        suspect = []
        if "theotokos" in str(rank).lower() and period == "feast":
            if base_tmpl in ["CASE_14", "CASE_13"]:
                suspect.append(f"Feast of Theotokos using Afterfeast template ({base_tmpl}) instead of CASE_12/CASE_11")
        if rank == "rank_vigil_saint" and base_tmpl not in ["CASE_07", "CASE_06"]:
            suspect.append(f"Vigil Saint using non-vigil base_template ({base_tmpl})")
        elif rank == "rank_vigil_saint" and base_tmpl == "CASE_06" and not variants:
            suspect.append(f"Vigil Saint hardcoded to Sunday Vigil (CASE_06) without weekday template")
        if rank == "rank_polyeleos" and base_tmpl in ["CASE_01", "CASE_02", "CASE_03"]:
            suspect.append(f"Polyeleos Saint using simple saint template ({base_tmpl})")
        if period == "afterfeast" and base_tmpl not in ["CASE_13", "CASE_14", "CASE_15", "CASE_16", "CASE_17", "CASE_18"]:
            suspect.append(f"Afterfeast day using non-afterfeast template ({base_tmpl})")
        if period == "apodosis" and base_tmpl not in ["CASE_19", "CASE_20"]:
            suspect.append(f"Apodosis day using non-apodosis template ({base_tmpl})")

        report.append({
            "month": month_id,
            "day": day_str,
            "title": title,
            "rank": rank,
            "period": period,
            "base_template": base_tmpl,
            "variants": variants,
            "suspect": suspect
        })

print(f"Total days audited: {len(report)}")
suspicious_count = 0
for r in report:
    if r["suspect"]:
        suspicious_count += 1
        print(f"[{r['month']:02d}-{r['day']}] {r['title']} (rank={r['rank']}, period={r['period']}, tmpl={r['base_template']}):")
        for s in r["suspect"]:
            print(f"  --> ALERT: {s}")

print(f"\nTotal suspicious days found: {suspicious_count}")
