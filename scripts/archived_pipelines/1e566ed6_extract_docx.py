import os
import zipfile
import xml.etree.ElementTree as ET

docx_path = r"E:\Google Drive\Liturgical Library\Typikon and Service Books\Typikon\Typyk UHKC(укр).docx"
output_path = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\doc_text_utf8.txt"

try:
    if not os.path.exists(docx_path):
        print("File not found.")
        sys.exit(1)

    print("File exists. Attempting zip extract...")
    with zipfile.ZipFile(docx_path) as docx:
        xml_content = docx.read('word/document.xml')
        root = ET.fromstring(xml_content)
        
        texts = []
        for paragraph in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            p_text = []
            for text in paragraph.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                if text.text:
                    p_text.append(text.text)
            texts.append("".join(p_text))
            
        full_text = "\n".join(texts)
        with open(output_path, "w", encoding="utf-8") as f_out:
            f_out.write(full_text)
            
        print(f"SUCCESS: Extracted {len(texts)} paragraphs ({len(full_text)} characters)")

except Exception as e:
    # Safely print exception representation
    print(f"Failed to extract DOCX: {repr(e)}")
