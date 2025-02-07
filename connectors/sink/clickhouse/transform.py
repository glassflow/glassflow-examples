import json


def handler(data, log):
    log.info("Echo: " + json.dumps(data))
    # expected data for clickhouse sink is a dictionary where each key is a column name and value is the column value
    # Clickhouse accepts only insert
    # event = {"column_name_1": "column_value_1", "column_name_2": "column_value_2"}
    clickhouse_event = {}
    return clickhouse_event
