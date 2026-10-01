import os
import re

def slugify(text):
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9\s\-]', '', slug)
    slug = slug.replace(' ', '-')
    slug = re.sub(r'-+', '-', slug)
    return slug

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
intro_path = os.path.join(typikon_dir, "Final_Dolnytsky_intro.md")

with open(intro_path, 'r', encoding='utf-8') as f:
    intro_content = f.read()

toc_links = re.findall(r'\[([^\]]+)\]\(#([^\)]+)\)', intro_content)

# We load and update the headings in all files
# Let's write a targeted list of heading replacements for Part 2 to make it 100% correct
part2_path = os.path.join(typikon_dir, "Final_Dolnytsky_part2_general_rubrics.md")
with open(part2_path, 'r', encoding='utf-8') as f:
    part2_content = f.read()

part2_replacements = [
    # 2.6
    (r'^##### 6\.\tSaint with All-Night Vigil on Sunday\s*$', '## 2.6 Saint with an All-Night Vigil on a Sunday'),
    # 2.7
    (r'^##### 7\.\tSaint with All-Night Vigil on weekdays\s*$', '## 2.7 Saint with an All-Night Vigil on Weekdays and Saturday'),
    # 2.8
    (r'^Forefeast with a Saint without Polyeleos on a Sunday\s*$', '## 2.8 Forefeast with a Saint without a Polyeleos on a Sunday'),
    # 2.13
    (r'^AFTERFEAST WITH A SAINT WITHOUT POLYELEOS ON A SUNDAY\s*$', '## 2.13 Afterfeast with a Saint without a Polyeleos on a Sunday'),
    # 2.15
    (r'^AFTERFEAST WITH A SAINT WITH POLYELEOS ON A SUNDAY\s*$', '## 2.15 Afterfeast with a Saint with a Polyeleos on a Sunday'),
    # 2.16
    (r'^AFTERFEAST WITH A SAINT WITH POLYELEOS ON WEEKDAYS\b.*$', '## 2.16 Afterfeast with a Saint with a Polyeleos on Weekdays'),
    # 2.18
    (r'^AFTERFEAST WITH A SAINT WITH ALL-NIGHT VIGIL ON WEEKDAYS\b.*$', '## 2.18 Afterfeast with a Saint with an All-Night Vigil on Weekdays'),
    # 2.19
    (r'^APODOSIS \(APODOSIS\) OF A FEAST ON A SUNDAY\s*$', '## 2.19 Apodosis of a Feast on a Sunday'),
    # 2.20
    (r'^APODOSIS \(APODOSIS\) OF A FEAST ON WEEKDAYS\s*$', '## 2.20 Apodosis of a Feast on Weekdays')
]

for pattern, repl in part2_replacements:
    part2_content, count = re.subn(pattern, repl, part2_content, flags=re.MULTILINE | re.IGNORECASE)
    if count > 0:
        print(f"Part 2 Heading Update: Replaced pattern with '{repl}' ({count} match(es)).")

with open(part2_path, 'w', encoding='utf-8') as f:
    f.write(part2_content)

# Now let's do similar replacements for Part 3 month date headings and sections to match TOC:
# For example:
# "3.1.1 1 September: Beginning of the Indiction (New Year)" -> in file: "### 1 SEPTEMBER - Beginning of the Indiction"
# Let's map the Part 3 headings!
part3_path = os.path.join(typikon_dir, "Final_Dolnytsky_part3_menaion.md")
with open(part3_path, 'r', encoding='utf-8') as f:
    part3_content = f.read()

part3_replacements = [
    (r'^### 1 SEPTEMBER\s+-\s+Beginning of the Indiction\s*$', '### 3.1.1 1 September: Beginning of the Indiction (New Year)'),
    (r'^SATURDAY AND SUNDAY BEFORE THE EXALTATION\s*$', '### 3.1.2 Saturday and Sunday before the Exaltation'),
    (r'^### 12 SEPTEMBER Memory of the Renovation of the Temple of the Resurrection\s*$', '### 3.1.3 12 September: Memory of the Renovation of the Temple of the Resurrection'),
    (r'^### 14 SEPTEMBER Universal Exaltation of the Precious Cross\s*$', '### 3.1.4 14 September: Universal Exaltation of the Precious Cross'),
    (r'^SATURDAY AFTER THE EXALTATION\s*$', '### 3.1.5 Saturday after the Exaltation'),
    (r'^SUNDAY AFTER THE EXALTATION\s*$', '### 3.1.6 Sunday after the Exaltation'),
    (r'^APODOSIS OF THE FEAST OF THE EXALTATION\s*$', '### 3.1.7 Apodosis of the Feast of the Exaltation'),
    (r'^### 23 SEPTEMBER Conception of St. John the Baptist\s*$', '### 3.1.8 23 September: Conception of St. John the Baptist'),
    (r'^### 27 SEPTEMBER Falling Asleep of the Holy Apostle John the Theologian\s*$', '### 3.1.9 27 September: Falling Asleep of the Holy Apostle John the Theologian'),
    (r'^### 1 OCTOBER Protection of the Most Holy Theotokos,?\s*$', '### 3.2.1 1 October: Protection of the Most Holy Theotokos'),
    (r'^### 11 OCTOBER Sunday of the Holy Fathers\s*$', '### 3.2.2 11 October: Sunday of the Holy Fathers')
]

for pattern, repl in part3_replacements:
    part3_content, count = re.subn(pattern, repl, part3_content, flags=re.MULTILINE | re.IGNORECASE)
    if count > 0:
        print(f"Part 3 Heading Update: Replaced pattern with '{repl}' ({count} match(es)).")

with open(part3_path, 'w', encoding='utf-8') as f:
    f.write(part3_content)
