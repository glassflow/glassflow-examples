import boto3
import json
import os
from dotenv import load_dotenv
from faker import Faker
import schedule


class DataGenerator():

    def __init__(self):
        self.fake = Faker()

    def generate_record(self):
        feedback_data = {
            "order_id":
            self.fake.random_int(min=10000, max=99990),
            "customer_id":
            self.fake.random_int(min=1000, max=9999),
            "text":
            "Loved the product! Will definitely recommend to my friends.",
            "order_timestamp":
            self.fake.date_time_between(start_date="-10m",
                                        end_date="now").isoformat(),
        }
        return feedback_data


def send_sqs_message(record_function, sqs, queue_url):
    record = record_function()
    message_body = json.dumps(record)
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    print(f"Message sent to SQS with ID: {response['MessageId']}")


def main():
    # Initialize the SQS client
    queue_url = os.environ['AWS_SQS_QUEUE_URL']
    print("Queue URL: ", queue_url)
    sqs = boto3.client("sqs", region_name=os.environ['AWS_REGION'])
    data_generator = DataGenerator()

    EVENTS_PER_SECOND = 5
    schedule.every(float(1 / EVENTS_PER_SECOND)).seconds.do(
        send_sqs_message, data_generator.generate_record, sqs, queue_url)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    load_dotenv()
    main()
