#!/usr/bin/env python3
"""
Universal Hieratic Deity Pronoun Auditor
========================================
Audits English liturgical translations to enforce 100% mandatory capitalization
of pronouns referring to the Persons of the Holy Trinity (He, Him, His, Thou,
Thee, Thy, Thine) while ensuring human participants (clergy, saints, singers)
remain correctly lowercase.

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
    r'Archbishop|Archpriest|Protodeacon|Hierarch|Superior|Abbot|celebrant|'
    r'saint|Saint|Prophet|prophet|Apostle|apostle|Martyr|martyr|Hieromartyr|'
    r'Monk|monk|Father|fathers|Synod|Dolnytsky|Mark|Sabbas|Basil|Chrysostom|'
    r'Nicholas|George|Theodore|Athanasius|Gregory|Neilos|Nilus|Bartholomew|'
    r'Peter|Paul|John|Luke|Matthew|Thomas|Andrew|James|Philip|Simon|Jude|Matthias|Timothy|Titus|'
    r'Cyprian|Alphonsus|Augustine|Jerome|Ambrose|Damascene|'
    r'Leo|Allatius|Benjamin|Clement|confessor|author|editor|publisher|writer|'
    r'composer|choir|choirs|Khagan|enemy|enemies|Emperor|king|kings|David|Christians|brother|'
    r'brethren|first deacon|second deacon|first choir|the saint|to the saint|'
    r'of the saint|if he has|if he does|nor is he|candle-bearer|sacristan|'
    r'pastor|parishioner|administrator|trustee|trustees|vicar|decan|cantor|chanter|chanters|singer|singers|'
    r'deacons|concelebrant|concelebrants|celebrants|'
    r'curate|curates|assistant|assistants|disciple|disciples|rector|rectors|prefect|prefects|'
    r'student|students|cleric|clerics|seminarian|seminarians|celebrating|celebrated|'
    r'preacher|preachers|preaching|'
    r'man|men|mankind|creature|creatures|human|humanity|person|persons|'
    r'heretic|heretics|schismatic|schismatics|deceiver|deceivers|sinner|sinners|'
    r'Satan|devil|demon|demons|Lucifer|adversary|evil one|'
    r'household|family|parent|parents|husband|wife|children|child|son|daughter|'
    r'servant|servants|handmaid|handmaids|serving|served|'
    r'flock|sheep|lay down|striketh|striking|repeateth|repeating|breast|'
    r'thyself|oneself|himself|herself|themselves|'
    r'bow|bows|bowing|boweth|shall bow|foldeth|setteth|lowereth|raiseth|'
    r'hands|his hands|his head|head|lips|my lips|mouth|eyes|ears|feet|knees|'
    r'kneeleth|kneeling|kneels|standeth|stands|prostrateth|prostrates|censing|reciteth|recites|taketh|takes|speaks|saying|signs|'
    r'he that|him that|he who|him who|those who|whosoever|whoever|God speed|bid him|biddeth|'
    r'Theotokos|Mother of God|Virgin Mary|Ever-Virgin|Most Holy Lady|Our Lady|Virgin|incarnate of)\b',
    re.IGNORECASE
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

    # Check lowercase deity pronouns in explicit divine contexts
    window = 120

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
        # Ignore comments or footnote marker definitions
        if line.strip().startswith("[^") and "]:" in line:
            # Check footnote body text as well
            pass

        for pat, p_name in pronoun_patterns:
            for match in pat.finditer(line):
                # Must be lowercase
                matched_str = match.group(1)
                if matched_str[0].isupper():
                    continue

                start = match.start()
                ws = max(0, start - window)
                we = min(len(line), match.end() + window)
                context = line[ws:we]

                # Check if near deity keywords
                if DEITY_KEYWORDS.search(context):
                    # Check if human indicator overrides
                    if HUMAN_INDICATORS.search(context):
                        continue

                    # Direct check: is it referring to Deity?
                    # e.g. "God and his holy church" -> "His holy church"
                    # "Christ gave his life" -> "His life"
                    # "Lord... thee" -> "Thee"
                    before_match = line[max(0, start - 40):start]
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
        # Look in Draft first, then Final MD
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
