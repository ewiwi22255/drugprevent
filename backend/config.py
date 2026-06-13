import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "drugprevent")
DEEPSEEK_API_KEY  = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://opencode.ai/zen/go/v1")
DEEPSEEK_MODEL    = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")
DEBUG     = os.getenv("FLASK_DEBUG", "true").lower() == "true"
