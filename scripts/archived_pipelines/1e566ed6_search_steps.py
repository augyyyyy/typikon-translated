import sys

with open("last_steps.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

output_path = "search_steps_output.txt"
with open(output_path, "w", encoding="utf-8") as out:
    for i, line in enumerate(lines):
        if "side" in line.lower() or "original doc" in line.lower() or "typyk" in line.lower() or "google drive" in line.lower():
            out.write(f"--- Line {i+1} ---\n")
            start = max(0, i-5)
            end = min(len(lines), i+15)
            for j in range(start, end):
                out.write(f"{j+1}: {lines[j].strip()}\n")
print("Done writing to search_steps_output.txt")

