import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

base = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded"
d_path = os.path.join(base, 'Data', 'Service Books', 'Typikon', 'Dolnytsky_Typikon_Master.md')
o_path = os.path.join(base, 'Data', 'Service Books', 'Typikon', 'Ordo', 'Ordo_Celebrationis_1996_CLEAN.md')

with open(d_path, 'r', encoding='utf-8') as f:
    d_lines = [l.rstrip('\r\n') for l in f]

with open(o_path, 'r', encoding='utf-8') as f:
    o_lines = [l.rstrip('\r\n') for l in f]

def find_in_lines(lines, pattern):
    regex = re.compile(pattern, re.I)
    results = []
    for idx, l in enumerate(lines):
        if regex.search(l):
            results.append((idx + 1, l))
    return results

queries = [
    ("Delta 1 & 2: Vigil duration & usage (Ordo Note 86)", o_lines, r"In normal parish use, the.*Vigil lasts about two hours"),
    ("Delta 3: Compline suppressed at Vigil (Dolnytsky Footnote 161)", d_lines, r"The Greek Typikon does not give anything, for the All-Night Vigil is implied"),
    ("Delta 4: Small Vespers before Vigil (Dolnytsky §1.2.4)", d_lines, r"### 1\.2\.4 Order of Small Vespers"),
    ("Delta 4b: Small Vespers on Sunday (Dolnytsky Footnote 160)", d_lines, r"According to the ancient typikon, on Sunday, in view of the All-Night Vigil"),
    ("Delta 5: Reverence to Superior (Ordo Note 96)", o_lines, r"The reference is to a monastic superior, or to a bishop"),
    ("Delta 6: Kathisma 1 selection vs whole (Dolnytsky §2.1.1.1)", d_lines, r"Kathisma 1.*Blessed is the man.*whole, according to the Typikon"),
    ("Delta 7: Entrance at Daily Vespers in parish (Dolnytsky §1.2.3.3)", d_lines, r"parish churches in the province, the general custom remains to make an Entrance"),
    ("Delta 8: Litya Temple Sticheron omitted in parish (Dolnytsky §2.6.1.4)", d_lines, r"first sticheron - of the temple \(which today we usually do not take\)"),
    ("Delta 8b: Litya Temple Sticheron weekday vigil (Dolnytsky §2.7.1.3)", d_lines, r"first sticheron - of the temple, which today we usually do not take"),
    ("Delta 8c: Footnote 143 on Temple Sticheron (Dolnytsky Footnote 143)", d_lines, r"sticheron of the Saint of the Monastery"),
    ("Delta 9: Sitting during Vespers (Dolnytsky §1.2.3.3)", d_lines, r"It is not proper to sit at this Vespers either"),
    ("Delta 10: Compline St Basil troparion (Dolnytsky §1.3.1.1)", d_lines, r"monks before 'O God of our Fathers' recite also the troparion to St\. Basil"),
    ("Delta 11: Compline/Midnight petitions in monasteries (Dolnytsky §1.3.1.1)", d_lines, r"petitions given before the litany are recited only in monasteries"),
    ("Delta 12: Midnight Office in monasteries (Dolnytsky §1.4)", d_lines, r"### 1\.4 Midnight Office"),
    ("Delta 13: Royal Office (Ordo Note 109)", o_lines, r"is a spiritual recompense for the King or Emperor who founded a given monastery"),
    ("Delta 14: Psalter Kathismata abbreviated (Dolnytsky §1.5.1.3)", d_lines, r"according to the current local custom, only a few verses"),
    ("Delta 15: Small litany silent by priest in parish (Dolnytsky §1.5.1.3)", d_lines, r"which according to local custom the Priest says quietly, sitting at his place"),
    ("Delta 16: Intercalation of Biblical Canticles (Dolnytsky Footnote 5476)", d_lines, r"combination of the Odes of the Psalter with the Odes of the Canon"),
    ("Delta 17: Katavasia descent in monasteries (Ordo Glossary)", o_lines, r"the two monastic choirs.*descend.*from their positions"),
    ("Delta 18: Polyeleos vs Vigil (Dolnytsky Part 3 L2387)", d_lines, r"even with All-Night Vigil.*although with us there is none, but only Polyeleos"),
    ("Delta 19: Little Hours omitted in parishes (Ordo Note 268)", o_lines, r"In parishes the Little Hours are often omitted"),
    ("Delta 20: Russian monastery 3 litanies per Hour (Dolnytsky Footnote 311)", d_lines, r"Typikons of some Russian monasteries.*prescribe for the Deacon at each Hour"),
    ("Delta 21: Inter-Hours (Dolnytsky §1.6)", d_lines, r"### 1\.6 Order of the Usual Hours"),
    ("Delta 22: 1 vs 5 prosphora (Dolnytsky Appendix §98)", d_lines, r"not necessary to always use five prosphora"),
    ("Delta 23: Multiple liturgies at same altar (Dolnytsky Appendix §97)", d_lines, r"If there is one or several secondary churches in the parish"),
    ("Delta 24: Athonite curtain custom (Dolnytsky Footnote 7476)", d_lines, r"curtain, according to the present custom of Athonite monasteries"),
    ("Delta 25: Concelebration & visiting parish priests (Ordo Note 245)", o_lines, r"priests who have already liturgized for their own parishes"),
    ("Delta 26: Large communion volume in parishes (Ordo Note 280)", o_lines, r"This can occur frequently in parishes where the faithful are accustomed to receive"),
    ("Delta 27: Earthly prostrations in parishes (Dolnytsky Footnote 13)", d_lines, r"In some parishes, they still bend their knees and heads to the ground"),
    ("Delta 28: Simple saints transfer during Great Lent (Dolnytsky Part IV)", d_lines, r"Friday Compline"),
    ("Delta 29: Fasting mitigations (Dolnytsky Foreword)", d_lines, r"obliged all clergy, monastics, and faithful in conscience to observe the fast"),
    ("Delta 30: Temple Feast outdoor water blessing for parish (Dolnytsky §5.2.1.3)", d_lines, r"Blessing of Water usually takes place outside the church.*all people of the parish"),
    ("Delta 31: Parish deceased liturgy after Temple feast (Dolnytsky §5.2.1.4)", d_lines, r"Liturgy for the deceased of the parish with a Parastas is sung"),
    ("Delta 32: Rite of the Panagia daily in monasteries (Dolnytsky Footnote 630)", d_lines, r"predominantly daily in monasteries, as is seen from the service of the meal"),
]

for label, lines, pat in queries:
    res = find_in_lines(lines, pat)
    if res:
        print(f"=== {label} ===")
        for ln, txt in res[:2]:
            print(f"  Line {ln}: {txt[:120]}")
    else:
        print(f"!!! MISSING: {label} (pattern: {pat})")
