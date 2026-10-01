import os
import re
import sys

# Reconfigure stdout to support utf-8 in case we still print some things
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def slugify(text):
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9\s\-]', '', slug)
    slug = slug.replace(' ', '-')
    slug = re.sub(r'-+', '-', slug)
    return slug

def main():
    typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
    master = os.path.join(typikon_dir, "Dolnytsky_Typikon_Master.md")
    report_file = os.path.join(typikon_dir, "broken_links_report.txt")
    
    with open(master, 'r', encoding='utf-8') as f:
        content = f.read()
        
    headings = re.findall(r'^#+\s+(.*)$', content, re.MULTILINE)
    anchors = set(slugify(h) for h in headings)
    
    explicit_anchors = re.findall(r'id="([^"]+)"', content)
    explicit_anchors += re.findall(r'name="([^"]+)"', content)
    anchors.update(explicit_anchors)
    
    links = re.findall(r'\[([^\]]*)\]\(#([^\)]+)\)', content)
    
    broken_links = []
    for text, link in links:
        link_clean = link.split('#')[-1]
        if link_clean not in anchors:
            broken_links.append((text, link))
            
    # Also find possible target headings in the master file
    all_headings_slugs = {slugify(h): h for h in headings}
    
    lines = []
    lines.append(f"Checked {len(links)} links. Found {len(broken_links)} broken links.")
    lines.append("\nDetailed list of broken links:")
    for i, (text, link) in enumerate(broken_links):
        link_clean = link.split('#')[-1]
        
        # Try to find a close match in existing anchors
        matches = []
        for slug, heading in all_headings_slugs.items():
            # Match if target slug contains part of the link, or vice versa
            if link_clean[:15] in slug or slug[:15] in link_clean or slugify(text)[:15] in slug:
                matches.append(heading)
        
        match_str = f" | Possible targets: {matches[:5]}" if matches else " | No close heading match found"
        lines.append(f"{i+1:3d}. Link: [{text}](#{link}){match_str}")
        
    with open(report_file, 'w', encoding='utf-8') as f_out:
        f_out.write("\n".join(lines))
        
    print(f"Report written to: {report_file}")

if __name__ == "__main__":
    main()
