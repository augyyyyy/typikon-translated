import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import fitz
from pathlib import Path

reg_path = Path('Liturgical Monuments/codex_registry.json')
reg = json.loads(reg_path.read_text(encoding='utf-8'))
base_e = Path(r'E:\Google Drive\Liturgical Library')

print(f'Checking {len(reg["monuments"])} monuments in registry against local Drive E: storage...\n')

found_count = 0
results = []
for idx, (mon_id, info) in enumerate(reg['monuments'].items()):
    rel_pdf = info.get('relative_pdf_path', '')
    
    # Check 1: Direct relative path from base_e
    direct_p = base_e / rel_pdf
    
    # Check 2: Try finding by basename in base_e
    actual_p = None
    if direct_p.exists():
        actual_p = direct_p
    else:
        pdf_name = Path(rel_pdf).name
        matches = list(base_e.rglob(pdf_name))
        if matches:
            actual_p = matches[0]

    # Check 3: Check Drive C: workspace if any
    if not actual_p:
        ws_dir = Path(info.get('workspace_dir', ''))
        if ws_dir.exists():
            c_matches = list(ws_dir.rglob('*.pdf'))
            if c_matches:
                actual_p = c_matches[0]

    if actual_p and actual_p.exists():
        found_count += 1
        size_mb = actual_p.stat().st_size / (1024 * 1024)
        try:
            doc = fitz.open(actual_p)
            pages = len(doc)
            results.append((idx, mon_id, True, pages, size_mb, actual_p))
            print(f'[{idx:02d}] FOUND: {mon_id:<28} | {pages:>4} pages | {size_mb:>6.1f} MB | {actual_p.name}')
        except Exception as e:
            results.append((idx, mon_id, False, 0, 0, str(e)))
            print(f'[{idx:02d}] ERROR: {mon_id:<28} | {e}')
    else:
        results.append((idx, mon_id, False, 0, 0, None))
        print(f'[{idx:02d}] MISSING: {mon_id:<26} | Target: {rel_pdf}')

print(f'\n======================================================')
print(f'VERIFICATION SUMMARY: {found_count} / {len(reg["monuments"])} MONUMENTS PRESENT LOCALLY')
print(f'======================================================')
