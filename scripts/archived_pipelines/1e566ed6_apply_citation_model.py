import os
import re
import sys
import io

# Enforce UTF-8 stdout configuration for Windows environment
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
files = [
    "Final_Dolnytsky_part1_structure.md",
    "Final_Dolnytsky_part2_general_rubrics.md",
    "Final_Dolnytsky_part3_menaion.md",
    "Final_Dolnytsky_part4_triodion.md",
    "Final_Dolnytsky_part5_temple.md",
    "Final_Dolnytsky_appendix.md"
]

def slugify(text):
    # Standard Markdown header slugification
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9\s\-]', '', slug)
    slug = slug.replace(' ', '-')
    slug = re.sub(r'-+', '-', slug) # reduce multiple hyphens
    return slug.strip('-')

def parse_header_number(title):
    # Extracts numbers like "1.1", "1.2.1" from heading start
    m = re.match(r'^(\d+(?:\.\d+)*)\b', title.strip())
    if m:
        return [int(x) for x in m.group(1).split('.')]
    return None

def clean_title(title):
    cleaned = title.strip()
    # Remove leading numbering like "1.1 ", "1. ", "1.\t", "V. "
    cleaned = re.sub(r'^(\d+(?:\.\d+)*[\.\t\s]*)+', '', cleaned)
    # Remove roman numerals like "I. ", "V. "
    cleaned = re.sub(r'^[IVXLCDM]+\.[\t\s]*', '', cleaned)
    # Remove leading tabs/bullets
    cleaned = cleaned.strip(" \t.*")
    return cleaned

def do_manual_restructurings():
    print("Performing manual restructurings...")
    
    # 1. Part 1 Structure: Daily Matins split
    part1_path = os.path.join(typikon_dir, "Final_Dolnytsky_part1_structure.md")
    if os.path.exists(part1_path):
        with open(part1_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        old_matins_block = """### 1.5.3 Order of Daily Matins
*From the beginning of Matins to the second Sessional Hymn inclusive everything happens just as at Great Matins without Vigil, with the exception of the censing at the beginning, which is prescribed in the Typikon, however, according to our custom of many years, is not practiced*[^40]*.* *After the second (or even the third)*[^41]* Sessional Hymn the 50th Psalm is taken and immediately the Canon just as given at Great Matins, except for the Katavasia, which will not be the current one, nor after every ode, but only after the 3rd, 6th, 8th and 9th - the heirmos of the last canon. At its 9th Ode, that is at 'My soul magnifies,' the Priest censes just as at Great Matins. After the Canon - 'It is truly meet'; after the Exaposteilarion - the Psalms of the Praises, simply, without singing and without the addition to the first two verses of the words: 'Let everything that hath breath' and 'To Thee belongs'; after Glory, Both now usually the Small Doxology is read, before which the Priest, having exited to the front of the Holy Doors says in the Forty Days: "To Thee belongs glory" and exclaims:*
> **Priest**: "Glory to Thee Who Hast shown us the light."

*Outside the Forty Days, he does not say 'To Thee belongs glory,' but immediately exclaims:*
> **Priest**: "Glory to Thee Who Hast shown us the light."

*...and then the choirs read the Doxology. The Priest stands there until the end of the litany 'Let us complete,' which follows after the Doxology, at it he also gives the peace, as at Vespers. After 'Let us complete' the Priest withdraws to his place, having bowed low. The Aposticha is sung, and after it - 'It is a good thing,' Trisagion and the rest with 'Our Father.' After this the Priest exclaims, standing at his place:*
> **Priest**: "For Thine is the kingdom."

*...also the troparion of the Saint is sung and Glory, Both now: the Dismissal Theotokion, according to the tone of the troparion of the Saint and according to the day of the week. In the Fore- and Afterfeast the Theotokion is not taken, but instead of it the troparion of the Feast is sung*[^42]*.* *When this troparion ends, the Priest comes out to the front of the Holy Doors and sings the litany 'Have mercy on us, O God' and after its exclamation says:*
> **Priest**: "Wisdom!"

*...the Choir responds:*
> **Choir**: "Bless."

*...the Priest sings:*
> **Priest**: "Blessed and pre-glorified Christ our God always, now and ever, and unto ages of ages."

*...choir: 'Amen' and immediately: 'Come, let us worship' with small bows. The Priest after the last low bow withdraws to his place and the 1st Hour begins.*"""

        new_matins_block = """### 1.5.3 Order of Daily Matins

##### From the Beginning to the Canon
*From the beginning of Matins to the second Sessional Hymn inclusive everything happens just as at Great Matins without Vigil, with the exception of the censing at the beginning, which is prescribed in the Typikon, however, according to our custom of many years, is not practiced*[^40]*.* *After the second (or even the third)*[^41]* Sessional Hymn the 50th Psalm is taken and immediately the Canon just as given at Great Matins, except for the Katavasia, which will not be the current one, nor after every ode, but only after the 3rd, 6th, 8th and 9th - the heirmos of the last canon. At its 9th Ode, that is at 'My soul magnifies,' the Priest censes just as at Great Matins. After the Canon - 'It is truly meet'; after the Exaposteilarion - the Psalms of the Praises, simply, without singing and without the addition to the first two verses of the words: 'Let everything that hath breath' and 'To Thee belongs'; after Glory, Both now usually the Small Doxology is read, before which the Priest, having exited to the front of the Holy Doors says in the Forty Days: "To Thee belongs glory" and exclaims:*
> **Priest**: "Glory to Thee Who Hast shown us the light."

##### Outside the Forty Days
*Outside the Forty Days, he does not say 'To Thee belongs glory,' but immediately exclaims:*
> **Priest**: "Glory to Thee Who Hast shown us the light."

##### The Doxology and Aposticha
*...and then the choirs read the Doxology. The Priest stands there until the end of the litany 'Let us complete,' which follows after the Doxology, at it he also gives the peace, as at Vespers. After 'Let us complete' the Priest withdraws to his place, having bowed low. The Aposticha is sung, and after it - 'It is a good thing,' Trisagion and the rest with 'Our Father.' After this the Priest exclaims, standing at his place:*
> **Priest**: "For Thine is the kingdom."

##### Troparia and Litany
*...also the troparion of the Saint is sung and Glory, Both now: the Dismissal Theotokion, according to the tone of the troparion of the Saint and according to the day of the week. In the Fore- and Afterfeast the Theotokion is not taken, but instead of it the troparion of the Feast is sung*[^42]*.* *When this troparion ends, the Priest comes out to the front of the Holy Doors and sings the litany 'Have mercy on us, O God' and after its exclamation says:*
> **Priest**: "Wisdom!"

##### Choir Response
*...the Choir responds:*
> **Choir**: "Bless."

##### Blessing
*...the Priest sings:*
> **Priest**: "Blessed and pre-glorified Christ our God always, now and ever, and unto ages of ages."

##### Dismissal and First Hour
*...choir: 'Amen' and immediately: 'Come, let us worship' with small bows. The Priest after the last low bow withdraws to his place and the 1st Hour begins.*"""
        
        # Replace block cleanly using normalized line endings
        content_norm = content.replace('\r\n', '\n')
        old_matins_norm = old_matins_block.replace('\r\n', '\n')
        new_matins_norm = new_matins_block.replace('\r\n', '\n')
        
        if old_matins_norm in content_norm:
            content_norm = content_norm.replace(old_matins_norm, new_matins_norm)
            with open(part1_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content_norm)
            print("  Successfully split Daily Matins in Part 1 Structure.")
        else:
            print("  Warning: Daily Matins block not found for splitting.")

    # 2. Part 3 Menaion: Exaltation uppercase headers
    part3_path = os.path.join(typikon_dir, "Final_Dolnytsky_part3_menaion.md")
    if os.path.exists(part3_path):
        with open(part3_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content_norm = content.replace('\r\n', '\n')
        
        replaces = [
            ("PREPARATION OF THE PRECIOUS CROSS", "#### Preparation of the Precious Cross"),
            ("BRINGING OUT OF THE PRECIOUS CROSS FROM THE SACRISTY\n\nTO THE MENA", "#### Bringing Out of the Precious Cross from the Sacristy to the Mensa"),
            ("TRANSFER OF THE PRECIOUS CROSS\nFROM THE MENA TO THE TETRAPOD.", "#### Transfer of the Precious Cross from the Mensa to the Tetrapod"),
            ("EXALTATION OF THE PRECIOUS CROSS AND VENERATION OF IT", "#### Exaltation of the Precious Cross and Veneration of It"),
            ("RETURN OF THE PRECIOUS CROSS FROM THE TETRAPOD", "#### Return of the Precious Cross from the Tetrapod")
        ]
        
        made_any = False
        for old, new in replaces:
            old_norm = old.replace('\r\n', '\n')
            if old_norm in content_norm:
                content_norm = content_norm.replace(old_norm, new)
                made_any = True
                print(f"  Replaced '{old_norm.replace('\n', ' ')}' with '{new}'")
        
        if made_any:
            with open(part3_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content_norm)
            print("  Successfully updated Exaltation headings in Part 3.")

    # 3. Part 2 General Rubrics: summary list cleaning
    part2_path = os.path.join(typikon_dir, "Final_Dolnytsky_part2_general_rubrics.md")
    if os.path.exists(part2_path):
        with open(part2_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content_norm = content.replace('\r\n', '\n')
        # We want to strip ##### from the summary list in the first 35 lines
        lines = content_norm.split('\n')
        for i in range(min(40, len(lines))):
            if lines[i].strip().startswith("#####") and ("Saint without" in lines[i] or "Forefeast on" in lines[i] or "Feast of the" in lines[i] or "Afterfeast on" in lines[i] or "Apodosis of" in lines[i]):
                # Remove ##### and replace with plain number/bullet
                lines[i] = re.sub(r'^#####\s*', '', lines[i])
                print(f"  Cleaned summary list line: {lines[i]}")
                
        with open(part2_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines))
        print("  Successfully cleaned summary list in Part 2.")

    # 4. Appendix: Promoted headers and sub-headings
    appendix_path = os.path.join(typikon_dir, "Final_Dolnytsky_appendix.md")
    if os.path.exists(appendix_path):
        with open(appendix_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content_norm = content.replace('\r\n', '\n')
        
        # Exact replacements for Roman numerals and sub-headings to enforce correct level
        replaces = [
            ("## I. Introductory Remarks", "### I. Introductory Remarks"),
            ("II. Rubric of Vespers without Vigil", "### II. Rubric of Vespers without Vigil"),
            ("III. Rubric of Vespers with Vigil", "### III. Rubric of Vespers with Vigil"),
            ("IV. Rubric of Matins in Sundays and Feasts", "### IV. Rubric of Matins in Sundays and Feasts"),
            ("### 6.1.1 V. Rubrics of the Divine Liturgy of St. John Chrysostom & St. Basil", "### V. Rubrics of the Divine Liturgy of St. John Chrysostom & St. Basil"),
            ("### 6.1.2 VI. Rubrics of the Liturgy of the Presanctified Gifts", "### VI. Rubrics of the Liturgy of the Presanctified Gifts"),
            
            ("##### 1. The Sanctuary and the Holy Table", "#### 1. The Sanctuary and the Holy Table"),
            ("##### 2. General Rules", "#### 2. General Rules"),
            
            ("##### 1. In Concelebration of One Deacon", "#### 1. In Concelebration of One Deacon"),
            ("##### 2. In Concelebration of Two Deacons", "#### 2. In Concelebration of Two Deacons"),
            ("##### 3. Without a Deacon", "#### 3. Without a Deacon"),
            ("##### 4. In Concelebration of Priests", "#### 4. In Concelebration of Priests"),
            ("Shortening of Matins[^767]", "#### Shortening of Matins[^767]"),
            ("Beginning of Paschal Matins", "#### Beginning of Paschal Matins"),
            
            ("##### 4. Rubric of the Non-Solemn Divine Liturgy, that is, served ordinarily", "#### 4. Rubric of the Non-Solemn Divine Liturgy, that is, served ordinarily"),
            ("##### 5. With Concelebrants", "#### 5. With Concelebrants")
        ]
        
        made_any = False
        for old, new in replaces:
            if old in content_norm:
                content_norm = content_norm.replace(old, new)
                made_any = True
                print(f"  Replaced Appendix: '{old}' -> '{new}'")
        
        if made_any:
            with open(appendix_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content_norm)
            print("  Successfully updated Appendix headings.")

def apply_numbering():
    print("\nApplying sequential path-qualified numbering to all headings...")
    
    global_mappings = {} # old_slug -> new_slug
    
    # Store files content to rewrite later
    files_rewritten = {}
    
    for filename in files:
        path = os.path.join(typikon_dir, filename)
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content_norm = content.replace('\r\n', '\n')
        lines = content_norm.split('\n')
        
        h1_val = None
        h2_val = None
        h3_val = None
        h4_val = 0
        h5_val = 0
        
        if "part1" in filename:
            h1_val = 1
        elif "part2" in filename:
            h1_val = 2
        elif "part3" in filename:
            h1_val = 3
        elif "part4" in filename:
            h1_val = 4
        elif "part5" in filename:
            h1_val = 5
        elif "appendix" in filename:
            h1_val = 6
            
        new_lines = []
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped.startswith("#"):
                new_lines.append(line)
                continue
                
            level = len(line_stripped) - len(line_stripped.lstrip('#'))
            title = line_stripped.lstrip('#').strip()
            
            existing_nums = parse_header_number(title)
            
            old_slug = slugify(line_stripped)
            
            if level == 1:
                # Part definitions
                if "PART I" in title.upper():
                    h1_val = 1
                elif "PART II" in title.upper():
                    h1_val = 2
                elif "PART III" in title.upper():
                    h1_val = 3
                elif "PART IV" in title.upper():
                    h1_val = 4
                elif "PART V" in title.upper():
                    h1_val = 5
                elif "APPENDIX" in title.upper():
                    h1_val = 6
                h2_val = None
                h3_val = None
                h4_val = 0
                h5_val = 0
                new_line = line_stripped
                
            elif level == 2:
                if existing_nums:
                    if len(existing_nums) >= 2:
                        h1_val, h2_val = existing_nums[0], existing_nums[1]
                    else:
                        h2_val = existing_nums[0]
                else:
                    if h2_val is None:
                        h2_val = 1
                    else:
                        h2_val += 1
                h3_val = None
                h4_val = 0
                h5_val = 0
                
                clean_t = clean_title(title)
                new_line = f"## {h1_val}.{h2_val} {clean_t}"
                
            elif level == 3:
                if existing_nums:
                    if len(existing_nums) >= 3:
                        h1_val, h2_val, h3_val = existing_nums[0], existing_nums[1], existing_nums[2]
                    elif len(existing_nums) == 2:
                        h2_val, h3_val = existing_nums[0], existing_nums[1]
                    else:
                        h3_val = existing_nums[0]
                else:
                    if h3_val is None:
                        h3_val = 1
                    else:
                        h3_val += 1
                h4_val = 0
                h5_val = 0
                
                clean_t = clean_title(title)
                new_line = f"### {h1_val}.{h2_val}.{h3_val} {clean_t}"
                
            elif level == 4:
                h4_val += 1
                h5_val = 0
                
                clean_t = clean_title(title)
                if h3_val is not None:
                    parent_prefix = f"{h1_val}.{h2_val}.{h3_val}"
                else:
                    parent_prefix = f"{h1_val}.{h2_val}"
                new_line = f"#### {parent_prefix}.{h4_val} {clean_t}"
                
            elif level == 5:
                h5_val += 1
                
                clean_t = clean_title(title)
                if h4_val > 0:
                    if h3_val is not None:
                        parent_prefix = f"{h1_val}.{h2_val}.{h3_val}.{h4_val}"
                    else:
                        parent_prefix = f"{h1_val}.{h2_val}.{h4_val}"
                elif h3_val is not None:
                    parent_prefix = f"{h1_val}.{h2_val}.{h3_val}"
                else:
                    parent_prefix = f"{h1_val}.{h2_val}"
                    
                new_line = f"##### {parent_prefix}.{h5_val} {clean_t}"
                
            else:
                new_line = line_stripped
                
            new_slug = slugify(new_line)
            if old_slug and new_slug:
                global_mappings[old_slug] = new_slug
                
            new_lines.append(new_line)
            
        files_rewritten[filename] = new_lines
        
    return files_rewritten, global_mappings

def update_links(files_rewritten, global_mappings):
    print("\nUpdating internal anchor links across all files...")
    
    # We also need to scan and update the Intro file (since it has the Table of Contents)
    intro_path = os.path.join(typikon_dir, "Final_Dolnytsky_intro.md")
    intro_lines = []
    if os.path.exists(intro_path):
        with open(intro_path, 'r', encoding='utf-8') as f:
            intro_content = f.read()
        intro_lines = intro_content.replace('\r\n', '\n').split('\n')
        
    def replace_line_links(line):
        # Match markdown links [Text](#anchor)
        def repl(match):
            text = match.group(1)
            anchor = match.group(2)
            if anchor in global_mappings:
                return f"[{text}](#{global_mappings[anchor]})"
            return match.group(0)
        return re.sub(r'\[([^\]]+)\]\(#([^\)]+)\)', repl, line)
        
    # Update Intro
    updated_intro_lines = [replace_line_links(l) for l in intro_lines]
    if intro_lines:
        with open(intro_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(updated_intro_lines))
        print("  Updated links in Final_Dolnytsky_intro.md")
        
    # Update the rest of the rewritten files
    for filename, lines in files_rewritten.items():
        updated_lines = [replace_line_links(l) for l in lines]
        path = os.path.join(typikon_dir, filename)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(updated_lines))
        print(f"  Updated links and wrote changes to {filename}")

if __name__ == "__main__":
    do_manual_restructurings()
    files_rewritten, global_mappings = apply_numbering()
    update_links(files_rewritten, global_mappings)
    print("\nAll done!")
