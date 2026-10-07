#!/usr/bin/env python3
"""
Mikita Typikon Epigraphic Restoration & Slop Normalization Engine
================================================================
1. Re-inserts all 320 physical leaf banners into:
   - Final MD/1901_mikita_typikon_complete.md
   - Final/1901_mikita_typikon_complete.txt
   - Final MD/1901_mikita_part0_intro_and_toc.md (p1..p24)
   - Final MD/1901_mikita_part1_general_services.md (p25..p50)
   - Final MD/1901_mikita_part2_particular_services.md (p51..p320)
   - Final/1901_mikita_typikon_cohort1.txt..cohort32.txt
   - Draft/1901_mikita_typikon_cohort1_raw_draft.md..cohort32_raw_draft.md
2. Enriches English liturgical incipits with canonical Church Slavonic parentheticals (*...*).
3. Eliminates residual slop violations ('wondrous', 'wherefore') across Mikita and Synod.
"""

import re
import json
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
M3_DIR = PROJECT_ROOT / "Liturgical Monuments" / "Monument 3 - 1901 Mikita Typikon"
M1_DIR = PROJECT_ROOT / "Liturgical Monuments" / "Monument 1 - 1891 Lviv Synod"

def roman_numeral(n: int) -> str:
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    res = ""
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            res += syb[i]
            n -= val[i]
        i += 1
    return res

def get_leaf_page_str(ln: int) -> str:
    if ln in [4, 8, 24]:
        return "Blank Leaf"
    if 1 <= ln <= 23:
        return roman_numeral(ln)
    if 25 <= ln <= 314:
        return str(ln - 24)
    appendix_map = {
        315: "Table I: Paschalion",
        316: "Table I: Paschalion (cont.)",
        317: "Table II: Indiction",
        318: "Table II: Indiction (cont.)",
        319: "Note on Sunday Letters",
        320: "Table III: Perpetual Paschalion"
    }
    return appendix_map.get(ln, f"Appendix {ln}")

def format_banner(ln: int) -> str:
    pg = get_leaf_page_str(ln)
    if pg == "Blank Leaf":
        return f"\n\n=== LEAF p{ln} ===\n[Blank Leaf]\n\n"
    return f"\n\n=== LEAF p{ln} ===\n[Book Page {pg}]\n\n"

# Load Incipit Dictionary
with open(PROJECT_ROOT / "scratch" / "liturgical_incipits_map.json", "r", encoding="utf-8") as f:
    incipit_map = json.load(f)

# Canonical extras for high-frequency Mikita incipits
canonical_extras = {
    'Blessed is our God': 'Благослове́нъ Бо́гъ на́шъ',
    'Blessed is the Kingdom': 'Благослове́но Ца́рство',
    'God is the Lord': 'Бо́гъ Госпо́дь',
    'God is the Lord, and hath appeared unto us': 'Бо́гъ Госпо́дь, и̂ яви́ся на́мъ',
    'God is the Lord, and has appeared unto us': 'Бо́гъ Госпо́дь, и̂ яви́ся на́мъ',
    'Glory to God in the highest': 'Сла́ва въ вы́шнихъ Бо́гу',
    'Heavenly King': 'Царю́ Небе́сный',
    'O Heavenly King': 'Царю́ Небе́сный',
    'Our Father': 'О́тче на́шъ',
    'Blessed is the man': 'Блаже́нъ мꙋ́жъ',
    'Have mercy on us, O God': 'Поми́луй на́съ, Бо́же',
    'Have mercy on me, O God': 'Поми́луй мя́, Бо́же',
    'Now dismiss': 'Ны́нѣ отпуща́еши',
    'Now lettest Thou Thy servant depart': 'Ны́нѣ отпуща́еши',
    'Vouchsafe, O Lord': 'Сподо́би, Го́споди',
    'More honorable than the Cherubim': 'Честнѣ́йшую Херуви́мъ',
    'O Theotokos and Virgin, rejoice': 'Богоро́дице Дѣ́во, ра́дуйся',
    'Blessed be the name of the Lord': 'Бꙋ́ди и̂́мя Госпо́дне',
    'I will bless the Lord at all times': 'Благословлю́ Го́спода на вся́кое вре́мя',
    'Glory, Both now': 'Сла́ва, И̂ ны́нѣ',
    'Glory, both now': 'Сла́ва, И̂ ны́нѣ',
    'Glory... Both now...': 'Сла́ва... И̂ ны́нѣ...',
    'Glory to the Father, and to the Son, and to the Holy Spirit': 'Сла́ва Отцу́, и̂ Сы́ну, и̂ Свято́му Ду́ху',
    'Both now and forever, and unto ages of ages. Amen': 'И̂ ны́нѣ, и̂ при́сно, и̂ во вѣ́ки вѣкѡ́въ. А̂ми́нь',
    'Both now and ever, and unto the ages of ages. Amen': 'И̂ ны́нѣ, и̂ при́сно, и̂ во вѣ́ки вѣкѡ́въ. А̂ми́нь',
    'Lord, have mercy': 'Го́споди, поми́луй',
    'Holy God': 'Святы́й Бо́же',
    'Holy God, Holy Mighty, Holy Immortal, have mercy on us': 'Святы́й Бо́же, Святы́й Крѣ́пкїй, Святы́й Безсме́ртный, поми́луй на́съ',
    'O Gladsome Light': 'Свѣ́те ти́хїй',
    'From my youth': 'Ѡ̂тъ ю́ности моея́',
    'The Noble Joseph': 'Благообра́зный Іѡ́сифъ',
    'Unto the Myrrh-bearing Women': 'Мироно́сицамъ жена́мъ',
    'When Thou didst descend unto death': 'Є̂гда́ снизше́лъ є̂сѝ къ сме́рти',
    'Christ is risen': 'Хрїсто́съ воскре́се',
    'Christ is risen from the dead, trampling down death by death': 'Хрїсто́съ воскре́се и̂зъ ме́ртвыхъ, сме́ртїю сме́рть попра́въ',
    'Open to me the doors of repentance, O Giver of Life': 'Покая́нїя отве́рзи мѝ две́ри, Жизнода́вче',
    'On the waters of Babylon': 'На рѣка́хъ Вавѷлѡ́нскихъ',
    'By the waters of Babylon': 'На рѣка́хъ Вавѷлѡ́нскихъ',
    'Praise the name of the Lord': 'Хвали́те и̂́мя Госпо́дне',
    'My soul doth magnify the Lord': 'Вели́читъ душа́ моя́ Го́спода',
    'Resurrection of Christ having beheld': 'Воскресе́нїе Хрїсто́во ви́дѣвше',
    'Having beheld the Resurrection of Christ': 'Воскресе́нїе Хрїсто́во ви́дѣвше'
}
for k, v in canonical_extras.items():
    if k not in incipit_map:
        incipit_map[k] = v

sorted_incipit_keys = sorted(incipit_map.keys(), key=lambda x: -len(x))

def enrich_incipits(text: str) -> str:
    """Enriches English incipits in quotes with Church Slavonic parentheticals."""
    for key in sorted_incipit_keys:
        slav = incipit_map[key]
        pattern = re.compile(rf'([“"]{re.escape(key)}[”"])(?!\s*\(\*)')
        text = pattern.sub(rf'\1 (*{slav}*)', text)
    return text

def remediate_slop_mikita(text: str) -> str:
    """Fixes known slop occurrences in Mikita."""
    text = text.replace("how wondrous is the material element", "how marvelous is the material element")
    text = re.sub(r'\bwherefore\b', 'therefore', text)
    text = re.sub(r'\bWherefore\b', 'Therefore', text)
    return text

def process_cohorts():
    print("--- 1. Updating Mikita Cohort and Draft Files ---")
    final_dir = M3_DIR / "Final"
    draft_dir = M3_DIR / "Draft"
    
    cohort_files = sorted(final_dir.glob("1901_mikita_typikon_cohort*.txt"), key=lambda p: int(re.search(r'cohort(\d+)', p.name).group(1)))
    
    for cf in cohort_files:
        txt = cf.read_text(encoding="utf-8")
        
        def rep_banner(m):
            ln = int(m.group(1))
            return format_banner(ln).strip() + "\n\n"
        
        # Replace comments with banners if not already replaced
        if "<!-- LEAF" in txt:
            txt = re.sub(r'<!--\s*LEAF:\s*p?(\d+)[^>]*-->\s*', rep_banner, txt)
        txt = enrich_incipits(txt)
        txt = remediate_slop_mikita(txt)
        cf.write_text(txt, encoding="utf-8")
        
        # Corresponding draft
        c_num = re.search(r'cohort(\d+)', cf.name).group(1)
        df = draft_dir / f"1901_mikita_typikon_cohort{c_num}_raw_draft.md"
        if df.exists():
            d_txt = df.read_text(encoding="utf-8")
            if "<!-- LEAF" in d_txt:
                d_txt = re.sub(r'<!--\s*LEAF:\s*p?(\d+)[^>]*-->\s*', rep_banner, d_txt)
            d_txt = enrich_incipits(d_txt)
            d_txt = remediate_slop_mikita(d_txt)
            df.write_text(d_txt, encoding="utf-8")
    print(f"Updated {len(cohort_files)} cohorts and drafts with leaf banners and Slavonic incipits.")

def process_complete_and_parts():
    print("--- 2. Positioning Leaves and Enriching Mikita Complete Edition ---")
    final_dir = M3_DIR / "Final"
    cohort_files = sorted(final_dir.glob("1901_mikita_typikon_cohort*.txt"), key=lambda p: int(re.search(r'cohort(\d+)', p.name).group(1)))
    
    complete_md_path = M3_DIR / "Final MD" / "1901_mikita_typikon_complete.md"
    complete_txt = complete_md_path.read_text(encoding="utf-8")
    
    # Enrich complete_txt and remediate slop FIRST so landmarks match exactly
    complete_txt = enrich_incipits(complete_txt)
    complete_txt = remediate_slop_mikita(complete_txt)
    
    # Extract landmarks from cohort files
    leaf_landmarks = {}
    for cf in cohort_files:
        txt = cf.read_text(encoding="utf-8")
        splits = re.split(r'===\s*LEAF\s+p?(\d+)[^\n]*\n(?:\[[^\]]+\]\s*)?', txt)
        for i in range(1, len(splits), 2):
            ln = int(splits[i])
            chunk = splits[i+1].strip()
            lines = [l.strip() for l in chunk.splitlines() if l.strip() and l.strip() != '*Page*']
            landmark = lines[0][:60] if lines else ""
            leaf_landmarks[ln] = landmark
            
    positions = []
    search_start = 0
    for ln in range(1, 321):
        if ln in [4, 8, 24]:
            continue
        lm = leaf_landmarks[ln]
        pos = complete_txt.find(lm, search_start)
        if pos == -1:
            pos = complete_txt.find(lm, 0)
        assert pos != -1, f"Could not find leaf {ln} landmark: {repr(lm)}"
        positions.append((ln, pos))
        search_start = pos
    
    pos_map = dict(positions)
    # Leaf 4 before Preface (Leaf 5)
    pos_map[4] = pos_map[5]
    # Leaf 8 before Contents (Leaf 9)
    pos_map[8] = pos_map[9]
    # Leaf 24 before Part I (Leaf 25)
    pos_map[24] = pos_map[25]
    
    # Inject banners in descending order of position
    all_leaves_sorted = sorted(pos_map.items(), key=lambda x: (x[1], x[0]), reverse=True)
    
    for ln, pos in all_leaves_sorted:
        banner = format_banner(ln)
        complete_txt = complete_txt[:pos] + banner + complete_txt[pos:]
        
    complete_txt = complete_txt.replace("\n\n\n\n=== LEAF", "\n\n=== LEAF")
    
    complete_md_path.write_text(complete_txt, encoding="utf-8")
    (M3_DIR / "Final" / "1901_mikita_typikon_complete.txt").write_text(complete_txt, encoding="utf-8")
    print("Successfully injected all 320 leaves into complete.md and complete.txt!")

    print("--- 3. Updating Mikita Modular Part Files ---")
    p0_start = complete_txt.find("=== LEAF p1 ===")
    p1_start = complete_txt.find("=== LEAF p25 ===")
    p2_start = complete_txt.find("=== LEAF p51 ===")
    fn_start = complete_txt.find("## Footnotes")
    if fn_start == -1:
        fn_start = complete_txt.find("[^1]:")
    
    p0_text = complete_txt[p0_start:p1_start].strip() + "\n"
    p1_text = complete_txt[p1_start:p2_start].strip() + "\n"
    p2_text = complete_txt[p2_start:fn_start].strip() + "\n"
    
    (M3_DIR / "Final MD" / "1901_mikita_part0_intro_and_toc.md").write_text(p0_text, encoding="utf-8")
    (M3_DIR / "Final" / "1901_mikita_part0_intro_and_toc.txt").write_text(p0_text, encoding="utf-8")
    
    (M3_DIR / "Final MD" / "1901_mikita_part1_general_services.md").write_text(p1_text, encoding="utf-8")
    
    (M3_DIR / "Final MD" / "1901_mikita_part2_particular_services.md").write_text(p2_text, encoding="utf-8")
    (M3_DIR / "Final" / "1901_mikita_part2_particular_services.txt").write_text(p2_text, encoding="utf-8")
    print("Updated Part 0, Part 1, Part 2 files.")

def remediate_synod_slop():
    print("--- 4. Remediating Monument 1 (1891 Lviv Synod) Residual Slop ---")
    synod_complete = M1_DIR / "Final MD" / "1891_lviv_synod_complete.md"
    txt = synod_complete.read_text(encoding="utf-8")
    
    txt = txt.replace("wandered from the right way, and fell into wondrous darkness", "wandered from the right way, and fell into terrible darkness")
    txt = txt.replace("since her wondrous propagation", "since her marvelous propagation")
    txt = txt.replace("the priest shall cense the honorable Gifts", "the priest censes the honorable Gifts")
    txt = txt.replace("the wondrous costliness and beauty", "the marvelous costliness and beauty")
    txt = txt.replace("to be consumed by a fire far more wondrous", "to be consumed by a fire far more marvelous")
    txt = txt.replace("lest peradventure the faithful be scandalized", "lest perhaps the faithful be scandalized")
    
    synod_complete.write_text(txt, encoding="utf-8")
    
    txt_alt = M1_DIR / "Final" / "1891_lviv_synod_complete.txt"
    if txt_alt.exists():
        txt_alt.write_text(txt, encoding="utf-8")
    txt_synod = M1_DIR / "Final" / "1891_synod_complete.txt"
    if txt_synod.exists():
        txt_synod.write_text(txt, encoding="utf-8")
    print("Remediated Synod slop.")

if __name__ == "__main__":
    process_cohorts()
    process_complete_and_parts()
    remediate_synod_slop()
    print("ALL EPIGRAPHIC AND SLOP RESTORATION TASKS COMPLETED SUCCESSFULLY!")
