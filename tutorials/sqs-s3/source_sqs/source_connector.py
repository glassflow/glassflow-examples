"""
Source connector to pull data from sqs into glassflow pipeline
"""
import glassflow
import os
import boto3
import json


def get_sqs_messages():
    sqs = boto3.client("sqs", region_name=os.environ['AWS_REGION'])
    queue_url = os.environ['SQS_QUEUE_URL']

    while True:
        try:
            messages = sqs.receive_message(QueueUrl=queue_url,
                                           MaxNumberOfMessages=10,
                                           WaitTimeSeconds=5)
            if "Messages" in messages:
                for message in messages["Messages"]:
                    data = json.loads(message["Body"])
                    yield data
                    sqs.delete_message(QueueUrl=queue_url,
                                       ReceiptHandle=message["ReceiptHandle"])
        except Exception as e:
            print(f"An error occurred: {e}")
            continue


def main():
    # Initalize the glassflow client
    pipeline_id = os.environ["PIPELINE_ID"]
    space_id = os.environ["SPACE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        space_id=space_id,
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token)

    # Initialize the SQS client
    queue_url = os.environ["SQS_QUEUE_URL"]
    print("Queue URL: ", queue_url)
    for message in get_sqs_messages():
        event_id = message.get("event_id")
        response = glassflow_client.publish(request_body=message)
        if response.status_code == 200:
            print("Data sent successfully to GlassFlow with event_id: ",
                  event_id)
        else:
            print(f"Failed to send data to GlassFlow: {response.text}")


if __name__ == "__main__":
    main()
#
