import json
import os
import re
import sys
import difflib

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

def clean_rd_content(content):
    # Strip metadata prefixes like *Troparion, Tone 1:* or *Kontakion, Tone 4:*
    clean = re.sub(r'^\*?(Troparion|Kontakion|Dismissal|Hypakoe)[^*:]*:\*?\s*', '', content, flags=re.IGNORECASE)
    return clean.strip()

def get_clause_diff(text1, text2):
    # Split by asterisks or punctuation to make it line-by-line diff readable
    clauses1 = [c.strip() for c in text1.split('*') if c.strip()]
    clauses2 = [c.strip() for c in text2.split('*') if c.strip()]
    
    diff = difflib.unified_diff(clauses1, clauses2, fromfile='Stamford', tofile='Royal Doors', lineterm='')
    diff_lines = list(diff)
    if len(diff_lines) <= 2: # No real differences
        return ""
    # Skip the first two lines of unified_diff header
    return '\n'.join(diff_lines[2:])

def types_compatible(s_type, rd_key):
    rd_key_lower = rd_key.lower()
    parts = rd_key_lower.split('.')
    service = parts[-2] if len(parts) >= 2 else ""
    hymn_name = parts[-1] if len(parts) >= 1 else ""
    
    if s_type == 'troparion':
        if service == 'liturgy':
            return 'troparion_' in hymn_name and not any(x in hymn_name for x in ['glory', 'both_now'])
        else:
            return 'troparion' in hymn_name
    elif s_type == 'kontakion':
        if 'kontakion' in hymn_name:
            return True
        if service == 'liturgy':
            return any(x in hymn_name for x in ['glory', 'both_now'])
        return False
    elif s_type == 'dismissal':
        return 'dismissal' in hymn_name
    elif s_type == 'hypakoe':
        return 'hypakoe' in hymn_name or 'hypacoe' in hymn_name
    return True

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    # Load databases
    with open(r'C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Festal Propers Comparisons\text_royaldoors.json', 'r', encoding='utf-8') as f:
        rd_data = json.load(f)
        
    with open(r'C:\Users\augus\.gemini\antigravity\brain\9025717e-97c6-4ee4-bc59-6a97eba223c0\text_stamford_troparia.json', 'r', encoding='utf-8') as f:
        stamford_data = json.load(f)
        
    # Group Royal Doors by MM_DD and movable tag
    rd_by_date = {}
    rd_by_movable = {}
    
    for k, v in rd_data.items():
        content = v.get('content', '')
        if not content:
            continue
            
        parts = k.split('.')
        date_str = parts[1]
        slug = parts[2]
        
        # Determine resolved date key
        mm_dd = None
        if '_' in date_str and len(date_str) == 10:
            mm_dd = date_str[5:] # MM_DD
            
        rd_entry = {
            'key': k,
            'slug': slug,
            'raw_content': content,
            'clean_content': clean_rd_content(content),
            'words': normalize_text(clean_rd_content(content))
        }
        
        if mm_dd:
            if mm_dd not in rd_by_date:
                rd_by_date[mm_dd] = []
            rd_by_date[mm_dd].append(rd_entry)
            
        # Also index by keywords in slug for movable feasts
        for m_tag in ['christ_the_king', 'forefathers', 'sunday_before_the_nativity', 'sunday_after_the_nativity']:
            if m_tag in slug or m_tag.replace('_', '') in slug.replace('_', ''):
                if m_tag not in rd_by_movable:
                    rd_by_movable[m_tag] = []
                rd_by_movable[m_tag].append(rd_entry)
                
    # All entries for global matching fallback
    all_rd_entries = []
    for date_list in rd_by_date.values():
        all_rd_entries.extend(date_list)
        
    # Execute comparisons
    results = []
    total_keys = 0
    matched_keys = 0
    identical_keys = 0
    diff_keys = 0
    unmatched_keys = 0
    
    # Sort Stamford keys chronologically
    sorted_stamford_keys = sorted(list(stamford_data.keys()))
    
    for k in sorted_stamford_keys:
        parts = k.split('.')
        h_type = parts[3].split('_')[0] if len(parts) >= 4 else "troparion"
        if h_type not in ['troparion', 'kontakion']:
            continue
            
        total_keys += 1
        s_val = stamford_data[k]
        s_content = s_val['content']
        s_words = normalize_text(s_content)
        s_rubric = s_val['rubric']
        s_tone = s_val['tone']
        
        # Extract cycle path
        cycle_type = parts[1] # e.g. '01_01' or 'forefathers'
        
        # Retrieve candidates
        candidates = []
        if cycle_type.startswith('0') or cycle_type.startswith('1'):
            candidates = rd_by_date.get(cycle_type, [])
        else:
            candidates = rd_by_movable.get(cycle_type, [])
        
        # Find best local match
        best_score = 0.0
        best_match = None
        for rd in candidates:
            if not types_compatible(h_type, rd['key']):
                continue
            score = jaccard_similarity(s_words, rd['words'])
            if score > best_score:
                best_score = score
                best_match = rd
                
        # Global fallback if local match is weak or missing
        is_global = False
        if best_score < 0.20:
            global_best_score = 0.0
            global_best_match = None
            for rd in all_rd_entries:
                if not types_compatible(h_type, rd['key']):
                    continue
                score = jaccard_similarity(s_words, rd['words'])
                if score > global_best_score:
                    global_best_score = score
                    global_best_match = rd
            if global_best_score >= 0.6: # high threshold for global match
                best_score = global_best_score
                best_match = global_best_match
                is_global = True
                
        if best_score >= 0.20 and best_match:
            matched_keys += 1
            # Check if identical (ignoring asterisks and punctuation)
            norm_s = ' '.join(s_words)
            norm_rd = ' '.join(best_match['words'])
            is_identical = (norm_s == norm_rd)
            
            diff_md = ""
            if not is_identical:
                diff_md = get_clause_diff(s_content, best_match['clean_content'])
                if not diff_md:
                    is_identical = True
                    
            if is_identical:
                identical_keys += 1
            else:
                diff_keys += 1
                
            results.append({
                'key': k,
                'stamford_rubric': s_rubric,
                'stamford_tone': s_tone,
                'stamford_content': s_content,
                'rd_key': best_match['key'],
                'rd_content': best_match['clean_content'],
                'jaccard': best_score,
                'is_identical': is_identical,
                'is_global': is_global,
                'diff': diff_md
            })
        else:
            unmatched_keys += 1
            results.append({
                'key': k,
                'stamford_rubric': s_rubric,
                'stamford_tone': s_tone,
                'stamford_content': s_content,
                'rd_key': None,
                'rd_content': None,
                'jaccard': 0.0,
                'is_identical': False,
                'is_global': False,
                'diff': ""
            })
            
    # Write comparison report
    report_path = r'C:\Users\augus\.gemini\antigravity\brain\9025717e-97c6-4ee4-bc59-6a97eba223c0\stamford_royaldoors_troparia_comparison.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Report: Stamford Divine Office vs Royal Doors Troparia & Kontakia Comparison\n\n")
        f.write("This report compares each Troparion and Kontakion from the **Stamford Divine Office (2014) Calendar Appendix** to the corresponding daily proper entries in the **Royal Doors database**.\n\n")
        
        f.write("## Summary Statistics\n\n")
        f.write(f"* **Total Stamford Keys Analyzed:** {total_keys}\n")
        f.write(f"* **Successfully Matched Keys:** {matched_keys} ({matched_keys/total_keys*100:.1f}%)\n")
        f.write(f"  * **Identical Content:** {identical_keys} ({identical_keys/total_keys*100:.1f}%)\n")
        f.write(f"  * **With Translation differences:** {diff_keys} ({diff_keys/total_keys*100:.1f}%)\n")
        f.write(f"* **Unmatched Stamford Keys:** {unmatched_keys} ({unmatched_keys/total_keys*100:.1f}%)\n\n")
        
        f.write("---\n\n")
        
        f.write("## Detailed Comparisons\n\n")
        
        current_month = None
        months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
        
        for r in results:
            # Group by month header in output
            parts = r['key'].split('.')
            cycle_type = parts[1] # e.g. '01_01' or 'forefathers'
            
            month_name = None
            if cycle_type.startswith('0') or cycle_type.startswith('1'):
                month_num = int(cycle_type.split('_')[0])
                month_name = months[month_num - 1]
            else:
                month_name = "MOVABLE FEASTS"
                
            if month_name != current_month:
                current_month = month_name
                f.write(f"\n# {current_month}\n\n")
                
            day_str = ""
            if cycle_type.startswith('0') or cycle_type.startswith('1'):
                day_num = int(cycle_type.split('_')[1])
                day_str = f"Day {day_num:02d}"
            else:
                day_str = cycle_type.upper().replace('_', ' ')
                
            f.write(f"### {day_str}: {r['stamford_rubric']} ({r['stamford_tone'] or 'No Tone'})\n")
            f.write(f"**Stamford Key:** `{r['key']}`\n\n")
            
            if r['rd_key']:
                f.write(f"**Royal Doors Key:** `{r['rd_key']}` (Jaccard Similarity: {r['jaccard']:.2f})\n\n")
                if r['is_identical']:
                    f.write("> [!NOTE]\n")
                    f.write("> **Translation Status:** Verbatim Match. The texts are identical.\n\n")
                    f.write(f"> {r['stamford_content']}\n\n")
                else:
                    f.write("> [!WARNING]\n")
                    f.write("> **Translation Status:** Phrasing Differences Found.\n\n")
                    f.write("**Stamford Text:**\n")
                    f.write(f"> {r['stamford_content']}\n\n")
                    f.write("**Royal Doors Text:**\n")
                    f.write(f"> {r['rd_content']}\n\n")
                    f.write("**Differences (Diff):**\n")
                    f.write("```diff\n")
                    f.write(r['diff'] + "\n")
                    f.write("```\n\n")
            else:
                f.write("> [!CAUTION]\n")
                f.write("> **Translation Status:** No Match Found in Royal Doors.\n\n")
                f.write("**Stamford Text:**\n")
                f.write(f"> {r['stamford_content']}\n\n")
                
            f.write("---\n\n")
            
    print(f"Comparison report successfully written to {report_path}")

if __name__ == '__main__':
    main()
