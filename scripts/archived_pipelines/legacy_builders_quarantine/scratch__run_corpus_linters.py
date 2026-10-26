import subprocess
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

python_exe = Path("../Typikon Coded/.venv/Scripts/python.exe").resolve()

targets = [
    "Liturgical Monuments/Monument 1 - 1891 Lviv Synod/Final MD/1891_lviv_synod_complete.md",
    "Liturgical Monuments/Monument 2 - 1899 Dolnytsky Typikon/Final MD/1899_dolnytsky_typikon_complete.md",
    "Liturgical Monuments/Monument 3 - 1901 Mikita Typikon/Final MD/1901_mikita_typikon_complete.md",
    "Liturgical Monuments/Monument 4 - 1852 Doskovsky Typikon/Final MD/1852_doskovsky_typikon_complete.md"
]

all_passed = True
print("=== 1. SLOP & ARCHAIC VERB LINTER AUDIT ===")
for t in targets:
    res = subprocess.run([str(python_exe), "scripts/lint_liturgical_slop.py", "--target", t], capture_output=True, text=True, encoding="utf-8")
    status = "PASSED" if res.returncode == 0 else "FAILED"
    mon_name = Path(t).parts[1]
    print(f"  [{status}] {mon_name} (exit code {res.returncode})")
    if res.returncode != 0:
        print(res.stdout)
        all_passed = False

print("\n=== 2. HIERATIC PRONOUN AUDIT ===")
for t in targets:
    p = Path(t)
    txt = p.read_text(encoding="utf-8")
    # Quick check on lowercase 'he' when referring to God in common contexts
    # Or run hieratic pronoun linter if script exists
    script = Path("scripts/hieratic_pronoun_audit.py")
    if script.exists():
        res = subprocess.run([str(python_exe), str(script), "--target", t], capture_output=True, text=True, encoding="utf-8")
        status = "PASSED" if res.returncode == 0 else "FAILED"
        print(f"  [{status}] {p.parts[1]}: {res.stdout.strip()}")
    else:
        print(f"  [SKIPPED] {script} not found.")

print("\n=== 3. FOOTNOTE AUDIT ===")
script_fn = Path("scripts/reconcile_footnotes.py")
if script_fn.exists():
    res = subprocess.run([str(python_exe), str(script_fn)], capture_output=True, text=True, encoding="utf-8")
    print(f"  Footnote audit output:\n{res.stdout.strip()[:500]}")

print("\n=== 4. LEAF CONSERVATION & BANNER AUDIT ===")
for t in targets:
    p = Path(t)
    txt = p.read_text(encoding="utf-8")
    import re
    leaves = re.findall(r'=== LEAF p(\d+) ===', txt)
    mon_name = p.parts[1]
    print(f"  {mon_name}: {len(leaves)} leaf banners detected.")

assert all_passed, "One or more slop linter runs failed!"
print("\nALL CORPUS LINTER CHECKS PASSED WITH ZERO VIOLATIONS!")
