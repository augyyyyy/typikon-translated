import json
from pathlib import Path

report_path = Path("scratch/reports/deterministic_audit_report.json")
data = json.loads(report_path.read_text(encoding="utf-8"))
issues = data.get("issues", [])
highs = [a for a in issues if a.get("severity") in ("CRITICAL", "HIGH")]
print(f"Total Critical/High severity anomalies: {len(highs)}")
for h in highs:
    print(f"[{h.get('category')}] {h.get('file')}:L{h.get('line', '')} - {h.get('message')}")
    print(f"    Context: {h.get('context')}")
