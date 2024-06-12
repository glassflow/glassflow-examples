import json
import requests


def handler(data, log):
    log.info("Event:" + json.dumps(data), data=data)
    
    enriched_location = enrich_location(data)
    data.update(
        {
            "latitude": enriched_location["latitude"],
            "longitude": enriched_location["longitude"],
            "region": enriched_location["region"],
        }
    )
    return data


def enrich_location(data):
    response = requests.get(
        f"https://api.geoapify.com/v1/geocode/search?text={data['address']}&apiKey=YOUR_API_KEY"
    )
    return response.json()
