# JANSAHAY — AI Community Issue Intelligence

**From citizen complaints to actionable priorities for a better tomorrow.**

JANSAHAY is a civic-tech MVP that turns citizen reports into structured, explainable priorities for local authorities. Citizens can submit **photo, voice, text and location**; Gemini can analyze the report, Google Maps can visualize issues, and the authority dashboard can prioritize, assign and track resolution.

> **Important:** This repository contains a working MVP with a local demo mode. Google Cloud integrations are enabled through environment variables. No API keys or private credentials are included in this repository.

## Core workflow

**REPORT → UNDERSTAND → STRUCTURE → MAP → PRIORITISE → ACT**

1. Citizen submits an issue.
2. Gemini multimodal analysis extracts issue type, category, severity, context, location and recommended action.
3. The application stores the structured issue.
4. Google Maps visualizes issue locations and hotspots.
5. The priority engine ranks issues using severity, report volume, impact, recency and recurrence.
6. Authorities assign departments and track `Assigned → In Progress → Resolved`.

## Google technologies

- **Gemini API / Google AI Studio** — multimodal understanding, classification, summarization and recommendations.
- **Google Maps Platform** — location visualization and issue hotspots.
- **Firebase** — supported integration path for authentication and real-time data.
- **BigQuery** — supported analytics path for historical complaint trends and hotspot analysis.
- **Google Cloud** — deployment/scaling foundation.

## MVP features

- Citizen issue reporting
- Text + location input
- Optional image analysis with Gemini
- AI classification
- Explainable priority scoring
- Issue map
- Authority priority queue
- Department assignment
- Status tracking
- Demo/sample dataset
- BigQuery-ready analytics query
- Firebase integration configuration template

## Run locally

### 1. Install

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure

Copy `.env.example` to `.env`.

For demo mode you can leave `GEMINI_API_KEY` empty. The application will use deterministic demo analysis.

For real Gemini analysis:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

For Google Maps:

```env
GOOGLE_MAPS_API_KEY=your_key_here
```

### 3. Start

```bash
python app.py
```

Open:

`http://127.0.0.1:5000`

## Demo mode

The app works without cloud credentials using sample civic issues. This is useful for a hackathon demo while keeping secrets out of GitHub.

Demo data is clearly labelled as sample/demo data and should not be presented as real Chandigarh statistics.

## Project structure

```text
JANSAHAY/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
├── data/
│   └── demo_issues.json
├── analytics/
│   ├── priority_engine.py
│   └── bigquery_schema.sql
├── gemini/
│   └── analyzer.py
├── firebase/
│   ├── firebase_config.example.js
│   └── FIREBASE_SETUP.md
├── docs/
│   └── ARCHITECTURE.md
└── screenshots/
    └── .gitkeep
```

## Human-in-the-loop

JANSAHAY is a **decision-support system**:

> **AI recommends. Humans decide. Departments act.**

AI output is not treated as an automatic government decision. A responsible authority reviews the recommendation before taking action.

## Security

Never commit `.env`, API keys, Firebase service-account JSON, Google Cloud credential files, passwords or tokens.

## Future roadmap

### Phase 1 — MVP
Gemini + Maps + local/Firebase-backed reporting.

### Phase 2 — Intelligence
BigQuery analytics, recurring hotspots and trend analysis.

### Phase 3 — Scale
Multilingual and voice-first reporting.

### Phase 4 — Integrate
Municipal systems and public datasets.
