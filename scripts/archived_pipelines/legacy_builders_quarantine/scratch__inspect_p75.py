import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/step75_thinking.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
print(f"Total paragraphs in step75_thinking: {len(paragraphs)}")
for i, p in enumerate(paragraphs):
    print(f"--- P{i} ({len(p)} chars) ---")
    print(p[:150] + ("..." if len(p) > 150 else ""))
