import boto3
from glassflow import GlassFlowClient
from dotenv import load_dotenv
import os
import time
import json
import uuid

# Load environment variables
load_dotenv()
ddb_table_name = os.getenv("DYNAMODB_TABLE_NAME")
region = os.getenv("REGION")
pipeline_id = os.getenv("PIPELINE_ID")
space_id = os.getenv("SPACE_ID")
token = os.getenv("PIPELINE_ACCESS_TOKEN")

# Initialize GlassFlow client
glassflow_client = GlassFlowClient().pipeline_client(
    space_id=space_id, pipeline_id=pipeline_id, pipeline_access_token=token
)

# Initialize DynamoDB client
ddb = boto3.client("dynamodb", region_name=region)

def create_dynamodb_table():
    """
    Create DynamoDB table.
    """
    try:
        ddb_table = ddb.create_table(
            TableName=ddb_table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},  # Partition key
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            }
        )
        print("DynamoDB table created successfully:", ddb_table_name)
        return ddb_table
    except Exception as e:
        print("Failed to create DynamoDB table:", e)

def table_exists(table_name):
    """
    Check if DynamoDB table exists.
    """
    existing_tables = ddb.list_tables()["TableNames"]
    return table_name in existing_tables

def write_to_dynamodb(record):
    """
    Write record to DynamoDB.
    """
    try:
        # Serialize the record dictionary into a JSON string
        record_json = json.dumps(record)
        record_id = str(uuid.uuid4())
        ddb.put_item(
            TableName=ddb_table_name,
            Item={"id": {"S": record_id}, "data": {"S": record_json}}
        )
        print("Record written to DynamoDB:", record)
    except Exception as e:
        print("Failed to write record to DynamoDB:", e)

def main():
    # Create DynamoDB table if it doesn't exist
    if not table_exists(ddb_table_name):
        ddb_table = create_dynamodb_table()

    try:
        while True:
            response = glassflow_client.consume()
            if response.status_code == 200:
                print("Consuming data from GlassFlow pipeline...")
                # Extract the transformed record from the response
                record = response.body.event
                print(record)

                # Write the record to DynamoDB
                write_to_dynamodb(record)
            if response.status_code == 204:
                print("Nothing to consume")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
        return

if __name__ == "__main__":
    main()
