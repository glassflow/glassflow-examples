import json


def handler(data, log):
    log.info("Event:" + json.dumps(data), data=data)

    if data["watchfrequency"] == 1:
        data["reaction"] = "dislike"
    elif data["watchfrequency"] > 5:
        data["reaction"] = "favourite"
    else:
        data["reaction"] = "like"

    return data
