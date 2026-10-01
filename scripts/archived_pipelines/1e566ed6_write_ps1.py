ps_code = r"""$word = New-Object -ComObject Word.Application
$word.DisplayAlerts = 0
$doc = $word.Documents.Open('E:\Google Drive\Liturgical Library\Typikon and Service Books\Typikon\Typyk UHKC(укр).doc', $false, $true)
$doc.SaveAs('C:\Users\augus\.gemini\antigravity\brain\1e566ed6-510f-4f9f-9987-1ea377eeb714\scratch\Typyk_UHKC_ukr.txt', 2)
$doc.Close()
$word.Quit()
"""

with open('C:\\Users\\augus\\.gemini\\antigravity\\brain\\1e566ed6-510f-4f9f-9987-1ea377eeb714\\scratch\\convert.ps1', 'w', encoding='utf-8-sig') as f:
    f.write(ps_code)

print("Robust Powershell script written with raw string literals.")
