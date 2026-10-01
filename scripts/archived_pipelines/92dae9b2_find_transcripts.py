import os
from pathlib import Path

def main():
    brain_dir = Path("C:/Users/augus/.gemini/antigravity/brain")
    if not brain_dir.exists():
        print(f"Error: {brain_dir} does not exist")
        return
        
    print(f"Scanning {brain_dir} for transcripts...")
    transcripts = []
    for p in brain_dir.iterdir():
        if p.is_dir():
            log_file = p / ".system_generated" / "logs" / "transcript.jsonl"
            if log_file.exists():
                size = log_file.stat().st_size
                transcripts.append((p.name, log_file, size))
                
    print(f"Found {len(transcripts)} transcripts.")
    # Sort by size descending
    transcripts.sort(key=lambda x: x[2], reverse=True)
    for name, path, size in transcripts[:20]:
        print(f"Conversation: {name} | Size: {size/1024:.2f} KB | Path: {path}")

if __name__ == "__main__":
    main()
