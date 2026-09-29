import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent.parent

txt_path = root / 'Final/Final_Dolnytsky_part2_general_rubrics.txt'
md_path = root / 'Final MD/Final_Dolnytsky_part2_general_rubrics.md'

txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

print("Applying Part 2 remediations...")

# 1. FN 88
assert 'at the 6th - to the temple, at the 9th - to the second saint.\n' in txt
txt = txt.replace('at the 6th - to the temple, at the 9th - to the second saint.\n',
                  'at the 6th - to the temple, at the 9th - to the second saint[^88].\n', 1)

assert '3rd Hour—first saint; 6th Hour—Temple; 9th Hour—second saint.\n' in md
md = md.replace('3rd Hour—first saint; 6th Hour—Temple; 9th Hour—second saint.\n',
                '3rd Hour—first saint; 6th Hour—Temple; 9th Hour—second saint[^88].\n', 1)

# 2. FN 104
old_txt_104 = '1.\tOn "God is the Lord" - Troparion of the saint twice, Glory, Both now: Theotokion from the Sunday ones in the tone of the saint\'s troparion.\n'
new_txt_104 = '1.\tOn "God is the Lord" - Troparion of the saint twice, Glory, Both now: Theotokion from the Sunday ones in the tone of the saint\'s troparion[^104].\n'
assert old_txt_104 in txt
txt = txt.replace(old_txt_104, new_txt_104, 1)

old_md_104 = '1. **On *"God is the Lord"*:* Troparion of the saint twice; **Glory, Both now:** Sunday Theotokion in the tone of the saint\'s troparion.\n'
new_md_104 = '1. **On *"God is the Lord"*:* Troparion of the saint twice; **Glory, Both now:** Sunday Theotokion in the tone of the saint\'s troparion[^104].\n'
assert old_md_104 in md
md = md.replace(old_md_104, new_md_104, 1)

# 3. FN 112
# remove spurious in TXT L87
assert "in the tone of the saint's troparion and of the day of the week[^112].\n" in txt
txt = txt.replace("in the tone of the saint's troparion and of the day of the week[^112].\n",
                  "in the tone of the saint's troparion and of the day of the week.\n", 1)

# add to MD L245
old_md_112 = "6. **Conclusion:** Troparion of the saint; **Glory, Both now:** Daily Dismissal Theotokion in the tone of the saint's troparion and day of the week.\n"
new_md_112 = "6. **Conclusion:** Troparion of the saint; **Glory, Both now:** Daily Dismissal Theotokion in the tone of the saint's troparion and day of the week[^112].\n"
assert old_md_112 in md
md = md.replace(old_md_112, new_md_112, 1)

# 4. FN 115
# remove spurious in TXT L119
assert "service is taken both of the day and to the saint[^115], then" in txt
txt = txt.replace("service is taken both of the day and to the saint[^115], then",
                  "service is taken both of the day and to the saint, then", 1)

# add to MD L257
old_md_115 = "Apostle and Gospel first of the day, then of the saint.\n"
new_md_115 = "Apostle and Gospel first of the day, then of the saint[^115].\n"
assert old_md_115 in md
md = md.replace(old_md_115, new_md_115, 1)

# 5. FN 123 (add to TXT L179)
assert "and of the Theotokos on 2, and of the saint on 8[^124]" in txt
txt = txt.replace("and of the Theotokos on 2, and of the saint on 8[^124]",
                  "and of the Theotokos on 2[^123], and of the saint on 8[^124]", 1)

# 6. FN 134
assert 'Canon of the Theotokos from the Octoechos of the current tone. After "It is truly meet" with the Trisagion - Kontakion to the saint alone[^135].' in txt
txt = txt.replace('Canon of the Theotokos from the Octoechos of the current tone. After "It is truly meet" with the Trisagion - Kontakion to the saint alone[^135].',
                  'Canon of the Theotokos from the Octoechos of the current tone[^134]. After "It is truly meet" with the Trisagion - Kontakion to the saint alone[^135].', 1)

assert '* Canon to the Theotokos from the *Octoechos* of the current tone. After *“It is truly meet”* and the Trisagion: Kontakion of the saint alone[^135].' in md
md = md.replace('* Canon to the Theotokos from the *Octoechos* of the current tone. After *“It is truly meet”* and the Trisagion: Kontakion of the saint alone[^135].',
                '* Canon to the Theotokos from the *Octoechos* of the current tone[^134]. After *“It is truly meet”* and the Trisagion: Kontakion of the saint alone[^135].', 1)

# 7. FN 144
assert '5.\tOn the Aposticha: stichera of the Sunday tone, Glory: to the saint, Both now: Theotokion from the Sunday Aposticha of Great Vespers, in the tone of the Doxastikon.\n' in txt
txt = txt.replace('5.\tOn the Aposticha: stichera of the Sunday tone, Glory: to the saint, Both now: Theotokion from the Sunday Aposticha of Great Vespers, in the tone of the Doxastikon.\n',
                  '5.\tOn the Aposticha: stichera of the Sunday tone, Glory: to the saint, Both now: Theotokion from the Sunday Aposticha of Great Vespers, in the tone of the Doxastikon[^144].\n', 1)

assert '5. **Aposticha:** Sunday stichera; **Glory:** to the saint, **Both now:** Sunday Theotokion in the tone of the Doxastikon.\n' in md
md = md.replace('5. **Aposticha:** Sunday stichera; **Glory:** to the saint, **Both now:** Sunday Theotokion in the tone of the Doxastikon.\n',
                '5. **Aposticha:** Sunday stichera; **Glory:** to the saint, **Both now:** Sunday Theotokion in the tone of the Doxastikon[^144].\n', 1)

# 8. FN 146
assert "1.\tOn \"God is the Lord\": Sunday Troparion twice, Glory: to the saint, Both now: Theotokion from the Sunday ones in the tone of the saint's troparion.\n" in txt
txt = txt.replace("1.\tOn \"God is the Lord\": Sunday Troparion twice, Glory: to the saint, Both now: Theotokion from the Sunday ones in the tone of the saint's troparion.\n",
                  "1.\tOn \"God is the Lord\": Sunday Troparion twice, Glory: to the saint, Both now: Theotokion from the Sunday ones in the tone of the saint's troparion[^146].\n", 1)

assert "1. **On *\"God is the Lord\"*:* Sunday troparion twice; **Glory:** to the saint, **Both now:** Sunday Theotokion in the tone of the saint's troparion.\n" in md
md = md.replace("1. **On *\"God is the Lord\"*:* Sunday troparion twice; **Glory:** to the saint, **Both now:** Sunday Theotokion in the tone of the saint's troparion.\n",
                "1. **On *\"God is the Lord\"*:* Sunday troparion twice; **Glory:** to the saint, **Both now:** Sunday Theotokion in the tone of the saint's troparion[^146].\n", 1)

# 9. FN 149
assert 'Sunday Exaposteilarion, Glory: to the saint, Both now: Theotokion of the Sunday Exaposteilarion\n' in txt
txt = txt.replace('Sunday Exaposteilarion, Glory: to the saint, Both now: Theotokion of the Sunday Exaposteilarion\n',
                  'Sunday Exaposteilarion, Glory: to the saint, Both now: Theotokion of the Sunday Exaposteilarion[^149]\n', 1)

assert 'Sunday Exaposteilarion; **Glory:** to the saint, **Both now:** Theotokion of the Sunday Exaposteilarion.\n' in md
md = md.replace('Sunday Exaposteilarion; **Glory:** to the saint, **Both now:** Theotokion of the Sunday Exaposteilarion.\n',
                'Sunday Exaposteilarion; **Glory:** to the saint, **Both now:** Theotokion of the Sunday Exaposteilarion[^149].\n', 1)

# 10. FN 192 (restore in MD L587)
old_md_192 = '1. **Antiphons:** Sunday Antiphons.\n'
new_md_192 = '1. **Antiphons & Entrance:** Sunday Antiphons. On *“Come, let us worship”*, if you wish, to *“Save us, O Son of God”* add the refrain: *“Through the prayers of the Theotokos, who sing to Thee, Alleluia”*[^192].\n'
assert old_md_192 in md
md = md.replace(old_md_192, new_md_192, 1)

# 11. FN 217 (add to MD L746)
old_md_217 = '## 2.16 Afterfeast with a Saint with a Polyeleos on Weekdays\n'
new_md_217 = '## 2.16 Afterfeast with a Saint with a Polyeleos on Weekdays[^217]\n'
assert old_md_217 in md
md = md.replace(old_md_217, new_md_217, 1)

# 12. FN 223
assert '3 of the feast and 3 to the saint, Glory: to the saint' in txt
txt = txt.replace('3 of the feast and 3 to the saint, Glory: to the saint',
                  '3 of the feast and 3 to the saint[^223], Glory: to the saint', 1)

old_md_223 = '5. **Praises (Lauds):** 4 or 6 stichera (3 of the Feast, 3 of the saint)[^222]; **Glory:** to the saint, **Both now:** of the Feast.\n'
new_md_223 = '5. **Praises (Lauds):** Sometimes 4 stichera to the saint[^222], sometimes 6 (3 of the Feast, 3 of the saint)[^223]; **Glory:** to the saint, **Both now:** of the Feast.\n'
assert old_md_223 in md
md = md.replace(old_md_223, new_md_223, 1)

# 13. Spurious removals in TXT
# Remove spurious [^196] from TXT L91
assert 'then first - of the day[^196], and then - of the temple.' in txt
txt = txt.replace('then first - of the day[^196], and then - of the temple.',
                  'then first - of the day, and then - of the temple.', 1)

# Remove spurious [^227] from TXT L227
assert 'twice and to the saint once[^227][^145].' in txt
txt = txt.replace('twice and to the saint once[^227][^145].',
                  'twice and to the saint once[^145].', 1)

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully written Part 2 remediations!")
