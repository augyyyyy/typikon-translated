import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# First, clean Part 3 TXT and MD of any incorrect/duplicate anchors from 247 to 278
txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

# Remove any existing [^247]..[^278] tags
import re
for n in range(247, 279):
    txt = txt.replace(f"[^{n}]", "")
    md = md.replace(f"[^{n}]", "")

# Verify clean
for n in range(247, 279):
    assert f"[^{n}]" not in txt
    assert f"[^{n}]" not in md

print("Cleaned existing 247-278 tags from Part 3.")

# Now define precise, unique target pairs for TXT and MD
# Format: (fid, txt_pattern, txt_replacement, md_pattern, md_replacement)
rules = [
    # 247: Saturday before Exaltation
    (247,
     "only according to Slavic typikons, the sequential Apostle-Gospel); Communion Hymn of the weekday.",
     "only according to Slavic typikons, the sequential Apostle-Gospel); Communion Hymn of the weekday[^247].",
     "only according to Slavic typikons, the sequential Apostle-Gospel); Communion Hymn of the weekday.",
     "only according to Slavic typikons, the sequential Apostle-Gospel); Communion Hymn of the weekday[^247]."),
    
    # 248: Forefeast of Nativity on Saturday before Exaltation
    (248,
     "first of the Saturday before the Exaltation, afterwards - to the Feast.",
     "first of the Saturday before the Exaltation, afterwards - to the Feast[^248].",
     "first of the Saturday before the Exaltation, afterwards – to the Feast.",
     "first of the Saturday before the Exaltation, afterwards – to the Feast[^248]."),

    # 249: Saturday in Forefeast of Exaltation
    (249,
     "Sunday before the Exaltation, Communion Hymn - to the Renovation.",
     "Sunday before the Exaltation, Communion Hymn - to the Renovation[^249].",
     "Sunday before the Exaltation, Communion Hymn – to the Renovation.",
     "Sunday before the Exaltation, Communion Hymn – to the Renovation[^249]."),

    # 250: Sunday before Exaltation alone
    (250,
     "under the Prokimenon (zaspiv)), Communion Hymn - \"Praise the Lord\".",
     "under the Prokimenon (zaspiv)), Communion Hymn - \"Praise the Lord\"[^250].",
     "under the Prokimenon (zaspiv)), Communion Hymn – *“Praise the Lord”*.",
     "under the Prokimenon (zaspiv)), Communion Hymn – *“Praise the Lord”*[^250]."),

    # 251: Sunday before Exaltation in Forefeast of Nativity
    (251,
     "of the Feast (the Resurrectional of the Sunday is discarded); Communion Hymn - \"Praise the Lord\" and of the Feast.",
     "of the Feast (the Resurrectional of the Sunday is discarded); Communion Hymn - \"Praise the Lord\" and of the Feast[^251].",
     "of the Feast (the Resurrectional of the Sunday is discarded); Communion Hymn – *“Praise the Lord”* and of the Feast.",
     "of the Feast (the Resurrectional of the Sunday is discarded); Communion Hymn – *“Praise the Lord”* and of the Feast[^251]."),

    # 252: III. In the Afterfeast of the Nativity of the Most Holy Theotokos
    (252,
     "III. In the Afterfeast of the Nativity of the Most Holy Theotokos\nEverything as above in the Forefeast, only the Communion Hymn - \"Praise the Lord\" and of the Feast.",
     "III. In the Afterfeast of the Nativity of the Most Holy Theotokos\nEverything as above in the Forefeast, only the Communion Hymn - \"Praise the Lord\" and of the Feast[^252].",
     "### 3.1.5 In the Afterfeast of the Nativity of the Most Holy Theotokos\n\nEverything as above in the Forefeast, only the Communion Hymn – *“Praise the Lord”* and of the Feast.",
     "### 3.1.5 In the Afterfeast of the Nativity of the Most Holy Theotokos\n\nEverything as above in the Forefeast, only the Communion Hymn – *“Praise the Lord”* and of the Feast[^252]."),

    # 253: Apodosis of the Nativity of the Most Holy Theotokos
    (253,
     "(According to Slavic typikons, Apostle-Gospel - under the Prokimenon (zaspiv) of the Sunday before the Exaltation).",
     "(According to Slavic typikons, Apostle-Gospel - under the Prokimenon (zaspiv) of the Sunday before the Exaltation)[^253].",
     "(According to Slavic typikons, Apostle-Gospel – under the Prokimenon (zaspiv) of the Sunday before the Exaltation).",
     "(According to Slavic typikons, Apostle-Gospel – under the Prokimenon (zaspiv) of the Sunday before the Exaltation)[^253]."),

    # 254: 12 September Memory of the Renovation
    (254,
     "12 SEPTEMBER Memory of the Renovation of the Temple of the Resurrection\nand Forefeast of the Exaltation",
     "12 SEPTEMBER Memory of the Renovation of the Temple of the Resurrection[^254]\nand Forefeast of the Exaltation",
     "### 3.1.7 September: Memory of the Renovation of the Temple of the Resurrection\n\nand Forefeast of the Exaltation",
     "### 3.1.7 September: Memory of the Renovation of the Temple of the Resurrection[^254]\n\nand Forefeast of the Exaltation"),

    # 255: 12 September Matins after 3rd ode
    (255,
     "after each ode. After the 3rd ode - Kontakion and Sessional hymn of the Renovation; Glory: Sessional hymn",
     "after each ode. After the 3rd ode - Kontakion[^255] and Sessional hymn of the Renovation; Glory: Sessional hymn",
     "After the 3rd Ode:* Kontakion and Sessional hymn of the Renovation; Glory: Sessional hymn to the Forefeast",
     "After the 3rd Ode:* Kontakion[^255] and Sessional hymn of the Renovation; Glory: Sessional hymn to the Forefeast"),

    # 256: 12 September Hours
    (256,
     "1st and 6th - of the Forefeast, on the 9th again - of the Renovation.\nAT THE LITURGY",
     "1st and 6th - of the Forefeast, on the 9th again - of the Renovation[^256].\nAT THE LITURGY",
     "1st and 6th – of the Forefeast, on the 9th again – of the Renovation.\n\n##### At the Divine Liturgy",
     "1st and 6th – of the Forefeast, on the 9th again – of the Renovation[^256].\n\n##### At the Divine Liturgy"),

    # 257: 12 September on Sunday Hours
    (257,
     "on the 1st and 6th - of the Forefeast, on the 9th - Resurrectional.\nAT THE LITURGY\nResurrectional Troparion",
     "on the 1st and 6th - of the Forefeast, on the 9th - Resurrectional[^257].\nAT THE LITURGY\nResurrectional Troparion",
     "on the 1st and 6th – of the Forefeast, on the 9th – Resurrectional.\n\n##### At the Divine Liturgy\n\nResurrectional Troparion",
     "on the 1st and 6th – of the Forefeast, on the 9th – Resurrectional[^257].\n\n##### At the Divine Liturgy\n\nResurrectional Troparion"),

    # 258: 14 September Strict fast permitted for dairy by Lviv Synod
    (258,
     "Strict fast on this day the Lviv Synod permits for dairy.\nThe service",
     "Strict fast on this day the Lviv Synod permits for dairy[^258].\nThe service",
     "Strict fast on this day the Lviv Synod permits for dairy.\n\nThe service",
     "Strict fast on this day the Lviv Synod permits for dairy[^258].\n\nThe service"),

    # 259: 14 September Preparation of Cross
    (259,
     "above the top of the Cross, between the basil and the Cross.\nBRINGING OUT",
     "above the top of the Cross, between the basil and the Cross[^259].\nBRINGING OUT",
     "above the top of the Cross, between the basil and the Cross.\n\n#### Bringing Out",
     "above the top of the Cross, between the basil and the Cross[^259].\n\n#### Bringing Out"),

    # 260: 14 September priest wearing epitrachelion
    (260,
     "the Priest, wearing an epitrachelion, the Deacon, if there be one",
     "the Priest, wearing an epitrachelion[^260], the Deacon, if there be one",
     "the Priest, wearing an epitrachelion, the Deacon, if there be one",
     "the Priest, wearing an epitrachelion[^260], the Deacon, if there be one"),

    # 261: 14 September in the place of the holy Gospel
    (261,
     "in the place of the holy Gospel, and places the Gospel on the High Place",
     "in the place of the holy Gospel[^261], and places the Gospel on the High Place",
     "in the place of the holy Gospel, and places the Gospel on the High Place",
     "in the place of the holy Gospel[^261], and places the Gospel on the High Place"),

    # 262: 14 September lit before it for the whole night
    (262,
     "lit before it for the whole night\". At the end",
     "lit before it for the whole night\"[^262]. At the end",
     "lit before it for the whole night”. At the end",
     "lit before it for the whole night”[^262]. At the end"),

    # 263: 14 September behind the Deacon to the sacristy
    (263,
     "behind the candle-bearers and behind the Deacon to the sacristy.\nTRANSFER",
     "behind the candle-bearers and behind the Deacon to the sacristy[^263].\nTRANSFER",
     "behind the candle-bearers and behind the Deacon to the sacristy.\n\n#### Transfer",
     "behind the candle-bearers and behind the Deacon to the sacristy[^263].\n\n#### Transfer"),

    # 264: 14 September Troparion "Save, O Lord"
    (264,
     "and the choirs sing the Troparion \"Save, O Lord\".\nEXALTATION",
     "and the choirs sing the Troparion \"Save, O Lord\"[^264].\nEXALTATION",
     "and the choirs sing the Troparion *“Save, O Lord”*.\n\n#### Exaltation",
     "and the choirs sing the Troparion *“Save, O Lord”*[^264].\n\n#### Exaltation"),

    # 265: 14 September sings solemnly and joyfully
    (265,
     "facing east, sings solemnly and joyfully the first petition",
     "facing east, sings[^265] solemnly and joyfully the first petition",
     "facing east, sings solemnly and joyfully the first petition",
     "facing east, sings[^265] solemnly and joyfully the first petition"),

    # 266: 14 September Voznesyisya
    (266,
     "\"Thou Who Wast lifted up\" (\"Voznesyisya\").\nAt the third time",
     "\"Thou Who Wast lifted up\" (\"Voznesyisya\")[^266].\nAt the third time",
     "*“Thou Who Wast lifted up”* (*“voznesyisya”*).\n\nAt the third time",
     "*“Thou Who Wast lifted up”* (*“voznesyisya”*)[^266].\n\nAt the third time"),

    # 267: 14 September kiss the Precious Cross
    (267,
     "also bow and kiss the Precious Cross. After this all together",
     "also bow and kiss the Precious Cross[^267]. After this all together",
     "also bow and kiss the Precious Cross. After this all together",
     "also bow and kiss the Precious Cross[^267]. After this all together"),

    # 268: 14 September dismissal with commemoration of the feast
    (268,
     "with commemoration of the feast.\nAT THE HOURS",
     "with commemoration of the feast[^268].\nAT THE HOURS",
     "with commemoration of the feast.\n\n##### At the Hours",
     "with commemoration of the feast[^268].\n\n##### At the Hours"),

    # 269: 14 September on Sunday Communion Hymn
    (269,
     "Communion Hymn \"Praise the Lord\" and of the Feast.\nNote: If a Saint with Polyeleos falls",
     "Communion Hymn \"Praise the Lord\" and of the Feast[^269].\nNote: If a Saint with Polyeleos falls",
     "Communion Hymn *“Praise the Lord”* and of the Feast.\n\n> **Note:** If a Saint with Polyeleos falls",
     "Communion Hymn *“Praise the Lord”* and of the Feast[^269].\n\n> **Note:** If a Saint with Polyeleos falls"),

    # 270: 14 September with Polyeleos saint Communion Hymn
    (270,
     "Communion Hymn \"Praise the Lord\" and of the Saint.\n________________________________________",
     "Communion Hymn \"Praise the Lord\" and of the Saint[^270].\n________________________________________",
     "Communion Hymn *“Praise the Lord”* and of the Saint.\n\n---",
     "Communion Hymn *“Praise the Lord”* and of the Saint[^270].\n\n---"),

    # 271: 27 September John the Theologian transfer
    (271,
     "as other feasts are usually transferred, but to the previous one.\n________________________________________",
     "as other feasts are usually transferred, but to the previous one[^271].\n________________________________________",
     "as other feasts are usually transferred, but to the previous one.\n\n---",
     "as other feasts are usually transferred, but to the previous one[^271].\n\n---"),

    # 272: 11 October Fathers (we need to reinsert the missing paragraph in MD!)
    # First handle TXT:
    (272,
     "if it falls on Thursday, Friday or Saturday. The Service of the Saint",
     "if it falls on Thursday, Friday or Saturday[^272]. The Service of the Saint",
     # In MD, we will insert the missing item 1 under Notes!
     None, None),

    # 273: 26 October Demetrius Liturgy
    (273,
     "AT THE LITURGY: According to our liturgikons everything - only to the Saint.\n________________________________________",
     "AT THE LITURGY: According to our liturgikons everything - only to the Saint[^273].\n________________________________________",
     "##### At the Divine Liturgy\n\nAccording to our liturgikons everything – only to the Saint.\n\n---",
     "##### At the Divine Liturgy\n\nAccording to our liturgikons everything – only to the Saint[^273].\n\n---"),

    # 274: 26 October Demetrius on Sunday Hours
    (274,
     "on the 1st and 6th - of the Earthquake, on the 3rd and 9th - to the Saint;\nAT THE LITURGY",
     "on the 1st and 6th - of the Earthquake, on the 3rd and 9th - to the Saint[^274];\nAT THE LITURGY",
     "on the 1st and 6th – of the Earthquake, on the 3rd and 9th – to the Saint;\n\n##### At the Divine Liturgy",
     "on the 1st and 6th – of the Earthquake, on the 3rd and 9th – to the Saint[^274];\n\n##### At the Divine Liturgy"),

    # 275: 26 October Demetrius on Sunday Liturgy
    (275,
     "everything - only sequential of the Sunday and to the Saint.\n________________________________________",
     "everything - only sequential of the Sunday and to the Saint[^275].\n________________________________________",
     "everything – only sequential of the Sunday and to the Saint.\n\n---",
     "everything – only sequential of the Sunday and to the Saint[^275].\n\n---"),

    # 276: 31 October Josaphat
    (276,
     "transferring it from a weekday to Sunday.\n________________________________________",
     "transferring it from a weekday to Sunday[^276].\n________________________________________",
     "transferring it from a weekday to Sunday.\n\n---",
     "transferring it from a weekday to Sunday[^276].\n\n---"),

    # 277: 8 November Archangel Michael
    (277,
     "8 NOVEMBER Synaxis of St. Archangel Michael\nand other Bodiless Powers\nWe serve All-Night Vigil and sing \"Blessed is the man\"; everything - according to the general rule of a Saint with All-Night Vigil.\n________________________________________",
     "8 NOVEMBER Synaxis of St. Archangel Michael\nand other Bodiless Powers\nWe serve All-Night Vigil and sing \"Blessed is the man\"; everything - according to the general rule of a Saint with All-Night Vigil[^277].\n________________________________________",
     "### 3.2.4 November: Synaxis of St. Archangel Michael\n\nand other Bodiless Powers\n\nWe serve All-Night Vigil and sing *“Blessed is the man”*; everything – according to the general rule of a Saint with All-Night Vigil.\n\n---",
     "### 3.2.4 November: Synaxis of St. Archangel Michael\n\nand other Bodiless Powers\n\nWe serve All-Night Vigil and sing *“Blessed is the man”*; everything – according to the general rule of a Saint with All-Night Vigil[^277].\n\n---"),

    # 278: 15 November Philip Fast
    (278,
     "5 \"Our Father\" and 5 \"Rejoice, O Virgin Theotokos\"  for the faithful",
     "5 \"Our Father\" and 5 \"Rejoice, O Virgin Theotokos\"[^278]  for the faithful",
     "5 *“Our Father”* and 5 *“Rejoice, O Virgin Theotokos”* for the faithful",
     "5 *“Our Father”* and 5 *“Rejoice, O Virgin Theotokos”*[^278] for the faithful")
]

print(f"Total rules to test: {len(rules)}")
for fid, t_pat, t_rep, m_pat, m_rep in rules:
    t_cnt = txt.count(t_pat) if t_pat else 0
    m_cnt = md.count(m_pat) if m_pat else 0
    print(f"FN {fid:3d}: txt_matches={t_cnt}, md_matches={m_cnt}")
