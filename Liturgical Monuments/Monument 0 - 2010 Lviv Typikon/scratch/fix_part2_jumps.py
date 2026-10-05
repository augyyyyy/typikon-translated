import re
from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part2_general_rubrics.txt')
md_path = Path('Final MD/Final_Dolnytsky_part2_general_rubrics.md')

txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

print("Remediating Part 2 backward jumps...")

# 1. FN 123:
# Premature in Chapter 2 at MD L103 / TXT L103
# "Two canons from the Octoechos on 6 (Resurrection with Heirmos on 4, Theotokos on 2[^123])"
md = md.replace('Theotokos on 2[^123]', 'Theotokos on 2')
txt = txt.replace('Theotokos on 2[^123]', 'Theotokos on 2')
# True home: Chapter 3 (para 519)
# "with the Irmos on 4 and of the Theotokos on 2, and of the saint on 8"
md = md.replace('with the Heirmos on 4 and of the Theotokos on 2, and of the Saint on 8', 'with the Heirmos on 4 and of the Theotokos on 2[^123], and of the Saint on 8')
md = md.replace('with the Heirmos on 4 and of the Theotokos on 2, and of the saint on 8', 'with the Heirmos on 4 and of the Theotokos on 2[^123], and of the saint on 8')
txt = txt.replace('with the heirmos on 4 and of the Theotokos on 2, and of the Saint on 8', 'with the heirmos on 4 and of the Theotokos on 2[^123], and of the Saint on 8')
txt = txt.replace('with the heirmos on 4 and of the Theotokos on 2, and of the saint on 8', 'with the heirmos on 4 and of the Theotokos on 2[^123], and of the saint on 8')

# 2. FN 112:
# Premature in Chapter 2 at MD L145 / TXT
md = md.replace('Dismissal Theotokion from the *Octoechos*[^112]', 'Dismissal Theotokion from the *Octoechos*')
txt = txt.replace('Dismissal Theotokion from the Octoechos[^112]', 'Dismissal Theotokion from the Octoechos')
# True home: Chapter 3 (para 494)
# "Dismissal Theotokion in the tone of the saint's troparion and of the day of the week"
md = md.replace('Dismissal Theotokion in the tone of the saint\'s troparion and of the day of the week.', 'Dismissal Theotokion in the tone of the saint\'s troparion and of the day of the week[^112].')
txt = txt.replace('Dismissal Theotokion in the tone of the saint\'s troparion and of the day of the week.', 'Dismissal Theotokion in the tone of the saint\'s troparion and of the day of the week[^112].')

# 3. FN 196:
# Premature in Chapter 2 at MD L151
md = md.replace('from Small Compline[^196]', 'from Small Compline')
txt = txt.replace('from Small Compline[^196]', 'from Small Compline')
# True home: Chapter 5/6 (para 703)
# "Apostle and Gospel – of the day"
md = md.replace('Apostle and Gospel – of the day.\n\nWhen on Sunday', 'Apostle and Gospel – of the day[^196].\n\nWhen on Sunday')
txt = txt.replace('Apostle and Gospel - of the day.\nWhen on Sunday', 'Apostle and Gospel - of the day[^196].\nWhen on Sunday')

# 4. FN 119 & 121:
# Premature in Chapter 2 at MD L159
md = md.replace('troparion[^121][^119]', 'troparion')
txt = txt.replace('troparion[^121][^119]', 'troparion')
# True home for 119: Chapter 3 para 511
# True home for 121: Chapter 3 para 516
md = md.replace('Dismissal Theotokion in the tone of the saint\'s troparion.\n\n2. Kathismata', 'Dismissal Theotokion in the tone of the saint\'s troparion[^119].\n\n2. Kathismata')
txt = txt.replace('Dismissal Theotokion in the tone of the saint\'s troparion.\nKathismata', 'Dismissal Theotokion in the tone of the saint\'s troparion[^119].\nKathismata')
md = md.replace('Dismissal Theotokion in the tone of the saint\'s troparion.\n\n3. Canons', 'Dismissal Theotokion in the tone of the saint\'s troparion[^121].\n\n3. Canons')
txt = txt.replace('Dismissal Theotokion in the tone of the saint\'s troparion.\nCanons', 'Dismissal Theotokion in the tone of the saint\'s troparion[^121].\nCanons')

# 5. FN 115:
# Premature in Chapter 2 at MD L194
md = md.replace('then of the saint[^115]', 'then of the saint')
txt = txt.replace('then of the saint[^115]', 'then of the saint')
# True home: Chapter 3 para 501
# "Apostle-Gospel of the day and to the saint"
md = md.replace('Apostle-Gospel of the day and to the saint.', 'Apostle-Gospel of the day and to the saint[^115].')
txt = txt.replace('Apostle-Gospel of the day and to the saint.', 'Apostle-Gospel of the day and to the saint[^115].')

# 6. FN 134:
# Premature in Chapter 2 Compline at MD L222
md = md.replace('Octoechos* of the current tone[^134].', 'Octoechos* of the current tone.')
txt = txt.replace('Octoechos of the current tone[^134].', 'Octoechos of the current tone.')
# True home: Chapter 4 Great Doxology Compline para 539
# "Canon to the Theotokos from the Octoechos of the current tone"
md = md.replace('Theotokos from the *Octoechos* of the current tone.\n\nAfter *“It is truly meet”*', 'Theotokos from the *Octoechos* of the current tone[^134].\n\nAfter *“It is truly meet”*')
txt = txt.replace('Theotokos from the Octoechos of the current tone.\nAfter "It is truly meet"', 'Theotokos from the Octoechos of the current tone[^134].\nAfter "It is truly meet"')

# 7. FN 125 and 126 swapped in MD L285-286:
md = md.replace('Saint on 8[^126]', 'Saint on 8')
md = md.replace('Saint on 6[^125].', 'Saint on 6[^125].')
md = md.replace('is not taken.\n\n', 'is not taken[^126].\n\n')

# 8. FN 143, 144, 153 cluster at MD L363 / TXT
md = md.replace('tone of the Doxastikon[^153][^144][^143]', 'tone of the Doxastikon[^143]')
txt = txt.replace('tone of the Doxastikon[^153][^144][^143]', 'tone of the Doxastikon[^143]')
# True home for 144: Para 564
# True home for 153: Para 581
md = md.replace('Sunday Great Vespers, in the tone of the Doxastikon.', 'Sunday Great Vespers, in the tone of the Doxastikon[^153].')
txt = txt.replace('Sunday Great Vespers, in the tone of the Doxastikon.', 'Sunday Great Vespers, in the tone of the Doxastikon[^153].')

# 9. FN 227 and 145 cluster at MD L365:
md = md.replace('twice, and of the saint once[^227][^145].', 'twice, and of the saint once[^145].')
txt = txt.replace('twice, and of the saint once[^227][^145].', 'twice, and of the saint once[^145].')
# True home for 227: Para 821 (Chapter 6 All-Night Vigil)
md = md.replace('twice and to the saint once.\n\n7. Litany', 'twice and to the saint once[^227].\n\n7. Litany')
txt = txt.replace('twice and to the saint once.\nLitany', 'twice and to the saint once[^227].\nLitany')

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully remediated Part 2 backward jumps!")
