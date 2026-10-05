#!/usr/bin/env python3
"""
Full terminology drift audit across all Final files.
Checks every known liturgical term for variant forms.
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')

final_dir = r'c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\Final'

checks = [
    # --- Church Eye / Tserkovne Oko ---
    ('Church Eye', r'\bChurch Eye\b'),
    ('Eye of the Church', r'\bEye of the Church\b'),
    ('Tserkovne Oko', r'\bTserkovne Oko\b'),
    ('Oko Tserkovne', r'\bOko Tserkovne\b'),

    # --- Horologion / Book of Hours ---
    ('Horologion', r'\bHorologion\b'),
    ('Chasoslov', r'\bChasoslov\b'),
    ('Book of Hours', r'\bBook of Hours\b'),
    ('Horo- and Prayer Book', r'\bHoro- and Prayer Book\b'),

    # --- Service Book / Sluzhebnik / Euchologion ---
    ('Sluzhebnik', r'\bSluzhebnik\b'),
    ('Service Book', r'\bService Book\b'),
    ('Euchologion', r'\bEuchologion\b'),

    # --- Octoechos ---
    ('Octoechos', r'\bOctoechos\b'),
    ('Oktoikh', r'\bOktoikh\b'),

    # --- Menaion ---
    ('Menaion', r'\bMenaion\b'),
    ('Menaia', r'\bMenaia\b'),
    ('Mineia', r'\bMineia\b'),

    # --- Triodion ---
    ('Triodion', r'\bTriodion\b'),
    ('Triodia', r'\bTriodia\b'),
    ('Triod', r'(?<!\w)Triod(?!\w|i|o)'),

    # --- Anthologion / Trephologion ---
    ('Anthologion', r'\bAnthologion\b'),
    ('Trephologion', r'\bTrephologion\b'),
    ('Trefoloy', r'\bTrefoloy\b'),

    # --- Irmos / Heirmos ---
    ('Irmos', r'\bIrmos\b'),
    ('Heirmos', r'\bHeirmos\b'),
    ('Irmoi', r'\bIrmoi\b'),
    ('Heirmoi', r'\bHeirmoi\b'),
    ('Irmologion', r'\bIrmologion\b'),
    ('Heirmologion', r'\bHeirmologion\b'),

    # --- Litiya ---
    ('Litiya', r'\bLitiya\b'),
    ('Litia', r'\bLitia\b'),
    ('Lity', r'\bLity\b'),

    # --- Prokimenon ---
    ('Prokimenon', r'\bProkimenon\b'),
    ('Prokeimenon', r'\bProkeimenon\b'),

    # --- Apodosis / Leavetaking ---
    ('Apodosis', r'\bApodosis\b'),
    ('Leavetaking', r'\bLeavetaking\b'),
    ('Leave-taking', r'\bLeave-taking\b'),
    ('Leave taking', r'\bLeave taking\b'),

    # --- Epitaphios / Shroud ---
    ('Epitaphios', r'\bEpitaphios\b'),
    ('Shroud', r'\bShroud\b'),

    # --- Kontakion / Kondak ---
    ('Kontakion', r'\bKontakion\b'),
    ('Kondak', r'\bKondak\b'),

    # --- Sessional Hymn / Sedalen ---
    ('Sessional Hymn', r'\bSessional [Hh]ymn\b'),
    ('Sedalen', r'\bSedalen\b'),
    ('Sidal', r'\bSidal\b'),

    # --- Exaposteilarion ---
    ('Exaposteilarion', r'\bExaposteilarion\b'),
    ('Exapostilarion', r'\bExapostilarion\b'),
    ('Svetilen', r'\bSvetilen\b'),
    ('Hymn of Light', r'\bHymn of Light\b'),

    # --- Communion Hymn ---
    ('Communion Hymn', r'\bCommunion [Hh]ymn\b'),
    ('Koinonikon', r'\bKoinonikon\b'),
    ('Prichasten', r'\bPrichasten\b'),

    # --- Katavasia ---
    ('Katavasia', r'\bKatavasia\b'),
    ('Katavasiae', r'\bKatavasiae\b'),
    ('Katavasi', r'\bKatavasi(?:e|a)s\b'),
    
    # --- Polyeleos ---
    ('Polyeleos', r'\bPolyeleos\b'),
    ('Polyeleios', r'\bPolyeleios\b'),
    ('Polieleos', r'\bPolieleos\b'),

    # --- Doxology ---
    ('Doxology', r'\bDoxology\b'),
    ('Slavoslovie', r'\bSlavoslovie\b'),

    # --- Theotokion ---
    ('Theotokion', r'\bTheotokion\b'),
    ('Theotokia', r'\bTheotokia\b'),
    ('Bogorodichen', r'\bBogorodichen\b'),

    # --- Troparion ---
    ('Troparion', r'\bTroparion\b'),
    ('Troparia', r'\bTroparia\b'),
    ('Tropar', r'(?<!\w)Tropar(?!\w|i|o)'),

    # --- Stichera ---
    ('Stichera', r'\bStichera\b'),
    ('Sticheron', r'\bSticheron\b'),
    ('Stikhira', r'\bStikhira\b'),

    # --- Kathisma ---
    ('Kathisma', r'\bKathisma\b'),
    ('Kafisma', r'\bKafisma\b'),
    ('Kafizma', r'\bKafizma\b'),
    ('Katisma', r'\bKatisma\b'),

    # --- Dismissal Theotokion ---
    ('Dismissal Theotokion', r'\bDismissal Theotokion\b'),
    ('Otpustitel Bogorodichen', r'\bOtpustitel\b'),

    # --- Doxastikon ---
    ('Doxastikon', r'\bDoxastikon\b'),
    ('Slavnik', r'\bSlavnik\b'),

    # --- Praises ---
    ('Praises', r'\bPraises\b'),
    ('Khvalitni', r'\bKhvalitni\b'),
    ('Lauds', r'\bLauds\b'),

    # --- Aposticha ---
    ('Aposticha', r'\bAposticha\b'),
    ('Stikhovni', r'\bStikhovni\b'),

    # --- Pochayiv / Pochaiv ---
    ('Pochayiv', r'\bPochayiv\b'),
    ('Pochaiv', r'\bPochaiv\b'),
    ('Pochaev', r'\bPochaev\b'),

    # --- Tetrapod ---
    ('Tetrapod', r'\bTetrapod\b'),
    ('Tetrapode', r'\bTetrapode\b'),

    # --- Krylos ---
    ('Krylos', r'\bKrylos\b'),
    ('Kryloi', r'\bKryloi\b'),
    ('Kliros', r'\bKliros\b'),
    ('Kliroi', r'\bKliroi\b'),

    # =============================================
    # NEW: System Instruction terms not previously tracked
    # =============================================

    # --- Idiomelon / Samohlasen ---
    ('Idiomelon', r'\bIdiomelon\b'),
    ('Idiomela', r'\bIdiomela\b'),
    ('Samohlasen', r'\bSamohlasen\b'),
    ('Samohlasnyi', r'\bSamohlasnyi\b'),

    # --- Prosomoion / Podiben ---
    ('Prosomoion', r'\bProsomoion\b'),
    ('Prosomoia', r'\bProsomoia\b'),
    ('Podiben', r'\bPodiben\b'),

    # --- Magnification / Megalynaria ---
    ('Magnification', r'\bMagnification\b'),
    ('Megalynaria', r'\bMegalynaria\b'),
    ('Velychannye', r'\bVelychannye\b'),

    # --- Gradual / Stepenna ---
    ('Gradual', r'\bGradual\b'),
    ('Stepenna', r'\bStepenna\b'),
    ('Anabathmoi', r'\bAnabathmoi\b'),

    # --- Forefeast / Afterfeast ---
    ('Forefeast', r'\bForefeast\b'),
    ('Peredsviattia', r'\bPeredsviattia\b'),
    ('Afterfeast', r'\bAfterfeast\b'),
    ('Posviattia', r'\bPosviattia\b'),

    # --- Shroud / Epitaphios / Plaschanitsa ---
    ('Plaschanitsa', r'\bPlaschanitsa\b'),
    ('Plashchanitsa', r'\bPlashchanitsa\b'),

    # --- Sluzhebnik / Service Book ---
    ('Sluzhebnik', r'\bSluzhebnik\b'),
    ('Sluzhebnyky', r'\bSluzhebnyky\b'),
    ('Service Book', r'\bService Book\b'),
    ('Service Books', r'\bService Books\b'),

    # --- Compline / Povechiria ---
    ('Compline', r'\bCompline\b'),
    ('Povechiria', r'\bPovechiria\b'),

    # --- Midnight Office / Pivnichna ---
    ('Midnight Office', r'\bMidnight Office\b'),
    ('Pivnichna', r'\bPivnichna\b'),

    # --- Typika / Obidnytsia ---
    ('Typika', r'\bTypika\b'),
    ('Obidnytsia', r'\bObidnytsia\b'),

    # --- All-Night Vigil ---
    ('All-Night Vigil', r'\bAll-Night Vigil\b'),
    ('Vsenichne', r'\bVsenichne\b'),

    # --- Tserkovne Oko (post-unification) ---
    ('Tserkovne Oko', r'\bTserkovne Oko\b'),
    ('Eye of the Church', r'\bEye of the Church\b'),
]

# Per-file results
results = {}
for name in sorted(os.listdir(final_dir)):
    if not name.endswith('.txt'): continue
    with open(os.path.join(final_dir, name), 'r', encoding='utf-8') as f:
        text = f.read()
    file_results = {}
    for label, pat in checks:
        c = len(re.findall(pat, text, re.IGNORECASE))
        if c > 0:
            file_results[label] = c
    if file_results:
        results[name] = file_results

# Print per-file
for fname, terms in results.items():
    print(f'\n=== {fname} ===')
    for term, count in sorted(terms.items()):
        print(f'  {term}: {count}')

# Print grouped by concept (terms that compete)
print('\n\n========== DRIFT GROUPS ==========')
groups = {
    'Tserkovne Oko': ['Tserkovne Oko', 'Eye of the Church', 'Church Eye', 'Oko Tserkovne'],
    'Irmos': ['Irmos', 'Heirmos', 'Irmoi', 'Heirmoi', 'Irmologion', 'Heirmologion'],
    'Litiya': ['Litiya', 'Litia', 'Lity'],
    'Prokimenon': ['Prokimenon', 'Prokeimenon'],
    'Apodosis': ['Apodosis', 'Leavetaking', 'Leave-taking', 'Leave taking'],
    'Pochayiv': ['Pochayiv', 'Pochaiv', 'Pochaev'],
    'Anthologion': ['Anthologion', 'Trephologion', 'Trefoloy'],
    'Krylos': ['Krylos', 'Kryloi', 'Kliros', 'Kliroi'],
    'Polyeleos': ['Polyeleos', 'Polyeleios', 'Polieleos'],
    'Kathisma': ['Kathisma', 'Kafisma', 'Kafizma', 'Katisma'],
    # NEW groups
    'Idiomelon': ['Idiomelon', 'Idiomela', 'Samohlasen', 'Samohlasnyi'],
    'Prosomoion': ['Prosomoion', 'Prosomoia', 'Podiben'],
    'Magnification': ['Magnification', 'Megalynaria', 'Velychannye'],
    'Gradual': ['Gradual', 'Stepenna', 'Anabathmoi'],
    'Forefeast': ['Forefeast', 'Peredsviattia'],
    'Afterfeast': ['Afterfeast', 'Posviattia'],
    'Shroud': ['Shroud', 'Epitaphios', 'Plaschanitsa', 'Plashchanitsa'],
    'Sluzhebnik': ['Sluzhebnik', 'Sluzhebnyky', 'Service Book', 'Service Books'],
    'Compline': ['Compline', 'Povechiria'],
    'Midnight Office': ['Midnight Office', 'Pivnichna'],
    'Typika': ['Typika', 'Obidnytsia'],
    'All-Night Vigil': ['All-Night Vigil', 'Vsenichne'],
}

grand_totals = {}
for label, pat in checks:
    total = 0
    for fname, terms in results.items():
        total += terms.get(label, 0)
    if total > 0:
        grand_totals[label] = total

for group_name, members in groups.items():
    found = {m: grand_totals.get(m, 0) for m in members if grand_totals.get(m, 0) > 0}
    if len(found) > 1:  # Drift detected!
        print(f'\n  *** DRIFT: {group_name} ***')
        for term, count in found.items():
            print(f'    {term}: {count}')
    elif len(found) == 1:
        term, count = list(found.items())[0]
        print(f'\n  OK: {group_name} -> unified as "{term}" ({count})')
    else:
        print(f'\n  UNUSED: {group_name}')
