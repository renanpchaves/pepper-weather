from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.logging import setup_log
from backend.routers.weather import router as weather_router

setup_log()
app = FastAPI(title="Pepper Weather API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
