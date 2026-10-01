import os
import shutil
import subprocess

scratch_dir = r"C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch"
src_doc = r"E:\Google Drive\Liturgical Library\Typikon and Service Books\Typikon\Typyk UHKC(укр).doc"
local_doc = os.path.join(scratch_dir, "Typyk_UHKC_ukr.doc")
local_txt = os.path.join(scratch_dir, "Typyk_UHKC_ukr.txt")

# 1. Copy file locally
print("Copying document file locally to scratch...")
shutil.copy2(src_doc, local_doc)

# 2. Write powershell script with SaveAs2 and UTF-8 encoding (65001)
# Parameters for SaveAs2:
# SaveAs2(FileName, FileFormat, LockComments, Password, AddToRecentFiles, WritePassword, 
#         ReadOnlyRecommended, EmbedTrueTypeFonts, SaveNativePictureFormat, SaveFormsData, 
#         SaveAsAOCELetter, Encoding, InsertLineBreaks, AllowSubstitutions, LineEnding, AddBiDiMarks)
# FileFormat = 7 (wdFormatEncodedText), Encoding = 65001 (UTF-8)
ps_code = f"""$word = New-Object -ComObject Word.Application
$word.DisplayAlerts = 0
$doc = $word.Documents.Open('{local_doc}', $false, $true)
# Call SaveAs2 with format 7 (encoded text) and code page 65001 (UTF-8)
$doc.SaveAs2('{local_txt}', 7, $false, "", $false, "", $false, $false, $false, $false, $false, 65001)
$doc.Close()
$word.Quit()
"""

ps_script_path = os.path.join(scratch_dir, "convert_local.ps1")
with open(ps_script_path, 'w', encoding='utf-8-sig') as f:
    f.write(ps_code)
print("Powershell conversion script generated with UTF-8 encoding.")

# 3. Execute PowerShell
print("Running PowerShell conversion...")
res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_script_path], capture_output=True, text=True)

print("PowerShell exit code:", res.returncode)
if res.stdout:
    print("STDOUT:", res.stdout.encode('ascii', 'backslashreplace').decode('ascii'))
if res.stderr:
    print("STDERR:", res.stderr.encode('ascii', 'backslashreplace').decode('ascii'))

# 4. Clean up local doc
if os.path.exists(local_doc):
    os.remove(local_doc)
    print("Cleaned up local .doc file.")

# 5. Verify output txt exists
if os.path.exists(local_txt):
    size = os.path.getsize(local_txt)
    print(f"SUCCESS: Converted file size: {size} bytes")
else:
    print("FAILURE: Converted text file was not created.")
