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
from typing import Any, Dict, List, Optional, Set, Tuple

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

from scripts.concurrency_lock import atomic_update_registry
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

NON_HYMNOGRAPHIC_MONUMENT_TYPES = {
    "typikon",
    "juridical_synodal",
    "lexicon_scholarly",
}

VALID_UNIT_CLASSES = (
    "PROPER_HYMN",
    "SACERDOTAL_PRAYER",
    "LITANY_OR_DIALOGUE",
    "FIXED_ORDINARY_OR_LECTION",
    "RUBRIC_OR_STATUTE",
)

# Structural & Running Header Patterns
RE_LEAF_BANNER = re.compile(
    r"^===\s*LEAF\s+p?(\d+)(?:\s*\([^=\n]*\))?\s*===(?:\s*\([^\n]*\))?\s*$",
    re.IGNORECASE,
)
RE_2UP_MILESTONE = re.compile(
    r"^(?:#{1,6}\s*|\*\*)?\[(Left|Right)\s+Page\s*(?:—|--|-|:)\s*(?:(?:Fol\.?|Folio)\s*([0-9]+[rv])|(.+?))\](?:\*\*)?(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_COLUMN_MARKER = re.compile(
    r"^(?:#{1,6}\s*|\*\*|\*)?\[?(?:Column|Колонка|Столбец)\s+([A-B1-2А-В]):?\]?(?:\*\*|\*)?(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_RUNNING_HEADER_BRACKET = re.compile(
    r"^\[(?:Fol\.?\s*([0-9]+[rv]?)\.?\s*)?(?:Running\s+header|Колонтитул):\s*([^\]]+)\](?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_CONTINUATION_BRACKET = re.compile(
    r"^(?:\*\*)?\[(?:Continuation\s+of\b|Continues\b|Продовження\b|Кустод:|Catchword:|Typographic\s+divider|Woodcut\s+typographic\s+(?:ornament|headband|tailpiece)|Ornamental\s+divider)[^\]]*\](?:\*\*)?(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_SLAVONIC_EDITORIAL_BRACKET = re.compile(
    r"^\[[^\]]+\](?:\s*(?:\[\^\d+\])+)?$",
)
RE_WOODCUT_INITIAL = re.compile(
    r"^\[(?:Fol\.?\s*([0-9]+[rv]?)\.?\s*)?(?:Decorative\s+|Historiated\s+|Engraved\s+|Woodcut\s+|Cinnabar\s+|Red\s+)*initial\s+([A-Za-zА-ЯІЇЄѠѢꙊ])\b[^\]]*\](?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_SHORT_RUNNING_TITLE = re.compile(
    r"^\*(?:Proskomedia|In\s+the\s+Liturgies|The\s+Holy\s+Liturgy|of\s+Saint\s+John\s+Chrysostom|of\s+Saint\s+Basil\s+the\s+Great|The\s+Presanctified\s+Liturgy|The\s+Ablutions|Order\s+of\s+Holy\s+Baptism)\.?(\*)?(?:\s*\[\^\d+\])?$",
    re.IGNORECASE,
)
RE_STANDALONE_SPEAKER = re.compile(
    r"^(?:>\s*)?\*\*(Priest(?:\s*(?:&|and)\s*Deacon)?|Deacon(?:\s*\[or\s+Priest\])?|Bishop|Hierarch|Archimandrite|Superior|Ecclesiarch|Canonarch|Reader|Choir(?:\s*/\s*Reader)?|Choirs|People|Chanter|Chanters|Clergy|Sponsor|Catechumen|Question|Answer)(?:\s*,\s*exclamation|\s*\(([^\)]+)\))?(?:\s*\[continued\])?:\*\*\s*$",
    re.IGNORECASE,
)
RE_INLINE_SPEAKER = re.compile(
    r"^(?:>\s*)?(?:\*\*)?(?:The\s+|Then\s+the\s+)?(Priest(?:\s*(?:&|and)\s*Deacon)?|Deacon(?:\s*\[or\s+Priest\])?|Bishop|Hierarch|Archimandrite|Superior|Ecclesiarch|Canonarch|Reader|Choir(?:\s*/\s*Reader)?|Choirs|People|Chanter|Chanters|Clergy|Sponsor|Catechumen|Question|Answer)(?:\s*,\s*exclamation|\s*\(([^\)]+)\))?(?:\*\*|\*)?:\s*(?:\*\*)?\s*(.+)$",
    re.IGNORECASE,
)
RE_PRAYER_HEADER_RUBRIC = re.compile(
    r"^\*(?:(?:The\s+)?(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Another)\s+Prayer\b|Prayer\s+(?:of|for|over|at|before|after|unto|to)\b|The\s+Priest\s+(?:says|prays|reads)\s+(?:this\s+)?prayer\b|(?:And\s+the\s+priest|The\s+priest)[^*\n]*(?:prays\s+secretly|saying\s+the\s+prayer)\b|Exorcism\b)[^*\n]*\*(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_STANDALONE_HYMN_ROLE = re.compile(
    r"^\*?(?:(?:After\s+Ode\s+[1-9],\s*)?(?:Ode|Canticle)\s+[1-9]\b[^*\n]*|Heirmos\b[^*\n]*|Katavasia\b[^*\n]*|Another\s*\[?Canon[^\n\*]*|(?:After\s+Ode\s+[1-9],\s*)?(?:Another\s+|Dismissal\s+|Resurrectional\s+)?(?:Troparion|Kontakion|Ikos|Sessional\s+Hymn|Kathisma|Exapost[ei]larion|Photagogi[ck]on|Hymn\s+of\s+Light|Hypakoe|Ypako[eë]|Gradual\s+Hymn|Antiphon\s+\d+|Martyri[ck]on|Triadi[ck]on|For\s+the\s+Departed|Hymn\s+for\s+the\s+Departed|Nekrosimon|Sticheron|Megalynarion|(?:Cross-|Stavro|Stauro)?Theotokion|To\s+the\s+Cross)\b[^*\n]*?)[\.:]?\*?(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_SLAVONIC_STANDALONE_ROLE = re.compile(
    r"^\*?(?:Пѣ[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*снь\s+[^\n:]{1,40}(?:[ЇІИ][\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*рмо[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*съ?)?|[ЇІИ][\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*рмо[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*с[аъ]?|(?:И|І|Ї)[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*н[ъы][\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*[\.,:]?\s*(?:Кано[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*нъ?|[ЇІИ][\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*рмо[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*съ?)|Катава[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*с[і ї и][ая]|Тропа[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*р[ьия]|(?:Богоро|Б[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*горо)[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*диченъ?|Б[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*ц[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*(?:енъ?|ѣ)|(?:Кресто|Кр[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*то)(?:богоро|б[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*горо)[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*диченъ?|Тро[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*иченъ?|М[ꙋу][\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*чениченъ?|Мертвенъ?|За\s+[ѹу]поко[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*й|Конда[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*къ?|[ИІЇ][\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*к[ѡо]съ?|С[ѣе]да[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*л(?:енъ?|на)|[YѴУ]пакои[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*|Св[ѣе]ти[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*ленъ?|Ексапост[іи]ла[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*р[іи]й|Степе[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*нна|Ант[іи]ф[ѡо][\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]*нъ?)\b[^\n]{0,60}?[\.:]?\*?(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_SECTION_RUBRIC_CUE = re.compile(
    r"^\*[^*\n]*\b(?:At\s+\"Lord,\s+I\s+(?:have\s+cried|call)\"|On\s+\"Lord,\s+I\s+(?:have\s+cried|call)\"|At\s+the\s+Aposticha|On\s+the\s+Aposticha|At\s+the\s+Praises|On\s+the\s+Praises|At\s+the\s+Litiya|Resurrectional\s+Stichera|Other\s+(?:Anatolian|Eastern)\s+Stichera|Stichera\s+(?:of|to|on)|At\s+Matins|At\s+Vespers|At\s+Small\s+Vespers|At\s+Great\s+Vespers|At\s+Compline|At\s+the\s+Midnight\s+Office|At\s+the\s+Liturgy|After\s+the\s+\d+(?:st|nd|rd|th)\s+(?:Stichologia|Kathisma)|After\s+the\s+(?:First|Second|Third)\s+(?:Stichologia|Kathisma)|After\s+Ode\s+[1-9]|After\s+the\s+(?:third|sixth|3rd|6th)\s+Ode|The\s+Canon|Gradual\s+Hymns|Songs\s+of\s+Ascent|Anabathmoi|At\s+the\s+Beatitudes|On\s+the\s+Beatitudes)\b[^*\n]*[\.:]?\*(?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)
RE_MENOLOGION_DAY = re.compile(
    r"^\*(?:Month\s+of\s+([A-Z][a-z]+)|(?:On\s+)?(?:the\s+)?(\d+(?:st|nd|rd|th)|(?:Twenty|Thirty)[-\s]+(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth)|First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth|Thirtieth)\s+day|(?:(?:In|On|Of)\s+)?(?:the\s+)?(?:same\s+month|month\s+of\s+the\s+same)[,:\s]+(?:on\s+)?(?:the\s+)?(\d+(?:st|nd|rd|th)|(?:Twenty|Thirty)[-\s]+(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth)|First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth|Thirtieth)(?:\s+day)?)\b[^*\n]*\*(?:\s*(?:\[\^\d+\])+)?",
    re.IGNORECASE,
)
RE_PLAIN_SERVICE_RUBRIC_HEADER = re.compile(
    r"^(?:(?:ON|IN\s+THE\s+EVENING[,]?\s+ON)\s+(?:SATURDAY|SUNDAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY)\b[^\n]{0,130}|(?i:(?:On\s+|In\s+the\s+evening[,]?\s+on\s+)?(?:Saturday|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday)(?:\s+evening)?[,:\s]+(?:at\s+(?:Small\s+Vespers|Little\s+Vespers|Great\s+Vespers|Vespers|Matins|Compline|the\s+Midnight\s+Office|the\s+Liturgy|\"?Lord,\s+I\s+(?:have\s+cried|call)|the\s+Aposticha|the\s+Praises|the\s+Beatitudes)|the\s+Beatitudes|Vespers|Matins)\b[^\n]{0,90})|(?:AT|ON)\s+(?:SMALL\s+VESPERS|LITTLE\s+VESPERS|GREAT\s+VESPERS|VESPERS|MATINS|COMPLINE|THE\s+MIDNIGHT\s+OFFICE|THE\s+LITURGY|\"?LORD,\s+I\s+(?:HAVE\s+CRIED|CALL)|THE\s+APOSTICHA|THE\s+PRAISES|THE\s+BEATITUDES)\b[^\n]{0,90}|(?i:After\s+the\s+(?:First|Second|Third|1st|2nd|3rd)\s+(?:Kathisma|Stichologia)\b[^:\n]{0,90}[:\.]))\s*(?:\[\^\d+\])*$"
)
RE_PODOBEN_HEADER = re.compile(
    r"^\*[^*\n]*?\bPodoben:\s*(?:\"([^\"]+)\"|([^*\(\n]+))(?:\s*\(([^\)]+)\))?[^*\n]*\*",
    re.IGNORECASE,
)
RE_VERSE_HEADER = re.compile(
    r"^\*(?:Verse|Stichos|Refrain)(?:\s+\d+)?\s*:\*?",
    re.IGNORECASE,
)
RE_EXPLICIT_HYMN_START = re.compile(
    r"^\*?(?:(?:After\s+Ode\s+[1-9],\s*)?(?:Ode|Canticle)\s+[1-9]\b[^*\n]*?(?:Heirmos|:|\.\*)|Heirmos\b[^:\n]{0,40}[:\.]|Katavasia\b[^:\n]{0,40}[:\.]|(?:Another\s+|Dismissal\s+|Resurrectional\s+)?Troparion\b[^:\n]{0,60}[:\.]|(?:Cross-|Stavro|Stauro)?Theotokion\b[^:\n]{0,60}[:\.]|Another\s+Theotokion\b[^:\n]{0,60}[:\.]|To\s+the\s+Cross\b[^:\n]{0,20}:|(?:Another\s+)?Kontakion\b[^:\n]{0,80}[:\.]|Ikos\b[^:\n]{0,60}[:\.]|(?:Another\s+)?Sessional\s+Hymn\b[^:\n]{0,80}[:\.]|Kathisma\b[^:\n]{0,60}[:\.]|Exapost[ei]larion\b[^:\n]{0,60}[:\.]|Photagogi[ck]on\b[^:\n]{0,60}[:\.]|Hymn\s+of\s+Light\b[^:\n]{0,60}[:\.]|Evangelical\s+Sticheron\b[^:\n]{0,60}[:\.]|Eothinon\b[^:\n]{0,60}[:\.]|Hypakoe\b[^:\n]{0,60}[:\.]|Ypako[eë]\b[^:\n]{0,60}[:\.]|Gradual\s+Hymn\b[^:\n]{0,60}[:\.]|Songs\s+of\s+Ascent\b[^:\n]{0,60}[:\.]|Antiphon\s+\d+\b[^:\n]{0,60}[:\.]|Martyri[ck]on\b[^:\n]{0,60}[:\.]|Triadi[ck]on\b[^:\n]{0,60}[:\.]|For\s+the\s+Departed\b[^:\n]{0,60}[:\.]|Hymn\s+for\s+the\s+Departed\b[^:\n]{0,60}[:\.]|Nekrosimon\b[^:\n]{0,60}[:\.]|Megalynarion\b[^:\n]{0,60}[:\.]|Sticheron\b[^:\n]{0,60}[:\.]|Idiomelon\b[^:\n]{0,60}[:\.]|Prosomoia\b[^:\n]{0,60}[:\.]|Tone\s+[1-8],\s*Podoben:)",
    re.IGNORECASE,
)
RE_NON_HYMN_RUBRIC_START = re.compile(
    r"^\*?(?:Note\s*:|Rubric\s*:|If\s+(?:a\s+forefeast|it\s+be\b|it\s+is\b|there\s+(?:is|be)\s+no\b|thou\s+wishest|however,\s+it\s+be|the\s+Feast\b|on\s+Saturday|on\s+Sunday)|Then\s+between\s+the\s+Nativity|(?:Then|And\s+then)\s*[,:]?\s*\*?\s*(?:Now\s+lettest|\"Now\s+lettest|It\s+is\s+truly\s+meet|\"It\s+is\s+truly\s+meet|Trisagion|the\s+Trisagion|Let\s+every\s+breath|Psalm\s+\d+|Alleluia|Lord,\s+have\s+mercy|we\s+sing\s+the\s+second\s+stasis|the\s+second\s+Choir|Little\s+Litany|Small\s+Litany|the\s+Ektenia|the\s+Deacon|the\s+Priest|the\s+Psalmist|this\s+Prayer|the\s+prayer|to\s+the\s+Saint\s+to\s+whom|at\s+the\s+Aposticha:\s+Idiomela)|Lord,\s+have\s+mercy\s*\(\d+|Then\s+the\s+same\s+day\s+at\s+evening,\s+being\s+the\s+first\s+day\s+of\s+the\s+week)\b",
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


def is_pure_italic_rubric(txt: str) -> bool:
    """
    Returns True if `txt` is a single-line or multi-line italic rubric (`*...*`),
    while returning False for:
      - Blocks containing plain non-italic body text (e.g. `*Ode 1:* Plain hymn... *Refrain.*`)
      - Two-span italic blocks where span 1 is a hymn role header and span 2 is a hymn body
        (e.g. `*Theotokion:* *O pure Mother of God...*` across 3,061 stanzas in the corpus)
      - Single-span italic blocks that start with an explicit hymn role + colon followed by
        a full hymn body (`>= 45` chars) that does not end with a colon (`:*`).
    """
    cleaned = re.sub(
        r"(?:\s*\[\^\d+\]|\s*\*?\((?:cont\.?|continued)\s+(?:on|from)\b[^)]*\)\*?)+",
        "",
        txt,
        flags=re.IGNORECASE,
    ).strip()
    if (cleaned.startswith("(*") and cleaned.endswith("*)")) or (
        cleaned.startswith("*(") and cleaned.endswith(")*")
    ) or (cleaned.startswith("*[") and cleaned.endswith("]*")):
        return True
    if not cleaned.startswith("*") or cleaned.startswith("**"):
        return False
    if not cleaned.endswith("*"):
        return False

    tokens = re.findall(r"\*\*[^*]+\*\*|\*[^*]+\*|[^*]+", cleaned)
    italic_spans: List[str] = []
    for tok in tokens:
        if tok.startswith("*") and tok.endswith("*") and not tok.startswith("**"):
            italic_spans.append(tok[1:-1].strip())
        elif tok.strip():
            # Non-whitespace plain text or bold text exists outside *...*
            return False

    if not italic_spans:
        return False

    if len(italic_spans) >= 2:
        first_span = f"*{italic_spans[0]}*"
        rest_joined = " ".join(italic_spans[1:]).strip()
        if (
            (RE_EXPLICIT_HYMN_START.match(first_span) or RE_STANDALONE_HYMN_ROLE.match(first_span))
            and len(rest_joined) >= 40
            and not rest_joined.endswith(":")
        ):
            return False

    single_inner = italic_spans[0]
    if len(italic_spans) == 1 and not single_inner.endswith(":"):
        m_role = RE_EXPLICIT_HYMN_START.match(f"*{single_inner}*")
        if m_role:
            remainder = single_inner[m_role.end() - 1 :].lstrip(" :.*")
            if (
                len(remainder) >= 45
                and not re.search(
                    r"\b(?:we\s+insert|we\s+sing|we\s+chant|are\s+sung|is\s+sung|see\s+in|twice|thrice)\b",
                    remainder[:80],
                    re.IGNORECASE,
                )
            ):
                return False

    return True


def _strip_combining(s: str) -> str:
    return re.sub(r"[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f\ufe20-\ufe2f]", "", s).lower()


def is_slavonic_standalone_role(s: str, plain: Optional[str] = None) -> bool:
    """
    Returns True if `s` is a standalone Slavonic hymn role / ode / heirmos header
    (e.g., 'Бг҃оро́диченъ:', 'Крⷭ҇тобг҃оро́диченъ.', 'И҆́нъ. І҆рмо́съ то́йже.', 'Пѣ́снь г҃. І҆рмо́съ:')
    that does NOT already contain the governed hymn body after a colon.
    """
    clean = s.strip()
    if not clean or len(clean) > 105:
        return False
    p = plain if plain is not None else _strip_combining(clean)
    if not (
        RE_SLAVONIC_STANDALONE_ROLE.match(clean)
        or re.match(
            r"^\*?(?:пѣснь\s+[^\n:]{1,40}(?:[іїи]рмосъ?)?|[іїи]рмос[аъ]?|[иії]н[ъы][\.,:]?\s*(?:канонъ?|[іїи]рмосъ?)|катавас[іи][ая]|тропар[ьия]|(?:богоро|бгоро)диченъ?|бц(?:енъ?|ѣ)|(?:кресто|крсто|крто)(?:богоро|бгоро)диченъ?|троиченъ?|м[ꙋу]чениченъ?|мертвенъ?|за\s+[ѹу]покой|кондакъ?|[иії]к[ѡо]съ?|с[ѣе]дал(?:енъ?|на)|[yѵу]пакои|св[ѣе]тиленъ?|ексапост[іи]лар[іи]й|степенна|ант[іи]ф[ѡо]нъ?)\b[^\n]{0,60}?[\.:]?\*?(?:\s*(?:\[\^\d+\])+)?$",
            p,
        )
    ):
        return False
    if len(clean) <= 38 or clean.endswith((":", ":*", ".*")):
        return True
    if ":" in clean:
        after_colon = clean.split(":", 1)[1].strip()
        after_plain = _strip_combining(after_colon)
        if (
            len(after_colon) >= 24
            and not after_colon.endswith((":", ":*"))
            and not re.match(
                r"^(?:[іїи]рмос|тойже|таже|гласъ|гл\b|подоб|под\b|канон|твореніе|пѣснь|богородичен|бгородичен)",
                after_plain,
            )
        ):
            return False
    return True


def strip_slavonic_leading_role_prefix(slav_text: str) -> str:
    """
    Strips leading chained or inline role/ode/doxology/podoben prefixes from a Slavonic
    hymn block so `slavonic_incipit` and `slavonic_stem_tier2` index the pure hymn body (Decision 2).
    """
    s = re.sub(r"^\[[^\]]+\]\s*", "", slav_text.strip()).strip()
    changed = True
    while changed and s:
        changed = False
        # Strip leading *Role:* or markdown bold/italic role tags
        m_star = re.match(r"^\*+([^\*\n]{1,75}?):?\*+\s*(.+)$", s)
        if m_star:
            hdr_p = _strip_combining(m_star.group(1))
            if re.match(
                r"^(?:пѣснь|[іїи]рмос|инъ|катавас|тропар|богородич|бгородич|бцен|крестобогородич|кртобгородич|кондак|[иі]кос|сѣдал|седал|свѣтил|ексапост|[ѵуy]пакои|степен|ант[іи]ф|слава|и\s+(?:нынѣ|ннѣ)|гласъ|подоб)",
                hdr_p,
            ):
                s = m_star.group(2).strip()
                changed = True
                continue
        # Strip plain-text leading role/doxology/ode/podoben header ending in colon or period
        m_lead = re.match(r"^([^\n]{2,95}?[:\.])\s+([А-ЯІЇЄҐѢѴѠꙊѦѪѮѰѲ\*].+)$", s)
        if m_lead:
            hdr_raw = m_lead.group(1).strip()
            hdr_p = _strip_combining(hdr_raw)
            if (
                is_slavonic_standalone_role(hdr_raw, hdr_p)
                or re.match(
                    r"^\*?(?:слава|и\s+(?:нынѣ|ннѣ)|пѣснь\s+[^\s]+|[іїи]рмос|инъ\s*[\.,:]?\s*(?:[іїи]рмос|канон)|богородич|бгородич|бцен|крестобогородич|крстобогородич|кртобогородич|троич|м[уꙋ]ченич|тропар|кондак|[иі]кос|сѣдал|седал|свѣтил|ексапост|[ѵуy]пакои|гласъ|гл\s*[:\.]|подоб)",
                    hdr_p,
                )
            ) and len(hdr_raw) <= 95:
                s = m_lead.group(2).strip()
                changed = True
                continue
    return s or slav_text.strip()


def parse_slavonic_numeral(raw_tok: str) -> Optional[int]:
    """Parses Slavonic Cyrillic letter numerals (а҃..ѳ҃), ordinal stems, or Arabic digits 1..9."""
    clean = _strip_combining(raw_tok).strip(".,:;()[]* ")
    if not clean:
        return None
    if clean.isdigit():
        val = int(clean)
        return val if 1 <= val <= 9 else None
    letter_map = {
        "а": 1, "в": 2, "г": 3, "д": 4, "е": 5,
        "ѕ": 6, "з": 7, "и": 8, "ѳ": 9, "і": 10,
    }
    if clean in letter_map:
        return letter_map[clean]
    stem_map = (
        ("перв", 1),
        ("втор", 2),
        ("трет", 3),
        ("четв", 4),
        ("пѧт", 5),
        ("пят", 5),
        ("шест", 6),
        ("седм", 7),
        ("осм", 8),
        ("осм", 8),
        ("дев", 9),
    )
    for prefix, num in stem_map:
        if clean.startswith(prefix):
            return num
    return None


RE_SLAVONIC_APPARATUS_BRACKET = re.compile(
    r"^\[(?:Колонка|Столбец|Column|Орнаментальн|Друкарськ|Дереворит|Гравійован|Заставка|Кінцівка|Фрагмент|Рукописний|Штамп|Запис|Каліграфічний|Нотатки|Жартівливий|Чистий\s+аркуш|Герб|Шестивіршний|Ставропігійське|Продовження|Кустод|Колонтитул|Fol\.?\s*[0-9]+|Листъ\s+[^\]]+|Стор\.?\s*\d+)[^\]]*\](?:\s*(?:\[\^\d+\])+)?$",
    re.IGNORECASE,
)

RE_SLAVONIC_RUBRIC_START = re.compile(
    r"^\*?(?:гласъ\b|гл\s*[:\.]|пѣснь\b|въ\s+(?:субботу|сꙋббѡтꙋ|недѣлю|понедѣльникъ|вторникъ|среду|средꙋ|четвертокъ|пятокъ|пѧтокъ|тойже\s+день)|в\s+(?:субботу|сꙋббѡтꙋ|недѣлю|понедѣльникъ|вторникъ|среду|средꙋ|четвертокъ|пятокъ|пѧтокъ|тойже\s+день)|на\s+(?:малѣй|велицѣй|вечерни|оутрени|ѹтрени|утрени|гди|господи|стиховнѣ|стіховнѣ|хвалитехъ|литургіи|літургіи|литіи|літіи)|по\s+[авгдеѕзиѳ1-9][,\.]?\s*(?:каѳісм|кадісм|ка\s*:|стихолог|стіхолог|стїхол|пѣсн)|таже\b|тат\s*:|посемъ\b|стихиры\b|стіхиры\b|стры\b|стрі\b|ины\s+(?:стихиры|стіхиры|стры|стрі|ст̃ры)|инны\s+(?:стихиры|стіхиры|стры|стрі|ст̃ры)|степенна\b|антифон|антіфон|прокимен|прокімен|всякое\s+дыханіе|всѧкое\s+дыханіе|еѵангеліе|еѵліе|канон|блаженна\b|отпустъ\b|ѿпустъ\b|ектенія\b|молитва\b|чтеніе\b|паремія\b|сінаѯар|синаѯар|премова\b|начало\s+съ\s+богомъ|подобен|подоб\s*:|подо\s*:|под\s*:|вечеръ,\s*вечеръ\s+на\s+гди|аще\s+ли\b|аще\s+же\b|егда\s+же\b|сице\b|подобаетъ\s+вѣдати|вѣдомо\s+да\s+есть|тогожде\s+мѣс|мѣсяца\b|мѣсѧца\b|память\b|памѧть\b|служба\b|слꙋжба\b|послѣдованіе\b|чинъ\b|уставъ\b|оуставъ\b|іерей\b|їерей\b|діакон\b|дїакон\b|ликъ\b|чтецъ\b)",
    re.IGNORECASE,
)


def is_slavonic_rubric_line(clean: str, plain: Optional[str] = None) -> bool:
    """Determines whether a Slavonic line/block is a liturgical rubric or heading."""
    s = clean.strip()
    if not s:
        return False
    if s.startswith("#") or (s.startswith("*") and s.endswith("*") and len(s) < 260):
        return True
    if s.startswith("[") and s.endswith("]") and len(s) < 180:
        return True
    if len(s) >= 220:
        return False
    p = plain if plain is not None else _strip_combining(s)
    if is_slavonic_standalone_role(s, p):
        return True
    if re.match(r"^\*?(?:слава|и\s+(?:нынѣ|ннѣ))\b", p) and (len(s) < 90 or s.endswith(":")):
        return True
    if RE_SLAVONIC_RUBRIC_START.match(p):
        if len(s) < 125 or s.endswith(":") or re.search(r"\b(?:гласъ|гл\s*[:\.]|подоб|под\s*:|стїхол|стихолог|шестопсалм|ѿпущаеши|воцарися)\b", p):
            return True
    return False


def _split_inline_slavonic_stanza_markers(blk: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Splits a Slavonic block that contains multiple stanzas separated on the same line by
    early-print/manuscript terminators (`:~`, `:-`, `:–`) + role/capital or inline `*Role:*` tags.
    """
    txt = blk["text"].strip()
    if len(txt) < 65 or txt.startswith(("#", "|", "[")):
        return [blk]

    # 1. Split at inline markdown *Role:* tags (e.g. 1600s Prykarpattia MS Octoechos `*Тропарь:*`, `*Богородиченъ:*`)
    parts = re.split(
        r"\s+(?=\*(?:Тропа[\u0300-\u036f\u0483-\u0489]*р[ьи]|Богоро[\u0300-\u036f\u0483-\u0489]*диченъ?|Бг҃оро́диченъ?|[ІЇИ][\u0300-\u036f\u0483-\u0489]*рмо[\u0300-\u036f\u0483-\u0489]*съ?|Слава|И\s+нынѣ|Инъ|Конда[\u0300-\u036f\u0483-\u0489]*къ?|[ІИ]косъ?|Сѣда[\u0300-\u036f\u0483-\u0489]*ленъ?)[^\*]{0,40}:\*)",
        txt,
    )
    if len(parts) == 1 and (":~" in txt or ":-" in txt or ":–" in txt):
        # 2. Split at early-print `:~\s+` / `:-\s+` stanza terminators when followed by a capital letter or role
        cand_parts = re.split(r"(?<=:~|:-|:\u2013)\s+(?=[А-ЯІЇЄҐѢѴѠꙊѦѪѮѰѲ\*])", txt)
        if len(cand_parts) >= 2 and all(len(cp.strip()) >= 22 for cp in cand_parts):
            parts = cand_parts

    if len(parts) <= 1:
        return [blk]

    out: List[Dict[str, Any]] = []
    total_k = len(parts)
    for idx, p_txt in enumerate(parts, start=1):
        p_clean = p_txt.strip()
        if not p_clean:
            continue
        prov = dict(blk["provenance"]) if blk.get("provenance") else None
        if prov is not None and total_k > 1:
            prov["slice_index"] = idx
            prov["slice_total"] = total_k
        out.append({
            **blk,
            "text": p_clean,
            "alignment_method": "SUB_SLICED_1_TO_K",
            "provenance": prov,
        })
    return out if out else [blk]


def parse_slavonic_blocks_by_leaf(
    source_dir: Path,
    ws_dir: Path,
    english_cross_leaf_starts: Optional[Set[int]] = None,
) -> Dict[int, List[Dict[str, Any]]]:
    """
    Loads Slavonic/Ukrainian source blocks indexed by physical leaf number with full
    SGC-02 TEXT_LINES provenance (source_file, source_sha256, start_line, end_line,
    verbatim_source), symmetric block splitting, milestone stripping, role chaining,
    and cross-column/cross-leaf continuation stitching.
    """
    by_leaf: Dict[int, List[Dict[str, Any]]] = {}
    s_files = (
        sorted(
            source_dir.glob("*source.txt"),
            key=lambda p: int(re.search(r"cohort0?(\d+)", p.name, re.IGNORECASE).group(1))
            if re.search(r"cohort0?(\d+)", p.name, re.IGNORECASE)
            else 9999,
        )
        if source_dir.exists()
        else []
    )

    if s_files:
        all_raw_blocks: List[Dict[str, Any]] = []
        file_lines_map: Dict[str, List[str]] = {}
        for sf in s_files:
            raw_bytes = sf.read_bytes()
            file_sha256 = hashlib.sha256(raw_bytes).hexdigest()
            rel_path = f"Translation/{sf.resolve().relative_to(PROJECT_ROOT).as_posix()}"
            text = raw_bytes.decode("utf-8-sig", errors="ignore")
            lines = text.splitlines()
            file_lines_map[rel_path] = lines

            m_c = re.search(r"cohort0?(\d+)", sf.name, re.IGNORECASE)
            curr_leaf = (int(m_c.group(1)) - 1) * 10 + 1 if m_c else 1

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
                            s_plain = _strip_combining(s)
                            prev_plain = _strip_combining(prev_s)
                            starts_block = (
                                s.startswith("===")
                                or s.startswith("#")
                                or s.startswith("**")
                                or s.startswith(">")
                                or s.startswith("*")
                                or s.startswith("[")
                                or s.startswith("|")
                                or s == "---"
                                or is_slavonic_standalone_role(s, s_plain)
                                or is_slavonic_rubric_line(s, s_plain)
                                or bool(
                                    re.match(
                                        r"^(?:гласъ|пѣснь|слава|и\s+(?:нынѣ|ннѣ)|стихъ?|стіхъ?|припѣвъ?|подобенъ?|їрмосъ?|ірмосъ?|инъ\b|тропарь|богородиченъ?|бгородиченъ?|крестобогородиченъ?|кртобгородиченъ?|кондакъ?|икосъ?|ікосъ?)\b",
                                        s_plain,
                                    )
                                )
                            )
                            s_cased = re.sub(r"[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]", "", s)
                            prev_complete = (
                                prev_s.startswith("===")
                                or prev_s.startswith("#")
                                or prev_s.startswith("|")
                                or prev_s == "---"
                                or (prev_s.startswith("*") and bool(re.search(r"\*(?:\s*\[\^\d+\])*$", prev_s)))
                                or (prev_s.startswith("[") and bool(re.search(r"\](?:\s*\[\^\d+\])*$", prev_s)))
                                or is_slavonic_standalone_role(prev_s, prev_plain)
                                or is_slavonic_rubric_line(prev_s, prev_plain)
                                or bool(re.search(r"(?:[\.!\?:\"\*\u201d\u00bb\];\u00b7\u0387]|:[~\-–\.]|\.~)(?:\s*\[\^\d+\])*$", prev_s))
                                or (
                                    len(prev_s) >= 35
                                    and not prev_s.endswith(("-", "‐", ","))
                                    and bool(re.match(r"^[А-ЯІЇЄҐѢѴѠꙊѦѪѮѰѲA-Z]", s_cased))
                                )
                            )
                            if starts_block or prev_complete:
                                para_tuples.append((cur_start, l_idx - 1, cur_lines))
                                cur_lines = []
                    if not cur_lines:
                        cur_start = l_idx
                    cur_lines.append(raw_ln)
            if cur_lines:
                para_tuples.append((cur_start, len(lines), cur_lines))

            pending_role: Optional[str] = None
            pending_start: Optional[int] = None

            for p_start, p_end, p_lines in para_tuples:
                surviving: List[str] = []
                for raw_l in p_lines:
                    sl = raw_l.strip()
                    m_lf = RE_LEAF_BANNER.match(sl)
                    if m_lf:
                        curr_leaf = int(m_lf.group(1))
                        pending_role = None
                        pending_start = None
                        continue
                    if (
                        RE_2UP_MILESTONE.match(sl)
                        or RE_COLUMN_MARKER.match(sl)
                        or RE_RUNNING_HEADER_BRACKET.match(sl)
                        or RE_CONTINUATION_BRACKET.match(sl)
                        or RE_SLAVONIC_APPARATUS_BRACKET.match(sl)
                        or RE_WOODCUT_INITIAL.match(sl)
                        or sl == "---"
                        or re.match(r"^\s*\[\^\d+\]:", sl)
                    ):
                        continue
                    surviving.append(raw_l)

                if not surviving:
                    continue

                joined = " ".join(l.strip() for l in surviving).strip()
                if not joined:
                    continue

                if len(surviving) == 1 and is_slavonic_standalone_role(joined) and len(joined) <= 105:
                    if pending_role:
                        pending_role = f"{pending_role} {joined}"
                    else:
                        pending_role = joined
                    if pending_start is None:
                        pending_start = p_start
                    continue

                if pending_role:
                    role_p = _strip_combining(pending_role)
                    is_antiphon_hdr = role_p.startswith(("степенна", "антифон", "антіфон"))
                    if not joined.startswith("#") and (not is_slavonic_rubric_line(joined) or not is_antiphon_hdr):
                        # If joined is itself a short Podoben/Tone rubric line before the stanza, chain both
                        if (
                            not is_antiphon_hdr
                            and len(surviving) == 1
                            and len(joined) < 85
                            and joined.endswith(":")
                            and is_slavonic_rubric_line(joined)
                        ):
                            pending_role = f"{pending_role} {joined}"
                            continue
                        joined = f"{pending_role} {joined}"
                    pending_role = None

                actual_start = pending_start if pending_start is not None else p_start
                pending_start = None
                verbatim_slice = "\n".join(lines[actual_start - 1 : p_end]).strip()[:1200]

                base_blk = {
                    "leaf": curr_leaf,
                    "text": joined,
                    "provenance": {
                        "source_file": rel_path,
                        "source_sha256": file_sha256,
                        "source_format": "TEXT_LINES",
                        "start_line": actual_start,
                        "end_line": p_end,
                        "verbatim_source": verbatim_slice,
                    },
                }
                for sub_blk in _split_inline_slavonic_stanza_markers(base_blk):
                    all_raw_blocks.append(sub_blk)

        # Stitch mid-sentence Slavonic continuations across columns/leaves
        stitched_slav: List[Dict[str, Any]] = []
        for blk in all_raw_blocks:
            txt = blk["text"]
            if stitched_slav and not txt.startswith("#") and not stitched_slav[-1]["text"].startswith("#"):
                prev = stitched_slav[-1]
                prev_txt = re.sub(r"(?:\s*\[\^\d+\]|\*)+$", "", prev["text"]).rstrip()
                prev_plain = _strip_combining(prev_txt)
                curr_probe = _strip_combining(re.sub(r"^\*+", "", txt).lstrip())
                prev_is_rub = is_slavonic_rubric_line(prev_txt, prev_plain) or bool(
                    re.match(r"^\*?(?:стихъ?|стіхъ?|припѣвъ?)\b", prev_plain)
                )
                curr_is_rub = is_slavonic_rubric_line(txt, curr_probe) or bool(
                    re.match(r"^\*?(?:стихъ?|стіхъ?|припѣвъ?)\b", curr_probe)
                )
                curr_probe_cased = re.sub(r"[\u0300-\u036f\u0483-\u0489\u2de0-\u2dff\ua670-\ua69f]", "", re.sub(r"^\*+", "", txt).lstrip())
                intervening_milestone_or_cont = (
                    blk["leaf"] > prev["leaf"]
                    or blk["provenance"]["start_line"] > prev["provenance"]["end_line"] + 1
                    or prev_txt.endswith(("-", "‐", ","))
                    or bool(re.match(r"^[а-яіїєґѣѵѡꙋѧѫѯѱѳa-z]", curr_probe_cased))
                )
                is_prev_open = (
                    not prev_is_rub
                    and intervening_milestone_or_cont
                    and (
                        prev_txt.endswith(",")
                        or prev_txt.endswith("-")
                        or prev_txt.endswith("...")
                        or prev_txt.endswith("…")
                        or not bool(re.search(r"(?:[\.!\?:;\]\)\"\u00bb\u00b7\u0387~]|:[~\-–\.]|\.~)$", prev_txt))
                    )
                )
                starts_new_slav_unit = (
                    curr_is_rub
                    or bool(
                        re.match(
                            r"^(?:гласъ|пѣснь|слава|и\s+(?:нынѣ|ннѣ)|стихъ?|стіхъ?|припѣвъ?|подобенъ?|їрмосъ?|ірмосъ?|инъ\b|тропарь|богородиченъ?|бгородиченъ?|крестобогородиченъ?|кртобгородиченъ?|кондакъ?|икосъ?|ікосъ?|въ\s+|на\s+|по\s+|мѣсѧц|сінаѯар|чтеніе)\b",
                            curr_probe,
                        )
                    )
                    or txt.startswith("[")
                )
                if (
                    blk["leaf"] >= prev["leaf"]
                    and (blk["leaf"] - prev["leaf"]) <= 1
                    and is_prev_open
                    and not starts_new_slav_unit
                    and len(prev_txt) >= 25
                ):
                    # If crossing a leaf boundary where the English cohort did not stitch across the leaf,
                    # attach only a short carry-over tail to prev["leaf"] and never swallow the entire new leaf (Bug 2).
                    if (
                        blk["leaf"] > prev["leaf"]
                        and english_cross_leaf_starts is not None
                        and prev["leaf"] not in english_cross_leaf_starts
                    ):
                        m_carry = re.match(
                            r"^([^\.!\?;\u00b7\u0387]{1,55}(?:[\.!\?;\u00b7\u0387]|:[~\-–\.]))\s+([А-ЯІЇЄҐѢѴѠꙊѦѪѮѰѲA-Z\*].*)$",
                            txt.strip(),
                        )
                        if m_carry and len(m_carry.group(2).strip()) >= 18:
                            prev["text"] = f"{prev['text'].rstrip()} {m_carry.group(1).strip()}"
                            if prev["provenance"]["source_file"] == blk["provenance"]["source_file"]:
                                prev["provenance"]["end_line"] = blk["provenance"]["end_line"]
                                f_lines = file_lines_map.get(prev["provenance"]["source_file"], [])
                                if f_lines:
                                    s_ln = prev["provenance"]["start_line"]
                                    e_ln = prev["provenance"]["end_line"]
                                    prev["provenance"]["verbatim_source"] = "\n".join(
                                        f_lines[s_ln - 1 : e_ln]
                                    ).strip()[:1200]
                            blk["text"] = m_carry.group(2).strip()
                            stitched_slav.append(blk)
                            continue
                        # Hard leaf-conservation guard: do not swallow blk's leaf into prev["leaf"]
                        stitched_slav.append(blk)
                        continue

                    prev["text"] = f"{prev['text'].rstrip()} {txt.lstrip()}"
                    if prev["provenance"]["source_file"] == blk["provenance"]["source_file"]:
                        prev["provenance"]["end_line"] = blk["provenance"]["end_line"]
                        f_lines = file_lines_map.get(prev["provenance"]["source_file"], [])
                        if f_lines:
                            s_ln = prev["provenance"]["start_line"]
                            e_ln = prev["provenance"]["end_line"]
                            prev["provenance"]["verbatim_source"] = "\n".join(f_lines[s_ln - 1 : e_ln]).strip()[:1200]
                    continue
            stitched_slav.append(blk)

        for blk in stitched_slav:
            by_leaf.setdefault(blk["leaf"], []).append(blk)

    elif (ws_dir / "Ukrainian TXTs").exists():
        # Monument 0 fallback with full TEXT_LINES provenance and deterministic part-key matching
        def _mon0_part_key(fname: str) -> Tuple[int, str]:
            low_f = fname.lower()
            if "intro" in low_f:
                return (1, low_f)
            m_p = re.search(r"part\s*0?(\d+)", low_f)
            if m_p:
                return (1 + int(m_p.group(1)), low_f)
            if "appendix" in low_f:
                return (90, low_f)
            return (50, low_f)

        u_files = sorted(
            [
                uf
                for uf in (ws_dir / "Ukrainian TXTs").glob("*.txt")
                if "footnote" not in uf.name.lower()
            ],
            key=lambda p: _mon0_part_key(p.name),
        )
        for idx, uf in enumerate(u_files, start=1):
            raw_bytes = uf.read_bytes()
            file_sha256 = hashlib.sha256(raw_bytes).hexdigest()
            rel_path = f"Translation/{uf.resolve().relative_to(PROJECT_ROOT).as_posix()}"
            lines = raw_bytes.decode("utf-8-sig", errors="ignore").splitlines()
            curr_leaf = (idx - 1) * 10 + 1
            leaf_blks: List[Dict[str, Any]] = []
            cur_start = 1
            cur_lines: List[str] = []
            for l_idx, raw_ln in enumerate(lines, start=1):
                s = raw_ln.strip()
                if not s:
                    if cur_lines:
                        joined = "\n".join(l.strip() for l in cur_lines).strip()
                        if not joined.startswith("#") and joined != "---":
                            leaf_blks.append({
                                "leaf": curr_leaf,
                                "text": joined,
                                "provenance": {
                                    "source_file": rel_path,
                                    "source_sha256": file_sha256,
                                    "source_format": "TEXT_LINES",
                                    "start_line": cur_start,
                                    "end_line": l_idx - 1,
                                    "verbatim_source": "\n".join(lines[cur_start - 1 : l_idx - 1]).strip()[:1200],
                                },
                            })
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
                            )
                            prev_complete = (
                                prev_s.startswith("===")
                                or prev_s.startswith("#")
                                or prev_s.startswith("|")
                                or prev_s == "---"
                                or (prev_s.startswith("*") and bool(re.search(r"\*(?:\s*\[\^\d+\])*$", prev_s)))
                                or (prev_s.startswith("[") and bool(re.search(r"\](?:\s*\[\^\d+\])*$", prev_s)))
                                or bool(re.search(r"[\.!\?:\"\*\u201d\u00bb\]](?:\s*\[\^\d+\])*$", prev_s))
                            )
                            if starts_block or prev_complete:
                                joined = "\n".join(l.strip() for l in cur_lines).strip()
                                if not joined.startswith("#") and joined != "---":
                                    leaf_blks.append({
                                        "leaf": curr_leaf,
                                        "text": joined,
                                        "provenance": {
                                            "source_file": rel_path,
                                            "source_sha256": file_sha256,
                                            "source_format": "TEXT_LINES",
                                            "start_line": cur_start,
                                            "end_line": l_idx - 1,
                                            "verbatim_source": "\n".join(lines[cur_start - 1 : l_idx - 1]).strip()[:1200],
                                        },
                                    })
                                cur_lines = []
                    if not cur_lines:
                        cur_start = l_idx
                    cur_lines.append(raw_ln)
            if cur_lines:
                joined = "\n".join(l.strip() for l in cur_lines).strip()
                if not joined.startswith("#") and joined != "---":
                    leaf_blks.append({
                        "leaf": curr_leaf,
                        "text": joined,
                        "provenance": {
                            "source_file": rel_path,
                            "source_sha256": file_sha256,
                            "source_format": "TEXT_LINES",
                            "start_line": cur_start,
                            "end_line": len(lines),
                            "verbatim_source": "\n".join(lines[cur_start - 1 :]).strip()[:1200],
                        },
                    })
            by_leaf[curr_leaf] = leaf_blks

    return by_leaf


def parse_slavonic_by_leaf(source_dir: Path, ws_dir: Path) -> Dict[int, List[str]]:
    """Backward-compatible helper returning Slavonic paragraph strings by physical leaf."""
    blocks_by_leaf = parse_slavonic_blocks_by_leaf(source_dir, ws_dir)
    return {lf: [b["text"] for b in blks] for lf, blks in blocks_by_leaf.items()}


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
        def _mon0_eng_part_key(fname: str) -> Tuple[int, str]:
            low_f = fname.lower()
            if "intro" in low_f:
                return (1, low_f)
            m_p = re.search(r"part\s*0?(\d+)", low_f)
            if m_p:
                return (1 + int(m_p.group(1)), low_f)
            if "appendix" in low_f:
                return (90, low_f)
            return (50, low_f)

        part_files = sorted(
            [
                pf
                for pf in final_dir.glob("*.txt")
                if "footnote" not in pf.name.lower()
            ],
            key=lambda p: _mon0_eng_part_key(p.name),
        )
        for idx, pf in enumerate(part_files, start=1):
            input_files.append((idx, pf))

    raw_blocks: List[Dict[str, Any]] = []
    file_lines_map: Dict[str, List[str]] = {}

    for c_idx, fpath in input_files:
        raw_bytes = fpath.read_bytes()
        file_sha256 = hashlib.sha256(raw_bytes).hexdigest()
        rel_path = f"Translation/{fpath.resolve().relative_to(PROJECT_ROOT).as_posix()}"
        text = raw_bytes.decode("utf-8-sig", errors="ignore")
        lines = text.splitlines()
        file_lines_map[rel_path] = lines

        curr_leaf = (c_idx - 1) * 10 + 1
        curr_locus = f"f. {curr_leaf - folio_offset}r" if (folio_offset and curr_leaf > folio_offset) else f"p{curr_leaf}"
        curr_running_header: Optional[str] = None

        # Group lines into logical blocks with exact 1-based (start_line, end_line).
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
                            or bool(RE_PLAIN_SERVICE_RUBRIC_HEADER.match(s))
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
                            or bool(RE_PLAIN_SERVICE_RUBRIC_HEADER.match(prev_s))
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

        # Pending stacked prefix state
        pending_prayer_title: Optional[str] = None
        pending_delivery_mode: Optional[str] = None
        pending_speaker: Optional[str] = None
        pending_woodcut_initial: Optional[str] = None
        pending_hymn_role: Optional[str] = None
        pending_start_line: Optional[int] = None
        pending_rescued_footnotes: List[str] = []

        for p_start, p_end, p_lines in para_tuples:
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
                    pending_rescued_footnotes.extend(re.findall(r"\[\^\d+\]", sl))
                    continue

                if RE_COLUMN_MARKER.match(sl) or RE_CONTINUATION_BRACKET.match(sl):
                    pending_rescued_footnotes.extend(re.findall(r"\[\^\d+\]", sl))
                    continue

                m_rh = RE_RUNNING_HEADER_BRACKET.match(sl)
                if m_rh:
                    if m_rh.group(1):
                        curr_locus = f"f. {m_rh.group(1)}"
                    curr_running_header = m_rh.group(2).strip()
                    pending_rescued_footnotes.extend(re.findall(r"\[\^\d+\]", sl))
                    continue

                if RE_SHORT_RUNNING_TITLE.match(sl):
                    curr_running_header = sl.strip("* .")
                    pending_rescued_footnotes.extend(re.findall(r"\[\^\d+\]", sl))
                    continue

                m_wc = RE_WOODCUT_INITIAL.match(sl)
                if m_wc:
                    if m_wc.group(1):
                        curr_locus = f"f. {m_wc.group(1)}"
                    pending_woodcut_initial = m_wc.group(2).upper()
                    if pending_start_line is None:
                        pending_start_line = p_start
                    pending_rescued_footnotes.extend(re.findall(r"\[\^\d+\]", sl))
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
                    continue

                if RE_PRAYER_HEADER_RUBRIC.match(joined_text):
                    pending_prayer_title = joined_text.strip("* :")
                    if "secret" in joined_text.lower() or "mystically" in joined_text.lower():
                        pending_delivery_mode = "SECRET"
                    elif "aloud" in joined_text.lower() or "loudly" in joined_text.lower():
                        pending_delivery_mode = "ALOUD"
                    if pending_start_line is None:
                        pending_start_line = p_start
                    continue

                if (
                    RE_STANDALONE_HYMN_ROLE.match(joined_text)
                    and len(joined_text) <= 180
                    and len(joined_text.split()) <= 20
                    and bool(re.search(r"(?::\*?|\.\*?|\])\s*(?:\[\^\d+\])*$", joined_text))
                ):
                    role_norm = joined_text if joined_text.startswith("*") else f"*{joined_text.strip('* ')}*"
                    if pending_hymn_role:
                        pending_hymn_role = f"{role_norm} {pending_hymn_role}"
                    else:
                        pending_hymn_role = role_norm
                    if pending_start_line is None:
                        pending_start_line = p_start
                    continue

            if pending_hymn_role:
                if not joined_text.startswith("#"):
                    joined_text = f"{pending_hymn_role} {joined_text}"
                pending_hymn_role = None

            if pending_rescued_footnotes:
                for fn_tok in pending_rescued_footnotes:
                    if fn_tok not in joined_text:
                        joined_text = f"{joined_text} {fn_tok}"
                pending_rescued_footnotes = []

            actual_start = pending_start_line if pending_start_line is not None else p_start
            verbatim_slice = "\n".join(lines[actual_start - 1 : p_end]).strip()[:1200]

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
                    "verbatim_source": verbatim_slice,
                },
            })

            pending_prayer_title = None
            pending_delivery_mode = None
            pending_speaker = None
            pending_woodcut_initial = None
            pending_hymn_role = None
            pending_start_line = None

    # Cross-leaf / cross-column mid-sentence continuation stitcher
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
            prev_base = re.sub(
                r"(?:\s*\[\^\d+\]|\s*\*?\((?:cont\.?|continued)\s+(?:on|from)\b[^)]*\)\*?)+$",
                "",
                prev["text"],
                flags=re.IGNORECASE,
            ).rstrip()
            prev_txt = re.sub(r"\*+$", "", prev_base).rstrip()
            curr_clean = re.sub(r"^\*\*[A-Za-z]+\s+\(continued\):\*\*\s*", "", txt, flags=re.IGNORECASE)
            curr_clean = re.sub(r"^\[continues[^\]]*\]\s*", "", curr_clean, flags=re.IGNORECASE)
            curr_clean = re.sub(
                r"^\*?\((?:cont\.?|continued)\s+(?:on|from)\b[^)]*\)\*?\s*",
                "",
                curr_clean,
                flags=re.IGNORECASE,
            )
            curr_probe = re.sub(r"^\*+", "", curr_clean).lstrip()

            unclosed_quote = (
                prev_txt.startswith('"')
                and not prev_txt.endswith('"')
                and not curr_probe.startswith('"')
                and curr_probe.endswith('"')
            )
            starts_new_unit = not bool(re.match(r"^[a-z]", curr_clean)) and (
                curr_clean.startswith(("#", "[", "|", "**"))
                or bool(RE_EXPLICIT_HYMN_START.match(curr_clean))
                or bool(RE_STANDALONE_HYMN_ROLE.match(curr_clean))
                or bool(RE_VERSE_HEADER.match(curr_clean))
                or bool(RE_PODOBEN_HEADER.match(curr_clean))
                or bool(RE_SECTION_RUBRIC_CUE.match(curr_clean))
                or bool(RE_PLAIN_SERVICE_RUBRIC_HEADER.match(curr_clean))
                or bool(
                    re.match(
                        r"^\*?(?:Glory|Both\s+now|Tone\s+[1-8]|Ode\s+[1-9]|Canticle\s+[1-9]|At\s+|On\s+|In\s+the\s+|After\s+)\b",
                        curr_clean,
                        re.IGNORECASE,
                    )
                )
            )
            lowercase_cont = (
                bool(re.match(r"^[a-z]", curr_probe))
                and not starts_new_unit
                and not is_pure_italic_rubric(prev["text"])
            )
            is_prev_open = (
                prev_txt.endswith("...")
                or prev_txt.endswith("…")
                or prev_txt.endswith(",")
                or prev_txt.endswith(";")
                or prev_txt.endswith(":")
                or prev_txt.endswith("-")
                or unclosed_quote
                or lowercase_cont
                or bool(re.search(r"[a-z]$", prev_txt))
            )
            is_curr_cont = (
                curr_probe.startswith("...")
                or curr_probe.startswith("…")
                or lowercase_cont
                or unclosed_quote
                or "(continued)" in txt[:35].lower()
                or (
                    bool(re.search(r"[a-z]$", prev_txt))
                    and not starts_new_unit
                    and (not is_pure_italic_rubric(curr_clean) or is_pure_italic_rubric(prev["text"]))
                )
            )
            if blk["leaf"] >= prev["leaf"] and (blk["leaf"] - prev["leaf"]) <= 1 and is_prev_open and is_curr_cont:
                merged_prev = re.sub(r"(?:\.\.\.|…)\s*$", "", prev_base).rstrip()
                merged_curr = re.sub(r"^(?:\.\.\.|…)\s*", "", curr_clean).lstrip()
                if lowercase_cont and merged_prev.endswith('."') and merged_curr.endswith('"') and not merged_curr.startswith('"'):
                    merged_prev = merged_prev[:-2]
                # If both halves are wrapped in *...*, merge cleanly without an internal ** seam
                m_prev_fns = re.search(r"(\*(?:\s*\[\^\d+\])*)$", merged_prev)
                if m_prev_fns and merged_curr.startswith("*") and not merged_curr.startswith("**"):
                    fns_only = re.findall(r"\[\^\d+\]", m_prev_fns.group(1))
                    base_prev = merged_prev[: m_prev_fns.start()].rstrip()
                    inner_curr = merged_curr[1:].lstrip()
                    combined = f"{base_prev} {inner_curr}"
                    for fn_t in fns_only:
                        if fn_t not in combined:
                            combined = f"{combined} {fn_t}"
                    prev["text"] = combined
                else:
                    prev["text"] = f"{merged_prev} {merged_curr}"
                leaf_tag = f"p{blk['leaf']}"
                if leaf_tag not in prev["leaf_span"]:
                    prev["leaf_span"].append(leaf_tag)
                if prev["provenance"]["source_file"] == blk["provenance"]["source_file"]:
                    prev["provenance"]["end_line"] = blk["provenance"]["end_line"]
                    f_lines = file_lines_map.get(prev["provenance"]["source_file"], [])
                    if f_lines:
                        s_ln = prev["provenance"]["start_line"]
                        e_ln = prev["provenance"]["end_line"]
                        prev["provenance"]["verbatim_source"] = "\n".join(f_lines[s_ln - 1 : e_ln]).strip()[:1200]
                    else:
                        comb_v = prev["provenance"]["verbatim_source"] + "\n" + blk["provenance"]["verbatim_source"]
                        prev["provenance"]["verbatim_source"] = comb_v[:1200]
                continue

        stitched_blocks.append(blk)

    return stitched_blocks


def classify_alignment_anchor(txt: str, is_slavonic: bool) -> Dict[str, Any]:
    """
    Extracts structural alignment anchors and block kind (EDITORIAL_SKIP, APPARATUS, RUBRIC, BODY)
    for Needleman-Wunsch bilingual leaf alignment (T-1).
    """
    clean = re.sub(
        r"(?:\s*\[\^\d+\]|\s*\*?\((?:cont\.?|continued)\s+(?:on|from)\b[^)]*\)\*?)+",
        "",
        txt,
        flags=re.IGNORECASE,
    ).strip()
    first_ln = clean.splitlines()[0].strip() if clean else ""
    plain = _strip_combining(first_ln)

    if (
        not clean
        or (clean.startswith("[") and is_slavonic and RE_SLAVONIC_APPARATUS_BRACKET.match(clean))
        or clean.startswith("*(")
        or clean.startswith("(*")
        or re.match(
            r"^\*?\[?(?:Note:|Editorial\s+Note:|Translator'?s?\s+Note:|Примѣчаніе:|Примітка:|Кустод:|Catchword:|Vacat\b)",
            clean,
            re.IGNORECASE,
        )
    ):
        return {
            "kind": "EDITORIAL_SKIP",
            "ode_num": None,
            "tone_num": None,
            "doxology": None,
            "is_stichos": False,
            "is_podoben": False,
            "role_tag": None,
            "length": len(clean),
            "propagated_dox": False,
        }

    if (clean.startswith("[") and clean.endswith("]")) or (clean.startswith("*[") and clean.endswith("]*")):
        return {
            "kind": "APPARATUS",
            "ode_num": None,
            "tone_num": None,
            "doxology": None,
            "is_stichos": False,
            "is_podoben": False,
            "role_tag": None,
            "length": len(clean),
            "propagated_dox": False,
        }

    ode_num: Optional[int] = None
    tone_num: Optional[int] = None
    doxology: Optional[str] = None
    is_stichos = False
    is_podoben = False
    role_tag: Optional[str] = None

    if is_slavonic:
        m_ode = re.search(r"\bпѣснь\s+([^\s\.,:;*]+)", plain)
        if m_ode and not plain.startswith("по "):
            ode_num = parse_slavonic_numeral(m_ode.group(1))
        m_tone = re.search(r"\b(?:гласъ|гл\s*[:\.]?)\s+([^\s\.,:;*]+)", plain)
        if m_tone:
            t_v = parse_slavonic_numeral(m_tone.group(1))
            if t_v and 1 <= t_v <= 8:
                tone_num = t_v
        if re.match(r"^\*?(?:слава\s*[:,\.]?\s*и\s+(?:нынѣ|ннѣ)|слава\s+и\s+(?:нынѣ|ннѣ))\b", plain):
            doxology = "GLORY_BOTH"
        elif re.match(r"^\*?слава\b", plain):
            doxology = "GLORY"
        elif re.match(r"^\*?и\s+(?:нынѣ|ннѣ)\b", plain):
            doxology = "NOW"
        if re.match(r"^\*?(?:стихъ?|стіхъ?|припѣвъ?)\b", plain):
            is_stichos = True
        if "подоб" in plain or "подо:" in plain or "под:" in plain or "самоглас" in plain:
            is_podoben = True
        if "їрмос" in plain or "ірмос" in plain or "ирмос" in plain:
            role_tag = "HEIRMOS"
        elif (
            "богородичен" in plain
            or "богор:" in plain
            or "бгородичен" in plain
            or "бго:" in plain
            or "бцен" in plain
            or "крестобогородичен" in plain
            or "крстобгородичен" in plain
            or "кртобгородичен" in plain
        ):
            role_tag = "THEOTOKION"
        elif "кондак" in plain:
            role_tag = "KONTAKION"
        elif "икос" in plain or "ікос" in plain:
            role_tag = "IKOS"
        elif "сѣдал" in plain or "седал" in plain:
            role_tag = "SESSIONAL"
        elif "свѣтил" in plain or "светил" in plain or "ексапостілар" in plain or "ексапостилар" in plain:
            role_tag = "EXAPOSTILARION"

        is_slav_rubric = is_slavonic_rubric_line(clean, plain) or (
            is_podoben and len(clean) < 160 and ":" in clean[-10:]
        ) or (ode_num is not None and len(clean) < 80 and role_tag is None)
        kind = "RUBRIC" if is_slav_rubric else "BODY"
    else:
        m_ode = re.match(r"^\*{0,2}(?:Ode|Canticle)\s+([1-9])\b", first_ln, re.IGNORECASE)
        if m_ode:
            ode_num = int(m_ode.group(1))
        m_tone = re.search(r"\bTone\s+([1-8])\b", first_ln, re.IGNORECASE)
        if m_tone:
            tone_num = int(m_tone.group(1))
        if re.match(r"^\*{0,2}(?:Glory[^\n]{0,45}Both\s+now)\b", first_ln, re.IGNORECASE):
            doxology = "GLORY_BOTH"
        elif re.match(r"^\*{0,2}Glory(?:\s+to\s+the\s+Father\b|\s*\.\.\.|\s*:|\s*,|\b)", first_ln, re.IGNORECASE):
            doxology = "GLORY"
        elif re.match(r"^\*{0,2}Both\s+now\b", first_ln, re.IGNORECASE):
            doxology = "NOW"
        if RE_VERSE_HEADER.match(first_ln):
            is_stichos = True
        if "podoben:" in plain or "idiomelon" in plain or "automelon" in plain:
            is_podoben = True
        if "heirmos" in plain:
            role_tag = "HEIRMOS"
        elif "theotokion" in plain:
            role_tag = "THEOTOKION"
        elif "kontakion" in plain:
            role_tag = "KONTAKION"
        elif "ikos" in plain:
            role_tag = "IKOS"
        elif "sessional" in plain or "kathisma" in plain:
            role_tag = "SESSIONAL"
        elif "exapost" in plain or "photagog" in plain or "hymn of light" in plain:
            role_tag = "EXAPOSTILARION"

        is_short_header_cue = (
            len(clean) < 68
            and (doxology is not None or role_tag is not None or ode_num is not None)
            and bool(re.search(r"(?::\*?|\.\*?)\s*$", clean))
        )
        is_eng_rubric = (
            clean.startswith("#")
            or (clean.startswith("**") and clean.endswith("**") and len(clean) < 160)
            or is_pure_italic_rubric(clean)
            or bool(RE_PLAIN_SERVICE_RUBRIC_HEADER.match(clean))
            or is_short_header_cue
        )
        kind = "RUBRIC" if is_eng_rubric else "BODY"

    return {
        "kind": kind,
        "ode_num": ode_num,
        "tone_num": tone_num,
        "doxology": doxology,
        "is_stichos": is_stichos,
        "is_podoben": is_podoben,
        "role_tag": role_tag,
        "length": len(clean),
        "propagated_dox": False,
    }


def align_bilingual_leaf_blocks(
    s_blocks: List[Dict[str, Any]],
    e_blocks: List[Dict[str, Any]],
) -> List[Optional[Dict[str, Any]]]:
    """
    Aligns Slavonic blocks (`s_blocks`) and English unit blocks (`e_blocks`) on a single
    physical leaf using anchor-synchronized Needleman-Wunsch dynamic programming (T-1),
    followed by standalone prefix attachment and generalized 1-to-K / K-to-1 sub-slicing.
    Returns a list of matched Slavonic block dicts (or None when an English rubric/editorial
    note has no Slavonic counterpart) of length `len(e_blocks)`.
    """
    m = len(s_blocks)
    n = len(e_blocks)
    if n == 0:
        return []
    if m == 0:
        return [None] * n

    s_infos = [classify_alignment_anchor(b["text"], is_slavonic=True) for b in s_blocks]
    e_infos = [classify_alignment_anchor(b["text"], is_slavonic=False) for b in e_blocks]

    # Propagate standalone rubric anchors (Doxology, Role, Ode, Tone) symmetrically onto
    # the immediately following BODY stanza for both Slavonic and English.
    for infos in (s_infos, e_infos):
        for k in range(1, len(infos)):
            prev_info = infos[k - 1]
            curr_info = infos[k]
            if prev_info["kind"] == "RUBRIC" and curr_info["kind"] == "BODY" and not prev_info["is_stichos"]:
                if curr_info["doxology"] is None and prev_info["doxology"] is not None:
                    curr_info["doxology"] = prev_info["doxology"]
                    curr_info["propagated_dox"] = True
                if curr_info["role_tag"] is None and prev_info["role_tag"] is not None:
                    curr_info["role_tag"] = prev_info["role_tag"]
                if curr_info["ode_num"] is None and prev_info["ode_num"] is not None:
                    curr_info["ode_num"] = prev_info["ode_num"]
                if curr_info["tone_num"] is None and prev_info["tone_num"] is not None:
                    curr_info["tone_num"] = prev_info["tone_num"]

    def gap_s_cost(si: Dict[str, Any]) -> int:
        if si["kind"] in ("EDITORIAL_SKIP", "APPARATUS"):
            return -1
        if si["kind"] == "RUBRIC" or si["is_stichos"] or si["doxology"] is not None:
            return -3
        return -12

    def gap_e_cost(ei: Dict[str, Any]) -> int:
        if ei["kind"] in ("EDITORIAL_SKIP", "APPARATUS"):
            return -1
        if ei["kind"] == "RUBRIC" or ei["is_stichos"] or ei["doxology"] is not None:
            return -3
        return -12

    def pair_score(si: Dict[str, Any], ei: Dict[str, Any]) -> int:
        if si["kind"] == "EDITORIAL_SKIP" or ei["kind"] == "EDITORIAL_SKIP":
            return -60

        if si["kind"] == "APPARATUS" or ei["kind"] == "APPARATUS":
            if si["kind"] == "APPARATUS" and ei["kind"] == "APPARATUS":
                return 35
            return -60

        if si["is_stichos"] or ei["is_stichos"]:
            if si["is_stichos"] and ei["is_stichos"]:
                return 80
            return -55

        s_len = max(1, si["length"])
        e_len = max(1, ei["length"])
        ratio = s_len / e_len

        # Hard guard: a short Slavonic header/fragment (< 60 chars, < 0.28x English length)
        # can never pair with a full English BODY stanza (>= 90 chars).
        if si["kind"] == "BODY" and ei["kind"] == "BODY" and s_len < 60 and e_len >= 90 and ratio < 0.28:
            return -45

        if si["kind"] != ei["kind"]:
            # Allow plain-text Slavonic rubrics (`BODY`) to pair with italicized English rubrics (`RUBRIC`)
            # and vice versa with a conservative score (+14) when lengths and anchors agree.
            if (
                {si["kind"], ei["kind"]} == {"BODY", "RUBRIC"}
                and 0.52 <= ratio <= 1.70
                and si["ode_num"] == ei["ode_num"]
                and si["role_tag"] == ei["role_tag"]
                and si["doxology"] == ei["doxology"]
            ):
                return 14
            return -55

        score = 28 if si["kind"] == "BODY" else 22
        if si["kind"] == "BODY":
            if 0.35 <= ratio <= 2.50:
                score += 10

        if si["ode_num"] is not None and ei["ode_num"] is not None:
            if si["ode_num"] == ei["ode_num"]:
                score += 85
            else:
                return -75

        if si["doxology"] is not None or ei["doxology"] is not None:
            if si["doxology"] == ei["doxology"]:
                score += 75
            elif si["doxology"] is not None and ei["doxology"] is not None:
                score -= 45
            elif not (si.get("propagated_dox") or ei.get("propagated_dox")):
                score -= 15

        if si["role_tag"] is not None and ei["role_tag"] is not None:
            if si["role_tag"] == ei["role_tag"]:
                score += 55
            else:
                score -= 25

        if si["is_podoben"] and ei["is_podoben"]:
            score += 50

        if si["tone_num"] is not None and ei["tone_num"] is not None:
            if si["tone_num"] == ei["tone_num"]:
                score += 35
            else:
                score -= 25

        return score

    neg_inf = -10**9
    dp = [[neg_inf] * (n + 1) for _ in range(m + 1)]
    ptr = [[0] * (n + 1) for _ in range(m + 1)]  # 1: diag (pair), 2: up (skip s), 3: left (skip e)
    dp[0][0] = 0

    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] + gap_s_cost(s_infos[i - 1])
        ptr[i][0] = 2
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] + gap_e_cost(e_infos[j - 1])
        ptr[0][j] = 3

    for i in range(1, m + 1):
        si = s_infos[i - 1]
        gs = gap_s_cost(si)
        for j in range(1, n + 1):
            ei = e_infos[j - 1]
            ge = gap_e_cost(ei)
            sc_pair = dp[i - 1][j - 1] + pair_score(si, ei)
            sc_up = dp[i - 1][j] + gs
            sc_left = dp[i][j - 1] + ge

            if sc_pair >= sc_up and sc_pair >= sc_left:
                dp[i][j] = sc_pair
                ptr[i][j] = 1
            elif sc_up >= sc_left:
                dp[i][j] = sc_up
                ptr[i][j] = 2
            else:
                dp[i][j] = sc_left
                ptr[i][j] = 3

    aligned: List[Optional[Dict[str, Any]]] = [None] * n
    aligned_s_idx_by_e: List[Optional[int]] = [None] * n
    used_s_indices: Set[int] = set()
    i, j = m, n
    while i > 0 or j > 0:
        move = ptr[i][j]
        if move == 1:
            if pair_score(s_infos[i - 1], e_infos[j - 1]) > 0:
                aligned[j - 1] = s_blocks[i - 1]
                aligned_s_idx_by_e[j - 1] = i - 1
                used_s_indices.add(i - 1)
            i -= 1
            j -= 1
        elif move == 2:
            i -= 1
        else:
            j -= 1

    # Post-DP Pass 1 (Decision 2): If a standalone Slavonic doxology/role rubric (`s_blocks[s_i - 1]`)
    # was skipped immediately before `s_blocks[s_i]` paired with an English BODY block `e_blocks[e_j]`
    # that embeds that doxology/role inline, prepend `s_blocks[s_i - 1]` onto `aligned[e_j]`.
    for e_j in range(n):
        s_i = aligned_s_idx_by_e[e_j]
        if s_i is not None and s_i > 0 and (s_i - 1) not in used_s_indices and e_infos[e_j]["kind"] == "BODY":
            prev_si = s_infos[s_i - 1]
            if (
                prev_si["kind"] == "RUBRIC"
                and prev_si["length"] <= 95
                and not prev_si["is_stichos"]
                and (
                    (prev_si["doxology"] is not None and prev_si["doxology"] == e_infos[e_j]["doxology"])
                    or (prev_si["role_tag"] is not None and prev_si["role_tag"] == e_infos[e_j]["role_tag"])
                )
            ):
                prefix_blk = s_blocks[s_i - 1]
                cur_blk = aligned[e_j]
                assert cur_blk is not None
                merged_prov = dict(cur_blk["provenance"]) if cur_blk.get("provenance") else None
                if (
                    merged_prov is not None
                    and prefix_blk.get("provenance")
                    and merged_prov.get("source_file") == prefix_blk["provenance"].get("source_file")
                ):
                    merged_prov["start_line"] = min(
                        int(merged_prov.get("start_line", 1)),
                        int(prefix_blk["provenance"].get("start_line", 1)),
                    )
                aligned[e_j] = {
                    **cur_blk,
                    "text": f"{prefix_blk['text'].strip()} {cur_blk['text'].strip()}",
                    "provenance": merged_prov,
                }
                used_s_indices.add(s_i - 1)

    # Post-DP Pass 2 (Generalized Option 2B / Decision 3): Punctuation-anchored 1-to-K (K in 2..8)
    # sub-slicing for multi-stanza Slavonic blocks corresponding to K consecutive English BODY stanzas.
    split_boundary_re = re.compile(
        r"([\.!\?:;\u00b7\u0387]|:[~\-–\.])(?:\s*\[\^\d+\]|\*)*\s+(?=[А-ЯІЇЄҐѢѴѠꙊѦѪѮѰѲA-Z\*])"
    )
    k = 0
    while k < n - 1:
        if e_infos[k]["kind"] != "BODY" or e_infos[k]["is_stichos"]:
            k += 1
            continue

        # Test candidate run lengths K from 2 up to min(8, n - k)
        best_run_k: Optional[int] = None
        best_run_slices: Optional[List[str]] = None
        best_run_s_blk: Optional[Dict[str, Any]] = None
        best_run_score = 999.0

        for cand_k in range(2, min(8, n - k) + 1):
            run_e_infos = e_infos[k : k + cand_k]
            if any(
                ri["kind"] != "BODY"
                or ri["is_stichos"]
                or (idx > 0 and (ri["ode_num"] is not None or ri["is_podoben"]))
                for idx, ri in enumerate(run_e_infos)
            ):
                break
            non_none = [aligned[k + idx] for idx in range(cand_k) if aligned[k + idx] is not None]
            if len(non_none) != 1:
                continue
            s_blk = non_none[0]
            assert s_blk is not None
            s_txt = s_blk["text"].strip()
            e_lens = [max(1, ri["length"]) for ri in run_e_infos]
            total_e_len = sum(e_lens)
            comb_ratio = len(s_txt) / max(1, total_e_len)
            if len(s_txt) < 25 * cand_k or not (0.35 <= comb_ratio <= 2.35):
                continue

            s_plain = _strip_combining(s_txt)
            if cand_k == 2 and run_e_infos[1]["doxology"] is not None:
                if not re.search(r"\b(?:слава|и\s+(?:нынѣ|ннѣ))\b", s_plain[15:]):
                    continue

            # Collect all valid internal sentence/stanza split indices in s_txt
            cand_splits = [m_sp.end(1) for m_sp in split_boundary_re.finditer(s_txt)]
            if len(cand_splits) < cand_k - 1:
                continue

            # Greedily select cand_k - 1 split points matching cumulative English length targets
            chosen_splits: List[int] = []
            prev_cut = 0
            cum_e = 0
            valid_cuts = True
            max_dist = 0.0
            for cut_idx in range(cand_k - 1):
                cum_e += e_lens[cut_idx]
                target_r = cum_e / total_e_len
                best_cut: Optional[int] = None
                best_d = 999.0
                for sp in cand_splits:
                    if sp <= prev_cut + 16 or (len(s_txt) - sp) < 18 * (cand_k - 1 - cut_idx):
                        continue
                    seg = s_txt[prev_cut:sp].strip()
                    seg_plain = _strip_combining(seg)
                    if cut_idx == 0 and (is_slavonic_rubric_line(seg, seg_plain) or is_slavonic_standalone_role(seg, seg_plain)):
                        continue
                    d = abs((sp / len(s_txt)) - target_r)
                    if d <= 0.35 and d < best_d:
                        best_d = d
                        best_cut = sp
                if best_cut is None:
                    valid_cuts = False
                    break
                chosen_splits.append(best_cut)
                prev_cut = best_cut
                if best_d > max_dist:
                    max_dist = best_d

            if not valid_cuts:
                continue

            cut_points = [0] + chosen_splits + [len(s_txt)]
            slices = [s_txt[cut_points[idx] : cut_points[idx + 1]].strip() for idx in range(cand_k)]
            if any(len(sl) < 16 for sl in slices):
                continue

            ratio_err = abs(comb_ratio - 0.88) + max_dist * 0.5
            if ratio_err < best_run_score:
                best_run_score = ratio_err
                best_run_k = cand_k
                best_run_slices = slices
                best_run_s_blk = s_blk

        if best_run_k is not None and best_run_slices is not None and best_run_s_blk is not None:
            shared_prov = dict(best_run_s_blk["provenance"]) if best_run_s_blk.get("provenance") else None
            for idx, sl_txt in enumerate(best_run_slices):
                prov_copy = dict(shared_prov) if shared_prov else None
                if prov_copy is not None:
                    prov_copy["slice_index"] = idx + 1
                    prov_copy["slice_total"] = best_run_k
                aligned[k + idx] = {
                    **best_run_s_blk,
                    "text": sl_txt,
                    "alignment_method": "SUB_SLICED_1_TO_K",
                    "provenance": prov_copy,
                }
            k += best_run_k
            continue

        k += 1

    # Post-DP Pass 3: Monotone recovery of unaligned BODY blocks when an unused Slavonic BODY block
    # lies strictly between the adjacent aligned Slavonic block indices on the same leaf.
    for e_j in range(n):
        if aligned[e_j] is not None or e_infos[e_j]["kind"] != "BODY" or e_infos[e_j]["is_stichos"]:
            continue
        # Only recover if there is an aligned block AFTER e_j on the same leaf (never attach trailing unmatched blocks)
        next_s_indices = [aligned_s_idx_by_e[r] for r in range(e_j + 1, n) if aligned_s_idx_by_e[r] is not None]
        if not next_s_indices:
            continue
        prev_s_indices = [aligned_s_idx_by_e[r] for r in range(0, e_j) if aligned_s_idx_by_e[r] is not None]
        low_s = (max(prev_s_indices) + 1) if prev_s_indices else 0
        high_s = min(next_s_indices)
        for cand_s in range(low_s, high_s):
            if cand_s not in used_s_indices and s_infos[cand_s]["kind"] == "BODY" and not s_infos[cand_s]["is_stichos"]:
                ratio = s_infos[cand_s]["length"] / max(1, e_infos[e_j]["length"])
                if 0.30 <= ratio <= 2.50:
                    aligned[e_j] = s_blocks[cand_s]
                    aligned_s_idx_by_e[e_j] = cand_s
                    used_s_indices.add(cand_s)
                    break

    return aligned


MONTH_NAME_TO_NUM: Dict[str, int] = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}
NUM_TO_MONTH_NAME: Dict[int, str] = {v: k.capitalize() for k, v in MONTH_NAME_TO_NUM.items()}

ENGLISH_ORDINAL_TO_DAY: Dict[str, int] = {
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
    "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
    "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14, "fifteenth": 15,
    "sixteenth": 16, "seventeenth": 17, "eighteenth": 18, "nineteenth": 19, "twentieth": 20,
    "twenty-first": 21, "twenty first": 21,
    "twenty-second": 22, "twenty second": 22,
    "twenty-third": 23, "twenty third": 23,
    "twenty-fourth": 24, "twenty fourth": 24,
    "twenty-fifth": 25, "twenty fifth": 25,
    "twenty-sixth": 26, "twenty sixth": 26,
    "twenty-seventh": 27, "twenty seventh": 27,
    "twenty-eighth": 28, "twenty eighth": 28,
    "twenty-ninth": 29, "twenty ninth": 29,
    "thirtieth": 30,
    "thirty-first": 31, "thirty first": 31,
}


def _parse_day_token(raw_tok: str) -> Optional[int]:
    t = re.sub(r"\s+", " ", raw_tok.strip().lower())
    if t in ENGLISH_ORDINAL_TO_DAY:
        return ENGLISH_ORDINAL_TO_DAY[t]
    m_d = re.match(r"^(\d{1,2})(?:st|nd|rd|th)?$", t)
    if m_d:
        val = int(m_d.group(1))
        if 1 <= val <= 31:
            return val
    return None


def parse_fixed_calendar_month_day(
    text: str,
    active_month_num: Optional[int],
    active_month_name: Optional[str],
    fixed_monument_month: bool = False,
) -> Tuple[Optional[int], Optional[str], Optional[int]]:
    """
    Parses internal month and calendar day (1..31) transitions from headings and rubrics
    without clobbering active dates on mid-service office headers, Podoben cues, or Synaxarion narratives.
    """
    clean = re.sub(r"\[\^\d+\]", "", text).strip()
    if len(clean) > 260 and not clean.startswith("#"):
        return active_month_num, active_month_name, None
    low = clean.lstrip("#* ").rstrip("* ").strip().lower()
    if (
        low.startswith("synaxarion")
        or low.startswith("note:")
        or "podoben" in low
        or "трїдне" in low
        or "тридне" in low
        or "tridneven" in low
        or '"on the third day"' in low
        or "if it fall on" in low
        or "if the feast fall" in low
        or re.search(
            r"\b(?:see\s+on|look\s+on|as\s+written\s+on|written\s+in\s+the\s+month|is\s+sung\s+on\s+the|magnify,\s+o\s+my\s+soul|receives\s+circumcision)\b",
            low,
        )
    ):
        return active_month_num, active_month_name, None

    new_m_num = active_month_num
    new_m_name = active_month_name
    new_day: Optional[int] = None
    day_tok_pat = r"(\d{1,2}(?:st|nd|rd|th)?|(?:twenty|thirty)[-\s]+(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth)|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|thirtieth)"
    month_tok_pat = r"(january|february|march|april|may|june|july|august|september|october|november|december)"

    # 1. Explicit "Month of <Month>"
    m_month_hdr = re.search(rf"\bmonth\s+of\s+{month_tok_pat}\b", low)
    if m_month_hdr:
        cand_m = MONTH_NAME_TO_NUM[m_month_hdr.group(1).lower()]
        if not fixed_monument_month or active_month_num is None or cand_m == active_month_num:
            new_m_num = cand_m
            new_m_name = NUM_TO_MONTH_NAME[new_m_num]

    # 2. Explicit "[Month of] <Month>[, on the] <Day>" or "[On] [the] <Day> [day] of [the month of] <Month>"
    m_md = re.search(
        rf"\b(?:month\s+of\s+)?{month_tok_pat}[,:\s]+(?:on\s+)?(?:the\s+)?{day_tok_pat}\b",
        low,
    )
    if m_md:
        cand_m = MONTH_NAME_TO_NUM[m_md.group(1).lower()]
        d_val = _parse_day_token(m_md.group(2))
        if d_val and (not fixed_monument_month or active_month_num is None or cand_m == active_month_num):
            new_m_num = cand_m
            new_m_name = NUM_TO_MONTH_NAME[new_m_num]
            new_day = d_val
            return new_m_num, new_m_name, new_day

    m_dm = re.search(
        rf"(?:^|\bon\s+the\s+)(?:on\s+)?(?:the\s+)?{day_tok_pat}\s+(?:day\s+)?of\s+(?:the\s+month\s+of\s+)?{month_tok_pat}\b",
        low,
    )
    if m_dm:
        d_val = _parse_day_token(m_dm.group(1))
        cand_m = MONTH_NAME_TO_NUM[m_dm.group(2).lower()]
        if d_val and (not fixed_monument_month or active_month_num is None or cand_m == active_month_num):
            new_m_num = cand_m
            new_m_name = NUM_TO_MONTH_NAME[new_m_num]
            new_day = d_val
            return new_m_num, new_m_name, new_day

    # 3. Ordinal/Cardinal day within active month:
    #    - "[In/On/Of] [the] same month / [the] month of the same, [on] [the] <Day> [day]"
    #    - "[On] the <Day> day [of the same month]"
    m_same = re.search(
        rf"^(?:(?:in|on|of)\s+)?(?:the\s+)?(?:same\s+month|month\s+of\s+the\s+same)[,:\s]+(?:on\s+)?(?:the\s+)?{day_tok_pat}(?:\s+day\b|[,:\.]|$)",
        low,
    )
    if m_same:
        d_val = _parse_day_token(m_same.group(1))
        if d_val:
            new_day = d_val
            return new_m_num, new_m_name, new_day

    m_ord = re.search(
        rf"^(?:on\s+)?(?:the\s+)?{day_tok_pat}\s+day(?:\s+of\s+the\s+same\s+month\b|\s*[:\.]|\s+of\s+(?:our|the\s+holy|saint\b)|$)",
        low,
    )
    if m_ord:
        d_val = _parse_day_token(m_ord.group(1))
        if d_val:
            new_day = d_val
            return new_m_num, new_m_name, new_day

    if clean.startswith("#"):
        m_day_hdr = re.search(r"\bday\s+(\d{1,2})\b", low)
        if m_day_hdr:
            d_val = int(m_day_hdr.group(1))
            if 1 <= d_val <= 31:
                new_day = d_val

    return new_m_num, new_m_name, new_day


def is_occasion_or_rite_heading(hdr_clean: str) -> bool:
    """
    Returns True if an H2/H3 heading names a top-level liturgical occasion, saint class,
    movable Sunday/weekday, or sacramental rite rather than an internal office/ode/prayer sub-header.
    """
    low = hdr_clean.strip().lower()
    if not low:
        return False
    # Exclude sub-office, ode, stichera, or single-prayer sub-headings
    if re.match(
        r"^(?:at\s+(?:small\s+vespers|little\s+vespers|great\s+vespers|vespers|matins|compline|the\s+midnight\s+office|the\s+liturgy|the\s+hours|\"?lord,\s+i\s+have\s+cried|\"?lord,\s+i\s+call|the\s+aposticha|the\s+litiya|the\s+praises|the\s+beatitudes)|on\s+\"?lord,\s+i\s+have\s+cried|the\s+canon\b|canon\s+to\b|another\s+canon\b|penitential\s+canon\b|ode\s+[1-9]\b|canticle\s+[1-9]\b|kontakion\b|ikos\b|sessional\b|exapostilarion\b|synaxarion\b|stichera\b|other\s+stichera\b|troparia\b|first\s+hour\b|third\s+hour\b|sixth\s+hour\b|ninth\s+hour\b|and\s+the\s+(?:first|third|sixth|ninth)\s+hour\b|prayer\s+(?:of|for|at|over)\b|the\s+(?:first|second|third)\s+prayer\b)",
        low,
    ):
        return False
    return True


def detect_day_of_week(text: str) -> Optional[str]:
    clean = re.sub(r"\[\^\d+\]", "", text).lower()
    for day_slug in ("saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"):
        if re.search(rf"\b{day_slug}\b", clean):
            return day_slug
    return None


def detect_office_slug_from_text(
    text: str,
    current_day_slug: Optional[str] = None,
    mon_type: str = "",
) -> Optional[str]:
    """Procedural detector for office transitions on #, **...**, inline *...*, and plain-text headers (T-2)."""
    clean = re.sub(r"\[\^\d+\]", "", text).strip()
    is_heading = clean.startswith("#")
    is_bold_hdr = clean.startswith("**") and clean.endswith("**") and len(clean) < 160
    is_plain_hdr = bool(RE_PLAIN_SERVICE_RUBRIC_HEADER.match(clean))
    if not is_heading and not is_bold_hdr and not is_pure_italic_rubric(clean) and not is_plain_hdr:
        return None
    low = clean.lstrip("#* ").rstrip("* ").lower()
    if len(low) > 260 and not is_heading:
        return None

    day_in_line = detect_day_of_week(low) or current_day_slug
    if re.search(r"\b(?:small\s+vespers|little\s+vespers)\b", low):
        return "sat_vespers" if (mon_type == "octoechos" or day_in_line == "saturday") else "small_vespers"
    if re.search(
        r"\b(?:great\s+vespers|at\s+vespers|in\s+the\s+evening|(?:saturday|sunday|monday|tuesday|wednesday|thursday|friday)\s+evening|vespers)\b",
        low,
    ):
        if mon_type == "octoechos" and day_in_line in ("saturday", None) and "sunday evening" not in low:
            return "sat_vespers"
        if day_in_line == "saturday" and "sunday evening" not in low:
            return "sat_vespers"
        return "vespers"
    if re.search(r"\b(?:at\s+matins|matins|orthros|the\s+beatitudes)\b", low):
        if mon_type == "octoechos" and day_in_line in ("sunday", "saturday", None):
            return "sun_matins"
        if day_in_line == "sunday":
            return "sun_matins"
        return "matins"
    if re.search(r"\b(?:midnight\s+office|mesonyktikon|nocturns)\b", low):
        return "midnight_office"
    if re.search(r"\b(?:compline|apodeipnon)\b", low):
        return "compline"
    if re.search(r"\b(?:first|third|sixth|ninth|royal)\s+hours?\b|\bat\s+the\s+hours\b", low):
        return "hours"
    if re.search(r"\b(?:divine\s+liturgy|at\s+the\s+liturgy|in\s+the\s+liturgy|liturgy\s+of|at\s+the\s+beatitudes)\b", low):
        return "liturgy"
    return None


def detect_section_slug_from_text(
    text: str,
    current_section_slug: str = "",
) -> Optional[Tuple[str, str, Optional[int]]]:
    """
    Procedural detector for liturgical section transitions on # headings, **...** headers,
    inline *...* rubrics, and plain-text headers (T-2). Returns (section_slug, human_section_label, new_ode_or_none).
    """
    clean = re.sub(r"\[\^\d+\]", "", text).strip()
    is_heading = clean.startswith("#")
    is_bold_hdr = clean.startswith("**") and clean.endswith("**") and len(clean) < 160
    is_rubric = is_pure_italic_rubric(clean) or bool(RE_PLAIN_SERVICE_RUBRIC_HEADER.match(clean))

    # Also allow leading italic rubric prefix at start of a stanza (e.g. *Ode 1, Heirmos:*)
    probe = clean
    if not is_heading and not is_bold_hdr and not is_rubric:
        m_lead = re.match(r"^\*([^*\n]{3,140})\*", clean)
        if not m_lead:
            return None
        probe = m_lead.group(1)

    low = probe.lstrip("#* ").rstrip("* ").lower()

    # Check Ode transition (excluding "After Ode N")
    m_after_ode = re.search(
        r"\bafter\s+(?:the\s+)?(?:(1st|first|3rd|third|6th|sixth|[1-9](?:st|nd|rd|th)?)\s+(?:ode|canticle)|(?:ode|canticle)\s+([1-9]))\b",
        low,
    )
    if m_after_ode:
        tok = (m_after_ode.group(1) or m_after_ode.group(2) or "").lower()
        if "6" in tok or "six" in tok or "kontakion" in low:
            return ("kontakion_ikos", probe.strip("*# :"), None)
        return ("sessionals", probe.strip("*# :"), None)

    m_ode = re.search(r"\b(?:ode|canticle)\s+([1-9])\b", low)
    if m_ode and (is_heading or is_bold_hdr or is_rubric or re.match(r"^\*?(?:ode|canticle)\s+[1-9]\b", low)):
        ode_n = int(m_ode.group(1))
        return (f"canon_ode_{ode_n}", f"Canon — Ode {ode_n}", ode_n)

    if not is_heading and not is_bold_hdr and not is_rubric:
        # For non-pure-rubric stanzas with a leading role tag, only switch section on explicit section roles
        if re.match(r"^(?:another\s+)?(?:kontakion|ikos)\b", low):
            return ("kontakion_ikos", "Kontakion and Ikos", None)
        if re.match(r"^(?:another\s+)?(?:sessional\s+hymn|kathisma)\b", low):
            return ("sessionals", "Sessional Hymns", None)
        if re.match(r"^(?:another\s+)?(?:exapost[ei]larion|photagogi[ck]on|hymn\s+of\s+light)\b", low):
            return ("exapostilarion", "Exapostilaria", None)
        if re.match(r"^(?:hypakoe|ypako[eë])\b", low):
            return ("hypakoe", "Hypakoe", None)
        if re.match(r"^(?:gradual\s+hymn|songs\s+of\s+ascent|antiphon\s+\d+)\b", low):
            return ("gradual", "Gradual Hymns (Anabathmoi)", None)
        return None

    if (
        "lord, i have cried" in low
        or "lord i have cried" in low
        or "lord, i call" in low
        or "lord i call" in low
    ):
        return ("stichera_lord_i_call", probe.strip("*# :"), None)
    if re.search(r"\b(?:at\s+the\s+litiya|on\s+the\s+litiya|at\s+the\s+litia)\b", low):
        return ("stichera_litiya", probe.strip("*# :"), None)
    if "aposticha" in low:
        return ("stichera_aposticha", probe.strip("*# :"), None)
    if re.search(r"\b(?:at\s+the\s+praises|on\s+the\s+praises|at\s+lauds|the\s+praises)\b", low):
        return ("stichera_praises", probe.strip("*# :"), None)
    if re.search(
        r"\b(?:resurrectional\s+stichera|stichera\s+of\s+the\s+resurrection|other\s+(?:eastern|anatolian)\s+stichera|other\s+stichera|stichera\s+of\s+the\s+cross|stichera\s+for\s+the\s+departed|supplicatory\s+stichera)\b",
        low,
    ) and len(low) < 160:
        sec_s = (
            current_section_slug
            if current_section_slug in ("stichera_lord_i_call", "stichera_litiya", "stichera_aposticha", "stichera_praises")
            else "stichera_lord_i_call"
        )
        return (sec_s, probe.strip("*# :"), None)
    if re.search(r"\b(?:beatitudes)\b", low):
        return ("beatitudes", probe.strip("*# :"), None)
    if re.search(
        r"\b(?:after\s+the\s+(?:1st|2nd|3rd|first|second|third)\s+(?:stichologia|kathisma)|sessional\s+hymns?|kathisma\s+hymns?)\b",
        low,
    ):
        return ("sessionals", probe.strip("*# :"), None)
    if re.search(r"\b(?:gradual\s+hymns?|songs\s+of\s+ascent|anabathmoi|antiphons?\s+of\s+the\s+gradual)\b", low):
        return ("gradual", probe.strip("*# :"), None)
    if re.search(r"\b(?:hypakoe|ypako[eë])\b", low):
        return ("hypakoe", probe.strip("*# :"), None)
    if re.search(r"\b(?:prokeimenon)\b", low) and len(low) < 120:
        return ("prokeimenon", probe.strip("*# :"), None)
    if re.search(r"\b(?:kontakion|ikos)\b", low) and len(low) < 160:
        return ("kontakion_ikos", probe.strip("*# :"), None)
    if re.search(r"\b(?:exapost[ei]lari(?:on|a)|photagogi[ck](?:on|a)|hymn\s+of\s+light)\b", low):
        return ("exapostilarion", probe.strip("*# :"), None)
    if re.search(r"\bsynaxarion\b", low):
        return ("synaxarion", probe.strip("*# :"), None)
    if re.search(
        r"\b(?:eleven\s+matins\s+resurrection\s+gospels|resurrection\s+gospel)\b",
        low,
    ) and len(low) < 160:
        return ("gospel", probe.strip("*# :"), None)
    if re.search(
        r"\b(?:the\s+reading\s+is\s+from|reading\s+from\s+the\s+prophecy|genesis|proverbs|isaiah|wisdom\s+of\s+solomon|exodus|job|ezekiel)\b",
        low,
    ) and len(low) < 180:
        return ("paremia", probe.strip("*# :"), None)
    if re.search(r"\b(?:instruction\s+of\s+saint|discourse\s+of\s+saint|catechetical\s+word|homily)\b", low):
        return ("patristic_homily", probe.strip("*# :"), None)
    if re.search(r"\b(?:the\s+canon|canon\s+of|canons)\b", low) and len(low) < 160:
        return ("canon_ode_1", probe.strip("*# :"), 1)
    if re.search(r"\b(?:god\s+is\s+the\s+lord|dismissal\s+troparia|apolytikion|troparion\s+of\s+the\s+resurrection)\b", low):
        return ("troparia", probe.strip("*# :"), None)

    return None


def slugify_coordinate(label: str) -> str:
    s = re.sub(r"\[\^\d+\]", "", label).lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s[:64] or "general"


def extract_podoben_slavonic_incipit(eng_txt: str, slav_txt: str = "") -> Optional[str]:
    """
    Extracts the diplomatic Slavonic Podoben incipit from parenthetical Cyrillic in the English
    rubric or from the aligned Slavonic rubric after 'Подобенъ:' (never falling back to hymn body).
    """
    m_paren = re.search(r"\(([^)]*[\u0400-\u04ff\ua640-\ua69f][^)]*)\)", eng_txt)
    if m_paren:
        return m_paren.group(1).strip()
    if slav_txt:
        m_slav = re.search(
            r"(?:подобенъ|подобен|подоб|подо|под)\s*[:\.]?\s*([^\.\n]{3,90})",
            slav_txt,
            re.IGNORECASE,
        )
        if m_slav:
            words = m_slav.group(1).strip().split()
            return " ".join(words[:6]).rstrip(",:;.")
    return None


def classify_attestation_mode(english_text: str, slavonic_text: str = "") -> str:
    """Classifies unit attestation as ATTESTED_FULL, INCIPIT_ONLY_POINTER, or DELEGATED_TO_COMMON (T-6)."""
    clean_e = re.sub(r"\[\^\d+\]", "", english_text).strip()
    body_e = re.sub(r"^\*[^*\n]{1,100}:\*\s*", "", clean_e).strip("* ")
    low_e = body_e.lower()
    if len(body_e) < 160 and re.search(
        r"\b(?:see\s+above|see\s+in|as\s+written\s+in|same\s+as\s+on|look\s+in\s+the)\b",
        low_e,
    ):
        return "DELEGATED_TO_COMMON"
    if len(body_e) < 130 and (
        "..." in body_e
        or "…" in body_e
        or re.search(r"\b(?:and\s+the\s+rest|and\s+the\s+troparion|etc\.)\b", low_e)
        or "прочее" in slavonic_text.lower()
    ):
        return "INCIPIT_ONLY_POINTER"
    return "ATTESTED_FULL"


def is_paratext_or_marginalia(
    txt: str,
    part_h1: str,
    office_h2: str,
    current_section: str,
    leaf_num: int = 1,
) -> bool:
    """Detects front-matter paratext, flyleaf marginalia, and foundation inscriptions (T-8 / SGC-06)."""
    if leaf_num <= 20:
        coord_probe = f"{part_h1} :: {office_h2} :: {current_section}".lower()
        if re.search(
            r"\b(?:front\s+matter|title\s+page|flyleaf|preface|to\s+the\s+reader|epigram|colophon|table\s+of\s+contents|approbatio|imprimatur)\b",
            coord_probe,
        ):
            return True
    low_t = txt.lower()
    if re.search(
        r"\b(?:gave\s+this\s+book|presented\s+this\s+book|bought\s+this\s+book|cursed\s+and\s+anathematized|foundation\s+inscription|marginal\s+inscription)\b",
        low_t,
    ):
        return True
    return False


def resolve_monument_year(monument_id: str, mon_info: Dict[str, Any]) -> int:
    """Deterministically extracts the 4-digit historical publication/manuscript year."""
    m_yr = re.match(r"^(\d{4})", monument_id)
    if m_yr:
        return int(m_yr.group(1))
    m_title = re.search(r"\b(1[4-9]\d{2}|20\d{2})\b", str(mon_info.get("title", "")))
    if m_title:
        return int(m_title.group(1))
    return int(mon_info.get("year", 1900) or 1900)


CANONICAL_RECENSION_WITNESS_ID = "kyivan_ruthenian_critical"
CANONICAL_RECENSION_TITLE = "Kyivan-Galician Ruthenian Critical Recension"
CANONICAL_WITNESS_PRIORITY_ORDER: Tuple[str, ...] = (
    "royal_doors",
    "stamford_2014",
    "sheptytsky_2021",
    "kyivan_ruthenian_critical",
    "st_sergius",
    "mci",
    "monthly_menaion",
    "royaldoors_old",
)


def resolve_monument_recension_stratum(monument_id: str, mon_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Deterministically resolves the unified canonical recension witness identity
    ('kyivan_ruthenian_critical' — Kyivan-Galician Ruthenian Critical Recension)
    and its chronological stratum (Pre-Nikonian Golden-Age Primacy vs. Post-Zamość Galician).
    """
    info = mon_info or {}
    year = resolve_monument_year(monument_id, info)
    if year < 1720:
        stratum_code = "PRE_NIKONIAN_KYIVAN_STAUROPEGION"
        stratum_witness_id = "kyivan_prenikonian_critical"
        stratum_title = "Pre-Nikonian Kyivan & Stauropegion Critical Recension (1491–1719)"
        stratum_primacy_rank = 1
    else:
        stratum_code = "POST_ZAMOSC_POCHAIV_GALICIAN"
        stratum_witness_id = "galician_synodal_critical"
        stratum_title = "Post-Zamość Pochaiv & Lviv Synodal Critical Recension (1720–2026)"
        stratum_primacy_rank = 2

    return {
        "canonical_recension_witness_id": CANONICAL_RECENSION_WITNESS_ID,
        "canonical_recension_title": CANONICAL_RECENSION_TITLE,
        "canonical_witness_priority_rank": 4,
        "historical_stratum": stratum_code,
        "stratum_witness_id": stratum_witness_id,
        "stratum_title": stratum_title,
        "stratum_primacy_rank": stratum_primacy_rank,
        "chronology_year": year,
    }


def emit_pipeline_ready_event(
    monument_id: str,
    mon_info: Dict[str, Any],
    mon_type: str,
    ws_rel: str,
    atomic_path: Path,
    propers_path: Path,
    total_pages: int,
    leaves_covered_count: int,
    total_atomic_units: int,
    total_propers_units: int,
    counts_by_class: Optional[Dict[str, int]] = None,
) -> None:
    """
    Updates pipeline_sync_state in codex_registry.json under cross-process lock and writes
    Typikon Coded/Data/Inbox/pipeline_events/translation_<monument_id>.ready.json (§4.1).
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    stratum_meta = resolve_monument_recension_stratum(monument_id, mon_info)
    chronology_year = stratum_meta["chronology_year"]
    has_propers_corpus = bool(total_propers_units > 0 and propers_path.exists())
    c_map = counts_by_class or {}
    euchological_units_count = (
        int(c_map.get("SACERDOTAL_PRAYER", 0))
        + int(c_map.get("LITANY_OR_DIALOGUE", 0))
        + int(c_map.get("FIXED_ORDINARY_OR_LECTION", 0))
    )
    atomic_sha256 = hashlib.sha256(atomic_path.read_bytes()).hexdigest() if atomic_path.exists() else None
    propers_sha256 = hashlib.sha256(propers_path.read_bytes()).hexdigest() if propers_path.exists() else None
    atomic_rel = f"Translation/{atomic_path.resolve().relative_to(PROJECT_ROOT).as_posix()}"
    propers_rel = (
        f"Translation/{propers_path.resolve().relative_to(PROJECT_ROOT).as_posix()}"
        if propers_path.exists()
        else None
    )
    primary_artifact_path = propers_rel if propers_rel else atomic_rel
    primary_artifact_sha256 = propers_sha256 if propers_sha256 else atomic_sha256

    events_dir = PROJECT_ROOT.parent / "Typikon Coded" / "Data" / "Inbox" / "pipeline_events"
    events_dir.mkdir(parents=True, exist_ok=True)
    event_file = events_dir / f"translation_{monument_id}.ready.json"
    event_rel = f"Typikon Coded/Data/Inbox/pipeline_events/{event_file.name}"

    sync_state = {
        "stage": "READY_FOR_COMPARISON",
        "transformation_schema_version": "4.0.0",
        "canonical_recension_witness_id": stratum_meta["canonical_recension_witness_id"],
        "canonical_recension_title": stratum_meta["canonical_recension_title"],
        "historical_stratum": stratum_meta["historical_stratum"],
        "stratum_witness_id": stratum_meta["stratum_witness_id"],
        "stratum_primacy_rank": stratum_meta["stratum_primacy_rank"],
        "chronology_year": chronology_year,
        "monument_type": mon_type,
        "has_propers_corpus": has_propers_corpus,
        "last_transformed_at": now_iso,
        "last_extracted_at": now_iso,
        "artifact_path": primary_artifact_path,
        "artifact_sha256": primary_artifact_sha256,
        "atomic_corpus_sha256": atomic_sha256,
        "propers_corpus_sha256": propers_sha256,
        "extracted_units_count": total_atomic_units,
        "total_atomic_units": total_atomic_units,
        "total_propers_units": total_propers_units,
        "euchological_units_count": euchological_units_count,
        "sgc02_verified": True,
        "sgc06_tabula_rasa_verified": True,
        "ready_for_comparison_ingest": True,
        "ready_for_chant_lab_omr": False,
        "ready_for_shared_lexicon_merge": False,
        "ready_for_typikon_hub_hydration": False,
        "event_file": event_rel,
    }

    def _mutate_reg(reg_data: Dict[str, Any]) -> None:
        m_entry = reg_data.get("monuments", {}).get(monument_id)
        if m_entry is not None:
            m_entry["pipeline_sync_state"] = sync_state

    atomic_update_registry(_mutate_reg, REGISTRY_FILE)

    event_payload = {
        "event_type": "TRANSLATION_MONUMENT_READY",
        "schema_version": "4.0.0",
        "producer_spoke": "Translation",
        "monument_or_codex_id": monument_id,
        "monument_id": monument_id,
        "canonical_recension_witness_id": stratum_meta["canonical_recension_witness_id"],
        "canonical_recension_title": stratum_meta["canonical_recension_title"],
        "historical_stratum": stratum_meta["historical_stratum"],
        "stratum_witness_id": stratum_meta["stratum_witness_id"],
        "stratum_primacy_rank": stratum_meta["stratum_primacy_rank"],
        "chronology_year": chronology_year,
        "monument_type": mon_type,
        "has_propers_corpus": has_propers_corpus,
        "status": mon_info.get("status", "completed"),
        "stage": "READY_FOR_COMPARISON",
        "emitted_at": now_iso,
        "workspace_dir": f"Translation/{ws_rel}",
        "artifact_path": primary_artifact_path,
        "artifact_sha256": primary_artifact_sha256,
        "extracted_units_count": total_atomic_units,
        "sgc02_verified": True,
        "sgc06_tabula_rasa_verified": True,
        "ready_for_ingest": True,
        "ready_for_comparison_ingest": True,
        "artifacts": {
            "atomic_corpus_path": atomic_rel,
            "atomic_corpus_sha256": atomic_sha256,
            "propers_corpus_path": propers_rel,
            "propers_corpus_sha256": propers_sha256,
        },
        "counts": {
            "total_physical_pages": total_pages,
            "leaves_covered_count": leaves_covered_count,
            "total_atomic_units": total_atomic_units,
            "total_propers_units": total_propers_units,
            "euchological_units_count": euchological_units_count,
            "counts_by_unit_class": c_map,
        },
    }
    event_file.write_text(json.dumps(event_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  [Pipeline Event] Emitted {event_rel}")


def extract_monument_atomic_corpus(
    monument_id: str,
    sync_hub: bool = False,
    emit_event: bool = False,
) -> Dict[str, Any]:
    """
    Extracts the 5-class atomic liturgical corpus and variable propers corpus
    for a single monument under v4.0.0 Tabula Rasa Producer Specification,
    writing deliverables to Final MD/ and optionally syncing to Typikon Coded/Data/Inbox/.
    """
    registry = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    mon_info = registry.get("monuments", {}).get(monument_id)
    if not mon_info:
        raise KeyError(f"Unknown monument_id '{monument_id}' in codex_registry.json")

    mon_type = resolve_monument_type(monument_id, mon_info)
    book_prefix = MONUMENT_TYPE_TO_PREFIX.get(mon_type, "LIT")
    cycle_name = MONUMENT_TYPE_TO_CYCLE.get(mon_type, "LITURGICAL_CORPUS")
    stratum_meta = resolve_monument_recension_stratum(monument_id, mon_info)

    ws_rel = mon_info.get("workspace_dir", f"Liturgical Monuments/{monument_id}")
    ws_dir = PROJECT_ROOT / ws_rel
    final_md_dir = ws_dir / "Final MD"
    final_md_dir.mkdir(parents=True, exist_ok=True)
    source_dir = ws_dir / "Source Text"

    folio_offset = int(mon_info.get("folio_offset", 0) or 0)
    total_pages = int(mon_info.get("total_physical_pages", 0) or 0)

    pod_catalog, stichoi_catalog = load_primitives_data()
    blocks = collect_cohort_blocks(ws_dir, folio_offset=folio_offset)
    eng_cross_leaf_starts = {b["leaf"] for b in blocks if len(b.get("leaf_span", [])) > 1}
    slavonic_blocks_by_leaf = parse_slavonic_blocks_by_leaf(
        source_dir,
        ws_dir,
        english_cross_leaf_starts=eng_cross_leaf_starts,
    )

    # Pre-align unit-emitting English blocks with Slavonic blocks on each physical leaf (T-1)
    eng_units_by_leaf: Dict[int, List[Dict[str, Any]]] = {}
    for blk in blocks:
        if not blk["text"].strip().startswith("#"):
            eng_units_by_leaf.setdefault(blk["leaf"], []).append(blk)

    for lf_num, e_leaf_list in eng_units_by_leaf.items():
        s_leaf_list = slavonic_blocks_by_leaf.get(lf_num, [])
        aligned_s = align_bilingual_leaf_blocks(s_leaf_list, e_leaf_list)
        for e_b, s_b in zip(e_leaf_list, aligned_s):
            e_b["aligned_slavonic_block"] = s_b

    # Determine if Part 0 is Front Matter with a verified Part 1 start_landmark within first 20 leaves (T-8 / SGC-06)
    pub_parts = mon_info.get("publication_spec", {}).get("parts", [])
    part1_landmark_re: Optional[re.Pattern] = None
    in_front_matter = False
    if len(pub_parts) >= 2:
        p0_title = str(pub_parts[0].get("title", ""))
        p1_landmark = pub_parts[1].get("start_landmark")
        if p1_landmark and re.search(r"\b(?:front\s+matter|title|preface|paratext)\b", p0_title, re.IGNORECASE):
            try:
                cand_re = re.compile(p1_landmark, re.IGNORECASE)
                if any(cand_re.search(b["text"].strip()) for b in blocks if b["leaf"] <= 20):
                    part1_landmark_re = cand_re
                    in_front_matter = True
            except re.error:
                part1_landmark_re = None

    # Initialize fixed-cycle month state if monument is a monthly Menaion or Nativity-Theophany codex
    active_month_num: Optional[int] = None
    active_month_name: Optional[str] = None
    active_day_num: Optional[int] = None
    fixed_monument_month = False
    for m_str, m_idx in MONTH_NAME_TO_NUM.items():
        if re.search(rf"\b{m_str}\b", f"{monument_id} {mon_info.get('title', '')}".lower()):
            active_month_num = m_idx
            active_month_name = NUM_TO_MONTH_NAME[m_idx]
            fixed_monument_month = "dec_feb" not in monument_id
            break
    if monument_id == "1905_lviv_nativity_theophany":
        active_month_num = 12
        active_month_name = "December"

    # Active hierarchical coordinates
    part_h1 = mon_info.get("short_title", monument_id)
    office_h2 = "Front Matter" if in_front_matter else "Opening Section"
    current_section = "Front Matter" if in_front_matter else "Introductory Material"
    current_office_slug = "front_matter" if in_front_matter else ("sat_vespers" if mon_type == "octoechos" else "general_office")
    current_section_slug = "front_matter" if in_front_matter else "introductory_material"
    current_section_rubric_verbatim: Optional[str] = None
    current_season_or_tone = (
        "Tone 1"
        if mon_type == "octoechos"
        else (f"Month of {active_month_name}" if active_month_name else cycle_name)
    )
    current_day_or_date = "General"
    current_day_slug: Optional[str] = "saturday" if mon_type == "octoechos" else None
    part_governing_tone: Optional[int] = 1 if mon_type == "octoechos" else None
    current_tone: Optional[int] = part_governing_tone
    canon_tones_by_num: Dict[int, int] = {1: 1} if mon_type == "octoechos" else {}
    current_ode: Optional[int] = None
    current_canon_num: int = 0
    ode_stanza_total: int = 0
    ode_troparion_seq: int = 0
    active_podoben_id: Optional[str] = None
    active_podoben_slavonic: Optional[str] = None
    active_podoben_label_raw: Optional[str] = None
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

    atomic_units: List[Dict[str, Any]] = []
    propers_items: List[Dict[str, Any]] = []
    leaf_seq_counter: Dict[int, int] = {}

    for blk in blocks:
        txt = blk["text"].strip()
        leaf_num = blk["leaf"]
        locus = blk["locus"]
        c_idx = blk["cohort"]

        if in_front_matter and (
            leaf_num > 20
            or active_day_num is not None
            or (part1_landmark_re and part1_landmark_re.search(txt))
        ):
            in_front_matter = False
            if current_office_slug == "front_matter":
                current_office_slug = "sat_vespers" if mon_type == "octoechos" else "general_office"
            if current_section_slug == "front_matter":
                current_section_slug = "introductory_material"

        # Track H1 / H2 / H3 structural headings
        if txt.startswith("#"):
            hdr_clean = re.sub(r"\[\^\d+\]", "", txt.lstrip("#")).strip()
            active_psalm_or_lection = False
            active_hymn_subtype_cue = None
            active_stichos = None
            active_doxology_tag = None
            active_podoben_id = None
            active_podoben_slavonic = None
            active_podoben_label_raw = None

            day_h = detect_day_of_week(hdr_clean)
            if day_h:
                current_day_slug = day_h
                current_day_or_date = hdr_clean

            # Fixed calendar month/day detection on headings (only for Fixed-Cycle Anthologion/Menaion or Horologion Menologion)
            allow_fixed_cal_hdr = (
                (mon_type == "anthologion" and monument_id != "1773_pochaiv_general_menaion")
                or (
                    mon_type == "horologion"
                    and bool(re.search(r"\b(?:menologion|month\s+of)\b", f"{part_h1} {office_h2} {hdr_clean}", re.IGNORECASE))
                )
            )
            if allow_fixed_cal_hdr:
                cand_m_num, cand_m_name, cand_day = parse_fixed_calendar_month_day(
                    txt, active_month_num, active_month_name, fixed_monument_month=fixed_monument_month
                )
                if cand_m_num is not None:
                    active_month_num = cand_m_num
                    active_month_name = cand_m_name
                if cand_day is not None and active_month_name:
                    active_day_num = cand_day
                    current_day_or_date = f"{active_month_name} {active_day_num}"
                    current_season_or_tone = f"{active_month_name} {active_day_num}"
                elif re.search(r"\b(?:common\s+service|general\s+service|appendix)\b", hdr_clean, re.IGNORECASE):
                    active_day_num = None

            m_t = re.search(
                r"\bTONE\s+(\d+|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|I|II|III|IV|V|VI|VII|VIII)\b",
                hdr_clean,
                re.IGNORECASE,
            )
            if m_t:
                t_raw = m_t.group(1).lower()
                t_val = word_to_num.get(t_raw, int(t_raw) if t_raw.isdigit() else 0)
                if 1 <= t_val <= 8:
                    prev_gov_tone = part_governing_tone
                    part_governing_tone = t_val
                    current_tone = t_val
                    current_season_or_tone = f"Tone {t_val}"
                    canon_tones_by_num = {1: t_val}
                    current_ode = None
                    current_canon_num = 0
                    if mon_type == "octoechos" and (txt.startswith("# ") or t_val != prev_gov_tone) and not day_h:
                        current_day_slug = "saturday"
                        current_day_or_date = "Saturday"
                        current_office_slug = "sat_vespers"

            off_h = detect_office_slug_from_text(txt, current_day_slug, mon_type)
            if off_h:
                current_office_slug = off_h

            sec_h = detect_section_slug_from_text(txt, current_section_slug)
            if sec_h:
                sec_slug, sec_label, ode_det = sec_h
                current_section_slug = sec_slug
                current_section = sec_label
                current_section_rubric_verbatim = hdr_clean
                current_ode = ode_det
                current_canon_num = 0
                ode_stanza_total = 0
                ode_troparion_seq = 0
                section_hymn_seq = 0
                if txt.startswith("# "):
                    part_h1 = hdr_clean
                elif txt.startswith("## "):
                    office_h2 = hdr_clean
                continue

            if txt.startswith("# "):
                part_h1 = hdr_clean
                if (
                    not m_t
                    and active_day_num is None
                    and mon_type in ("lenten_triodion", "pentecostarion", "anthologion", "horologion", "euchologion_liturgikon", "trebnyk_euchologion")
                ):
                    current_season_or_tone = hdr_clean
                current_ode = None
                current_canon_num = 0
                active_litany_type = None
                litany_petition_idx = 0
                section_hymn_seq = 0
                if not in_front_matter:
                    current_section = hdr_clean
                    current_section_slug = slugify_coordinate(hdr_clean)
                continue
            elif txt.startswith("## "):
                office_h2 = hdr_clean
                current_ode = None
                current_canon_num = 0
                active_litany_type = None
                litany_petition_idx = 0
                section_hymn_seq = 0
                if (
                    not m_t
                    and active_day_num is None
                    and not in_front_matter
                    and is_occasion_or_rite_heading(hdr_clean)
                    and mon_type in ("lenten_triodion", "pentecostarion", "anthologion", "horologion", "euchologion_liturgikon", "trebnyk_euchologion")
                ):
                    current_season_or_tone = hdr_clean
                    if not day_h:
                        current_day_or_date = hdr_clean
                if not off_h and not in_front_matter:
                    current_section = hdr_clean
                    current_section_slug = slugify_coordinate(hdr_clean)
                continue
            else:
                current_section = hdr_clean
                current_section_slug = slugify_coordinate(hdr_clean)
                current_ode = None
                current_canon_num = 0
                section_hymn_seq = 0
                continue

        first_line = txt.splitlines()[0].strip()
        pure_italic_rubric = is_pure_italic_rubric(txt)
        is_bold_rubric = first_line.startswith("**") and first_line.endswith("**") and len(first_line) < 160
        plain_hdr_rubric = bool(RE_PLAIN_SERVICE_RUBRIC_HEADER.match(first_line)) and len(txt.splitlines()) == 1

        # Procedural day / calendar date / office / section detection on inline rubrics and role cues (T-2)
        if pure_italic_rubric or is_bold_rubric or plain_hdr_rubric or first_line.startswith("*"):
            allow_fixed_cal_in = (
                (mon_type == "anthologion" and monument_id != "1773_pochaiv_general_menaion")
                or (
                    mon_type == "horologion"
                    and bool(re.search(r"\b(?:menologion|month\s+of)\b", f"{part_h1} {office_h2} {first_line}", re.IGNORECASE))
                )
            )
            if allow_fixed_cal_in and (pure_italic_rubric or is_bold_rubric or RE_MENOLOGION_DAY.match(first_line)):
                cand_m_num, cand_m_name, cand_day = parse_fixed_calendar_month_day(
                    first_line, active_month_num, active_month_name, fixed_monument_month=fixed_monument_month
                )
                if cand_m_num is not None:
                    active_month_num = cand_m_num
                    active_month_name = cand_m_name
                if cand_day is not None and active_month_name:
                    active_day_num = cand_day
                    current_day_or_date = f"{active_month_name} {active_day_num}"
                    current_season_or_tone = f"{active_month_name} {active_day_num}"
                    active_psalm_or_lection = False

        if pure_italic_rubric or is_bold_rubric or plain_hdr_rubric:
            day_r = detect_day_of_week(first_line)
            if day_r and len(first_line) < 180 and (
                detect_office_slug_from_text(txt, day_r, mon_type) is not None
                or plain_hdr_rubric
                or re.match(
                    r"^[\*\s]*(?:On\s+|In\s+the\s+evening[,]?\s+on\s+)?(?:Saturday|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday)\b",
                    first_line,
                    re.IGNORECASE,
                )
            ):
                current_day_slug = day_r
                if active_day_num is None:
                    current_day_or_date = first_line.strip("* :.")
                if mon_type in ("lenten_triodion", "pentecostarion") and re.search(
                    r"\b(?:week|cheesefare|meatfare|bright|palm|lazarus|thomas|paralytic|samaritan|blind)\b",
                    first_line,
                    re.IGNORECASE,
                ):
                    current_season_or_tone = first_line.strip("* :.")

        off_in = detect_office_slug_from_text(txt, current_day_slug, mon_type)
        if off_in:
            current_office_slug = off_in
            if pure_italic_rubric and len(first_line) < 160:
                office_h2 = first_line.strip("* :.")
            current_ode = None
            current_canon_num = 0
            ode_stanza_total = 0
            ode_troparion_seq = 0
            section_hymn_seq = 0
            active_podoben_id = None
            active_podoben_slavonic = None
            active_podoben_label_raw = None
            active_stichos = None
            active_doxology_tag = None

        sec_in = detect_section_slug_from_text(txt, current_section_slug)
        if sec_in:
            sec_slug, sec_label, ode_det = sec_in
            prev_ode = current_ode
            prev_sec_slug = current_section_slug
            current_section_slug = sec_slug
            current_section = sec_label
            if pure_italic_rubric:
                current_section_rubric_verbatim = txt.strip()
            active_psalm_or_lection = False
            if ode_det is not None:
                if ode_det != prev_ode:
                    current_ode = ode_det
                    current_canon_num = 0
                    ode_stanza_total = 0
                    ode_troparion_seq = 0
                    section_hymn_seq = 0
                    active_podoben_id = None
                    active_podoben_slavonic = None
                    active_podoben_label_raw = None
                    active_stichos = None
                    active_doxology_tag = None
            else:
                current_ode = None
                current_canon_num = 0
                ode_stanza_total = 0
                ode_troparion_seq = 0
                if sec_slug != prev_sec_slug:
                    section_hymn_seq = 0
                    active_podoben_id = None
                    active_podoben_slavonic = None
                    active_podoben_label_raw = None
                    active_stichos = None
                    active_doxology_tag = None
        elif RE_SECTION_RUBRIC_CUE.match(first_line) and pure_italic_rubric:
            current_section_rubric_verbatim = txt.strip()
            active_psalm_or_lection = False
            active_podoben_id = None
            active_podoben_slavonic = None
            active_podoben_label_raw = None
            active_stichos = None
            active_doxology_tag = None

        # Update inline Tone / Menologion context
        m_in_t = re.search(r"\bTone\s+([1-8])\b", first_line, re.IGNORECASE)
        if m_in_t:
            current_tone = int(m_in_t.group(1))
            if mon_type == "octoechos" and part_governing_tone:
                current_season_or_tone = f"Tone {part_governing_tone}"
            elif mon_type == "octoechos":
                current_season_or_tone = f"Tone {current_tone}"

        if re.search(r"\b(?:idiomelon|idiomela|automelon|self-melody)\b", first_line, re.IGNORECASE):
            active_podoben_id = None
            active_podoben_slavonic = None
            active_podoben_label_raw = None

        m_men = RE_MENOLOGION_DAY.match(first_line)
        if m_men:
            if active_day_num is None or not active_month_name:
                current_day_or_date = first_line.strip("* ")
            active_psalm_or_lection = False

        # Retrieve anchor-aligned Slavonic block for this English block (T-1)
        slav_block: Optional[Dict[str, Any]] = blk.get("aligned_slavonic_block")
        slav_text = slav_block["text"] if slav_block else ""
        slav_provenance = slav_block["provenance"] if slav_block else None
        slav_body_only = strip_slavonic_leading_role_prefix(slav_text) if slav_text else ""
        slav_words = slav_body_only.split() if slav_body_only else slav_text.split()
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
        local_slot_suffix: Optional[str] = None

        m_lxx = re.search(
            r"\[((?:LXX\s+)?(?:Ps(?:alm)?\.?|Isa\.?|Gen\.?|Prov\.?|Matt\.?|Mt\.?|Mark|Mk\.?|Luke|Lk\.?|John|Jn\.?|Rom\.?|1?\s*Cor\.?|2\s*Cor\.?|Gal\.?|Eph\.?|Phil\.?|Col\.?|1?\s*Tim\.?|2\s*Tim\.?|Heb\.?|Acts)\s+[^\]]+)\]",
            txt,
        )
        if m_lxx:
            lxx_ref = m_lxx.group(1).strip()
        m_zach = re.search(r"\b(?:Pericope|Section|Zachalo|lection)\s*\[?(\d+)\]?", txt, re.IGNORECASE)
        if m_zach:
            zachalo_number = m_zach.group(1)

        paratext_flag = in_front_matter or is_paratext_or_marginalia(txt, part_h1, office_h2, current_section, leaf_num)

        # Check standalone Podoben prescription line
        if RE_PODOBEN_HEADER.match(txt) and pure_italic_rubric and len(txt) < 240:
            m_pod_hdr = RE_PODOBEN_HEADER.match(txt)
            pod_label = (m_pod_hdr.group(1) or m_pod_hdr.group(2) or "").strip() if m_pod_hdr else ""
            pod_slav = extract_podoben_slavonic_incipit(txt, slav_text)
            p_id, _, _ = match_podoben_model(txt, pod_slav or "", current_tone or 1, pod_catalog)
            active_podoben_id = p_id
            active_podoben_slavonic = pod_slav
            active_podoben_label_raw = pod_label or txt.strip("* ")
            unit_class = "RUBRIC_OR_STATUTE"
            unit_subtype = "PODOBEN_PRESCRIPTION"
            active_psalm_or_lection = False
        # Check standalone Verse / Stichos line (supports both *Verse:* Text and *Verse: Text*)
        elif RE_VERSE_HEADER.match(txt) and len(txt) < 280:
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
        elif (
            re.match(
                r"^\*(?:Glory\s+to\s+the\s+Father\b|Glory\s*\.\.\.|Glory\s*:|Glory\s*,|Glory\b|Both\s+now\b)[^*\n]*\*(?:\s*\[\^\d+\])*\s*$",
                txt,
                re.IGNORECASE,
            )
            and pure_italic_rubric
            and len(txt) < 200
        ):
            unit_class = "FIXED_ORDINARY_OR_LECTION"
            unit_subtype = "DOXOLOGY_HEADER"
            if "glory" in txt.lower() and "both now" in txt.lower():
                active_doxology_tag = "GLORY_BOTH_NOW"
            elif "glory" in txt.lower():
                active_doxology_tag = "GLORY"
            else:
                active_doxology_tag = "BOTH_NOW"
            if "podoben:" in txt.lower():
                m_pod_dox = RE_PODOBEN_HEADER.search(txt)
                pod_lbl = (m_pod_dox.group(1) or m_pod_dox.group(2) or "").strip() if m_pod_dox else ""
                pod_slav = extract_podoben_slavonic_incipit(txt, slav_text)
                p_id, _, _ = match_podoben_model(txt, pod_slav or "", current_tone or 1, pod_catalog)
                active_podoben_id = p_id
                active_podoben_slavonic = pod_slav
                active_podoben_label_raw = pod_lbl or txt.strip("* ")
            else:
                active_podoben_id = None
                active_podoben_slavonic = None
                active_podoben_label_raw = None
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
                or (
                    not pure_italic_rubric
                    and bool(
                        re.match(
                            r"^\*(?:(?:The\s+)?(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Another)\s+Prayer\b|Prayer\s+(?:of|for|over|at|before|after|unto|to)\b|Exorcism\b)",
                            first_line,
                            re.IGNORECASE,
                        )
                    )
                )
                or (speaker == "PRIEST" and delivery_mode == "SECRET" and len(txt) >= 120)
                or (speaker == "PRIEST" and len(txt) >= 210 and not RE_LITANY_PETITION_END.search(txt))
            )
            is_cued_choral_hymn = (
                speaker in ("CHOIR", "CHOIRS", "CHANTER", "CHANTERS")
                and active_hymn_subtype_cue is not None
                and mon_type not in NON_HYMNOGRAPHIC_MONUMENT_TYPES
                and len(txt) >= 40
                and not re.search(
                    r"\b(?:Lord,\s+have\s+mercy|To\s+Thee,\s+O\s+Lord|Grant\s+this,\s+O\s+Lord|Come,\s+let\s+us\s+worship)\b",
                    txt,
                    re.IGNORECASE,
                )
            )
            if is_prayer and not paratext_flag:
                unit_class = "SACERDOTAL_PRAYER"
                active_psalm_or_lection = False
                active_hymn_subtype_cue = None
                active_stichos = None
                active_doxology_tag = None
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

                m_dox = re.search(
                    r"(For\s+(?:unto\s+Thee\s+is\s+due|Thine\s+is\s+the\s+kingdom|Thou\s+art\s+a\s+merciful|blessed\s+and\s+glorified)[^\.!\n]+[\.!])",
                    txt,
                    re.IGNORECASE,
                )
                if m_dox:
                    doxology_formula = m_dox.group(1).strip()

            # 2. Check LITANY_OR_DIALOGUE
            elif not paratext_flag and (
                (speaker is not None and not is_cued_choral_hymn)
                or RE_SACRAMENTAL_FORMULA.search(txt)
                or RE_EKPHONESIS_FORMULA.search(txt)
                or RE_LITANY_PETITION_END.search(txt)
                or re.match(
                    r"^\*(?:Dismissal\s+(?:on|for|of)|After\s+the\s+(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth)\s+Ode|And\s+the\s+exclamation)\b",
                    first_line,
                    re.IGNORECASE,
                )
            ):
                unit_class = "LITANY_OR_DIALOGUE"
                active_psalm_or_lection = False
                active_hymn_subtype_cue = None
                active_stichos = None
                active_doxology_tag = None
                if RE_SACRAMENTAL_FORMULA.search(txt):
                    unit_subtype = "SACRAMENTAL_DECLARATIVE_FORMULA"
                    litany_or_exchange_type = "SACRAMENTAL_FORM"
                elif re.match(
                    r"^\*After\s+the\s+(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth)\s+Ode\b",
                    first_line,
                    re.IGNORECASE,
                ):
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
            elif not paratext_flag and (
                (
                    not pure_italic_rubric
                    and re.match(
                        r"^\*?(?:Psalm\s+\d+|A\s+Psalm\s+of\s+David|(?:Great\s+)?Prokeimenon|Alleluia|Communion\s+(?:Hymn|Verse)|Koinonikon|Kinonikon|The\s+Reading\s+is\s+from|(?:The\s+)?Holy\s+Gospel\s+according\s+to|Gospel\s+according\s+to|Epistle\s+of|(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh)\s+Matins\s+Resurrection\s+Gospel)\b",
                        first_line,
                        re.IGNORECASE,
                    )
                )
                or (not txt.startswith("*") and lxx_ref and "ps" in lxx_ref.lower())
                or (not txt.startswith("*") and active_psalm_or_lection and len(txt) >= 35)
                or (not pure_italic_rubric and current_section_slug == "paremia" and len(txt) >= 60)
            ):
                unit_class = "FIXED_ORDINARY_OR_LECTION"
                active_hymn_subtype_cue = None
                active_stichos = None
                active_doxology_tag = None
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

            # 4. Check PROPER_HYMN (Strictly gated against typikon/synodal/lexicon, front-matter, prose sections, and pure italic rubrics — T-4, T-8)
            elif (
                mon_type not in NON_HYMNOGRAPHIC_MONUMENT_TYPES
                and not paratext_flag
                and not pure_italic_rubric
                and not plain_hdr_rubric
                and not RE_NON_HYMN_RUBRIC_START.match(txt)
                and not txt.startswith("[")
                and not txt.startswith("*(")
                and not txt.startswith("(*")
                and not txt.startswith("*[")
                and current_section_slug not in ("front_matter", "synaxarion", "paremia", "patristic_homily", "gospel")
                and (
                    RE_EXPLICIT_HYMN_START.match(first_line)
                    or re.match(r"^\*\*We\s+magnify\s+(?:Thee|you)\b", first_line, re.IGNORECASE)
                    or (
                        active_hymn_subtype_cue is not None
                        and len(txt) >= 40
                        and not bool(re.search(r":\*(?:\s*\[\^\d+\])*$", txt))
                    )
                    or (
                        mon_type in HYMNOGRAPHIC_AND_HOROLOGION_TYPES
                        and not txt.startswith("|")
                        and (
                            current_ode is not None
                            or active_podoben_id is not None
                            or active_stichos is not None
                            or current_section_slug
                            in (
                                "stichera_lord_i_call",
                                "stichera_litiya",
                                "stichera_aposticha",
                                "stichera_praises",
                                "sessionals",
                                "gradual",
                                "hypakoe",
                                "kontakion_ikos",
                                "exapostilarion",
                                "beatitudes",
                                "troparia",
                            )
                        )
                        and len(txt) >= 45
                    )
                )
            ):
                unit_class = "PROPER_HYMN"
                active_psalm_or_lection = False
                fl_low = first_line.lower()
                if "heirmos" in fl_low:
                    unit_subtype = "HEIRMOS"
                elif "katavasia" in fl_low:
                    unit_subtype = "KATAVASIA"
                elif (
                    "stavrotheotokion" in fl_low
                    or "staurotheotokion" in fl_low
                    or "cross-theotokion" in fl_low
                    or "to the cross" in fl_low
                ):
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
                    current_ode = None
                    current_section_slug = "kontakion_ikos"
                elif "ikos" in fl_low:
                    unit_subtype = "IKOS"
                    current_ode = None
                    current_section_slug = "kontakion_ikos"
                elif "sessional" in fl_low or "kathisma" in fl_low or "stichologia" in fl_low:
                    unit_subtype = "SESSIONAL_HYMN"
                    current_ode = None
                    current_section_slug = "sessionals"
                elif "exapost" in fl_low or "photagog" in fl_low or "hymn of light" in fl_low:
                    unit_subtype = "EXAPOSTILARION"
                    current_ode = None
                    current_section_slug = "exapostilarion"
                elif "evangelical" in fl_low or "eothinon" in fl_low:
                    unit_subtype = "EOTHINON"
                elif "hypakoe" in fl_low or "ypakoe" in fl_low:
                    unit_subtype = "HYPAKOE"
                    current_ode = None
                    current_section_slug = "hypakoe"
                elif "gradual" in fl_low or "ascent" in fl_low or "antiphon" in fl_low:
                    unit_subtype = "ANABATHMOS"
                    current_ode = None
                    current_section_slug = "gradual"
                elif "beatitudes" in fl_low or current_section_slug == "beatitudes":
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

                # Multi-canon Ode counter & Canon Tone preservation across Sessionals/Kontakia (T-2, T-5)
                if current_ode is not None:
                    if unit_subtype == "HEIRMOS" or re.search(r"\banother\s+\[?canon\b", fl_low):
                        if ode_stanza_total == 0:
                            current_canon_num = 1
                        else:
                            current_canon_num += 1
                        ode_troparion_seq = 0
                        if m_in_t and current_tone:
                            canon_tones_by_num[current_canon_num] = current_tone
                        elif current_canon_num in canon_tones_by_num:
                            current_tone = canon_tones_by_num[current_canon_num]
                        elif part_governing_tone:
                            current_tone = part_governing_tone
                    else:
                        if current_canon_num == 0:
                            current_canon_num = 1
                        if not m_in_t:
                            if current_canon_num in canon_tones_by_num:
                                current_tone = canon_tones_by_num[current_canon_num]
                            elif part_governing_tone:
                                current_tone = part_governing_tone
                    ode_stanza_total += 1
                elif not m_in_t and mon_type == "octoechos" and part_governing_tone and current_section_slug not in ("sessionals", "kontakion_ikos", "exapostilarion"):
                    current_tone = part_governing_tone

                # Check if inline Podoben is attached to the hymn's first line
                if "podoben:" in fl_low:
                    m_pod_in = RE_PODOBEN_HEADER.search(first_line)
                    pod_lbl = (m_pod_in.group(1) or m_pod_in.group(2) or "").strip() if m_pod_in else ""
                    pod_slav = extract_podoben_slavonic_incipit(first_line, slav_text)
                    p_id, _, _ = match_podoben_model(first_line, pod_slav or "", current_tone or 1, pod_catalog)
                    active_podoben_id = p_id
                    active_podoben_slavonic = pod_slav
                    active_podoben_label_raw = pod_lbl or first_line.strip("* ")

                # Route to Shared_Lexicon 4-Shard Corpus
                if unit_subtype in ("HEIRMOS", "KATAVASIA"):
                    target_shard = "03_irmologion.json"
                    codex_domain = "IRMOLOGION"
                elif current_ode is not None and unit_subtype in (
                    "CANON_TROPARION",
                    "THEOTOKION",
                    "STAVROTHEOTOKION",
                    "TRIADIKON",
                    "MARTYRIKON",
                    "NEKROSIMON",
                ):
                    target_shard = "04_kanonnik.json"
                    codex_domain = "KANONNIK"
                else:
                    target_shard = "02_sticherarion.json"
                    codex_domain = "STICHERARION"

                # Compute Stamford sequence suffix (_1, _2, _glory, _both_now, _glory_both_now)
                if "glory" in fl_low and "both now" in fl_low:
                    doxology_tag = "GLORY_BOTH_NOW"
                    stamford_suffix = "_glory_both_now"
                    active_doxology_tag = None
                elif fl_low.startswith("*glory"):
                    doxology_tag = "GLORY"
                    stamford_suffix = "_glory"
                    active_doxology_tag = None
                elif fl_low.startswith("*both now"):
                    doxology_tag = "BOTH_NOW"
                    stamford_suffix = "_both_now"
                    active_doxology_tag = None
                elif active_doxology_tag:
                    doxology_tag = active_doxology_tag
                    stamford_suffix = f"_{active_doxology_tag.lower()}"
                    active_doxology_tag = None
                else:
                    section_hymn_seq += 1
                    stamford_suffix = f"_{section_hymn_seq}"

                # Compute local_slot_suffix for v4.0.0 internal_coordinates (T-5, T-7)
                if current_ode is not None:
                    c_num = max(1, current_canon_num)
                    if unit_subtype == "HEIRMOS":
                        local_slot_suffix = f"_c{c_num}_irmos"
                    elif unit_subtype == "KATAVASIA":
                        local_slot_suffix = f"_c{c_num}_katavasia"
                    elif unit_subtype == "STAVROTHEOTOKION":
                        local_slot_suffix = f"_c{c_num}_stavrotheotokion"
                    elif unit_subtype == "THEOTOKION" or doxology_tag in ("GLORY_BOTH_NOW", "BOTH_NOW"):
                        local_slot_suffix = f"_c{c_num}_theotokion"
                    elif unit_subtype == "TRIADIKON" or doxology_tag == "GLORY":
                        local_slot_suffix = f"_c{c_num}_glory"
                    else:
                        ode_troparion_seq += 1
                        local_slot_suffix = f"_c{c_num}_{ode_troparion_seq}"
                else:
                    if unit_subtype == "KONTAKION":
                        local_slot_suffix = "_kontakion"
                    elif unit_subtype == "IKOS":
                        local_slot_suffix = "_ikos"
                    else:
                        local_slot_suffix = stamford_suffix or f"_{section_hymn_seq}"

            # 5. Otherwise RUBRIC_OR_STATUTE
            else:
                unit_class = "RUBRIC_OR_STATUTE"
                active_stichos = None
                active_doxology_tag = None
                low_t = txt.lower()
                if re.search(r"(?:psalm\s+(?:of\s+david,?\s*)?\d+|\[lxx\s+ps\.\s*\d+\]):?\*(?:\s*\[\^\d+\])*$", low_t):
                    active_psalm_or_lection = True
                elif re.search(
                    r"\b(kontakion|troparion|theotokion|sessional\s+hymn|hypakoe|exapostilarion|stichera|troparia)\b[^*\n]*:\*(?:\s*\[\^\d+\])*$",
                    low_t,
                ):
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
                elif re.search(
                    r"\b(?:Instruction\s+of\s+Saint|Discourse\s+of\s+Saint|Catechetical\s+Word\s+of|Homily)\b",
                    txt,
                    re.IGNORECASE,
                ) or current_section_slug == "patristic_homily":
                    unit_subtype = "PATRISTIC_HOMILY"
                elif "synaxarion" in low_t or current_section_slug == "synaxarion" or ("in the same month" in low_t and len(txt) >= 200):
                    unit_subtype = "HAGIOGRAPHICAL_SYNAXARION"
                elif re.search(
                    r"\b(?:if\s+it\s+be\s+a\s+Sunday|if\s+the\s+Feast\s+falls|it\s+should\s+be\s+known\s+that|when\s+the\s+feast\s+of)\b",
                    low_t,
                ):
                    unit_subtype = "COLLISION_MARKIAN_RULE"
                elif re.search(r"\b(?:if\s+a\s+child\s+be\s+weak|in\s+danger\s+of\s+death|cautela|warning\s+to\s+the\s+priest)\b", low_t):
                    unit_subtype = "SACRAMENTAL_CAUTELA"
                elif re.search(
                    r"\b(?:gave\s+this\s+book|in\s+the\s+name\s+of\s+the\s+father.*servant\s+of\s+god.*presented|cursed\s+and\s+anathematized)\b",
                    low_t,
                ):
                    unit_subtype = "DEDICATION_OR_FOUNDATION_INSCRIPTION"
                elif txt.startswith("[") or txt.startswith("*(") or "woodcut" in low_t or "headpiece" in low_t or "vacat" in low_t:
                    unit_subtype = "VISUAL_ORNAMENT_OR_MARGINALIA"
                elif paratext_flag or (c_idx == 1 and ("to the reader" in low_t or "preface" in low_t or "title page" in low_t or "printed" in low_t)):
                    unit_subtype = "FRONT_MATTER_PARATEXT"
                elif re.search(r"\b(?:we\s+stitch|we\s+insert|sign\s+to\s+sing|twice|thrice|stichera\s+on\s+\d+)\b", low_t):
                    unit_subtype = "HYMNOGRAPHIC_PRESCRIPTION"
                else:
                    unit_subtype = "CEREMONIAL_ACTION"

        leaf_seq = leaf_seq_counter.get(leaf_num, 0) + 1
        leaf_seq_counter[leaf_num] = leaf_seq
        corpus_id = f"{book_prefix}.{monument_id.upper()}.C{c_idx:03d}.P{leaf_num:04d}.U{leaf_seq:03d}"
        physical_unit_id = corpus_id

        fn_refs = [f"[^{m}]" for m in re.findall(r"\[\^(\d+)\]", txt)]
        actors_found = [a for a in ACTOR_KEYWORDS if re.search(rf"\b{a}\b", txt, re.IGNORECASE)]
        realia_found = [r for r in REALIA_KEYWORDS if re.search(rf"\b{r}\b", txt, re.IGNORECASE)]
        is_cond = bool(re.search(r"\b(?:if|when|whenever|unless|should)\b", txt[:80], re.IGNORECASE))

        parent_heirmos_id = (
            f"HEIRMOS.T{current_tone}.ODE{current_ode}"
            if (unit_class == "PROPER_HYMN" and current_ode in range(1, 10) and current_tone in range(1, 9))
            else None
        )

        if mon_type == "octoechos":
            feast_or_tone_slug = f"tone_{part_governing_tone or current_tone or 1}"
        elif active_month_num is not None and active_day_num is not None and not in_front_matter:
            feast_or_tone_slug = f"month_{active_month_num:02d}_day_{active_day_num:02d}"
        else:
            feast_or_tone_slug = slugify_coordinate(current_season_or_tone)
        attestation_mode = classify_attestation_mode(txt, slav_text)
        internal_coordinates = {
            "cycle_code": cycle_name,
            "feast_or_tone_slug": feast_or_tone_slug,
            "day_of_week": current_day_slug,
            "office_slug": current_office_slug,
            "section_slug": current_section_slug,
            "tone": current_tone,
            "ode_number": current_ode,
            "canon_number": max(1, current_canon_num) if current_ode is not None else None,
            "local_slot_suffix": local_slot_suffix,
            "podoben_label_raw": active_podoben_label_raw if unit_class == "PROPER_HYMN" else None,
            "podoben_slavonic_incipit": active_podoben_slavonic if unit_class == "PROPER_HYMN" else None,
        }

        unit_record: Dict[str, Any] = {
            "physical_unit_id": physical_unit_id,
            "corpus_id": corpus_id,
            "monument_id": monument_id,
            "monument_type": mon_type,
            "canonical_recension_witness_id": stratum_meta["canonical_recension_witness_id"],
            "historical_stratum": stratum_meta["historical_stratum"],
            "stratum_witness_id": stratum_meta["stratum_witness_id"],
            "stratum_primacy_rank": stratum_meta["stratum_primacy_rank"],
            "unit_class": unit_class,
            "unit_subtype": unit_subtype,
            "attestation_mode": attestation_mode,
            "target_shard": target_shard,
            "codex_domain": codex_domain,
            "cohort": c_idx,
            "leaf": f"p{leaf_num}",
            "leaf_span": blk["leaf_span"],
            "locus": locus,
            "running_header": blk["running_header"],
            "verbatim_book_heading": f"{part_h1} :: {office_h2}",
            "verbatim_section_rubric": current_section_rubric_verbatim,
            "internal_coordinates": internal_coordinates,
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
            "slavonic_diplomatic": slav_text,
            "english_cohort_translation": txt,
            "slavonic_text": slav_text,
            "english_text": txt,
            "alignment_method": slav_block.get("alignment_method", "NW_DIRECT") if slav_block else "UNALIGNED",
            "footnotes_referenced": fn_refs,
            "slavonic_provenance": slav_provenance,
            "cohort_provenance": blk["provenance"],
            "provenance": blk["provenance"],
        }
        atomic_units.append(unit_record)

        if unit_class == "PROPER_HYMN":
            propers_items.append({
                "physical_unit_id": physical_unit_id,
                "corpus_id": corpus_id,
                "monument_id": monument_id,
                "monument_type": mon_type,
                "canonical_recension_witness_id": stratum_meta["canonical_recension_witness_id"],
                "historical_stratum": stratum_meta["historical_stratum"],
                "stratum_witness_id": stratum_meta["stratum_witness_id"],
                "stratum_primacy_rank": stratum_meta["stratum_primacy_rank"],
                "attestation_mode": attestation_mode,
                "alignment_method": slav_block.get("alignment_method", "NW_DIRECT") if slav_block else "UNALIGNED",
                "verbatim_book_heading": f"{part_h1} :: {office_h2}",
                "verbatim_section_rubric": current_section_rubric_verbatim,
                "internal_coordinates": internal_coordinates,
                "tone": current_tone or 0,
                "cohort": c_idx,
                "leaf": f"p{leaf_num}",
                "locus": locus,
                "office": office_h2,
                "section": current_section,
                "season_or_tone": current_season_or_tone,
                "day_or_date": current_day_or_date,
                "ode": current_ode,
                "canon_number": max(1, current_canon_num) if current_ode is not None else None,
                "hymn_type": unit_subtype,
                "target_shard": target_shard,
                "codex_domain": codex_domain,
                "podoben_id": active_podoben_id,
                "podoben_slavonic_witness": active_podoben_slavonic,
                "parent_heirmos_id": parent_heirmos_id,
                "preceding_stichos": active_stichos,
                "doxology_tag": doxology_tag,
                "stamford_slug_suffix": stamford_suffix,
                "local_slot_suffix": local_slot_suffix,
                "slavonic_diplomatic": slav_text,
                "english_cohort_translation": txt,
                "slavonic_text": slav_text,
                "english_text": txt,
                "slavonic_provenance": slav_provenance,
                "cohort_provenance": blk["provenance"],
                "provenance": blk["provenance"],
            })
            # Consume preceding_stichos once attached to its governed hymn (T-4)
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
        "canonical_recension_witness_id": stratum_meta["canonical_recension_witness_id"],
        "canonical_recension_title": stratum_meta["canonical_recension_title"],
        "historical_stratum": stratum_meta["historical_stratum"],
        "stratum_witness_id": stratum_meta["stratum_witness_id"],
        "stratum_primacy_rank": stratum_meta["stratum_primacy_rank"],
        "corpus_schema": "4.0.0",
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

    def _atomic_json_write(p: Path, payload_obj: dict) -> None:
        raw_s = json.dumps(payload_obj, indent=2, ensure_ascii=False) + "\n"
        tmp_p = p.with_name(p.name + ".tmp_corpus")
        tmp_p.write_text(raw_s, encoding="utf-8", newline="\n")
        for att in range(8):
            try:
                tmp_p.replace(p)
                return
            except OSError:
                if att == 7:
                    if tmp_p.exists():
                        tmp_p.unlink()
                    raise
                import time
                time.sleep(0.35)

    atomic_path = final_md_dir / f"{monument_id}_atomic_corpus.json"
    _atomic_json_write(atomic_path, atomic_payload)
    print(
        f"  [Atomic Corpus] Emitted {atomic_path.relative_to(PROJECT_ROOT)} "
        f"({len(atomic_units):,} total units: {counts_by_class['PROPER_HYMN']:,} propers, "
        f"{len(atomic_units) - counts_by_class['PROPER_HYMN']:,} non-propers)"
    )

    # Emit {monument_id}_propers_corpus.json across all monument types (Octoechos freeze guard removed — T-3)
    propers_path = final_md_dir / f"{monument_id}_propers_corpus.json"
    if propers_items:
        propers_payload = {
            "monument_id": monument_id,
            "monument_type": mon_type,
            "canonical_recension_witness_id": stratum_meta["canonical_recension_witness_id"],
            "canonical_recension_title": stratum_meta["canonical_recension_title"],
            "historical_stratum": stratum_meta["historical_stratum"],
            "stratum_witness_id": stratum_meta["stratum_witness_id"],
            "stratum_primacy_rank": stratum_meta["stratum_primacy_rank"],
            "corpus_schema": "4.0.0",
            "corpus_type": f"{mon_type.upper()}_PROPERS_BILINGUAL_COMPLETE",
            "source_provenance": {
                "source_dir": f"{ws_rel}/Source Text",
                "cohorts_dir": f"{ws_rel}/Cohorts",
                "total_stanzas_extracted": len(propers_items),
            },
            "items": propers_items,
        }
        _atomic_json_write(propers_path, propers_payload)
        print(f"  [Propers Corpus] Emitted {propers_path.relative_to(PROJECT_ROOT)} ({len(propers_items):,} proper hymns)")
    elif propers_path.exists():
        propers_path.unlink()
        print(f"  [Propers Corpus] Removed stale empty propers corpus {propers_path.relative_to(PROJECT_ROOT)}")

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
            from scripts.assemble_and_sync_hub import get_hub_inbox
            pub_spec = mon_info.get("publication_spec", {})
            hub_folder = pub_spec.get("hub_inbox_folder", monument_id)
            target_inbox = get_hub_inbox(hub_folder)
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
                elif (target_inbox / comp_name).exists() and comp_name.endswith("_propers_corpus.json"):
                    (target_inbox / comp_name).unlink()
            print(f"  [Hub Sync] Synced {synced} atomic/podoben deliverables to Typikon Coded/Data/Inbox/{hub_folder}")

    if emit_event:
        emit_pipeline_ready_event(
            monument_id=monument_id,
            mon_info=mon_info,
            mon_type=mon_type,
            ws_rel=ws_rel,
            atomic_path=atomic_path,
            propers_path=propers_path,
            total_pages=total_pages,
            leaves_covered_count=len(leaves_covered),
            total_atomic_units=len(atomic_units),
            total_propers_units=len(propers_items),
            counts_by_class=counts_by_class,
        )

    return atomic_payload


def batch_extract_all_completed(sync_hub: bool = False, emit_event: bool = False) -> Dict[str, Any]:
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
        if status != "completed":
            continue
        ws_dir = PROJECT_ROOT / mon_info.get("workspace_dir", f"Liturgical Monuments/{mon_id}")
        if not ws_dir.exists():
            continue
        has_cohorts = (ws_dir / "Cohorts").exists() and bool(list((ws_dir / "Cohorts").glob("*cohort*.md")))
        has_final = (ws_dir / "Final").exists() and bool(list((ws_dir / "Final").glob("*.txt")))
        if not (has_cohorts or has_final):
            continue

        payload = extract_monument_atomic_corpus(mon_id, sync_hub=sync_hub, emit_event=emit_event)
        c_class = payload["summary"]["counts_by_unit_class"]
        c_shard = payload["summary"]["counts_by_target_shard"]
        u_total = payload["source_provenance"]["total_atomic_units"]
        total_units_all += u_total

        for k, v in c_class.items():
            global_by_class[k] = global_by_class.get(k, 0) + v
        for k, v in c_shard.items():
            global_by_shard[k] = global_by_shard.get(k, 0) + v

        propers_cnt = int(c_class.get("PROPER_HYMN", 0))
        euch_cnt = (
            int(c_class.get("SACERDOTAL_PRAYER", 0))
            + int(c_class.get("LITANY_OR_DIALOGUE", 0))
            + int(c_class.get("FIXED_ORDINARY_OR_LECTION", 0))
        )
        ws_rel = mon_info.get("workspace_dir", f"Liturgical Monuments/{mon_id}")
        stratum_meta = resolve_monument_recension_stratum(mon_id, mon_info)
        summaries.append({
            "monument_id": mon_id,
            "canonical_recension_witness_id": stratum_meta["canonical_recension_witness_id"],
            "historical_stratum": stratum_meta["historical_stratum"],
            "stratum_witness_id": stratum_meta["stratum_witness_id"],
            "stratum_primacy_rank": stratum_meta["stratum_primacy_rank"],
            "chronology_year": stratum_meta["chronology_year"],
            "monument_type": payload["monument_type"],
            "status": status,
            "has_propers_corpus": bool(propers_cnt > 0),
            "leaves_covered": payload["source_provenance"]["leaves_covered_count"],
            "cross_leaf_stitched": payload["source_provenance"]["cross_leaf_stitched_units"],
            "total_units": u_total,
            "PROPER_HYMN": propers_cnt,
            "SACERDOTAL_PRAYER": c_class.get("SACERDOTAL_PRAYER", 0),
            "LITANY_OR_DIALOGUE": c_class.get("LITANY_OR_DIALOGUE", 0),
            "FIXED_ORDINARY_OR_LECTION": c_class.get("FIXED_ORDINARY_OR_LECTION", 0),
            "RUBRIC_OR_STATUTE": c_class.get("RUBRIC_OR_STATUTE", 0),
            "euchological_units_count": euch_cnt,
            "event_file": f"Typikon Coded/Data/Inbox/pipeline_events/translation_{mon_id}.ready.json",
            "atomic_corpus_path": f"Translation/{ws_rel}/Final MD/{mon_id}_atomic_corpus.json",
            "propers_corpus_path": (
                f"Translation/{ws_rel}/Final MD/{mon_id}_propers_corpus.json"
                if propers_cnt > 0
                else None
            ),
        })

    now_iso = datetime.now(timezone.utc).isoformat()
    propers_monument_ids = [s["monument_id"] for s in summaries if s["has_propers_corpus"]]
    chronology_map = {s["monument_id"]: s["chronology_year"] for s in summaries}

    ledger = {
        "generated_at": now_iso,
        "corpus_schema": "4.0.0",
        "canonical_recension_witness_id": CANONICAL_RECENSION_WITNESS_ID,
        "canonical_recension_title": CANONICAL_RECENSION_TITLE,
        "canonical_witness_priority_order": list(CANONICAL_WITNESS_PRIORITY_ORDER),
        "total_monuments_extracted": len(summaries),
        "propers_bearing_monuments_count": len(propers_monument_ids),
        "total_atomic_units_extracted": total_units_all,
        "global_counts_by_unit_class": global_by_class,
        "global_counts_by_target_shard": global_by_shard,
        "monument_chronology_year_map": chronology_map,
        "propers_monument_ids": propers_monument_ids,
        "monuments": summaries,
    }

    audit_dir = PROJECT_ROOT / "Audit_Reports"
    audit_dir.mkdir(parents=True, exist_ok=True)
    ledger_json = audit_dir / "ATOMIC_CORPUS_LEDGER.json"
    ledger_md = audit_dir / "ATOMIC_CORPUS_LEDGER.md"
    ledger_json.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if emit_event:
        events_dir = PROJECT_ROOT.parent / "Typikon Coded" / "Data" / "Inbox" / "pipeline_events"
        events_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = events_dir / "translation_corpus_manifest.ready.json"
        manifest_payload = {
            "event_type": "TRANSLATION_CORPUS_MANIFEST_READY",
            "schema_version": "4.0.0",
            "producer_spoke": "Translation",
            "canonical_recension_witness_id": CANONICAL_RECENSION_WITNESS_ID,
            "canonical_recension_title": CANONICAL_RECENSION_TITLE,
            "canonical_witness_priority_order": list(CANONICAL_WITNESS_PRIORITY_ORDER),
            "generated_at": now_iso,
            "total_monuments_ready": len(summaries),
            "propers_bearing_monuments_count": len(propers_monument_ids),
            "total_atomic_units": total_units_all,
            "total_propers_units": global_by_class.get("PROPER_HYMN", 0),
            "monument_chronology_year_map": chronology_map,
            "propers_monument_ids": propers_monument_ids,
            "monuments": summaries,
        }
        manifest_path.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(
            f"[Manifest] Emitted Typikon Coded/Data/Inbox/pipeline_events/{manifest_path.name} "
            f"({len(summaries)} monuments ready, {len(propers_monument_ids)} propers-bearing)."
        )

    md_lines = [
        "# Universal Atomic Liturgical Corpus Ledger (Propers + Non-Propers)",
        "",
        f"- **Generated At**: `{ledger['generated_at']}`",
        "- **Corpus Schema**: `4.0.0`",
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
    parser = argparse.ArgumentParser(description="Universal Atomic Liturgical Corpus Extractor (v4.0.0)")
    parser.add_argument("--monument", help="Extract atomic corpus for a single monument ID")
    parser.add_argument("--all-completed", action="store_true", help="Batch-extract all completed/audited monuments")
    parser.add_argument("--sync-hub", action="store_true", help="Synchronize emitted corpora and Podoben grids to Typikon Coded Hub Inbox")
    parser.add_argument("--emit-event", action="store_true", help="Update codex_registry.json pipeline_sync_state and emit pipeline_events/*.ready.json")
    args = parser.parse_args()

    if args.all_completed:
        batch_extract_all_completed(sync_hub=args.sync_hub, emit_event=args.emit_event)
    elif args.monument:
        extract_monument_atomic_corpus(args.monument, sync_hub=args.sync_hub, emit_event=args.emit_event)
    else:
        parser.error("Provide --monument <ID> or --all-completed")


if __name__ == "__main__":
    main()
