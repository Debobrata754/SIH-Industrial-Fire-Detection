from fastapi import FastAPI
from services.firms_service import get_hotspots
from services.osm_service import get_nearby_industries

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "SIH 26162 Backend is running!"
    }


@app.get("/hotspots")
def hotspots(
    area: str = "world",
    days: int = 1
):
    data = get_hotspots(
        area=area,
        days=days
    )

    return {
        "source": "NASA FIRMS",
        "area": area,
        "days": days,
        "count": len(data),
        "data": data
    }
@app.get("/industries")
def industries(
    latitude: float,
    longitude: float,
    radius: int = 5000
):
    data = get_nearby_industries(latitude, longitude, radius)

    return {
        "source": "OpenStreetMap",
        "latitude": latitude,
        "longitude": longitude,
        "radius_meters": radius,
        "count": len(data),
        "data": data
    }
@app.get("/hotspot/nearby-industries")
def hotspot_nearby_industries(
    latitude: float,
    longitude: float,
    radius: int = 5000
):
    industries = get_nearby_industries(
        latitude,
        longitude,
        radius
    )

    return {
        "hotspot": {
            "latitude": latitude,
            "longitude": longitude
        },
        "radius_meters": radius,
        "nearby_industries_count": len(industries),
        "nearby_industries": industries
    }
@app.get("/analyze-hotspot")
def analyze_hotspot(
    area: str = "world",
    days: int = 1,
    radius: int = 500
):
    hotspots_data = get_hotspots(
        area=area,
        days=days
    )

    if not hotspots_data:
        return {
            "message": "No hotspots found"
        }

    hotspot = hotspots_data[0]

    latitude = hotspot["latitude"]
    longitude = hotspot["longitude"]

    industries = get_nearby_industries(
        latitude,
        longitude,
        radius
    )

    return {
        "source": "NASA FIRMS + OpenStreetMap",
        "hotspot": hotspot,
        "nearby_industries_count": len(industries),
        "nearby_industries": industries
    }