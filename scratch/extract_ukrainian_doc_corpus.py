#!/usr/bin/env python3
"""
Extract Ukrainian Master Corpus from Converted Docx
===================================================
Extracts all 785 native footnotes and all body paragraphs from
scratch/Typyk_UHKC_ukr.docx into structured JSON reports.
"""

from pathlib import Path
import os
import sys
import json
import zipfile
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def get_project_root() -> Path:
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "scratch").exists():
            return parent
    return Path(__file__).resolve().parent.parent

def main():
    root = get_project_root()
    docx_file = root / "scratch" / "Typyk_UHKC_ukr.docx"
    if not docx_file.exists():
        print(f"Error: {docx_file} not found.")
        sys.exit(1)

    reports_dir = root / "scratch" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(docx_file, "r") as z:
        print("Extracting Ukrainian native footnotes...")
        fn_xml = z.read("word/footnotes.xml")
        tree = ET.fromstring(fn_xml)
        footnotes = {}
        for fn in tree.findall(f"{{{W_NS}}}footnote"):
            fid = fn.attrib.get(f"{{{W_NS}}}id")
            if fid and int(fid) >= 1:
                texts = [t.text for t in fn.iter(f"{{{W_NS}}}t") if t.text]
                footnotes[int(fid)] = "".join(texts).strip()

        print(f"Extracted {len(footnotes)} Ukrainian native footnotes.")

        print("Extracting Ukrainian body paragraphs...")
        doc_xml = z.read("word/document.xml")
        doc_tree = ET.fromstring(doc_xml)
        body = doc_tree.find(f"{{{W_NS}}}body")
        paragraphs = []
        p_idx = 0
        for p in body.findall(f"{{{W_NS}}}p"):
            p_idx += 1
            pPr = p.find(f"{{{W_NS}}}pPr")
            style = None
            if pPr is not None:
                pStyle = pPr.find(f"{{{W_NS}}}pStyle")
                if pStyle is not None:
                    style = pStyle.attrib.get(f"{{{W_NS}}}val")

            texts = []
            fn_refs = []
            for r in p.findall(f"{{{W_NS}}}r"):
                for fn_ref in r.findall(f"{{{W_NS}}}footnoteReference"):
                    fid = fn_ref.attrib.get(f"{{{W_NS}}}id")
                    if fid and int(fid) >= 1:
                        fn_refs.append(int(fid))
                for t in r.findall(f"{{{W_NS}}}t"):
                    if t.text:
                        texts.append(t.text)

            p_text = "".join(texts).strip()
            if p_text or fn_refs:
                paragraphs.append({
                    "index": p_idx,
                    "style": style,
                    "text": p_text,
                    "footnote_refs": fn_refs
                })

        print(f"Extracted {len(paragraphs)} Ukrainian paragraphs.")

    # Save to JSON
    with open(reports_dir / "ukrainian_footnotes_master.json", "w", encoding="utf-8") as f:
        json.dump(footnotes, f, ensure_ascii=False, indent=2)

    with open(reports_dir / "ukrainian_paragraphs_master.json", "w", encoding="utf-8") as f:
        json.dump(paragraphs, f, ensure_ascii=False, indent=2)

    print(f"Saved master reports to {reports_dir.relative_to(root)}")

if __name__ == "__main__":
    main()
