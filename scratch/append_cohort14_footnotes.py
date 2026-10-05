from pathlib import Path

fn_master_path = Path("Typikons/1891 Lviv Synod/Final/Final_footnotes.txt")
fn_draft_path = Path("Typikons/1891 Lviv Synod/Draft/1891_lviv_synod_cohort14_footnotes.txt")

draft_lines = fn_draft_path.read_text(encoding="utf-8").splitlines()
cohort14_notes = [line for line in draft_lines if not line.startswith("#")]
text_to_append = "\n".join(cohort14_notes).strip()

master_content = fn_master_path.read_text(encoding="utf-8")
if not master_content.endswith("\n\n"):
    if master_content.endswith("\n"):
        new_master_content = master_content + "\n" + text_to_append + "\n"
    else:
        new_master_content = master_content + "\n\n" + text_to_append + "\n"
else:
    new_master_content = master_content + text_to_append + "\n"

fn_master_path.write_text(new_master_content, encoding="utf-8")
print(f"Successfully appended Cohort 14 footnotes to {fn_master_path}")
print(f"Total lines in Final_footnotes.txt: {len(new_master_content.splitlines())}")
print(f"Total bytes in Final_footnotes.txt: {len(new_master_content.encode('utf-8'))}")
