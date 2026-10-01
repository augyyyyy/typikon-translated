import json
from openai import OpenAI

transcript_path = r'C:\Users\augus\.gemini\antigravity\brain\9686e761-280f-434e-9d19-e1c17478fcc5\.system_generated\logs\transcript.jsonl'

conversation_history = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step_type = data.get('type')
            if step_type == 'USER_INPUT':
                content = data.get('content', '')
                if '<USER_REQUEST>' in content:
                    content = content.split('</USER_REQUEST>')[0].split('<USER_REQUEST>')[-1].strip()
                conversation_history.append(f"USER: {content}")
            elif step_type == 'PLANNER_RESPONSE':
                content = data.get('content', '')
                if content:
                    # just take first 200 chars to save space
                    conversation_history.append(f"AI: {content[:200]}...")
        except:
            continue

transcript_text = "\n\n".join(conversation_history)

# Compress drastically to fit 4096 tokens (approx 12000 chars)
if len(transcript_text) > 12000:
    transcript_text = transcript_text[-12000:]

prompt = f"""
You are reviewing a conversation transcript about building a 'Kliros Master Binder' (a liturgical book project involving Ruthenian/Stamford Typikon, MS Word documents).

Transcript snippet:
---------------------
{transcript_text}
---------------------

Provide a recap with exactly these sections:
1. **How we stayed on track:** (Goals achieved according to user's vision)
2. **How we drifted:** (Where the AI misunderstood instructions or overstepped, especially regarding document consolidation vs. separation)
3. **Next Steps for this chat:** (Logical next actions)
"""

client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

try:
    response = client.chat.completions.create(
      model="qwen2.5-coder-14b-instruct",
      messages=[
        {"role": "user", "content": prompt}
      ],
      temperature=0.2
    )

    result = response.choices[0].message.content
    with open('recap_result.md', 'w', encoding='utf-8') as out:
        out.write(result)
    print("Success. Saved to recap_result.md")
except Exception as e:
    print("Error:", e)
