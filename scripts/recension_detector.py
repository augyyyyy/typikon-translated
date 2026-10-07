#!/usr/bin/env python3
"""
Kachmar Recension Detector & Affinity Auditor
==============================================
Analyzes liturgical texts against the 5-dimension Kachmar Recension Grid:
  1. Prosphora count & preparation (1 vs 4 vs 5)
  2. Filioque treatment in the Credo & synodal decrees
  3. Epiclesis Third Hour troparion presence/absence
  4. Commemoration formulas (Pope, Kyiv Metropolitan, Moscow Synod/Patriarch, Constantinople)
  5. Chant models & liturgical realia (Samohlasen, Podoben, Tetrapod, Klepalo, etc.)

Outputs:
  - Quantitative affinity scorecard (% affinity across historical recensions)
  - Detailed dimension-by-dimension breakdown
  - Comparative apparatus and codicological citations ledger
  - Structured JSON export (default: Audit_Reports/recension_analysis.json)

Usage:
  python scripts/recension_detector.py --target "path/to/text.md"
  python scripts/recension_detector.py --target "path/to/text.md" --output "Audit_Reports/recension_analysis.json" --export-md
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_GRID_PATH = PROJECT_ROOT.parent / "Shared_Lexicon" / "typikon_recension_grid.json"

def load_grid(grid_path: Optional[Path] = None) -> Dict[str, Any]:
    path = grid_path or DEFAULT_GRID_PATH
    if not path.exists():
        # Fallback check inside project
        local_path = PROJECT_ROOT / "Shared_Lexicon" / "typikon_recension_grid.json"
        if local_path.exists():
            path = local_path
        else:
            raise FileNotFoundError(f"Recension grid definition not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def audit_recension(target_path: Path, grid: Dict[str, Any]) -> Dict[str, Any]:
    if not target_path.exists():
        raise FileNotFoundError(f"Target file not found: {target_path}")

    text = target_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    recensions = grid.get("recensions", {})
    markers = grid.get("markers", [])
    dimensions = grid.get("dimensions", [])

    hits_by_recension: Dict[str, int] = {k: 0 for k in recensions.keys()}
    hits_by_dimension: Dict[str, Dict[str, int]] = {
        dim: {k: 0 for k in recensions.keys()} for dim in dimensions
    }
    hit_ledger: List[Dict[str, Any]] = []
    comparative_notes: List[Dict[str, Any]] = []

    # Compile regexes
    compiled_markers = []
    for m in markers:
        m_id = m.get("id")
        m_dim = m.get("dimension")
        m_name = m.get("name")
        sigs = m.get("signatures", {})
        for rec_key, sig_data in sigs.items():
            pattern_str = sig_data.get("regex")
            if pattern_str:
                compiled = re.compile(pattern_str, re.IGNORECASE)
                compiled_markers.append({
                    "id": m_id,
                    "dimension": m_dim,
                    "name": m_name,
                    "recension": rec_key,
                    "token": sig_data.get("token"),
                    "significance": sig_data.get("significance"),
                    "compiled": compiled
                })

    # Pattern for comparative codicological notes (contrasting editions)
    comparative_pattern = re.compile(
        r"(?:according to the (?:Moscow|Greek|Venetian|Pochaiv|Roman|Ruthenian) (?:Typikon|edition|Oktoechos|Menaion|Sluzhebnik)|"
        r"contrary to (?:the )?(?:Greeks|Moscow|Synod)|"
        r"diversity of (?:rubrics|editions)|"
        r"let each church (?:preserve|adhere to) its own custom)",
        re.IGNORECASE
    )

    for line_num, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith("<!--"):
            continue

        # Check markers
        for cm in compiled_markers:
            m = cm["compiled"].search(s)
            if m:
                rec = cm["recension"]
                dim = cm["dimension"]
                hits_by_recension[rec] = hits_by_recension.get(rec, 0) + 1
                if dim in hits_by_dimension:
                    hits_by_dimension[dim][rec] = hits_by_dimension[dim].get(rec, 0) + 1

                hit_ledger.append({
                    "line": line_num,
                    "recension": rec,
                    "recension_name": recensions.get(rec, {}).get("display_name", rec),
                    "dimension": dim,
                    "marker_id": cm["id"],
                    "marker_name": cm["name"],
                    "matched_text": m.group(0),
                    "context_snippet": s[:140]
                })

        # Check comparative apparatus notes
        comp_m = comparative_pattern.search(s)
        if comp_m:
            comparative_notes.append({
                "line": line_num,
                "matched_clause": comp_m.group(0),
                "snippet": s[:160]
            })

    total_hits = sum(hits_by_recension.values())
    affinity_scores: Dict[str, float] = {}
    for rec_key, count in hits_by_recension.items():
        affinity_scores[rec_key] = round((count / total_hits * 100.0), 2) if total_hits > 0 else 0.0

    # Determine primary and secondary affinity
    sorted_affinities = sorted(affinity_scores.items(), key=lambda item: item[1], reverse=True)
    primary_recension = sorted_affinities[0][0] if sorted_affinities and sorted_affinities[0][1] > 0 else "undetermined"

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target_file": target_path.name,
        "total_lines_analyzed": len(lines),
        "total_recension_hits": total_hits,
        "primary_recension": primary_recension,
        "primary_recension_name": recensions.get(primary_recension, {}).get("display_name", "Undetermined"),
        "affinity_scores": affinity_scores,
        "hits_by_recension": hits_by_recension,
        "hits_by_dimension": hits_by_dimension,
        "comparative_notes_count": len(comparative_notes),
        "comparative_apparatus_sample": comparative_notes[:15],
        "hits_sample": hit_ledger[:30]
    }

def format_markdown_report(report: Dict[str, Any], recensions_meta: Dict[str, Any]) -> str:
    md = []
    md.append(f"# Recension Affinity Audit: {report['target_file']}")
    md.append(f"**Audit Timestamp:** {report['timestamp']}")
    md.append(f"**Total Analyzed Lines:** {report['total_lines_analyzed']}")
    md.append(f"**Total Diagnostic Markers Detected:** {report['total_recension_hits']}")
    md.append(f"**Primary Recension Affinity:** **{report['primary_recension_name']}**\n")

    md.append("## Quantitative Recension Affinity Scorecard")
    md.append("| Recension | Display Name | Hits | Affinity % |")
    md.append("|---|---|---:|---:|")
    for rec_key, score in sorted(report["affinity_scores"].items(), key=lambda x: x[1], reverse=True):
        name = recensions_meta.get(rec_key, {}).get("display_name", rec_key)
        hits = report["hits_by_recension"].get(rec_key, 0)
        md.append(f"| `{rec_key}` | {name} | {hits} | **{score:.2f}%** |")
    md.append("")

    md.append("## Dimension-by-Dimension Diagnostic Breakdown")
    md.append("| Dimension | Ruthenian Kyivan | Post-Zamość Galician | Muscovite Synodal | Neo-Sabbaitic Greek |")
    md.append("|---|---:|---:|---:|---:|")
    for dim, counts in report["hits_by_dimension"].items():
        rk = counts.get("ruthenian_kyivan", 0)
        pzg = counts.get("post_zamosc_galician", 0)
        ms = counts.get("muscovite_synodal", 0)
        nsg = counts.get("neo_sabbaitic_greek", 0)
        md.append(f"| `{dim}` | {rk} | {pzg} | {ms} | {nsg} |")
    md.append("")

    md.append(f"## Comparative Apparatus & Scholarly Cross-References ({report['comparative_notes_count']} detected)")
    if report["comparative_apparatus_sample"]:
        for n in report["comparative_apparatus_sample"]:
            md.append(f"- **Line {n['line']}**: *\"{n['matched_clause']}\"*\n  > {n['snippet']}")
    else:
        md.append("_No comparative cross-references detected._")
    md.append("")

    return "\n".join(md)

def main():
    parser = argparse.ArgumentParser(description="Kachmar Recension Detector CLI")
    parser.add_argument("--target", required=True, help="Path to text or markdown document")
    parser.add_argument("--grid", help="Optional path to custom typikon_recension_grid.json")
    parser.add_argument("--output", help="Optional output JSON path")
    parser.add_argument("--export-md", action="store_true", help="Also generate markdown report")
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout")

    args = parser.parse_args()

    target_path = Path(args.target)
    grid_path = Path(args.grid) if args.grid else None

    grid = load_grid(grid_path)
    report = audit_recension(target_path, grid)

    if args.output:
        out_file = Path(args.output)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Saved JSON recension report to: {out_file}")

        if args.export_md:
            md_file = out_file.with_suffix(".md")
            md_content = format_markdown_report(report, grid.get("recensions", {}))
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(md_content + "\n")
            print(f"Saved Markdown recension report to: {md_file}")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif not args.output:
        print("=" * 65)
        print(f"  RECENSION AFFINITY AUDIT: {report['target_file']}")
        print(f"  Primary Recension: {report['primary_recension_name']}")
        print(f"  Total Markers: {report['total_recension_hits']}")
        print("-" * 65)
        for rec, score in sorted(report["affinity_scores"].items(), key=lambda x: x[1], reverse=True):
            hits = report["hits_by_recension"].get(rec, 0)
            print(f"  {rec:25s}: {score:6.2f}% ({hits} hits)")
        print(f"  Comparative Notes Detected: {report['comparative_notes_count']}")
        print("=" * 65)

if __name__ == "__main__":
    main()
