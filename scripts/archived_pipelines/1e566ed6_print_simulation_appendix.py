import os

with open("simulation_output.txt", 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
in_appendix = False
for line in lines:
    if "SIMULATION FOR Final_Dolnytsky_appendix.md" in line:
        in_appendix = True
    elif "SIMULATION FOR" in line and in_appendix:
        in_appendix = False
    
    if in_appendix:
        print(line)
