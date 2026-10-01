import json
import os
import re

almanac_path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\json_db\almanac\annual_almanac_2026.json"

with open(almanac_path, "r", encoding="utf-8") as f:
    data = json.load(f)

unique_comms = set()
for date_str, day_data in data.get("days", {}).items():
    comm = day_data.get("dolnytsky_commemoration")
    if comm and comm != "None":
        unique_comms.add(comm)

saint_parts = set()
for comm in unique_comms:
    parts = re.split(r'\s+and\s+|\s+&\s+|;', comm, flags=re.IGNORECASE)
    for p in parts:
        p_clean = p.strip().strip('*').strip()
        if p_clean:
            saint_parts.add(p_clean)

def get_liturgical_category(name):
    n = name.lower()
    
    # 1. Strip out "equal-to-the-apostles" or "equal to the apostles" for plural/category checks
    n_for_plural = re.sub(r'equal[- ]to[- ]the[- ]apostles?', '', n)
    
    # Plural indicators
    is_plural = False
    
    # Check for plural keywords using word boundaries
    plural_keywords = [
        r'\bmartyrs\b', r'\bapostles\b', r'\bprophets\b', r'\bvenerables\b', 
        r'\bsaints\b', r'\bfathers\b', r'\bhierarchs\b', r'\bunmercenaries\b',
        r'\bcompanions\b', r'\bothers\b', r'\bfellows\b', r'\bwomen\b', r'\bmonastics\b'
    ]
    if any(re.search(pattern, n_for_plural) for pattern in plural_keywords):
        is_plural = True
    elif re.search(r'\bsts\b', n_for_plural):
        is_plural = True
    elif re.search(r'\band\b', n_for_plural) or '&' in n_for_plural:
        is_plural = True
    elif 'those with' in n_for_plural or 'companion' in n_for_plural:
        is_plural = True
    elif ',' in n_for_plural:
        parts = n_for_plural.split(',')
        if len(parts) > 1:
            after_comma = parts[1].strip()
            singular_titles = ['bishop', 'pope', 'abbot', 'monk', 'nun', 'martyr', 'hierarch', 'archbishop', 'metropolitan', 'patriarch', 'priest', 'deacon', 'king', 'prince', 'writer', 'disciple', 'apostle', 'forerunner']
            is_title = any(after_comma.startswith(t) for t in singular_titles)
            if not is_title:
                is_plural = True

    # 2. Check categories by priority with word boundaries
    # Forerunner
    if re.search(r'\bforerunner\b', n):
        return 'Forerunner'
    # Cross
    if re.search(r'\bcross\b', n):
        return 'Cross'
    # Angels
    if re.search(r'\bangels?\b|\barchangels?\b', n):
        return 'Angels'
    # Fools for Christ
    if re.search(r'\bfools?\b', n):
        return 'Fools for Christ' if is_plural else 'Fool for Christ'
    # Hieromartyr
    if re.search(r'\bhieromartyrs?\b', n):
        return 'Hieromartyrs' if is_plural else 'Hieromartyr'
    # Venerable Martyr
    if (
        re.search(r'\bvenerable[- ]martyrs?\b', n) or 
        re.search(r'\bmonk[- ]martyrs?\b', n) or 
        re.search(r'\bnun[- ]martyrs?\b', n) or 
        (re.search(r'\bven\b\.?', n) and re.search(r'\bmart\b\.?|\bmartyr\b', n))
    ):
        return 'Venerable Martyrs' if is_plural else 'Venerable Martyr'
    # Venerable Woman
    if re.search(r'\bvenerable[- ]women\b|\bnuns\b', n):
        return 'Venerable Women'
    if re.search(r'\bvenerable[- ]woman\b|\bnun\b', n):
        return 'Venerable Woman'
    # Venerable
    if (
        re.search(r'\bven\b\.?|\bvenerables?\b', n) or 
        re.search(r'\babbots?\b|\bmonastics?\b|\bmonks?\b', n)
    ):
        return 'Venerables' if is_plural else 'Venerable'
    # Hierarch
    if (
        re.search(r'\bbp\b\.?|\bbishops?\b|\bhierarchs?\b', n) or 
        re.search(r'\barchbishops?\b|\bmetropolitans?\b|\bpatriarchs?\b|\bpopes?\b', n)
    ):
        return 'Hierarchs' if is_plural else 'Hierarch'
    # Woman Martyr
    if re.search(r'\bmartyresses\b|\bwomen[- ]martyrs\b', n):
        return 'Women Martyrs'
    if re.search(r'\bmartyress\b|\bwoman[- ]martyr\b', n):
        return 'Woman Martyr'
    # Martyr
    if (
        re.search(r'\bmart\b\.?|\bmartyrs?\b', n) or 
        re.search(r'\bgreat[- ]martyrs?\b|\bgreatmartyrs?\b|\bprotomartyrs?\b', n)
    ):
        return 'Martyrs' if is_plural else 'Martyr'
    # Apostle
    if (
        re.search(r'\bap\b\.?|\bapostles?\b|\bevangelists?\b', n)
    ):
        return 'Apostles' if is_plural else 'Apostle'
    # Prophet
    if re.search(r'\bprophets?\b|\bprophetesses?\b|\bprop\b\.?', n):
        return 'Prophets' if is_plural else 'Prophet'
    # Unmercenary
    if re.search(r'\bunmercenar', n):
        return 'Unmercenaries' if is_plural else 'Unmercenary'
    # Holy Fathers
    if re.search(r'\bfathers\b', n):
        return 'Holy Fathers'
        
    # Default to Saint
    return 'Saints' if is_plural else 'Saint'

categorized = {}
for name in sorted(saint_parts):
    cat = get_liturgical_category(name)
    categorized.setdefault(cat, []).append(name)

# Print a summary of everything
for cat, names in sorted(categorized.items()):
    print(f"\n=== {cat} (Count: {len(names)}) ===")
    for n in names:
        print(f"  - {n}")
