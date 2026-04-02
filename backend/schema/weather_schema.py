from pydantic import BaseModel, Field
from typing import Optional


class WeatherData(BaseModel):
    """
    Pydantic model representing weather data.
    """

    temperature: float = Field(..., description="Current temperature in Celsius")
    humidity: int = Field(..., description="Current humidity percentage")
    pressure: int = Field(..., description="Current atmospheric pressure in hPa")
    wind_speed: float = Field(..., description="Current wind speed in m/s")
    weather_description: str = Field(
        ..., description="Description of the current weather conditions"
    )
    icon: str = Field(
        ..., description="Weather condition icon code from OpenWeatherMap"
    )
    city_name: Optional[str] = Field(
        None, description="Name of the city for which the weather data is provided"
    )
    country_code: Optional[str] = Field(None, description="Country code for the city")
