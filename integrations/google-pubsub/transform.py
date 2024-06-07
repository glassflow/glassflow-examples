import json
from datetime import datetime, timedelta


def handler(data, log):
    log.info("Event:" + json.dumps(data), data=data)

    order_timestamp = datetime.strptime(data["order_timestamp"], "%Y-%m-%dT%H:%M:%SZ")
    # Assume delivery takes 3 days
    estimated_delivery = order_timestamp + timedelta(days=3)
    data["estimated_delivery"] = estimated_delivery.strftime("%Y-%m-%d")
    return data
