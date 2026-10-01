import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    p = r'c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Recensions\Stamford Divine Office\JSON_MD\TROPARIA MENAION.md'
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    start = text.find('[')
    end = text.rfind(']')
    data = json.loads(text[start:end+1])
    
    current_month = None
    comms = []
    for idx, item in enumerate(data):
        for k, v in item.items():
            v_str = str(v).strip()
            if k in ['feast', 'rubric'] and v_str.upper() == 'JANUARY':
                current_month = 'JANUARY'
            elif k in ['feast', 'rubric'] and v_str.upper() == 'FEBRUARY':
                current_month = 'FEBRUARY'
            elif (k.startswith('sticheron_') or k == 'rubric') and current_month == 'JANUARY':
                # Check if it's a hymn: has a colon and the prefix is a hymn type
                is_hymn = False
                if ':' in v_str:
                    prefix = v_str.split(':', 1)[0].lower()
                    if any(h in prefix for h in ['troparion', 'kontakion', 'dismissal', 'hypakoe']):
                        is_hymn = True
                
                is_metadata = any(m in v_str.lower() for m in ['readings at vespers', 'for readings'])
                if not is_hymn and not is_metadata and len(v_str) > 5:
                    comms.append((idx, v_str))
                    
    for i, (idx, name) in enumerate(comms):
        print(f"{i+1}: Index {idx} -> {name}")

if __name__ == '__main__':
    main()
