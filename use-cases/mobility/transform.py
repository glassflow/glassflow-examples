"""
Transform function by the user
"""
import json
import requests


def handler(data, log):
    log.info("Event:" + json.dumps(data), data=data)
    try:
        transformed = handle(data)
    except Exception as e:
        log.error("Error in transformation", error=str(e))
        raise e
    return transformed


def get_nearest_fuel_station(gps_cordinates, fuel_type):
    print("get nearest fuel station")
    url = "https://mock-mobility-585858172927.europe-west3.run.app/mobility/gas-stations/nearest"
    resp = requests.get(url,
                        params={
                            'cordinates_lat': gps_cordinates[0],
                            'cordinates_long': gps_cordinates[1],
                            'fuel_type': fuel_type
                        })
    if resp.status_code == 200:
        fuel_station = resp.json()
        print(fuel_station)
        return fuel_station
    else:
        print("error getting nearest fuel station")
        print(resp.status_code)
        return None


def handle(data: json):
    data['discount'] = {"discount": False}
    if not data['is_electric'] and data['current_fuel_percentage'] < 25:
        # find nearest gas station using a partner API
        fuel_station = get_nearest_fuel_station(data['gps_cordinates'],
                                                data['fuel_type'])
        if fuel_station:
            data['discount'] = {
                "discount": True,
                "fuel_station": fuel_station,
                "discount_type": "fuel"
            }

    return data
