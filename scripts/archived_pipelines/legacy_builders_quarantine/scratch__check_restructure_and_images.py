import os
from pathlib import Path

def audit():
    print("=== CHECKING E:\\Google Drive\\Liturgical Library ===")
    base_lib = Path(r"E:\Google Drive\Liturgical Library")
    if not base_lib.exists():
        print("Base library does not exist!")
        return

    # Check subfolders in 2. Historical Liturgical Texts
    hist = base_lib / "2. Historical Liturgical Texts"
    if hist.exists():
        print("\n--- 2. Historical Liturgical Texts Subdirectories ---")
        for root, dirs, files in os.walk(hist):
            # If folder has images, print count
            img_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            pdf_files = [f for f in files if f.lower().endswith('.pdf')]
            if img_files or pdf_files:
                rel = Path(root).relative_to(hist)
                print(f"{rel}: {len(img_files)} images, {len(pdf_files)} PDFs")

    # Check 3. Modern Service Books and Typikons
    modern = base_lib / "3. Modern Service Books and Typikons"
    if modern.exists():
        print("\n--- 3. Modern Service Books and Typikons ---")
        for root, dirs, files in os.walk(modern):
            img_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            pdf_files = [f for f in files if f.lower().endswith('.pdf')]
            if img_files or pdf_files:
                rel = Path(root).relative_to(modern)
                print(f"{rel}: {len(img_files)} images, {len(pdf_files)} PDFs")

    # Check Translation project Liturgical Monuments
    proj_monuments = Path("Liturgical Monuments")
    if proj_monuments.exists():
        print("\n--- Translation Project: Liturgical Monuments ---")
        for m in sorted(proj_monuments.iterdir()):
            if m.is_dir():
                img_dir = m / "Source Text" / "images"
                count = len(list(img_dir.glob("*.png"))) if img_dir.exists() else 0
                source_txts = len(list((m / "Source Text").glob("*.txt"))) if (m / "Source Text").exists() else 0
                drafts = len(list((m / "Draft").glob("*.*"))) if (m / "Draft").exists() else 0
                finals = len(list((m / "Final").glob("*.*"))) if (m / "Final").exists() else 0
                print(f"{m.name}:")
                print(f"   images: {count}")
                print(f"   source txts: {source_txts}")
                print(f"   drafts: {drafts}")
                print(f"   finals: {finals}")

if __name__ == '__main__':
    audit()
