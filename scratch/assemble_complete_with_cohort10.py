import sys
from pathlib import Path
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    root = Path(__file__).resolve().parent.parent
    final_md_dir = root / "Typikons" / "1891 Lviv Synod" / "Final MD"
    final_txt_dir = root / "Typikons" / "1891 Lviv Synod" / "Final"
    source_dir = root / "Typikons" / "1891 Lviv Synod" / "Source Text"
    
    inbox_synod_dir = Path(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Inbox\1891_Lviv_Provincial_Synod")
    inbox_root = Path(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Inbox")

    c10_md_file = final_md_dir / "1891_synod_cohort10.md"
    c10_txt_file = final_txt_dir / "1891_synod_cohort10.txt"
    c10_src_file = source_dir / "1891_lviv_synod_cohort10_source.txt"
    complete_md_file = final_md_dir / "1891_lviv_synod_complete.md"
    complete_txt_file = final_txt_dir / "1891_lviv_synod_complete.txt"
    master_fn_file = final_txt_dir / "Final_footnotes.txt"

    c10_md_content = c10_md_file.read_text(encoding="utf-8").strip()
    c10_txt_content = c10_txt_file.read_text(encoding="utf-8").strip()

    # 1. Update 1891_lviv_synod_complete.md
    complete_md_text = complete_md_file.read_text(encoding="utf-8")
    old_assembled = "> **Assembled Cohorts**: ['1891_synod_cohort3.md', '1891_synod_cohort4.md', '1891_synod_cohort5.md', '1891_synod_cohort6.md', '1891_synod_cohort7.md', '1891_synod_cohort8.md', '1891_synod_cohort9.md', '1891_synod_cohort1.md', '1891_synod_cohort2.md']"
    new_assembled = "> **Assembled Cohorts**: ['1891_synod_cohort3.md', '1891_synod_cohort4.md', '1891_synod_cohort5.md', '1891_synod_cohort6.md', '1891_synod_cohort7.md', '1891_synod_cohort8.md', '1891_synod_cohort9.md', '1891_synod_cohort10.md', '1891_synod_cohort1.md', '1891_synod_cohort2.md']"

    c10_md_block = f"\n\n<!-- START COHORT 1891_synod_cohort10 -->\n\n{c10_md_content}\n\n<!-- END COHORT 1891_synod_cohort10 -->\n\n---\n"
    
    target_boundary = "<!-- END COHORT 1891_synod_cohort9 -->\n\n---\n\n<!-- START COHORT 1891_synod_cohort1 -->"
    replacement_boundary = f"<!-- END COHORT 1891_synod_cohort9 -->\n\n---{c10_md_block}\n<!-- START COHORT 1891_synod_cohort1 -->"

    if target_boundary in complete_md_text:
        updated_complete_md = complete_md_text.replace(old_assembled, new_assembled).replace(target_boundary, replacement_boundary)
        complete_md_file.write_text(updated_complete_md, encoding="utf-8")
        print(f"Updated {complete_md_file} (New size: {complete_md_file.stat().st_size} bytes)")
    else:
        print("WARNING: target_boundary not found in complete_md_text")

    # 2. Update 1891_lviv_synod_complete.txt
    complete_txt_text = complete_txt_file.read_text(encoding="utf-8")
    c10_txt_block = f"\n\n<!-- START COHORT 1891_synod_cohort10 -->\n\n{c10_md_content}\n\n<!-- END COHORT 1891_synod_cohort10 -->\n\n---\n"
    if target_boundary in complete_txt_text:
        updated_complete_txt = complete_txt_text.replace(old_assembled, new_assembled).replace(target_boundary, replacement_boundary)
        complete_txt_file.write_text(updated_complete_txt, encoding="utf-8")
        print(f"Updated {complete_txt_file} (New size: {complete_txt_file.stat().st_size} bytes)")
    else:
        print("WARNING: target_boundary not found in complete_txt_text")

    # 3. Copy files to inbox_synod_dir
    print(f"Copying deliverables to {inbox_synod_dir}...")
    shutil.copy2(c10_md_file, inbox_synod_dir / "1891_synod_cohort10.md")
    shutil.copy2(c10_txt_file, inbox_synod_dir / "1891_synod_cohort10.txt")
    shutil.copy2(c10_src_file, inbox_synod_dir / "1891_lviv_synod_cohort10_source.txt")
    shutil.copy2(master_fn_file, inbox_synod_dir / "Final_footnotes.txt")
    shutil.copy2(complete_md_file, inbox_synod_dir / "1891_lviv_synod_complete.md")
    shutil.copy2(complete_txt_file, inbox_synod_dir / "1891_lviv_synod_complete.txt")

    # 4. Copy to inbox_root
    shutil.copy2(c10_md_file, inbox_root / "1891_synod_cohort10.md")
    shutil.copy2(c10_txt_file, inbox_root / "1891_synod_cohort10.txt")
    shutil.copy2(c10_src_file, inbox_root / "1891_lviv_synod_cohort10_source.txt")

    print("Deliverables successfully copied to Inbox locations.")

if __name__ == "__main__":
    main()
