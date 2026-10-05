import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')

txt = txt_path.read_text(encoding='utf-8')
md = md_path.read_text(encoding='utf-8')

replacements = [
    # FN 247: Saturday before Exaltation
    ("Communion Hymn of the weekday.", "Communion Hymn of the weekday[^247]."),
    ("Communion Hymn of the weekday", "Communion Hymn of the weekday[^247]"),

    # FN 248: Forefeast of Nativity of Theotokos
    ("afterwards - of the Feast.", "afterwards - of the Feast[^248]."),
    ("afterwards – of the Feast.", "afterwards – of the Feast[^248]."),

    # FN 249: Saturday in Forefeast of Exaltation
    ("Communion Hymn - of the Renovation.", "Communion Hymn - of the Renovation[^249]."),
    ("Communion Hymn – of the Renovation.", "Communion Hymn – of the Renovation[^249]."),

    # FN 250: Sunday before Exaltation alone
    ("Communion Hymn - \"Praise the Lord\".", "Communion Hymn - \"Praise the Lord\"[^250]."),
    ("Communion Hymn – *“Praise the Lord”*.", "Communion Hymn – *“Praise the Lord”*[^250]."),

    # FN 251: Sunday before Exaltation in Forefeast of Nativity
    ("Communion Hymn - \"Praise the Lord\" and of the Feast.", "Communion Hymn - \"Praise the Lord\" and of the Feast[^251]."),
    ("Communion Hymn – *“Praise the Lord”* and of the Feast.", "Communion Hymn – *“Praise the Lord”* and of the Feast[^251]."),

    # FN 252: Afterfeast of Nativity
    ("only Communion Hymn - \"Praise the Lord\" and of the Feast.", "only Communion Hymn - \"Praise the Lord\" and of the Feast[^252]."),
    ("only Communion Hymn – *“Praise the Lord”* and of the Feast.", "only Communion Hymn – *“Praise the Lord”* and of the Feast[^252]."),

    # FN 253: Apodosis of Nativity
    ("(According to Slavic typikons, Apostle-Gospel - under the Prokimenon (zaspiv) of the Sunday before the Exaltation).", "(According to Slavic typikons, Apostle-Gospel - under the Prokimenon (zaspiv) of the Sunday before the Exaltation)[^253]."),
    ("(According to Slavic typikons, Apostle-Gospel – under the Prokimenon (zaspiv) of the Sunday before the Exaltation).", "(According to Slavic typikons, Apostle-Gospel – under the Prokimenon (zaspiv) of the Sunday before the Exaltation)[^253]."),

    # FN 254: 12 September heading
    ("12 SEPTEMBER Memory of the Renovation of the Temple of the Resurrection", "12 SEPTEMBER Memory of the Renovation of the Temple of the Resurrection[^254]"),
    ("### 12 September — Memory of the Renovation of the Temple of the Resurrection", "### 12 September — Memory of the Renovation of the Temple of the Resurrection[^254]"),

    # FN 255: 12 September Matins
    ("After the 3rd ode - Kontakion  and Sessional hymn of the Renovation;", "After the 3rd ode - Kontakion[^255] and Sessional hymn of the Renovation;"),
    ("After the 3rd ode – Kontakion and Sessional hymn of the Renovation;", "After the 3rd ode – Kontakion[^255] and Sessional hymn of the Renovation;"),

    # FN 256: 12 September Hours
    ("on the 9th again - of the Renovation.", "on the 9th again - of the Renovation[^256]."),
    ("on the 9th again – of the Renovation.", "on the 9th again – of the Renovation[^256]."),

    # FN 259: 14 September Preparation of Cross
    ("between the basil and the Cross.", "between the basil and the Cross[^259]."),

    # FN 260, 261, 262, 263: 14 September Bringing Out
    ("the Priest, wearing an epitrachelion,", "the Priest, wearing an epitrachelion[^260],"),
    ("lays the precious Cross on the holy mensa, in the place of the holy Gospel,", "lays the precious Cross on the holy mensa, in the place of the holy Gospel[^261],"),
    ("candle is lit before it for the whole night\".", "candle is lit before it for the whole night\"[^262]."),
    ("candle is lit before it for the whole night”.", "candle is lit before it for the whole night”[^262]."),
    ("behind the candle-bearers and behind the Deacon to the sacristy.", "behind the candle-bearers and behind the Deacon to the sacristy[^263]."),

    # FN 264: 14 September Transfer
    ("and the choirs sing the Troparion \"Save, O Lord\".", "and the choirs sing the Troparion \"Save, O Lord\"[^264]."),
    ("and the choirs sing the Troparion *“Save, O Lord”*.", "and the choirs sing the Troparion *“Save, O Lord”*[^264]."),

    # FN 265, 266: 14 September Exaltation
    ("facing east, sings  solemnly and joyfully", "facing east, sings[^265] solemnly and joyfully"),
    ("facing east, sings solemnly and joyfully", "facing east, sings[^265] solemnly and joyfully"),
    ("Troparion \"Thou Who Wast lifted up\" (\"Voznesyisya\").", "Troparion \"Thou Who Wast lifted up\" (\"Voznesyisya\")[^266]."),
    ("Troparion *“Thou Who Wast lifted up”* (*“Voznesyisya”*).", "Troparion *“Thou Who Wast lifted up”* (*“Voznesyisya”*)[^266]."),
    ("Troparion \"Thou Who Wast lifted up\" (\"voznesyisya\").", "Troparion \"Thou Who Wast lifted up\" (\"voznesyisya\")[^266]."),
    ("Troparion *“Thou Who Wast lifted up”* (*“voznesyisya”*).", "Troparion *“Thou Who Wast lifted up”* (*“voznesyisya”*)[^266]."),
    ("Glory, Both now is sung: \"Thou Who Wast lifted up\" (\"Voznesyisya\").", "Glory, Both now is sung: \"Thou Who Wast lifted up\" (\"Voznesyisya\")[^266]."),
    ("Glory, Both now is sung: *“Thou Who Wast lifted up”* (*“Voznesyisya”*).", "Glory, Both now is sung: *“Thou Who Wast lifted up”* (*“Voznesyisya”*)[^266]."),

    # FN 267, 268: 14 September Veneration
    ("until other sacred ministers also bow and kiss the Precious Cross.", "until other sacred ministers also bow and kiss the Precious Cross[^267]."),
    ("with commemoration of the feast.", "with commemoration of the feast[^268]."),

    # FN 271: 1 October Protection
    ("as you have here on p. 129.", "as you have here on p. 129[^271]."),
    ("as you have here on p. 129", "as you have here on p. 129[^271]"),
    ("transfer to the previous Sunday, as you have here on p. 129.", "transfer to the previous Sunday, as you have here on p. 129[^271]."),

    # FN 272: 11 October Fathers
    ("if it falls on Thursday, Friday or Saturday.", "if it falls on Thursday, Friday or Saturday[^272]."),

    # FN 273: 26 October Demetrius Liturgy
    ("According to our liturgikons everything - only to the Saint.", "According to our liturgikons everything - only to the Saint[^273]."),
    ("According to our liturgikons everything – only to the Saint.", "According to our liturgikons everything – only to the Saint[^273]."),

    # Clean spurious [^362] and [^445] on October 26 Small Vespers:
    ("Saint with All-Night Vigil[^362] on Sunday[^445],", "Saint with All-Night Vigil on Sunday,"),
    ("Saint with All-Night Vigil[^362] on Sunday[^445]", "Saint with All-Night Vigil on Sunday"),

    # FN 274: 26 October Hours
    ("on the 1st and 6th - of the Earthquake, on the 3rd and 9th - to the Saint;", "on the 1st and 6th - of the Earthquake, on the 3rd and 9th - to the Saint[^274];"),
    ("on the 1st and 6th – of the Earthquake, on the 3rd and 9th – to the Saint;", "on the 1st and 6th – of the Earthquake, on the 3rd and 9th – to the Saint[^274];"),

    # FN 275: 26 October Liturgy Sunday
    ("only sequential of Sunday and to the Saint.", "only sequential of Sunday and to the Saint[^275]."),
    ("only sequential of Sunday and to the Saint", "only sequential of Sunday and to the Saint[^275]"),

    # FN 276: 28 October Paraskeva
    ("transferring it from a weekday to Sunday.", "transferring it from a weekday to Sunday[^276]."),
    ("transferring it from a weekday to Sunday", "transferring it from a weekday to Sunday[^276]"),

    # FN 277: 8 November Michael
    ("according to the general rule of a Saint with All-Night Vigil.", "according to the general rule of a Saint with All-Night Vigil[^277]."),
    ("according to the general rule of a Saint with All-Night Vigil", "according to the general rule of a Saint with All-Night Vigil[^277]"),

    # FN 278: 15 November Philip Fast
    ("5 \"Our Father\" and 5 \"Rejoice, O Virgin Theotokos\"  for the faithful,", "5 \"Our Father\" and 5 \"Rejoice, O Virgin Theotokos\"[^278]  for the faithful,"),
    ("5 *“Our Father”* and 5 *“Rejoice, O Virgin Theotokos”* for the faithful,", "5 *“Our Father”* and 5 *“Rejoice, O Virgin Theotokos”*[^278] for the faithful,"),
    ("5 *“Our Father”* and 5 *“Rejoice, O Virgin Theotokos”*  for the faithful,", "5 *“Our Father”* and 5 *“Rejoice, O Virgin Theotokos”*[^278]  for the faithful,")
]

print("Applying replacements...")
txt_count = 0
md_count = 0
for src, dst in replacements:
    if src in txt:
        txt = txt.replace(src, dst)
        txt_count += 1
    if src in md:
        md = md.replace(src, dst)
        md_count += 1

txt_path.write_text(txt, encoding='utf-8')
md_path.write_text(md, encoding='utf-8')
print(f"Applied {txt_count} replacements to TXT and {md_count} replacements to MD!")
