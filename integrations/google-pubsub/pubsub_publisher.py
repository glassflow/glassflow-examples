from google.cloud import pubsub_v1
import json
from dotenv import dotenv_values

config = dotenv_values(".env")
project_id = config.get("PROJECT_ID")
topic_id = config.get("TOPIC_ID")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

order_data = {
    "order_id": "12345",
    "product_id": "67890",
    "quantity": 2,
    "order_timestamp": "2024-01-01T12:00:00Z",
}

future = publisher.publish(topic_path, data=json.dumps(order_data).encode("utf-8"))

print(f"Published message ID: {future.result()}")
