import os
import re
import difflib

# Configuration: Mapping RAW parts to English Broken files
FILE_MAPPING = {
    "RAW_PART1_TRANSLATION.txt": "dolnytsky_part1_structure.txt",
    "RAW_PART2_TRANSLATION.txt": "dolnytsky_part2_general_rubrics.txt",
    "RAW_PART3_TRANSLATION.txt": "dolnytsky_part3_menaion.txt",
    "RAW_PART4_TRANSLATION.txt": "dolnytsky_part4_triodion.txt",
    "RAW_PART5_TRANSLATION.txt": "dolnytsky_part5_temple.txt",
}

RAW_DIR = "e:/Google Antigravity/Projects/Translation/RAW"
REF_DIR = "e:/Google Antigravity/Projects/Translation/English Broken"

def normalize(text):
    # Remove punctuation for better matching, but keep word boundary cues
    text = re.sub(r'[^\w\s]', '', text)
    return ' '.join(text.lower().split())

def stitch_part(raw_name, ref_name):
    print(f"Stitching {raw_name} -> {ref_name}...")
    
    raw_path = os.path.join(RAW_DIR, raw_name)
    ref_path = os.path.join(REF_DIR, ref_name)
    
    if not os.path.exists(raw_path) or not os.path.exists(ref_path):
        print(f"Error: Missing {raw_path} or {ref_path}")
        return

    raw_content = open(raw_path, 'r', encoding='utf-8').read()
    ref_content = open(ref_path, 'r', encoding='utf-8').read()
    
    # Identify markers in RAW
    # Markers appear as ^[n]
    markers = list(re.finditer(r'\^\[(\d+)\]', raw_content))
    
    stitched_text = ref_content
    offset_delta = 0
    
    report = []
    
    for match in markers:
        m_num = match.group(1)
        m_start = match.start()
        
        # Take context from RAW
        context_before_raw = raw_content[max(0, m_start-100):m_start]
        # Skip labels like "Chunk X" or footnote definitions at end of file
        if "Chunk" in context_before_raw or "\n^[" in context_before_raw:
             # This is likely a definition, skip it
             continue
             
        # Extract meaningful local anchor (last 40 chars)
        anchor_raw = context_before_raw.strip()
        if len(anchor_raw) > 40:
            anchor_raw = anchor_raw[-40:]
            
        # Optimization: Simple string find if possible, else fuzzy
        # Since refined text is polished, we use a specialized matcher
        
        # Find matches in ref_content
        # We look for the most similar sequence
        # For now, let's try a direct substring match of a normalized slice
        norm_anchor = normalize(anchor_raw)
        
        # We search in a moving target
        # To avoid misplacing footnote 100 in the place of footnote 5, 
        # we should stay close to the relative progress.
        
        # For now, let's find all occurrences of normalized anchor and pick best one
        # but realistically, direct string search on un-normalized content is safer if wording matches
        
        # Attempt direct match on a small snippet
        snippet = anchor_raw.strip().split()[-4:] # Last 4 words
        search_str = " ".join(snippet)
        
        target_pos = -1
        last_found_pos = 0 # Track progress to ensure sequence
        
        # Fuzzy find
        # We use a windowed search to maintain sequence
        search_area = stitched_text[last_found_pos:]
        
        # Very simple version: find the snippet
        # In a real scenario, I'd use fuzzy matching logic here.
        # Let's try to locate the sentence ending.
        
        # Search for roughly the same text
        # Since I'm an agent and can't use complex 3rd party libs easily, 
        # I'll rely on common rubrical anchors.
        
        found = False
        # Try to find the exact 3-4 word phrase
        for i in range(len(snippet), 1, -1):
            sub_snippet = " ".join(snippet[-i:])
            if sub_snippet in search_area:
                pos = search_area.find(sub_snippet) + len(sub_snippet)
                target_pos = last_found_pos + pos
                found = True
                break
        
        if found:
            # Insert the marker
            marker_str = f"^[ {m_num} ]" # Using space for visibility during test
            stitched_text = stitched_text[:target_pos] + marker_str + stitched_text[target_pos:]
            last_found_pos = target_pos + len(marker_str)
            report.append(f"Inserted ^[{m_num}] at {target_pos}")
        else:
            report.append(f"FAILED to place ^[{m_num}] context: '{anchor_raw}'")
            
    # Write output to scratch for verification
    out_path = os.path.join(REF_DIR, "stitched_" + ref_name)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(stitched_text)
    
    return report

if __name__ == "__main__":
    # Test on Part 1
    rep = stitch_part("RAW_PART1_TRANSLATION.txt", "dolnytsky_part1_structure.txt")
    for line in rep[:20]: print(line)
