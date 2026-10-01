import json
import sys

def get_is_hymn(v_str):
    if ':' in v_str:
        prefix = v_str.split(':', 1)[0].lower()
        if any(h in prefix for h in ['troparion', 'kontakion', 'dismissal', 'hypakoe']):
            return True
    return False

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    p = r'c:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\Typikon Coded\Data\Service Books\Recensions\Stamford Divine Office\JSON_MD\TROPARIA MENAION.md'
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    start = text.find('[')
    end = text.rfind(']')
    data = json.loads(text[start:end+1])
    
    months = ['FEBRUARY', 'JUNE', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
    current_month = None
    comms = {m: [] for m in months}
    
    for idx, item in enumerate(data):
        for k, v in item.items():
            v_str = str(v).strip()
            if k in ['feast', 'rubric'] and v_str.upper() in months:
                current_month = v_str.upper()
            elif k in ['feast', 'rubric'] and v_str.upper() in ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'] and v_str.upper() not in months:
                current_month = None
            elif (k.startswith('sticheron_') or k == 'rubric') and current_month:
                is_hymn = get_is_hymn(v_str)
                is_metadata = any(m in v_str.lower() for m in ['readings at vespers', 'for readings'])
                if not is_hymn and not is_metadata and len(v_str) > 5:
                    comms[current_month].append((idx, v_str))
                    
    for m in months:
        print(f"\n--- {m} ---")
        for i, (idx, name) in enumerate(comms[m]):
            print(f"  {i+1}: Index {idx} -> {name}")

if __name__ == '__main__':
    main()
