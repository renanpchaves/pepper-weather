import os
from dotenv import load_dotenv
import requests
import logging
from backend.core.exceptions import CityNotFound


logger = logging.getLogger(__name__)
load_dotenv()


class WeatherService:
    """
    Service for fetching weather data using OpenWeatherMap API.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

    def get_weather(self, city: str) -> dict:
        """
        Fetch current weather data for a given city.

        Args:
            city: City name, e.g. "Rio de Janeiro", "São Paulo"

        Returns:
            A dictionary containing weather data
        """
        if not self.api_key:
            logger.warning("⚠️ OPENWEATHER_API_KEY not found. Returning empty dict.")
            return {}

        try:
            logger.info(f"🔍 Fetching weather for city: {city}")

            response = requests.get(
                self.BASE_URL,
                params={
                    "q": city,
                    "appid": self.api_key,
                    "units": "metric",
                    "lang": "pt_br",
                },
            )
            if response.status_code == 404:
                logger.error(f"❌ City not found: {city}")
                raise CityNotFound(f"City not found: {city}")

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logger.error(f"❌ Error fetching weather data: {e}")
            raise RuntimeError(f"Failed to fetch weather data: {e}")
