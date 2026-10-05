import re

with open(r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_part3_menaion.txt', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    # Fix 249 double print from previous run
    (r'Communion Hymn - to the Renovation\[\^249\]\.\^249\]\.', r'Communion Hymn - to the Renovation[^249].'),
    # 250
    (r'Communion Hymn - "Praise the Lord"!', r'Communion Hymn - "Praise the Lord"[^250]'), # If it's isolated
    (r'r the Prokeimenon \(zaspiv\)\), Communion Hymn - "Praise the Lord"', r'r the Prokeimenon (zaspiv)), Communion Hymn - "Praise the Lord"[^250]'),
    (r'and of the sequential under the section\), also of the feast\. Communion Hymn - "Praise the Lord" and of the feast', r'and of the sequential under the section), also of the feast. Communion Hymn - "Praise the Lord" and of the feast[^251]'),
    (r'only Communion Hymn - "Praise the Lord" and of the', r'only Communion Hymn - "Praise the Lord" and of the[^252]'),
    (r'Apostle-Gospel - under the Prokeimenon \(zaspiv\) of the Sunday before the Exaltation\)', r'Apostle-Gospel - under the Prokeimenon (zaspiv) of the Sunday before the Exaltation)[^253]'),
    (r'12 SEPTEMBER Memory of the Renovation of the Temple of the Resurrection', r'12 SEPTEMBER Memory of the Renovation of the Temple of the Resurrection[^254]'),
]

for orig, repl in replacements:
    old_text = text
    text = re.sub(orig, repl, text, flags=re.IGNORECASE)
    if text != old_text:
        print(f"Successfully replaced for {repl[-6:]}")

with open(r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_part3_menaion.txt', 'w', encoding='utf-8') as f:
    f.write(text)
