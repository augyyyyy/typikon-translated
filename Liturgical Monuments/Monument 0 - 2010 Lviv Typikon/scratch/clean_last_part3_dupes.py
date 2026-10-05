from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

# TXT cleanups
txt = txt.replace('transfer the service of the Akathist[^409]', 'transfer the service of the Akathist')
txt = txt.replace('Kontakion of the Feast[^409]', 'Kontakion of the Feast')
txt = txt.replace('Sessional hymn of the Feast[^417];', 'Sessional hymn of the Feast;')
txt = txt.replace('Psalter or Menaion[^426]', 'Psalter or Menaion')
txt = txt.replace('[^453][^450]', '[^450]')

# MD cleanups
md = md.replace('transfer the service of the Akathist[^409]', 'transfer the service of the Akathist')
md = md.replace('Kontakion of the Feast[^409]', 'Kontakion of the Feast')
md = md.replace('Sessional hymn of the *Triodion*, Glory, and now: Sessional hymn of the Feast[^417];', 'Sessional hymn of the *Triodion*, Glory, and now: Sessional hymn of the Feast;')
md = md.replace('Psalter or *Menaion*[^426]', 'Psalter or *Menaion*')
md = md.replace('If one of these saints falls outside the *Triodion*[^361],', 'If one of these saints falls outside the *Triodion*,')

# Remove duplicate 313 in MD at L1153:
# "1. The Priest, having put on an epitrachelion and having gone out before the Holy Doors, bows low and begins the usual: \"Blessed is our God\"[^313]"
md = md.replace('"Blessed is our God"[^313]', '"Blessed is our God"')

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully cleaned last Part 3 duplicates!")
