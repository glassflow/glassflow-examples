import os
import requests
import json
import time
import random
import glassflow
from dotenv import load_dotenv


class SinkConnectorSlack:
    def __init__(self):
        load_dotenv()
        self.slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        self.pipeline_id = os.getenv("PIPELINE_ID")
        self.pipeline_access_token = os.getenv("PIPELINE_ACCESS_TOKEN")
        self.pipeline_client = glassflow.GlassFlowClient().pipeline_client(
            pipeline_id=self.pipeline_id,
            pipeline_access_token=self.pipeline_access_token,
        )

    def send_to_slack(self, data):
        headers = {"Content-Type": "application/json"}
        payload = {"text": json.dumps(data)}
        response = requests.post(
            self.slack_webhook_url,
            headers=headers,
            json=payload,
        )
        if response.status_code != 200:
            print(
                "Failed to send message to Slack:",
                response.text,
            )

    def run(self):
        retry_delay = 10
        try:
            while True:
                # Consume transformed event from the pipeline
                res = self.pipeline_client.consume()

                if res.status_code == 204:
                    time.sleep(retry_delay)
                    retry_delay = min(
                        retry_delay * 2 + random.uniform(0, 1),
                        60,
                    )  # Cap delay to 60 seconds
                    continue
                if res.status_code == 200:
                    record = res.json()
                    print(record)
                    self.send_to_slack(record)

                    print(
                        "Consumed transformed event from Glassflow" "and sent to Slack"
                    )
                    # Reset the delay after successful processing
                    retry_delay = 10
        except KeyboardInterrupt:
            print("Exiting...")


if __name__ == "__main__":
    SinkConnectorSlack().run()
