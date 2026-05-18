#!/usr/bin/env python3
"""
Phase 1 v3: AI-Derived Manual Marker Placement
================================================
Handles the 63 markers that v2's fuzzy matching couldn't place.
These are placed based on semantic analysis of the RAW context and
the corresponding text in the English Broken files.

Categories of failures:
1. Parts 2-3: "his Theotokion" / ambiguous short snippets (14 markers)
2. Part 4: Section headers ("Of Orthodoxy", "FLOWER SUNDAY", "GREAT THURSDAY") (3 markers) 
3. Part 5 Menologion: Text reformatted to markdown bullets (35 markers)
4. Part 5 Rubrics: Liturgical rubric section (13 markers)
"""

import re
import json
from pathlib import Path

BASE_DIR = Path(r"e:\Google Antigravity\Projects\Translation")
SCRATCH_DIR = BASE_DIR / "scratch"
EN_DIR = BASE_DIR / "English Broken"
REPORT_DIR = SCRATCH_DIR / "reports"

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

def insert_marker_after(text, search_text, marker, occurrence=1):
    """Insert ^[N] marker right after the Nth occurrence of search_text."""
    pos = 0
    for i in range(occurrence):
        idx = text.find(search_text, pos)
        if idx == -1:
            return text, False
        pos = idx + len(search_text)
    return text[:pos] + marker + text[pos:], True

def insert_marker_at_regex(text, pattern, marker, group_end=0, occurrence=1):
    """Insert marker right after a regex match."""
    count = 0
    for m in re.finditer(pattern, text):
        count += 1
        if count == occurrence:
            pos = m.end(group_end)
            return text[:pos] + marker + text[pos:], True
    return text, False

# =============================================================================
# PART 2: General Rubrics (6 failures)
# =============================================================================

def fix_part2(text):
    """Fix 6 failed markers in Part 2.
    
    Fn 60, 82, 83, 122, 147: all end with "his Theotokion" or "its Theotokion"
    - these appear multiple times in text, need specific context to disambiguate
    Fn 131: "6 stichera^[130] or 8" - needs the already-placed ^[130] as anchor
    """
    results = []
    
    # Fn 60: "Both now: his theotokion^[60]. After the 6th Ode – Kontakion and Ikos"
    # Context: In the section about "Saint without Polyeleos on a Sunday"
    # RAW: "**Both now:** his theotokion^[60]. After the 6th Ode"
    # Occurs after "3rd Ode – Sessional Hymn... Both now: his Theotokion"
    # in the first case (Case 1: Saint without Polyeleos on Sunday)
    pattern = r'(3rd Ode\s*[-–]\s*Sessional Hymn[^.]*?Both now:\s*his [Tt]heotokion)'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        pos = m.end()
        text = text[:pos] + '^[60]' + text[pos:]
        results.append(('60', True))
    else:
        results.append(('60', False))
    
    # Fn 82: Part 2, Case 5 "Saint with Polyeleos on Weekdays and Saturday" 
    # Context: "3rd Ode – Sessional Hymn of the second saint, Both now: his Theotokion^[82]"
    # This is in the "Matins" section of Case 5
    # Search for the distinctive "Sessional Hymn of the second saint" pattern
    pattern = r'(Sessional Hymn of the second saint[^.]*?Both now:\s*his [Tt]heotokion)'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        pos = m.end()
        text = text[:pos] + '^[82]' + text[pos:]
        results.append(('82', True))
    else:
        results.append(('82', False))
    
    # Fn 83: Also "Both now: his Theotokion" but in a different case
    # Context: "Glory: of the second, if he has one, Both now: his Theotokion^[83]."
    pattern = r'(if he has one[^.]*?Both now:\s*his [Tt]heotokion)'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        pos = m.end()
        text = text[:pos] + '^[83]' + text[pos:]
        results.append(('83', True))
    else:
        results.append(('83', False))
    
    # Fn 122: "3rd Sessional Hymn of the saint, Both now: his Theotokion^[122]"
    # Context: In section about Polyeleos saint with Vigil
    pattern = r'(3rd Sessional Hymn of the saint[^.]*?Both now:\s*his [Tt]heotokion)'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        pos = m.end()
        text = text[:pos] + '^[122]' + text[pos:]
        results.append(('122', True))
    else:
        results.append(('122', False))
    
    # Fn 131: "6 stichera^[130] or 8^[131]"
    # Since ^[130] was already placed by v2, search for it
    pattern = r'(\^\[130\]\s*or\s*8)'
    m = re.search(pattern, text)
    if m:
        pos = m.end()
        text = text[:pos] + '^[131]' + text[pos:]
        results.append(('131', True))
    else:
        results.append(('131', False))
    
    # Fn 147: "which is called the Polyeleos one, Both now: its Theotokion^[147]."
    pattern = r'(which is called the Polyeleos one[^.]*?Both now:\s*its [Tt]heotokion)'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        pos = m.end()
        text = text[:pos] + '^[147]' + text[pos:]
        results.append(('147', True))
    else:
        results.append(('147', False))
    
    return text, results


# =============================================================================
# PART 3: Menaion (5 failures)
# =============================================================================

def fix_part3(text):
    """Fix 5 failed markers in Part 3.
    
    339: "Pochaiv Trefologion of 1777"
    346: "Title XII, part 4, a.c.)" 
    381: "3. Entrance^[381]" - very short context
    410, 420: "Without canon^[N]" - duplicate phrase, need ordering
    """
    results = []
    
    # Fn 339: "Trefologion of 1777" - the EN may have "Trephologion"
    pattern = r'(Tr[e]?[ph]*ologion of 1777)'
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        pos = m.end()
        text = text[:pos] + '^[339]' + text[pos:]
        results.append(('339', True))
    else:
        results.append(('339', False))
    
    # Fn 346: "Title XII, part 4, a.c.)" or "Tit. XII, part 4"
    pattern = r'(Tit(?:le)?\.?\s*XII[^)]*a\.c\.\))'
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        pos = m.end()
        text = text[:pos] + '^[346]' + text[pos:]
        results.append(('346', True))
    else:
        results.append(('346', False))
    
    # Fn 381: "3. Entrance^[381]" - after the word "Entrance" in a numbered list
    # RAW context after: "Prokeimenon of the day from the Horologion"
    # Search: "Entrance" near "Prokeimenon of the day"
    pattern = r'(3\.\s*Entrance)'
    matches = list(re.finditer(pattern, text))
    # Find the one followed by "Prokeimenon"
    placed = False
    for m in matches:
        following = text[m.end():m.end()+60]
        if 'Prok' in following or 'prok' in following:
            pos = m.end()
            text = text[:pos] + '^[381]' + text[pos:]
            placed = True
            break
    results.append(('381', placed))
    
    # Fn 410: "Without canon^[410]" - first occurrence
    # Context after: "and without prostrations"
    pattern = r'(Without canon)'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    placed = False
    for m in matches:
        following = text[m.end():m.end()+60]
        if 'prostration' in following.lower() and '^[410]' not in text[m.start():m.end()+5]:
            pos = m.end()
            text = text[:pos] + '^[410]' + text[pos:]
            placed = True
            break
    results.append(('410', placed))
    
    # Fn 420: "Without canon^[420]" - second occurrence (after 410 has been placed)
    pattern = r'(?<!\[\d\d\d\])(Without canon)(?!\^)'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    placed = False
    for m in matches:
        following = text[m.end():m.end()+60]
        if 'prostration' in following.lower():
            pos = m.end()
            text = text[:pos] + '^[420]' + text[pos:]
            placed = True
            break
    results.append(('420', placed))
    
    return text, results


# =============================================================================
# PART 4: Triodion (3 failures)
# =============================================================================

def fix_part4(text):
    """Fix 3 failed markers in Part 4.
    
    542: "Of Orthodoxy^[542]" - section header
    562: "FLOWER SUNDAY^[562]" - section header  
    576: "GREAT THURSDAY^[576]" - section header
    """
    results = []
    
    # These are section headers - place marker after the header text
    for fn, search in [
        ('542', 'Orthodoxy'),
        ('562', r'(?:FLOWER|PALM)\s*SUNDAY'),
        ('576', 'GREAT THURSDAY'),
    ]:
        marker = f'^[{fn}]'
        if marker in text:
            results.append((fn, True))
            continue
        
        if fn == '542':
            # "Of Orthodoxy" might be "Orthodoxy" in various formats
            pattern = r'(Orthodoxy[:\s]*(?:\*\*)?)'
            m = re.search(pattern, text)
            if m:
                pos = m.end()
                text = text[:pos] + marker + text[pos:]
                results.append((fn, True))
            else:
                results.append((fn, False))
        elif fn == '562':
            pattern = r'((?:FLOWER|PALM)\s+SUNDAY[:\s]*(?:\*\*)?)'
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                pos = m.end()
                text = text[:pos] + marker + text[pos:]
                results.append((fn, True))
            else:
                results.append((fn, False))
        elif fn == '576':
            pattern = r'(GREAT THURSDAY[:\s]*(?:\*\*)?)'
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                pos = m.end()
                text = text[:pos] + marker + text[pos:]
                results.append((fn, True))
            else:
                results.append((fn, False))
    
    return text, results


# =============================================================================
# PART 5: Temple Rubrics (49 failures)
# =============================================================================

# Menologion footnotes: These annotate specific saint entries in the calendar.
# RAW format: "28 `+` Ven. Chariton^[703]."
# EN format:  "* **28** **[POL]** Ven. Chariton."
# 
# We need to find the saint name and place the marker after match.

MENOLOGION_MARKERS = {
    # (fn_num, search_phrase, after_text)
    665: ("1. GENERAL RUBRICS", None),              # After section header
    699: ("without Troparion", "4 NO"),              # After the last designation line  
    702: ("Prophet Jonah and Ven. Jonah", None),     # Sept 22
    703: ("Ven. Chariton", None),                    # Sept 28
    704: ("Apostle Thomas", None),                   # Oct 6
    705: ("Ven. Paraskeva", "Oct"),                   # Oct 14
    707: ("Martyr Paraskeva", "Oct 28"),              # Oct 28
    712: ("Barlaam", "Nov 19"),                       # Nov 19
    714: ("Ven. Alypius", None),                      # Nov 26
    715: ("Ven. Acacius", None),                      # Nov 29
    716: ("Prop. Nahum", None),                        # Dec 1 - EN uses "Prop. Nahum"
    717: ("Prop. Habakkuk", None),                     # Dec 2
    718: ("Prop. Zephaniah", None),                    # Dec 3
    720: ("St. Ambrose", "Dec"),                       # Dec 7
    721: ("Ven. Patapius", None),                      # Dec 8
    725: ("Martyr Sebastian", "Dec"),                  # Dec 18
    726: ("Martyr Boniface", None),                    # Dec 19
    727: ("Fast-free", "Theophany"),                   # Dec 25 note
    728: ("Theodore Graptos", None),                   # Dec 27 - EN uses "Graptos" not "Branded"
    729: ("Hieromartyr Artemon", None),                # Apr 13
    730: ("Theodore of Perge", None),                  # Apr 21
    734: ("Martyr Hermias", None),                     # May 31
}

# Rubrics section footnotes - these are in the final "Rubric about Holy Doors" 
# and "Rubric of Divine Services" sections starting around line 690+
RUBRIC_MARKERS = {
    # fn_num: (distinctive_search_string, fallback)
    745: ("TYPIKON OF SAVA", "NUMBER OF ALL-NIGHT VIGILS"),
    753: None,  # Just "Liturgy" - too ambiguous, skip or handle specially
    755: ("communion of the celebrant", None),
    756: ("Lamp-lighting", "Vespers (Lamp-lighting)"),
    757: ("returns into the sanctuary", None),
    759: ("lifts the Gospel up", "the Gospel up"),
    760: ("says the dismissal", "standing in the holy doors, says the dismissal"),
    761: ("Let us be attentive", "of the title"),
    762: ("priest goes out", "custom and the holy doors"),
    763: ("wheat, wine and oil", None),
    764: ("Matins begins thus", None),
    765: ("The priest exclaims", "Glory to the Holy, Consubstantial"),
    766: ("reading of the Six Psalms", None),
    767: ("Shortening of Matins", None),
    768: ("none falls off", None),
    771: ("Gospel to the priest", "gives the rolled"),
    772: ("through the northern doors", "Wisdom"),
    773: ("he censes the priest", "southern doors into the sanctuary"),
    774: ("deacon's head", "places it with"),
    776: ("takes from the deacon", "holy chalice"),
    777: ("and became man", "I believe"),
    778: ("at a distance", "warm water"),
    779: ("antimension", "folded antimension"),
    780: ("Prayer behind the Ambo", None),
    783: ("Entrance all go out", "Little Entrance"),
    784: ("All go out", "spear, the spoon"),
    785: ("oblation takes place thus", "table of oblation"),
}


def fix_part5(text):
    """Fix 49 failed markers in Part 5."""
    results = []
    
    # === Menologion entries ===
    for fn_num, (search_phrase, hint) in MENOLOGION_MARKERS.items():
        marker = f'^[{fn_num}]'
        if marker in text:
            results.append((str(fn_num), True))
            continue
        
        placed = False
        
        if fn_num == 665:
            # "1. GENERAL RUBRICS^[665]" - section header
            pattern = r'(1\.\s*GENERAL RUBRICS\s*)'
            m = re.search(pattern, text)
            if m:
                pos = m.end()
                text = text[:pos] + marker + text[pos:]
                placed = True
        elif fn_num == 699:
            # "Feast on 4 without Troparion^[699]" in designations section
            # EN: "* **[4 NO]** Simple (No Symbol)" or similar
            # Search for the designation listing that ends the list
            pattern = r'(\*\s*\*\*\[4 NO\]\*\*[^\n]*)'
            m = re.search(pattern, text)
            if m:
                pos = m.end()
                text = text[:pos] + marker + text[pos:]
                placed = True
            else:
                # Try alternate: "without Troparion" or "Simple" or "No Symbol"
                pattern = r'((?:without Troparion|Simple|No Symbol)[^\n]*)'
                m = re.search(pattern, text)
                if m:
                    pos = m.end()
                    text = text[:pos] + marker + text[pos:]
                    placed = True
        elif fn_num == 727:
            # "Fast-free period – until Theophany inclusive^[727]."
            # EN: "Fast-free period - until Theophany inclusive."
            pattern = r'(Fast-free period[^.]*inclusive)\s*\.?'
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                pos = m.end(1)
                text = text[:pos] + marker + text[pos:]
                placed = True
        elif fn_num == 728:
            # "Ven. Theodore the Branded^[728]" → EN: "Theodore Graptos"
            pattern = r'(Theodore Graptos[^\n.]*)'
            m = re.search(pattern, text)
            if m:
                pos = m.end()
                text = text[:pos] + marker + text[pos:]
                placed = True
        else:
            # Generic Menologion entry: find saint name in the bullet-point list
            # Try exact phrase first
            idx = text.find(search_phrase)
            if idx != -1:
                # Find end of this entry (end of line or next bullet)
                end = idx + len(search_phrase)
                # Place marker right after the search phrase
                # But check: is there already a period or end of line?
                # Place before any trailing period
                rest = text[end:end+10]
                if rest.startswith('.'):
                    text = text[:end] + marker + text[end:]
                    placed = True
                elif rest.startswith('\n') or rest.startswith('\r') or rest == '':
                    text = text[:end] + marker + text[end:]
                    placed = True
                else:
                    # Place at end of the search phrase
                    text = text[:end] + marker + text[end:]
                    placed = True
        
        results.append((str(fn_num), placed))
    
    # === Rubric section markers ===
    for fn_num, info in RUBRIC_MARKERS.items():
        marker = f'^[{fn_num}]'
        if marker in text:
            results.append((str(fn_num), True))
            continue
        
        if info is None:
            results.append((str(fn_num), False))
            continue
        
        search_phrase, fallback = info
        placed = False
        
        if fn_num == 745:
            # "ACCORDING TO THE TYPIKON OF SABBAS" or "TYPIKON OF SAVA"
            pattern = r'(TYPIKON OF SAV[AE]|NUMBER OF ALL-NIGHT VIGILS[^\n]*)'
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                pos = m.end()
                text = text[:pos] + marker + text[pos:]
                placed = True
        else:
            # For rubric markers, search for the distinctive phrase
            idx = text.find(search_phrase)
            if idx == -1 and fallback:
                idx = text.find(fallback)
                if idx != -1:
                    search_phrase = fallback
            
            if idx != -1:
                end = idx + len(search_phrase)
                text = text[:end] + marker + text[end:]
                placed = True
        
        results.append((str(fn_num), placed))
    
    return text, results


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("PHASE 1 v3: AI-DRIVEN MANUAL MARKER PLACEMENT")
    print("=" * 70)
    
    all_results = {}
    total_placed = 0
    total_failed = 0
    
    # Process each part
    for part_name, fix_fn in [
        ("dolnytsky_part2_general_rubrics.txt", fix_part2),
        ("dolnytsky_part3_menaion.txt", fix_part3),
        ("dolnytsky_part4_triodion.txt", fix_part4),
        ("dolnytsky_part5_temple.txt", fix_part5),
    ]:
        stitched_path = SCRATCH_DIR / f"STITCHED_v2_{part_name}"
        if not stitched_path.exists():
            print(f"  SKIP: {stitched_path.name} not found")
            continue
        
        print(f"\n--- Fixing {part_name} ---")
        text = load_file(stitched_path)
        
        text, results = fix_fn(text)
        
        placed = [r for r in results if r[1]]
        failed = [r for r in results if not r[1]]
        
        print(f"  Placed: {len(placed)} ({[r[0] for r in placed]})")
        print(f"  Failed: {len(failed)} ({[r[0] for r in failed]})")
        
        total_placed += len(placed)
        total_failed += len(failed)
        
        # Save as v3
        v3_path = SCRATCH_DIR / f"STITCHED_v3_{part_name}"
        save_file(v3_path, text)
        
        all_results[part_name] = {
            'placed': [r[0] for r in placed],
            'failed': [r[0] for r in failed],
        }
    
    # Part 1 had 0 v2 failures, just copy v2 -> v3
    p1_v2 = SCRATCH_DIR / "STITCHED_v2_dolnytsky_part1_structure.txt"
    p1_v3 = SCRATCH_DIR / "STITCHED_v3_dolnytsky_part1_structure.txt"
    if p1_v2.exists():
        text = load_file(p1_v2)
        save_file(p1_v3, text)
        print(f"\n--- Part 1: Copied v2 to v3 (no fixes needed) ---")
    
    # Save report
    report_path = REPORT_DIR / "v3_manual_placement.json"
    save_file(report_path, json.dumps(all_results, indent=2, ensure_ascii=False))
    
    print(f"\n{'=' * 70}")
    print(f"PHASE 1 v3 COMPLETE")
    print(f"Total newly placed: {total_placed}")
    print(f"Still failed: {total_failed}")
    print(f"Stitched files: {SCRATCH_DIR}/STITCHED_v3_*")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
