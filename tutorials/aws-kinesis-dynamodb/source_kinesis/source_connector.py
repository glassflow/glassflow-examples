import boto3
import time
import json
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
from glassflow import GlassFlowClient


def get_kinesis_records():
    kinesis_stream_name = os.environ["AWS_KINESIS_STREAM_NAME"]
    aws_region = os.environ['AWS_REGION']
    kinesis_client = boto3.client("kinesis", region_name=aws_region)
    print("Kinesis client initialized.")
    stream_details = kinesis_client.describe_stream(
        StreamName=kinesis_stream_name)
    shard_id = stream_details["StreamDescription"]["Shards"][0]["ShardId"]

    shard_iterator = kinesis_client.get_shard_iterator(
        StreamName=kinesis_stream_name,
        ShardId=shard_id,
        ShardIteratorType="LATEST")["ShardIterator"]

    while True:
        try:
            print("Fetching records from Kinesis.")
            response = kinesis_client.get_records(ShardIterator=shard_iterator,
                                                  Limit=10)
            records = response["Records"]
            shard_iterator = response["NextShardIterator"]
            for record in records:
                data = json.loads(record["Data"].decode("utf-8"))
                print(data)
                yield data
            time.sleep(1)  # Polling interval
        except ClientError as e:
            print(f"Error fetching records from Kinesis: {e}")
            break


def main():

    pipeline_id = os.getenv("PIPELINE_ID")
    space_id = os.getenv("SPACE_ID")
    pipeline_access_token = os.getenv("PIPELINE_ACCESS_TOKEN")
    glassflow_client = GlassFlowClient().pipeline_client(
        space_id=space_id,
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token)

    for record in get_kinesis_records():
        response = glassflow_client.publish(request_body=record)
        if response.status_code == 200:
            print("Data sent successfully to GlassFlow")
        else:
            print(f"Failed to send data to GlassFlow: {response.text}")


if __name__ == "__main__":
    load_dotenv()
    main()
