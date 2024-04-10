import glassflow
import boto3
import sys
import time
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

pipeline_id = config.get("PIPELINE_ID")
space_id = config.get("SPACE_ID")
token = config.get("PIPELINE_ACCESS_TOKEN")
aws_account_id = None

try:
    # Create a new STS (Security Token Service) client
    sts_client = boto3.client('sts')
    
    # Call the get_caller_identity API to retrieve account information
    response = sts_client.get_caller_identity()
    
    # Extract and return the account ID from the response
    aws_account_id = response['Account']
    
except Exception as e:
    print(f"An error occurred while retrieving AWS account ID: {e}")

# Create S3 client
s3_client = boto3.client('s3')

# Define the name of your S3 bucket
bucket_name = 'netflix-metrics-result'

# Create S3 bucket if not exists
try:
    s3_client.head_bucket(Bucket=bucket_name)
    print("Bucket already exists.")
except s3_client.exceptions.ClientError as e:
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        print("Bucket does not exist. Creating...")
        s3_client.create_bucket(
            Bucket=bucket_name
        )
        print("Bucket created successfully.")
    else:
        print("An error occurred:", e)
        sys.exit(1)

# Create IAM client
iam_client = boto3.client('iam')

# Define IAM role name
role_name = 'firehose_delivery_role'

# Define IAM policy document
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"  # Replace with your S3 bucket ARN
        }
    ]
}

# Create IAM role if not exists
try:
    iam_client.get_role(RoleName=role_name)
    print("IAM role already exists.")
except iam_client.exceptions.NoSuchEntityException:
    print("IAM role does not exist. Creating...")
    response = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "firehose.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        })
    )
    print("IAM role created successfully.")

    # Attach IAM policy to role
    iam_client.put_role_policy(
        RoleName=role_name,
        PolicyName='firehose_delivery_policy',
        PolicyDocument=json.dumps(policy_document)
    )
    print("IAM policy attached to role.")
except Exception as e:
    print("An error occurred:", e)
    sys.exit(1)


# Create a Kinesis Firehose client
firehose_client = boto3.client('firehose')

# Define the name of your Firehose delivery stream
delivery_stream_name = 'netflix-view-metrics'

# Create Firehose delivery stream if not exists
try:
    firehose_client.describe_delivery_stream(DeliveryStreamName=delivery_stream_name)
    print("Delivery stream already exists.")
except firehose_client.exceptions.ResourceNotFoundException:
    print("Delivery stream does not exist. Creating...")
    firehose_client.create_delivery_stream(
        DeliveryStreamName=delivery_stream_name,
        S3DestinationConfiguration={
            'RoleARN': f'arn:aws:iam::{aws_account_id}:role/{role_name}',  # Use the created IAM role ARN
            'BucketARN': f'arn:aws:s3:::{bucket_name}',  # Use the created S3 bucket ARN
            'Prefix': 'firehose_data/'  # Prefix for S3 objects
        }
    )
    print("Delivery stream created successfully.")

# Create GlassFlow client
client = glassflow.GlassFlowClient()
pipeline_client = client.pipeline_client(space_id=space_id,
                                          pipeline_id=pipeline_id,
                                          pipeline_access_token=token)

# Main loop to consume data from GlassFlow and put it into Firehose
while True:
    try:
        print("Consuming data from GlassFlow pipeline...")
        res = pipeline_client.consume()
        if res.status_code == 204:
            print("Nothing to consume")
        if res.status_code == 200:
            # Get the transformed data as JSON
            record = res.body.event
            if record:
                print("Data consumed successfully")
                print(record)
                
                # Convert data to JSON format
                json_data = json.dumps(record)

                # Put record to Firehose delivery stream
                response = firehose_client.put_record(
                    DeliveryStreamName=delivery_stream_name,
                    Record={
                        'Data': json_data.encode('utf-8')
                    }
                )

                # Print the response
                print("Response:", response)
            else:
                print("Nothing to consume")
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit(0)
    time.sleep(0.5)
