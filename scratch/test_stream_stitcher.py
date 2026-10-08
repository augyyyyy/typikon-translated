import sys
import re
from pathlib import Path
from typing import List, Tuple

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
cohorts_dir = PROJECT_ROOT / "Liturgical Monuments" / "Monument 4 - 1852 Doskovsky Typikon" / "Cohorts"

# Collect all cohort text
cohort_files = sorted(cohorts_dir.glob("*.md"), key=lambda f: int(re.search(r'cohort(\d+)', f.name).group(1)))
full_raw = "\n\n".join(cf.read_text(encoding="utf-8") for cf in cohort_files)

# Strip raw cohort headers and cohort footnotes
text = re.sub(r"^#+\s*.*?Cohort\s+\d+.*?\n+", "", full_raw, flags=re.MULTILINE | re.IGNORECASE)
text = re.sub(r"<!--\s*(?:START|END)?\s*COHORT.*?-->\n*", "", text, flags=re.IGNORECASE)
text = re.sub(r"##\s+Table of Contents\s*\n(?:[ \t]*[-*\d\.]+\s+.*?\(#.*?\)\s*\n)+", "", text, flags=re.IGNORECASE)
text = re.sub(r">\s*\[!NOTE\]\s*\n(?:>\s*.*?\n)+", "", text)
text = re.sub(r"##\s+(?:Scholarly Critical Apparatus & Footnotes|Footnotes)\s*\n(?:\[\^\d+\]:.*?\n*)+", "", text, flags=re.IGNORECASE)
text = re.sub(r"^#+\s*Cohort\s+\d+\s+Footnotes.*?\n*", "", text, flags=re.MULTILINE | re.IGNORECASE)

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
    if re.fullmatch(r"\*?\((?:Physical\s+Page|Physical\s+pp\.|Physical\s+Leaf|Book\s+Page|Leaf\s+p?|Blank)[^)]*\)\*?", s, re.IGNORECASE):
        return True
    if re.fullmatch(r"(?:Month\s+—\s*\d+\s*—\s*[A-Za-z]+|—\s*\d+\s*—|\d+\s+—\s+[A-Za-z]+)", s, re.IGNORECASE):
        return True
    return False

def stitch_leaf_stream(input_text: str) -> Tuple[str, List[Tuple[str, str, str]]]:
    lines = input_text.splitlines()
    stitched_log = []
    
    # We will build output paragraphs / lines
    # First: break lines into (is_content, line)
    # Then group sequences of non-content lines
    
    output_segments: List[str] = []
    i = 0
    n = len(lines)
    
    while i < n:
        line = lines[i]
        s = line.strip()
        
        # Check if line is part of a gap / leaf boundary
        if not s or is_explicit_leaf_marker(s) or s == "---":
            # Collect entire boundary cluster
            gap_lines = []
            has_leaf_marker = False
            has_hr = False
            
            while i < n:
                curr_s = lines[i].strip()
                if not curr_s:
                    gap_lines.append(lines[i])
                    i += 1
                elif is_explicit_leaf_marker(curr_s):
                    has_leaf_marker = True
                    gap_lines.append(lines[i])
                    i += 1
                elif curr_s == "---":
                    has_hr = True
                    gap_lines.append(lines[i])
                    i += 1
                else:
                    break
            
            # Now we are between output_segments[-1] (if any) and lines[i] (if i < n)
            if not output_segments:
                # Leading gap at start of document
                continue
            if i >= n:
                # Trailing gap at end of document
                break
                
            prev_line = output_segments[-1]
            next_line = lines[i]
            
            if has_leaf_marker:
                # This gap represents a page turn! Check if prev_line was cut mid-sentence
                core_prev = re.sub(r'(?:\[\^\d+\]|[*_`"\'\”\’]|\s)+$', '', prev_line)
                ends_punct = bool(core_prev and core_prev[-1] in ('.', '!', '?', ':', ';'))
                
                next_s = next_line.strip()
                starts_heading = next_s.startswith('#') or next_s.startswith('===')
                starts_bullet = bool(re.match(r'^(?:[-*+]\s+|\d+[\.)]\s+|☞|☩)', next_s))
                starts_dialogue = bool(re.match(r'^(?:>\s*)?(?:\*\*)?(?:Priest|Deacon|Second Deacon|First Deacon|Choir|Reader|Bishop|Hierarch|People|Chanter):', next_s, re.IGNORECASE))
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
                    # Stitching together!
                    # Handle italics across break: e.g. "with*" and "*the"
                    if prev_line.rstrip().endswith('*') and next_s.startswith('*') and not prev_line.rstrip().endswith('**') and not next_s.startswith('**'):
                        # merge italics cleanly
                        output_segments[-1] = prev_line.rstrip()[:-1] + " " + next_s[1:]
                    else:
                        output_segments[-1] = prev_line.rstrip() + " " + next_s
                    # Advance i past next_line since we merged it
                    i += 1
                else:
                    # Natural paragraph break across leaf turn
                    output_segments.append("")  # blank line for paragraph separation
            else:
                # Regular gap inside page without leaf marker
                if has_hr:
                    output_segments.append("")
                    output_segments.append("---")
                    output_segments.append("")
                else:
                    output_segments.append("")
        else:
            output_segments.append(line)
            i += 1
            
    # Reconstruct text and normalize blank lines
    result_text = "\n".join(output_segments)
    result_text = re.sub(r'\n{3,}', '\n\n', result_text)
    return result_text.strip(), stitched_log

result, log = stitch_leaf_stream(text)
print(f"Total Stitched Mid-Sentence Seams: {len(log)}")

print("\n--- FIRST 15 STITCHED SEAMS ---")
for pre, tag, post in log[:15]:
    print(f"  PRE:  ...{pre}")
    print(f"  POST: {post}...")
    print("  ---")

print("\n--- CHECKING BOOK PAGE 134 SEAM ---")
idx = result.find("Venerable Father.[^147]")
if idx != -1:
    print(result[idx-100:idx+40])
else:
    print("Not found")

print("\n--- CHECKING FOR ANY LEAKED LEAF MARKERS ---")
leaks = re.findall(r'(\[(?:Book\s+Page|Physical\s+Page|Leaf|Page)\s+\d+[^\]]*\]|<!--\s*LEAF:?[^>]*-->|===\s*LEAF\s+[^=]+===)', result, re.IGNORECASE)
print(f"Leaked markers count: {len(leaks)}")
