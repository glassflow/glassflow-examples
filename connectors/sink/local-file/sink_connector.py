"""
Consume data from glassflow to local file
"""
import os
from dotenv import load_dotenv
import glassflow
import time
import random
import json


class SinkConnectorFile():

    def __init__(self) -> None:
        self.filename = os.environ.get("SINK_FILE_PATH", "glassflow_sink.txt")
        self.file = None

    def setup(self):
        self.file = open(self.filename, "a+")

    def put(self, data):
        self.file.write(json.dumps(data) + "\n")
        self.file.flush()

    def cleanup(self):
        self.file.close()


def main():
    pipeline_id = os.environ["PIPELINE_ID"]
    space_id = os.environ["SPACE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]
    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(
        space_id=space_id,
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token)

    sink_connector = SinkConnectorFile()
    sink_connector.setup()

    retry_delay = 10
    while True:
        try:
            res = pipeline_client.consume()
            if res.status_code == 204:
                # No new events. sleep for a little bit
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the delay for the next attempt
                retry_delay += random.uniform(0, 1)  # Add jitter
                continue
            if res.status_code == 200:
                record = res.json()
                sink_connector.put(record)
                # set the retry delay back to original
                retry_delay = 10
        except KeyboardInterrupt:
            print("Exiting")
            sink_connector.cleanup()
            break


if __name__ == "__main__":
    load_dotenv()
    main()
