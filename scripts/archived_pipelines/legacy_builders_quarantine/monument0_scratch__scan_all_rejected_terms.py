import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# Compile all rejected variants from Section 3 of vocabulary_standardization_matrix.md
rejected_terms = [
    'Leavetaking', 'Leave-taking', 'Leave taking', 'Viddannia',
    'Prokeimenon', 'Prokeimena',
    'Irmos', 'Irmoi', 'Irmologion',
    'Litia', 'Lity',
    'Pochayiv', 'Pochaev',
    'Oko Tserkovne', 'Church Eye', 'Eye of the Church',
    'Service Book', 'Service Books',
    'Kafisma', 'Kafizma', 'Katisma',
    'Polyeleios', 'Polieleos', 'Polyeley',
    'Trephologion', 'Trefoloy', 'Antolohion',
    'Krylos', 'Kryloi',
    'Samohlasen', 'Samohlasnyi',
    'Podiben',
    'Velychannye',
    'Peredsviattia', 'Posviattia',
    'Plaschanitsa', 'Plashchanitsa',
    'Povechiria', 'Pivnichna', 'Obidnytsia', 'Vsenichne',
    'Typicon'
]

pattern = re.compile(r'\b(' + '|'.join(re.escape(t) for t in rejected_terms) + r')\b', re.IGNORECASE)

final_md = Path('Final MD')
final_txt = Path('Final')

violations = []
for folder in [final_md, final_txt]:
    for f in sorted(folder.glob('*.*')):
        if f.suffix in ['.md', '.txt'] and 'glossary' not in f.name and 'matrix' not in f.name:
            lines = f.read_text(encoding='utf-8').splitlines()
            for idx, l in enumerate(lines, 1):
                clean_line = re.sub(r'\(lit\.\s*"[^"]+"\)', '', l)
                for m in pattern.finditer(clean_line):
                    violations.append((folder.name, f.name, idx, m.group(0), l[:75]))

print(f"Total rejected vocabulary violations across Final and Final MD: {len(violations)}")
for folder_name, fname, lno, term, ctx in violations:
    print(f"  [{folder_name}] {fname}:L{lno} -> Found \"{term}\" | \"{ctx}\"")
