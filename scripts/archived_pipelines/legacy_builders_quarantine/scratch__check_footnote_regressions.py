import re
from pathlib import Path

def check_fn_sequence(name, path):
    text = Path(path).read_text(encoding='utf-8')
    # find lines where footnotes occur
    calls = []
    for line_num, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"\[\^(\d+)\]", line):
            if not line.strip().startswith("[^"): # not definition
                calls.append((line_num, int(m.group(1))))
    
    # check for regressions (where call_id < previous call_id)
    regressions = []
    for i in range(1, len(calls)):
        prev_line, prev_id = calls[i-1]
        curr_line, curr_id = calls[i]
        if curr_id < prev_id:
            regressions.append((prev_line, prev_id, curr_line, curr_id))
            
    print(f"\n=== {name} Footnote Calls Sequence ===")
    print(f"Total non-def calls: {len(calls)}")
    print(f"Number of regressions: {len(regressions)}")
    if regressions:
        print("Sample regressions (where footnote number drops):")
        for r in regressions[:5]:
            print(f"  Line {r[0]} ([^{r[1]}]) -> Line {r[2]} ([^{r[3]}])")

check_fn_sequence("M1 (1891 Synod)", "Liturgical Monuments/Monument 1 - 1891 Lviv Synod/Final MD/1891_lviv_synod_complete.md")
check_fn_sequence("M2 (1899 Dolnytsky)", "Liturgical Monuments/Monument 2 - 1899 Dolnytsky Typikon/Final MD/1899_dolnytsky_typikon_complete.md")
check_fn_sequence("M3 (1901 Mikita)", "Liturgical Monuments/Monument 3 - 1901 Mikita Typikon/Final MD/1901_mikita_typikon_complete.md")
