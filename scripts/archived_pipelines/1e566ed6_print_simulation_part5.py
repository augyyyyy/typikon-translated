import os

with open("simulation_output.txt", 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
in_part5 = False
for line in lines:
    if "SIMULATION FOR Final_Dolnytsky_part5_temple.md" in line:
        in_part5 = True
    elif "SIMULATION FOR" in line and in_part5:
        in_part5 = False
    
    if in_part5:
        print(line)
