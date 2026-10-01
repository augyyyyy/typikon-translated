import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
backup_path = os.path.join(typikon_dir, "backup", "Final_Dolnytsky_part2_general_rubrics.md")
target_path = os.path.join(typikon_dir, "Final_Dolnytsky_part2_general_rubrics.md")

with open(backup_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n')

# Keep headers updated
content = content.replace(
    "# PART II\r\nGENERAL RUBRICS FOR VARIOUS SERVICES OF THE OCTOECHOS AND MENAION",
    "# PART II: GENERAL RUBRICS FOR VARIOUS SERVICES (OCTOECHOS & MENAION)"
)

# Replace book names (avoid double-formatting if already formatted)
books = ["Octoechos", "Menaion", "Horologion", "Heirmologion", "Sluzhebnik", "Anthologion", "Triodion", "Triodia", "Menology"]
for book in books:
    # Match book name not preceded by * and not followed by *
    content = re.sub(r'(?<!\*)\b' + book + r'\b(?!\*)', r'*' + book + r'*', content)

# Format common incipits in quotes
incipits = [
    ("Blessed is the man", "*“Blessed is the man”*"),
    ("Lord, I have cried", "*“Lord, I have cried”*"),
    ("God is the Lord", "*“God is the Lord”*"),
    ("It is truly meet", "*“It is truly meet”*"),
    ("Glory to Thee, O Christ God", "*“Glory to Thee, O Christ God”*"),
    ("Glory, Both now", "*“Glory, Both now”*"),
    ("The Lord is King", "*“The Lord is King”*"),
    ("Today salvation has come to the world", "*“Today salvation has come to the world”*"),
    ("Having risen from the tomb", "*“Having risen from the tomb”*"),
    ("Confirm, O God", "*“Confirm, O God”*"),
    ("More honorable", "*“More honorable”*"),
    ("Blessed is our God", "*“Blessed is our God”*"),
    ("Blessed be He", "*“Blessed be He”*"),
    ("For Thine is the kingdom", "*“For Thine is the kingdom”*"),
    ("Glory to the Holy, Consubstantial", "*“Glory to the Holy, Consubstantial...”*"),
]

for orig, formatted in incipits:
    # replace "orig" with formatted, and also format raw orig if found
    content = content.replace(f'"{orig}"', formatted)
    content = content.replace(f'\'{orig}\'', formatted)
    
# Let's clean up bullet points: "o\t" and "?\t"
# We replace o\t or ?\t with two spaces and a hyphen
content = re.sub(r'^\s*o\t', '  * ', content, flags=re.MULTILINE)
content = re.sub(r'^\s*\?\t', '  * ', content, flags=re.MULTILINE)
content = re.sub(r'^\s*o\s+', '  * ', content, flags=re.MULTILINE)
content = re.sub(r'^\s*\?\s+', '  * ', content, flags=re.MULTILINE)
content = re.sub(r'^\s*•\t', '  * ', content, flags=re.MULTILINE)

# Bold common conditionals in lists
# e.g., "* If two saints occur, then" -> "* **If two saints occur**:"
# We match "* If" or "* When" at the beginning of lines
conditionals = [
    ("If two saints occur", "If two saints occur"),
    ("If a saint on 6 occurs", "If a saint on 6 occurs"),
    ("If the saint on 6 has", "If the saint on 6 has"),
    ("If there is only one choir", "If there is only one choir"),
    ("If there are also deacons", "If there are also deacons"),
    ("If the temple is of a saint", "If the temple is of a saint"),
    ("If the temple be of a saint", "If the temple be of a saint"),
    ("If the temple is of the Lord", "If the temple is of the Lord or of the Theotokos"),
    ("If the saint be on 6", "If the saint be on 6"),
]

for orig, replacement in conditionals:
    # match optional list marker and spacing
    pattern = r'(\*\s+)' + re.escape(orig) + r'\b'
    content = re.sub(pattern, r'\1**' + replacement + r'**', content)

# Check and fix section headers to match TOC format
headers_map = [
    ("SAINT WITHOUT POLYELEOS ON A SUNDAY", "## 2.1 Saint without Polyeleos on a Sunday"),
    ("SAINT WITHOUT POLYELEOS ON WEEKDAYS (EXCEPT SATURDAY)", "## 2.2 Saint without Polyeleos on Weekdays (Except Saturday)"),
    ("SAINT WITHOUT POLYELEOS ON A SATURDAY", "## 2.3 Saint without Polyeleos on a Saturday"),
    ("SAINT WITH POLYELEOS ON A SUNDAY", "## 2.4 Saint with Polyeleos on a Sunday"),
    ("SAINT WITH POLYELEOS ON WEEKDAYS AND SATURDAY", "## 2.5 Saint with Polyeleos on Weekdays and Saturday"),
    ("SAINT WITH ALL-VIGIL ON SUNDAY", "## 2.6 Saint with All-Night Vigil on a Sunday"),
    ("SAINT WITH ALL-NIGHT VIGIL ON SUNDAY", "## 2.6 Saint with All-Night Vigil on a Sunday"),
    ("SAINT WITH All-Night Vigil ON A SUNDAY", "## 2.6 Saint with All-Night Vigil on a Sunday"),
    ("SAINT WITH ALL-NIGHT VIGIL ON WEEKDAYS AND SATURDAY", "## 2.7 Saint with All-Night Vigil on Weekdays and Saturday"),
    ("SAINT WITH All-Night Vigil ON WEEKDAYS AND ON SATURDAY", "## 2.7 Saint with All-Night Vigil on Weekdays and Saturday"),
    ("FOREFEAST WITH A SAINT WITHOUT POLYELEOS ON SUNDAY", "## 2.8 Forefeast on Sunday with a Saint without Polyeleos"),
    ("FOREFEAST WITH A SAINT WITHOUT POLYELEOS ON WEEKDAYS AND ON SATURDAY", "## 2.9 Forefeast on Weekdays and Saturday with a Saint without Polyeleos"),
    ("FEAST OF THE LORD ON A SUNDAY AND ON WEEKDAYS", "## 2.10 Feast of the Lord on Sunday and Weekdays"),
    ("FEAST OF THE THEOTOKOS ON A SUNDAY", "## 2.11 Feast of the Theotokos on Sunday"),
    ("FEAST OF THE THEOTOKOS ON WEEKDAYS", "## 2.12 Feast of the Theotokos on Weekdays"),
    ("AFTERFEAST WITH A SAINT WITHOUT POLYELEOS ON A SUNDAY", "## 2.13 Afterfeast on Sunday with a Saint without Polyeleos"),
    ("AFTERFEAST WITH A SAINT WITHOUT POLYELEOS ON WEEKDAYS AND ON SATURDAY", "## 2.14 Afterfeast on Weekdays and Saturday with a Saint without Polyeleos"),
    ("AFTERFEAST WITH A SAINT WITH POLYELEOS ON A SUNDAY", "## 2.15 Afterfeast on Sunday with a Saint with Polyeleos"),
    ("AFTERFEAST WITH A SAINT WITH POLYELEOS ON WEEKDAYS[^217]", "## 2.16 Afterfeast on Weekdays and Saturday with a Saint with Polyeleos[^217]"),
    ("AFTERFEAST WITH A SAINT WITH POLYELEOS ON WEEKDAYS AND ON SATURDAY", "## 2.16 Afterfeast on Weekdays and Saturday with a Saint with Polyeleos"),
    ("AFTERFEAST WITH A SAINT WITH All-Night Vigil ON A SUNDAY", "## 2.17 Afterfeast on Sunday with a Saint with All-Night Vigil"),
    ("AFTERFEAST WITH A SAINT WITH ALL-NIGHT VIGIL ON A SUNDAY", "## 2.17 Afterfeast on Sunday with a Saint with All-Night Vigil"),
    ("AFTERFEAST WITH A SAINT WITH All-Night Vigil ON WEEKDAYS", "## 2.18 Afterfeast on Weekdays and Saturday with a Saint with All-Night Vigil"),
    ("AFTERFEAST WITH A SAINT WITH ALL-NIGHT VIGIL ON WEEKDAYS AND ON SATURDAY", "## 2.18 Afterfeast on Weekdays and Saturday with a Saint with All-Night Vigil"),
    ("APODOSIS (APODOSIS) OF A FEAST ON A SUNDAY", "## 2.19 Apodosis of a Feast of the Lord or Theotokos on Sunday"),
    ("APODOSIS OF A FEAST OF THE LORD OR THE THEOTOKOS ON A SUNDAY", "## 2.19 Apodosis of a Feast of the Lord or Theotokos on Sunday"),
    ("APODOSIS (APODOSIS) OF A FEAST ON WEEKDAYS", "## 2.20 Apodosis of a Feast of the Lord or Theotokos on Weekdays"),
    ("APODOSIS OF A FEAST OF THE LORD OR THE THEOTOKOS ON WEEKDAYS", "## 2.20 Apodosis of a Feast of the Lord or Theotokos on Weekdays"),
]

# Sort headers_map by length of the target string in descending order to avoid substring mismatch issues
headers_map = sorted(headers_map, key=lambda x: len(x[0]), reverse=True)

for orig, formatted in headers_map:
    content = content.replace(orig, formatted)
    # also replace case variations if any
    content = re.sub(r'(?mi)^' + re.escape(orig) + r'\s*$', formatted, content)

with open(target_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Formatting of Part 2 completed.")
