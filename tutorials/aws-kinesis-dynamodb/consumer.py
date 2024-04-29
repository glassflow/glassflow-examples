import boto3
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
ddb_table_name = os.getenv("AWS_DYNAMODB_TABLE_NAME")
region = os.getenv("AWS_REGION")

# Initialize DynamoDB client
ddb = boto3.client("dynamodb", region_name=region)

def read_from_dynamodb():
    """
    Read records from DynamoDB and print them.
    """
    try:
        response = ddb.scan(
            TableName=ddb_table_name
        )
        items = response.get("Items", [])
        for item in items:
            # Decode the record JSON string and print it
            record_json = item.get("data", {}).get("S")
            if record_json:
                record = json.loads(record_json)
                print(record)
    except Exception as e:
        print("Failed to read records from DynamoDB:", e)

if __name__ == "__main__":
    print("Reading records from DynamoDB...")
    read_from_dynamodb()
