# Transition to DeepSeek-Only API Configuration

Refactor all AI, agent, brain, and orchestration scripts within the Kyivan Musicology spoke to use exclusively the DeepSeek API. The Google Gemini API key has been removed from the environment and `Projects/.env`, so all residual Gemini configurations and clients must be removed. We will configure DeepSeek `deepseek-v4-pro` calls across both translation pipelines and auditing utilities.

## User Review Required

> [!IMPORTANT]
> - **API Provider Limitation:** Gemini integrations are fully deleted. The codebase will run exclusively on DeepSeek V4 Pro.
> - **Thinking Parameter Behavior:** As per DeepSeek API guidelines, when `thinking` mode is enabled, traditional parameters like `temperature` must be omitted. When `thinking` is disabled (optimized for standard high-throughput translation chunks), we will supply a standard `temperature=0.1`.

## Open Questions

- No major open questions are identified, as the prompt specifies that Gemini is defunct and must be completely replaced by DeepSeek API calls.

## Proposed Changes

---

### Translation Pipelines & Scripts

#### [MODIFY] [translate_catalogue_pipeline.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Kyivan%20Musicology/Irmologia%20Catalogue/_scratch/translate_catalogue_pipeline.py)
- Remove `from google import genai` and `from google.genai import types`.
- Import `from openai import OpenAI`.
- Replace `load_gemini_key()` with `get_deepseek_key()`.
- Refactor `translate_file(client, ukr_filepath, url)` to use the standard OpenAI client completions call targeting `deepseek-v4-pro` in non-thinking mode (`thinking: {"type": "disabled"}`) with `temperature=0.1`.
- Update `main()` to resolve the DeepSeek key and instantiate `OpenAI(api_key=api_key, base_url="https://api.deepseek.com")`.

---

### Auditing Utilities

#### [MODIFY] [api_translation_auditor.py](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Kyivan%20Musicology/Irmologia%20Catalogue/_brain/api_translation_auditor.py)
- Remove `reasoning_effort="high"` from `client.chat.completions.create` when calling DeepSeek V4 Pro in thinking mode. DeepSeek uses `extra_body={"thinking": {"type": "enabled"}}` and does not support the `reasoning_effort` parameter, which could cause validation failures.

---

### Workspace Rules

#### [MODIFY] [.cursorrules](file:///c:/Users/augus/OneDrive/Documents/Google%20Antigravity/Projects/Kyivan%20Musicology/Irmologia%20Catalogue/.cursorrules)
- Verify there are no legacy model references and ensure it correctly points to the central rules page `GLOBAL_SYSTEM_RULES.md`.

## Verification Plan

### Automated Tests
- We will execute python syntax verification on all changed files:
  ```powershell
  python -m py_compile "Irmologia Catalogue\_scratch\translate_catalogue_pipeline.py"
  python -m py_compile "Irmologia Catalogue\_brain\api_translation_auditor.py"
  ```
- Run a dry-run test of `translate_catalogue_pipeline.py` with `--test 410 --limit 1` to ensure API connection and parsing succeed.
