import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
backup_path = os.path.join(typikon_dir, "backup", "Final_Dolnytsky_part3_menaion.md")
target_path = os.path.join(typikon_dir, "Final_Dolnytsky_part3_menaion.md")

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
# 1. L252 dialogue
dialogue_252_orig = 'the Deacon, holding the orarion with three fingers, exclaims: "Wisdom, upright!" and immediately the Choir: "Amen" and the Priest: "For Thine is the kingdom" and we close the Holy Doors.'
dialogue_252_form = 'the Deacon, holding the *orarion* with three fingers, exclaims:\r\n> **Deacon**: "Wisdom, upright!"\r\n> \r\n> **Choir**: "Amen."\r\n> \r\n> **Priest**: "For Thine is the kingdom..."\r\n\r\nAnd we close the Holy Doors.'

# Normalize dialogue forms to Unix newlines
dialogue_252_form = dialogue_252_form.replace('\r\n', '\n')
dialogue_259_form = dialogue_259_form.replace('\r\n', '\n')
dialogue_788_form = dialogue_788_form.replace('\r\n', '\n')
dialogue_792_form1 = dialogue_792_form1.replace('\r\n', '\n')
dialogue_792_form2 = dialogue_792_form2.replace('\r\n', '\n')
dialogue_812_form = dialogue_812_form.replace('\r\n', '\n')
dialogue_879_form = dialogue_879_form.replace('\r\n', '\n')
dialogue_1334_form = dialogue_1334_form.replace('\r\n', '\n')
dialogue_1335_form = dialogue_1335_form.replace('\r\n', '\n')
dialogue_1337_form = dialogue_1337_form.replace('\r\n', '\n')

content = content.replace(dialogue_252_orig, dialogue_252_form)

# 2. L259 dialogue
dialogue_259_orig = 'At the end of the Doxology the Priest exclaims: "Glory to Thee, Who Hast shown us the light" and while singing'
dialogue_259_form = 'At the end of the Doxology the Priest exclaims:\r\n> **Priest**: "Glory to Thee, Who Hast shown us the light!"\r\n\r\nAnd while singing'
content = content.replace(dialogue_259_orig, dialogue_259_form)

# 3. L788 dialogue
dialogue_788_orig = 'begins the usual: "Blessed is our God". Choir: "Amen", also "Glory to Thee, our God, glory to Thee", "O Heavenly King" and everything else, as usual, up to "O come, let us worship" inclusive[^320][^313].'
dialogue_788_form = 'begins the usual:\r\n> **Priest**: "Blessed is our God always, now and ever, and unto ages of ages."\r\n> \r\n> **Choir**: "Amen."\r\n\r\nAlso "Glory to Thee, our God, glory to Thee", "O Heavenly King" and everything else, as usual, up to "O come, let us worship" inclusive[^320][^313].'
content = content.replace(dialogue_788_orig, dialogue_788_form)

# 4. L792 dialogues
dialogue_792_orig1 = 'The right Deacon exclaims: "Let us attend!", and the left, after the giving of peace by the Priest: "Wisdom! Let us attend!". Also before the first and second reading - the right: "Wisdom!", and the left: "Let us attend!" and they cense'
dialogue_792_form1 = 'The right Deacon exclaims:\r\n> **Right Deacon**: "Let us attend!"\r\n> \r\n> And the left, after the giving of peace by the Priest:\r\n> **Left Deacon**: "Wisdom! Let us attend!"\r\n> \r\n> Also before the first and second reading, the right exclaims:\r\n> **Right Deacon**: "Wisdom!"\r\n> \r\n> And the left:\r\n> **Left Deacon**: "Let us attend!"\r\n\r\nAnd they cense'
content = content.replace(dialogue_792_orig1, dialogue_792_form1)

dialogue_792_orig2 = 'The right Deacon exclaims: "Wisdom, attend!", "Let us hear", the Priest: "The reading from the Holy Gospel according to (Name)", and the left deacon: "Let us attend!". The Priest sings the Gospel.'
dialogue_792_form2 = 'The right Deacon exclaims:\r\n> **Right Deacon**: "Wisdom, attend! Let us hear."\r\n> \r\n> The Priest exclaims:\r\n> **Priest**: "The reading from the Holy Gospel according to (Name)."\r\n> \r\n> And the left Deacon:\r\n> **Left Deacon**: "Let us attend!"\r\n\r\nThe Priest sings the Gospel.'
content = content.replace(dialogue_792_orig2, dialogue_792_form2)

# 5. L812, 813, 814 dialogues
dialogue_812_orig = '##### 8.\tChoir: "It is truly meet" with "More honorable than the Cherubim".\r\nPriest: "Glory to Thee, O Christ God".\r\nChoir: "Glory, Both now", "Lord, have mercy" (3), "Lord, bless".'
dialogue_812_form = '##### 8. Liturgical Dialogues\r\n> **Choir**: "It is truly meet" with "More honorable than the Cherubim".\r\n> \r\n> **Priest**: "Glory to Thee, O Christ God."\r\n> \r\n> **Choir**: "Glory, Both now. Lord, have mercy (3). Lord, bless."'
content = content.replace(dialogue_812_orig, dialogue_812_form)

# 6. L879 dialogue
dialogue_879_orig = 'begins the usual: "Blessed is our God". Choir: "Amen", also "Glory to Thee, our God, glory to Thee", "O Heavenly King" and everything else, as usual, up to "O come, let us worship" inclusive. At the second "O come, let us worship" the Priest, having bowed low'
dialogue_879_form = 'begins the usual:\r\n> **Priest**: "Blessed is our God always, now and ever, and unto ages of ages."\r\n> \r\n> **Choir**: "Amen."\r\n\r\nAlso "Glory to Thee, our God, glory to Thee", "O Heavenly King" and everything else, as usual, up to "O come, let us worship" inclusive. At the second "O come, let us worship" the Priest, having bowed low'
content = content.replace(dialogue_879_orig, dialogue_879_form)

# 7. L1334, 1335, 1337 dialogues
dialogue_1334_orig = 'before which the first Deacon exclaims: "Wisdom, attend" and the rest, and the second: "Let us attend".'
dialogue_1334_form = 'before which the first Deacon exclaims:\r\n> **First Deacon**: "Wisdom, attend!"\r\n> \r\n> And the second:\r\n> **Second Deacon**: "Let us attend!"'
content = content.replace(dialogue_1334_orig, dialogue_1334_form)

dialogue_1335_orig = 'the Deacon says the litany "In peace let us pray to the Lord", during which the Priest reads quietly the prayer "O Lord Jesus Christ"; and after the prayer He does not exclaim, but says to Himself: "Amen". And when "For the precipitous, pure" is said, the Priest begins loudly this prayer: "Great Art Thou, O Lord"'
dialogue_1335_form = 'the Deacon says the litany:\r\n> **Deacon**: "In peace let us pray to the Lord."\r\n> \r\n> During which the Priest reads quietly the prayer *"O Lord Jesus Christ"*; and after the prayer he does not exclaim, but says to himself:\r\n> **Priest**: "Amen."\r\n> \r\n> And when *"For the precipitous, pure"* is said, the Priest begins loudly this prayer: *"Great Art Thou, O Lord"*'
content = content.replace(dialogue_1335_orig, dialogue_1335_form)

dialogue_1337_orig = 'At the end of this prayer the Choir: "Amen"; priest: "Peace be unto all" and, after the prayer at the bowing of heads, which he says quietly, he exclaims: "For Thou Art the sanctification" and immediately'
dialogue_1337_form = 'At the end of this prayer:\r\n> **Choir**: "Amen."\r\n> \r\n> **Priest**: "Peace be unto all."\r\n> \r\n> And after the prayer at the bowing of heads, which he says quietly, he exclaims:\r\n> **Priest**: "For Thou Art the sanctification..."\r\n\r\nAnd immediately'
content = content.replace(dialogue_1337_orig, dialogue_1337_form)

with open(target_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Formatting of Part 3 completed.")
