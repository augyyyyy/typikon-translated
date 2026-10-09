import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

fn_text = Path("scratch/russian_footnotes_cohort17.txt").read_text(encoding="utf-8")
lines = fn_text.splitlines()

# Filter 189 to 283
cohort_fn = []
for line in lines:
    if line.startswith("["):
        idx_str = line[1:line.find("]")]
        if idx_str.isdigit():
            idx = int(idx_str)
            if 189 <= idx <= 283:
                cohort_fn.append(line)

print(f"Total cohort 17 footnotes found: {len(cohort_fn)}")
Path("scratch/cohort17_russian_notes.txt").write_text("\n".join(cohort_fn), encoding="utf-8")

# Print first 10 and last 10
for l in cohort_fn[:10]:
    print(l)
print("...")
for l in cohort_fn[-10:]:
    print(l)
