"""
Produce sample messages to SQS
"""

import boto3
import json
import random
from faker import Faker
import os
import schedule


class DataGenerator:

    def __init__(self):
        self.fake = Faker()
        self.userid = 0
        self.channelid = 0
        self.genre = ""
        self.lastactive = None
        self.title = ""
        self.watchfrequency = 0
        self.etags = None

    def generate_record(self):
        data = {
            "event_id":
            self.fake.uuid4(),
            "userid":
            self.fake.uuid4(),
            "channelid":
            self.fake.pyint(min_value=1, max_value=50),
            "genre":
            random.choice(["thriller", "comedy", "romcom", "fiction"]),
            "lastactive":
            self.fake.date_time_between(start_date="-10m",
                                        end_date="now").isoformat(),
            "title":
            self.fake.name(),
            "watchfrequency":
            self.fake.pyint(min_value=1, max_value=10),
        }
        return data


def send_sqs_message(record_function, sqs, queue_url):
    record = record_function()
    event_id = record.get('event_id')
    message_body = json.dumps(record)
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    print(
        f"Message sent to SQS with ID: {response['MessageId']} and event_id {event_id}"
    )


def main():
    # Initialize the SQS client
    queue_url = os.environ['SQS_QUEUE_URL']
    print("Queue URL: ", queue_url)
    sqs = boto3.client("sqs", region_name=os.environ['AWS_REGION'])
    data_generator = DataGenerator()

    EVENTS_PER_SECOND = 5
    schedule.every(float(1 / EVENTS_PER_SECOND)).seconds.do(
        send_sqs_message, data_generator.generate_record, sqs, queue_url)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
