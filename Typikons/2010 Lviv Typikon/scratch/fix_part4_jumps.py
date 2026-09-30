import re
from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part4_triodion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part4_triodion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

print("Remediating Part 4 backward jumps...")

# 1. FN 484 and 490 on same line
# In TXT:
txt = txt.replace('12 small[^484][^490].', '12 small[^484].')
txt = txt.replace('12 small[^490][^484].', '12 small[^484].')
# In MD:
md = md.replace('12 small[^484][^490].', '12 small[^484].')
md = md.replace('12 small[^490][^484].', '12 small[^484].')

# Add [^490] to its true location: First Monday of Lent (para 2854)
# In DOCX: "Note We make prostrations according to the rule ... St. Ephrem – 16 prostrations: 4 great and 12 small."
txt = re.sub(
    r'(Note:?\s*We make prostrations[^\n]*?12 small)\.',
    r'\1[^490].',
    txt,
    count=1
)
md = re.sub(
    r'(Note:?\s*We make prostrations[^\n]*?12 small)\.',
    r'\1[^490].',
    md,
    count=1
)

# 2. Premature 561 and 572 at TXT L117 / MD L237
txt = txt.replace('with heirmos on 6[^561][^572],', 'with heirmos on 6,')
txt = txt.replace('with heirmos on 6[^572][^561],', 'with heirmos on 6,')
txt = txt.replace('with heirmos on 6[^561],', 'with heirmos on 6,')
txt = txt.replace('with heirmos on 6[^572],', 'with heirmos on 6,')

md = md.replace('with heirmos on 6[^561][^572],', 'with heirmos on 6,')
md = md.replace('with heirmos on 6[^572][^561],', 'with heirmos on 6,')
md = md.replace('with heirmos on 6[^561],', 'with heirmos on 6,')
md = md.replace('with heirmos on 6[^572],', 'with heirmos on 6,')

# Place 561 at Palm Sunday (para 3209):
# "troparia – \"Glory to Thee, our God, glory to Thee\". After the 3rd Ode"
txt = txt.replace(
    '"Glory to Thee, our God, glory to Thee".\nAfter the 3rd Ode',
    '"Glory to Thee, our God, glory to Thee"[^561].\nAfter the 3rd Ode'
)
md = md.replace(
    '“Glory to Thee, our God, glory to Thee”.\n\nAfter the 3rd Ode',
    '“Glory to Thee, our God, glory to Thee”[^561].\n\nAfter the 3rd Ode'
)
md = md.replace(
    '"Glory to Thee, our God, glory to Thee".\n\nAfter the 3rd Ode',
    '"Glory to Thee, our God, glory to Thee"[^561].\n\nAfter the 3rd Ode'
)

# Place 572 at Great Tuesday (para 3246):
# "canon \"Glory to Thee, our God, glory to Thee\", then the Katavasia"
txt = txt.replace(
    '"Glory to Thee, our God, glory to Thee", then the Katavasia',
    '"Glory to Thee, our God, glory to Thee"[^572], then the Katavasia'
)
md = md.replace(
    '“Glory to Thee, our God, glory to Thee”, then the Katavasia',
    '“Glory to Thee, our God, glory to Thee”[^572], then the Katavasia'
)
md = md.replace(
    '"Glory to Thee, our God, glory to Thee", then the Katavasia',
    '"Glory to Thee, our God, glory to Thee"[^572], then the Katavasia'
)

# 3. Premature 521 at TXT L189 / MD L394
txt = txt.replace('only up to the end of the 1st Hour[^521].', 'only up to the end of the 1st Hour.')
md = md.replace('only up to the end of the 1st Hour[^521].', 'only up to the end of the 1st Hour.')

# Place 521 at Typika/Beatitudes (para 2972):
# "dismissal of the day with the commemoration of the saint."
txt = txt.replace(
    'commemoration of the saint.\nAT Great Compline',
    'commemoration of the saint[^521].\nAT Great Compline'
)
md = md.replace(
    'commemoration of the Saint.\n\n##### At Great Compline',
    'commemoration of the Saint[^521].\n\n##### At Great Compline'
)
md = md.replace(
    'commemoration of the saint.\n\n##### At Great Compline',
    'commemoration of the saint[^521].\n\n##### At Great Compline'
)

# 4. Premature 548 at TXT L231 / MD L472
txt = txt.replace('Sessional Hymn of the Saint[^548], after the 6th - Kontakion and Ikos of the Saint', 'Sessional Hymn of the Saint, after the 6th - Kontakion and Ikos of the Saint')
md = md.replace('Sessional Hymn of the Saint[^548], after the 6th – Kontakion and Ikos of the Saint', 'Sessional Hymn of the Saint, after the 6th – Kontakion and Ikos of the Saint')

# Place 548 at Second Saturday of Lent (para 3072):
# "After the 3rd Ode – Sessional Hymn of the Saint, after the 6th – Kondakion and Ikos for the Dead"
txt = txt.replace(
    'Sessional Hymn of the Saint, after the 6th - Kontakion and Ikos for the Dead',
    'Sessional Hymn of the Saint[^548], after the 6th - Kontakion and Ikos for the Dead'
)
md = md.replace(
    'Sessional Hymn of the Saint, after the 6th – Kontakion and Ikos for the Dead',
    'Sessional Hymn of the Saint[^548], after the 6th – Kontakion and Ikos for the Dead'
)

# 5. Premature 566 at TXT L303 / MD L600
txt = txt.replace('Forefeast of the Annunciation[^566]', 'Forefeast of the Annunciation')
md = md.replace('Forefeast of the Annunciation[^566]', 'Forefeast of the Annunciation')

# Place 566 at Great Monday, Tuesday and Wednesday heading (para 3223):
txt = txt.replace('GREAT MONDAY, TUESDAY AND WEDNESDAY\n', 'GREAT MONDAY, TUESDAY AND WEDNESDAY[^566]\n')
md = md.replace('### 4.2.3 Great Monday, Tuesday and Wednesday\n', '### 4.2.3 Great Monday, Tuesday and Wednesday[^566]\n')
md = md.replace('### Great Monday, Tuesday and Wednesday\n', '### Great Monday, Tuesday and Wednesday[^566]\n')

# 6. Premature 651 at TXT L309 / MD L612
txt = txt.replace('Presanctified Gifts, here on p. 28-30[^651].', 'Presanctified Gifts, here on p. 28-30.')
md = md.replace('Presanctified Gifts, here on p. 28-30[^651].', 'Presanctified Gifts, here on p. 28-30.')

# 7. Premature 638 at TXT L751 / MD L1518
txt = txt.replace('"Shine, shine, new Jerusalem"[^638]', '"Shine, shine, new Jerusalem"')
md = md.replace('"Shine, shine, new Jerusalem"[^638]', '"Shine, shine, new Jerusalem"')

# 8. Misplaced 643 at TXT L814 / MD L1646 (before 639)
txt = txt.replace('on the feast of Mid-Pentecost[^643]', 'on the feast of Mid-Pentecost')
md = md.replace('on the feast of Mid-Pentecost[^643]', 'on the feast of Mid-Pentecost')

# Place 643 at Liturgy (para 3442):
# "Pentecost and on the Leavetaking of the Resurrection. We suppose"
txt = txt.replace(
    'on the Leavetaking of the Resurrection.\nWe suppose',
    'on the Leavetaking of the Resurrection[^643].\nWe suppose'
)
md = md.replace(
    'on the Leavetaking of the Resurrection.\n\nWe suppose',
    'on the Leavetaking of the Resurrection[^643].\n\nWe suppose'
)

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully remediated Part 4 backward jumps!")
