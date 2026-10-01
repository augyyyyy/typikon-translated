import json
import glob
import os

files = glob.glob("json_db/02*.json")
issues = []

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            issues.append(f"{fpath}: JSON parse error: {e}")
            continue

    def check_obj(obj, path):
        if not isinstance(obj, dict):
            return
        for k, v in obj.items():
            current_path = f"{path}.{k}"
            if k in ["vespers_stichera_distribution", "praises_distribution", "aposticha_distribution"]:
                if isinstance(v, dict):
                    if "inherits" in v or "source_ref" in v:
                        pass
                    elif "total_count" not in v and "distribution" not in v:
                        issues.append(f"{current_path}: Non-standard schema: keys={list(v.keys())}")
            elif k == "matins_canon_distribution":
                if isinstance(v, dict):
                    if "inherits" in v or "source_ref" in v:
                        pass
                    elif "distribution" not in v:
                        issues.append(f"{current_path}: Matins canon non-standard: keys={list(v.keys())}")
            if isinstance(v, dict):
                check_obj(v, current_path)
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    check_obj(item, f"{current_path}[{i}]")

    check_obj(data, os.path.basename(fpath))

print(f"Total issues found: {len(issues)}")
for issue in issues:
    print(issue)
