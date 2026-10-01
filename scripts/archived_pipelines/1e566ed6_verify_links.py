import os
import re

def slugify(text):
    # Standard Markdown header slugification
    # 1. Lowercase
    # 2. Strip non-alphanumeric/spaces/hyphens
    # 3. Replace spaces with hyphens
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9\s\-]', '', slug)
    slug = slug.replace(' ', '-')
    slug = re.sub(r'-+', '-', slug) # reduce multiple hyphens
    return slug

def verify_links(master_path):
    if not os.path.exists(master_path):
        return f"Master file not found: {master_path}"
        
    with open(master_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all headings (e.g. # Heading) and slugify them
    # Headings look like: ^#+ (.*)
    headings = re.findall(r'^#+\s+(.*)$', content, re.MULTILINE)
    anchors = set(slugify(h) for h in headings)
    
    # Also find explicit anchors like <a name="anchor"></a> or id="anchor"
    explicit_anchors = re.findall(r'id="([^"]+)"', content)
    explicit_anchors += re.findall(r'name="([^"]+)"', content)
    anchors.update(explicit_anchors)
    
    # Find all local links like [text](#link)
    links = re.findall(r'\[([^\]]*)\]\(#([^\)]+)\)', content)
    
    broken_links = []
    checked_count = 0
    for text, link in links:
        checked_count += 1
        # Strip query parameters or lines if any
        link_clean = link.split('#')[-1]
        if link_clean not in anchors:
            broken_links.append((text, link))
            
    res = f"Checked {checked_count} internal links. Found {len(broken_links)} broken links.\n"
    if broken_links:
        res += "Broken links:\n"
        for text, link in broken_links[:20]: # show first 20
            res += f"  * [{text}](#{link})\n"
    else:
        res += "SUCCESS: No broken internal links found!"
    return res

if __name__ == "__main__":
    typikon_dir = r"c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Typikon"
    master = os.path.join(typikon_dir, "Dolnytsky_Typikon_Master.md")
    print(verify_links(master))
