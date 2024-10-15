import json
import requests
import os


def handler(data, log):
    key = os.getenv("GEOAPI_KEY")
    log.info("Event received: " + json.dumps(data))

    enriched_location = enrich_location(key, data)
    data.update(
        {
            "latitude": enriched_location["lat"],
            "longitude": enriched_location["lon"],
            "postcode": enriched_location["postcode"],
        }
    )
    return data


def enrich_location(key, data):
    response = requests.get(
        f"https://api.geoapify.com/v1/geocode/search?text={data['address']}&apiKey={key}"
    )
    response_data = response.json()
    if (
        response_data
        and "features" in response_data
        and len(response_data["features"]) > 0
    ):
        location_data = response_data["features"][0]["properties"]
        return {
            "lat": location_data.get("lat"),
            "lon": location_data.get("lon"),
            "postcode": location_data.get("postcode"),
        }
    return {"lat": None, "lon": None, "postcode": None}