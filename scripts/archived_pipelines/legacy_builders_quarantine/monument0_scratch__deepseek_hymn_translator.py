import os
import base64
import json
import argparse
from openai import OpenAI
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Robust DeepSeek key loader to handle different execution directories and formats
def get_deepseek_key():
    # 1. Try direct environment variable
    key = os.getenv("DEEPSEEK_API_KEY")
    if key and key != "your_deepseek_api_key_here":
        return key

    # 2. Try global .env file path
    global_env = r"C:\Users\augus\OneDrive\Documents\Google Antigravity\Projects\.env"
    if os.path.exists(global_env):
        try:
            with open(global_env, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k_clean = k.strip().replace("[", "").replace("]", "")
                        if k_clean in ("deepseek-v4-pro", "DEEPSEEK_API_KEY"):
                            val = v.strip()
                            if val:
                                return val
        except Exception as e:
            print(f"Warning: Error reading global .env: {e}")

    # 3. Try local .env
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k_clean = k.strip().replace("[", "").replace("]", "")
                        if k_clean in ("deepseek-v4-pro", "DEEPSEEK_API_KEY"):
                            val = v.strip()
                            if val and val != "your_deepseek_api_key_here":
                                return val
        except Exception as e:
            print(f"Warning: Error reading local .env: {e}")

    return None

load_dotenv()

DEEPSEEK_API_KEY = get_deepseek_key()
if DEEPSEEK_API_KEY:
    os.environ["DEEPSEEK_API_KEY"] = DEEPSEEK_API_KEY

# Initialize DeepSeek client (using OpenAI compatible interface)
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def pdf_page_to_base64(pdf_path, page_num):
    """Extract a specific page from a PDF and convert it to a base64 PNG."""
    print(f"Extracting page {page_num} from {pdf_path}...")
    doc = fitz.open(pdf_path)
    # PyMuPDF is 0-indexed. We assume user inputs 1-indexed page numbers.
    page = doc.load_page(page_num - 1)
    # 2x zoom for better resolution for the Vision model
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img_data = pix.tobytes("png")
    return base64.b64encode(img_data).decode('utf-8')

def translate_hymns(slavonic_b64, greek_b64):
    """Send images to DeepSeek Vision API for translation."""
    print("Sending images to DeepSeek API...")
    
    system_prompt = """
    You are an expert in Kyivan/Galician liturgical musicology, Church Slavonic, and Byzantine Greek.
    You are translating the Sessional Hymns (Sidalni) and Exapostilaria (Svitylni) for a feast from the Menaion.
    
    You have been provided with two images:
    1. The 1761 Pochaiv Church Slavonic Menaion (The authentic Kyivan structural and poetic base).
    2. The Greek Menaion (The semantic anchor).
    
    TRANSLATION RULES:
    - Use the Greek text to understand the exact theological meaning and metaphor.
    - However, map your English phrasing, meter, and syllable count strictly to the Slavonic text to ensure 'singability' and preserve the historical rhythm.
    - Do NOT force a literal modern translation if it breaks the poetic rhythm.
    - Pronouns (Hieratic vs. Modern): Parishes use both (e.g., Thou/Thy or You/Your). Do not force one over the other if the provided source text leans a certain way, but ensure internal consistency.
    - Capitalize Deity pronouns (He, Him, Who, You, Your).
    - Terminology: "Hymn of Light" is an acceptable term for Exaposteilarion. "Prokeimenon" is the standard spelling.
    - Doxology Standard: Always translate the doxology as exactly: "Glory be to the Father and to the Son and to the Holy Spirit, now and forever and unto the ages of ages. Amen."
    - Insert asterisks (*) to indicate musical breath marks and phrasing for chanting.
    
    GOLD STANDARD EXAMPLE:
    Slavonic: Прiиди'те взы'демъ со iи~сомъ восходѧ'щимъ на го'рꙋ ст~ꙋ'ю, и та'мѡ ѹслы'шимъ гла́съ бг҃а жива́гѡ, ѻц҃а̀ пребезнача́лна, ѻ́блакомъ свѣ́тлымъ свидѣ́телствꙋюща бжⷭ҇твеннымъ дх҃омъ, тогѡ̀ сво́йство присносꙋ́щнагѡ сыновства̀: и ѹмо́мъ просвѣща́еми, во свѣ́тѣ свѣ́тъ ѹзри́мъ.
    Translation: "Come, let us go up with Jesus who ascends the holy mountain,* and there let us listen to the voice of the living God,* the all-unoriginate Father, which through the divine Spirit* bears witness by a cloud to His true Sonship;* and, illumined in mind,* let us gaze upon Light amid light."
    
    OUTPUT FORMAT:
    Output valid JSON matching this schema exactly. Return ONLY JSON.
    {
      "menaion": {
        "august": {
          "06": {
            "matins": {
              "sessional_hymn_1": {
                "tone": "Tone X",
                "text": "..."
              },
              "exapostilarion": {
                "text": "..."
              }
            }
          }
        }
      }
    }
    """

    response = client.chat.completions.create(
        model="deepseek-v4-pro", # Transitioned to current V4 API
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Here is the Slavonic 1761 Pochaiv Menaion page:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{slavonic_b64}"}},
                    {"type": "text", "text": "Here is the corresponding Greek Menaion page:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{greek_b64}"}},
                    {"type": "text", "text": "Please extract and translate the Sessional Hymns and Exapostilaria into JSON."}
                ]
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        extra_body={
            "thinking": {"type": "disabled"} # Keep thinking disabled for deterministic JSON vision extraction
        }
    )
    
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="DeepSeek Hymn Translator")
    parser.add_argument("--slavonic_pdf", required=True, help="Path to Slavonic PDF")
    parser.add_argument("--slavonic_page", required=True, type=int, help="Page number in Slavonic PDF (1-indexed)")
    parser.add_argument("--greek_pdf", required=True, help="Path to Greek PDF")
    parser.add_argument("--greek_page", required=True, type=int, help="Page number in Greek PDF (1-indexed)")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    
    args = parser.parse_args()
    
    if not get_deepseek_key():
        print("ERROR: DEEPSEEK_API_KEY environment variable or .env file entry not set.")
        print("Please create a .env file with DEEPSEEK_API_KEY=your_key")
        return

    try:
        slavonic_b64 = pdf_page_to_base64(args.slavonic_pdf, args.slavonic_page)
        greek_b64 = pdf_page_to_base64(args.greek_pdf, args.greek_page)
        
        json_output = translate_hymns(slavonic_b64, greek_b64)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_output)
            
        print(f"Successfully wrote output to {args.output}")
        
    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    main()
