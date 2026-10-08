import sys
import re
from pathlib import Path
from typing import List, Tuple

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def is_explicit_leaf_marker(s: str) -> bool:
    if not s:
        return False
    if re.fullmatch(r"<!--\s*LEAF:?[^>]*-->", s, re.IGNORECASE):
        return True
    if re.fullmatch(r"===\s*LEAF\s+[^=]+===", s, re.IGNORECASE):
        return True
    if re.fullmatch(r"\[(?:Physical\s+Page\s+\d+\s*/\s*)?(?:Book\s+Page|Physical\s+Page|Leaf|Page)\s+[^\]]+\]", s, re.IGNORECASE):
        return True
    if re.fullmatch(r"\*?\[Blank\s+[^\]]+\]\*?", s, re.IGNORECASE):
        return True
    if re.fullmatch(r"\*?\((?:Physical\s+Page|Physical\s+pp\.|Physical\s+Leaf|Book\s+Page|Leaf\s+p?|Blank\s+Flyleaf)[^)]*\)\*?", s, re.IGNORECASE):
        return True
    if re.fullmatch(r"(?:Month\s+—\s*\d+\s*—\s*[A-Za-z]+|—\s*\d+\s*—|\d+\s+—\s+[A-Za-z]+)", s, re.IGNORECASE):
        return True
    return False

def stitch_leaf_stream(input_text: str) -> Tuple[str, List[Tuple[str, str, str]]]:
    lines = input_text.splitlines()
    stitched_log = []
    output_segments: List[str] = []
    i = 0
    n = len(lines)
    
    while i < n:
        line = lines[i]
        s = line.strip()
        
        if not s or is_explicit_leaf_marker(s) or s == "---":
            has_leaf_marker = False
            has_hr = False
            
            while i < n:
                curr_s = lines[i].strip()
                if not curr_s:
                    i += 1
                elif is_explicit_leaf_marker(curr_s):
                    has_leaf_marker = True
                    i += 1
                elif curr_s == "---":
                    has_hr = True
                    i += 1
                else:
                    break
            
            if not output_segments:
                continue
            if i >= n:
                break
                
            prev_line = output_segments[-1]
            next_line = lines[i]
            
            if has_leaf_marker:
                core_prev = re.sub(r'(?:\[\^\d+\]|[\]\)\*_`"\'\”\’]|\s)+$', '', prev_line)
                ends_punct = bool(core_prev and core_prev[-1] in ('.', '!', '?', ':', ';'))
                
                next_s = next_line.strip()
                starts_heading = next_s.startswith('#') or next_s.startswith('===')
                starts_bullet = bool(re.match(r'^(?:[-*+]\s+|\d+[\.)]\s+|☞|☩)', next_s))
                starts_dialogue = bool(re.match(r'^(?:>\s*)?(?:\*\*)?(?:The\s+)?(?:Priest|Deacon|Second Deacon|First Deacon|Choir|Reader|Bishop|Hierarch|People|Chanter):', next_s, re.IGNORECASE))
                starts_table = next_s.startswith('|')
                starts_quote = next_s.startswith('>') and not prev_line.strip().startswith('>')
                
                is_cut = (
                    not ends_punct
                    and not starts_heading
                    and not starts_bullet
                    and not starts_dialogue
                    and not starts_table
                    and not starts_quote
                    and not prev_line.strip().startswith('#')
                    and not prev_line.strip().startswith('|')
                )
                
                if is_cut:
                    stitched_log.append((prev_line[-40:], "LEAF_BREAK", next_s[:40]))
                    prev_words = prev_line.split()
                    next_words = next_s.split()
                    if prev_words and next_words:
                        last_w = re.sub(r'^[^\w]+|[^\w]+$', '', prev_words[-1]).lower()
                        first_w = re.sub(r'^[^\w]+|[^\w]+$', '', next_words[0]).lower()
                        if last_w and last_w == first_w:
                            next_s = " ".join(next_words[1:])
                    
                    if prev_line.rstrip().endswith('*') and next_s.startswith('*') and not prev_line.rstrip().endswith('**') and not next_s.startswith('**'):
                        output_segments[-1] = prev_line.rstrip()[:-1] + " " + next_s[1:]
                    else:
                        output_segments[-1] = prev_line.rstrip() + " " + next_s
                    i += 1
                else:
                    output_segments.append("")
            else:
                if has_hr:
                    output_segments.append("")
                    output_segments.append("---")
                    output_segments.append("")
                else:
                    output_segments.append("")
        else:
            output_segments.append(line)
            i += 1
            
    result_text = "\n".join(output_segments)
    result_text = re.sub(r'\n{3,}', '\n\n', result_text)
    return result_text.strip(), stitched_log

def purge_scaffolding_and_stitch_seams(cohort_texts: List[str]) -> str:
    cleaned_cohorts = []
    for c_text in cohort_texts:
        c_clean = re.split(r"\n##\s+(?:Scholarly Critical Apparatus & Footnotes|Footnotes)\b", c_text, flags=re.IGNORECASE)[0]
        c_clean = re.sub(r"^#+\s*.*?Cohort\s+\d+.*?\n+", "", c_clean, flags=re.MULTILINE | re.IGNORECASE)
        c_clean = re.sub(r"<!--\s*(?:START|END)?\s*COHORT.*?-->\n*", "", c_clean, flags=re.IGNORECASE)
        c_clean = re.sub(r"##\s+Table of Contents\s*\n(?:[ \t]*[-*\d\.]+\s+.*?\(#.*?\)\s*\n)+", "", c_clean, flags=re.IGNORECASE)
        c_clean = re.sub(r">\s*\[!NOTE\]\s*\n(?:>\s*.*?\n)+", "", c_clean)
        cleaned_cohorts.append(c_clean.strip())

    full_raw = "\n\n".join(cleaned_cohorts)
    stitched_text, log = stitch_leaf_stream(full_raw)
    print(f"  [Seam Stitcher] Successfully stitched {len(log)} mid-sentence page breaks into continuous text.")
    return stitched_text

for mon_id, mon_title in [
    ("Monument 4 - 1852 Doskovsky Typikon", "1852 Doskovsky"),
    ("Monument 2 - 1899 Dolnytsky Typikon", "1899 Dolnytsky"),
    ("Monument 1 - 1891 Lviv Synod", "1891 Lviv Synod"),
]:
    c_dir = PROJECT_ROOT / "Liturgical Monuments" / mon_id / "Cohorts"
    if not c_dir.exists():
        continue
    c_files = sorted(c_dir.glob("*.md"), key=lambda f: int(re.search(r'cohort(\d+)', f.name).group(1)))
    raw = [cf.read_text(encoding="utf-8") for cf in c_files]
    
    stitched = purge_scaffolding_and_stitch_seams(raw)
    leaks = re.findall(r'(\[(?:Book\s+Page|Physical\s+Page|Leaf|Page)\s+\d+[^\]]*\]|<!--\s*LEAF:?[^>]*-->|===\s*LEAF\s+[^=]+===|\*?\[Blank\s+[^\]]+\]\*?)', stitched, re.IGNORECASE)
    print(f"{mon_title}: Leaked markers in body: {len(leaks)}")
    has_bernard = "Totum nos habere voluit per Mariam" in stitched
    print(f"{mon_title}: Leaked St. Bernard footnote in body: {has_bernard}")
