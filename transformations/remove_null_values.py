import json


def handler(data, log):
    log.info("Event:" + json.dumps(data), data=data)

    cleaned_data = {k: v for k, v in data.items() if v is not None}

    return cleaned_data
