import re
from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

print("Executing comprehensive Part 3 monotonicity fix...")

# 1. Strip [^370] from September in MD & TXT
md = re.sub(r'sequential\[\^370\]', 'sequential', md)
txt = re.sub(r'sequential\[\^370\]', 'sequential', txt)

# 2. Strip premature [^418] from Eve of Nativity in MD & TXT
md = md.replace('Psalm "I will bless the Lord"[^418]', 'Psalm "I will bless the Lord"')
txt = txt.replace('Psalm "I will bless the Lord"[^418]', 'Psalm "I will bless the Lord"')

# 3. Strip premature [^426] from Circumcision in MD & TXT
md = md.replace('Psalter or *Menaion*[^426]', 'Psalter or *Menaion*')
md = md.replace('Psalter or Menaion[^426]', 'Psalter or Menaion')
txt = txt.replace('Psalter or Menaion[^426]', 'Psalter or Menaion')

# 4. Strip premature [^417] from Theophany in MD & TXT
md = md.replace('Sessional hymn of the Feast[^417];', 'Sessional hymn of the Feast;')
txt = txt.replace('Sessional hymn of the Feast[^417];', 'Sessional hymn of the Feast;')

# 5. Fix Para 1225 and Para 1257 (FN 313 & 320)
# In MD:
# Remove spurious [^320] from L1039
md = md.replace('"O come, let us worship" inclusive[^320]', '"O come, let us worship" inclusive')
# Remove second spurious [^313] from L1153
md = re.sub(r'\[\^313\](\s*\[\^323\])', r'\1', md)
md = md.replace('Bows low and begins the usual: "Blessed is our God"[^313]', 'Bows low and begins the usual: "Blessed is our God"')
# Ensure [^320] is at Para 1257:
# "as usual, up to \"O come, let us worship\" inclusive." under Royal Hours on Friday
md = md.replace(
    'as usual, up to "O come, let us worship" inclusive.\n\n3. After the second',
    'as usual, up to "O come, let us worship" inclusive[^320].\n\n3. After the second'
)

# 6. Premature [^381] in January
md = md.replace('Entrance[^381]', 'Entrance')
txt = txt.replace('Entrance[^381]', 'Entrance')

# Ensure [^381] is at February 24:
# "Entrance, Prokimenon of the day from the Horologion, 3 readings to the Forerunner"
md = md.replace('Entrance, Prokimenon of the day', 'Entrance[^381], Prokimenon of the day')
txt = txt.replace('Entrance, Prokimenon of the day', 'Entrance[^381], Prokimenon of the day')

# 7. Premature [^393] on February 24 heading
md = md.replace('RULES FOR THE ABOVE-MENTIONED CASES[^393]', 'RULES FOR THE ABOVE-MENTIONED CASES')
txt = txt.replace('RULES FOR THE ABOVE-MENTIONED CASES[^393]', 'RULES FOR THE ABOVE-MENTIONED CASES')

# Ensure [^393] is at March 24:
# "RULES FOR THE ABOVE-MENTIONED CASES" before "1. Forefeast of the Annunciation"
md = re.sub(
    r'(RULES FOR THE ABOVE-MENTIONED CASES)(\s+#####\s+1\.\s+Forefeast of the Annunciation)',
    r'\1[^393]\2',
    md
)
txt = re.sub(
    r'(RULES FOR THE ABOVE-MENTIONED CASES)(\s+1\.\s+FOREFEAST OF THE ANNUNCIATION)',
    r'\1[^393]\2',
    txt
)

# 8. Premature [^412] in March
md = md.replace('Kontakion of the Feast[^412]', 'Kontakion of the Feast')
txt = txt.replace('Kontakion of the Feast[^412]', 'Kontakion of the Feast')
# Re-attach [^412] to its true location in March 25 (Great Monday/Tuesday/Wednesday):
# DOCX: "the Feast, after the 2nd – Kontakion of the Feast."
md = md.replace(
    'the Feast, after the 2nd – Kontakion of the Feast.\n\n##### At the Litya',
    'the Feast, after the 2nd – Kontakion of the Feast[^412].\n\n##### At the Litya'
)
md = md.replace(
    'the Feast, after the 2nd – Kontakion of the Feast.\n\nAt the Litya',
    'the Feast, after the 2nd – Kontakion of the Feast[^412].\n\nAt the Litya'
)

# 9. Premature [^409] in March
# DOCX: "Akathist they prescribe on 6 and of the Feast on 8."
md = md.replace('of the Feast on 8.\n\n', 'of the Feast on 8[^409].\n\n')
txt = txt.replace('of the Feast on 8.\n', 'of the Feast on 8[^409].\n')

# 10. Premature [^438]
md = md.replace('Both now: of the Ascension[^438]', 'Both now: of the Ascension')
txt = txt.replace('Both now: of the Ascension[^438]', 'Both now: of the Ascension')
# Re-attach [^438] to its true home:
# DOCX: "Glory: of the Apostle, Both now: of the Ascension."
md = md.replace(
    'Glory: of the Apostle, Both now: of the Ascension.\n\n##### At the Divine Liturgy',
    'Glory: of the Apostle, Both now: of the Ascension[^438].\n\n##### At the Divine Liturgy'
)
txt = txt.replace(
    'Glory: of the Apostle, Both now: of the Ascension.\nAT THE LITURGY',
    'Glory: of the Apostle, Both now: of the Ascension[^438].\nAT THE LITURGY'
)

# Write back
txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Finished applying Part 3 monotonicity fixes!")
