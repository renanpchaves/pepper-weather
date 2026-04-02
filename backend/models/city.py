import os
from dotenv import load_dotenv
import requests
import logging

logger = logging.getLogger(__name__)
load_dotenv()


class CityService:
    """
    Service for fetching city data using OpenWeatherMap API.
    """

    BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

    def search_city(self, city: str) -> list:
        """
        Fetch city data for a given city.

        Args:
            city: City name, e.g. "Rio de Janeiro", "São Paulo"

        Returns:
            A list containing city data
        """
        if not self.api_key:
            logger.warning("⚠️ OPENWEATHER_API_KEY not found. Returning empty list.")
            return []

        try:
            logger.info(f"🔍 Fetching city data for city: {city}")

            response = requests.get(
                self.BASE_URL,
                params={
                    "q": city,
                    "appid": self.api_key,
                    "limit": 5,
                },
            )
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logger.error(f"❌ Error fetching city data: {e}")
            raise
