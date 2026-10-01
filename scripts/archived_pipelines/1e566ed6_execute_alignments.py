import os
import shutil
import subprocess
import re

def main():
    typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
    scratch_dir = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch"
    
    # 1. Restore files from backup
    print("--- 1. RESTORING BACKUPS ---")
    files_to_restore = [
        "Final_Dolnytsky_part1_structure.md",
        "Final_Dolnytsky_part2_general_rubrics.md",
        "Final_Dolnytsky_part3_menaion.md",
        "Final_Dolnytsky_part4_triodion.md",
        "Final_Dolnytsky_part5_temple.md",
        "Final_Dolnytsky_appendix.md",
        "Final_Dolnytsky_glossary.md"
    ]
    for filename in files_to_restore:
        backup_path = os.path.join(typikon_dir, "backup", filename)
        target_path = os.path.join(typikon_dir, filename)
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, target_path)
            print(f"  Restored: {filename}")
            
    # 2. Run formatters
    print("\n--- 2. RUNNING FORMATTERS ---")
    format_scripts = [
        "faithful_format_part1.py",
        "format_part2.py",
        "format_part3.py",
        "format_part4.py",
        "format_part5.py",
        "format_appendix.py",
        "format_glossary.py"
    ]
    for script in format_scripts:
        script_path = os.path.join(scratch_dir, script)
        print(f"  Running: {script}...")
        res = subprocess.run(["python", script_path], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"    Error in {script}:\n{res.stderr}")
        else:
            print(f"    {res.stdout.strip()}")
            
    # 3. Apply manual precise heading formatting adjustments in place
    print("\n--- 3. APPLYING HEADING ADJUSTMENTS ---")
    
    # Helper for simple replacements
    def apply_replacements(filepath, replacements_dict):
        with open(filepath, 'r', encoding='utf-8', newline='') as f:
            content = f.read()
            
        content = content.replace('\r\n', '\n')
        
        changed = False
        # Sort replacement keys by length descending to prevent substring collisions (e.g. Chapter I vs Chapter II)
        sorted_keys = sorted(replacements_dict.keys(), key=len, reverse=True)
        for orig in sorted_keys:
            repl = replacements_dict[orig]
            orig_normalized = orig.replace('\r\n', '\n')
            repl_normalized = repl.replace('\r\n', '\n')
            if orig_normalized in content:
                content = content.replace(orig_normalized, repl_normalized)
                changed = True
                print(f"    Replaced in {os.path.basename(filepath)}: '{orig_normalized.splitlines()[0]}' -> '{repl_normalized.splitlines()[0]}'")
            else:
                # Try regex matching (for case insensitivity or whitespace variations)
                pattern = re.escape(orig_normalized)
                content, count = re.subn(pattern, repl_normalized, content, flags=re.IGNORECASE)
                if count > 0:
                    changed = True
                    print(f"    Regex replaced in {os.path.basename(filepath)}: '{orig_normalized.splitlines()[0]}'")
                    
        if changed:
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
                
    # Part 2
    part2_path = os.path.join(typikon_dir, "Final_Dolnytsky_part2_general_rubrics.md")
    part2_reps = {
        "Forefeast with a Saint without Polyeleos on a Sunday": "## 2.8 Forefeast with a Saint without a Polyeleos on a Sunday",
        "Forefeast with a Saint without Polyeleos on Sunday": "## 2.8 Forefeast with a Saint without a Polyeleos on a Sunday",
    }
    apply_replacements(part2_path, part2_reps)
    
    # Part 3
    part3_path = os.path.join(typikon_dir, "Final_Dolnytsky_part3_menaion.md")
    part3_reps = {
        "SATURDAY AND SUNDAY BEFORE THE EXALTATION": "### 3.1.2 Saturday and Sunday before the Exaltation",
        "SATURDAY AFTER THE EXALTATION": "### 3.1.5 Saturday after the Exaltation",
        "SUNDAY AFTER THE EXALTATION": "### 3.1.6 Sunday after the Exaltation",
        "APODOSIS OF THE FEAST OF THE EXALTATION": "### 3.1.7 Apodosis of the Feast of the Exaltation",
        "SUNDAY OF THE HOLY FOREFATHERS": "### 3.4.2 Sunday of the Holy Forefathers",
        "SUNDAY OF THE HOLY FATHERS BEFORE THE NATIVITY OF CHRIST": "### 3.4.5 Sunday of the Holy Fathers before the Nativity of Christ",
        "20-24 DECEMBER Forefeast of the Nativity of Christ": "### 3.4.6 20-24 December: Forefeast of the Nativity of Christ",
        "Saturday after the Nativity": "### 3.4.10 Saturday after the Nativity",
        "Sunday after the Nativity of Christ": "### 3.4.11 Sunday after the Nativity of Christ",
        "#### RULE ABOUT SATURDAYS AND SUNDAYS\nbetween the Nativity and Theophany": "### 3.4.12 Rule Concerning Saturdays and Sundays between the Nativity and Theophany",
        "2, 3, 4 and 5 JANUARY Forefeast of Theophany": "### 3.5.2 2, 3, 4 and 5 January: Forefeast of Theophany",
        "Eve of Theophany": "### 3.5.3 Eve of Theophany",
        "Saturday after Theophany": "### 3.5.6 Saturday after Theophany",
        "Sunday after Theophany": "### 3.5.7 Sunday after Theophany",
        "3 - 8 FEBRUARY Afterfeast of the Meeting": "### 3.6.3 3 - 8 February: Afterfeast of the Meeting",
        "### 3.12 August": "## 3.12 August",
        "### 1 AUGUST Procession of the Wood of the Precious Cross": "## 3.12 August\n\n### 3.12.1 1 August: Procession of the Wood of the Precious Cross",
    }
    apply_replacements(part3_path, part3_reps)
    
    # Part 4
    part4_path = os.path.join(typikon_dir, "Final_Dolnytsky_part4_triodion.md")
    part4_reps = {
        "# PART IV\nRUBRICS OF THE TRIODIA": "# PART IV: RUBRICS OF THE TRIODION\n\n## 4.1 Lenten Triodion",
        "SUNDAY OF THE PUBLICAN AND PHARISEE": "### 4.1.1 Sunday of the Publican and Pharisee",
        "SUNDAY OF THE PRODIGAL SON": "### 4.1.2 Sunday of the Prodigal Son",
        "MEATFARE, OR SOUL SATURDAY": "### 4.1.3 Meatfare, or Soul Saturday",
        "MEATFARE SUNDAY": "### 4.1.4 Meatfare Sunday",
        "CHEESEFARE WEEK": "### 4.1.5 Cheesefare Week",
        "CHEESEFARE SUNDAY": "### 4.1.6 Cheesefare Sunday",
        "BEGINNING OF GREAT LENT": "### 4.1.7 Beginning of Great Lent",
        "VESPERS ON WEDNESDAY AND FRIDAY WITH PRESANCTIFIED": "### 4.1.8 Vespers on Wednesday and Friday with Presanctified",
        "FIRST SATURDAY OF GREAT LENT": "### 4.1.9 First Saturday of Great Lent",
        "FIRST SUNDAY OF GREAT LENT": "### 4.1.10 First Sunday of Great Lent",
        "OF THE SECOND WEEK OF GREAT LENT": "### 4.1.11 Monday, Tuesday, Wednesday, Thursday and Friday of the Second Week of Great Lent",
        "SATURDAY OF THE SECOND WEEK OF GREAT LENT": "### 4.1.12 Saturday of the Second Week of Great Lent",
        "SECOND SUNDAY OF GREAT LENT": "### 4.1.13 Second Sunday of Great Lent",
        "THIRD WEEK OF GREAT LENT": "### 4.1.14 Third Week of Great Lent",
        "FOURTH SATURDAY OF GREAT LENT": "### 4.1.15 Fourth Saturday of Great Lent",
        "FOURTH SUNDAY OF GREAT LENT": "### 4.1.16 Fourth Sunday of Great Lent",
        "MONDAY, TUESDAY, WEDNESDAY AND FRIDAY OF THE FIFTH WEEK OF GREAT LENT": "### 4.1.17 Monday, Tuesday, Wednesday and Friday of the Fifth Week of Great Lent",
        "FIFTH SUNDAY OF GREAT LENT": "### 4.1.18 Fifth Sunday of Great Lent",
        "OF THE SIXTH WEEK OF GREAT LENT": "### 4.1.19 Monday, Tuesday, Wednesday, Thursday and Friday of the Sixth Week of Great Lent",
        "FLOWER TRIODION": "## 4.2 Flower Triodion (Pentecostarion)",
        "SIXTH SATURDAY OF GREAT LENT - OF LAZARUS": "### 4.2.1 Lazarus Saturday",
        "FLOWER SUNDAY": "### 4.2.2 Flower Sunday (Palm Sunday)",
        "GREAT MONDAY, TUESDAY AND WEDNESDAY": "### 4.2.3 Great Monday, Tuesday and Wednesday",
        "GREAT THURSDAY": "### 4.2.4 Great Thursday",
        "GREAT FRIDAY": "### 4.2.5 Great Friday",
        "MATINS OF GREAT SATURDAY": "### 4.2.6 Matins of Great Saturday",
        "Beginning of Holy Pentecost": "### 4.2.7 Beginning of Holy Pentecost",
        "RESURRECTION MATINS": "### 4.2.8 Resurrection Matins",
        "ON THE DAY OF RESURRECTION IN THE EVENING": "### 4.2.9 On the Day of Resurrection in the Evening",
        "GENERAL RUBRIC FOR ALL DAYS OF BRIGHT WEEK": "### 4.2.10 General Rubric for All Days of Bright Week",
        "SUNDAY OF AP. THOMAS": "### 4.2.11 Sunday of the Apostle Thomas",
        "SUNDAY OF THE MYRRH-BEARERS": "### 4.2.12 Sunday of the Myrrh-Bearing Women",
        "SUNDAY OF THE PARALYTIC": "### 4.2.13 Sunday of the Paralytic",
        "MID-PENTECOST": "### 4.2.14 Mid-Pentecost",
        "SUNDAY OF THE SAMARITAN WOMAN": "### 4.2.15 Sunday of the Samaritan Woman",
        "SUNDAY OF THE BLIND MAN": "### 4.2.16 Sunday of the Man Born Blind",
        "ASCENSION OF THE LORD": "### 4.2.17 Ascension of the Lord",
        "SUNDAY OF THE HOLY FATHERS OF THE FIRST NICAEAN COUNCIL": "### 4.2.18 Sunday of the Holy Fathers of the First Nicaean Council",
        "SUNDAY OF PENTECOST": "### 4.2.19 Sunday of Pentecost",
        "MONDAY OF THE HOLY SPIRIT": "### 4.2.20 Monday of the Holy Spirit",
        "SUNDAY OF ALL SAINTS": "### 4.2.21 Sunday of All Saints",
        "BEGINNING OF THE FAST OF THE SAINTS\nCHIEF APOSTLES PETER AND PAUL": "### 4.2.22 Beginning of the Fast of the Saints Chief Apostles Peter and Paul",
        "FEAST OF THE MOST HOLY EUCHARIST": "### 4.2.23 Feast of the Most Holy Eucharist",
        "FEAST OF THE CO-SUFFERING OF THE MOST HOLY THEOTOKOS": "### 4.2.24 Feast of the Co-suffering of the Most Holy Theotokos",
    }
    apply_replacements(part4_path, part4_reps)
    
    # Part 5
    part5_path = os.path.join(typikon_dir, "Final_Dolnytsky_part5_temple.md")
    part5_reps = {
        "## Chapter I": "## 5.1 Chapter I",
        "##### 1. ABOUT THE EXPOSITION OF THE HOLY MYSTERIES ON THE HOLY TABLE": "### 5.1.1 Concerning the Exposition of the Holy Mysteries on the Altar",
        "##### 2. ABOUT THE PROCESSION WITH THE HOLY MYSTERIES": "### 5.1.2 Concerning Processions with the Holy Mysteries",
        "## Chapter II\nTEMPLE RUBRICS,": "## 5.2 Chapter II: Temple Rubrics",
        "##### 1. GENERAL RUBRICS": "### 5.2.1 General Rubrics",
        "##### 2. SPECIFIC TEMPLE RUBRICS[^669]": "### 5.2.2 Specific Temple Rubrics[^669]",
        "#### RULE OF SERVICES OF THE WHOLE YEAR": "## 5.3 Rule of Services for the Whole Year",
        "### RULE OF MOVABLE SERVICES": "## 5.4 Rule of Moveable Services",
        "ABOUT THE HOLY DOORS AND THE CURTAIN OF THE ICONOSTASIS": "## 5.5 Rubrics Concerning the Holy Doors and Curtain of the Iconostasis",
    }
    apply_replacements(part5_path, part5_reps)
    
    # Appendix
    appendix_path = os.path.join(typikon_dir, "Final_Dolnytsky_appendix.md")
    appendix_reps = {
        "## Appendix": "## 6.1 Appendix (Rubrics of the Divine Services)",
        "V. Rubric of the Divine Liturgy": "### 6.1.1 V. Rubrics of the Divine Liturgy of St. John Chrysostom & St. Basil",
        "VI. Rubric of the Liturgy of Presanctified Gifts": "### 6.1.2 VI. Rubrics of the Liturgy of the Presanctified Gifts",
    }
    apply_replacements(appendix_path, appendix_reps)
    
    # Glossary
    glossary_path = os.path.join(typikon_dir, "Final_Dolnytsky_glossary.md")
    glossary_reps = {
        "# Dolnytsky Typikon — Liturgical Terminology & Commentary Appendix": "# 6.3 Glossary and Liturgical Terminology Commentary",
        "(#dismissals-feast-vs.-day-commemorations)": "(#dismissals-feast-vs-day-commemorations)",
        "(#feast-of-st.-catherine-transfer-of-feasts)": "(#feast-of-st-catherine-transfer-of-feasts)",
        "(#feasts-of-saints-service-of-st.-anne)": "(#feasts-of-saints-service-of-st-anne)",
        "(#feasts-of-saints-st.-peter-and-paul-stichera)": "(#feasts-of-saints-st-peter-and-paul-stichera)",
        "(#holy-doors-vs.-royal-doors-historical-usage-and-rubrics)": "(#holy-doors-vs-royal-doors-historical-usage-rubrics)",
        "(#holy-doors-vs.-royal-doors-terminology)": "(#holy-doors-vs-royal-doors-terminology)",
        "(#holy-liturgy-concelebration-and-repetition)": "(#holy-liturgy-concelebration-repetition)",
        "(#litanies-at-the-liturgical-hours-greek-vs.-slavic)": "(#litanies-at-the-liturgical-hours-greek-vs-slavic)",
        "(#liturgical-commemorations-moscow-typikon-vs.-marks-chapters)": "(#liturgical-commemorations-moscow-typikon-vs-marks-chapters)",
        "(#liturgical-readings-for-forefathers-and-saints)": "(#liturgical-readings-for-forefathers-saints)",
        "(#trisagion-vs.-as-many-as-have-been-baptized-into-christ)": "(#trisagion-vs-as-many-as-have-been-baptized-into-christ)",
        "(#weekday-liturgy-commemorations-greek-vs.-slavonic)": "(#weekday-liturgy-commemorations-greek-vs-slavonic)",
    }
    apply_replacements(glossary_path, glossary_reps)
    
    # 4. Run heading alignment script
    print("\n--- 4. ALIGNING REMAINING HEADINGS ---")
    align_script = os.path.join(scratch_dir, "align_all_headings.py")
    res = subprocess.run(["python", align_script], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  Error in align_all_headings.py:\n{res.stderr}")
    else:
        print(f"  {res.stdout.strip()}")
        
    # 5. Compile Master Document
    print("\n--- 5. COMPILED MASTER DOCUMENT ---")
    build_script = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\build_master_document.py"
    res = subprocess.run(["python", build_script], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  Error compiling master document:\n{res.stderr}")
    else:
        print(f"  {res.stdout.strip()}")
        
    # 6. Verify Links
    print("\n--- 6. VERIFYING LINKS ---")
    verify_script = os.path.join(scratch_dir, "verify_links.py")
    res = subprocess.run(["python", verify_script], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  Error verifying links:\n{res.stderr}")
    else:
        print(f"  {res.stdout.strip()}")

if __name__ == "__main__":
    main()
