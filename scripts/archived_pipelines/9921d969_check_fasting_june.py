import sys
sys.path.append(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded")

from ruthenian_engine import RuthenianEngine
from datetime import date

e = RuthenianEngine('.')

for d in range(7, 30):
    dt = date(2026, 6, d)
    ctx = e.get_liturgical_context(dt)
    rule = e.resolve_fasting_rule(ctx)
    print(f"Date: {dt} | Type: {rule.get('type')} | Note: {rule.get('note')} | Rank: {ctx.get('rank')} | Commem: {ctx.get('dolnytsky_commemoration')}")
