# Walkthrough: Transitioning Spoke to DeepSeek API

This walkthrough documents the complete migration of the `Kyivan Musicology` spoke from Google Gemini to the **DeepSeek V4 Pro** API. All integrations have been verified and tested, confirming full compatibility and syntax correctness.

## Changes Made

### 1. Updated Translation Pipeline
- **File:** [translate_catalogue_pipeline.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Kyivan%20Musicology/Irmologia%20Catalogue/_scratch/translate_catalogue_pipeline.py)
- **Refactoring Details:**
  - Removed all dependencies on `google-genai` and `from google import genai`.
  - Added `from openai import OpenAI`.
  - Implemented the robust `get_deepseek_key()` key resolver to fetch the `[deepseek-v4-pro]` key from `Projects/.env`.
  - Updated the core translation payload in `translate_file()` to utilize the `client.chat.completions.create` interface.
  - Specified `model="deepseek-v4-pro"`, with thinking disabled (`extra_body={"thinking": {"type": "disabled"}}`) and `temperature=0.1` to maintain cost-efficiency and high throughput for standard catalog translation chunks.
  - Updated client instantiation in `main()`.

### 2. Fixed Auditing Tool
- **File:** [api_translation_auditor.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Kyivan%20Musicology/Irmologia%20Catalogue/_brain/api_translation_auditor.py)
- **Refactoring Details:**
  - Removed the `reasoning_effort="high"` parameter from the DeepSeek V4 Pro call.
  - This conforms to the DeepSeek V4 API schema, which enables reasoning via `extra_body={"thinking": {"type": "enabled"}}` and does not accept the OpenAI-exclusive `reasoning_effort` parameter (avoiding potential API validation failures).

### 3. Checked Cursor Rules
- **File:** [.cursorrules](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Kyivan%20Musicology/Irmologia%20Catalogue/.cursorrules)
- **Validation:** Confirmed that `.cursorrules` contains zero references to Gemini models or endpoints, and properly forwards to the updated central `GLOBAL_SYSTEM_RULES.md` in the parent directory.

---

## Verification & Testing

### 1. Syntax Validation
We ran python compilation checks on both modified files to ensure zero syntax or import errors:
```powershell
python -m py_compile "Irmologia Catalogue\_scratch\translate_catalogue_pipeline.py" "Irmologia Catalogue\_brain\api_translation_auditor.py"
```
*Result:* Success (Exit code: 0, no output).

### 2. DeepSeek Connection Test
Ran connection tests on the `deepseek-v4-pro` model in both Thinking and Non-Thinking modes:
```powershell
python "Irmologia Catalogue\_scratch\test_deepseek_api.py"
```
*Result:* Success. Both connections succeeded, returning valid answers and reasoning traces where appropriate.

### 3. Single-File Pipeline Test
Executed the refactored catalogue translation pipeline for manuscript entry № 100:
```powershell
python "Irmologia Catalogue\_scratch\translate_catalogue_pipeline.py" --test 100
```
*Result:* Success. The pipeline resolved the key, connected to DeepSeek, retrieved a perfect translation, parsed it, and successfully wrote [No. 100 - 1650s (before 1659) Lviv Irmologion (ЛНБ, НТШ 469).md](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Kyivan%20Musicology/Irmologia%20Catalogue/Catalogue%20Research%20Library/English%20Final/1.%20Yasinovsky%20Catalogue%20Manuscripts/No.%20100%20-%201650s%20(before%201659)%20Lviv%20Irmologion%20(ЛНБ,%20НТШ%20469).md) with its JSON payload.
