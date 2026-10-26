import os
import stat
import shutil
import sys
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HUB_INBOX_ROOT = PROJECT_ROOT.parent / "Typikon Coded" / "Data" / "Inbox"

def on_rm_error(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"Warning: could not remove {path}: {e}")

monuments_map = [
    {
        "mon_dir": "Monument 1 - 1891 Lviv Synod",
        "inbox_dir": "1891_Lviv_Synod",
        "complete_md": "1891_lviv_synod_complete.md",
        "complete_txt": "1891_lviv_synod_complete.txt",
        "footnotes": "Final_footnotes.txt"
    },
    {
        "mon_dir": "Monument 2 - 1899 Dolnytsky Typikon",
        "inbox_dir": "1899_Dolnytsky_Typikon",
        "complete_md": "1899_dolnytsky_typikon_complete.md",
        "complete_txt": "1899_dolnytsky_typikon_complete.txt",
        "footnotes": "Final_footnotes.txt"
    },
    {
        "mon_dir": "Monument 3 - 1901 Mikita Typikon",
        "inbox_dir": "1901_Mikita_Typikon",
        "complete_md": "1901_mikita_typikon_complete.md",
        "complete_txt": "1901_mikita_typikon_complete.txt",
        "footnotes": "Final_footnotes.txt"
    },
    {
        "mon_dir": "Monument 4 - 1852 Doskovsky Typikon",
        "inbox_dir": "1852_Doskovsky_Typikon",
        "complete_md": "1852_doskovsky_typikon_complete.md",
        "complete_txt": "1852_doskovsky_typikon_complete.txt",
        "footnotes": "Final_footnotes.txt"
    }
]

# 1. Clean duplicate 1891_Lviv_Provincial_Synod
dup_dir = HUB_INBOX_ROOT / "1891_Lviv_Provincial_Synod"
if dup_dir.exists():
    print(f"Removing legacy duplicate directory: {dup_dir}")
    shutil.rmtree(dup_dir, onexc=on_rm_error)

# 2. Sync each monument
for item in monuments_map:
    mon_base = PROJECT_ROOT / "Liturgical Monuments" / item["mon_dir"]
    target_inbox = HUB_INBOX_ROOT / item["inbox_dir"]
    target_inbox.mkdir(parents=True, exist_ok=True)
    
    print(f"\n--- Syncing {item['inbox_dir']} ---")
    
    # Copy Final MD deliverables
    final_md = mon_base / "Final MD"
    if final_md.exists():
        for f in final_md.glob("*.md"):
            dst = target_inbox / f.name
            shutil.copy2(str(f), str(dst))
            print(f"  [MD] Copied {f.name}")
            
    # Copy Final txt deliverables and cohorts
    final_dir = mon_base / "Final"
    if final_dir.exists():
        for f in final_dir.glob("*.txt"):
            dst = target_inbox / f.name
            shutil.copy2(str(f), str(dst))
            print(f"  [TXT] Copied {f.name}")

print("\nHub Inbox synchronization complete!")
