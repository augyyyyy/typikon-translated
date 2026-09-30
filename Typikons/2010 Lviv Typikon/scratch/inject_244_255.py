import re

with open(r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_part3_menaion.txt', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    (r'Glory: to the Saint, Both now: to the Indiction\.', r'Glory: to the Saint, Both now: to the Indiction[^244].'),
    (r'on the 6th - to the Saint, on the 9th - Sunday', r'on the 6th - to the Saint, on the 9th - Sunday[^246]'),
    (r'Saturday before the Exaltation, afterwards - of the Feast.', r'Saturday before the Exaltation, afterwards - of the Feast[^248].'),
    (r'afterwards - to the Saturday before the Exaltation, Communion Hymn - to the Renovation.', r'afterwards - to the Saturday before the Exaltation, Communion Hymn - to the Renovation[^249].'),
    (r'under the Prokeimenon \[zaspiv\]\), Communion Hymn - "Praise the Lord from the heavens"', r'under the Prokeimenon [zaspiv]), Communion Hymn - "Praise the Lord from the heavens"[^250]'),
    (r'Communion Hymn - "Praise the Lord from the heavens" and of the feast', r'Communion Hymn - "Praise the Lord from the heavens" and of the feast[^251]'),
    (r'only Communion Hymn - "Praise the Lord from the heavens" and of the feast\.', r'only Communion Hymn - "Praise the Lord from the heavens" and of the feast[^252].'),
    (r'Apostle-Gospel - under the Prokeimenon \[zaspiv\] of the Sunday before the Exaltation\)', r'Apostle-Gospel - under the Prokeimenon [zaspiv] of the Sunday before the Exaltation)[^253]'),
    (r'12 SEPTEMBER: Commemoration of the Renovation of the Temple of the Resurrection', r'12 SEPTEMBER: Commemoration of the Renovation of the Temple of the Resurrection[^254]'),
    (r'After the 3rd Ode - kontakion and sessional hymn of the Renovation', r'After the 3rd Ode - kontakion[^255] and sessional hymn of the Renovation')
]

for orig, repl in replacements:
    old_text = text
    text = re.sub(orig, repl, text, flags=re.IGNORECASE)
    if text != old_text:
        print(f"Successfully replaced for {repl[-6:]}")

with open(r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_part3_menaion.txt', 'w', encoding='utf-8') as f:
    f.write(text)
