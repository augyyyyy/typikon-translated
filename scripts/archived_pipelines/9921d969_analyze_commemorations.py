import json
import os

almanac_path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\json_db\almanac\annual_almanac_2026.json"

with open(almanac_path, "r", encoding="utf-8") as f:
    data = json.load(f)

unique_comms = set()
for date_str, day_data in data.get("days", {}).items():
    comm = day_data.get("dolnytsky_commemoration")
    if comm and comm != "None":
        unique_comms.add(comm)

# Split commemorations into individual saint parts using regex or simple split
import re
saint_parts = set()
for comm in unique_comms:
    parts = re.split(r'\s+and\s+|\s+&\s+|;', comm, flags=re.IGNORECASE)
    for p in parts:
        p_clean = p.strip().strip('*').strip()
        if p_clean:
            saint_parts.add(p_clean)

# Print a sorted list of unique saint names
print(f"Total unique commemorations: {len(unique_comms)}")
print(f"Total unique saint names: {len(saint_parts)}")
print("\nFirst 100 saint names:")
for name in sorted(saint_parts)[:100]:
    print(f"- {name}")
