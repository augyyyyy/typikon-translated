"""
Phase D: Hieratic Pronoun Audit — REFINED Pass
================================================
Narrows the 183 deity candidates by applying stronger context filters.

True violations are cases where lowercase "he/him/his/who/whom" refers to:
  - God the Father
  - Jesus Christ / the Son
  - The Holy Spirit

FALSE positives (correctly lowercase) are references to:
  - A priest / deacon / reader / bishop (any clergyman)  
  - A saint being commemorated
  - Dolnytsky himself
  - An ecclesiarch / choir director
  - "he" in general rubrical instructions ("if the saint has [something], he...")
"""

import re
import os

FINAL_DIR = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\Final"

# Strong indicators that lowercase "he/him/his" refers to a HUMAN (correct)
HUMAN_INDICATORS = re.compile(
    r'\b(?:Priest|priest|Deacon|deacon|Reader|reader|Bishop|bishop|'
    r'Ecclesiarch|Hierarch|Superior|Abbot|celebrant|'
    r'saint|Saint|Prophet|prophet|Apostle|apostle|'
    r'Martyr|martyr|Hieromartyr|Monk|monk|Father|'
    r'Synod|Dolnytsky|Mark|Sabbas|Basil|Chrysostom|Nicholas|'
    r'George|Theodore|Athanasius|Gregory|Neilos|Nilus|'
    r'Bartholomew|Leo|Allatius|Benjamin|Clement|'
    r'confessor|Patriarch|Metropolitan|Archbishop|'
    r'Archpriest|Protodeacon|'
    r'celebr|author|editor|publisher|writer|composer|'
    r'choir|choirs|Khagan|enemy|enemies|Emperor|'
    r'Christians|brother|brethren|Superior|'
    r'first deacon|second deacon|first choir|'
    r'the saint|to the saint|of the saint|'
    r'if he has|if he does|nor is he|'  # rubrical "he" = saint, always
    r'candle-bearer|lamp-lighter|sacristan)\b',
    re.IGNORECASE
)

# Strong indicators of DEITY reference (should be capitalized)
DEITY_STRONG = re.compile(
    r'\b(?:Body of Christ|Blood of Christ|Mysteries|'
    r'God and Saviour|true God|Christ, true|'
    r'Christ is risen|Truly He is|'
    r'rose from the dead|born in a cavern|born in Bethlehem|'
    r'Who rose|Who was born|'
    r'let himself be laid|Who blessest|'
    r'precious and most holy|most pure|blameless hands|'
    r'gave thanks and blessed|'
    r'Mystical Supper|His holy)\b',
    re.IGNORECASE
)

WINDOW = 150

files = sorted([f for f in os.listdir(FINAL_DIR) if f.endswith('.txt')])

deity_keywords = re.compile(
    r'\b(?:God|Lord|Christ|Saviour|Savior|Holy Spirit|Theotokos|'
    r'Mother of God|Most Holy|Almighty|Comforter|Redeemer|Jesus|'
    r'the Son|the Father|Holy Trinity|Trinity|Divine)\b', re.IGNORECASE
)

pronoun_checks = [
    (re.compile(r'\b(he)\b'), 'he'),
    (re.compile(r'\b(him)\b'), 'him'),  
    (re.compile(r'\b(his)\b'), 'his'),
    (re.compile(r'\b(who)\b'), 'who'),
    (re.compile(r'\b(whom)\b'), 'whom'),
    (re.compile(r'\b(himself)\b'), 'himself'),
]

true_violations = []
likely_false_positives = []
ambiguous = []

for fname in files:
    filepath = os.path.join(FINAL_DIR, fname)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        for patt, desc in pronoun_checks:
            for match in patt.finditer(line):
                # Only lowercase instances
                if match.group(1)[0].isupper():
                    continue
                    
                start = match.start()
                ws = max(0, start - WINDOW)
                we = min(len(line), start + WINDOW)
                context = line[ws:we]
                
                # Must be near a deity keyword
                if not deity_keywords.search(context):
                    continue
                
                # Check for strong deity indicators
                is_deity = bool(DEITY_STRONG.search(context))
                
                # Check for human indicators
                is_human = bool(HUMAN_INDICATORS.search(context))
                
                entry = {
                    'file': fname,
                    'line': line_num,
                    'pronoun': desc,
                    'context': context.strip()[:200],
                }
                
                if is_deity and not is_human:
                    true_violations.append(entry)
                elif is_human:
                    likely_false_positives.append(entry)
                else:
                    ambiguous.append(entry)

with open(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\pronoun_violations.txt", 'w', encoding='utf-8') as out:
    def write_line(text=""):
        out.write(text + "\n")

    write_line("=" * 80)
    write_line("HIERATIC PRONOUN AUDIT — REFINED RESULTS")
    write_line("=" * 80)

    write_line(f"\n🔴 TRUE VIOLATIONS (deity context, needs fix): {len(true_violations)}")
    for v in true_violations:
        write_line(f"  {v['file']}:L{v['line']} [{v['pronoun']}]")
        write_line(f"    {v['context'][:180]}")
        write_line()

    write_line(f"\n🟡 AMBIGUOUS (needs human review): {len(ambiguous)}")
    for a in ambiguous:
        write_line(f"  {a['file']}:L{a['line']} [{a['pronoun']}]")
        write_line(f"    {a['context'][:180]}")
        write_line()

    write_line(f"\n✅ LIKELY FALSE POSITIVES (human referent, lowercase correct): {len(likely_false_positives)}")
    write_line(f"   (not shown — these are references to priests, deacons, saints, etc.)")

    write_line(f"\n{'='*80}")
    write_line(f"SUMMARY: {len(true_violations)} violations | {len(ambiguous)} ambiguous | {len(likely_false_positives)} OK")
    write_line(f"{'='*80}")

