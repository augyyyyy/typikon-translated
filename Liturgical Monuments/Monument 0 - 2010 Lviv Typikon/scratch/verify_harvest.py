import os
import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).resolve().parent.parent.parent.parent
manifest_path = Path(__file__).resolve().parent / 'ingested_manifest.json'
registry_path = project_root / 'ARTIFACT_REGISTRY.md'

print("=" * 80)
print("DETERMINISTIC VERIFICATION & FORENSIC AUDIT OF HARVEST")
print("=" * 80)

# 1. Verify Manifest
if not manifest_path.exists():
    print("FATAL: Manifest path does not exist!")
    sys.exit(1)

with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

# 2. Verify Registry File
if not registry_path.exists():
    print("FATAL: ARTIFACT_REGISTRY.md does not exist!")
    sys.exit(1)

with open(registry_path, 'r', encoding='utf-8') as f:
    registry_text = f.read()

total_checked = 0
total_verified_bytes = 0
errors = []

tier_stats = {}

for tier, items in manifest.items():
    tier_count = 0
    tier_bytes = 0
    
    for it in items:
        target_path = project_root / it['target_rel_path']
        
        # Check existence
        if not target_path.exists():
            errors.append(f"MISSING: {target_path}")
            continue
            
        # Check size
        actual_size = target_path.stat().st_size
        if actual_size != it['size']:
            errors.append(f"SIZE MISMATCH: {target_path} (expected {it['size']}, got {actual_size})")
            continue
            
        # Check entry in ARTIFACT_REGISTRY.md
        if it['target_name'] not in registry_text:
            errors.append(f"REGISTRY MISSING ITEM: {it['target_name']}")
            continue

        if it['cid'] not in registry_text:
            errors.append(f"REGISTRY MISSING CID: {it['cid']}")
            continue

        total_checked += 1
        total_verified_bytes += actual_size
        tier_count += 1
        tier_bytes += actual_size

    tier_stats[tier] = (tier_count, tier_bytes)

print(f"\nRegistry File Size: {registry_path.stat().st_size:,} bytes, {len(registry_text.splitlines())} lines")
print(f"Total Verified Items: {total_checked}")
print(f"Total Verified Bytes: {total_verified_bytes / (1024*1024):.2f} MB ({total_verified_bytes:,} bytes)")
print("\nBreakdown by Tier:")
for tier, (cnt, b) in tier_stats.items():
    print(f"  {tier.upper():<6}: {cnt:>3} files, {b/(1024*1024):>6.2f} MB ({b:>12,} bytes)")

if errors:
    print(f"\nVERIFICATION FAILED WITH {len(errors)} ERRORS:")
    for err in errors[:10]:
        print(f"  ❌ {err}")
    sys.exit(1)
else:
    print("\n✅ DETERMINISTIC PROOF PASSED: 100% of files exist, byte sizes match, and registry links are valid.")
print("=" * 80)
