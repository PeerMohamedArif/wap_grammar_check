import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    PORT = int(os.getenv("PORT", 8000))

    # WhatsApp API
    WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
    PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
    WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")

    # Default forward target
    DEFAULT_FORWARD_NUMBER = os.getenv("DEFAULT_FORWARD_NUMBER")

    # Local LLaMA
    LLAMA_API_URL = os.getenv("LLAMA_API_URL", "http://localhost:11434/api/generate")
