"""
Source connector to pull data from sqs into glassflow pipeline
"""
import glassflow
import os
import boto3
import json
from dotenv import load_dotenv


# common interface for any source that needs to be implemented
class SourceConnectorSQS:

    def __init__(self) -> None:
        self.sqs_client = None
        self.queue_url = None
        self.setup_source()

    def setup_source(self):
        self.sqs_client = boto3.client("sqs",
                                       region_name=os.environ['AWS_REGION'])
        self.queue_url = os.environ['AWS_SQS_QUEUE_URL']

    def get_next(self):
        while True:
            try:
                messages = self.sqs_client.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=10,
                    WaitTimeSeconds=5)
                if "Messages" in messages:
                    for message in messages["Messages"]:
                        data = json.loads(message["Body"])
                        yield data
                        self.sqs_client.delete_message(
                            QueueUrl=self.queue_url,
                            ReceiptHandle=message["ReceiptHandle"])
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

    def cleanup(self):
        pass


def main():
    # Initalize the glassflow client
    pipeline_id = os.environ["PIPELINE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token)

    # Initialize the SQS client
    source_connector = SourceConnectorSQS()
    for message in source_connector.get_next():
        response = glassflow_client.publish(request_body=message)
        if response.status_code == 200:
            print("Data sent successfully to GlassFlow")
        else:
            print(f"Failed to send data to GlassFlow: {response.text}")


if __name__ == "__main__":
    load_dotenv()
    main()
#
