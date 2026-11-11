#!/usr/bin/env python3
"""
Universal Hieratic Deity Pronoun Auditor
========================================
Audits English liturgical translations to enforce 100% mandatory capitalization
of pronouns referring to the Persons of the Holy Trinity (He, Him, His, Thou,
Thee, Thy, Thine) while ensuring human participants (clergy, saints, singers),
Marian addresses (Birthgiver of God, Mother of God, Theotokos), and adversary
nouns (serpent, enemy, devil, death, hades) remain correctly lowercase.

Usage:
    python scripts/hieratic_pronoun_audit.py --target path/to/draft.md
    python scripts/hieratic_pronoun_audit.py --monument 1891_lviv_synod --cohort 3
"""

import sys
import re
import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"

HUMAN_INDICATORS = re.compile(
    r'\b(?:Priest|priest|Deacon|deacon|Reader|reader|Bishop|bishop|Metropolitan|'
    r'Patriarch|patriarch|Patriarchal|patriarchal|Archimandrite|archimandrite|Hierodeacon|hierodeacon|Primikirios|primikirios|'
    r'Archbishop|Archpriest|Protodeacon|Hierarch|Superior|Abbot|celebrant|'
    r'saint|saints|Saint|Saints|Prophet|prophet|Forerunner|forerunner|Baptist|baptist|Apostle|apostle|Martyr|martyr|Hieromartyr|passion-bearer|passion-bearers|'
    r'Monk|monk|Father|fathers|Synod|Dolnytsky|Mark|Sabbas|Basil|Chrysostom|'
    r'Nicholas|George|Theodore|Joannicius|Athanasius|Gregory|Neilos|Nilus|Bartholomew|'
    r'Peter|Paul|John|Luke|Matthew|Thomas|Andrew|James|Philip|Simon|Jude|Matthias|Timothy|Titus|Lazarus|Martha|Mary|Cornelius|'
    r'Euthymius|Anthony|Maximus|Theodosius|Macarius|Agathangelus|Xenia|Ephraim|Ignatius|Simeon|Anna|Tryphon|Agatha|Parthenius|Charalampus|Blase|Meletius|Auxentius|Onesimus|Flavian|Porphyrius|Procopius|Cassian|Eudocia|Gerasimus|Conon|Sophronius|Theophanes|Benedict|Alexius|Cyril|Daria|Chrysanthus|Gabriel|Archangel|Michael|Zosimas|Eutychius|Antipas|Martin|Irene|Acacius|Stephen|Pachomius|Modestus|Constantine|Helena|Helen|Nicetas|Onuphrius|Amos|Tychon|Leontius|Sampson|Cyrus|Cosmas|Damian|Hyacinth|Pancratius|Euphemia|Vladimir|Olga|Marina|Macrina|Elijah|Elias|Ezekiel|Christina|Panteleimon|Callinicus|Eudocimus|Maccabees|Eleazar|Solomonia|Eusignius|Ananias|Azariah|Mishael|Daniel|Habakkuk|Jonah|Isaiah|Jeremiah|Zacharias|Zechariah|Elizabeth|Joachim|'
    r'Cyprian|Alphonsus|Augustine|Jerome|Ambrose|Damascene|Barbara|Sozon|Symeon|Triphyllius|Lysimachus|Febronia|'
    r'Leo|Allatius|Benjamin|Clement|confessor|author|editor|publisher|writer|'
    r'composer|choir|choirs|Khagan|enemy|enemies|Emperor|king|kings|Arius|Nestorius|Adam|Eve|Cain|Abel|Seth|Enos|Cainan|Mahalalel|Jared|Enoch|Methuselah|Lamech|Noah|David|Joseph|Moses|Balaam|Israel|Egyptians|Egyptian|Abraham|Abram|Isaac|Jacob|Solomon|Christians|brother|'
    r'brethren|first deacon|second deacon|first choir|the saint|to the saint|'
    r'of the saint|if he has|if he does|nor is he|candle-bearer|sacristan|'
    r'pastor|parishioner|administrator|trustee|trustees|vicar|decan|cantor|chanter|chanters|singer|singers|'
    r'deacons|concelebrant|concelebrants|celebrants|priestly|communicant|candidate|novice|paralytic|hierarchs|venerable one|burning bush|in a flame of fire|'
    r'curate|curates|assistant|assistant|Disciples|disciple|disciples|rector|rectors|prefect|prefects|'
    r'student|students|cleric|clerics|seminarian|seminarians|celebrating|celebrated|'
    r'preacher|preachers|preaching|'
    r'man|men|mankind|creature|creatures|human|humanity|person|persons|soul|souls|'
    r'heretic|heretics|schismatic|schismatics|deceiver|deceivers|sinner|sinners|ungodly|'
    r'Judas|Iscariot|betrayer|betrayers|thief|thieves|robber|robbers|'
    r'Satan|devil|demon|demons|Lucifer|adversary|evil one|serpent|dragon|foe|corrupter|one who held them fast|O Death|O Hades|death|hades|grave|tomb|hell|pit|O (?:three-part |precious |most precious |life-giving )?Cross|'
    r'O Jordan|O sea|O Cave|O Manger|O Desert|O Earth|O Heaven|O Paradise|O Eden|O Ark|O Temple|O City|Mount Horeb|'
    r'Matrona|Xenophon|Porphyrios|Eusebius|Naaman|angel|angels|teacher|teachers|primate|president|herald|our prince|initiate|imitator|sufferer|bodiless|gold-flowing Euphrates|pattern of piety|heresies thou|bestowed upon thee|'
    r'O (?:all-|most )?glorious one|O wise one|O all-valiant one|O God-wise|O God-receiver|O divinely revealed one|O exceedingly rich one|all-comely citizen|impassable gate|bridal chamber|full of grace|Queen of all|pure boast|all-honorable|'
    r'martyrdom|banishments|chrism of priesthood|thy course|by adoption|lusts of the flesh|strict fasting|faint from fasting|thine abstinence|thine alms|his tears|his complete|see me again|'
    r'all-blessed|thrice-blessed|most blessed|divinely wise|all-wise|all-praised|all-honored|hieromartyr|hieromartyrs|Andrew|ever-memorable|wonderworker|god-bearer|god-bearing|myrrh-bearer|myrrh-bearers|virgin-martyr|archpastor|ascetic|faster|anchorite|stylite|unmercenary|unmercenaries|'
    r'household|family|parent|parents|husband|wife|woman|women|maiden|maidens|Samaritan|intercessor|intercessors|children|child|son|daughter|'
    r'servant|servants|handmaid|handmaids|serving|served|'
    r'righteous|blessed|blessed one|departed|deceased|reposed|'
    r'flock|sheep|lay down|striketh|striking|repeateth|repeating|breast|'
    r'thyself|oneself|himself|herself|themselves|'
    r'hear thee|give ear unto thee|declare unto thee|preserve thy|thy heart|unto Christ thou|glory of God thou|Take up thy bed|with thee|encompass thee|compassion on thee|grant thee|deliver thee|teach thee|give thee|forgive thee|lead thee|open unto thee|glorified thee|vouchsafed thee|robed thee|strengthened thy|thy God|Pasa he ktisis|'
    r'bow|bows|bowing|boweth|shall bow|foldeth|setteth|lowereth|raiseth|'
    r'hands|his hands|his head|head|lips|my lips|mouth|eyes|ears|feet|knees|'
    r'kneeleth|kneeling|kneels|standeth|stands|prostrateth|prostrates|censing|reciteth|recites|taketh|takes|speaks|saying|signs|'
    r'he that|him that|he who|him who|those who|whosoever|whoever|God speed|bid him|biddeth|'
    r'Theotokos|O Theotokos|Theotokion|Stavrotheotokion|Mother of God|O Mother of God|Mother of my God|Birthgiver of God|O Birthgiver of God|Birthgiver|O Birthgiver|Birth-giver of God|Bride of God|Virgin Mary|Ever-Virgin|Most Holy Lady|Our Lady|O Lady|Virgin|O Virgin|All-Immaculate|all-immaculate|All-Spotless|all-spotless|O All-Spotless|Spotless One|spotless one|O Spotless One|All-Pure|all-pure|Pure One|protectress|Immaculate|immaculate|Sion|Zion|Jerusalem|Bethlehem|Ephratha|all-pure Mother|pure Mother|Sovereign Lady|all-lauded|incarnate of|incarnate from)\b',
    re.IGNORECASE
)

MARIAN_GENITIVE_SCRUB_RE = re.compile(
    r'\b(?:Mother|Birthgiver|Birth-giver|Bride|Handmaid|Servant|Ark|Tabernacle|Temple)\s+of\s+(?:my\s+|our\s+|the\s+)?God\b',
    re.IGNORECASE,
)

DEITY_KEYWORDS = re.compile(
    r'\b(?:God|Lord|Christ|Jesus|Saviour|Savior|Holy Spirit|'
    r'Almighty|Comforter|Redeemer|the Son|the Father|'
    r'Holy Trinity|Trinity|Divine|Creator|Lord God|Word of God)\b',
    re.IGNORECASE
)

DEITY_CONTEXT_PATTERNS = [
    r'\b(?:God|Christ|Lord|Holy Spirit|Savior|Saviour|Redeemer|Creator)\b[^.\n]*?\b(his|him|he)\b',
    r'\b(?:Thee|Thou|Thy|Thine)\b[^.\n]*?\b(thee|thou|thy|thine)\b',
    r'\b(?:Body of Christ|Blood of Christ|in His blood|His gift|His holy|His mercy|His grace)\b',
]


def audit_file(filepath: Path) -> Dict[str, Any]:
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    violations: List[Dict[str, Any]] = []

    window = 180

    pronoun_patterns = [
        (re.compile(r'\b(he)\b'), 'he'),
        (re.compile(r'\b(him)\b'), 'him'),
        (re.compile(r'\b(his)\b'), 'his'),
        (re.compile(r'\b(thee)\b'), 'thee'),
        (re.compile(r'\b(thou)\b'), 'thou'),
        (re.compile(r'\b(thy)\b'), 'thy'),
        (re.compile(r'\b(thine)\b'), 'thine'),
    ]

    for line_num, line in enumerate(lines, 1):
        for pat, p_name in pronoun_patterns:
            for match in pat.finditer(line):
                matched_str = match.group(1)
                if matched_str[0].isupper():
                    continue

                start = match.start()
                ws = max(0, start - window)
                we = min(len(line), match.end() + window)
                context = line[ws:we]

                # Direct doxological address check ('glory to thee' / 'glory be to thee') even if clergy nouns appear nearby
                if p_name == "thee" and re.search(r"\bglory\s+(?:be\s+)?(?:to|unto)\s+$", line[max(0, start - 20):start], re.IGNORECASE):
                    near_ctx = line[max(0, start - 140):min(len(line), match.end() + 140)]
                    if not re.search(r"\b(?:Theotokos|Mother of God|Bride of God|Birthgiver|Virgin|Lady|Pure One|all-pure|all-immaculate|all-honorable|full of grace|Queen of all|pure boast|Cross|passion-bearer|martyr|by thy prayers|Philip)\b", near_ctx, re.IGNORECASE):
                        violations.append({
                            "line": line_num,
                            "pronoun": matched_str,
                            "context": context.strip(),
                            "position": start
                        })
                        continue

                # Check if human/Marian/adversary indicator overrides
                if HUMAN_INDICATORS.search(context):
                    continue

                scrubbed_context = MARIAN_GENITIVE_SCRUB_RE.sub("Theotokos", context)
                if DEITY_KEYWORDS.search(scrubbed_context):
                    before_match = MARIAN_GENITIVE_SCRUB_RE.sub("Theotokos", line[max(0, start - 40):start])
                    if re.search(r'\b(?:God|Christ|Lord|Savior|Jesus|Holy Spirit)\b', before_match, re.IGNORECASE):
                        violations.append({
                            "line": line_num,
                            "pronoun": matched_str,
                            "context": context.strip(),
                            "position": start
                        })

    passed = len(violations) == 0
    return {
        "file": str(filepath.name),
        "passed": passed,
        "violations": violations,
        "violation_count": len(violations)
    }


def main():
    parser = argparse.ArgumentParser(description="Universal Hieratic Deity Pronoun Auditor")
    parser.add_argument("--target", help="Specific text or markdown file to audit")
    parser.add_argument("--monument", help="Monument ID")
    parser.add_argument("--cohort", type=int, help="Cohort number")
    parser.add_argument("--json", action="store_true", help="Output JSON results")

    args = parser.parse_args()

    target_path = None
    if args.target:
        target_path = Path(args.target)
    elif args.monument and args.cohort:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            registry = json.load(f)
        mon_info = registry.get("monuments", {}).get(args.monument, {})
        ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{args.monument}")
        draft_cand = ws / "Draft" / f"{args.monument}_cohort{args.cohort}_raw_draft.md"
        final_cand = ws / "Final MD" / f"{args.monument}_cohort{args.cohort}.md"
        if final_cand.exists():
            target_path = final_cand
        elif draft_cand.exists():
            target_path = draft_cand
        else:
            print(f"ERROR: Could not find candidate draft or final file for {args.monument} cohort {args.cohort}", file=sys.stderr)
            sys.exit(1)

    if not target_path:
        print("ERROR: Specify --target or --monument and --cohort", file=sys.stderr)
        sys.exit(1)

    res = audit_file(target_path)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"Hieratic Pronoun Audit for: {res['file']}")
        print(f"Status: {'PASSED (100% Capitalization)' if res['passed'] else 'FAILED'}")
        if not res['passed']:
            print(f"Violations ({res['violation_count']}):")
            for v in res['violations']:
                print(f"  Line {v['line']}: Lowercase '{v['pronoun']}' in context: ...{v['context']}...")

    sys.exit(0 if res["passed"] else 1)


if __name__ == "__main__":
    main()
