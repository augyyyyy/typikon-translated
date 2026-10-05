import re
import os

appendix_path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\Final\Final_Dolnytsky_appendix.txt"
oc_1996_path = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\English OC 1996\Ordo_Celebrationis_1996_CLEAN.txt"

def extract_points(filepath):
    points = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # Match "1. Text" or "145. Text"
            match = re.match(r'^(\d+)\.\s+(.*)', line.strip())
            if match:
                num = int(match.group(1))
                text = match.group(2)
                # Just take the first sentence or first 50 chars for comparison
                points[num] = text[:75] + "..."
    return points

dolnytsky_points = extract_points(appendix_path)
oc_1996_points = extract_points(oc_1996_path)

missing_in_doln = set(oc_1996_points.keys()) - set(dolnytsky_points.keys())
missing_in_oc = set(dolnytsky_points.keys()) - set(oc_1996_points.keys())

print("=== STRUCTURAL ALIGNMENT ===")
print(f"Total points in Dolnytsky: {len(dolnytsky_points)}")
print(f"Total points in OC 1996: {len(oc_1996_points)}")

if missing_in_doln:
    print(f"Points in OC 1996 missing in Dolnytsky: {sorted(list(missing_in_doln))}")
if missing_in_oc:
    print(f"Points in Dolnytsky missing in OC 1996: {sorted(list(missing_in_oc))}")

print("\n=== SAMPLE TRANSLATION COMPARISON ===")
for p in [1, 10, 50, 100, 200]:
    if p in dolnytsky_points and p in oc_1996_points:
        print(f"Point {p}:")
        print(f"  Dolnytsky : {dolnytsky_points[p]}")
        print(f"  OC 1996   : {oc_1996_points[p]}")

print("\n=== TERMINOLOGY AUDIT ===")
with open(oc_1996_path, 'r', encoding='utf-8') as f:
    oc_text = f.read().lower()

terms = {
    "Censer vs Thurible": ("censer", "thurible"),
    "Holy Table vs Altar": ("holy table", "altar"),
    "Epitrachelion vs Stole": ("epitrachelion", "stole"),
    "Antimension vs Iliton": ("antimension", "iliton"),
    "Proskomedia vs Prothesis": ("proskomedia", "prothesis"),
    "Matins vs Orthros": ("matins", "orthros")
}

for desc, (term1, term2) in terms.items():
    c1 = oc_text.count(term1)
    c2 = oc_text.count(term2)
    print(f"{desc}: OC 1996 uses '{term1}' {c1} times, and '{term2}' {c2} times.")
