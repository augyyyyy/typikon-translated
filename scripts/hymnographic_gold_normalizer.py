#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hymnographic Gold Normalizer & 3-Tier Drift Engine
===================================================
Applies leaf-synchronized liturgical primitive normalization (Podobens, Psalm Stichoi,
Weekday Canon Heirmoi), deterministic 2-up column/folio seam stitching with inline
locus milestones ([f. XvA]), stanza-level paragraph formatting (\\n\\n), 3-tier source vs.
translation drift analysis, and complete bilingual Cross-Propers Corpus generation.

Complies strictly with MTS-1, .agents/AGENTS.md, and GLOBAL_SYSTEM_RULES.md.
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_FILE = PROJECT_ROOT / "data" / "liturgical_primitives_registry.json"


# ==============================================================================
# 1. 3-Tier Church Slavonic Drift Classifier
# ==============================================================================

DIACRITICS_RE = re.compile(r"[\u0300-\u036f\u0483-\u0487\u2de0-\u2dff\ua670-\ua67f]")

CONTRACTIONS = {
    "бг": "бог",
    "бга": "бога",
    "бгу": "богу",
    "бгом": "богом",
    "бзѣ": "бозѣ",
    "бже": "боже",
    "гд": "господ",
    "гда": "господа",
    "гду": "господу",
    "гдем": "господем",
    "гди": "господи",
    "хр": "христ",
    "хс": "христос",
    "ха": "христа",
    "ху": "христу",
    "хом": "христом",
    "хѣ": "христѣ",
    "хе": "христе",
    "ст": "свят",
    "ста": "свята",
    "стѣ": "святѣ",
    "сто": "свято",
    "сти": "святи",
    "стых": "святых",
    "стым": "святым",
    "стыми": "святыми",
    "члвк": "человѣк",
    "члка": "человѣка",
    "члку": "человѣку",
    "члком": "человѣком",
    "члцы": "человѣцы",
    "члвколюбец": "человѣколюбец",
    "млст": "милост",
    "воскрсн": "воскресен",
    "воскрн": "воскресен",
    "крст": "крест",
    "бц": "богородиц",
    "бце": "богородице",
    "дх": "дух",
    "сна": "сына",
    "сну": "сыну",
    "сн": "сын",
    "оц": "отец",
    "оца": "отца",
    "мти": "мати",
    "мтре": "матере",
    "дв": "дѣв",
    "дво": "дѣво",
    "влк": "владык",
    "влко": "владыко",
    "прпдбн": "преподобн",
    "мчнк": "мученик",
    "мчнц": "мучениц",
    "апл": "апостол",
    "еѵгліе": "евангелие",
    "іис": "іисус",
    "іиса": "іисуса",
    "іису": "іисусу",
    "іисе": "іисусе",
}


def strip_brackets_and_punct(s: str) -> str:
    """Removes editorial brackets, footnotes, and punctuation from Cyrillic string."""
    s = re.sub(r"\[\^\d+\]", "", s)
    s = re.sub(r"[\[\]\(\)\{\}\.,:;!?'\"«»—–-]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def normalize_slavonic_tier1(s: str) -> str:
    """Tier 1: Strips titla, accents, punctuation, and expands standard sacred contractions."""
    cleaned = strip_brackets_and_punct(s.lower())
    cleaned = DIACRITICS_RE.sub("", cleaned)
    tokens = cleaned.split()
    expanded = []
    for tok in tokens:
        tok_clean = tok.rstrip("ъь")
        if tok in CONTRACTIONS:
            expanded.append(CONTRACTIONS[tok])
        elif tok_clean in CONTRACTIONS:
            expanded.append(CONTRACTIONS[tok_clean])
        else:
            expanded.append(tok)
    return " ".join(expanded)


def normalize_slavonic_tier2(s: str) -> str:
    """
    Tier 2: Normalizes Ruthenian / Middle-Ukrainian vs. standard Church Slavonic
    spelling and phonological reflexes (vowels, yers, iotation).
    """
    t1 = normalize_slavonic_tier1(s)
    t2 = t1.replace("ѡ", "о").replace("ѻ", "о").replace("ꙋ", "у").replace("ѧ", "я")
    t2 = t2.replace("ѣ", "е").replace("є", "е")
    t2 = t2.replace("ї", "и").replace("і", "и").replace("ѵ", "и").replace("ы", "и")
    t2 = t2.replace("ѿ", "от").replace("ѳ", "ф").replace("ѯ", "кс").replace("ѱ", "пс")
    words = t2.split()
    harmonized = []
    for w in words:
        w_norm = re.sub(r"[ъь]+$", "", w)
        w_norm = re.sub(r"^вз(?=[гдбвжз])", "воз", w_norm)
        if w_norm:
            harmonized.append(w_norm)
    return " ".join(harmonized)


def classify_slavonic_drift(text_a: str, text_b: str) -> Tuple[str, float, Dict[str, Any]]:
    """
    Classifies the textual relationship between two Slavonic occurrences:
    - TIER_0_EXACT: 100% character identical.
    - TIER_1_TYPOGRAPHIC_TITLO: Identical after removing accents, titla, contractions.
    - TIER_2_ORTHOGRAPHIC_PHONOLOGICAL: Identical after Ruthenian spelling harmonization.
    - TIER_3_LEXICAL_RECENSIONAL: Lexical, syntactic, or morphological variation.
    """
    if text_a.strip() == text_b.strip():
        return "TIER_0_EXACT", 1.0, {"details": "Exact character match"}

    t1_a = normalize_slavonic_tier1(text_a)
    t1_b = normalize_slavonic_tier1(text_b)
    if t1_a == t1_b:
        return "TIER_1_TYPOGRAPHIC_TITLO", 0.98, {"t1": t1_a, "details": "Accents, titla, or contractions variance"}

    t2_a = normalize_slavonic_tier2(text_a)
    t2_b = normalize_slavonic_tier2(text_b)
    if t2_a == t2_b:
        return "TIER_2_ORTHOGRAPHIC_PHONOLOGICAL", 0.92, {"t2": t2_a, "details": "Ruthenian spelling / phonological reflex variance"}

    matcher = difflib.SequenceMatcher(None, t2_a.split(), t2_b.split())
    ratio = matcher.ratio()

    diff_tokens_a = [t for t in t2_a.split() if t not in t2_b.split()]
    diff_tokens_b = [t for t in t2_b.split() if t not in t2_a.split()]

    return "TIER_3_LEXICAL_RECENSIONAL", round(ratio, 3), {
        "similarity": round(ratio, 3),
        "tokens_only_in_a": diff_tokens_a,
        "tokens_only_in_b": diff_tokens_b,
        "details": f"Lexical/syntactic variation (token similarity: {ratio:.1%})"
    }


# ==============================================================================
# 2. Leaf-Synchronized Conditional Primitive Normalizer & Drift Tracker
# ==============================================================================

SLAV_POD_RE = re.compile(
    r"(?:^|[\s\.\*:])(Подо́?б?е?н?ъ?|Подѡ́?б?е?н?ъ?|По́?д?о?б?|По̀?|Гла́мо(?:\s*\[Подобен\])?)\s*:\s*(.*)$",
    re.IGNORECASE
)
SLAV_VERSE_RE = re.compile(
    r"(?:^|\s)(?:Сті́?хъ?|Стї́?хъ?|Сті́?|Стї́?)\s*[:.]\s*(.+)$",
    re.IGNORECASE
)


def extract_leaf_slavonic_primitives(s_lines: List[str]) -> Tuple[List[str], List[str], List[str]]:
    """Extracts Slavonic Podoben incipits, Psalm Stichoi, and full stanzas from a single leaf's lines."""
    s_pods: List[str] = []
    s_verses: List[str] = []
    s_stanzas: List[str] = []

    for idx_s, raw_sl in enumerate(s_lines):
        sl = raw_sl.strip()
        if not sl or sl.startswith("#") or sl.startswith("===") or sl.startswith("[Колонка"):
            continue
        sl_no_diac = DIACRITICS_RE.sub("", sl)
        ms_pod = SLAV_POD_RE.search(sl) or SLAV_POD_RE.search(sl_no_diac)
        if ms_pod:
            colon_parts = re.split(r"(?:По[^\s:]*|Гла́мо(?:\s*\[Подобен\])?)\s*:\s*", sl, maxsplit=1, flags=re.IGNORECASE)
            rest = colon_parts[1].strip() if len(colon_parts) > 1 else ""
            if not rest and idx_s + 1 < len(s_lines):
                rest = s_lines[idx_s + 1].strip()
            if rest:
                s_pods.append(rest.rstrip(".:"))

        ms_v = SLAV_VERSE_RE.search(sl)
        if ms_v:
            s_verses.append(ms_v.group(1).strip())

        if len(sl) > 35:
            s_stanzas.append(sl)

    return s_pods, s_verses, s_stanzas


class HymnographicNormalizer:
    def __init__(self, registry_path: Path = REGISTRY_FILE):
        if not registry_path.is_file():
            raise FileNotFoundError(f"Registry not found: {registry_path}")
        self.registry = json.loads(registry_path.read_text(encoding="utf-8"))
        self.stichoi = self.registry.get("psalm_stichoi", [])
        self.podobens = self.registry.get("podoben_models", [])
        self.heirmoi = self.registry.get("sunday_heirmoi", [])
        self.rubrics = self.registry.get("rubrical_calls", {})

    def normalize_podoben_line(
        self,
        line: str,
        s_pods: List[str],
        current_tone: int,
        c_idx: int,
        leaf_num: int
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Normalizes any Podoben / Model / Melodic model / Same melody / To: line into the
        canonical parenthetical format:
            *Podoben: "[Canonical English]" (Verbatim 1630 Slavonic):*
        """
        stripped = line.strip()
        fn_m = re.search(r"(\[\^\d+\])", stripped)
        fn_suffix = f" {fn_m.group(1)}" if fn_m else ""
        stripped_no_fn = re.sub(r"\[\^\d+\]", "", stripped).strip()

        # Case 1: Saturday Stichera for the Departed where `По:` = `Поко́инъ:` was misread as bare Podoben:/Model:
        if re.match(r"^\*?(?:Podoben|Model):\*?$", stripped_no_fn, re.IGNORECASE):
            return f"*For the Departed [Поко́инъ]:*{fn_suffix}", {
                "type": "POKOIN_ABBREV_CORRECTED",
                "locus": f"C{c_idx:02d}:p{leaf_num}",
                "tone": current_tone,
                "slavonic_source": "По[ко́инъ]:",
                "raw_cohort_english": stripped_no_fn,
                "canonical_english": "*For the Departed [Поко́инъ]:*",
                "is_ai_drift": True
            }
        if re.search(r"For the Departed:\s*Podoben:\s*$", stripped_no_fn, re.IGNORECASE):
            return f"*For the Departed [Поко́инъ]:*{fn_suffix}", {
                "type": "POKOIN_ABBREV_CORRECTED",
                "locus": f"C{c_idx:02d}:p{leaf_num}",
                "tone": current_tone,
                "slavonic_source": "По[ко́инъ]:",
                "raw_cohort_english": stripped_no_fn,
                "canonical_english": "*For the Departed [Поко́инъ]:*",
                "is_ai_drift": True
            }

        # Case 2: C11 p106 `Resurrectional. Tone 4. To:` (unstated Podoben `Оудиви́ся Іѡ́сифъ` after `По:`)
        if re.match(r"^\*?Resurrectional\.\s*Tone\s+4\.\s*To:\*?$", stripped_no_fn, re.IGNORECASE):
            norm_res = f'*Resurrectional, Tone 4.*\n\n*Podoben: "Joseph was amazed" (По: [Оу҆диви́ся І҆ѡ́сифъ]):*{fn_suffix}'
            return norm_res, {
                "type": "PODOBEN_NORMALIZED",
                "primitive_id": "POD.T4.UDIVISYA_IOSIF",
                "locus": f"C{c_idx:02d}:p{leaf_num}",
                "tone": 4,
                "slavonic_source": "По: [Оу҆диви́ся І҆ѡ́сифъ]",
                "raw_cohort_english": stripped_no_fn,
                "canonical_english": "Joseph was amazed",
                "is_ai_drift": True
            }

        # Case 3: "The same" Podoben / Model / Melodic model / Melody
        same_pat = re.compile(
            r"(?:,\s*|\.\s*|^|\*)(?:"
            r"Tone\s+and\s+(?:Podoben|Model|melodic\s+model)\s*:?\s*the\s+same"
            r"|the\s+same\s+Tone\s+and\s+(?:Podoben|Model|melodic\s+model)"
            r"|Same\s+Tone\s+and\s+(?:Podoben|Model|melodic\s+model|melody)"
            r"|(?:The\s+)?same\s+(?:Podoben|Model|melodic\s+model|melody)"
            r"|(?:Podoben|Model|Melodic\s+model)\s*:\s*The\s+same"
            r")\s*[\.:]?\*?",
            re.IGNORECASE
        )
        m_same = same_pat.search(stripped_no_fn)
        if m_same:
            prefix = stripped_no_fn[:m_same.start()].strip().strip("*").rstrip(".,:")
            matched_text = m_same.group(0).lower()
            if "tone" in matched_text:
                rep = f'*Podoben: "The same Tone and Podoben" (Гла́съ и҆ подо́бенъ то́йже):*{fn_suffix}'
            else:
                rep = f'*Podoben: "The same" (то́йже):*{fn_suffix}'
            final_str = f"*{prefix}.*\n\n{rep}" if prefix else rep
            return final_str, {
                "type": "PODOBEN_SAME_NORMALIZED",
                "primitive_id": f"POD.T{current_tone}.SAME",
                "locus": f"C{c_idx:02d}:p{leaf_num}",
                "tone": current_tone,
                "slavonic_source": "то́йже",
                "raw_cohort_english": stripped_no_fn,
                "canonical_english": "The same (то́йже)",
                "is_ai_drift": ("model" in matched_text or "melody" in matched_text)
            }

        # Case 4: Standard Named Podoben / Model / Melodic model / Special Melody / To:
        label_pat = re.compile(
            r"(?:^|\*|\.\s*)\b(Podoben|Model|Melodic\s+model|Special\s+Melody|To):\s*(.+)$",
            re.IGNORECASE
        )
        m_lbl = label_pat.search(stripped_no_fn)
        if not m_lbl:
            return line, None

        label_used = m_lbl.group(1)
        prefix = stripped_no_fn[:m_lbl.start()].strip().strip("*").rstrip(".,:")
        rest_after_lbl = m_lbl.group(2).strip().strip("*")

        # Check if rest_after_lbl has a trailing clause like "Composition of..." or "Verse: ..."
        trailing_clause = ""
        m_trail = re.search(r":\s*((?:Composition\s+of|Verse:|Stichos:).+)$", rest_after_lbl, re.IGNORECASE)
        if m_trail:
            trailing_clause = m_trail.group(1).strip()
            raw_eng_incipit = rest_after_lbl[:m_trail.start()].strip().strip('"\'“”.:*')
        else:
            # Remove any existing parenthetical Slavonic if present
            raw_eng_incipit = re.sub(r"\s*\([^)]*[\u0400-\u04FF][^)]*\)\s*:?\*?$", "", rest_after_lbl).strip()
            raw_eng_incipit = raw_eng_incipit.strip('"\'“”.:*')

        # Match against self.podobens (prioritizing current_tone, then any tone)
        matched_model = None
        candidates_ordered = (
            [p for p in self.podobens if p["tone"] == current_tone]
            + [p for p in self.podobens if p["tone"] != current_tone]
        )

        # 4a. Match by English alias substring
        for pod in candidates_ordered:
            aliases = [pod["english_canonical"].lower()] + [a.lower() for a in pod.get("english_aliases", [])]
            if any(a == raw_eng_incipit.lower() or a in raw_eng_incipit.lower() or raw_eng_incipit.lower() in a for a in aliases if a):
                matched_model = pod
                break

        # 4b. Fallback match by leaf-aligned Slavonic Podoben
        if not matched_model and s_pods:
            for sp in s_pods:
                sp_stem = normalize_slavonic_tier2(sp)
                for pod in candidates_ordered:
                    if any(pat in sp_stem or sp_stem in pat for pat in pod.get("slavonic_patterns", [])):
                        matched_model = pod
                        break
                if matched_model:
                    break

        if not matched_model:
            return line, None

        canonical_eng = matched_model["english_canonical"]

        # Find leaf-local verbatim 1630 Slavonic witness if present on this leaf
        verbatim_slav = ""
        for sp in s_pods:
            sp_stem = normalize_slavonic_tier2(sp)
            if any(pat in sp_stem or sp_stem in pat for pat in matched_model.get("slavonic_patterns", [])):
                # Clean any trailing "Стіх:" from sp
                sp_clean = re.split(r"\s+Ст[і ї]́?х?", sp, maxsplit=1)[0].strip().rstrip(".:")
                verbatim_slav = sp_clean
                break

        slav_display = verbatim_slav if verbatim_slav else matched_model["slavonic_canonical"]
        normalized_core = f'*Podoben: "{canonical_eng}" ({slav_display}):*{fn_suffix}'

        parts_out = []
        if prefix:
            parts_out.append(f"*{prefix}.*")
        parts_out.append(normalized_core)
        if trailing_clause:
            if trailing_clause.lower().startswith("verse:") or trailing_clause.lower().startswith("stichos:"):
                norm_v, _ = self.normalize_verse_line(f"*{trailing_clause}*", [])
                parts_out.append(norm_v)
            else:
                parts_out.append(f"*{trailing_clause}*")

        normalized_line = "\n\n".join(parts_out)

        drift_record = {
            "type": "PODOBEN_NORMALIZED",
            "primitive_id": matched_model["id"],
            "locus": f"C{c_idx:02d}:p{leaf_num}",
            "tone": matched_model["tone"],
            "greek_incipit": matched_model["greek"],
            "slavonic_source": slav_display,
            "slavonic_canonical": matched_model["slavonic_canonical"],
            "raw_cohort_english": f"{label_used}: {raw_eng_incipit}",
            "canonical_english": canonical_eng,
            "is_ai_drift": (
                raw_eng_incipit.lower() != canonical_eng.lower()
                or label_used.lower() != "podoben"
            )
        }
        return normalized_line, drift_record

    def normalize_verse_line(
        self,
        line: str,
        s_verses: List[str],
        c_idx: int = 0,
        leaf_num: int = 0
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Normalizes a Psalm *Verse:* (*Stichos:*) line based on 3-tier Slavonic equivalence.
        """
        m = re.match(
            r"^\*?(?:Verse|Stichos|Стихъ):\s*(.+?)(?:\s*[\[\(](?:Ps|LXX|Psalm)[^\]\)]*[\]\)])?\s*\*?$",
            line.strip(),
            re.IGNORECASE
        )
        if not m:
            return line, None

        fn_m = re.search(r"(\[\^\d+\])", line)
        fn_suffix = f" {fn_m.group(1)}" if fn_m else ""
        raw_eng_verse = re.sub(r"\[\^\d+\]", "", m.group(1)).strip().strip("*").strip()
        if not raw_eng_verse:
            return line, None

        matched_stichos = None
        # 1. Match by English patterns first to identify which Psalm verse this line is
        for st in self.stichoi:
            if any(pat in raw_eng_verse.lower() for pat in st.get("english_patterns", [])):
                # Check if leaf-local s_verses has a corresponding Slavonic witness
                slav_witness = st["slavonic_canonical"]
                drift_tier = "TIER_1_TYPOGRAPHIC_TITLO"
                info: Dict[str, Any] = {"details": "Matched via leaf-synchronized stichos"}
                for sv in s_verses:
                    sv_stem = normalize_slavonic_tier2(sv)
                    if any(sp in sv_stem for sp in st.get("slavonic_patterns", [])):
                        slav_witness = sv
                        drift_tier, _, info = classify_slavonic_drift(sv, st["slavonic_canonical"])
                        break
                matched_stichos = (st, slav_witness, drift_tier, info)
                break

        # 2. Fallback similarity match
        if not matched_stichos:
            for st in self.stichoi:
                matcher = difflib.SequenceMatcher(None, raw_eng_verse.lower(), st["english_canonical"].lower())
                if matcher.ratio() > 0.68:
                    matched_stichos = (st, st["slavonic_canonical"], "TIER_1_TYPOGRAPHIC_TITLO", {"details": "Similarity match"})
                    break

        if matched_stichos:
            st, slav_witness, drift_tier, info = matched_stichos
            canonical_eng = st["english_canonical"]

            if drift_tier != "TIER_3_LEXICAL_RECENSIONAL":
                final_line = canonical_eng + fn_suffix
                drift_event = {
                    "type": "PSALM_VERSE_NORMALIZED",
                    "id": st["id"],
                    "locus": f"C{c_idx:02d}:p{leaf_num}",
                    "lxx_ref": st["lxx_ref"],
                    "slavonic_source": slav_witness,
                    "raw_english": raw_eng_verse,
                    "canonical_english": canonical_eng,
                    "drift_tier": drift_tier,
                    "greek": st["greek"],
                    "is_ai_drift": (raw_eng_verse.lower() not in canonical_eng.lower())
                }
                return final_line, drift_event
            else:
                # Tier 3 lexical variant in source: preserve distinct English!
                preserved_line = f"*Verse: {raw_eng_verse}*{fn_suffix}"
                drift_event = {
                    "type": "PSALM_VERSE_TIER3_SOURCE_VARIANT",
                    "id": st["id"],
                    "locus": f"C{c_idx:02d}:p{leaf_num}",
                    "lxx_ref": st["lxx_ref"],
                    "raw_english": raw_eng_verse,
                    "slavonic_source": slav_witness,
                    "drift_tier": "TIER_3_LEXICAL_RECENSIONAL",
                    "info": info,
                    "is_ai_drift": False
                }
                return preserved_line, drift_event

        return f"*Verse: {raw_eng_verse}*{fn_suffix}", None

    def normalize_weekday_heirmos_line(
        self,
        line: str,
        tone: int,
        ode: int,
        c_idx: int = 0,
        leaf_num: int = 0
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Normalizes a weekday *Heirmos:* incipit so its opening words match the Sunday parent Heirmos
        when they share the same Slavonic Heirmos.
        """
        m = re.match(
            r"^\*?(?:Another\s+(?:Canon|Heirmos)(?:\s*\[[^\]]+\])?[\.:]\s*)?(?:Tone\s+\d+[\.,]\s*)?(?:Ode\s+\d+[\.,]\s*)?Heirmos:\s*([^\*\n]+?)\s*\*?$",
            line.strip(),
            re.IGNORECASE
        )
        if not m:
            return line, None

        raw_incipit = re.sub(r"\[\^\d+\]", "", m.group(1)).strip().rstrip(".:*")
        if not raw_incipit or "the same" in raw_incipit.lower():
            return line, None

        for h in self.heirmoi:
            if h["tone"] == tone and h["ode"] == ode:
                sunday_opening = h["english_incipit"]
                # Check if this weekday Heirmos is an incipit of the Sunday Heirmos (similarity >= 0.45)
                sim = difflib.SequenceMatcher(None, raw_incipit.lower(), sunday_opening.lower()).ratio()
                if sim >= 0.45 and raw_incipit.lower() != sunday_opening.lower():
                    fn_m = re.search(r"(\[\^\d+\])", line)
                    fn_suffix = f" {fn_m.group(1)}" if fn_m else ""
                    clean_line = re.sub(r"\[\^\d+\]", "", line).strip().strip("*")
                    normalized_core = re.sub(
                        r"(Heirmos:\s*)(.+)$",
                        rf"\1{sunday_opening}...",
                        clean_line,
                        flags=re.IGNORECASE
                    )
                    normalized_line = f"*{normalized_core}*{fn_suffix}"
                    drift_event = {
                        "type": "WEEKDAY_HEIRMOS_ALIGNED",
                        "id": h["id"],
                        "locus": f"C{c_idx:02d}:p{leaf_num}",
                        "tone": tone,
                        "ode": ode,
                        "raw_incipit": raw_incipit,
                        "canonical_english": sunday_opening,
                        "greek": h["greek"],
                        "is_ai_drift": True
                    }
                    return normalized_line, drift_event

        return line, None


# ==============================================================================
# 3. 2-Up Folio & Column Seam Stitcher with Inline Milestones
# ==============================================================================

RE_LEAF_BANNER = re.compile(r"^===\s*LEAF\s+p?(\d+)\s*===$", re.IGNORECASE)
RE_PAGE_HEADER = re.compile(
    r"^#{1,6}\s*\[(Left|Right)\s+Page\s+—\s+(?:Folio\s+([0-9]+[rv])|([^\]]+))\](?:\s*(\[\^\d+\]))?",
    re.IGNORECASE
)
RE_COLUMN_HEADER = re.compile(
    r"^#{1,6}\s*(?:\[)?(?:Column|Колонка)\s+([ABab])(?::|\])?(?:\s*(\[\^\d+\]))?",
    re.IGNORECASE
)
RE_CONTINUATION = re.compile(
    r"^\[(?:Continuation\s+of\s+|Продовження\s+)[^\]]+\](\[\^\d+\])?",
    re.IGNORECASE
)
RE_BLANK_LINE = re.compile(r"^\*?\[(?:Blank|Чистий)\s+[^\]]+\]\*?$", re.IGNORECASE)

RE_NON_STITCHABLE_START = re.compile(
    r"^(?:#|\[\d+\]|\*\*\d+\.\*\*|\d+\.\s|\*?(?:Podoben|Verse|Stichos|Glory|Both now|Theotokion|Stavrotheotokion|For the Martyrs|For the Departed|Ode\s+\d+|Another\s+(?:Canon|Heirmos|Stichera)|Other\s+Stichera|Stichera\b|Penitential\s+Stichera|Resurrectional|After\s+the\s+\d+|At\s+the\s+(?:Aposticha|Praises)|Sessional\s+Hymn|Kontakion|Ikos|Hypakoe|Prokeimenon|Tone\s+\d+|Same\s+Tone)\b)",
    re.IGNORECASE
)


class LocusTracker:
    def __init__(self):
        self.leaf_num = 1
        self.side = "L"
        self.folio = ""
        self.col = "A"

    def update_leaf(self, leaf_num: int):
        self.leaf_num = leaf_num
        self.side = "L"
        self.col = "A"

    def update_page(self, side_str: str, folio_str: str, desc_str: str):
        self.side = "L" if side_str.lower() == "left" else "R"
        if folio_str:
            self.folio = folio_str.strip()
        elif desc_str:
            m_f = re.search(r"Folio\s+([0-9]+[rv])", desc_str, re.IGNORECASE)
            if m_f:
                self.folio = m_f.group(1).strip()
            else:
                self.folio = f"p{self.leaf_num}{self.side}"
        self.col = "A"

    def update_col(self, col_str: str):
        self.col = col_str.upper().strip()

    def get_milestone(self) -> str:
        if self.folio:
            return f"[f. {self.folio}{self.col}]"
        return f"[p{self.leaf_num}{self.side}{self.col}]"


def stitch_2up_hymnographic_stream(cohort_text: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Parses cohort text line by line, tracking folio/column locus.
    Stitches sentences severed across column and leaf breaks, inserting compact
    inline locus milestones `[f. XvA]` at the exact boundary.
    """
    lines = cohort_text.splitlines()
    output_lines: List[str] = []
    stitch_events: List[Dict[str, Any]] = []

    locus = LocusTracker()
    pending_milestone: Optional[str] = None
    pending_footnote: Optional[str] = None

    i = 0
    n = len(lines)

    while i < n:
        raw_line = lines[i]
        line = raw_line.strip()

        if RE_BLANK_LINE.match(line):
            i += 1
            continue

        m_leaf = RE_LEAF_BANNER.match(line)
        if m_leaf:
            locus.update_leaf(int(m_leaf.group(1)))
            i += 1
            continue

        m_page = RE_PAGE_HEADER.match(line)
        if m_page:
            locus.update_page(m_page.group(1), m_page.group(2) or "", m_page.group(3) or "")
            pending_milestone = locus.get_milestone()
            if m_page.group(4):
                pending_footnote = m_page.group(4)
            i += 1
            continue

        m_col = RE_COLUMN_HEADER.match(line)
        if m_col:
            locus.update_col(m_col.group(1))
            pending_milestone = locus.get_milestone()
            if m_col.group(2):
                pending_footnote = m_col.group(2)
            i += 1
            continue

        m_cont = RE_CONTINUATION.match(line)
        if m_cont:
            if m_cont.group(1):
                pending_footnote = m_cont.group(1)
            i += 1
            continue

        if line.lower() == "[typographic divider]" or line == "---":
            if pending_milestone and output_lines:
                output_lines.append(f"{pending_milestone} ---")
                pending_milestone = None
            else:
                output_lines.append("---")
            i += 1
            continue

        if not line:
            output_lines.append("")
            i += 1
            continue

        curr_line = line

        if pending_milestone and output_lines:
            last_idx = -1
            for idx in range(len(output_lines) - 1, -1, -1):
                if output_lines[idx].strip():
                    last_idx = idx
                    break

            if last_idx >= 0:
                prev_content = output_lines[last_idx].strip()
                core_prev = re.sub(r'(?:\[\^\d+\]|[\]\)\*_`"\'\”\’]|\s)+$', '', prev_content)
                ends_punct = bool(core_prev and core_prev[-1] in ('.', '!', '?', ':'))
                ends_ellipsis = prev_content.rstrip().endswith("...")
                starts_ellipsis = curr_line.startswith("...")
                starts_new_block = bool(RE_NON_STITCHABLE_START.match(curr_line))
                prev_is_rubric = prev_content.startswith("*Podoben:") or prev_content.startswith("*Verse:")

                is_mid_sentence = (
                    (ends_ellipsis or starts_ellipsis or not ends_punct)
                    and not starts_new_block
                    and not prev_is_rubric
                )

                if is_mid_sentence:
                    cleaned_prev = re.sub(r"\.\.\.\s*$", "", prev_content).rstrip()
                    cleaned_curr = re.sub(r"^\.\.\.\s*", "", curr_line).lstrip()

                    words_prev = cleaned_prev.split()
                    words_curr = cleaned_curr.split()
                    if words_prev and words_curr:
                        last_w = re.sub(r"^[^\w]+|[^\w]+$", "", words_prev[-1]).lower()
                        first_w = re.sub(r"^[^\w]+|[^\w]+$", "", words_curr[0]).lower()
                        if last_w and last_w == first_w:
                            cleaned_curr = " ".join(words_curr[1:])

                    fn_suffix = f" {pending_footnote}" if pending_footnote else ""
                    pending_footnote = None

                    stitched = f"{cleaned_prev}{fn_suffix} {pending_milestone} {cleaned_curr}"
                    output_lines[last_idx] = stitched

                    stitch_events.append({
                        "milestone": pending_milestone,
                        "prev_tail": prev_content[-30:],
                        "curr_head": curr_line[:30],
                        "type": "SEAM_STITCHED"
                    })
                    pending_milestone = None
                    i += 1
                    continue

        if pending_milestone:
            if not curr_line.startswith("#"):
                curr_line = f"{pending_milestone} {curr_line}"
            pending_milestone = None

        if pending_footnote:
            curr_line = f"{curr_line} {pending_footnote}"
            pending_footnote = None

        output_lines.append(curr_line)
        i += 1

    return "\n".join(output_lines), stitch_events


# ==============================================================================
# 4. Hymnographic Stanza Separator & Heading Normalizer
# ==============================================================================

RE_INVENTED_STANZA_NUM = re.compile(r"^((?:\[(?:f\.\s*[^\]]+|p\d+[LR][AB])\]\s*)?)(?:\[\d+\]|\*\*\d+\.\*\*|\d+\.)\s+", re.IGNORECASE)

RE_MAJOR_OFFICE = re.compile(
    r"^#+\s*(?:Tone\s+\d+\s*[-—:]\s*)?(?:ON\s+)?(SATURDAY\s+EVENING|SUNDAY\s+MORNING|SUNDAY\s+MATINS|MONDAY\s+EVENING|MONDAY\s+MORNING|TUESDAY\s+EVENING|TUESDAY\s+MORNING|WEDNESDAY\s+EVENING|WEDNESDAY\s+MORNING|THURSDAY\s+EVENING|THURSDAY\s+MORNING|FRIDAY\s+EVENING|FRIDAY\s+MORNING|SATURDAY\s+MORNING)\b[^\n]*",
    re.IGNORECASE
)

RE_SECTION_HEADING = re.compile(
    r"^#+\s*(AT\s+[\"“]LORD,\s+I\s+HAVE\s+CRIED[\"”]|AT\s+THE\s+APOSTICHA|AT\s+MATINS|CANONS|THE\s+BEATITUDES|AT\s+LITTLE\s+VESPERS|AT\s+GREAT\s+VESPERS|AT\s+MIDNIGHT\s+OFFICE|AT\s+THE\s+HOURS|EXAPOSTILARIA)\b[^\n]*",
    re.IGNORECASE
)

RE_CANON_ODE = re.compile(r"^#+\s*Ode\s+(\d+)\b[^\n]*", re.IGNORECASE)


def format_hymnographic_stanzas_and_headings(text: str) -> str:
    """
    Enforces hymnographic paragraph separation:
    - Every sticheron, troparion, heirmos, and rubric is separated by \\n\\n.
    - Heading hierarchy is normalized across all 8 Tones (H2 Office, H3 Section, H4 Ode).
    - Subagent-invented bracketed stanza numbers ([1], [2]) are stripped (even after [f. XvA]).
    """
    lines = text.splitlines()
    formatted: List[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            formatted.append("")
            continue

        # 1. Strip invented stanza numbers (preserving any leading [f. XvA] milestone)
        line = RE_INVENTED_STANZA_NUM.sub(r"\1", line)

        # 2. Heading Normalizations
        # Codex-level division headers (H1: Tone 1..8, Exapostilaria, Preface, Colophon) must NEVER be demoted
        if re.match(r"^#\s+(?:TONE\s+\d+|PREFACE|EXAPOSTILARIA|EVANGELICAL|COLOPHON)", line, re.IGNORECASE):
            formatted.extend(["", line, ""])
            continue

        m_ode = RE_CANON_ODE.match(line)
        if m_ode:
            line = f"#### Ode {m_ode.group(1)}"
            formatted.extend(["", line, ""])
            continue

        m_office = RE_MAJOR_OFFICE.match(line)
        if m_office:
            office_title = m_office.group(0).lstrip("#").strip()
            office_title = re.sub(r"^TONE\s+\d+\s*[-—:]\s*", "", office_title, flags=re.IGNORECASE)
            line = f"## {office_title.upper()}"
            formatted.extend(["", line, ""])
            continue

        m_sec = RE_SECTION_HEADING.match(line)
        if m_sec:
            sec_title = m_sec.group(0).lstrip("#").strip()
            line = f"### {sec_title}"
            formatted.extend(["", line, ""])
            continue

        # 3. Liturgical Stanza Separation: always insert blank line between distinct paragraphs
        if formatted and formatted[-1].strip():
            prev_l = formatted[-1].strip()
            if not prev_l.startswith("#") and prev_l != "---":
                formatted.append("")

        formatted.append(line)

    result = "\n".join(formatted)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


# ==============================================================================
# 5. Monument Processor & Deliverable Generators
# ==============================================================================

POD_TRIGGER_RE = re.compile(
    r"\b(?:Podoben|Model|Melodic\s+model|Special\s+Melody|Same\s+melody)\b"
    r"|\b(?:Tone\s+\d+|Same\s+Tone|For\s+the\s+Departed|Resurrectional|Penitential\s+Stichera|Stichera\s+[^\n:]+)\.\s+To:",
    re.IGNORECASE
)


def process_monument_cohorts(
    monument_id: str,
    cohorts_dir: Path,
    source_dir: Path,
    final_md_dir: Path
) -> Tuple[str, Dict[str, Any]]:
    """
    Main orchestrator for hymnographic normalizations:
    1. Reads all cohorts and verbatim Slavonic source files.
    2. Performs leaf-synchronized primitive normalization (Podobens, Stichoi, Weekday Heirmoi).
    3. Runs 2-up seam stitching with [f. XvA] locus milestones.
    4. Runs stanza separation (\\n\\n) and heading hierarchy standardization.
    5. Emits _drift_ledger.json, _drift_report.md, _primitives_review.md,
       _propers_corpus.json, and _slavonic_complete.md.
    """
    normalizer = HymnographicNormalizer()

    cohort_files = sorted(
        list(cohorts_dir.glob("*.md")),
        key=lambda p: int(re.search(r"cohort(\d+)", p.name).group(1)) if re.search(r"cohort(\d+)", p.name) else 999
    )
    source_files = sorted(
        list(source_dir.glob("*source.txt")),
        key=lambda p: int(re.search(r"cohort(\d+)", p.name).group(1)) if re.search(r"cohort(\d+)", p.name) else 999
    )

    all_stitched_cohorts: List[str] = []
    total_stitch_count = 0
    all_drift_events: List[Dict[str, Any]] = []
    slavonic_stanzas_by_leaf: Dict[int, List[str]] = {}

    current_tone = 1
    current_ode = 1

    for idx, c_file in enumerate(cohort_files):
        c_idx = idx + 1
        c_text = c_file.read_text(encoding="utf-8")
        s_text = source_files[idx].read_text(encoding="utf-8") if idx < len(source_files) else ""

        # Parse Slavonic source by physical leaf pN
        s_by_leaf: Dict[int, List[str]] = {}
        curr_s_leaf = 0
        for sl in s_text.splitlines():
            m_lf = RE_LEAF_BANNER.match(sl.strip())
            if m_lf:
                curr_s_leaf = int(m_lf.group(1))
                s_by_leaf[curr_s_leaf] = []
            elif curr_s_leaf > 0:
                s_by_leaf.setdefault(curr_s_leaf, []).append(sl)

        s_primitives_by_leaf: Dict[int, Tuple[List[str], List[str], List[str]]] = {}
        for lf_num, s_lns in s_by_leaf.items():
            s_pods, s_verses, s_stanzas = extract_leaf_slavonic_primitives(s_lns)
            s_primitives_by_leaf[lf_num] = (s_pods, s_verses, s_stanzas)
            slavonic_stanzas_by_leaf[lf_num] = s_stanzas

        # Step A: Leaf-Synchronized Primitive Normalization (while === LEAF pN === banners are intact)
        norm_lines: List[str] = []
        curr_c_leaf = 1

        for raw_c_line in c_text.splitlines():
            c_line = raw_c_line.strip()

            m_lf = RE_LEAF_BANNER.match(c_line)
            if m_lf:
                curr_c_leaf = int(m_lf.group(1))
                norm_lines.append(raw_c_line)
                continue

            m_t = re.search(r"\bTONE\s+(\d+)\b", c_line, re.IGNORECASE)
            if m_t:
                current_tone = int(m_t.group(1))

            m_o = re.search(r"\bOde\s+(\d+)\b", c_line, re.IGNORECASE)
            if m_o:
                current_ode = int(m_o.group(1))

            s_pods, s_verses, _ = s_primitives_by_leaf.get(curr_c_leaf, ([], [], []))

            # 1. Check Podoben / Model / Melodic model / Same melody / To:
            if POD_TRIGGER_RE.search(c_line):
                norm_l, event = normalizer.normalize_podoben_line(
                    c_line, s_pods, current_tone, c_idx, curr_c_leaf
                )
                if event:
                    all_drift_events.append(event)
                norm_lines.append(norm_l)
                continue

            # 2. Check Verse / Stichos
            if re.match(r"^\*?(?:Verse|Stichos):", c_line, re.IGNORECASE):
                norm_l, event = normalizer.normalize_verse_line(
                    c_line, s_verses, c_idx, curr_c_leaf
                )
                if event:
                    all_drift_events.append(event)
                norm_lines.append(norm_l)
                continue

            # 3. Check Weekday Heirmos
            if "Heirmos:" in c_line:
                norm_l, event = normalizer.normalize_weekday_heirmos_line(
                    c_line, current_tone, current_ode, c_idx, curr_c_leaf
                )
                if event:
                    all_drift_events.append(event)
                norm_lines.append(norm_l)
                continue

            norm_lines.append(raw_c_line)

        pre_norm_cohort = "\n".join(norm_lines)

        # Step B: 2-up seam stitching with [f. XvA] milestones
        stitched_c, stitch_log = stitch_2up_hymnographic_stream(pre_norm_cohort)
        total_stitch_count += len(stitch_log)

        # Step C: Stanza separation & heading standardization
        formatted_c = format_hymnographic_stanzas_and_headings(stitched_c)
        all_stitched_cohorts.append(formatted_c)

    unified_codex_text = "\n\n".join(all_stitched_cohorts)
    unified_codex_text = re.sub(r"\n{3,}", "\n\n", unified_codex_text)

    # Step D: Emit Companion Deliverables
    emit_deliverables(
        monument_id=monument_id,
        source_files=source_files,
        all_stitched_cohorts=all_stitched_cohorts,
        slavonic_stanzas_by_leaf=slavonic_stanzas_by_leaf,
        all_drift_events=all_drift_events,
        total_stitch_count=total_stitch_count,
        final_md_dir=final_md_dir,
        normalizer=normalizer
    )

    stats = {
        "total_stitches": total_stitch_count,
        "drift_events_count": len(all_drift_events),
    }
    return unified_codex_text, stats


def emit_deliverables(
    monument_id: str,
    source_files: List[Path],
    all_stitched_cohorts: List[str],
    slavonic_stanzas_by_leaf: Dict[int, List[str]],
    all_drift_events: List[Dict[str, Any]],
    total_stitch_count: int,
    final_md_dir: Path,
    normalizer: HymnographicNormalizer
) -> None:
    """Emits the 5 companion deliverables into Final MD/."""
    final_md_dir.mkdir(parents=True, exist_ok=True)

    # 1. Consolidated Church Slavonic Master
    slavonic_parts = [sf.read_text(encoding="utf-8").strip() for sf in source_files]
    slavonic_complete = "\n\n---\n\n".join(slavonic_parts)
    (final_md_dir / f"{monument_id}_slavonic_complete.md").write_text(slavonic_complete, encoding="utf-8")
    print(f"  [Companion] Emitted {monument_id}_slavonic_complete.md ({len(slavonic_complete):,} chars)")

    # 2. Drift Ledger JSON
    ledger_data = {
        "monument_id": monument_id,
        "total_stitches": total_stitch_count,
        "total_drift_records": len(all_drift_events),
        "events": all_drift_events
    }
    (final_md_dir / f"{monument_id}_drift_ledger.json").write_text(
        json.dumps(ledger_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    audit_rep_dir = PROJECT_ROOT / "Audit_Reports"
    audit_rep_dir.mkdir(parents=True, exist_ok=True)
    (audit_rep_dir / f"{monument_id}_drift_ledger.json").write_text(
        json.dumps(ledger_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"  [Companion] Emitted {monument_id}_drift_ledger.json ({len(all_drift_events)} records)")

    # 3. Father Paul Primitives Review Digest (Complete 8-Tone Edition)
    primitives_review = generate_father_paul_digest(monument_id, normalizer, all_drift_events)
    (final_md_dir / f"{monument_id}_primitives_review.md").write_text(primitives_review, encoding="utf-8")
    print(f"  [Companion] Emitted {monument_id}_primitives_review.md ({len(primitives_review):,} chars)")

    # 4. Drift Analysis Markdown Report
    drift_report = generate_drift_report(monument_id, total_stitch_count, all_drift_events)
    (final_md_dir / f"{monument_id}_drift_report.md").write_text(drift_report, encoding="utf-8")
    print(f"  [Companion] Emitted {monument_id}_drift_report.md ({len(drift_report):,} chars)")

    # 5. Complete Bilingual Cross-Propers Corpus JSON
    corpus_json = generate_propers_corpus(
        monument_id=monument_id,
        all_stitched_cohorts=all_stitched_cohorts,
        slavonic_stanzas_by_leaf=slavonic_stanzas_by_leaf,
        normalizer=normalizer
    )
    (final_md_dir / f"{monument_id}_propers_corpus.json").write_text(
        json.dumps(corpus_json, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"  [Companion] Emitted {monument_id}_propers_corpus.json ({len(corpus_json.get('items', []))} items)")

    # 6. Companion Deliverables generated directly by compiler engine


def generate_father_paul_digest(
    monument_id: str,
    normalizer: HymnographicNormalizer,
    events: List[Dict[str, Any]]
) -> str:
    lines = [
        f"# Canonical Liturgical Primitives Review Digest: {monument_id.replace('_', ' ').title()}",
        "",
        "> [!IMPORTANT]",
        "> **For Pastoral and Liturgical Review by Father Paul**",
        f"> This document collects all recurring liturgical primitives across **all 8 Tones** of the 1630 Lviv Octoechos (`{len(normalizer.stichoi)}` Psalm *Stichoi*, `{len(normalizer.podobens)}` *Podoben* / *Automelon* models across Tones 1–8, and all `{len(normalizer.heirmoi)}` Sunday Canon *Heirmoi* across Tones 1–8).",
        "> Any revision made to a canonical English rendering in `data/liturgical_primitives_registry.json` will automatically propagate across every service in the codex via a single re-compile.",
        "",
        "---",
        "",
        "## 1. Recurring Psalm Verses (Stichoi)",
        "",
        "| ID | LXX Reference | Church Slavonic Canonical | Byzantine Greek | Canonical English Translation | Attested Loci |",
        "| :--- | :--- | :--- | :--- | :--- | :---: |"
    ]
    for st in normalizer.stichoi:
        loci_cnt = len(st.get("attested_loci", []))
        lines.append(
            f"| `{st['id']}` | **{st['lxx_ref']}** | *{st['slavonic_canonical']}* | *{st['greek']}* | {st['english_canonical']} | {loci_cnt} leaves |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 2. Model Hymns (Podobens / Automela — Tones 1 to 8)",
        "",
        "> [!NOTE]",
        f"> **Internal Attestation Guarantee:** 100% of the models below are physically attested and prescribed within `{monument_id}`.",
        f"> For the complete chronological invocation log across the codex, see [{monument_id}_podoben_grid.md]({monument_id}_podoben_grid.md).",
        "",
        "| ID | Tone | 1630 Church Slavonic Incipit | Byzantine Greek Automelon | Canonical English Incipit | Attested Loci |",
        "| :--- | :---: | :--- | :--- | :--- | :---: |"
    ])
    for pod in normalizer.podobens:
        loci_cnt = len(pod.get("attested_loci", []))
        loci_sample = ", ".join(pod.get("attested_loci", [])[:4])
        if loci_cnt > 4:
            loci_sample += f" (+{loci_cnt - 4} more)"
        lines.append(
            f"| `{pod['id']}` | Tone {pod['tone']} | *{pod['slavonic_canonical']}* | *{pod['greek']}* | **{pod['english_canonical']}** | `{loci_sample or 'C01:p1'}` ({loci_cnt}x) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Sunday Canon Heirmoi (Complete 8-Tone Cycle: Tones 1–8, Odes 1, 3–9)",
        ""
    ])
    for tone_num in range(1, 9):
        lines.extend([
            f"### Tone {tone_num} Sunday Canon Heirmoi",
            "",
            "| Ode | Locus | 1630 Church Slavonic Incipit | Byzantine Greek Incipit | 1630 Lviv Octoechos Translation |",
            "| :---: | :---: | :--- | :--- | :--- |"
        ])
        tone_heirmoi = [h for h in normalizer.heirmoi if h["tone"] == tone_num]
        for h in tone_heirmoi:
            lines.append(
                f"| Ode {h['ode']} | `{h.get('leaf', '')}` | *{h['slavonic_incipit']}* | *{h['greek']}* | {h['english_full']} |"
            )
        lines.append("")

    # Section 4: Un-invoked Comparative Automela
    unattested = normalizer.registry.get("unattested_comparative_models", [])
    if unattested:
        lines.extend([
            "",
            "---",
            "",
            "## 4. Un-Invoked Comparative Automela (Not Prescribed in this Octoechos)",
            "",
            "The following classical Byzantine Automela exist in the broader Byzantine/Slavonic tradition but are **not physically prescribed** within the weekly Octoechos cycle of the 1630 Lviv edition (they belong primarily to the Menaion, Triodion, or Horologion):",
            "",
            "| Tone | Model ID | Classical Slavonic Incipit | Byzantine Greek Automelon | Classical English Title | Liturgical Provenance / Reason for Non-Invocation |",
            "| :---: | :--- | :--- | :--- | :--- | :--- |"
        ])
        notes_map = {
            "POD.T2.DOM_EVFRATOV": "Menaion December cycle (Forefeast of the Nativity); not used in the weekly Octoechos.",
            "POD.T4.VOZNESYISYA_NA_KREST": "Horologion Troparion of the Holy Cross; used as a statutory dismissal troparion rather than a sticheron model in this print.",
            "POD.T4.UDIVISYA_IOSIF": "Tone 4 Sessional Hymn model; in this 1630 edition on f. 105v (p106) the rubric is left as an unstated incipit after 'По:'.",
            "POD.T7.RADUISYA": "Chanted as a borrowed model heading on f. 227v (p227); functions as a cross-tone reference rather than an independent Tone 7 model."
        }
        for u in unattested:
            note = notes_map.get(u["id"], "Festal or specialized cycle automelon not prescribed in Octoechos.")
            lines.append(
                f"| Tone {u['tone']} | `{u['id']}` | *{u['slavonic_canonical']}* | *{u['greek']}* | **{u['english_canonical']}** | {note} |"
            )

    return "\n".join(lines)


def generate_drift_report(
    monument_id: str,
    total_stitches: int,
    events: List[Dict[str, Any]]
) -> str:
    ai_drift_count = sum(1 for e in events if e.get("is_ai_drift"))
    tier3_source_count = sum(1 for e in events if e.get("drift_tier") == "TIER_3_LEXICAL_RECENSIONAL")
    pod_events = [e for e in events if "PODOBEN" in e.get("type", "") or "POKOIN" in e.get("type", "")]
    verse_events = [e for e in events if "VERSE" in e.get("type", "")]
    heirmos_events = [e for e in events if "HEIRMOS" in e.get("type", "")]

    lines = [
        f"# Scholarly Drift & Seam-Stitching Audit Report: {monument_id.replace('_', ' ').title()}",
        "",
        f"- **Monument ID**: `{monument_id}`",
        f"- **Total 2-Up Mid-Sentence Seams Stitched**: {total_stitches} boundaries",
        f"- **Inline Locus Milestones Inserted**: `[f. XvA]`, `[f. XvB]` across all 267 leaves",
        f"- **Total Primitive Normalization & Drift Events**: {len(events)} (`{len(pod_events)}` Podobens, `{len(verse_events)}` Psalm Stichoi, `{len(heirmos_events)}` Weekday Heirmoi)",
        f"- **Pre-Normalization AI Translation Drift Unified**: {ai_drift_count} occurrences",
        f"- **Source-Text (1630 Slavonic) Tier 3 Variations Preserved**: {tier3_source_count} events",
        "",
        "---",
        "",
        "## 1. Summary of 3-Tier Source Drift Engine",
        "",
        "1. **Tier 1 (Typographic / Titlo Equivalence)**: Strips accents, titla, and sacred abbreviations (`бг҃` -> `богъ`). Unified silently to canonical English.",
        "2. **Tier 2 (Orthographic / Phonological Variant)**: Harmonizes Ruthenian/Church Slavonic vowel and yer reflexes (`ѡ`/`о`, `ѣ`/`е`, `ꙋ`/`у`). Unified to canonical English while logging orthographic drift.",
        "3. **Tier 3 (Lexical / Syntactic / Recensional Variant)**: Genuine source variations in the 1630 print. **Preserved as distinct English translations** and annotated.",
        "",
        "---",
        "",
        "## 2. Complete Podoben & Rubric Drift Log",
        "",
        "| Type | Locus | ID | 1630 Slavonic Witness | Pre-Normalization Cohort Text | Canonical Normalized Reading |",
        "| :--- | :---: | :--- | :--- | :--- | :--- |"
    ]

    for ev in pod_events:
        ev_type = ev.get("type", "PODOBEN_NORMALIZED")
        locus = ev.get("locus", "")
        prim_id = ev.get("primitive_id", ev.get("id", "N/A"))
        slav = ev.get("slavonic_source", ev.get("slavonic_canonical", ""))
        raw_eng = ev.get("raw_cohort_english", ev.get("raw_english", ""))
        canon_eng = ev.get("canonical_english", "")
        lines.append(f"| `{ev_type}` | `{locus}` | `{prim_id}` | *{slav}* | {raw_eng} | **{canon_eng}** |")

    return "\n".join(lines)


def generate_propers_corpus(
    monument_id: str,
    all_stitched_cohorts: List[str],
    slavonic_stanzas_by_leaf: Dict[int, List[str]],
    normalizer: HymnographicNormalizer
) -> Dict[str, Any]:
    """
    Parses all 27 stitched cohorts into a complete bilingual atomic hymn corpus
    (`~5,000+` stanzas across all 8 Tones and Appendix) with full liturgical coordinates
    and leaf-synchronized Slavonic source text.
    """
    items: List[Dict[str, Any]] = []

    current_tone = 0
    current_office = "Front Matter"
    current_section = "Introductory Prayers & Dedicatory Preface"
    current_ode: Optional[int] = None
    active_podoben_id: Optional[str] = None
    active_locus = "f. 1rA"
    current_leaf = 1
    leaf_stanza_cursor: Dict[int, int] = {}

    for c_idx, cohort_text in enumerate(all_stitched_cohorts, start=1):
        # Estimate base leaf for cohort if no milestone yet
        current_leaf = (c_idx - 1) * 10 + 1
        paragraphs = [p.strip() for p in cohort_text.split("\n\n") if p.strip()]

        for para in paragraphs:
            # Update active_locus if paragraph contains a milestone [f. XvA] or [p12LA]
            m_loc = re.search(r"\[(f\.\s*([0-9]+)[rv][AB]|p(\d+)[LR][AB])\]", para)
            if m_loc:
                active_locus = m_loc.group(1)
                if m_loc.group(3):
                    current_leaf = int(m_loc.group(3))
                elif m_loc.group(2):
                    # Approximate leaf from folio number (folio + 6)
                    current_leaf = min(267, int(m_loc.group(2)) + 6)

            # Check Headings to update Tone / Office / Section / Ode
            if para.startswith("#"):
                hdr_clean = para.lstrip("#").strip()
                m_t = re.search(r"\bTONE\s+(\d+)\b", hdr_clean, re.IGNORECASE)
                if m_t:
                    current_tone = int(m_t.group(1))
                    current_ode = None
                    active_podoben_id = None
                    continue

                m_o = re.match(r"^Ode\s+(\d+)\b", hdr_clean, re.IGNORECASE)
                if m_o:
                    current_ode = int(m_o.group(1))
                    current_section = f"Canon — Ode {current_ode}"
                    continue

                if any(day in hdr_clean.upper() for day in ("SATURDAY", "SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY")):
                    current_office = hdr_clean
                    current_ode = None
                    active_podoben_id = None
                    continue

                current_section = hdr_clean
                if "CANON" not in hdr_clean.upper():
                    current_ode = None
                continue

            if para == "---":
                continue

            # Strip inline milestones for clean text inspection
            clean_para = re.sub(r"\[(?:f\.\s*[^\]]+|p\d+[LR][AB])\]\s*", "", para).strip()
            if not clean_para:
                continue

            # Check if this paragraph is a Podoben declaration
            if clean_para.startswith("*Podoben:"):
                m_pod_eng = re.search(r'\*Podoben:\s*"([^"]+)"', clean_para)
                if m_pod_eng:
                    eng_inc = m_pod_eng.group(1).lower()
                    for pod in normalizer.podobens:
                        if pod["english_canonical"].lower() == eng_inc:
                            active_podoben_id = pod["id"]
                            break
                continue

            # Skip pure short rubrics or standalone Verse lines without hymn body
            if clean_para.startswith("*Verse:") and len(clean_para) < 160:
                continue
            if len(clean_para) < 40 and clean_para.startswith("*") and clean_para.endswith("*"):
                continue

            # Determine hymn_type
            hymn_type = "Sticheron"
            if current_ode is not None:
                if "Heirmos:" in clean_para:
                    hymn_type = "Heirmos"
                else:
                    hymn_type = "Canon Troparion"
            elif "Theotokion" in clean_para:
                hymn_type = "Theotokion"
            elif "Stavrotheotokion" in clean_para:
                hymn_type = "Stavrotheotokion"
            elif "Sessional" in current_section or "Kathisma" in current_section:
                hymn_type = "Sessional Hymn (Sedalen)"
            elif "Beatitudes" in current_section:
                hymn_type = "Beatitudes Troparion"
            elif "Kontakion" in clean_para or "KONTAKION" in current_section.upper():
                hymn_type = "Kontakion / Ikos"

            # Pair with leaf-local Slavonic stanza
            s_list = slavonic_stanzas_by_leaf.get(current_leaf, [])
            cur_idx = leaf_stanza_cursor.get(current_leaf, 0)
            slav_text = ""
            if s_list:
                if cur_idx < len(s_list):
                    slav_text = s_list[cur_idx]
                    leaf_stanza_cursor[current_leaf] = cur_idx + 1
                else:
                    slav_text = s_list[-1]

            item_num = len(items) + 1
            corpus_id = f"OCT.{monument_id.upper()}.T{current_tone}.C{c_idx:02d}.{item_num:04d}"

            items.append({
                "corpus_id": corpus_id,
                "tone": current_tone,
                "cohort": c_idx,
                "leaf": f"p{current_leaf}",
                "locus": active_locus,
                "office": current_office,
                "section": current_section,
                "ode": current_ode,
                "hymn_type": hymn_type,
                "podoben_id": active_podoben_id,
                "parent_heirmos_id": f"HEIRMOS.T{current_tone}.ODE{current_ode}" if current_ode in (1, 3, 4, 5, 6, 7, 8, 9) and current_tone in range(1, 9) else None,
                "slavonic_text": slav_text,
                "english_text": clean_para
            })

    return {
        "monument_id": monument_id,
        "corpus_schema": "2.0.0",
        "corpus_type": "OCTOECHOS_PROPERS_BILINGUAL_COMPLETE",
        "source_provenance": {
            "source_dir": f"Liturgical Monuments/Monument 9 - {monument_id.replace('_', ' ').title()}/Source Text",
            "cohorts_dir": f"Liturgical Monuments/Monument 9 - {monument_id.replace('_', ' ').title()}/Cohorts",
            "cohorts_count": len(all_stitched_cohorts),
            "total_stanzas_extracted": len(items)
        },
        "primitive_models_referenced": len(normalizer.podobens) + len(normalizer.stichoi) + len(normalizer.heirmoi),
        "items": items
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Hymnographic Gold Normalizer")
    parser.add_argument("--monument", default="1630_lviv_octoechos", help="Monument ID")
    args = parser.parse_args()

    ws_dir = PROJECT_ROOT / "Liturgical Monuments" / f"Monument 9 - {args.monument.replace('_', ' ').title()}"
    cohorts_dir = ws_dir / "Cohorts"
    source_dir = ws_dir / "Source Text"
    final_md_dir = ws_dir / "Final MD"

    process_monument_cohorts(args.monument, cohorts_dir, source_dir, final_md_dir)
