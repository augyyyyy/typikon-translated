from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

# 1. FN 313 & 320
# In TXT:
txt = txt.replace(
    '"O come, let us worship" inclusive[^320][^313]. At the second',
    '"O come, let us worship" inclusive[^313]. At the second'
)
# And in TXT Para 1257:
txt = txt.replace(
    'up to "O come, let us worship" inclusive.\nDeacons, if there be',
    'up to "O come, let us worship" inclusive[^320].\nDeacons, if there be'
)
# In MD:
# The first one (Para 1225) has [^313], the second (Para 1257) has [^313] -> change second to [^320]
p1257_old = 'up to "O come, let us worship" inclusive[^313]. Deacons, if there be'
p1257_new = 'up to "O come, let us worship" inclusive[^320]. Deacons, if there be'
assert p1257_old in md
md = md.replace(p1257_old, p1257_new)

# 2. FN 361 in MD:
# Remove match 2
m2_361_old = 'Both now: Kontakion of the *Triodion*[^361].\n\n##### At Great Matins'
m2_361_new = 'Both now: Kontakion of the *Triodion*.\n\n##### At Great Matins'
assert m2_361_old in md
md = md.replace(m2_361_old, m2_361_new)

# 3. FN 409: Remove match 2 in TXT & MD
txt = txt.replace('Kontakion of the Feast of the Annunciation[^409].', 'Kontakion of the Feast of the Annunciation.')
md = md.replace('Kontakion of the Feast of the Annunciation[^409].', 'Kontakion of the Feast of the Annunciation.')

# 4. FN 417: Remove match 1 in TXT & MD
txt = txt.replace('Glory, and now: of the Feast[^417];', 'Glory, and now: of the Feast;')
md = md.replace('Glory, and now: of the Feast[^417];', 'Glory, and now: of the Feast;')

# 5. FN 426: Remove match 1 in TXT & MD
txt = txt.replace('only Both now: of the Feast[^426]. Gradual of Tone 4', 'only Both now: of the Feast. Gradual of Tone 4')
md = md.replace('only Both now: of the Feast[^426]. Gradual of Tone 4', 'only Both now: of the Feast. Gradual of Tone 4')

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully executed final Part 3 de-duplication!")
