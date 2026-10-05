from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

# In TXT: remove spurious 388 from Case 3 (around L1291)
txt = txt.replace('and dismissal[^388] from "Glory to Thee', 'and dismissal from "Glory to Thee')

# In MD: remove 375 from Forefeast (around L2102)
lines = md.splitlines()
for i in range(2095, 2110):
    if '[^375]' in lines[i]:
        lines[i] = lines[i].replace('[^375]', '')
        print(f"Removed [^375] from MD L{i+1}")
md = '\n'.join(lines)

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully cleaned 388 and 375!")
