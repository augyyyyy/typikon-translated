import zipfile

docx_path = r"E:\Google Drive\Liturgical Library\Typikon and Service Books\Typikon\Typyk UHKC(укр).docx"

try:
    with zipfile.ZipFile(docx_path) as docx:
        names = docx.namelist()
        print("Files in DOCX:")
        for name in names:
            if "comment" in name or "document" in name or "footnote" in name:
                print(f"  {name}")
except Exception as e:
    print(f"Error reading zip: {e}")
