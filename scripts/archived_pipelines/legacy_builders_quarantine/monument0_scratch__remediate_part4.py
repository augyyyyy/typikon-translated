import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent.parent

txt_path = root / 'Final/Final_Dolnytsky_part4_triodion.txt'
md_path = root / 'Final MD/Final_Dolnytsky_part4_triodion.md'

txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

print("Applying Part 4 remediations...")

# 1. FN 502
assert 'Canon of the Theotokos, but we sing the Canon of the Menaion' in txt
txt = txt.replace('Canon of the Theotokos, but we sing the Canon of the Menaion',
                  'Canon of the Theotokos[^502], but we sing the Canon of the Menaion', 1)

assert 'Canon of the Theotokos, but we sing the Canon of the *Menaion*' in md
md = md.replace('Canon of the Theotokos, but we sing the Canon of the *Menaion*',
                'Canon of the Theotokos[^502], but we sing the Canon of the *Menaion*', 1)

# 2. FN 516
assert 'Martyric Sessional Hymn of the Octoechos of the current tone, given also at the end of the Triodion.' in txt
txt = txt.replace('Martyric Sessional Hymn of the Octoechos of the current tone, given also at the end of the Triodion.',
                  'Martyric Sessional Hymn of the Octoechos of the current tone[^516], given also at the end of the Triodion.', 1)

assert 'Martyric Sessional Hymn of the *Octoechos* of the current tone, given also at the end of the *Triodion*.' in md
md = md.replace('Martyric Sessional Hymn of the *Octoechos* of the current tone, given also at the end of the *Triodion*.',
                'Martyric Sessional Hymn of the *Octoechos* of the current tone[^516], given also at the end of the *Triodion*.', 1)

# 3. FN 518 & 519 (MD restoration)
old_md_518_519 = '''1. In the archcathedral temple the Hours 3rd, 6th, 9th, Typika and Vespers are celebrated in this way:

2. The last prayer of the 9th Hour "O Master Lord Jesus Christ our God"'''

new_md_518_519 = '''1. In the archcathedral temple the Hours 3rd, 6th, 9th, Typika and Vespers are celebrated together, beginning at 11 o'clock in the morning, and in the afternoon, at the usual time of Vespers, – Great Compline[^518].

2. The last prayer of the 9th Hour "O Master Lord Jesus Christ" is transferred to the Typika, to the place of the prayer "O All-holy Trinity", and the prayer "O All-holy Trinity" with the psalm following it is transferred, according to the rubric of our Pochaiv Triodion, to the end of Vespers[^519]. And on Wednesday and Friday, since Vespers will be with the Presanctified, "O All-holy Trinity" cannot be transferred to the end of Vespers, for it ends with the Liturgy and therefore remains in its place at the Typika, exactly so the prayer "O Master Lord Jesus Christ" remains in its place at the 9th Hour.'''

assert old_md_518_519 in md, "old_md_518_519 not found in md"
md = md.replace(old_md_518_519, new_md_518_519, 1)

# 4. FN 521 in TXT
assert '8.\tDismissal of the day with the commemoration of the saint.\n' in txt
txt = txt.replace('8.\tDismissal of the day with the commemoration of the saint.\n',
                  '8.\tDismissal of the day with the commemoration of the saint[^521].\n', 1)

# 5. FN 545
assert 'Troparion Sunday and "We venerate Thy most pure image", Glory, Both now: Kontakion of the Triodion.' in txt
txt = txt.replace('Troparion Sunday and "We venerate Thy most pure image", Glory, Both now: Kontakion of the Triodion.',
                  'Troparion Sunday and "We venerate Thy most pure image", Glory, Both now: Kontakion of the Triodion[^545].', 1)

assert '1. **Troparia:** Troparion Sunday and "We venerate Thy most pure image", Glory, Both now: Kontakion of the *Triodion*' in md
md = md.replace('1. **Troparia:** Troparion Sunday and "We venerate Thy most pure image", Glory, Both now: Kontakion of the *Triodion*',
                '1. **Troparia:** Troparion Sunday and "We venerate Thy most pure image", Glory, Both now: Kontakion of the *Triodion*[^545].', 1)

# 6. FN 547 (MD restoration)
old_md_547 = '5. **Canons:** *Distribution:* Canons 3 on 14: of the Temple of the Lord or Theotokos with heirmos on 6, of the Saint of the *Menaion* on 4 and of the *Triodion* on 4'
new_md_547 = '5. **Canons:** *Distribution:* Canons 3 on 14: of the Temple of the Lord or Theotokos with heirmos on 6, of the Saint of the *Menaion* on 4 and of the *Octoechos* of the current tone the second[^547] on 4. If the Temple is of a Saint, then – Canon of the Saint with heirmos on 6, Temple on 4 and Octoechos on 4. From the 6th Ode, leaving the Canons of the Temple and Octoechos, we sing the Canon of the Saint of the *Menaion* on 6 and both canons of the tetraodion on 8. Refrain to the troparia of the tetraodion – "Holy Martyrs, pray to God for us". At the end of the eight troparia of each ode of the tetraodion we add two more troparia: one Martyric with the Martyric refrain, and the second – for the dead with the refrain for the dead. From the two Martyric refrains "Wondrous is God" and "To the saints that are in His earth" and from the two refrains for the dead "Their souls" and "Blessed are they Whom Thou Hast chosen", the first we refrain to the Martyric and for the dead of the 6th and 8th Odes, and the second – to the Martyric and for the dead of the 7th and 9th Odes.'

assert old_md_547 in md, "old_md_547 not found in md"
md = md.replace(old_md_547, new_md_547, 1)

# 7. FN 561
assert 'Refrain to the troparia - "Glory to Thee, our God, glory to Thee". After the 3rd Ode' in txt
txt = txt.replace('Refrain to the troparia - "Glory to Thee, our God, glory to Thee". After the 3rd Ode',
                  'Refrain to the troparia - "Glory to Thee, our God, glory to Thee"[^561]. After the 3rd Ode', 1)

assert 'Refrain to the troparia – "Glory to Thee, our God, glory to Thee". \n   * *After the 3rd Ode:*' in md
md = md.replace('Refrain to the troparia – "Glory to Thee, our God, glory to Thee". \n   * *After the 3rd Ode:*',
                'Refrain to the troparia – "Glory to Thee, our God, glory to Thee"[^561]. \n   * *After the 3rd Ode:*', 1)

# 8. FN 576
assert '\nGREAT THURSDAY\nAT MATINS' in txt
txt = txt.replace('\nGREAT THURSDAY\nAT MATINS',
                  '\nGREAT THURSDAY[^576]\nAT MATINS', 1)

assert '### 4.2.4 Great Thursday\n' in md
md = md.replace('### 4.2.4 Great Thursday\n',
                '### 4.2.4 Great Thursday[^576]\n', 1)

# 9. FN 579
assert 'at the 9th we do not sing "More honorable", nor after the 9th' in txt
txt = txt.replace('at the 9th we do not sing "More honorable", nor after the 9th',
                  'at the 9th we do not sing "More honorable"[^579], nor after the 9th', 1)

assert 'at the 9th we do not sing "More honorable", nor \n   * *After the 9th Ode:*' in md
md = md.replace('at the 9th we do not sing "More honorable", nor \n   * *After the 9th Ode:*',
                'at the 9th we do not sing "More honorable"[^579], nor \n   * *After the 9th Ode:*', 1)

# 10. Relocate FN 642, add 640 & 643
# TXT:
assert 'feast of Mid-Pentecost[^642] we take' in txt
txt = txt.replace('feast of Mid-Pentecost[^642] we take', 'feast of Mid-Pentecost we take', 1)

assert 'We conclude the troparia with the Kontakion of the Resurrection, except the Week of Thomas' in txt
txt = txt.replace('We conclude the troparia with the Kontakion of the Resurrection, except the Week of Thomas',
                  'We conclude the troparia with the Kontakion of the Resurrection[^640], except the Week of Thomas', 1)

assert 'only on Sundays[^641], on the feast of Mid-Pentecost and on the Apodosis of the Resurrection.' in txt
txt = txt.replace('only on Sundays[^641], on the feast of Mid-Pentecost and on the Apodosis of the Resurrection.',
                  'only on Sundays[^641], on the feast of Mid-Pentecost[^642] and on the Apodosis of the Resurrection[^643].', 1)

# MD:
assert 'feast of Mid-Pentecost[^642] we take' in md
md = md.replace('feast of Mid-Pentecost[^642] we take', 'feast of Mid-Pentecost we take', 1)

assert 'We conclude the troparia with the Kontakion of the Resurrection, except the Week of Thomas' in md
md = md.replace('We conclude the troparia with the Kontakion of the Resurrection, except the Week of Thomas',
                  'We conclude the troparia with the Kontakion of the Resurrection[^640], except the Week of Thomas', 1)

assert 'only on Sundays[^641], on the feast of Mid-Pentecost and on the Apodosis of the Resurrection.' in md
md = md.replace('only on Sundays[^641], on the feast of Mid-Pentecost and on the Apodosis of the Resurrection.',
                  'only on Sundays[^641], on the feast of Mid-Pentecost[^642] and on the Apodosis of the Resurrection[^643].', 1)

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully written Part 4 remediations!")
