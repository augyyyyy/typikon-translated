import subprocess
import os

scratch_dir = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch"

scripts = [
    "format_part1_full.py",
    "format_part2.py",
    "format_part3.py",
    "format_part4.py",
    "format_part5.py",
    "format_glossary.py",
    "format_appendix.py"
]

for script in scripts:
    path = os.path.join(scratch_dir, script)
    print(f"Running {script}...")
    res = subprocess.run(["python", path], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error running {script}:")
        print(res.stderr)
    else:
        print(res.stdout.strip())
print("All formatters complete.")
