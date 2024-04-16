import boto3
from glassflow import GlassFlowClient
from dotenv import load_dotenv
import os
import time
import json
import uuid
import random


def table_exists(ddb_client, table_name):
    """
    Check if DynamoDB table exists.
    """
    existing_tables = ddb_client.list_tables()["TableNames"]
    return table_name in existing_tables


def create_dynamodb_table(ddb_client, ddb_table_name):
    """
    Create DynamoDB table.
    """
    try:
        ddb_table = ddb_client.create_table(
            TableName=ddb_table_name,
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
        print("DynamoDB table created successfully:", ddb_table_name)
        return ddb_table
    except Exception as e:
        print("Failed to create DynamoDB table:", e)
        raise e


def setup_data_sink():
    aws_region_name = os.environ['AWS_REGION']
    ddb_client = boto3.client("dynamodb", region_name=aws_region_name)
    ddb_table_name = os.getenv("AWS_DYNAMODB_TABLE_NAME")
    # Create DynamoDB table if it doesn't exist
    if not table_exists(ddb_client, ddb_table_name):
        print("Creating DynamoDB table:", ddb_table_name)
        ddb_table = create_dynamodb_table(ddb_client, ddb_table_name)
        time.sleep(30)  # Wait for table to be created
    else:
        print("DynamoDB table already exists:", ddb_table_name)

    return ddb_client, ddb_table_name


def write_to_dynamodb(ddb_client, ddb_table_name, record):
    """
    Write record to DynamoDB.
    """
    try:
        # Serialize the record dictionary into a JSON string
        record_json = json.dumps(record)
        record_id = str(uuid.uuid4())
        ddb_client.put_item(TableName=ddb_table_name,
                            Item={
                                "id": {
                                    "S": record_id
                                },
                                "data": {
                                    "S": record_json
                                }
                            })
        print("Record written to DynamoDB:", record)
    except Exception as e:
        print("Failed to write record to DynamoDB:", e)


def get_glassflow_data():
    pipeline_id = os.getenv("PIPELINE_ID")
    space_id = os.getenv("SPACE_ID")
    pipeline_access_token = os.getenv("PIPELINE_ACCESS_TOKEN")

    glassflow_client = GlassFlowClient().pipeline_client(
        space_id=space_id,
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token)
    retry_delay = 10
    while True:
        try:
            res = glassflow_client.consume()
            if res.status_code == 204:
                # No new events. sleep for a little bit
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the delay for the next attempt
                retry_delay += random.uniform(0, 1)  # Add jitter
                continue
            if res.status_code == 200:
                record = res.json()
                yield record
                # set the retry delay back to original
                retry_delay = 10
        except Exception as e:
            print(f"An error occurred: {e}")
            continue


def main():
    ddb_client, ddb_table_name = setup_data_sink()
    for record in get_glassflow_data():
        write_to_dynamodb(ddb_client, ddb_table_name, record)


if __name__ == "__main__":
    load_dotenv()
    main()
