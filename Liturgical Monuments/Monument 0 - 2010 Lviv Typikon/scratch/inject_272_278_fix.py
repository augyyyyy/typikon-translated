import re

with open(r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_part3_menaion.txt', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    # 272
    (r'falls on Thursday, Friday or Saturday\.', r'falls on Thursday, Friday or Saturday[^272].'),
    # 275
    (r'nothing - of the Earthquake, but everything - only sequential of the Sunday and to the Saint\.', r'nothing - of the Earthquake, but everything - only sequential of the Sunday and to the Saint[^275].'),
    # 276
    (r'31 OCTOBER Saint Hieromartyr Josaphat,', r'31 OCTOBER Saint Hieromartyr Josaphat,[^276]'),
    (r'transferring it from a weekday to a Sunday\.', r'transferring it from a weekday to a Sunday[^276].'),
    # 277
    (r'Synaxis of St\. Archangel Michael', r'Synaxis of St. Archangel Michael[^277]'),
    (r'service according to the general rule of a Saint with an All-Night Vigil\.', r'service according to the general rule of a Saint with an All-Night Vigil[^277].'),
    # 278
    (r'5 "Our Father" and 5 "Rejoice, O Virgin Theotokos" for the faithful', r'5 "Our Father" and 5 "Rejoice, O Virgin Theotokos"[^278] for the faithful'),
]

for orig, repl in replacements:
    old_text = text
    text = re.sub(orig, repl, text, flags=re.IGNORECASE)
    if text != old_text:
        print(f"Successfully placed for {repl[-6:]}")

with open(r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_part3_menaion.txt', 'w', encoding='utf-8') as f:
    f.write(text)
