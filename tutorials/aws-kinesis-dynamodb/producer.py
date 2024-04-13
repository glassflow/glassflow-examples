import json
import random
import boto3
from faker import Faker
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import time
import os

load_dotenv()
stream_name = os.getenv("KINESIS_STREAM_NAME")
region = os.getenv("REGION")


class RecordGenerator:
    def __init__(self):
        self.userid = 0
        self.channelid = 0
        self.genre = ""
        self.lastactive = None
        self.title = ""
        self.watchfrequency = 0
        self.etags = None

    def generate_netflix_record(self, fake):
        netflix_data = {
            "userid": fake.uuid4(),
            "channelid": fake.pyint(min_value=1, max_value=50),
            "genre": random.choice(["thriller", "comedy", "romcom", "fiction"]),
            "lastactive": fake.date_time_between(
                start_date="-10m", end_date="now"
            ).isoformat(),
            "title": fake.name(),
            "watchfrequency": fake.pyint(min_value=1, max_value=10),
            "etags": fake.uuid4(),
        }
        data = json.dumps(netflix_data)
        print(f"Sending record to Kinesis stream: '{data}'")
        return {"Data": bytes(data, "utf-8"), "PartitionKey": "partition_key"}

    def generate_netflix_records(self, rate, fake):
        return [self.generate_netflix_record(fake) for _ in range(rate)]


class KinesisStream:
    """Encapsulates a Kinesis stream."""

    def __init__(self, kinesis_client):
        self.kinesis_client = kinesis_client
        self.stream_exists_waiter = kinesis_client.get_waiter("stream_exists")

    def create_stream(self, name):
        try:
            self.kinesis_client.create_stream(StreamName=name, ShardCount=1)
            print("Created stream {}.".format(name))
            self.stream_exists_waiter.wait(StreamName=name)
            self.describe_stream(name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceInUseException":
                print("Stream '{}' already exists.".format(name))
            else:
                print("Couldn't create stream {}.".format(name))
                raise

    def describe_stream(self, name):
        try:
            response = self.kinesis_client.describe_stream(StreamName=name)
            stream_details = response["StreamDescription"]
            print("Stream details: {}".format(stream_details))
        except ClientError as e:
            print("Couldn't describe stream {}.".format(name))
            raise


def main():
    try:
        fake = Faker()
        kinesis_client = boto3.client("kinesis", region)
        stream_manager = KinesisStream(kinesis_client)
        rate = 200  # rate at which data is generated

        # Create Kinesis Stream if it doesn't exist
        if stream_name:
            stream_manager.create_stream(stream_name)

        generator = RecordGenerator()

        # Generate and stream data
        while True:
            fake_data = generator.generate_netflix_records(rate, fake)
            kinesis_client.put_records(StreamName=stream_name, Records=fake_data)
            time.sleep(30)  # Generate record every 30 seconds
    except Exception as e:
        print("Error:", e)
        raise


if __name__ == "__main__":
    main()
