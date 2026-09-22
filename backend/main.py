import os
import requests
import time
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5500").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def map_weather_code(code):
    if code == 0: return "맑음", "☀️"
    if code in [1, 2, 3]: return "흐림", "☁️"
    if code in [45, 48]: return "안개", "🌫️"
    if 51 <= code <= 67 or 80 <= code <= 82: return "비", "🌧️"
    if 71 <= code <= 77: return "눈", "❄️"
    if 95 <= code <= 99: return "뇌우", "⛈️"
    return "흐림", "☁️"

@app.get("/weather")
def get_weather():
    for attempt in range(3):
        try:
            res = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={"latitude": 37.5665, "longitude": 126.9780, "current": "temperature_2m,weather_code"},
                timeout=8,
            )
            res.raise_for_status()
            data = res.json()["current"]
            condition, icon = map_weather_code(data["weather_code"])
            return {"temp": data["temperature_2m"], "condition": condition, "icon": icon}
        except Exception:
            if attempt < 2:
                time.sleep(1)
    return {"temp": None, "condition": "정보 없음", "icon": "⚠️"}

@app.get("/hobbies")
def get_hobbies():
    return {"hobbies": ["유튜브·영화 시청", "F1 관람", "순대국 맛집 탐방"]}

@app.get("/pick")
def get_pick():
    picks = [
        {"label": "안원잘부", "video": "OrCOflk2QmQ"},
        {"label": "침착맨", "video": "yN_GxazmPT8"},
        {"label": "F1", "video": "EG_QbWsuu9U"},
    ]
    return random.choice(picks)

@app.get("/routine")
def get_routine():
    return {"routine": ["걸으며 노래 듣기", "골프(초보)"]}