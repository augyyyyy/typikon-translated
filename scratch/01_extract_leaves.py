import os
import sys
import argparse
from pathlib import Path
import fitz

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def extract_leaves(pdf_path_arg=None):
    if pdf_path_arg:
        pdf_path = Path(pdf_path_arg)
    else:
        pdf_env = os.environ.get("SYNOD_PDF_PATH")
        if pdf_env:
            pdf_path = Path(pdf_env)
        else:
            # Fallback searching mounted drives or standard relative path
            candidates = [
                Path("E:") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon" / "Historical Typikons" / "1891-1896-Chynnosty-i-Rishenia-Lviv-Provincial-Synod.pdf",
                Path("D:") / "Google Drive" / "Liturgical Library" / "3. Modern Service Books and Typikons" / "Typikon" / "Historical Typikons" / "1891-1896-Chynnosty-i-Rishenia-Lviv-Provincial-Synod.pdf",
            ]
            pdf_path = None
            for cand in candidates:
                if cand.exists():
                    pdf_path = cand
                    break

    if not pdf_path or not pdf_path.exists():
        raise FileNotFoundError(f"Source PDF not found at {pdf_path}. Set SYNOD_PDF_PATH or pass via --pdf.")

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    output_dir = project_root / "Source Text" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Opening {pdf_path}...")
    doc = fitz.Document(str(pdf_path))
    print(f"Total pages in doc: {len(doc)}")

    # Extract pages 245 through 261 (1-indexed pages -> 0-indexed indices 244 through 260)
    start_page = 245
    end_page = 261

    for p in range(start_page, end_page + 1):
        idx = p - 1
        page = doc[idx]
        pix = page.get_pixmap(dpi=300)
        out_file = output_dir / f"p{p}.png"
        pix.save(str(out_file))
        print(f"Extracted page {p} (index {idx}) -> {out_file.name} ({out_file.stat().st_size} bytes)")

    doc.close()
    print("Leaf extraction complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract leaf images from Synod PDF.")
    parser.add_argument("--pdf", help="Path to Synod PDF")
    args = parser.parse_args()
    extract_leaves(args.pdf)
