import boto3
from dotenv import load_dotenv
import os


def create_sqs_queue():
    queue_name = os.environ['SQS_QUEUE_NAME']
    print("Queue NAME: ", queue_name)
    sqs = boto3.client("sqs", region_name=os.environ['AWS_REGION'])

    # Create a SQS queue
    response = sqs.create_queue(QueueName=queue_name,
                                Attributes={
                                    'DelaySeconds': '60',
                                    'MessageRetentionPeriod': '86400'
                                })

    print(response['QueueUrl'])
    return response['QueueUrl']


if __name__ == "__main__":
    load_dotenv()
    create_sqs_queue()
