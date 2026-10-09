import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# We can read each p{pno}.txt from scratch/cohort76_extracted/ and format properly
source_leaves = {}

for pno in range(751, 761):
    raw = Path(f'scratch/cohort76_extracted/p{pno}.txt').read_text(encoding='utf-8')
    # Let's inspect paragraphs and clean up soft line breaks
    # Replace non-breaking spaces with standard space
    raw = raw.replace('\xa0', ' ')
    source_leaves[pno] = raw

print("Read all leaves successfully.")
