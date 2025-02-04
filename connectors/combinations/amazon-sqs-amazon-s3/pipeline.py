import glassflow
personal_access_token = ""

# AMAZON SQS PARAMETERS
AMAZON_SQS_QUEUE_URL = "" # The URL of the SQS queue where the events will be published
AMAZON_SQS_AWS_REGION = "" # The AWS region where your SQS queue is located
AMAZON_SQS_AWS_ACCESS_KEY = "" # AWS access key ID with access to the SQS queue
AMAZON_SQS_AWS_SECRET_KEY = "" # AWS secret key

# AMAZON S3 PARAMETERS
AMAZON_S3_BUCKET = "" # s3 bucket name
AMAZON_S3_KEY = "" # s3 key where to sink the data into
AMAZON_S3_AWS_REGION = "" # aws region
AMAZON_S3_AWS_ACCESS_KEY = "" # AWS access key ID with access to the S3 bucket
AMAZON_S3_AWS_SECRET_KEY = "" # AWS secret key

client = glassflow.GlassFlowClient(
    personal_access_token=personal_access_token
)

# create a space to put the pipeline 
space = client.create_space(name="amazon-sqs-pipelines")
space_id = space.id
pipeline_name = "amazon-sqs-to-amazon-s3"
transformation_file = "transform.py" # location of the file where the transformation code is 

pipeline = client.create_pipeline(
    name=pipeline_name, 
    transformation_file=transformation_file,
    space_id=space_id, 
    source_kind="amazon_sqs",
    source_config={
        "queue_url": AMAZON_SQS_QUEUE_URL,
        "aws_region": AMAZON_SQS_AWS_REGION,
        "aws_access_key": AMAZON_SQS_AWS_ACCESS_KEY,
        "aws_secret_key": AMAZON_SQS_AWS_SECRET_KEY
    },
    sink_kind="amazon_s3",
    sink_config={
        "s3_bucket": AMAZON_S3_BUCKET,
        "s3_key": AMAZON_S3_KEY,
        "aws_region": AMAZON_S3_AWS_REGION,
        "aws_access_key": AMAZON_S3_AWS_ACCESS_KEY,
        "aws_secret_key": AMAZON_S3_AWS_SECRET_KEY
}
)
print("Pipeline ID:", pipeline.id)
print("Explore your pipeline on the web UI at", "https://app.glassflow.dev/pipelines/{}/logs".format(pipeline.id))
