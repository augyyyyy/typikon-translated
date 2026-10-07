import re
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Load verb map
with open("scratch/verb_normalization_map.json", "r", encoding="utf-8") as f:
    verb_map = json.load(f)

sorted_eth_words = sorted(verb_map.keys(), key=len, reverse=True)
pattern = re.compile(r"\b(" + "|".join(re.escape(k) for k in sorted_eth_words) + r")\b", re.IGNORECASE)

def replace_match(m):
    original = m.group(1)
    lower = original.lower()
    replacement = verb_map.get(lower, original)
    if original.isupper():
        return replacement.upper()
    elif original[0].isupper():
        return replacement.capitalize()
    else:
        return replacement

def remediate_file(path: Path, is_synod: bool = False):
    if not path.exists():
        return 0, 0
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    new_lines = []
    verb_count = 0
    wherefore_count = 0
    
    for line in lines:
        s = line.strip()
        # Protect scripture footnotes
        if s.startswith("[^") and any(bk in s for bk in ["Gen.", "Ex.", "Lev.", "Num.", "Deut.", "Matt.", "Mark", "Luke", "John", "Acts", "Rom.", "Cor.", "Gal.", "Eph.", "Phil.", "Col.", "Thess.", "Tim.", "Tit.", "Heb.", "Jas.", "Pet.", "Rev.", "Isa.", "Jer.", "Ezek.", "Dan.", "Hos.", "Joel", "Amos", "Obad.", "Jonah", "Mic.", "Nah.", "Hab.", "Zeph.", "Hag.", "Zech.", "Mal.", "Ps.", "Prov.", "Wisd.", "Eccl.", "Sir."]):
            new_lines.append(line)
            continue
            
        def sub_func(m):
            nonlocal verb_count
            verb_count += 1
            return replace_match(m)
            
        modified_line = pattern.sub(sub_func, line)
        
        if is_synod:
            if "wherefore" in modified_line.lower():
                def sub_wf(m):
                    nonlocal wherefore_count
                    wherefore_count += 1
                    orig = m.group(0)
                    if orig == "Wherefore":
                        return "Therefore"
                    elif orig == "WHEREFORE":
                        return "THEREFORE"
                    else:
                        return "therefore"
                modified_line = re.sub(r"\bwherefore\b", sub_wf, modified_line, flags=re.IGNORECASE)
                
        new_lines.append(modified_line)
        
    out_text = "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")
    path.write_text(out_text, encoding='utf-8')
    return verb_count, wherefore_count

def main():
    root = Path("Liturgical Monuments")
    total_verbs = 0
    total_wherefore = 0

    # 1. Monument 1 - 1891 Synod
    m1_dir = root / "Monument 1 - 1891 Lviv Synod"
    print("\n--- Remediating Monument 1 (1891 Lviv Synod) ---")
    for folder in [m1_dir / "Final MD", m1_dir / "Final", m1_dir / "Draft"]:
        if folder.exists():
            for f in sorted(folder.glob("*.*")):
                if f.suffix in [".md", ".txt"]:
                    vc, wc = remediate_file(f, is_synod=True)
                    if vc > 0 or wc > 0:
                        print(f"  {f.name}: {vc} verbs, {wc} wherefore replaced")
                        total_verbs += vc
                        total_wherefore += wc

    # 2. Monument 3 - 1901 Mikita Typikon
    m3_dir = root / "Monument 3 - 1901 Mikita Typikon"
    print("\n--- Remediating Monument 3 (1901 Mikita Typikon) ---")
    for folder in [m3_dir / "Final MD", m3_dir / "Final", m3_dir / "Draft"]:
        if folder.exists():
            for f in sorted(folder.glob("*.*")):
                if f.suffix in [".md", ".txt"]:
                    vc, wc = remediate_file(f, is_synod=False)
                    if vc > 0:
                        print(f"  {f.name}: {vc} verbs replaced")
                        total_verbs += vc

    # 3. Monument 4 - 1852 Doskovsky Typikon
    m4_dir = root / "Monument 4 - 1852 Doskovsky Typikon"
    print("\n--- Remediating Monument 4 (1852 Doskovsky Typikon) ---")
    for folder in [m4_dir / "Final MD", m4_dir / "Final", m4_dir / "Draft"]:
        if folder.exists():
            for f in sorted(folder.glob("*.*")):
                if f.suffix in [".md", ".txt"]:
                    vc, wc = remediate_file(f, is_synod=False)
                    if vc > 0:
                        print(f"  {f.name}: {vc} verbs replaced")
                        total_verbs += vc

    print("\n" + "=" * 55)
    print(f"TOTAL VERBS NORMALIZED: {total_verbs:,}")
    print(f"TOTAL WHEREFORE REPLACED: {total_wherefore:,}")
    print("=" * 55)

if __name__ == '__main__':
    main()
