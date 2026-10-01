import json
import os
import re
import sys

def get_is_hymn(v_str):
    if ':' in v_str:
        prefix = v_str.split(':', 1)[0].lower()
        if any(h in prefix for h in ['troparion', 'kontakion', 'dismissal', 'hypakoe']):
            return True
    return False

def parse_prefix(prefix):
    # e.g., "Troparion of the Circumcision (Tone 1)"
    # e.g., "Kontakion of St. Basil (Tone 4)"
    # e.g., "Dismissal"
    hymn_type = "troparion"
    for h in ['kontakion', 'dismissal', 'hypakoe']:
        if h in prefix.lower():
            hymn_type = h
            
    tone = None
    if '(' in prefix and ')' in prefix:
        start_paren = prefix.find('(')
        end_paren = prefix.find(')', start_paren)
        inside = prefix[start_paren+1:end_paren].strip()
        if 'tone' in inside.lower():
            tone = inside
            
    # Extract rubric (everything except the (Tone X) part)
    rubric = prefix
    if '(' in prefix:
        rubric = prefix[:prefix.find('(')].strip()
        
    return hymn_type, tone, rubric

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
                    if current_block:
                        blocks.append(current_block)
                    current_block = {
                        'month': current_month,
                        'title': v_str,
                        'hymns': [],
                        'start_index': idx
                    }
                else:
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
    
    stamford_path = r'c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Recensions\Stamford Divine Office\JSON_MD\TROPARIA MENAION.md'
    blocks = parse_blocks(stamford_path)
    
    months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
    month_days = {
        'JANUARY': 31, 'FEBRUARY': 29, 'MARCH': 31, 'APRIL': 30, 'MAY': 31, 'JUNE': 30,
        'JULY': 31, 'AUGUST': 31, 'SEPTEMBER': 30, 'OCTOBER': 31, 'NOVEMBER': 30, 'DECEMBER': 31
    }
    
    # Resolve dates
    # We group by month to keep date sequencing independent
    from collections import defaultdict
    by_month = defaultdict(list)
    for b in blocks:
        by_month[b['month']].append(b)
        
    final_db = {}
    
    for month, m_blocks in by_month.items():
        month_num = months.index(month) + 1
        day_of_month = 1
        
        for b in m_blocks:
            title_lower = b['title'].lower()
            
            # 1. Check if rubric
            is_rubric = False
            if (title_lower.startswith('for readings') or 
                title_lower.startswith('for the service') or 
                title_lower.startswith('for the troparion') or 
                title_lower.startswith('for the kontakion') or 
                'readings at vespers' in title_lower or 
                'for reading at vespers' in title_lower):
                is_rubric = True
                
            # 2. Check if movable Sunday
            movable_tag = None
            if 'sunday of christ the king' in title_lower:
                movable_tag = 'christ_the_king'
            elif 'sunday of the holy forefathers' in title_lower:
                movable_tag = 'forefathers'
            elif 'sunday following dec. 18' in title_lower or 'sunday before the nativity' in title_lower:
                movable_tag = 'sunday_before_nativity'
            elif 'sunday after the nativity' in title_lower:
                movable_tag = 'sunday_after_nativity'
                
            # 3. Handle skipped calendar days (offsets)
            if not is_rubric and not movable_tag:
                if month == 'FEBRUARY' and day_of_month == 17:
                    # Skip Feb 17 (Theodore Recruit is skipped in Stamford)
                    day_of_month = 18
                elif month == 'JUNE' and day_of_month == 8:
                    # Skip June 8 (Theodore Stratelates is skipped in Stamford)
                    day_of_month = 9
                elif month == 'JUNE' and day_of_month == 30:
                    # Skip June 30 (Twelve Apostles is skipped in Stamford)
                    day_of_month = 31 # will exceed June but handled safely
            
            # Resolve the key prefix
            if is_rubric:
                # We skip rubrics from standard key database ingestion since they have no hymns
                continue
            elif movable_tag:
                cycle_key = f"menaion.{movable_tag}"
            else:
                cycle_key = f"menaion.{month_num:02d}_{day_of_month:02d}"
                day_of_month += 1
                
            # Compile the hymns in this block into flat keys
            hymn_counts = defaultdict(int)
            
            for h in b['hymns']:
                h_type, tone, rubric = parse_prefix(h['header'])
                hymn_counts[h_type] += 1
                suffix_idx = hymn_counts[h_type]
                
                # Suffix indexing conventions
                flat_key = f"{cycle_key}.liturgy.{h_type}_{suffix_idx}"
                
                final_db[flat_key] = {
                    "content": h['content'],
                    "source": "Stamford Divine Office (2014)",
                    "tone": tone,
                    "rubric": rubric
                }
                
    # Save the database
    output_path = r'C:\Users\augus\.gemini\antigravity\brain\9025717e-97c6-4ee4-bc59-6a97eba223c0\text_stamford_troparia.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_db, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully compiled {len(final_db)} keys into {output_path}")

if __name__ == '__main__':
    main()
