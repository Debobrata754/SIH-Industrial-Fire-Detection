import os
import csv
from io import StringIO

import requests
from dotenv import load_dotenv

load_dotenv()

MAP_KEY = os.getenv("NASA_FIRMS_MAP_KEY")

BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"


def get_hotspots(
    source: str = "VIIRS_SNPP_NRT",
    area: str = "world",
    days: int = 1
):
    url = f"{BASE_URL}/{MAP_KEY}/{source}/{area}/{days}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    csv_data = StringIO(response.text)
    reader = csv.DictReader(csv_data)

    hotspots = []

    for row in reader:
        hotspot = {
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "brightness": float(row["bright_ti4"]),
            "confidence": row["confidence"],
            "frp": float(row["frp"]),
            "acq_date": row["acq_date"],
            "acq_time": row["acq_time"],
            "satellite": row["satellite"],
            "instrument": row["instrument"]
        }

        hotspots.append(hotspot)

    return hotspots