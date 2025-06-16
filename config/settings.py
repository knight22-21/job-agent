import os
from dotenv import load_dotenv

load_dotenv()

# General Settings
WHATSAPP_GROUP = os.getenv("WHATSAPP_GROUP", "default-group-id")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
SCRAPER_DELAY = int(os.getenv("SCRAPER_DELAY", 2))
print("OLLAMA_MODEL in settings.py:", OLLAMA_MODEL)