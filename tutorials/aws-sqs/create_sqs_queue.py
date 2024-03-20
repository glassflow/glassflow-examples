import boto3
from dotenv import dotenv_values

config = dotenv_values(".env")
queue_name = config.get("QUEUE_NAME")

# Create SQS client
sqs = boto3.client('sqs')

# Create a SQS queue
response = sqs.create_queue(
    QueueName=queue_name,
    Attributes={
        'DelaySeconds': '60',
        'MessageRetentionPeriod': '86400'
    }
)

print(response['QueueUrl'])