# AI_Thermal_Tracker — SIH Industrial Fire Detection

AI-powered geospatial platform that detects thermal hotspots via satellite data and classifies them as industrial fires, persistent industrial sources (gas flares), or natural fires (wildfire/agricultural burning) — built for **Smart India Hackathon 2026**.

**Problem Statement ID:** 26162
**Theme:** Disaster Management
**Category:** Software
**Organization:** National Technical Research Organisation (NTRO)

## What it does

Satellite-based fire monitoring tools like NASA FIRMS can tell you *that* something is hot — not *why*. ThermoGuard combines thermal anomaly data with land-infrastructure data to close that gap:

- Pulls real-time thermal hotspots from **NASA FIRMS** (VIIRS)
- Cross-references each hotspot against **OpenStreetMap** industrial infrastructure data
- Classifies each hotspot as a critical industrial fire, a persistent industrial source, or a natural fire
- Visualizes everything on an interactive GIS dashboard with live filtering

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript, Leaflet.js |
| Backend | Python, FastAPI |
| Classification | Scikit-learn (rule-based bootstrap, model training in progress) |
| Data sources | NASA FIRMS API, OpenStreetMap Overpass API |

## Project structure

```
SIH-Industrial-Fire-Detection/
├── frontend/          # Dashboard UI (HTML/CSS/JS + Leaflet map)
├── backend/           # FastAPI server
│   ├── main.py
│   └── services/
│       ├── firms_service.py         # NASA FIRMS data fetching
│       ├── osm_service.py           # OSM industrial infrastructure lookup
│       └── classification_service.py # Hotspot classification logic
├── AI/                # Model training scripts
│   └── models/        # Trained model files
└── README.md
```

## Getting started

### 1. Backend setup

```bash
cd backend
pip install fastapi uvicorn requests python-dotenv
```

Create a `.env` file inside `backend/` with your free NASA FIRMS key ([get one here](https://firms.modaps.eosdis.nasa.gov/api/map_key/)):

```
NASA_FIRMS_MAP_KEY=your_key_here
```

Run the server:

```bash
uvicorn main:app --reload
```

Server runs at `http://127.0.0.1:8000`.

### 2. Frontend setup

Open `frontend/index.html` in a browser (or serve it with VS Code's Live Server extension). No build step required.

## API endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Health check |
| `GET /hotspots?area=&days=` | Raw FIRMS hotspot data |
| `GET /industries?latitude=&longitude=&radius=` | Nearby OSM industrial sites |
| `GET /analyze-hotspot` | Single hotspot, classified |
| `GET /api/hotspots?area=&days=&limit=` | Multiple hotspots, classified — used by the frontend |

**Note:** NASA FIRMS limits `days` to a maximum of 5 per request.

## Team

**Team Name:** IGNISIX

Debobrata Paul(Lead)
Akash Santra
Aditya Das
Aritra Bhattacharjee
Anurag Sen
Sonali Shaw

## References

- Schroeder, W., et al. "The New VIIRS 375m active fire detection data product." *Remote Sensing of Environment* 143 (2014): 85-96.
- NASA Earthdata FIRMS API Documentation — firms.modaps.eosdis.nasa.gov
- OpenStreetMap Overpass API — wiki.openstreetmap.org/wiki/Overpass_API
- Pedregosa, F., et al. "Scikit-learn: Machine Learning in Python." *JMLR* 12 (2011): 2825-2830.