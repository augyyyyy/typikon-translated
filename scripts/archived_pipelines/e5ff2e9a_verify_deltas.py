import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

base = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded"
d_path = os.path.join(base, 'Data', 'Service Books', 'Typikon', 'Dolnytsky_Typikon_Master.md')
o_path = os.path.join(base, 'Data', 'Service Books', 'Typikon', 'Ordo', 'Ordo_Celebrationis_1996_CLEAN.md')

with open(d_path, 'r', encoding='utf-8') as f:
    d_text = f.read()

with open(o_path, 'r', encoding='utf-8') as f:
    o_text = f.read()

checks = [
    ('Dolnytsky Entrance at Daily Vespers in parish churches', r'parish churches in the province', d_text),
    ('Dolnytsky Compline troparia with St Basil', r'monks before .*St\. Basil', d_text),
    ('Dolnytsky Compline/Midnight Office litany petitions', r'petitions given before the litany are recited only in monasteries', d_text),
    ('Dolnytsky Kathisma 1 selection vs whole', r'Kathisma 1.*Blessed is the man.*according to the Typikon - whole', d_text),
    ('Dolnytsky Paradigm 6 Lytia temple sticheron', r'first sticheron - of the temple \(which today we usually do not take\)', d_text),
    ('Dolnytsky Paradigm 7 Lytia temple sticheron', r'first sticheron - of the temple, which today we usually do not take', d_text),
    ('Dolnytsky Temple feast parish water blessing', r'Blessing of Water usually takes place.*people of the parish', d_text),
    ('Dolnytsky Temple feast parish deceased liturgy', r'Liturgy for the deceased of the parish with a Parastas', d_text),
    ('Dolnytsky Multiple Liturgies at same holy table', r'secondary churches in the parish', d_text),
    ('Dolnytsky 1 vs 5 prosphora', r'not necessary to always use five prosphora', d_text),
    ('Dolnytsky Athonite curtain custom', r'curtain, according to the present custom of Athonite monasteries', d_text),
    ('Dolnytsky St Catherine transfer by Sinai monks', r'wish of the monks of Mount Sinai', d_text),
    ('Dolnytsky 3 litanies per Hour in Russian monasteries', r'Russian monasteries.*prescribe for the deacon at each Hour to sing three litanies', d_text),
    ('Dolnytsky Rite of the Panagia', r'Rite of the Panagia.*daily in monasteries', d_text),
    ('Dolnytsky Kneeling/prostrations in parishes', r'In some parishes, they still bend their knees', d_text),
    ('Ordo Vigil duration parish vs monastic', r'In normal parish use, the.*Vigil lasts about two hours.*in monasteries', o_text),
    ('Ordo Royal Office parish vs monastic', r'Royal Office.*seldom done in parish churches.*maintained in monasteries', o_text),
    ('Ordo Little Hours omitted in parishes', r'In parishes the Little Hours are often omitted', o_text),
    ('Ordo Katavasia descent in monasteries', r'monastic choirs.*descend.*center of the nave', o_text),
    ('Ordo Superior/Bishop distinction', r'reference is to a monastic superior, or to a bishop', o_text),
    ('Ordo Visiting parish priests concelebrating', r'priests who have already liturgized for their own parishes', o_text),
    ('Ordo Presanctified communication in parishes', r'frequently in parishes where the faithful are accustomed to receive', o_text),
]

for label, pat, text_src in checks:
    m = re.search(pat, text_src, re.I | re.DOTALL)
    if m:
        matched_str = ' '.join(m.group(0).split())[:100]
        print(f"MATCH: {label} -> '{matched_str}'")
    else:
        print(f"MISS:  {label}")
