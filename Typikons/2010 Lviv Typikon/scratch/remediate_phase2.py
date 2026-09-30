import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def remediate_part3():
    txt_path = Path('Final/Final_Dolnytsky_part3_menaion.txt')
    md_path = Path('Final MD/Final_Dolnytsky_part3_menaion.md')
    
    txt = txt_path.read_text(encoding='utf-8')
    md = md_path.read_text(encoding='utf-8')

    # =========================================================================
    # 1. REMEDIATE SEPTEMBER 1 & JANUARY 11 FOOTNOTES
    # =========================================================================
    # Ingest [^241], [^242], [^243], [^244], [^245], [^246] into September 1
    # Remove spurious [^360] from September 1 and place on January 11

    # In TXT:
    # L6: Service of the Indiction[^241], that is, the New Year, and of our Venerable Father Simeon the Stylite, and the memory of the Synaxis of the Most Holy Theotokos in Miasena[^242],
    txt = txt.replace(
        "Service of the Indiction, that is, the New Year, and of our Venerable Father Simeon the Stylite, and the memory of the Synaxis of the Most Holy Theotokos in Miasena,",
        "Service of the Indiction[^241], that is, the New Year, and of our Venerable Father Simeon the Stylite, and the memory of the Synaxis of the Most Holy Theotokos in Miasena[^242],"
    )
    # L7: ...from the canon to the end is Great[^243].
    txt = txt.replace(
        "from the canon to the end is Great.",
        "from the canon to the end is Great[^243]."
    )
    # L24: 12.	After the Great Doxology: Troparion of the Indiction, Glory: to the Saint, Both now: to the Synaxis[^244].
    txt = txt.replace(
        "12.\tAfter the Great Doxology: Troparion of the Indiction, Glory: to the Saint, Both now: to the Synaxis.",
        "12.\tAfter the Great Doxology: Troparion of the Indiction, Glory: to the Saint, Both now: to the Synaxis[^244]."
    )
    # L29: After the Entrance - Troparion of the Indiction, Synaxis and Saint; Glory: Kontakion to the Saint, Both now: to the Indiction[^245].
    txt = txt.replace(
        "Glory: Kontakion to the Saint, Both now: to the Indiction. Everything else",
        "Glory: Kontakion to the Saint, Both now: to the Indiction[^245]. Everything else"
    )
    # L31: Remove [^360] from September 1 Sunday note
    txt = txt.replace(
        "transferred to another day, at the decision of the Ecclesiarch[^360].",
        "transferred to another day, at the decision of the Ecclesiarch."
    )
    # L48: ...on the 9th - Resurrectional[^246].
    txt = txt.replace(
        "on the 6th - to the Saint, on the 9th - Resurrectional.",
        "on the 6th - to the Saint, on the 9th - Resurrectional[^246]."
    )
    # January 11: Attach [^360] where it belongs!
    txt = txt.replace(
        "11 JANUARY Our Venerable Father Theodosius\nEverything according to the general rule of a Saint with Polyeleos; but if it falls on the Sunday of the Publican, then his service must be transferred to another day, at the decision of the Ecclesiarch.",
        "11 JANUARY Our Venerable Father Theodosius\nEverything according to the general rule of a Saint with Polyeleos; but if it falls on the Sunday of the Publican, then his service must be transferred to another day, at the decision of the Ecclesiarch[^360]."
    )

    # In MD:
    md = md.replace(
        "Service of the Indiction, that is, the New Year, and of our Venerable Father Simeon the Stylite, and the memory of the Synaxis of the Most Holy Theotokos in Miasena,",
        "Service of the Indiction[^241], that is, the New Year, and of our Venerable Father Simeon the Stylite, and the memory of the Synaxis of the Most Holy Theotokos in Miasena[^242],"
    )
    md = md.replace(
        "from the canon to the end is Great.",
        "from the canon to the end is Great[^243]."
    )
    md = md.replace(
        "6. **After the Great Doxology:** Troparion of the Indiction, Glory: to the Saint, Both now: to the Synaxis",
        "6. **After the Great Doxology:** Troparion of the Indiction, Glory: to the Saint, Both now: to the Synaxis[^244]"
    )
    md = md.replace(
        "Glory: Kontakion to the Saint, Both now: to the Indiction. Everything else",
        "Glory: Kontakion to the Saint, Both now: to the Indiction[^245]. Everything else"
    )
    md = md.replace(
        "> **Note:** The Troparion of the Synaxis is not taken; the canon of the martyrs is transferred to another day, at the decision of the Ecclesiarch[^360].",
        "> **Note:** The Troparion of the Synaxis is not taken; the canon of the martyrs is transferred to another day, at the decision of the Ecclesiarch."
    )
    # January 11 in MD:
    md = md.replace(
        "#### 11 January — Our Venerable Father Theodosius\n\nEverything according to the general rule of a Saint with Polyeleos; but if it falls on the Sunday of the Publican, then his service must be transferred to another day, at the decision of the Ecclesiarch.",
        "#### 11 January — Our Venerable Father Theodosius\n\nEverything according to the general rule of a Saint with Polyeleos; but if it falls on the Sunday of the Publican, then his service must be transferred to another day, at the decision of the Ecclesiarch[^360]."
    )

    # =========================================================================
    # 2. REMEDIATE SUNDAY GREAT VESPERS NUMBERING IN MD
    # =========================================================================
    sunday_vespers_target = """##### At Great Vespers

1. **Kathisma:** *“Blessed is the man”* (according to the rule – entire)

2. **On *"Lord, I have cried"*:* 10 stichera: Resurrectional of the *Octoechos* – 4, Indiction – 3 and Saint – 3; Glory: to the Saint, Both now: 1st Theotokion of the tone (Dogmatikon)

3.	3 readings: Indiction – 2 and Saint – 1.

3. **Aposticha:** Aposticha Resurrectional, Glory: to the Saint, Both now: to the Indiction

4. **Troparia:** Troparion Resurrectional, Glory: to the Saint, Both now: to the Indiction

5. **Dismissal:** Great Dismissal with Resurrectional and Saints' commemorations"""

    sunday_vespers_replacement = """##### At Great Vespers

1. **Kathisma:** *“Blessed is the man”* (according to the rule – entire)

2. **On *"Lord, I have cried"*:* 10 stichera: Resurrectional of the *Octoechos* – 4, Indiction – 3 and Saint – 3; Glory: to the Saint, Both now: 1st Theotokion of the tone (Dogmatikon)

3. **Readings:** 3 readings: Indiction – 2 and Saint – 1.

4. **Aposticha:** Aposticha Resurrectional, Glory: to the Saint, Both now: to the Indiction

5. **Troparia:** Troparion Resurrectional, Glory: to the Saint, Both now: to the Indiction

6. **Dismissal:** Great Dismissal with Resurrectional and Saints' commemorations"""

    md = md.replace(sunday_vespers_target, sunday_vespers_replacement)

    # Also clean Sunday Hours footnote in MD:
    md = md.replace(
        "on the 6th – to the Saint, on the 9th – Resurrectional.",
        "on the 6th – to the Saint, on the 9th – Resurrectional[^246]."
    )

    # =========================================================================
    # 3. REMEDIATE SEPTEMBER 12 & 14 FOOTNOTE MISPLACEMENTS
    # =========================================================================
    # In Sept 12: replace [^300] with [^257]
    txt = txt.replace(
        "on the 3rd and 9th - of the Forefeast[^300];",
        "on the 3rd and 9th - of the Forefeast[^257];"
    )
    md = md.replace(
        "on the 3rd and 9th – of the Forefeast[^300];",
        "on the 3rd and 9th – of the Forefeast[^257];"
    )

    # In Sept 14 Sunday after Exaltation:
    # replace [^379][^359][^338] with [^269]
    txt = txt.replace(
        '3.\tCommunion Hymn "Praise the Lord" and of the Feast[^379][^359][^338].',
        '3.\tCommunion Hymn "Praise the Lord" and of the Feast[^269].'
    )
    md = md.replace(
        '3. Communion Hymn "Praise the Lord" and of the Feast[^379][^359][^338]',
        '3. Communion Hymn "Praise the Lord" and of the Feast[^269]'
    )

    # Note after: replace [^345] with [^270]
    txt = txt.replace(
        'Communion Hymn "Praise the Lord" and of the Saint[^345].',
        'Communion Hymn "Praise the Lord" and of the Saint[^270].'
    )
    md = md.replace(
        'Communion Hymn "Praise the Lord" and of the Saint[^345].',
        'Communion Hymn "Praise the Lord" and of the Saint[^270].'
    )

    # Attach Footnote 258 to Sept 14:
    txt = txt.replace(
        "Strict fast on this day the Lviv Synod permits for dairy.",
        "Strict fast on this day the Lviv Synod permits for dairy[^258]."
    )
    md = md.replace(
        "Strict fast on this day the Lviv Synod permits for dairy.",
        "Strict fast on this day the Lviv Synod permits for dairy[^258]."
    )

    # =========================================================================
    # 4. VOCABULARY MATRIX AUTO-REMEDIATION FOR PART 3
    # =========================================================================
    # Replace "irmos" -> "heirmos", "irmoi" -> "heirmoi", "prokeimena" -> "prokimena"
    # Case-sensitive / boundary-safe replacements
    for src, dst in [
        (r'\birmos\b', 'heirmos'),
        (r'\bIrmos\b', 'Heirmos'),
        (r'\birmoi\b', 'heirmoi'),
        (r'\bIrmoi\b', 'Heirmoi'),
        (r'\bprokeimena\b', 'prokimena'),
        (r'\bProkeimena\b', 'Prokimena'),
        (r'\bprokeimenon\b', 'prokimenon'),
        (r'\bProkeimenon\b', 'Prokimenon'),
        (r'\bService Book\b', 'Sluzhebnik'),
        (r'\bService Books\b', 'Sluzhebnyky'),
        (r'\bservice books\b', 'sluzhebnyky'),
        (r'\bIrmologion\b', 'Heirmologion'),
        (r'\birmologion\b', 'heirmologion'),
    ]:
        txt = re.sub(src, dst, txt)
        md = re.sub(src, dst, md)

    txt_path.write_text(txt, encoding='utf-8')
    md_path.write_text(md, encoding='utf-8')
    print("Part 3 remediation completed for TXT and MD!")

def remediate_other_files():
    # Fix Service Book in Part 4 and Footnotes
    p4_txt = Path('Final/Final_Dolnytsky_part4_triodion.txt')
    p4_md = Path('Final MD/Final_Dolnytsky_part4_triodion.md')
    fn_txt = Path('Final/Final_footnotes.txt')
    fn_md = Path('Final MD/Final_footnotes.md')

    for p in [p4_txt, p4_md]:
        if p.exists():
            c = p.read_text(encoding='utf-8')
            c = re.sub(r'\bService Book\b', 'Sluzhebnik', c)
            p.write_text(c, encoding='utf-8')

    for p in [fn_txt, fn_md]:
        if p.exists():
            c = p.read_text(encoding='utf-8')
            c = re.sub(r'\bService Book\b', 'Sluzhebnik', c)
            c = re.sub(r'\bservice books\b', 'sluzhebnyky', c)
            c = re.sub(r'\bTypicon\b', 'Typikon', c)
            # Fix corrupted ????? in Footnote 360:
            c = c.replace('The Constantinopolitan ????? /Typikon/', 'The Constantinopolitan Τυπικὸν /Typikon/')
            p.write_text(c, encoding='utf-8')

    print("Part 4 and Footnotes vocabulary remediation completed!")

if __name__ == '__main__':
    remediate_part3()
    remediate_other_files()
