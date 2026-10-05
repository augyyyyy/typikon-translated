import os, re
from pathlib import Path

base_dir = Path("Typikons/1891 Lviv Synod")

files = {
    'source': base_dir / 'Source Text' / '1891_lviv_synod_cohort7_source.txt',
    'draft_md': base_dir / 'Draft' / '1891_lviv_synod_cohort7_raw_draft.md',
    'draft_fn': base_dir / 'Draft' / '1891_lviv_synod_cohort7_footnotes.txt',
    'final_md': base_dir / 'Final MD' / '1891_synod_cohort7.md',
    'final_txt': base_dir / 'Final' / '1891_synod_cohort7.txt',
    'final_fn': base_dir / 'Final' / 'Final_footnotes.txt'
}

print('=== FILE STATS ===')
for name, path in files.items():
    if path.exists():
        content = path.read_text(encoding='utf-8')
        lines = content.count('\n') + 1
        bytes_len = len(content.encode('utf-8'))
        print(f'{name:10}: {lines:5} lines, {bytes_len:6} bytes | {path.name}')
    else:
        print(f'{name:10}: MISSING')

print('\n=== FOOTNOTE MONOTONICITY & BIJECTIVITY ===')
fn_draft = set(re.findall(r'\[\^(\d+)\]:', files['draft_fn'].read_text(encoding='utf-8')))
fn_draft_md = set(re.findall(r'\[\^(\d+)\](?!:)', files['draft_md'].read_text(encoding='utf-8')))
fn_final_md_body = set(re.findall(r'\[\^(\d+)\](?!:)', files['final_md'].read_text(encoding='utf-8')))
fn_final_md_defs = set(re.findall(r'\[\^(\d+)\]:', files['final_md'].read_text(encoding='utf-8')))
fn_final_txt_body = set(re.findall(r'\[\^(\d+)\](?!:)', files['final_txt'].read_text(encoding='utf-8')))
fn_final_txt_defs = set(re.findall(r'\[\^(\d+)\]:', files['final_txt'].read_text(encoding='utf-8')))

expected = set(str(i) for i in range(70, 112))
print('Expected footnotes [70..111]: count =', len(expected))
print('Draft defs match expected:', fn_draft == expected, f'(count: {len(fn_draft)})')
print('Draft MD body markers match expected:', fn_draft_md == expected, f'(count: {len(fn_draft_md)})')
print('Final MD body markers match expected:', fn_final_md_body == expected, f'(count: {len(fn_final_md_body)})')
print('Final MD defs match expected:', fn_final_md_defs == expected, f'(count: {len(fn_final_md_defs)})')
print('Final TXT body markers match expected:', fn_final_txt_body == expected, f'(count: {len(fn_final_txt_body)})')
print('Final TXT defs match expected:', fn_final_txt_defs == expected, f'(count: {len(fn_final_txt_defs)})')

print('\n=== FORBIDDEN VARIANTS CHECK ===')
forbidden = ['for ever and ever', 'Eye of the Church', 'Trephologion', 'Samohlasen', 'Podiben', 'Prokeimenon', 'Kafisma']
for name in ['draft_md', 'final_md', 'final_txt']:
    content = files[name].read_text(encoding='utf-8')
    violations = [t for t in forbidden if t.lower() in content.lower()]
    if violations:
        print(f'VIOLATION in {name}: found {violations}')
    else:
        print(f'{name}: all forbidden term checks passed.')
