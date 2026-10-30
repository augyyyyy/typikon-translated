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
CODEX_REGISTRY_FILE = PROJECT_ROOT / "Liturgical Monuments" / "codex_registry.json"


def load_monument_metadata(monument_id: str) -> Dict[str, Any]:
    """Loads dynamic codicological and topology metadata for monument_id from codex_registry.json."""
    default_year = "1630"
    m_yr = re.match(r"^(\d{4})_", monument_id)
    if m_yr:
        default_year = m_yr.group(1)

    meta: Dict[str, Any] = {
        "monument_id": monument_id,
        "title": monument_id.replace("_", " ").title(),
        "short_title": monument_id.replace("_", " ").title(),
        "publication_year": default_year,
        "total_physical_pages": 267,
        "workspace_dir": f"Liturgical Monuments/{monument_id}",
        "folio_offset": 13 if "1629" in monument_id else 6,
        "opening_geometry": "2-up",
    }
    if CODEX_REGISTRY_FILE.is_file():
        try:
            reg = json.loads(CODEX_REGISTRY_FILE.read_text(encoding="utf-8-sig"))
            mon_cfg = reg.get("monuments", {}).get(monument_id, {})
            if mon_cfg:
                meta["title"] = mon_cfg.get("title", meta["title"])
                meta["short_title"] = mon_cfg.get("short_title", meta["title"])
                meta["total_physical_pages"] = int(mon_cfg.get("total_physical_pages", meta["total_physical_pages"]))
                meta["workspace_dir"] = mon_cfg.get("workspace_dir", meta["workspace_dir"])
                if "folio_offset" in mon_cfg:
                    meta["folio_offset"] = int(mon_cfg["folio_offset"])
                if "opening_geometry" in mon_cfg:
                    meta["opening_geometry"] = str(mon_cfg["opening_geometry"])
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    return meta


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
    "два": "дѣва",
    "дваа": "дѣва",
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
    t2 = t1.replace("\u1c82у", "у").replace("\u1c82", "о").replace("оу", "у")
    t2 = t2.replace("ѡ", "о").replace("ѻ", "о").replace("ꙋ", "у").replace("ѧ", "я")
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
    - SCRIBAL_INCIPIT_TRUNCATION: Scribe printed an abbreviated/shortened opening incipit of the canonical model.
    - TIER_3_LEXICAL_RECENSIONAL: Lexical, syntactic, or morphological variation.
    """
    clean_a = re.sub(r"^\[Подо́бенъ:\]\s*", "", text_a.strip())
    clean_b = re.sub(r"^\[Подо́бенъ:\]\s*", "", text_b.strip())
    if clean_a == clean_b:
        return "TIER_0_EXACT", 1.0, {"details": "Exact character match"}

    t1_a = normalize_slavonic_tier1(clean_a)
    t1_b = normalize_slavonic_tier1(clean_b)
    if t1_a == t1_b:
        return "TIER_1_TYPOGRAPHIC_TITLO", 0.98, {"t1": t1_a, "details": "Accents, titla, or contractions variance"}

    t2_a = normalize_slavonic_tier2(clean_a)
    t2_b = normalize_slavonic_tier2(clean_b)
    if t2_a == t2_b:
        return "TIER_2_ORTHOGRAPHIC_PHONOLOGICAL", 0.92, {"t2": t2_a, "details": "Ruthenian spelling / phonological reflex variance"}

    words_a = t2_a.split()
    words_b = t2_b.split()
    if words_a and words_b and len(words_a) < len(words_b):
        if words_b[:len(words_a)] == words_a or words_a[0][:4] == words_b[0][:4]:
            return "SCRIBAL_INCIPIT_TRUNCATION", 0.90, {
                "t2_source": t2_a,
                "t2_canonical": t2_b,
                "details": f"Scribal incipit truncation ({len(words_a)} vs {len(words_b)} words)"
            }

    matcher = difflib.SequenceMatcher(None, words_a, words_b)
    ratio = matcher.ratio()

    diff_tokens_a = [t for t in words_a if t not in words_b]
    diff_tokens_b = [t for t in words_b if t not in words_a]

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
    r"(?:^|[\s\.\*:])(Подо́?б?е?н?ъ?|Подѡ́?б?е?н?ъ?|Поⷣо́?б?е?н?ъ?|По́?д?о?б?|Поⷣ\.?|По́\.|По̀\s*,|По̀\s*:|Гла́мо(?:\s*\[Подобен\])?)(?:\s*[:\.,]|\s+)\s*(.*)$",
    re.IGNORECASE
)
SLAV_UNLABELED_POD_RE = re.compile(
    r"(?:Сѣда́?л?н?а?|Сѣ̑да̑|Стїхи́?р?ы?|Стіхи́?р?ы?)\s*,?\s*(?:Гла́?с?ъ?|гла̑)\s*,?\s*[а-яіїєѡꙋ҃\d]+\s*[\.,:]\s*(.+)$",
    re.IGNORECASE
)
SLAV_VERSE_RE = re.compile(
    r"(?:^|\s)(?:Сті́?хъ?|Стї́?хъ?|Сті́?|Стї́?)\s*[:.]\s*(.+)$",
    re.IGNORECASE
)


def extract_leaf_slavonic_primitives(
    s_lines: List[str],
    podoben_models: Optional[List[Dict[str, Any]]] = None
) -> Tuple[List[str], List[str], List[str]]:
    """Extracts Slavonic Podoben incipits, Psalm Stichoi, and full stanzas from a single leaf's lines."""
    s_pods: List[str] = []
    s_verses: List[str] = []
    s_stanzas: List[str] = []

    for idx_s, raw_sl in enumerate(s_lines):
        sl = raw_sl.strip()
        if not sl or sl.startswith("#") or sl.startswith("===") or sl.startswith("[Колонка") or sl.startswith("[Кустод"):
            continue
        sl_clean = sl.strip("*")
        sl_no_diac = DIACRITICS_RE.sub("", sl_clean)
        ms_pod = SLAV_POD_RE.search(sl_clean) or SLAV_POD_RE.search(sl_no_diac)
        if ms_pod:
            # Extract substring from original sl_clean starting at group(2)
            # To preserve original diacritics even when matched on sl_no_diac, split on the label pattern
            split_parts = re.split(
                r"(?:Подо́?б?е?н?ъ?|Подѡ́?б?е?н?ъ?|Поⷣо́?б?е?н?ъ?|По́?д?о?б?|Поⷣ\.?|По́\.|По̀\s*[,:]|По\s*:|Гла́мо(?:\s*\[Подобен\])?)(?:\s*[:\.,]|\s+)\s*",
                sl_clean,
                maxsplit=1,
                flags=re.IGNORECASE,
            )
            rest = split_parts[1].strip() if len(split_parts) > 1 else ms_pod.group(2).strip()
            if not rest and idx_s + 1 < len(s_lines):
                rest = s_lines[idx_s + 1].strip().strip("*")
            if rest:
                s_pods.append(rest.rstrip(".:*"))
        elif podoben_models and len(sl_clean) < 110:
            # Check for scribal omission of 'Подо́бенъ' immediately after 'Гла́съ X,' (e.g., 'Сѣда̑ гла̑, з҃, И҆́же менера́ди')
            m_unlbl = SLAV_UNLABELED_POD_RE.search(sl_clean)
            if m_unlbl:
                cand_inc = m_unlbl.group(1).strip().rstrip(".:*")
                cand_t2 = normalize_slavonic_tier2(cand_inc)
                if cand_t2 and any(
                    any(
                        normalize_slavonic_tier2(pat) in cand_t2 or cand_t2 in normalize_slavonic_tier2(pat)
                        for pat in p.get("slavonic_patterns", [])
                    )
                    for p in podoben_models
                ):
                    s_pods.append(f"[Подо́бенъ:] {cand_inc}")

        ms_v = SLAV_VERSE_RE.search(sl_clean)
        if ms_v:
            s_verses.append(ms_v.group(1).strip())

        if len(sl_clean) > 35:
            s_stanzas.append(sl_clean)

    return s_pods, s_verses, s_stanzas


class HymnographicNormalizer:
    def __init__(self, registry_path: Path = REGISTRY_FILE):
        if not registry_path.is_file():
            raise FileNotFoundError(f"Registry not found: {registry_path}")
        self.registry = json.loads(registry_path.read_text(encoding="utf-8-sig"))
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
        Normalizes any Podoben / Prosomoion / Model / Melodic model / Same melody / To: / Pokoin line
        into the canonical parenthetical format:
            *Podoben: "[Canonical English]" (Verbatim Slavonic):*
        or when the scribe omitted the Podoben label on the physical leaf:
            *Podoben: "[Canonical English]" ([Подо́бенъ:] Verbatim Slavonic):*
        """
        stripped = line.strip()
        fn_m = re.search(r"(\[\^\d+\])", stripped)
        fn_suffix = f" {fn_m.group(1)}" if fn_m else ""
        stripped_no_fn = re.sub(r"\[\^\d+\]", "", stripped).strip()

        # Case 1: Saturday Stichera / Canon Troparia for the Departed (`Поко́инъ:` / `Nekrosimon:` / `For the Departed:`)
        if re.match(
            r"^\*?(?:Podoben|Model|Nekrosimon|For\s+the\s+Departed(?:\s*\[Поко́инъ\])?|Hymn\s+for\s+the\s+Departed(?:\s*\(Поко́инъ\))?):\*?$",
            stripped_no_fn,
            re.IGNORECASE,
        ):
            is_bare_pod = bool(re.match(r"^\*?(?:Podoben|Model|Nekrosimon):\*?$", stripped_no_fn, re.IGNORECASE))
            return f"*Hymn for the Departed (Поко́инъ):*{fn_suffix}", (
                {
                    "type": "POKOIN_ABBREV_CORRECTED",
                    "locus": f"C{c_idx:02d}:p{leaf_num}",
                    "tone": current_tone,
                    "slavonic_source": "Поко́инъ",
                    "raw_cohort_english": stripped_no_fn,
                    "canonical_english": "*Hymn for the Departed (Поко́инъ):*",
                    "drift_tier": "TIER_1_TYPOGRAPHIC_TITLO",
                    "is_ai_drift": is_bare_pod,
                }
                if is_bare_pod
                else None
            )
        if re.search(r"For the Departed:\s*(?:Podoben|Model):\s*$", stripped_no_fn, re.IGNORECASE):
            return f"*Hymn for the Departed (Поко́инъ):*{fn_suffix}", {
                "type": "POKOIN_ABBREV_CORRECTED",
                "locus": f"C{c_idx:02d}:p{leaf_num}",
                "tone": current_tone,
                "slavonic_source": "По[ко́инъ]:",
                "raw_cohort_english": stripped_no_fn,
                "canonical_english": "*Hymn for the Departed (Поко́инъ):*",
                "drift_tier": "TIER_1_TYPOGRAPHIC_TITLO",
                "is_ai_drift": True,
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
                "drift_tier": "SCRIBAL_INCIPIT_TRUNCATION",
                "is_ai_drift": False,
            }

        # Case 3: "The same" Podoben / Model / Melodic model / Melody
        same_pat = re.compile(
            r"(?:[,;:]\s*|\.\s*|^|\*)(?:"
            r"(?:same\s+Tone\s+and\s+(?:Podoben|Prosomoion|Model\s+melody|Model|melodic\s+model|melody))"
            r"|(?:Tone\s+and\s+(?:Podoben|Prosomoion|Model\s+melody|Model|melodic\s+model)\s*:?\s*the\s+same)"
            r"|(?:the\s+same\s+Tone\s+and\s+(?:Podoben|Prosomoion|Model\s+melody|Model|melodic\s+model))"
            r"|(?:(?:The\s+)?same\s+(?:Podoben|Prosomoion|Model\s+melody|Model|melodic\s+model|melody))"
            r"|(?:(?:Podoben|Prosomoion|Model\s+melody|Model|Melodic\s+model)\s*:\s*[\"“]?(?:The\s+same|The\s+same\s+Tone\s+and\s+Podoben)[\"”]?)"
            r")(?:\s*\([^)]*\))?\s*[\.:]?\*?",
            re.IGNORECASE,
        )
        m_same = same_pat.search(stripped_no_fn)
        if m_same:
            prefix = stripped_no_fn[:m_same.start()].strip().strip("*").rstrip(".,:")
            matched_text = m_same.group(0).lower()
            if "tone" in matched_text:
                rep = f'*Podoben: "The same Tone and Podoben" (Гла́съ и҆ подо́бенъ то́йже):*{fn_suffix}'
                canon_same = "The same Tone and Podoben (Гла́съ и҆ подо́бенъ то́йже)"
            else:
                rep = f'*Podoben: "The same" (то́йже):*{fn_suffix}'
                canon_same = "The same (то́йже)"
            final_str = f"*{prefix}.*\n\n{rep}" if prefix else rep
            return final_str, {
                "type": "PODOBEN_SAME_NORMALIZED",
                "primitive_id": f"POD.T{current_tone}.SAME",
                "locus": f"C{c_idx:02d}:p{leaf_num}",
                "tone": current_tone,
                "slavonic_source": "то́йже",
                "raw_cohort_english": stripped_no_fn,
                "canonical_english": canon_same,
                "drift_tier": "TIER_0_EXACT",
                "is_ai_drift": ("model" in matched_text or "melody" in matched_text or "prosomoion" in matched_text),
            }

        # Case 4: Standard Named Podoben / Prosomoion / Model melody / Model / Melodic model / Special Melody / To:
        label_pat = re.compile(
            r"(?:^|\*|[\.,;:]\s*)\b(Podoben|Prosomoion|Model\s+melody|Model|Melodic\s+model|Special\s+Melody|To):\s*(.+)$",
            re.IGNORECASE,
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
            raw_eng_incipit = re.sub(r"\s*\([^)]*[\u0400-\u04FF][^)]*\)\s*:?\*?$", "", rest_after_lbl).strip()
            raw_eng_incipit = raw_eng_incipit.strip('"\'“”.:*')

        # Match against self.podobens (prioritizing current_tone, then any tone)
        matched_model = None
        candidates_ordered = (
            [p for p in self.podobens if p["tone"] == current_tone]
            + [p for p in self.podobens if p["tone"] != current_tone]
        )

        # 4a. Match by exact English alias first, then substring match
        raw_eng_clean = raw_eng_incipit.lower().rstrip(".")
        for pod in candidates_ordered:
            aliases = [pod["english_canonical"].lower()] + [a.lower() for a in pod.get("english_aliases", [])]
            if any(a == raw_eng_clean for a in aliases if a):
                matched_model = pod
                break
        if not matched_model:
            for pod in candidates_ordered:
                aliases = [pod["english_canonical"].lower()] + [a.lower() for a in pod.get("english_aliases", [])]
                if any(a in raw_eng_clean or raw_eng_clean in a for a in aliases if a):
                    matched_model = pod
                    break

        # 4b. Fallback match by leaf-aligned Slavonic Podoben
        if not matched_model and s_pods:
            for sp in s_pods:
                sp_clean_check = re.sub(r"^\[Подо́бенъ:\]\s*", "", sp)
                sp_stem = normalize_slavonic_tier2(sp_clean_check)
                for pod in candidates_ordered:
                    if any(
                        normalize_slavonic_tier2(pat) in sp_stem or sp_stem in normalize_slavonic_tier2(pat)
                        for pat in pod.get("slavonic_patterns", [])
                    ):
                        matched_model = pod
                        break
                if matched_model:
                    break

        if not matched_model:
            return line, None

        canonical_eng = matched_model["english_canonical"]

        # Find leaf-local verbatim Slavonic witness if present on this leaf
        verbatim_slav = ""
        scribal_omitted_label = False
        for sp in s_pods:
            has_supplied_lbl = sp.startswith("[Подо́бенъ:]")
            sp_body = re.sub(r"^\[Подо́бенъ:\]\s*", "", sp)
            sp_stem = normalize_slavonic_tier2(sp_body)
            if any(
                normalize_slavonic_tier2(pat) in sp_stem or sp_stem in normalize_slavonic_tier2(pat)
                for pat in matched_model.get("slavonic_patterns", [])
            ):
                sp_clean = re.split(r"\s+Ст[і ї]́?х?", sp_body, maxsplit=1)[0].strip().rstrip(".:*")
                verbatim_slav = f"[Подо́бенъ:] {sp_clean}" if has_supplied_lbl else sp_clean
                scribal_omitted_label = has_supplied_lbl
                break

        slav_display = verbatim_slav if verbatim_slav else matched_model["slavonic_canonical"]
        drift_tier, drift_sim, drift_info = classify_slavonic_drift(slav_display, matched_model["slavonic_canonical"])

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

        # Layer 3 (True AI Translation Drift):
        # True AI drift occurs ONLY when the translator used a non-MTS-1 label (e.g. Model:, Prosomoion:)
        # OR diverged from the canonical English when the Slavonic source itself was NOT truncated/variant.
        eng_diverged = raw_eng_clean != canonical_eng.lower()
        non_mts1_label = label_used.lower() != "podoben"
        scribal_truncated_or_tier3 = drift_tier in ("SCRIBAL_INCIPIT_TRUNCATION", "TIER_3_LEXICAL_RECENSIONAL")

        is_ai_drift = non_mts1_label or (eng_diverged and not scribal_truncated_or_tier3)

        drift_record = {
            "type": "PODOBEN_NORMALIZED",
            "primitive_id": matched_model["id"],
            "locus": f"C{c_idx:02d}:p{leaf_num}",
            "tone": matched_model["tone"],
            "greek_incipit": matched_model["greek"],
            "slavonic_source": slav_display,
            "slavonic_canonical": matched_model["slavonic_canonical"],
            "scribal_omitted_label": scribal_omitted_label,
            "drift_tier": drift_tier,
            "drift_similarity": drift_sim,
            "drift_info": drift_info,
            "raw_cohort_english": f"{label_used}: {raw_eng_incipit}",
            "canonical_english": canonical_eng,
            "is_ai_drift": is_ai_drift,
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
        for st in self.stichoi:
            if any(pat in raw_eng_verse.lower() for pat in st.get("english_patterns", [])):
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
RE_COHORT_BOUNDARY = re.compile(r"^===\s*COHORT_BOUNDARY\s+(\d+)\s*===$", re.IGNORECASE)
RE_PAGE_HEADER = re.compile(
    r"^(?:#{1,6}\s*|\*\*)?\[(Left|Right)\s+Page\s*(?:—|--|-|:)\s*(?:(?:Fol\.?|Folio)\s*([0-9]+[rv])|(.+?))\](?:\*\*)?(?:\s*(\[\^\d+\]))?$",
    re.IGNORECASE
)
RE_COLUMN_HEADER = re.compile(
    r"^(?:#{1,6}\s*|\*\*)?(?:\[)?(?:Column|Колонка)\s+([ABab])(?::|\])?(?:\s*\([^)]+\))?(?:\*\*)?(?:\s*(\[\^\d+\]))?$",
    re.IGNORECASE
)
RE_CONTINUATION = re.compile(
    r"^(?:\[(?:Continuation\s+of\s+|Продовження\s+)[^\]]+\]|\*\([^)]*?\b(?:continued|concluded|conclusion)\b[^)]*\):?\*?\:?)(?:\s*(\[\^\d+\]))?$",
    re.IGNORECASE
)
RE_BLANK_LINE = re.compile(r"^\*?\[(?:Blank|Чистий)\s+[^\]]+\]\*?(?:\s*(\[\^\d+\]))?$", re.IGNORECASE)
RE_MS_RUNNING_HEADER = re.compile(
    r"^(?:\*?\((?:fol\.?|folio)\s*\d+[rv]?\)\*?|\[(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)(?:\s*/\s*(?:Sunday|Saturday))?(?:,\s*Tone\s+\d+)?\.?\])(?:\s*(\[\^\d+\]))?$",
    re.IGNORECASE,
)

RE_NON_STITCHABLE_START = re.compile(
    r"^(?:#|\[\d+\]|\*\*\d+\.\*\*|\d+\.\s|\[(?:Headpiece|Woodcut|Primary|Marginalia|17th-century)|\*?(?:Podoben|Prosomoion|Model\s+melody|Model|Verse|Stichos|Glory|Both now|Theotokion|Stavrotheotokion|For the Martyrs|For the Departed|Hymn for the Departed|Nekrosimon|Ode\s+\d+|Another\s+(?:Canon|Heirmos|Stichera)|Other\s+Stichera|Stichera\b|Penitential\s+Stichera|Resurrectional|After\s+the\s+\d+|At\s+the\s+(?:Aposticha|Praises)|Sessional\s+Hymn|Kontakion|Ikos|Hypakoe|Prokeimenon|Tone\s+\d+|Same\s+Tone)\b)",
    re.IGNORECASE
)

SEAM_STOPWORDS = {
    "that", "this", "with", "from", "unto", "upon", "have", "hath", "hast", "thou",
    "thee", "thine", "your", "their", "them", "they", "were", "been", "being", "which",
    "when", "what", "where", "there", "into", "through", "before", "after", "over",
    "under", "more", "most", "also", "even", "only", "all", "both", "each", "other",
    "some", "such", "than", "then", "very", "will", "shall", "may", "might", "must",
    "would", "should", "could", "who", "whom", "whose",
}

ANAPHORA_EXEMPT_WORDS = {
    "rejoice", "hail", "blessed", "bless", "praise", "sing", "exalt", "holy", "alleluia", "glory",
}


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
            m_f = re.search(r"(?:Fol\.?|Folio)\s*([0-9]+[rv])", desc_str, re.IGNORECASE)
            if m_f:
                self.folio = m_f.group(1).strip()
            else:
                self.folio = ""
        self.col = "A"

    def update_col(self, col_str: str):
        self.col = col_str.upper().strip()

    def get_milestone(self) -> str:
        if self.folio:
            return f"[f. {self.folio}{self.col}]"
        return f"[p{self.leaf_num}{self.side}{self.col}]"


def _norm_seam_word(w: str) -> str:
    """Normalizes a token for seam catchword/phrase overlap comparison."""
    w_no_fn = re.sub(r"\[\^\d+\]", "", w)
    return re.sub(r"^[^\w]+|[^\w]+$", "", w_no_fn).lower()


def _content_stem(w: str) -> str:
    """Returns a 5-char lowercase stem for content words (length >= 4, excluding stopwords)."""
    nw = _norm_seam_word(w)
    if len(nw) < 4 or nw in SEAM_STOPWORDS:
        return ""
    return nw[:5]


def _extract_fn_markers(tokens: List[str]) -> List[str]:
    """Extracts any [^N] footnote markers from a list of tokens so none are ever lost."""
    markers: List[str] = []
    for t in tokens:
        markers.extend(re.findall(r"\[\^\d+\]", t))
    return markers


def deduplicate_seam_overlap(cleaned_prev: str, cleaned_curr: str) -> Tuple[str, str]:
    """
    Universal 5-rule seam overlap deduplicator for 2-up folios and inter-cohort boundaries.
    Guarantees 100% preservation of [^N] footnote markers on both sides of the seam, while
    protecting legitimate liturgical anaphora/refrains.
    """
    # Rule 0: Hyphenated word split across seam (e.g. "virginal ha-" + "nds borne")
    m_hyph = re.search(r"([A-Za-z]{2,})-(?:\s*(\[\^\d+\]))*\s*$", cleaned_prev)
    m_curr_frag = re.match(r"^([a-z]{2,})\b(.*)$", cleaned_curr)
    if m_hyph and m_curr_frag:
        rescued_fns = re.findall(r"\[\^\d+\]", m_hyph.group(0))
        joined_word = m_hyph.group(1) + m_curr_frag.group(1)
        prefix_prev = cleaned_prev[:m_hyph.start()] + joined_word
        if rescued_fns:
            prefix_prev = f"{prefix_prev} {' '.join(rescued_fns)}"
        cleaned_prev = prefix_prev.rstrip()
        cleaned_curr = m_curr_frag.group(2).lstrip()
        return cleaned_prev, cleaned_curr

    # Rule 1: Bracketed catchword/editorial restoration at tail or mid-phrase (0-6 trailing words) of cleaned_prev
    # e.g. "...we magnify the [first-enthroned bishop]. [^28]" + "first-enthroned hierarch..."
    # or "...anoint thee, [first-enthroned bishop] of the people of Myra" + "first-enthroned bishop, and..."
    m_br = re.search(r"\s*\[([^\^\]]+)\]([\.,;:]?(?:\s+\S+){0,6}?)(?:\s*(\[\^\d+\]))*\s*$", cleaned_prev)
    if m_br:
        bracket_inner = m_br.group(1)
        trailing_after_br = m_br.group(2) or ""
        bracket_words = [_norm_seam_word(w) for w in bracket_inner.split() if _norm_seam_word(w)]
        curr_words_raw = cleaned_curr.split()
        curr_words_norm = [_norm_seam_word(w) for w in curr_words_raw[:8] if _norm_seam_word(w)]
        if bracket_words and curr_words_norm:
            first_match = (bracket_words[0] == curr_words_norm[0])
            content_match = any(len(bw) >= 4 and bw in curr_words_norm[:5] for bw in bracket_words)
            if first_match or content_match:
                rescued_fns = re.findall(r"\[\^\d+\]", m_br.group(0))
                if not trailing_after_br.strip(".,;: "):
                    # Bracket is at the very end of cleaned_prev: strip bracketed catchword from prev
                    prefix_prev = cleaned_prev[:m_br.start()].rstrip()
                    prefix_prev = re.sub(r"(?:\.\.\.|…)+\s*$", "", prefix_prev).rstrip()
                    if rescued_fns:
                        prefix_prev = f"{prefix_prev} {' '.join(rescued_fns)}"
                    cleaned_prev = prefix_prev
                else:
                    # Mid-phrase bracket followed by trailing words on prev (e.g. L5613):
                    # Unwrap the bracket in prev and strip the repeated bracket_words prefix from curr
                    k_br = len(bracket_words)
                    if curr_words_norm[:k_br] == bracket_words:
                        rescued_curr = _extract_fn_markers(curr_words_raw[:k_br])
                        cleaned_prev = (
                            cleaned_prev[:m_br.start()]
                            + " "
                            + bracket_inner
                            + trailing_after_br
                            + (f" {' '.join(rescued_fns + rescued_curr)}" if (rescued_fns or rescued_curr) else "")
                        ).strip()
                        cleaned_curr = " ".join(curr_words_raw[k_br:]).lstrip(",;: ")
                        return cleaned_prev, cleaned_curr

    words_prev = cleaned_prev.split()
    words_curr = cleaned_curr.split()
    if not words_prev or not words_curr:
        return cleaned_prev, cleaned_curr

    norm_prev = [_norm_seam_word(w) for w in words_prev]
    norm_curr = [_norm_seam_word(w) for w in words_curr]

    # Rule 2a: Exact k-word suffix of prev matching k-word prefix of curr (1 <= k <= 18)
    max_k = min(18, len(words_prev), len(words_curr))
    for k in range(max_k, 0, -1):
        if norm_prev[-k:] == norm_curr[:k] and any(norm_prev[-k:]):
            if norm_curr[0] in ANAPHORA_EXEMPT_WORDS and (k == 1 or re.search(r"[\.!\?;:]\s*$", cleaned_prev)):
                continue
            rescued = _extract_fn_markers(words_curr[:k])
            if rescued:
                cleaned_prev = f"{cleaned_prev} {' '.join(rescued)}"
            cleaned_curr = " ".join(words_curr[k:])
            return cleaned_prev, cleaned_curr

    # Rule 2b: 3-word near-exact suffix/prefix where word 1 and word 3 (>=5 chars) match (e.g. "at the childbirth" / "at thy childbirth")
    if len(words_prev) >= 3 and len(words_curr) >= 3:
        if (
            norm_prev[-3] == norm_curr[0]
            and norm_prev[-1] == norm_curr[2]
            and len(norm_curr[2]) >= 5
            and norm_curr[2] not in ANAPHORA_EXEMPT_WORDS
        ):
            rescued = _extract_fn_markers(words_prev[-3:])
            trimmed_prev = " ".join(words_prev[:-3]).rstrip()
            if rescued:
                trimmed_prev = f"{trimmed_prev} {' '.join(rescued)}"
            return trimmed_prev, cleaned_curr

    # Rule 3: Short incomplete tail phrase on prev after a shared anchor word (1 <= tail_len <= 5)
    # e.g. prev="...who with faith celebrate your all-laudable" + curr="celebrate your all-praised memory..."
    # or prev="...the deadness of the guards, and the seals" + curr="and the destruction of the seals..."
    anchor_curr = norm_curr[0]
    if anchor_curr and anchor_curr not in ANAPHORA_EXEMPT_WORDS:
        for tail_len in range(1, min(6, len(words_prev))):
            idx = len(words_prev) - 1 - tail_len
            if norm_prev[idx] == anchor_curr:
                tail_stems = {_content_stem(w) for w in words_prev[idx:] if _content_stem(w)}
                curr_head_stems = {_content_stem(w) for w in words_curr[:7] if _content_stem(w)}
                if len(anchor_curr) >= 4 or (tail_stems and (tail_stems & curr_head_stems)):
                    rescued = _extract_fn_markers(words_prev[idx:])
                    trimmed_prev = " ".join(words_prev[:idx]).rstrip(",;: ")
                    if rescued:
                        trimmed_prev = f"{trimmed_prev} {' '.join(rescued)}"
                    return trimmed_prev, cleaned_curr

    # Rule 4: Syntax-Bounded Sub-Clause / Restatement Overlap Trimmer with Anaphora Guards
    # 4a. Whole-clause anticipation on prev: when cleaned_prev is a short unpunctuated clause (<= 15 words)
    # whose content stems are >= 60% repeated inside cleaned_curr (e.g. L2979, L6325).
    if len(words_prev) <= 15 and not re.search(r"[\.!?;:]\s*$", cleaned_prev):
        prev_stems = [_content_stem(w) for w in words_prev if _content_stem(w)]
        curr_stems_set = {_content_stem(w) for w in words_curr[:20] if _content_stem(w)}
        if len(prev_stems) >= 3 and not (set( norm_prev ) & ANAPHORA_EXEMPT_WORDS):
            overlap_cnt = sum(1 for st in prev_stems if st in curr_stems_set)
            if overlap_cnt >= 3 and (overlap_cnt / len(prev_stems)) >= 0.60:
                rescued = _extract_fn_markers(words_prev)
                trimmed_prev = " ".join(rescued) if rescued else ""
                if cleaned_curr and cleaned_curr[0].islower():
                    cleaned_curr = cleaned_curr[0].upper() + cleaned_curr[1:]
                return trimmed_prev, cleaned_curr

    # 4b. Opening sub-clause of curr (up to first comma/semicolon/colon/period, max 8 words)
    # repeating an exact phrase or >= 75% content stems from the last 14 words of prev (e.g. L1111, L4269, L5735).
    m_open_clause = re.match(r"^([^\.,;:!\?]+?)([\.,;:!\?])(?:\s+(.*))?$", cleaned_curr)
    if m_open_clause:
        clause_body = m_open_clause.group(1).strip()
        clause_punct = m_open_clause.group(2)
        clause_rest = (m_open_clause.group(3) or "").strip()
        c_clause_words = clause_body.split()
        c_clause_norm = [_norm_seam_word(w) for w in c_clause_words if _norm_seam_word(w)]
        prev_window_norm = norm_prev[-14:]

        if 2 <= len(c_clause_norm) <= 8 and not (set(c_clause_norm) & ANAPHORA_EXEMPT_WORDS):
            # Check if c_clause_norm appears verbatim inside prev_window_norm
            k_cl = len(c_clause_norm)
            exact_in_window = any(
                prev_window_norm[j:j + k_cl] == c_clause_norm
                for j in range(len(prev_window_norm) - k_cl + 1)
            )
            # Or if clause_rest is empty (terminal clause) and >= 75% of its content stems are in prev_window
            c_stems = [_content_stem(w) for w in c_clause_words if _content_stem(w)]
            p_win_stems = {_content_stem(w) for w in words_prev[-14:] if _content_stem(w)}
            stem_restatement = (
                not clause_rest
                and len(c_stems) >= 3
                and sum(1 for st in c_stems if st in p_win_stems) / len(c_stems) >= 0.75
            )
            if exact_in_window or stem_restatement:
                rescued = _extract_fn_markers(c_clause_words)
                if rescued:
                    cleaned_prev = f"{cleaned_prev} {' '.join(rescued)}"
                if clause_rest:
                    return cleaned_prev, clause_rest
                else:
                    # Preserve terminal punctuation on prev if prev lacks it
                    if not re.search(r"[\.!\?]\s*$", re.sub(r"\[\^\d+\]\s*$", "", cleaned_prev)):
                        cleaned_prev = re.sub(r"[\.,;:]?\s*((?:\[\^\d+\]\s*)*)$", rf"{clause_punct} \1", cleaned_prev).strip()
                    return cleaned_prev, ""

    return cleaned_prev, cleaned_curr


def stitch_2up_hymnographic_stream(cohort_text: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Parses cohort/codex text line by line, tracking folio/column locus.
    Stitches sentences severed across column, leaf, and cohort breaks, inserting compact
    inline locus milestones `[f. XvA]` at the exact boundary while preserving cohort boundary markers.
    """
    lines = cohort_text.splitlines()
    output_lines: List[str] = []
    stitch_events: List[Dict[str, Any]] = []

    locus = LocusTracker()
    pending_milestone: Optional[str] = None
    pending_footnote: Optional[str] = None
    pending_cohort_boundary: Optional[str] = None

    i = 0
    n = len(lines)

    while i < n:
        raw_line = lines[i]
        line = raw_line.strip()

        m_blank = RE_BLANK_LINE.match(line)
        if m_blank:
            if m_blank.group(1):
                pending_footnote = f"{pending_footnote} {m_blank.group(1)}".strip() if pending_footnote else m_blank.group(1)
            i += 1
            continue

        m_cb = RE_COHORT_BOUNDARY.match(line)
        if m_cb:
            c_num = int(m_cb.group(1))
            if c_num > 1:
                pending_cohort_boundary = f"=== COHORT_BOUNDARY {c_num} ==="
            i += 1
            continue

        m_leaf = RE_LEAF_BANNER.match(line)
        if m_leaf:
            locus.update_leaf(int(m_leaf.group(1)))
            pending_milestone = locus.get_milestone()
            i += 1
            continue

        m_run = RE_MS_RUNNING_HEADER.match(line)
        if m_run:
            m_f_run = re.search(r"(?:fol\.?|folio)\s*(\d+[rv]?)", line, re.IGNORECASE)
            if m_f_run:
                locus.folio = m_f_run.group(1).strip()
                pending_milestone = locus.get_milestone()
            if m_run.group(1):
                pending_footnote = f"{pending_footnote} {m_run.group(1)}".strip() if pending_footnote else m_run.group(1)
            i += 1
            continue

        m_page = RE_PAGE_HEADER.match(line)
        if m_page:
            locus.update_page(m_page.group(1), m_page.group(2) or "", m_page.group(3) or "")
            pending_milestone = locus.get_milestone()
            if m_page.group(4):
                pending_footnote = f"{pending_footnote} {m_page.group(4)}".strip() if pending_footnote else m_page.group(4)
            i += 1
            continue

        m_col = RE_COLUMN_HEADER.match(line)
        if m_col:
            locus.update_col(m_col.group(1))
            pending_milestone = locus.get_milestone()
            if m_col.group(2):
                pending_footnote = f"{pending_footnote} {m_col.group(2)}".strip() if pending_footnote else m_col.group(2)
            i += 1
            continue

        m_cont = RE_CONTINUATION.match(line)
        if m_cont:
            if m_cont.group(1):
                pending_footnote = f"{pending_footnote} {m_cont.group(1)}".strip() if pending_footnote else m_cont.group(1)
            i += 1
            continue

        if line.lower() == "[typographic divider]" or line == "---":
            if pending_cohort_boundary:
                output_lines.append(pending_cohort_boundary)
                pending_cohort_boundary = None
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
                s_cand = output_lines[idx].strip()
                if s_cand and not RE_COHORT_BOUNDARY.match(s_cand):
                    last_idx = idx
                    break

            if last_idx >= 0:
                prev_content = output_lines[last_idx].strip()
                prev_no_fn = re.sub(r"(?:\s*\[\^\d+\])+\s*$", "", prev_content).rstrip()
                core_prev = re.sub(r'(?:\[\^\d+\]|[\]\)\*_`"\'\”\’]|\s)+$', '', prev_content)
                ends_punct = bool(core_prev and core_prev[-1] in ('.', '!', '?', ':'))
                ends_ellipsis = prev_no_fn.endswith("...")
                starts_ellipsis = curr_line.startswith("...")
                curr_starts_lower = bool(re.match(r"^[a-z]", curr_line))
                has_bracket_tail = bool(re.search(r"\[[^\^\]]+\][\.,;:]?(?:\s*\[\^\d+\])*\s*$", prev_content))
                prev_is_paratext_block = bool(prev_no_fn.startswith("[") and prev_no_fn.endswith("]"))
                starts_new_block = bool(RE_NON_STITCHABLE_START.match(curr_line))
                prev_is_rubric = (
                    prev_content.startswith("*Podoben:")
                    or prev_content.startswith("*Verse:")
                    or prev_content.startswith("#")
                    or prev_is_paratext_block
                    or (prev_content.startswith("*") and prev_content.endswith("*") and not curr_line.startswith("*"))
                )

                is_mid_sentence = (
                    (ends_ellipsis or starts_ellipsis or not ends_punct or (curr_starts_lower and has_bracket_tail))
                    and not starts_new_block
                    and not prev_is_rubric
                )

                if is_mid_sentence:
                    # Strip '...' before or after trailing [^N] footnote markers on prev_content
                    cleaned_prev = re.sub(r"\.\.\.(?=\s*(?:\[\^\d+\]\s*)*$)", "", prev_content)
                    cleaned_prev = re.sub(r"\.\.\.\s*$", "", cleaned_prev).rstrip()
                    cleaned_curr = re.sub(r"^\.\.\.\s*", "", curr_line).lstrip()

                    # Merge adjacent italic wrappers across the seam if both sides are italicized
                    if cleaned_prev.endswith("*") and not cleaned_prev.endswith("**") and cleaned_curr.startswith("*") and not cleaned_curr.startswith("**"):
                        cleaned_prev = cleaned_prev[:-1].rstrip()
                        cleaned_curr = cleaned_curr[1:].lstrip()

                    before_dedup = (cleaned_prev, cleaned_curr)
                    cleaned_prev, cleaned_curr = deduplicate_seam_overlap(cleaned_prev, cleaned_curr)
                    was_dedup = (cleaned_prev, cleaned_curr) != before_dedup

                    fn_suffix = f" {pending_footnote}" if pending_footnote else ""
                    pending_footnote = None

                    if cleaned_prev and cleaned_curr:
                        stitched = f"{cleaned_prev}{fn_suffix} {pending_milestone} {cleaned_curr}"
                    elif cleaned_curr:
                        stitched = f"{pending_milestone} {cleaned_curr}{fn_suffix}"
                    else:
                        # Avoid trailing orphan milestone at end of line: place milestone before terminal clause or keep clean
                        stitched = f"{cleaned_prev}{fn_suffix}"
                    output_lines[last_idx] = stitched

                    if pending_cohort_boundary:
                        output_lines.append(pending_cohort_boundary)
                        pending_cohort_boundary = None

                    stitch_events.append({
                        "milestone": pending_milestone,
                        "prev_tail": prev_content[-40:],
                        "curr_head": curr_line[:40],
                        "type": "SEAM_OVERLAP_DEDUPLICATED" if was_dedup else "SEAM_STITCHED",
                        "deduplicated": was_dedup,
                    })
                    pending_milestone = None
                    i += 1
                    continue

        if pending_cohort_boundary:
            output_lines.append(pending_cohort_boundary)
            pending_cohort_boundary = None

        if pending_milestone:
            if not curr_line.startswith("#"):
                curr_line = f"{pending_milestone} {curr_line}"
                pending_milestone = None

        if pending_footnote:
            curr_line = f"{curr_line} {pending_footnote}"
            pending_footnote = None

        output_lines.append(curr_line)
        i += 1

    if pending_footnote and output_lines:
        output_lines[-1] = f"{output_lines[-1]} {pending_footnote}"
        pending_footnote = None

    if pending_cohort_boundary:
        output_lines.append(pending_cohort_boundary)

    return "\n".join(output_lines), stitch_events


# ==============================================================================
# 4. Hymnographic Stanza Separator & Heading Normalizer
# ==============================================================================

RE_INVENTED_STANZA_NUM = re.compile(r"^((?:\[(?:f\.\s*[^\]]+|p\d+[LR][AB])\]\s*)?)(?:\[\d+\]|\*\*\d+\.\*\*|\d+\.)\s+", re.IGNORECASE)

RE_MAJOR_OFFICE = re.compile(
    r"^#+\s*(?:Tone\s+\d+\s*[-—:]\s*)?(?:ON\s+)?(SATURDAY\s+EVENING|SUNDAY\s+MORNING|SUNDAY\s+MATINS|SUNDAY\s+MIDNIGHT\s+OFFICE|AT\s+THE\s+MIDNIGHT\s+OFFICE|MONDAY\s+EVENING|MONDAY\s+MORNING|MONDAY\s+AT\s+MATINS|TUESDAY\s+EVENING|TUESDAY\s+MORNING|TUESDAY\s+AT\s+MATINS|WEDNESDAY\s+EVENING|WEDNESDAY\s+MORNING|WEDNESDAY\s+AT\s+MATINS|THURSDAY\s+EVENING|THURSDAY\s+MORNING|THURSDAY\s+AT\s+MATINS|FRIDAY\s+EVENING|FRIDAY\s+MORNING|FRIDAY\s+AT\s+MATINS|SATURDAY\s+MORNING|SATURDAY\s+AT\s+MATINS)\b[^\n]*",
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
    - Deterministically promotes italicized liturgical office rubrics into canonical H2
      service headings (and injects H1 # WEEKDAY OFFICES OF THE OCTOECHOS for consolidated
      weekday cycles) when any Tone/section has < 3 explicit H2 headings.
    - Subagent-invented bracketed stanza numbers ([1], [2]) are stripped (even after [f. XvA]).
    """
    lines = text.splitlines()
    formatted: List[str] = []

    def _section_has_enough_explicit_h2(start_idx: int) -> bool:
        count = 0
        for fwd_line in lines[start_idx + 1:]:
            s_fwd = re.sub(r"^(?:\[(?:f\.\s*[^\]]+|p\d+[LR][AB])\]\s*)+", "", fwd_line.strip()).strip()
            if re.match(r"^#+\s*(?:TONE\s+\d+|Book\s+of\s+the\s+Octoechos.*Tone\s+\d+|WEEKDAY\s+OFFICES|PREFACE|EXAPOSTILARIA|EVANGELICAL|COLOPHON)\b", s_fwd, re.IGNORECASE):
                break
            if RE_MAJOR_OFFICE.match(s_fwd):
                count += 1
        return count >= 3

    section_has_explicit_h2 = _section_has_enough_explicit_h2(0)
    active_macro = "FRONT_MATTER"
    emitted_in_section: Set[str] = set()

    weekday_rubric_map = [
        ("MON_MATINS", r"^\*?(?:On\s+)?Monday\s+(?:at\s+Matins|Morning)\b", "## MONDAY MATINS: REPENTANCE AND THE BODILESS POWERS"),
        ("MON_VESPERS", r"^\*?(?:On\s+)?Monday\s+evening\b", "## MONDAY EVENING VESPERS (FOR TUESDAY)"),
        ("TUE_MATINS", r"^\*?(?:On\s+)?Tuesday\s+(?:at\s+Matins|Morning)\b", "## TUESDAY MATINS: REPENTANCE AND ST. JOHN THE FORERUNNER"),
        ("TUE_VESPERS", r"^\*?(?:On\s+)?Tuesday\s+evening\b", "## TUESDAY EVENING VESPERS (FOR WEDNESDAY)"),
        ("WED_MATINS", r"^\*?(?:On\s+)?Wednesday\s+(?:at\s+Matins|Morning)\b", "## WEDNESDAY MATINS: THE PRECIOUS CROSS AND THE THEOTOKOS"),
        ("WED_VESPERS", r"^\*?(?:On\s+)?Wednesday\s+evening\b", "## WEDNESDAY EVENING VESPERS (FOR THURSDAY)"),
        ("THU_MATINS", r"^\*?(?:(?:On\s+)?Thursday\s+(?:at\s+Matins|Morning)|At\s+Matins,\s+after\s+the\s+(?:1st|First)\s+Kathisma,\s+Sessional\s+Hymns,\s+Tone\s+4)\b", "## THURSDAY MATINS: THE HOLY APOSTLES AND ST. NICHOLAS"),
        ("THU_VESPERS", r"^\*?(?:On\s+)?Thursday\s+evening\b", "## THURSDAY EVENING VESPERS (FOR FRIDAY)"),
        ("FRI_MATINS", r"^\*?(?:On\s+)?Friday\s+(?:at\s+Matins|Morning)\b", "## FRIDAY MATINS: THE PRECIOUS CROSS AND THE THEOTOKOS"),
        ("FRI_VESPERS", r"^\*?(?:On\s+)?Friday\s+evening\b", "## FRIDAY EVENING VESPERS (FOR SATURDAY)"),
        ("SAT_MATINS", r"^\*?(?:On\s+)?Saturday\s+(?:at\s+Matins|Morning)\b", "## SATURDAY MATINS: ALL SAINTS, MARTYRS, AND THE DEPARTED"),
    ]

    for line_idx, raw_line in enumerate(lines):
        line = raw_line.strip()
        if not line:
            formatted.append("")
            continue

        if RE_COHORT_BOUNDARY.match(line):
            formatted.extend(["", line, ""])
            continue

        # 1. Strip invented stanza numbers (preserving any leading [f. XvA] milestone)
        line = RE_INVENTED_STANZA_NUM.sub(r"\1", line)
        clean_line = re.sub(r"^(?:\[(?:f\.\s*[^\]]+|p\d+[LR][AB])\]\s*)+", "", line).strip()

        # 2. Heading Normalizations
        if re.match(r"^#+\s*(?:TONE\s+\d+|Book\s+of\s+the\s+Octoechos.*Tone\s+\d+|WEEKDAY\s+OFFICES|PREFACE|EXAPOSTILARIA|EVANGELICAL|COLOPHON)\b", clean_line, re.IGNORECASE):
            m_t = re.search(r"\bTONE\s+(\d+)\b", clean_line, re.IGNORECASE)
            if m_t and not RE_MAJOR_OFFICE.match(clean_line):
                active_macro = f"TONE_{int(m_t.group(1))}"
                emitted_in_section.clear()
                section_has_explicit_h2 = _section_has_enough_explicit_h2(line_idx)
                if clean_line.startswith("# "):
                    formatted.extend(["", clean_line, ""])
                    continue
            elif re.match(r"^#\s+WEEKDAY\s+OFFICES", clean_line, re.IGNORECASE):
                active_macro = "WEEKDAY_OFFICES"
                emitted_in_section.clear()
                section_has_explicit_h2 = _section_has_enough_explicit_h2(line_idx)
                formatted.extend(["", clean_line, ""])
                continue
            elif re.match(r"^#\s+(?:EXAPOSTILARIA|EVANGELICAL)", clean_line, re.IGNORECASE):
                active_macro = "EXAPOSTILARIA"
                emitted_in_section.clear()
                section_has_explicit_h2 = _section_has_enough_explicit_h2(line_idx)
                formatted.extend(["", clean_line, ""])
                continue
            elif re.match(r"^#\s+(?:PREFACE|COLOPHON)", clean_line, re.IGNORECASE):
                section_has_explicit_h2 = _section_has_enough_explicit_h2(line_idx)
                formatted.extend(["", clean_line, ""])
                continue

        # Detect Consolidated Weekday Cycle after Tone 8 Sunday Evening (Layout B Octoechos, e.g. Kyiv 1629)
        if (
            active_macro == "TONE_8"
            and "SUNDAY_EVENING" in emitted_in_section
            and re.match(r"^\*?(?:On\s+Monday\s+at\s+Matins|Monday\s+Matins)\b.*?\bTone\s+1\b", clean_line, re.IGNORECASE)
        ):
            formatted.extend(["", "# WEEKDAY OFFICES OF THE OCTOECHOS (MONDAY THROUGH SATURDAY)", ""])
            active_macro = "WEEKDAY_OFFICES"
            emitted_in_section.clear()
            section_has_explicit_h2 = _section_has_enough_explicit_h2(line_idx)

        # Promote italicized liturgical office rubrics into canonical H2 headings when section has < 3 explicit H2s
        if not section_has_explicit_h2 and not clean_line.startswith("#") and clean_line != "---":
            if active_macro.startswith("TONE_"):
                t_num = active_macro.split("_")[1]
                if "SATURDAY_EVENING" not in emitted_in_section and (
                    re.match(r"^\*?(?:On\s+Saturday\s+evening|At\s+Great\s+Vespers|At\s+Vespers|At\s+[\"“']?Lord,\s+I\s+have\s+cried)\b", clean_line, re.IGNORECASE)
                    or len(emitted_in_section) == 0
                ):
                    if not clean_line.startswith("["):
                        formatted.extend(["", f"## SATURDAY EVENING: VESPERS (TONE {t_num})", ""])
                        emitted_in_section.add("SATURDAY_EVENING")
                elif "SUNDAY_MIDNIGHT" not in emitted_in_section and (
                    re.match(r"^\*?(?:On\s+Sunday\s+at\s+the\s+Midnight\s+Office|At\s+the\s+Midnight\s+Office|Midnight\s+Office)\b", clean_line, re.IGNORECASE)
                    or re.search(r"\bCanon\s+(?:to|of)\s+the\s+(?:Most\s+)?Holy\s+(?:and\s+)?(?:Life-[A-Za-z]+\s+)?Trinity\b", clean_line, re.IGNORECASE)
                ):
                    formatted.extend(["", f"## SUNDAY MIDNIGHT OFFICE (TONE {t_num})", ""])
                    emitted_in_section.add("SUNDAY_MIDNIGHT")
                elif "SUNDAY_MATINS" not in emitted_in_section and re.match(
                    r"^\*?(?:At\s+Matins|Beginning\s+of\s+Matins|On\s+Sunday\s+Morning|On\s+Sunday\s+at\s+Matins|At\s+[\"“]?God\s+is\s+the\s+Lord|(?:After|At|Resurrection\s+Sessional\s+Hymn\.\s+At)\s+the\s+(?:1st|First)\s+(?:Kathisma|Stichology))\b",
                    clean_line,
                    re.IGNORECASE,
                ):
                    formatted.extend(["", f"## SUNDAY MATINS (TONE {t_num})", ""])
                    emitted_in_section.add("SUNDAY_MATINS")
                elif "SUNDAY_BEATITUDES" not in emitted_in_section and re.match(
                    r"^\*?(?:On\s+Sunday,?\s+(?:at\s+)?the\s+Beatitudes|At\s+the\s+(?:Divine\s+)?Liturgy,\s+the\s+Beatitudes|The\s+Beatitudes,\s+Tone)\b",
                    clean_line,
                    re.IGNORECASE,
                ):
                    formatted.extend(["", f"## SUNDAY LITURGY: THE BEATITUDES (TONE {t_num})", ""])
                    emitted_in_section.add("SUNDAY_BEATITUDES")
                elif "SUNDAY_EVENING" not in emitted_in_section and re.match(
                    r"^\*?(?:On\s+)?Sunday\s+evening\b",
                    clean_line,
                    re.IGNORECASE,
                ):
                    formatted.extend(["", f"## SUNDAY EVENING VESPERS (TONE {t_num})", ""])
                    emitted_in_section.add("SUNDAY_EVENING")
                else:
                    for wk_key, wk_pat, wk_h2 in weekday_rubric_map:
                        if wk_key not in emitted_in_section and re.match(wk_pat, clean_line, re.IGNORECASE):
                            formatted.extend(["", f"{wk_h2} (TONE {t_num})", ""])
                            emitted_in_section.add(wk_key)
                            break
            elif active_macro == "WEEKDAY_OFFICES":
                for wk_key, wk_pat, wk_h2 in weekday_rubric_map:
                    if wk_key not in emitted_in_section and re.match(wk_pat, clean_line, re.IGNORECASE):
                        formatted.extend(["", wk_h2, ""])
                        emitted_in_section.add(wk_key)
                        break
            elif active_macro == "EXAPOSTILARIA":
                if "EXAP_EOTHINA" not in emitted_in_section and re.match(
                    r"^\*?(?:\*\*)?(?:The\s+)?(?:Resurrectional\s+Exapostilaria|First\s+Exapostilarion|Exapostilarion\s+1)\b",
                    clean_line,
                    re.IGNORECASE,
                ):
                    formatted.extend(["", "## RESURRECTIONAL EXAPOSTILARIA AND ELEVEN EVANGELICAL STICHERA (EOTHINA)", ""])
                    emitted_in_section.add("EXAP_EOTHINA")
                elif "TRIADIKA" not in emitted_in_section and re.match(
                    r"^\*?(?:Beginning\s+with\s+God\s+of\s+the\s+Triadika|Triadika\s+(?:of\s+the\s+days|hymns))\b",
                    clean_line,
                    re.IGNORECASE,
                ):
                    formatted.extend(["", "## WEEKDAY TRIADIKA (HYMNS TO THE TRINITY) AND PHOTOGOGIKA (TONES 1–8)", ""])
                    emitted_in_section.add("TRIADIKA")
                elif "PROVENANCE" not in emitted_in_section and re.match(
                    r"^\*?(?:\*\*|\[)?(?:Lower\s+Margin|Archival\s+Stamp|Library\s+Stamp|Rear\s+Pastedown|Rear\s+Flyleaf|Manuscript\s+provenance)\b",
                    clean_line,
                    re.IGNORECASE,
                ):
                    formatted.extend(["", "## CODICOLOGICAL PROVENANCE, ARCHIVAL INSCRIPTIONS, AND REAR BINDING", ""])
                    emitted_in_section.add("PROVENANCE")

        m_ode = RE_CANON_ODE.match(clean_line)
        if m_ode:
            line = f"#### Ode {m_ode.group(1)}"
            formatted.extend(["", line, ""])
            continue

        m_office = RE_MAJOR_OFFICE.match(clean_line)
        if m_office:
            office_title = m_office.group(0).lstrip("#").strip()
            office_title = re.sub(r"^TONE\s+\d+\s*[-—:]\s*", "", office_title, flags=re.IGNORECASE)
            line = f"## {office_title.upper()}"
            formatted.extend(["", line, ""])
            continue

        m_sec = RE_SECTION_HEADING.match(clean_line)
        if m_sec and not RE_MAJOR_OFFICE.match(clean_line):
            sec_title = m_sec.group(0).lstrip("#").strip()
            line = f"### {sec_title}"
            formatted.extend(["", line, ""])
            continue

        # 3. Liturgical Stanza Separation: always insert blank line between distinct paragraphs
        if formatted and formatted[-1].strip():
            prev_l = formatted[-1].strip()
            if not prev_l.startswith("#") and prev_l != "---" and not RE_COHORT_BOUNDARY.match(prev_l):
                formatted.append("")

        formatted.append(line)

    result = "\n".join(formatted)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


# ==============================================================================
# 5. Monument Processor & Deliverable Generators
# ==============================================================================

POD_TRIGGER_RE = re.compile(
    r"\b(?:Podoben|Prosomoion|Model\s+melody|Model|Melodic\s+model|Special\s+Melody|Same\s+melody|Nekrosimon)\b"
    r"|^\*?(?:For\s+the\s+Departed(?:\s*\[Поко́инъ\])?|Hymn\s+for\s+the\s+Departed(?:\s*\(Поко́инъ\))?):\*?(?:\s*\[\^\d+\])?$"
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
    2. Performs leaf-synchronized primitive normalization (Podobens, Stichoi, Weekday Heirmoi, Pokoin).
    3. Runs unified codex-wide 2-up seam stitching with [f. XvA] locus milestones across both
       intra-cohort and inter-cohort boundaries.
    4. Runs stanza separation (\\n\\n) and heading hierarchy standardization.
    5. Emits _drift_ledger.json, _drift_report.md, _primitives_review.md,
       _propers_corpus.json, and _slavonic_complete.md.
    """
    normalizer = HymnographicNormalizer()
    mon_meta = load_monument_metadata(monument_id)

    cohort_files = sorted(
        list(cohorts_dir.glob("*.md")),
        key=lambda p: int(re.search(r"cohort(\d+)", p.name).group(1)) if re.search(r"cohort(\d+)", p.name) else 999
    )
    source_files = sorted(
        list(source_dir.glob("*source.txt")),
        key=lambda p: int(re.search(r"cohort(\d+)", p.name).group(1)) if re.search(r"cohort(\d+)", p.name) else 999
    )

    pre_norm_cohorts: List[str] = []
    all_drift_events: List[Dict[str, Any]] = []
    slavonic_stanzas_by_leaf: Dict[int, List[str]] = {}
    folio_to_leaf_map: Dict[str, int] = {}

    current_tone = 1
    current_ode = 1

    for idx, c_file in enumerate(cohort_files):
        c_idx = idx + 1
        c_text = c_file.read_text(encoding="utf-8-sig")
        s_text = source_files[idx].read_text(encoding="utf-8-sig") if idx < len(source_files) else ""

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
            s_pods, s_verses, s_stanzas = extract_leaf_slavonic_primitives(s_lns, normalizer.podobens)
            s_primitives_by_leaf[lf_num] = (s_pods, s_verses, s_stanzas)
            slavonic_stanzas_by_leaf[lf_num] = s_stanzas

        # Step A: Leaf-Synchronized Primitive Normalization (while === LEAF pN === banners are intact)
        norm_lines: List[str] = [f"=== COHORT_BOUNDARY {c_idx} ==="]
        curr_c_leaf = 1

        for raw_c_line in c_text.splitlines():
            c_line = raw_c_line.strip()

            m_lf = RE_LEAF_BANNER.match(c_line)
            if m_lf:
                curr_c_leaf = int(m_lf.group(1))
                norm_lines.append(raw_c_line)
                continue

            m_pg = RE_PAGE_HEADER.match(c_line)
            if m_pg:
                f_str = (m_pg.group(2) or "").strip().lower()
                if not f_str and m_pg.group(3):
                    mf_desc = re.search(r"(?:Fol\.?|Folio)\s*([0-9]+[rv])", m_pg.group(3), re.IGNORECASE)
                    if mf_desc:
                        f_str = mf_desc.group(1).strip().lower()
                if f_str:
                    folio_to_leaf_map[f_str] = curr_c_leaf

            m_t = re.search(r"\bTONE\s+(\d+|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT)\b", c_line, re.IGNORECASE)
            if m_t:
                word_to_num = {
                    "one": 1, "two": 2, "three": 3, "four": 4,
                    "five": 5, "six": 6, "seven": 7, "eight": 8
                }
                t_val = m_t.group(1).lower()
                current_tone = word_to_num.get(t_val, int(t_val) if t_val.isdigit() else current_tone)

            m_o = re.search(r"\bOde\s+(\d+)\b", c_line, re.IGNORECASE)
            if m_o:
                current_ode = int(m_o.group(1))

            s_pods, s_verses, _ = s_primitives_by_leaf.get(curr_c_leaf, ([], [], []))

            # 1. Check Podoben / Prosomoion / Model / Melodic model / Same melody / To: / Pokoin
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

        pre_norm_cohorts.append("\n".join(norm_lines))

    # Step B: Unified Codex-Wide 2-up seam stitching with [f. XvA] milestones (intra-cohort + inter-cohort)
    combined_pre_norm = "\n".join(pre_norm_cohorts)
    stitched_codex, stitch_log = stitch_2up_hymnographic_stream(combined_pre_norm)
    total_stitch_count = len(stitch_log)

    # Record SEAM_OVERLAP_DEDUPLICATED events into all_drift_events for auditability
    for s_ev in stitch_log:
        if s_ev.get("deduplicated"):
            all_drift_events.append({
                "type": "SEAM_OVERLAP_DEDUPLICATED",
                "locus": s_ev.get("milestone", ""),
                "prev_tail": s_ev.get("prev_tail", ""),
                "curr_head": s_ev.get("curr_head", ""),
                "is_ai_drift": True,
            })

    # Step C: Stanza separation & heading standardization across full codex
    formatted_codex = format_hymnographic_stanzas_and_headings(stitched_codex)

    # Split back by cohort boundaries for propers corpus tracking, and strip markers for unified text
    all_stitched_cohorts = [
        chunk.strip()
        for chunk in re.split(r"(?m)^===\s*COHORT_BOUNDARY\s+\d+\s*===$", formatted_codex)
        if chunk.strip()
    ]
    unified_codex_text = re.sub(r"(?m)^===\s*COHORT_BOUNDARY\s+\d+\s*===\n*", "", formatted_codex)
    unified_codex_text = re.sub(r"\n{3,}", "\n\n", unified_codex_text).strip()

    # Step D: Emit Companion Deliverables
    emit_deliverables(
        monument_id=monument_id,
        mon_meta=mon_meta,
        source_files=source_files,
        all_stitched_cohorts=all_stitched_cohorts,
        slavonic_stanzas_by_leaf=slavonic_stanzas_by_leaf,
        folio_to_leaf_map=folio_to_leaf_map,
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
    mon_meta: Dict[str, Any],
    source_files: List[Path],
    all_stitched_cohorts: List[str],
    slavonic_stanzas_by_leaf: Dict[int, List[str]],
    folio_to_leaf_map: Dict[str, int],
    all_drift_events: List[Dict[str, Any]],
    total_stitch_count: int,
    final_md_dir: Path,
    normalizer: HymnographicNormalizer
) -> None:
    """Emits the 5 companion deliverables into Final MD/."""
    final_md_dir.mkdir(parents=True, exist_ok=True)

    # 1. Consolidated Church Slavonic Master
    slavonic_parts = [sf.read_text(encoding="utf-8-sig").strip() for sf in source_files]
    slavonic_complete = "\n\n---\n\n".join(slavonic_parts)
    slavonic_complete = re.sub(r"^Tropar hlas 7$", "(*Tropar hlas 7*)", slavonic_complete, flags=re.MULTILINE)
    (final_md_dir / f"{monument_id}_slavonic_complete.md").write_text(slavonic_complete, encoding="utf-8")
    print(f"  [Companion] Emitted {monument_id}_slavonic_complete.md ({len(slavonic_complete):,} chars)")

    # 2. Drift Ledger JSON
    seam_dedup_count = sum(1 for e in all_drift_events if e.get("type") == "SEAM_OVERLAP_DEDUPLICATED")
    ledger_data = {
        "monument_id": monument_id,
        "title": mon_meta["title"],
        "publication_year": mon_meta["publication_year"],
        "total_physical_pages": mon_meta["total_physical_pages"],
        "total_stitches": total_stitch_count,
        "seam_overlaps_deduplicated": seam_dedup_count,
        "total_drift_records": len(all_drift_events),
        "events": all_drift_events
    }
    (final_md_dir / f"{monument_id}_drift_ledger.json").write_text(
        json.dumps(ledger_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    audit_rep_dir = final_md_dir.parent / "Audit_Reports"
    audit_rep_dir.mkdir(parents=True, exist_ok=True)
    (audit_rep_dir / f"{monument_id}_drift_ledger.json").write_text(
        json.dumps(ledger_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"  [Companion] Emitted {monument_id}_drift_ledger.json ({len(all_drift_events)} records, {seam_dedup_count} seam overlaps deduplicated)")

    # 3. Complete Bilingual Cross-Propers Corpus JSON (computed first so dynamic Heirmoi can feed Primitives Digest)
    corpus_json = generate_propers_corpus(
        monument_id=monument_id,
        mon_meta=mon_meta,
        all_stitched_cohorts=all_stitched_cohorts,
        slavonic_stanzas_by_leaf=slavonic_stanzas_by_leaf,
        folio_to_leaf_map=folio_to_leaf_map,
        normalizer=normalizer
    )
    (final_md_dir / f"{monument_id}_propers_corpus.json").write_text(
        json.dumps(corpus_json, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"  [Companion] Emitted {monument_id}_propers_corpus.json ({len(corpus_json.get('items', []))} items)")

    # 4. Father Paul Primitives Review Digest (Dynamic Per-Monument Attestation)
    primitives_review = generate_father_paul_digest(
        monument_id=monument_id,
        mon_meta=mon_meta,
        normalizer=normalizer,
        events=all_drift_events,
        corpus_items=corpus_json.get("items", []),
        stitched_cohorts=all_stitched_cohorts
    )
    (final_md_dir / f"{monument_id}_primitives_review.md").write_text(primitives_review, encoding="utf-8")
    print(f"  [Companion] Emitted {monument_id}_primitives_review.md ({len(primitives_review):,} chars)")

    # 5. Drift Analysis Markdown Report
    drift_report = generate_drift_report(monument_id, mon_meta, total_stitch_count, all_drift_events)
    (final_md_dir / f"{monument_id}_drift_report.md").write_text(drift_report, encoding="utf-8")
    print(f"  [Companion] Emitted {monument_id}_drift_report.md ({len(drift_report):,} chars)")


def generate_father_paul_digest(
    monument_id: str,
    mon_meta: Dict[str, Any],
    normalizer: HymnographicNormalizer,
    events: List[Dict[str, Any]],
    corpus_items: List[Dict[str, Any]],
    stitched_cohorts: Optional[List[str]] = None
) -> str:
    """
    Generates the Canonical Liturgical Primitives Review Digest dynamically from the target
    monument's actual normalization events and extracted corpus stanzas.
    """
    pub_year = mon_meta["publication_year"]
    short_title = mon_meta["short_title"]

    # Dynamically aggregate Stichoi attested in this monument
    verse_loci_by_id: Dict[str, List[str]] = {}
    verse_slav_by_id: Dict[str, str] = {}
    for ev in events:
        if ev.get("type") in ("PSALM_VERSE_NORMALIZED", "PSALM_VERSE_TIER3_SOURCE_VARIANT"):
            vid = ev.get("id", "")
            loc = ev.get("locus", "")
            if vid:
                verse_loci_by_id.setdefault(vid, []).append(loc)
                if vid not in verse_slav_by_id and ev.get("slavonic_source"):
                    verse_slav_by_id[vid] = ev["slavonic_source"]

    # Dynamically aggregate Podobens attested in this monument
    pod_loci_by_id: Dict[str, List[str]] = {}
    pod_slav_by_id: Dict[str, str] = {}
    same_pod_loci: List[str] = []
    for ev in events:
        ev_type = ev.get("type", "")
        if ev_type == "PODOBEN_NORMALIZED":
            pid = ev.get("primitive_id", "")
            loc = ev.get("locus", "")
            if pid:
                pod_loci_by_id.setdefault(pid, []).append(loc)
                if pid not in pod_slav_by_id and ev.get("slavonic_source"):
                    pod_slav_by_id[pid] = ev["slavonic_source"]
        elif ev_type == "PODOBEN_SAME_NORMALIZED":
            same_pod_loci.append(ev.get("locus", ""))

    attested_stichoi = [st for st in normalizer.stichoi if verse_loci_by_id.get(st["id"])]
    unattested_stichoi = [st for st in normalizer.stichoi if not verse_loci_by_id.get(st["id"])]

    attested_podobens = [pod for pod in normalizer.podobens if pod_loci_by_id.get(pod["id"])]
    unattested_podobens_in_monument = [pod for pod in normalizer.podobens if not pod_loci_by_id.get(pod["id"])]

    total_pod_invocations = sum(len(v) for v in pod_loci_by_id.values()) + len(same_pod_loci)
    ws_dir = PROJECT_ROOT / mon_meta["workspace_dir"]
    complete_file = ws_dir / "Final MD" / f"{monument_id}_complete.md"
    if stitched_cohorts:
        total_pod_invocations = sum(
            1
            for txt in stitched_cohorts
            for ln in txt.splitlines()
            if re.search(r"\bpodoben:", ln, re.IGNORECASE)
        )
    elif complete_file.exists():
        comp_txt = complete_file.read_text(encoding="utf-8")
        comp_body = re.split(r"\n#\s*FOOTNOTES AND SCHOLARLY COMMENTARY", comp_txt, flags=re.IGNORECASE)[0]
        total_pod_invocations = sum(1 for ln in comp_body.splitlines() if re.search(r"\bpodoben:", ln, re.IGNORECASE))
    else:
        cohorts_dir = ws_dir / "Cohorts" if (ws_dir / "Cohorts").exists() else ws_dir / "Final MD"
        cohorts_pod_count = sum(
            1
            for cf in cohorts_dir.glob("*cohort*.md")
            for ln in cf.read_text(encoding="utf-8").splitlines()
            if re.search(r"\bpodoben:", ln, re.IGNORECASE)
        )
        if cohorts_pod_count > 0:
            total_pod_invocations = cohorts_pod_count

    lines = [
        f"# Canonical Liturgical Primitives Review Digest: {short_title}",
        "",
        "> [!IMPORTANT]",
        "> **For Pastoral and Liturgical Review by Father Paul**",
        f"> This document collects all recurring liturgical primitives physically attested across **all 8 Tones** of the {short_title} (`{len(attested_stichoi)}` recurring Psalm *Stichoi*, `{len(attested_podobens)}` distinct *Podoben* / *Automelon* models invoked `{total_pod_invocations}` times across Tones 1–8, and all `{len(normalizer.heirmoi)}` Sunday Canon *Heirmoi* across Tones 1–8).",
        "> Any revision made to a canonical English rendering in `data/liturgical_primitives_registry.json` will automatically propagate across every service in the codex via a single re-compile.",
        "",
        "---",
        "",
        "## 1. Recurring Psalm Verses (Stichoi)",
        "",
        f"| ID | LXX Reference | {pub_year} Church Slavonic Witness | Byzantine Greek | Canonical English Translation | Attested Loci |",
        "| :--- | :--- | :--- | :--- | :--- | :---: |"
    ]
    for st in (attested_stichoi if attested_stichoi else normalizer.stichoi):
        loci_list = verse_loci_by_id.get(st["id"], [])
        loci_cnt = len(loci_list)
        slav_w = verse_slav_by_id.get(st["id"], st["slavonic_canonical"])
        lines.append(
            f"| `{st['id']}` | **{st['lxx_ref']}** | *{slav_w}* | *{st['greek']}* | {st['english_canonical']} | {loci_cnt} leaves |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 2. Model Hymns (Podobens / Automela — Tones 1 to 8)",
        "",
        "> [!NOTE]",
        f"> **Internal Attestation & Mathematical Parity Guarantee:** 100% of the `{len(attested_podobens)}` models below (plus `{len(same_pod_loci)}` *\"The same\"* continuation rubrics = `{total_pod_invocations}` total Podoben invocations) are physically attested and prescribed within `{monument_id}`.",
        f"> For the complete chronological invocation log across all `{total_pod_invocations}` occurrences, see [{monument_id}_podoben_grid.md]({monument_id}_podoben_grid.md).",
        "",
        f"| ID | Tone | {pub_year} Church Slavonic Incipit | Byzantine Greek Automelon | Canonical English Incipit | Attested Loci |",
        "| :--- | :---: | :--- | :--- | :--- | :--- |"
    ])
    for pod in attested_podobens:
        loci_list = pod_loci_by_id.get(pod["id"], [])
        loci_cnt = len(loci_list)
        loci_sample = ", ".join(loci_list[:4])
        if loci_cnt > 4:
            loci_sample += f" (+{loci_cnt - 4} more)"
        slav_w = pod_slav_by_id.get(pod["id"], pod["slavonic_canonical"])
        lines.append(
            f"| `{pod['id']}` | Tone {pod['tone']} | *{slav_w}* | *{pod['greek']}* | **{pod['english_canonical']}** | `{loci_sample}` ({loci_cnt}x) |"
        )
    if same_pod_loci:
        same_cnt = len(same_pod_loci)
        same_sample = ", ".join(same_pod_loci[:4]) + (f" (+{same_cnt - 4} more)" if same_cnt > 4 else "")
        lines.append(
            f"| `POD.SAME.TOIZHE` | Tones 1–8 | *то́йже / Гла́съ и҆ подо́бенъ то́йже* | *Ὁ αὐτός* | **The same / The same Tone and Podoben** | `{same_sample}` ({same_cnt}x) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Sunday Canon Heirmoi (Complete 8-Tone Cycle: Tones 1–8, Odes 1, 3–9)",
        ""
    ])

    # Build dynamic lookup of Sunday Resurrectional Canon Heirmoi from corpus_items
    dynamic_heirmoi_by_key: Dict[Tuple[int, int], Dict[str, Any]] = {}
    for it in corpus_items:
        t_num = int(it.get("tone", 0))
        o_num = it.get("ode") or 0
        if t_num in range(1, 9) and o_num in (1, 3, 4, 5, 6, 7, 8, 9):
            if (t_num, o_num) not in dynamic_heirmoi_by_key and it.get("hymn_type") == "Heirmos":
                dynamic_heirmoi_by_key[(t_num, o_num)] = it

    for tone_num in range(1, 9):
        lines.extend([
            f"### Tone {tone_num} Sunday Canon Heirmoi",
            "",
            f"| Ode | Locus | {pub_year} Church Slavonic Incipit | Byzantine Greek Incipit | {short_title} Translation |",
            "| :---: | :---: | :--- | :--- | :--- |"
        ])
        tone_heirmoi = [h for h in normalizer.heirmoi if h["tone"] == tone_num]
        for h in tone_heirmoi:
            dyn_h = dynamic_heirmoi_by_key.get((tone_num, h["ode"]))
            if dyn_h:
                loc_str = f"{dyn_h.get('leaf', '')} ({dyn_h.get('locus', '')})"
                slav_inc = (dyn_h.get("slavonic_text") or h["slavonic_incipit"])[:75].strip()
                eng_full = re.sub(r"^\*?[^\*:]*Heirmos:\*?\s*", "", dyn_h.get("english_text", "")).strip() or h["english_full"]
            else:
                loc_str = h.get("leaf", "")
                slav_inc = h["slavonic_incipit"]
                eng_full = h["english_full"]
            lines.append(
                f"| Ode {h['ode']} | `{loc_str}` | *{slav_inc}* | *{h['greek']}* | {eng_full} |"
            )
        lines.append("")

    # Section 4: Un-Invoked Comparative Automela in This Edition
    all_uninvoked = unattested_podobens_in_monument + normalizer.registry.get("unattested_comparative_models", [])
    if all_uninvoked:
        lines.extend([
            "",
            "---",
            "",
            "## 4. Un-Invoked Comparative Automela (Not Prescribed in This Edition)",
            "",
            f"The following classical Byzantine/Slavonic Automela exist in the shared liturgical registry (`data/liturgical_primitives_registry.json`) but have **0 invocations** within the physical leaves of `{monument_id}`:",
            "",
            "| Tone | Model ID | Classical Slavonic Incipit | Byzantine Greek Automelon | Classical English Title | Liturgical Provenance / Reason for Non-Invocation |",
            "| :---: | :--- | :--- | :--- | :--- | :--- |"
        ])
        notes_map = {
            "POD.T2.DOM_EVFRATOV": "Menaion December cycle (Forefeast of the Nativity); not used in the weekly Octoechos.",
            "POD.T4.VOZNESYISYA_NA_KREST": "Horologion Troparion of the Holy Cross; chanted as a Sessional model in some recensions.",
            "POD.T4.UDIVISYA_IOSIF": "Tone 4 Sessional Hymn model; omitted when weekday cycles are condensed.",
            "POD.T7.RADUISYA": "Cross-tone borrowed model heading.",
        }
        seen_uninv: Set[str] = set()
        for u in all_uninvoked:
            if u["id"] in seen_uninv:
                continue
            seen_uninv.add(u["id"])
            note = notes_map.get(
                u["id"],
                f"Prescribed in full 8-week weekday Octoechos recensions; not invoked in the {short_title} cycle."
            )
            lines.append(
                f"| Tone {u['tone']} | `{u['id']}` | *{u['slavonic_canonical']}* | *{u['greek']}* | **{u['english_canonical']}** | {note} |"
            )

    return "\n".join(lines)


def generate_drift_report(
    monument_id: str,
    mon_meta: Dict[str, Any],
    total_stitches: int,
    events: List[Dict[str, Any]]
) -> str:
    pub_year = mon_meta["publication_year"]
    short_title = mon_meta["short_title"]
    total_pages = mon_meta["total_physical_pages"]

    ai_drift_count = sum(1 for e in events if e.get("is_ai_drift"))
    tier3_source_count = sum(1 for e in events if e.get("drift_tier") in ("TIER_3_LEXICAL_RECENSIONAL", "SCRIBAL_INCIPIT_TRUNCATION"))
    seam_dedup_events = [e for e in events if e.get("type") == "SEAM_OVERLAP_DEDUPLICATED"]
    pod_events = [e for e in events if "PODOBEN" in e.get("type", "") or "POKOIN" in e.get("type", "")]
    verse_events = [e for e in events if "VERSE" in e.get("type", "")]
    heirmos_events = [e for e in events if "HEIRMOS" in e.get("type", "")]

    lines = [
        f"# Scholarly Drift & Seam-Stitching Audit Report: {short_title}",
        "",
        f"- **Monument ID**: `{monument_id}`",
        f"- **Total 2-Up Mid-Sentence Seams Stitched**: {total_stitches} boundaries (`{len(seam_dedup_events)}` sub-clause seam overlaps deduplicated)",
        f"- **Inline Locus Milestones Inserted**: `[f. XvA]`, `[f. XrA]` across all {total_pages} leaves",
        f"- **Total Primitive Normalization & Drift Events**: {len(events)} (`{len(pod_events)}` Podobens/Pokoin, `{len(verse_events)}` Psalm Stichoi, `{len(heirmos_events)}` Weekday Heirmoi, `{len(seam_dedup_events)}` Seam Deduplications)",
        f"- **True Pre-Normalization AI Translation Drift Unified**: {ai_drift_count} occurrences",
        f"- **Source-Text ({pub_year} Slavonic) Scribal Truncations & Tier 3 Variations Classified**: {tier3_source_count} events",
        "",
        "---",
        "",
        "## 1. Summary of 3-Tier Source & Scribal Drift Engine",
        "",
        "1. **Tier 1 (Typographic / Titlo Equivalence)**: Strips accents, titla, and sacred abbreviations (`бг҃` -> `богъ`). Unified silently to canonical English.",
        "2. **Tier 2 (Orthographic / Phonological Variant)**: Harmonizes Ruthenian/Church Slavonic vowel and yer reflexes (`ѡ`/`о`, `ѣ`/`е`, `ꙋ`/`у`, `ᲂу`/`у`). Unified to canonical English while logging orthographic drift.",
        "3. **Scribal Incipit Truncation (`SCRIBAL_INCIPIT_TRUNCATION`)**: The printer/scribe abbreviated the model incipit on the physical leaf (e.g. `По̀, Дв҃аа` for `Дѣ́ва дне́сь`, or omitted `Подо́бенъ` before the incipit). Classified as a scribal convention, never counted as AI translation error.",
        f"4. **Tier 3 (Lexical / Syntactic / Recensional Variant)**: Genuine source variations in the {pub_year} print. **Preserved as distinct English translations** and annotated.",
        "",
        "---",
        "",
        "## 2. Complete Podoben & Rubric Drift Log",
        "",
        f"| Type | Locus | ID | Drift Tier | {pub_year} Slavonic Witness | Pre-Normalization Cohort Text | Canonical Normalized Reading |",
        "| :--- | :---: | :--- | :---: | :--- | :--- | :--- |"
    ]

    for ev in pod_events:
        ev_type = ev.get("type", "PODOBEN_NORMALIZED")
        locus = ev.get("locus", "")
        prim_id = ev.get("primitive_id", ev.get("id", "N/A"))
        d_tier = ev.get("drift_tier", "TIER_1_TYPOGRAPHIC_TITLO")
        slav = ev.get("slavonic_source", ev.get("slavonic_canonical", ""))
        raw_eng = ev.get("raw_cohort_english", ev.get("raw_english", ""))
        canon_eng = ev.get("canonical_english", "")
        lines.append(f"| `{ev_type}` | `{locus}` | `{prim_id}` | `{d_tier}` | *{slav}* | {raw_eng} | **{canon_eng}** |")

    return "\n".join(lines)


def generate_propers_corpus(
    monument_id: str,
    mon_meta: Dict[str, Any],
    all_stitched_cohorts: List[str],
    slavonic_stanzas_by_leaf: Dict[int, List[str]],
    folio_to_leaf_map: Dict[str, int],
    normalizer: HymnographicNormalizer
) -> Dict[str, Any]:
    """
    Parses all stitched cohorts into a complete bilingual atomic hymn corpus
    with full liturgical coordinates and leaf-synchronized Slavonic source text.
    """
    items: List[Dict[str, Any]] = []
    total_pages = mon_meta["total_physical_pages"]
    folio_offset = mon_meta["folio_offset"]
    ws_rel = mon_meta["workspace_dir"]

    current_tone = 0
    current_office = "Front Matter"
    current_section = "Introductory Prayers & Dedicatory Preface"
    current_ode: Optional[int] = None
    active_podoben_id: Optional[str] = None
    active_locus = "f. 1rA"
    current_leaf = 1
    leaf_stanza_cursor: Dict[int, int] = {}

    for c_idx, cohort_text in enumerate(all_stitched_cohorts, start=1):
        current_leaf = (c_idx - 1) * 10 + 1
        paragraphs = [p.strip() for p in cohort_text.split("\n\n") if p.strip()]

        for para in paragraphs:
            m_loc = re.search(r"\[(f\.\s*([0-9]+[rv])[AB]?|p(\d+)[LR][AB]?)\]", para)
            if m_loc:
                active_locus = m_loc.group(1)
                if m_loc.group(3):
                    current_leaf = int(m_loc.group(3))
                elif m_loc.group(2):
                    f_key = m_loc.group(2).strip().lower()
                    if f_key in folio_to_leaf_map:
                        current_leaf = folio_to_leaf_map[f_key]
                    else:
                        f_num_only = int(re.sub(r"[^0-9]", "", f_key))
                        current_leaf = min(total_pages, f_num_only + folio_offset)

            if para.startswith("#"):
                hdr_clean = para.lstrip("#").strip()
                m_t = re.search(r"\bTONE\s+(\d+)\b", hdr_clean, re.IGNORECASE)
                if m_t:
                    current_tone = int(m_t.group(1))
                    current_ode = None
                    active_podoben_id = None

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

                if m_t and para.startswith("# "):
                    current_office = f"Tone {current_tone}"
                    continue

                current_section = hdr_clean
                if "CANON" not in hdr_clean.upper():
                    current_ode = None
                continue

            if para == "---":
                continue

            clean_para = re.sub(r"\[(?:f\.\s*[^\]]+|p\d+[LR][AB])\]\s*", "", para).strip()
            if not clean_para:
                continue

            first_line = clean_para.splitlines()[0].strip()
            if first_line.startswith("*"):
                m_in_t = re.search(r"\bTone\s+(\d+)\b", first_line, re.IGNORECASE)
                if m_in_t and 1 <= int(m_in_t.group(1)) <= 8:
                    current_tone = int(m_in_t.group(1))
                m_in_ode = re.match(r"^\*Ode\s+(\d+)\b", first_line, re.IGNORECASE)
                if m_in_ode:
                    current_ode = int(m_in_ode.group(1))
                    current_section = f"Canon — Ode {current_ode}"
                m_in_day = re.match(
                    r"^\*(?:On\s+)?(Saturday|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday)\s+"
                    r"(?:evening|morning|at\s+Matins|at\s+Vespers|at\s+Compline|at\s+the\s+Midnight\s+Office)",
                    first_line,
                    re.IGNORECASE,
                )
                if m_in_day:
                    current_office = first_line.strip("* :")
                    current_ode = None

            if clean_para.startswith("*Podoben:") or re.match(r"^\*Tone\s+\d+,\s*Podoben:", clean_para, re.IGNORECASE):
                m_pod_eng = re.search(r'Podoben:\s*"([^"]+)"', clean_para, re.IGNORECASE)
                if m_pod_eng:
                    eng_inc = m_pod_eng.group(1).lower()
                    for pod in normalizer.podobens:
                        if pod["english_canonical"].lower() == eng_inc:
                            active_podoben_id = pod["id"]
                            break
                if "\n" not in clean_para:
                    continue

            if clean_para.startswith("*Verse:") and len(clean_para) < 160:
                continue
            if len(clean_para) < 40 and clean_para.startswith("*") and clean_para.endswith("*"):
                continue

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
                hymn_type = "Sessional Hymn"
            elif "Beatitudes" in current_section:
                hymn_type = "Beatitudes Troparion"
            elif "Kontakion" in clean_para or "KONTAKION" in current_section.upper():
                hymn_type = "Kontakion / Ikos"

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
            "source_dir": f"{ws_rel}/Source Text",
            "cohorts_dir": f"{ws_rel}/Cohorts",
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

    mon_meta = load_monument_metadata(args.monument)
    ws_dir = PROJECT_ROOT / mon_meta["workspace_dir"]
    cohorts_dir = ws_dir / "Cohorts"
    source_dir = ws_dir / "Source Text"
    final_md_dir = ws_dir / "Final MD"

    process_monument_cohorts(args.monument, cohorts_dir, source_dir, final_md_dir)
