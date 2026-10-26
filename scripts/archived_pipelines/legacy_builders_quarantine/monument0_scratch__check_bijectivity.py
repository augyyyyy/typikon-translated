import json
from pathlib import Path

report_path = Path("scratch/reports/deterministic_audit_report.json")
data = json.loads(report_path.read_text(encoding="utf-8"))
issues = data.get("issues", [])

bijectivity = [i for i in issues if i.get("category") == "Footnote Bijectivity"]
print(f"Total Footnote Bijectivity issues: {len(bijectivity)}")
for b in bijectivity:
    print(f"  {b.get('file')}:L{b.get('line')} - {b.get('message')}")
