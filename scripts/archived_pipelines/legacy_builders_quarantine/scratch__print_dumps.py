import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
print("=== STEP 41 ===")
print(Path("scratch/step_41_dump.txt").read_text(encoding="utf-8"))
print("=== STEP 47 ===")
print(Path("scratch/step_47_dump.txt").read_text(encoding="utf-8"))
