import json

# Define the canonical service types and variables for each of the 34 cases
CASE_VARIABLES = {
    "case_1a": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:31-49"
    },
    "case_1b": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:50-70"
    },
    "case_2": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_basil",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:71-74"
    },
    "case_3": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:77-84"
    },
    "case_4": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "memorial_transferred_to": "thursday_before_meatfare",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:85-86"
    },
    "case_5": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:87-91"
    },
    "case_6": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:92-96"
    },
    "case_7": {
        "vespers_type": "lenten_vespers",
        "matins_type": "lenten_matins_weekday",
        "liturgy_type": "structure_suppressed",
        "has_polyeleos": False,
        "doxology_type": "daily_read",
        "rank": "rank_simple_6",
        "action": "transfer_to_cheesefare_sunday",
        "transfer_target": "sunday_cheesefare",
        "transferred_service_types": {
            "vespers_type": "great_vespers_vigil",
            "matins_type": "great_matins",
            "liturgy_type": "liturgy_chrysostom",
            "has_polyeleos": True,
            "doxology_type": "great_doxology",
            "rank": "rank_vigil_patronal"
        },
        "source_ref": "Final_Dolnytsky_part5_temple.txt:97-100"
    },
    "case_8": {
        "vespers_type": "lenten_vespers",
        "matins_type": "lenten_matins_weekday",
        "liturgy_type": "structure_suppressed",
        "has_polyeleos": False,
        "doxology_type": "daily_read",
        "rank": "rank_simple_6",
        "action": "transfer_to_first_saturday_lent",
        "transfer_target": "saturday_1st_lent",
        "transferred_service_types": {
            "vespers_type": "great_vespers_vigil",
            "matins_type": "great_matins",
            "liturgy_type": "liturgy_chrysostom",
            "has_polyeleos": True,
            "doxology_type": "great_doxology",
            "rank": "rank_vigil_patronal"
        },
        "source_ref": "Final_Dolnytsky_part5_temple.txt:101-104"
    },
    "case_9": {
        "vespers_type": "lenten_vespers_presanctified",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:105-113"
    },
    "case_10": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_basil",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:114-126"
    },
    "case_11": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_presanctified",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:127-148"
    },
    "case_12": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:149-152"
    },
    "case_13": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_basil",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:153-155"
    },
    "case_14": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_basil",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:156-157"
    },
    "case_15": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_presanctified",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:158-159"
    },
    "case_16": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_presanctified",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:160-161"
    },
    "case_17": {
        "vespers_type": "lenten_vespers_presanctified",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:162-182"
    },
    "case_18": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:183-200"
    },
    "case_19": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:201-205"
    },
    "case_20": {
        "vespers_type": "structure_suppressed",
        "matins_type": "structure_suppressed",
        "liturgy_type": "structure_suppressed",
        "has_polyeleos": False,
        "doxology_type": "none",
        "rank": "rank_simple_6",
        "action": "transfer_to_palm_sunday_or_bright_week",
        "transfer_target": "palm_sunday_or_bright_monday",
        "transferred_service_types": {
            "vespers_type": "great_vespers_vigil",
            "matins_type": "great_matins",
            "liturgy_type": "liturgy_chrysostom",
            "has_polyeleos": True,
            "doxology_type": "great_doxology",
            "rank": "rank_vigil_patronal"
        },
        "source_ref": "Final_Dolnytsky_part5_temple.txt:206-208"
    },
    "case_21": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:209-211"
    },
    "case_22": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:212-215"
    },
    "case_23": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:216-218"
    },
    "case_24": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:219-220"
    },
    "case_25": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:221-223"
    },
    "case_26": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:224-225"
    },
    "case_27": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "memorial_transferred_to": "previous_saturday_or_thursday",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:226-227"
    },
    "case_28": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:228-229"
    },
    "case_29": {
        "vespers_type": "kneeling_vespers",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:230-231"
    },
    "case_30": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:232-234"
    },
    "case_31": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:235-236"
    },
    "case_32": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:238-239"
    },
    "case_33": {
        "vespers_type": "great_vespers_vigil",
        "matins_type": "great_matins",
        "liturgy_type": "liturgy_chrysostom",
        "has_polyeleos": True,
        "doxology_type": "great_doxology",
        "rank": "rank_vigil_patronal",
        "source_ref": "Final_Dolnytsky_part5_temple.txt:240-243"
    }
}

with open("json_db/02d_logic_temple.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cases = data.get("specific_cases", {})
for cid, vals in CASE_VARIABLES.items():
    if cid in cases:
        c = cases[cid]
        # Set top-level service types
        c["vespers_type"] = vals["vespers_type"]
        c["matins_type"] = vals["matins_type"]
        c["liturgy_type"] = vals["liturgy_type"]
        c["has_polyeleos"] = vals["has_polyeleos"]
        c["doxology_type"] = vals["doxology_type"]
        
        # Ensure variables block exists and contains all types and rank
        if "variables" not in c or not isinstance(c["variables"], dict):
            c["variables"] = {}
        c["variables"]["vespers_type"] = vals["vespers_type"]
        c["variables"]["matins_type"] = vals["matins_type"]
        c["variables"]["liturgy_type"] = vals["liturgy_type"]
        c["variables"]["has_polyeleos"] = vals["has_polyeleos"]
        c["variables"]["doxology_type"] = vals["doxology_type"]
        c["variables"]["rank"] = vals["rank"]
        
        # Transfer fields
        if "action" in vals:
            c["action"] = vals["action"]
            c["transfer_target"] = vals["transfer_target"]
            c["transferred_service_types"] = vals["transferred_service_types"]
        if "memorial_transferred_to" in vals:
            c["memorial_transferred_to"] = vals["memorial_transferred_to"]
        c["source_ref"] = vals["source_ref"]

data["file_metadata"]["version"] = "3.1 (Canonical Service Types Fortified)"
data["file_metadata"]["last_updated"] = "2026-09-07"

with open("json_db/02d_logic_temple.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Successfully fortified json_db/02d_logic_temple.json!")
