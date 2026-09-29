import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

p = Path('Final MD/Final_Dolnytsky_part4_triodion.md')
lines = p.read_text(encoding='utf-8').splitlines()

# Fix L500 and L502
for i in range(len(lines)):
    if 'In the archcathedral temple the Hours 3rd' in lines[i]:
        lines[i] = '1. In the archcathedral temple the Hours 3rd, 6th, 9th, Typika and Vespers are celebrated in this way:'
        lines[i+2] = '2. The last prayer of the 9th Hour "O Master Lord Jesus Christ our God"'
        print('Fixed L500 notes')
        break

# Fix L769
for i in range(len(lines)):
    if lines[i].startswith('7. At the end: Troparion to all saints'):
        lines[i] = '8. At the end: Troparion to all saints ("Apostles, prophets, martyrs"), Glory: "Remember, O Lord", Both now: "O Holy Mother of the Ineffable Light" and Dismissal.'
        print('Fixed L769')
        break

# Fix L1388 and L1390
for i in range(len(lines)):
    if 'Where there will be only one priest, let him choose' in lines[i]:
        lines[i] = '1. Where there will be only one priest, let him choose the Shroud...'
        lines[i+2] = '2. If the pastor has several churches, then in the mother [church]...'
        print('Fixed L1388 notes')
        break

p.write_text('\n'.join(lines), encoding='utf-8')
print("Successfully fixed final 3 Triodion numbering issues!")
