import requests
from math import radians, sin, cos, sqrt, atan2


OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    delta_lat = lat2 - lat1
    delta_lon = radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def get_nearby_industries(latitude, longitude, radius=1000):

    query = f"""
[out:json][timeout:20];
(
    nwr["industrial"](around:{radius},{latitude},{longitude});
    nwr["landuse"="industrial"](around:{radius},{latitude},{longitude});
);
out center;
"""

    response = None

    for overpass_url in OVERPASS_URLS:

        try:
            response = requests.post(
                overpass_url,
                data={"data": query},
                headers={
                    "User-Agent": "SIH-Industrial-Fire-Detection/1.0"
                },
                timeout=30
            )

            if response.status_code == 200:
                break

        except requests.RequestException:
            continue

    if response is None or response.status_code != 200:
     return [] 
    data = response.json()

    industries = []

    for element in data.get("elements", []):

        tags = element.get("tags", {})

        if element["type"] == "node":

            lat = element.get("lat")
            lon = element.get("lon")

        else:

            center = element.get("center", {})

            lat = center.get("lat")
            lon = center.get("lon")

        if lat is None or lon is None:
            continue

        distance = calculate_distance(
            latitude,
            longitude,
            lat,
            lon
        )

        industries.append({
            "name": tags.get("name", "Unknown"),
            "type": tags.get("industrial", "Unknown"),
            "latitude": lat,
            "longitude": lon,
            "distance_meters": round(distance, 2)
        })

    industries.sort(
        key=lambda x: x["distance_meters"]
    )

    return industries