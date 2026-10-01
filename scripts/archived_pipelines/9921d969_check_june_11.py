import sys
import os
from datetime import date
sys.path.insert(0, "c:/Users/augus/OneDrive/Documents/Google Antigravity/Projects/Typikon Coded")
from ruthenian_engine import RuthenianEngine

engine = RuthenianEngine(base_dir="c:/Users/augus/OneDrive/Documents/Google Antigravity/Projects/Typikon Coded")
target_date = date(2026, 6, 11)
context = engine.get_liturgical_context(target_date)

print("Before resolve_rubrics:")
print("Saints:", [s.get("name") for s in context.get("saints", [])])
print("is_afterfeast:", context.get("is_afterfeast"))
print("period (before):", context.get("period"))
print("feast_level:", context.get("feast_level"))

rubrics = engine.resolve_rubrics(context)

print("\nAfter resolve_rubrics:")
print("Saints:", [s.get("name") for s in context.get("saints", [])])
print("period (after):", context.get("period"))
print("Trace:", rubrics.get("_trace")[-5:])
