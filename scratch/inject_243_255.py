import re

with open(r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_part3_menaion.txt', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    # 243
    (r'from the canon to the end is Great\.', r'from the canon to the end is Great[^243].'),
    # 246
    (r'on the 6th - to the Saint, on the 9th - Resurrectional', r'on the 6th - to the Saint, on the 9th - Resurrectional[^246]'),
    # 248
    (r'Saturday before the Exaltation, afterwards - to the Feast', r'Saturday before the Exaltation, afterwards - to the Feast[^248]'),
    # 250
    (r'Communion Hymn - "Praise the Lord from the heavens"!', r'Communion Hymn - "Praise the Lord from the heavens"[^250]'),
    (r'Communion Hymn - "Praise the Lord from the heavens"\.', r'Communion Hymn - "Praise the Lord from the heavens"[^250].'),
    # 251
    (r'Communion Hymn - "Praise the Lord from the heavens" and of the Feast\.', r'Communion Hymn - "Praise the Lord from the heavens" and of the Feast[^251].'),
    # 253
    (r'Apostle-Gospel - under the Prokeimenon \[zaspiv\] of the Sunday before the Exaltation\)', r'Apostle-Gospel - under the Prokeimenon [zaspiv] of the Sunday before the Exaltation)[^253]'),
    # 254
    (r'12 SEPTEMBER: Commemoration of the Renovation of the Temple of the Resurrection', r'12 SEPTEMBER: Commemoration of the Renovation of the Temple of the Resurrection[^254]'),
    # 255
    (r'After the 3rd Ode - kontakion and sessional hymn of the Renovation', r'After the 3rd Ode - kontakion[^255] and sessional hymn of the Renovation')
]

for orig, repl in replacements:
    old_text = text
    text = re.sub(orig, repl, text, flags=re.IGNORECASE)
    if text != old_text:
        print(f"Successfully replaced for {repl[-6:]}")

with open(r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_part3_menaion.txt', 'w', encoding='utf-8') as f:
    f.write(text)
