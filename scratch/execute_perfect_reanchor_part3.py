import re
from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')

txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

print("Starting surgical Part 3 re-anchoring...")

# ----------------- CLEAN SPURIOUS LATER TAGS FIRST -----------------
# Remove spurious [^248] that were injected into later chapters
# In TXT:
# Lines like "Monday, Tuesday and Wednesday, here on p. 264-265, only, instead of the Liturgy of Chrysostom...[^248]"
txt = re.sub(r'(\bp\.\s*264-265[^\n]*?)\[\^248\]', r'\1', txt)
txt = re.sub(r'(Reader – readings[^\n]*?)\[\^248\]', r'\1', txt)
txt = re.sub(r'(first of the day[^\n]*?)\[\^248\]', r'\1', txt)
# Spurious [^277] in July:
txt = re.sub(r'(Saint with All-Night Vigil)\[\^277\](\s+on Sunday\[\^445\])', r'\1\2', txt)

# In MD:
md = re.sub(r'(\bp\.\s*264-265[^\n]*?)\[\^248\]', r'\1', md)
md = re.sub(r'(Reader  readings[^\n]*?)\[\^248\]', r'\1', md)
md = re.sub(r'(first of the day[^\n]*?)\[\^248\]', r'\1', md)
md = re.sub(r'(Saint with All-Night Vigil)\[\^277\](\s+on Sunday\[\^445\])', r'\1\2', md)
md = re.sub(r'(Sunday of the Myrrh-bearers[^\n]*?)\[\^277\]', r'\1', md)

# Also strip spurious [^277] from October 26 in TXT and MD:
# TXT:
txt = txt.replace("Saint with All-Night Vigil[^277] on Sunday, only at the end", "Saint with All-Night Vigil on Sunday, only at the end")
txt = txt.replace("Saint with All-Night Vigil[^277]; only at \"Lord, I have cried\"", "Saint with All-Night Vigil; only at \"Lord, I have cried\"")
txt = txt.replace("Saint with All-Night Vigil[^277] on Sunday; only canons", "Saint with All-Night Vigil on Sunday; only canons")

# MD:
md = md.replace("Saint with All-Night Vigil[^277] on Sunday, only at the end", "Saint with All-Night Vigil on Sunday, only at the end")
md = md.replace("Saint with All-Night Vigil[^277]; only at *Lord, I have cried*", "Saint with All-Night Vigil; only at *Lord, I have cried*")
md = md.replace("Saint with All-Night Vigil[^277]; only at *“Lord, I have cried”*", "Saint with All-Night Vigil; only at *“Lord, I have cried”*")
md = md.replace("Saint with All-Night Vigil[^277] on Sunday; only canons", "Saint with All-Night Vigil on Sunday; only canons")

# ----------------- FIX TXT SPECIFICS -----------------
# 247: Fix double [^247][^247]
txt = txt.replace("Communion Hymn of the weekday[^247][^247].", "Communion Hymn of the weekday[^247].")

# 248: Add [^248]
txt = txt.replace(
    "first to the Saturday before the Exaltation, afterwards - to the Feast.",
    "first to the Saturday before the Exaltation, afterwards - to the Feast[^248]."
)

# 249: Add [^249]
txt = txt.replace(
    "afterwards - to the Saturday before the Exaltation, Communion Hymn - to the Renovation.",
    "afterwards - to the Saturday before the Exaltation, Communion Hymn - to the Renovation[^249]."
)

# 252: Replace duplicate [^251] with [^252]
txt = txt.replace(
    "III. In the Afterfeast of the Nativity of the Most Holy Theotokos\nEverything as above in the Forefeast, only the Communion Hymn - \"Praise the Lord\" and of the Feast[^251].",
    "III. In the Afterfeast of the Nativity of the Most Holy Theotokos\nEverything as above in the Forefeast, only the Communion Hymn - \"Praise the Lord\" and of the Feast[^252]."
)

# 253: Add [^253]
txt = txt.replace(
    "(According to the Slavic typikon, Apostle-Gospel - under the Prokimenon (zaspiv) of the Sunday before the Exaltation).",
    "(According to the Slavic typikon, Apostle-Gospel - under the Prokimenon (zaspiv) of the Sunday before the Exaltation)[^253]."
)

# 271: Add [^271]
txt = txt.replace(
    "as other feasts are usually transferred, but to the previous one.\n________________________________________",
    "as other feasts are usually transferred, but to the previous one[^271].\n________________________________________"
)

# 275: Add [^275]
txt = txt.replace(
    "everything - only sequential of the Sunday and to the Saint.\n31 OCTOBER",
    "everything - only sequential of the Sunday and to the Saint[^275].\n31 OCTOBER"
)

# 276: Fix double [^276][^276]
txt = txt.replace(
    "transferring it from a weekday to Sunday[^276][^276].",
    "transferring it from a weekday to Sunday[^276]."
)

# 277: Fix double [^277][^277]
txt = txt.replace(
    "Saint with All-Night Vigil[^277][^277].",
    "Saint with All-Night Vigil[^277]."
)


# ----------------- FIX MD SPECIFICS -----------------
# 248: Add [^248]
md = md.replace(
    "Apostle-Gospel  first to the Saturday before the Exaltation, afterwards  to the Feast",
    "Apostle-Gospel  first to the Saturday before the Exaltation, afterwards  to the Feast[^248]"
)
md = md.replace(
    "Apostle-Gospel – first to the Saturday before the Exaltation, afterwards – to the Feast",
    "Apostle-Gospel – first to the Saturday before the Exaltation, afterwards – to the Feast[^248]"
)

# 249: Add [^249]
md = md.replace(
    "Apostle-Gospel  first to the Renovation, and afterwards  to the Saturday before the Exaltation, Communion Hymn  to the Renovation.",
    "Apostle-Gospel  first to the Renovation, and afterwards  to the Saturday before the Exaltation, Communion Hymn  to the Renovation[^249]."
)
md = md.replace(
    "Apostle-Gospel – first to the Renovation, and afterwards – to the Saturday before the Exaltation, Communion Hymn – to the Renovation.",
    "Apostle-Gospel – first to the Renovation, and afterwards – to the Saturday before the Exaltation, Communion Hymn – to the Renovation[^249]."
)

# 250: Add [^250]
md = md.replace(
    "Communion Hymn  \"Praise the Lord\"",
    "Communion Hymn  \"Praise the Lord\"[^250]"
)
md = md.replace(
    "Communion Hymn – *“Praise the Lord”*",
    "Communion Hymn – *“Praise the Lord”*[^250]"
)

# 251: Add [^251]
md = md.replace(
    "Communion Hymn  \"Praise the Lord\" and of the Feast\n\n#### III. In the Afterfeast",
    "Communion Hymn  \"Praise the Lord\" and of the Feast[^251]\n\n#### III. In the Afterfeast"
)
md = md.replace(
    "Communion Hymn – *“Praise the Lord”* and of the Feast\n\n#### III. In the Afterfeast",
    "Communion Hymn – *“Praise the Lord”* and of the Feast[^251]\n\n#### III. In the Afterfeast"
)

# 252: Add [^252]
md = md.replace(
    "#### III. In the Afterfeast of the Nativity of the Most Holy Theotokos\n\nEverything as above in the Forefeast, only the Communion Hymn  \"Praise the Lord\" and of the Feast.",
    "#### III. In the Afterfeast of the Nativity of the Most Holy Theotokos\n\nEverything as above in the Forefeast, only the Communion Hymn  \"Praise the Lord\" and of the Feast[^252]."
)
md = md.replace(
    "#### III. In the Afterfeast of the Nativity of the Most Holy Theotokos\n\nEverything as above in the Forefeast, only the Communion Hymn – *“Praise the Lord”* and of the Feast.",
    "#### III. In the Afterfeast of the Nativity of the Most Holy Theotokos\n\nEverything as above in the Forefeast, only the Communion Hymn – *“Praise the Lord”* and of the Feast[^252]."
)

# 253: Add [^253]
md = md.replace(
    "(According to the Slavic typikon, Apostle-Gospel  under the Prokimenon (refrain) of the Sunday before the Exaltation)",
    "(According to the Slavic typikon, Apostle-Gospel  under the Prokimenon (refrain) of the Sunday before the Exaltation)[^253]"
)
md = md.replace(
    "(According to the Slavic typikon, Apostle-Gospel – under the Prokimenon (refrain) of the Sunday before the Exaltation)",
    "(According to the Slavic typikon, Apostle-Gospel – under the Prokimenon (refrain) of the Sunday before the Exaltation)[^253]"
)

# 254: Add [^254]
md = md.replace(
    "### 3.1.3 September: Memory of the Renovation of the Temple of the Resurrection\n",
    "### 3.1.3 September: Memory of the Renovation of the Temple of the Resurrection[^254]\n"
)

# 255: Add [^255]
md = md.replace(
    "* *After the 3rd Ode:* Kontakion and Sessional hymn of the Renovation;",
    "* *After the 3rd Ode:* Kontakion[^255] and Sessional hymn of the Renovation;"
)

# 271: Add [^271]
md = md.replace(
    "as other feasts are usually transferred, but to the previous one.\n\n---",
    "as other feasts are usually transferred, but to the previous one[^271].\n\n---"
)

# 272: Restore missing item 1 under 3.2.2 October: Sunday of the Holy Fathers
fathers_old = """### 3.2.2 October: Sunday of the Holy Fathers

of the VII Ecumenical Council against the iconoclasts

Notes

#### On a Sunday"""

fathers_new = """### 3.2.2 October: Sunday of the Holy Fathers

of the VII Ecumenical Council against the iconoclasts

Notes

1. If 11 October falls on a Sunday, then the Service of the Holy Fathers is sung on the same Sunday; if – on another day, then it is sung on the nearest Sunday, whether previous or following. On the previous, if 11 October falls on Wednesday, Tuesday or Monday; on the following, if it falls on Thursday, Friday or Saturday[^272]. The Service of the Saint that falls on the same Sunday must be transferred to another day, at the decision of the Ecclesiarch, as the *Menaion* gives.

#### On a Sunday"""

md = md.replace(fathers_old, fathers_new)

# 275: Add [^275]
md = md.replace(
    "everything  only sequential of the Sunday and to the Saint.\n\n### 3.2.4 October: Holy Priest-Martyr Josaphat",
    "everything  only sequential of the Sunday and to the Saint[^275].\n\n### 3.2.4 October: Holy Priest-Martyr Josaphat"
)
md = md.replace(
    "everything – only sequential of the Sunday and to the Saint.\n\n### 3.2.4 October: Holy Priest-Martyr Josaphat",
    "everything – only sequential of the Sunday and to the Saint[^275].\n\n### 3.2.4 October: Holy Priest-Martyr Josaphat"
)

# 276: Fix double [^276][^276]
md = md.replace(
    "transferring it from a weekday to Sunday[^276][^276].",
    "transferring it from a weekday to Sunday[^276]."
)

# 277: Fix double [^277][^277]
md = md.replace(
    "Saint with All-Night Vigil[^277][^277].",
    "Saint with All-Night Vigil[^277]."
)

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully written modified TXT and MD files!")
