import os
import requests
import json
import time
import random
import glassflow
from dotenv import load_dotenv


class SinkConnectorSlack:
    def __init__(self):
        self.slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def setup(self):
        pass

    def put(self, data):
        headers = {"Content-Type": "application/json"}
        payload = {"text": json.dumps(data)}
        response = requests.post(self.slack_webhook_url, headers=headers, json=payload)
        if response.status_code != 200:
            print("Failed to send message to Slack:", response.text)

    def cleanup(self):
        pass


def main():
    sink_connector = SinkConnectorSlack()
    sink_connector.setup()

    pipeline_id = os.environ["PIPELINE_ID"]
    space_id = os.environ["SPACE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]

    # Create GlassFlow client
    pipeline_client = glassflow.GlassFlowClient().pipeline_client(
        space_id=space_id,
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

    retry_delay = 10
    while True:
        try:
            res = pipeline_client.consume()
            if res.status_code == 204:
                # No new events. sleep for a little bit
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the delay for the next attempt
                retry_delay += random.uniform(0, 1)
                continue
            if res.status_code == 200:
                record = res.json()
                print(record)
                sink_connector.put(record)
                print("Consumed transformed event from Glassflow and sent to Slack")
                # set the retry delay back to original
                retry_delay = 10
        except KeyboardInterrupt:
            print("Exiting")
            sink_connector.cleanup()
            break


if __name__ == "__main__":
    load_dotenv()
    main()
