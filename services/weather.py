from dotenv import load_dotenv
import requests
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "⚠️ OPENWEATHER_API_KEY not found. Weather data will not be available."
    )


def get_weather(city: str):
    try:
        response = requests.get(
            BASE_URL,
            params={"q": city, "appid": API_KEY, "units": "metric", "lang": "pt_br"},
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"❌ Error fetching weather data: {e}")
        raise RuntimeError(f"Failed to fetch weather data: {e}")
