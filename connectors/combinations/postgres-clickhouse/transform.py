import json

def handler(data, log):
    log.info("Echo: " + json.dumps(data))
    # Clickhouse accepts only insert 
    if data["action"] not in ["I"]:
        return {}

    # Transform data from postgres cdc format to clickhouse
    # expected data for clickhouse sink is a dictionary where each key is a column name and value is the column value
    event = {}
    for item in data["columns"]:
        key = item["name"]
        value = item["value"]
        event[key] = value

    return event