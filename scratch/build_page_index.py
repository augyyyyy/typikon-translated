import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Concordance dictionary mapping each page number / page range to its target file and heading anchor slug
# Based on the text analysis of Dolnytsky Typikon:
PAGE_CONCORDANCE = {
    # Part 1: Structure of Services
    "p21": {
        "target_file": "Final_Dolnytsky_part1_structure.md",
        "heading": "Order of Great Vespers without Vigil",
        "slug": "order-of-great-vespers-without-vigil"
    },
    # Part 2: General Rubrics
    "p26-27": {
        "target_file": "Final_Dolnytsky_part2_general_rubrics.md",
        "heading": "Order of Great Compline",
        "slug": "order-of-great-compline"
    },
    "p29-30": {
        "target_file": "Final_Dolnytsky_part2_general_rubrics.md",
        "heading": "Refrains to the Odes of the Canon",
        "slug": "refrains-to-the-odes-of-the-canon"
    },
    "p47-54": {
        "target_file": "Final_Dolnytsky_part2_general_rubrics.md",
        "heading": "General Rubric for a Saint Without Polyeleos on Sunday",
        "slug": "general-rubric-for-a-saint-without-polyeleos-on-sunday"
    },
    "p79": {
        "target_file": "Final_Dolnytsky_part2_general_rubrics.md",
        "heading": "Forefeast with a Saint Without Polyeleos on Weekdays and on Saturday",
        "slug": "forefeast-with-a-saint-without-polyeleos-on-weekdays-and-on-saturday"
    },
    "p104-105": {
        "target_file": "Final_Dolnytsky_part2_general_rubrics.md",
        "heading": "General Rubric for a Temple Saint in the Afterfeast",
        "slug": "general-rubric-for-a-temple-saint-in-the-afterfeast"
    },
    "p104": {
        "target_file": "Final_Dolnytsky_part2_general_rubrics.md",
        "heading": "General Rubric for a Saint with Vigil in the Afterfeast",
        "slug": "general-rubric-for-a-saint-with-vigil-in-the-afterfeast"
    },
    # Part 3: Menaion Specific Rubrics
    "p110-111": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "13 September – Forefeast of the Exaltation",
        "slug": "13-september--forefeast-of-the-exaltation"
    },
    "p111": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "13 September – Memory of the Renovation of the Temple of the Resurrection",
        "slug": "13-september--memory-of-the-renovation-of-the-temple-of-the-resurrection"
    },
    "p112": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "13 September – At the Liturgy",
        "slug": "at-the-liturgy"
    },
    "p113-114": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "13 September – Sunday Before the Exaltation",
        "slug": "13-september--sunday-before-the-exaltation"
    },
    "p121-122": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "14 September – Exaltation of the Precious and Life-Giving Cross",
        "slug": "14-september--exaltation-of-the-precious-and-life-giving-cross"
    },
    "p122-123": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "14 September – Bringing Out of the Precious Cross",
        "slug": "14-september--bringing-out-of-the-precious-cross"
    },
    "p124-127": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "14 September – Veneration of the Precious Cross",
        "slug": "14-september--veneration-of-the-precious-cross"
    },
    "p129": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "26 September – Falling Asleep of the Holy Apostle and Evangelist John the Theologian",
        "slug": "26-september--falling-asleep-of-the-holy-apostle-and-evangelist-john-the-theologian"
    },
    "p135": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "8 November – Synaxis of the Archangel Michael and the Other Bodiless Powers",
        "slug": "8-november--synaxis-of-the-archangel-michael-and-the-other-bodiless-powers"
    },
    "p136": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "12 November – Holy Hieromartyr Josaphat",
        "slug": "12-november--holy-hieromartyr-josaphat"
    },
    "p144": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "Sunday of the Holy Ancestors (Forefathers)",
        "slug": "sunday-of-the-holy-ancestors-forefathers"
    },
    "p169-170": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "24 December – Eve of the Nativity of Christ",
        "slug": "24-december--eve-of-the-nativity-of-christ"
    },
    "p169-171": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "24 December – Royal Hours and Vespers of the Eve of Nativity",
        "slug": "24-december--royal-hours-and-vespers-of-the-eve-of-nativity"
    },
    "p175": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "Sunday After the Nativity of Christ",
        "slug": "sunday-after-the-nativity-of-christ"
    },
    "p201": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "7 January – Synaxis of the Holy Glorious Prophet, Forerunner and Baptist John",
        "slug": "7-january--synaxis-of-the-holy-glorious-prophet-forerunner-and-baptist-john"
    },
    "p204": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "14 January – Apodosis of the Feast of Theophany",
        "slug": "14-january--apodosis-of-the-feast-of-theophany"
    },
    "p212": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "2 February – Meeting of our Lord Jesus Christ",
        "slug": "2-february--meeting-of-our-lord-jesus-christ"
    },
    "p216-217": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "2 February – The Meeting on Weekdays and Saturday",
        "slug": "2-february--the-meeting-on-weekdays-and-saturday"
    },
    "p218-219": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "2 February – The Meeting on Sunday",
        "slug": "2-february--the-meeting-on-sunday"
    },
    "p220": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "2 February – The Meeting on Cheesefare Sunday",
        "slug": "2-february--the-meeting-on-cheesefare-sunday"
    },
    "p229": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "9 February – Apodosis of the Meeting",
        "slug": "9-february--apodosis-of-the-meeting"
    },
    "p229-230": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "9 February – Apodosis of the Meeting in Cheesefare Week",
        "slug": "9-february--apodosis-of-the-meeting-in-cheesefare-week"
    },
    "p232": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "24 February – First and Second Finding of the Precious Head of John the Baptist",
        "slug": "24-february--first-and-second-finding-of-the-precious-head-of-john-the-baptist"
    },
    "p233": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "24 February – The Finding on Weekdays of Great Lent",
        "slug": "24-february--the-finding-on-weekdays-of-great-lent"
    },
    "p234": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "24 February – The Finding on Saturday of Great Lent",
        "slug": "24-february--the-finding-on-saturday-of-great-lent"
    },
    "p235": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "24 February – The Finding on Sunday of Great Lent",
        "slug": "24-february--the-finding-on-sunday-of-great-lent"
    },
    "p235-236": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "24 February – The Finding in the 2nd, 3rd, and 4th Weeks of Great Lent",
        "slug": "24-february--the-finding-in-the-2nd-3rd-and-4th-weeks-of-great-lent"
    },
    "p254": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "9. Annunciation on Great Thursday",
        "slug": "9-annunciation-on-great-thursday"
    },
    "p293": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "8 May – Holy Apostle and Evangelist John the Theologian",
        "slug": "8-may--holy-apostle-and-evangelist-john-the-theologian"
    },
    "p295": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "8 May – John the Theologian with the Ascension",
        "slug": "8-may--john-the-theologian-with-the-ascension"
    },
    "p295-296": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "8 May – John the Theologian on the Sunday of the Fathers",
        "slug": "8-may--john-the-theologian-on-the-sunday-of-the-fathers"
    },
    "p296": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "8 May – Rubric for the Divine Liturgy",
        "slug": "8-may--rubric-for-the-divine-liturgy"
    },
    "p303": {
        "target_file": "Final_Dolnytsky_part3_menaion.md",
        "heading": "2 July – Deposition of the Precious Robe of the Most Holy Theotokos",
        "slug": "2-july--deposition-of-the-precious-robe-of-the-most-holy-theotokos"
    },
    # Part 4: Triodion Rubrics
    "p319": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Sunday of the Prodigal Son",
        "slug": "sunday-of-the-prodigal-son"
    },
    "p320-322": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Meatfare Saturday (Saturday of the Dead)",
        "slug": "meatfare-saturday-saturday-of-the-dead"
    },
    "p324-325": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "On Cheesefare Wednesday and Friday",
        "slug": "on-cheesefare-wednesday-and-friday"
    },
    "p326": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Cheesefare Friday and Saturday - Note on Prostrations",
        "slug": "cheesefare-friday-and-saturday---note-on-prostrations"
    },
    "p378": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Palm Sunday Evening",
        "slug": "palm-sunday-evening"
    },
    "p379-380": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Great Monday and Great Tuesday",
        "slug": "great-monday-and-great-tuesday"
    },
    "p383-384": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Great Thursday - Matins",
        "slug": "great-thursday---matins"
    },
    "p385": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Great Thursday - Divine Liturgy and Consecration of the Lamb",
        "slug": "great-thursday---divine-liturgy-and-consecration-of-the-lamb"
    },
    "p416-418": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "The Bright and Glorious Resurrection of Christ (Pascha)",
        "slug": "the-bright-and-glorious-resurrection-of-christ-pascha"
    },
    "p421": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Resurrection of Christ - Sunday Evening (Great Vespers)",
        "slug": "resurrection-of-christ---sunday-evening-great-vespers"
    },
    "p427": {
        "target_file": "Final_Dolnytsky_part5_temple.md",
        "heading": "Specific Temple Rubrics Outside the Triodion",
        "slug": "specific-temple-rubrics-outside-the-triodion"
    },
    "p431-432": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Sunday of the Paralytic",
        "slug": "sunday-of-the-paralytic"
    },
    "p432-433": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Weekdays of the Paralytic",
        "slug": "weekdays-of-the-paralytic"
    },
    "p441": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Sunday of the Holy Fathers of the First Ecumenical Council",
        "slug": "sunday-of-the-holy-fathers-of-the-first-ecumenical-council"
    },
    "p449": {
        "target_file": "Final_Dolnytsky_part4_triodion.md",
        "heading": "Solemnity of the Most Holy Body and Blood of Christ (Eucharist)",
        "slug": "solemnity-of-the-most-holy-body-and-blood-of-christ-eucharist"
    },
    # Part 5: Temple Rubrics
    "p458": {
        "target_file": "Final_Dolnytsky_part5_temple.md",
        "heading": "General Rubric for a Temple Saint",
        "slug": "general-rubric-for-a-temple-saint"
    },
    "p468": {
        "target_file": "Final_Dolnytsky_part5_temple.md",
        "heading": "General Lenten Rubric for a Temple Saint",
        "slug": "general-lenten-rubric-for-a-temple-saint"
    },
    # External citation
    "p334": {
        "target_file": "EXTERNAL",
        "heading": "Bishop Pelesh, Pastoral Theology",
        "slug": ""
    }
}

print(f"Defined {len(PAGE_CONCORDANCE)} concordance targets.")
with open('scratch/reports/page_concordance_master.json', 'w', encoding='utf-8') as f:
    json.dump(PAGE_CONCORDANCE, f, indent=2, ensure_ascii=False)
print("Saved scratch/reports/page_concordance_master.json")
