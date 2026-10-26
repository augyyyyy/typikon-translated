from pathlib import Path

txt = Path('Final/Final_Dolnytsky_part4_triodion.txt').read_text(encoding='utf-8')
md = Path('Final MD/Final_Dolnytsky_part4_triodion.md').read_text(encoding='utf-8')
for fn in [484, 490, 510, 517, 521, 529, 535, 548, 561, 566, 572, 624, 638, 639, 643, 651]:
    t_c = txt.count(f"[^{fn}]")
    m_c = md.count(f"[^{fn}]")
    print(f"FN {fn}: in TXT = {t_c}, in MD = {m_c}")
