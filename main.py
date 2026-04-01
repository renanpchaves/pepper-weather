from fastapi import FastAPI
from services.weather import get_weather
from core.logging import setup_log

setup_log()
app = FastAPI(title="Pepper Weather API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import json

    data = get_weather("Rio de Janeiro")
    print(json.dumps(data, indent=2, ensure_ascii=False))
