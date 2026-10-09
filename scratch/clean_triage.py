from pathlib import Path

p = Path("scratch/triage_inbox.jsonl")
if p.exists():
    lines = p.read_text(encoding="utf-8").splitlines()
    new_lines = [l for l in lines if '"cohort": 15' not in l and '"cohort":15' not in l]
    p.write_text("\n".join(new_lines) + ("\n" if new_lines else ""), encoding="utf-8")
    print(f"Cleaned triage_inbox: {len(lines)} -> {len(new_lines)}")
