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
        car_data = {
            "id": self.fake.uuid4(),
            "model": self.fake.word(),
            "year": self.fake.year(),
            "price": self.fake.random_int(min=10000, max=50000),
            "transmission": random.choice(["manual", "automatic"]),
            "mileage": self.fake.random_int(min=0, max=200000),
            "fuelType": random.choice(["petrol", "diesel", "electric", "hybrid"]),
            "tax": self.fake.random_int(min=0, max=500),
            "mpg": self.fake.random_int(min=10, max=60),
            "engineSize": round(random.uniform(1.0, 5.0), 1)
        }
        return car_data


def send_message_to_glassflow(record_function, glassflow_client):
    record = record_function()

    # 3. Publishes a new event into the pipeline
    response = glassflow_client.publish(request_body=record)
    if response.status_code == 200:
        print("Message sent to GlassFlow:", record)
    else:
        print(f"Failed to send data to GlassFlow: {response.text}")


def main():
    pipeline_id = os.environ["PIPELINE_ID"]
    token = os.environ["PIPELINE_ACCESS_TOKEN"]

    # 1. Initializes a GlassFlow Python client
    client = glassflow.GlassFlowClient()

    # 2. Creates a pipeline
    pipeline_client = client.pipeline_client(
        pipeline_id=pipeline_id, pipeline_access_token=token
    )

    data_generator = DataGenerator()

    EVENTS_PER_SECOND = 5
    schedule.every(float(1 / EVENTS_PER_SECOND)).seconds.do(
        send_message_to_glassflow, data_generator.generate_record, pipeline_client
    )

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    load_dotenv()
    main()
