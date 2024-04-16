import json
import random
import boto3
from faker import Faker
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import time
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
            "etags":
            self.fake.uuid4(),
        }
        return data


def create_kinesis_stream(kinesis_client, stream_name):
    try:
        kinesis_client.create_stream(StreamName=stream_name, ShardCount=1)
        print("Created stream {}.".format(stream_name))
        stream_exists_waiter = kinesis_client.get_waiter("stream_exists")
        stream_exists_waiter.wait(StreamName=stream_name)
        response = kinesis_client.describe_stream(StreamName=stream_name)
        stream_details = response["StreamDescription"]
        print("Stream details: {}".format(stream_details))
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print("Stream '{}' already exists.".format(stream_name))
        else:
            print("Couldn't create stream {}.".format(stream_name))
            raise


def send_kinesis_record(kinesis_client, stream_name, record_generator):
    kinesis_record = [{
        "Data": bytes(json.dumps(record_generator()), "utf-8"),
        "PartitionKey": "partition_key"
    }]
    kinesis_client.put_records(StreamName=stream_name, Records=kinesis_record)
    print("Sent record to Kinesis.", kinesis_record)


def main():
    kinesis_stream_name = os.environ["AWS_KINESIS_STREAM_NAME"]
    kinesis_client = boto3.client("kinesis",
                                  region_name=os.environ['AWS_REGION'])

    data_generator = DataGenerator()

    create_kinesis_stream(kinesis_client, kinesis_stream_name)

    EVENTS_PER_SECOND = 5
    schedule.every(float(1 / EVENTS_PER_SECOND)).seconds.do(
        send_kinesis_record, kinesis_client, kinesis_stream_name,
        data_generator.generate_record)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    load_dotenv()
    main()
