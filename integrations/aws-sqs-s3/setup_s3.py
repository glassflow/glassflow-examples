import boto3
import os
from dotenv import load_dotenv


class S3Setup:
    def __init__(self, bucket_name, aws_region_name):
        self.bucket_name = bucket_name
        self.aws_region_name = aws_region_name

    def setup_bucket(self):
        # Create S3 client
        s3_client = boto3.client("s3", region_name=self.aws_region_name)

        # Create S3 bucket if not exists
        print(self.bucket_name)
        location = {"LocationConstraint": self.aws_region_name}
        s3_client.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration=location,
        )
        print("Bucket created successfully.")


if __name__ == "__main__":
    load_dotenv()
    bucket_name = os.environ["AWS_S3_BUCKET_NAME"]
    aws_region_name = os.environ["AWS_REGION"]

    s3_setup = S3Setup(bucket_name, aws_region_name)
    s3_setup.setup_bucket()
