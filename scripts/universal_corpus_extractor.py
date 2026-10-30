#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Atomic Liturgical Corpus Extractor (Propers + Non-Propers)
====================================================================
Decomposes 100% of any liturgical monument (Octoechos, Lenten Triodion,
Pentecostarion, Anthologion/Menaion, Horologion, Liturgikon, Trebnyk/Euchologion,
Typikon, Synodal Statutes, and Scholarly Lexica) into atomic, cross-comparable
bilingual liturgical units without re-translating a single leaf.

Emits:
  1. Final MD/{monument_id}_atomic_corpus.json (All 5 unit classes:
       PROPER_HYMN, SACERDOTAL_PRAYER, LITANY_OR_DIALOGUE,
       FIXED_ORDINARY_OR_LECTION, RUBRIC_OR_STATUTE)
  2. Final MD/{monument_id}_propers_corpus.json (Variable Propers slice,
       enriching existing Octoechos propers corpora in-place and generating
       new propers corpora for Triodion, Pentecostarion, Horologion, Anthologion,
       Liturgikon, and Trebnyk codices)
  3. Final MD/{monument_id}_podoben_grid.{json,md} (for hymnographic/Horologion codices)
  4. Audit_Reports/ATOMIC_CORPUS_LEDGER.{json,md} (when --all-completed is run)

Schema Compatibility:
  - Shared_Lexicon 4-Shard Primitives Corpus (01_ordinarium_primitives.json ..
    04_kanonnik.json) with pre-computed target_shard, codex_domain, and SGC-02
    ProvenanceBlock (source_file, source_sha256, TEXT_LINES, start_line, end_line,
    verbatim_source).
  - Festal Propers Comparisons Two-Binder Architecture (strict Binder 1 Ordinarium
    vs. Binder 2 Proprium separation, preceding_stichos, podoben_id, colometric
    asterisks, and Stamford sequence suffixes _1, _2, _glory, _both_now).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.orchestrator_state import resolve_monument_type
from scripts.generate_podoben_grid import (
    emit_podoben_grid,
    match_podoben_model,
    normalize_slavonic_tier2,
)

REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"
PRIMITIVES_FILE = PROJECT_ROOT / "data" / "liturgical_primitives_registry.json"

MONUMENT_TYPE_TO_PREFIX: Dict[str, str] = {
    "octoechos": "OCT",
    "lenten_triodion": "TRI",
    "pentecostarion": "PEN",
    "anthologion": "ANT",
    "akathistnik": "AKA",
    "irmologion": "IRM",
    "horologion": "HOR",
    "psalter": "PSA",
    "euchologion_liturgikon": "LIT",
    "trebnyk_euchologion": "TRE",
    "typikon": "TYP",
    "juridical_synodal": "SYN",
    "lexicon_scholarly": "LEX",
}

MONUMENT_TYPE_TO_CYCLE: Dict[str, str] = {
    "octoechos": "OCTOECHOS_8_TONE",
    "lenten_triodion": "MOVABLE_LENTEN_TRIODION",
    "pentecostarion": "MOVABLE_PASCHAL_PENTECOSTARION",
    "anthologion": "FIXED_MENAION_ANTHOLOGION",
    "akathistnik": "DEVOTIONAL_AKATHIST",
    "irmologion": "EIGHT_TONE_IRMOLOGION",
    "horologion": "DAILY_OFFICE_AND_MENOLOGION",
    "psalter": "BIBLICAL_PSALTER_KATHISMATA",
    "euchologion_liturgikon": "EUCHOLOGION_DIVINE_LITURGY",
    "trebnyk_euchologion": "EUCHOLOGION_SACRAMENTAL_TREBNYK",
    "typikon": "LITURGICAL_ORDO_TYPIKON",
    "juridical_synodal": "CANONICAL_SYNODAL_STATUTES",
    "lexicon_scholarly": "SCHOLARLY_LITURGICAL_COMPENDIUM",
}

HYMNOGRAPHIC_AND_HOROLOGION_TYPES = {
    "octoechos",
    "lenten_triodion",
    "pentecostarion",
    "anthologion",
    "akathistnik",
    "irmologion",
    "horologion",
}

VALID_UNIT_CLASSES = (
    "PROPER_HYMN",
    "SACERDOTAL_PRAYER",
    "LITANY_OR_DIALOGUE",
    "FIXED_ORDINARY_OR_LECTION",
    "RUBRIC_OR_STATUTE",
)

# Structural & Running Header Patterns
RE_LEAF_BANNER = re.compile(r"^===\s*LEAF\s+p?(\d+)\s*===$", re.IGNORECASE)
RE_2UP_MILESTONE = re.compile(
    r"^(?:#{1,6}\s*|\*\*)?\[(Left|Right)\s+Page\s*(?:—|--|-|:)\s*(?:(?:Fol\.?|Folio)\s*([0-9]+[rv])|([^\]]+))\](?:\*\*)?(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_COLUMN_MARKER = re.compile(
    r"^(?:#{1,6}\s*|\*\*|\*)?\[?Column\s+([A-B1-2])\]?(?:\*\*|\*)?(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_RUNNING_HEADER_BRACKET = re.compile(
    r"^\[(?:Fol\.?\s*([0-9]+[rv]?)\.?\s*)?Running\s+header:\s*([^\]]+)\](?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_WOODCUT_INITIAL = re.compile(
    r"^\[(?:Fol\.?\s*([0-9]+[rv]?)\.?\s*)?(?:Decorative\s+|Historiated\s+|Engraved\s+|Woodcut\s+|Cinnabar\s+|Red\s+)*initial\s+([A-Za-zА-ЯІЇЄѠѢꙊ])\b[^\]]*\]$",
    re.IGNORECASE,
)
RE_SHORT_RUNNING_TITLE = re.compile(
    r"^\*(?:Proskomedia|In\s+the\s+Liturgies|The\s+Holy\s+Liturgy|of\s+Saint\s+John\s+Chrysostom|of\s+Saint\s+Basil\s+the\s+Great|The\s+Presanctified\s+Liturgy|The\s+Ablutions|Order\s+of\s+Holy\s+Baptism)\.?(\*)?(?:\s*\[\^\d+\])?$",
    re.IGNORECASE,
)
RE_STANDALONE_SPEAKER = re.compile(
    r"^(?:>\s*)?\*\*(Priest|Deacon|Bishop|Hierarch|Archimandrite|Superior|Ecclesiarch|Canonarch|Reader|Choir|Choirs|People|Chanter|Chanters|Clergy|Sponsor|Catechumen|Question|Answer)(?:\s*\(([^\)]+)\))?(?:\s*\[continued\])?:\*\*\s*$",
    re.IGNORECASE,
)
RE_INLINE_SPEAKER = re.compile(
    r"^(?:>\s*)?(?:\*\*)?(?:The\s+)?(Priest|Deacon|Bishop|Hierarch|Archimandrite|Superior|Ecclesiarch|Canonarch|Reader|Choir|Choirs|People|Chanter|Chanters|Clergy|Sponsor|Catechumen|Question|Answer)(?:\s*\(([^\)]+)\))?(?:\*\*|\*)?:\s*(?:\*\*)?\s*(.+)$",
    re.IGNORECASE,
)
RE_PRAYER_HEADER_RUBRIC = re.compile(
    r"^\*(?:(?:The\s+)?(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Another)\s+Prayer\b|Prayer\s+(?:of|for|over|at|before|after|unto|to)\b|The\s+Priest\s+(?:says|prays|reads)\s+(?:this\s+)?prayer\b|(?:And\s+the\s+priest|The\s+priest)[^*\n]*(?:prays\s+secretly|saying\s+the\s+prayer)\b|Exorcism\b)[^*\n]*\*(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_STANDALONE_HYMN_ROLE = re.compile(
    r"^\*?(?:(?:After\s+Ode\s+[1-9],\s*)?(?:Ode|Canticle)\s+[1-9]\b[^*\n]*|Heirmos\b[^*\n]*|Katavasia\b[^*\n]*|Another\s*\[?Canon[^\n\*]*|(?:After\s+Ode\s+[1-9],\s*)?(?:Another\s+|Dismissal\s+|Resurrectional\s+)?(?:Troparion|Kontakion|Ikos|Sessional\s+Hymn|Kathisma|Exapost[ei]larion|Photagogi[ck]on|Hymn\s+of\s+Light|Hypakoe|Ypako[eë]|Gradual\s+Hymn|Antiphon\s+\d+|Martyri[ck]on|Triadi[ck]on|Sticheron|Megalynarion|(?:Cross-|Stavro|Stauro)?Theotokion|To\s+the\s+Cross)\b[^*\n]*?)[\.:]?\*?(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_SECTION_RUBRIC_CUE = re.compile(
    r"^\*[^*\n]*\b(?:At\s+\"Lord,\s+I\s+have\s+cried\"|On\s+\"Lord,\s+I\s+have\s+cried\"|At\s+the\s+Aposticha|On\s+the\s+Aposticha|At\s+the\s+Praises|On\s+the\s+Praises|At\s+the\s+Litiya|Resurrectional\s+Stichera|Other\s+(?:Anatolian|Eastern)\s+Stichera|Stichera\s+(?:of|to|on)|At\s+Matins|At\s+Vespers|At\s+the\s+Liturgy|After\s+the\s+\d+(?:st|nd|rd|th)\s+(?:Stichologia|Kathisma)|The\s+Canon)\b[^*\n]*:\*(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_MENOLOGION_DAY = re.compile(
    r"^\*(?:Month\s+of\s+([A-Z][a-z]+)|On\s+the\s+(\d+(?:st|nd|rd|th))\s+day|In\s+the\s+same\s+month\s+on\s+the\s+(\d+(?:st|nd|rd|th))|Synaxarion)\b[^*\n]*\*(?:\s*(?:\[\^\d+\])+)?",
    re.IGNORECASE,
)
RE_PODOBEN_HEADER = re.compile(
    r"^\*[^*\n]*?\bPodoben:\s*(?:\"([^\"]+)\"|([^*\(\n]+))(?:\s*\(([^\)]+)\))?[^*\n]*\*",
    re.IGNORECASE,
)
RE_SACRAMENTAL_FORMULA = re.compile(
    r"\b(?:The\s+servant\s+of\s+God\s+\[?N\.?\]?[,]?\s+is\s+(?:baptized|betrothed|crowned|shorn|churched)|The\s+seal\s+of\s+the\s+gift\s+of\s+the\s+Holy\s+Spirit|I\s+forgive\s+and\s+absolve|is\s+baptized\s+in\s+the\s+name\s+of\s+the\s+Father)\b",
    re.IGNORECASE,
)
RE_EKPHONESIS_FORMULA = re.compile(
    r"\bFor\s+(?:unto\s+Thee\s+is\s+due\s+all\s+glory|Thine\s+is\s+the\s+kingdom|Thou\s+art\s+a\s+merciful\s+and\s+(?:man-befriending|loving)\s+God|Thou\s+art\s+the\s+sanctification|Thou\s+art\s+He\s+that\s+blesses|Thou\s+art\s+our\s+sanctification|blessed\s+and\s+glorified\s+is\s+Thine\s+all-honorable\s+and\s+majestic\s+name|Through\s+the\s+mercies\s+of\s+Thine\s+only-begotten\s+Son|By\s+the\s+grace\s+and\s+compassions)\b",
    re.IGNORECASE,
)
RE_LITANY_PETITION_END = re.compile(
    r"(?:let\s+us\s+pray\s+to\s+the\s+Lord|let\s+us\s+ask\s+of\s+the\s+Lord|Help\s+us,\s+save\s+us,\s+have\s+mercy\s+on\s+us|Commemorating\s+our\s+most\s+holy,\s+most\s+pure|let\s+us\s+commend\s+ourselves\s+and\s+one\s+another)\.?\"?(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_NOMOCANON_HEADER = re.compile(
    r"^\*(?:\d+\.\s*)?(?:Concerning\s+[^*\n]+|Of\s+the\s+Holy\s+Fathers[^*\n]*|Injunctions[^*\n]*|Statute[^*\n]*|Canon\s+\d+[^*\n]*|Degree\s+[^*\n]*|Rule\s+\d+[^*\n]*):\*(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)

ACTOR_KEYWORDS = (
    "Priest", "Deacon", "Bishop", "Hierarch", "Superior", "Ecclesiarch",
    "Canonarch", "Reader", "Choir", "People", "Sponsor", "Catechumen", "Penitent",
)
REALIA_KEYWORDS = (
    "Tetrapod", "Klepalo", "Aer", "Kolyvo", "Plashchanytsia", "Sluzhebnik",
    "Diskos", "Chalice", "Asterisk", "Lance", "Sponge", "Zeon", "Antimension",
    "Censer", "Cinnabar", "Chrism", "Gospel", "Cross", "Mitre", "Epitrachelion",
    "Phelonion", "Sticharion", "Orarion", "Polystavrion", "Litiya", "Artos",
)


def load_primitives_data() -> Tuple[Dict[str, Dict[str, Any]], List[Dict[str, Any]]]:
    if not PRIMITIVES_FILE.exists():
        return {}, []
    try:
        data = json.loads(PRIMITIVES_FILE.read_text(encoding="utf-8"))
        pod_cat = {p["id"]: p for p in data.get("podoben_models", [])}
        stichoi = data.get("psalm_stichoi", [])
        return pod_cat, stichoi
    except (OSError, json.JSONDecodeError):
        return {}, []


def parse_slavonic_by_leaf(source_dir: Path, ws_dir: Path) -> Dict[int, List[str]]:
    """Loads Slavonic/Ukrainian source paragraphs indexed by physical leaf number."""
    by_leaf: Dict[int, List[str]] = {}
    if source_dir.exists():
        s_files = sorted(
            source_dir.glob("*source.txt"),
            key=lambda p: int(re.search(r"cohort0?(\d+)", p.name, re.IGNORECASE).group(1))
            if re.search(r"cohort0?(\d+)", p.name, re.IGNORECASE)
            else 9999,
        )
        for sf in s_files:
            m_c = re.search(r"cohort0?(\d+)", sf.name, re.IGNORECASE)
            curr_leaf = (int(m_c.group(1)) - 1) * 10 + 1 if m_c else 1
            buf: List[str] = []
            for raw_ln in sf.read_text(encoding="utf-8-sig", errors="ignore").splitlines():
                ln = raw_ln.strip()
                m_lf = RE_LEAF_BANNER.match(ln)
                if m_lf:
                    if buf:
                        by_leaf.setdefault(curr_leaf, []).append(" ".join(buf))
                        buf = []
                    curr_leaf = int(m_lf.group(1))
                    continue
                if not ln:
                    if buf:
                        by_leaf.setdefault(curr_leaf, []).append(" ".join(buf))
                        buf = []
                else:
                    buf.append(ln)
            if buf:
                by_leaf.setdefault(curr_leaf, []).append(" ".join(buf))
    elif (ws_dir / "Ukrainian TXTs").exists():
        # Monument 0 fallback
        for idx, uf in enumerate(sorted((ws_dir / "Ukrainian TXTs").glob("*.txt")), start=1):
            paras = [
                p.strip()
                for p in uf.read_text(encoding="utf-8-sig", errors="ignore").split("\n\n")
                if p.strip()
            ]
            by_leaf[idx] = paras
    return by_leaf


def collect_cohort_blocks(
    ws_dir: Path,
    folio_offset: int = 0,
) -> List[Dict[str, Any]]:
    """
    Reads Cohorts/*.md (or Final/*.txt for Monument 0), tracks exact line numbers and SHA-256
    for SGC-02 ProvenanceBlock, updates leaf/locus/running-header state, chains stacked
    speaker/woodcut prefixes, and stitches mid-sentence cross-leaf continuations.
    """
    cohorts_dir = ws_dir / "Cohorts"
    final_dir = ws_dir / "Final"

    input_files: List[Tuple[int, Path]] = []
    if cohorts_dir.exists() and list(cohorts_dir.glob("*cohort*.md")):
        for cf in sorted(
            cohorts_dir.glob("*cohort*.md"),
            key=lambda p: int(re.search(r"cohort0?(\d+)", p.name, re.IGNORECASE).group(1))
            if re.search(r"cohort0?(\d+)", p.name, re.IGNORECASE)
            else 9999,
        ):
            m_c = re.search(r"cohort0?(\d+)", cf.name, re.IGNORECASE)
            c_idx = int(m_c.group(1)) if m_c else 1
            input_files.append((c_idx, cf))
    elif final_dir.exists():
        part_files = sorted(final_dir.glob("*part*.txt")) or sorted(final_dir.glob("*.txt"))
        for idx, pf in enumerate(part_files, start=1):
            if "footnotes" in pf.name.lower():
                continue
            input_files.append((idx, pf))

    raw_blocks: List[Dict[str, Any]] = []

    for c_idx, fpath in input_files:
        raw_bytes = fpath.read_bytes()
        file_sha256 = hashlib.sha256(raw_bytes).hexdigest()
        rel_path = f"Translation/{fpath.relative_to(PROJECT_ROOT).as_posix()}"
        text = raw_bytes.decode("utf-8-sig", errors="ignore")
        lines = text.splitlines()

        curr_leaf = (c_idx - 1) * 10 + 1
        curr_locus = f"f. {curr_leaf - folio_offset}r" if (folio_offset and curr_leaf > folio_offset) else f"p{curr_leaf}"
        curr_running_header: Optional[str] = None

        # Group lines into logical blocks with exact 1-based (start_line, end_line).
        # Adjacent lines without blank lines are split into distinct tuples unless they are
        # consecutive Markdown table rows (`|...`) or soft-wrapped plain-text continuations.
        para_tuples: List[Tuple[int, int, List[str]]] = []
        cur_start = 1
        cur_lines: List[str] = []
        for l_idx, raw_ln in enumerate(lines, start=1):
            s = raw_ln.strip()
            if not s:
                if cur_lines:
                    para_tuples.append((cur_start, l_idx - 1, cur_lines))
                    cur_lines = []
            else:
                if cur_lines:
                    prev_s = cur_lines[-1].strip()
                    both_table = s.startswith("|") and prev_s.startswith("|")
                    if not both_table:
                        starts_block = (
                            s.startswith("===")
                            or s.startswith("#")
                            or s.startswith("**")
                            or s.startswith(">")
                            or s.startswith("*")
                            or s.startswith("[")
                            or s.startswith("|")
                            or s == "---"
                            or bool(RE_STANDALONE_HYMN_ROLE.match(s))
                            or bool(RE_INLINE_SPEAKER.match(s))
                        )
                        prev_complete = (
                            prev_s.startswith("===")
                            or prev_s.startswith("#")
                            or prev_s.startswith("|")
                            or prev_s == "---"
                            or (prev_s.startswith("*") and bool(re.search(r"\*(?:\s*\[\^\d+\])*$", prev_s)))
                            or (prev_s.startswith("[") and bool(re.search(r"\](?:\s*\[\^\d+\])*$", prev_s)))
                            or bool(RE_STANDALONE_SPEAKER.match(prev_s))
                            or bool(RE_INLINE_SPEAKER.match(prev_s))
                            or bool(re.search(r"[\.!\?:\"\*\u201d\u00bb\]](?:\s*\[\^\d+\])*$", prev_s))
                        )
                        if starts_block or prev_complete:
                            para_tuples.append((cur_start, l_idx - 1, cur_lines))
                            cur_lines = []
                if not cur_lines:
                    cur_start = l_idx
                cur_lines.append(raw_ln)
        if cur_lines:
            para_tuples.append((cur_start, len(lines), cur_lines))

        # Pending stacked prefix state (e.g. *Prayer rubric* + **Priest:** + [Woodcut initial O] + *Kontakion:*)
        pending_prayer_title: Optional[str] = None
        pending_delivery_mode: Optional[str] = None
        pending_speaker: Optional[str] = None
        pending_woodcut_initial: Optional[str] = None
        pending_hymn_role: Optional[str] = None
        pending_start_line: Optional[int] = None
        pending_verbatim_lines: List[str] = []

        for p_start, p_end, p_lines in para_tuples:
            # Scan lines within the paragraph for leaf banners, 2-up milestones, running headers
            surviving_lines: List[str] = []
            for raw_l in p_lines:
                sl = raw_l.strip()
                m_lf = RE_LEAF_BANNER.match(sl)
                if m_lf:
                    curr_leaf = int(m_lf.group(1))
                    curr_locus = (
                        f"f. {curr_leaf - folio_offset}r"
                        if (folio_offset and curr_leaf > folio_offset)
                        else f"p{curr_leaf}"
                    )
                    continue

                m_2up = RE_2UP_MILESTONE.match(sl)
                if m_2up:
                    f_code = (m_2up.group(2) or m_2up.group(3) or "").strip()
                    if f_code:
                        curr_locus = f"f. {f_code}" if not f_code.lower().startswith("f") else f_code
                    continue

                if RE_COLUMN_MARKER.match(sl):
                    continue

                m_rh = RE_RUNNING_HEADER_BRACKET.match(sl)
                if m_rh:
                    if m_rh.group(1):
                        curr_locus = f"f. {m_rh.group(1)}"
                    curr_running_header = m_rh.group(2).strip()
                    continue

                if RE_SHORT_RUNNING_TITLE.match(sl):
                    curr_running_header = sl.strip("* .")
                    continue

                m_wc = RE_WOODCUT_INITIAL.match(sl)
                if m_wc:
                    if m_wc.group(1):
                        curr_locus = f"f. {m_wc.group(1)}"
                    pending_woodcut_initial = m_wc.group(2).upper()
                    if pending_start_line is None:
                        pending_start_line = p_start
                    pending_verbatim_lines.append(raw_l)
                    continue

                if sl == "---" or re.match(r"^\s*\[\^\d+\]:", sl):
                    continue

                surviving_lines.append(raw_l)

            if not surviving_lines:
                continue

            joined_text = "\n".join(l.strip() for l in surviving_lines).strip()
            if not joined_text:
                continue

            # Check if this single-line block is a standalone prefix to chain onto the next block
            if len(surviving_lines) == 1:
                m_sp = RE_STANDALONE_SPEAKER.match(joined_text)
                if m_sp:
                    pending_speaker = m_sp.group(1).upper()
                    if m_sp.group(2) and "secret" in m_sp.group(2).lower():
                        pending_delivery_mode = "SECRET"
                    elif m_sp.group(2) and ("aloud" in m_sp.group(2).lower() or "loud" in m_sp.group(2).lower()):
                        pending_delivery_mode = "ALOUD"
                    if pending_start_line is None:
                        pending_start_line = p_start
                    pending_verbatim_lines.extend(surviving_lines)
                    continue

                if RE_PRAYER_HEADER_RUBRIC.match(joined_text):
                    pending_prayer_title = joined_text.strip("* :")
                    if "secret" in joined_text.lower() or "mystically" in joined_text.lower():
                        pending_delivery_mode = "SECRET"
                    elif "aloud" in joined_text.lower() or "loudly" in joined_text.lower():
                        pending_delivery_mode = "ALOUD"
                    if pending_start_line is None:
                        pending_start_line = p_start
                    pending_verbatim_lines.extend(surviving_lines)
                    continue

                if (
                    RE_STANDALONE_HYMN_ROLE.match(joined_text)
                    and len(joined_text) <= 180
                    and len(joined_text.split()) <= 20
                    and bool(re.search(r"(?::\*?|\.\*|\])\s*(?:\[\^\d+\])*$", joined_text))
                ):
                    role_norm = joined_text if joined_text.startswith("*") else f"*{joined_text.strip('* ')}*"
                    if pending_hymn_role:
                        pending_hymn_role = f"{role_norm} {pending_hymn_role}"
                    else:
                        pending_hymn_role = role_norm
                    if pending_start_line is None:
                        pending_start_line = p_start
                    pending_verbatim_lines.extend(surviving_lines)
                    continue

            if pending_hymn_role:
                if not joined_text.startswith("#"):
                    joined_text = f"{pending_hymn_role} {joined_text}"
                pending_hymn_role = None

            actual_start = pending_start_line if pending_start_line is not None else p_start
            verbatim_all = "\n".join(pending_verbatim_lines + surviving_lines)

            raw_blocks.append({
                "cohort": c_idx,
                "leaf": curr_leaf,
                "leaf_span": [f"p{curr_leaf}"],
                "locus": curr_locus,
                "running_header": curr_running_header,
                "text": joined_text,
                "chained_prayer_title": pending_prayer_title,
                "chained_delivery_mode": pending_delivery_mode,
                "chained_speaker": pending_speaker,
                "woodcut_initial": pending_woodcut_initial,
                "provenance": {
                    "source_file": rel_path,
                    "source_sha256": file_sha256,
                    "source_format": "TEXT_LINES",
                    "start_line": actual_start,
                    "end_line": p_end,
                    "verbatim_source": verbatim_all[:1200],
                },
            })

            pending_prayer_title = None
            pending_delivery_mode = None
            pending_speaker = None
            pending_woodcut_initial = None
            pending_hymn_role = None
            pending_start_line = None
            pending_verbatim_lines = []

    # Cross-leaf mid-sentence continuation stitcher
    stitched_blocks: List[Dict[str, Any]] = []
    for blk in raw_blocks:
        txt = blk["text"]
        if (
            stitched_blocks
            and not txt.startswith("#")
            and not stitched_blocks[-1]["text"].startswith("#")
            and blk["chained_prayer_title"] is None
            and blk["chained_speaker"] is None
        ):
            prev = stitched_blocks[-1]
            prev_txt = re.sub(r"(?:\s*\[\^\d+\]|\*)+$", "", prev["text"]).rstrip()
            curr_clean = re.sub(r"^\*\*[A-Za-z]+\s+\(continued\):\*\*\s*", "", txt, flags=re.IGNORECASE)
            curr_clean = re.sub(r"^\[continues[^\]]*\]\s*", "", curr_clean, flags=re.IGNORECASE)
            curr_probe = re.sub(r"^\*+", "", curr_clean).lstrip()

            is_prev_open = (
                prev_txt.endswith("...")
                or prev_txt.endswith("…")
                or prev_txt.endswith(",")
                or prev_txt.endswith(";")
                or prev_txt.endswith("-")
                or bool(re.search(r"[a-z]$", prev_txt))
            )
            is_curr_cont = (
                curr_probe.startswith("...")
                or curr_probe.startswith("…")
                or bool(re.match(r"^[a-z]", curr_probe))
                or "(continued)" in txt[:35].lower()
            )
            if blk["leaf"] >= prev["leaf"] and is_prev_open and is_curr_cont:
                merged_prev = re.sub(r"(?:\.\.\.|…)\s*$", "", prev["text"]).rstrip()
                merged_curr = re.sub(r"^(?:\.\.\.|…)\s*", "", curr_clean).lstrip()
                prev["text"] = f"{merged_prev} {merged_curr}"
                leaf_tag = f"p{blk['leaf']}"
                if leaf_tag not in prev["leaf_span"]:
                    prev["leaf_span"].append(leaf_tag)
                if prev["provenance"]["source_file"] == blk["provenance"]["source_file"]:
                    prev["provenance"]["end_line"] = blk["provenance"]["end_line"]
                    comb_v = prev["provenance"]["verbatim_source"] + "\n" + blk["provenance"]["verbatim_source"]
                    prev["provenance"]["verbatim_source"] = comb_v[:1200]
                continue

        stitched_blocks.append(blk)

    return stitched_blocks


def extract_monument_atomic_corpus(
    monument_id: str,
    sync_hub: bool = False,
) -> Dict[str, Any]:
    """
    Extracts the 5-class atomic liturgical corpus and variable propers corpus
    for a single monument, writing deliverables to Final MD/ and optionally
    syncing to Typikon Coded/Data/Inbox/.
    """
    registry = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    mon_info = registry.get("monuments", {}).get(monument_id)
    if not mon_info:
        raise KeyError(f"Unknown monument_id '{monument_id}' in codex_registry.json")

    mon_type = resolve_monument_type(monument_id, mon_info)
    book_prefix = MONUMENT_TYPE_TO_PREFIX.get(mon_type, "LIT")
    cycle_name = MONUMENT_TYPE_TO_CYCLE.get(mon_type, "LITURGICAL_CORPUS")

    ws_rel = mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
    ws_dir = PROJECT_ROOT / ws_rel
    final_md_dir = ws_dir / "Final MD"
    final_md_dir.mkdir(parents=True, exist_ok=True)
    source_dir = ws_dir / "Source Text"

    folio_offset = int(mon_info.get("folio_offset", 0) or 0)
    total_pages = int(mon_info.get("total_physical_pages", 0) or 0)

    pod_catalog, stichoi_catalog = load_primitives_data()
    slavonic_by_leaf = parse_slavonic_by_leaf(source_dir, ws_dir)
    blocks = collect_cohort_blocks(ws_dir, folio_offset=folio_offset)

    # Active hierarchical coordinates
    part_h1 = mon_info.get("short_title", monument_id)
    office_h2 = "Opening Section"
    current_section = "Introductory Material"
    current_season_or_tone = "Tone 1" if mon_type == "octoechos" else cycle_name
    current_day_or_date = "General"
    current_tone: Optional[int] = 1 if mon_type == "octoechos" else None
    current_ode: Optional[int] = None
    active_podoben_id: Optional[str] = None
    active_podoben_slavonic: Optional[str] = None
    active_stichos: Optional[str] = None
    active_doxology_tag: Optional[str] = None
    active_litany_type: Optional[str] = None
    active_psalm_or_lection = False
    active_hymn_subtype_cue: Optional[str] = None
    litany_petition_idx = 0
    section_hymn_seq = 0

    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8,
        "i": 1, "ii": 2, "iii": 3, "iv": 4,
        "v": 5, "vi": 6, "vii": 7, "viii": 8,
    }

    slav_cursor_by_leaf: Dict[int, int] = {}
    atomic_units: List[Dict[str, Any]] = []
    propers_items: List[Dict[str, Any]] = []
    leaf_seq_counter: Dict[int, int] = {}

    for blk in blocks:
        txt = blk["text"].strip()
        leaf_num = blk["leaf"]
        locus = blk["locus"]
        c_idx = blk["cohort"]

        # Track H1 / H2 / H3 structural headings
        if txt.startswith("#"):
            hdr_clean = re.sub(r"\[\^\d+\]", "", txt.lstrip("#")).strip()
            active_psalm_or_lection = False
            active_hymn_subtype_cue = None
            m_t = re.search(
                r"\bTONE\s+(\d+|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|I|II|III|IV|V|VI|VII|VIII)\b",
                hdr_clean,
                re.IGNORECASE,
            )
            if m_t:
                t_raw = m_t.group(1).lower()
                t_val = word_to_num.get(t_raw, int(t_raw) if t_raw.isdigit() else 0)
                if 1 <= t_val <= 8:
                    current_tone = t_val
                    current_season_or_tone = f"Tone {t_val}"
                    current_ode = None
                    active_podoben_id = None

            m_ode = re.search(r"\b(?:ODE|CANTICLE)\s+(\d+)\b", hdr_clean, re.IGNORECASE)
            if m_ode:
                current_ode = int(m_ode.group(1))
                current_section = f"Canon — Ode {current_ode}"
                section_hymn_seq = 0
                continue

            if txt.startswith("# "):
                part_h1 = hdr_clean
                if not m_t and mon_type in ("lenten_triodion", "pentecostarion", "anthologion", "horologion"):
                    current_season_or_tone = hdr_clean
                current_ode = None
                active_litany_type = None
                litany_petition_idx = 0
                continue
            elif txt.startswith("## "):
                office_h2 = hdr_clean
                for day_w in ("SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"):
                    if day_w in hdr_clean.upper():
                        current_day_or_date = hdr_clean
                        break
                current_ode = None
                active_litany_type = None
                litany_petition_idx = 0
                section_hymn_seq = 0
                continue
            else:
                current_section = hdr_clean
                section_hymn_seq = 0
                continue

        # Update inline Tone / Ode / Day / Menologion context from leading italic tags
        first_line = txt.splitlines()[0].strip()
        m_in_t = re.search(r"\bTone\s+([1-8])\b", first_line, re.IGNORECASE)
        if m_in_t:
            current_tone = int(m_in_t.group(1))
            if mon_type == "octoechos":
                current_season_or_tone = f"Tone {current_tone}"

        m_in_ode = re.match(r"^\*?(?:(?:After\s+Ode\s+[1-9],\s*)?(?:Ode|Canticle))\s+([1-9])\b", first_line, re.IGNORECASE)
        if m_in_ode and not first_line.lower().startswith("*after ode"):
            current_ode = int(m_in_ode.group(1))
            current_section = f"Canon — Ode {current_ode}"
            section_hymn_seq = 0
            active_psalm_or_lection = False

        if RE_SECTION_RUBRIC_CUE.match(first_line):
            current_section = first_line.strip("* :")
            section_hymn_seq = 0
            active_psalm_or_lection = False

        m_men = RE_MENOLOGION_DAY.match(first_line)
        if m_men:
            current_day_or_date = first_line.strip("* ")
            active_psalm_or_lection = False

        # Match paired Slavonic paragraph from same physical leaf
        s_list = slavonic_by_leaf.get(leaf_num, [])
        s_cur = slav_cursor_by_leaf.get(leaf_num, 0)
        slav_text = ""
        if s_list:
            if s_cur < len(s_list):
                slav_text = s_list[s_cur]
                slav_cursor_by_leaf[leaf_num] = s_cur + 1
            else:
                slav_text = s_list[-1]
        slav_words = slav_text.split()
        slav_incipit = " ".join(slav_words[:6]) if slav_words else ""
        slav_stem = normalize_slavonic_tier2(" ".join(slav_words[:8])) if slav_words else ""

        # Determine Unit Class & Subtype
        unit_class = "RUBRIC_OR_STATUTE"
        unit_subtype = "CEREMONIAL_ACTION"
        target_shard = "01_ordinarium_primitives.json"
        codex_domain = "ORDINARIUM_PRIMITIVES"

        # Class-specific fields
        rite_name = part_h1
        structural_slot = f"{office_h2} :: {current_section}"
        delivery_mode = blk["chained_delivery_mode"] or ("SECRET" if "secretly" in first_line.lower() else "ALOUD")
        prayer_title = blk["chained_prayer_title"]
        speaker = blk["chained_speaker"]
        woodcut_initial = blk["woodcut_initial"]
        doxology_formula: Optional[str] = None
        litany_or_exchange_type: Optional[str] = None
        petition_index: Optional[int] = None
        lxx_ref: Optional[str] = None
        primitive_stichos_id: Optional[str] = None
        zachalo_number: Optional[str] = None
        doxology_tag: Optional[str] = active_doxology_tag
        stamford_suffix: Optional[str] = None

        m_lxx = re.search(r"\[((?:LXX\s+)?(?:Ps(?:alm)?\.?|Isa\.?|Gen\.?|Prov\.?|Matt\.?|Mt\.?|Mark|Mk\.?|Luke|Lk\.?|John|Jn\.?|Rom\.?|1?\s*Cor\.?|2\s*Cor\.?|Gal\.?|Eph\.?|Phil\.?|Col\.?|1?\s*Tim\.?|2\s*Tim\.?|Heb\.?|Acts)\s+[^\]]+)\]", txt)
        if m_lxx:
            lxx_ref = m_lxx.group(1).strip()
        m_zach = re.search(r"\b(?:Pericope|Section|Zachalo|lection)\s*\[?(\d+)\]?", txt, re.IGNORECASE)
        if m_zach:
            zachalo_number = m_zach.group(1)

        # Check standalone Podoben prescription line
        if RE_PODOBEN_HEADER.match(txt) and "\n" not in txt and len(txt) < 220:
            m_paren_c = re.search(r"\(([^)]*[\u0400-\u04ff\ua640-\ua69f][^)]*)\)", txt)
            pod_slav = m_paren_c.group(1).strip() if m_paren_c else slav_incipit
            p_id, _, _ = match_podoben_model(txt, pod_slav, current_tone or 1, pod_catalog)
            active_podoben_id = p_id
            active_podoben_slavonic = pod_slav
            unit_class = "RUBRIC_OR_STATUTE"
            unit_subtype = "PODOBEN_PRESCRIPTION"
            active_psalm_or_lection = False
        # Check standalone Verse / Stichos line
        elif re.match(r"^\*(?:Verse|Stichos)(?:\s+\d+)?:\*", txt, re.IGNORECASE) and len(txt) < 260:
            unit_class = "FIXED_ORDINARY_OR_LECTION"
            unit_subtype = "PSALM_STICHOS"
            active_stichos = txt.strip("* ")
            low_v = txt.lower()
            for st_entry in stichoi_catalog:
                if any(pat in low_v for pat in st_entry.get("english_patterns", [])):
                    primitive_stichos_id = st_entry["id"]
                    if not lxx_ref:
                        lxx_ref = st_entry.get("lxx_ref")
                    break
        # Check standalone Doxology header (*Glory... Both now...*)
        elif re.match(r"^\*(?:Glory\s+to\s+the\s+Father|Glory\.\.\.|Glory\s*:|Glory,|Both\s+now)\b[^*\n]*\*(?:\s*\[\^\d+\])*\s*$", txt, re.IGNORECASE) and len(txt) < 120:
            unit_class = "FIXED_ORDINARY_OR_LECTION"
            unit_subtype = "DOXOLOGY_HEADER"
            if "glory" in txt.lower() and "both now" in txt.lower():
                active_doxology_tag = "GLORY_BOTH_NOW"
            elif "glory" in txt.lower():
                active_doxology_tag = "GLORY"
            else:
                active_doxology_tag = "BOTH_NOW"
            if "theotokion" in txt.lower():
                active_hymn_subtype_cue = "THEOTOKION"
        else:
            # Check inline speaker prefix (**Priest:**, **Deacon:**, **Choir:**)
            m_isp = RE_INLINE_SPEAKER.match(txt)
            if m_isp and not txt.startswith("*Ode ") and not txt.startswith("*Troparion"):
                speaker = m_isp.group(1).upper()
                sp_mod = (m_isp.group(2) or "").lower()
                if "secret" in sp_mod:
                    delivery_mode = "SECRET"
                elif "aloud" in sp_mod or "loud" in sp_mod:
                    delivery_mode = "ALOUD"

            # 1. Check SACERDOTAL_PRAYER
            is_prayer = (
                prayer_title is not None
                or bool(re.match(r"^\*(?:(?:The\s+)?(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Another)\s+Prayer\b|Prayer\s+(?:of|for|over|at|before|after|unto|to)\b|Exorcism\b)", first_line, re.IGNORECASE))
                or (speaker == "PRIEST" and delivery_mode == "SECRET" and len(txt) >= 120)
                or (speaker == "PRIEST" and len(txt) >= 210 and not RE_LITANY_PETITION_END.search(txt))
            )
            if is_prayer:
                unit_class = "SACERDOTAL_PRAYER"
                active_psalm_or_lection = False
                active_hymn_subtype_cue = None
                p_probe = f"{prayer_title or ''} {office_h2} {first_line}".lower()
                if "exorcism" in p_probe:
                    unit_subtype = "EXORCISM_PRAYER"
                elif "proskomedia" in p_probe or "prothesis" in p_probe or "offering" in p_probe:
                    unit_subtype = "PROSKOMEDIA_PRAYER"
                elif "antiphon" in p_probe:
                    unit_subtype = "ANTIPHON_PRAYER"
                elif "trisagion" in p_probe or "thrice-holy" in p_probe:
                    unit_subtype = "TRISAGION_PRAYER"
                elif "catechumen" in p_probe or "faithful" in p_probe:
                    unit_subtype = "CATECHUMEN_OR_FAITHFUL_PRAYER"
                elif "cherubic" in p_probe:
                    unit_subtype = "CHERUBIC_PRAYER"
                elif "anaphora" in p_probe or "holy oblation" in p_probe or "epiclesis" in p_probe:
                    unit_subtype = "ANAPHORA_PRAYER"
                elif "bowing" in p_probe or "bowed their heads" in p_probe:
                    unit_subtype = "HEAD_BOWING_PRAYER"
                elif "ambon" in p_probe:
                    unit_subtype = "AMBON_PRAYER"
                elif "kneeling" in p_probe or "pentecost" in p_probe:
                    unit_subtype = "KNEELING_PRAYER"
                elif delivery_mode == "SECRET":
                    unit_subtype = "SECRET_PRAYER"
                elif mon_type == "trebnyk_euchologion":
                    unit_subtype = "SACRAMENTAL_PRAYER"
                else:
                    unit_subtype = "DEVOTIONAL_PRAYER"

                m_dox = re.search(r"(For\s+(?:unto\s+Thee\s+is\s+due|Thine\s+is\s+the\s+kingdom|Thou\s+art\s+a\s+merciful|blessed\s+and\s+glorified)[^\.!\n]+[\.!])", txt, re.IGNORECASE)
                if m_dox:
                    doxology_formula = m_dox.group(1).strip()

            # 2. Check LITANY_OR_DIALOGUE
            elif (
                speaker is not None
                or RE_SACRAMENTAL_FORMULA.search(txt)
                or RE_EKPHONESIS_FORMULA.search(txt)
                or RE_LITANY_PETITION_END.search(txt)
                or re.match(r"^\*(?:Dismissal\s+(?:on|for|of)|After\s+the\s+(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth)\s+Ode|And\s+the\s+exclamation)\b", first_line, re.IGNORECASE)
            ):
                unit_class = "LITANY_OR_DIALOGUE"
                active_psalm_or_lection = False
                active_hymn_subtype_cue = None
                if RE_SACRAMENTAL_FORMULA.search(txt):
                    unit_subtype = "SACRAMENTAL_DECLARATIVE_FORMULA"
                    litany_or_exchange_type = "SACRAMENTAL_FORM"
                elif re.match(r"^\*After\s+the\s+(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth)\s+Ode\b", first_line, re.IGNORECASE):
                    unit_subtype = "PASCHAL_ODE_EKTENIA_EXCLAMATION"
                    litany_or_exchange_type = "PASCHAL_LITTLE_LITANY"
                elif re.match(r"^\*Dismissal\b", first_line, re.IGNORECASE) or "may christ our true god" in txt.lower():
                    unit_subtype = "WEEKLY_AND_FESTAL_APOLYSIS" if first_line.startswith("*") else "DISMISSAL"
                    litany_or_exchange_type = "APOLYSIS_DISMISSAL"
                elif RE_EKPHONESIS_FORMULA.search(txt) or "exclamation:" in first_line.lower():
                    unit_subtype = "EXCLAMATION_EKPHONESIS"
                    litany_or_exchange_type = "SACERDOTAL_EKPHONESIS"
                    active_litany_type = None
                    litany_petition_idx = 0
                elif RE_LITANY_PETITION_END.search(txt):
                    speaker = speaker or "DEACON"
                    if "in peace let us pray" in txt.lower() or "for the peace from above" in txt.lower():
                        active_litany_type = "GREAT_LITANY"
                        litany_petition_idx = 1
                    elif "again and again in peace" in txt.lower():
                        active_litany_type = "LITTLE_LITANY"
                        litany_petition_idx = 1
                    elif "have mercy on us, o god, according to thy great mercy" in txt.lower():
                        active_litany_type = "FERVENT_LITANY"
                        litany_petition_idx = 1
                    elif "catechumens" in txt.lower():
                        active_litany_type = "CATECHUMENS_LITANY"
                        litany_petition_idx = 1
                    elif "let us ask of the lord" in txt.lower():
                        active_litany_type = "SUPPLICATORY_AITESIS"
                        litany_petition_idx += 1
                    else:
                        active_litany_type = active_litany_type or "GREAT_LITANY"
                        litany_petition_idx += 1
                    unit_subtype = active_litany_type
                    litany_or_exchange_type = active_litany_type
                    petition_index = litany_petition_idx
                elif speaker in ("CHOIR", "CHOIRS", "PEOPLE", "READER", "CHANTER", "CHANTERS"):
                    unit_subtype = "CHOIR_OR_READER_RESPONSE"
                    litany_or_exchange_type = "CONGREGATIONAL_RESPONSE"
                elif speaker == "DEACON":
                    unit_subtype = "DEACON_COMMAND"
                    litany_or_exchange_type = "DIACONAL_BIDDING"
                elif "peace be unto all" in txt.lower():
                    unit_subtype = "PEACE_DIALOGUE"
                    litany_or_exchange_type = "PAX_EXCHANGE"
                elif "lift up our hearts" in txt.lower() or "let us give thanks unto the lord" in txt.lower():
                    unit_subtype = "ANAPHORA_DIALOGUE"
                    litany_or_exchange_type = "SURSUM_CORDA"
                else:
                    unit_subtype = "DIALOGUE_EXCHANGE"
                    litany_or_exchange_type = "LITURGICAL_DIALOGUE"

            # 3. Check FIXED_ORDINARY_OR_LECTION (Psalms, Prokeimena, Alleluia, Communion Hymns, Epistles, Gospels, Paremia)
            elif (
                re.match(
                    r"^\*?(?:Psalm\s+\d+|A\s+Psalm\s+of\s+David|(?:Great\s+)?Prokeimenon|Alleluia|Communion\s+(?:Hymn|Verse)|Koinonikon|Kinonikon|The\s+Reading\s+is\s+from|(?:The\s+)?Holy\s+Gospel\s+according\s+to|Gospel\s+according\s+to|Epistle\s+of|(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh)\s+Matins\s+Resurrection\s+Gospel)\b",
                    first_line,
                    re.IGNORECASE,
                )
                or (not txt.startswith("*") and lxx_ref and "ps" in lxx_ref.lower())
                or (not txt.startswith("*") and active_psalm_or_lection and len(txt) >= 35)
            ):
                unit_class = "FIXED_ORDINARY_OR_LECTION"
                active_hymn_subtype_cue = None
                fl_low = first_line.lower()
                if "psalm" in fl_low or (lxx_ref and "ps" in lxx_ref.lower()) or active_psalm_or_lection:
                    unit_subtype = "PSALM_TEXT"
                elif "prokeimenon" in fl_low:
                    unit_subtype = "PROKEIMENON"
                elif "alleluia" in fl_low:
                    unit_subtype = "REFRAN_ALLELUIA"
                elif "communion" in fl_low or "koinonikon" in fl_low or "kinonikon" in fl_low:
                    unit_subtype = "COMMUNION_KOINONIKON"
                elif "gospel" in fl_low:
                    unit_subtype = "GOSPEL_PERICOPE"
                elif "epistle" in fl_low or "acts" in fl_low:
                    unit_subtype = "EPISTLE_PERICOPE"
                else:
                    unit_subtype = "OT_PAREMIA"

            # 4. Check PROPER_HYMN
            elif (
                re.match(
                    r"^\*?(?:(?:After\s+Ode\s+[1-9],\s*)?(?:Ode|Canticle)\s+[1-9][^*\n]*Heirmos|Heirmos|Katavasia|(?:Another\s+|Dismissal\s+|Resurrectional\s+)?Troparion|(?:Cross-|Stavro|Stauro)?Theotokion|Another\s+Theotokion|To\s+the\s+Cross|(?:Another\s+)?Kontakion|Ikos|(?:Another\s+)?Sessional\s+Hymn|Kathisma|Exapost[ei]larion|Photagogi[ck]on|Hymn\s+of\s+Light|Evangelical\s+Sticheron|Eothinon|Hypakoe|Ypako[eë]|Gradual\s+Hymn|Songs\s+of\s+Ascent|Antiphon\s+\d+|On\s+the\s+Beatitudes|In\s+the\s+Beatitudes|Beatitudes|Martyri[ck]on|Triadi[ck]on|For\s+the\s+Departed|Nekrosimon|Megalynarion|Sticheron|Stichera|Idiomelon|Prosomoia|Tone\s+[1-8],\s*Podoben:)\b",
                    first_line,
                    re.IGNORECASE,
                )
                or re.match(r"^\*\*We\s+magnify\s+(?:Thee|you)\b", first_line, re.IGNORECASE)
                or (
                    active_hymn_subtype_cue is not None
                    and len(txt) >= 40
                    and not bool(re.search(r":\*(?:\s*\[\^\d+\])*$", txt))
                )
                or (
                    mon_type in HYMNOGRAPHIC_AND_HOROLOGION_TYPES
                    and not (txt.startswith("*") and txt.endswith("*") and "\n" not in txt)
                    and not txt.startswith("[")
                    and not txt.startswith("*(")
                    and not txt.startswith("|")
                    and (current_ode is not None or active_podoben_id is not None or active_stichos is not None or "stichera" in current_section.lower() or "canon" in current_section.lower() or "anabathm" in current_section.lower() or "gradual" in current_section.lower() or "sessional" in current_section.lower())
                    and len(txt) >= 45
                )
            ):
                unit_class = "PROPER_HYMN"
                active_psalm_or_lection = False
                fl_low = first_line.lower()
                if "heirmos" in fl_low:
                    unit_subtype = "HEIRMOS"
                elif "katavasia" in fl_low:
                    unit_subtype = "KATAVASIA"
                elif "stavrotheotokion" in fl_low or "staurotheotokion" in fl_low or "cross-theotokion" in fl_low or "to the cross" in fl_low:
                    unit_subtype = "STAVROTHEOTOKION"
                elif "theotokion" in fl_low or "dogmatikon" in fl_low:
                    unit_subtype = "THEOTOKION"
                elif "triadikon" in fl_low or "triadicon" in fl_low or "trinity" in fl_low:
                    unit_subtype = "TRIADIKON"
                elif "martyrikon" in fl_low or "martyricon" in fl_low or "for the martyrs" in fl_low:
                    unit_subtype = "MARTYRIKON"
                elif "departed" in fl_low or "nekrosimon" in fl_low:
                    unit_subtype = "NEKROSIMON"
                elif "kontakion" in fl_low:
                    unit_subtype = "KONTAKION"
                elif "ikos" in fl_low:
                    unit_subtype = "IKOS"
                elif "sessional" in fl_low or "kathisma" in fl_low or "stichologia" in fl_low:
                    unit_subtype = "SESSIONAL_HYMN"
                elif "exapost" in fl_low or "photagog" in fl_low or "hymn of light" in fl_low:
                    unit_subtype = "EXAPOSTILARION"
                elif "evangelical" in fl_low or "eothinon" in fl_low:
                    unit_subtype = "EOTHINON"
                elif "hypakoe" in fl_low or "ypakoe" in fl_low:
                    unit_subtype = "HYPAKOE"
                elif "gradual" in fl_low or "ascent" in fl_low or "antiphon" in fl_low:
                    unit_subtype = "ANABATHMOS"
                elif "beatitudes" in fl_low:
                    unit_subtype = "BEATITUDES_TROPARION"
                elif "megalynarion" in fl_low or first_line.lower().startswith("**we magnify"):
                    unit_subtype = "MEGALYNARION"
                elif active_hymn_subtype_cue:
                    unit_subtype = active_hymn_subtype_cue
                elif current_ode is not None:
                    unit_subtype = "CANON_TROPARION"
                elif "troparion" in fl_low:
                    unit_subtype = "TROPARION"
                else:
                    unit_subtype = "STICHERON"
                active_hymn_subtype_cue = None

                # Check if inline Podoben is attached to the hymn's first line
                if "podoben:" in fl_low:
                    m_paren_c = re.search(r"\(([^)]*[\u0400-\u04ff\ua640-\ua69f][^)]*)\)", first_line)
                    pod_slav = m_paren_c.group(1).strip() if m_paren_c else slav_incipit
                    p_id, _, _ = match_podoben_model(first_line, pod_slav, current_tone or 1, pod_catalog)
                    active_podoben_id = p_id
                    active_podoben_slavonic = pod_slav

                # Route to Shared_Lexicon 4-Shard Corpus
                if unit_subtype in ("HEIRMOS", "KATAVASIA"):
                    target_shard = "03_irmologion.json"
                    codex_domain = "IRMOLOGION"
                elif current_ode is not None and unit_subtype in ("CANON_TROPARION", "THEOTOKION", "STAVROTHEOTOKION", "TRIADIKON"):
                    target_shard = "04_kanonnik.json"
                    codex_domain = "KANONNIK"
                else:
                    target_shard = "02_sticherarion.json"
                    codex_domain = "STICHERARION"

                # Compute Stamford sequence suffix (_1, _2, _glory, _both_now, _glory_both_now)
                if "glory" in fl_low and "both now" in fl_low:
                    doxology_tag = "GLORY_BOTH_NOW"
                    stamford_suffix = "_glory_both_now"
                elif fl_low.startswith("*glory"):
                    doxology_tag = "GLORY"
                    stamford_suffix = "_glory"
                elif fl_low.startswith("*both now"):
                    doxology_tag = "BOTH_NOW"
                    stamford_suffix = "_both_now"
                elif active_doxology_tag:
                    doxology_tag = active_doxology_tag
                    stamford_suffix = f"_{active_doxology_tag.lower()}"
                    active_doxology_tag = None
                else:
                    section_hymn_seq += 1
                    stamford_suffix = f"_{section_hymn_seq}"

            # 5. Otherwise RUBRIC_OR_STATUTE
            else:
                unit_class = "RUBRIC_OR_STATUTE"
                low_t = txt.lower()
                if re.search(r"(?:psalm\s+(?:of\s+david,?\s*)?\d+|\[lxx\s+ps\.\s*\d+\]):?\*(?:\s*\[\^\d+\])*$", low_t):
                    active_psalm_or_lection = True
                elif re.search(r"\b(kontakion|troparion|theotokion|sessional\s+hymn|hypakoe|exapostilarion|stichera|troparia)\b[^*\n]*:\*(?:\s*\[\^\d+\])*$", low_t):
                    if "kontakion" in low_t.split(";")[-1]:
                        active_hymn_subtype_cue = "KONTAKION"
                    elif "theotokion" in low_t.split(";")[-1]:
                        active_hymn_subtype_cue = "THEOTOKION"
                    elif "sessional" in low_t.split(";")[-1]:
                        active_hymn_subtype_cue = "SESSIONAL_HYMN"
                    elif "tropar" in low_t.split(";")[-1]:
                        active_hymn_subtype_cue = "TROPARION"
                    else:
                        active_hymn_subtype_cue = "STICHERON"
                else:
                    active_hymn_subtype_cue = None
                if m_men:
                    unit_subtype = "MENOLOGION_DAY_HEADER"
                elif RE_NOMOCANON_HEADER.match(first_line) or (mon_type == "juridical_synodal" and len(txt) >= 80):
                    unit_subtype = "NOMOCANON_CANON_OR_DEGREE" if mon_type == "trebnyk_euchologion" else "CANONICAL_STATUTE"
                elif re.search(r"\b(?:Instruction\s+of\s+Saint|Discourse\s+of\s+Saint|Catechetical\s+Word\s+of|Homily)\b", txt, re.IGNORECASE):
                    unit_subtype = "PATRISTIC_HOMILY"
                elif "synaxarion" in low_t or ("in the same month" in low_t and len(txt) >= 200):
                    unit_subtype = "HAGIOGRAPHICAL_SYNAXARION"
                elif re.search(r"\b(?:if\s+it\s+be\s+a\s+Sunday|if\s+the\s+Feast\s+falls|it\s+should\s+be\s+known\s+that|when\s+the\s+feast\s+of)\b", low_t):
                    unit_subtype = "COLLISION_MARKIAN_RULE"
                elif re.search(r"\b(?:if\s+a\s+child\s+be\s+weak|in\s+danger\s+of\s+death|cautela|warning\s+to\s+the\s+priest)\b", low_t):
                    unit_subtype = "SACRAMENTAL_CAUTELA"
                elif re.search(r"\b(?:gave\s+this\s+book|in\s+the\s+name\s+of\s+the\s+father.*servant\s+of\s+god.*presented|cursed\s+and\s+anathematized)\b", low_t):
                    unit_subtype = "DEDICATION_OR_FOUNDATION_INSCRIPTION"
                elif txt.startswith("[") or txt.startswith("*(") or "woodcut" in low_t or "headpiece" in low_t or "vacat" in low_t:
                    unit_subtype = "VISUAL_ORNAMENT_OR_MARGINALIA"
                elif c_idx == 1 and ("to the reader" in low_t or "preface" in low_t or "title page" in low_t or "printed" in low_t):
                    unit_subtype = "FRONT_MATTER_PARATEXT"
                elif re.search(r"\b(?:we\s+stitch|sign\s+to\s+sing|twice|thrice|stichera\s+on\s+\d+)\b", low_t):
                    unit_subtype = "HYMNOGRAPHIC_PRESCRIPTION"
                else:
                    unit_subtype = "CEREMONIAL_ACTION"

        leaf_seq = leaf_seq_counter.get(leaf_num, 0) + 1
        leaf_seq_counter[leaf_num] = leaf_seq
        corpus_id = f"{book_prefix}.{monument_id.upper()}.C{c_idx:03d}.P{leaf_num:04d}.U{leaf_seq:03d}"

        fn_refs = [f"[^{m}]" for m in re.findall(r"\[\^(\d+)\]", txt)]
        actors_found = [a for a in ACTOR_KEYWORDS if re.search(rf"\b{a}\b", txt, re.IGNORECASE)]
        realia_found = [r for r in REALIA_KEYWORDS if re.search(rf"\b{r}\b", txt, re.IGNORECASE)]
        is_cond = bool(re.search(r"\b(?:if|when|whenever|unless|should)\b", txt[:80], re.IGNORECASE))

        parent_heirmos_id = (
            f"HEIRMOS.T{current_tone}.ODE{current_ode}"
            if (unit_class == "PROPER_HYMN" and current_ode in range(1, 10) and current_tone in range(1, 9))
            else None
        )

        unit_record: Dict[str, Any] = {
            "corpus_id": corpus_id,
            "monument_id": monument_id,
            "monument_type": mon_type,
            "unit_class": unit_class,
            "unit_subtype": unit_subtype,
            "target_shard": target_shard,
            "codex_domain": codex_domain,
            "cohort": c_idx,
            "leaf": f"p{leaf_num}",
            "leaf_span": blk["leaf_span"],
            "locus": locus,
            "running_header": blk["running_header"],
            "coordinates": {
                "cycle": cycle_name,
                "part_h1": part_h1,
                "office_h2": office_h2,
                "section": current_section,
                "season_or_tone": current_season_or_tone,
                "day_or_date": current_day_or_date,
                "tone": current_tone,
                "ode": current_ode,
            },
            "hymnographic_metadata": {
                "podoben_id": active_podoben_id if unit_class == "PROPER_HYMN" else None,
                "podoben_slavonic_witness": active_podoben_slavonic if unit_class == "PROPER_HYMN" else None,
                "parent_heirmos_id": parent_heirmos_id,
                "preceding_stichos": active_stichos if unit_class == "PROPER_HYMN" else None,
                "doxology_tag": doxology_tag if unit_class == "PROPER_HYMN" else None,
                "stamford_slug_suffix": stamford_suffix,
            },
            "euchological_and_rubrical_metadata": {
                "rite": rite_name,
                "structural_slot": structural_slot,
                "delivery_mode": delivery_mode if unit_class in ("SACERDOTAL_PRAYER", "LITANY_OR_DIALOGUE") else None,
                "prayer_title": prayer_title,
                "woodcut_initial": woodcut_initial,
                "doxology_formula": doxology_formula,
                "litany_or_exchange_type": litany_or_exchange_type,
                "petition_index": petition_index,
                "speaker": speaker,
                "lxx_or_biblical_ref": lxx_ref,
                "primitive_stichos_id": primitive_stichos_id,
                "zachalo_number": zachalo_number,
                "is_conditional": is_cond,
                "actors_referenced": actors_found,
                "realia_referenced": realia_found,
            },
            "slavonic_incipit": slav_incipit,
            "slavonic_stem_tier2": slav_stem,
            "slavonic_text": slav_text,
            "english_text": txt,
            "footnotes_referenced": fn_refs,
            "provenance": blk["provenance"],
        }
        atomic_units.append(unit_record)

        if unit_class == "PROPER_HYMN":
            propers_items.append({
                "corpus_id": corpus_id,
                "tone": current_tone or 0,
                "cohort": c_idx,
                "leaf": f"p{leaf_num}",
                "locus": locus,
                "office": office_h2,
                "section": current_section,
                "season_or_tone": current_season_or_tone,
                "day_or_date": current_day_or_date,
                "ode": current_ode,
                "hymn_type": unit_subtype,
                "target_shard": target_shard,
                "codex_domain": codex_domain,
                "podoben_id": active_podoben_id,
                "podoben_slavonic_witness": active_podoben_slavonic,
                "parent_heirmos_id": parent_heirmos_id,
                "preceding_stichos": active_stichos,
                "doxology_tag": doxology_tag,
                "stamford_slug_suffix": stamford_suffix,
                "slavonic_text": slav_text,
                "english_text": txt,
                "provenance": blk["provenance"],
            })
            # Consume preceding_stichos once attached to its governed hymn
            active_stichos = None

    # Build summary statistics
    counts_by_class: Dict[str, int] = {k: 0 for k in VALID_UNIT_CLASSES}
    counts_by_subtype: Dict[str, int] = {}
    counts_by_shard: Dict[str, int] = {
        "01_ordinarium_primitives.json": 0,
        "02_sticherarion.json": 0,
        "03_irmologion.json": 0,
        "04_kanonnik.json": 0,
    }
    leaves_covered = sorted(list({u["leaf"] for u in atomic_units}), key=lambda s: int(s.lstrip("p") or 0))
    stitched_count = sum(1 for u in atomic_units if len(u.get("leaf_span", [])) > 1)

    for u in atomic_units:
        counts_by_class[u["unit_class"]] = counts_by_class.get(u["unit_class"], 0) + 1
        counts_by_subtype[u["unit_subtype"]] = counts_by_subtype.get(u["unit_subtype"], 0) + 1
        counts_by_shard[u["target_shard"]] = counts_by_shard.get(u["target_shard"], 0) + 1

    atomic_payload = {
        "monument_id": monument_id,
        "monument_title": mon_info.get("title", monument_id),
        "monument_type": mon_type,
        "corpus_schema": "3.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_provenance": {
            "workspace_dir": ws_rel,
            "total_physical_pages": total_pages,
            "leaves_covered_count": len(leaves_covered),
            "cross_leaf_stitched_units": stitched_count,
            "total_atomic_units": len(atomic_units),
        },
        "summary": {
            "counts_by_unit_class": counts_by_class,
            "counts_by_target_shard": counts_by_shard,
            "counts_by_subtype": dict(sorted(counts_by_subtype.items(), key=lambda kv: -kv[1])),
        },
        "units": atomic_units,
    }

    atomic_path = final_md_dir / f"{monument_id}_atomic_corpus.json"
    atomic_path.write_text(json.dumps(atomic_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"  [Atomic Corpus] Emitted {atomic_path.relative_to(PROJECT_ROOT)} "
        f"({len(atomic_units):,} total units: {counts_by_class['PROPER_HYMN']:,} propers, "
        f"{len(atomic_units) - counts_by_class['PROPER_HYMN']:,} non-propers)"
    )

    # Emit or enrich {monument_id}_propers_corpus.json
    propers_path = final_md_dir / f"{monument_id}_propers_corpus.json"
    if mon_type == "octoechos" and propers_path.exists():
        # Enrich existing Octoechos propers corpus in-place so Gate 7D item counts remain 100% intact
        try:
            existing_p = json.loads(propers_path.read_text(encoding="utf-8"))
            ex_items = existing_p.get("items", [])
            if len(ex_items) >= len(propers_items):
                for idx_it, it in enumerate(ex_items, start=1):
                    h_type = str(it.get("hymn_type", "Sticheron")).upper()
                    ode_v = it.get("ode")
                    if "HEIRMOS" in h_type or "KATAVASIA" in h_type:
                        it["target_shard"] = "03_irmologion.json"
                        it["codex_domain"] = "IRMOLOGION"
                    elif ode_v is not None and ("TROPARION" in h_type or "THEOTOKION" in h_type):
                        it["target_shard"] = "04_kanonnik.json"
                        it["codex_domain"] = "KANONNIK"
                    else:
                        it["target_shard"] = "02_sticherarion.json"
                        it["codex_domain"] = "STICHERARION"
                    it.setdefault("stamford_slug_suffix", f"_{idx_it}")
                existing_p["corpus_schema"] = "3.0.0"
                propers_path.write_text(json.dumps(existing_p, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        except (OSError, json.JSONDecodeError):
            pass
    elif propers_items:
        propers_payload = {
            "monument_id": monument_id,
            "monument_type": mon_type,
            "corpus_schema": "3.0.0",
            "corpus_type": f"{mon_type.upper()}_PROPERS_BILINGUAL_COMPLETE",
            "source_provenance": {
                "source_dir": f"{ws_rel}/Source Text",
                "cohorts_dir": f"{ws_rel}/Cohorts",
                "total_stanzas_extracted": len(propers_items),
            },
            "items": propers_items,
        }
        propers_path.write_text(json.dumps(propers_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  [Propers Corpus] Emitted {propers_path.relative_to(PROJECT_ROOT)} ({len(propers_items):,} proper hymns)")

    # Emit Podoben Grid for hymnographic / Horologion monuments if _complete.md exists
    comp_file = final_md_dir / f"{monument_id}_complete.md"
    if mon_type in HYMNOGRAPHIC_AND_HOROLOGION_TYPES and comp_file.exists():
        try:
            emit_podoben_grid(monument_id)
        except (OSError, ValueError, KeyError) as e:
            print(f"  [Podoben Grid] Note for {monument_id}: {e}")

    # Sync companion files to Typikon Coded Hub Inbox if requested
    if sync_hub:
        hub_root = PROJECT_ROOT.parent / "Typikon Coded" / "Data" / "Inbox"
        if hub_root.exists():
            pub_spec = mon_info.get("publication_spec", {})
            hub_folder = pub_spec.get("hub_inbox_folder", monument_id)
            target_inbox = hub_root / hub_folder
            target_inbox.mkdir(parents=True, exist_ok=True)
            synced = 0
            for comp_name in (
                f"{monument_id}_atomic_corpus.json",
                f"{monument_id}_propers_corpus.json",
                f"{monument_id}_podoben_grid.json",
                f"{monument_id}_podoben_grid.md",
            ):
                src_f = final_md_dir / comp_name
                if src_f.exists():
                    shutil.copy2(src_f, target_inbox / comp_name)
                    synced += 1
            print(f"  [Hub Sync] Synced {synced} atomic/podoben deliverables to Typikon Coded/Data/Inbox/{hub_folder}")

    return atomic_payload


def batch_extract_all_completed(sync_hub: bool = False) -> Dict[str, Any]:
    """Runs atomic extraction across all completed/audited monuments and writes ATOMIC_CORPUS_LEDGER.{json,md}."""
    registry = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    monuments = registry.get("monuments", {})

    summaries: List[Dict[str, Any]] = []
    global_by_class: Dict[str, int] = {k: 0 for k in VALID_UNIT_CLASSES}
    global_by_shard: Dict[str, int] = {
        "01_ordinarium_primitives.json": 0,
        "02_sticherarion.json": 0,
        "03_irmologion.json": 0,
        "04_kanonnik.json": 0,
    }
    total_units_all = 0

    for mon_id, mon_info in monuments.items():
        status = mon_info.get("status", "")
        if status not in ("completed", "paused", "in_progress"):
            continue
        ws_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{mon_id}")
        if not ws_dir.exists():
            continue
        has_cohorts = (ws_dir / "Cohorts").exists() and bool(list((ws_dir / "Cohorts").glob("*cohort*.md")))
        has_final = (ws_dir / "Final").exists() and bool(list((ws_dir / "Final").glob("*.txt")))
        if not (has_cohorts or has_final):
            continue

        payload = extract_monument_atomic_corpus(mon_id, sync_hub=sync_hub)
        c_class = payload["summary"]["counts_by_unit_class"]
        c_shard = payload["summary"]["counts_by_target_shard"]
        u_total = payload["source_provenance"]["total_atomic_units"]
        total_units_all += u_total

        for k, v in c_class.items():
            global_by_class[k] = global_by_class.get(k, 0) + v
        for k, v in c_shard.items():
            global_by_shard[k] = global_by_shard.get(k, 0) + v

        summaries.append({
            "monument_id": mon_id,
            "monument_type": payload["monument_type"],
            "status": status,
            "leaves_covered": payload["source_provenance"]["leaves_covered_count"],
            "cross_leaf_stitched": payload["source_provenance"]["cross_leaf_stitched_units"],
            "total_units": u_total,
            "PROPER_HYMN": c_class.get("PROPER_HYMN", 0),
            "SACERDOTAL_PRAYER": c_class.get("SACERDOTAL_PRAYER", 0),
            "LITANY_OR_DIALOGUE": c_class.get("LITANY_OR_DIALOGUE", 0),
            "FIXED_ORDINARY_OR_LECTION": c_class.get("FIXED_ORDINARY_OR_LECTION", 0),
            "RUBRIC_OR_STATUTE": c_class.get("RUBRIC_OR_STATUTE", 0),
        })

    ledger = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_monuments_extracted": len(summaries),
        "total_atomic_units_extracted": total_units_all,
        "global_counts_by_unit_class": global_by_class,
        "global_counts_by_target_shard": global_by_shard,
        "monuments": summaries,
    }

    audit_dir = PROJECT_ROOT / "Audit_Reports"
    audit_dir.mkdir(parents=True, exist_ok=True)
    ledger_json = audit_dir / "ATOMIC_CORPUS_LEDGER.json"
    ledger_md = audit_dir / "ATOMIC_CORPUS_LEDGER.md"
    ledger_json.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md_lines = [
        "# Universal Atomic Liturgical Corpus Ledger (Propers + Non-Propers)",
        "",
        f"- **Generated At**: `{ledger['generated_at']}`",
        f"- **Total Monuments Extracted**: `{len(summaries)}`",
        f"- **Total Atomic Units Extracted**: `{total_units_all:,}`",
        "",
        "## Global Distribution by 5 Atomic Unit Classes",
        "",
        "| Unit Class | Total Atomic Units | Target `Shared_Lexicon` Shard(s) |",
        "| :--- | :---: | :--- |",
        f"| **`PROPER_HYMN`** | `{global_by_class['PROPER_HYMN']:,}` | `02_sticherarion.json`, `03_irmologion.json`, `04_kanonnik.json` |",
        f"| **`SACERDOTAL_PRAYER`** | `{global_by_class['SACERDOTAL_PRAYER']:,}` | `01_ordinarium_primitives.json` |",
        f"| **`LITANY_OR_DIALOGUE`** | `{global_by_class['LITANY_OR_DIALOGUE']:,}` | `01_ordinarium_primitives.json` |",
        f"| **`FIXED_ORDINARY_OR_LECTION`** | `{global_by_class['FIXED_ORDINARY_OR_LECTION']:,}` | `01_ordinarium_primitives.json` |",
        f"| **`RUBRIC_OR_STATUTE`** | `{global_by_class['RUBRIC_OR_STATUTE']:,}` | `01_ordinarium_primitives.json` |",
        "",
        "## Global Distribution by `Shared_Lexicon` 4-Shard Routing",
        "",
        "| Target Shard | Domain | Total Atomic Units |",
        "| :--- | :--- | :---: |",
        f"| `01_ordinarium_primitives.json` | `ORDINARIUM_PRIMITIVES` | `{global_by_shard['01_ordinarium_primitives.json']:,}` |",
        f"| `02_sticherarion.json` | `STICHERARION` | `{global_by_shard['02_sticherarion.json']:,}` |",
        f"| `03_irmologion.json` | `IRMOLOGION` | `{global_by_shard['03_irmologion.json']:,}` |",
        f"| `04_kanonnik.json` | `KANONNIK` | `{global_by_shard['04_kanonnik.json']:,}` |",
        "",
        "## Per-Monument Atomic Decomposition",
        "",
        "| Monument ID | Type | Leaves | Stitched | Total Units | `PROPER_HYMN` | `SACERDOTAL_PRAYER` | `LITANY_OR_DIALOGUE` | `ORDINARY_LECTION` | `RUBRIC_STATUTE` |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    for s in summaries:
        md_lines.append(
            f"| `{s['monument_id']}` | `{s['monument_type']}` | {s['leaves_covered']} | {s['cross_leaf_stitched']} | "
            f"**{s['total_units']:,}** | {s['PROPER_HYMN']:,} | {s['SACERDOTAL_PRAYER']:,} | "
            f"{s['LITANY_OR_DIALOGUE']:,} | {s['FIXED_ORDINARY_OR_LECTION']:,} | {s['RUBRIC_OR_STATUTE']:,} |"
        )
    ledger_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"\n[Ledger] Wrote {ledger_md.relative_to(PROJECT_ROOT)} ({len(summaries)} monuments, {total_units_all:,} atomic units).")
    return ledger


def main() -> None:
    parser = argparse.ArgumentParser(description="Universal Atomic Liturgical Corpus Extractor")
    parser.add_argument("--monument", help="Extract atomic corpus for a single monument ID")
    parser.add_argument("--all-completed", action="store_true", help="Batch-extract all completed/audited monuments")
    parser.add_argument("--sync-hub", action="store_true", help="Synchronize emitted corpora and Podoben grids to Typikon Coded Hub Inbox")
    args = parser.parse_args()

    if args.all_completed:
        batch_extract_all_completed(sync_hub=args.sync_hub)
    elif args.monument:
        extract_monument_atomic_corpus(args.monument, sync_hub=args.sync_hub)
    else:
        parser.error("Provide --monument <ID> or --all-completed")


if __name__ == "__main__":
    main()
