from app.config import get_settings
import importlib.util

s = get_settings()
print('llm_provider =', s.llm_provider)
print('gemini_api_key set =', bool(s.gemini_api_key))
print('google-genai installed =', importlib.util.find_spec('google.genai') is not None)
