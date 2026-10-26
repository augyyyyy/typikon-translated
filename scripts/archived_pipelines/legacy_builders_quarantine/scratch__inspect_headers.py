from pathlib import Path
import sys
sys.stdout.reconfigure(encoding="utf-8")

for i in range(511, 521):
    txt = (Path("scratch/cohort52_raw_extracted") / f"p{i}.txt").read_text(encoding="utf-8")
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    headers = [l for l in lines if not l[0].isdigit() and not l.startswith("(") and not l.startswith("[")]
    print(f"p{i} non-numeric lines: {headers[:5]}")
