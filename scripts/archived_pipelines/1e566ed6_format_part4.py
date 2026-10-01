import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
backup_path = os.path.join(typikon_dir, "backup", "Final_Dolnytsky_part4_triodion.md")
target_path = os.path.join(typikon_dir, "Final_Dolnytsky_part4_triodion.md")

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

# Specific Dialogues replacements
# 1. L118 dialogue
dialogue_118_orig = 'Both now: Sunday Theotokion. Priest exclaims: "To Thee belongs glory".'
dialogue_118_form = 'Both now: Sunday Theotokion.\r\n\r\nPriest exclaims:\r\n> **Priest**: "To Thee belongs glory..."'

# Normalize dialogue forms to Unix newlines
dialogue_118_form = dialogue_118_form.replace('\r\n', '\n')
dialogue_232_form = dialogue_232_form.replace('\r\n', '\n')
dialogue_273_form = dialogue_273_form.replace('\r\n', '\n')
dialogue_304_form = dialogue_304_form.replace('\r\n', '\n')
dialogue_469_form = dialogue_469_form.replace('\r\n', '\n')
dialogue_547_form = dialogue_547_form.replace('\r\n', '\n')
dialogue_567_form = dialogue_567_form.replace('\r\n', '\n')
dialogue_602_form = dialogue_602_form.replace('\r\n', '\n')
dialogue_637_form = dialogue_637_form.replace('\r\n', '\n')
dialogue_642_form = dialogue_642_form.replace('\r\n', '\n')

content = content.replace(dialogue_118_orig, dialogue_118_form)

# 2. L232 dialogue
dialogue_232_orig = 'Both now: "With the hand of clay". Priest exclaims: "To Thee belongs glory".'
dialogue_232_form = 'Both now: "With the hand of clay".\r\n\r\nPriest exclaims:\r\n> **Priest**: "To Thee belongs glory..."'
content = content.replace(dialogue_232_orig, dialogue_232_form)

# 3. L273 dialogue
dialogue_273_orig = 'the Priest: "Blessed is our God". The Choir: "Amen", also reader: "Glory to Thee, our God, glory to Thee", "O Heavenly King" and everything else as at Compline. After "Glory to God in the highest" in the middle of Compline, the Priest, having gone out before the steps of the altar, bows and opens the Holy Doors, and the Choir: "Amen", also reader: "O come, let us worship" (3).'
dialogue_273_form = 'the Priest:\r\n> **Priest**: "Blessed is our God always, now and ever, and unto ages of ages."\r\n> \r\n> **Choir**: "Amen."\r\n\r\nAlso reader: "Glory to Thee, our God, glory to Thee", "O Heavenly King" and everything else as at Compline. After "Glory to God in the highest" in the middle of Compline, the Priest, having gone out before the steps of the altar, bows and opens the Holy Doors, and:\r\n> **Choir**: "Amen."\r\n> \r\n> **Reader**: "O come, let us worship..." (3)'
content = content.replace(dialogue_273_orig, dialogue_273_form)

# 4. L304 dialogue
dialogue_304_orig = 'At the end of the readings the Priest exclaims: "Peace be to all", "Wisdom", and the first Deacon exclaims: "Let us attend", and the second: "Wisdom! Let us attend!" and they sing the Prokimenon'
dialogue_304_form = 'At the end of the readings the Priest exclaims:\r\n> **Priest**: "Peace be to all."\r\n> \r\n> **Priest**: "Wisdom!"\r\n> \r\n> **First Deacon**: "Let us attend!"\r\n> \r\n> **Second Deacon**: "Wisdom! Let us attend!"\r\n\r\nAnd they sing the Prokimenon'
content = content.replace(dialogue_304_orig, dialogue_304_form)

# 5. L469 dialogue
dialogue_469_orig = 'Troparion of the Feast once. Priest: "Glory to Thee, O Christ God". Choir: "Glory, Both now", "Lord, have mercy" (3), "Lord, bless". Dismissal'
dialogue_469_form = 'Troparion of the Feast once.\r\n> **Priest**: "Glory to Thee, O Christ God, our hope, glory to Thee."\r\n> \r\n> **Choir**: "Glory, Both now. Lord, have mercy (3). Lord, bless."\r\n\r\nDismissal'
content = content.replace(dialogue_469_orig, dialogue_469_form)

# 6. L547 dialogue
dialogue_547_orig = 'reads the prayer of blessing. Deacon exclaims (if there be none, then the Priest himself) "Let us pray to the Lord", reads aloud (from the Sluzhebnik) the prayer "O Lord our God". Priest: "Peace be to all". The deacon: "Bow your heads unto the Lord". The Choir: "Amen", and after the prayer at the bowing of heads (which he says quietly), he exclaims: "By the grace". And immediately he blesses the branches'
dialogue_547_form = 'reads the prayer of blessing.\r\n\r\nDeacon exclaims (if there be none, then the Priest himself):\r\n> **Deacon**: "Let us pray to the Lord."\r\n\r\nReads aloud (from the *Sluzhebnik*) the prayer "O Lord our God".\r\n> **Priest**: "Peace be to all."\r\n> \r\n> **Deacon**: "Bow your heads unto the Lord."\r\n> \r\n> **Choir**: "Amen."\r\n\r\nAnd after the prayer at the bowing of heads (which he says quietly), he exclaims:\r\n> **Priest**: "By the grace..."\r\n\r\nAnd immediately he blesses the branches'
content = content.replace(dialogue_547_orig, dialogue_547_form)

# 7. L567 dialogue
dialogue_567_orig = 'At the end of the readings: the Priest: "And that we may be accounted worthy".'
dialogue_567_form = 'At the end of the readings:\r\n> **Priest**: "And that we may be accounted worthy..."'
content = content.replace(dialogue_567_orig, dialogue_567_form)

# 8. L602, 603 dialogue
dialogue_602_orig = '##### 8.\tPriest: "Wisdom"; Choir: "Bless".\r\nPriest: "Blessed be He... ages"; Choir: "Amen"; and 1st Hour.'
dialogue_602_form = '##### 8. Dismissal\r\n> **Priest**: "Wisdom!"\r\n> \r\n> **Choir**: "Bless."\r\n> \r\n> **Priest**: "Blessed be He... ages."\r\n> \r\n> **Choir**: "Amen."\r\n\r\nAnd 1st Hour.'
content = content.replace(dialogue_602_orig, dialogue_602_form)

# 9. L637 dialogue
dialogue_637_orig = 'Priest: "Let us attend" and reads the first Gospel.'
dialogue_637_form = '> **Priest**: "Let us attend!"\r\n\r\nAnd reads the first Gospel.'
content = content.replace(dialogue_637_orig, dialogue_637_form)

# 10. L642 dialogue
dialogue_642_orig = 'comes out through the holy doors to the analogion, the first Deacon exclaims: "And that we may be accounted worthy". Priest: "Peace be to all". Second deacon: "Wisdom, Aright. Let us listen". Priest: "The Reading from (Name)". First deacon: "Let us attend". Priest - reading.'
dialogue_642_form = 'comes out through the holy doors to the analogion:\r\n> **First Deacon**: "And that we may be accounted worthy."\r\n> \r\n> **Priest**: "Peace be to all."\r\n> \r\n> **Second Deacon**: "Wisdom, Aright. Let us listen."\r\n> \r\n> **Priest**: "The Reading from (Name)."\r\n> \r\n> **First Deacon**: "Let us attend."\r\n\r\nPriest - reading.'
content = content.replace(dialogue_642_orig, dialogue_642_form)

with open(target_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Formatting of Part 4 completed.")
