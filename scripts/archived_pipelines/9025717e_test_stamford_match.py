import json
import os
import re
import sys

def normalize_text(text):
    text = text.lower()
    text = text.replace('*', ' ')
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    return words

def jaccard_similarity(words1, words2):
    set1 = set(words1)
    set2 = set(words2)
    if not set1 and not set2:
        return 0.0
    return len(set1.intersection(set2)) / len(set1.union(set2))

def parse_stamford_troparia(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    start = content.find('[')
    end = content.rfind(']')
    data = json.loads(content[start:end+1])
    
    current_month = None
    current_feast = None
    extracted = []
    
    for idx, item in enumerate(data):
        for k, v in item.items():
            v_str = str(v).strip()
            if k in ['feast', 'rubric'] and v_str.upper() in ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']:
                current_month = v_str.upper()
                current_feast = None
            elif k == 'sticheron_1' and idx == 3: # Special first item
                current_feast = v_str
            elif k.startswith('sticheron_') or k == 'rubric':
                is_hymn = any(h in v_str.lower() for h in ['troparion', 'kontakion', 'dismissal'])
                if not is_hymn:
                    current_feast = v_str
                else:
                    parts = v_str.split(':', 1)
                    hymn_header = parts[0].strip()
                    hymn_content = parts[1].strip() if len(parts) > 1 else ''
                    extracted.append({
                        'index': idx,
                        'month': current_month,
                        'feast': current_feast,
                        'header': hymn_header,
                        'content': hymn_content
                    })
    return extracted

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Load Royal Doors
    with open(r'c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Festal Propers Comparisons\text_royaldoors.json', 'r', encoding='utf-8') as f:
        rd_data = json.load(f)
    
    # Pre-tokenize all Royal Doors entries
    rd_entries = []
    for k, v in rd_data.items():
        content = v.get('content', '')
        if not content:
            continue
        # Strip metadata prefixes like *Troparion, Tone 1:* from Royal Doors if present
        clean_content = re.sub(r'^\*?(Troparion|Kontakion|Dismissal)[^*:]*:\*?\s*', '', content, flags=re.IGNORECASE)
        rd_entries.append({
            'key': k,
            'source': v.get('source', ''),
            'content': clean_content,
            'words': normalize_text(clean_content)
        })
        
    # Load Stamford
    stamford_path = r'c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Recensions\Stamford Divine Office\JSON_MD\TROPARIA MENAION.md'
    stamford_hymns = parse_stamford_troparia(stamford_path)
    
    print(f"Loaded {len(stamford_hymns)} Stamford hymns and {len(rd_entries)} Royal Doors entries.")
    
    # Test match first 30 Stamford hymns
    matched_count = 0
    for sh in stamford_hymns[:30]:
        sh_words = normalize_text(sh['content'])
        best_score = 0.0
        best_match = None
        
        for rd in rd_entries:
            score = jaccard_similarity(sh_words, rd['words'])
            if score > best_score:
                best_score = score
                best_match = rd
                
        if best_score >= 0.4:
            matched_count += 1
            print(f"MATCH ({best_score:.2f}):")
            print(f"  Stamford: [{sh['month']}] [{sh['feast']}] {sh['header']} -> {sh['content'][:60]}...")
            print(f"  Royal Doors: Key={best_match['key']} -> {best_match['content'][:60]}...")
        else:
            print(f"NO MATCH (best {best_score:.2f}):")
            print(f"  Stamford: [{sh['month']}] [{sh['feast']}] {sh['header']} -> {sh['content'][:60]}...")
            if best_match:
                print(f"  Best RD: Key={best_match['key']} -> {best_match['content'][:60]}...")

    print(f"Matched {matched_count}/30 tested hymns.")

if __name__ == '__main__':
    main()
