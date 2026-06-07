import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "drugprevent")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEBUG     = os.getenv("FLASK_DEBUG", "true").lower() == "true"
