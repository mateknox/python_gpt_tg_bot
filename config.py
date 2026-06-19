import os
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# API Tokens - Securely extracted from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "<INSERT TOKEN>")
OMDB_TOKEN = os.getenv("OMDB_TOKEN", "<INSERT TOKEN>")
GOOGLE_TOKEN = os.getenv("GOOGLE_TOKEN", "<INSERT TOKEN>")
KP_TOKEN = os.getenv("KP_TOKEN", "<INSERT TOKEN>")
IMDB_TOKEN = os.getenv("IMDB_TOKEN", "<INSERT TOKEN>")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "<INSERT TOKEN>")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(BASE_DIR / "logs.txt", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("media_bot")
