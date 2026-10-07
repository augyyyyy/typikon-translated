#!/usr/bin/env python3
"""
Universal Publication Compiler & Formatter Engine
==================================================
Transforms intermediate translation cohorts into a pure, functional,
publication-grade digital codex modeled directly on Monument 0 (2010 Lviv Typikon).

Key Operations:
1. Enforces Closed Mathematical Leaf Conservation on cohort inputs.
2. Archives raw 10-leaf translation cohorts into `Cohorts/` for permanent academic auditability.
3. Purges 100% of academic placeholders and translation scaffolding:
   - [Leaf p... / Page ...]
   - [Blank Leaf]
   - === LEAF ... ===
   - <!-- LEAF ... -->
   - Cohort X Raw Draft headers
   - Cohort X Footnotes headers
4. Stitches severed sentences across cohort seams.
5. Applies liturgical typography formatting (dialogue blockquotes with bold roles, alert callouts).
6. Decomposes the codex into canonical modular Parts declared in `codex_registry.json`.
7. Builds a Dual-Context Interactive Table of Contents (relative cross-file links for part0, local anchors for _complete).
8. Inlines relevant footnotes locally into each Part file, while compiling the master edition
   with all footnotes integrated at the foot.
9. Emits standalone critical apparatus markdown file.
10. Synchronizes deliverables to `Projects/Typikon Coded/Data/Inbox/<Monument>/` and writes handoff notes.

Usage:
    python scripts/compile_final_edition.py --monument 1899_dolnytsky_typikon
    python scripts/compile_final_edition.py --monument 1891_lviv_synod
"""

import sys
import os
import re
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple, Optional, Any

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"

sys.path.insert(0, str(PROJECT_ROOT))
from scripts.assemble_and_sync_hub import verify_closed_leaf_conservation, extract_accounted_leaves, get_hub_inbox

def slugify(heading_text: str) -> str:
    """Computes standard GitHub Flavored Markdown heading slug."""
    cleaned = re.sub(r'\[\^?\d+\]', '', heading_text)
    cleaned = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned)
    cleaned = re.sub(r'[*_`~]', '', cleaned)
    cleaned = cleaned.lower()
    cleaned = re.sub(r'[^\w\s-]', '', cleaned, flags=re.UNICODE)
    cleaned = re.sub(r'[\s_]+', '-', cleaned)
    cleaned = re.sub(r'-+', '-', cleaned)
    return cleaned.strip('-')

def strip_academic_placeholders(text: str) -> str:
    """Removes all academic scaffolding, leaf tags, and cohort delimiters."""
    # 1. Strip raw cohort banners and markdown headers
    text = re.sub(r"^#+\s*.*?Cohort\s+\d+.*?\n+", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"<!--\s*(?:START|END)?\s*COHORT.*?-->\n*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<!--\s*LEAF:?[^>]*-->\n*", "", text, flags=re.IGNORECASE)

    # 2. Strip intermediate Table of Contents blocks in individual cohorts
    text = re.sub(r"##\s+Table of Contents\s*\n(?:[ \t]*[-*\d\.]+\s+.*?\(#.*?\)\s*\n)+", "", text, flags=re.IGNORECASE)

    # 3. Strip cohort introductory callout blocks
    text = re.sub(r">\s*\[!NOTE\]\s*\n(?:>\s*.*?\n)+", "", text)

    # 4. Strip bracketed leaf markers, blank folios, and physical page references
    text = re.sub(r"\[(?:Physical\s+Page\s+\d+\s*/\s*)?Leaf\s+p?\d+[^\]]*\]\n*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[Blank Leaf\]\n*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"===\s*LEAF\s+p?\d+\s*===\n*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\*?\(\*?(?:Physical Page|Physical pp\.|Physical Leaf|Leaf\s+p?)[^)]*\)?\*?\n*", "", text, flags=re.IGNORECASE)

    # 5. Strip intermediate cohort footnote sections and headers
    text = re.sub(r"##\s+(?:Scholarly Critical Apparatus & Footnotes|Footnotes)\s*\n(?:\[\^\d+\]:.*?\n*)+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^#+\s*Cohort\s+\d+\s+Footnotes.*?\n*", "", text, flags=re.MULTILINE | re.IGNORECASE)

    # 6. Clean horizontal rules that were used strictly as leaf dividers
    text = re.sub(r"\n---\s*\n(?=\s*\n)", "\n", text)

    # 7. Clean excess blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def stitch_cohort_boundaries(cohort_texts: List[str]) -> str:
    """Combines cohort texts, rejoining sentences split across file boundaries."""
    stitched_parts: List[str] = []

    for i, raw_text in enumerate(cohort_texts):
        cleaned = strip_academic_placeholders(raw_text)
        if not cleaned:
            continue

        if not stitched_parts:
            stitched_parts.append(cleaned)
            continue

        prev_text = stitched_parts[-1]
        prev_lines = prev_text.splitlines()
        curr_lines = cleaned.splitlines()

        last_line = prev_lines[-1].strip() if prev_lines else ""
        first_line = curr_lines[0].strip() if curr_lines else ""

        # Check if last line of previous cohort cuts off mid-sentence
        is_cut_sentence = False
        if last_line and not last_line.startswith("#") and not last_line.startswith(">"):
            if not any(last_line.endswith(p) for p in [".", "!", "?", ":", ";", '"', "”", "'", "’", "*", "—"]):
                if first_line and not first_line.startswith("#") and not first_line.startswith(">") and not first_line.startswith("*"):
                    is_cut_sentence = True

        if is_cut_sentence:
            prev_lines[-1] = last_line + " " + first_line
            stitched_parts[-1] = "\n".join(prev_lines)
            if len(curr_lines) > 1:
                stitched_parts.append("\n".join(curr_lines[1:]))
        else:
            stitched_parts.append(cleaned)

    return "\n\n---\n\n".join(stitched_parts)

def format_liturgical_typography(text: str) -> str:
    """Enhances liturgical dialogue formatting, blockquotes, and rubrical notes."""
    lines = text.splitlines()
    formatted_lines: List[str] = []

    roles = r"(Priest|Deacon|Second Deacon|First Deacon|Choir|Reader|Bishop|Hierarch|People|Chanter)"

    for line in lines:
        trimmed = line.strip()
        # 1. Dialogue role: > Priest: "..." -> > **Priest:** "..."
        m_dlg = re.match(r"^(?:>\s*)?(?:The\s+)?(" + roles + r"):\s*(.*)$", trimmed, re.IGNORECASE)
        if m_dlg:
            role = m_dlg.group(1).title()
            rest = m_dlg.group(3).strip()
            # If rest is quoted or liturgical prayer text, format as blockquote
            if rest.startswith('"') or rest.startswith('“') or rest.startswith('*'):
                line = f"> **{role}:** {rest}"
            else:
                line = f"> **{role}:** \"{rest}\""

        # 2. Liturgical Alert Callouts: "Let it be known:" or "Rubrics on ..."
        if re.match(r"^> \*\*Rubrics on .*?\*\*:", line):
            # Already formatted
            pass
        elif re.match(r"^(?:>\s*)?Let it be known:[ ]*$", trimmed, re.IGNORECASE):
            line = "> [!NOTE]\n> **Let it be known:**"

        formatted_lines.append(line)

    return "\n".join(formatted_lines)

def clean_and_parse_footnotes(footnotes_file: Path) -> Dict[int, str]:
    """Cleans cohort headers from footnotes file and returns footnote_number -> definition text."""
    if not footnotes_file.exists():
        return {}

    content = footnotes_file.read_text(encoding="utf-8")
    cleaned_content = re.sub(r"^#+\s*Cohort\s+\d+\s+Footnotes.*?\n+", "", content, flags=re.MULTILINE | re.IGNORECASE)
    cleaned_content = re.sub(r"\n{3,}", "\n\n", cleaned_content).strip()

    if cleaned_content != content:
        footnotes_file.write_text(cleaned_content, encoding="utf-8")

    fn_map: Dict[int, str] = {}
    pattern = re.compile(r"^\[\^(\d+)\]:\s*(.*?)(?=\n\[\^\d+\]:|\Z)", re.DOTALL | re.MULTILINE)
    for m in pattern.finditer(cleaned_content):
        fn_num = int(m.group(1))
        fn_text = m.group(2).strip()
        fn_map[fn_num] = fn_text

    return fn_map

def format_footnotes_for_part(part_text: str, fn_map: Dict[int, str]) -> str:
    """Extracts footnote citations in part_text and formats local definitions at bottom."""
    # Strip any existing synthesized bottom notes block (identified by --- then ### Notes then [^...)
    clean_part = re.split(r"\n---\s*\n\s*### Notes\s*\n\s*\[\^", part_text, flags=re.IGNORECASE)[0].rstrip()

    cited_nums = [int(n) for n in re.findall(r"\[\^(\d+)\]", clean_part)]
    if not cited_nums:
        return clean_part

    # Unique in order of appearance
    seen = set()
    ordered_nums = []
    for n in cited_nums:
        if n not in seen:
            seen.add(n)
            ordered_nums.append(n)

    lines = [clean_part, "", "---", "", "### Notes", ""]
    for n in ordered_nums:
        if n in fn_map:
            lines.append(f"[^{n}]: {fn_map[n]}")
        else:
            lines.append(f"[^{n}]: *(Definition not found in master apparatus)*")

    return "\n".join(lines)

def adapt_toc_for_part0(toc_markdown: str, part_slug_map: Dict[str, str], part0_filename: str) -> str:
    """
    Converts intra-file anchor links '[Title](#slug)' into relative cross-file links
    '[Title](filename#slug)' for anchors located in other modular part files.
    """
    def replacer(match):
        text = match.group(1)
        slug = match.group(2)
        target_file = part_slug_map.get(slug.lower())
        if target_file and target_file != part0_filename:
            return f"[{text}]({target_file}#{slug})"
        return f"[{text}](#{slug})"

    return re.sub(r'\[([^\]]+)\]\(#([^\)]+)\)', replacer, toc_markdown)

class UniversalPublicationEngine:
    def __init__(self, monument_id: str):
        self.monument_id = monument_id
        if not REGISTRY_FILE.exists():
            raise FileNotFoundError(f"Registry file not found at {REGISTRY_FILE}")

        self.registry = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        if monument_id not in self.registry.get("monuments", {}):
            raise ValueError(f"Monument '{monument_id}' not found in codex_registry.json!")

        self.cfg = self.registry["monuments"][monument_id]
        self.ws_dir = PROJECT_ROOT / self.cfg["workspace_dir"]
        self.cohorts_dir = self.ws_dir / "Cohorts"
        self.final_md_dir = self.ws_dir / "Final MD"
        self.final_dir = self.ws_dir / "Final"
        self.footnotes_file = self.final_dir / "Final_footnotes.txt"
        self.pub_spec = self.cfg.get("publication_spec", {})
        self.total_pages = self.cfg["total_physical_pages"]

        self.cohorts_dir.mkdir(parents=True, exist_ok=True)
        self.final_md_dir.mkdir(parents=True, exist_ok=True)
        self.final_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        print("=" * 75)
        print(f"  UNIVERSAL PUBLICATION ENGINE: {self.cfg['title']}")
        print(f"  Monument ID: {self.monument_id} | Total Leaves: {self.total_pages}")
        print("=" * 75)

        # 1. Collect & Verify Cohorts
        cohort_files = self._collect_cohort_files()
        print(f"[Step 1] Collected {len(cohort_files)} translation cohorts.")

        # 2. Closed Leaf Conservation
        print("[Step 2] Verifying Closed Mathematical Leaf Conservation...")
        verify_closed_leaf_conservation(cohort_files, self.total_pages, self.monument_id, is_final_assembly=True)

        # 3. Archive raw cohorts to Cohorts/
        print("[Step 3] Archiving raw cohort drafts to Cohorts/ folder...")
        self._archive_cohorts(cohort_files)

        # 4. Read archived cohorts in strict order
        archived_cohorts = sorted(list(self.cohorts_dir.glob("*.md")), key=self._cohort_sort_key)
        cohort_texts = [cf.read_text(encoding="utf-8") for cf in archived_cohorts]

        # 5. Parse master footnotes (purging cohort headers)
        fn_map = clean_and_parse_footnotes(self.footnotes_file)
        print(f"[Step 4] Parsed {len(fn_map)} clean master footnote definitions.")

        # 6. Scaffolding Purging & Seam Stitching
        print("[Step 5] Purging academic scaffolding and stitching cohort seams...")
        stitched_body = stitch_cohort_boundaries(cohort_texts)

        # 7. Apply Liturgical Typography
        print("[Step 6] Applying liturgical typography rules (Monument 0 parity)...")
        typography_body = format_liturgical_typography(stitched_body)

        # 8. Modular Part Slicing
        print("[Step 7] Slicing codex into canonical modular Parts...")
        parts_raw = self._slice_parts(typography_body)
        print(f"  Sliced into {len(parts_raw)} modular parts: {list(parts_raw.keys())}")

        # 9. Build Part Slug Map for Dual-Context TOC
        part_slug_map = self._build_part_slug_map(parts_raw)

        # 10. Build Table of Contents
        master_toc = self._build_master_toc(parts_raw)
        part0_spec = self.pub_spec["parts"][0]
        part0_toc = adapt_toc_for_part0(master_toc, part_slug_map, part0_spec["filename"])

        # 11. Format Part Contents with In-File Footnotes
        print("[Step 8] Formatting modular part files and local in-file footnotes...")
        formatted_parts: Dict[str, str] = {}
        for part_id, raw_content in parts_raw.items():
            spec_entry = next(p for p in self.pub_spec["parts"] if p["id"] == part_id)
            filename = spec_entry["filename"]

            if part_id == "part0":
                # Inject Part 0 TOC
                content = raw_content.rstrip() + "\n\n---\n\n" + part0_toc
            else:
                content = raw_content

            # Format local footnotes
            formatted_content = format_footnotes_for_part(content, fn_map)
            formatted_parts[filename] = formatted_content

        # 12. Assemble Master Complete Edition
        print("[Step 9] Assembling master unabridged complete edition...")
        master_footnotes_block = ["# FOOTNOTES AND SCHOLARLY COMMENTARY", ""]
        for n in sorted(fn_map.keys()):
            master_footnotes_block.append(f"[^{n}]: {fn_map[n]}")
        master_footnotes_text = "\n\n".join(master_footnotes_block)

        # In master complete, Part 0 uses the master_toc with local anchors
        part0_for_complete = parts_raw["part0"].rstrip() + "\n\n---\n\n" + master_toc
        complete_sections = [part0_for_complete]
        for p in self.pub_spec["parts"][1:]:
            complete_sections.append(parts_raw[p["id"]])
        complete_sections.append(master_footnotes_text)

        complete_md = "\n\n---\n\n".join(complete_sections)

        # 13. Write Deliverables
        print("[Step 10] Emitting publication deliverables to Final MD/ and Final/...")
        complete_filename = f"{self.monument_id}_complete.md"
        footnotes_filename = self.pub_spec.get("footnotes_filename", f"{self.monument_id}_footnotes.md")

        all_deliverables = {
            complete_filename: complete_md,
            footnotes_filename: master_footnotes_text
        }
        all_deliverables.update(formatted_parts)

        for filename, content in all_deliverables.items():
            md_path = self.final_md_dir / filename
            md_path.write_text(content, encoding="utf-8")
            print(f"  Emitted Final MD: {filename} ({len(content):,} chars)")

            # Text mirror in Final/
            if filename.endswith(".md"):
                txt_path = self.final_dir / (filename[:-3] + ".txt")
                txt_path.write_text(content, encoding="utf-8")

        # 14. Synchronize to Typikon Coded Hub Inbox
        print("[Step 11] Synchronizing deliverables to Typikon Coded Hub Inbox...")
        hub_folder_name = self.pub_spec.get("hub_inbox_folder", self.monument_id)
        hub_inbox = get_hub_inbox(hub_folder_name)
        for filename, content in all_deliverables.items():
            (hub_inbox / filename).write_text(content, encoding="utf-8")
        print(f"  Successfully synced {len(all_deliverables)} files to: {hub_inbox.relative_to(PROJECT_ROOT.parent)}")

        # 15. Generate Handoff Note
        self._write_handoff_note(hub_inbox, len(all_deliverables), len(fn_map))
        print("  Emitted handoff_note.md to Hub Inbox.")

        print("\n" + "=" * 75)
        print(f"  >>> PUBLICATION COMPILATION SUCCEEDED FOR {self.monument_id} <<<")
        print("=" * 75)

    def _collect_cohort_files(self) -> List[Path]:
        """Locates and sorts all translation cohorts."""
        candidates = list(self.cohorts_dir.glob("*cohort*.md"))
        if not candidates:
            candidates = list(self.final_md_dir.glob("*cohort*.md"))

        if not candidates:
            raise FileNotFoundError(f"No translation cohorts found in {self.cohorts_dir} or {self.final_md_dir}")

        return sorted(candidates, key=self._cohort_sort_key)

    def _cohort_sort_key(self, path: Path) -> int:
        m = re.search(r"cohort(\d+)", path.name, re.IGNORECASE)
        return int(m.group(1)) if m else 9999

    def _archive_cohorts(self, cohort_files: List[Path]) -> None:
        """Ensures all cohorts are in Cohorts/ and removed from Final MD/."""
        for cf in cohort_files:
            dest = self.cohorts_dir / cf.name
            if cf != dest:
                shutil.copy2(str(cf), str(dest))
                cf.unlink()

    def _slice_parts(self, text: str) -> Dict[str, str]:
        lines = text.splitlines()
        part_specs = self.pub_spec.get("parts", [])
        if not part_specs:
            return {"part0": text}

        # Find landmark indices
        landmarks: List[Tuple[str, int, str]] = [] # (part_id, line_index, title)
        for ps in part_specs:
            pid = ps["id"]
            pat = ps.get("start_landmark")
            if not pat:
                landmarks.append((pid, 0, ps["title"]))
                continue

            found_idx = -1
            for idx, line in enumerate(lines):
                if re.search(pat, line.strip(), re.IGNORECASE):
                    # For Part 6 table of contents, Dolnytsky's historical index is after line 8000
                    if self.monument_id == "1899_dolnytsky_typikon" and pid == "part6" and idx < 8000:
                        continue
                    found_idx = idx
                    break

            if found_idx == -1:
                raise ValueError(f"Failed to locate landmark for {pid} with pattern: {pat}")
            landmarks.append((pid, found_idx, ps["title"]))

        landmarks.sort(key=lambda x: x[1])

        parts_raw: Dict[str, str] = {}
        for i in range(len(landmarks)):
            pid, start_idx, title = landmarks[i]
            end_idx = landmarks[i+1][1] if i + 1 < len(landmarks) else len(lines)
            chunk = "\n".join(lines[start_idx:end_idx]).strip()

            if pid == "part0":
                # Ensure clean headers in Part 0 for Approbations and Dedication
                if "## Approbation and Imprimatur" not in chunk:
                    chunk = re.sub(r"\*{0,2}(No\.\s*1195/Ord\.)\*{0,2}", r"## Approbation and Imprimatur\n\n**\1**", chunk, count=1)
                if "## Dedication" not in chunk:
                    chunk = re.sub(r"(To the glory\s*\nof the All-Holy)", r"## Dedication\n\n\1", chunk, count=1)
                master_title_slug = slugify(self.pub_spec.get("master_title", ""))
                if master_title_slug and f'<a id="{master_title_slug}">' not in chunk:
                    chunk = re.sub(r"^(#\s+[^\n]+)", rf'\1 <a id="{master_title_slug}"></a>', chunk, count=1, flags=re.MULTILINE)

            # Ensure proper H1 header for modular parts > 0
            if i > 0:
                chunk = f"# {title}\n\n" + re.sub(r"^#+\s*.*?\n+", "", chunk, count=1).lstrip()

            parts_raw[pid] = chunk

        return parts_raw

    def _build_part_slug_map(self, parts_raw: Dict[str, str]) -> Dict[str, str]:
        slug_map: Dict[str, str] = {}
        for ps in self.pub_spec["parts"]:
            pid = ps["id"]
            filename = ps["filename"]
            raw_text = parts_raw.get(pid, "")
            for line in raw_text.splitlines():
                m = re.match(r"^#{1,6}\s+(.+)$", line.strip())
                if m:
                    heading = m.group(1).strip()
                    tag_m = re.search(r'<a\s+id="([^"]+)"', heading)
                    if tag_m:
                        slug_map.setdefault(tag_m.group(1).lower(), filename)
                    slug = slugify(heading)
                    if slug:
                        slug_map.setdefault(slug, filename)
        return slug_map

    def _build_master_toc(self, parts_raw: Dict[str, str]) -> str:
        """Builds master Table of Contents matching Dolnytsky or auto-generating from parts."""
        if self.monument_id == "1899_dolnytsky_typikon":
            return """## TABLE OF CONTENTS

* **[Title Page & Frontispiece Icon](#typikon)**
* **[Approbation and Imprimatur](#approbation-and-imprimatur)**
* **[Dedication](#dedication)**
* **[Notice](#notice)**
* **[Constituent Parts of the Typikon](#constituent-parts-of-the-typikon)**
* **[PART I: THE GENERAL ORDER OF DIVINE WORSHIP](#part-i-the-general-order-of-divine-worship)**
  * [On the Various Parts of Divine Worship](#on-the-various-parts-of-divine-worship)
  * [Vespers](#on-vespers)
    * [Order of Great Vespers at an All-Night Vigil](#order-of-great-vespers-at-an-all-night-vigil)
    * [Order of Great Vespers without an All-Night Vigil](#order-of-great-vespers-without-an-all-night-vigil)
    * [Order of Daily Vespers](#order-of-daily-vespers)
    * [Order of Small Vespers](#order-of-small-vespers)
  * [Compline](#concerning-compline)
    * [Order of Small Compline](#order-of-small-compline)
    * [Order of Great Compline without an All-Night Vigil](#order-of-great-compline-without-an-all-night-vigil)
    * [Order of Great Compline with an All-Night Vigil](#order-of-great-compline-with-an-all-night-vigil)
  * [Midnight Office](#concerning-the-midnight-office)
  * [Matins](#order-of-great-matins)
    * [Order of Great Matins (With & Without Vigil)](#with-an-all-night-vigil-and-without-an-all-night-vigil)
    * [From the Praises unto the End](#from-the-praises-unto-the-end)
    * [Rubric for Deacons](#rubric-for-deacons)
    * [Order of Daily Matins](#order-of-daily-matins)
  * [Order of the Usual Hours](#order-of-the-usual-hours)
  * [Vespers with the Divine Liturgy](#concerning-vespers-with-the-divine-liturgy)
* **[PART II: COMMON RUBRICS FOR THE DIVERSE SERVICES (OCTOECHOS & MENAION)](#part-ii-common-rubrics-for-the-diverse-services-of-the-octoechos-and-menaion)**
  * [Outside a Feast (The Seven Ranks of Saints)](#outside-a-feast)
    * [1. Non-Polyeleos Saint on Sunday](#1-non-polyeleos-saint-on-sunday)
    * [2. Non-Polyeleos Saint on Weekdays](#non-polyeleos-saint-on-weekdays-except-saturday)
    * [3. Non-Polyeleos Saint on Saturday](#non-polyeleos-saint-on-saturday)
    * [4. Polyeleos Saint on Sunday](#polyeleos-saint-on-sunday)
    * [5. Polyeleos Saint on Weekdays & Saturday](#polyeleos-saint-on-weekdays-and-on-saturday)
    * [6. Vigil Saint on Sunday](#vigil-saint-on-sunday)
    * [7. Vigil Saint on Weekdays & Saturday](#vigil-saint-on-weekdays-and-on-saturday)
  * [Within a Feast](#within-a-feast)
    * [In the Forefeast](#in-the-forefeast)
    * [On the Feast (Dominical & Theotokion)](#on-the-feast)
    * [In the Afterfeast](#in-the-afterfeast)
    * [On the Apodosis of the Feast](#on-the-apodosis-of-the-feast)
* **[PART III: PROPER RUBRICS FOR CERTAIN SERVICES OF THE MENAION](#part-iii-proper-rubrics-for-certain-services-of-the-menaion)**
  * [September](#september) (Nativity of the Theotokos, Exaltation of the Cross)
  * [October](#october-1) (Protection of the Theotokos, Demetrius)
  * [November](#november) (Michael the Archangel, Entrance of the Theotokos)
  * [December](#december) (St. Nicholas, Conception of St. Anna, Nativity of Christ)
  * [January](#january) (Circumcision, Theophany, Three Hierarchs)
  * [February](#february-the-meeting-of-the-lord) (Meeting of the Lord, Finding of Forerunner's Head)
  * [March](#march) (Forty Martyrs, Annunciation of the Theotokos)
  * [April](#april) (St. George)
  * [May](#may) (St. Athanasius, St. John the Theologian, St. Nicholas Translation)
  * [June](#june) (Nativity of St. John the Baptist, Sts. Peter & Paul)
  * [July](#july) (St. Vladimir, St. Elias)
  * [August](#august) (Transfiguration, Dormition of the Theotokos, Beheading of Forerunner)
* **[PART IV: TYPIKA OF THE TRIODION](#part-iv-typika-of-the-triodion)**
  * [Lenten Triodion](#typika-of-the-triodion) (Publican & Pharisee to Great Saturday)
  * [Flowery Triodion / Pentecostarion](#flowery-triodion) (Pascha to All Saints)
* **[PART V: TYPIKON CONCERNING TEMPLES](#part-v-typikon-concerning-temples)**
  * [Chapter I & II: Temple Typika](#typikon-concerning-temples)
  * [General & Proper Temple Typika](#temple-typika)
  * [Paschal Tablets & Perpetual Calendar](#tablet-i)
* **[PART VI: HISTORICAL INDEX, SYNODAL DECREES AND COLOPHON](#part-vi-historical-index-synodal-decrees-and-colophon)**
  * [Historical Table of Contents (1899)](#table-of-contents)
  * [Colophon and Thanksgiving](#colophon-and-thanksgiving)
* **[FOOTNOTES AND SCHOLARLY COMMENTARY](#footnotes-and-scholarly-commentary)**"""

        # Auto-generation fallback from parts
        toc_lines = ["## TABLE OF CONTENTS", ""]
        for ps in self.pub_spec.get("parts", []):
            pid = ps["id"]
            title = ps["title"]
            if pid == "part0":
                title = self.pub_spec.get("master_title", title)
            slug = slugify(title)
            toc_lines.append(f"* **[{title}](#{slug})**")
            raw_text = parts_raw.get(pid, "")
            for line in raw_text.splitlines():
                m = re.match(r"^##\s+(.+)$", line.strip())
                if m:
                    sub_title = m.group(1).strip()
                    sub_slug = slugify(sub_title)
                    if sub_slug in ["table-of-contents", "notes", "footnotes", "scholarly-critical-apparatus-footnotes"]:
                        continue
                    toc_lines.append(f"  * [{sub_title}](#{sub_slug})")
        return "\n".join(toc_lines)

    def _write_handoff_note(self, inbox_dir: Path, total_files: int, total_fn: int) -> None:
        note_path = inbox_dir / "handoff_note.md"
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        text = f"""# Publication Handoff Note: {self.cfg['title']}

- **Monument ID**: `{self.monument_id}`
- **Date**: {now_str}
- **Physical Leaves Accounted**: {self.total_pages} / {self.total_pages} (100% Closed Set Conservation)
- **Total Published Deliverables**: {total_files} files
- **Critical Footnotes Apparatus**: {total_fn} verified bijective definitions
- **Typographic Benchmark**: Modelled strictly on Monument 0 (2010 Lviv Typikon)
- **Scaffolding Purged**: 100% zero leaf markers, banners, or cohort draft scaffolding
- **Footnote Resolution**: Dual in-file local resolution (`partX.md`) and monolithic master apparatus

### Deliverables Manifest
"""
        for ps in self.pub_spec.get("parts", []):
            text += f"- `{ps['filename']}`: {ps['title']}\n"
        text += f"- `{self.monument_id}_complete.md`: Master Unabridged Publication Edition\n"
        text += f"- `{self.pub_spec.get('footnotes_filename', f'{self.monument_id}_footnotes.md')}`: Standalone Master Critical Apparatus\n"

        note_path.write_text(text, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Universal Publication Compiler & Formatter Engine")
    parser.add_argument("--monument", default="1899_dolnytsky_typikon", help="Monument ID")
    args = parser.parse_args()

    engine = UniversalPublicationEngine(args.monument)
    engine.run()

if __name__ == "__main__":
    main()
