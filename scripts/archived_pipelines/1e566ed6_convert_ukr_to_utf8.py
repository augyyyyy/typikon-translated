encodings = ['windows-1251', 'utf-16', 'utf-16-le', 'utf-16-be', 'utf-8', 'cp1252']
path = "Typyk_UHKC_ukr.txt"

text = None
for enc in encodings:
    try:
        with open(path, 'r', encoding=enc) as f:
            content = f.read()
        # Verify it has cyrillic letters
        if any(c in content for c in 'аеиоу'):
            text = content
            print(f"SUCCESS: Read file with encoding: {enc}")
            break
    except Exception as e:
        print(f"Failed with {enc}: {e}")

if text is None:
    # fallback with ignore
    with open(path, 'r', encoding='windows-1251', errors='ignore') as f:
        text = f.read()
    print("Fallback: Read with windows-1251 (errors ignored)")

# Write as standard UTF-8
with open("Typyk_UHKC_ukr_utf8.txt", 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved converted file to Typyk_UHKC_ukr_utf8.txt")
