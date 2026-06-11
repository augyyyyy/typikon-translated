import os
import re

FINAL_DIR = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\Final"

def get_path(filename):
    return os.path.join(FINAL_DIR, filename)

def modify_part2():
    path = get_path("Final_Dolnytsky_part2_general_rubrics.txt")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Truncate footnotes starting at line 553's separator
    # The split is at the marker: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- [^46]:
    parts = content.split(" -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- [^46]:")
    if len(parts) > 1:
        # Keep everything before the separator and add a newline
        new_content = parts[0].rstrip() + "\n"
    else:
        print("Warning: Could not find the separator for footnote truncation in Part 2.")
        new_content = content
        
    # 2. Apply corrections to the remaining text
    # Line 55: two of the current tone -> two appointed
    new_content = new_content.replace(
        "two of the current tone, after each of which",
        "two appointed, after each of which"
    )
    
    # Line 59: "Having Beheld the Resurrection of Christ" -> "Jesus is risen"
    new_content = new_content.replace(
        '"Having Beheld the Resurrection of Christ"',
        '"Jesus is risen"'
    )
    
    # Line 60: Songs of the saint -> Kontakion and Ikos of the saint
    new_content = new_content.replace(
        "Songs of the saint, if there be (for the Menaion does not always give a Kontakion-Ikos)",
        "Kontakion and Ikos of the saint, if there be (for the Menaion does not always give a Kontakion-Ikos)"
    )
    
    # Line 60: Heirmologic -> Idiomela
    new_content = new_content.replace(
        "refrain of the Heirmologic hymns",
        "refrain of the Idiomela hymns"
    )
    
    # Lines 68, 69: patron -> temple
    new_content = new_content.replace("to the patron[^64] of the church", "to the temple[^64] of the church")
    new_content = new_content.replace("to the patron.", "to the temple.")
    new_content = new_content.replace("to the patron, at the 9th", "to the temple, at the 9th")
    new_content = new_content.replace("to the patron, at the 9th - to the second saint[^65].", "to the temple, at the 9th - to the second saint[^65].")
    
    # Line 107: He has -> he has
    new_content = new_content.replace("Sometimes He has not only", "Sometimes he has not only")
    
    # Line 148, 150: patron saint -> temple saint
    new_content = new_content.replace("patron saint on 4", "temple saint on 4")
    
    # Line 149: if He has -> if he has
    new_content = new_content.replace("if He has one;", "if he has one;")
    # Line 149: His Theotokion -> his theotokion
    new_content = new_content.replace("Both now: His Theotokion.", "Both now: his theotokion.")
    new_content = new_content.replace("Both now: His Theotokion. After the 6th Ode", "Both now: his theotokion. After the 6th Ode")
    
    # Line 207: Tone 8 -> Tone 2
    new_content = new_content.replace(
        '("Having traversed the moisture", Tone 8 of Sunday Matins',
        '("Having traversed the moisture", Tone 2 of Sunday Matins'
    )
    
    # Line 251: Patronal Feast -> Feast of the temple
    new_content = new_content.replace("the Patronal Feast[^156].", "the Feast of the temple[^156].")
    
    # Line 268: if He has -> if he has, refrains of His -> refrains of his
    new_content = new_content.replace("if He has, with two separate refrains of His;", "if he has, with two separate refrains of his;")
    
    # Line 272: we refuse alternatingly -> we say alternatingly
    new_content = new_content.replace("we refuse alternatingly, that is at the 1st", "we say alternatingly, that is at the 1st")
    
    # Line 284: if He has -> if he has
    new_content = new_content.replace("if He has, Both now:", "if he has, Both now:")
    
    # Line 371: saint/saint -> feast/saint
    new_content = new_content.replace(
        "taken in the first place - to the saint, afterwards - to the saint. But because",
        "taken in the first place - to the feast, afterwards - to the saint. But because"
    )
    
    # Line 394: we refuse alternatingly -> we say alternatingly
    new_content = new_content.replace("we refuse alternatingly, that is: at the 1st", "we say alternatingly, that is: at the 1st")
    
    # Line 401: if He has -> if he has
    new_content = new_content.replace("if He has, Both now: of the feast.", "if he has, Both now: of the feast.")
    
    # Globally replace "Dismissal great" -> "the Great Dismissal"
    new_content = new_content.replace("Dismissal great", "the Great Dismissal")
    new_content = new_content.replace("Dismissal great,", "the Great Dismissal,")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Part 2 updated successfully.")

def modify_part4():
    path = get_path("Final_Dolnytsky_part4_triodion.txt")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Truncate footnotes starting at line 1098's separator
    parts = content.split(" -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- [^466]:")
    if len(parts) > 1:
        new_content = parts[0].rstrip() + "\n"
    else:
        print("Warning: Could not find the separator for footnote truncation in Part 4.")
        new_content = content
        
    # 2. Apply corrections
    # Line 430: "Today is salvation" -> "Save, O Lord"
    new_content = new_content.replace(
        'troparion "Today is salvation", for then',
        'troparion "Save, O Lord", for then'
    )
    
    # Line 517: Remove [^650][^649][^640]
    new_content = new_content.replace("Resurrection[^650][^649][^640] very early", "Resurrection very early")
    
    # Line 519: Remove [^576]
    new_content = new_content.replace("Great Thursday [^576]and Saturday", "Great Thursday and Saturday")
    
    # Line 539: Remove [^646][^606][^579]
    new_content = new_content.replace('"More honorable"[^646][^606][^579]; after', '"More honorable"; after')
    
    # Line 699: Insert [^606] after "More honorable"
    new_content = new_content.replace(
        'we do not sing "More honorable" and after the 9th',
        'we do not sing "More honorable"[^606] and after the 9th'
    )
    
    # Insert bilingual paragraph from page 183
    # Find: ...and the people kiss the Shroud[^602].
    # Replace with: ...and the people kiss the Shroud[^602].\n\n[Bilingual Note]\n\nNotes
    target_block = 'and the people kiss the Shroud[^602].\nNotes'
    bilingual_note = (
        'and the people kiss the Shroud[^602].\n\n'
        'The icon of the Shroud is transferred on Holy and Great Friday from the sanctuary at the '
        'end of Vespers, while the Dismissal Troparia "The noble Joseph", etc. are sung, and is placed '
        'on a prepared table in the middle of the presbytery, where there are already and remain lit '
        'candles with vessels of flowers throughout the whole day until the hour of Matins of Great '
        'Saturday (which is celebrated on the evening of Great Friday).\n\nNotes'
    )
    if target_block in new_content:
        new_content = new_content.replace(target_block, bilingual_note)
    else:
        # Try with Windows line endings just in case
        target_block_win = 'and the people kiss the Shroud[^602].\r\nNotes'
        bilingual_note_win = (
            'and the people kiss the Shroud[^602].\r\n\r\n'
            'The icon of the Shroud is transferred on Holy and Great Friday from the sanctuary at the '
            'end of Vespers, while the Dismissal Troparia "The noble Joseph", etc. are sung, and is placed '
            'on a prepared table in the middle of the presbytery, where there are already and remain lit '
            'candles with vessels of flowers throughout the whole day until the hour of Matins of Great '
            'Saturday (which is celebrated on the evening of Great Friday).\r\n\r\nNotes'
        )
        if target_block_win in new_content:
            new_content = new_content.replace(target_block_win, bilingual_note_win)
        else:
            print("Warning: Could not find exact location to insert bilingual paragraph in Part 4.")
            
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Part 4 updated successfully.")

def modify_part5():
    path = get_path("Final_Dolnytsky_part5_temple.txt")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Truncate footnotes starting at line 1127's separator
    parts = content.split(" -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- [^663]:")
    if len(parts) > 1:
        new_content = parts[0].rstrip() + "\n"
    else:
        print("Warning: Could not find the separator for footnote truncation in Part 5.")
        new_content = content
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Part 5 updated successfully.")

def modify_appendix():
    path = get_path("Final_Dolnytsky_appendix.txt")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Truncate footnotes starting at line 597: \nFootnotes:\n
    parts = re.split(r'\nFootnotes:?\s*\n', content, flags=re.IGNORECASE)
    if len(parts) > 1:
        new_content = parts[0].rstrip() + "\n"
    else:
        # Check with CRLF
        parts_crlf = re.split(r'\r\nFootnotes:?\s*\r\n', content, flags=re.IGNORECASE)
        if len(parts_crlf) > 1:
            new_content = parts_crlf[0].rstrip() + "\n"
        else:
            print("Warning: Could not find Footnotes header in Appendix.")
            new_content = content
            
    # 2. Renumber paragraphs
    # First renumber 229-236 -> 224-231
    # We will do this carefully using regex search-and-replace to avoid double replacements.
    # Note: paragraphs to change:
    # 229 -> 224, 230 -> 225, 231 -> 226, 232 -> 227, 233 -> 228, 234 -> 229, 235 -> 230, 236 -> 231
    # 237 -> 232, 238 -> 233, 239 -> 234, 240 -> 235
    # 241 -> 236 (Wait, line 551 has 241. It should be 236!)
    # 242 -> 237? Wait, let's look at page 284: original is 232-239.
    # Original numbers on Page 284: 232, 233, 234, 235, 236, 237, 238, 239.
    # Wait, our text currently has:
    # 237 -> 232
    # 238 -> 233
    # 239 -> 234
    # 240 -> 235
    # Then unnumbered paragraphs representing parts of 236 in original.
    # Then 241 -> 236.
    # Then 242 -> 237.
    # Then 243 -> 238.
    # Then 244 -> 239.
    # And then Page 285 original runs from 240 to 247.
    # Current text has 245-252.
    # So:
    # 245 -> 240
    # 246 -> 241
    # 247 -> 242
    # 248 -> 243
    # 249 -> 244
    # 250 -> 245
    # 251 -> 246
    # 252 -> 247
    # Page 286: original runs from 248 to 254.
    # Current text has:
    # 253 -> 248
    # 254 -> 249
    # 255 -> 250
    # 256 -> merge into 250 (so remove "256. " prefix and join to previous)
    # 257 -> 251
    # 258 -> 252
    # 259 -> 253
    # 260 -> 254
    # 261 -> 255 (Wait, in draft: 261. After the holy diskos... becomes 255)
    # 262 -> 256
    # 263 -> 257
    # 264 -> 258
    # 265 -> 259
    # 266 -> 260
    # 267 -> 261 (Wait, is there a 267? In draft, there was no 267, wait, let's check: 266 was the last one in the concelebration of priests. So 266 becomes 261. Wait! Let's check: what is 267? Ah, in draft there is no 267. So 266 is the last one.)
    
    # Let's perform these string replacements sequentially, using unique targets or temporary placeholders to avoid conflicts:
    # Replace in reverse order so that we don't overwrite newly written numbers!
    
    # Let's double check if "266." exists. Yes, line 592 starts with "266."
    new_content = new_content.replace("\n266. ", "\n261. ")
    new_content = new_content.replace("\n265. ", "\n260. ")
    new_content = new_content.replace("\n264. ", "\n259. ")
    new_content = new_content.replace("\n263. ", "\n258. ")
    new_content = new_content.replace("\n262. ", "\n257. ")
    
    # 261 -> 255
    new_content = new_content.replace("\n261. ", "\n255. ")
    # 260 -> 254
    new_content = new_content.replace("\n260. ", "\n254. ")
    # 259 -> 253
    new_content = new_content.replace("\n259. ", "\n253. ")
    # 258 -> 252
    new_content = new_content.replace("\n258. ", "\n252. ")
    # 257 -> 251
    new_content = new_content.replace("\n257. ", "\n251. ")
    
    # Merge 255 and 256 into 250:
    # 255 starts: 255. The censing on...
    # 256 starts: 256. After the second...
    # Let's find the exact text of 255 and 256 and merge them.
    # First, let's change "255. " to "250. "
    new_content = new_content.replace("\n255. ", "\n250. ")
    # Now, replace "\n256. " with a space or join it:
    new_content = new_content.replace("\n256. ", " ")
    
    # 254 -> 249
    new_content = new_content.replace("\n254. ", "\n249. ")
    # 253 -> 248
    new_content = new_content.replace("\n253. ", "\n248. ")
    
    # 252 -> 247
    new_content = new_content.replace("\n252. ", "\n247. ")
    # 251 -> 246
    new_content = new_content.replace("\n251. ", "\n246. ")
    # 250 -> 245
    new_content = new_content.replace("\n250. ", "\n245. ")
    # 249 -> 244
    new_content = new_content.replace("\n249. ", "\n244. ")
    # 248 -> 243
    new_content = new_content.replace("\n248. ", "\n243. ")
    # 247 -> 242
    new_content = new_content.replace("\n247. ", "\n242. ")
    # 246 -> 241
    new_content = new_content.replace("\n246. ", "\n241. ")
    # 245 -> 240
    new_content = new_content.replace("\n245. ", "\n240. ")
    
    # 244 -> 239
    new_content = new_content.replace("\n244. ", "\n239. ")
    # 243 -> 238
    new_content = new_content.replace("\n243. ", "\n238. ")
    # 242 -> 237
    new_content = new_content.replace("\n242. ", "\n237. ")
    # 241 -> 236
    new_content = new_content.replace("\n241. ", "\n236. ")
    
    # 240 -> 235
    new_content = new_content.replace("\n240. ", "\n235. ")
    # 239 -> 234
    new_content = new_content.replace("\n239. ", "\n234. ")
    # 238 -> 233
    new_content = new_content.replace("\n238. ", "\n233. ")
    # 237 -> 232
    new_content = new_content.replace("\n237. ", "\n232. ")
    
    # 236 -> 231
    new_content = new_content.replace("\n236. ", "\n231. ")
    # 235 -> 230
    new_content = new_content.replace("\n235. ", "\n230. ")
    # 234 -> 229
    new_content = new_content.replace("\n234. ", "\n229. ")
    # 233 -> 228
    new_content = new_content.replace("\n233. ", "\n228. ")
    # 232 -> 227
    new_content = new_content.replace("\n232. ", "\n227. ")
    # 231 -> 226
    new_content = new_content.replace("\n231. ", "\n226. ")
    # 230 -> 225
    new_content = new_content.replace("\n230. ", "\n225. ")
    # 229 -> 224
    new_content = new_content.replace("\n229. ", "\n224. ")
    
    # Capitalize "Apostle" in paragraph 237 (now 242? wait, in draft it was 242, which is now 237):
    # Draft 242 is: "242. If on these days... the Prokimenon of the Apostle... the Apostle and Gospel are read..."
    # Let's replace "Prokimenon of the Apostle" with "Prokimenon of the Apostle" (already capitalized),
    # but "apostle and gospel" with "Apostle and Gospel".
    new_content = new_content.replace(
        "the Apostle the Apostle and Gospel are read",
        "the Apostle the Apostle and Gospel are read"
    ) # Let's do a more generic replace
    new_content = new_content.replace("Prokimenon of the Apostle, after which the Apostle and Gospel are read", "Prokimenon of the Apostle, after which the Apostle and Gospel are read") # wait, let's see. In line 552: "Prokimenon of the Apostle, after which the Apostle and Gospel are read". Ah, "Apostle" is already capitalized in line 552. Let's make sure.
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Appendix updated successfully.")

def modify_footnotes():
    path = get_path("Final_footnotes.txt")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Footnote 50: at Vespers 4 troparia are not refused -> at Vespers 4 troparia are not said
    content = content.replace("at Vespers 4 troparia are not refused", "at Vespers 4 troparia are not said")
    
    # Footnote 77: refuses them only -> says them only, refused also -> said also
    content = content.replace("the Priest refuses them only at the Vigil", "the Priest says them only at the Vigil")
    content = content.replace("these litanies should be refused also at Small Matins", "these litanies should be said also at Small Matins")
    
    # Footnote 226: does not refuse him -> does not omit him
    content = content.replace("does not refuse him.", "does not omit him.")
    
    # Footnote 531: In the Greek Euchologion... -> append Greek
    content = content.replace(
        '[^531]: In the Greek Euchologion it is prescribed for the Singer to sing "Let my prayer be set forth", in the Triodion - for the Domesticus, in Slavonic rubrics - for the Reader, in other Greek ones of Morellius and Barberini - for the Priest, which corresponds also to the new Constantinopolitan Typikon...',
        '[^531]: In the Greek Euchologion it is prescribed for the Singer to sing "Let my prayer be set forth", in the Triodion - for the Domesticus, in Slavonic rubrics - for the Reader, in other Greek ones of Morellius and Barberini - for the Priest, which corresponds also to the new Constantinopolitan Typikon... (Greek: То Каτευνθύντω ψαλ. εκ του Βήματος άπαξ, meaning "Let my prayer be set forth" is sung once from the sanctuary, twice by the choirs, and again once from the sanctuary)'
    )
    
    # Footnote 533: In Greek copies... -> append Greek
    content = content.replace(
        '[^533]: In Greek copies censing is not mentioned, only in the oldest Barberini...',
        '[^533]: In Greek copies censing is not mentioned, only in the oldest Barberini... (Greek: Кад й ψάλλων: Каτευνθύνθτω η προσευχ μou, meaning "the priest stands, censing again and singing \'Let my prayer be set forth\'")'
    )
    
    # Footnote 537: replace with Nilles direct quote
    old_fn537 = '[^537]: For some reason on every Saturday the memory of St. Great Martyr Theodore is honored... (Nilles in Eortologion). In Constantinople there was a great cult of one holy martyr... for the sake of the miracle of peace and for the sake of this miracle a more special feast was established, on which the annual memory is celebrated, on the first Saturday of the forty-day fast. Julian the Apostate... 362. St. Theodore the Tyro appeared at night to the Bishop of the imperial city... (Nilles Calend. Part 2, p. 106).'
    new_fn537 = '[^537]: For some reason on this Saturday the memory of St. Great Martyr Theodore is honored, as Nilles expresses in the Eortologion (calendar of feasts), and he writes: Constantinopoli perelebris fuit eiusdem S.Martyris coltus ob'
    content = content.replace(old_fn537, new_fn537)
    
    # Footnote 542: restrict to 785 council
    old_fn542 = '[^542]: Orthodoxy means correct belief, that is the correct faith regarding the veneration of holy icons, which the Iconoclasts destroyed. The Seventh Ecumenical Council (Second of Nicaea) in 787 restored their veneration. Another council, convened in Constantinople in 842, under St. Methodius, with the support of the holy Empress Theodora, ordered the commemoration of this restoration every year on the first Sunday of Great Lent.'
    new_fn542 = '[^542]: Orthodoxy (Orthodoxia /orthodoxy/) means correct belief, that is, the correct faith regarding the veneration of holy icons, which the Iconoclasts destroyed. The Seventh Ecumenical Council (Second of Nicaea) in 785 restored their veneration.'
    content = content.replace(old_fn542, new_fn542)
    
    # Footnote 544: Каноновєς -> Κανονες
    content = content.replace('Каноновєς оі αναστάσιμοι', 'Κανονες οι αναστάσιμοι')
    
    # Footnote 551: After the 50th Psalm -> After the 8th Psalm
    content = content.replace(
        '[^551]: After the 50th Psalm immediately, is written in the Greek and Pochaiv Triodia; so also in Tserkovne Oko: "then the 50th Psalm and canon". Not good in the Peremyshl Typikon is prescribed "Save, O God".',
        '[^551]: After the 8th Psalm immediately, is written in the Greek and Pochaiv Triodia; so also in Tserkovne Oko: "then the 50th Psalm and canon". Not good in the Peremyshl Typikon is prescribed "Save, O God".'
    )
    
    # Footnote 559: add exposition text
    content = content.replace(
        '[^559]: Title IV, Chapter IV, part VIII.',
        '[^559]: And with the exposition of the Holy Mysteries (Title IV, Chapter IV, part VIII).'
    )
    
    # Footnote 741: restore missing text
    old_fn741 = '[^741]: Everything -- according to the rubric of the Theologian, when it falls on the Sunday of the Fathers before Pentecost, with the exception of the Vigil. At the Liturgy: Troparia of all three services -- according to their order. Prokimenon-Alleluia, Apostle-Gospel -- to the Fathers and Vladimir; we do not take the daily ones (Note on p. 296 [→REF:p296]). Communion Hymn -- "Praise" and to Vladimir.'
    new_fn741 = '[^741]: Everything -- according to the rubric of the Theologian, when it falls on the Sunday of the Fathers before Pentecost, with the exception of the Vigil. At the Liturgy: Troparia of all three services -- according to their order. Prokimenon-Alleluia, Apostle-Gospel -- to the Fathers and Vladimir; we do not take the daily ones (Note on p. 296 [→REF:p296]). Communion Hymn -- "Praise" and to Vladimir. The Tserkovne Oko and our Menaion add: with Polyeleos; and our Menaion adds: "Praise [the Lord]" (Kvalite) also to Vladimir.'
    content = content.replace(old_fn741, new_fn741)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Footnotes updated successfully.")

def modify_glossary():
    path = get_path("Final_Dolnytsky_glossary.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("the priest refuses them only at the Vigil", "the priest says them only at the Vigil")
        content = content.replace("these litanies should be refused also at Small Matins", "these litanies should be said also at Small Matins")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Glossary updated successfully.")
    else:
        print("Glossary file not found, skipping.")

if __name__ == "__main__":
    modify_part2()
    modify_part4()
    modify_part5()
    modify_appendix()
    modify_footnotes()
    modify_glossary()
    print("All remediations applied successfully!")
