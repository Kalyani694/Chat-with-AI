import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    ACTIVE_LLM = os.getenv("ACTIVE_LLM", "openai")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

settings = Settings()  
