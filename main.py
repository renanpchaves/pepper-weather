from fastapi import FastAPI
from core.logging import setup_log
from models.weather import WeatherService
from routers.weather import router as weather_router

setup_log()
app = FastAPI(title="Pepper Weather API", version="1.0.0")
app.include_router(weather_router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
