# -*- coding: utf-8 -*-
from pathlib import Path
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base = Path("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon")
src = base / "Source Text" / "1910_skaballanovich_typikon_cohort10_source.txt"
draft = base / "Draft" / "1910_skaballanovich_typikon_cohort10_raw_draft.md"
fn = base / "Draft" / "1910_skaballanovich_typikon_cohort10_footnotes.txt"

for p in [src, draft, fn]:
    assert p.exists(), f"Missing {p}"
    lines = len(p.read_text(encoding="utf-8").splitlines())
    print(f"File: {p.name} | Size: {p.stat().st_size:,} bytes | Lines: {lines:,}")

draft_text = draft.read_text(encoding="utf-8")
fn_text = fn.read_text(encoding="utf-8")
src_text = src.read_text(encoding="utf-8")

draft_markers = [int(x) for x in re.findall(r"\[\^(\d+)\]", draft_text)]
fn_defs = [int(x) for x in re.findall(r"\[\^(\d+)\]:", fn_text)]

print(f"Draft footnote markers: {len(draft_markers)} (span: [^{min(draft_markers)}]..[^{max(draft_markers)}])")
print(f"Footnote definitions: {len(fn_defs)} (span: [^{min(fn_defs)}:]..[^{max(fn_defs)}:])")
assert draft_markers == sorted(draft_markers), "Markers are not sorted!"
assert set(draft_markers) == set(fn_defs), "Markers and defs do not match!"

banned = ["for ever and ever", "wherefore", "verily", "betwixt", "methinks", "twas"]
for b in banned:
    assert not re.search(r"\b" + b + r"\b", draft_text, re.IGNORECASE), f"Found banned: {b}"
print("All banned phrases check: PASSED (zero violations).")

for leaf in range(91, 101):
    m = f"=== LEAF p{leaf} ==="
    assert m in src_text, f"Missing {m} in source"
    assert m in draft_text, f"Missing {m} in draft"
print("Leaf banners check: PASSED (all 10 leaves p91..p100 present in source and draft).")
print("\n>>> ALL CHECKS PASSED PERFECTLY! <<<")
