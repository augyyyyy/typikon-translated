import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/step75_thinking.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length:", len(text))
print("--- HEAD 1500 chars ---")
print(text[:1500])
print("\n--- TAIL 2000 chars ---")
print(text[-2000:])
