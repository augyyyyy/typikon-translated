import json
import os
import re
import sys

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return set(text.split())

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Load Royal Doors
    with open('text_royaldoors.json', 'r', encoding='utf-8') as f:
        rd_data = json.load(f)
        
    # Extract unique (MM_DD, slug) from Royal Doors
    rd_slugs = {}
    for k in rd_data.keys():
        parts = k.split('.')
        if len(parts) >= 3:
            date_str = parts[1]
            slug = parts[2]
            if '_' in date_str and len(date_str) == 10:
                mm_dd = date_str[5:] # MM_DD
                rd_slugs[slug] = mm_dd
                
    print(f"Extracted {len(rd_slugs)} unique slugs from Royal Doors.")
    
    # Load Stamford
    stamford_path = r'c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Recensions\Stamford Divine Office\JSON_MD\TROPARIA MENAION.md'
    with open(stamford_path, 'r', encoding='utf-8') as f:
        text = f.read()
    start = text.find('[')
    end = text.rfind(']')
    data = json.loads(text[start:end+1])
    
    current_month = None
    comms = []
    for idx, item in enumerate(data):
        for k, v in item.items():
            v_str = str(v).strip()
            if k in ['feast', 'rubric'] and v_str.upper() in ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']:
                current_month = v_str.upper()
            elif (k.startswith('sticheron_') or k == 'rubric') and current_month:
                is_hymn = any(h in v_str.lower() for h in ['troparion', 'kontakion', 'dismissal'])
                is_metadata = any(m in v_str.lower() for m in ['readings at vespers', 'for readings'])
                if not is_hymn and not is_metadata and len(v_str) > 5:
                    comms.append((v_str, current_month, idx))
                    
    print(f"Loaded {len(comms)} Stamford commemorations.")
    
    # Test match first 20 Stamford commemorations
    for title, month, idx in comms[:30]:
        title_words = normalize_text(title)
        best_slug = None
        best_mm_dd = None
        best_overlap = 0
        
        for slug, mm_dd in rd_slugs.items():
            slug_words = normalize_text(slug.replace('_', ' '))
            overlap = len(title_words.intersection(slug_words))
            if overlap > best_overlap:
                best_overlap = overlap
                best_slug = slug
                best_mm_dd = mm_dd
                
        print(f"Index {idx} [{month}]: \"{title[:60]}...\"")
        print(f"  -> Matched RD Date: {best_mm_dd} (overlap={best_overlap}, slug={best_slug})")

if __name__ == '__main__':
    main()
