import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('text_royaldoors.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    versions = {}
    for k, v in data.items():
        if '02_02' in k and 'troparion_1' in k:
            content = v.get('content', '').strip()
            versions[content] = versions.get(content, []) + [k]
            
    print(f"Found {len(versions)} unique versions of the Presentation Troparion:")
    for content, keys in versions.items():
        print(f"  Keys: {keys[:3]} (total {len(keys)})")
        print(f"  Content: {repr(content[:100])}")
        
if __name__ == '__main__':
    main()
