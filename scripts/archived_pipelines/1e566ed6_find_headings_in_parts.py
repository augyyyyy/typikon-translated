import os
import re
import sys

def search_text(path, query):
    if not os.path.exists(path):
        return
    print(f"\nSearching in {os.path.basename(path)} for: {query}")
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if query.lower() in line.lower():
                print(f"  Line {i+1:4d}: {line.strip()[:100]}")

def main():
    typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
    part3 = os.path.join(typikon_dir, "Final_Dolnytsky_part3_menaion.md")
    part4 = os.path.join(typikon_dir, "Final_Dolnytsky_part4_triodion.md")
    
    # Let's search for the headings we need
    search_text(part3, "Saturday after Theophany")
    search_text(part3, "Sunday after Theophany")
    search_text(part3, "Afterfeast of the Meeting")
    search_text(part3, "Procession of the Wood")
    
    search_text(part4, "Lenten Triodion")
    search_text(part4, "Publican and Pharisee")
    search_text(part4, "Prodigal Son")
    search_text(part4, "Meatfare, or Soul Saturday")
    search_text(part4, "Meatfare Sunday")
    search_text(part4, "Cheesefare Week")
    search_text(part4, "Cheesefare Sunday")
    search_text(part4, "Beginning of Great Lent")
    search_text(part4, "Vespers on Wednesday and Friday with Presanctified")
    search_text(part4, "First Saturday of Great Lent")
    search_text(part4, "First Sunday of Great Lent")
    search_text(part4, "Second Week of Great Lent")
    search_text(part4, "Saturday of the Second Week of Great Lent")
    search_text(part4, "Second Sunday of Great Lent")
    search_text(part4, "Third Week of Great Lent")
    search_text(part4, "Fourth Saturday of Great Lent")
    search_text(part4, "Fourth Sunday of Great Lent")
    search_text(part4, "Fifth Week of Great Lent")
    search_text(part4, "Fifth Sunday of Great Lent")
    search_text(part4, "Sixth Week of Great Lent")
    
    search_text(part4, "Flower Triodion")
    search_text(part4, "Lazarus Saturday")
    search_text(part4, "Flower Sunday")
    search_text(part4, "Palm Sunday")
    search_text(part4, "Great Monday, Tuesday")
    search_text(part4, "Great Thursday")
    search_text(part4, "Great Friday")
    search_text(part4, "Matins of Great Saturday")
    search_text(part4, "Beginning of Holy Pentecost")
    search_text(part4, "Resurrection Matins")
    search_text(part4, "On the Day of Resurrection in the Evening")
    search_text(part4, "General Rubric for All Days of Bright Week")
    search_text(part4, "Sunday of the Apostle Thomas")
    search_text(part4, "Sunday of the Myrrh-Bearing Women")
    search_text(part4, "Sunday of the Paralytic")
    search_text(part4, "Mid-Pentecost")
    search_text(part4, "Sunday of the Samaritan Woman")
    search_text(part4, "Sunday of the Man Born Blind")
    search_text(part4, "Ascension of the Lord")
    search_text(part4, "First Nicaean Council")
    search_text(part4, "Sunday of Pentecost")
    search_text(part4, "Monday of the Holy Spirit")
    search_text(part4, "Sunday of All Saints")
    search_text(part4, "Beginning of the Fast of the Saints")
    search_text(part4, "Feast of the Most Holy Eucharist")
    search_text(part4, "Feast of the Co-suffering")

if __name__ == "__main__":
    main()
