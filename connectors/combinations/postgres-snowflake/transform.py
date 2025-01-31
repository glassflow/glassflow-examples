import json


def handler(data, log):
    log.info("Echo: " + json.dumps(data))
    if data["action"] not in ["I", "D", "U"]:
        return

    event = {}
    if data["action"] == "I":
        event["operation"] = "INSERT"
        event["columns"] = data["columns"]
    elif data["action"] == "D":
        event["operation"] = "DELETE"
        event["filters"] = data["identity"]
    elif data["action"] == "U":
        event["operation"] = "UPDATE"
        event["columns"] = data["columns"]
        event["filters"] = data["identity"]

    event["schema"] = data["schema"]
    event["table"] = data["table"]

    return event 