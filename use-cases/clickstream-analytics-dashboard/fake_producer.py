from dotenv import load_dotenv
import schedule
from faker import Faker
import glassflow
import os
import random


class DataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_record(self):
        data = {
            "activeUsers": str(random.randint(0, 10)),
            "city": self.fake.city(),
            "country": self.fake.country(),
            "deviceCategory": random.choice(["desktop", "mobile", "tablet"]),
            "eventCount": str(random.randint(1, 20)),
            "screenPageViews": str(random.randint(1, 10)),
            "unifiedScreenName": random.choice(
                ["Home", "Product", "About", "Contact", "Manage pipeline"]
            ),
        }
        return data


def send_message_to_glassflow(record_function, glassflow_client):
    record = record_function()
    response = glassflow_client.publish(request_body=record)
    if response.status_code == 200:
        print("Message sent to GlassFlow:", record)
    else:
        print(f"Failed to send data to GlassFlow: {response.text}")


def main():
    # Initialize GlassFlow client
    pipeline_id = os.environ["PIPELINE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

    # Initialize data generator
    data_generator = DataGenerator()

    # Schedule message sending to GlassFlow
    EVENTS_PER_SECOND = 5
    schedule.every(float(1 / EVENTS_PER_SECOND)).seconds.do(
        send_message_to_glassflow, data_generator.generate_record, glassflow_client
    )

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    load_dotenv()
    main()
