from fastapi import APIRouter, HTTPException
from backend.models.weather import WeatherService
from backend.schema.weather_schema import WeatherData
from backend.core.exceptions import CityNotFound


router = APIRouter(prefix="/weather", tags=["Weather"])
service = WeatherService()


@router.get("/{city}", response_model=WeatherData)
def get_weather(city: str):
    try:
        data = service.get_weather(city)
        if not data:
            raise HTTPException(
                status_code=404, detail="City not found or API key missing"
            )
        return WeatherData(
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            wind_speed=data["wind"]["speed"],
            weather_description=data["weather"][0]["description"],
            icon=data["weather"][0]["icon"],
            city_name=data["name"],
            country_code=data["sys"]["country"],
        )
    except CityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
