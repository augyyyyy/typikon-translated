from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part4_triodion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part4_triodion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

print("Executing precise Part 4 monotonicity cleanup...")

# 1. FN 572 & 561 at L237 / TXT L117
txt = txt.replace('"Glory to Thee, our God, glory to Thee"[^572][^561]', '"Glory to Thee, our God, glory to Thee"')
md = md.replace('"Glory to Thee, our God, glory to Thee"[^572][^561]', '"Glory to Thee, our God, glory to Thee"')
md = md.replace('“Glory to Thee, our God, glory to Thee”[^572][^561]', '“Glory to Thee, our God, glory to Thee”')

# Place 561 at Palm Sunday (para 3209):
# "troparia – \"Glory to Thee, our God, glory to Thee\". After the 3rd Ode"
txt = txt.replace(
    'our God, glory to Thee".\nAfter the 3rd Ode',
    'our God, glory to Thee"[^561].\nAfter the 3rd Ode'
)
md = md.replace(
    'our God, glory to Thee”.\n\nAfter the 3rd Ode',
    'our God, glory to Thee”[^561].\n\nAfter the 3rd Ode'
)
md = md.replace(
    'our God, glory to Thee".\n\nAfter the 3rd Ode',
    'our God, glory to Thee"[^561].\n\nAfter the 3rd Ode'
)

# 2. FN 521: Move from L394 / TXT L189 to L534 / TXT L262
# Remove from L394 / TXT L189
txt = txt.replace('commemoration of the saint[^521].', 'commemoration of the saint.')
md = md.replace('commemoration of the saint[^521].', 'commemoration of the saint.')

# Place at L534 / TXT L262
txt = txt.replace(
    'Dismissal of the day with the commemoration of the saint.\nAT VESPERS',
    'Dismissal of the day with the commemoration of the saint[^521].\nAT VESPERS'
)
md = md.replace(
    'Dismissal of the day with the commemoration of the saint\n\n##### At Vespers',
    'Dismissal of the day with the commemoration of the saint[^521].\n\n##### At Vespers'
)

# 3. FN 566: Remove premature duplicate at L600 / TXT L303
txt = txt.replace('and on Great Monday, Tuesday and Wednesday[^566] entrance', 'and on Great Monday, Tuesday and Wednesday entrance')
md = md.replace('and on Great Monday, Tuesday and Wednesday[^566] entrance', 'and on Great Monday, Tuesday and Wednesday entrance')

# 4. FN 651: Remove premature duplicate at L612 / TXT L309
txt = txt.replace('Troparion of the Saint[^651] and, after the litany', 'Troparion of the Saint and, after the litany')
md = md.replace('Troparion of the Saint[^651] and, after the litany', 'Troparion of the Saint and, after the litany')

# 5. FN 638: Remove premature duplicate at L1518 / TXT L751
txt = txt.replace('"Shine, shine"[^638] and, instead of "Glory, Both now"', '"Shine, shine" and, instead of "Glory, Both now"')
md = md.replace('"Shine, shine"[^638] and, instead of "Glory, Both now"', '"Shine, shine" and, instead of "Glory, Both now"')

# 6. FN 643: Move from L1646 / TXT L814 to Liturgy para 3442
txt = txt.replace('on the Apodosis of the Resurrection[^643] - the Resurrection Troparion', 'on the Apodosis of the Resurrection - the Resurrection Troparion')
md = md.replace('on the Apodosis of the Resurrection[^643] – the Resurrection Troparion', 'on the Apodosis of the Resurrection – the Resurrection Troparion')
md = md.replace('on the Apodosis of the Resurrection[^643] - the Resurrection Troparion', 'on the Apodosis of the Resurrection - the Resurrection Troparion')

# Place 643 at Liturgy (para 3442):
txt = txt.replace(
    'Leavetaking of the Resurrection.\nWe suppose that also on some other days',
    'Leavetaking of the Resurrection[^643].\nWe suppose that also on some other days'
)
md = md.replace(
    'Leavetaking of the Resurrection.\n\nWe suppose that also on some other days',
    'Leavetaking of the Resurrection[^643].\n\nWe suppose that also on some other days'
)

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully applied Part 4 monotonicity cleanup!")
