#!/usr/bin/env python3
"""
Extract Docx Corpus & Footnote Apparatus
========================================
Extracts all paragraphs, styling runs (bold, italic, headings),
and native Word footnotes from the original .docx translation manuscript.
Outputs structured JSON to scratch/reports/docx_corpus.json.
"""

from pathlib import Path
import os
import sys
import json
import zipfile
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def get_docx_path() -> Path:
    env_path = os.environ.get("TYPIKON_DOCX_PATH")
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p

    home_desktop = Path.home() / "OneDrive" / "Desktop" / "Here is the revised translation of the Typikon.docx"
    if home_desktop.exists():
        return home_desktop

    regular_desktop = Path.home() / "Desktop" / "Here is the revised translation of the Typikon.docx"
    if regular_desktop.exists():
        return regular_desktop

    raise FileNotFoundError("Could not locate 'Here is the revised translation of the Typikon.docx'")

def extract_footnotes(zip_ref: zipfile.ZipFile) -> dict:
    footnotes = {}
    if "word/footnotes.xml" not in zip_ref.namelist():
        return footnotes

    xml_content = zip_ref.read("word/footnotes.xml")
    tree = ET.fromstring(xml_content)

    for fn in tree.findall(f"{{{W_NS}}}footnote"):
        fn_id = fn.attrib.get(f"{{{W_NS}}}id")
        if not fn_id or int(fn_id) < 1:
            continue

        paragraphs = []
        for p in fn.findall(f"{{{W_NS}}}p"):
            p_text = []
            for t in p.iter(f"{{{W_NS}}}t"):
                if t.text:
                    p_text.append(t.text)
            if p_text:
                paragraphs.append("".join(p_text))

        fn_text = " ".join(paragraphs).strip()
        footnotes[int(fn_id)] = fn_text

    return footnotes

def extract_document(zip_ref: zipfile.ZipFile) -> list:
    if "word/document.xml" not in zip_ref.namelist():
        return []

    xml_content = zip_ref.read("word/document.xml")
    tree = ET.fromstring(xml_content)

    paragraphs = []
    body = tree.find(f"{{{W_NS}}}body")
    if body is None:
        return []

    p_idx = 0
    for p in body.findall(f"{{{W_NS}}}p"):
        p_idx += 1
        p_style = None
        pPr = p.find(f"{{{W_NS}}}pPr")
        if pPr is not None:
            pStyle_el = pPr.find(f"{{{W_NS}}}pStyle")
            if pStyle_el is not None:
                p_style = pStyle_el.attrib.get(f"{{{W_NS}}}val")

        runs = []
        fn_refs = []
        full_text_parts = []

        for r in p.findall(f"{{{W_NS}}}r"):
            r_bold = False
            r_italic = False
            rPr = r.find(f"{{{W_NS}}}rPr")
            if rPr is not None:
                if rPr.find(f"{{{W_NS}}}b") is not None:
                    r_bold = True
                if rPr.find(f"{{{W_NS}}}i") is not None:
                    r_italic = True

            for fn_ref in r.findall(f"{{{W_NS}}}footnoteReference"):
                f_id = fn_ref.attrib.get(f"{{{W_NS}}}id")
                if f_id:
                    fn_refs.append(int(f_id))

            r_text_parts = []
            for t in r.findall(f"{{{W_NS}}}t"):
                if t.text:
                    r_text_parts.append(t.text)

            r_text = "".join(r_text_parts)
            if r_text:
                full_text_parts.append(r_text)
                runs.append({
                    "text": r_text,
                    "bold": r_bold,
                    "italic": r_italic
                })

        p_text = "".join(full_text_parts).strip()
        if p_text or fn_refs:
            paragraphs.append({
                "index": p_idx,
                "style": p_style,
                "text": p_text,
                "footnote_refs": fn_refs,
                "runs": runs
            })

    return paragraphs

def main():
    try:
        docx_path = get_docx_path()
        print(f"Found source DOCX: {docx_path}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    with zipfile.ZipFile(docx_path, "r") as z:
        print("Extracting native footnotes...")
        footnotes = extract_footnotes(z)
        print(f"Extracted {len(footnotes)} native footnotes.")

        print("Extracting paragraphs & formatting runs...")
        paragraphs = extract_document(z)
        print(f"Extracted {len(paragraphs)} paragraphs.")

    # Save to project scratch reports
    proj_root = Path(__file__).resolve().parent.parent
    # Check if inside brain directory or project directory
    if "brain" in str(proj_root):
        output_dir = Path(r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Translation\scratch\reports")
    else:
        output_dir = proj_root / "scratch" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "docx_corpus.json"

    data = {
        "source_file": docx_path.name,
        "total_paragraphs": len(paragraphs),
        "total_footnotes": len(footnotes),
        "footnotes": footnotes,
        "paragraphs": paragraphs
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Extraction complete! Saved to {out_file}")

if __name__ == "__main__":
    main()
