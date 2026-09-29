import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent

pairs = [
    ("intro", "Final/Final_Dolnytsky_intro.txt", "Final MD/Final_Dolnytsky_intro.md"),
    ("part1", "Final/Final_Dolnytsky_part1_structure.txt", "Final MD/Final_Dolnytsky_part1_structure.md"),
    ("part2", "Final/Final_Dolnytsky_part2_general_rubrics.txt", "Final MD/Final_Dolnytsky_part2_general_rubrics.md"),
    ("part3", "Final/Final_Dolnytsky_part3_menaion.txt", "Final MD/Final_Dolnytsky_part3_menaion.md"),
    ("part4", "Final/Final_Dolnytsky_part4_triodion.txt", "Final MD/Final_Dolnytsky_part4_triodion.md"),
    ("part5", "Final/Final_Dolnytsky_part5_temple.txt", "Final MD/Final_Dolnytsky_part5_temple.md"),
    ("appendix", "Final/Final_Dolnytsky_appendix.txt", "Final MD/Final_Dolnytsky_appendix.md")
]

for name, txt_p, md_p in pairs:
    t_text = (root / txt_p).read_text(encoding='utf-8')
    m_text = (root / md_p).read_text(encoding='utf-8')
    
    t_fns = [int(m.group(1)) for m in re.finditer(r'\[\^(\d+)\]', t_text)]
    m_fns = [int(m.group(1)) for m in re.finditer(r'\[\^(\d+)\]', m_text)]
    
    t_set = set(t_fns)
    m_set = set(m_fns)
    
    in_txt_not_md = t_set - m_set
    in_md_not_txt = m_set - t_set
    
    print(f"=== {name} ===")
    print(f"  TXT fns: {len(t_fns)} (unique: {len(t_set)})")
    print(f"  MD  fns: {len(m_fns)} (unique: {len(m_set)})")
    if in_txt_not_md:
        print(f"  In TXT but NOT in MD: {sorted(in_txt_not_md)}")
    if in_md_not_txt:
        print(f"  In MD but NOT in TXT: {sorted(in_md_not_txt)}")
    # Check duplicates in each
    t_dups = [x for x in t_set if t_fns.count(x) > 1]
    m_dups = [x for x in m_set if m_fns.count(x) > 1]
    if t_dups:
        print(f"  TXT duplicates: {sorted(t_dups)}")
    if m_dups:
        print(f"  MD duplicates: {sorted(m_dups)}")
