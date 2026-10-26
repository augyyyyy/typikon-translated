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
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
STATE_FILE = PROJECT_ROOT / "Liturgical Monuments" / "ACTIVE_ORCHESTRATOR_STATE.json"

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
    workspace_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
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

    template_dir = PROJECT_ROOT / "data" / "templates"
    directive_tpl = (template_dir / "monument_startup_directive_template.md").read_text(encoding="utf-8")
    directive_content = directive_tpl.format(
        title=mon_info.get("title"),
        num_cohorts=num_cohorts,
        num_cohorts_minus_1=num_cohorts - 1,
        total_pages=total_pages,
        monument_id=monument_id,
        rel_pdf=rel_pdf,
        cohort_size=cohort_size,
        last_leaf_count=partitions[-1]["leaf_count"],
        genre_register_upper=genre_register.upper(),
        rel_ws=rel_ws,
        table_str=table_str,
        short_title_slug=mon_info.get("short_title", monument_id).replace(" ", "_"),
    )

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
    workspace_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
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

    source_lang = mon_info.get("source_language", "Church Slavonic")
    if "bilingual" in source_lang.lower():
        transcription_inst = "Transcribe Greek and bilingual English facing text leaf-by-leaf with headers `=== LEAF p{start_page} ===` (Greek on even folios, English on odd folios)."
        translation_inst = f"Translate and critically audit into MTS-1 compliant text in `{draft_md_out.name}` with inline footnote markers `[^N]`, rectifying chant terms to Tone 1–8 and canonical UGCC loanwords."
    elif "russian" in source_lang.lower():
        transcription_inst = f"Transcribe Russian source text, Church Slavonic incipits, and Greek citations leaf-by-leaf with headers `=== LEAF p{{N}} ===` (for each leaf p{start_page} through p{end_page})."
        translation_inst = f"Translate and critically audit into MTS-1 compliant scholarly critical text in `{draft_md_out.name}` with inline footnote markers `[^N]`, preserving original page markers `*(Orig. p. N)*` and rendering Greek/Slavonic apparatus in footnotes."
    else:
        transcription_inst = f"Transcribe Church Slavonic source text leaf-by-leaf with headers `=== LEAF p{{N}} ===` (for each leaf p{start_page} through p{end_page})."
        translation_inst = f"Translate unabridged into `{draft_md_out.name}` with inline footnote markers `[^N]`."

    scaffolds_path = PROJECT_ROOT / "data" / "templates" / "publication_spec_scaffolds.json"
    if scaffolds_path.exists():
        try:
            scaffolds = json.loads(scaffolds_path.read_text(encoding="utf-8"))
            key = "octoechos" if "octoechos" in monument_id.lower() else "default"
            h1_inst = scaffolds.get(key, scaffolds.get("default", {})).get("canonical_h1_instruction", "")
            if h1_inst:
                translation_inst = f"{translation_inst} {h1_inst}"
        except (OSError, json.JSONDecodeError) as e:
            print(f"[Warning] Could not load publication_spec_scaffolds.json: {e}", file=sys.stderr)

    work_order_tpl = (PROJECT_ROOT / "data" / "templates" / "work_order_template.md").read_text(encoding="utf-8")
    content = work_order_tpl.format(
        title=mon_info.get("title"),
        cohort_num=cohort_num,
        monument_id=monument_id,
        start_page=start_page,
        end_page=end_page,
        leaf_count=leaf_count,
        starting_footnote=starting_footnote,
        genre_register_upper=genre_register.upper(),
        genre_register_cap=genre_register.capitalize(),
        images_rel=images_dir.relative_to(PROJECT_ROOT),
        source_rel=source_out.relative_to(PROJECT_ROOT),
        draft_rel=draft_md_out.relative_to(PROJECT_ROOT),
        footnotes_rel=footnotes_out.relative_to(PROJECT_ROOT),
        footnotes_name=footnotes_out.name,
        transcription_inst=transcription_inst,
        translation_inst=translation_inst,
    )

    coord_notes = mon_info.get("coordinate_notes")
    guardrails = mon_info.get("flash_execution_guardrails", [])
    if coord_notes or guardrails:
        content += "\n\n---\n\n## 4. Monument-Specific Codicological & Formatting Guardrails\n"
        if coord_notes:
            content += f"**Codicological Notes**: {coord_notes}\n\n"
        if guardrails:
            content += "**Flash Execution Guardrails**:\n"
            for g in guardrails:
                content += f"- {g}\n"

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
