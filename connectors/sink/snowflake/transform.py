import json


def handler(data, log):
    log.info("Echo: " + json.dumps(data))

    return data
