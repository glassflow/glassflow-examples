import boto3
import time
import json
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
from glassflow import GlassFlowClient

# Load environment variables
load_dotenv()
stream_name = os.getenv("KINESIS_STREAM_NAME")
region = os.getenv("REGION")
pipeline_id = os.getenv("PIPELINE_ID")
space_id = os.getenv("SPACE_ID")
token = os.getenv("PIPELINE_ACCESS_TOKEN")

# Initialize AWS Kinesis and GlassFlow clients
kinesis_client = boto3.client("kinesis", region)
glassflow_client = GlassFlowClient().pipeline_client(
    space_id=space_id, pipeline_id=pipeline_id, pipeline_access_token=token
)


def get_stream_details(stream_name):
    try:
        response = kinesis_client.describe_stream(StreamName=stream_name)
        return response["StreamDescription"]
    except ClientError as e:
        print(f"Failed to describe Kinesis stream: {e}")
        raise


def get_records(stream_name):
    stream_details = get_stream_details(stream_name)
    shard_id = stream_details["Shards"][0]["ShardId"]
    shard_iterator = kinesis_client.get_shard_iterator(
        StreamName=stream_name, ShardId=shard_id, ShardIteratorType="LATEST"
    )["ShardIterator"]

    while True:
        try:
            response = kinesis_client.get_records(
                ShardIterator=shard_iterator, Limit=10
            )
            records = response["Records"]
            shard_iterator = response["NextShardIterator"]
            if records:
                print(f"Retrieved {len(records)} records from Kinesis.")
                yield records
            time.sleep(1)  # Polling interval
        except ClientError as e:
            print(f"Error fetching records from Kinesis: {e}")
            break


def push_data_to_glassflow(records):
    for record in records:
        try:
            data_json = json.loads(record["Data"].decode("utf-8"))
            print(data_json)
            glassflow_client.publish(request_body=data_json)
            print("Record pushed to GlassFlow.")
        except Exception as e:
            print(f"Failed to push data to GlassFlow: {e}")


if __name__ == "__main__":
    try:
        for records_batch in get_records(stream_name):
            push_data_to_glassflow(records_batch)
    except KeyboardInterrupt:
        print("Process interrupted by user.")
