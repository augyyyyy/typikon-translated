from pathlib import Path
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

txt = Path('scratch/cohort56_extracted/notes_p964.txt').read_text(encoding='utf-8')
print(txt)
