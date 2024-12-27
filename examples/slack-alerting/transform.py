"""
Input:
    {"event_name": "user_login", "username": "","ip": "", "email": "", "known_ip: false, etc.}

Transform:
    - If "known_ip" is False, then send an alert, otherwise send empty message
    - Format message
    - Enrich message with new IP city and country

Output:
    Slack formatted message
"""
import os
import requests


GEOAPI_KEY = os.getenv("GEOAPI_KEY")


def handler(data, log):
    if data["known_ip"]:
        log.debug("User Login from known IP")
        message = {}
    else:
        log.debug("User Login from unknown IP")
        location = get_ip_location(ip=data["ip"], log=log)
        message = format_message(data, location)
    return message


def get_ip_location(ip, log):
    try:
        response = requests.get(
            f"https://api.geoapify.com/v1/ipinfo?ip={ip}&apiKey={GEOAPI_KEY}"
        )
        response_data = response.json()
        response.raise_for_status()
    except Exception as e:
        log.error(e)
        raise e

    city = ""
    if response_data and "city" in response_data:
        city = response_data["city"]["name"]

    country = ""
    if response_data and "country" in response_data:
        country = response_data["country"]["name"]

    return f"{city}, {country}"


def format_message(data, location):
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Suspicious Login",
                    "emoji": True
                },
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Username:*\n{data['username']}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Login location:*\n{location}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Device IP:*\n{data['ip']}",
                    }
                ],
            }
        ]
    }
