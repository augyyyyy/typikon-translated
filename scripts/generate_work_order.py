#!/usr/bin/env python3
"""
Universal Work Order & Startup Directive Generator
===================================================
Generates deterministic dispatch packets and full-monument autonomous startup
directives across the Byzantine-Ruthenian transmission chain.

Enforces Section 14 of .agents/AGENTS.md:
  - Generates comprehensive full-monument directives driving the automator across all cohorts.
  - Eliminates single-cohort stalls and copy-paste turns.

Usage:
    python scripts/generate_work_order.py --monument 1899_dolnytsky_typikon --monument-startup-directive
    python scripts/generate_work_order.py --monument 1899_dolnytsky_typikon --cohort 1
"""

import sys
import re
import json
import argparse
import math
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Typikons" / "codex_registry.json"
STATE_FILE = PROJECT_ROOT / "Typikons" / "ACTIVE_ORCHESTRATOR_STATE.json"

def get_next_footnote_index(footnotes_path: Path) -> int:
    if not footnotes_path.exists():
        return 1
    with open(footnotes_path, "r", encoding="utf-8") as f:
        text = f.read()
    markers = [int(m) for m in re.findall(r"\[\^(\d+)\]", text)]
    if not markers:
        return 1
    return max(markers) + 1

def parse_range_from_state(state: Dict[str, Any], cohort_num: int) -> Optional[Tuple[int, int]]:
    """Extract start and end page if state defines current_cohort_range matching cohort_num."""
    if state.get("current_cohort") == cohort_num:
        range_str = state.get("current_cohort_range", "")
        m = re.search(r"leaves\s+p(\d+)-p(\d+)", range_str)
        if m:
            return int(m.group(1)), int(m.group(2))
        m2 = re.search(r"pp\.\s*(\d+)-(\d+)", range_str)
        if m2:
            return int(m2.group(1)), int(m2.group(2))
    return None

def compute_monument_cohort_partitions(total_pages: int, cohort_size: int = 20) -> List[Dict[str, int]]:
    num_cohorts = math.ceil(total_pages / cohort_size)
    partitions = []
    for k in range(1, num_cohorts + 1):
        sp = ((k - 1) * cohort_size) + 1
        ep = min(total_pages, k * cohort_size)
        partitions.append({
            "cohort": k,
            "start_page": sp,
            "end_page": ep,
            "leaf_count": ep - sp + 1
        })
    return partitions

def generate_monument_startup_directive(monument_id: Optional[str] = None) -> Path:
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
    monuments = registry.get("monuments", {})

    state: Dict[str, Any] = {}
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)

    if not monument_id:
        monument_id = state.get("monument_id", "1899_dolnytsky_typikon")

    if monument_id not in monuments:
        raise ValueError(f"Unknown monument '{monument_id}'. Available: {list(monuments.keys())}")

    mon_info = monuments[monument_id]
    total_pages = mon_info.get("total_physical_pages", 591)
    cohort_size = mon_info.get("default_cohort_size", 20)
    genre_register = mon_info.get("genre_register", "rubrical")
    rel_pdf = mon_info.get("relative_pdf_path", "")
    workspace_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Typikons/{monument_id}")
    workspace_dir.mkdir(parents=True, exist_ok=True)
    (workspace_dir / "Source Text" / "images").mkdir(parents=True, exist_ok=True)
    (workspace_dir / "Draft").mkdir(parents=True, exist_ok=True)
    (workspace_dir / "Final").mkdir(parents=True, exist_ok=True)
    (workspace_dir / "Final MD").mkdir(parents=True, exist_ok=True)
    (workspace_dir / "Work_Orders").mkdir(parents=True, exist_ok=True)
    (workspace_dir / "Audit_Reports").mkdir(parents=True, exist_ok=True)

    partitions = compute_monument_cohort_partitions(total_pages, cohort_size)
    num_cohorts = len(partitions)
    rel_ws = mon_info.get("workspace_dir", monument_id).replace("\\", "/")

    # Build cohort partition table
    table_lines = [
        "| Cohort | Physical Pages | Leaf Count | Status | Target Deliverables |",
        "|---|---|---|---|---|"
    ]
    for p in partitions:
        table_lines.append(
            f"| **Cohort {p['cohort']:02d}** | pp. {p['start_page']}–{p['end_page']} | {p['leaf_count']} leaves | `PENDING` | `cohort{p['cohort']:02d}_source.txt` / `raw_draft.md` |"
        )
    table_str = "\n".join(table_lines)

    directive_content = f"""# Autonomous Monument Translation Directive: {mon_info.get('title')}
## Complete Unabridged Translation Execution Specification across All {num_cohorts} Cohorts

> [!IMPORTANT]
> **Sovereign Autonomous Execution Mandate (Rule 14 of `.agents/AGENTS.md`)**  
> This directive equips the Automator / Worker Agent with the **complete codex partition schedule and autonomous loop controller** for **{mon_info.get('title')}** ({total_pages} physical pages).  
> **Zero Inter-Cohort Human Stalls**: The Automator executes continuously through Cohort 1 to Cohort {num_cohorts}, triggering backend Small Pause Gates (`scripts/run_small_pause_gate.py`) automatically between cohorts.  
> Execution yields to the Human Operator **strictly and exclusively at the Sovereign Grand Pause** when 100% of all {total_pages} leaves are translated and assembled (`remaining_pages == 0`).

---

## 1. Codex Transmission Metadata & Conservation Scope
* **Monument ID**: `{monument_id}`
* **Title**: {mon_info.get('title')}
* **Source Facsimile**: `{rel_pdf}`
* **Total Physical Pages**: **{total_pages} leaves**
* **Cohort Bounding**: Strictly **{cohort_size} physical pages** per cohort ($15 \\le C \\le 25$, final cohort = {partitions[-1]['leaf_count']} leaves)
* **Total Scheduled Cohorts**: **{num_cohorts} cohorts**
* **Governing Register**: **{genre_register.upper()}** (Per Master Translation Standard MTS-1)
* **Mathematical Conservation**:
  $$\\mathbf{{Total\\ Physical\\ Pages\\ in\\ Codex}} \\equiv \\sum_{{k=1}}^{{{num_cohorts}}} C_k = ({num_cohorts - 1} \\times {cohort_size}) + {partitions[-1]['leaf_count']} = {total_pages} \\text{{ Leaves (100.0% Closed Conservation)}}$$

---

## 2. Inviolable Liturgical Translation Standards (MTS-1 / TA-1)

### A. Universal Native Vision Mandate (Physical Ink Sovereignty)
* Inspect each 300 DPI image (`p{{N}}.png`) in `{rel_ws}/Source Text/images/` directly.
* Cinnabar Rubrics: Red ink is visually identified and rendered in ceremonial italics (`*...*`); black ink is rendered in spoken/chanted prayers, psalmody, and hymnography.

### B. Ceremonial / Rubrical Register Norms ({genre_register.upper()})
* Concise, imperative, and active: Use **Active Present Indicative** for all rubrical actions (*"The Priest enters the sanctuary, venerates the Holy Table, and begins..."*).
* Absolute prohibition of gratuitous legalistic *"shall"*s in ordinary liturgical rubrics.

### C. Byzantine-Ruthenian Realia & Melodic Headings
* Technical Loanwords mandatory: `Tetrapod` (never "center table"), `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
* Ruthenian Chant Headings: Tone designations must be **`Tone 1`** through **`Tone 8`** (never Greek "Mode I").
* Model Melodies: **`Podoben: "[Canonical Incipit]"`**, **`Samohlasen`** (proper melody), **`Samopodoben`**.
* Dual Incipits: Bold English followed by italicized Slavonic (*"Lord, I have cried"* (*Господи воззвахъ*)).

### D. Father Paul Doxology Standard & Hieratic Pronouns
* Full choral: *"Glory be to the Father, and to the Son, and to the Holy Spirit, now and forever, and unto the ages of ages. Amen."*
* Shorthand rubric: *"Glory... Now and forever, and unto the ages of ages:"*
* **Strict Ban**: The phrase *"for ever and ever"* is 100% prohibited.
* **100% Deity Pronoun Capitalization**: Mandatory capitalization for Divine Persons (*He, Him, His, Thou, Thee, Thy, Thine*). Clergy, celebrants, saints, and rubrical "he" remain lowercase.

### E. Scripture & Psalter (Septuagint LXX)
* Mandatory Septuagint versification across all psalm citations and biblical references.

### F. Footnote Bijectivity
* Continuous monotonic numbering across the monument: Every `[^N]` in body text must have a matching `[^N]:` definition.

---

## 3. Autonomous Multi-Cohort Loop Controller Specification

For each cohort $k \\in [1, {num_cohorts}]$:

```
[COHORT LOOP: k = 1 to {num_cohorts}]
  1. INGESTION : Verify/render 300 DPI leaves p{{start}}..p{{end}} in '{rel_ws}/Source Text/images/'
  2. TRANSCRIPTION : Transcribe source ink into '{rel_ws}/Source Text/{monument_id}_cohort{{k}}_source.txt'
  3. TRANSLATION : Draft unabridged English into '{rel_ws}/Draft/{monument_id}_cohort{{k}}_raw_draft.md'
  4. FOOTNOTES : Write definitions into '{rel_ws}/Draft/{monument_id}_cohort{{k}}_footnotes.txt'
  5. SMALL PAUSE GATE : Run 'python scripts/run_small_pause_gate.py --monument {monument_id} --cohort {{k}}'
     - Gate 1: Shared_Lexicon/lint_vocabulary.py (0 violations)
     - Gate 2: scripts/hieratic_pronoun_audit.py (100% Deity capitalization)
     - Gate 3: scripts/reconcile_footnotes.py (1:1 footnote parity)
     - Gate 4: scripts/structural_audit.py (unbroken sequence)
  6. INTEGRATION : Run 'python scripts/assemble_and_sync_hub.py --monument {monument_id} --cohort {{k}}'
     - Promotes Draft -> Final MD & Final
     - Appends footnotes to Final_footnotes.txt
     - Advances ACTIVE_ORCHESTRATOR_STATE.json
  7. NEXT COHORT : If k < {num_cohorts}, immediately advance to cohort k+1. DO NOT pause for human input!
[END LOOP at k = {num_cohorts} -> REACHED SOVEREIGN GRAND PAUSE]
```

---

## 4. Complete Codex Partition Schedule ({num_cohorts} Cohorts)

{table_str}

---

## 5. Sovereign Grand Pause Termination
When Cohort {num_cohorts} completes its Small Pause Gate and final integration:
- `remaining_pages == 0`
- The entire {total_pages}-page codex is assembled in `{rel_ws}/Final MD/{monument_id}_complete.md`
- Deliverables are synchronized to `Projects/Typikon Coded/Data/Inbox/{mon_info.get('short_title', monument_id).replace(' ', '_')}/`
- Automator halts and delivers the final Grand Pause notification to the Human Operator.
"""

    directive_path = workspace_dir / "AUTONOMOUS_MONUMENT_DIRECTIVE.md"
    with open(directive_path, "w", encoding="utf-8") as f:
        f.write(directive_content)

    print(f"Generated Autonomous Monument Directive: {directive_path.relative_to(PROJECT_ROOT)}")
    return directive_path

def generate_work_order(
    monument_id: Optional[str] = None,
    cohort_num: Optional[int] = None,
    start_page: Optional[int] = None,
    end_page: Optional[int] = None,
    print_prompt: bool = True
) -> Path:
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
    monuments = registry.get("monuments", {})

    state: Dict[str, Any] = {}
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)

    if not monument_id:
        monument_id = state.get("monument_id", "1899_dolnytsky_typikon")

    if monument_id not in monuments:
        raise ValueError(f"Unknown monument '{monument_id}'. Available: {list(monuments.keys())}")

    mon_info = monuments[monument_id]
    total_pages = mon_info.get("total_physical_pages", 591)
    cohort_size = mon_info.get("default_cohort_size", 20)
    genre_register = mon_info.get("genre_register", "rubrical")
    workspace_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Typikons/{monument_id}")
    work_orders_dir = workspace_dir / "Work_Orders"
    work_orders_dir.mkdir(parents=True, exist_ok=True)

    if cohort_num is None:
        cohort_num = state.get("current_cohort", 1)

    if start_page is None or end_page is None:
        state_range = parse_range_from_state(state, cohort_num)
        if state_range:
            start_page, end_page = state_range
        else:
            start_page = ((cohort_num - 1) * cohort_size) + 1
            end_page = min(total_pages, cohort_num * cohort_size)

    leaf_count = (end_page - start_page) + 1
    footnotes_file = workspace_dir / "Final" / "Final_footnotes.txt"
    starting_footnote = get_next_footnote_index(footnotes_file)

    source_out = workspace_dir / "Source Text" / f"{monument_id}_cohort{cohort_num}_source.txt"
    draft_md_out = workspace_dir / "Draft" / f"{monument_id}_cohort{cohort_num}_raw_draft.md"
    footnotes_out = workspace_dir / "Draft" / f"{monument_id}_cohort{cohort_num}_footnotes.txt"
    images_dir = workspace_dir / "Source Text" / "images"

    work_order_file = work_orders_dir / f"cohort_{cohort_num:02d}_work_order.md"

    content = f"""# Work Order: {mon_info.get('title')} — Cohort {cohort_num}

**Document ID**: `{monument_id}`  
**Cohort Number**: {cohort_num}  
**Physical Leaves**: Physical pages {start_page} to {end_page} (`p{start_page}.png` through `p{end_page}.png`, {leaf_count} leaves total)  
**Starting Footnote Index**: `[^{starting_footnote}]`  
**Governing Genre Register**: **{genre_register.upper()}** (Per Master Translation Standard MTS-1)  
**Image Cache Directory**: `{images_dir.relative_to(PROJECT_ROOT)}`  

---

## 1. Statutory Mandates & Inviolable Guardrails (MTS-1 / TA-1)
1. **Physical Ink Witness**: Transcribe 100% directly from 300 DPI page images in `Source Text/images/`. Distinguish red cinnabar rubrics (render in italics `*...*`) from black text (render in standard Roman).
2. **Register Enforcement ({genre_register.capitalize()})**: Concise, imperative, Active Present Indicative for rubrical movements.
3. **Canonical Realia & Loanwords**: `Tetrapod`, `Klepalo`, `Aer`, `Kolyvo`, `Plashchanytsia`, `Sluzhebnik`, `Trebnik`.
4. **Father Paul Doxology Standard**: Banned phrase *"for ever and ever"*.
5. **Hieratic Deity Pronouns**: 100% mandatory capitalization for Holy Trinity pronouns (*He, Him, His, Thou, Thee, Thy, Thine*).
6. **Scripture & Psalter**: Septuagint (LXX) versification mandatory.
7. **Footnote Monotonic Bijectivity**: Every marker `[^N]` in body text MUST have an exact corresponding entry `[^N]:` in the footnotes file.

---

## 2. Target Disk Output Files
- **Source Text Transcription**: `{source_out.relative_to(PROJECT_ROOT)}`
- **Draft Markdown Translation**: `{draft_md_out.relative_to(PROJECT_ROOT)}`
- **Cohort Footnotes File**: `{footnotes_out.relative_to(PROJECT_ROOT)}`

---

## 3. Autonomous Execution Instructions
1. Inspect images `p{start_page}.png` through `p{end_page}.png` in `{images_dir.relative_to(PROJECT_ROOT)}`.
2. Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{start_page} ===`.
3. Translate unabridged into `{draft_md_out.name}` with inline footnote markers `[^N]`.
4. Write footnote definitions into `{footnotes_out.name}` starting at `[^{starting_footnote}]`.
5. Flush outputs to disk and advance through the autonomous pipeline.
"""

    with open(work_order_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated Work Order: {work_order_file.relative_to(PROJECT_ROOT)}")
    return work_order_file

def main():
    parser = argparse.ArgumentParser(description="Universal Work Order & Startup Directive Generator")
    parser.add_argument("--monument", help="Monument ID")
    parser.add_argument("--cohort", type=int, help="Cohort number")
    parser.add_argument("--start", type=int, help="Override start physical page")
    parser.add_argument("--end", type=int, help="Override end physical page")
    parser.add_argument("--monument-startup-directive", action="store_true", help="Generate full-monument autonomous directive across all cohorts")
    parser.add_argument("--no-prompt", action="store_true", help="Suppress console startup prompt")

    args = parser.parse_args()
    try:
        if args.monument_startup_directive:
            generate_monument_startup_directive(monument_id=args.monument)
        else:
            generate_work_order(
                monument_id=args.monument,
                cohort_num=args.cohort,
                start_page=args.start,
                end_page=args.end,
                print_prompt=not args.no_prompt
            )
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
