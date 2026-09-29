import re
from pathlib import Path

txt_lines = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8').splitlines()
md_lines = Path('Final MD/Final_Dolnytsky_part3_menaion.md').read_text(encoding='utf-8').splitlines()

# Search queries for each footnote
queries = [
    (247, "Communion Hymn of the weekday"),
    (248, "first of the Saturday before the Exaltation"),
    (249, "Communion Hymn - to the Renovation", "Communion Hymn – to the Renovation"),
    (250, "Praise the Lord", "Sunday before the Exaltation alone"),
    (251, "Praise the Lord", "Sunday before the Exaltation in the Forefeast"),
    (252, "Praise the Lord", "Afterfeast of the Nativity of the Most Holy Theotokos"),
    (253, "According to Slavic typikons", "zaspiv"),
    (254, "Memory of the Renovation of the Temple"),
    (255, "Kontakion and Sessional hymn of the Renovation"),
    (256, "on the 9th again - of the Renovation", "on the 9th again – of the Renovation"),
    (257, "on the 9th - Resurrectional", "on the 9th – Resurrectional"),
    (258, "Lviv Synod permits for dairy"),
    (259, "between the basil and the Cross"),
    (260, "wearing an epitrachelion"),
    (261, "place of the holy Gospel"),
    (262, "whole night"),
    (263, "behind the Deacon to the sacristy"),
    (264, "Save, O Lord"),
    (265, "sings solemnly and joyfully"),
    (266, "Voznesyisya", "voznesyisya"),
    (267, "kiss the Precious Cross"),
    (268, "commemoration of the feast", "AT THE HOURS"),
    (269, "Praise the Lord", "14 September"),
    (270, "Praise the Lord and of the Saint"),
    (271, "as other feasts are usually transferred"),
    (272, "Thursday, Friday or Saturday"),
    (273, "According to our liturgikons everything - only to the Saint", "According to our liturgikons everything – only to the Saint"),
    (274, "on the 1st and 6th - of the Earthquake", "on the 1st and 6th – of the Earthquake"),
    (275, "sequential of the Sunday and to the Saint"),
    (276, "transferring it from a weekday to Sunday"),
    (277, "Synaxis of St. Archangel Michael"),
    (278, "Rejoice, O Virgin Theotokos")
]

print("Verifying query lines...")
for item in queries:
    fn = item[0]
    q1 = item[1]
    q2 = item[2] if len(item) > 2 else None
    
    t_matches = [i for i, l in enumerate(txt_lines) if q1.lower() in l.lower() and (not q2 or q2.lower() in l.lower())]
    m_matches = [i for i, l in enumerate(md_lines) if q1.lower() in l.lower() and (not q2 or q2.lower() in l.lower())]
    print(f"FN {fn:3d}: TXT lines={[i+1 for i in t_matches]}, MD lines={[i+1 for i in m_matches]}")
