#!/usr/bin/env python3
"""
Terminology Audit: Scan all STITCHED files for vocabulary drift.
Each part was translated in a separate chat instance, so terminology
may vary despite having the same system instructions.
"""

import re
import os
from collections import defaultdict

SCRATCH = r"e:\Google Antigravity\Projects\Translation\scratch"
FILES = {
    "Part1": "STITCHED_v3_dolnytsky_part1_structure.txt",
    "Part2": "STITCHED_v3_dolnytsky_part2_general_rubrics.txt",
    "Part3": "STITCHED_v3_dolnytsky_part3_menaion.txt",
    "Part4": "STITCHED_v3_dolnytsky_part4_triodion.txt",
    "Part5": "STITCHED_v3_dolnytsky_part5_temple.txt",
    "Appendix": "STITCHED_v3_dolnytsky_appendix.txt",
}

# (correct_term, [incorrect_variants_to_search_for])
# Case-insensitive search
TERMS = [
    # === HYMNOGRAPHY ===
    ("Sessional Hymn", ["sedalen", "sitting hymn", "sedalion", "kathisma hymn", "sjedalen"]),
    ("Kontakion", ["kondak", "kontakio", "kondakion"]),
    ("Doxastikon", ["naslavnik", "doxasticon", "slavnik"]),
    ("Theotokion", ["bohorodychnyi", "bogorodichen", "theotokia"]),
    ("Aposticha", ["stykhivnia", "apostikha", "apostikha", "stichera at the verse"]),
    ("Gradual", ["stepenna", "step hymn", "antiphons of ascent", "graduale", "hymns of ascent"]),
    ("Exaposteilarion", ["svitylny", "exapostilarion", "luminous hymn", "svetilen", "exapostilaria"]),
    ("Idiomelon", ["samohlasen", "samoglasny", "idiomela", "automela", "samoglasen"]),
    ("Prosomoion", ["podoben", "podiben", "prosomoia"]),
    ("Magnification", ["velychannye", "megalynarion"]),
    ("Polyeleos", ["polyeley", "polieleos", "polyeleios"]),
    ("Tone", ["glas ", "hlas "]),  # space to avoid false positives
    # === SERVICES ===
    ("All-Night Vigil", ["all night vigil", "vsenichne"]),
    ("Compline", ["povechiria", "povecheriye", "complins"]),
    ("Midnight Office", ["pivnichna", "nocturns", "midnight service"]),
    ("Typika", ["obidnytsia", "typica ", "typikon office"]),
    ("Litiya", ["lity ", "litia ", "litias"]),
    # === FEASTS ===
    ("Forefeast", ["peredsviattia", "pre-feast", "prefeast", "fore-feast"]),
    ("Afterfeast", ["posviattia", "post-feast", "postfeast", "after-feast"]),
    ("Apodosis", ["viddannia", "leave-taking", "leavetaking", "otdanie"]),
    ("Shroud", ["plaschanitsa", "epitaphios", "plashchanitsa"]),
    # === BOOKS ===
    ("Anthologion", ["trefologion", "trephologion", "antologion"]),
    ("Menaion", ["mineya", "menaia"]),
    # === OTHER ===
    ("Praises", ["lauds ", "khvalytni", "chvalytni"]),
    ("Doxology", ["slavoslovya", "slavoslovija"]),
    # === CAPITALIZATION / PRONOUN ===
    ("Priest (cap)", ["priest"]),  # We need case-sensitive for this
    ("Deacon (cap)", ["deacon"]),
    # === LITURGICAL OBJECTS ===
    ("Prokimenon", ["prokeimenon", "prokeimena"]),
    ("Troparion", ["tropar ", "tropariy"]),
    ("Sticheron", ["stikhira", "stikheera", "stikher"]),
    ("Katavasia", ["katavasiya", "katavassiya"]),
    ("Irmos", ["hirmos", "eirmos"]),
    ("Heirmos", []),  # check if used as alternate to Irmos
    # === WEEK DAYS ===
    ("Sunday", ["nedilya"]),
    ("Saturday", ["subota"]),
]

def main():
    print("=" * 80)
    print("TERMINOLOGY AUDIT: Cross-Part Vocabulary Drift Detection")
    print("=" * 80)
    
    texts = {}
    for part_key, fname in FILES.items():
        fpath = os.path.join(SCRATCH, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                texts[part_key] = f.read()
    
    # Check each term
    issues_found = []
    
    for correct_term, wrong_variants in TERMS:
        term_results = {}
        has_issue = False
        
        for part_key, text in texts.items():
            text_lower = text.lower()
            correct_count = len(re.findall(re.escape(correct_term.lower()), text_lower))
            
            variant_hits = {}
            for v in wrong_variants:
                count = len(re.findall(re.escape(v.lower()), text_lower))
                if count > 0:
                    variant_hits[v] = count
                    has_issue = True
            
            term_results[part_key] = {
                "correct": correct_count,
                "variants": variant_hits,
            }
        
        if has_issue:
            issues_found.append((correct_term, term_results))
    
    # Print results
    if not issues_found:
        print("\nNo terminology drift found!")
    else:
        print(f"\n{'='*80}")
        print(f"ISSUES FOUND: {len(issues_found)} terms with variant usage")
        print(f"{'='*80}\n")
        
        for correct_term, term_results in issues_found:
            print(f"\n--- {correct_term} ---")
            for part_key in FILES:
                if part_key not in term_results:
                    continue
                data = term_results[part_key]
                if data["correct"] > 0 or data["variants"]:
                    line = f"  {part_key}: correct={data['correct']}"
                    for v, c in data["variants"].items():
                        line += f"  | WRONG '{v}'={c}"
                    print(line)
    
    # Also check for specific cross-part inconsistencies
    print(f"\n{'='*80}")
    print("ADDITIONAL CHECKS: Case Sensitivity & Style")
    print(f"{'='*80}\n")
    
    # Check: "Priest" vs "priest" (should be capitalized per appendix usage)
    for part_key, text in texts.items():
        # Count lowercase "priest" at start of sentences (after ". " or "\n")
        lowercase_priest = len(re.findall(r'(?<![A-Za-z])[tT]he priest\b', text))
        uppercase_priest = len(re.findall(r'(?<![A-Za-z])[tT]he Priest\b', text))
        lowercase_deacon = len(re.findall(r'(?<![A-Za-z])[tT]he deacon\b', text))
        uppercase_deacon = len(re.findall(r'(?<![A-Za-z])[tT]he Deacon\b', text))
        
        if lowercase_priest > 0 or uppercase_priest > 0:
            print(f"  {part_key}: 'the priest'={lowercase_priest} vs 'the Priest'={uppercase_priest}")
        if lowercase_deacon > 0 or uppercase_deacon > 0:
            print(f"  {part_key}: 'the deacon'={lowercase_deacon} vs 'the Deacon'={uppercase_deacon}")
    
    print()
    
    # Check: Quote style (" vs smart quotes)
    for part_key, text in texts.items():
        smart_single = text.count("\u2018") + text.count("\u2019")
        smart_double = text.count("\u201C") + text.count("\u201D")
        straight_single = text.count("'")
        straight_double = text.count('"')
        if smart_single > 0 or smart_double > 0:
            print(f"  {part_key}: smart quotes: single={smart_single} double={smart_double}")
            print(f"  {part_key}: straight quotes: single={straight_single} double={straight_double}")
    
    print()
    
    # Check: Em dash variants
    for part_key, text in texts.items():
        em_dash = text.count("\u2014")
        en_dash = text.count("\u2013")
        double_dash = text.count("--")
        hyphen_spaced = len(re.findall(r' - ', text))
        if em_dash + en_dash + double_dash > 0:
            print(f"  {part_key}: em={em_dash} en={en_dash} --={double_dash} ' - '={hyphen_spaced}")
    
    print()
    
    # Check: Deity pronoun capitalization  
    print("--- Deity Pronoun Check (He/Him/His/Who/Whom for God/Christ) ---")
    for part_key, text in texts.items():
        # This is complex - just count lowercase 'he ' 'him ' 'his ' as rough indicator
        # Many will be legitimate (referring to humans)
        # Focus: lines mentioning God/Christ/Lord with lowercase pronouns nearby
        lines = text.split('\n')
        potential_issues = 0
        for line in lines:
            line_lower = line.lower()
            if any(w in line_lower for w in ['god', 'christ', 'lord', 'savior', 'saviour']):
                # Check for lowercase pronouns on same line
                if re.search(r'\b(he|him|his)\b', line) and not re.search(r'\b(He|Him|His)\b', line):
                    potential_issues += 1
        if potential_issues > 0:
            print(f"  {part_key}: ~{potential_issues} lines with god-context + lowercase pronouns")


if __name__ == "__main__":
    main()
