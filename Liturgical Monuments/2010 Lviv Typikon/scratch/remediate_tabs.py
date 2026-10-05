import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent.parent

def clean_intro():
    p = root / 'Final MD/Final_Dolnytsky_intro.md'
    txt = p.read_text(encoding='utf-8')
    txt = txt.replace('##### 1.\t', '##### 1. ')
    txt = txt.replace('##### 2.\t', '##### 2. ')
    txt = txt.replace('##### 3.\t', '##### 3. ')
    p.write_text(txt, encoding='utf-8')
    print("Cleaned intro tabs.")

def clean_glossary():
    p = root / 'Final MD/Final_Dolnytsky_glossary.md'
    lines = p.read_text(encoding='utf-8').splitlines()
    new_lines = []
    for l in lines:
        if '\t' in l:
            # Replace tab after numbers like '7.\t'
            l = re.sub(r'^(\d+[\.\)])\t', r'\1 ', l)
        new_lines.append(l)
    p.write_text('\n'.join(new_lines), encoding='utf-8')
    print("Cleaned glossary tabs.")

def clean_part4():
    p = root / 'Final MD/Final_Dolnytsky_part4_triodion.md'
    lines = p.read_text(encoding='utf-8').splitlines()
    new_lines = []
    for l in lines:
        if '\t' in l:
            l = re.sub(r'^(\d+[\.\)]|•|-)\t', r'\1 ', l)
            l = l.replace('\t', ' ')
        new_lines.append(l)
    p.write_text('\n'.join(new_lines), encoding='utf-8')
    print("Cleaned part4 tabs.")

def clean_part3():
    p = root / 'Final MD/Final_Dolnytsky_part3_menaion.md'
    lines = p.read_text(encoding='utf-8').splitlines()
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check Table 1: BOUNDARY KEYS
        if 'BOUNDARY KEYS\tPASCHAL DAYS' in line:
            table_lines = [line]
            i += 1
            while i < len(lines) and (lines[i].strip() == '' or '\t' in lines[i]):
                if lines[i].strip():
                    table_lines.append(lines[i].strip())
                i += 1
            # format table 1
            rows = [[c.strip() for c in tl.split('\t')] for tl in table_lines]
            new_lines.append('| ' + ' | '.join(rows[0]) + ' |')
            new_lines.append('| ' + ' | '.join(['---'] * len(rows[0])) + ' |')
            for r in rows[1:]:
                new_lines.append('| ' + ' | '.join(r) + ' |')
            continue
            
        # Check Table 2: DECEMBER ... JANUARY calendar
        if 'DECEMBER\t\t\t\t\t\t\tJANUARY' in line:
            table_lines = [line]
            i += 1
            while i < len(lines) and (lines[i].strip() == '' or '\t' in lines[i]):
                if lines[i].strip():
                    table_lines.append(lines[i].strip())
                i += 1
            # format as code block or clean markdown table
            # since it is a calendar grid, let's format it as a markdown code block or table
            new_lines.append('```text')
            for tl in table_lines:
                new_lines.append(tl)
            new_lines.append('```')
            continue

        # Check Table 3: MEETING ON \t APODOSIS ON
        if 'MEETING ON\tAPODOSIS ON' in line:
            table_lines = [line]
            i += 1
            while i < len(lines) and (lines[i].strip() == '' or '\t' in lines[i]):
                if lines[i].strip():
                    table_lines.append(lines[i].strip())
                i += 1
            rows = [[c.strip() for c in tl.split('\t')] for tl in table_lines]
            new_lines.append('| ' + ' | '.join(rows[0]) + ' |')
            new_lines.append('| ' + ' | '.join(['---'] * len(rows[0])) + ' |')
            for r in rows[1:]:
                new_lines.append('| ' + ' | '.join(r) + ' |')
            continue

        if '\t' in line:
            line = re.sub(r'^(\d+[\.\)]|•|-)\t', r'\1 ', line)
            line = line.replace('\t', ' ')
            
        new_lines.append(line)
        i += 1

    p.write_text('\n'.join(new_lines), encoding='utf-8')
    print("Cleaned part3 tabs.")

def clean_part5():
    p = root / 'Final MD/Final_Dolnytsky_part5_temple.md'
    lines = p.read_text(encoding='utf-8').splitlines()
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Table 1: BEGINNING \t ENDING
        if 'BEGINNING\tENDING\tFIRST WORDS\tTONE\tFEAST' in line:
            table_lines = [line]
            i += 1
            while i < len(lines) and (lines[i].strip() == '' or '\t' in lines[i]):
                if lines[i].strip():
                    table_lines.append(lines[i].strip())
                i += 1
            rows = [[c.strip() for c in tl.split('\t')] for tl in table_lines]
            new_lines.append('| ' + ' | '.join(rows[0]) + ' |')
            new_lines.append('| ' + ' | '.join(['---'] * len(rows[0])) + ' |')
            for r in rows[1:]:
                new_lines.append('| ' + ' | '.join(r) + ' |')
            continue

        # Table 2: TIME \t FIRST WORDS
        if 'TIME\tFIRST WORDS\tTONE\tFEAST' in line:
            table_lines = [line]
            i += 1
            while i < len(lines) and (lines[i].strip() == '' or '\t' in lines[i]):
                if lines[i].strip():
                    table_lines.append(lines[i].strip())
                i += 1
            rows = [[c.strip() for c in tl.split('\t')] for tl in table_lines]
            new_lines.append('| ' + ' | '.join(rows[0]) + ' |')
            new_lines.append('| ' + ' | '.join(['---'] * len(rows[0])) + ' |')
            for r in rows[1:]:
                new_lines.append('| ' + ' | '.join(r) + ' |')
            continue

        # Table 3: Year \t Letter \t Key
        if 'Year\tLetter\tKey\tYear\tLetter\tKey' in line:
            table_lines = [line]
            i += 1
            while i < len(lines) and (lines[i].strip() == '' or '\t' in lines[i]):
                if lines[i].strip():
                    table_lines.append(lines[i].strip())
                i += 1
            rows = [[c.strip() for c in tl.split('\t')] for tl in table_lines]
            new_lines.append('| ' + ' | '.join(rows[0]) + ' |')
            new_lines.append('| ' + ' | '.join(['---'] * len(rows[0])) + ' |')
            for r in rows[1:]:
                # pad row if needed
                padded = r + [''] * (len(rows[0]) - len(r))
                new_lines.append('| ' + ' | '.join(padded) + ' |')
            continue

        if '\t' in line:
            line = line.replace('[^665]1.\t', '[^665]1. ')
            line = re.sub(r'^(\d+[\.\)]|•|-)\t', r'\1 ', line)
            line = line.replace('\t', ' ')
            
        new_lines.append(line)
        i += 1

    p.write_text('\n'.join(new_lines), encoding='utf-8')
    print("Cleaned part5 tabs.")

clean_intro()
clean_glossary()
clean_part4()
clean_part3()
clean_part5()
print("All tab remediations complete!")
