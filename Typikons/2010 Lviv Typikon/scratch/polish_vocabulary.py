import re
import os

# Master Glossary
GLOSSARY = {
    r'\bOko Tserkovne\b': 'Tserkovne Oko',
    r'\bAntolohion\b': 'Anthologion',
    r'\bTrefologion\b': 'Anthologion',
    r'\bMineya\b': 'Menaion',
    r'\bVsenichne\b': 'All-Night Vigil',
    r'\bPovechiri[ay]\b': 'Compline',
    r'\bPivnichna\b': 'Midnight Office',
    r'\bObidnytsia\b': 'Typika',
    r'\bSidalen\b': 'Sessional Hymn',
    r'\bSidalnyi\b': 'Sessional Hymn',
    r'\bKondak\b': 'Kontakion',
    r'\bKondakia\b': 'Kontakia',
    r'\bNaslavnik\b': 'Doxastikon',
    r'\bBohorodychnyi\b': 'Theotokion',
    r'\bKhvalytni\b': 'Praises',
    r'\bStykhivnia\b': 'Aposticha',
    r'\bStepenna\b': 'Gradual',
    r'\bSvitylny\b': 'Exaposteilarion',
    r'\bSlavoslovya\b': 'Doxology',
    r'\bSamohlasen\b': 'Idiomelon',
    r'\bSamohlasnyi\b': 'Idiomelon',
    r'\bPodiben\b': 'Prosomoion',
    r'\bVelychannye\b': 'Magnification',
    r'\bPolyeley\b': 'Polyeleos',
    r'\bBezpolieleyinyi\b': 'Without Polyeleos',
    r'\bHlas\b': 'Tone',
    r'\bPeredsviattia\b': 'Forefeast',
    r'\bPosviattia\b': 'Afterfeast',
    r'\bViddannia\b': 'Apodosis',
    r'\bSviato\b': 'Feast',
    r'\bPlaschanitsa\b': 'Shroud',
}

# Phase 4 Titles - Universal Capitalization (Ecclesiastical & Secular)
TITLES = [
    'Emperor', 'Pope', 'Metropolitan', 'Bishop', 'Patriarch', 'Exarch', 
    'Rector', 'Archimandrite', 'Hegumen', 'Abbot', 'Spiritual Father',
    'Pontiff', 'Tsar', 'Prince', 'Priest', 'Deacon', 'Choir', 'Singer',
    'Reader', 'Cantor', 'Psalmist', 'Superior', 'Ecclesiarch'
]

DEITY_CONTEXTS = [
    r'\b(God|Lord|Christ|Jesus|Savior|Almighty|Father|Son|Spirit|Thee|Thou|Thy)\s+(who|whom)\b',
    r'\b(God|Lord|Christ|Jesus|Savior|Almighty|Father|Son|Spirit|Thee|Thou|Thy)\s+([Hh])e\b',
    r'\b(He|Who)\s+Who\s+([Hh])as\b',
    r'\b(Lord|Christ|Jesus)\s+(is|was|has|had|does|did)\s+\b(he|him|his)\b',
    r'\b(Thee|Thou|Thy|Thine),\s+\b(who|whom)\b',
]

HIERATIC_PRONOUNS = {
    r'\bthee\b': 'Thee',
    r'\bthou\b': 'Thou',
    r'\bthy\b': 'Thy',
    r'\bthine\b': 'Thine',
    r'\bhast\b': 'Hast',
    r'\bart\b': 'Art',
    r'\bwast\b': 'Wast',
    r'\bshalt\b': 'Shalt',
}

SERVICES = {
    r'\bgreat vespers\b': 'Great Vespers',
    r'\bdaily vespers\b': 'Daily Vespers',
    r'\blenten matins\b': 'Lenten Matins',
    r'\bgreat compline\b': 'Great Compline',
    r'\bsmall compline\b': 'Small Compline',
    r'\ball-night vigil\b': 'All-Night Vigil',
    r'\bmidnight office\b': 'Midnight Office',
    r'\bdaily matins\b': 'Daily Matins',
    r'\bgreat matins\b': 'Great Matins',
    r'\bholy liturgy\b': 'Holy Liturgy',
    r'\bdivine liturgy\b': 'Divine Liturgy',
    r'\bgreat litany\b': 'Great Litany',
    r'\bsmall litany\b': 'Small Litany',
    r'\baugmented litany\b': 'Augmented Litany',
    r'\blitany of supplication\b': 'Litany of Supplication',
}

def clean_characters(text):
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u2013', '-').replace('\u2014', '--')
    text = text.replace('\u00a0', ' ').replace('\u2003', ' ').replace('\u2002', ' ')
    text = text.replace('\ufffd', '') 
    text = re.sub(r'\s+([,;:?.])', r'\1', text) 
    text = re.sub(r'([,;:?.])([a-zA-Z])', r'\1 \2', text)
    return text

def polish_text(text):
    text = clean_characters(text)
    for pattern, replacement in GLOSSARY.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    def deity_cap(match):
        return match.group(1) + " " + match.group(2).capitalize()
    
    def deity_comma_cap(match):
        return match.group(1) + ", " + match.group(2).capitalize()

    for pattern in DEITY_CONTEXTS:
        if ',' in pattern:
            text = re.sub(pattern, deity_comma_cap, text)
        else:
            text = re.sub(pattern, deity_cap, text)

    for pattern, replacement in HIERATIC_PRONOUNS.items():
        text = re.sub(pattern, replacement, text)

    for title in TITLES:
        text = re.sub(r'\b(the|a|every|each|by|with|to)\s+\b' + title.lower() + r'\b', 
                      r'\1 ' + title, text, flags=re.IGNORECASE)
        # Handle start of sentence or standalone in rubrics
        text = re.sub(r'\b' + title.lower() + r'\b\s+\b(says|exclaims|shall|takes|blesses|does|reads|signs|makes|is)\b', 
                      title + r' \1', text, flags=re.IGNORECASE)

    for pattern, replacement in SERVICES.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    text = re.sub(r'\bGod is Lord\b', 'God is the Lord', text, flags=re.IGNORECASE)
    text = re.sub(r'\bHexapsalmos\b', 'Six Psalms', text, flags=re.IGNORECASE)
    return text

def process_file(filepath):
    print(f"Polishing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        polished = polish_text(content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(polished)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    root = 'e:/Google Antigravity/Projects/Translation/English Broken'
    for f in os.listdir(root):
        if f.endswith('.txt'):
            process_file(os.path.join(root, f))
