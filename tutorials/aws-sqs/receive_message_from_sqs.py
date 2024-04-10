import boto3
import json
from glassflow import GlassFlowClient

from dotenv import dotenv_values

config = dotenv_values(".env")

# Initialize the SQS client
sqs = boto3.client("sqs")
queue_url = config.get("QUEUE_URL")

# Initialize the GlassFlow client
glassflow_client = GlassFlowClient()
pipeline_id = config.get("PIPELINE_ID")
space_id = config.get("SPACE_ID")
token = config.get("PIPELINE_ACCESS_TOKEN")

pipeline_client = glassflow_client.pipeline_client(space_id=space_id,
                                                   pipeline_id=pipeline_id,
                                                   pipeline_access_token=token)


def send_to_glassflow(message):
    data = json.loads(message["Body"])
    print(f"Received message: {data}")

    try:
        # Publish the data to the GlassFlow pipeline
        response = pipeline_client.publish(request_body=data)
        if response.status_code == 200:
            print("Data sent successfully to GlassFlow.")
        else:
            print(f"Failed to send data to GlassFlow: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")


def retrieve_sqs_messages():
    while True:
        messages = sqs.receive_message(
            QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=5
        )
        if "Messages" in messages:
            for message in messages["Messages"]:
                send_to_glassflow(message)
                sqs.delete_message(
                    QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
                )


if __name__ == "__main__":
    retrieve_sqs_messages()
