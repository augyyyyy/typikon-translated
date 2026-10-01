import json
import os
import re
import sys
import difflib
from collections import defaultdict

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
    clauses1 = [c.strip() for c in text1.split('*') if c.strip()]
    clauses2 = [c.strip() for c in text2.split('*') if c.strip()]
    
    diff = difflib.unified_diff(clauses1, clauses2, fromfile='Prev Version', tofile='New Version', lineterm='')
    diff_lines = list(diff)
    if len(diff_lines) <= 2:
        return ""
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
    
    # 1. Load and merge Royal Doors databases
    print("Loading text_royaldoors.json (latest)...")
    with open(r'C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Festal Propers Comparisons\text_royaldoors.json', 'r', encoding='utf-8') as f:
        rd_latest = json.load(f)
        
    print("Loading text_royaldoors_old.json (historical)...")
    with open(r'C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Festal Propers Comparisons\text_royaldoors_old.json', 'r', encoding='utf-8') as f:
        rd_old = json.load(f)
        
    # Merge (latest overrides old if there are key overlaps)
    rd_merged = {**rd_old, **rd_latest}
    print(f"Merged Royal Doors databases: {len(rd_merged)} total keys.")
    
    # Group by (MM_DD, year) and (movable_tag, year)
    rd_by_date_year = defaultdict(list)
    rd_by_movable_year = defaultdict(list)
    rd_all_by_year = defaultdict(list)
    
    for k, v in rd_merged.items():
        content = v.get('content', '')
        if not content:
            continue
            
        parts = k.split('.')
        date_str = parts[1]
        slug = parts[2]
        
        # Parse year and date
        if '_' not in date_str or len(date_str) != 10:
            continue
        year = date_str[:4]
        mm_dd = date_str[5:]
        
        rd_entry = {
            'key': k,
            'slug': slug,
            'year': year,
            'raw_content': content,
            'clean_content': clean_rd_content(content),
            'words': normalize_text(clean_rd_content(content))
        }
        
        rd_by_date_year[(mm_dd, year)].append(rd_entry)
        rd_all_by_year[year].append(rd_entry)
        
        # Movable tags
        for m_tag in ['christ_the_king', 'forefathers', 'sunday_before_the_nativity', 'sunday_after_the_nativity']:
            if m_tag in slug or m_tag.replace('_', '') in slug.replace('_', ''):
                rd_by_movable_year[(m_tag, year)].append(rd_entry)
                
    # 2. Load Stamford
    with open(r'C:\Users\augus\.gemini\antigravity\brain\9025717e-97c6-4ee4-bc59-6a97eba223c0\text_stamford_troparia.json', 'r', encoding='utf-8') as f:
        stamford_data = json.load(f)
        
    # Filter to Troparia and Kontakia only
    sorted_stamford_keys = sorted([k for k in stamford_data.keys() if k.split('.')[-1].split('_')[0] in ['troparion', 'kontakion']])
    print(f"Loaded {len(sorted_stamford_keys)} Stamford troparia/kontakia keys.")
    
    results = []
    years_range = [str(y) for y in range(2017, 2027)] # 2017 to 2026
    
    total_analyzed = 0
    any_match_count = 0
    shift_count = 0
    
    for k in sorted_stamford_keys:
        total_analyzed += 1
        s_val = stamford_data[k]
        s_content = s_val['content']
        s_words = normalize_text(s_content)
        s_rubric = s_val['rubric']
        s_tone = s_val['tone']
        
        parts = k.split('.')
        cycle_type = parts[1] # '01_01' or 'forefathers'
        h_type = parts[3].split('_')[0]
        
        # Match year by year
        yearly_matches = {}
        
        for year in years_range:
            # Get candidates for this year and date
            candidates = []
            if cycle_type.startswith('0') or cycle_type.startswith('1'):
                candidates = rd_by_date_year.get((cycle_type, year), [])
            else:
                candidates = rd_by_movable_year.get((cycle_type, year), [])
                
            best_score = 0.0
            best_match = None
            for rd in candidates:
                if not types_compatible(h_type, rd['key']):
                    continue
                score = jaccard_similarity(s_words, rd['words'])
                if score > best_score:
                    best_score = score
                    best_match = rd
                    
            # Global fallback for this year if local match is weak
            if best_score < 0.20:
                global_best_score = 0.0
                global_best_match = None
                for rd in rd_all_by_year.get(year, []):
                    if not types_compatible(h_type, rd['key']):
                        continue
                    score = jaccard_similarity(s_words, rd['words'])
                    if score > global_best_score:
                        global_best_score = score
                        global_best_match = rd
                if global_best_score >= 0.60:
                    best_score = global_best_score
                    best_match = global_best_match
                    
            if best_score >= 0.20 and best_match:
                yearly_matches[year] = {
                    'key': best_match['key'],
                    'content': best_match['clean_content'],
                    'words': best_match['words'],
                    'score': best_score
                }
                
        # Group yearly matches into unique versions chronologically
        unique_versions = []
        for year in sorted(list(yearly_matches.keys())):
            match_info = yearly_matches[year]
            m_content = match_info['content']
            
            # Find if this content is already in unique_versions
            found = False
            for v in unique_versions:
                # Compare normalized words to ignore spacing/case differences
                if ' '.join(v['words']) == ' '.join(normalize_text(m_content)):
                    v['years'].append(year)
                    found = True
                    break
            if not found:
                unique_versions.append({
                    'content': m_content,
                    'words': normalize_text(m_content),
                    'years': [year]
                })
                
        has_matches = len(unique_versions) > 0
        if has_matches:
            any_match_count += 1
            # Check if any version has differences from Stamford
            has_shifts = False
            norm_s = ' '.join(s_words)
            for v in unique_versions:
                if ' '.join(v['words']) != norm_s:
                    has_shifts = True
                    break
            if has_shifts:
                shift_count += 1
                
        results.append({
            'key': k,
            'stamford_rubric': s_rubric,
            'stamford_tone': s_tone,
            'stamford_content': s_content,
            'versions': unique_versions,
            'has_matches': has_matches
        })
        
    # Write final report
    report_path = r'C:\Users\augus\.gemini\antigravity\brain\9025717e-97c6-4ee4-bc59-6a97eba223c0\stamford_royaldoors_troparia_comparison_yearly.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Report: Stamford vs Royal Doors Translation Evolution (2017 - 2026)\n\n")
        f.write("This report tracks how the translations of the **Stamford Divine Office (2014) Troparia & Kontakia** compare against the **Royal Doors Daily Propers** across a 10-year span (2017–2026).\n\n")
        f.write("Stamford translations have remained static, while Royal Doors has undergone revision cycles over the years. Below, we map out each revision version and show the exact pointing diffs between them.\n\n")
        
        f.write("## Summary Statistics\n\n")
        f.write(f"* **Total Stamford Keys Analyzed:** {total_analyzed}\n")
        f.write(f"* **Keys with Royal Doors Matches (Any Year):** {any_match_count} ({any_match_count/total_analyzed*100:.1f}%)\n")
        f.write(f"  * **With Translation Evolution/Shifts:** {shift_count} ({shift_count/total_analyzed*100:.1f}%)\n")
        f.write(f"  * **Verbatim Match Across All Years:** {any_match_count - shift_count} ({(any_match_count - shift_count)/total_analyzed*100:.1f}%)\n")
        f.write(f"* **Unmatched Keys:** {total_analyzed - any_match_count} ({(total_analyzed - any_match_count)/total_analyzed*100:.1f}%)\n\n")
        
        f.write("---\n\n")
        f.write("## Detailed Translation Evolution Maps\n\n")
        
        current_month = None
        months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
        
        for r in results:
            parts = r['key'].split('.')
            cycle_type = parts[1]
            
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
                day_str = f"Day {int(cycle_type.split('_')[1]):02d}"
            else:
                day_str = cycle_type.upper().replace('_', ' ')
                
            f.write(f"### {day_str}: {r['stamford_rubric']} ({r['stamford_tone'] or 'No Tone'})\n")
            f.write(f"**Stamford Key:** `{r['key']}`\n\n")
            
            f.write("**Stamford Static Text:**\n")
            f.write(f"> {r['stamford_content']}\n\n")
            
            if r['has_matches']:
                f.write("### Royal Doors Evolution:\n\n")
                prev_text = r['stamford_content']
                
                for idx, v in enumerate(r['versions']):
                    years_str = ", ".join(sorted(v['years']))
                    f.write(f"* **Version {idx+1} (Years: {years_str}):**\n")
                    f.write(f"  > {v['content']}\n\n")
                    
                    # Compute diff
                    diff_md = get_clause_diff(prev_text, v['content'])
                    if diff_md:
                        f.write("  ```diff\n")
                        # Add a visual indicator of diff source
                        if idx == 0:
                            f.write(f"  # Diff: Stamford -> Royal Doors Version 1\n")
                        else:
                            f.write(f"  # Diff: Version {idx} -> Version {idx+1}\n")
                        f.write(diff_md.replace('\n', '\n  ') + "\n")
                        f.write("  ```\n\n")
                    else:
                        f.write("  *(No phrasing differences from previous version)*\n\n")
                    prev_text = v['content']
            else:
                f.write("> [!CAUTION]\n")
                f.write("> **Translation Status:** No corresponding daily proper entry found in Royal Doors across any year.\n\n")
                
            f.write("---\n\n")
            
    print(f"Yearly comparison report successfully written to {report_path}")

if __name__ == '__main__':
    main()
