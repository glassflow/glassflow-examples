import boto3
import json
from dotenv import dotenv_values

# Initialize the SQS client
sqs = boto3.client("sqs")
config = dotenv_values(".env")
queue_url = config.get("QUEUE_URL")

# Sample customer feedback data
feedback_data = {
    "order_id": "123456",
    "customer_id": "78910",
    "text": "Loved the product! Will definitely recommend to my friends.",
    "order_timestamp": "2024-01-01T12:00:00Z",
}

# Convert the feedback data to a JSON string
message_body = json.dumps(feedback_data)

# Send the message to the SQS queue
response = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)

# Print the message ID of the sent message
print(f"Message sent to SQS with ID: {response['MessageId']}")
