#!/usr/bin/env python3
"""
Comprehensive audit of Final files against the Translation System Instructions.
Checks every mandate from 'system instructions typikon.txt' in one pass.
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

final_dir = r'e:\Google Antigravity\Projects\Translation\Final'

# Load all text once
corpus = {}
full_text = ""
for name in sorted(os.listdir(final_dir)):
    if not name.endswith('.txt'):
        continue
    with open(os.path.join(final_dir, name), 'r', encoding='utf-8') as f:
        t = f.read()
    corpus[name] = t
    full_text += t + "\n"

print("=" * 70)
print("SYSTEM INSTRUCTIONS COMPLIANCE AUDIT")
print("=" * 70)

# =========================================================================
# 1. MASTER GLOSSARY CHECK — System instructions mandate specific terms
# =========================================================================
print("\n\n### 1. MASTER GLOSSARY COMPLIANCE ###")

# Format: (Instruction term, should_appear_regex, should_NOT_appear_variants)
glossary_checks = [
    # System says: Tserkovne Oko = Tserkovne Oko (Do NOT translate as "Eye of the Church")
    ("Tserkovne Oko", r'\bTserkovne Oko\b', [
        ("Eye of the Church", r'\bEye of the Church\b'),
        ("Oko Tserkovne", r'\bOko Tserkovne\b'),
        ("Church Eye", r'\bChurch Eye\b'),
    ]),
    # Anthologion
    ("Anthologion", r'\bAnthologion\b', [
        ("Trephologion", r'\bTrephologion\b'),
        ("Trefoloy", r'\bTrefoloy\b'),
        ("Antolohion", r'\bAntolohion\b'),
    ]),
    # Menaion
    ("Menaion", r'\bMenaion\b', [
        ("Mineia", r'\bMineia\b'),
        ("Mineya", r'\bMineya\b'),
    ]),
    # Sessional Hymn
    ("Sessional Hymn", r'\bSessional Hymn\b', [
        ("Sedalen", r'\bSedalen\b'),
        ("Sidalen", r'\bSidalen\b'),
    ]),
    # Kontakion
    ("Kontakion", r'\bKontakion\b', [
        ("Kondak", r'\bKondak\b'),
    ]),
    # Doxastikon
    ("Doxastikon", r'\bDoxastikon\b', [
        ("Naslavnik", r'\bNaslavnik\b'),
        ("Slavnik", r'\bSlavnik\b'),
    ]),
    # Theotokion
    ("Theotokion", r'\bTheotokion\b', [
        ("Bohorodychnyi", r'\bBohorodychnyi\b'),
        ("Bogorodichen", r'\bBogorodichen\b'),
    ]),
    # Praises
    ("Praises", r'\bPraises\b', [
        ("Khvalytni", r'\bKhvalytni\b'),
        ("Khvalitni", r'\bKhvalitni\b'),
    ]),
    # Aposticha
    ("Aposticha", r'\bAposticha\b', [
        ("Stikhovni", r'\bStikhovni\b'),
        ("Stykhivnia", r'\bStykhivnia\b'),
    ]),
    # Exaposteilarion
    ("Exaposteilarion", r'\bExaposteilarion\b', [
        ("Svitylny", r'\bSvitylny\b'),
        ("Svetilen", r'\bSvetilen\b'),
    ]),
    # Doxology
    ("Doxology", r'\bDoxology\b', [
        ("Slavoslovie", r'\bSlavoslovie\b'),
        ("Slavoslovya", r'\bSlavoslovya\b'),
    ]),
    # Idiomelon (for Samohlasen)
    ("Idiomelon", r'\bIdiomelon\b', [
        ("Samohlasen", r'\bSamohlasen\b'),
    ]),
    # Prosomoion (for Podiben)
    ("Prosomoion", r'\bProsomoion\b', [
        ("Podiben", r'\bPodiben\b'),
    ]),
    # Magnification (for Velychannye)
    ("Magnification", r'\bMagnification\b', [
        ("Velychannye", r'\bVelychannye\b'),
        ("Megalynaria", r'\bMegalynaria\b'),
    ]),
    # Polyeleos
    ("Polyeleos", r'\bPolyeleos\b', [
        ("Polyeley", r'\bPolyeley\b'),
    ]),
    # Gradual (for Stepenna)
    ("Gradual", r'\bGradual\b', [
        ("Stepenna", r'\bStepenna\b'),
    ]),
    # Tone (for Hlas)
    ("Tone", r'\bTone\b', [
        ("Hlas", r'\bHlas\b'),
    ]),
    # Apodosis
    ("Apodosis", r'\bApodosis\b', [
        ("Viddannia", r'\bViddannia\b'),
        ("Leavetaking", r'\bLeavetaking\b'),
    ]),
    # Forefeast
    ("Forefeast", r'\bForefeast\b', [
        ("Peredsviattia", r'\bPeredsviattia\b'),
    ]),
    # Afterfeast
    ("Afterfeast", r'\bAfterfeast\b', [
        ("Posviattia", r'\bPosviattia\b'),
    ]),
    # Temple (for Khram)
    ("Temple", r'\bTemple\b', [
        ("Khram", r'\bKhram\b'),
    ]),
    # Shroud
    ("Shroud", r'\bShroud\b', [
        ("Plaschanitsa", r'\bPlaschanitsa\b'),
        ("Plashchanitsa", r'\bPlashchanitsa\b'),
    ]),
    # Litiya
    ("Litiya", r'\bLitiya\b', [
        ("Litia", r'\bLitia\b'),
    ]),
    # All-Night Vigil
    ("All-Night Vigil", r'\bAll-Night Vigil\b', [
        ("Vsenichne", r'\bVsenichne\b'),
    ]),
    # Compline
    ("Compline", r'\bCompline\b', [
        ("Povechiria", r'\bPovechiria\b'),
    ]),
    # Midnight Office
    ("Midnight Office", r'\bMidnight Office\b', [
        ("Pivnichna", r'\bPivnichna\b'),
    ]),
    # Typika
    ("Typika", r'\bTypika\b', [
        ("Obidnytsia", r'\bObidnytsia\b'),
    ]),
]

for canonical, canonical_re, variants in glossary_checks:
    canonical_count = len(re.findall(canonical_re, full_text))
    violations = []
    for vname, vre in variants:
        vc = len(re.findall(vre, full_text))
        if vc > 0:
            violations.append(f"{vname}: {vc}")
    
    status = "OK" if not violations else "*** VIOLATION ***"
    print(f"\n  {canonical}: {canonical_count} occurrences  [{status}]")
    for v in violations:
        print(f"    REJECTED VARIANT FOUND -> {v}")

# =========================================================================
# 2. HIERATIC PRONOUN CHECK — Deity capitalization
# =========================================================================
print("\n\n### 2. HIERATIC PRONOUN / DEITY CAPITALIZATION ###")

# Check for Thee/Thou/Thy/Thine usage
for pron, pat in [
    ("Thee", r'\bThee\b'), ("Thou", r'\bThou\b'),
    ("Thy", r'\bThy\b'), ("Thine", r'\bThine\b'),
    ("Hast", r'\bHast\b'), ("Wast", r'\bWast\b'),
]:
    c = len(re.findall(pat, full_text))
    print(f"  {pron}: {c}")

# =========================================================================
# 3. MENAION/CALENDAR SYMBOLS — Special formatting
# =========================================================================
print("\n\n### 3. CALENDAR SYMBOL PRESERVATION ###")
# Check for Влк, Тр, А-Є markers in Part 3 (Menaion)
menaion_text = corpus.get('Final_Dolnytsky_part3_menaion.txt', '')
for sym, pat in [
    ("= (Feast of Lord)", r'^=', ),
    ("+ (Polyeleos)", r'^\+',),
    ("Влк", r'Влк'),
    ("Тр", r'\bТр\b'),
    ("А-Є", r'А-Є'),
    ("ALL CAPS lines", None),
    ("Bold markers", None),
]:
    if pat:
        c = len(re.findall(pat, menaion_text, re.MULTILINE))
        print(f"  {sym}: {c}")

# =========================================================================
# 4. FOOTNOTE MIXED CONTENT — Foreign citations in original script
# =========================================================================
print("\n\n### 4. FOOTNOTE FOREIGN CITATION PRESERVATION ###")
fn_text = corpus.get('Final_footnotes.txt', '')
# Count Greek characters (should be many - foreign citations preserved)
greek_chars = len(re.findall(r'[\u0370-\u03FF\u1F00-\u1FFF]', fn_text))
# Count Cyrillic characters
cyrillic_chars = len(re.findall(r'[\u0400-\u04FF]', fn_text))
latin_liturgical = len(re.findall(r'\b[A-Z][a-z]*\b', fn_text))
print(f"  Greek characters in footnotes: {greek_chars}")
print(f"  Cyrillic characters in footnotes: {cyrillic_chars}")
print(f"  (Foreign citations appear preserved: {'YES' if greek_chars > 100 else 'NEEDS REVIEW'})")

# =========================================================================
# 5. HISTORICAL FIDELITY — Latin-derived terms kept as written
# =========================================================================
print("\n\n### 5. HISTORICAL FIDELITY (Latin-derived terms) ###")
for term, pat in [
    ("Monstrance", r'\bMonstrance\b'),
    ("Dalmatic", r'\b[Dd]almatic\b'),
    ("Orarion", r'\bOrarion\b'),
    ("Epitrachelion", r'\b[Ee]pitrachelion\b'),
    ("Phelonion", r'\b[Pp]helonion\b'),
    ("Sticharion", r'\b[Ss]ticharion\b'),
]:
    c = len(re.findall(pat, full_text))
    print(f"  {term}: {c}")

# =========================================================================
# 6. UNTRANSLATED UKRAINIAN RESIDUE — should be zero
# =========================================================================
print("\n\n### 6. UNTRANSLATED UKRAINIAN RESIDUE CHECK ###")
# Check for common Ukrainian words that should have been translated
body_text = ""
for name, t in corpus.items():
    if name != 'Final_footnotes.txt':  # footnotes have intentional Cyrillic
        body_text += t + "\n"

cyrillic_in_body = re.findall(r'[а-яА-ЯіІїЇєЄґҐ]{3,}', body_text)
# Filter out known intentional Cyrillic (like "Влк", "Тр")
intentional = {'Влк', 'Тр'}
residue = [w for w in cyrillic_in_body if w not in intentional]
print(f"  Cyrillic words in body text (excl. footnotes): {len(residue)}")
if residue[:20]:
    print(f"  Sample: {residue[:20]}")

# =========================================================================
# 7. STRUCTURE FIDELITY — paragraph/enumeration check
# =========================================================================
print("\n\n### 7. KEY STRUCTURAL METRICS ###")
for name, t in corpus.items():
    if not name.endswith('.txt'):
        continue
    lines = t.split('\n')
    non_empty = [l for l in lines if l.strip()]
    fn_markers = len(re.findall(r'\[\^[\w]+\]', t))
    print(f"  {name}: {len(lines)} lines, {len(non_empty)} non-empty, {fn_markers} footnote refs")

print("\n" + "=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)
