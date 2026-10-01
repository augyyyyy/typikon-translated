import sys
from datetime import date
from ruthenian_engine import RuthenianEngine

# Initialize the engine in the project root
engine = RuthenianEngine(base_dir="c:/Users/augus/OneDrive/Documents/Google Antigravity/Projects/Typikon Coded")

# Target date: June 13, 2026
target_date = date(2026, 6, 13)
context = engine.get_liturgical_context(target_date)

print("Dolnytsky Title:", context.get("dolnytsky_title"))
print("Dolnytsky Commemoration:", context.get("dolnytsky_commemoration"))
print("Saints:")
for s in context.get("saints", []):
    print(f"  - ID: {s.get('id')}")
    print(f"    Name: {s.get('name')}")
    print(f"    Rank: {s.get('rank')}")
    print(f"    Rank Code: {s.get('rank_code')}")
