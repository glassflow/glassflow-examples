# Integrating AWS SQS and S3 with GlassFlow

This example project demonstrates how to build an end-to-end serverless streaming data pipeline with AWS SQS and S3.

## Prerequisites

To run the sample pipeline, you'll need the following:

- [Docker](https://www.docker.com/get-started) is installed on your machine
- You created a [GlassFlow account](https://learn.glassflow.dev/docs/get-started/create-account#create-a-new-account), installed [GlassFlow CLI](https://learn.glassflow.dev/docs/get-started/glassflow-cli#installation), and logged into your account via the CLI.
- You have an [AWS account](https://portal.aws.amazon.com/).
- You installed [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

## Installation

1. Clone the `glassflow-examples` repository to your local machine:
    
    ```bash
    git clone https://github.com/glassflow/glassflow-examples.git
    ```
2. Navigate to the project directory:
    
    ```bash
    cd tutorials/aws-sqs-s3
    ```

3. (Optional) If you do not have existing services on AWS:
    - Run `python setup_s3.py` to set up an S3 bucket. You need to specify `AWS_S3_BUCKET_NAME` and `AWS_REGION`.
    - Run `python setup_sqs_queue.py` to create an SQS queue. You need to specify `AWS_SQS_QUEUE_NAME` and `AWS_REGION`. This scrip returns `AWS_SQS_QUEUE_URL` values in the console.

4. Read the following tutorial to learn how to run the GlassFlow and obtain `PIPELINE_ID`, `SPACE_ID` and `PIPELINE_ACCESS_TOKEN` values: [Integrating AWS SQS with GlassFlow](https://learn.glassflow.dev/docs/develop/tutorials/integrating-aws-sqs-with-glassflow)

5. Create a `.env` file in the same project directory and fill it with the following environment variables:

    ```
    AWS_ACCESS_KEY_ID=your_access_key_id
    AWS_SECRET_ACCESS_KEY=your_secret_access_key
    AWS_SQS_QUEUE_NAME=your_sqs_queue_name
    AWS_SQS_QUEUE_URL=your_sqs_queue_url
    AWS_S3_BUCKET_NAME=your_s3_bucket_name
    AWS_REGION=your_aws_region
    PIPELINE_ID=your_pipeline_id
    SPACE_ID=your_space_id
    PIPELINE_ACCESS_TOKEN=your_pipeline_access_token
    ```

5. Run the project with Docker Compose:
    
    ```bash
    docker compose up
    ```

## Environment Variables

Before running the project, ensure you have set the following environment variables:

| Variable Name           | Description                              |
|-------------------------|------------------------------------------|
| AWS_ACCESS_KEY_ID       | Your AWS access key ID                   |
| AWS_SECRET_ACCESS_KEY   | Your AWS secret access key               |
| AWS_SQS_QUEUE_NAME      | The name of your AWS SQS queue           |
| AWS_SQS_QUEUE_URL       | The URL of your AWS SQS queue            |
| AWS_S3_BUCKET_NAME      | The name of your AWS S3 bucket           |
| AWS_REGION              | The AWS region where your resources are located |
| PIPELINE_ID             | Your GlassFlow pipeline ID               |
| SPACE_ID                | Your GlassFlow space ID                  |
| PIPELINE_ACCESS_TOKEN   | Your GlassFlow pipeline access token     |
