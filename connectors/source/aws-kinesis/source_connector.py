import glassflow
import os
import boto3
import json
import time
from botocore.exceptions import ClientError
from dotenv import load_dotenv


class SourceConnectorKinesis:

    def __init__(self) -> None:
        self.kinesis_stream_name = os.environ["AWS_KINESIS_STREAM_NAME"]
        aws_region = os.environ['AWS_REGION']
        self.kinesis_client = boto3.client("kinesis", region_name=aws_region)
        self.shard_iterator = None

    def setup(self):
        stream_details = self.kinesis_client.describe_stream(
            StreamName=self.kinesis_stream_name)
        shard_id = stream_details["StreamDescription"]["Shards"][0]["ShardId"]

        self.shard_iterator = self.kinesis_client.get_shard_iterator(
            StreamName=self.kinesis_stream_name,
            ShardId=shard_id,
            ShardIteratorType="LATEST")["ShardIterator"]

    def get_next(self):
        while True:
            try:
                print("Fetching records from Kinesis.")
                response = self.kinesis_client.get_records(
                    ShardIterator=self.shard_iterator, Limit=10)
                records = response["Records"]
                self.shard_iterator = response["NextShardIterator"]
                for record in records:
                    data = json.loads(record["Data"].decode("utf-8"))
                    print(data)
                    yield data
                time.sleep(1)  # Polling interval
            except ClientError as e:
                print(f"Error fetching records from Kinesis: {e}")
                break
            except KeyboardInterrupt:
                self.cleanup()
                break

    def cleanup(self):
        pass


def main():
    # Initalize the glassflow client
    pipeline_id = os.environ["PIPELINE_ID"]
    space_id = os.environ["SPACE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]
    glassflow_client = glassflow.GlassFlowClient().pipeline_client(
        space_id=space_id,
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token)

    # Initialize the SQS client
    source_connector = SourceConnectorKinesis()
    source_connector.setup()

    for message in source_connector.get_next():
        response = glassflow_client.publish(request_body=message)
        if response.status_code == 200:
            print("Data sent successfully to GlassFlow")
        else:
            print(f"Failed to send data to GlassFlow: {response.text}")


if __name__ == "__main__":
    load_dotenv()
    main()
