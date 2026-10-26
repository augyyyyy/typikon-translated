import sys
import re
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
cohorts_dir = PROJECT_ROOT / "Liturgical Monuments" / "Monument 4 - 1852 Doskovsky Typikon" / "Cohorts"

# Collect all cohort text
cohort_files = sorted(cohorts_dir.glob("*.md"), key=lambda f: int(re.search(r'cohort(\d+)', f.name).group(1)))
full_raw = "\n\n".join(cf.read_text(encoding="utf-8") for cf in cohort_files)

# Strip headers and notes first
text = re.sub(r"^#+\s*.*?Cohort\s+\d+.*?\n+", "", full_raw, flags=re.MULTILINE | re.IGNORECASE)
text = re.sub(r"<!--\s*(?:START|END)?\s*COHORT.*?-->\n*", "", text, flags=re.IGNORECASE)
text = re.sub(r"##\s+Table of Contents\s*\n(?:[ \t]*[-*\d\.]+\s+.*?\(#.*?\)\s*\n)+", "", text, flags=re.IGNORECASE)
text = re.sub(r">\s*\[!NOTE\]\s*\n(?:>\s*.*?\n)+", "", text)
text = re.sub(r"##\s+(?:Scholarly Critical Apparatus & Footnotes|Footnotes)\s*\n(?:\[\^\d+\]:.*?\n*)+", "", text, flags=re.IGNORECASE)
text = re.sub(r"^#+\s*Cohort\s+\d+\s+Footnotes.*?\n*", "", text, flags=re.MULTILINE | re.IGNORECASE)

leaf_item = r"""(?:
    <!--\s*LEAF:?[^>]*-->
  | ===\s*LEAF\s+[^=]+===
  | \[(?:Physical\s+Page\s+\d+\s*/\s*)?(?:Book\s+Page|Physical\s+Page|Leaf|Page)\s+[^\]]+\]
  | \*?\[Blank\s+[^\]]+\]\*?
  | \*?\((?:Physical\s+Page|Physical\s+pp\.|Physical\s+Leaf|Book\s+Page|Leaf\s+p?|Blank\s+Flyleaf)[^)]*\)\*?
  | (?:Month\s+—\s*\d+\s*—\s*[A-Za-z]+|—\s*\d+\s*—|\d+\s+—\s+[A-Za-z]+)
  | ---
)"""

# Pattern for a block of leaf markers and dividers
leaf_block_pat = re.compile(
    rf'(?:\n[ \t]*)*\n[ \t]*{leaf_item}(?:[ \t]*\n[ \t]*(?:{leaf_item}|\s*))*(?:\n[ \t]*)*',
    re.VERBOSE | re.IGNORECASE
)

# Test stitching
def stitch_seams(content: str) -> Tuple[str, List[Tuple[str, str, str]]]:
    stitched_log = []
    
    def replacer(match):
        start = match.start()
        end = match.end()
        
        pre = content[:start]
        post = content[end:]
        
        pre_lines = [l.strip() for l in pre.splitlines() if l.strip()]
        post_lines = [l.strip() for l in post.splitlines() if l.strip()]
        
        if not pre_lines or not post_lines:
            return "\n\n"
            
        last_line = pre_lines[-1]
        first_line = post_lines[0]
        
        # Check if pre cut off mid-sentence
        core_pre = re.sub(r'(?:\[\^\d+\]|[*_`"\'\”\’]|\s)+$', '', last_line)
        ends_punct = bool(core_pre and core_pre[-1] in ('.', '!', '?', ':', ';'))
        
        starts_heading = first_line.startswith('#') or first_line.startswith('===')
        starts_bullet = bool(re.match(r'^(?:[-*+]\s+|\d+[\.)]\s+|☞|☩)', first_line))
        starts_dialogue = bool(re.match(r'^(?:>\s*)?(?:\*\*)?(?:Priest|Deacon|Second Deacon|First Deacon|Choir|Reader|Bishop|Hierarch|People|Chanter):', first_line, re.IGNORECASE))
        starts_table = first_line.startswith('|')
        starts_quote = first_line.startswith('>') and not last_line.startswith('>')
        
        is_cut = (
            not ends_punct
            and not starts_heading
            and not starts_bullet
            and not starts_dialogue
            and not starts_table
            and not starts_quote
            and not last_line.startswith('#')
            and not last_line.startswith('|')
        )
        
        if is_cut:
            stitched_log.append((last_line[-40:], match.group(0).strip()[:40], first_line[:40]))
            # Handle italics boundary
            if last_line.endswith('*') and first_line.startswith('*') and not last_line.endswith('**') and not first_line.startswith('**'):
                # Both italicized: we will join with space, but we need to merge the * *
                # Return a special join token that will collapse the asterisks
                return " __ITALIC_JOIN__ "
            return " "
        else:
            return "\n\n"

    new_content = leaf_block_pat.sub(replacer, content)
    # Clean up italic joins: e.g. "with* __ITALIC_JOIN__ *the" -> "with the"
    new_content = re.sub(r'\*\s*__ITALIC_JOIN__\s*\*?', ' ', new_content)
    new_content = new_content.replace('__ITALIC_JOIN__', ' ')
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    return new_content.strip(), stitched_log

stitched_text, log = stitch_seams(text)
print(f"Stitched {len(log)} mid-sentence seams!")
print("\n--- FIRST 15 STITCHED SEAMS ---")
for pre, marker, post in log[:15]:
    print(f"  PRE:  ...{pre}")
    print(f"  POST: {post}...")
    print("  ---")

# Check if Book Page 133 / 134 area is seamless!
print("\n--- CHECKING BOOK PAGE 134 SEAM IN RESULT ---")
m = re.search(r'readings.{0,100}Indiction', stitched_text)
if m:
    print(f"MATCH: {m.group(0)}")
else:
    print("Could not find Indiction reading match")
