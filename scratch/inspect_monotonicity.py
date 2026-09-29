import json
from pathlib import Path

report_path = Path("scratch/reports/deterministic_audit_report.json")
data = json.loads(report_path.read_text(encoding="utf-8"))
issues = data.get("issues", [])

monotonicity = [i for i in issues if i.get("category") == "Footnote Monotonicity"]
print(f"Total Footnote Monotonicity issues: {len(monotonicity)}")

by_file = {}
for m in monotonicity:
    f = m.get("file")
    by_file[f] = by_file.get(f, 0) + 1

for f, cnt in by_file.items():
    print(f"\nFile: {f} ({cnt} issues)")
    file_issues = [i for i in monotonicity if i.get("file") == f]
    for i in file_issues:
        print(f"  L{i.get('line')}: {i.get('message')}")
        print(f"     Context: {i.get('context')}")
