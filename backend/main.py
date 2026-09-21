import os
import requests
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5500").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    res = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": 37.5665, "longitude": 126.9780, "current": "temperature_2m,weather_code"},
    )
    data = res.json()["current"]
    condition, icon = map_weather_code(data["weather_code"])
    return {"temp": data["temperature_2m"], "condition": condition, "icon": icon}

@app.get("/hobbies")
def get_hobbies():
    return {"hobbies": ["유튜브·영화 시청", "F1 관람", "순대국 맛집 탐방"]}

@app.get("/routine")
def get_routine():
    return {"routine": ["걸으며 노래 듣기", "골프(초보)"]}

@app.post("/guestbook")
def add_message(name: str, content: str, db: Session = Depends(get_db)):
    msg = models.Message(name=name, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return {"id": msg.id, "name": msg.name, "content": msg.content}

@app.get("/guestbook")
def list_messages(db: Session = Depends(get_db)):
    rows = db.query(models.Message).all()
    return [{"id": r.id, "name": r.name, "content": r.content} for r in rows]