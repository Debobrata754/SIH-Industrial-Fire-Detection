import requests


OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def get_nearby_industries(latitude, longitude, radius=5000):

    query = f"""
    [out:json][timeout:30];
    node["industrial"](around:{radius},{latitude},{longitude});
    out center;
    """

    response = requests.post(
        OVERPASS_URL,
        data={"data": query},
        headers={
            "User-Agent": "SIH-Industrial-Fire-Detection/1.0"
        },
        timeout=45
    )

    if response.status_code != 200:
        raise Exception(
            f"Overpass API error: HTTP {response.status_code}"
        )

    data = response.json()

    industries = []

    for element in data.get("elements", []):

        if element["type"] == "node":
            lat = element.get("lat")
            lon = element.get("lon")
        else:
            center = element.get("center", {})
            lat = center.get("lat")
            lon = center.get("lon")

        tags = element.get("tags", {})

        industries.append({
            "name": tags.get("name", "Unknown"),
            "type": tags.get("industrial", "Unknown"),
            "latitude": lat,
            "longitude": lon
        })

    return industries