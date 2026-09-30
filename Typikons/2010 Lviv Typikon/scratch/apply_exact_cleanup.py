from pathlib import Path

txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

# TXT cleanups
txt = txt.replace(
    "first of the Cross, and afterwards - of the Feast[^248].",
    "first of the Cross, and afterwards - of the Feast."
)
txt = txt.replace(
    "the service of the Hierarchs is sung according to the general rule of a Saint with All-Night Vigil[^277].",
    "the service of the Hierarchs is sung according to the general rule of a Saint with All-Night Vigil."
)
txt = txt.replace(
    "From the beginning to the canon everything - according to the general rule of a Saint with All-Night Vigil[^277];",
    "From the beginning to the canon everything - according to the general rule of a Saint with All-Night Vigil;"
)
txt = txt.replace(
    "Everything - according to the general rule of a Saint with All-Night Vigil[^277] on Sunday. Only at the end",
    "Everything - according to the general rule of a Saint with All-Night Vigil on Sunday. Only at the end"
)

# MD cleanups & replacements
md = md.replace(
    "the service of the Hierarchs is sung according to the general rule of a Saint with All-Night Vigil[^277].",
    "the service of the Hierarchs is sung according to the general rule of a Saint with All-Night Vigil."
)
md = md.replace(
    "From the beginning to the canon everything – according to the general rule of a Saint with All-Night Vigil[^277];",
    "From the beginning to the canon everything – according to the general rule of a Saint with All-Night Vigil;"
)
md = md.replace(
    "Everything – according to the general rule of a Saint with All-Night Vigil[^277] on Sunday. Only at the end",
    "Everything – according to the general rule of a Saint with All-Night Vigil on Sunday. Only at the end"
)

# 250 in MD
assert 'Communion Hymn – "Praise the Lord"\n\n#### II. On the Feast' in md
md = md.replace(
    'Communion Hymn – "Praise the Lord"\n\n#### II. On the Feast',
    'Communion Hymn – "Praise the Lord"[^250]\n\n#### II. On the Feast'
)

# 251 in MD
assert 'Communion Hymn – "Praise the Lord" and of the Feast\n\n#### III. In the Afterfeast' in md
md = md.replace(
    'Communion Hymn – "Praise the Lord" and of the Feast\n\n#### III. In the Afterfeast',
    'Communion Hymn – "Praise the Lord" and of the Feast[^251]\n\n#### III. In the Afterfeast'
)

# 252 in MD
assert 'Everything as above in the Forefeast, only the Communion Hymn – "Praise the Lord" and of the Feast.' in md
md = md.replace(
    'Everything as above in the Forefeast, only the Communion Hymn – "Praise the Lord" and of the Feast.',
    'Everything as above in the Forefeast, only the Communion Hymn – "Praise the Lord" and of the Feast[^252].'
)

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print("Successfully cleaned up TXT and MD!")
