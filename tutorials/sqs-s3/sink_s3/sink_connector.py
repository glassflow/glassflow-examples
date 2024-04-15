import glassflow
import boto3
import sys
import time
import json
import os
import uuid
from dotenv import load_dotenv


def get_aws_account_id(aws_region_name):
    try:
        # Create a new STS (Security Token Service) client
        sts_client = boto3.client("sts", region_name=aws_region_name)

        # Call the get_caller_identity API to retrieve account information
        response = sts_client.get_caller_identity()

        # Extract and return the account ID from the response
        aws_account_id = response["Account"]
        return aws_account_id
    except Exception as e:
        print(f"An error occurred while retrieving AWS account ID: {e}")


def setup_s3_bucket(bucket_name, aws_region_name):
    # Create S3 client
    s3_client = boto3.client("s3", region_name=aws_region_name)

    # Create S3 bucket if not exists
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists.")
    except s3_client.exceptions.ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            print("Bucket does not exist. Creating...")
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': aws_region_name
                },
            )
            print("Bucket created successfully.")
        else:
            print("An error occurred:", e)
            sys.exit(1)


def setup_iam_firehose_role(bucket_name, role_name):
    # Create IAM client
    iam_client = boto3.client("iam")
    # Define IAM policy document
    policy_document = {
        "Version":
        "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }]
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
                "Version":
                "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "firehose.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }]
            }),
        )
        print("IAM role created successfully.")

        # Attach IAM policy to role
        iam_client.put_role_policy(
            RoleName=role_name,
            PolicyName="firehose_delivery_policy",
            PolicyDocument=json.dumps(policy_document),
        )
        print("IAM policy attached to role.")
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)


def setup_aws_firehose(aws_account_id, role_name, bucket_name, aws_region_name,
                       firehose_delivery_stream_name):

    # Create a Kinesis Firehose client
    firehose_client = boto3.client("firehose", region_name=aws_region_name)

    # Create Firehose delivery stream if not exists
    try:
        firehose_client.create_delivery_stream(
            DeliveryStreamName=firehose_delivery_stream_name,
            ExtendedS3DestinationConfiguration={
                "RoleARN":
                f"arn:aws:iam::{aws_account_id}:role/{role_name}",  # Use the created IAM role ARN
                "BucketARN":
                f"arn:aws:s3:::{bucket_name}",  # Use the created S3 bucket ARN
                "Prefix": "glassflow_transforms/",  # Prefix for S3 objects
                "ProcessingConfiguration": {
                    "Enabled":
                    True,
                    "Processors": [{
                        "Type":
                        "AppendDelimiterToRecord",
                        "Parameters": [{
                            "ParameterName": "Delimiter",
                            "ParameterValue": "\\n"
                        }]
                    }]
                },
            },
        )
        print(
            f"Delivery stream: {firehose_delivery_stream_name} created successfully."
        )
    except Exception as e:
        print("An error occurred when creating stream:", e)
        sys.exit(1)


def check_firehose_stream(aws_region_name, firehose_delivery_stream_name):
    firehose_client = boto3.client("firehose", region_name=aws_region_name)
    try:
        stream = firehose_client.describe_delivery_stream(
            DeliveryStreamName=firehose_delivery_stream_name)
        return True
    except firehose_client.exceptions.ResourceNotFoundException:
        return False


def main():
    aws_region_name = os.environ['AWS_REGION']
    pipeline_id = os.environ["PIPELINE_ID"]
    space_id = os.environ["SPACE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]

    # Define the name of your S3 bucket
    bucket_name = os.environ["AWS_S3_BUCKET_NAME"]
    setup_s3_bucket(bucket_name, aws_region_name)

    firehose_uid = uuid.uuid4().hex[0:4]
    role_name = "firehose_delivery_role_%s" % firehose_uid
    firehose_delivery_stream_name = "glassflow-pipeline-%s" % firehose_uid
    print("bucket_name", bucket_name)
    print("firehose_delivery_stream_name", firehose_delivery_stream_name)
    if not check_firehose_stream(aws_region_name,
                                 firehose_delivery_stream_name):
        setup_iam_firehose_role(bucket_name, role_name)
        time.sleep(30)
        # waiting for role to be created before setting up firehose
        setup_aws_firehose(get_aws_account_id(aws_region_name), role_name,
                           bucket_name, aws_region_name,
                           firehose_delivery_stream_name)

    if not check_firehose_stream(aws_region_name,
                                 firehose_delivery_stream_name):
        print("Delivery stream still not exist. Exiting...")
        sys.exit(1)

    # Sleep for 30 seconds to allow the delivery stream to be created
    time.sleep(30)

    firehose_client = boto3.client("firehose", region_name=aws_region_name)
    # Create GlassFlow client
    pipeline_client = glassflow.GlassFlowClient().pipeline_client(
        space_id=space_id,
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token)

    while True:
        try:
            res = pipeline_client.consume()
            if res.status_code == 204:
                continue
            if res.status_code == 200:
                record = res.json()
                event_id = record.get("event_id")
                json_data = json.dumps(record)
                # Put record to Firehose delivery stream
                response = firehose_client.put_record(
                    DeliveryStreamName=firehose_delivery_stream_name,
                    Record={"Data": json_data.encode("utf-8")},
                )
                print(response)
                # Print the response
                print(
                    f"Consumed transformed event from glassflow with event_id {event_id} and sent to s3 via Firehose"
                )
        except firehose_client.exceptions.ResourceNotFoundException:
            print("Delivery stream does not exist. Exiting...")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("Exiting")
            sys.exit(0)


if __name__ == "__main__":
    main()
