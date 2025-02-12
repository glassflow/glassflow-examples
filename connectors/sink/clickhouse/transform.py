import json


def handler(data, log):
    log.info("Echo: " + json.dumps(data))
    # expected data for clickhouse sink is a dictionary where each key is a column name and value is the column value
    # Clickhouse accepts only insert
    # event = {"column_name_1": "column_value_1", "column_name_2": "column_value_2"}
    # details on clickhouse docs at https://www.glassflow.dev/docs/integrations/sinks/clickhouse
    clickhouse_event = {}
    return clickhouse_event
