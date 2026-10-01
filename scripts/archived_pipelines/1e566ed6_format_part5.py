import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
backup_path = os.path.join(typikon_dir, "backup", "Final_Dolnytsky_part5_temple.md")
target_path = os.path.join(typikon_dir, "Final_Dolnytsky_part5_temple.md")

with open(backup_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n')

# Replace book names
books = ["Octoechos", "Menaion", "Horologion", "Heirmologion", "Sluzhebnik", "Anthologion", "Triodion", "Triodia", "Menology"]
for book in books:
    content = re.sub(r'(?<!\*)\b' + book + r'\b(?!\*)', r'*' + book + r'*', content)

# Clean up lists (o\t and ?\t)
content = re.sub(r'^\s*o\t', '  * ', content, flags=re.MULTILINE)
content = re.sub(r'^\s*\?\t', '  * ', content, flags=re.MULTILINE)
content = re.sub(r'^\s*o\s+', '  * ', content, flags=re.MULTILINE)
content = re.sub(r'^\s*\?\s+', '  * ', content, flags=re.MULTILINE)
content = re.sub(r'^\s*•\t', '  * ', content, flags=re.MULTILINE)

# Bold conditionals in lists
conditionals = [
    ("If two saints occur", "If two saints occur"),
    ("If a saint on 6 occurs", "If a saint on 6 occurs"),
    ("If the saint on 6 has", "If the saint on 6 has"),
    ("If there is only one choir", "If there is only one choir"),
    ("If there are also deacons", "If there are also deacons"),
    ("If the temple is of a saint", "If the temple is of a saint"),
    ("If the temple be of a saint", "If the temple be of a saint"),
    ("If the temple is of the Lord", "If the temple is of the Lord"),
    ("If the saint be on 6", "If the saint be on 6"),
]

for orig, replacement in conditionals:
    pattern = r'(\*\s+)' + re.escape(orig) + r'\b'
    content = re.sub(pattern, r'\1**' + replacement + r'**', content)

# Strip outer quotes from instruction paragraphs in Part 5
replacements = [
    (
        '"If on January 1 falls [the feast] of the temple of St. Basil of Caesarea or another saint, on the Sunday before Theophany, we sing the service of the temple, as of the temple of Symeon Stylites on Sunday"[^676], taking, instead of the service of the Indiction, the service of the Circumcision.',
        'If on January 1 falls [the feast] of the temple of St. Basil of Caesarea or another saint, on the Sunday before Theophany, we sing the service of the temple, as of the temple of Symeon Stylites on Sunday[^676], taking, instead of the service of the Indiction, the service of the Circumcision.'
    ),
    (
        '"On all these days we sing the service of the temple just as the service of the Meeting"[^677] here, on pp. 216-217 [→REF:p216-217] and 220. However:',
        'On all these days we sing the service of the temple just as the service of the Meeting[^677] here, on pp. 216-217 [→REF:p216-217] and 220. However:'
    ),
    (
        '"On these days we sing the service of the temple just as of other great saints which fall during Great Lent; and where at Matins there will be no *Triodion* [Three-Odes], we sing the Canon of the Theotokos with the Heirmos on 6 and of the temple on 8. Katavasia of the Theotokos. And where we sing the *Triodion* [Three-Odes], we take the Canon of the temple on 6 and of the *Triodion* according to its order (on 8), and at the end - Heirmos of the *Triodion*"[^685].',
        'On these days we sing the service of the temple just as of other great saints which fall during Great Lent; and where at Matins there will be no *Triodion* [Three-Odes], we sing the Canon of the Theotokos with the Heirmos on 6 and of the temple on 8. Katavasia of the Theotokos. And where we sing the *Triodion* [Three-Odes], we take the Canon of the temple on 6 and of the *Triodion* according to its order (on 8), and at the end - Heirmos of the *Triodion*[^685].'
    ),
    # Let's also support the version without already formatted Triodion in case the search is from backup
    (
        '"On these days we sing the service of the temple just as of other great saints which fall during Great Lent; and where at Matins there will be no Triodion [Three-Odes], we sing the Canon of the Theotokos with the Heirmos on 6 and of the temple on 8. Katavasia of the Theotokos. And where we sing the Triodion [Three-Odes], we take the Canon of the temple on 6 and of the Triodion according to its order (on 8), and at the end - Heirmos of the Triodion"[^685].',
        'On these days we sing the service of the temple just as of other great saints which fall during Great Lent; and where at Matins there will be no *Triodion* [Three-Odes], we sing the Canon of the Theotokos with the Heirmos on 6 and of the temple on 8. Katavasia of the Theotokos. And where we sing the *Triodion* [Three-Odes], we take the Canon of the temple on 6 and of the *Triodion* according to its order (on 8), and at the end - Heirmos of the *Triodion*[^685].'
    ),
    (
        '"In these days we sing the service of the temple just as the service of St. George"[^689].',
        'In these days we sing the service of the temple just as the service of St. George[^689].'
    ),
    (
        '"We sing the service of the temple in the evening, and the stichera as indicated for the Theologian or St. George with Mid-Pentecost. On Pentecost Sunday, at Great Vespers - "Entrance," Great Prokimenon "Who is so great a God"; Readings (readings - 3) are of the temple and everything else with the kneeling prayers. At the Litiya: stichera of the temple, if there be any, Glory: of the temple, Both now: of the feast. Aposticha of the feast with its stichera; the rest of the service in the evening and in the morning is sung just as for the Theologian on Mid-Pentecost"[^690].',
        'We sing the service of the temple in the evening, and the stichera as indicated for the Theologian or St. George with Mid-Pentecost. On Pentecost Sunday, at Great Vespers - "Entrance," Great Prokimenon *“Who is so great a God”*; Readings (readings - 3) are of the temple and everything else with the kneeling prayers. At the Litiya: stichera of the temple, if there be any, Glory: of the temple, Both now: of the feast. Aposticha of the feast with its stichera; the rest of the service in the evening and in the morning is sung just as for the Theologian on Mid-Pentecost[^690].'
    )
]

for orig, form in replacements:
    content = content.replace(orig, form)

with open(target_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Formatting of Part 5 completed.")
