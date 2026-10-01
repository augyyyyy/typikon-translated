import os
import sys

doc_path = r"E:\Google Drive\Liturgical Library\Typikon and Service Books\Typikon\Typyk UHKC(укр).doc"

# Method 1: Try using win32com.client
try:
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(doc_path)
    text = doc.Content.Text
    doc.Close()
    word.Quit()
    print("SUCCESS via win32com.client")
    with open("doc_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted {len(text)} characters to doc_text.txt")
    sys.exit(0)
except Exception as e:
    print(f"win32com failed: {e}")

# Method 2: Try using docx2txt (if it's actually a docx renamed, or if we can parse binary doc)
# If it's a true binary .doc file, we might be able to extract plain text strings using basic string extraction
try:
    with open(doc_path, "rb") as f:
        content = f.read()
    # Find all printable strings of length > 4
    import re
    # Simple extraction of text-like chunks (Ukrainian text uses cyrillic, so range is \u0400-\u04FF)
    # Let's write a small string extractor
    words = []
    # Cyrillic characters are in 0400-04FF. In binary DOC, they are typically encoded in windows-1251.
    text_1251 = content.decode('windows-1251', errors='ignore')
    # Filter for Cyrillic / Latin printable words
    matches = re.findall(r'[\u0400-\u04FF\w\s\-\.,:;!\?\(\)\[\]]{5,}', text_1251)
    extracted = "\n".join(matches)
    with open("doc_text_binary.txt", "w", encoding="utf-8") as f:
        f.write(extracted)
    print(f"Binary decode fallback: extracted {len(extracted)} chars to doc_text_binary.txt")
except Exception as e:
    print(f"Binary decode failed: {e}")
