# producer.py

import glassflow
from dotenv import dotenv_values
import datetime
import random


def random_event_json(event_number=1):
    return {
        "product_id": 1000 + event_number,
        "product_name": random.choice(
            [
                "Blue T-Shirt",
                "Black Jeans",
                "Running Shoes",
                "Baseball Caps",
                "Socks",
                "Leather Belts",
                "Wallets",
                "Sunglasses",
            ]
        ),
        "quantity": random.randint(20, 500),
        "unit": random.choice(["kg", "pounds"]),
        "supplier_id": random.choice(
            ["supplier1", "supplier2", "supplier3", "supplier4", "supplier5"]
        ),
        "created_at": datetime.datetime.now().isoformat(),
    }


def send_data_to_pipeline():
    config = dotenv_values(".env")
    pipeline_id = config.get("PIPELINE_ID")
    space_id = config.get("SPACE_ID")
    token = config.get("PIPELINE_ACCESS_TOKEN")

    client = glassflow.GlassFlowClient()
    pipeline_client = client.pipeline_client(
        space_id=space_id, pipeline_id=pipeline_id, pipeline_access_token=token
    )

    counter = 0
    try:
        while True and counter < 1000:
            # Create a random event
            event = random_event_json(counter)
            counter += 1
            try:
                res = pipeline_client.publish(request_body=event)
                if res.status_code == 200:
                    print("Event published successfully")
                    print(event)
            except Exception as e:
                print("Error in publishing event")
                print(e)
    except KeyboardInterrupt:
        print("Exiting ")


if __name__ == "__main__":
    send_data_to_pipeline()
