import json
import os
import re
import sys

def normalize_text(text):
    text = text.lower()
    text = text.replace('*', ' ')
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.split()

def jaccard_similarity(words1, words2):
    set1 = set(words1)
    set2 = set(words2)
    if not set1 and not set2:
        return 0.0
    return len(set1.intersection(set2)) / len(set1.union(set2))

def get_is_hymn(v_str):
    if ':' in v_str:
        prefix = v_str.split(':', 1)[0].lower()
        if any(h in prefix for h in ['troparion', 'kontakion', 'dismissal', 'hypakoe']):
            return True
    return False

def parse_blocks(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    start = content.find('[')
    end = content.rfind(']')
    data = json.loads(content[start:end+1])
    
    months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
    current_month = None
    blocks = []
    current_block = None
    
    for idx, item in enumerate(data):
        for k, v in item.items():
            v_str = str(v).strip()
            if k in ['feast', 'rubric'] and v_str.upper() in months:
                current_month = v_str.upper()
            elif (k.startswith('sticheron_') or k == 'rubric') and current_month:
                is_hymn = get_is_hymn(v_str)
                is_metadata = any(m in v_str.lower() for m in ['readings at vespers', 'for readings'])
                if is_metadata:
                    continue
                
                if not is_hymn:
                    # New commemoration block
                    if current_block:
                        blocks.append(current_block)
                    current_block = {
                        'month': current_month,
                        'title': v_str,
                        'hymns': [],
                        'start_index': idx
                    }
                else:
                    # It's a hymn belonging to the current block
                    if not current_block:
                        current_block = {
                            'month': current_month,
                            'title': 'Pre-month Hymn',
                            'hymns': [],
                            'start_index': idx
                        }
                    parts = v_str.split(':', 1)
                    hymn_header = parts[0].strip()
                    hymn_content = parts[1].strip() if len(parts) > 1 else ''
                    current_block['hymns'].append({
                        'header': hymn_header,
                        'content': hymn_content
                    })
    if current_block:
        blocks.append(current_block)
    return blocks

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Load Royal Doors
    with open('text_royaldoors.json', 'r', encoding='utf-8') as f:
        rd_data = json.load(f)
        
    # Pre-tokenize all Royal Doors entries
    rd_entries = []
    for k, v in rd_data.items():
        content = v.get('content', '')
        if not content:
            continue
        # Strip metadata prefix
        clean_content = re.sub(r'^\*?(Troparion|Kontakion|Dismissal)[^*:]*:\*?\s*', '', content, flags=re.IGNORECASE)
        # Parse MM_DD from key
        parts = k.split('.')
        date_str = parts[1]
        mm_dd = None
        if '_' in date_str and len(date_str) == 10:
            mm_dd = date_str[5:]
        rd_entries.append({
            'key': k,
            'mm_dd': mm_dd,
            'content': clean_content,
            'words': normalize_text(clean_content)
        })
        
    # Load Stamford blocks
    stamford_path = r'c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Recensions\Stamford Divine Office\JSON_MD\TROPARIA MENAION.md'
    blocks = parse_blocks(stamford_path)
    print(f"Parsed {len(blocks)} commemoration blocks from Stamford.")
    
    # Match dates
    for b in blocks:
        b['matched_dates'] = []
        for h in b['hymns']:
            h_words = normalize_text(h['content'])
            if len(h_words) < 5:
                continue
            best_score = 0.0
            best_mm_dd = None
            
            for rd in rd_entries:
                score = jaccard_similarity(h_words, rd['words'])
                if score > best_score:
                    best_score = score
                    best_mm_dd = rd['mm_dd']
            if best_score >= 0.35:
                b['matched_dates'].append((best_mm_dd, best_score))
                
        # Determine the date of this block
        if b['matched_dates']:
            # Count frequencies
            freq = {}
            for d, s in b['matched_dates']:
                freq[d] = freq.get(d, 0) + 1
            best_d = max(freq, key=freq.get)
            b['resolved_date'] = best_d
        else:
            b['resolved_date'] = None

    # Interpolate missing dates month-by-month
    month_days = {
        'JANUARY': 31, 'FEBRUARY': 29, 'MARCH': 31, 'APRIL': 30, 'MAY': 31, 'JUNE': 30,
        'JULY': 31, 'AUGUST': 31, 'SEPTEMBER': 30, 'OCTOBER': 31, 'NOVEMBER': 30, 'DECEMBER': 31
    }
    
    # Group by month
    from collections import defaultdict
    by_month = defaultdict(list)
    for b in blocks:
        by_month[b['month']].append(b)
        
    for month, m_blocks in by_month.items():
        print(f"\n=== Interpolating {month} ({len(m_blocks)} blocks) ===")
        # We will scan through and fill in resolved_date
        # First, convert matched MM_DD into integer days
        # E.g. '01_15' -> 15
        for b in m_blocks:
            if b['resolved_date']:
                try:
                    b['day'] = int(b['resolved_date'].split('_')[1])
                except:
                    b['day'] = None
            else:
                b['day'] = None
                
        # Linear fill in days
        # If block 0 has no day, set to 1
        # Then, scan forward: if b[i] has a day, and b[i+k] has a day, fill in between
        # Let's write a simple propagation loop
        last_day = 0
        for i in range(len(m_blocks)):
            if m_blocks[i]['day'] is not None:
                last_day = m_blocks[i]['day']
            else:
                # Find next known day
                next_day = None
                next_idx = None
                for j in range(i + 1, len(m_blocks)):
                    if m_blocks[j]['day'] is not None:
                        next_day = m_blocks[j]['day']
                        next_idx = j
                        break
                
                if next_day is not None:
                    # Interpolate step by step
                    # If last_day < next_day, we increment last_day
                    # otherwise we just keep it or increment slowly
                    step = (next_day - last_day) / (next_idx - i + 1)
                    # Simple interpolation: just increment by 1 if possible, but keep <= next_day
                    day = last_day + 1
                    if day >= next_day:
                        day = next_day - 1 if next_day > 1 else 1
                    m_blocks[i]['day'] = int(day)
                    last_day = day
                else:
                    # No more known days, just increment last_day
                    day = last_day + 1
                    max_d = month_days.get(month, 31)
                    if day > max_d:
                        day = max_d
                    m_blocks[i]['day'] = int(day)
                    last_day = day
                    
        # Update resolved_date
        for b in m_blocks:
            month_num = list(month_days.keys()).index(month) + 1
            b['resolved_date'] = f"{month_num:02d}_{b['day']:02d}"
            print(f"  Day {b['day']:02d} | \"{b['title'][:50]}...\" (resolved={b['resolved_date']})")

if __name__ == '__main__':
    main()
