import json
from pathlib import Path

def main():
    report_file = Path(__file__).resolve().parent / "reports" / "deterministic_audit_report.json"
    with open(report_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    bij_issues = [a for a in data["issues"] if a.get("category") == "Footnote Bijectivity"]
    print(f"Total Footnote Bijectivity issues: {len(bij_issues)}")
    for a in bij_issues:
        print(f"{a.get('file')}:{a.get('line')} - {a.get('message')}")

if __name__ == "__main__":
    main()
