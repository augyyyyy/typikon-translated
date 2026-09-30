# -*- coding: utf-8 -*-
import sys

# Define mappings from the line index (0-based) to term title and category
mapping = {
    0: ("Holy Doors vs. Royal Doors (Terminology)", "Liturgical Objects & Architecture", "Footnote [754], Appendix, L66"),
    1: ("Holy Liturgy (Concelebration & Repetition)", "Liturgical Monastic & Parish Celebrations", "Point 97, Appendix, L275"),
    2: ("Kyivan Rite (Byzantine-Ukrainian Rite)", "History & Rite Identification", "Intro, L214"),
    3: ("Typikons", "History & Rite Identification", "Intro, L215"),
    4: ("Daily Vespers (without Kathisma)", "Liturgical Services & Offices", "Part 1 Structure, L92"),
    5: ("Biblical Odes (Odes of Holy Scripture)", "Hymnographic Elements & Structures", "Part 1 Structure, L174"),
    6: ("Canon Structure (Litanies, Hymns, Sessional Hymns, Kontakia, Exaposteilaria)", "Hymnographic Elements & Structures", "Part 1 Structure, L176"),
    7: ("Troparia and Kontakia of the Saints", "Hymnographic Elements & Structures", "Part 1 Structure, L214"),
    8: ("Liturgical Readings (Prokeimena, Alleluias, Apostle-Gospel, Communion Hymns)", "Liturgical Readings & Scriptures", "Part 2 General Rubrics, L123"),
    9: ("Lity (Lytia) Rubrics", "Liturgical Services & Offices", "Part 2 General Rubrics, L225"),
    10: ("Liturgical Readings for Forefathers & Saints", "Liturgical Readings & Scriptures", "Part 3 Menaion, L425"),
    11: ("Feasts of Saints (Service of St. Anne)", "Liturgical Monastic & Parish Celebrations", "Part 3 Menaion, L2387"),
    12: ("Biblical Odes in the Triodion Canon", "Hymnographic Elements & Structures", "Part 4 Triodion, L211"),
    13: ("Tomb Canon of Great Saturday", "Liturgical Services & Offices", "Part 4 Triodion, L723"),
    14: ("Shroud (Epitaphios) Placement and Custom", "Liturgical Objects & Architecture", "Part 4 Triodion, L729"),
    17: ("Ruthenian Catholic Church (Ukrainian Greek Catholic Church)", "History & Rite Identification", "Footnote 1, L2"),
    18: ("Censing at the Litiya (Lytia)", "Liturgical Services & Offices", "Footnote 14, L15"),
    19: ("Troparia of the Day, Temple, and Saints", "Hymnographic Elements & Structures", "Footnote 20, L21"),
    20: ("Midnight Office on Feasts of the Lord and Theotokos", "Liturgical Services & Offices", "Footnote 22, L23"),
    21: ("Hymn 'Holy is the Lord our God' and its Verses", "Hymnographic Elements & Structures", "Footnote 38, L41"),
    22: ("Saints 'on 4' and Alleluia Services", "Liturgical Services & Offices", "Footnote 45, L49"),
    23: ("Sunday Troparia and Kontakia at the Liturgical Hours", "Hymnographic Elements & Structures", "Footnote 65, L70"),
    24: ("Kathismata and Small Litanies at Matins", "Liturgical Services & Offices", "Footnote 77, L86"),
    25: ("Weekday Liturgy Commemorations (Greek vs. Slavonic)", "Liturgical Monastic & Parish Celebrations", "Footnote 91, L100"),
    26: ("Ancient Liturgical Gospels (Ostroh, Vatican)", "Liturgical Readings & Scriptures", "Footnote 93, L102"),
    27: ("Canon for the Dead and Panikhida", "Liturgical Services & Offices", "Footnote 107, L117"),
    28: ("Refrains to the Canons of the Octoechos", "Hymnographic Elements & Structures", "Footnote 108, L118"),
    29: ("Polyeleos Feasts (Greek and Slavic Rubrics)", "Liturgical Services & Offices", "Footnote 116, L128"),
    30: ("Exaposteilaria, Kontakia, and Theotokia after Canons", "Hymnographic Elements & Structures", "Footnote 127, L139"),
    31: ("Small Vespers and Great Vespers on Feasts", "Liturgical Services & Offices", "Footnote 160, L175"),
    32: ("Saints 'on 6' without Polyeleos", "Liturgical Services & Offices", "Footnote 168, L184"),
    33: ("Forefeast and Afterfeast Rubrics", "Liturgical Services & Offices", "Footnote 171, L187"),
    34: ("Troparion and Kontakion of Forefeast and Saints", "Hymnographic Elements & Structures", "Footnote 180, L196"),
    35: ("Tserkovne Oko (Church Eye) Authority", "History & Rite Identification", "Footnote 181, L197"),
    36: ("Trisagion vs. 'As Many as Have Been Baptized into Christ'", "Hymnographic Elements & Structures", "Footnote 183, L199"),
    38: ("Dogmatikon Refrains on Afterfeasts", "Hymnographic Elements & Structures", "Footnote 184, L201"),
    39: ("Feast of the Annunciation (Irmos Rubrics)", "Liturgical Services & Offices", "Footnote 193, L210"),
    40: ("Trisagion in Afterfeast and Bright Week", "Hymnographic Elements & Structures", "Footnote 201, L219"),
    42: ("Liturgical Commemorations (Moscow Typikon vs. Mark's Chapters)", "History & Rite Identification", "Footnote 202, L220"),
    43: ("Feasts of Saints (Forefathers and Saints)", "Liturgical Monastic & Parish Celebrations", "Footnote 250, L269"),
    44: ("Exaltation of the Holy Cross (Flowers and Basil)", "Liturgical Services & Offices", "Footnote 259, L278"),
    45: ("Holy Doors vs. Royal Doors (Historical Usage & Rubrics)", "Liturgical Objects & Architecture", "Footnote 264, L283"),
    46: ("Kathisma 'Blessed is the Man' on Feasts", "Hymnographic Elements & Structures", "Footnote 277, L296"),
    47: ("Feast of St. Catherine (Transfer of Feasts)", "Liturgical Monastic & Parish Celebrations", "Footnote 279, L298"),
    48: ("Feasts of Saints (St. Peter and Paul stichera)", "Liturgical Monastic & Parish Celebrations", "Footnote 282, L301"),
    49: ("Troparion of the Saints at Hours", "Hymnographic Elements & Structures", "Footnote 285, L304"),
    50: ("Saturday before the Nativity of Christ (Forefathers Saturday)", "Liturgical Services & Offices", "Footnote 297, L317"),
    51: ("Litanies at the Liturgical Hours (Greek vs. Slavic)", "Liturgical Services & Offices", "Footnote 311, L331"),
    52: ("Dismissals (Feast vs. Day Commemorations)", "Liturgical Services & Offices", "Footnote 317, L337"),
    53: ("Vespers and Vigil on the Eves of Nativity and Theophany", "Liturgical Services & Offices", "Footnote 318, L338"),
    54: ("Weekday Commemorations (Moscow Typikon)", "Liturgical Monastic & Parish Celebrations", "Footnote 334, L354"),
    55: ("Compline and Midnight Office on Feasts without Vigil", "Liturgical Services & Offices", "Footnote 341, L362"),
    56: ("Prokeimena and Gospels on Circumcision and Feast", "Liturgical Readings & Scriptures", "Footnote 342, L363"),
    57: ("Dogmatikon and Afterfeasts on Fridays", "Hymnographic Elements & Structures", "Footnote 376, L397"),
    58: ("Blessing of Water on August 1", "Liturgical Services & Offices", "Footnote 454, L475"),
    59: ("Liturgical Colors (Crimson and Red)", "Liturgical Objects & Architecture", "Footnote 455, L476"),
    60: ("Lenten Vespers (The Litany after Vespers)", "Liturgical Services & Offices", "Footnote 508, L529"),
    61: ("Gospel at Lazarus Saturday Matins", "Liturgical Readings & Scriptures", "Footnote 570, L591"),
    62: ("Rite of the Shroud (Epitaphios) in the Greek and Ukrainian Rite", "Liturgical Services & Offices", "Footnote 600, L621"),
    63: ("Paschal Procession and Reception of Light", "Liturgical Services & Offices", "Footnote 615, L636"),
    64: ("Singing of 'Christ is Risen' from Pascha to Ascension", "Liturgical Services & Offices", "Footnote 626, L647"),
    66: ("Saints' Troparia in modern Horologia", "Hymnographic Elements & Structures", "Footnote 699, L720"),
    67: ("Feasts of the Holy Apostles (Vigil and Polyeleos)", "Liturgical Monastic & Parish Celebrations", "Footnote 704, L725"),
}

def clean_content(text):
    text = text.strip()
    # Remove leading quotes or formatting if any
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    return text

with open(r'e:\Google Antigravity\Projects\Translation\scratch\typikon_terms.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

glossary_entries = []
seen_content = set()

for idx, line in enumerate(lines):
    if idx not in mapping:
        continue
    
    parts = line.split(':', 2)
    if len(parts) < 3:
        continue
    
    content = clean_content(parts[2])
    
    # Simple deduplication
    if content in seen_content:
        continue
    seen_content.add(content)
    
    term_name, category, ref = mapping[idx]
    glossary_entries.append({
        'term': term_name,
        'category': category,
        'ref': ref,
        'content': content
    })

# Sort alphabetically by term
glossary_entries.sort(key=lambda x: x['term'].lower())

# Build Markdown output
md = []
md.append("# Dolnytsky Typikon — Liturgical Terminology & Commentary Appendix")
md.append("This appendix compiles and organizes the extensive historical, theological, and rubrical commentary from the footnotes and structural notes of the Dolnytsky Typikon translation. It serves as an authoritative reference for scholars and translators studying the Kyivan and Byzantine-Ruthenian liturgical traditions.\n")

# Table of Contents
md.append("## Table of Contents")
for entry in glossary_entries:
    anchor = entry['term'].lower().replace(" ", "-").replace("(", "").replace(")", "").replace("/", "").replace(",", "").replace("'", "").replace("&", "and")
    md.append(f"- [{entry['term']}](#{anchor})")
md.append("\n---\n")

# Direct alphabetical listing
current_letter = ""
for entry in glossary_entries:
    first_char = entry['term'][0].upper()
    if first_char != current_letter:
        current_letter = first_char
        md.append(f"## {current_letter}\n")
    
    md.append(f"### {entry['term']}")
    md.append(f"- **Category:** *{entry['category']}*")
    md.append(f"- **Source Reference:** *{entry['ref']}*")
    md.append(f"\n{entry['content']}\n")
    md.append("---\n")

# Write output file
output_path = r'e:\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_glossary.md'
with open(output_path, 'w', encoding='utf-8') as out:
    out.write("\n".join(md))

print(f"Glossary successfully generated at {output_path} with {len(glossary_entries)} entries.")
