import glassflow
import boto3
import sys
import time
import json
import os
import uuid
from dotenv import load_dotenv
import random


class SinkConnectorDynamoDB():

    def __init__(self) -> None:
        aws_region_name = os.environ['AWS_REGION']
        self.ddb_client = boto3.client("dynamodb", region_name=aws_region_name)
        self.ddb_table_name = os.getenv("AWS_DYNAMODB_TABLE_NAME")

    def setup(self):
        if not self._table_exists():
            print("Creating DynamoDB table:", self.ddb_table_name)
            ddb_table = self._create_dynamodb_table()
            time.sleep(30)  # Wait for table to be created
        else:
            print("DynamoDB table already exists:", self.ddb_table_name)

    def _table_exists(self):
        """
        Check if DynamoDB table exists.
        """
        existing_tables = self.ddb_client.list_tables()["TableNames"]
        return self.ddb_table_name in existing_tables

    def _create_dynamodb_table(self):
        """
        Create DynamoDB table.
        """
        try:
            ddb_table = self.ddb_client.create_table(
                TableName=self.ddb_table_name,
                KeySchema=[
                    {
                        "AttributeName": "id",
                        "KeyType": "HASH"
                    },  # Partition key
                ],
                AttributeDefinitions=[
                    {
                        "AttributeName": "id",
                        "AttributeType": "S"
                    },
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                })
            print("DynamoDB table created successfully:", self.ddb_table_name)
            return ddb_table
        except Exception as e:
            print("Failed to create DynamoDB table:", e)
            raise e

    def put(self, data):
        try:
            record_json = json.dumps(data)
            record_id = str(uuid.uuid4())
            self.ddb_client.put_item(TableName=self.ddb_table_name,
                                     Item={
                                         "id": {
                                             "S": record_id
                                         },
                                         "data": {
                                             "S": record_json
                                         }
                                     })
            print("Record written to DynamoDB:", data)
        except Exception as e:
            print("Failed to write record to DynamoDB:", e)

    def cleanup(self):
        pass


def main():
    sink_connector = SinkConnectorDynamoDB()
    sink_connector.setup()

    pipeline_id = os.environ["PIPELINE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]

    # Create GlassFlow client
    pipeline_client = glassflow.GlassFlowClient().pipeline_client(
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token)

    retry_delay = 10
    while True:
        try:
            res = pipeline_client.consume()
            if res.status_code == 204:
                # No new events. sleep for a little bit
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the delay for the next attempt
                retry_delay += random.uniform(0, 1)  # Add jitter
                continue
            if res.status_code == 200:
                record = res.json()
                sink_connector.put(record)
                print(
                    "Consumed transformed event from Glassflow and sent to DynamoDB"
                )
                # set the retry delay back to original
                retry_delay = 10
        except KeyboardInterrupt:
            print("Exiting")
            sink_connector.cleanup()
            break


if __name__ == "__main__":
    load_dotenv()
    main()
