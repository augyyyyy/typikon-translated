import re

with open(r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_part3_menaion.txt', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    # 256
    (r'on the 6th - of the Forefeast, on the 9th again - of the Renovation\.',
     r'on the 6th - of the Forefeast, on the 9th again - of the Renovation[^256].'),
    # 257
    (r'on the 6th - of the Forefeast, on the 9th - Resurrectional\.',
     r'on the 6th - of the Forefeast, on the 9th - Resurrectional[^257].'),
    # 258
    (r'Strict fast on this day the Lviv Synod permits for dairy\.',
     r'Strict fast on this day the Lviv Synod permits for dairy[^258].'),
    # 259
    (r'between the basil and the Cross\.',
     r'between the basil and the Cross[^259].'),
    # 260
    (r'wearing an epitrachelion,',
     r'wearing an epitrachelion[^260],'),
    # 261
    (r'in the place of the holy Gospel,',
     r'in the place of the holy Gospel[^261],'),
    # 262
    (r'for the whole night"\.',
     r'for the whole night"[^262].'),
    # 263
    (r'withdraws behind the candle-bearers and behind the Deacon to the sacristy\.',
     r'withdraws behind the candle-bearers and behind the Deacon to the sacristy[^263].'),
    # 264
    (r'choirs sing the Troparion "Save, O Lord"\.',
     r'choirs sing the Troparion "Save, O Lord"[^264].'),
    # 265
    (r'facing east, sings solemnly',
     r'facing east, sings[^265] solemnly'),
    # 266
    (r'\("Voznesyisya"\)\.',
     r'("Voznesyisya")[^266].'),
    # 267
    (r'kiss the Precious Cross\.',
     r'kiss the Precious Cross[^267].'),
    # 268
    (r'Great Dismissal, as usual, with commemoration of the feast\.',
     r'Great Dismissal, as usual, with commemoration of the feast[^268].'),
    # 269
    (r'3\.\tCommunion Hymn "Praise the Lord" and of the Feast\.',
     r'3.\tCommunion Hymn "Praise the Lord" and of the Feast[^269].'),
    # 270
    (r'the Saint, Communion Hymn "Praise the Lord" and to the saint\.',
     r'the Saint, Communion Hymn "Praise the Lord" and to the saint[^270].'),
    # 271
    (r'other feasts are usually transferred, but to the previous one\.',
     r'other feasts are usually transferred, but to the previous one[^271].')
]

for orig, repl in replacements:
    old_text = text
    # Using re.escape for exact matching but replacing \. with \. regex syntax
    text = re.sub(orig, repl, text, flags=re.IGNORECASE)
    if text != old_text:
        print(f"Successfully placed {repl[-6:]}")
    else:
        print(f"FAILED on {repl[-6:]}")

with open(r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_part3_menaion.txt', 'w', encoding='utf-8') as f:
    f.write(text)
