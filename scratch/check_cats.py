import json
from pathlib import Path

report_path = Path("scratch/reports/deterministic_audit_report.json")
data = json.loads(report_path.read_text(encoding="utf-8"))
issues = data.get("issues", [])

by_cat = {}
for i in issues:
    cat = i.get("category")
    by_cat[cat] = by_cat.get(cat, 0) + 1

print("Issue count by category:")
for cat, cnt in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {cnt}")

unanchored = [i for i in issues if "Unanchored Footnote" in i.get("category")]
print(f"\nTotal unanchored definitions: {len(unanchored)}")
for u in unanchored:
    print(f"  {u.get('message')}")
