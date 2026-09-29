import re
from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

print("Fixing last 3 backward jumps in Part 3...")

# 1. FN 375:
# In MD: Remove from Forefeast (L2102) and place at Afterfeast (L2373)
md = md.replace('On Cheesefare Saturday[^375]\n\n#### I. FOREFEAST', 'On Cheesefare Saturday\n\n#### I. FOREFEAST')
md = md.replace('On Cheesefare Saturday\n\n#### I. AFTERFEAST', 'On Cheesefare Saturday[^375]\n\n#### I. AFTERFEAST')

# In TXT: Check where 375 is
txt = txt.replace('On Cheesefare Saturday[^375]\nI. FOREFEAST', 'On Cheesefare Saturday\nI. FOREFEAST')
txt = txt.replace('On Cheesefare Saturday\nI. AFTERFEAST', 'On Cheesefare Saturday[^375]\nI. AFTERFEAST')

# 2. FN 389:
# Remove from Case 2 (Aposticha)
txt = txt.replace(
    'Aposticha Resurrectional, Glory: to the Forerunner, Both now: of the Triodion[^389].',
    'Aposticha Resurrectional, Glory: to the Forerunner, Both now: of the Triodion.'
)
md = md.replace(
    'Aposticha Resurrectional, Glory: to the Forerunner, Both now: of the *Triodion*[^389]',
    'Aposticha Resurrectional, Glory: to the Forerunner, Both now: of the *Triodion*'
)

# Place at Case 11 (Liturgy):
# "Resurrectional Troparion and to the Forerunner, Glory: Kontakion to the Forerunner, Both now: of the Triodion[^389]."
txt = txt.replace(
    'Troparion and to the Forerunner, Glory: Kontakion to the Forerunner, Both now: of the Triodion.',
    'Troparion and to the Forerunner, Glory: Kontakion to the Forerunner, Both now: of the Triodion[^389].'
)
md = md.replace(
    'Troparion and to the Forerunner, Glory: Kontakion to the Forerunner, Both now: of the *Triodion*.',
    'Troparion and to the Forerunner, Glory: Kontakion to the Forerunner, Both now: of the *Triodion*[^389].'
)
md = md.replace(
    'Troparion and to the Forerunner, Glory: Kontakion to the Forerunner, Both now: of the *Triodion*',
    'Troparion and to the Forerunner, Glory: Kontakion to the Forerunner, Both now: of the *Triodion*[^389]'
)

# 3. FN 388:
# Remove from MD L2634 (Case 3)
spurious_388 = '(On Wednesday evening, after the litany – 3 great prostrations, and also "O All-Holy Trinity", "Blessed be the name of the Lord", "Blessed be the Lord", *“It is truly meet”* and dismissal[^388] from "Glory to Thee, O Christ God").\n\n'
md = md.replace(spurious_388, '')
md = md.replace('(On Wednesday evening, after the litany – 3 great prostrations, and also "O All-Holy Trinity", "Blessed be the name of the Lord", "Blessed be the Lord", *“It is truly meet”* and dismissal[^388] from "Glory to Thee, O Christ God").', '')

# In TXT: ensure 388 is at Case 9 L1378
txt = txt.replace('"It is truly meet" and Dismissal.\nON WEDNESDAY EVENING', '"It is truly meet" and Dismissal[^388].\nON WEDNESDAY EVENING')

# In MD: place 388 at Case 9
md = md.replace('"It is truly meet" and Dismissal.\n\n', '"It is truly meet" and Dismissal[^388].\n\n')
md = md.replace('*“It is truly meet”* and Dismissal.\n\n', '*“It is truly meet”* and Dismissal[^388].\n\n')

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully fixed last 3 backward jumps in Part 3!")
