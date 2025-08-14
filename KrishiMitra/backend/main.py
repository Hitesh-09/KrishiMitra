
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from langdetect import detect
import pandas as pd
import os, json

app = FastAPI(title="KrishiMitra MVP API", version="0.1.0")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Load demo datasets into memory
weather_df = pd.read_csv(os.path.join(DATA_DIR, "weather_sample.csv"))
market_df = pd.read_csv(os.path.join(DATA_DIR, "market_prices_sample.csv"))
with open(os.path.join(DATA_DIR, "schemes_sample.json"), "r", encoding="utf-8") as fh:
    schemes_data = json.load(fh)
soil_df = pd.read_csv(os.path.join(DATA_DIR, "soil_sample.csv"))

class AskRequest(BaseModel):
    query: str
    language: Optional[str] = None  # 'en', 'hi', etc.
    pincode: Optional[str] = None
    crop: Optional[str] = None

class AgentResponse(BaseModel):
    answer: str
    language: str
    reasoning: List[str]
    sources: List[str]
    data: Dict[str, Any]

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "en"

def get_weather(pincode: Optional[str]) -> Dict[str, Any]:
    if pincode and pincode in set(weather_df["pincode"].astype(str)):
        row = weather_df[weather_df["pincode"].astype(str) == str(pincode)].iloc[0].to_dict()
    else:
        row = weather_df.iloc[0].to_dict()
    return row

def get_market(crop: Optional[str], district: Optional[str]) -> Dict[str, Any]:
    df = market_df.copy()
    if crop:
        df = df[df["crop"].str.lower() == crop.lower()]
    if df.empty:
        row = market_df.iloc[0].to_dict()
    else:
        row = df.sort_values("avg_price_rs_per_kg", ascending=False).iloc[0].to_dict()
    return row

def get_soil(pincode: Optional[str]) -> Dict[str, Any]:
    df = soil_df.copy()
    if pincode and pincode in set(df["pincode"].astype(str)):
        row = df[df["pincode"].astype(str) == str(pincode)].iloc[0].to_dict()
    else:
        row = df.iloc[0].to_dict()
    return row

def get_schemes(crop: Optional[str]) -> List[Dict[str, Any]]:
    # Return top 2 schemes; in real app, filter by crop/state
    return schemes_data[:2]

@app.post("/ask", response_model=AgentResponse)
def ask_agent(req: AskRequest):
    lang = req.language or detect_language(req.query)

    reasoning = []
    sources = [
        "Demo: IMD (weather)",
        "Demo: Agmarknet/eNAM (market prices)",
        "Demo: Soil Health Card (soil)",
        "Demo: MyGov/PM-Kisan (schemes)"
    ]

    # Simple intent detection
    q = req.query.lower()
    weather_info = market_info = soil_info = None

    if any(k in q for k in ["rain", "barish", "weather", "mosam", "temperature"]):
        weather_info = get_weather(req.pincode)
        reasoning.append("Checked local 7-day forecast for pincode.")

    if any(k in q for k in ["price", "daam", "market", "mandi"]) or req.crop:
        market_info = get_market(req.crop, None)
        reasoning.append("Fetched recent district-level market prices for the crop.")

    if any(k in q for k in ["soil", "npk", "ph"]) or req.pincode:
        soil_info = get_soil(req.pincode)
        reasoning.append("Retrieved soil health indicators from last survey.")

    top_schemes = get_schemes(req.crop)
    reasoning.append("Matched relevant central schemes and subsidies.")

    # Compose answer (very simple template logic for MVP)
    parts = []
    if weather_info:
        parts.append(f"Weather: {weather_info['forecast_summary']} | Rain chance next 7 days: {weather_info['rain_prob_pct']}% | Temp range: {weather_info['temp_min_c']}–{weather_info['temp_max_c']}°C.")
    if soil_info:
        parts.append(f"Soil: pH {soil_info['ph']}, N {soil_info['nitrogen']}, P {soil_info['phosphorus']}, K {soil_info['potassium']}. Recommended crop: {soil_info['recommended_crop']}.")
    if market_info:
        parts.append(f"Market: Avg price for {market_info['crop']} is ₹{market_info['avg_price_rs_per_kg']}/kg (mandi: {market_info['mandi']}).")
    if top_schemes:
        schemes_txt = "; ".join([s['name'] for s in top_schemes])
        parts.append(f"Schemes: {schemes_txt}.")

    if not parts:
        parts.append("I can help with weather, soil health, market prices, and schemes. Try asking: 'Agle hafte barish hogi? (pincode 110001)' or 'Bhindi ke daam kya hain?'")

    answer = " ".join(parts)

    return AgentResponse(
        answer=answer,
        language=lang,
        reasoning=reasoning,
        sources=sources,
        data={
            "weather": weather_info,
            "soil": soil_info,
            "market": market_info,
            "schemes": top_schemes
        }
    )

@app.get("/health")
def health():
    return {"status": "ok"}
