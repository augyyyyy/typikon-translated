from pathlib import Path

txt_lines = Path('Final/Final_Dolnytsky_part3_menaion.txt').read_text(encoding='utf-8').splitlines()
md_lines = Path('Final MD/Final_Dolnytsky_part3_menaion.md').read_text(encoding='utf-8').splitlines()

def show_context(keyword, num_lines=5):
    print(f"\n==================== KEYWORD: '{keyword}' ====================")
    print("--- TXT ---")
    for i, l in enumerate(txt_lines):
        if keyword.lower() in l.lower():
            for j in range(max(0, i-1), min(len(txt_lines), i+num_lines)):
                print(f"TXT L{j+1}: {txt_lines[j]}")
            break
    print("--- MD ---")
    for i, l in enumerate(md_lines):
        if keyword.lower() in l.lower():
            for j in range(max(0, i-1), min(len(md_lines), i+num_lines)):
                print(f"MD L{j+1}: {md_lines[j]}")
            break

for kw in [
    "Saturday before the Exaltation",
    "Forefeast of the Nativity of the Most Holy Theotokos",
    "Saturday in the Forefeast",
    "Sunday before the Exaltation",
    "Afterfeast of the Nativity",
    "Apodosis of the Nativity",
    "Memory of the Renovation",
    "between the basil and the Cross",
    "dalmatic with a horarion",
    "Transfer of the Precious Cross",
    "Thou Who Wast lifted up",
    "Falling Asleep of the Holy Apostle John",
    "Sunday of the Holy Fathers",
    "St. Great Martyr Demetrius",
    "Saint Hieromartyr Josaphat",
    "Synaxis of St. Archangel Michael",
    "The fast of this Forty Days the Lviv Synod"
]:
    show_context(kw, num_lines=3)
