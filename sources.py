import logging
import requests
from google import genai
from google.genai import types
import config

logger = logging.getLogger("media_bot")


# Base API Client to abstract away repetitive requests logic
class BaseApiClient:
    def __init__(self, base_url, headers=None, default_params=None):
        self.base_url = base_url
        self.headers = headers or {}
        self.default_params = default_params or {}

    def _get(self, endpoint="", params=None, extra_headers=None):
        url = f"{self.base_url}{endpoint}"
        combined_params = {**self.default_params, **(params or {})}
        combined_headers = {**self.headers, **(extra_headers or {})}

        try:
            response = requests.get(url, headers=combined_headers, params=combined_params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API Error for {url}: {e}")
            return None


# Dedicated Media Engine Provider
class MediaSearchEngine:
    def __init__(self):
        # OMDb client setup via RapidAPI
        self.omdb = BaseApiClient(
            base_url="https://online-movie-database.p.rapidapi.com/title",
            headers={
                "X-RapidAPI-Key": config.OMDB_TOKEN,
                "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
            }
        )
        # Kinopoisk client setup
        self.kp = BaseApiClient(
            base_url="https://kinopoiskapiunofficial.tech/api/v2.1/films",
            headers={"accept": "application/json", "X-API-KEY": config.KP_TOKEN}
        )

        # Initialize Gemini Engine
        try:
            self.ai_client = genai.Client()
        except Exception as e:
            logger.error(f"Gemini init error: {e}")
            self.ai_client = None

    def ask_gemini(self, prompt: str) -> str:
        if not self.ai_client:
            return "AI engine unconfigured."

        # Enforcing strict, flat paragraph structures for Telegram compatibility
        telegram_rules = (
            "You are a media recommendation assistant for a Telegram bot.\n"
            "CRITICAL FORMATTING LAWS FOR TELEGRAM PARSER:\n"
            "1. NEVER use headers like #, ##, or ###. Use normal text instead.\n"
            "2. NEVER use markdown bullet characters (* or -) for numbered lists.\n"
            "3. Format lists simply by using a clear number and bold title, exactly like this:\n"
            "1. **Movie Title (Year)**\n"
            "Write the movie description on a fresh, non-indented newline immediately below it.\n"
            "4. Keep descriptions concise, single-paragraph, and avoid nested details or indented sub-bullets."
        )

        try:
            # Setup the correct configuration parameters object using the unified SDK
            config_options = types.GenerateContentConfig(
                system_instruction=telegram_rules,
                temperature=0.7
            )

            response = self.ai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=config_options
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API failure: {e}")
            return "Failed to fetch response from Gemini."

    def search_movies_by_genre(self, genre: str) -> list:
        # Hits the popular movies endpoint
        data = self.omdb._get("/v2/get-popular-movies-by-genre", params={"genre": genre, "limit": "100"})
        return data if isinstance(data, list) else []

    def get_movie_details(self, title_id: str) -> dict:
        data = self.omdb._get("/get-details", params={"tconst": title_id})
        return data if isinstance(data, dict) else {}

    def search_kinopoisk(self, keyword: str) -> dict:
        return self.kp._get("/search-by-keyword", params={"keyword": keyword}) or {"films": []}
