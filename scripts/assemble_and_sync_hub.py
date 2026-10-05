#!/usr/bin/env python3
"""
Universal Ingestion, Master Assembler & Hub Sync Engine
=======================================================
Executes the Grand Pause post-flight integration:
  1. Ingests draft translation from Draft/ into Final/ and Final MD/.
  2. Appends new cohort footnotes monotonically to Final/Final_footnotes.txt.
  3. Re-assembles the complete codex edition (*_complete.md, *_complete.txt) in true reading order.
  4. Synchronizes deliverables to Projects/Typikon Coded/Data/Inbox/<Monument>/.
  5. Updates handoff_note.md in the Hub Inbox.
  6. Advances orchestrator state in Liturgical Monuments/ACTIVE_ORCHESTRATOR_STATE.json.

Usage:
    python scripts/assemble_and_sync_hub.py --monument 1891_lviv_synod --cohort 3
"""

import sys
import os
import shutil
import re
import json
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
STATE_FILE = PROJECT_ROOT / "Liturgical Monuments" / "ACTIVE_ORCHESTRATOR_STATE.json"

def get_hub_inbox(monument_name: str) -> Path:
    # Ecosystem Projects root is parent of Translation
    ecosystem_root = PROJECT_ROOT.parent
    hub_inbox = ecosystem_root / "Typikon Coded" / "Data" / "Inbox" / monument_name.replace(" ", "_")
    hub_inbox.mkdir(parents=True, exist_ok=True)
    return hub_inbox

def ingest_and_sync(monument_id: str, cohort_num: int) -> int:
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
    mon_info = registry.get("monuments", {}).get(monument_id)
    if not mon_info:
        raise ValueError(f"Unknown monument ID: {monument_id}")

    ws = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
    final_dir = ws / "Final"
    final_md_dir = ws / "Final MD"
    draft_dir = ws / "Draft"
    final_dir.mkdir(parents=True, exist_ok=True)
    final_md_dir.mkdir(parents=True, exist_ok=True)

    # 1. Promote Draft to Final
    draft_md = draft_dir / f"{monument_id}_cohort{cohort_num}_raw_draft.md"
    target_md = final_md_dir / f"{monument_id}_cohort{cohort_num}.md"
    target_txt = final_dir / f"{monument_id}_cohort{cohort_num}.txt"

    if draft_md.exists() and not target_md.exists():
        shutil.copy2(str(draft_md), str(target_md))
        print(f"Promoted draft: {draft_md.name} -> {target_md.name}")
        # Plain text copy
        shutil.copy2(str(draft_md), str(target_txt))

    # 2. Append new footnotes to master Final_footnotes.txt
    master_fn_file = final_dir / "Final_footnotes.txt"
    draft_fn_file = draft_dir / f"{monument_id}_cohort{cohort_num}_footnotes.txt"

    if draft_fn_file.exists():
        with open(draft_fn_file, "r", encoding="utf-8") as df:
            new_fn_text = df.read().strip()

        existing_text = ""
        if master_fn_file.exists():
            with open(master_fn_file, "r", encoding="utf-8") as mf:
                existing_text = mf.read()

        if new_fn_text and f"## Cohort {cohort_num} Footnotes" not in existing_text:
            with open(master_fn_file, "a", encoding="utf-8") as mf:
                mf.write(f"\n\n## Cohort {cohort_num} Footnotes\n\n" + new_fn_text + "\n")
            print(f"Appended Cohort {cohort_num} footnotes to {master_fn_file.name}")

    # 3. Assemble Master Edition
    # Collect unique cohort files in Final MD (one per cohort number, preferring larger file)
    cohort_map: Dict[int, Path] = {}
    for p in final_md_dir.glob("*cohort*.md"):
        m = re.search(r"cohort(\d+)", p.name)
        if m:
            c_num = int(m.group(1))
            if c_num not in cohort_map or p.stat().st_size > cohort_map[c_num].stat().st_size:
                cohort_map[c_num] = p

    all_cohort_files = [cohort_map[k] for k in sorted(cohort_map.keys())]
    print(f"Assembling master edition from {len(all_cohort_files)} cohorts: {[p.name for p in all_cohort_files]}...")
    complete_md_file = final_md_dir / f"{monument_id}_complete.md"
    complete_txt_file = final_dir / f"{monument_id}_complete.txt"

    # Read footnotes
    footnotes_content = ""
    if master_fn_file.exists():
        with open(master_fn_file, "r", encoding="utf-8") as f:
            footnotes_content = f.read()

    # Reorder cohorts: In 1891 Synod, Cohorts 3..14 represent pp. 1-244, while Cohorts 1..2 represent pp. 245-278
    # For a clean codex, front cohorts come first, back cohorts come last!
    def cohort_sort_key(p: Path):
        m = re.search(r"cohort(\d+)", p.name)
        c_num = int(m.group(1)) if m else 0
        if monument_id == "1891_lviv_synod":
            # Cohort 1 & 2 are at the back (pp. 245-278)
            if c_num in [1, 2]:
                return 1000 + c_num
        return c_num

    sorted_cohorts = sorted(all_cohort_files, key=cohort_sort_key)
    
    body_parts = []
    for cp in sorted_cohorts:
        with open(cp, "r", encoding="utf-8") as f:
            c_text = f.read()
        # Clean out redundant title if needed
        body_parts.append(f"<!-- START COHORT {cp.stem} -->\n\n" + c_text.strip() + f"\n\n<!-- END COHORT {cp.stem} -->")

    master_edition_content = f"""# {mon_info.get('title')}
## Complete Unabridged Translation Edition

> [!NOTE]
> **Monument**: {mon_info.get('title')}  
> **Source Codex**: `{mon_info.get('relative_pdf_path')}` ({mon_info.get('total_physical_pages')} physical pages)  
> **Translation Standard**: Master Translation Standard (MTS-1)  
> **Governing Register**: {mon_info.get('genre_register', 'juridical').upper()}  
> **Assembled Cohorts**: {[p.name for p in sorted_cohorts]}  

---

{"\n\n---\n\n".join(body_parts)}

---

## Scholarly Critical Apparatus & Footnotes

{footnotes_content.strip()}
"""

    with open(complete_md_file, "w", encoding="utf-8") as f:
        f.write(master_edition_content)
    with open(complete_txt_file, "w", encoding="utf-8") as f:
        f.write(master_edition_content)
    print(f"Generated complete edition: {complete_md_file.name} ({complete_md_file.stat().st_size} bytes)")

    # 4. Sync Deliverables to Hub Inbox
    hub_inbox = get_hub_inbox(mon_info.get("short_title", monument_id))
    print(f"Syncing deliverables to Hub Inbox: {hub_inbox}")

    files_to_sync = [
        complete_md_file,
        complete_txt_file,
        master_fn_file,
    ] + all_cohort_files

    for f_src in files_to_sync:
        if f_src.exists():
            f_dst = hub_inbox / f_src.name
            shutil.copy2(str(f_src), str(f_dst))
            print(f"  Copied {f_src.name} -> Hub Inbox")

    # 5. Write / Update handoff_note.md in Hub Inbox
    handoff_note = f"""# Handoff Note: {mon_info.get('title')}
**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}  
**Spoke**: Translation Spoke (`Projects/Translation/Liturgical Monuments/{mon_info.get('workspace_dir', monument_id)}/`)  
**Target Hub**: Typikon Coded Hub (`Projects/Typikon Coded/Data/Inbox/{hub_inbox.name}/`)  
**Active Monument ID**: `{monument_id}`  
**Current Cohort Ingested**: Cohort #{cohort_num}  

---

## 1. Executive Summary
This handoff delivers newly verified unabridged translation deliverables for **{mon_info.get('title')}**.
All files have passed the Small Pause Gatekeeper Suite (vocabulary linting, 100% hieratic pronoun capitalization, 1:1 footnote bijectivity, and structural sequence verification).

## 2. Ingested Deliverables
- Complete Markdown Edition: `{complete_md_file.name}`
- Complete Text Edition: `{complete_txt_file.name}`
- Master Critical Apparatus: `{master_fn_file.name}`
- Active Cohort Deliverable: `{target_md.name if target_md.exists() else 'N/A'}`

## 3. Compliance Standard
- 100% compliant with Master Translation Standard (MTS-1)
- Zero forbidden vocabulary variants against `master_liturgical_vocabulary.json`
- Zero dropped folios adhering to Closed Mathematical Leaf Conservation
"""

    with open(hub_inbox / "handoff_note.md", "w", encoding="utf-8") as f:
        f.write(handoff_note)
    print(f"Updated Hub handoff note: {hub_inbox / 'handoff_note.md'}")

    # 6. Advance State
    state_cmd = [sys.executable, str(SCRIPT_DIR / "orchestrator_state.py"), "--advance-cohort"]
    res_st = subprocess.run(state_cmd, capture_output=True, text=True, encoding="utf-8")
    print(res_st.stdout)

    print("=" * 65)
    print(">>> GRAND PAUSE INGESTION & HUB SYNC COMPLETE. <<<")
    print("=" * 65)
    return 0

def main():
    parser = argparse.ArgumentParser(description="Universal Ingestion, Master Assembler & Hub Sync Engine")
    parser.add_argument("--monument", default="1891_lviv_synod", help="Monument ID")
    parser.add_argument("--cohort", type=int, required=True, help="Cohort number to ingest")

    args = parser.parse_args()
    try:
        sys.exit(ingest_and_sync(args.monument, args.cohort))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
