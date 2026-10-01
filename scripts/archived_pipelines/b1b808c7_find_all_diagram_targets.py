#!/usr/bin/env python3
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

proj_root = Path(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation")
app_path = proj_root / "Final" / "Final_Dolnytsky_appendix.txt"
app_txt = app_path.read_text(encoding='utf-8')
lines = app_txt.splitlines()

targets = [
    # 1. Entrance (Vespers)
    ('51. For the Entrance', 'After the call of the Deacon'),
    # 2. Narthex (Vespers Litiya)
    ('71. Then, during the procession', 'If only one deacon censes'),
    # 3. Blessing of Loaves
    ('72. At the blessing of loaves', 'After the blessing of loaves'),
    # 4. Magnification (Matins)
    ('middle before the tetrapod, and to his right - the deacon.', '95. Then all sing the Magnification.'),
    # 5. Paschal Matins Church Doors
    ('In the narthex all stand before the closed church doors.', 'Here the principal celebrant takes the censer'),
    # 6. Proskomedia Lamb
    ('saying: "One of the soldiers."', '109. The Deacon, having taken wine and water'),
    # 7. Little Entrance (Two Deacons)
    ('and the priest stands in the middle behind them.', 'The first deacon says: "Let us pray to the Lord,"'),
    # 8. Before Little Entrance (Concelebration)
    ('occupy their places near the holy table.', 'concelebrants sit near the High Throne'),
    # 9. High Throne (Concelebration)
    ('concelebrants sit near the High Throne', 'During the reading of the Gospel all remain in their places'),
    # 10. Concelebrants Communion
    ('communion of the Most Precious Blood from the principal celebrant.', 'Each, having just communicated')
]

for idx, (pre, post) in enumerate(targets, 1):
    found_pre = [i for i, l in enumerate(lines) if pre in l]
    found_post = [i for i, l in enumerate(lines) if post in l]
    print(f"=== Diagram {idx} ===")
    print(f"  Pre target: '{pre}' -> Line(s): {[p+1 for p in found_pre]}")
    print(f"  Post target: '{post}' -> Line(s): {[p+1 for p in found_post]}")
    if found_pre and found_post:
        print(f"  Lines range: {found_pre[0]+1} to {found_post[0]+1}")
        for ln in range(found_pre[0], min(found_post[0]+1, len(lines))):
            print(f"    {ln+1}: {lines[ln][:100]}")
