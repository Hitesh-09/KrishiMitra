
# KrishiMitra – Offline-First Multilingual AI Farm Advisor (MVP)

This is a hackathon-ready minimal MVP for the Capital One Launchpad submission.

## What it does
- Accepts a farmer's question (voice/text planned; text demo provided)
- Performs simple "agentic" steps: check weather, soil, market prices, and schemes (demo data)
- Returns an answer with reasoning steps and example sources

## Repo structure
```
KrishiMitra/
  backend/
    main.py
    requirements.txt
  frontend/
    index.html
  data/
    weather_sample.csv
    market_prices_sample.csv
    soil_sample.csv
    schemes_sample.json
```

## Run locally (Backend)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API will be available at `http://127.0.0.1:8000`

## Open the demo (Frontend)
Open `frontend/index.html` in your browser. Ensure the backend is running locally on port 8000.

## Example queries
- "Agle hafte barish hogi kya? pincode 110001"
- "Bhindi ke daam kya hain?"
- "Soil report for 110001?"
- "Which schemes apply to paddy?"

## Notes
- This MVP uses small demo datasets (CSV/JSON) to simulate public data sources (IMD, Agmarknet/eNAM, Soil Health Card, ICAR, MyGov). Replace with real datasets/APIs for production.
- For multilingual support, integrate STT (e.g., Whisper) and TTS, and add proper translation/routing.
- For true offline-first, bundle datasets and run the API on-device; add periodic sync logic.
