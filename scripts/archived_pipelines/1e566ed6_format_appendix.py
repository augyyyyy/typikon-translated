import os
import re

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
backup_path = os.path.join(typikon_dir, "backup", "Final_Dolnytsky_appendix.md")
target_path = os.path.join(typikon_dir, "Final_Dolnytsky_appendix.md")

with open(backup_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n')

# Replace book names
books = ["Octoechos", "Menaion", "Horologion", "Heirmologion", "Sluzhebnik", "Anthologion", "Triodion", "Triodia", "Menology", "Liturgicon"]
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

# Smart Dialogue formatting using Regex
dialogue_pattern = r'\b(1st\s+[dD]eacon|2nd\s+[dD]eacon|first\s+[dD]eacon|second\s+[dD]eacon|right\s+[dD]eacon|left\s+[dD]eacon|[dD]eacon|[pP]riest|[cC]hoir|[rR]eader|[bB]ishop)\s*:\s*\"([^\"]+)\"'

def repl(match):
    speaker = match.group(1).strip()
    text = match.group(2).strip()
    
    # Normalize speaker role
    role = "Priest"
    if "deacon" in speaker.lower():
        if "1st" in speaker.lower() or "first" in speaker.lower():
            role = "First Deacon"
        elif "2nd" in speaker.lower() or "second" in speaker.lower():
            role = "Second Deacon"
        elif "right" in speaker.lower():
            role = "Right Deacon"
        elif "left" in speaker.lower():
            role = "Left Deacon"
        else:
            role = "Deacon"
    elif "choir" in speaker.lower():
        role = "Choir"
    elif "reader" in speaker.lower():
        role = "Reader"
    elif "bishop" in speaker.lower():
        role = "Bishop"
        
    # We return the blockquoted version
    return f'\r\n> **{role}**: "{text}"\r\n'

content = re.sub(dialogue_pattern, repl, content)

with open(target_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Formatting of Appendix completed.")
