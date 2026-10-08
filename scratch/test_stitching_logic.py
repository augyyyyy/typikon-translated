import sys
import re
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
cohorts_dir = PROJECT_ROOT / "Liturgical Monuments" / "Monument 4 - 1852 Doskovsky Typikon" / "Cohorts"

running_header_re = re.compile(r'^[ \t]*(?:Month\s+—\s*\d+\s*—\s*[A-Za-z]+|—\s*\d+\s*—|\d+\s+—\s+[A-Za-z]+)[ \t]*$', re.IGNORECASE)

leaf_pat = re.compile(
    r'(\n(?:[ \t]*\n)*(?:<!--\s*LEAF:[^>]+-->|\[(?:Book\s+Page|Physical\s+Page|Leaf|Page|Blank)[^\]]+\]|===\s*LEAF[^=]+===|\*?\[Blank\s+[^\]]+\]\*?|\*?\((?:Physical Page|Physical pp\.|Physical Leaf|Book Page|Leaf\s+p?|Blank)[^)]*\)\*?)(?:\s*\n(?:<!--\s*LEAF:[^>]+-->|\[(?:Book\s+Page|Physical\s+Page|Leaf|Page|Blank)[^\]]+\]|===\s*LEAF[^=]+===|\*?\[Blank\s+[^\]]+\]\*?|\*?\((?:Physical Page|Physical pp\.|Physical Leaf|Book Page|Leaf\s+p?|Blank)[^)]*\)\*?))*\n(?:[ \t]*\n)*)'
)

samples = []
for cf in sorted(cohorts_dir.glob("*.md")):
    text = cf.read_text(encoding="utf-8")
    for m in leaf_pat.finditer(text):
        start, end = m.span()
        pre_lines = [l.strip() for l in text[:start].splitlines() if l.strip()]
        post_lines = [l.strip() for l in text[end:].splitlines() if l.strip()]
        last_pre = pre_lines[-1] if pre_lines else ''
        first_post = post_lines[0] if post_lines else ''
        if running_header_re.match(first_post) and len(post_lines) > 1:
            first_post = post_lines[1]
        samples.append((cf.name, last_pre, m.group(0).strip(), first_post))

print(f"Total leaf boundaries: {len(samples)}")

mid_cuts = []
paragraph_breaks = []

for cf_name, pre, tag, post in samples:
    # Strip footnote citations and markdown closing formatting from pre
    core_pre = re.sub(r'(?:\[\^\d+\]|[*_`"\'\”\’]|\s)+$', '', pre)
    ends_punct = bool(core_pre and core_pre[-1] in ('.', '!', '?', ':', ';'))
    starts_heading = post.startswith('#') or post.startswith('===')
    starts_dialogue = bool(re.match(r'^(?:>\s*)?(?:\*\*)?(?:Priest|Deacon|Choir|Reader|Bishop|Hierarch|People|Chanter):', post, re.IGNORECASE))
    starts_bullet = bool(re.match(r'^(?:[-*+]\s+|\d+\.\s+|☞|☩)', post))
    
    # If not ending with punct and next doesn't start with heading/bullet/dialogue
    is_cut = (not ends_punct) and (not starts_heading) and (not starts_bullet) and (not starts_dialogue)
    if is_cut:
        mid_cuts.append((cf_name, pre, tag, post))
    else:
        paragraph_breaks.append((cf_name, pre, tag, post))

print(f"Detected Mid-Sentence Cuts: {len(mid_cuts)}")
print(f"Detected Natural Paragraph/Section Breaks: {len(paragraph_breaks)}")

print("\n--- SAMPLE MID-SENTENCE CUTS (First 10) ---")
for cf_name, pre, tag, post in mid_cuts[:10]:
    print(f"[{cf_name}]")
    print(f"  PRE:  ...{pre[-60:]}")
    print(f"  POST: {post[:60]}...")
