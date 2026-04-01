from fastapi import APIRouter, HTTPException
from models.weather import WeatherService
from models.weather_schema import WeatherData

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
            city_name=data["name"],
            country_code=data["sys"]["country"],
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
