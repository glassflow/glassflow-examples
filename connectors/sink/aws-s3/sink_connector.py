import glassflow
import boto3
import sys
import time
import json
import os
import uuid
from dotenv import load_dotenv
import random


class SinkConnectorS3:
    def __init__(self) -> None:
        self.bucket_name = os.environ["AWS_S3_BUCKET_NAME"]
        self.aws_region_name = os.environ["AWS_REGION"]
        self.firehose_uid = uuid.uuid4().hex[0:4]
        self.role_name = "firehose_delivery_role_%s" % self.firehose_uid
        self.firehose_delivery_stream_name = "glassflow-pipeline-%s" % self.firehose_uid
        self.aws_account_id = self._get_aws_account_id()
        self.firehose_client = boto3.client(
            "firehose", region_name=self.aws_region_name
        )

    def setup(self):
        if not self._check_firehose_stream():
            self._setup_iam_firehose_role()
            time.sleep(30)
            # waiting for role to be created before setting up firehose
            self._setup_aws_firehose()

        if not self._check_firehose_stream():
            print("Delivery stream still not exist. Exiting...")
            sys.exit(1)

        # Sleep for 30 seconds to allow the delivery stream to be created
        time.sleep(30)

    def _get_aws_account_id(self):
        try:
            # Create a new STS (Security Token Service) client
            sts_client = boto3.client("sts", region_name=self.aws_region_name)

            # Call the get_caller_identity API to retrieve account information
            response = sts_client.get_caller_identity()

            # Extract and return the account ID from the response
            aws_account_id = response["Account"]
            return aws_account_id
        except Exception as e:
            print(f"An error occurred while retrieving AWS account ID: {e}")

    def _setup_iam_firehose_role(self):
        # Create IAM client
        iam_client = boto3.client("iam")
        # Define IAM policy document
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:PutObject",
                    "Resource": f"arn:aws:s3:::{self.bucket_name}/*",
                }
            ],
        }
        # Create IAM role if not exists
        try:
            iam_client.get_role(RoleName=self.role_name)
            print("IAM role already exists.")
        except iam_client.exceptions.NoSuchEntityException:
            print("IAM role does not exist. Creating...")
            response = iam_client.create_role(
                RoleName=self.role_name,
                AssumeRolePolicyDocument=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"Service": "firehose.amazonaws.com"},
                                "Action": "sts:AssumeRole",
                            }
                        ],
                    }
                ),
            )
            print("IAM role created successfully.")

            # Attach IAM policy to role
            iam_client.put_role_policy(
                RoleName=self.role_name,
                PolicyName="firehose_delivery_policy",
                PolicyDocument=json.dumps(policy_document),
            )
            print("IAM policy attached to role.")
        except Exception as e:
            print("An error occurred:", e)
            sys.exit(1)

    def _check_firehose_stream(self):
        try:
            stream = self.firehose_client.describe_delivery_stream(
                DeliveryStreamName=self.firehose_delivery_stream_name
            )
            return True
        except self.firehose_client.exceptions.ResourceNotFoundException:
            return False

    def _setup_aws_firehose(self):
        # Create a Kinesis Firehose client
        firehose_client = boto3.client("firehose", region_name=self.aws_region_name)

        # Create Firehose delivery stream if not exists
        try:
            firehose_client.create_delivery_stream(
                DeliveryStreamName=self.firehose_delivery_stream_name,
                ExtendedS3DestinationConfiguration={
                    "RoleARN": f"arn:aws:iam::{self.aws_account_id}:role/{self.role_name}",  # Use the created IAM role ARN
                    "BucketARN": f"arn:aws:s3:::{self.bucket_name}",  # Use the created S3 bucket ARN
                    "Prefix": "glassflow_transforms/",  # Prefix for S3 objects
                    "ProcessingConfiguration": {
                        "Enabled": True,
                        "Processors": [
                            {
                                "Type": "AppendDelimiterToRecord",
                                "Parameters": [
                                    {
                                        "ParameterName": "Delimiter",
                                        "ParameterValue": "\\n",
                                    }
                                ],
                            }
                        ],
                    },
                },
            )
            print(
                f"Delivery stream: {self.firehose_delivery_stream_name} created successfully."
            )
        except Exception as e:
            print("An error occurred when creating stream:", e)
            sys.exit(1)

    def put(self, data):
        try:
            json_data = json.dumps(data)

            # Put record to Firehose delivery stream
            response = self.firehose_client.put_record(
                DeliveryStreamName=self.firehose_delivery_stream_name,
                Record={"Data": json_data.encode("utf-8")},
            )
            print(response)
        except Exception as e:
            print("An error occurred when putting record to Firehose:", e)
            # TODO decide what to do in case of error

    def cleanup(self):
        self.file.close()


def main():
    sink_connector = SinkConnectorS3()
    sink_connector.setup()

    pipeline_id = os.environ["PIPELINE_ID"]
    pipeline_access_token = os.environ["PIPELINE_ACCESS_TOKEN"]

    # Create GlassFlow client
    pipeline_client = glassflow.GlassFlowClient().pipeline_client(
        pipeline_id=pipeline_id,
        pipeline_access_token=pipeline_access_token,
    )

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
                    "Consumed transformed event from GlassFlow and sent to S3 via Firehose"
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
